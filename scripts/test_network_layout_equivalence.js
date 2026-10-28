#!/usr/bin/env node
"use strict";
// Real corpus and boundary cases compare optimized layout against the original
// brute-force placement policy. Network coordinates and every label box must
// remain identical; a faster layout that drops/filter/reorders nodes fails.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { performance } = require("node:perf_hooks");
const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "assets/app.js"), "utf8");
function section(start, end) {
  const from = source.indexOf(start), to = source.indexOf(end, from);
  assert.ok(from >= 0 && to > from, `missing source section: ${start}`);
  return source.slice(from, to);
}
const context = {localStorage: {getItem: () => null}};
vm.createContext(context);
vm.runInContext(
  section("const PX_PER_YEAR_DEFAULT", "// ---------- DOM refs") +
  section("const state =", "function chronologyModeLabel") +
  section("function computeRange()", "function updateSubtitle()") +
  section("function yearToX", "// ---------- render: lane rail") +
  section("function computeLaneLabelPlacements", "// ---------- render: dots") +
  `\nvar CURRENT_YEAR=2026, RANGE_HIGH_MAX=2050, LANE_H=96;\n` +
  `${referenceNetworkLayout.toString()}\n${referenceLabelPlacements.toString()}\n` +
  `this.api={state, computeRange, computeRenderLanes, computeNetworkLayout,
    computeLanesLayout, computeLaneLabelPlacements, referenceNetworkLayout,
    referenceLabelPlacements, setLaneHeight: h => {LANE_H=h;}};`, context);
const api = context.api;
const manifest = JSON.parse(fs.readFileSync(path.join(root, "data/manifest.json")));
const thinkers = manifest.thinkers.map(file => JSON.parse(
  fs.readFileSync(path.join(root, "data/thinkers", file)))).filter(t => t.display !== false);
const clone = value => JSON.parse(JSON.stringify(value));
const layoutSnapshot = () => clone([...api.state.layout].map(([id, p]) => [id, {...p, thinker: p.thinker.id}]));
let cases = 0;
for (const chronology of ["academic", "traditional"]) {
  for (const zoom of [0.6, 1.9, 6]) {
    for (const laneHeight of [64, 96]) {
      for (const filter of ["all", "advaita", "comparators", "empty"]) {
        api.state.thinkers = thinkers;
        api.state.chronologyMode = chronology;
        api.state.pxPerYear = zoom;
        api.setLaneHeight(laneHeight);
        api.state.visibleLanes = new Set(filter === "all"
          ? ["proto", "advaita", "bhedabheda", "vishishtadvaita", "dvaita", "acintya", "shuddha", "avibhaga", "purna-advaita", "__comparator_group__"]
          : filter === "comparators" ? ["__comparator_group__"] : filter === "empty" ? [] : ["advaita"]);
        api.computeRange(); api.computeRenderLanes();
        api.referenceNetworkLayout(); const expected = layoutSnapshot();
        api.computeNetworkLayout();
        assert.deepEqual(layoutSnapshot(), expected, `${chronology}/${zoom}/${laneHeight}/${filter}: network`);
        for (const laneLocal of [false, true]) {
          if (laneLocal) api.computeLanesLayout();
          const options = {laneHeight, plotBottom: laneLocal ? api.state.renderLanes.length*laneHeight : 1500, laneLocal};
          assert.deepEqual(clone([...api.computeLaneLabelPlacements(api.state.layout.values(), options)]),
            clone([...api.referenceLabelPlacements(api.state.layout.values(), options)]),
            `${chronology}/${zoom}/${laneHeight}/${filter}: labels (${laneLocal})`);
        }
        cases++;
      }
    }
  }
}
// Negative and bucket-edge coordinates, exact collision thresholds, repeated
// x positions, and very long names challenge neighboring-bucket inclusion.
for (const laneLocal of [false, true]) {
  const values = [-120, -60, -0.001, 0, 59.999, 60, 120, 120, 180, 241].map((x, i) => ({
    thinker: {id: `boundary-${i}`, name: i % 3 ? `Node ${i}` : "Long boundary name ".repeat(15)},
    x, y: 48 + (i % 3 - 1)*12, lane: 0,
  }));
  const opts = {laneHeight: 96, plotBottom: laneLocal ? 96 : 1500, laneLocal};
  assert.deepEqual(clone([...api.computeLaneLabelPlacements(values, opts)]),
    clone([...api.referenceLabelPlacements(values, opts)]), "label bucket boundaries");
}
// Seeded dense boxes include overlaps whose closest distance is diagonal,
// along with decimal x coordinates around bucket boundaries. This challenges
// the clearance bound separately from the corpus's mostly integral geometry.
let seed = 4751;
const random = () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 2**32);
for (let run = 0; run < 16; run++) {
  const values = Array.from({length: 70}, (_, i) => ({
    thinker: {id: `random-${i}`, name: "n".repeat(1 + Math.floor(random()*80))},
    x: -180 + random()*600, y: 10 + random()*1300, lane: 0,
  }));
  const opts = {laneHeight: 96, plotBottom: 1500, laneLocal: false};
  assert.deepEqual(clone([...api.computeLaneLabelPlacements(values, opts)]),
    clone([...api.referenceLabelPlacements(values, opts)]), `seeded label clearance ${run}`);
}
api.state.visibleLanes = new Set(["advaita"]);
api.state.thinkers = Array.from({length: 50}, (_, i) => ({
  id: `same-date-${i}`, name: `Synthetic ${i}`, dates_low: i < 45 ? 0 : i*60,
  dates_high: i < 45 ? 0 : i*60, school_color_token: "advaita", lineage_in: i ? [`same-date-${i-1}`] : [],
}));
api.state.pxPerYear = 1; api.computeRange(); api.computeRenderLanes();
api.referenceNetworkLayout(); const boundaryNetwork = layoutSnapshot();
api.computeNetworkLayout(); assert.deepEqual(layoutSnapshot(), boundaryNetwork, "dense repeated dates and lineage");
console.log(`network layout: ${cases} corpus configurations and boundary cases preserve exact coordinates and labels`);
if (process.argv.includes("--benchmark")) {
  api.state.thinkers = thinkers; api.state.chronologyMode = "academic"; api.state.pxPerYear = 1.9;
  api.state.visibleLanes = new Set(["proto", "advaita", "bhedabheda", "vishishtadvaita", "dvaita", "acintya", "shuddha", "avibhaga", "purna-advaita", "__comparator_group__"]);
  api.setLaneHeight(96); api.computeRange(); api.computeRenderLanes();
  const results = {reference: [], optimized: []};
  const opts = {laneHeight: 96, plotBottom: 1500, laneLocal: false};
  for (let i=0; i<10; i++) {
    for (const key of i % 2 ? ["optimized", "reference"] : ["reference", "optimized"]) {
      const start=performance.now();
      api[key === "reference" ? "referenceNetworkLayout" : "computeNetworkLayout"]();
      const networkEnd=performance.now();
      api[key === "reference" ? "referenceLabelPlacements" : "computeLaneLabelPlacements"](api.state.layout.values(), opts);
      if (i >= 2) results[key].push({network: networkEnd-start, labels: performance.now()-networkEnd, total: performance.now()-start});
    }
  }
  for (const [key, rows] of Object.entries(results)) {
    const median = field => rows.map(row=>row[field]).sort((a,b)=>a-b)[Math.floor(rows.length/2)].toFixed(2);
    console.log(`${key}: n=${rows.length}, median network=${median("network")}ms, labels=${median("labels")}ms, total=${median("total")}ms; worst total=${Math.max(...rows.map(r=>r.total)).toFixed(2)}ms`);
  }
  api.computeLanesLayout();
  const laneOptions = {laneHeight: 96, plotBottom: api.state.renderLanes.length*96, laneLocal: true};
  const laneResults = {};
  for (const [key, fn] of [["reference", api.referenceLabelPlacements], ["optimized", api.computeLaneLabelPlacements]]) {
    const durations = [];
    for (let i=0; i<10; i++) {
      const start = performance.now(); fn(api.state.layout.values(), laneOptions);
      if (i >= 2) durations.push(performance.now()-start);
    }
    laneResults[key] = durations.sort((a,b)=>a-b)[4].toFixed(2);
  }
  console.log(`lanes label median: reference=${laneResults.reference}ms, optimized=${laneResults.optimized}ms`);
}

// Baseline policy, intentionally brute force; independent of spatial buckets.
function referenceNetworkLayout() {
  state.layout.clear();
  const sorted = [...state.thinkers].sort((a, b) => {
    const aChronology = resolveChronology(a);
    const bChronology = resolveChronology(b);
    const al = (typeof aChronology.low === "number") ? aChronology.low : 0;
    const bl = (typeof bChronology.low === "number") ? bChronology.low : 0;
    if (al !== bl) return al - bl;
    return ((al + aChronology.highForLayout) / 2) - ((bl + bChronology.highForLayout) / 2);
  });

  const placed = []; // [{x, y, r, id}]
  const STEP = 18;
  const X_PAD = 60;
  const Y_PAD = 26;

  const usableH = NETWORK_CANVAS_H - NETWORK_PAD_TOP - NETWORK_PAD_BOTTOM;
  const yFromBand = (b) => NETWORK_PAD_TOP + b * usableH;

  for (const t of sorted) {
    if (!isThinkerVisible(t)) continue;
    const chronology = resolveChronology(t);
    if (typeof chronology.low !== "number") continue;
    const tok = t.school_color_token || "proto";
    const tier = tierOf(t);
    const xMid = yearToX((chronology.low + chronology.highForLayout) / 2);
    const x1 = yearToX(chronology.low);
    const x2 = yearToX(chronology.highForLayout);

    let lineageY = null;
    let lineageN = 0;
    let lineageSum = 0;
    for (const inId of (t.lineage_in || [])) {
      const p = state.layout.get(inId);
      if (p) { lineageSum += p.y; lineageN++; }
    }
    if (lineageN > 0) lineageY = lineageSum / lineageN;

    const bandY = yFromBand(SCHOOL_BAND[tok] != null ? SCHOOL_BAND[tok] : 0.5);
    const desiredY = lineageY != null ? (0.55 * lineageY + 0.45 * bandY) : bandY;

    const dotR = tier === 1 ? 9 : (tier === 2 ? 6 : 4);
    const minTop = NETWORK_PAD_TOP;
    const maxTop = NETWORK_CANVAS_H - NETWORK_PAD_BOTTOM;
    let chosenY = desiredY;
    let found = false;
    for (let k = 0; k <= 200 && !found; k++) {
      const offsets = k === 0 ? [0] : [k * STEP, -k * STEP];
      for (const off of offsets) {
        const y = Math.max(minTop, Math.min(maxTop, desiredY + off));
        let conflict = false;
        for (const q of placed) {
          if (Math.abs(q.x - xMid) < X_PAD && Math.abs(q.y - y) < (Y_PAD + (q.r + dotR) * 0.5)) {
            conflict = true;
            break;
          }
        }
        if (!conflict) { chosenY = y; found = true; break; }
      }
    }

    placed.push({ x: xMid, y: chosenY, r: dotR, id: t.id });
    state.layout.set(t.id, {
      thinker: t, x: xMid, y: chosenY,
      lane: 0, shade: shadeFor(t), tier,
      barX1: x1, barX2: x2,
    });
  }
}


function referenceLabelPlacements(layoutValues, {
  laneHeight,
  plotBottom,
  laneLocal = true,
  compact = laneHeight <= 72,
} = {}) {
  const LABEL_BASE = laneLocal ? (compact ? 7 : 9) : 11;
  const LABEL_TIER_DY = compact ? 12 : 19;
  const LABEL_H_FULL = compact ? 24 : 36;
  const GAP_X = 5;           // min horizontal breathing room between labels
  const GAP_Y = 4;           // min vertical breathing room between labels
  const MAX_LABEL_SLOTS = 22;
  const laneInset = compact ? 1 : 3;
  const placedByLane = new Map();
  const placements = new Map();
  const sortedLayout = [...layoutValues].sort((a, b) =>
    (laneLocal ? a.lane - b.lane : 0) || a.x - b.x);
  for (const p of sortedLayout) {
    const t = p.thinker;
    const nm = t.name || t.id;
    const LABEL_H = LABEL_H_FULL;
    const labelW = compact ? Math.min(nm.length * 6 + 14, 114) : nm.length * 6 + 14;
    const x1 = p.x - labelW / 2;
    const x2 = p.x + labelW / 2;
    const laneTop = laneLocal ? p.lane * laneHeight + laneInset : 6;
    const laneBottom = laneLocal
      ? (p.lane + 1) * laneHeight - laneInset
      : plotBottom - 4;
    const laneKey = laneLocal ? p.lane : "plot";
    const placedBoxes = placedByLane.get(laneKey) || [];
    placedByLane.set(laneKey, placedBoxes);
    const boxFor = (slot) => {
      const where = slot % 2 === 0 ? "above" : "below";
      const dy = LABEL_BASE + Math.floor(slot / 2) * LABEL_TIER_DY;
      const y2 = where === "above" ? p.y - dy : p.y + dy + LABEL_H;
      const y1 = y2 - LABEL_H;
      const inBounds = y1 >= laneTop && y2 <= laneBottom;
      return { where, dy, x1, x2, y1, y2, inBounds };
    };
    const overlaps = (b) => placedBoxes.some((q) =>
      !(q.x2 < b.x1 - GAP_X || q.x1 > b.x2 + GAP_X ||
        q.y2 < b.y1 - GAP_Y || q.y1 > b.y2 + GAP_Y));
    let placed = null;
    let bestBox = null;
    let bestClearance = -Infinity;
    for (let s = 0; s < MAX_LABEL_SLOTS; s++) {
      const b = boxFor(s);
      if (!b.inBounds) continue;
      if (!overlaps(b)) { placed = b; break; }
      let clr = Infinity;
      for (const q of placedBoxes) {
        const dx = Math.max(q.x1 - b.x2, b.x1 - q.x2, 0);
        const dyv = Math.max(q.y1 - b.y2, b.y1 - q.y2, 0);
        const d = Math.hypot(dx, dyv);
        if (d < clr) clr = d;
      }
      if (clr > bestClearance) { bestClearance = clr; bestBox = b; }
    }
    if (!placed) placed = bestBox;
    if (!placed) {
      const roomAbove = p.y - laneTop;
      const roomBelow = laneBottom - p.y;
      if (roomAbove >= roomBelow) {
        const y1 = laneTop;
        const y2 = Math.min(laneBottom, y1 + LABEL_H);
        placed = { where: "above", dy: Math.max(0, p.y - y2), x1, x2, y1, y2 };
      } else {
        const y2 = laneBottom;
        const y1 = Math.max(laneTop, y2 - LABEL_H);
        placed = { where: "below", dy: Math.max(0, y1 - p.y), x1, x2, y1, y2 };
      }
    }
    placedBoxes.push({ x1: placed.x1, x2: placed.x2, y1: placed.y1, y2: placed.y2 });
    placements.set(t.id, placed);
  }

  return placements;
}
