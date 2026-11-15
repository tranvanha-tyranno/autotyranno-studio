"""Retain full first export, correct selected chapters without changing its take."""
import argparse,copy,json,shutil,time
from pathlib import Path
import business,business_render
from documentary import FF

WORK=Path(__file__).resolve().parent
save=business.save;load=business.load;sha=business.sha;require=business.require

def refine(batch,base_attempt,revision='r02'):
    batch=Path(batch).resolve();base=Path(base_attempt).resolve();out=batch/revision
    require(base.is_relative_to(batch/'render-attempts'),'Use retained attempt inside this batch')
    require(not out.exists(),'Revision exists; inspect it before another attempt')
    old=load(batch/'data.json');data=copy.deepcopy(old);shots={s['id']:s for s in data['shots']}
    aligned=load(batch/'aligned-words.json')
    def phrase(shot_id,text):
        shot=shots[shot_id];q=business.production.normalized_words(text);ws=[w for w in aligned if shot['start']/30-.03<=w['start']<shot['end']/30]
        tokens=[business.production.normalized_words(w['text'])[0] for w in ws]
        ix=[i for i in range(len(tokens)-len(q)+1) if tokens[i:i+len(q)]==q]
        require(len(ix)==1,'Refinement cue missing/ambiguous: '+text)
        return round(ws[ix[0]]['start']*30)-shot['start']
    shots['h02']['design']['cues']=[phrase('h02',p) for p in ['Có thể quán','Cũng có thể','hoặc tiền phải chi']]
    shots['p04']['design']['cues']=[0,phrase('p04','bốn mươi ba phần trăm')]
    shots['h01']['images'][1]['trimBeforeFrames']=450
    changed={'h01','h02','p04'}
    require(data['captions']==old['captions'] and data['frames']==old['frames'],'Exact take/caption mismatch')
    for a,b in zip(old['shots'],data['shots']):
        require((a['id'],a['start'],a['end'],a['text'])==(b['id'],b['start'],b['end'],b['text']),'Narration/timing changed')
        if a['id'] not in changed:require(a==b,'Unselected scene appearance changed')
    # Check the underlying source file rather than aliases created per trim.
    receipts={r['publicFile']:r for r in load(batch/'source-receipts.json')}
    check=copy.deepcopy(data)
    for s in check['shots']:
        for image in s['images']:
            image['file']=receipts[image['file']]['source']['file']
    media=business.validate_media_intervals(check)
    out.mkdir();save(out/'data.json',data);save(out/'props.json',{'data':data});save(out/'media-interval-check.json',media)
    save(out/'change-plan.json',{'changedShots':sorted(changed),'audioChanged':False,'timingChanged':False,'captionsChanged':False,
         'baseDataSHA256':sha(batch/'data.json'),'newDataSHA256':sha(out/'data.json'),
         'observations':'Actual opening strip showed three choices entering out of spoken order. Enforce all three exact cues; chart bars also use complete explicit cues. Opening extraction uses an active unused source interval starting15s.'})
    while not(batch/'render-receipt.json').is_file():
        state=load(base/'state.json');require(state['status']!='failed','Base render failed; resume it before refinement')
        time.sleep(5)
    state=load(base/'state.json');require(state['status']=='completed','Base not completed')
    require(sha(batch/'final.mp4')==load(batch/'render-receipt.json')['finalSHA256'],'Base final differs')
    require(sha(batch/'data.json')==state['dataSHA256'],'Base data changed')
    for record in state['bundleFiles']:require(sha(base/'bundle'/record['file'])==record['sha256'],'Frozen bundle differs')
    snapshot=out/'source-snapshot';snapshot.mkdir()
    shutil.copy2(Path(__file__),snapshot/'business_refine.py')
    shutil.copy2(batch/'audio/mix-report.json',snapshot/'mix-report.json')
    save(snapshot/'hashes.json',[{'file':p.name,'sha256':sha(p)} for p in snapshot.iterdir() if p.is_file()])
    target_chapters={s['chapter'] for s in data['shots'] if s['id'] in changed}
    parts=[]
    for i,part in enumerate(state['parts']):
        if part['id'] not in target_chapters:
            p=base/f'part-{i:02}.mp4';require(sha(p)==part['receipt']['sha256'],'Retained chapter differs');parts.append(p);continue
        p=out/f'part-{i:02}.mp4';print('REFINE',part['id'],part['end']-part['start'],'frames',flush=True)
        business_render.run(['node',business_render.CLI,'render',base/'bundle','BusinessPreview',p,f'--props={out/"props.json"}',
           f'--frames={part["start"]}-{part["end"]-1}','--muted','--codec=h264','--crf=18','--concurrency=2',
           '--media-cache-size-in-bytes=268435456','--log=info'],out/f'part-{i:02}.log')
        business_render.decoded(p,part['end']-part['start']);parts.append(p)
    listing=out/'concat.txt';listing.write_text('\n'.join("file '"+p.as_posix()+"'" for p in parts),encoding='utf-8')
    print('JOIN REFINED',data['frames'],flush=True)
    business_render.run([FF,'-y','-v','error','-f','concat','-safe','0','-i',listing,'-i',batch/'audio/final-mix.wav',
       '-map','0:v:0','-map','1:a:0','-vf','setsar=1,scale=iw:ih:in_range=auto:out_range=tv:out_color_matrix=bt709,format=yuv420p',
       '-c:v','libx264','-preset','fast','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
       '-color_range','tv','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(data['frames']/30),
       '-movflags','+faststart',out/'final.mp4'],out/'join.log')
    final=business_render.decoded(out/'final.mp4',data['frames'])
    save(out/'render-receipt.json',{'schema':'business-refinement/1','finalSHA256':final['sha256'],'frames':final['frames'],
        'baseFinalSHA256':sha(batch/'final.mp4'),'audioMixSHA256':sha(batch/'audio/final-mix.wav'),
        'newDataSHA256':sha(out/'data.json'),'changedShots':sorted(changed),'chaptersReplaced':sorted(target_chapters),
        'sameSpokenTake':True,'sameWordTiming':True,'sameCaptions':True,'userAcceptance':'pending',
        'limitation':'All video is encoded again at join; unmodified decoded pixels are not asserted byte-identical.'})
    print('REFINED COMPLETE',out/'final.mp4',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);p.add_argument('--base-attempt',type=Path,required=True);p.add_argument('--revision',default='r02');a=p.parse_args();refine(a.batch,base_attempt=a.base_attempt,revision=a.revision)
