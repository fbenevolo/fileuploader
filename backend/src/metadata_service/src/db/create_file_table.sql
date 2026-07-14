CREATE TABLE IF NOT EXISTS files (
    file_id TEXT PRIMARY KEY,
    original_name TEXT NOT NULL,
    stored_name TEXT NOT NULL,
    size INTEGER NOT NULL,
    created_at TEXT NOT NULL
);