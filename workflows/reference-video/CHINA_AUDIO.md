# China economy audio and cost measurement

`china_audio.py` uses the approved Nhật Phong / eleven_v3 / Vietnamese voice at natural speed. Its music and Foley plan is separate from the café topic: industrial networks, balance-sheet friction and adaptation music; port, crane, rail, factory, pencil/paper and restrained pulse sounds. Generic retained music/taps/transitions retain original hashes and provider receipts. These sounds are illustrative design, not archival recordings from the locations pictured.

Only `--phase voice` and `--phase generate` call billable endpoints. `plan`, `account-start`, `account-end` and `benchmark` do not generate media. There is no automatic retry after unresolved provider transport failure. `mix` is local and uses an isolated instance of the existing speech-first PCM/stem engine, with this module's sound plan and explicit cue definitions; it does not change café defaults or reroute shared module globals.

```powershell
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase account-start
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase plan
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase generate
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase voice
```

After the chapter takes are assembled and `data.json` is compiled, write `audio/cue-plan.json` with `cues: [{beat, asset, offsetSeconds, gainDB, role}]` and optional `quietPivots: [{beat}]`. Each beat must exist; offsets must remain inside that beat; role must identify the relevant visible action or editorial relationship. The helper rejects coffee-only sounds and never fills insufficient music duration by looping.

```powershell
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase mix
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase account-end
python -X utf8 workflows/reference-video/china_audio.py --batch videos/NEW-CHINA-BATCH --phase benchmark
```

`benchmark/audio-requests/<request-hash>.json` records the route before each call, UTC start/end, measured elapsed seconds, endpoint, model, request hash, request ID when exposed, source/receipt SHA and `cache_hit`. Numeric `character-cost` response headers from new calls are summed. A missing header remains unknown. A cached asset's historical header is retained for provenance but contributes zero new request usage. Re-running the same completed operation reuses its event and verified audio; an unresolved event blocks another call.

`audio/mix-dependencies.json` pins narration, source receipts, cue plan and exact caption/beat timing. Later photographic/layout changes with those dependencies unchanged reuse the same mixed waveform and write a separate `mix-visual-equivalence` receipt; the original mix report stays intact. A timing, cue or source change stops instead of overwriting the mix. The default public audio namespace is `production-public/china`.

Account snapshots retain only plan/status and numeric count/limit/remaining. Account differences can contain other jobs, rollover or adjustments and must not be assigned wholly to this task. No account identity, invoices, payment details, complete account response or API key is written.

The dated list-price calculation in `audio-cost-summary.json` uses [official ElevenAPI pricing](https://elevenlabs.io/pricing/api), checked 2026-11-13: v3 $0.08 per 1,000 input characters, music $0.15 per minute and sound effects $0.12 per minute. It estimates new completed requests from requested duration/input text, excludes taxes and is not an invoice, actual cash charge, account credit conversion or plan allocation. The API [subscription reference](https://elevenlabs.io/docs/api-reference/user/subscription/get) documents count/limit fields. Provider duration/level checks and successful generation do not establish listening or user acceptance.

Offline guards: `python -B -m pytest workflows/reference-video/test_china_audio.py -q -p no:cacheprovider`.
