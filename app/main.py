import os
import io
import base64
import streamlit as st
import psycopg2
from openai import OpenAI
from PIL import Image
import pytesseract

from auth import authenticate

# Initialize the OpenAI client using the BOOF_API_KEY environment variable
# if available. Fallback to the standard OPENAI_API_KEY so the application
# remains compatible with setups that already use that name.
API_KEY = os.getenv("BOOF_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None
DB_URL = os.getenv("DATABASE_URL")


def connect_db():
    return psycopg2.connect(DB_URL)


def save_image(conn, user_id, image_bytes):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO cap.images (user_id, image) VALUES (%s, %s) RETURNING id", (user_id, image_bytes))
        image_id = cur.fetchone()[0]
        conn.commit()
        return image_id


def save_text(conn, image_id, content):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO cap.texts (image_id, content) VALUES (%s, %s)", (image_id, content))
        conn.commit()


def save_diagram(conn, image_id, markdown):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO cap.diagrams (image_id, markdown) VALUES (%s, %s)", (image_id, markdown))
        conn.commit()


def save_summary(conn, image_id, summary, actions):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO cap.summaries (image_id, summary, next_actions) VALUES (%s, %s, %s)",
            (image_id, summary, actions),
        )
        conn.commit()


def ocr_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)


def gpt_vision(image_bytes, prompt, model="gpt-4o"):
    """Query the OpenAI vision model with ``image_bytes`` and ``prompt``."""

    if client is None:
        return ""

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

    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content


def main():
    st.title("Capture Application")
    if not authenticate():
        st.stop()

    if client is None:
        st.error("OpenAI API key not configured")
        st.stop()

    user_id = st.session_state.get("token", {}).get("sub", "anon")
    conn = connect_db()

    picture = st.camera_input("Take a picture")
    if picture:
        image_bytes = picture.getvalue()
        image_id = save_image(conn, user_id, image_bytes)

        with st.spinner("Processing image..."):
            text = ocr_image(image_bytes)
            save_text(conn, image_id, text)

            diagram_md = gpt_vision(image_bytes, "Convert any diagrams to Markdown")
            save_diagram(conn, image_id, diagram_md)

            summary = gpt_vision(image_bytes, "Summarize and organize the content")
            actions = gpt_vision(image_bytes, "Generate a list of next actions from the content")
            save_summary(conn, image_id, summary, actions)

        st.success("Image processed and data saved")
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
