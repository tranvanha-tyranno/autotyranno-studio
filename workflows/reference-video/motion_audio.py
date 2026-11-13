"""Mix isolated narration, generated instrumental and one contextual Foley cue.

Usage: python workflows/reference-video/motion_audio.py --batch videos/<batch>
No provider calls; originals stay immutable. Music automation follows a word cue.
"""
from pathlib import Path
import argparse,json,re,shutil
from documentary import FF,run

def build(batch:Path):
    timeline=json.loads((batch/'timeline.json').read_text(encoding='utf-8'))
    start=timeline['sewingStart']
    hold=timeline['cuts'][1]/30
    score=batch/'audio/motion-score.mp3'
    voice=batch/'narration.wav'
    foley=batch/'audio/sewing-detail.mp3'
    # A short score vacuum makes "Nhưng khoan" land. This is gain automation,
    # not a fresh random effect on every visual cut. All expression times are seconds.
    gain=f"if(lt(t,{hold-.25:.4f}),1,if(lt(t,{hold-.10:.4f}),1-0.9*(t-{hold-.25:.4f})/0.15,if(lt(t,{hold+.90:.4f}),0.1,if(lt(t,{hold+1.20:.4f}),0.1+0.9*(t-{hold+.90:.4f})/0.3,1))))"
    graph=(
        '[0:a]highpass=f=70,loudnorm=I=-16:TP=-2:LRA=8,asplit=2[v][key];'
        '[1:a]loudnorm=I=-27:TP=-7:LRA=8,'
        f"volume='{gain}':eval=frame,afade=t=in:d=0.6,afade=t=out:st=48:d=2[m];"
        '[m][key]sidechaincompress=threshold=.025:ratio=3:attack=18:release=260:makeup=1[duck];'
        f'[2:a]highpass=f=180,lowpass=f=7000,loudnorm=I=-30:TP=-9:LRA=5,afade=t=in:d=0.15,afade=t=out:st=4.4:d=0.6,adelay={round(start*1000)}|{round(start*1000)}[fx];'
        '[v][duck][fx]amix=inputs=3:duration=longest:normalize=0,'
        'alimiter=limit=.89:level=false,apad=whole_dur=50[out]'
    )
    target=batch/'audio/final-mix.wav'
    run([FF,'-y','-v','error','-i',str(voice),'-i',str(score),'-i',str(foley),'-filter_complex',graph,'-map','[out]','-t','50','-ar','48000','-ac','2',str(target)])
    report=run([FF,'-hide_banner','-i',str(target),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    raw=report.stderr if hasattr(report,'stderr') else str(report)
    if isinstance(raw,bytes):raw=raw.decode('utf-8',errors='replace')
    # documentary.run returns CompletedProcess with captured stderr.
    match=re.findall(r'\{\s*"input_i".*?\}',raw,re.S)
    measured=json.loads(match[-1]) if match else {'log':raw[-1500:]}
    (batch/'audio/mix-report.json').write_text(json.dumps({'measurement':measured,'music':str(score),'voice':str(voice),'foley':str(foley),'scoreVacuum':[hold-.2,hold+1.05],'sewingAt':start,'foleySeconds':5,'manualListening':False},ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(target,Path(__file__).parent/'cinematic/public/mix.wav')
    print(json.dumps(measured))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);build(p.parse_args().batch)
