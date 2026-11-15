const fs=require('node:fs');const path=require('node:path');
const {openBrowser,selectComposition,renderStill}=require('@remotion/renderer');
(async()=>{
 const [bundle,propsFile,out]=process.argv.slice(2);const inputProps=JSON.parse(fs.readFileSync(propsFile,'utf8'));
 const browser=await openBrowser('chrome');
 try{
  for(const [style,id] of [['comic','FinanceLongComic'],['flow','FinanceLongFlow']]){
   const dir=path.join(out,style,'preflight');fs.mkdirSync(dir,{recursive:true});
   const composition=await selectComposition({serveUrl:bundle,id,inputProps,puppeteerInstance:browser});
   // Every beat, at its exact cue and at a developed later state.
   for(const s of inputProps.plan.segments){
    for(const [label,local] of [['cue',s.cueFrame+10],['late',Math.floor(s.duration*.78)]]){
     const frame=Math.min(s.from+s.duration-1,s.from+local);
     const output=path.join(dir,`${s.id}-${label}-${frame}.jpg`);
     if(!fs.existsSync(output))await renderStill({serveUrl:bundle,composition,inputProps,frame,output,scale:.6,imageFormat:'jpeg',jpegQuality:90,puppeteerInstance:browser});
    }
   }
   console.log('PREFLIGHT',style);
  }
 }finally{await browser.close({silent:true});}
})().catch(e=>{console.error(e);process.exit(1)});
