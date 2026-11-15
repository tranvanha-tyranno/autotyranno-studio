# China context assets — source selection

20 candidates are ready: 16 new photographs and four 9-second, 1280×720 real-video derivatives; selected files total 15,184,666 bytes. All were sourced for this batch and are not cafe/grocery assets. Candidates are optional: original maps, diagrams and simulations should carry the mechanism and figures. Use each chosen source ID at most once.

## Recommended concise uses

| Spoken context | Candidate | What the pixels support | Material limitation |
| --- | --- | --- | --- |
| Export/logistics | `cn-yangshan-port` | Container stacks and gantry cranes at Yangshan | Archival 2017; not export-volume evidence |
| Manufacturing | `cn-auto-assembly`, `cn-toy-assembly-workers` | Geely car line; manual puzzle-cube assembly | Different factories/dates; Geely is not BYD and not established as EV production |
| Automation/labor | `cn-industry-robots`, `cn-toy-assembly-workers` | Visible industrial automation versus manual assembly | A comparison illustrates mechanisms, not a measured displacement or same-factory before/after |
| Consumption | `cn-shanghai-supermarket`, `cn-nanjing-shoppers` | Shanghai storefront and shopping-street pedestrians | Crowds/storefront do not prove purchases, confidence or spending trends |
| Solar versus housing context | `cn-solar-golmud`, `cn-shenzhen-residential` | Golmud solar-array satellite image; Shenzhen residential street/construction | Different places/years; no claims about occupancy, current output or measured national sector shares |
| Brief moving retail | `cn-clip-guangzhou-retail` | People passing a Guangzhou mall tea counter | Intrinsic CoCo signage; no purchases or consumption growth proved |
| Brief moving city | `cn-clip-shenzhen-night` | Shenzhen waterfront night skyline | Context only; not a growth or vacancy indicator |
| Brief moving rail | `cn-clip-shenzhen-train` | Seated train interior and overhead racks | Source calls it high-speed; speed/route not established from images |
| Brief moving market | `cn-clip-china-market` | Pedestrians and shops along a Chinese market street | Exact city not established; do not relabel it Shanghai/Shenzhen |

## Specific restrictions

- `cn-byd-shenzhen-display` is BYD **retail in a mall**, not BYD manufacturing. `cn-engine-mianyang` is source-described BMW engine production, not battery/EV production.
- `cn-hangzhou-metro-construction` is metro Line 15 construction. It must not illustrate an asserted stalled residential development.
- `cn-beijing-seniors` is an archival cultural activity in Jingshan Park (2007), not evidence of precise ages, pensions, poverty or population statistics.
- `cn-solar-yangyuan` remains in raw selection receipts but is **excluded from the production catalog**: distant plane-window framing does not clearly show useful solar panels.
- The Shenzhen residential and BYD display photos have small intrinsic lower-right camera timestamps. A lower-5% crop is suggested in the catalog, but the final actual crop still needs inspection. The 960-pixel worker/senior/silk photos suit inset panels.

## Inspection and provenance

Opened the actual downloaded photo contact sheets (including additional worker/senior/silk sheet), plus five sampled frames from each of the four actual video derivatives at approximately 0.43, 2.23, 4.50, 6.73 and 8.53 seconds. Visible content and mismatches are recorded per asset in `sources-candidates.json`. These are source/sample observations, not a claim of continuous audiovisual listening or final rendered-frame approval. No requested channel branding or source-overlay watermark was observed in these samples. Intrinsic real-world brands are identified separately and do not imply endorsement.

Country/location comes from each primary source description/title/location metadata, never ethnicity. The Chinese market video establishes country only; the robotics photo establishes country only. None of the images is evidence for disputed map boundaries.

Commons creator, license URL, page URL, date, asset hash and modification statements are in the catalog; the complete primary metadata is retained in `selected-photo-metadata.json` and `photo-search-receipts.json`. Attribute each selected CC BY/CC BY-SA source with creator/title/source/license and modifications. Adapted CC BY-SA photographs remain under their respective original licenses; original diagrams/graphics are separate works. Preserve the source file and attribution when cropping/animating it.

Pexels video pages were checked for their source descriptions, creator and the Pexels License (https://www.pexels.com/license/). Publication dates are source-page dates, **not recording dates**. Official source URLs are retained in `videos/download-receipts.json`. To bound disk/bandwidth output, FFmpeg streamed the first nine seconds of the official higher-resolution rendition into a silent 720p/30fps H.264 derivative at native playback timing. Raw 4K sources were not saved locally, so the hashes bind downloaded derivatives, not original remote files. Each derivative is under 4.3 MB. Further trims/crops belong in production receipts.
