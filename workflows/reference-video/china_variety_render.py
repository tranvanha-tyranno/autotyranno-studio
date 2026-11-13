"""Use the measured China renderer with a separate, fully snapshotted visual rewrite."""
from pathlib import Path
import argparse
import shutil
import china_render as base

base.ENTRY=base.PROJECT/'src/china-variety-entry.tsx'
original_snapshot=base.snapshot

def variety_snapshot(batch,destination):
    original_snapshot(batch,destination)
    records=base.load(destination/'hashes.json')
    paths=[base.WORK/'china_variety.py',Path(__file__),base.ENTRY,
           base.PROJECT/'src/business/Shared.tsx',base.PROJECT/'src/directions/types.ts']+list((base.PROJECT/'src/china-v2').rglob('*'))
    for src in paths:
        if not src.is_file():continue
        target=destination/'workflow'/src.relative_to(base.WORK)
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
        records.append({'file':target.relative_to(destination).as_posix(),'sha256':base.sha(target)})
    base.save(destination/'hashes.json',records)

base.snapshot=variety_snapshot

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);p.add_argument('--resume',type=Path)
    p.add_argument('--concurrency',type=int,choices=[1,2,4],default=2)
    a=p.parse_args();base.render(a.batch,a.resume,a.concurrency)
