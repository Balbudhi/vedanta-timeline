#!/usr/bin/env node
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
class Element extends EventTarget {
  constructor() {super(); this.dataset = {}; this.style = {}; this.attributes = {}; this.classList = {add() {}, remove() {}, toggle() {}};}
  setAttribute(key, value) {this.attributes[key] = value;}
  querySelector(selector) {return this.children?.[selector] || null;}
  querySelectorAll() {return [];}
  getBoundingClientRect() {return {left:0, width:100};}
}
class Audio extends Element {
  constructor() {super(); this.currentTime = 40; this.duration = 100; this.playbackRate = 1; this.src = 'recitation.mp3'; this.paused = true; this.ended = false;}
  play() {this.paused = false; this.dispatchEvent(new Event('play')); return Promise.resolve();}
  pause() {this.paused = true; this.dispatchEvent(new Event('pause'));}
}
for (const type of ['gita', 'sahasranama']) {
  const handlers = new Map();
  const root = new Element(), bar = new Element(), audio = new Audio();
  const play = new Element(), back = new Element(), next = new Element(), progress = new Element();
  bar.children = type === 'gita'
    ? {'#rbPlay':play, '#rbBack':back, '#rbFwd':next, '#rbProgress':progress, '#rbBar':new Element(), '#rbTime':new Element()}
    : {'audio':audio, '.vsn-play':play, '.vsn-back':back, '.vsn-forward':next, '.vsn-progress':progress, '.rb-bar':new Element(), '.rb-time':new Element()};
  root.children = {[type === 'gita' ? '#reciteBar' : '.vsn-recite-bar']:bar};
  const context = {window:{}, navigator:{mediaSession:{setActionHandler(name, fn) {handlers.set(name,fn);}, setPositionState() {}}},
    document:{title:'Reading', getElementById() {return null;}, addEventListener() {}}, AbortController, URL, location:{href:'https://vedanta.eeshan.xyz/'},
    requestAnimationFrame() {return 1;}, cancelAnimationFrame() {}, CSS:{escape: x => x}};
  context.window = context;
  vm.runInNewContext(fs.readFileSync('assets/media-session.js','utf8'),context);
  let source = fs.readFileSync(`assets/${type}.js`,'utf8');
  if (type === 'gita') source = source.replace('window.GitaReader = {',
    'window.testAudio = (root, audio) => { ROOT=root; AUDIO=audio; AUDIO_MANIFEST={src:"recitation.mp3", verses:[{start:0,end:100,locus:"test"}]}; wireRecitation(); }; window.GitaReader = {');
  else source = source.replace('window.SahasranamaReader = {',
    'window.testAudio = (root) => { ROOT=root; DATA={audio:{duration_seconds:100,units:[]}}; wireAudio(); }; window.SahasranamaReader = {');
  vm.runInNewContext(source,context);
  context.testAudio(root,audio);
  back.dispatchEvent(new Event('click'));
  assert.equal(audio.currentTime,30, `${type} back button seeks ten seconds`);
  next.dispatchEvent(new Event('click'));
  assert.equal(audio.currentTime,40, `${type} forward button seeks ten seconds`);
  play.dispatchEvent(new Event('click'));
  assert.equal(audio.paused,false);
  handlers.get('seekbackward')({});
  assert.equal(audio.currentTime,30);
  const reader = type === 'gita' ? context.GitaReader : context.SahasranamaReader;
  reader.stopAudio();
  assert.equal(audio.paused,true);
  assert.equal(handlers.get('play'),null,'closed reader releases OS controls');
  play.dispatchEvent(new Event('click'));
  assert.equal(audio.paused,false,'reopened cached reader retains functioning controls');
  assert.equal(typeof handlers.get('play'),'function','cached player reclaims Media Session');
}
console.log('Both real reader transport bindings seek ten seconds and survive close/reopen.');

(async () => {
  let resolveFetch;
  const root = new Element();
  let current = true;
  const context = {window:{location:{search:''}}, document:{querySelector() {return {};}, addEventListener() {}},
    performance:{now: () => 0}, localStorage:{getItem: () => 'true'}, URLSearchParams,
    fetch: () => new Promise(resolve => {resolveFetch = resolve;})};
  const source = fs.readFileSync('assets/sahasranama.js','utf8').replace('window.SahasranamaReader = {',
    'window.testDetails = (names, current) => { NAME_BY_NUMBER=names; isCurrent=current; DETAILS_URL="details.json"; DETAILS_PROMISE=null; return ensureDetails(); }; window.SahasranamaReader = {');
  vm.runInNewContext(source,context);
  const pending = context.window.SahasranamaReader.render(root,{isCurrent:() => current});
  current = false;
  root.innerHTML = 'Newly selected article';
  resolveFetch({ok:true,json:async () => ({})});
  await pending;
  assert.equal(root.innerHTML,'Newly selected article','late reader data cannot replace newer content');
  const name = {number:1};
  current = true;
  const details = context.window.testDetails(new Map([[1,name]]),() => current);
  current = false;
  resolveFetch({ok:true,json:async () => ({names:[{number:1,meaning:'stale'}]})});
  assert.equal(await details,false);
  assert.equal(name.meaning,undefined,'stale details cannot mutate another render');
  console.log('Late Sahasranama core and details responses cannot adopt stale state.');
})().catch(error => {console.error(error);process.exitCode=1;});
