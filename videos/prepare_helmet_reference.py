"""Prepare the user's single 30-second helmet review; no provider calls here."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "videos/2026-10-28-helmet-reference-30s"
PRODUCT = """The exact adult bicycle helmet in reference image 1: matte charcoal-black sculpted shell, broad curved projecting front visor, long angular ventilation openings and dark mesh beneath, black Y-shaped chin straps and small black buckle. Preserve the silhouette, vent layout, visor shape, dark finish and straps from the photograph. The small existing light-colored wordmark stays subtle and unchanged; never invent lettering. It is a vented BICYCLE helmet, with NO transparent face shield, no motorcycle ear covers, no LED, no camera and no extra accessory. Do not invent safety certification, impact-test performance, weight, material grade, sizing or price."""
PERSON = """One fictional Vietnamese adult woman, about 28 years old, oval face, medium-length dark hair tied in a low ponytail, olive-green zip cycling jacket, plain black athletic trousers, short natural nails, no jewelry. Friendly understated expression, no resemblance to a named real person. Keep the exact same face, ponytail and clothing across scenes. Her mouth stays relaxed, no talking or lip-sync; male Vietnamese voice-over will be added separately."""
BASE_IMAGE = f"""Create one realistic product-review photograph, vertical 9:16, full bleed, natural smartphone advertising photography. Product reference image 1 is the sole authority for the HELMET geometry and finish. {PRODUCT}
{PERSON}
If a second reference is supplied, use it for the exact fictional presenter's identity and clothes, not as a replacement helmet design. The helmet is the main subject, no oversized proportions, no duplicate helmet. Plausible hands, five fingers per hand, no extra limbs. Keep all important helmet parts within the central 80% of the frame. No graphic overlays, subtitles, captions, price cards or watermark.
"""
SCENES = [
    {
        "time": "00:00–00:06",
        "title": "Hook — cầm mũ trong cửa hàng",
        "opening": "In a bright contemporary bicycle and helmet shop with softly blurred bicycle racks and warm shelf lighting. Medium shot, presenter waist-up centered slightly to the right. She holds the complete helmet at chest height toward camera, one palm beneath it and the other hand lightly at the side, in the same front-left three-quarter angle as the product photo. All straps hang freely and are visible. Helmet dominates the lower-middle foreground, presenter face visible above it. No display stand or duplicate helmets in the foreground.",
        "action": "Action starts at frame zero: she smoothly brings the held helmet 8 cm closer toward the camera during seconds 0–2, turns it only 12 degrees to reveal the front visor during seconds 2–5, then makes a short presenting gesture beside it while keeping support beneath it. The camera makes an obvious small lateral track, maintaining the full helmet in view. No long motionless hold.",
        "line": "[upbeat] Đạp xe mà mê kiểu đen thể thao, nghía chiếc mũ này nè! Dáng gọn, lưỡi trai phía trước nhìn rất cá tính.",
    },
    {
        "time": "00:06–00:12",
        "title": "Cận vỏ, khe thoáng và lưới",
        "opening": "In the SAME bicycle shop, a close product-detail shot cropped below the presenter's shoulders; face outside frame. Olive sleeves and two natural hands hold the helmet close to camera in a slightly elevated front-left three-quarter view, revealing the long top vents and dark mesh without exposing an invented rear design. Product fills 60% of frame height; complete front visor, shell and dangling chin straps stay in frame. Warm shelf bokeh behind.",
        "action": "From frame zero the camera slides briskly 15 cm from left to right while rising 8 cm, revealing the existing top vents and dark mesh. Her supporting hand stays under the helmet; one index finger briefly indicates an existing vent from its outer edge without covering it. Only a small 10-degree product tilt, no deformation, no full spin. Keep the complete visor and shell inside the frame.",
        "line": "[explaining] Nhìn gần mới rõ: vỏ mũ tông đen nhám, các khe thoáng chạy dọc thân, bên dưới có lớp lưới tối màu.",
    },
    {
        "time": "00:12–00:18",
        "title": "Đội thử — chỉ quai cài",
        "opening": "Outdoors on a quiet leafy paved bicycle path in soft daylight, no moving traffic. Medium portrait from waist up. The SAME presenter now WEARS the exact reference bicycle helmet level on her head, natural adult fit, visor above eyebrows. Black Y straps run naturally beside her ears with buckle already secured under chin. Her right index finger points just beside the visible strap, not across her face; left arm relaxed. No second helmet, no sunglasses, no transparent face shield. A parked bicycle is softly blurred to one side.",
        "action": "Start immediately with a clear small hand gesture indicating the already-fastened chin strap, then lower her hand and turn her head only 15 degrees from three-quarter toward camera. Camera tracks sideways 15 cm with visible tree parallax. The helmet stays level on her head and rigidly follows the head, no removal or clipping through hair, no unfastening and no cycling. Keep visor and chin in frame.",
        "line": "[friendly] Phía dưới là quai đen và khóa cài. Khi đội, chỉnh quai vừa vặn, để mũ ôm ngay ngắn trên đầu nha.",
    },
    {
        "time": "00:18–00:24",
        "title": "Phối đồ bên xe đạp",
        "opening": "On the SAME leafy park cycle path, wider three-quarter-length shot of the SAME presenter wearing the same exact helmet correctly with secured chin strap, olive jacket and black athletic trousers. She stands beside a stationary simple matte dark bicycle, one hand lightly on handlebar, both feet on ground. She is NOT seated or riding. Lush green background, natural daylight. Helmet remains large enough to identify, no other people or helmets.",
        "action": "Action from frame zero: a brisk smooth camera dolly moves 30 cm sideways and pushes in 10 percent. The presenter glances naturally from the stationary bicycle toward camera, straightens her jacket hem once with her free hand and gives a small friendly nod. Bicycle remains stationary, no pedaling or riding. Helmet is unchanged, visor above brows and straps secured. Avoid drifting into full-body distant framing.",
        "line": "[upbeat] Phối cùng áo đạp xe hay đồ năng động đều dễ. Đứng cạnh chiếc xe là có ngay một tổng thể khỏe khoắn.",
    },
    {
        "time": "00:24–00:30",
        "title": "Cầm mũ chốt — xem chi tiết và chọn cỡ",
        "opening": "A sunny grassy park beside the same cycle path, softly blurred greenery. Medium shot of the SAME presenter with her bare head visible and the exact helmet HELD at chest height toward camera in the same front-left three-quarter orientation as the original product photo. This is a new shot after taking the helmet off between scenes; do not show removal. Both hands naturally support the helmet from below and the side; all straps visible and free. Product foreground, warm friendly expression behind.",
        "action": "Start immediately: she presents the helmet forward 8 cm and gently tilts it 8 degrees toward camera, then returns to its original front three-quarter angle. One hand remains supporting it at all times, the other briefly makes an open-palm inviting gesture beside it and supports again. Smooth camera push-in 12 percent with subtle lateral parallax, no long pause. Finish with the complete recognizable helmet prominent.",
        "line": "[encouraging] Thích kiểu mũ này thì mở giỏ hàng xem thông tin và chọn đúng cỡ nha. Đạp xe cuối tuần, lên đồ gọn thôi!",
    },
]

dialogue = "\n\n".join(scene["line"] for scene in SCENES)
shot_prompts = [
    f"""Generate a NEW realistic ten-second single continuous video shot from this exact opening photograph, vertical 9:16, 720p. {PRODUCT}
Keep this same fictional adult presenter, clothes, room/location and lighting from the opening photograph. {scene['action']}
Brisk natural real-time human motion, visible movement from the very first frame and continuing with purpose. No ultra-slow-motion orbit. Frame the HELMET as the product, not an appliance. Preserve all vents, mesh, visor, shell and chin straps consistently. No invented rear view or 360 rotation. Anatomically plausible hands, no extra fingers, no helmet morphing or changing into another model. No scene cuts, montage, text, subtitles, watermark, music, sound effects or narration. Relaxed closed mouth, no talking or lip sync. Do not add a motorcycle face shield or accessory. Keep the full helmet visible throughout."""
    for scene in SCENES
]
config = {
    "recipe_version": 3,
    "duration_seconds": 30,
    "muse_base": "http://127.0.0.1:18610",
    "visual_speed": 1.5,
    "scene_count": 5,
    "product_description": PRODUCT,
    "clips": [{
        "slug": "helmet-reference-review",
        "presentation_mode": "presenter",
        "background": "Bicycle shop followed by leafy park, as detailed in storyboard.json.",
        "presenter": PERSON,
        "dialogue": dialogue,
        "opening_prompt": BASE_IMAGE + SCENES[0]["opening"],
        "shot_prompts": shot_prompts,
    }],
    "cache": {"muse": True, "tts": True},
}
config_path = ROOT / "videos/helmet-reference-30s-config.json"
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
subprocess.run([
    "python", str(ROOT / "workflows/product-video/run.py"), "init",
    "--config", str(config_path),
    "--image", r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-6a60d0ae-d473-4c42-a755-f8328e246a06.png",
    "--output", str(BATCH),
], check=True)
shutil.copy2(
    r"C:\Users\tyranno\Downloads\1793149090772_3731987180214464481_3731987180214464481.mp4",
    BATCH / "input/reference-style.mp4",
)
(BATCH / "storyboard.json").write_text(json.dumps(SCENES, ensure_ascii=False, indent=2), encoding="utf-8")
(BATCH / "image-base-prompt.txt").write_text(BASE_IMAGE, encoding="utf-8")
clip_dir = BATCH / "clip-01-helmet-reference-review"
for n, scene in enumerate(SCENES, 1):
    (clip_dir / f"scene-{n:02}-opening-prompt.txt").write_text(BASE_IMAGE + scene["opening"], encoding="utf-8")
    (clip_dir / f"scene-{n:02}-prompt.txt").write_text(shot_prompts[n-1], encoding="utf-8")
lines = [
    "# Kịch bản video mũ xe đạp — 30 giây",
    "",
    "Một video dọc 720 × 1280, 30 fps. Năm cảnh AI độc lập, mỗi nguồn 10 giây; lấy 9 giây mỗi nguồn và phát hình 1,5× thành 6 giây/cảnh. Không lặp hoặc kéo chậm. Voice-over tiếng Việt: Adam / Eleven v3.",
    "",
    "Tham chiếu phong cách: clip người dùng dài 39,87 giây; chỉ lấy nhịp cầm mũ, cận chi tiết, đội thử và bối cảnh công viên. Sản phẩm và lời đọc dựa trên ảnh mũ xe đạp đen của người dùng.",
    "",
]
for scene in SCENES:
    lines += [f"## {scene['time']} — {scene['title']}", "", scene["line"], ""]
lines += [
    "## Phạm vi thông tin",
    "",
    "Chỉ mô tả thiết kế quan sát được: màu đen nhám, lưỡi trai, khe thoáng, lưới tối màu, quai và khóa cài. Ảnh không cung cấp khối lượng, chất liệu chính xác, chứng nhận, giá hoặc kích cỡ nên lời đọc không nêu các thông số này.",
    "",
    "Người mẫu là nhân vật AI trưởng thành. Hình đội thử và các góc không có trong ảnh là AI suy diễn, cần xem QA trước khi sử dụng.",
]
(BATCH / "KICH-BAN.md").write_text("\n".join(lines), encoding="utf-8")
print(BATCH)
