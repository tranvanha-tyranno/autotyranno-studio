const fs = require('node:fs');
const path = require('node:path');
const {openBrowser, selectComposition, renderStill} = require('@remotion/renderer');
(async () => {
  const [bundle, propsFile, out] = process.argv.slice(2);
  const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
  const browser = await openBrowser('chrome');
  try {
    const composition = await selectComposition({serveUrl: bundle, id: 'EconomyStory', inputProps, puppeteerInstance: browser});
    const dir = path.join(out, 'preflight');fs.mkdirSync(dir, {recursive: true});
    for (const beat of inputProps.plan.segments) {
      const frame = beat.from + Math.floor(beat.duration * .55);
      const output = path.join(dir, `beat-${beat.id}-${String(frame).padStart(5,'0')}.jpg`);
      if (!fs.existsSync(output)) await renderStill({serveUrl: bundle, composition, inputProps, frame, output, scale: .65, imageFormat: 'jpeg', jpegQuality: 92, puppeteerInstance: browser, logLevel: 'error'});
    }
    console.log('ECONOMY_PREFLIGHT', inputProps.plan.segments.length);
  } finally { await browser.close({silent: true}); }
})().catch(error => { console.error(error);process.exit(1); });
