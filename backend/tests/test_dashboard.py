import io
import zipfile
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image
import pytest

from app.main import app
from app import studio
from app import studio_dashboard as dashboard


@pytest.fixture
def client(tmp_path,monkeypatch):
    root=tmp_path/'studio';root.mkdir()
    monkeypatch.setattr(studio,'ROOT',root)
    with TestClient(app) as client:yield client


def project_with_image(client):
    p=client.post('/studio/projects',json={'name':'Dashboard test','profile':'mica'}).json()
    buffer=io.BytesIO();Image.new('RGB',(100,160),'beige').save(buffer,format='PNG')
    response=client.post(f'/studio/projects/{p["id"]}/upload',files={'files':('ref.png',buffer.getvalue(),'image/png')})
    assert response.status_code==200
    return response.json()


def test_metadata_summary_and_archive_restore(client):
    p=project_with_image(client)
    changed=client.patch(f'/studio/projects/{p["id"]}/metadata',json={'name':'Đổi tên','pinned':True,'archived':True})
    assert changed.status_code==200
    summary=client.get('/studio/projects').json()[0]
    assert summary['name']=='Đổi tên' and summary['pinned'] and summary['archived']
    assert summary['thumbnail'].startswith('/api/studio/projects/')
    assert summary['ready']==0
    overview=client.get('/studio/overview').json()
    assert overview['projects']==0 and overview['archived']==1
    assert len(overview['activity'])==7
    restored=client.patch(f'/studio/projects/{p["id"]}/metadata',json={'archived':False})
    assert restored.status_code==200
    assert client.get('/studio/overview').json()['projects']==1
    assert client.patch(f'/studio/projects/{p["id"]}/metadata',json={'name':'   '}).status_code==400


def test_queued_cancellation_prevents_worker_execution(client):
    p=project_with_image(client);base=studio.folder(p['id'])
    job={'id':'abc123','project_id':p['id'],'clip_id':None,'stage':'images','status':'queued','message':'pending','created_at':studio.now()}
    path=base/'jobs/abc123.json';studio.write(path,job)
    assert client.post('/studio/jobs/abc123/cancel').status_code==200
    with patch.object(studio,'run_stage') as run:
        studio.work(path)
        run.assert_not_called()
    assert studio.read(path)['status']=='cancelled'
    job['status']='running';studio.write(path,job)
    assert client.post('/studio/jobs/abc123/cancel').status_code==409
    assert client.patch(f'/studio/projects/{p["id"]}/metadata',json={'archived':True}).status_code==409


def test_export_is_usable_zip_and_leaves_original(client):
    p=project_with_image(client);base=studio.folder(p['id'])
    (base/'.do-not-export.txt').write_text('private scratch',encoding='utf-8')
    response=client.get(f'/studio/projects/{p["id"]}/export')
    assert response.status_code==200
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        names=archive.namelist()
        assert 'project.json' in names
        assert any(n.startswith('inputs/') for n in names)
        assert '.do-not-export.txt' not in names
        assert all(not n.startswith(('/', '..')) for n in names)
    assert (base/'project.json').exists()
    assert not list((studio.ROOT/'.exports').glob('*.zip'))


def test_accounts_allowlist_never_exposes_credentials(client):
    class Response:
        def raise_for_status(self):pass
        def json(self):return [{'id':'a','label':'Account A','enabled':True,'cookies':{'secret':'must-not-leak'},'api_key':'must-not-leak','note':'secret note','use_count':3,'ok':None}]
    with patch.object(dashboard.httpx,'get',return_value=Response()),patch.object(studio.runner,'muse_headers',return_value={}):
        response=client.get('/studio/accounts')
    assert response.status_code==200
    assert 'must-not-leak' not in response.text and 'secret note' not in response.text
    assert response.json()['accounts'][0]['use_count']==3


def test_media_favorite_and_poster_without_external_calls(client,tmp_path,monkeypatch):
    source=tmp_path/'clip.mp4'
    studio.runner.run_ff([studio.runner.FF,'-y','-f','lavfi','-i','color=c=orange:s=180x320:r=24:d=1','-c:v','libx264','-preset','ultrafast',str(source)])
    monkeypatch.setattr(dashboard,'media_entries',lambda:[{'id':'local-test','title':'Local','url':'local','_path':source,'size_bytes':source.stat().st_size,'created_at':studio.now()}])
    assert client.post('/studio/media/local-test/favorite').json()['favorite']
    assert client.get('/studio/media').json()[0]['favorite']
    assert not client.post('/studio/media/local-test/favorite').json()['favorite']
    assert client.post('/studio/media/unknown/favorite').status_code==404
    response=client.get('/studio/media/local-test/poster')
    assert response.status_code==200 and response.headers['content-type']=='image/jpeg'
    with patch.object(dashboard.subprocess,'run',side_effect=AssertionError('must reuse poster cache')):
        assert client.get('/studio/media/local-test/poster').status_code==200


def test_prompt_collection_is_complete(client):
    collection=client.get('/studio/templates').json()
    assert [t['number'] for t in collection]==list(range(11,21))
    assert all(t['hands']==2 for t in collection if t['number'] in [18,20])
    assert all(t['seconds']==6 for t in collection)
