from pathlib import Path
import json
import cv2
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa'
capture = cv2.VideoCapture(str(ROOT / 'final.mp4'))
records = []
pages = []
for page_start in range(3, 82, 27):
    times = list(range(page_start, min(page_start + 27, 82), 3))
    sheet = Image.new('RGB', (960, len(times) * 204), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for row, second in enumerate(times):
        group = {'second': second, 'frames': []}
        for col, frame in enumerate([second * 30 - 1, second * 30, second * 30 + 1]):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, bgr = capture.read()
            if not ok:
                raise RuntimeError(f'Cannot decode frame {frame}')
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(rgb).resize((320, 180))
            sheet.paste(im, (col * 320, row * 204 + 24))
            draw.text((col * 320 + 7, row * 204 + 5), f'{second}s | frame {frame}', fill='#000000')
            group['frames'].append({'frame': frame, 'meanLuma': float(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).mean())})
        records.append(group)
    filename = f'chunk-boundaries-{len(pages)+1:02}.jpg'
    sheet.save(OUT / filename, quality=90)
    pages.append(filename)
capture.release()
(OUT / 'chunk-boundaries.json').write_text(json.dumps({'source': 'final.mp4', 'method': 'Actual frame at each 3-second boundary minus1, exact, plus1. Visual inspection required.', 'sheets': pages, 'boundaries': records}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'sheets': pages, 'boundaries': len(records), 'frames': len(records) * 3}))
