"""Independent local ASR of the complete shared mix; never a listening claim."""
import difflib,re,time
from faster_whisper import WhisperModel
from finance_long import BATCH,save,load,sha

def norm(text):return re.findall(r'\w+',text.casefold())
def main():
    source=BATCH/'audio/final-mix.wav';start=time.perf_counter()
    model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
    chunks,info=model.transcribe(str(source),language='vi',beam_size=3,word_timestamps=True,vad_filter=False)
    rows=[]
    for s in chunks:
        rows.append({'start':s.start,'end':s.end,'text':s.text,
            'words':[{'text':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in (s.words or [])]})
        save(BATCH/'audio/asr-progress.json',{'segments':rows})
    plan=load(BATCH/'plan.json');chapters=[]
    for i,ch in enumerate(plan['chapters']):
        begin=ch['from']/30;end=plan['chapters'][i+1]['from']/30 if i+1<len(plan['chapters']) else plan['durationFrames']/30
        expected=' '.join(s['text']for s in plan['segments']if s['chapterId']==ch['id'])
        observed=' '.join(w['text'] for r in rows for w in r['words'] if begin<=w['start']<end)
        ratio=difflib.SequenceMatcher(None,norm(expected),norm(observed),autojunk=False).ratio()
        chapters.append({'chapter':ch['id'],'expected':expected,'recognized':observed,'tokenSimilarity':round(ratio,4)})
    save(BATCH/'audio/asr-review.json',{'sourceSHA256':sha(source),'model':'faster-whisper-small / local CPU int8','wallSeconds':time.perf_counter()-start,
        'segments':rows,'chapters':chapters,'recognizerLanguage':info.language,
        'scope':'Complete shared mix independently recognized. ASR may mishear names/numbers; similarity is diagnostic, not manual listening or aesthetic acceptance.'})
    print('ASR_COMPLETE',[(c['chapter'],c['tokenSimilarity'])for c in chapters],flush=True)
if __name__=='__main__':main()
