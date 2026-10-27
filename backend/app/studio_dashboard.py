"""Dashboard utilities. Uses existing media and metadata; never generates paid media."""
from datetime import datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import uuid
import zipfile

import httpx
from fastapi import APIRouter,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from starlette.background import BackgroundTask

from . import studio as s

router=APIRouter(prefix='/studio',tags=['Studio dashboard'])


class MetadataEdit(BaseModel):
    name:str|None=Field(default=None,min_length=1,max_length=160)
    pinned:bool|None=None
    archived:bool|None=None


@router.patch('/projects/{project_id}/metadata')
def update_metadata(project_id:str,payload:MetadataEdit):
    base=s.folder(project_id)
    with s.LOCK:
        if s.busy(project_id):raise HTTPException(409,'Đợi tác vụ hoàn tất trước khi sửa dự án.')
        project=s.read(base/'project.json')
        changes=payload.model_dump(exclude_none=True)
        if 'name' in changes:
            changes['name']=changes['name'].strip()
            if not changes['name']:raise HTTPException(400,'Tên dự án không được để trống.')
        project.update(changes);s.save_project(base,project)
    return s.public_project(base)


@router.post('/jobs/{job_id}/cancel')
def cancel_queued(job_id:str):
    with s.LOCK:
        path=next((p for p in s.ROOT.glob('*/jobs/*.json') if p.stem==job_id),None)
        if not path:raise HTTPException(404,'Không tìm thấy tác vụ.')
        job=s.read(path)
        if job['status']!='queued':raise HTTPException(409,'Chỉ hủy được tác vụ chưa bắt đầu. Không ngắt tác vụ provider đang chạy.')
        job.update(status='cancelled',message='Đã hủy trước khi chạy. Không gửi yêu cầu tạo mới.',finished_at=s.now())
        s.write(path,job)
    return job


@router.get('/projects/{project_id}/export')
def export_project(project_id:str):
    base=s.folder(project_id)
    if s.busy(project_id):raise HTTPException(409,'Đợi tác vụ hoàn tất để xuất gói nhất quán.')
    exports=s.ROOT/'.exports';exports.mkdir(exist_ok=True)
    target=exports/(uuid.uuid4().hex+'.zip')
    allowed={'.json','.txt','.md','.png','.jpg','.jpeg','.webp','.mp4','.mp3','.wav'}
    with zipfile.ZipFile(target,'w',allowZip64=True) as archive:
        for path in base.rglob('*'):
            if path.is_symlink() or not path.is_file() or path.suffix.lower() not in allowed:continue
            if not path.resolve().is_relative_to(base.resolve()):continue
            relative=path.relative_to(base)
            if any(p.startswith('.') for p in relative.parts):continue
            archive.write(path,relative.as_posix(),compress_type=zipfile.ZIP_DEFLATED if path.suffix in {'.json','.md','.txt'} else zipfile.ZIP_STORED)
    return FileResponse(target,media_type='application/zip',filename=f'autotyranno-{project_id}.zip',background=BackgroundTask(target.unlink,missing_ok=True))


def prefs():
    path=s.ROOT/'preferences.json'
    return s.read(path) if path.exists() else {'favorites':[]}


def media_entries():
    result=[]
    for item in s.library():
        url=item['url']
        if item.get('project_id'):
            base=s.folder(item['project_id'])
            relative=url.split('/files/',1)[1]
            path=s.safe_file(base,relative)
            project=s.read(base/'project.json')
            profile=project['profile'];project_name=project['name']
        elif '/legacy-files/' in url:
            path=s.safe_file(s.PROJECT/'videos',url.split('/legacy-files/',1)[1]);profile='review';project_name=path.parent.parent.name
            meta=path.parent.parent/'batch.json'
            if meta.exists():profile=s.read(meta).get('profile','review')
        else:
            relative=url.split('/data-files/',1)[1].removeprefix('cocobear-two-reviews/')
            path=s.safe_file(s.PROJECT/'data/cocobear-two-reviews',relative);profile='review';project_name='Coco Bear · Thử nghiệm'
        identity=hashlib.sha256(url.encode()).hexdigest()[:20]
        pretty={'night-female-presenter':'Người mẫu nữ · Bếp ban đêm','day-male-presenter':'Người mẫu nam · Bếp sáng','hands-daylight-curiosity':'Chỉ tay · Bếp sáng','hands-evening-funny':'Chỉ tay · Bếp tối','night-nursery':'Góc pha sữa ban đêm','daylight-kitchen':'Căn bếp sáng'}
        title=item['title']
        for key,value in pretty.items():
            if key in title:title=value;break
        info={'id':identity,'title':title,'project_name':project_name,'url':url,'project_id':item.get('project_id'),'profile':profile,'size_bytes':path.stat().st_size,'created_at':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),'poster_url':f'/api/studio/media/{identity}/poster','_path':path}
        result.append(info)
    return sorted(result,key=lambda i:i['created_at'],reverse=True)


@router.get('/media')
def media():
    favorites=set(prefs().get('favorites',[]))
    return [{k:v for k,v in item.items() if k!='_path'}|{'favorite':item['id'] in favorites} for item in media_entries()]


@router.post('/media/{media_id}/favorite')
def favorite(media_id:str):
    if not any(item['id']==media_id for item in media_entries()):raise HTTPException(404,'Video không còn trong thư viện.')
    with s.LOCK:
        data=prefs();values=set(data.get('favorites',[]))
        if media_id in values:values.remove(media_id)
        else:values.add(media_id)
        data['favorites']=sorted(values);s.write(s.ROOT/'preferences.json',data)
    return {'favorite':media_id in values}


@router.get('/media/{media_id}/poster')
def poster(media_id:str):
    item=next((i for i in media_entries() if i['id']==media_id),None)
    if not item:raise HTTPException(404,'Không tìm thấy video.')
    source=item['_path']
    cache=s.ROOT/'.posters';cache.mkdir(exist_ok=True)
    key=hashlib.sha256(f'{media_id}:{source.stat().st_size}:{source.stat().st_mtime_ns}'.encode()).hexdigest()
    target=cache/(key+'.jpg')
    with s.LOCK:
        if not target.exists():
            try:
                completed=subprocess.run([s.runner.FF,'-v','error','-y','-ss','0.3','-i',str(source),'-frames:v','1','-vf','scale=480:-2','-q:v','3',str(target)],capture_output=True,timeout=20)
            except subprocess.TimeoutExpired as exc:raise HTTPException(504,'Ảnh xem trước chưa sẵn sàng.') from exc
            if completed.returncode or not target.exists():raise HTTPException(422,'Không trích được ảnh xem trước.')
    return FileResponse(target,media_type='image/jpeg',headers={'Cache-Control':'private, max-age=3600'})


@router.get('/overview')
def overview():
    projects=s.list_projects();job_list=s.jobs();items=media()
    local_zone=timezone(timedelta(hours=7));today=datetime.now(local_zone).date()
    activity=[]
    for back in range(6,-1,-1):
        day=today-timedelta(days=back)
        def on_day(value):return datetime.fromisoformat(value).astimezone(local_zone).date()==day
        activity.append({'date':day.isoformat(),'jobs':sum(on_day(j['created_at']) for j in job_list),'videos':sum(on_day(m['created_at']) for m in items)})
    live=[p for p in projects if not p['archived']]
    return {'projects':len(live),'archived':len(projects)-len(live),'products':sum(p['products'] for p in live),'clips':sum(p['clips'] for p in live),'videos':len(items),'active_jobs':sum(j['status'] in ['running','queued'] for j in job_list),'needs_review':sum(p['awaiting_review'] for p in live),'failed_jobs':sum(j['status']=='failed' for j in job_list),'completed_jobs':sum(j['status']=='completed' for j in job_list),'activity':activity,'recent_jobs':job_list[:6],'recent_media':items[:4]}


@router.get('/templates')
def templates():
    output=[]
    for item in s.mica.ACTIONS:
        output.append({'id':f'mica-{item["id"]}','number':item['id'],'title':item['title'],'category':'mica','seconds':6,'hands':item['hands'],'requires':item['requires'],'text':s.mica.video_prompt(item),'summary':item['action']})
    return output


@router.get('/accounts')
def account_overview():
    try:
        response=httpx.get('http://127.0.0.1:18610/admin/accounts',headers=s.runner.muse_headers(),timeout=4)
        response.raise_for_status()
        raw=response.json()
        accounts=raw if isinstance(raw,list) else raw.get('accounts',raw.get('items',[]))
        safe=[]
        for item in accounts:
            # Explicit allowlist: never relay cookies, raw provider errors or auth metadata.
            safe.append({k:item.get(k) for k in ['id','label','enabled','ok','use_count','last_used','expires_at','expires_estimated','essential_ok','cookie_count']})
        return {'online':True,'accounts':safe,'worker_count':1,'note':'Trạng thái phiên từ pool; quota riêng từng loại chưa được xác minh ở màn hình này.'}
    except (httpx.HTTPError,ValueError,TypeError,KeyError):
        return {'online':False,'accounts':[],'worker_count':1,'note':'Chưa đọc được pool. Bật Muse2API hoặc kiểm tra key local.'}
