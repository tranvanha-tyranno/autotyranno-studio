from __future__ import annotations

import re


BLOCKED_PATTERNS = (
    r"chữa khỏi",
    r"điều trị dứt điểm",
    r"cam kết (100|tuyệt đối)%?",
    r"giàu nhanh",
    r"kiếm tiền chắc chắn",
    r"không có tác dụng phụ",
)


def check_product(product: dict) -> list[str]:
    reasons: list[str] = []
    if not product.get("name"):
        reasons.append("Thiếu tên sản phẩm")
    if not product.get("affiliate_url") and not product.get("source_url"):
        reasons.append("Thiếu link sản phẩm hoặc link affiliate")
    if product.get("price") is not None and product["price"] < 0:
        reasons.append("Giá sản phẩm không hợp lệ")
    return reasons


def check_script(script: str) -> list[str]:
    lowered = script.lower()
    return [f"Nội dung chứa claim bị chặn: {pattern}" for pattern in BLOCKED_PATTERNS if re.search(pattern, lowered)]


def evaluate(product: dict | None = None, script: str = "") -> tuple[bool, list[str]]:
    reasons = check_product(product or {})
    reasons.extend(check_script(script))
    return not reasons, reasons
