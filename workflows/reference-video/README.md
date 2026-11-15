# Explainer production workflows

This directory contains reusable Python production, review, repair and research
tools plus the Remotion source project in `cinematic/`. Selected latest exports,
production assets, original compressed audio and selected exact final mixes are archived with Git LFS alongside
batch records. Superseded renders, expanded intermediate WAVs, downloaded reference
videos, credentials, browser sessions, the local learning ledger and duplicate
renderer bundles stay local. See [repository storage](../../docs/repository-storage.md).

Latest content correction: read [CONTENT_FIRST.md](CONTENT_FIRST.md) and the
dated chapter analyses in `docs/video-references/2026-11-14-content-study/`.
The user rejected unfocused writing and requires clear sections with an argument,
concrete example, emphasis and causal bridge. New timed narration through
`eleven_audio.generate` requires a reviewed, matching `editorial-map.json`;
existing exact takes/cache remain reusable. This is research and script workflow
work, not approval or production of a new film.

Latest complete bread-film rewrite: read [BREAD_DOCUMENTARY.md](BREAD_DOCUMENTARY.md).
The subsequent user upgrade is [BREAD_LAB.md](BREAD_LAB.md): richer visible
information, eight causal simulation families, web-downloaded CC0 Foley and
OpenAI narration. Both supplied keys were rejected401; any retained-voice visual
preview is explicitly provisional until OpenAI speech succeeds.
The user now requires real moving footage, a continuous bakery story, natural
emphasis, no cartoon cast/subtitles, and no separate long opening disclaimer.
The new isolated branch is `bread_documentary.py` / `src/bread-documentary/`.
After ElevenLabs quota blocked chapter three, the user explicitly authorized a
different Vietnamese voice for this film. Its five final takes use consistent
`vi-VN-NamMinhNeural` at `+8%` synthesis rate, with no post-synthesis time stretch;
`active-generation-plan.json` selects them. The two Nhật Phong takes and failure
receipts remain retained. This batch-specific override leaves Nhật Phong as the
default for other explainers. Voice quality still awaits listening/user feedback.

For the retained economics trial, read [ECONOMY_STORY.md](ECONOMY_STORY.md).
The still-cast r03 was subsequently rejected; motion r06 is pending feedback.
Its isolated renderer bundles Vietnamese Be Vietnam Pro fonts. Previous source
families and their acceptance/rejection history remain retained.

## Current finance options

Read [FINANCE_STYLES.md](FINANCE_STYLES.md) and
[finance-styles.profile.json](finance-styles.profile.json). The first minimalist
preview was criticized as slide-like, and the first human cast needs a redesign.
The user selected **expressive, slightly humorous comic characters** for the
revision. The new artwork and motion proofs still await user feedback.

- `cinematic/src/finance-flow/`: continuous money/receipt actions using exact
  narration cues; `FlowFilm` supports a supplied timeline.
- `cinematic/src/finance-cast-v2/` and `finance-comic/`: two new adult comic leads,
  expressive poses and palm anchors for held props.
- `cinematic/src/finance-cast/`: the original thirty-character library, retained
  for comparison rather than marked aesthetically approved.
- `finance_style_reset.py`: frozen source snapshots, preflight stills, sequential
  local rendering and full technical checks for the short motion comparison.

The batch-specific demo commands reuse local narration, alignment, music and
source receipts under `videos/`. Those files are required to reproduce an
existing export. Published media are fetched with `git lfs pull`; filtered historical
exports and intermediate stems still require the retained local files. Installing
dependencies does not regenerate them. A code-only checkout can compile and run offline tests.
New paid narration is only requested by explicit audio generation commands;
unresolved-call guards and matching caches prevent blind duplicate retries.

## Setup and offline checks

From the repository root, use Python 3.11+ and the Node version required by
`cinematic/package.json`:

```powershell
python -m pip install -r workflows/reference-video/requirements.txt
npm --prefix workflows/reference-video/cinematic ci
python -X utf8 -B -m pytest workflows/reference-video -q
```

From `workflows/reference-video/cinematic/`:

```powershell
npx tsc --noEmit
npx remotion studio src/finance-reset-entry.tsx --no-open
```

Small timeline JSON files in `cinematic/public/` support legacy composition
imports and clean-checkout type checking. Their referenced media are local
production assets; installing dependencies alone does not make those films
renderable. Source data such as geographic boundaries and font metrics remain
under `cinematic/src/`.

## Other production branches

- [PRODUCTION.md](PRODUCTION.md): sourced photographs/gallery and exact-take
  narration, with [LEARNING_LOOP.md](LEARNING_LOOP.md) for evidence-backed lessons.
- [APPROVED_BASELINE.md](APPROVED_BASELINE.md): pinned Nhật Phong narration and
  speech-first sound approach; later topic-specific visual instructions apply.
- [CHINA_VARIETY.md](CHINA_VARIETY.md): content-specific animated compositions.
- [REFERENCE_LEARNING.md](REFERENCE_LEARNING.md): reference-study scope and limits.

Legacy/rejected implementations remain available for history. Technical passes,
sampled frame inspection, continuous audiovisual review and explicit user
approval are separate records. Do not promote an old or new preview to approved
based only on its successful render.
