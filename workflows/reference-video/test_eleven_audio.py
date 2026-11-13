"""Billing guards and Vietnamese alignment; all checks are offline."""
import hashlib,json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).parent))
import eleven_audio as audio

def deny_key():raise AssertionError('Offline reuse must not read credentials')

def test_changed_script_cannot_reuse_existing_take(tmp_path,monkeypatch):
    monkeypatch.setattr(audio,'CACHE',tmp_path/'cache');monkeypatch.setattr(audio,'key',deny_key)
    p=tmp_path/'voice.mp3';p.write_bytes(b'existing take');audio.save(p.with_suffix('.receipt.json'),{'request_hash':'old-script'})
    with pytest.raises(ValueError,match='does not match'):audio.generate(p,'/test',{'text':'new text'},False)

def test_unresolved_call_never_submits_again(tmp_path,monkeypatch):
    monkeypatch.setattr(audio,'CACHE',tmp_path/'cache');monkeypatch.setattr(audio,'key',deny_key)
    p=tmp_path/'voice.mp3';audio.save(p.with_suffix('.intent.json'),{'request_hash':'pending'})
    with pytest.raises(RuntimeError,match='Unresolved'):audio.generate(p,'/test',{'text':'same text'},False)

def test_cached_timed_take_reuses_audio_and_alignment_without_key(tmp_path,monkeypatch):
    cache=tmp_path/'cache';cache.mkdir();monkeypatch.setattr(audio,'CACHE',cache);monkeypatch.setattr(audio,'key',deny_key)
    body={'text':'Giá trị ở lại.'};endpoint='/test';digest=hashlib.sha256(json.dumps({'endpoint':endpoint,'body':body},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    (cache/(digest+'.mp3')).write_bytes(b'cached take');audio.save(cache/(digest+'.json'),{'request_hash':digest});audio.save(cache/(digest+'.alignment.json'),{'characters':['G']})
    p=tmp_path/'out/voice.mp3';audio.generate(p,endpoint,body,True)
    assert p.read_bytes()==b'cached take'
    assert json.loads(p.with_suffix('.alignment.json').read_text())['characters']==['G']

def test_alignment_keeps_vietnamese_punctuation_and_gaps():
    chars=list('Giá  trị.');times=[i*.1 for i in range(len(chars))]
    rows=audio.words({'characters':chars,'character_start_times_seconds':times,'character_end_times_seconds':[x+.05 for x in times]})
    assert [x['text'] for x in rows]==['Giá','trị.']
    assert rows[1]['start']==pytest.approx(.5)
    assert rows[1]['end']==pytest.approx(.85)
