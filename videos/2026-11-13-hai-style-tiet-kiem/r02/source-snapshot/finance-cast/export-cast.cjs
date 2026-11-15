/* Native SVG export; no paid services or browser required. Run from cinematic/. */
const fs = require('fs');
const path = require('path');
const ts = require('typescript');
const React = require('react');
const {renderToStaticMarkup} = require('react-dom/server');
for (const ext of ['.ts','.tsx']) {
  require.extensions[ext] = (module, filename) => {
    const source = fs.readFileSync(filename,'utf8');
    const compiled = ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX,target:ts.ScriptTarget.ES2018,esModuleInterop:true}}).outputText;
    module._compile(compiled,filename);
  };
}
const {roster} = require('./roster.ts');
const {Character} = require('./Character.tsx');
const destination=path.resolve(process.argv[2] || 'public/finance-cast');
fs.mkdirSync(destination,{recursive:true});
for(const c of roster) {
  const svg=React.createElement('svg',{xmlns:'http://www.w3.org/2000/svg',width:720,height:1040,viewBox:'-180 -500 360 520',role:'img','aria-label':`${c.name} — ${c.role}`},React.createElement(Character,{id:c.id,emotion:'neutral',pose:'idle',frame:42}));
  fs.writeFileSync(path.join(destination,`${String(c.id).padStart(2,'0')}.svg`),renderToStaticMarkup(svg),'utf8');
}
const data={schema:'finance-cast/1',medium:'original-native-svg-2d',status:'preview-pending-user-feedback',count:roster.length,characters:roster};
fs.writeFileSync(path.join(destination,'roster.json'),JSON.stringify(data,null,2)+'\n','utf8');
fs.writeFileSync(path.resolve(__dirname,'../../../finance-cast.json'),JSON.stringify(data,null,2)+'\n','utf8');
console.log(JSON.stringify({directory:destination,characters:roster.length,format:'svg',paidCalls:0}));
