# Bread documentary renderer

New isolated footage-first composition. It imports only the existing local Be Vietnam Pro font binaries; it does not import or modify any earlier animation renderer/cast. Entry `../bread-documentary-entry.tsx`, composition ID `BreadDocumentary`, 1920×1080 at 30fps.

Input props:

```json
{
  "plan": {
    "fps": 30,
    "durationFrames": 420,
    "title": "Bánh mì và sức mua",
    "audio": "BATCH/audio/mix.wav",
    "shots": [
      {
        "id": "s01", "from": 0, "duration": 420,
        "chapterId": "cost", "chapterTitle": "Hai nghìn đồng đã đi đâu?",
        "media": "graphic", "file": "BATCH/footage/bread.mp4",
        "sourceStartSeconds": 2.5,
        "headline": "Giá tăng, phần còn lại giảm",
        "kind": "cost_stack", "cueFrames": [12, 130, 245, 345],
        "data": {"beforePrice": 20000, "afterPrice": 22000, "beforeVariable": 12000, "afterVariable": 14500, "fixedPerUnit": 5000},
        "graphicSide": "right", "label": "Mô hình minh họa"
      }
    ]
  },
  "startFrame": 0,
  "frames": 420
}
```

All `file`/`audio` paths are relative to Remotion `public/`; forward slashes. `from`, `duration`, `cueFrames`, `startFrame`, `frames` use composition frames. **Only `sourceStartSeconds` uses seconds.** `cueFrames` are local to their shot and should come from the final narration take. Source footage must cover `sourceStartSeconds + duration / fps`; prepare bounded clips and verify source duration outside this renderer. No automatic loops or still fallbacks.

`media: video` gives uninterrupted full-frame footage with optional short editorial `headline`/`emphasis`, shown for at most 4.5 seconds. These fields are selective points, never a transcript or caption track. Use `media: graphic` only for a meaningful calculation; it still requires a real moving footage `file` as background, with a side gradient to protect legibility. `graphicSide` protects the important action in the crop. `exposure` is an optional source-specific brightness multiplier; inspect actual rendered crops before setting it. There are no cartoon characters, logos, disclaimer cards, subtitles, chapter slides, decorative progress bars or automatic waveform graphics.

Calculation kinds:

- `cost_stack`: general data `beforePrice`, `afterPrice`, `beforeVariable`, `afterVariable`, `fixedPerUnit`. Four cues: initial context, variable cost rises while old selling price holds, selling price changes, remainder difference. For the bread script, `stage: before` uses `price/variable/fixed` with cues `[price, variable, fixed, remainder]`; `stage: after` uses `price/variable/fixed` for the new state and cues `[variable rise, old price hold, new price, delta]`; `stage: compare` compares the existing modeled 3,000 with 2,500 and cues `[after remainder, added sale versus cost, conclusion]`. It subtracts the variables rather than accepting a separately invented margin. Small note distinguishes modeled remainder from net profit and pins unchanged sales volume. These examples are explicitly illustrative.
- `price_path`: data `prices` or `values` (2–4 numeric prices), `labels` (matching short period labels). Cue per point, then one cue for the concluding relation. Uses the exact supplied numbers; percentage changes derive from them. Labels do not continuously count through artificial economic values.
- `purchasing_power`: general data `wageGrowth` and `basketGrowth` in percent. Three cues: income change, comparable basket change, exact purchasing-power ratio. It calculates `(1+wageGrowth/100)/(1+basketGrowth/100)`, not subtraction of growth rates. Script stages: `income` uses `incomeBefore/incomeAfter/priceBefore/priceAfter`, cues `[income, bread price]`; `quantity` and `result` use quantities `before/after` (500/477.2727 in this script), cues `[after quantity, ratio result, optional conclusion]`. The result is approximately −4.5%, explicitly only the bread comparison and not CPI/all-basket purchasing power. Never substitute the old five-versus-eight-percent example.

Each chapter's first footage shot carries a short signpost over the action for up to 104 frames. It is not a standalone title scene. Videos cut directly on narration boundaries; only overlays fade for ~6 frames, preventing black joins from double fades. Final mix is played untouched; source video sound is muted. Proof props trim the same composition and audio to an absolute interval.

Render a complete short interval with `--props=props.json` after setting `startFrame`/`frames`, then inspect moving scenes. A still or TypeScript pass does not establish aesthetic approval. Long export remains the runner/operator's separate step after proof review.
