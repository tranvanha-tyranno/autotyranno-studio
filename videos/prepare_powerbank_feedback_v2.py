"""Compile feedback into a fresh, portrait-first, text-free power-bank batch."""
from pathlib import Path
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'videos/2026-10-28-powerbank-marketing-42s'
BATCH = ROOT/'videos/2026-10-28-powerbank-feedback-v2-42s'
previous = json.loads((OLD/'batch.json').read_text(encoding='utf-8'))
product = (
    "Exactly ONE pastel lavender portable power bank as shown in product reference 1: "
    "a compact thick rounded rectangular smooth lavender body, glossy BLACK rounded-rectangle "
    "level window inset at one end of the broad front face, existing small white level markings, "
    "matching lavender loop strap and the original shell seam/visible side openings. Preserve "
    "the supplied body proportions and black window location. Do not add any brand, "
    "connector, port, cable, charging feature or invented value. The loop is treated only "
    "as a strap. Always show the existing front face at nearly its original three-quarter "
    "angle; only a small 5–8 degree yaw is permitted. Never expose an invented rear. "
    "Exactly ONE short original-style loop only: no second strap, long wrist lanyard, hanging extension or cable."
)
person = (
    "The exact fictional adult Vietnamese woman in reference image 2, about 28 years old, "
    "same oval face, eyes, nose, lips, medium warm skin tone, dark hair in a neat low ponytail, "
    "plain cream cotton blouse with long sleeves and dark trousers, short natural nails, no jewelry. "
    "Copy her face and tied-back hairstyle consistently; do not create a new woman. "
    "She is calm and friendly, lips relaxed and closed; narration is separate male Adam voice-over."
)
character = {
    "reference": "character/portrait.png",
    "prompt": """Create ONE photorealistic canonical character-reference portrait, vertical 9:16. A newly invented adult Vietnamese woman, about 28 years old, oval face, natural dark-brown eyes, straight small nose, naturally shaped lips, warm medium-light skin with realistic slight texture, dark hair neatly tied in a LOW PONYTAIL, a few tidy small wisps by ears. Plain cream long-sleeve cotton blouse with a simple collar, no jewelry. Medium head-and-upper-torso view, facing camera, both ears and full hairline visible, shoulders level, relaxed closed-mouth friendly half-smile. Neutral pale warm-gray studio backdrop. Stable bright softbox illumination from front-left plus gentle fill, neutral white balance, no harsh shadows or backlight. This is a fictional adult, not a likeness of any real person. Exact face, hairstyle and blouse will be used as an identity anchor across later product-review scenes. No product, other person, text, collage, graphic, label, signature or watermark. One single portrait, not a contact sheet.""",
}
environment = (
    "One bright clean product-review studio styled as a small electronics shop: pale oak counter, "
    "soft warm-white neutral wall and a few heavily blurred unbranded accessories, no readable "
    "signs or packaging. Broad FIXED diffuse studio key light plus fill at neutral 5200K. "
    "No visible window, sunlight beam, moving shadow, RGB lights or dark background transition. "
    "Keep identical bright exposure and neutral white balance in all scenes, especially the lavender body and cream sleeves."
)
dialogues = [
    "[surprised] Tưởng hộp phấn? Sạc dự phòng đó! [playful] Tím pastel nhìn cưng vậy, mang đi làm hay cà phê đều hợp nè.",
    "[upbeat] Cầm lên xoay nhẹ nè: thân bo góc, mặt vỏ trơn, có quai đồng màu. Thích đồ gọn xinh thì nghía em này!",
    previous['clips'][0]['scenes'][2]['dialogue'],
    previous['clips'][0]['scenes'][3]['dialogue'],
    previous['clips'][0]['scenes'][4]['dialogue'],
    previous['clips'][0]['scenes'][5]['dialogue'],
]
compositions = [
    "Medium upper-body portrait, woman centered with face fully visible, exact power bank on her supporting left open palm at chest level, front face angled just as in product reference. Right hand beside the blank lavender shell ready to touch it. Entire body and loop visible, power bank no more than 27% of frame height. Frame from above head to counter. No phone in hands.",
    "A close-up from below the woman's chin to the tabletop: the exact power bank centered in her supporting left palm, her right index and middle fingertips beside its broad blank lavender shell. The black window remains unobstructed. Complete strap and body visible with 20% side margins. Same cream sleeves; face is outside composition.",
    "A distinct three-quarter medium-close view from upper chest to tabletop, power bank in the SAME front-facing orientation on right supporting palm, free left index finger poised beside the blank shell just ABOVE the black level window without covering the window. Full strap visible. Face outside composition; original cream blouse visible.",
    "Medium upper-body view of the SAME woman, face fully visible, standing behind the pale oak counter. She holds the power bank in her left palm near chest level and her right hand is relaxed beside its blank shell. A closed plain unbranded laptop sits far to one side. The power bank is the only handheld product. Same bright fixed studio light.",
    "Tabletop medium-close view cropped below the woman's chin. Power bank supported above counter in left palm at its original front-facing angle, right fingertips poised near the blank lavender face. A plain black phone lies FACE DOWN at least 15 cm away on the counter, unconnected. No cable or charger adapter. Entire product and loop centered with generous margins.",
    "Medium upper-body closing portrait of the SAME woman with full face visible and a friendly closed-mouth smile. Power bank in supporting left palm at chest height, right hand lightly beside its blank lavender shell. Full product and loop visible. Clean pale studio/counter, no other foreground prop.",
]
actions = [
    "0.0–1.2s: supporting palm brings the product straight forward only 3 cm, clearly visible immediate action. 1.2–1.8s: brief NATURAL settling pause, camera also stops; real breathing only, no freeze-frame. 1.8–3.4s: gently yaw the rigid body only 7 degrees toward camera, keep original front and black window visible. 3.4–5.8s: other hand comes up; index and middle fingertips make ACTUAL light contact on the blank lavender shell ABOVE the black window and stroke a short 2 cm path once. Do not hover or point beside it. 5.8–7.8s: fingers lift, support stays secure, gently return the 7 degrees. 7.8–10s: clear final product presentation, small natural wrist settling, full strap inside frame.",
    "0.0–1.0s: free hand rises visibly toward the body; supporting hand keeps product stable. 1.0–1.6s: brief natural steady pose to show shape, no edited freeze. 1.6–3.0s: slowly turn rigid product only 6 degrees and STOP, keeping original front view. 3.0–6.0s: two fingertips visibly touch the BLANK upper lavender face and gently slide down 2 cm, stopping BEFORE the black window. Keep a real small contact shadow, no fingers merging into shell. 6.0–7.5s: fingertips release; rotate back 6 degrees. 7.5–10s: settle into secure palm presentation; no extra spin.",
    "0–1.2s: index finger lifts clearly toward the outer rim of the black window. 1.2–1.7s: settle briefly. 1.7–3.2s: supporting palm turns product 5 degrees so the original face remains visible. 3.2–5.6s: fingertip touches the lavender shell JUST ABOVE the black window, strokes a short sideways path without covering display or pressing any button. 5.6–7.2s: free hand lifts away and opens beside the product. 7.2–10s: return 5 degrees and present securely, small natural motion, no display-value changes.",
    "0–1.0s: lift product in palm 2 cm to present it. 1.0–1.6s: natural short pause. 1.6–3.2s: yaw it 6 degrees without revealing rear. 3.2–5.8s: right hand visibly touches and gently strokes the blank lavender body with two fingertips, all five fingers anatomically plausible. 5.8–7.4s: fingertips lift, supporting palm returns 6 degrees. 7.4–10s: a small friendly nod and stable product pose, relaxed closed lips.",
    "0–1.2s: free hand moves visibly from beside the separate face-down phone toward the held power bank. 1.2–1.8s: settle briefly. 1.8–3.4s: support turns power bank only 5 degrees and pauses. 3.4–5.9s: free fingertips make real contact on the blank lavender shell and give one short gentle stroke. Do not operate it, cover black window or connect phone. 5.9–7.5s: fingers release, restore original front angle. 7.5–10s: supporting palm continues secure natural presentation, phone stays separate.",
    "0–1.0s: present the power bank 2 cm forward on palm. 1.0–1.6s: brief natural pause. 1.6–3.2s: rotate rigid shell gently 6 degrees. 3.2–5.5s: other hand comes up and fingertips touch/stroke the blank lavender face once, not the black window. 5.5–7.2s: release fingers and restore original angle. 7.2–10s: small closed-mouth smile, product remains clearly presented in both supporting hands. No pointing at imaginary text.",
]
titles = ["Cú lật nhận diện trong 3 giây", "Dừng–xoay nhẹ–chạm vỏ", "Cận ô báo pin và lựa chọn màu", "Hai lựa chọn dung lượng theo nguồn", "Chọn đúng thông số và điện thoại", "CTA nói cuối video"]
scenes = []
for n in range(6):
    scenes.append({
        "title": titles[n], "seconds": 7, "visual_speed": 1.4, "dialogue": dialogues[n],
        "opening_prompt": (
            "Create one realistic vertical 9:16 product-review photograph. "
            "REFERENCE 1 is the exact product; REFERENCE 2 is the canonical fictional adult identity. "
            +product+'\n'+person+'\n'+environment+'\n'+compositions[n]+
            "\nNatural realistic palm-sized scale, normal fingers. Keep body and full loop inside central 70% with 15–20% margins. "
            "Do not manufacture a different face, hairstyle or blouse. No added text anywhere, no captions, titles, signs, "
            "subtitles, promotional cards, logos or watermark. Keep only physical markings originally on product. "
            "Bright steady neutral fill, no dramatic grade or vignette."
        ),
        "video_prompt": (
            "Generate ONE continuous realistic TEN-SECOND vertical 9:16 video at 720x1280. "
            "REFERENCE 1 is exact opening photograph. REFERENCE 2 is original product crop. "
            "REFERENCE 3 is CANONICAL CHARACTER PORTRAIT: same fictional adult face, ponytail and cream blouse whenever visible. "
            "Never cut to reference images or reveal a new person. "
            +product+'\n'+environment+
            "\nCAMERA: fixed tripod at the opening viewpoint; at most 2 cm lateral slide, no orbit, push-in, upward tilt or auto zoom. "
            "Keep the full product and full loop in central 70% throughout. Preserve size. "
            "Only 5–8 degree natural hand turn specified below, no wide rotation or rear view. "
            "The brief pause must be performed by the woman, not a frozen or repeated frame. "
            "Tactile demonstration means fingers actually contact the blank shell with a plausible contact shadow; "
            "not pointing beside it. No finger penetrating, extra fingers or melting shell. "
            "Do not cover, press or change the black display. "
            "Keep all source proportions, lavender color, black window and original level markings. "
            "No connecting cables, animated charging, accessories or invented features. "
            "Lips remain closed and relaxed; this is product B-ROLL with independent narration, no speaking or lip-sync. "
            "\nEXACT ACTION TIMELINE:\n"+actions[n]+
            "\nNo added text anywhere, including signs, subtitles, hook/CTA/spec cards, readable packaging or watermark. "
            "No music, speech or sound effects. No cuts, fade-in, fade-out, darkening, shadow sweep or exposure change."
        ),
        "action_timeline": actions[n],
    })
config = {
    "recipe_version": 5, "duration_seconds": 42, "visual_speed": 1.4,
    "text_overlays": False, "character": character,
    "quality": {"lock_exposure": True, "require_video_review": True,
                "exposure_lock": {"enabled": True, "max_brightness": .07, "roi": [.1, .1, .9, .9]}},
    "product_crop": previous['product_crop'], "product_description": product,
    "clips": [{
        "slug": "lavender-tactile-review", "presentation_mode": "presenter",
        "background": environment, "presenter": person,
        "dialogue": "\n\n".join(dialogues), "scenes": scenes,
        "marketing": {
            "hook": "Tưởng hộp phấn? Sạc dự phòng đó!", "hook_seconds": 3,
            "hook_strategy": "Reveal the product category after a visual cosmetic-case resemblance; truthful design comparison, no invented price.",
            "buyer_benefit": "A compact-looking pastel power-bank design to carry alongside the phone.",
            "reason_to_believe": "Visible product design demonstrated with real hand contact; source-qualified supplier capacity/power, not unverified claims.",
            "cta": previous['clips'][0]['marketing']['cta'],
        },
    }],
    "cache": {"muse": True, "tts": True},
    "research": previous['research'],
    "feedback": {
        "source_batch": str(OLD.relative_to(ROOT)),
        "requirements": ["Canonical face BEFORE every scene", "No text overlays", "No progressive dimming",
                         "Immediate action, natural short stop, 5–8 degree turn, other hand touches shell",
                         "Surprise-first spoken hook within 3 seconds, purchase CTA at end"],
        "old_batch_audit": "Previous batch feedback-audit/brightness-samples.json and brightness-and-motion.jpg",
    },
}
manifest = ROOT/'workflows/product-video/example-powerbank-portrait-first.json'
manifest.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
subprocess.run(["python", str(ROOT/'workflows/product-video/run.py'), "init", "--config", str(manifest),
                "--image", str(OLD/'input/original.png'), "--output", str(BATCH)], check=True)
for name in ['research.json', 'research-primary-check.json']:
    if (OLD/name).exists():
        shutil.copy2(OLD/name, BATCH/name)
shutil.copytree(OLD/'feedback-audit', BATCH/'feedback-audit')
shutil.copy2(OLD/'input/research-supplier-thumbnail.jpg', BATCH/'input/research-supplier-thumbnail.jpg')
(BATCH/'LOI-DOC.txt').write_text(re.sub(r'\[[^\]]+\]\s*', '', config['clips'][0]['dialogue']), encoding='utf-8')
lines = ["# Bản sửa sạc dự phòng — 42 giây, không chữ chèn", "",
         "Tạo và duyệt chân dung riêng trước ảnh cảnh. Sáu nguồn 10 giây, mỗi nguồn dùng 9,8 giây ở 1,4×; lời Adam căn riêng. Ánh sáng cố định, đo và hiệu chỉnh luma nhẹ nếu cần. Không lặp, không dùng freeze-frame làm nhịp dừng.", "",
         "Hook: **Tưởng hộp phấn? Sạc dự phòng đó!** — cú lật nhận diện từ ngoại hình, không bịa giá. CTA nói ở cuối, không có card hoặc phụ đề.", ""]
for n, scene in enumerate(scenes, 1):
    lines += [f"## {(n-1)*7:02}–{n*7:02}s — {scene['title']}", "", scene['dialogue'], "",
              "Chuyển động nguồn 10 giây: "+scene['action_timeline'], ""]
lines += ["## Phạm vi", "", "Thông số giữ điều kiện theo nhà cung cấp mẫu cùng kiểu. Ví dụ giá ấm inox của người dùng chỉ là định hướng hook, không phải giá sạc. Số trên ô báo pin là chi tiết gốc của sản phẩm; không thêm bất cứ dòng chữ quảng cáo/phụ đề nào."]
(BATCH/'KICH-BAN.md').write_text('\n'.join(lines), encoding='utf-8')
print("BATCH", BATCH)
