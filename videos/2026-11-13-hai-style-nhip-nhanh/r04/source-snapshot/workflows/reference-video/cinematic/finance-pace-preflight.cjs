const fs=require('node:fs');const path=require('node:path');
const {openBrowser,selectComposition,renderStill}=require('@remotion/renderer');
(async()=>{
 const[bundle,propsFile,out]=process.argv.slice(2),inputProps=JSON.parse(fs.readFileSync(propsFile,'utf8'));
 const browser=await openBrowser('chrome');
 try{
  for(const[style,id]of[['comic','FinancePacedComic'],['flow','FinancePacedFlow']]){
   const dir=path.join(out,style,'preflight');fs.mkdirSync(dir,{recursive:true});
   const composition=await selectComposition({serveUrl:bundle,id,inputProps,puppeteerInstance:browser});
   for(const shot of inputProps.plan.shots){
    const frame=shot.from+Math.floor(shot.duration*.62),output=path.join(dir,`${shot.id}-${String(frame).padStart(5,'0')}.jpg`);
    if(!fs.existsSync(output))await renderStill({serveUrl:bundle,composition,inputProps,frame,output,scale:.6,imageFormat:'jpeg',jpegQuality:90,puppeteerInstance:browser,logLevel:'error'});
   }
   console.log('SHOT_PREFLIGHT',style,inputProps.plan.shots.length);
  }
 }finally{await browser.close({silent:true});}
})().catch(e=>{console.error(e);process.exit(1)});
