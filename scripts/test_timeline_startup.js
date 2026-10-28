#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(require("node:path").join(__dirname, "../assets/app.js"), "utf8");
const start = source.indexOf("async function loadAll()");
const end = source.indexOf("\ntry {", start);
assert.ok(start >= 0 && end > start);

// Real bootstrap with boundary-only doubles. Optional graph acquisition must
// not gate the timeline; the renderer owns a single layout pass. Exercise both
// the deployed summary and the source-checkout fallback, including hidden data.
async function run(useIndex) {
  const requests = [], calls = [];
  const thinkers = [{ id: "visible" }, { id: "hidden", display: false }];
  const manifest = { thinkers: ["visible.json", "hidden.json"] };
  const context = {
    state: { thinkersById: new Map() }, window: {},
    timelineLoadingEl: { hidden: false },
    loadJSON: async (path) => {
      requests.push(path);
      if (path === "data/manifest.json") return manifest;
      if (path === "data/timeline_index.json") return useIndex ? { thinkers } : null;
      if (path.startsWith("data/thinkers/")) return thinkers.find(t => path.endsWith(t.id + ".json"));
      if (path === "data/registries/primitive_graph.json") throw Error("optional graph requested on startup");
      return {};
    },
    setChronologyMode() {}, chooseInitialChronologyMode: () => "academic",
    computeRange: () => calls.push("range"),
    computeRenderLanes: () => calls.push("lanes"),
    computeLayout: () => calls.push("layout"),
    renderAll: () => { calls.push("render"); calls.push("layout"); },
    renderFilterChips() {}, updateSubtitle() {}, scrollToInitialFocus() {},
    requestIdleCallback: (callback) => { context.idle = callback; },
    loadSupportData: async () => calls.push("support"),
    showEmptyState: () => assert.fail("valid manifest must render"),
  };
  vm.createContext(context);
  vm.runInContext(source.slice(start, end), context);
  await context.loadAll();
  assert.equal(context.timelineLoadingEl.hidden, true);
  assert.deepEqual(Array.from(context.state.thinkersById.keys()), ["visible"]);
  assert.equal(calls.filter(x => x === "layout").length, 1, "one layout pass per initial render");
  assert.equal(calls.includes("support"), false, "reader support remains deferred");
  assert.equal(requests.includes("data/registries/primitive_graph.json"), false);
  assert.equal(requests.some(x => x.startsWith("data/thinkers/")), !useIndex);
  assert.equal(Boolean(context.state.thinkers[0].__timelineSummary), useIndex);
  await context.idle();
  assert.ok(calls.includes("support"));
}
(async () => { await run(true); await run(false); console.log("timeline startup: summary/fallback, optional graph, single layout passed"); })().catch(e => { console.error(e); process.exitCode = 1; });
