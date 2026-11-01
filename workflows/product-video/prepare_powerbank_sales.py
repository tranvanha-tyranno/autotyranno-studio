"""Prepare two forty-second sales edits with stable, product-led storyboards.

Each output uses three inspected existing sources and three new context shots.
This step makes no provider calls and keeps all source provenance.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from prepare_powerbank_variants import PRODUCT, NO_TEXT, locked_video_prompt

ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).with_name('run.py')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def source_folder(batch, clip, n):
    revision = clip['scenes'][n-1].get('revision', 1)
    return batch/('clip-01-'+clip['slug'])/(
        f'scene-{n:02}'+(f'-r{revision:02}' if revision > 1 else ''))


SPEECH = [
    [
        "[surprised] Không phải hộp phấn, là pin dự phòng! [playful] Tím pastel này hợp team mê đồ công nghệ xinh mà có việc để dùng.",
        "[upbeat] Đi làm, chờ xe hay ngồi cà phê, chưa tiện cắm ổ điện? Có nguồn sạc mang theo sẽ chủ động hơn cho điện thoại.",
        "[playful] Cận hơn nè: thân bo góc, vỏ trơn, quai đồng màu. Đặt cùng đồ mang đi vừa hợp tông, vừa dễ nhận ra chiếc sạc của mình.",
        "[explaining] Ô báo mức pin nằm ngay mặt trước, tiện nhìn trước khi ra ngoài. Nhớ nạp lại sạc dự phòng để lúc cần còn có pin nha.",
        "[confident] Chọn phiên bản hợp điện thoại nhé: xem dung lượng, công suất và cổng kết nối trong giỏ hàng. Phù hợp nhu cầu thì mua sẽ đáng hơn.",
        "[encouraging] Muốn có nguồn pin mang theo mà vẫn hợp gu? Mở giỏ hàng, xem thông số, chọn đúng phiên bản rồi đặt mua nha, mấy ní!",
    ],
    [
        "[excited] Ô báo pin nằm ngay mặt trước! [playful] Còn thân tím pastel này nhìn như món phụ kiện, đặt cạnh điện thoại là có điểm nhấn.",
        "[upbeat] Di chuyển nhiều, không phải lúc nào cũng có ổ điện gần mình. Một chiếc sạc dự phòng giúp chủ động nguồn sạc mang theo.",
        "[playful] Xem gần nè: thân bo góc, quai tím cùng tông, bề mặt trơn. Team thích đồ phối màu chắc sẽ để ý em này đó!",
        "[explaining] Trước buổi làm việc hay buổi hẹn, liếc ô báo để kiểm tra mức pin. Chuẩn bị trước, lúc cần lấy ra dùng sẽ tiện hơn.",
        "[confident] Trong giỏ hàng, xem dung lượng và công suất của đúng phiên bản; kiểm tra cổng phù hợp với điện thoại. Chọn đúng nhu cầu rồi mua nha.",
        "[encouraging] Đang tìm sạc dự phòng kiểu này? Mở giỏ hàng, xem đúng thông số, chọn phiên bản phù hợp, chọn màu mình thích rồi đặt mua nha!",
    ],
]

HOOKS = [
    "Không phải hộp phấn, là pin dự phòng!",
    "Ô báo pin nằm ngay mặt trước!",
]
CTAS = [
    "Mở giỏ hàng, xem thông số, chọn đúng phiên bản rồi đặt mua nha, mấy ní!",
    "Mở giỏ hàng, xem đúng thông số, chọn phiên bản phù hợp, chọn màu mình thích rồi đặt mua nha!",
]

SCENE_ROLES = [
    "Immediate concrete reveal",
    "Buyer situation: portable power away from a wall outlet",
    "Visible design and coordinated accessories",
    "Front level window: check before leaving",
    "Right variant and phone compatibility",
    "Clear purchase close",
]


def new_scene_prompt(variant, number):
    clothing = 'cream long-sleeve blouse' if variant == 1 else 'sage-green long-sleeve shirt'
    hair = 'low dark ponytail' if variant == 1 else 'chin-length black bob'
    background = (
        'pale oak counter and softly blurred warm-white shelves'
        if variant == 1 else
        'off-white desk, pale blue wall and soft blurred leafy plant'
    )
    context = {
        2: (
            'An unbranded black smartphone lies FACE DOWN on the desk, separate '
            'from the power bank by 12 cm. A plain cream fabric tote is softly '
            'out of focus in the far background, no lettering. Nothing connected.'
        ),
        4: (
            'The original glossy black level window is clearly readable as a '
            'physical product detail, not an added graphic. The free hand is poised '
            'beside the blank lavender shell well ABOVE the window; it never points '
            'at or covers the window. Plain desk with no other foreground object.'
        ),
        6: (
            'A distinct clean three-quarter closing composition, power bank centered '
            'on the supporting palm above the desk, free fingertips relaxed beside '
            'the blank shell. One plain closed notebook and FACE-DOWN unbranded '
            'smartphone stay separate in far background. No cable or charger.'
        ),
    }[number]
    prompt = (
        'Create ONE photorealistic vertical 9:16 product review photograph. '
        'Reference 1 locks the original product. Reference 2 locks the fictional '
        'adult identity and clothing.\n'+PRODUCT+'\n'
        'TIGHT PRODUCT CLOSE-UP, camera framing from BELOW CHIN to desk, eyes and '
        'most of face outside frame. Same adult woman, '+hair+', '+clothing+
        '. Do not change her identity if a small lower face is visible. '
        'Realistic small product on supporting LEFT palm, free RIGHT hand beside '
        'blank lavender shell. Product body plus loop fills about 60–65% of frame '
        'width, with at least 15% margins. All product edges and the ENTIRE short '
        'loop remain visible. Two plausible hands, relaxed fingers, no jewelry. '
        'The shell lies low in the original diagonal three-quarter pose; black '
        'window lower-right and single original loop upper-right. Camera moves '
        'closer for a macro view; do not physically enlarge or elongate the product.\n'
        +context+'\nBackground: '+background+
        '. Bright diffuse fixed key and fill at neutral 5200K. No window, moving '
        'sunlight, hard shadow, vignette, dramatic grade or specular glare. Same '
        'brightness and white balance on shell, skin and shirt throughout.\n'+NO_TEXT
    )
    video = locked_video_prompt()+'\nContext stays static: '+context+(
        '\nKeep the close product framing from first frame; never widen to show '
        'the whole presenter. The separate phone is face-down and unconnected; '
        'no imagined charging animation, percentage change, cables or hidden ports.'
    )
    return prompt, video


def prepare(previous, output):
    output.mkdir(parents=True, exist_ok=False)
    research = {
        'checked_date': '2026-10-28',
        'source': 'https://en.yiwugo.com/product/detail/985643339.html',
        'identity': 'Visually matching ym-931-style supplier listing; supplied exact unit unverified.',
        'supplier_claims_not_used_as_exact_unit_specs': ['10000/20000 mAh options', '10 W', 'four rear cables'],
        'spoken_claims': [
            'Visible lavender shell, rounded corners, smooth surface, matching loop, black level window.',
            'General power-bank use: carry a power source when a wall outlet is inconvenient.',
            'Check actual variant capacity, power and phone connector compatibility before purchasing.',
        ],
        'excluded': ['price/discount', 'stock scarcity', 'PD/QC', 'fast-charge promises',
                     'recharge count', 'exact unit capacity/power', 'invented charging demo',
                     'first-person usage testimonial', 'unseen rear or cables'],
    }
    save(output/'research.json', research)
    for variant in (1, 2):
        old = previous/f'variant-{variant:02}'
        old_config = read(old/'batch.json')
        old_clip = old_config['clips'][0]
        config = copy.deepcopy(old_config)
        config.pop('references', None)
        config.pop('created_at', None)
        config.pop('product_image_sha256', None)
        config.pop('composition_update', None)
        config.pop('motion_revision_notes', None)
        config['duration_seconds'] = 40
        config['product_crop'] = [.145, .015, .6, .4]
        config['research'] = research
        config['quality']['exposure_lock'].update(
            preserve_blacks=True, black_floor=.12, black_transition=.32)
        config['quality']['final_review_required'] = True
        scenes = []
        for n, text in enumerate(SPEECH[variant-1], 1):
            if n in (1, 3, 5):
                source_n = {1: 1, 3: 2, 5: 3}[n]
                scene = copy.deepcopy(old_clip['scenes'][source_n-1])
                for field in ('revision', 'audio_segments', 'audio_edit_notes'):
                    scene.pop(field, None)
                scene['reuse_visual_from'] = str(source_folder(old, old_clip, source_n).relative_to(ROOT))
            else:
                image, video = new_scene_prompt(variant, n)
                scene = {'opening_prompt': image, 'video_prompt': video}
            scene.update(title=SCENE_ROLES[n-1], seconds=40/6, visual_speed=1.5,
                         dialogue=text, source_start=0)
            scenes.append(scene)
        clip = {
            'slug': 'lavender-sales-cream' if variant == 1 else 'lavender-sales-sage',
            'presentation_mode': 'presenter',
            'background': old_clip['background'],
            'presenter': old_clip['presenter'],
            'dialogue': '\n\n'.join(SPEECH[variant-1]),
            'scenes': scenes,
            'marketing': {
                'hook': HOOKS[variant-1], 'hook_seconds': 3,
                'buyer_benefit': 'A portable power source for time away from convenient wall outlets, with a visible front level window and coordinated lavender design.',
                'reason_to_believe': 'Product-led close-up footage, real shell contact, visible front/loop and contextual separate phone; no unsupported performance claim.',
                'cta': CTAS[variant-1],
                'story_arc': SCENE_ROLES,
                'no_fabricated_testimonial': True,
            },
        }
        config['clips'] = [clip]
        config['improvement_intent'] = {
            'user_feedback': 'Longer, more persuasive, more stable and relevant to buying a power bank.',
            'editorial': 'Six distinct story beats; practical portable-power context and variant fit, not repeated shell rubbing with generic beauty claims.',
            'visuals': 'Three accepted sources retained without repeating within output; three distinct new context sources.',
            'stability': 'Canonical identity, original diagonal product pose, whole loop, locked supporting grip, bounded exposure correction with black preservation.',
        }
        manifest = output/f'variant-{variant:02}-config.json'
        save(manifest, config)
        batch = output/f'variant-{variant:02}'
        subprocess.run([sys.executable, str(RUNNER), 'init', '--config', str(manifest),
                        '--image', str(old/'input/original.png'), '--output', str(batch)], check=True)
        # Preserve the previously generated and inspected separate canonical portrait.
        shutil.copytree(old/'character', batch/'character')
        for n, scene in enumerate(scenes, 1):
            if not scene.get('reuse_visual_from'):
                continue
            origin = ROOT/scene['reuse_visual_from']
            target = batch/('clip-01-'+clip['slug'])/f'scene-{n:02}'
            for name in ['opening.png', 'opening-review.json', 'source.mp4',
                         'source-task.json', 'opening-task.json', 'action-sheet.jpg',
                         'contact-sheet.jpg', 'video-review.json']:
                if (origin/name).exists():
                    shutil.copy2(origin/name, target/name)
            save(target/'reuse-provenance.json', {
                'source_scene': str(origin.relative_to(ROOT)),
                'source_sha256': hashlib.sha256((target/'source.mp4').read_bytes()).hexdigest(),
                'reason': 'Keep already reviewed stable motion; new script and independent narration.',
                'provider_calls_for_reuse': 0,
            })
        (batch/'LOI-DOC.txt').write_text(clip['dialogue'], encoding='utf-8')
    (output/'README.md').write_text(
        '# Hai bản bán hàng 40 giây\n\n'
        'Sáu cảnh mỗi bản: hook cụ thể → ngữ cảnh cần nguồn pin → thiết kế → '
        'ô báo mức pin → chọn phiên bản → CTA. Ba nguồn đã duyệt + ba nguồn '
        'ngữ cảnh mới ở mỗi bản; không lặp/kéo chậm. Giọng Adam / eleven_v3; '
        'không chữ chèn. Thông số của listing giống ngoại hình không được '
        'coi là thông số của đúng chiếc trong ảnh. Nguồn và claim lưu ở research.json.\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    prepare(Path(args.previous).resolve(), Path(args.output).resolve())
