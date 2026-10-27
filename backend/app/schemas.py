from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ProductImportRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    price: float | None = Field(default=None, ge=0)
    currency: str = "VND"
    benefits: list[str] = Field(default_factory=list)
    image_url: str = ""
    image_path: str = ""
    source_url: str = ""
    affiliate_url: str = ""
    sku: str = ""


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float | None
    currency: str
    image_path: str
    source_url: str
    affiliate_url: str
    benefits: list[str]
    created_at: str


class VideoJobRequest(BaseModel):
    product_id: int | None = None
    trend_id: int | None = None
    template: str = "product_slideshow"
    idempotency_key: str = Field(min_length=3, max_length=120)
    auto_publish: bool = False


class TrendCollectRequest(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)


class ScheduleRequest(BaseModel):
    video_job_id: int
    scheduled_at: datetime
    target_id: int | None = None
    idempotency_key: str = Field(min_length=3, max_length=120)


class PublishTargetRequest(BaseModel):
    platform: str = "tiktok"
    account_name: str = Field(min_length=1, max_length=120)
    external_account_id: str = ""


class PolicyRequest(BaseModel):
    product_id: int | None = None
    script: str = ""
