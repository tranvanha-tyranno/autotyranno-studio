from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

from .config import settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    price REAL,
    currency TEXT DEFAULT 'VND',
    benefits_json TEXT DEFAULT '[]',
    image_path TEXT DEFAULT '',
    source_url TEXT DEFAULT '',
    affiliate_url TEXT DEFAULT '',
    sku TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT DEFAULT '',
    source_url TEXT NOT NULL,
    published_at TEXT,
    rights_status TEXT DEFAULT 'unknown',
    relevance_score REAL DEFAULT 0,
    status TEXT DEFAULT 'candidate',
    created_at TEXT NOT NULL,
    UNIQUE(source_url, title)
);
CREATE TABLE IF NOT EXISTS video_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idempotency_key TEXT NOT NULL UNIQUE,
    product_id INTEGER,
    trend_id INTEGER,
    template TEXT NOT NULL DEFAULT 'product_slideshow',
    status TEXT NOT NULL DEFAULT 'queued',
    script_json TEXT DEFAULT '{}',
    output_path TEXT DEFAULT '',
    poster_path TEXT DEFAULT '',
    error TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(trend_id) REFERENCES trends(id)
);
CREATE TABLE IF NOT EXISTS policy_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_job_id INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    reasons_json TEXT DEFAULT '[]',
    checked_at TEXT NOT NULL,
    FOREIGN KEY(video_job_id) REFERENCES video_jobs(id)
);
CREATE TABLE IF NOT EXISTS publish_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    account_name TEXT NOT NULL,
    external_account_id TEXT DEFAULT '',
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    UNIQUE(platform, account_name)
);
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_job_id INTEGER NOT NULL,
    target_id INTEGER,
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    external_post_id TEXT DEFAULT '',
    error TEXT DEFAULT '',
    idempotency_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    FOREIGN KEY(video_job_id) REFERENCES video_jobs(id),
    FOREIGN KEY(target_id) REFERENCES publish_targets(id)
);
"""


def init_db() -> None:
    with connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


@contextmanager
def connection():
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def fetch_one(query: str, params: Iterable[Any] = ()) -> dict[str, Any] | None:
    with connection() as conn:
        row = conn.execute(query, tuple(params)).fetchone()
        return dict(row) if row else None


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
    with connection() as conn:
        return [dict(row) for row in conn.execute(query, tuple(params)).fetchall()]


def execute(query: str, params: Iterable[Any] = ()) -> int:
    with connection() as conn:
        cursor = conn.execute(query, tuple(params))
        conn.commit()
        return int(cursor.lastrowid or 0)
