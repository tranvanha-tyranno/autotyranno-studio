from __future__ import annotations

from datetime import datetime, timezone

from ..db import execute, fetch_all


def collect(items: list[dict]) -> list[dict]:
    saved = []
    for item in items:
        title = str(item.get("title", "")).strip()
        source_url = str(item.get("source_url", "")).strip()
        if not title or not source_url:
            continue
        summary = str(item.get("summary", ""))
        rights_status = str(item.get("rights_status", "unknown"))
        score = float(item.get("relevance_score", 0) or 0)
        try:
            row_id = execute(
                "INSERT OR IGNORE INTO trends(title, summary, source_url, published_at, rights_status, relevance_score, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [title, summary, source_url, item.get("published_at"), rights_status, score, datetime.now(timezone.utc).isoformat()],
            )
            saved.append({"id": row_id, "title": title, "source_url": source_url, "relevance_score": score, "rights_status": rights_status})
        except Exception:
            continue
    return saved


def list_trends(limit: int = 50) -> list[dict]:
    return fetch_all("SELECT * FROM trends ORDER BY relevance_score DESC, created_at DESC LIMIT ?", [limit])
