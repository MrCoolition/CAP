from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

app = FastAPI()

_pool: SimpleConnectionPool | None = None


def _get_pool() -> SimpleConnectionPool:
    global _pool
    if _pool is None:
        _pool = SimpleConnectionPool(
            1,
            int(os.environ.get("DB_POOL_SIZE", 5)),
            host=os.environ.get("AIVEN_HOST"),
            port=os.environ.get("AIVEN_PORT"),
            dbname=os.environ.get("AIVEN_DB"),
            user=os.environ.get("AIVEN_USER"),
            password=os.environ.get("AIVEN_PASSWORD"),
            sslmode="require",
        )
    return _pool


def get_conn():
    return _get_pool().getconn()


def put_conn(conn) -> None:
    _get_pool().putconn(conn)


@app.on_event("shutdown")
def close_pool() -> None:
    if _pool is not None:
        _pool.closeall()


def run_query(query, params=None, fetch=True):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall() if fetch else []
            conn.commit()
        return rows
    finally:
        put_conn(conn)


class ImageCreate(BaseModel):
    user_id: str
    image: str  # base64 encoded


@app.post("/images")
def create_image(image: ImageCreate):
    data = base64.b64decode(image.image)
    rows = run_query(
        "INSERT INTO cap.images (user_id, image) VALUES (%s, %s) RETURNING id",
        [image.user_id, psycopg2.Binary(data)],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to store image")
    return {"id": rows[0]["id"]}


@app.get("/images/{image_id}")
def read_image(image_id: int):
    rows = run_query(
        "SELECT id, user_id, created_at, image FROM cap.images WHERE id = %s",
        [image_id],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Image not found")
    row = rows[0]
    encoded = base64.b64encode(row["image"]).decode()
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "created_at": row["created_at"],
        "image": encoded,
    }


class TextCreate(BaseModel):
    image_id: int
    content: str


@app.post("/texts")
def create_text(text: TextCreate):
    rows = run_query(
        "INSERT INTO cap.texts (image_id, content) VALUES (%s, %s) RETURNING id",
        [text.image_id, text.content],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to store text")
    return {"id": rows[0]["id"]}


@app.get("/texts/{image_id}")
def read_text(image_id: int):
    rows = run_query(
        "SELECT id, image_id, content FROM cap.texts WHERE image_id = %s ORDER BY id DESC LIMIT 1",
        [image_id],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Text not found")
    return rows[0]


class DiagramCreate(BaseModel):
    image_id: int
    markdown: str


@app.post("/diagrams")
def create_diagram(diagram: DiagramCreate):
    rows = run_query(
        "INSERT INTO cap.diagrams (image_id, markdown) VALUES (%s, %s) RETURNING id",
        [diagram.image_id, diagram.markdown],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to store diagram")
    return {"id": rows[0]["id"]}


@app.get("/diagrams/{image_id}")
def read_diagram(image_id: int):
    rows = run_query(
        "SELECT id, image_id, markdown FROM cap.diagrams WHERE image_id = %s ORDER BY id DESC LIMIT 1",
        [image_id],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Diagram not found")
    return rows[0]


class SummaryCreate(BaseModel):
    image_id: int
    summary: str
    next_actions: str


@app.post("/summaries")
def create_summary(summary: SummaryCreate):
    rows = run_query(
        "INSERT INTO cap.summaries (image_id, summary, next_actions) VALUES (%s, %s, %s) RETURNING id",
        [summary.image_id, summary.summary, summary.next_actions],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to store summary")
    return {"id": rows[0]["id"]}


@app.get("/summaries/{image_id}")
def read_summary(image_id: int):
    rows = run_query(
        "SELECT id, image_id, summary, next_actions FROM cap.summaries WHERE image_id = %s ORDER BY id DESC LIMIT 1",
        [image_id],
        fetch=True,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Summary not found")
    return rows[0]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
