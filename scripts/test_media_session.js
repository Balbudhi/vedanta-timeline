#!/usr/bin/env node
// Application contract tests: transport commands, bounds, ownership and cleanup.
// MediaSession is a browser boundary; OS control layout still needs device QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
class Audio extends EventTarget {
  constructor() { super(); this.currentTime = 40; this.duration = 100; this.paused = true; this.ended = false; this.playbackRate = 1; }
  play() { this.paused = false; this.dispatchEvent(new Event('play')); return Promise.resolve(); }
  pause() { this.paused = true; this.dispatchEvent(new Event('pause')); }
}
const handlers = new Map();
const positions = [];
const session = {setActionHandler(name, handler) { handlers.set(name, handler); }, setPositionState(state) { positions.push(state); }};
const context = {window: {}, navigator: {mediaSession: session}, MediaMetadata: class { constructor(data) {Object.assign(this, data);} }};
vm.runInNewContext(fs.readFileSync('assets/media-session.js', 'utf8'), context);
const media = context.window.VedantaMediaSession;
const a = new Audio();
let seeks = 0, plays = 0;
const first = media.attach(a, {metadata: {title: 'First'}, beforePlay() {plays++;}, onSeek() {seeks++;}});
a.play();
assert.equal(session.metadata.title, 'First');
handlers.get('seekbackward')({});
assert.equal(a.currentTime, 30);
handlers.get('seekforward')({});
assert.equal(a.currentTime, 40);
handlers.get('seekforward')({seekOffset: 20});
assert.equal(a.currentTime, 60);
handlers.get('seekto')({seekTime: 500});
assert.equal(a.currentTime, 100);
handlers.get('seekto')({seekTime: -3});
assert.equal(a.currentTime, 0);
assert.equal(seeks, 5);
handlers.get('seekto')({seekTime: NaN});
assert.equal(a.currentTime, 0);
assert.equal(handlers.get('previoustrack'), null);
assert.equal(handlers.get('nexttrack'), null);
handlers.get('pause')();
assert.equal(a.paused, true);
assert.equal(session.playbackState, 'paused');
handlers.get('play')();
assert.equal(plays, 1);
assert.equal(session.playbackState, 'playing');
a.playbackRate = 1.5;
a.dispatchEvent(new Event('ratechange'));
assert.equal(positions.at(-1).playbackRate, 1.5);
const b = new Audio();
const second = media.attach(b, {metadata: {title: 'Second'}});
assert.equal(a.paused, false, 'rendering another player must not steal active playback');
b.play();
assert.equal(a.paused, true, 'playing a new reader pauses the old audio');
assert.equal(session.metadata.title, 'Second');
first.dispose();
assert.equal(session.metadata.title, 'Second', 'disposing an inactive reader preserves the active session');
second.dispose();
assert.equal(b.paused, true);
assert.equal(session.playbackState, 'none');
assert.equal(session.metadata, null);
assert.equal(handlers.get('seekforward'), null);
a.play();
assert.equal(session.metadata, null, 'disposed listeners cannot reclaim the session');
// Feature absence and partial browser support must leave ordinary playback usable.
const limited = {window: {}, navigator: {mediaSession: {setActionHandler() {throw Error('unsupported');}}}};
vm.runInNewContext(fs.readFileSync('assets/media-session.js', 'utf8'), limited);
const c = new Audio();
const fallback = limited.window.VedantaMediaSession.attach(c, {});
c.play();
fallback.dispose();
console.log('Media Session transport, bounds, ownership, cleanup and unsupported-browser checks passed.');
