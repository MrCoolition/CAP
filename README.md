# CAP - Capture Application

A Streamlit application for capturing images and extracting actionable knowledge using OpenAI vision models.

## Features
- **Image Capture**: Use camera input to take pictures of whiteboards, notebooks or any other source.
- **OCR & GPT Vision**: Extract text from handwriting and typed content. Convert diagrams to Markdown.
- **Summaries & Next Actions**: Summarize the captured content and suggest next steps.
- **PostgreSQL Storage**: All data is stored in a dedicated schema.

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app locally:
```bash
streamlit run app/main.py
```

The database schema can be initialized using the SQL in `sql/schema.sql`.

Configuration values are loaded exclusively from `st.secrets`.
Place your PostgreSQL connection string in `DATABASE_URL` under the
`[database]` section and store the OpenAI key as `BOOF_API_KEY` in the same
section. No environment variable lookup is performed by the app.

