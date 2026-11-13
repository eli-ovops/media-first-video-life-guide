import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import sharp from '/Volumes/EXTERNAL/.codex-global-tools/npm/lib/node_modules/hyperframes/node_modules/sharp/dist/index.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const movie=process.argv[2]?path.resolve(process.argv[2]):path.join(root,'renders/人生指南-首条-v1.mp4');
const revision=process.argv[3]||'final';
if(!/^[a-z0-9-]+$/.test(revision))throw new Error('Invalid revision label');
const dir=path.join(root,`evidence/${revision}-frames`);await fs.mkdir(dir,{recursive:true});
const times=revision==='bilingual-final'?[0,.4667,.5,1.5,8.5,16.5,18,23.5,25.5,28.5,32.5,34.9,37.2,39,40.5,42.7,44.5,47.4,49.5,52.5,56.2,58.7,59.3,59.45]:[1,5,8,10.85,11.05,16,21.65,23,25,27.98,30.95,32,33.35,34.4,36.7,38.5,39.95,42.2,44,46.9,49,52,55.7,58.2];
const files=[];
for(let i=0;i<times.length;i++){
 const file=path.join(dir,`frame-${String(i).padStart(2,'0')}-at-${times[i]}.jpg`);
 let exists=false;try{exists=(await fs.stat(file)).size>0;}catch{}
 if(!exists)execFileSync('/Users/USER/.local/bin/ffmpeg',['-hide_banner','-nostdin','-v','error','-ss',String(times[i]),'-i',movie,'-frames:v','1','-q:v','2',file],{stdio:'pipe'});
 files.push(file);
}
for(let sheet=0;sheet<2;sheet++){
 const layers=[];
 for(let j=0;j<12;j++){
  const i=sheet*12+j;let img=await sharp(files[i]).resize(270,480).toBuffer();
  layers.push({input:img,left:(j%4)*270,top:Math.floor(j/4)*508});
  const label=Buffer.from(`<svg width="270" height="28"><rect width="270" height="28" fill="#17251e"/><text x="12" y="21" font-family="sans-serif" font-size="18" fill="#f5f1e8">${times[i]}s</text></svg>`);
  layers.push({input:label,left:(j%4)*270,top:Math.floor(j/4)*508+480});
 }
 await sharp({create:{width:1080,height:1524,channels:3,background:'#17251e'}}).composite(layers).jpeg({quality:95}).toFile(path.join(root,`evidence/${revision}-sheet-${sheet+1}.jpg`));
}
const crop=revision==='pip-final'||revision==='bilingual-final'?{left:113,top:275,width:330,height:370}:{left:90,top:500,width:430,height:780};
const pair=revision==='bilingual-final'?[23.5,25.5]:[23,25];
let a=await sharp(files[times.indexOf(pair[0])]).extract(crop).removeAlpha().raw().toBuffer();
let b=await sharp(files[times.indexOf(pair[1])]).extract(crop).removeAlpha().raw().toBuffer();
let abs=0,changed=0;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-b[i]);abs+=d;if(d>20)changed++;}
let result={movie,timestamps:times,scope:'实际成片场景/转场采样；不是完整动态看听',directory_region:crop,directory_frame_pair:pair,directory_mean_absolute_pixel_difference:abs/a.length,directory_changed_channel_fraction:changed/a.length,notes:'像素差异仅作录屏进入成片的辅助证据；动作和内容由实际采样图阅读确认。'};
await fs.writeFile(path.join(root,`evidence/${revision}-visual-check.json`),JSON.stringify(result,null,2));
const coverIndex=revision==='bilingual-final'?0:times.indexOf(16);
const coverFile=revision==='bilingual-final'?'renders/封面海报-v3-preview.jpg':revision==='pip-final'?'renders/封面-画中画-v2.jpg':'renders/封面-首版.jpg';
await sharp(files[coverIndex]).jpeg({quality:95}).toFile(path.join(root,coverFile));
console.log(JSON.stringify({frames:files.length,contactSheets:2,meanDifference:result.directory_mean_absolute_pixel_difference}));
