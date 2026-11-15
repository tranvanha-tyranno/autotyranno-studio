"""Collect licensed real-photo illustrations with reproducible source/crop receipts.

The input seed is editorial research, not a search-result-to-image assumption.
Download and contact-sheet creation deliberately leave inspection pending until
a reviewer records what the actual pixels and intended crop show.
"""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, io, json, time
from datetime import datetime, timezone
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'videos/2026-11-14-tai-chinh-anh-that'
LICENSE_URL = 'https://www.pexels.com/license/'

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def collect(batch: Path):
    seed = json.loads((batch / 'source-seed.json').read_text(encoding='utf-8'))
    if isinstance(seed, dict): seed = seed['assets']
    ids = [a['id'] for a in seed]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate asset IDs')
    (batch / 'assets').mkdir(parents=True, exist_ok=True)
    (batch / 'sources').mkdir(exist_ok=True)
    old_path = batch / 'asset-catalog.json'
    old = {a['id']: a for a in json.loads(old_path.read_text(encoding='utf-8'))['assets']} if old_path.exists() else {}
    inspections_path = batch / 'inspection-notes.json'
    inspections = json.loads(inspections_path.read_text(encoding='utf-8')) if inspections_path.exists() else {}

    def download(a):
        a = dict(a)
        number = str(a['pexelsID'])
        url = a.get('downloadURL') or f'https://images.pexels.com/photos/{number}/pexels-photo-{number}.jpeg?auto=compress&cs=tinysrgb&w=2400'
        target = batch / 'assets' / (a['id'] + '.jpg')
        if target.exists():
            if a['id'] in old and sha(target) != old[a['id']]['sha256']: raise ValueError('Retained photo changed: ' + a['id'])
        else:
            response = requests.get(url, timeout=40)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content)); image.verify()
            target.write_bytes(response.content)
        with Image.open(target) as im:
            width, height = im.size
            if min(width, height) < 650: raise ValueError('Insufficient image size: ' + a['id'])
        note = inspections.get(a['id'], {})
        a.update(file=target.relative_to(batch).as_posix(), downloadURL=url,
                 width=width, height=height, sha256=sha(target),
                 license='Pexels License', licenseURL=LICENSE_URL,
                 medium='real_stock_photograph', use='Illustration only; not evidence about named fictional characters.',
                 inspection=note.get('inspection', 'pending_actual_pixel_review'),
                 observed=note.get('observed', ''), crop=note.get('crop', {}),
                 limits=note.get('limits', ['Location is unverified unless explicitly documented by source.', 'No personal financial circumstances or endorsement are asserted.']))
        save(batch / 'sources' / (a['id'] + '.json'), a)
        return a

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        assets = list(pool.map(download, seed))
    save(old_path, {'schema':'finance-real-photo-catalog/1', 'createdAt':datetime.now(timezone.utc).isoformat(),
        'policy':'Real sourced photography is the primary illustration. Simulations are separate and used only where needed to explain arithmetic or processes.',
        'paidProviderCalls':0, 'assets':assets})
    sheets(batch, assets)
    print('PHOTO_ASSETS_READY', len(assets), flush=True)

def sheets(batch, assets):
    out = batch / 'inspection'; out.mkdir(exist_ok=True)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
    small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    # Both original aspect (contain) and the proposed 16:9 center crop are shown.
    for start in range(0, len(assets), 9):
        sheet = Image.new('RGB', (1920, 1350), '#e8e0d1')
        d = ImageDraw.Draw(sheet)
        for j, a in enumerate(assets[start:start+9]):
            x, y = j % 3 * 640, j // 3 * 450
            with Image.open(batch / a['file']) as src:
                src = ImageOps.exif_transpose(src).convert('RGB')
                whole = ImageOps.contain(src, (630, 210))
                sheet.paste(whole, (x + (630-whole.width)//2, y+30))
                crop = ImageOps.fit(src, (630, 178), method=Image.Resampling.LANCZOS, centering=(.5,.5))
                sheet.paste(crop, (x, y+245))
            d.text((x+7,y+4),a['id']+' / '+str(a['pexelsID']),font=font,fill='#252136')
            d.text((x+7,y+426),'Top: full image | bottom: center 16:9 crop',font=small,fill='#252136')
        sheet.save(out / f'photos-{start//9+1:02}.jpg', quality=92)
    save(out / 'receipt.json', {'method':'original-aspect plus proposed center 16:9 crop contact sheets',
        'inspectionIsAutomatic':False,'sheets':[{'file':p.relative_to(batch).as_posix(),'sha256':sha(p)} for p in sorted(out.glob('photos-*.jpg'))]})

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--batch',type=Path,default=DEFAULT);args=parser.parse_args()
    collect(args.batch.resolve())
