# Measured China video render

`china_render.py` renders isolated `ChinaPreview` from `cinematic/src/china/`. It snapshots the exact content, timing, props, source receipts, China code and audio dependency receipts before bundling. Chapters run sequentially with two render pages by default and the minimum supported **268435456-byte media cache**. `--concurrency 4` is an explicit option; it is not a guaranteed speed-up or total RAM cap.

```powershell
python -X utf8 -B workflows/reference-video/china_render.py --batch videos/CHINA-BATCH --concurrency 2
python -X utf8 -B workflows/reference-video/china_render.py --batch videos/CHINA-BATCH --resume videos/CHINA-BATCH/render-attempts/ATTEMPT --concurrency 2
```

Resume requires the same frozen data/props/mix/bundle/source snapshot and render options. Completed chapter files must still match their saved hashes and decoded frame counts. Partial chapters are renamed with `-failed-<id>` and retained; only missing chapters render again. A pre-existing final is never overwritten.

Chapter H264 is rendered at 1920×1080, 30 fps, CRF18, yuv420p and explicit BT.709. Before the fast join, the helper checks codec/profile/size/frame rate, then remuxes each compatible chapter to a common timebase with H264 VUI aspect/color metadata normalized. Stream copy proceeds only when the normalized parameters agree. A mismatch or failed copy/decode falls back to a normalized encode, retaining the failed artifact/log. Original chapter files remain intact. The final AAC always comes from the exact pinned speech-first mix, not chapter audio.

Every finished final is decoded completely for the exact configured frame count (17,913 for this batch). Audio is decoded to sample count to check duration and coverage through the last spoken word. These checks do not establish listening, visual acceptance or user approval; rendered editorial review remains separate.

`benchmark/render-stage.json` records bundle/chapter/join wall times, actual frame throughput and real-time factors, final decode timings, concurrency and memory available at start. On Windows each process receipt also reports direct Node/FFmpeg CPU seconds from `GetProcessTimes`; this excludes browser/encoder descendant CPU and is labelled as such. No dollar estimate for machine time, power or hardware is invented. Snapshots and checkpoint state stay within each attempt.

Three focused offline checks: `python -B -m pytest workflows/reference-video/test_china_render.py -q -p no:cacheprovider`. They include an actual six-frame H264 packet-normalization/stream-copy join with final video and audio decode.
