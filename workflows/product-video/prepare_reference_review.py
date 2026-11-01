"""Prepare two audio-first power-bank talking-review manifests; no provider calls."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

from prepare_powerbank_variants import PRODUCT, NO_TEXT
from talking_review import STYLE

RUNNER = Path(__file__).with_name('run.py')
SCRIPTS = [
    [
        '[surprised] Hộp phấn gì? PIN DỰ PHÒNG đó!',
        '[playful] Cận nè: thân tím bo góc, quai cùng màu.',
        '[upbeat] Đi làm hay đi cà phê, có nguồn pin mang theo thì chủ động hơn lúc chưa tiện cắm ổ điện.',
        '[explaining] Ô báo ngay mặt trước, liếc kiểm tra trước khi ra ngoài.',
        '[encouraging] Hợp gu chưa? Mở giỏ hàng, xem thông số, chọn đúng phiên bản rồi đặt mua nha!',
    ],
    [
        '[surprised] Khoan! Cục tím này là SẠC DỰ PHÒNG!',
        '[playful] Bo góc, quai tím, ô đen ngay mặt trước.',
        '[upbeat] Mê đồ công nghệ hợp tông mà vẫn có việc để dùng? Đây là nguồn pin mang theo khi chưa tiện tìm ổ điện.',
        '[explaining] Liếc ô báo để kiểm tra mức pin trước khi mang đi nha.',
        '[encouraging] Thích màu này thì mở giỏ hàng, xem thông số, chọn phiên bản hợp điện thoại rồi đặt mua nha!',
    ],
]
HOOKS = ['Hộp phấn gì? PIN DỰ PHÒNG đó!', 'Khoan! Cục tím này là SẠC DỰ PHÒNG!']
CTAS = [
    'Mở giỏ hàng, xem thông số, chọn đúng phiên bản rồi đặt mua nha!',
    'Thích màu này thì mở giỏ hàng, xem thông số, chọn phiên bản hợp điện thoại rồi đặt mua nha!',
]
BEATS = ['hook', 'proof', 'benefit', 'use_case', 'cta']
SECONDS = [3, 3, 5, 4, 5]
ACTIONS = [
    'The existing free hand makes one brief surprised open-palm gesture beside the product, then settles',
    'The existing free fingertips touch the blank shell and stroke once by 1 cm after a brief natural settling pause; the supporting hand permits only one 3-degree depth tilt',
    'The existing free hand makes one small open-palm presenting gesture toward the separate face-down phone on the desk',
    'The existing free index finger approaches and stops BESIDE the black level window, leaving it unobstructed',
    'The existing free hand gives one small inviting palm-up gesture while the supporting palm keeps the product steady',
]


def build_configs():
    configs = []
    for variant in range(2):
        identity = [
            'A fictional adult Vietnamese man aged 29, short neat black hair, oval face, warm medium skin, plain cream polo shirt',
            'A different fictional adult Vietnamese man aged 32, short textured dark hair, softly angular face, plain sage-green shirt',
        ][variant]
        background = [
            'Bright pale-oak electronics review desk, warm-white shelves softly blurred, no readable signs',
            'Bright modern desk, pale-blue wall, soft blurred plant and a plain cream tote in the background',
        ][variant]
        portrait = (
            'Create one photorealistic canonical adult portrait, 9:16. '+identity+
            '. Face, hair and shoulders fully visible, looking toward camera, even neutral diffuse '
            '5200K light, natural skin, relaxed expression, no glasses, no product or props. '
            'Invent a new face, do not resemble the performer in a reference clip. '+NO_TEXT
        )
        scenes = []
        for n, dialogue in enumerate(SCRIPTS[variant]):
            talking = n != 1
            composition = (
                'Stable medium-close frame, full face and mouth clearly visible, eyes toward lens. '
                'Product below the chin, far from mouth, held LOW AND FLAT on supporting left palm '
                'above desk. Leave clear space around mouth and both hands.'
                if talking else
                'Tight product close-up, face entirely out of frame, same shirt and hands. '
                'Complete body and single short loop within central 65% of frame.'
            )
            opening = (
                'Create one photorealistic 9:16 opening. Reference 1 locks product, reference 2 '
                'locks canonical fictional adult. '+identity+'. '+PRODUCT+'\n'+composition+
                '\n'+background+'. Fixed diffuse key and fill, stable neutral 5200K, no visible window. '
                'Exactly TWO hands, existing supporting left palm and existing free right hand. '
                'Separate unbranded face-down phone on desk, unconnected. '+NO_TEXT
            )
            video = (
                'One continuous 10-second 9:16 source shot, exact opening in image 1, product in '
                'image 2, canonical adult in image 3. Locked tripod and identical exposure/white '
                'balance. '+PRODUCT+' Supporting palm, grip and wrist remain still; do not stand '
                'the product upright, flip, roll, reveal rear, change digits or add a loop. Exactly '
                'the TWO existing hands; no duplicate hand left on desk. '+ACTIONS[n]+'. '
                'Begin the action within the first half second. No reframing, darkening or fade. '+
                (
                    'Keep the entire face visible, natural expressive eyebrows and small head movement, '
                    'unobstructed mouth facing lens. This is a TALKING presenter shot, not silent closed-mouth '
                    'B-roll. Exact Vietnamese mouth motion will be driven by the FINAL timed audio in a '
                    'separate actual lip-sync stage; random mouth motion is not synchronization. '
                    if talking else
                    'Product B-roll with offscreen narration; keep face out of this close-up. '
                )+NO_TEXT
            )
            scenes.append({
                'title': BEATS[n], 'beat': BEATS[n], 'seconds': SECONDS[n],
                'visual_speed': 1. if talking else 1.5,
                'speech_mode': 'lip_sync' if talking else 'voiceover',
                'face_visible': talking, 'visible_action': ACTIONS[n],
                'dialogue': dialogue, 'opening_prompt': opening, 'video_prompt': video,
            })
        configs.append({
            'recipe_version': 6, 'reference_style': STYLE,
            'duration_seconds': 20, 'text_overlays': False, 'visual_speed': 1.,
            'product_description': PRODUCT, 'product_crop': [.145, .015, .6, .4],
            'character': {'reference': 'character/portrait.png', 'prompt': portrait},
            'quality': {
                'lock_exposure': True, 'require_video_review': True, 'final_review_required': True,
                'exposure_lock': {'enabled': True, 'max_brightness': .07, 'allow_dimming': False,
                                  'roi': [.1, .1, .9, .9], 'preserve_blacks': True,
                                  'black_floor': .12, 'black_transition': .32},
            },
            'cache': {'muse': True, 'tts': True},
            'reference_learning': {
                'sample': 'viesnap.vn_tiktok_7693215191420456212.mp4',
                'priority': 'Most runtime shows a presenter whose mouth matches the exact spoken audio.',
                'transfer': 'Surprise → product pitch; expressive performer, steady camera, purposeful hand actions.',
                'do_not_copy': 'Real performer identity, unrelated wall-breaking skit, captions, black bars, fades.',
                'lip_sync_engine': 'not_connected; current local Muse VideoRequest has no audio input',
            },
            'claim_basis': {
                'source': 'Supplied image; lavender product crop',
                'visible': ['lavender rounded shell', 'single matching loop', 'black front level window'],
                'excluded': ['price', 'capacity', 'wattage', 'charge count', 'unseen cables', 'first-person testimonial'],
            },
            'clips': [{
                'slug': 'talking-lavender-'+('cream' if variant == 0 else 'sage'),
                'presentation_mode': 'presenter', 'presenter': identity, 'background': background,
                'dialogue': '\n\n'.join(SCRIPTS[variant]), 'scenes': copy.deepcopy(scenes),
                'marketing': {
                    'hook': HOOKS[variant], 'hook_seconds': 3, 'cta': CTAS[variant],
                    'buyer_benefit': 'Carry a power source when an outlet is inconvenient; check front level window.',
                    'reason_to_believe': 'Visible product details and general power-bank use; exact performance unverified.',
                },
            }],
        })
    return configs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    for n, config in enumerate(build_configs(), 1):
        manifest = output/f'variant-{n:02}-config.json'
        manifest.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
        subprocess.run([sys.executable, str(RUNNER), 'init', '--config', str(manifest),
                        '--image', args.image, '--output', str(output/f'variant-{n:02}')], check=True)
    (output/'README.md').write_text(
        '# Bản chuẩn bị theo video mẫu — chưa sinh video\n\n'
        'Hai bản 20 giây, mỗi bản 17 giây nhân vật nam trưởng thành hư cấu nói trực tiếp '
        '(Adam / eleven_v3) và 3 giây cận sản phẩm. Không chèn chữ. '
        'Mạch: hook → chi tiết cận → lợi ích → ô báo pin → CTA. '
        'Các hành động tay khác nhau, chỉ một cảnh miết vỏ. Cảnh nói ở 1×; '
        'cận sản phẩm 1,5×. Tất cả chỉ là manifest/prompt, chưa có hình hoặc video mới.\n\n'
        'API Muse local chưa nhận audio điều khiển khẩu hình. Sau khi có nguồn được QA và TTS, '
        'talking_review.py chuẩn bị hình/tiếng ở thời gian cuối để đưa qua engine lip-sync thực. '
        'Render chặn nếu chưa có synced.mp4 và review khớp hash. Số call lip-sync/giá chưa xác định.\n',
        encoding='utf-8')


if __name__ == '__main__':
    main()
