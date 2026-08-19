#!/usr/bin/env node
/* Match acquisition works to Muktabodha's published e-text catalogue. */
"use strict";
const child = require("child_process");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const file = process.argv[2];
if (!file || process.argv.includes("--help")) { console.error("Usage: node scripts/discover_muktabodha_catalog.js <catalog.csv> [--json]"); process.exit(1); }
function csv(line) { const out=[]; let part="", quoted=false; for(let i=0;i<line.length;i++){const c=line[i]; if(c==='"'){if(quoted&&line[i+1]==='"'){part+='"';i++;}else quoted=!quoted;} else if(c===','&&!quoted){out.push(part);part="";}else part+=c;} out.push(part); return out; }
function key(value) { return String(value||"").replace(/[āā]/g,"a").replace(/[ī]/g,"i").replace(/[ū]/g,"u").replace(/[ṛṝ]/g,"r").replace(/[ḷ]/g,"l").replace(/[ṅñṇ]/g,"n").replace(/[ṭṭ]/g,"t").replace(/[ḍ]/g,"d").replace(/[śṣ]/g,"s").replace(/[ṃṁ]/g,"m").replace(/[ḥ]/g,"h").replace(/z/g,"s").toLowerCase().replace(/[^a-z0-9]/g,""); }
const lines=fs.readFileSync(file,"utf8").trim().split(/\r?\n/); const headers=csv(lines.shift()); const rows=lines.map(csv).map(v=>Object.fromEntries(headers.map((h,i)=>[h,v[i]||""])));
const queue=JSON.parse(child.execFileSync(process.execPath,[path.join(ROOT,"scripts/report_acquisition_queue.js"),"--json"],{encoding:"utf8"})).works.filter(w=>w.language==="sanskrit");
const hits=[];
for(const work of queue){
  const wk=key(work.work_id), tk=key(work.title_iast), ak=key(work.thinker_id);
  if(wk.length<6)continue;
  for(const row of rows){
    const title=[row.uniform_title,row.main_title,row.secondary_title,row.path].map(key).join(" ");
    const author=key(row.author);
    const titleMatch=title.includes(wk)||(tk.length>=8&&title.includes(tk));
    if(!titleMatch)continue;
    const authorMatch=author && (author.includes(ak)||ak.includes(author));
    const authorConflict=author && !authorMatch;
    if(authorConflict)continue;
    hits.push({thinker_id:work.thinker_id,work_id:work.work_id,title_iast:work.title_iast,catalog_no:row.catalog_no,path:row.path,uniform_title:row.uniform_title,author:row.author,source_description:row.source_description,license:row.license,confidence:authorMatch?"author-and-title-match":"title-match-author-unidentified",note:"Verify coverage and title-level metadata before candidate registration."});
  }
}
const report={queue_total:queue.length,catalog_records:rows.length,title_matches:hits.length,candidates:hits}; if(process.argv.includes("--json")) console.log(JSON.stringify(report,null,2)); else {console.log(`Muktabodha catalogue discovery: ${hits.length} title match(es).`);for(const h of hits)console.log(`${h.thinker_id}\t${h.work_id}\t${h.catalog_no}\t${h.uniform_title}`);}
