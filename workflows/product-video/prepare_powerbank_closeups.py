"""Use approved local takes and a tighter product-first composition after motion QA.

No provider calls. Originals, rejected attempts and task IDs remain in place.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

from PIL import Image
from prepare_powerbank_variants import locked_video_prompt

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT/'videos/2026-10-28-powerbank-feedback-v2-42s'
OLD_CLIP = OLD/'clip-01-lavender-tactile-review'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def scene_path(batch, clip, number):
    revision = clip['scenes'][number-1].get('revision', 1)
    return batch/('clip-01-'+clip['slug'])/(
        f'scene-{number:02}'+(f'-r{revision:02}' if revision > 1 else ''))


def prepare(root):
    known = read(OLD/'batch.json')
    prompt = locked_video_prompt()
    for variant in (1, 2):
        batch = root/f'variant-{variant:02}'
        config = read(batch/'batch.json')
        backup = batch/'batch-before-closeups.json'
        if backup.exists():
            raise ValueError('Close-up preparation already exists; resume its stages.')
        shutil.copy2(batch/'batch.json', backup)
        clip = config['clips'][0]
        for n, scene in enumerate(clip['scenes'], 1):
            prior = scene_path(batch, clip, n)
            # Two full, distinct, inspected ten-second sources of the visually
            # matched lavender unit; original product photograph retained too.
            reusable = variant == 1 and n in (2, 3)
            original_scene = OLD_CLIP/('scene-02-r02' if n == 2 else 'scene-03-r02')
            scene['revision'] = scene.get('revision', 1)+1
            target = scene_path(batch, clip, n)
            target.mkdir()
            if reusable:
                for name in ('opening.png', 'source.mp4', 'action-sheet.jpg',
                             'contact-sheet.jpg', 'opening-task.json', 'source-task.json'):
                    if (original_scene/name).exists():
                        shutil.copy2(original_scene/name, target/name)
                opening = known['clips'][0]['scenes'][n-1]['opening_prompt']
                scene['opening_prompt'] = opening
                scene['video_prompt'] = prompt
                save(target/'reuse-provenance.json', {
                    'source_batch': str(OLD.relative_to(ROOT)),
                    'source_scene': str(original_scene.relative_to(ROOT)),
                    'source_sha256': hashlib.sha256((target/'source.mp4').read_bytes()).hexdigest(),
                    'original_review': read(original_scene/'video-review.json'),
                    'reference_match': 'Agent visually compared lavender shell, black window, original loop and supplied collage. Original screenshot bytes differ; no exact-file identity claim.',
                    'provider_calls': 0,
                    'reason': 'Reuse separately inspected close-up motion retaining diagonal pose rather than repeatedly billing failed medium-portrait poses.',
                })
            else:
                # Crop a scene image already generated using product + its own
                # canonical portrait; no new identity or synthetic product edit.
                with Image.open(prior/'opening.png') as im:
                    w, h = im.size
                    top = round(h*.36)
                    height = h-top
                    width = round(height*9/16)
                    left = round(w*.04)
                    im.crop((left, top, left+width, h)).resize((720, 1280)).save(target/'opening.png')
                scene['opening_prompt'] = (
                    'Deterministic 9:16 crop of previously generated canonical scene opening; '
                    'left=4% of width, top=36% of height, preserve aspect ratio to bottom. '
                    'Product and full loop retained, no invented pixels. Source: '+str(prior.relative_to(ROOT)))
                scene['video_prompt'] = prompt.replace('cream blouse', 'sage-green shirt') if variant == 2 else prompt
                save(target/'crop-provenance.json', {
                    'source_image': str((prior/'opening.png').relative_to(ROOT)),
                    'source_sha256': hashlib.sha256((prior/'opening.png').read_bytes()).hexdigest(),
                    'crop_pixels': [left, top, left+width, h],
                    'output_size': [720, 1280], 'provider_calls': 0,
                })
            scene['action_timeline'] = (
                'Free hand moves immediately; brief settling; tiny 3-degree depth yaw, '
                'same palm/grip; fingers actually stroke blank shell around 3–6s then release. '
                'Maintain original diagonal product pose, black window and short single loop.')
            for filename, key in [('opening-prompt.txt', 'opening_prompt'),
                                  ('video-prompt.txt', 'video_prompt'), ('dialogue.txt', 'dialogue')]:
                (target/filename).write_text(scene[key], encoding='utf-8')
        config['composition_update'] = (
            'Three distinct close product shots per output. Variant 1 uses two explicitly '
            'provenanced locally approved sources of the visually matched unit. Remaining '
            'sources start from deterministic tight crops of their own canonical scene '
            'images with the motion prompt previously validated on close-ups. No loop, '
            'slowdown or rejected medium-pose source is used.')
        save(batch/'batch.json', config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch-root', required=True)
    args = parser.parse_args()
    prepare(Path(args.batch_root).resolve())
