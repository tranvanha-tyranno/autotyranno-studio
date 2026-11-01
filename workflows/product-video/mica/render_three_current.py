"""Render the three supplied kettle-in-mica references as separate 6-second clips.

This is a thin, reproducible wrapper around render_uploaded_images.py. It keeps
the existing provider polling/FFmpeg/QA implementation while selecting only
the three references from the current request.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "mica_uploaded_runner", ROOT / "workflows/product-video/mica/render_uploaded_images.py"
)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)

runner.OUT = ROOT / "videos" / "2026-10-28-inox-kettle-3clips"
runner.REFS = [
    (
        r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-13b8ac5a-88ef-474d-a22e-b1f51459f3bb.png",
        "01-factory-forward",
        "Ấm inox cao cấp 1,8 lít",
        "bối cảnh xưởng sản xuất điện máy đang có trong ảnh",
        "[excited] Ê ê ê! Ấm inox 1,8 lít, đun sôi nhanh và tự ngắt điện khi nước sôi nè!",
    ),
    (
        r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-60c4dd6f-e070-4bf6-a1c6-7058d413d711.png",
        "02-mall-sidewalk",
        "Ấm inox cao cấp 1,8 lít",
        "bối cảnh trung tâm thương mại đang có trong ảnh",
        "[playful] Các dợ nhìn nè! Vòi rót gọn, tay cầm cách nhiệt, đế xoay 360 độ luôn á!",
    ),
    (
        r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bf6674cd-0a5f-4f9e-b029-834f3a8fd341.png",
        "03-appliance-shelf",
        "Ấm inox cao cấp 1,8 lít",
        "bối cảnh cửa hàng gia dụng đang có trong ảnh",
        "[amazed] Inox sáng bóng, nắp mở tiện, dung tích 1,8 lít; mấy ní thấy hợp thì chốt nha!",
    ),
]


def prompt_for(name, setting, product):
    if name.startswith("01-"):
        action = (
            "0–0,3 giây bắt đầu bước ngay; 0,3–4,8 giây đi 3 bước dứt khoát về phía trước, "
            "camera theo nhịp bước tạo parallax rõ với dây chuyền phía sau; hộp nhún chỉ 1–3 cm, "
            "mặt trước luôn thẳng camera; 4,8–6 giây tiếp tục một bước ngắn và ổn định."
        )
    elif name.startswith("02-"):
        action = (
            "0–0,3 giây bắt đầu dịch ngang; 0,3–5,3 giây đi 3 bước ngang qua hành lang trung tâm thương mại, "
            "hậu cảnh và đèn trôi ngang rõ, camera đi cùng tay giữ hộp; 5,3–6 giây vẫn chuyển động nhẹ, "
            "không dừng tạo dáng."
        )
    else:
        action = (
            "0–0,3 giây hạ hộp ngay 8–10 cm bằng cẳng tay; 0,3–2,2 giây camera lùi rất ngắn để giữ trọn quai và đáy; "
            "2,2–4,8 giây đi ngang một nhịp qua kệ gia dụng có sẵn, hậu cảnh trôi rõ; 4,8–6 giây ổn định gọn, "
            "không đặt hộp lên kệ hay mặt đỡ."
        )
    return f'''Tạo video POV dọc 9:16, đúng 6 giây, từ chính ảnh tham chiếu này. Đây là biến thể {name}, {setting}.
Giữ đúng ấm inox màu bạc, thân kim loại, quai đen, nắp đen, vòi rót, đèn báo đỏ và đế xoay; không biến thành sản phẩm khác. Giữ nguyên các claim nhìn thấy trên ảnh: dung tích 1.8L, inox cao cấp, đun sôi nhanh, tự động ngắt điện, vòi rót tiện lợi, tay cầm cách nhiệt, nút mở nắp và đế xoay 360 độ.

NHỊP HÀNH ĐỘNG: {action} Hành động phải bắt đầu trong 0–0,3 giây, không slow motion, không giữ ảnh tĩnh lâu.

Chỉ một bàn tay và cẳng tay nữ trưởng thành đang giữ quai được xuất hiện; không có mặt, đầu, thân, phản chiếu mặt người, tay thứ hai hay ngón thừa. Hộp mica lơ lửng, không chạm bàn/sàn/kệ; hộp cứng, ấm cố định bên trong, không xoay, không lật, không orbit rộng, mặt trước luôn hướng camera. Giữ nguyên bố cục nền, ánh sáng, màu móng, kiểu quai, kích thước hộp, sản phẩm, phụ kiện, từng chữ và nhãn; thấy trọn quai và đáy với khoảng trống dưới đáy. Không thêm logo, chữ, watermark, props, nhạc, thoại hay sound effect. Một shot liền mạch, không cắt.'''


runner.prompt_for = prompt_for

if __name__ == "__main__":
    runner.main()
