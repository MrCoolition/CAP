CREATE SCHEMA IF NOT EXISTS cap;

CREATE TABLE IF NOT EXISTS cap.images (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    image BYTEA,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cap.texts (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES cap.images(id) ON DELETE CASCADE,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cap.diagrams (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES cap.images(id) ON DELETE CASCADE,
    markdown TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cap.summaries (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES cap.images(id) ON DELETE CASCADE,
    summary TEXT,
    next_actions TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
