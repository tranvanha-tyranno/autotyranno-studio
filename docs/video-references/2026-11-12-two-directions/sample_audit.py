"""Reproduce sparse visual evidence; this does not certify full AV viewing."""
from pathlib import Path
import json
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-11-11'
SAMPLES = {
    'JlfAd_OaFek': [0, 2, 5, 12, 20, 32, 35, 39, 43, 46, 1070, 1075],
    'podWgLH4b3M': [0, 3, 10, 20, 35, 58, 62, 65, 68, 70, 980, 987],
    'w3z43Hlzq3c': [0, 3, 10, 20, 35, 56, 60, 64, 69, 72, 1246, 1250],
    '29B8-FtuC6U': [0, 3, 10, 20, 45, 82, 86, 90, 94, 98, 880, 892],
    '5zqAMK2qsfM': [0, 3, 10, 20, 45, 79, 83, 87, 91, 95, 1274, 1288],
    '5uTC396kCs4': [0, 3, 10, 20, 45, 92, 96, 100, 104, 108, 1300, 1319],
}

for video_id, times in SAMPLES.items():
    source_dir = HERE / video_id
    if not (source_dir / 'reference.mp4').exists():
        source_dir = OLD / video_id
    folder = HERE / 'targeted-samples' / video_id
    folder.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1600, 3 * 250), '#171717')
    draw = ImageDraw.Draw(sheet)
    for i, time in enumerate(times):
        frame = folder / f'{time:07.2f}.jpg'
        subprocess.run([
            imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y',
            '-ss', str(time), '-i', str(source_dir / 'reference.mp4'),
            '-frames:v', '1', '-vf', 'scale=400:225', str(frame),
        ], check=True, capture_output=True)
        with Image.open(frame) as image:
            sheet.paste(image, ((i % 4) * 400, (i // 4) * 250 + 25))
        draw.text(((i % 4) * 400 + 5, (i // 4) * 250 + 5), f'{time:.2f}s', fill='white')
    sheet.save(folder / 'targeted-contact-sheet.jpg', quality=92)
    (folder / 'sample-times.json').write_text(json.dumps(times), encoding='utf-8')
print('Created six targeted contact sheets; sparse inspection only.')
