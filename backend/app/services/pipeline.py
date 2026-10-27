from __future__ import annotations

import json
from datetime import datetime, timezone

from ..db import execute, fetch_one
from .policy import evaluate
from .providers import content_provider, tts_provider
from .render import render_video


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_video_job(job_id: int) -> dict:
    job = fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id])
    if not job:
        raise ValueError("Video job không tồn tại")
    product = None
    if job.get("product_id"):
        product = fetch_one("SELECT * FROM products WHERE id = ?", [job["product_id"]])
        if product:
            product["benefits"] = json.loads(product.pop("benefits_json", "[]"))
    trend = fetch_one("SELECT * FROM trends WHERE id = ?", [job["trend_id"]]) if job.get("trend_id") else None
    if not product and not trend:
        _fail(job_id, "Cần product_id hoặc trend_id")
        return fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id]) or {}
    product = product or {"name": trend["title"], "benefits": [], "image_path": "", "currency": "VND"}
    script = content_provider.generate_script(product, trend)
    script_json = {"hook": script.hook, "body": script.body, "cta": script.cta, "full_text": script.full_text}
    passed, reasons = evaluate(product, script.full_text)
    execute("UPDATE video_jobs SET status = ?, script_json = ?, updated_at = ?, error = ? WHERE id = ?", ["blocked" if not passed else "rendering", json.dumps(script_json, ensure_ascii=False), now(), "; ".join(reasons), job_id])
    execute("INSERT INTO policy_decisions(video_job_id, passed, reasons_json, checked_at) VALUES (?, ?, ?, ?)", [job_id, int(passed), json.dumps(reasons, ensure_ascii=False), now()])
    if not passed:
        return fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id]) or {}
    output_path, poster_path = render_video(product, script_json, job["template"])
    execute("UPDATE video_jobs SET status = ?, output_path = ?, poster_path = ?, updated_at = ? WHERE id = ?", ["ready", output_path, poster_path, now(), job_id])
    return fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id]) or {}


def _fail(job_id: int, message: str) -> None:
    execute("UPDATE video_jobs SET status = 'failed', error = ?, updated_at = ? WHERE id = ?", [message, now(), job_id])
