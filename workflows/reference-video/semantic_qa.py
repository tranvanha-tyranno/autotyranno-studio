"""Decode the final MP4 and pair every narrated clause with its actual pixels."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import cv2
from PIL import Image, ImageDraw, ImageFont
from documentary import FF, run
from semantic_pairs import pairs


def inspect(batch):
    data = json.loads((batch / 'data.json').read_text(encoding='utf-8'))
    video = batch / 'final.mp4'
    digest = hashlib.sha256(video.read_bytes()).hexdigest()
    out = batch / 'qa'
    proof = out / 'proofs'
    proof.mkdir(parents=True, exist_ok=True)
    records = []
    for shot in data['shots']:
        frame = min(shot['end'] - 1, shot['start'] + max(1, round((shot['end'] - shot['start']) * .72)))
        records.append({**shot, 'frame': frame, 'file': f"{shot['id']}-{frame}.jpg", 'reviewStatus': 'requires_actual_visual_review', 'videoSHA256': digest})
    by_frame = {row['frame']: row for row in records}
    seconds, temporal = {}, {}
    operation_frames = {min(shot['end'] - 1, shot['start'] + round((shot['end'] - shot['start']) * fraction))
                        for shot in data['shots'] if shot['scene'] in ['email_prompt', 'wrong_claim', 'source_check', 'tone_edit', 'time_log', 'comment_cta', 'task_map', 'send_gate', 'decision']
                        for fraction in [.1, .5, .9]}
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    count = 0
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        if count in by_frame or count % 30 == 15 or count in operation_frames or count == data['frames'] - 1:
            image = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            if count in by_frame:
                image.save(proof / by_frame[count]['file'], quality=94)
            if count % 30 == 15:
                seconds[count] = image.resize((384, 216))
            if count in operation_frames:
                temporal[count] = image.resize((640, 360))
            if count == data['frames'] - 1:
                image.save(out / 'last-frame.jpg', quality=94)
        count += 1
    cap.release()
    (proof / 'manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    pairs(out)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
    def sheets(frames, cols, size, per_page, prefix):
        keys = sorted(frames)
        w, h = size
        for offset in range(0, len(keys), per_page):
            page = keys[offset:offset + per_page]
            sheet = Image.new('RGB', (cols * w, ((len(page) + cols - 1) // cols) * (h + 30)), '#101a22')
            draw = ImageDraw.Draw(sheet)
            for i, frame in enumerate(page):
                x, y = i % cols * w, i // cols * (h + 30)
                sheet.paste(frames[frame].resize(size), (x, y))
                draw.text((x + 8, y + h + 3), f'{frame / fps:.2f}s / {frame}', font=font, fill='white')
            sheet.save(out / f'{prefix}-{offset // per_page + 1:02}.jpg', quality=93)
    sheets(seconds, 5, (384, 216), 30, 'full-duration')
    sheets(temporal, 3, (640, 360), 18, 'operations')
    with Image.open(proof / records[0]['file']) as image:
        image.save(batch / 'poster.jpg', quality=94)
    result = run([FF, '-hide_banner', '-i', str(video), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    log = result.stderr.decode('utf-8', errors='replace')
    (out / 'audio-measurement.log').write_text(log, encoding='utf-8')
    measured = json.loads(re.findall(r'\{\s*"input_i".*?\}', log, re.S)[-1])
    report = {'decodedFrames': count, 'expectedFrames': data['frames'], 'frameCountPass': count == data['frames'],
              'fps': fps, 'seconds': count / fps, 'width': width, 'height': height, 'clauses': len(records),
              'fullNarratedClausesPairedToActualMP4': True, 'videoSHA256': digest,
              'audioMeasuredOnFinalMP4': measured, 'semanticAcceptance': 'pending per-clause actual visual review',
              'userAcceptance': 'pending', 'humanAudioListening': 'not performed by this script'}
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False), flush=True)
    if count != data['frames']:
        raise ValueError('Frame count differs from the exact take')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, required=True)
    inspect(parser.parse_args().batch)
