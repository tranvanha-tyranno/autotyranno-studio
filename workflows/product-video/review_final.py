"""Build opening/raw/final comparisons and measured QA; never auto-approve visuals."""
import argparse
import hashlib
import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw


def review(batch):
    spec = importlib.util.spec_from_file_location('product_runner', Path(__file__).with_name('run.py'))
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    storyboard = runner.storyboard_module()
    quality = storyboard.quality_module()
    config = runner.read_json(batch/'batch.json')
    for i, clip in enumerate(config['clips'], 1):
        folder = runner.clip_path(batch, i, clip)
        final = folder/'final.mp4'
        scenes = clip['scenes']
        canvas = Image.new('RGB', (5*180, len(scenes)*344), 'white')
        draw = ImageDraw.Draw(canvas)
        offset, rows, hashes = 0., [], []
        for n, scene in enumerate(scenes, 1):
            sf = storyboard.folder(runner, batch, i, clip, n)
            speed = scene.get('visual_speed', clip.get('visual_speed', config.get('visual_speed', 1.5)))
            start, seconds = scene.get('source_start', 0), scene['seconds']
            used_end = start+seconds*speed-.12
            opening = Image.open(sf/'opening.png').convert('RGB').resize((180, 320))
            opening_luma = quality.luma(opening)
            raw_end = quality.sample_frame(runner.FF, sf/'source.mp4', used_end, (180, 320))
            detail = Image.new('RGB', (1080, 664), 'white')
            detail_draw = ImageDraw.Draw(detail)
            detail_times = [
                start+(seconds*speed)*fraction for fraction in (.25, .5, .75)
            ]
            for column, t in enumerate(detail_times):
                image = quality.sample_frame(runner.FF, sf/'source.mp4', t, (360, 640))
                detail.paste(image, (column*360, 24))
                detail_draw.text((column*360+5, 5), f'Source {n} at {t:.2f}s', fill='black')
            detail.save(sf/'source-detail-review.jpg', quality=95)
            sample_times = [.1, seconds/2, seconds-.15]
            processed = [
                quality.sample_frame(runner.FF, final, offset+t, (180, 320))
                for t in sample_times
            ]
            images = [opening, raw_end]+processed
            labels = ['opening', f'raw {used_end:.1f}s', 'final start', 'final middle', 'final end']
            for x, (im, label) in enumerate(zip(images, labels)):
                canvas.paste(im, (x*180, (n-1)*344+24))
                draw.text((x*180+4, (n-1)*344+5), f'{n}: {label}', fill='black')
            source_hash = hashlib.sha256((sf/'source.mp4').read_bytes()).hexdigest()
            hashes.append(source_hash)
            receipt = runner.read_json(sf/'video-review.json')
            if not receipt.get('result', '').startswith('accepted') or receipt.get('source_sha256') != source_hash:
                raise ValueError('Stale/rejected source review: '+str(sf))
            audio = storyboard.voice_folder(runner, sf)/'voice.mp3'
            audio_review_path = sf/'audio-timing-review.json'
            if audio_review_path.exists():
                audio_review = runner.read_json(audio_review_path)
                if audio_review['voice_sha256'] != hashlib.sha256(audio.read_bytes()).hexdigest():
                    raise ValueError('Narration timing belongs to another take')
            rows.append({
                'scene': n, 'role': scene.get('title'), 'offset_seconds': offset,
                'duration_seconds': seconds, 'visual_speed': speed,
                'source_seconds_used': [start, start+seconds*speed],
                'source_sha256': source_hash, 'review_result': receipt['result'],
                'enlarged_source_detail_sheet': str((sf/'source-detail-review.jpg').relative_to(batch)),
                'source_detail_times': detail_times,
                'reference_opening_luma': opening_luma,
                'raw_selected_end_opening_ratio': quality.luma(raw_end)/max(1, opening_luma),
                'corrected_samples': [
                    {'scene_seconds': t, 'opening_luma_ratio': quality.luma(im)/max(1, opening_luma)}
                    for t, im in zip(sample_times, processed)
                ],
                'limitations': 'ROI includes skin, product and background. Composition changes affect mean; inspect product/skin/black window in the actual comparison before acceptance.',
            })
            offset += seconds
        if len(set(hashes)) != len(scenes):
            raise ValueError('Repeated source within one output')
        canvas.save(folder/'opening-raw-final-comparison.jpg', quality=94)
        runner.save_json(folder/'corrected-final-review.json', {
            'final_sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
            'distinct_sources': len(set(hashes)), 'visual_review': 'pending agent inspection',
            'comparison': 'opening-raw-final-comparison.jpg', 'scenes': rows,
        })
        print('REVIEW_SHEET', folder/'opening-raw-final-comparison.jpg')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    review(Path(args.batch).resolve())
