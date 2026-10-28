#!/usr/bin/env node
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
// Exercise fetch policy with real Request/Response objects. Cache storage is a
// boundary double here; installed worker behavior requires browser verification.
const events = {};
const writes = [];
const cache = {match: async () => undefined, put: async (key, response) => {writes.push(response.status);}, addAll: async () => {}};
const context = {self: {location: {origin: 'https://vedanta.eeshan.xyz'}, addEventListener(type, fn) {events[type] = fn;}},
  URL, Request, Response, caches: {open: async () => cache, match: cache.match}, fetch: async () => new Response('ok')};
vm.runInNewContext(fs.readFileSync('sw.js', 'utf8'), context);
function request(path, options = {}) {
  const pending = [];
  let response;
  events.fetch({request: new Request('https://vedanta.eeshan.xyz' + path, options),
    respondWith(value) {response = value;}, waitUntil(value) {pending.push(value);}});
  return {get response() {return response;}, pending};
}
(async () => {
  assert.equal(request('/gita/sthitaprajna/recitation.mp3', {headers: {Range: 'bytes=0-1'}}).response, undefined,
    'range requests must reach native networking, not a full-body cache');
  assert.equal(request('/gita/sthitaprajna/recitation.mp3').response, undefined, 'large media must not fill shell cache');
  const normal = request('/data/timeline_index.json?v=test');
  assert.equal((await normal.response).status, 200);
  await Promise.all(normal.pending);
  assert.deepEqual(writes, [200]);
  cache.put = async () => {throw Error('QuotaExceededError');};
  const full = request('/assets/app.js?v=test');
  assert.equal((await full.response).status, 200, 'cache failures must not fail an otherwise successful request');
  await Promise.all(full.pending);
  function pwa(audio) {
    const pwaEvents = {}, windowEvents = {}, docEvents = {};
    let reloads = 0;
    const pwaContext = {navigator: {serviceWorker: {controller: {}, addEventListener(type, fn) {pwaEvents[type] = fn;},
      register: async () => ({update: async () => {}})}},
      document: {visibilityState: 'visible', querySelectorAll() {return [audio];}, addEventListener(type, fn) {docEvents[type] = fn;}},
      window: {addEventListener(type, fn) {windowEvents[type] = fn;}, location: {reload() {reloads++;}}}, Date};
    vm.runInNewContext(fs.readFileSync('assets/pwa.js', 'utf8'), pwaContext);
    return {pwaEvents,windowEvents,docEvents,get reloads() {return reloads;}};
  }
  const audio = {paused: false, ended: false};
  const listening = pwa(audio);
  await listening.windowEvents.load();
  listening.docEvents.play();
  listening.pwaEvents.controllerchange();
  assert.equal(listening.reloads, 0, 'a deployment cannot interrupt active recitation');
  audio.paused = true;
  listening.docEvents.visibilitychange();
  assert.equal(listening.reloads, 0, 'pausing mid-recording must preserve playback position');
  audio.ended = true;
  listening.docEvents.visibilitychange();
  assert.equal(listening.reloads, 0, 'a completed listening session remains resumable until the next launch');
  const seeked = pwa({paused:true,ended:false});
  await seeked.windowEvents.load();
  seeked.docEvents.seeking();
  seeked.pwaEvents.controllerchange();
  assert.equal(seeked.reloads,0,'seeking before play also preserves the chosen position');
  const pending = pwa({paused:false,ended:false});
  pending.pwaEvents.controllerchange();
  assert.equal(pending.reloads,0,'pending playback is protected before its play event arrives');
  const idle = pwa({paused:true,ended:false});
  idle.pwaEvents.controllerchange();
  assert.equal(idle.reloads,1,'an unused audio element does not block a safe update');
  idle.pwaEvents.controllerchange();
  assert.equal(idle.reloads,1,'reload is idempotent');
  const shell = vm.runInNewContext('[' + fs.readFileSync('sw.js','utf8').match(/const SHELL = \[([\s\S]*?)\];/)[1] + ']');
  const index = fs.readFileSync('index.html','utf8');
  for (const match of index.matchAll(/(?:src|href)="(assets\/[^"?#]+(?:\?[^"#]*)?)"/g)) {
    assert.ok(shell.includes('/' + match[1]), `first-install shell must cache ${match[1]}`);
  }
  console.log('PWA range/media bypass, cache failure isolation, and playback-safe update checks passed.');
})().catch(error => {console.error(error); process.exitCode = 1;});
