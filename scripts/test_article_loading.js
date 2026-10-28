#!/usr/bin/env node
"use strict";

// Behavioral lifecycle tests: execute real app entrypoints, Markdown, KaTeX,
// numbering and footer code. Network/script/thinker dependencies are controlled.
// The deliberately bounded DOM fixture checks ownership, writes and node identity;
// it does NOT establish browser parsing, selection, layout, find or performance.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const app = fs.readFileSync(process.env.ARTICLE_LOADING_APP || path.join(root, "assets/app.js"), "utf8");
function section(start, end) {
  const a = app.indexOf(start), b = app.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `application section found: ${start}`);
  return app.slice(a, b);
}
const code = [
  section("async function loadJSON(", "async function loadPrimitiveGraph("),
  section("async function loadCitationIndex(", "// Interpretations are distinct"),
  section("// ---------- markdown helpers", "// The active chronology resolver"),
  section("function openPanel(", "function showTab("),
  section("async function openThinker(", "function scrollDotIntoView("),
  section("let panelNavigationVersion =", "// Markdown renderer for the article reader."),
  section("// Markdown renderer for the article reader.", "// ---------- keyboard nav"),
].join("\n");

const { Element } = require("./test_helpers/article_dom");
function deferred() { let resolve, reject; const promise = new Promise((a,b) => { resolve=a; reject=b; }); return { promise, resolve, reject }; }
const tick = () => new Promise(resolve => setImmediate(resolve));
async function settle() { await tick(); await tick(); }
const key = "author/work/1";
const index = { entries: { [key]: { author_name: "Reviewed author", work_title: "Reviewed work", locus: "Precise locus" } } };
const cited = `# Opening\n\nFIRST paragraph [source](cite://${key}).\n\n\\(x+1\\)\n\nLAST paragraph [same](cite://${key}).`;
function harness() {
  const body = new Element("body"), articleBody = new Element(), detail = new Element(), mode = new Element(); body.append(articleBody,detail,mode);
  const routes = [], requests = [], passageCalls = [], errors = [];
  let responder = async url => ({ ok:true, text:async () => url.includes("b.md") ? "# B\n\nB ONLY" : cited, json:async () => index });
  const c = {
    URL, location: { href:"https://example.test/", pathname:"/", search:"" }, DATA_VERSION:"test",
    state: { thinkersById:new Map([["t",{id:"t"}]]), citationIndex:null, glossaryRegex:null, activeId:null },
    panelState: {open:false,activeTab:"thinker",loaded:{}},
    PANEL_TABS:["thinker","article","translation","citation","source"], dpTabBar:null, localStorage:{setItem(){}}, ensureSourceTreeRendered(){},
    document: {body, getElementById:()=>null, querySelectorAll:s=>body.querySelectorAll(s), createElement:t=>new Element(t)},
    dpArticleBody:articleBody, dpReaderMode:mode, dpTabTitle:new Element(), dpArticleHead:null,
    detailContent:detail, detailPane:new Element(), stage:null,
    router: { push:r=>routes.push({...r}), _suspendSerialize:false }, history:{replaceState:()=>routes.push({kind:"closed"})},
    fetch: input => { const url=String(input); requests.push(url); return responder(url); },
    SAHASRANAMA_READING:{slug:"sahasranama",title:"Sahasranama",dataUrl:"reader.json",detailsUrl:"reader-details.json"}, GITA_READINGS:{gita:{title:"Gita",base:"gita/",files:["verses.js"],data:()=>({})}},
    closeArticlesModal(){}, applyTabContext(){}, clearDetailPaneWidth(){}, rememberPwaRoute(){},
    setReadingMode(){}, colorFor:()=>"black", scrollDotIntoView(){},
    loadThinkerById:async ()=>({id:"t"}), renderDetail:()=>"<p>THINKER VIEW</p>",
    applyDetailPaneWidth(){},
    loadScriptOnce:async ()=>{},
    linkifyGlossaryText:s=>s, gitaGlossaryResolve:()=>null, openGlossary(){},
    setTimeout, clearTimeout, requestAnimationFrame:fn=>setTimeout(fn,0),
    console:{log(){},warn(){},error:e=>errors.push(e)},
    katex:require(path.join(root,"assets/vendor/katex-0.19.1/katex.min.js")),
  };
  c.window = c;
  c.GitaReader = {render:container=>{container.innerHTML="<p>GITA VIEW</p>";}, renderPassages:(container,passages)=>{passageCalls.push({container,passages});container.appendChild(new Element("p",{},"PASSAGES"));}};
  c.SahasranamaReader = { render:async container=>{container.innerHTML="<p>SAHASRANAMA VIEW</p>";} };
  vm.createContext(c); vm.runInContext(code,c);
  return {c,body:articleBody,routes,requests,passageCalls,errors,setResponder:fn=>{responder=fn;}};
}
// Exercise the actual asynchronous engine and its shared state, not a simulated
// renderer. Pure presentation and event wiring are bounded substitutes here;
// acquisition, merging, mode state and every awaited render continuation are real.
function installActualSahas(h) {
  const source=fs.readFileSync(path.join(root,"assets/sahasranama.js"),"utf8");
  const part=(start,end)=>{const a=source.indexOf(start),b=source.indexOf(end,a);assert.ok(a>=0&&b>a);return source.slice(a,b);};
  const e={window:h.c,performance,fetch:(...args)=>h.c.fetch(...args),localStorage:{setItem(){}},
    requestAnimationFrame:fn=>h.c.requestAnimationFrame(fn),cancelAnimationFrame(){},HTMLMediaElement:{HAVE_METADATA:1}, CSS:{escape:String},
    ensureStyle(){},readChantView:()=>false,readDeepLinkName:()=>null,closeWordCard(){},
    renderAttribution:()=>"",renderPreface:()=>"",renderPostlude:()=>"",renderAudio:()=>"",
    wireWords(){},wireDetails(){},wireAudio(){},wireNameRange(){},updateNameRange(){},writeDeepLinkName(){},
    fmtTime:String,timingAt:()=>"timing",setActiveTiming:(...args)=>h.audioCalls.push(args)};
  h.audioCalls=[];
  if(h.actualAudio)e.renderAudio=()=>'<div class="vsn-recite-bar"><audio></audio><button class="vsn-play"></button><button class="vsn-back"></button><button class="vsn-forward"></button><div class="vsn-progress"></div><span class="rb-bar"></span><span class="rb-time"></span></div>';
  vm.createContext(e);
  vm.runInContext([
    part("let ROOT =", "function esc("),
    part("async function ensureDetails(", "function range("),
    part("async function setDetails(", "function updateNameRange("),
    part("async function openDeepLinkedName(", "function readChantView("),
    part("async function setChantView(", "function wireDetails("),
    part("let MEDIA_SESSION =", "function wireAudio()"),
    part("async function render(root, options)", "window.SahasranamaReader ="),
    h.actualAudio?part("function wireAudio()", "async function render(root, options)"):"",
    `function renderDetailToggle(){return '<p>MODE '+DATA.marker+'</p>';}
     function renderNamesSection(){return '<p>BODY '+DATA.marker+'</p>';}
     function modeControl(selector){return MODE_HOST?.querySelector(selector);}
     globalThis.api={render,setChantView,setDetails,read:()=>({data:DATA,root:ROOT,mode:MODE_HOST,names:NAME_BY_NUMBER})};`
  ].join("\n"),e);
  h.c.SahasranamaReader=e.api;
  h.c.GitaReader.bindWords=container=>{h.boundWords=container;};
  h.c.GitaReader.clearWords=()=>{h.clearCalls=(h.clearCalls||0)+1;};
  const oldRender=h.c.GitaReader.render;
  h.c.GitaReader.render=(container,...args)=>{h.boundWords=container;return oldRender(container,...args);};
  return e.api;
}
const sahasData=marker=>({marker,audio:{units:[]},stanzas:[{names:[{number:1,marker}]}]});
const article = slug => ({slug,title:slug.toUpperCase(),source_doc:`${slug}.md`});
const failures = [];
async function test(name, fn) { try { await fn(); console.log("PASS "+name); } catch(e) { failures.push(name); console.error("FAIL "+name+"\n"+e.stack); } }
function lastRoute(h) { return h.routes.at(-1); }
(async () => {
  await test("readable complete article and fallback footnotes precede metadata; enrichment preserves reading nodes",async()=>{
    const h=harness(), gate=deferred();
    h.setResponder(async url=>url.includes("citation_index") ? gate.promise : {ok:true,text:async()=>cited});
    const opening=h.c.openArticle(article("a")); await settle();
    let before;
    try {
      assert.ok(h.body.textContent.includes("FIRST") && h.body.textContent.includes("LAST"),"all prose visible while metadata unresolved");
      assert.equal(h.body.querySelectorAll(".cite-fn-row").length,1,"complete numbered fallback list deduplicates repeated key");
      assert.equal(h.body.querySelectorAll(".cite-fn-link").length,2);
      assert.ok(h.body.querySelector("math"),"actual KaTeX MathML is already present");
      assert.equal(h.c.panelState.loaded.article,true,"readiness does not depend on metadata");
      before={article:h.body.querySelector("article"),paragraph:h.body.querySelector("p"),writes:h.body.writes}; h.body.scrollTop=319;
    } finally { gate.resolve({ok:true,json:async()=>index}); await opening; await settle(); }
    assert.ok(h.body.textContent.includes("Reviewed work") && h.body.textContent.includes("Precise locus"));
    assert.equal(h.body.querySelector("article"),before.article);
    assert.equal(h.body.querySelector("p"),before.paragraph,"prose nodes remain the same");
    assert.equal(h.body.writes,before.writes,"metadata must not rewrite body");
    assert.equal(h.body.scrollTop,319,"metadata must not reset scroll");
  });
  await test("citation requests share in-flight acquisition, cache success and retry failure",async()=>{
    const h=harness(),gate=deferred();h.setResponder(()=>gate.promise);
    const a=h.c.loadCitationIndex(),b=h.c.loadCitationIndex(); await settle();
    const initial=h.requests.length; gate.resolve({ok:false});await Promise.all([a,b]);
    assert.equal(initial,1,"simultaneous callers issue one request");
    h.setResponder(async()=>({ok:true,json:async()=>index}));await h.c.loadCitationIndex();
    assert.equal(h.requests.length,2,"failed acquisition can retry");
    await h.c.loadCitationIndex();assert.equal(h.requests.length,2,"success remains cached");
    assert.equal(h.c.state.citationIndex.entries[key].author_name,"Reviewed author");
  });
  for (const stage of ["response","text"]) for (const target of ["b","thinker","close"]) {
    await test(`stale source ${stage} cannot commit after ${target}`,async()=>{
      const h=harness(),gate=deferred();h.c.state.citationIndex=index;
      h.setResponder(async url=> url==="a.md" ? (stage==="response" ? gate.promise : {ok:true,text:()=>gate.promise}) : {ok:true,text:async()=>"# B\n\nB ONLY"});
      const a=h.c.openArticle(article("a"));await settle();
      if(target==="b")await h.c.openArticle(article("b"));else if(target==="thinker")await h.c.openThinker("t");else h.c.closePanel();
      const html=h.body.innerHTML,writes=h.body.writes,routes=h.routes.length;h.body.scrollTop=417;
      gate.resolve(stage==="response" ? {ok:true,text:async()=>"A STALE"} : "A STALE");await a;await settle();
      assert.equal(h.body.innerHTML,html,"old source cannot change article pane");assert.equal(h.body.writes,writes);
      assert.equal(h.body.scrollTop,417);assert.equal(h.routes.length,routes,"no route rollback");
      if(target==="close")assert.equal(h.c.panelState.open,false);else assert.equal(h.c.panelState.activeTab,target==="b"?"article":"thinker");
    });
  }
  for(const target of ["b","thinker","close"]) {
    await test(`late metadata cannot mutate current pane or route after ${target}`,async()=>{
      const h=harness(),gate=deferred();h.setResponder(async url=>url.includes("citation_index")?gate.promise:{ok:true,text:async()=>url==="a.md"?cited:"# B\n\nB ONLY"});
      const a=h.c.openArticle(article("a"));await settle();
      if(target==="b")await h.c.openArticle(article("b"));else if(target==="thinker")await h.c.openThinker("t");else h.c.closePanel();
      const html=h.body.innerHTML,routes=h.routes.length;h.body.scrollTop=518;
      gate.resolve({ok:true,json:async()=>index});await a;await settle();
      assert.equal(h.body.innerHTML,html);assert.equal(h.body.scrollTop,518);assert.equal(h.routes.length,routes);
      if(target==="close")assert.equal(h.c.panelState.open,false);
    });
  }
  for(const stage of ["response","json","include","script"]) for(const target of ["b","thinker","close"]) {
    await test(`late passage ${stage} cannot render or reset route after ${target}`,async()=>{
      const h=harness(),gate=deferred();h.c.state.citationIndex=index;
      const pd={passages:[{id:"p"}],includes:stage==="include"?["extra.json"]:[]};
      h.setResponder(async url=>{
        if(url==="passages.json")return stage==="response"?gate.promise:{ok:true,json:()=>stage==="json"?gate.promise:pd};
        if(url==="extra.json")return gate.promise;
        return {ok:true,text:async()=>url==="a.md"?cited:"# B\n\nB ONLY"};
      });
      if(stage==="script")h.c.loadScriptOnce=()=>gate.promise;
      const a=h.c.openArticle({...article("a"),passages_doc:"passages.json"});await settle();
      if(target==="b")await h.c.openArticle(article("b"));else if(target==="thinker")await h.c.openThinker("t");else h.c.closePanel();
      const html=h.body.innerHTML,routes=h.routes.length;h.body.scrollTop=619;
      gate.resolve(stage==="json"?pd:stage==="script"?undefined:{ok:true,json:async()=>pd});await a;await settle();
      assert.equal(h.passageCalls.length,0,"stale passage renderer must not run on shared surface");
      assert.equal(h.body.innerHTML,html);assert.equal(h.body.scrollTop,619);assert.equal(h.routes.length,routes);
      if(target==="close")assert.equal(h.c.panelState.open,false);
    });
  }
  await test("current passages and routes still finish (guard must not suppress legitimate work)",async()=>{
    const h=harness();h.c.state.citationIndex=index;
    h.setResponder(async url=>url.endsWith(".json")?{ok:true,json:async()=>({passages:[{id:"p"}]})}:{ok:true,text:async()=>cited});
    await h.c.openArticle({...article("a"),passages_doc:"passages.json"});
    assert.equal(h.passageCalls.length,1);assert.ok(h.body.textContent.includes("LAST"));
    assert.equal(lastRoute(h).slug,"a");assert.equal(h.c.panelState.loaded.article,true);
  });
  await test("failed optional metadata leaves complete fallback article and can recover",async()=>{
    const h=harness();h.setResponder(async url=>url.includes("citation_index")?{ok:false}:{ok:true,text:async()=>cited});
    await h.c.openArticle(article("a"));await settle();assert.ok(h.body.textContent.includes("LAST"));assert.equal(h.body.querySelectorAll(".cite-fn-row").length,1);
    h.setResponder(async url=>url.includes("citation_index")?{ok:true,json:async()=>index}:{ok:true,text:async()=>cited});
    await h.c.openArticle(article("b"));await settle();assert.ok(h.body.textContent.includes("Reviewed work"));
  });
  for (const kind of ["gita", "sahasranama"]) for (const phase of ["script", "render"]) {
    await test(`late interactive ${kind} ${phase} cannot alter replacement article`,async()=>{
      const h=harness(),gate=deferred();h.c.state.citationIndex=index;
      if(phase==="script") h.c.loadScriptOnce=()=>gate.promise;
      else {
        const renderer=kind==="gita"?h.c.GitaReader:h.c.SahasranamaReader;
        renderer.render=async (container,options)=>{ await gate.promise; container.innerHTML="<p>OLD INTERACTIVE RESULT</p>"; if(options.modeHost) options.modeHost.innerHTML="<p>OLD MODE</p>"; };
      }
      const opening=h.c.openArticle({...article("reading"),interactive:kind});await settle();
      await h.c.openArticle(article("b")); const html=h.body.innerHTML,routes=h.routes.length;
      gate.resolve();await opening;await settle();
      assert.equal(h.body.innerHTML,html,"renderer must own a detachable load-specific mount");
      assert.equal(h.routes.length,routes,"old interactive load cannot roll back route");
      assert.equal(h.c.dpTabTitle.textContent,"B");
      assert.ok(!h.c.dpReaderMode.textContent.includes("OLD MODE"),"old reader cannot repopulate replacement mode controls");
    });
  }
  for (const failure of ["response", "text"]) {
    await test(`current source ${failure} rejection recovers without leaving Loading`,async()=>{
      const h=harness();h.setResponder(async()=>{
        if(failure==="response")throw new Error("offline");
        return {ok:true,text:async()=>{throw new Error("broken body");}};
      });
      await assert.doesNotReject(()=>h.c.openArticle(article("a")));
      assert.ok(!h.body.textContent.includes("Loading"),"readable error replaces spinner");
      assert.ok(h.body.textContent.trim(),"error is visible");
      h.setResponder(async()=>({ok:true,text:async()=>"RECOVERED"}));
      await h.c.openArticle(article("b"));assert.ok(h.body.textContent.includes("RECOVERED"));
    });
  }
  await test("source HTTP failure remains bounded to its current article",async()=>{
    const h=harness(),gate=deferred();h.c.state.citationIndex=index;
    h.setResponder(async url=>url==="a.md"?gate.promise:{ok:true,text:async()=>"B ONLY"});
    const a=h.c.openArticle(article("a"));await settle();await h.c.openArticle(article("b"));
    const html=h.body.innerHTML;gate.resolve({ok:false});await a;
    assert.equal(h.body.innerHTML,html,"old HTTP failure must not replace new article with error");
  });
  for(const kind of ["gita","sahasranama"]) {
    await test(`current interactive ${kind} still renders`,async()=>{
      const h=harness(); await h.c.openArticle({...article("reading"),interactive:kind});
      assert.ok(h.body.textContent.includes(kind==="gita"?"GITA VIEW":"SAHASRANAMA VIEW"));
      assert.equal(lastRoute(h).slug,"reading"); assert.equal(h.c.panelState.loaded.article,true);
    });
  }
  await test("rejected metadata JSON is retryable after shared acquisition",async()=>{
    const h=harness(),gate=deferred();h.setResponder(async()=>({ok:true,json:()=>gate.promise}));
    const a=h.c.loadCitationIndex(),b=h.c.loadCitationIndex();await settle();
    gate.reject(new Error("invalid JSON"));await Promise.all([a,b]);
    assert.equal(h.requests.length,1); assert.ok(!h.c.state.citationIndex);
    h.setResponder(async()=>({ok:true,json:async()=>index}));await h.c.loadCitationIndex();
    assert.equal(h.requests.length,2);assert.equal(h.c.state.citationIndex.entries[key].work_title,"Reviewed work");
  });
  await test("citation tab preserves pending article content without stealing the active surface",async()=>{
    const h=harness(),gate=deferred();h.c.state.citationIndex=index;
    h.setResponder(()=>gate.promise);const a=h.c.openArticle(article("a"));await settle();
    h.c.setPanelTab("citation");const html=h.body.innerHTML,routes=h.routes.length;
    gate.resolve({ok:true,text:async()=>"CACHED ARTICLE"});await a;
    assert.ok(h.body.textContent.includes("CACHED ARTICLE"));assert.equal(h.routes.length,routes);
    assert.equal(h.c.panelState.activeTab,"citation");
  });
  await test("uncited article displays without acquiring citation metadata",async()=>{
    const h=harness();h.setResponder(async()=>({ok:true,text:async()=>"PLAIN LAST"}));
    await h.c.openArticle(article("plain"));assert.ok(h.body.textContent.includes("PLAIN LAST"));
    assert.equal(h.requests.filter(u=>u.includes("citation_index")).length,0);
  });
  for(const kind of ["gita","sahasranama"]) await test(`completed ${kind} survives citation tab and return with node identity`,async()=>{
    const h=harness();await h.c.openArticle({...article("reading"),interactive:kind});
    const node=h.body.firstElementChild,html=h.body.innerHTML;
    h.c.setPanelTab("citation");h.c.setPanelTab("article");
    assert.equal(h.body.firstElementChild,node);assert.equal(h.body.innerHTML,html);
    assert.equal(h.c.panelState.loaded.article,true);
  });
  for(const away of ["citation","close"]) await test(`actual completed Sahasranama controls work after ${away} and return`,async()=>{
    const h=harness(),engine=installActualSahas(h);
    h.setResponder(async url=>({ok:true,json:async()=>url.includes("details")?({names:[]}):sahasData("CURRENT")}));
    await h.c.openArticle({...article("reading"),interactive:"sahasranama"});
    const node=h.body.firstElementChild,reader=node.querySelector(".vsn-reader");
    assert.ok(reader,"actual completed reader visible");
    if(away==="close")h.c.closePanel();else h.c.setPanelTab("citation");
    h.c.openPanel("article");
    assert.equal(h.body.firstElementChild,node);
    await engine.setChantView(true,false);assert.ok(reader.classList.contains("vsn-chant-only"),"returned control still acts on cached reader");
    await engine.setChantView(false,false);assert.ok(!reader.classList.contains("vsn-chant-only"));
  });
  await test("actual pending Sahasranama finishes behind a citation and remains usable on return", async()=>{
    const h=harness(), engine=installActualSahas(h), gate=deferred();
    h.setResponder(async url=>url.includes("details")?({ok:true,json:async()=>({names:[]})}):gate.promise);
    const opening=h.c.openArticle({...article("reading"),interactive:"sahasranama"});await settle();
    h.c.setPanelTab("citation");const routes=h.routes.length;
    gate.resolve({ok:true,json:async()=>sahasData("CURRENT")});await opening;
    assert.ok(h.body.textContent.includes("BODY CURRENT"));assert.equal(h.c.panelState.activeTab,"citation");
    assert.equal(h.routes.length,routes,"background reader cannot change the active route");
    h.c.setPanelTab("article");await engine.setChantView(true,false);
    assert.ok(h.body.querySelector(".vsn-reader").classList.contains("vsn-chant-only"));
  });
  for(const phase of ["response","json","details","details-json"]) for(const target of ["sahasranama","gita"]) {
    await test(`actual Sahasranama late ${phase} cannot overwrite newer ${target} state`,async()=>{
      const h=harness(),engine=installActualSahas(h),gate=deferred();let cores=0,details=0;
      h.setResponder(async url=>{
        if(url.includes("details")) {
          details++;return phase==="details"&&details===1?gate.promise:{ok:true,json:()=>phase==="details-json"&&details===1?gate.promise:Promise.resolve({names:[]})};
        }
        cores++;const marker=cores===1?"OLD":"NEW";
        if(cores===1&&phase==="response")return gate.promise;
        return {ok:true,json:()=>cores===1&&phase==="json"?gate.promise:Promise.resolve(sahasData(marker))};
      });
      const old=h.c.openArticle({...article("old"),interactive:"sahasranama"});await settle();
      assert.equal(cores,1,"actual first engine reached core acquisition");
      if(phase.startsWith("details"))assert.equal(details,1,"actual first engine reached detail acquisition");
      await h.c.openArticle({...article("new"),interactive:target});
      const html=h.body.innerHTML,mode=h.c.dpReaderMode.innerHTML,bound=h.boundWords,clears=h.clearCalls;
      assert.ok(html.includes(target==="gita"?"GITA VIEW":"BODY NEW"),"replacement actually rendered");
      gate.resolve(phase==="details-json"?({names:[{number:1,marker:"POISON"}]}):phase==="json"?sahasData("OLD"):{ok:true,json:async()=>phase==="details"?({names:[{number:1,marker:"POISON"}]}):sahasData("OLD")});
      await old;await settle();
      assert.equal(h.body.innerHTML,html);assert.equal(h.c.dpReaderMode.innerHTML,mode,"late global mode host write");
      assert.equal(h.boundWords,bound,"old bindWords must not replace newer reader word owner");
      assert.equal(h.clearCalls,clears,"old continuation must not clear newer word state");
      if(target==="sahasranama")assert.equal(engine.read().names.get(1).marker,"NEW","old detail merge must not mutate current data");
    });
  }
  await test("actual old audio events and queued clock cannot update newer reader timing",async()=>{
    const h=harness();h.actualAudio=true;const engine=installActualSahas(h),frames=[];
    h.c.requestAnimationFrame=fn=>{frames.push(fn);return frames.length;};
    h.setResponder(async url=>({ok:true,json:async()=>url.includes("details")?({names:[]}):sahasData("CURRENT")}));
    await h.c.openArticle({...article("old"),interactive:"sahasranama"});
    const oldAudio=h.body.querySelector("audio");assert.ok(oldAudio,"actual audio rendered");
    oldAudio.emit("play");assert.ok(frames.length,"actual old clock queued");
    await h.c.openArticle({...article("new"),interactive:"sahasranama"});
    const count=h.audioCalls.length;
    oldAudio.emit("timeupdate");oldAudio.emit("seeking");oldAudio.emit("ended");
    for(const fn of frames.splice(0))fn();
    assert.equal(h.audioCalls.length,count,"old audio cannot call current timing-state writer");
    h.body.querySelector("audio").emit("timeupdate");assert.ok(h.audioCalls.length>count,"current audio still updates timing");
  });
  console.log(`${failures.length} failure(s)`);if(failures.length)process.exitCode=1;
})();
