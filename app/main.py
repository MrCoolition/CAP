import os
import io
import streamlit as st
import psycopg2
import openai
from PIL import Image
import pytesseract

from auth import authenticate

openai.api_key = os.getenv("OPENAI_API_KEY")
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


def gpt_vision(image_bytes, prompt):
    if not openai.api_key:
        return ""
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "image": image_bytes}]},
        ],
    )
    return response.choices[0].message.content


def main():
    st.title("Capture Application")
    if not authenticate():
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
