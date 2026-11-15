"""Estimate exact-script timing from locally recognized word timestamps.

No synthesis, network download or credential access. This is ASR-anchor mapping
plus explicit interpolation, NOT forced alignment or phoneme-level timing.
Produces the existing character-array shape for documentary timeline consumers.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import wave

for _name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '2'

import bread_documentary_asr as asr
import economy_story_asr as base

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BATCH = ROOT / 'videos/2026-11-15-banh-mi-mo-phong-openai'
METHOD = 'ASR word-anchor mapping to known script; unmatched spans and within-word character times interpolated; not forced/phoneme alignment.'


def signature(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def expanded_script(text):
    expanded, original = [], []
    for index, match in enumerate(re.finditer(r'\S+', text)):
        row={'text':match.group(),'startChar':match.start(),'endChar':match.end(),'index':index}
        original.append(row)
        expanded.extend({'token':token,'originalIndex':index} for token in base.normalized_tokens(match.group()))
    return expanded, original


def expanded_recognition(words):
    rows=[]
    for i, word in enumerate(words):
        tokens=base.normalized_tokens(word['word'])
        for j, token in enumerate(tokens):
            length=max(0,word['end']-word['start'])
            rows.append({'token':token,'start':word['start']+length*j/len(tokens),
                         'end':word['start']+length*(j+1)/len(tokens),
                         'recognizedWordIndex':i,'numericExpansion':len(tokens)>1,
                         'probability':word.get('probability')})
    return rows


def map_timing(text, recognized, duration):
    expected, originals=expanded_script(text); observed=expanded_recognition(recognized)
    if not expected or not observed:
        raise ValueError('Cannot align empty script or recognition')
    matcher=difflib.SequenceMatcher(None,[r['token'] for r in expected],[r['token'] for r in observed],autojunk=False)
    timing=[None]*len(expected)
    matched=0
    for block in matcher.get_matching_blocks():
        for j in range(block.size):
            timing[block.a+j]={**observed[block.b+j],'method':'matched_asr_anchor'}
            matched+=1
    gaps=[]; i=0
    while i<len(timing):
        if timing[i] is not None:
            i+=1;continue
        a=i
        while i<len(timing) and timing[i] is None:i+=1
        b=i;left=timing[a-1]['end'] if a else 0.;right=timing[b]['start'] if b<len(timing) else duration
        right=max(left,min(duration,right))
        for j in range(a,b):
            timing[j]={'start':left+(right-left)*(j-a)/(b-a),'end':left+(right-left)*(j+1-a)/(b-a),
                       'method':'unmatched_interpolation','probability':None,'numericExpansion':False}
        gaps.append({'normalizedStart':a,'normalizedEndExclusive':b,'text':' '.join(e['token'] for e in expected[a:b]),
                     'start':left,'end':right,'seconds':right-left,'needsReview':True})
    # Monotonic constrained output is deterministic; preserve every correction as evidence.
    corrections=[];previous=0.
    for i,row in enumerate(timing):
        raw=(row['start'],row['end'])
        row['start']=min(duration,max(previous,row['start']))
        row['end']=min(duration,max(row['start'],row['end']))
        previous=row['end']
        if raw!=(row['start'],row['end']):corrections.append({'normalizedIndex':i,'raw':raw,'constrained':[row['start'],row['end']]})
    words=[]
    for original in originals:
        selected=[timing[i] for i,r in enumerate(expected) if r['originalIndex']==original['index']]
        if not selected:
            # A standalone punctuation token inherits a zero-length boundary.
            last=words[-1]['end'] if words else 0.
            start=end=last;method='punctuation_boundary';estimated=True
        else:
            start,end=selected[0]['start'],selected[-1]['end']
            estimated=any(s['method']!='matched_asr_anchor' or s['numericExpansion'] for s in selected)
            method='interpolated_or_numeric_expanded' if estimated else 'matched_asr_anchor'
        words.append({**original,'start':start,'end':end,'method':method,'estimated':estimated})
    starts=[0.]*len(text);ends=[0.]*len(text);cursor=0;previous=0.
    for word in words:
        for i in range(cursor,word['startChar']):starts[i]=ends[i]=previous
        a,b=word['startChar'],word['endChar']
        for i in range(a,b):
            starts[i]=word['start']+(word['end']-word['start'])*(i-a)/max(1,b-a)
            ends[i]=word['start']+(word['end']-word['start'])*(i+1-a)/max(1,b-a)
        cursor=b;previous=word['end']
    for i in range(cursor,len(text)):starts[i]=ends[i]=previous
    # Stable serialization avoids sub-ulp overlaps at word/whitespace joins.
    starts=[round(v,6) for v in starts]
    ends=[round(v,6) for v in ends]
    alignment={'characters':list(text),'character_start_times_seconds':starts,
               'character_end_times_seconds':ends,'timingMethod':METHOD}
    quality={'normalizedTokenCount':len(expected),'recognizedNormalizedTokens':len(observed),
             'matchedTokenCount':matched,'matchedTokenCoverage':matched/len(expected),
             'sequenceSimilarity':matcher.ratio(),'unmatchedSpans':gaps,'monotonicCorrections':corrections,
             'estimatedOriginalWords':sum(w['estimated'] for w in words),'originalWordCount':len(words),
             'words':words,'requiresReview':bool(gaps or corrections),
             'qualityScope':'Timing-estimation diagnostics; does not confirm that every supplied script word was spoken.'}
    if matched/len(expected)<.60:
        raise ValueError('Too few acoustic anchors (<60%); do not interpolate a mostly unrecognized chapter')
    return alignment,quality


def unit_bounds(chapter,alignment,quality):
    output=[];cursor=0
    for unit in chapter['units']:
        a,b=cursor,cursor+len(unit['text'])
        if ''.join(alignment['characters'][a:b])!=unit['text']:
            raise ValueError('Unit offset differs from exact chapter text')
        selected=[w for w in quality['words'] if a<=w['startChar']<b]
        head=selected[:3];tail=selected[-3:]
        output.append({'id':unit['id'],'start':alignment['character_start_times_seconds'][a],
                       'end':alignment['character_end_times_seconds'][b-1],
                       'estimatedWordCount':sum(w['estimated'] for w in selected),
                       'boundaryNeedsReview':any(w['estimated'] for w in head+tail),
                       'firstWords':head,'lastWords':tail})
        cursor=b+2
    return output


def align_batch(batch, plan_path, model_name='small', available_only=False):
    batch=batch.resolve();plan_path=plan_path.resolve();content=base.load(batch/'content.json');plan=base.load(plan_path)
    chapters=content['chapters'];takes=plan['chapterTakes']
    if [c['id'] for c in chapters]!=[r['chapter'] for r in takes]:raise ValueError('Chapter order mismatch')
    params={'model':model_name,'device':'cpu','compute_type':'int8','cpu_threads':2,'num_workers':1,
            'language':'vi','beam_size':3,'best_of':1,'word_timestamps':True,'condition_on_previous_text':False,
            'vad_filter':False,'temperature':0,'repetition_penalty':1.1,'no_repeat_ngram_size':3,
            'local_files_only':True,'mappingVersion':'asr-monotonic-known-text/1'}
    directory=batch/'audio/local-word-alignment';directory.mkdir(parents=True,exist_ok=True)
    ffmpeg=base.resolve_ffmpeg(None);model=None;records=[];skipped=[]
    for chapter,take in zip(chapters,takes):
        text='\n\n'.join(u['text'] for u in chapter['units'])
        payload=take['payload'];requested=payload.get('text',payload.get('input'))
        if requested!=text:raise ValueError('Frozen request differs from exact chapter script')
        source=(batch/take['file']).resolve()
        if not source.is_relative_to(batch):raise ValueError('Audio path escapes batch')
        if not source.exists():
            if available_only:skipped.append(chapter['id']);continue
            raise FileNotFoundError(str(source))
        receipt=source.with_suffix('.receipt.json')
        if not receipt.exists() or base.load(receipt).get('sha256')!=base.sha(source):
            raise ValueError('Audio is missing a matching source receipt')
        alignment_path=source.with_suffix('.alignment.json');review_path=source.with_suffix('.alignment-review.json')
        if alignment_path.exists() and (not review_path.exists() or base.load(alignment_path).get('timingMethod')!=METHOD):
            raise ValueError('Preserve existing provider timing; this helper must not overwrite it')
        wav,info=asr.prepare_audio(source,directory/'chunks',ffmpeg)
        request={'audioSHA256':base.sha(source),'resampledSHA256':info['sha256'],
                 'scriptSHA256':hashlib.sha256(text.encode()).hexdigest(),'parameters':params,
                 'runtimeVersions':base.runtime_versions()};key=signature(request);cache=directory/'cache'/(key+'.json')
        if cache.exists():recognized=base.load(cache)
        else:
            if model is None:
                from faster_whisper import WhisperModel
                model=WhisperModel(model_name,device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
            stream,metadata=model.transcribe(str(wav),language='vi',beam_size=3,best_of=1,
                word_timestamps=True,condition_on_previous_text=False,vad_filter=False,temperature=0,
                repetition_penalty=1.1,no_repeat_ngram_size=3)
            segments=[];words=[]
            for segment in stream:
                segments.append({'start':segment.start,'end':segment.end,'text':segment.text})
                words.extend({'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in segment.words or [])
                base.save(directory/(chapter['id']+'-progress.json'),{'requestHash':key,'segments':segments,'words':words})
            recognized={'requestHash':key,'request':request,'segments':segments,'words':words,'language':metadata.language}
            base.save(cache,recognized)
        if recognized['requestHash']!=key or recognized['request']!=request:raise ValueError('Recognition cache mismatch')
        alignment,quality=map_timing(text,recognized['words'],info['seconds'])
        review={'schema':'bread-local-word-alignment-review/1','requestHash':key,'request':request,
                'chapter':chapter['id'],'method':METHOD,'recognitionCache':cache.relative_to(batch).as_posix(),
                'recognitionCacheSHA256':base.sha(cache),'durationSeconds':info['seconds'],'quality':quality,
                'unitBoundaries':unit_bounds(chapter,alignment,quality),
                'numberDiagnostics':asr.lexical_checks(chapter['id'],text,' '.join(s['text'] for s in recognized['segments'])),
                'boundaryInstruction':'Use acoustic matched word times for exact phrase cues. Interpolated start/end/number spans require inspection; do not claim forced alignment.',
                'continuousListening':False,'userApproval':'not_established'}
        base.save(alignment_path,alignment);base.save(review_path,review)
        records.append({'chapter':chapter['id'],'file':take['file'],'alignment':alignment_path.relative_to(batch).as_posix(),
                        'alignmentSHA256':base.sha(alignment_path),'review':review_path.relative_to(batch).as_posix(),
                        'matchedTokenCoverage':quality['matchedTokenCoverage'],'requiresReview':quality['requiresReview']})
        print('ALIGNMENT_ESTIMATED',chapter['id'],round(quality['matchedTokenCoverage'],3),flush=True)
    report={'schema':'bread-local-word-alignment-summary/1','method':METHOD,'records':records,'skippedChapters':skipped,
            'status':'partial' if skipped else 'complete-estimated-timing','continuousListening':False,'userApproval':'not_established'}
    base.save(directory/'summary.json',report)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,default=DEFAULT_BATCH)
    parser.add_argument('--plan',type=Path)
    parser.add_argument('--model',choices=['small','base'],default='small')
    parser.add_argument('--available-only',action='store_true')
    args=parser.parse_args();plan=args.plan or args.batch/'openai-generation-plan.json'
    align_batch(args.batch,plan,args.model,args.available_only)
