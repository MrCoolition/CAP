import io
import base64
import logging
import streamlit as st
import psycopg2
from openai import OpenAI
from PIL import Image
import pytesseract

BOOF_API_KEY = st.secrets["database"]["BOOF_API_KEY"]
client = OpenAI(api_key=BOOF_API_KEY)

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


def ocr_image(image_bytes):
    logger.debug("Running OCR on captured image")
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)


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
    logger.info("Starting Capture Application")
    st.title("Capture Application")


    user_id = "anon"
    logger.info("User ID: %s", user_id)
    conn = connect_db()

    picture = st.camera_input("Take a picture")
    if picture:
        logger.info("Image captured")
        image_bytes = picture.getvalue()
        image_id = save_image(conn, user_id, image_bytes)

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
