from __future__ import annotations

import json
import shutil
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import execute, fetch_all, fetch_one, init_db
from .schemas import (
    PolicyRequest,
    ProductImportRequest,
    PublishTargetRequest,
    ScheduleRequest,
    TrendCollectRequest,
    VideoJobRequest,
)
from .services.pipeline import process_video_job
from .services.policy import evaluate
from .services.providers import publisher
from .services.trends import collect, list_trends
from .worker import run_pending
from .studio import router as studio_router
from .studio_dashboard import router as dashboard_router


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Affiliate Auto Tyranno API", version="0.1.0", lifespan=lifespan)
app.include_router(studio_router)
app.include_router(dashboard_router)


@app.middleware("http")
async def local_studio_origin(request: Request, call_next):
    origin=request.headers.get("origin")
    if request.url.path.startswith('/studio') and request.method not in ['GET','HEAD','OPTIONS'] and origin:
        if origin not in {'http://localhost:3000','http://127.0.0.1:3000','http://localhost:8000','http://127.0.0.1:8000'}:
            return JSONResponse(status_code=403,content={'detail':'Studio local chỉ nhận thao tác từ web local.'})
    return await call_next(request)
app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins) or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/media", StaticFiles(directory=settings.media_root), name="media")
init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "affiliate-auto-tyranno", "time": now()}


@app.post("/products/import")
def import_product(payload: ProductImportRequest) -> dict:
    image_path = payload.image_path
    if payload.image_url and not image_path:
        try:
            with httpx.Client(timeout=15, follow_redirects=True) as client:
                response = client.get(payload.image_url)
                response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise ValueError("URL không trả về file ảnh")
            if len(response.content) > 10 * 1024 * 1024:
                raise ValueError("Ảnh vượt quá giới hạn 10MB")
            extension = ".jpg"
            if "png" in content_type:
                extension = ".png"
            elif "webp" in content_type:
                extension = ".webp"
            image_dir = settings.media_root / "uploads"
            image_dir.mkdir(parents=True, exist_ok=True)
            downloaded = image_dir / f"{secrets.token_hex(8)}{extension}"
            downloaded.write_bytes(response.content)
            image_path = str(downloaded)
        except Exception as exc:
            raise HTTPException(400, f"Không tải được image_url: {exc}") from exc
    product_id = execute(
        "INSERT INTO products(name, description, price, currency, benefits_json, image_path, source_url, affiliate_url, sku, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [payload.name, payload.description, payload.price, payload.currency, json.dumps(payload.benefits, ensure_ascii=False), image_path, payload.source_url, payload.affiliate_url, payload.sku, now()],
    )
    return get_product(product_id)


@app.post("/products/upload")
async def upload_product(file: UploadFile = File(...), name: str = "Sản phẩm mới", affiliate_url: str = "", price: float | None = None) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Chỉ nhận file ảnh")
    upload_dir = settings.media_root / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    target = upload_dir / Path(file.filename or "product.jpg").name
    with target.open("wb") as handle:
        shutil.copyfileobj(file.file, handle)
    product_id = execute("INSERT INTO products(name, price, benefits_json, image_path, affiliate_url, created_at) VALUES (?, ?, ?, ?, ?, ?)", [name, price, "[]", str(target), affiliate_url, now()])
    return get_product(product_id)


def get_product(product_id: int) -> dict:
    row = fetch_one("SELECT * FROM products WHERE id = ?", [product_id])
    if not row:
        raise HTTPException(404, "Product không tồn tại")
    row["benefits"] = json.loads(row.pop("benefits_json", "[]"))
    return row


@app.get("/products")
def products() -> list[dict]:
    return [get_product(row["id"]) for row in fetch_all("SELECT id FROM products ORDER BY id DESC")]


@app.post("/video-jobs")
def create_video_job(payload: VideoJobRequest, background_tasks: BackgroundTasks) -> dict:
    if not payload.product_id and not payload.trend_id:
        raise HTTPException(400, "Cần product_id hoặc trend_id")
    existing = fetch_one("SELECT * FROM video_jobs WHERE idempotency_key = ?", [payload.idempotency_key])
    if existing:
        return existing
    job_id = execute("INSERT INTO video_jobs(idempotency_key, product_id, trend_id, template, status, created_at, updated_at) VALUES (?, ?, ?, ?, 'queued', ?, ?)", [payload.idempotency_key, payload.product_id, payload.trend_id, payload.template, now(), now()])
    background_tasks.add_task(process_video_job, job_id)
    return fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id]) or {}


@app.get("/video-jobs")
def video_jobs(limit: int = 50) -> list[dict]:
    return fetch_all("SELECT * FROM video_jobs ORDER BY id DESC LIMIT ?", [min(limit, 200)])


@app.get("/video-jobs/{job_id}")
def video_job(job_id: int) -> dict:
    row = fetch_one("SELECT * FROM video_jobs WHERE id = ?", [job_id])
    if not row:
        raise HTTPException(404, "Video job không tồn tại")
    return row


@app.post("/worker/run")
def run_worker(limit: int = 10) -> dict:
    """Process queued jobs; suitable for cron/container loops until Celery is added."""
    return run_pending(limit)


@app.post("/trends/collect")
def collect_trends(payload: TrendCollectRequest) -> dict:
    return {"items": collect(payload.items), "count": len(payload.items)}


@app.get("/trends")
def trends() -> list[dict]:
    return list_trends()


@app.post("/policies/check")
def check_policy(payload: PolicyRequest) -> dict:
    product = get_product(payload.product_id) if payload.product_id else None
    passed, reasons = evaluate(product, payload.script)
    return {"passed": passed, "reasons": reasons}


@app.post("/publish-targets")
def create_target(payload: PublishTargetRequest) -> dict:
    target_id = execute("INSERT OR IGNORE INTO publish_targets(platform, account_name, external_account_id, created_at) VALUES (?, ?, ?, ?)", [payload.platform, payload.account_name, payload.external_account_id, now()])
    row = fetch_one("SELECT * FROM publish_targets WHERE platform = ? AND account_name = ?", [payload.platform, payload.account_name])
    return row or {"id": target_id}


@app.get("/publish-targets")
def targets() -> list[dict]:
    return fetch_all("SELECT * FROM publish_targets ORDER BY id DESC")


@app.post("/schedule")
def schedule(payload: ScheduleRequest) -> dict:
    job = fetch_one("SELECT * FROM video_jobs WHERE id = ?", [payload.video_job_id])
    if not job:
        raise HTTPException(404, "Video job không tồn tại")
    existing = fetch_one("SELECT * FROM schedules WHERE idempotency_key = ?", [payload.idempotency_key])
    if existing:
        return existing
    schedule_id = execute("INSERT INTO schedules(video_job_id, target_id, scheduled_at, idempotency_key, created_at) VALUES (?, ?, ?, ?, ?)", [payload.video_job_id, payload.target_id, payload.scheduled_at.isoformat(), payload.idempotency_key, now()])
    return fetch_one("SELECT * FROM schedules WHERE id = ?", [schedule_id]) or {}


@app.post("/scheduler/run")
def run_scheduler() -> dict:
    due = fetch_all("SELECT * FROM schedules WHERE status = 'scheduled' AND scheduled_at <= ? ORDER BY scheduled_at", [now()])
    published = []
    for item in due:
        job = fetch_one("SELECT * FROM video_jobs WHERE id = ?", [item["video_job_id"]])
        if not job or job["status"] != "ready":
            execute("UPDATE schedules SET status = 'failed', error = ? WHERE id = ?", ["Video chưa sẵn sàng", item["id"]])
            continue
        try:
            post_id = publisher.publish(job["output_path"], json.loads(job.get("script_json") or "{}").get("full_text", ""), item["idempotency_key"])
            execute("UPDATE schedules SET status = 'published', external_post_id = ? WHERE id = ?", [post_id, item["id"]])
            published.append(post_id)
        except Exception as exc:
            execute("UPDATE schedules SET status = 'failed', error = ? WHERE id = ?", [str(exc), item["id"]])
    return {"processed": len(due), "published": published}


@app.get("/analytics")
def analytics() -> dict:
    counts = fetch_all("SELECT status, COUNT(*) AS count FROM video_jobs GROUP BY status")
    schedule_counts = fetch_all("SELECT status, COUNT(*) AS count FROM schedules GROUP BY status")
    return {"video_jobs": {row["status"]: row["count"] for row in counts}, "schedules": {row["status"]: row["count"] for row in schedule_counts}}
