import fs from 'node:fs/promises';
import path from 'node:path';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';

const args = process.argv.slice(2);
const arg = (key, fallback) => {const i = args.indexOf(key); return i < 0 ? fallback : args[i + 1];};
const batch = path.resolve(arg('--batch', '.'));
const serveUrl = path.resolve(arg('--bundle', 'build'));
const props = JSON.parse(await fs.readFile(path.join(batch, 'props.json'), 'utf8'));
const filter = arg('--ids', '').split(',').filter(Boolean);
const out = path.join(batch, 'proofs');
await fs.mkdir(out, {recursive: true});
const browser = await openBrowser('chrome', {logLevel: 'error'});
const manifest = [];
try {
  const composition = await selectComposition({serveUrl, id: 'SemanticReview', inputProps: props, puppeteerInstance: browser, logLevel: 'error'});
  for (const shot of props.data.shots) {
    if (filter.length && !filter.includes(shot.id)) continue;
    const frame = Math.min(shot.end - 1, shot.start + Math.max(1, Math.round((shot.end - shot.start) * .72)));
    const file = `${shot.id}-${frame}.jpg`;
    await renderStill({serveUrl, composition, inputProps: props, puppeteerInstance: browser,
      output: path.join(out, file), frame, imageFormat: 'jpeg', jpegQuality: 92, overwrite: true, logLevel: 'error'});
    manifest.push({id: shot.id, frame, file, scene: shot.scene, mode: shot.mode,
      narratedText: shot.narratedText, requiredVisual: shot.requiredVisual, visibleFacts: shot.visibleFacts,
      reviewStatus: 'requires_actual_visual_review'});
    process.stdout.write(`PROOF ${shot.id} ${frame}\n`);
  }
} finally {
  await browser.close({silent: true});
}
await fs.writeFile(path.join(out, filter.length ? 'selected-manifest.json' : 'manifest.json'), JSON.stringify(manifest, null, 2));
