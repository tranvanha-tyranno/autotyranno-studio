# Remotion revision after repetitive China visuals

The user rejected the China r02 film for repeating a few scene styles. Different labels, numbers, source assets or 51 decoded shots did not establish visual variety. Preserve r02 as rejected evidence; do not describe it as approved. This correction applies to the current film, with the same original narration and topic.

R03 uses `cinematic/src/china-v2/`: physical/spatial scenes, people and household scenes, data and trade scenes, and original editorial/story scenes. Each scene needs a visible subject, an action that explains its spoken point, and an authored progression. Examples include exploded product assembly, a building completed by floors, household decisions and coin allocation, a price-adjustment lens, trade arithmetic blocks, and a liability moving between balance sheets. These are SVG/2D or spatial illustrations unless actual Three.js geometry or real media is used; do not call drawings footage or true 3D.

Keep the exact Nhật Phong takes, word/caption timing, final spoken sentence and pinned speech-first mix. A visual revision does not authorize a duplicate paid voice/music generation. Preserve hook → short disclaimer → main content → CTA, source periods/units/age thresholds, hypothetical-model labels, licensed context receipts and no channel branding. New artwork and mechanical labels still need actual viewing; more objects or animation do not establish quality.

Each shot carries `variety.module` and `variety.mechanic`. These are an inventory, not proof of diversity. Review the film's sequence as well as individual frames: different geometry should serve different spoken actions, and related callbacks should be intentional. Do not accept the same machine, donut or ribbon arrangement with renamed text as a new scene language.

Run full QA only after the final export exists:

```powershell
python -X utf8 -B workflows/reference-video/china_variety_qa.py --batch videos/2026-11-13-kinh-te-trung-quoc --revision r03
```

The wrapper retains the complete `china_qa.py` frame/FPS/dimensions, font/caption, branding, single-use media, source-hash and final-audio checks. It samples five times in **every** shot, including media, disclaimer and closing, while retaining midframes, three-second thumbnails and the last frame. The current film expects 17,913 actual decoded frames because that is its pinned timeline, not a universal duration constant. R03 has isolated receipts/public assets and the wrapper checks those revision files.

`qa/mechanic-plan.json` records the authored scene inventory; `qa/report.json` leaves motion/diversity/semantic review and user acceptance pending. Open the actual evidence and record observations and limits separately. Full decode, source dates, label counts and sample capture do not imply continuous watching/listening, aesthetic acceptance or model-weight training.
