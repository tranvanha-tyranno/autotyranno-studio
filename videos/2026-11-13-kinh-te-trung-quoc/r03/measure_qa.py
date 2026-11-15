"""Record the measured QA of the new visual rewrite, after its export exists."""
from pathlib import Path
import sys
import json
import datetime
import time

batch=Path(__file__).resolve().parent
root=batch.parents[2]
sys.path.insert(0,str(root/'workflows/reference-video'))
if not (batch/'final.mp4').is_file():raise FileNotFoundError('Final must exist first')
from china_variety_qa import inspect
clock=time.monotonic()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'schema':'china-variety-qa-timing/1','startedUTC':utc(),'status':'running'}
target=batch/'benchmark/qa-stage.json'
target.write_text(json.dumps(record,indent=2),encoding='utf-8')
try:
    result=inspect(batch)
    record.update(status='completed',decodedFrames=result['decodedFrames'],technicalIntegrity=result['technicalIntegrity'])
except BaseException as e:
    record.update(status='failed',errorType=type(e).__name__,error=str(e))
    raise
finally:
    record.update(finishedUTC=utc(),wallSeconds=round(time.monotonic()-clock,3))
    target.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False,indent=2),flush=True)
