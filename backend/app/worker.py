"""Database-backed worker for deployments without Celery/Redis yet.

The endpoint can be invoked by a cron job or a container loop. It keeps the job
state durable and can later be replaced by a Celery task with the same service
function.
"""

from .db import execute, fetch_all
from .services.pipeline import process_video_job


def run_pending(limit: int = 10) -> dict:
    jobs = fetch_all("SELECT id FROM video_jobs WHERE status = 'queued' ORDER BY id LIMIT ?", [min(limit, 100)])
    processed = []
    for job in jobs:
        try:
            processed.append(process_video_job(job["id"]))
        except Exception as exc:
            execute("UPDATE video_jobs SET status = 'failed', error = ? WHERE id = ?", [str(exc), job["id"]])
    return {"processed": len(processed), "jobs": processed}
