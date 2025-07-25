import io
import base64
import logging
try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise ImportError(
        "streamlit is required to run this app. "
        "Install dependencies using `pip install -r requirements.txt`."
    ) from exc
import psycopg2
from openai import OpenAI
import requests

BOOF_API_KEY = st.secrets["database"]["BOOF_API_KEY"]
client = OpenAI(api_key=BOOF_API_KEY)

MISTRAL_API_KEY = st.secrets["database"]["MISTRAL_API_KEY"]

# Individual database connection parameters
DB_HOST = st.secrets["database"]["AIVEN_HOST"]
DB_PORT = st.secrets["database"]["AIVEN_PORT"]
DB_NAME = st.secrets["database"]["AIVEN_DB"]
DB_USER = st.secrets["database"]["AIVEN_USER"]
DB_PASSWORD = st.secrets["database"]["AIVEN_PASSWORD"]

if not BOOF_API_KEY:
    st.error("BOOF_API_KEY not set.")
    st.stop()

if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    st.error("DB connection params incomplete.")
    st.stop()

log_level = st.secrets.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def connect_db():
    logger.info("Connecting to database")
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def save_image(conn, user_id, image_bytes):
    logger.info("Saving image for user %s", user_id)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO cap.images (user_id, image) VALUES (%s, %s) RETURNING id",
            (user_id, image_bytes),
        )
        image_id = cur.fetchone()[0]
        conn.commit()
        return image_id


def save_text(conn, image_id, content):
    logger.debug("Saving OCR text for image %s", image_id)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO cap.texts (image_id, content) VALUES (%s, %s)",
            (image_id, content),
        )
        conn.commit()


def save_diagram(conn, image_id, markdown):
    logger.debug("Saving diagram markdown for image %s", image_id)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO cap.diagrams (image_id, markdown) VALUES (%s, %s)",
            (image_id, markdown),
        )
        conn.commit()


def save_summary(conn, image_id, summary, actions):
    logger.debug("Saving summary for image %s", image_id)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO cap.summaries (image_id, summary, next_actions) VALUES (%s, %s, %s)",
            (image_id, summary, actions),
        )
        conn.commit()


def mistral_ocr(image_bytes):
    """Use the Mistral OCR service to extract text."""
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY not configured")

    logger.debug("Calling Mistral OCR service")
    b64 = base64.b64encode(image_bytes).decode()
    data_uri = f"data:image/png;base64,{b64}"
    payload = {
        "model": "mistral-ocr-latest",
        "document": {"type": "image_url", "image_url": data_uri},
    }
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        "https://api.mistral.ai/v1/ocr", json=payload, headers=headers, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    # Recent API versions return a list of pages with Markdown content instead of
    # a plain ``text`` field. Combine the Markdown from all pages to keep
    # backwards compatibility with older responses.
    if "pages" in data:
        markdown_parts = [p.get("markdown", "") for p in data.get("pages", [])]
        return "\n".join(filter(None, markdown_parts))
    return data.get("text", "")


def ocr_image(image_bytes):
    """Extract text using both Mistral OCR and GPT Vision."""
    logger.debug("Running OCR on captured image")

    text_mistral = ""
    error_msg = ""
    if MISTRAL_API_KEY:
        try:
            text_mistral = mistral_ocr(image_bytes).strip()
        except Exception as exc:
            error_msg = str(exc)
            logger.warning("Mistral OCR failed: %s", exc)
    else:
        error_msg = "MISTRAL_API_KEY missing"
        logger.warning("Mistral OCR not configured")

    if not text_mistral:
        msg = "Mistral OCR unavailable. Using GPT Vision only for text extraction."
        if error_msg:
            msg = (
                f"Mistral OCR unavailable ({error_msg}). Using GPT Vision only for text extraction."
            )
        st.warning(msg)

    text_gpt = gpt_vision(
        image_bytes, "Extract the text from this image as plain text"
    ).strip()

    if text_mistral and text_gpt and text_mistral != text_gpt:
        return text_mistral + "\n" + text_gpt
    return text_mistral or text_gpt


def gpt_vision(image_bytes, prompt, model="gpt-4o"):
    """Query the OpenAI vision model with ``image_bytes`` and ``prompt``."""

    b64 = base64.b64encode(image_bytes).decode()
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    logger.debug("Calling OpenAI vision model with prompt: %s", prompt)
    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content


def main():
    logger.info("Starting CAP")
    st.title("cap")


    user_id = "anon"
    logger.info("User ID: %s", user_id)
    conn = connect_db()

    picture = st.camera_input("Take a picture")
    if not picture:
        picture = st.file_uploader("Or upload an image", type=["png", "jpg", "jpeg"])

    if picture:
        logger.info("Image captured")
        image_bytes = picture.getvalue()
        image_id = save_image(conn, user_id, image_bytes)
        # ``use_column_width`` was deprecated in Streamlit 1.32. Replace with
        # the recommended ``use_container_width`` argument.
        st.image(
            image_bytes,
            caption="Captured image",
            use_container_width=True,
        )

        with st.spinner("Processing image..."):
            logger.info("Running OCR")
            text = ocr_image(image_bytes)
            save_text(conn, image_id, text)

            logger.info("Generating diagram markdown")
            diagram_md = gpt_vision(image_bytes, "Convert any diagrams to Markdown")
            save_diagram(conn, image_id, diagram_md)

            logger.info("Generating summary and next actions")
            summary = gpt_vision(image_bytes, "Summarize and organize the content")
            actions = gpt_vision(image_bytes, "Generate a list of next actions from the content")
            save_summary(conn, image_id, summary, actions)

        st.success("Image processed and data saved")
        logger.info("Image processing complete")
        st.subheader("Extracted Text")
        st.write(text)
        st.subheader("Diagram Markdown")
        st.markdown(diagram_md)
        st.subheader("Summary")
        st.write(summary)
        st.subheader("Next Actions")
        st.write(actions)


if __name__ == "__main__":
    main()
