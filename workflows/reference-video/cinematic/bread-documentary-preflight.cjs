// Samples only; moving proof scenes and listening remain separate review steps.
const fs = require('node:fs');
const path = require('node:path');
const {openBrowser, selectComposition, renderStill} = require('@remotion/renderer');

(async () => {
  const [bundle, propsFile, outputRoot, shotIds] = process.argv.slice(2);
  if (!bundle || !propsFile || !outputRoot) throw new Error('Usage: node bread-documentary-preflight.cjs BUNDLE PROPS_JSON OUTPUT_DIR [id1,id2]');
  const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8').replace(/^\uFEFF/, ''));
  const startFrame = inputProps.startFrame ?? 0;
  const frames = inputProps.frames ?? inputProps.plan.durationFrames - startFrame;
  const selectedIds = shotIds ? new Set(shotIds.split(',')) : null;
  const browser = await openBrowser('chrome');
  const samples = [];
  const dir = path.join(outputRoot, 'preflight');
  fs.mkdirSync(dir, {recursive: true});
  try {
    const composition = await selectComposition({serveUrl: bundle, id: 'BreadDocumentary', inputProps, puppeteerInstance: browser, logLevel: 'error'});
    for (const shot of inputProps.plan.shots) {
      if (selectedIds && !selectedIds.has(shot.id)) continue;
      if (shot.from >= startFrame + frames || shot.from + shot.duration <= startFrame) continue;
      const offsets = [...new Set([
        Math.round(shot.duration * .15), Math.round(shot.duration * .55), Math.round(shot.duration * .88),
        ...(shot.cueFrames ?? []).map(frame => Math.min(shot.duration - 8, frame + 8)),
      ])].sort((a, b) => a - b);
      for (const offset of offsets) {
        const absoluteFrame = shot.from + offset;
        const frame = absoluteFrame - startFrame;
        if (frame < 0 || frame >= frames) continue;
        const output = path.join(dir, `${shot.id}-${String(absoluteFrame).padStart(6, '0')}.jpg`);
        await renderStill({serveUrl: bundle, composition, inputProps, frame, output, scale: .6,
          imageFormat: 'jpeg', jpegQuality: 93, puppeteerInstance: browser, logLevel: 'error'});
        samples.push({shotId: shot.id, kind: shot.kind ?? 'video', stage: shot.data?.stage ?? null,
          absoluteFrame, compositionFrame: frame, localShotFrame: offset, image: output});
      }
    }
  } finally { await browser.close({silent: true}); }
  const report = {schema: 'bread-documentary-preflight/1', method: 'selected_rendered_frames',
    continuousAvReview: false, aestheticApproval: false, audioListened: false,
    startFrame, frames, samples};
  fs.writeFileSync(path.join(outputRoot, 'preflight-report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log('BREAD_PREFLIGHT', samples.length);
})().catch(error => { console.error(error); process.exit(1); });
