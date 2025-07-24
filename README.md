# CAP - Capture Application

A Streamlit application for capturing images and extracting actionable knowledge using OpenAI vision models.

## Features
- **Image Capture**: Use camera input to take pictures of whiteboards, notebooks or any other source.
- **Mistral OCR & GPT Vision**: Combine both services to extract text and convert diagrams to Markdown.
- **Summaries & Next Actions**: Summarize the captured content and suggest next steps.
- **PostgreSQL Storage**: All data is stored in a dedicated schema.

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

The app combines Mistral OCR with OpenAI's vision models. Provide a `MISTRAL_API_KEY`
in `st.secrets` to enable the Mistral service. GPT Vision is always used alongside
Mistral to refine the extracted text.

Run the app locally:
```bash
streamlit run app/main.py
```

If the browser does not prompt for camera access you can upload an image instead when running the app. Make sure to open `http://localhost:8501` in a browser that allows camera permissions.

The database schema can be initialized using the SQL in `sql/schema.sql`.

Configuration values are loaded exclusively from `st.secrets`.
Provide the database credentials under the `[database]` section using
`AIVEN_HOST`, `AIVEN_PORT`, `AIVEN_DB`, `AIVEN_USER`, and `AIVEN_PASSWORD`.
Store the OpenAI key as `BOOF_API_KEY` in the same section and optionally
include `MISTRAL_API_KEY` for the Mistral OCR service. No environment
variable lookup is performed by the app.


## API Service

A FastAPI application in `app/api.py` exposes CRUD endpoints for images,
extracted text, diagrams and summaries. Start the service with:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

The service uses the same database credentials as the Streamlit app, provided
via the environment variables `AIVEN_HOST`, `AIVEN_PORT`, `AIVEN_DB`,
`AIVEN_USER` and `AIVEN_PASSWORD`.

## Troubleshooting

If the app displays the message `Mistral OCR unavailable. Using GPT Vision only
for text extraction.` it means the Mistral service failed or is not configured.
Provide a valid `MISTRAL_API_KEY` in `st.secrets` to enable the dedicated OCR
service.
