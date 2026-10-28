#!/usr/bin/env node
"use strict";

// Exercise the actual input handler with a controlled animation-frame queue.
// These assertions cover event ordering and pixel geometry, not browser paint.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "../assets/app.js"), "utf8");
const start = source.indexOf("function wirePanZoom()");
const end = source.indexOf("// ---------- Reset View button", start);
assert.ok(start >= 0 && end > start);

function harness({scale = 1.9, mode = "network"} = {}) {
  const listeners = new Map(), frames = new Map(), timers = new Map();
  let frameId = 0, timerId = 0, renders = 0;
  const scroller = {
    scrollLeft: 500, scrollTop: 0, clientWidth: 800, clientHeight: 600, style: {},
    addEventListener(type, handler) {
      const handlers = listeners.get(type) || [];
      handlers.push(handler); listeners.set(type, handlers);
    },
    getBoundingClientRect: () => ({left: 20}),
  };
  const canvas = {style: {}};
  const state = {pxPerYear: scale, viewMode: mode, range: {low: -650}};
  const context = {
    scroller, canvas, state, LANE_RAIL_W: 188, PAD_LEFT: 60,
    window: {addEventListener() {}}, document: {body: {classList: {toggle() {}}}},
    isNarrowViewport: () => false,
    requestAnimationFrame(fn) { frames.set(++frameId, fn); return frameId; },
    cancelAnimationFrame(id) { frames.delete(id); },
    setTimeout(fn) { timers.set(++timerId, fn); return timerId; },
    clearTimeout(id) { timers.delete(id); },
    renderAll() { renders++; },
  };
  vm.createContext(context);
  vm.runInContext(source.slice(start, end) + "\nwirePanZoom();", context);
  function emit(type, properties = {}) {
    const event = {ctrlKey: false, metaKey: false, shiftKey: false,
      deltaX: 0, deltaY: 0, deltaMode: 0, clientX: 300,
      preventDefault() { this.prevented = true; }, ...properties};
    for (const handler of listeners.get(type) || []) handler(event);
    return event;
  }
  return {scroller, canvas, state, frames, timers, emit, renders: () => renders,
    frame() { const pending = [...frames.values()]; frames.clear(); pending.forEach(fn => fn()); },
    idle() { const pending = [...timers.values()]; timers.clear(); pending.forEach(fn => fn()); }};
}

function closeTo(actual, expected, message) {
  assert.ok(Math.abs(actual - expected) < 1e-9, `${message}: ${actual} != ${expected}`);
}

// The first ctrl-trackpad event remains intercepted. An immediate interruption
// must commit every queued delta exactly once, then leave no temporary transform.
for (const mode of ["network", "lanes"]) {
  for (const end of ["pointerdown", "gestureend", "touchend", "idle"]) {
    const h = harness({mode});
    const rail = mode === "lanes" ? 188 : 0;
    const anchorBefore = (300 - 20 + 500 - rail - 60) / 1.9 - 650;
    assert.equal(h.emit("wheel", {ctrlKey: true, deltaY: -25}).prevented, true);
    h.emit("wheel", {ctrlKey: true, deltaY: -25});
    const staleFrame = [...h.frames.values()][0];
    if (end === "idle") h.idle();
    else h.emit(end, {changedTouches: []});
    closeTo(h.state.pxPerYear, 1.9 * Math.exp(50 * 0.0018), `${mode}/${end}: committed scale`);
    closeTo((300 - 20 + h.scroller.scrollLeft - rail - 60) / h.state.pxPerYear - 650,
      anchorBefore, `${mode}/${end}: cursor anchor`);
    assert.equal(h.canvas.style.transform, "");
    assert.equal(h.frames.size, 0, "queued frame was cancelled");
    assert.equal(h.renders(), 1, "one final render");
    staleFrame();
    assert.equal(h.canvas.style.transform, "", "stale frame cannot resurrect a transform");
    h.idle(); assert.equal(h.renders(), 1, "stale idle timer cannot commit twice");
  }
}

// A normal delivered frame plus a pending final delta must both survive;
// the previous gesture's cancelled callback must not affect a new gesture.
{
  const h = harness();
  h.emit("wheel", {ctrlKey: true, deltaY: -20}); h.frame();
  h.emit("wheel", {ctrlKey: true, deltaY: -10});
  const staleFrame = [...h.frames.values()][0]; h.idle();
  closeTo(h.state.pxPerYear, 1.9 * Math.exp(30 * 0.0018), "delivered plus pending frame");
  h.emit("wheel", {ctrlKey: true, deltaY: 10});
  staleFrame(); assert.equal(h.canvas.style.transform, "");
  h.frame(); h.idle();
  closeTo(h.state.pxPerYear, 1.9 * Math.exp(20 * 0.0018), "second gesture remains independent");
}
for (const [scale, deltaY, expected] of [[6, -50, 6], [0.6, 50, 0.6]]) {
  const h = harness({scale}); h.emit("wheel", {ctrlKey: true, deltaY}); h.idle();
  assert.equal(h.state.pxPerYear, expected); assert.equal(h.renders(), 0);
}

// A pending zoom must not undo a subsequent horizontal pan. Compare against
// the same zoom completed on its own, then the independently requested pan.
for (const deliveredFrame of [false, true]) {
  for (const pan of ["shift", "native-wheel", "native-scroll"]) {
    const baseline = harness();
    baseline.emit("wheel", {ctrlKey: true, deltaY: -20}); baseline.idle();
    const expectedLeft = baseline.scroller.scrollLeft + 100;
    const h = harness();
    h.emit("wheel", {ctrlKey: true, deltaY: -20});
    if (deliveredFrame) h.frame();
    if (pan === "shift") h.emit("wheel", {shiftKey: true, deltaX: 100});
    else {
      if (pan === "native-wheel") {
        assert.equal(h.emit("wheel", {deltaX: 100}).prevented, undefined);
      }
      // Native wheel/scrollbar scrolling occurs outside the JS handler.
      h.scroller.scrollLeft += 100;
    }
    h.idle();
    closeTo(h.scroller.scrollLeft, expectedLeft, `${pan}/${deliveredFrame}: pan survives zoom commit`);
    closeTo(h.state.pxPerYear, baseline.state.pxPerYear, "mixed gesture keeps zoom");
    assert.equal(h.canvas.style.transform, "");
  }
}
// A native pan between two zoom inputs remains visible when zoom resumes,
// whether the first input's animation frame has been delivered yet or not.
for (const deliveredFrame of [false, true]) {
  const h = harness();
  h.emit("wheel", {ctrlKey: true, deltaY: -20});
  if (deliveredFrame) h.frame();
  h.scroller.scrollLeft += 100;
  const expected = harness();
  expected.emit("wheel", {ctrlKey: true, deltaY: -20}); expected.idle();
  expected.scroller.scrollLeft += 100;
  expected.emit("wheel", {ctrlKey: true, deltaY: -10}); expected.idle();
  h.emit("wheel", {ctrlKey: true, deltaY: -10}); h.frame(); h.idle();
  closeTo(h.scroller.scrollLeft, expected.scroller.scrollLeft,
    `resumed zoom preserves prior pan (delivered=${deliveredFrame})`);
}

// Firefox may report native Shift horizontal scrolling in deltaX. Wheel
// values can be pixels, lines (the timeline's existing 16 px convention),
// or pages; page movement uses the horizontal scrollport width.
for (const [deltaX, deltaY, deltaMode, expected] of [
  [20, 0, 0, 20], [0, 20, 0, 20], [-3, 0, 1, -48], [0, 3, 1, 48],
  [1, 0, 2, 800], [0, -1, 2, -800], [20, 5, 0, 20],
]) {
  const h = harness();
  const event = h.emit("wheel", {shiftKey: true, deltaX, deltaY, deltaMode});
  assert.equal(h.scroller.scrollLeft - 500, expected, `shift wheel ${deltaX}/${deltaY}/${deltaMode}`);
  assert.equal(event.prevented, true);
}
{
  const h = harness();
  assert.equal(h.emit("wheel", {deltaY: 20}).prevented, undefined, "ordinary scroll remains native");
  assert.equal(h.scroller.scrollLeft, 500);
}
console.log("timeline gestures: pending-frame ordering, zoom bounds/anchor, and wheel units passed");
