"""Prepare two independent portrait-first 20s batches from this power-bank collage.

Only prepares local assets/manifests. Provider stages remain in run.py with its
cache, saved tasks, image-review gate and video-review gate.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).with_name('run.py')

PRODUCT = (
    "Exactly ONE palm-sized pastel lavender power bank matching product reference: "
    "thick rounded rectangular rigid smooth shell, glossy BLACK rounded rectangular "
    "level window at one end of the broad front face, original white level markings, "
    "one short matching lavender loop and original seam. Preserve shell/window/loop "
    "proportions and relative positions. Never add cables, extra loops, new ports, "
    "brand names or accessories. The loop is a strap, not a charging cable. "
    "Keep original front facing the camera; no rear or hidden-edge reconstruction. "
    "Product lies LOW AND FLAT across the supporting palm at the reference diagonal "
    "three-quarter angle: squat blank shell UPPER-LEFT, black window LOWER-RIGHT, "
    "one short original loop UPPER-RIGHT. Never stand upright or elongate the body."
)
NO_TEXT = (
    "No added text anywhere: no captions, subtitles, titles, cards, watermark, "
    "readable background signs or invented product lettering. Preserve only "
    "intrinsic product markings. No collage or graphic layout."
)
ACTION = (
    "0–1.0s: free hand visibly rises toward the blank shell while the supporting "
    "palm keeps its original grip. 1.0–1.5s: natural short settling pause. "
    "Around 2s: tilt the entire rigid product only 3 degrees in depth, front and black "
    "window always visible, same supporting grip and wrist orientation. "
    "3.0–6.0s: the OTHER hand's index and middle fingertips actually touch the BLANK "
    "lavender shell and stroke a short 1 cm path once, with plausible contact shadow. "
    "Do not hover, point beside it, touch or cover the window. "
    "6.0–10s: fingertips lift and the supporting palm keeps the original product "
    "pose, only natural hand breathing, full product and loop in frame."
)


def locked_video_prompt():
    """Motion brief validated on close-ups; source QA is still mandatory.

    A later Chinese-only version still produced upright turns on medium portraits.
    Preserve that failed attempt in its batch and default to this tested close-up
    brief, without treating prompt wording alone as proof of product fidelity.
    """
    return (
        "A realistic single continuous 10-second vertical product demonstration, 9:16, 720x1280. "
        "Use image 1 exactly as the starting shot. Same hands, clothing, lavender power bank "
        "and light. Image 2 locks the exact product, image 3 locks the same adult woman if "
        "any face becomes visible.\n"
        "Keep the product CRADLED HORIZONTALLY in the SAME supporting palm, in the SAME "
        "diagonal orientation as image 1 for all ten seconds. The black display stays at "
        "the LOWER-RIGHT of the visible body, the loop stays at the UPPER-RIGHT, and the "
        "same long edge stays nearest the camera. Do not roll it in the picture plane, "
        "turn it upright, turn it upside down, flip, change grip or show any other side. "
        "Keep the supporting forearm and wrist still. Only a tiny 3-degree side-to-side "
        "depth yaw once, which never changes those screen positions. The black window "
        "is always glossy solid BLACK with its original tiny white markings, never gray, "
        "never blank or glowing. Exactly one short lavender loop, original body proportions "
        "and visible side geometry.\n"
        "EXACTLY TWO HANDS TOTAL: the existing supporting palm and the existing free hand "
        "already visible in the opening. The same free hand follows one continuous visible "
        "path to the shell and back. If it starts resting on the desk, that desk position "
        "becomes EMPTY when it lifts. Never leave a duplicate hand on the desk or summon "
        "a third hand from the opposite edge. Keep the supporting hand in its original grip.\n"
        "Simple action: immediately lift the FREE HAND toward the blank lavender shell; "
        "settle for half a second. Around second 2 make the tiny 3-degree depth yaw and "
        "stop. From seconds 3 to 6, gently place two fingertips ON the blank upper lavender "
        "shell and slowly stroke just 1 cm, then lift them away. Supporting hand and body "
        "remain in their original pose. From seconds 6 to 10 keep product steady, only "
        "natural hand breathing and one small free-finger gesture beside it. No extra "
        "action or handling. Do not touch/cover the black display or loop. Fingers must "
        "have believable contact shadows, no fingers through product.\n"
        "Camera is a LOCKED tripod, same crop as opening: no zoom, no pan, no travel, "
        "no face-following, no reframe. Full body and loop always inside frame. Same "
        "fixed bright diffuse light throughout with locked exposure/white balance, no "
        "darkening, fade, changing shadow or vignette. No speaking or mouth movement, "
        "no captions, subtitles, marketing cards, added text or watermark. Keep only "
        "original physical product markings. No audio, music or voice. No cuts, "
        "repeated or frozen frames."
    )


def build_configs():
    prior = json.loads(RUNNER.with_name('example-powerbank-portrait-first.json').read_text(encoding='utf-8'))
    portraits = [
        prior['character']['prompt'],
        (
            "Create ONE photorealistic canonical character portrait, vertical 9:16. "
            "A newly invented adult Vietnamese woman aged 30 with a softly angular "
            "face, warm tan skin, dark almond-shaped eyes, straight chin-length BLACK "
            "BOB haircut with a side part. Plain pastel sage-green long-sleeve shirt, "
            "simple collar, no jewelry or visible logos. Head and upper torso clearly "
            "visible, full hair and shoulders, friendly relaxed closed-mouth smile. "
            "Even bright diffuse neutral studio illumination, pale warm-gray background. "
            "Fictional adult, no likeness of a specific real person. One person only. "
            "No product, prop, text, watermark, illustration or collage."
        ),
    ]
    people = [
        "The exact fictional adult woman from canonical reference: low dark ponytail, oval face, cream long-sleeve blouse.",
        "The exact fictional adult woman from canonical reference: chin-length side-part black bob, softly angular face, sage-green long-sleeve shirt.",
    ]
    backgrounds = [
        (
            "Bright pale-oak electronics review counter, warm-white wall and soft "
            "blurred neutral accessory shelves, no signs or readable packaging. "
            "Fixed diffuse studio key and fill at 5200K, no visible window, no "
            "moving sunlight, same bright lighting in all scenes."
        ),
        (
            "Bright modern home workspace, off-white desk, pale blue wall, small "
            "blurred leafy plant and closed plain notebook well away from product. "
            "Fixed large diffuse studio lights at 5200K, no visible window, no "
            "moving sunlight, no signage, consistent neutral exposure."
        ),
    ]
    speeches = [
        [
            "[surprised] Nhìn như hộp phấn, hóa ra sạc dự phòng! [playful] Tím pastel, bo góc xinh ghê, mấy ní!",
            "[upbeat] Vỏ trơn, quai đồng màu, có ô báo mức pin. [explaining] Liếc nhanh để chủ động chuẩn bị trước khi ra ngoài.",
            "[encouraging] Thích kiểu gọn xinh này? Bấm giỏ hàng, kiểm tra thông số, chọn đúng phiên bản rồi chốt đơn nha!",
        ],
        [
            "[excited] Sạc dự phòng mà tím như kẹo! [playful] Bo góc, có quai đồng màu; đặt cạnh đồ đi làm nhìn hợp ghê.",
            "[upbeat] Xoay nhẹ, chạm lớp vỏ trơn nè. [explaining] Ô báo mức pin ở mặt trước giúp mình tiện theo dõi.",
            "[encouraging] Mê màu tím này thì bấm giỏ hàng, xem kỹ thông số, chọn đúng phiên bản rồi đặt mua nha!",
        ],
    ]
    hooks = ["Nhìn như hộp phấn, hóa ra sạc dự phòng!", "Sạc dự phòng mà tím như kẹo!"]
    ctas = [
        "Bấm giỏ hàng, kiểm tra thông số, chọn đúng phiên bản rồi chốt đơn nha!",
        "Mê màu tím này thì bấm giỏ hàng, xem kỹ thông số, chọn đúng phiên bản rồi đặt mua nha!",
    ]
    compositions = [
        (
            "Tight product-first photograph from below the presenter's chin to the "
            "desk. Product prominent on supporting LEFT palm, filling about 65% of "
            "frame width with its full body and loop visible. Right fingertips "
            "beside blank shell ready to touch. Keep realistic palm-sized scale by "
            "moving the camera closer, never enlarging the physical product. "
            "Do not use a medium or waist-up portrait."
        ),
        (
            "Close product photograph cropped from below chin to desktop, same "
            "presenter's sleeves and BOTH hands visible. Product on left palm at "
            "the same original three-quarter front angle, black window near the "
            "lower-right end and loop upper-right as in reference. Right fingertips "
            "poised beside blank shell above the window. Full loop and entire "
            "product within central 65% of frame; generous margins."
        ),
        (
            "Distinct tight three-quarter product close-up from below chin to desk, "
            "same canonical clothing visible, product on supporting left palm, free right hand "
            "beside blank shell. Product lies LOW AND FLAT across the palm, broad "
            "front facing camera at the original diagonal three-quarter angle: "
            "blank lavender shell UPPER-LEFT, black window LOWER-RIGHT, short loop "
            "UPPER-RIGHT. Keep the original squat rounded body proportions. "
            "Never stand the product upright or stretch it into a long thin rectangle. "
            "Entire palm-sized product and loop visible in central 65% of frame. "
            "Friendly closed-mouth smile."
        ),
    ]
    configs = []
    for variant in range(2):
        scenes = []
        for n, dialogue in enumerate(speeches[variant]):
            opening = (
                "Create ONE photorealistic vertical 9:16 product-review opening. "
                "REFERENCE 1 is product crop; REFERENCE 2 is canonical adult identity. "
                + PRODUCT + "\n" + people[variant] + " Same face, hair and clothing "
                "throughout, normal five-finger hands, relaxed closed lips; separate "
                "male voice-over later.\n" + backgrounds[variant] + "\n"
                + compositions[n] + "\n" + NO_TEXT
            )
            video = locked_video_prompt()
            scenes.append({
                "title": ["Hook and reveal", "Tactile design demonstration", "Purchase CTA"][n],
                "seconds": 20/3, "visual_speed": 1.5,
                "dialogue": dialogue, "opening_prompt": opening,
                "video_prompt": video, "action_timeline": ACTION,
            })
        configs.append({
            "recipe_version": 5, "duration_seconds": 20, "visual_speed": 1.5,
            "text_overlays": False, "product_crop": [.145, .015, .6, .4],
            "product_description": PRODUCT,
            "character": {"reference": "character/portrait.png", "prompt": portraits[variant]},
            "quality": {
                "lock_exposure": True, "require_video_review": True,
                "exposure_lock": {"enabled": True, "max_brightness": .07,
                                  "allow_dimming": False, "roi": [.1, .1, .9, .9]},
            },
            "cache": {"muse": True, "tts": True},
            "claim_basis": {
                "source": "Supplied collage only; lavender product selected.",
                "observed": ["pastel lavender shell", "rounded corners", "matching loop", "black level window"],
                "unverified_and_excluded": ["price", "capacity", "power", "charging protocols", "certification", "real user experience"],
            },
            "clips": [{
                "slug": ["lavender-reveal", "lavender-desk"][variant],
                "presentation_mode": "presenter", "background": backgrounds[variant],
                "presenter": people[variant], "dialogue": "\n\n".join(speeches[variant]),
                "scenes": scenes,
                "marketing": {
                    "hook": hooks[variant], "hook_seconds": 3,
                    "buyer_benefit": "A coordinated pastel design with a front-facing level window for convenient visual checking.",
                    "reason_to_believe": "Features visible in supplied image, demonstrated with hand contact; no unverified technical performance.",
                    "cta": ctas[variant],
                },
            }],
        })
    return configs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    for index, config in enumerate(build_configs(), 1):
        manifest = output/f'variant-{index:02}-config.json'
        manifest.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
        subprocess.run([sys.executable, str(RUNNER), 'init', '--config', str(manifest),
                        '--image', args.image, '--output', str(output/f'variant-{index:02}')], check=True)
    (output/'README.md').write_text(
        '# Hai video sạc dự phòng — 20 giây mỗi bản\n\n'
        'Hai nhân vật trưởng thành hư cấu, hai bối cảnh, mỗi bản ba nguồn 10 giây '
        'ở tốc độ hình 1,5×. Adam / eleven_v3, không chèn chữ. '
        'Chỉ dùng đặc điểm thấy trong ảnh, không suy đoán thông số hoặc giá.\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
