import json
import time
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.db import init_db
from app.main import app


def test_product_to_publish_flow(tmp_path, monkeypatch):
    db_path = tmp_path / "app.db"
    media_path = tmp_path / "media"
    object.__setattr__(settings, "database_path", db_path)
    object.__setattr__(settings, "media_root", media_path)
    settings.ensure_dirs()
    init_db()

    with TestClient(app) as client:
        product = client.post("/products/import", json={
            "name": "Bình giữ nhiệt",
            "price": 199000,
            "benefits": ["Giữ nóng"],
            "affiliate_url": "https://example.test/product/1",
        }).json()
        job = client.post("/video-jobs", json={
            "product_id": product["id"],
            "idempotency_key": "test-job-1",
        }).json()
        for _ in range(20):
            job = client.get(f"/video-jobs/{job['id']}").json()
            if job["status"] in {"ready", "blocked", "failed"}:
                break
            time.sleep(0.1)
        assert job["status"] == "ready"
        assert Path(job["output_path"]).exists()

        duplicate = client.post("/video-jobs", json={
            "product_id": product["id"],
            "idempotency_key": "test-job-1",
        }).json()
        assert duplicate["id"] == job["id"]

        schedule = client.post("/schedule", json={
            "video_job_id": job["id"],
            "scheduled_at": "2020-01-01T00:00:00Z",
            "idempotency_key": "test-schedule-1",
        })
        assert schedule.status_code == 200
        result = client.post("/scheduler/run").json()
        assert result["published"]


def test_policy_blocks_unsafe_claim(tmp_path):
    object.__setattr__(settings, "database_path", tmp_path / "policy.db")
    settings.ensure_dirs()
    init_db()
    with TestClient(app) as client:
        response = client.post("/policies/check", json={"script": "Sản phẩm chữa khỏi mọi bệnh và cam kết 100%"})
        body = response.json()
        assert body["passed"] is False
        assert body["reasons"]
