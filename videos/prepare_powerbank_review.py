"""Compile the researched power-bank brief into the reusable storyboard runner."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT/'videos/2026-10-28-powerbank-marketing-42s'
PRODUCT = """ONE compact pastel lavender power bank from the reference crop. Rounded rectangular thick smooth shell, broad glossy black rounded-rectangle battery-level window inset near one end of its broad front face, original small white level markings inside that window, lavender edge seam, matching flexible loop strap attached at that end, small side openings only where visible in the original. Preserve exact body proportions, the black window shape/location, original markings, lavender finish and loop strap. This is a portable power bank, NOT a phone, speaker, cosmetic case or purse. No added logo or brand, no invented port layout, connector, integrated charging cable, wireless charging coil or accessory. The loop is a STRAP, not a proven charging cable. Reference image does not establish actual capacity, charge rate, charging protocol or runtime. Keep the original product's visible front three-quarter orientation; do not show an invented rear view."""
PERSON = """A single fictional Vietnamese adult woman aged about 28, dark hair in a tidy low ponytail, pale cream long-sleeve cotton blouse and dark casual trousers, short natural nails, no jewelry. Same invented adult, face, hands and clothing in every scene, not a real person's likeness. Friendly, natural expression and relaxed closed mouth; Adam voice-over is separate, do not speak or lip-sync."""
SHOP = "A bright tidy modern electronics shop with pale oak counter, softly blurred accessory shelves and neutral daylight, no readable retail signs."
CAFE = "A bright quiet contemporary café workspace, pale oak table, softly blurred window, green plants and warm daylight; clean foreground with plenty of empty space."
IMAGE_BASE = f"""Create one realistic vertical 9:16 product-review photograph, full frame. Image 1 is the sole product authority. {PRODUCT}
{PERSON}
If reference image 2 is supplied, copy only that fictional adult's identity, clothes and natural lighting style; do not copy its composition when this scene asks for a close-up or a different setting.
The product is realistically palm-sized, one unit only, with its entire body AND strap in the central 70% of frame and at least 15% free space on each side. Product occupies 22–35% of frame height in presenter shots and at most 45% in close-ups, never giant. Keep the original front face aimed toward the camera and the same three-quarter orientation. Hands naturally support it, never cover the black window or deform the strap. Accurate five fingers, no extra limbs. No generated captions, price cards, added logo, watermark or invented display values. Leave clear space near the lower frame for captions added later by code.
"""
VIDEO_BASE = f"""Create one realistic continuous TEN-SECOND vertical 9:16 image-to-video shot, 720x1280. Reference 1 is the exact opening frame for composition, person and setting. Reference 2 is the original product crop: lock product design to it throughout, do not cut to or display this reference separately.
{PRODUCT}
Keep the SAME fictional adult and clothes, scene and lighting as reference 1. The power bank is one RIGID physical prop: never change its shell, black window, original markings, color or strap. Keep its front in the SAME three-quarter orientation as the opening photograph, no product spin, turn, flip, tilt or showing the back. Keep its full body and loop strap within the central 75% of every frame. No giant foreground push-in, no product crossing frame edges.
Natural purposeful motion starts immediately, no long still hold, no slow motion and no slideshow. Use the specified hand/camera action, not an orbit. Relaxed closed mouth, no lip-sync. No connecting or disconnecting cables, no simulated charging speed, no animated display or percentage jumps. Keep original display markings unchanged. No extra devices or accessories except those explicitly already visible in the opening.
"""
scenes_data = [
    {
        "title": "Hook 0–3 giây: pin yếu đúng lúc cần",
        "dialogue": "[animated] Pin đỏ đúng lúc cần? Bực ghê! [upbeat] Mấy ní xem mẫu sạc dự phòng mini này, nhìn xinh mà mang theo gọn nè.",
        "image": SHOP+" Medium waist-up shot. The adult presenter holds the exact lavender power bank at chest height in one open supporting palm. Her other hand presents it from beside the body. Her face is visible above it. A plain black smartphone lies face down on the counter, no visible screen. Clear product focus, realistic palm-sized product.",
        "action": "From the first frame she brings her supporting palm straight toward camera by only 3 cm during one second, preserving the product orientation; the other hand makes one clear inviting open-palm gesture BESIDE it. Camera tracks laterally 8 cm with obvious shelf parallax, fixed product view. Then both hands settle into a secure presentation with natural breathing; no head turn.",
        "card": {"title": "PIN ĐỎ ĐÚNG LÚC CẦN?", "subtitle": "Một phương án dự phòng để mang theo", "position": "top", "seconds": 3},
    },
    {
        "title": "Thiết kế: tím pastel, bo góc, quai đồng màu",
        "dialogue": "[friendly] Tông tím pastel, thân bo góc, thêm quai đeo đồng màu. Đi làm hay cà phê, có một cục pin dự phòng bên cạnh yên tâm hơn.",
        "image": SHOP+" Product close-up cropped below the presenter's shoulders, NO face in this frame. Two cream-sleeved adult hands hold the exact lavender power bank at the center, one palm beneath it and the other at its outer edge. Full body and loop strap visible, original black level window facing camera, natural realistic scale. Wide margins around the product.",
        "action": "From frame zero camera slides sideways 10 cm at a fixed distance, retaining the original product angle. Supporting palm stays still; the free index finger briefly indicates the outer rounded edge from BESIDE it, then opens to a small presentation. Do not touch the display, lift the loop or change grip.",
        "card": {"title": "TÍM PASTEL • BO GÓC", "subtitle": "Quai đồng màu — thiết kế nhìn từ ảnh gốc"},
    },
    {
        "title": "Cận ô báo pin và thông tin màu",
        "dialogue": "[explaining] Mặt trước có ô báo mức pin, liếc qua dễ theo dõi. Ảnh còn có đen, xanh nhạt và trắng, tùy phiên bản bán nha.",
        "image": SHOP+" A second distinct product close-up from slightly farther above but still showing the SAME front face at the original three-quarter angle. The exact lavender power bank rests centered in one cream-sleeved open palm just above the counter; the other index finger points beside the black battery-level window without touching or covering it. Full loop strap visible. No face in frame. No other colored units.",
        "action": "At frame zero the free finger makes one clear indication BESIDE the original black display window, then retracts outside the product outline. Camera moves down smoothly by 6 cm with an 8 cm lateral slide; not an orbit and not a zoom. The product remains steady on the palm, display unchanged, entire strap visible.",
        "card": {"title": "Ô BÁO MỨC PIN", "subtitle": "Ảnh có tím / đen / xanh nhạt / trắng"},
    },
    {
        "title": "Dung lượng: thông tin có nguồn và đúng phiên bản",
        "dialogue": "[confident] Theo nhà cung cấp, mẫu cùng kiểu có bản mười nghìn và hai mươi nghìn miliampe giờ. Nhớ chọn đúng dung lượng trên tem nha!",
        "image": CAFE+" Medium waist-up shot, SAME presenter seated at the table, one hand holding the exact lavender power bank at chest level at its original front three-quarter orientation. Other hand open beside it. A closed laptop and a face-down plain black phone sit well away from the product on the table. No cables attached, no charging demonstration. Product remains palm-sized, no visible labels or numbers on props.",
        "action": "From frame zero the free hand makes a clear small two-finger counting gesture BESIDE the power bank to indicate two available variants, then relaxes. The supporting hand and product remain steady. Camera tracks 10 cm sideways at a fixed distance, no push-in or orbit. Natural blinking, mouth stays closed.",
        "card": {"title": "10.000 / 20.000 mAh", "subtitle": "Theo nhà cung cấp mẫu cùng kiểu • tùy phiên bản"},
    },
    {
        "title": "Gỡ băn khoăn: kiểm tra công suất và cổng",
        "dialogue": "[explaining] Nhà cung cấp ghi công suất mười oát cho mẫu cùng kiểu. Muốn chọn đúng, kiểm tra tem, cổng sạc và điện thoại của mình nha.",
        "image": CAFE+" A tabletop hands-only composition cropped below the shoulders, SAME cream sleeves. Exact lavender power bank on one open supporting palm above the table at original front three-quarter angle, all body and strap visible. A plain black phone lies FACE DOWN on the table beside it with 15 cm separation; no cord connecting them, no adapters. Her free hand rests beside the phone, no face in frame.",
        "action": "Immediate clear action: her free hand makes one short open-palm sweep BETWEEN the face-down phone and power bank without touching either, then rests on the empty tabletop. Camera slides sideways 10 cm at a fixed distance so both objects remain separated and whole. Power bank orientation and original black window unchanged. Do not connect anything or reveal unseen ports.",
        "card": {"title": "10 W: THÔNG TIN NHÀ CUNG CẤP", "subtitle": "Đối chiếu tem và cổng sạc đúng phiên bản"},
    },
    {
        "title": "CTA chốt: giỏ hàng → dung lượng → màu → đặt",
        "dialogue": "[upbeat] Thích kiểu gọn xinh này? [encouraging] Bấm giỏ hàng, xem đúng dung lượng, chọn màu mình thích rồi chốt đơn nha, mấy ní!",
        "image": CAFE+" Medium waist-up closing product-review portrait, SAME presenter smiling naturally and holding the exact lavender power bank steadily at chest height in BOTH hands, front three-quarter orientation identical to the reference, complete loop strap visible. Product dominates center without being oversized. Table clear in foreground. Frame leaves clear room at lower edge for a purchase CTA added later.",
        "action": "From frame zero camera gently dollies backward 15 cm and slides 4 cm sideways, creating visible background parallax, no orbit. Both hands keep the product steadily in its original pose with natural breathing. She gives one small friendly smile and a tiny nod without turning her head. Do not lift, rotate or push the product toward camera. Preserve entire body and strap.",
        "card": {"title": "BẤM GIỎ HÀNG • CHỐT ĐƠN", "subtitle": "Xem dung lượng • chọn phiên bản và màu"},
    },
]
scenes = []
for number, data in enumerate(scenes_data, 1):
    scenes.append({
        "title": data["title"], "seconds": 7, "visual_speed": 1.4,
        "dialogue": data["dialogue"],
        "opening_prompt": IMAGE_BASE+data["image"],
        "video_prompt": VIDEO_BASE+"\nACTION: "+data["action"]+"\nNo added graphics, captions, narration, music or sound effects.",
        "on_screen": data["card"],
    })
    if number in (2, 3, 5):
        scenes[-1]["presenter_reference"] = "clip-01-lavender-powerbank-review/scene-01/opening.png"
config = {
    "recipe_version": 4, "duration_seconds": 42, "visual_speed": 1.4,
    "product_crop": [.145, .015, .60, .40], "product_description": PRODUCT,
    "muse_base": "http://127.0.0.1:18610",
    "clips": [{
        "slug": "lavender-powerbank-review", "presentation_mode": "presenter",
        "background": SHOP+" Then "+CAFE, "presenter": PERSON,
        "dialogue": "\n\n".join(scene["dialogue"] for scene in scenes),
        "scenes": scenes,
        "marketing": {
            "hook": "Pin đỏ đúng lúc cần? Bực ghê!", "hook_seconds": 3,
            "buyer_benefit": "Có phương án pin dự phòng mang theo trong ngày, thiết kế gọn và màu hợp gu.",
            "reason_to_believe": "Thiết kế thấy trực tiếp trong ảnh; dung lượng/công suất được gắn nguồn nhà cung cấp và điều kiện đúng phiên bản.",
            "cta": "Bấm giỏ hàng, xem đúng dung lượng, chọn màu mình thích rồi chốt đơn nha, mấy ní!",
            "buyer_friction": "Chọn đúng dung lượng, công suất và cổng phù hợp; không hứa số lần sạc hay tốc độ chưa kiểm chứng.",
        },
    }],
    "cache": {"muse": True, "tts": True},
    "research": {
        "checked_date": "2026-10-28",
        "identity": "Unbranded visual match to YM-931-style listings. Exact supplied unit has no readable model/rating label.",
        "primary_source": "https://en.yiwugo.com/product/detail/985643339.html",
        "image_match_source": "https://manuals.plus/ae/1005009175456096",
        "conflicting_secondary_source": "https://manuals.plus/m/8be5c3aa7a3f015d633bb28259739e5d44a4b19185427f21c2f8a02d4b11cac3",
        "claims": [
            {"claim": "Matching supplier advertises 10000/20000 mAh versions and 10 W", "status": "listing claim, not exact-unit verification"},
            {"claim": "Secondary page says 20 W", "status": "conflicts; excluded from narration"},
            {"claim": "Purple/black/light-blue/white body, rounded edges, strap, black level window", "status": "visible in user image"},
        ],
        "excluded": ["brand certainty", "20 W fast charging", "PD/QC", "actual capacity test", "number of phone recharges", "loop as cable", "discounts", "price", "stock scarcity"],
    },
}
manifest = ROOT/'workflows/product-video/example-powerbank-storyboard.json'
manifest.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
subprocess.run([
    "python", str(ROOT/'workflows/product-video/run.py'), "init",
    "--config", str(manifest), "--image",
    r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-e39aa554-de13-438b-8234-fe4d75da9282.png",
    "--output", str(BATCH),
], check=True)
(BATCH/'research.json').write_text(json.dumps(config['research'], ensure_ascii=False, indent=2), encoding='utf-8')
lines = [
    "# Kịch bản giới thiệu sạc dự phòng — 42 giây", "",
    "Một video dọc 720 × 1280, 30 fps. Sáu cảnh riêng, nguồn 10 giây/cảnh; dùng 9,8 giây ở 1,4× thành 7 giây/cảnh. Adam / Eleven v3, tiếng Việt.", "",
    "## Ý tưởng marketing", "",
    "Người đi làm/cà phê ngại điện thoại hết pin đúng lúc cần. Hook đánh thẳng vào tình huống này trong 3 giây; sản phẩm xuất hiện ngay, rồi chuyển từ thiết kế thấy được sang thông số có nguồn và tiêu chí chọn đúng. CTA cuối chỉ rõ hành động mở giỏ hàng, chọn dung lượng/màu và đặt mua. Không bịa giảm giá, khan hiếm hoặc trải nghiệm đã sử dụng.", "",
]
for n, data in enumerate(scenes_data):
    lines += [f"## {n*7:02}–{(n+1)*7:02} giây — {data['title']}", "", data["dialogue"], "", "**Chữ trên hình:** "+data["card"]["title"]+" — "+data["card"]["subtitle"], ""]
lines += ["## Phạm vi thông số", "", "Ảnh không có nhãn model/tem công suất đọc được. Nguồn nhà cung cấp là mẫu cùng kiểu YM-931, không xác nhận thông số chiếc trong ảnh. Vì vậy lời đọc và chữ đều giữ điều kiện theo nhà cung cấp/tùy phiên bản. Không khẳng định sạc nhanh 20 W, PD/QC, số lần sạc, cáp tích hợp hoặc dung lượng thực đo.", "", "Nguồn và claim lưu trong research.json. Các ảnh và chuyển động AI phải được xem QA trước khi chọn ghép."]
(BATCH/'KICH-BAN.md').write_text("\n".join(lines), encoding='utf-8')
print("BATCH_READY", BATCH)
