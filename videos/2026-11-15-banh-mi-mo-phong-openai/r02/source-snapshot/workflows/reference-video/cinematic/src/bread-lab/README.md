# BreadLab renderer contract

Entry `../bread-lab-entry.tsx`, composition `BreadLab`, 1920×1080/30fps. This isolated renderer does not change the retained BreadDocumentary output.

Props `{plan:{fps,durationFrames,title,shots,audio},startFrame?,frames?}`. `from`, `duration`, `cueFrames`, proof offsets use frames; `sourceStartSeconds` alone uses seconds. All file/audio paths are relative to the chosen Remotion public directory. Video interludes require actual moving `file`; simulations may omit it. A simulation is selected by `simulation`, not `kind`. `media` accepts `video`, `graphic`, `simulation`.

Shot fields extend the old BreadShot interface with `simulation`, `narrationId/narrationUnit`, and `overlay:{title,kicker?,items?:string[]}`. Up to three short information items can appear over real footage; they are editorial points, not automatic subtitles. Exact cue frames must be integer, strictly ordered and inside each shot. Defaults are only development fallbacks; production should use aligned narration.

| Simulation | Meaning / data.stage | Cue order |
|---|---|---|
| `money_split` | Default: baseline → cost change → selling price. `before`: baseline only. `after`: start baseline piles then higher cost, then higher selling price. `compare`: **after state fully known at frame0**, later trace before3k versus after2.5k. | Default/before `[split,costChange,priceRaise,summary]`; after `[costChange,priceRaise,summary]`; compare `[beforeGhost,addedSaleVsAddedCost,conclusion]` |
| `price_level` | 20k→22k→22.44k, +10%→+2%; line ends above previous price. | `[firstRise,secondRise,conclusion]` |
| `inventory` | Old stock feeds today's bowl throughout; lower-price new stock arrives and **waits on shelf**, never feeds the same batch. | `[consumeOld,newArrives,currentBatchContext,delayConclusion]` |
| `cost_ledger` | Default: flour lower, rent/pay held, other inputs unknown; total unknown. `counterexample`: price/sales held, total cost assumed to have fallen; remaining surplus may rise. | `[flourDown,otherRows,total,conditionalResult]` |
| `cost_ledger` | `not_net_profit`: 3k plus uncounted taxes/depreciation/owner labor. No flour movement. | `[tax,depreciation,ownerLabor,notNetConclusion]` |
| `cost_ledger` | `question`: lower news rate does not establish individual invoices; only the final cue asks conditional future flour example. | `[flourUnknown,rentUnknown,electricUnknown,futureQuestion]` |
| `competition` | Two equivalent bread choices, consumer-choice dots move. At cue2 the alternative becomes inconvenient and pressure weakens. `weak_alternative` starts weak. | `[alternative,customerSwitch,weakAlternative]` |
| `bread_power` | Default: full wage/price/quantity sequence. `income`: only bread20k→22k, income10m→10.5m; no bread quantity grid. | `income:[price22k,income10m,income10.5m,conclusion]` |
| `bread_power` | `quantity`: known wage/price inputs, 500 bread units become477; 23 rounded missing units leave grid. | `[500Intro,477Reveal,result,conclusion]` |
| `bread_power` | `result`: 477/−4.5% known at frame0; no repeated salary or500→477 transition. | `[conclusion]` |
| `basket_scope` | Default: bread moves into a broader set of spending groups. `households`: two qualitative household compositions differ. Areas are explicitly not measured CPI weights. | `[breadOrHouseholdA,otherCategoriesOrHouseholdB,compositionDifference,conclusion]` |
| `synthesis` | Three connected foci with exact order matching final narration: costs, price rate, income. | `[costFocus,priceFocus,incomeFocus,connect]` |

All money is the existing illustrative model:20/22k sale,12/14.5k variable,5k fixed allocation,3/2.5k remainder. Fixed-token color is gray, input rust, remainder green, added payment gold. Each monetary token is500đ. Remainder is not labeled net profit. Bread purchasing power uses10m/20k=500 versus10.5m/22k≈477.27, approximately−4.55%; the grid rounds to477 and23 missing. These quantities do not represent actual consumption or CPI. Qualitative diagrams add no empirical market numbers.

Local Be Vietnam Pro fonts wait for all400/600/700 weights before rendering. All state animation is driven by local frame and exact cues. Real footage hard-cuts on narration boundaries; only overlays fade briefly. Final audio is supplied by the runner without changing speed. The runner must normalize video track timebases before concat, retaining the previous BreadDocumentary lesson.

Synthetic runtime evidence lives in the new batch's `renderer-runtime-proof/`: eight family states, semantic stage cases, and two60-frame decoded moving processes. That evidence checks runtime, numbers and selected layouts only. It does not replace actual take-aligned scenes, listening or user approval.
