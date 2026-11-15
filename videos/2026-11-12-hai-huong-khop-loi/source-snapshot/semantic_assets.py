"""Fetch narrowly scoped illustrative sources; their role is never inferred from tags."""
from pathlib import Path
import argparse
import hashlib
import json
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
CATALOG = [
    ('lamp-desk', 4884134, 'desk-lamp-beside-a-laptop', 'Artem Podrez',
     'Desk lamp beside laptop', 'Product/category illustration only; no physical photo proves the fictional USB-C, battery or price facts.'),
    ('typing-hands', 9644689, 'close-up-shot-of-a-person-typing-on-laptop', 'Liudmyla Shalimova',
     'Hands typing on laptop', 'Show only with a visible email composer/brief for the writing operation. Cannot replace the spoken email, draft content or AI error.'),
]


def fetch(batch):
    assets = batch / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    records = []
    for name, photo_id, slug, creator, subject, constraint in CATALOG:
        path = assets / f'{name}.jpg'
        url = f'https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=2048'
        if not path.exists():
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            if not response.headers.get('content-type', '').startswith('image/'):
                raise ValueError('Expected image: ' + name)
            path.write_bytes(response.content)
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
        records.append({'id': name, 'file': 'assets/' + path.name,
                        'page': f'https://www.pexels.com/photo/{slug}-{photo_id}/',
                        'download': url, 'creator': creator, 'subject': subject,
                        'usageConstraint': constraint, 'license': 'Pexels License',
                        'licenseURL': 'https://www.pexels.com/license/',
                        'width': width, 'height': height,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'inspection': 'pending actual pixel inspection; metadata is not visual approval'})
    (batch / 'source-images.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    sheet = Image.new('RGB', (1800, 720), '#131c23')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
    for index, row in enumerate(records):
        with Image.open(batch / row['file']) as image:
            image = ImageOps.contain(image.convert('RGB'), (590, 630))
            sheet.paste(image, (index * 600 + (590 - image.width) // 2, (630 - image.height) // 2))
        draw.text((index * 600 + 15, 656), row['id'], fill='white', font=font)
    sheet.save(batch / 'source-review.jpg', quality=94)
    print('FETCHED', len(records), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, default=ROOT / 'videos/2026-11-12-hai-huong-khop-loi')
    fetch(parser.parse_args().batch)
