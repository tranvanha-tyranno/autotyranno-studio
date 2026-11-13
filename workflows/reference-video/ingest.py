"""Resume reference acquisition; preserve evidence without claiming analysis."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

import imageio_ffmpeg
import requests
import yt_dlp

IDS = '29B8-FtuC6U 5uTC396kCs4 96eyTrbH-ak 5_7IDQEU5OI UA7yZNRmZYY 5zqAMK2qsfM NCl_PG00oa4 Glw9YcOMw2s ggxRI_1u0_4 njD0SI3TNxg L0uNZyvCAxE bm5q0e4MXhg v74IRBimBk0 X2Uadb-AKTw BOD_6bf_6pM ERI4I4V4sBs 9I2suK0eob4'.split()

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

class Quiet:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def acquire(item):
    root, video_id, media = item
    folder = root/video_id
    folder.mkdir(parents=True, exist_ok=True)
    evidence = {'id':video_id, 'url':f'https://www.youtube.com/watch?v={video_id}', 'analysis_status':'not_yet_reviewed', 'errors':[]}
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'logger':Quiet(),'socket_timeout':25,'retries':1,'extractor_retries':1}) as ydl:
            info = ydl.extract_info(evidence['url'], download=False)
        evidence.update({k:info.get(k) for k in ['title','channel','duration','upload_date','description','chapters','width','height']})
        evidence['caption_tracks'] = list(info.get('subtitles', {}))
        evidence['automatic_caption_tracks'] = list(info.get('automatic_captions', {}))
        subs = next(folder.glob('*.vi.json3'), None)
        if subs is None and (folder/'captions.json3').exists():
            subs = folder/'captions.json3'
        tracks = info.get('subtitles', {}) or info.get('automatic_captions', {})
        lang = next((x for x in ['vi-orig','vi','en-orig','en'] if x in tracks), None)
        if subs is None and lang:
            track = next((t for t in tracks[lang] if t['ext']=='json3'), None)
            if track:
                response = requests.get(track['url'], timeout=40)
                response.raise_for_status()
                subs = folder/'captions.json3'
                subs.write_bytes(response.content)
        if subs:
            raw = json.loads(subs.read_text(encoding='utf-8'))
            segments = []
            for event in raw.get('events', []):
                text = ''.join(s.get('utf8','') for s in event.get('segs',[])).strip()
                if text:
                    segments.append({'start':event.get('tStartMs',0)/1000,'duration':event.get('dDurationMs',0)/1000,'text':text})
            save(folder/'transcript.json', segments)
            (folder/'transcript.txt').write_text('\n'.join(f"[{s['start']:.2f}] {s['text']}" for s in segments),encoding='utf-8')
            evidence['transcript'] = {'path':'transcript.json','segments':len(segments),'source':'YouTube captions; may contain ASR errors','language':lang,'sha256':hashlib.sha256(subs.read_bytes()).hexdigest()}
        save(folder/'evidence.json', evidence)
        if media:
            video = folder/'reference.mp4'
            if not video.exists():
                with yt_dlp.YoutubeDL({'quiet':True,'noprogress':True,'logger':Quiet(),'socket_timeout':25,'retries':1,'fragment_retries':1,'concurrent_fragment_downloads':2,'ffmpeg_location':imageio_ffmpeg.get_ffmpeg_exe(),'format':'134/bestvideo[height<=360][ext=mp4]/worstvideo','outtmpl':str(video)}) as ydl:
                    ydl.download([evidence['url']])
            evidence['media'] = {'path':video.name,'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest()}
            # Sparse samples are navigation aids, never proof of full viewing.
            from PIL import Image, ImageDraw
            seconds = info['duration']
            sheet = Image.new('RGB',(1280,5*204),'#181818')
            draw = ImageDraw.Draw(sheet)
            times = sorted(set([0,3,10,20,30]+[round(seconds*i/14,2) for i in range(1,15)]))
            for n,t in enumerate(times):
                t = min(t,max(0,seconds-1))
                frame = folder/f'frame-{n:02}.jpg'
                if not frame.exists():
                    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=320:180',str(frame)],check=True,capture_output=True)
                with Image.open(frame) as im: sheet.paste(im,(n%4*320,n//4*204+24))
                draw.text((n%4*320+4,n//4*204+4),f'{t:.2f}s',fill='white')
            sheet.save(folder/'contact-sheet.jpg', quality=90)
            evidence['visual_sampling'] = {'times':times,'scope':'Sparse frames only; not full audiovisual or lip-sync review'}
    except Exception as exc:
        evidence['errors'].append(type(exc).__name__+': '+str(exc)[:300])
    save(folder/'evidence.json',evidence)
    print(json.dumps({k:evidence.get(k) for k in ['id','title','duration','transcript','media','errors']},ensure_ascii=True),flush=True)
    return evidence

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--media',action='store_true')
    parser.add_argument('--ids',nargs='*',default=IDS)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        result=list(pool.map(acquire,[(args.output,x,args.media) for x in args.ids]))
    save(args.output/'catalog.json', result)
