from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GeneratedScript:
    hook: str
    body: str
    cta: str
    full_text: str


class ContentProvider:
    """Provider boundary for a hosted or self-hosted LLM/vision model."""

    def generate_script(self, product: dict, trend: dict | None = None) -> GeneratedScript:
        name = product["name"]
        benefits = [item for item in product.get("benefits", []) if item]
        benefit_text = ", ".join(benefits[:3]) or "thiết kế tiện dụng, dễ dùng mỗi ngày"
        hook = f"Bạn đang tìm một lựa chọn tốt hơn cho {name}?"
        body = f"{name} nổi bật với {benefit_text}. "
        if product.get("price") is not None:
            body += f"Giá tham khảo hiện tại là {product['price']:,.0f} {product.get('currency', 'VND')}. "
        if trend:
            body = f"Theo chủ đề {trend['title']}, {body[0].lower() + body[1:]}"
        cta = "Xem thông tin và ưu đãi ở link trong phần mô tả."
        full_text = " ".join((hook, body, cta))
        return GeneratedScript(hook=hook, body=body, cta=cta, full_text=full_text)


class TTSProvider:
    """Provider boundary for Vietnamese TTS. MVP returns no audio; renderer adds silence."""

    def synthesize(self, text: str, output_path: Path) -> Path | None:
        return None


class Publisher:
    """Idempotent mock publisher; replace with official TikTok OAuth adapter."""

    def publish(self, video_path: str, caption: str, idempotency_key: str) -> str:
        digest = hashlib.sha256(idempotency_key.encode()).hexdigest()[:16]
        return f"mock_tiktok_{digest}"


content_provider = ContentProvider()
tts_provider = TTSProvider()
publisher = Publisher()
