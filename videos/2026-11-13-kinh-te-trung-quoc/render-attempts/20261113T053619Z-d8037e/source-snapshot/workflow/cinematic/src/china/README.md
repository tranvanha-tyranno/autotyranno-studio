# China economy motion renderer

Entry `src/china-entry.tsx`, composition `ChinaPreview`, props `{data: ChinaTimeline}`.
Exact contract is in `types.ts`. This entry imports typography/media primitives
from the business renderer, but no prior photos, clips, coffee geometry or channel
branding. All motion is deterministic from composition frames. No remote tile
server, key, WebGL scene or paid asset generation is needed at render time.

## Scene forms

| Layout | Authored data | Visual form |
| --- | --- | --- |
| c-map | design.map | China equal-area reference or world connection diagram |
| c-flow | design.flow | Directed economic transmission / Sankey-style ribbon diagram |
| c-chart | design.chart | Bars, signed contribution waterfall, time series, multiple series |
| c-sim | simulation.kind=factory | Conveyor and processing parts; motion speed explicitly schematic |
| c-sim | simulation.kind=household | Allocation ring and exact authored item values |
| c-sim | simulation.kind=property | Property/balance-sheet transmission nodes |
| c-sim | simulation.kind=cohorts | Cohort value bars with a restrained demographic illustration |
| c-compare | design.comparison | Two/three policy choices and optional comparison rows |
| c-question | headline/body/emphasis | One kinetic question and selective emphasis |
| c-photo / c-closing | inspected images/clips | Contextual media with native-speed clips and exact cues |

Statistical values are read directly from the authored manifest. Source date,
unit and scope belong in headline/eyebrow/body/sourceNote. This renderer does not
know whether a statistic is verified or whether a scenario is a prediction.

## Cue timing

`design.cues` is local frames, not seconds. Exact phrase alignment must be made
after final narration. Supply one cue per element when explicit staggered order
matters. Unspecified cues use fallback frame timing. Chart lines use cue0 as the
start of the line reveal. Photo media use cue0/1 for cuts to media2/3; media1 is
at frame0. Every original clip must cover its assigned interval without looping.

## Charts and diagrams

Waterfalls treat the final item as a separately authored balance anchored at
zero; preceding items are signed changes. Line graphs use actual `items[].x`
with a fitted domain so years such as2020–2025 do not collapse at one edge.
`chart.min` may state a signed vertical minimum; automatic negative domains leave
space above x-axis labels. Multiple series use
`series:[{label,color,items:[{label,x,value}]}]`, while primary `items` remains
required. Keep one unit per chart and use a separate chart for incompatible units.

Flow node columns run left-to-right (`column:0,1,2`). Link values set relative
ribbon widths; if these are schematic weights, state that in `flow.note`.
Never present arbitrary widths as measured trade shares. Factory conveyor
movement is always labeled schematic; displayed item values still require
their own source or explicit scenario label. Household ring angles normalize
within the displayed items and do not imply those items cover a whole economy.

## Geographic data

`geography/natural-earth-110m.json` retains177country geometries from Natural
Earth110m Admin0, with coordinate precision reduced to4decimals. Source and
SHA256 receipts are in `geography/source-receipt.json`. No population/GDP
attributes from the geographical file are used as economic statistics.

China view uses Albers equal-area conic (105°E center,25°/47°N standard
parallels). The international diagram uses equirectangular world positioning.
Animated arcs are schematic connections, not geodesics or verified shipping
routes. The neutral visible boundary note and Natural Earth source must remain.
The generalized data does not resolve or endorse territorial claims.

Maps with many close nodes need rendered label review. Supply only the nodes
needed for the current spoken point. Do not infer geographic correctness,
semantic relevance or aesthetic acceptance from a TypeScript/render pass.
