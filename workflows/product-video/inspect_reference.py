"""Inspect a local reference without provider calls; measurements are not lip-sync QA."""
import argparse
import hashlib
import importlib.util
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageStat
import imageio_ffmpeg


def inspect(source, output):
    output.mkdir(parents=True, exist_ok=False)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    spec = importlib.util.spec_from_file_location('product_runner', Path(__file__).with_name('run.py'))
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    duration = runner.duration(source)
    # A single full decode, sampled four times a second. Small decoded buffers.
    result = subprocess.run([ff, '-hide_banner', '-i', str(source), '-an', '-vf',
                             'fps=4,scale=144:256', '-pix_fmt', 'rgb24',
                             '-f', 'rawvideo', 'pipe:1'], capture_output=True, check=True)
    frame_bytes = 144*256*3
    frames = [Image.frombytes('RGB', (144, 256), result.stdout[n:n+frame_bytes])
              for n in range(0, len(result.stdout)-frame_bytes+1, frame_bytes)]
    sheet = Image.new('RGB', (8*144, math.ceil(len(frames)/8)*278), '#202020')
    draw = ImageDraw.Draw(sheet)
    differences = []
    for n, image in enumerate(frames):
        x, y = n % 8*144, n//8*278
        sheet.paste(image, (x, y+22))
        draw.text((x+4, y+4), f'{n/4:.2f}s', fill='white')
        if n:
            delta = ImageStat.Stat(ImageChops.difference(frames[n-1], image).convert('L')).mean[0]
            differences.append({'seconds': n/4, 'mean_absolute_difference': round(delta, 3)})
    sheet.save(output/'quarter-second-sheet.jpg', quality=94)
    audio = subprocess.run([ff, '-hide_banner', '-i', str(source), '-vn',
                            '-af', 'volumedetect', '-f', 'null', '-'],
                           capture_output=True, text=True, check=True)
    (output/'audio-levels.txt').write_text(audio.stderr, encoding='utf-8')
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(source), '-vn', '-ac', '1',
                    '-ar', '16000', str(output/'reference-audio.wav')], capture_output=True, check=True)
    runner.save_json(output/'inspection.json', {
        'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'seconds': duration, 'full_decode': 'passed', 'sample_period_seconds': .25,
        'sampled_frames': len(frames),
        'largest_visual_changes': sorted(differences, key=lambda x: x['mean_absolute_difference'], reverse=True)[:12],
        'scope': 'Visual samples and audio-level measurements only. No transcript or objective lip-sync score. '
                 'Mouth motion in frames cannot prove synchronization; audiovisual review is required.',
        'provider_calls': 0,
    })
    print('REFERENCE_INSPECTED', output, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    inspect(args.video.resolve(), args.output.resolve())
