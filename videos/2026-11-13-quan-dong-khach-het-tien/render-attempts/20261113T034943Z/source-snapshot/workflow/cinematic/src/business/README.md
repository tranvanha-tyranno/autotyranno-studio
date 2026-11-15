# Business explainer renderer

Isolated entry: `src/business-entry.tsx`, composition `BusinessPreview`.
Props: `{data: BusinessTimeline}`; see `types.ts` for the exact contract.
All animation comes from composition frames. The entry imports no old video
composition and displays no channel name, logo or watermark.

## Scene choices

- `b-photo`: one to three inspected photos or real clips. With multiple media,
  `design.cues[0]` cuts to image2 and `[1]` to image3; absent cues divide the shot
  evenly. Clips remain at native speed and never silently loop. A media item
  must have enough inspected duration for its subshot.
- `b-paper`: a contextual photo and one receipt sheet. Supply `design.paper`
  with up to five rows, optionally one total. Rows are strings so units and
  wording remain authored, not inferred.
- `b-question`: one large question, a few selected emphasized words, optional
  supporting photo. Also used for the explicit disclaimer section.
- `b-chart`: manifest-driven bars, waterfall, line or break-even graphic.
  Values and units must be verified before rendering.
- `b-split`: two concrete choices with one image each. `design.choices` carries
  short label/title/body text, not a dashboard or a nested list.
- `b-coffee`: an original lathed ceramic cup, handle, coffee surface and short
  coin/flow animation next to a contextual photo. Optional `design.paper.rows`
  supplies up to three plainly labeled values; the renderer invents none.
- `b-closing`: a full image or clip with a spoken-action headline and body.

Themes are `cream`, `dark` and `warm`. `design.emphasis` lists exact substrings
to accent. Cue frames are local to the shot and should follow exact narration
phrases. Narration, music and Foley are delivered through one premeasured final
mix, with exact-take captions in seconds.

## Chart conventions

Bars use `items[].value` directly. A waterfall treats each item as a signed
change except the final item, which is a separately authored final balance
anchored to zero. Thus `105, -45, -48, 12` shows revenue, variable costs, fixed
costs and the remaining operating result without double-counting the balance.

Line and break-even use `items[].x` for the horizontal coordinate, or sequential
positions when omitted. `items[].label` labels the horizontal axis and
`items[].value` is the vertical quantity. For break-even, `fixed` is a horizontal
fixed-cost line in the same unit as values. `max` sets the vertical scale;
`xLabel`, `unit`, `highlight` and optional `target` are authored display fields.

Example break-even: values `0,24,48,72`, x positions `0,40,80,120`, fixed cost
`48`, unit `triệu đồng/tháng`, x label `Ly mỗi ngày`, highlighted item2.
These example numbers are explanatory arithmetic, not measurements of a real
venue. This renderer does not establish source accuracy or aesthetic approval.

Keep important content inside the safe area and inspect actual rendered frames.
The full final spoken sentence and its caption remain visible through the tail.
