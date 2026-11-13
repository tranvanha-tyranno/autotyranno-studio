const fs=require('node:fs');
const path=require('node:path');
const {bundle}=require('@remotion/bundler');
const {openBrowser,selectComposition,renderStill}=require('@remotion/renderer');

(async()=>{
 const batch=path.resolve(process.argv[2]);
 const out=path.join(batch,process.argv[5]||'preview');fs.mkdirSync(out,{recursive:true});
 const props=JSON.parse(fs.readFileSync(path.join(batch,'props.json'),'utf8'));
 props.data.audio='';
 const requested=(process.argv[3]||'').split(',').filter(Boolean);
 const rows=props.data.shots.filter(s=>!requested.length||requested.includes(s.id));
 const started=new Date().toISOString(),clock=performance.now();
 const serveUrl=await bundle({entryPoint:path.resolve(__dirname,process.argv[4]||'src/china-variety-entry.tsx'),outDir:path.join(out,'bundle'),publicDir:path.join(batch,'production-public'),onProgress:()=>{}});
 const browser=await openBrowser('chrome');
 try{
  const composition=await selectComposition({serveUrl,id:'ChinaPreview',inputProps:props,puppeteerInstance:browser});
  const captures=[];
  for(let i=0;i<rows.length;i+=2){
   const result=await Promise.all(rows.slice(i,i+2).map(async s=>{
    const frame=Math.floor((s.start+s.end)/2),output=path.join(out,`${s.id}.jpg`);
    await renderStill({serveUrl,composition,inputProps:props,frame,output,imageFormat:'jpeg',jpegQuality:88,puppeteerInstance:browser,logLevel:'error',overwrite:true});
    return {id:s.id,frame,file:path.basename(output)};
   }));captures.push(...result);console.log('CAPTURED',...result.map(r=>r.id));
  }
  fs.writeFileSync(path.join(out,'capture-receipt.json'),JSON.stringify({startedUTC:started,finishedUTC:new Date().toISOString(),wallSeconds:(performance.now()-clock)/1000,captures,scope:'Actual rendered midpoint images; requires visual review, not an animation/aesthetic acceptance check.'},null,2));
 }finally{await browser.close({silent:true});}
})().catch(e=>{console.error(e);process.exit(1)});
