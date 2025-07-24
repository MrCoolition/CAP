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

The OCR functionality uses the Tesseract engine if available.
On Ubuntu install it with:

```bash
sudo apt-get install tesseract-ocr
```

On Windows download it from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) and set the `TESSERACT_CMD` environment variable to the installed binary path if it's not in your `PATH`.

If you are deploying to an environment where system packages cannot be installed (e.g. Streamlit Community Cloud), include a PyPI package that bundles Tesseract in your `requirements.txt` or rely on the GPT Vision fallback built into the app. When Tesseract is placed in a custom location, set the `TESSERACT_CMD` variable so `pytesseract` can find it.

Run the app locally:
```bash
streamlit run app/main.py
```

If the browser does not prompt for camera access you can upload an image instead when running the app. Make sure to open `http://localhost:8501` in a browser that allows camera permissions.

The database schema can be initialized using the SQL in `sql/schema.sql`.

Configuration values are loaded exclusively from `st.secrets`.
Provide the database credentials under the `[database]` section using
`AIVEN_HOST`, `AIVEN_PORT`, `AIVEN_DB`, `AIVEN_USER`, and `AIVEN_PASSWORD`.
Store the OpenAI key as `BOOF_API_KEY` in the same section. No environment
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
