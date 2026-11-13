"""Place actual pixels beside the complete narrated clause and visual requirement."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont


def pairs(batch, manifest='manifest.json'):
    folder = batch / 'proofs'
    records = json.loads((folder / manifest).read_text(encoding='utf-8'))
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 25)
    small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
    title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
    def wrap(draw, text, face, width):
        lines, part = [], ''
        for word in text.split():
            candidate = (part + ' ' + word).strip()
            if draw.textlength(candidate, font=face) > width and part:
                lines.append(part)
                part = word
            else:
                part = candidate
        return lines + ([part] if part else [])
    for page in range((len(records) + 3) // 4):
        sheet = Image.new('RGB', (1920, 1680), '#101a22')
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(records[page * 4:page * 4 + 4]):
            x, y = index % 2 * 960, index // 2 * 840
            with Image.open(folder / row['file']) as image:
                sheet.paste(image.resize((960, 540)), (x, y))
            draw.text((x + 20, y + 555), f"{row['id']} · {row['frame'] / 30:.2f}s · {row['scene']} / {row.get('mode', '')}", fill='#67d9c7', font=title)
            cursor = y + 595
            for text, face, color in [('LỜI: ' + row['narratedText'], font, '#ffffff'), ('CẦN THẤY: ' + row['requiredVisual'], small, '#bdc8ce')]:
                for line in wrap(draw, text, face, 910):
                    draw.text((x + 20, cursor), line, fill=color, font=face)
                    cursor += 31
        sheet.save(folder / f'pairs-{page + 1:02}.jpg', quality=94)
    print('PAIRED', len(records), 'actual rendered clauses', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--manifest', default='manifest.json')
    args = parser.parse_args()
    pairs(args.batch, args.manifest)
