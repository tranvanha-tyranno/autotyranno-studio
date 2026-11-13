# Explainer production workflows

This directory contains reusable Python production, review, repair and research
tools plus the Remotion source project in `cinematic/`. Rendered video/audio,
downloaded reference media, credentials, browser sessions and the local learning
ledger stay outside this source publication.

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
existing export and are not fetched or regenerated automatically by installing
the code. A fresh checkout can compile and run offline tests without them.
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
