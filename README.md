# CAP - Capture Application

A Streamlit application for capturing images and extracting actionable knowledge using OpenAI vision models.

## Features
- **Image Capture**: Upload or capture photos using Streamlit's file uploader.
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

If your browser does not support camera access you can still upload an image
when running the app. Open `http://localhost:8501` in any modern browser to
capture or upload a photo.

The database schema can be initialized using the SQL in `sql/schema.sql`.

Configuration values are loaded exclusively from `st.secrets`.
Provide the database credentials under the `[database]` section using
`AIVEN_HOST`, `AIVEN_PORT`, `AIVEN_DB`, `AIVEN_USER`, and `AIVEN_PASSWORD`.
Store the OpenAI key as `BOOF_API_KEY` in the same section and optionally
include `MISTRAL_API_KEY` for the Mistral OCR service. No environment
variable lookup is performed by the app.

Recent versions of Streamlit deprecated the ``use_column_width`` argument
used by ``st.image``. The application now relies on ``use_container_width``
instead. If you see a deprecation warning, update the app to the latest
code and ensure your Streamlit package is up to date.


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

If you encounter `ModuleNotFoundError` when starting the app, double-check that
all dependencies listed in `requirements.txt` are installed. Streamlit
Community Cloud automatically installs these packages when the app is deployed,
so updating the file and re-deploying is usually sufficient. Locally you can
run `pip install -r requirements.txt` to replicate the same environment. The
error typically appears when ``streamlit`` is missing from the Python
environment.

If the app displays a message beginning with `Mistral OCR unavailable` it means
the Mistral service failed or is not configured. The warning now includes the
underlying error when available. Provide a valid `MISTRAL_API_KEY` in
`st.secrets` to enable the dedicated OCR service. Check the terminal output for
log messages starting with `Mistral OCR failed` or `Mistral OCR not configured`
to determine whether the API key is missing or the remote service is
unreachable.
