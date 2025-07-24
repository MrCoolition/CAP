# CAP - Capture Application

A Streamlit application for capturing images and extracting actionable knowledge using OpenAI vision models.

## Features
- **Image Capture**: Use camera input to take pictures of whiteboards, notebooks or any other source.
- **Auth0 Authentication**: Users must authenticate via Auth0 before using the app.
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

Environment variables required:
- `OPENAI_API_KEY`
- `DATABASE_URL` (e.g. `postgresql://user:pass@localhost:5432/dbname`)

Auth0 credentials must be provided in `st.secrets` under an `auth0` section:

```toml
[auth0]
client_id = "..."
domain = "..."
```
