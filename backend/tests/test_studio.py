import io
from pathlib import Path
import subprocess
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image
import pytest

from app.main import app
from app import studio


@pytest.fixture
def client(tmp_path,monkeypatch):
    root=tmp_path/'studio';root.mkdir()
    monkeypatch.setattr(studio,'ROOT',root)
    class ImmediateExecutor:
        def submit(self,fn,*args):fn(*args)
    monkeypatch.setattr(studio,'EXECUTOR',ImmediateExecutor())
    with TestClient(app) as client:yield client


def create_ready(client,profile):
    response=client.post('/studio/projects',json={'name':'Offline test','profile':profile})
    assert response.status_code==200
    identity=response.json()['id']
    image=io.BytesIO();Image.new('RGB',(100,180),'white').save(image,format='PNG')
    uploaded=client.post(f'/studio/projects/{identity}/upload',files={'files':('product.png',image.getvalue(),'image/png')})
    assert uploaded.status_code==200
    product=uploaded.json()['products'][0]
    saved=client.put(f'/studio/projects/{identity}/products/{product["id"]}',json={'name':'Coco Bear','description':'Ấm trắng ngà, bình thủy tinh, nắp gấu, logo Coco Bear','features':['Điều khiển từ xa']})
    assert saved.status_code==200
    result=client.post(f'/studio/projects/{identity}/build',json={'variants':1,'hands_only':True,'mica_prompt':20})
    assert result.status_code==200
    return result.json()


def fake_media(batch,config,path,target,endpoint,payload):
    if target.exists():return
    if endpoint=='/v1/images/tasks':
        Image.new('RGB',(180,320),'white').save(target)
    else:
        studio.runner.run_ff([studio.runner.FF,'-y','-f','lavfi','-i',f'color=c=purple:s=180x320:r=24:d={payload["duration"]}','-c:v','libx264','-preset','ultrafast',str(target)])
    studio.write(path/(target.stem+'-task.json'),{'id':'offline_fixture','status':'completed'})


def fake_voice(batch,config,index,clip):
    target=studio.runner.clip_path(batch,index,clip)/'voice.mp3'
    if not target.exists():studio.runner.run_ff([studio.runner.FF,'-y','-f','lavfi','-i','sine=frequency=440:duration=18','-c:a','libmp3lame',str(target)])


@pytest.mark.parametrize('profile,seconds',[('mica',6),('review',20)])
def test_whole_pipeline_pauses_for_image_and_renders_without_provider(client,profile,seconds,monkeypatch):
    project=create_ready(client,profile);identity=project['id'];clip=project['clips'][0]
    assert len(project['clips'])==(3 if profile=='mica' else 1)
    monkeypatch.setattr(studio.runner,'task_media',fake_media)
    monkeypatch.setattr(studio.runner,'voice',fake_voice)
    with patch.object(studio.httpx.Client,'post',side_effect=AssertionError('No external provider in test')):
        queued=client.post(f'/studio/projects/{identity}/run',json={'stage':'all','clip_id':clip['id']})
        assert queued.status_code==200
        after=client.get(f'/studio/projects/{identity}').json()
        assert after['jobs'][0]['status']=='needs_review'
        assert after['clips'][0]['assets'].get('opening')
        assert not after['clips'][0]['assets'].get('final')
        assert client.post(f'/studio/projects/{identity}/clips/{clip["id"]}/approve').status_code==200
        assert client.post(f'/studio/projects/{identity}/run',json={'stage':'all','clip_id':clip['id']}).status_code==200
    after=client.get(f'/studio/projects/{identity}').json()
    assert after['jobs'][0]['status']=='completed',after['jobs'][0]
    output=studio.folder(identity)/'batch'/clip['directory']/'final.mp4'
    assert abs(studio.runner.duration(output)-seconds)<0.05
    url=after['clips'][0]['assets']['final'].removeprefix('/api')
    response=client.get(url,headers={'Range':'bytes=0-100'})
    assert response.status_code in [200,206]
    assert response.headers['content-type']=='video/mp4'
    assert any(item['project_id']==identity for item in client.get('/studio/library').json() if 'project_id' in item)
    editing=client.put(f'/studio/projects/{identity}/clips/{clip["id"]}',json={'dialogue':'changed','opening_prompt':clip['opening_prompt'],'shot_prompts':clip['shot_prompts']})
    assert editing.status_code==409
    cloned=client.post(f'/studio/projects/{identity}/clips/{clip["id"]}/clone').json()['clips'][-1]
    assert not cloned['assets']
    changed=client.put(f'/studio/projects/{identity}/clips/{cloned["id"]}',json={'dialogue':'new','opening_prompt':clip['opening_prompt'],'shot_prompts':clip['shot_prompts']})
    assert changed.status_code==200


def test_upload_validation_and_path_escape(client):
    identity=client.post('/studio/projects',json={'name':'Validation','profile':'mica'}).json()['id']
    invalid=client.post(f'/studio/projects/{identity}/upload',files={'files':('x.png',b'not an image','image/png')})
    assert invalid.status_code==400
    assert client.get('/studio/projects/bad/files/project.json').status_code==404
    with pytest.raises(Exception):studio.safe_file(studio.folder(identity),'../../app.db')


def test_gemini_suggestion_uses_header_key_cache_and_does_not_edit(client,monkeypatch):
    project=create_ready(client,'mica');clip=project['clips'][0];identity=project['id']
    monkeypatch.setattr(studio,'provider_key',lambda provider:'test-secret-only')
    class Response:
        status_code=200
        def json(self):return {'candidates':[{'content':{'parts':[{'text':'Prompt sửa có hành động ngay từ đầu.'}]}}]}
    with patch.object(studio.httpx.Client,'post',return_value=Response()) as post:
        payload={'provider':'gemini','clip_id':clip['id'],'field':'shot_prompt','scene':1,'instruction':'Nhịp nhanh hơn'}
        first=client.post(f'/studio/projects/{identity}/suggest',json=payload)
        assert first.status_code==200,first.text
        assert post.call_count==1
        assert post.call_args.kwargs['headers']['x-goog-api-key']=='test-secret-only'
        assert 'test-secret-only' not in post.call_args.args[0]
        second=client.post(f'/studio/projects/{identity}/suggest',json=payload)
        assert second.json()['cache_hit']
        assert post.call_count==1
    unchanged=client.get(f'/studio/projects/{identity}').json()['clips'][0]
    assert unchanged['shot_prompts']==clip['shot_prompts']
    assert 'test-secret-only' not in ''.join(p.read_text(encoding='utf-8') for p in studio.folder(identity).rglob('*.json'))


def test_plan_calls_without_executing(client):
    project=create_ready(client,'review')
    with patch.object(studio.httpx.Client,'post',side_effect=AssertionError('No calls')):
        report=client.get(f'/studio/projects/{project["id"]}/plan').json()
    assert report['new_provider_calls_upper_bound']==5
    assert report['llm_calls']==0


def test_partial_gemini_response_is_not_cached_or_applied(client,monkeypatch):
    project=create_ready(client,'mica');clip=project['clips'][0]
    monkeypatch.setattr(studio,'provider_key',lambda provider:'test-only')
    class Partial:
        status_code=200
        def json(self):return {'candidates':[{'finishReason':'MAX_TOKENS','content':{'parts':[{'text':'incomplete'}]}}]}
    with patch.object(studio.httpx.Client,'post',return_value=Partial()):
        response=client.post(f'/studio/projects/{project["id"]}/suggest',json={'provider':'gemini','clip_id':clip['id'],'instruction':'Sửa nhanh hơn'})
        assert response.status_code==502
    assert not list((studio.folder(project['id'])/'suggestions').glob('*.json'))


def test_untrusted_origin_cannot_mutate_studio(client):
    response=client.post('/studio/projects',json={'name':'blocked','profile':'mica'},headers={'Origin':'https://untrusted.invalid'})
    assert response.status_code==403
