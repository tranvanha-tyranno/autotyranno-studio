"""Generate selected audio assets with cached, guarded ElevenLabs calls."""
import argparse
from pathlib import Path
from documentary import load,save
from eleven_audio import speech,sound

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['plan','samples','voice','sounds']);p.add_argument('--batch',type=Path,required=True);a=p.parse_args()
    b=a.batch;d=load(b/'batch.json');profile=load(Path(__file__).with_name('lang-kinh.profile.json'));(b/'audio').mkdir(exist_ok=True)
    if a.stage=='plan':
        requested=sorted({x['name'] for x in d['sound_effects']}|{'port'})
        out={'tts_characters':len(d['script']),'voice':d['voice'],'new_tts_calls_upper_bound':int(not (b/'audio/narration-original.mp3').exists()),'new_sound_calls_upper_bound':sum(not (b/'audio'/f'{x}.mp3').exists() for x in requested),'sound_seconds_upper_bound':sum(profile['sound_presets'][x]['duration_seconds'] for x in requested if not (b/'audio'/f'{x}.mp3').exists()),'note':'File-based upper bound before content-addressed cache lookup; credentials excluded.'}
        save(b/'audio-plan.json',out);print(out)
    elif a.stage=='voice':speech(b/'audio/narration-original.mp3',d['script'],d['voice']['id'],d['voice']['model'])
    elif a.stage=='samples':
        sample=d['script'].split('Báo cáo')[0].strip()
        for v,name in zip(profile['voice_candidates'],['sample-thuy-tien','sample-adam']):speech(b/'audio'/f'{name}.mp3',sample,v['id'],profile['audio_model'])
    else:
        for name in sorted({x['name'] for x in d['sound_effects']}|{'port'}):
            preset=profile['sound_presets'][name];sound(b/'audio'/f'{name}.mp3',preset['prompt'],preset['duration_seconds'])

if __name__=='__main__':main()
