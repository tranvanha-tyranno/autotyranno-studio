"""Measure the actual final-film QA invocation; never count queued render time."""
from pathlib import Path
import argparse
import datetime
import json
import sys
import time

batch = Path(__file__).resolve().parent
root = batch.parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--revision')
args = parser.parse_args()
output = batch / args.revision if args.revision else batch
if not (output / 'final.mp4').is_file():
    raise FileNotFoundError('Final film must exist before measured QA starts')
sys.path.insert(0, str(root / 'workflows/reference-video'))
started = time.monotonic()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt = {'schema': 'china-final-qa-timing/1', 'startedUTC': stamp(), 'status': 'running'}
target = batch / 'benchmark' / ('qa-' + args.revision + '-stage.json' if args.revision else 'qa-stage.json')
target.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
try:
    from china_qa import inspect
    result = inspect(batch, revision=args.revision)
    receipt.update(status='completed', decodedFrames=result['decodedFrames'],
                   technicalIntegrity=result['technicalIntegrity'])
except BaseException as error:
    receipt.update(status='failed', errorType=type(error).__name__, error=str(error))
    raise
finally:
    receipt.update(finishedUTC=stamp(), wallSeconds=round(time.monotonic() - started, 3))
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2), flush=True)
