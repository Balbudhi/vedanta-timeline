// Vedānta interactive timeline.
// Cladogram swim-lanes + sticky lane rail + manhattan-routed lineage edges.
// Detail pane: hero thesis, nested work→passage cards, Pāṇinian tables.
// Canvas-style 2D pan (drag) + wheel scroll + zoom.
// Sanskrit-term popover glossary (loads from data/glossary/).
// Vanilla ES module. No framework, no build step.

// ---------- layout constants (kept in sync with style.css :root) -----------
// Read responsive values from CSS so JS and CSS stay in sync.
function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if (!v) return fallback;
  const n = parseFloat(v);
  return Number.isFinite(n) ? n : fallback;
}
let TOPBAR_H = 48;
let LANE_H = 96;
let LANE_RAIL_W = 188;
let ERA_STRIP_H = 26;
const AXIS_H = 28;

function refreshLayoutConstants() {
  TOPBAR_H = cssVar("--topbar-h", 48);
  LANE_H = cssVar("--lane-h", 96);
  LANE_RAIL_W = cssVar("--lane-rail-w", 188);
  ERA_STRIP_H = cssVar("--era-strip-h", 26);
}

const PX_PER_YEAR_DEFAULT = 1.9;
const PAD_LEFT = 60;
const PAD_RIGHT = 80;

// On first load, center the viewport here (densest period of Vedānta thinkers).
const INITIAL_FOCUS_YEAR = 1100;

const LANE_ORDER = [
  "proto",
  "advaita",
  "bhedabheda",
  "vishishtadvaita",
  "dvaita",
  "acintya",
  "shuddha",
  "avibhaga",
  "samkhya-comparator",
  "yoga-comparator",
  "nyaya-comparator",
  "navya-nyaya-comparator",
  "vaisesika-comparator",
  "mimamsa-comparator",
  "jaina-comparator",
  "carvaka-comparator",
  "madhyamaka-comparator",
  "yogacara-comparator",
  "buddhist-pramana-comparator",
  "sarvastivada-comparator",
  "theravada-comparator",
  "tathagatagarbha-comparator",
  "trika-comparator",
  "pasupata-comparator",
  "pancaratra-comparator",
  "virashaiva-comparator",
  "bhairava-tantra-comparator",
  "cross-tradition",
];

const LANE_DISPLAY = {
  "proto": "Proto-Vedānta",
  "advaita": "Advaita",
  "bhedabheda": "Bhedābheda",
  "vishishtadvaita": "Viśiṣṭādvaita",
  "dvaita": "Dvaita",
  "acintya": "Acintya-Bhedābheda",
  "shuddha": "Śuddhādvaita",
  "avibhaga": "Avibhāgādvaita",
  "samkhya-comparator": "Sāṃkhya",
  "yoga-comparator": "Yoga",
  "nyaya-comparator": "Nyāya",
  "navya-nyaya-comparator": "Navya-Nyāya",
  "vaisesika-comparator": "Vaiśeṣika",
  "mimamsa-comparator": "Pūrva-Mīmāṃsā",
  "jaina-comparator": "Jaina",
  "carvaka-comparator": "Cārvāka",
  "madhyamaka-comparator": "Mādhyamaka",
  "yogacara-comparator": "Yogācāra",
  "buddhist-pramana-comparator": "Buddhist Pramāṇa",
  "sarvastivada-comparator": "Sarvāstivāda / Sautrāntika",
  "theravada-comparator": "Theravāda",
  "tathagatagarbha-comparator": "Tathāgatagarbha",
  "trika-comparator": "Pratyabhijñā / Trika",
  "pasupata-comparator": "Pāśupata",
  "pancaratra-comparator": "Pāñcarātra",
  "virashaiva-comparator": "Vīraśaiva",
  "bhairava-tantra-comparator": "Bhairava-tantra",
  "cross-tradition": "Cross-tradition",
};

// Compact labels for narrow viewports.
const LANE_DISPLAY_COMPACT = {
  "dvaita": "Dvaita",
  "acintya": "Acintya-Bhed.",
  "avibhaga": "Avibhāgādv.",
};
const COMPARATOR_GROUP_LABEL_COMPACT = "Other";
function isNarrowViewport() {
  return window.matchMedia && window.matchMedia("(max-width: 720px)").matches;
}
function laneDisplayName(tok) {
  if (isNarrowViewport() && LANE_DISPLAY_COMPACT[tok]) return LANE_DISPLAY_COMPACT[tok];
  return state.schools[tok]?.display_name || LANE_DISPLAY[tok] || tok;
}

// Vedāntic schools always render as their own lanes.
const VEDANTA_LANES = new Set([
  "proto", "advaita", "bhedabheda", "vishishtadvaita",
  "dvaita", "acintya", "shuddha", "avibhaga",
]);
// Other darśanas / cross-tradition collapse into one virtual group lane by default.
const COMPARATOR_LANES = [
  "samkhya-comparator", "yoga-comparator", "nyaya-comparator",
  "navya-nyaya-comparator", "vaisesika-comparator", "mimamsa-comparator",
  "jaina-comparator", "carvaka-comparator",
  "madhyamaka-comparator", "yogacara-comparator", "buddhist-pramana-comparator",
  "sarvastivada-comparator", "theravada-comparator", "tathagatagarbha-comparator",
  "trika-comparator",
  "pasupata-comparator", "pancaratra-comparator",
  "virashaiva-comparator", "bhairava-tantra-comparator",
  "cross-tradition",
];
const COMPARATOR_GROUP_KEY = "__comparator_group__";
const COMPARATOR_GROUP_LABEL = "Other darśanas";

const ERA_BANDS = [
  { name: "Pre-Śaṅkara",  low: -800, high:  700, fill: "#a8a29e", fillOpacity: 0.05 },
  { name: "Classical",    low:  700, high: 1100, fill: "#94a3b8", fillOpacity: 0.06 },
  { name: "Late-Medieval",low: 1100, high: 1500, fill: "#d97706", fillOpacity: 0.05 },
  { name: "Early-Modern", low: 1500, high: 1800, fill: "#9333ea", fillOpacity: 0.04 },
  { name: "Modern",       low: 1800, high: 2050, fill: "#0891b2", fillOpacity: 0.05 },
];

const TIER_1 = new Set([
  "sankara","ramanuja","madhva","caitanya","vallabha",
  "madhusudana","vyasatirtha","jiva-gosvami","nimbarka",
  "bhaskara","yamuna","sureshvara","mandana",
  "vijnanabhiksu","appayya","gaudapada","badarayana",
  "vidyaranya","prakasatman","abhinavagupta",
]);

// ---------- DOM refs -----------
const stage = document.getElementById("stage");
const detailPane = document.getElementById("detailPane");
const detailContent = document.getElementById("detailContent");
const closeDetail = document.getElementById("closeDetail");
const closeReader = document.getElementById("closeReader");
const readerModal = document.getElementById("readerModal");
const readerContent = document.getElementById("readerContent");
const scroller = document.getElementById("timelineScroller");
const canvas = document.getElementById("canvas");
const dotsLayer = document.getElementById("timelineDots");
const axisEl = document.getElementById("timelineAxis");
const svg = document.getElementById("timelineSvg");
const laneRailEl = document.getElementById("laneRail");
const eraStripEl = document.getElementById("eraStrip");
const subtitleEl = document.getElementById("subtitle");
const readingModeBtn = document.getElementById("readingModeBtn");

// ---------- state -----------
const state = {
  thinkers: [],
  thinkersById: new Map(),
  schools: {},
  subSchools: {},
  comparativeClaims: [],
  glossary: new Map(),       // term-key → entry
  glossaryRegex: null,
  range: { low: -800, high: 2050 },
  pxPerYear: PX_PER_YEAR_DEFAULT,
  layout: new Map(),         // id → {x, y, lane, shade, tier, barX1, barX2, name, label}
  activeId: null,
  // Filter state: which top-level lane tokens are currently visible.
  // Comparator group is a single virtual lane until expanded.
  visibleLanes: new Set([...VEDANTA_LANES, COMPARATOR_GROUP_KEY]),
  comparatorExpanded: false,
  // Effective render order, recomputed when filter / expansion changes.
  renderLanes: [],
  laneToIndex: new Map(),
  hasInitialScroll: false,
  // View mode: "lanes" (swim-lane cladogram) or "network" (free-form,
  // date-ordered, lineage-gravity collision-avoidance layout).
  viewMode: (function () {
    try {
      const v = localStorage.getItem("vedanta-view-mode");
      return v === "network" ? "network" : "lanes";
    } catch (_) { return "lanes"; }
  })(),
};

function setViewMode(mode) {
  if (mode !== "lanes" && mode !== "network") return;
  if (state.viewMode === mode) return;
  state.viewMode = mode;
  try { localStorage.setItem("vedanta-view-mode", mode); } catch (_) {}
  document.querySelectorAll(".view-toggle-btn").forEach((b) => {
    const on = b.dataset.view === mode;
    b.classList.toggle("is-active", on);
    b.setAttribute("aria-selected", on ? "true" : "false");
  });
  // Re-center on the dense period after layout swap.
  state.hasInitialScroll = false;
  renderAll();
  renderFilterChips();
  scrollToInitialFocus();
}

// ---------- loaders -----------
async function loadJSON(path) {
  try {
    const r = await fetch(path);
    if (!r.ok) return null;
    return await r.json();
  } catch (e) { return null; }
}

async function loadAll() {
  const manifest = await loadJSON("data/manifest.json");
  if (!manifest) {
    showEmptyState("No data yet — corpus pipeline is still populating.");
    return;
  }
  state.schools     = (await loadJSON("data/registries/schools.json"))     || {};
  state.subSchools  = (await loadJSON("data/registries/sub_schools.json")) || {};

  const thinkers = await Promise.all(
    (manifest.thinkers || []).map((f) => loadJSON(`data/thinkers/${f}`))
  );
  state.thinkers = thinkers.filter(Boolean);
  state.thinkers.forEach((t) => state.thinkersById.set(t.id, t));

  const claims = await Promise.all(
    (manifest.comparative_claims || []).map((f) => loadJSON(`data/comparative_claims/${f}`))
  );
  state.comparativeClaims = claims.filter(Boolean);

  // glossary (optional; absent on first deploy)
  const glossManifest = await loadJSON("data/glossary/manifest.json");
  if (glossManifest && Array.isArray(glossManifest.terms)) {
    const terms = await Promise.all(
      glossManifest.terms.map((f) => loadJSON(`data/glossary/${f}`))
    );
    for (const t of terms.filter(Boolean)) {
      state.glossary.set(t.term_key, t);
      for (const alias of (t.aliases || [])) {
        state.glossary.set(alias, t);
      }
    }
    buildGlossaryRegex();
  }

  computeRange();
  computeRenderLanes();
  computeLayout();
  renderAll();
  renderFilterChips();
  updateSubtitle();
  scrollToInitialFocus();
}

function scrollToInitialFocus() {
  if (state.hasInitialScroll) return;
  const x = yearToX(INITIAL_FOCUS_YEAR);
  const paneW = scroller.clientWidth;
  const railOffset = state.viewMode === "network" ? 0 : LANE_RAIL_W;
  scroller.scrollLeft = Math.max(0, x - paneW / 2 + railOffset);
  if (state.viewMode === "network") {
    const paneH = scroller.clientHeight;
    scroller.scrollTop = Math.max(0, NETWORK_CANVAS_H / 2 - paneH / 2 + ERA_STRIP_H);
  }
  state.hasInitialScroll = true;
}

function computeRange() {
  if (!state.thinkers.length) return;
  let lo = Infinity, hi = -Infinity;
  for (const t of state.thinkers) {
    if (typeof t.dates_low === "number") lo = Math.min(lo, t.dates_low);
    if (typeof t.dates_high === "number") hi = Math.max(hi, t.dates_high);
  }
  state.range.low = Math.floor(lo / 50) * 50 - 50;
  state.range.high = Math.ceil(hi / 50) * 50 + 50;
}

function updateSubtitle() {
  const n = state.thinkers.length;
  const span = state.range.high - state.range.low;
  subtitleEl.textContent = `${n} thinkers across ~${span} years.`;
}

// ---------- layout -----------
function yearToX(y) {
  return PAD_LEFT + (y - state.range.low) * state.pxPerYear;
}
function totalWidth() {
  return PAD_LEFT + (state.range.high - state.range.low) * state.pxPerYear + PAD_RIGHT;
}
function totalHeight() {
  if (state.viewMode === "network") return NETWORK_CANVAS_H + AXIS_H + 8;
  return state.renderLanes.length * LANE_H + AXIS_H + 8;
}
function plotHeight() {
  // height of the dots / svg layer (excludes axis)
  if (state.viewMode === "network") return NETWORK_CANVAS_H;
  return state.renderLanes.length * LANE_H;
}

// Build the effective rendered lane order from filter + expansion state.
// Each entry is { key, kind: "school" | "group" | "sub", token? } where
// `key` is what `laneIndex()` resolves a thinker into.
function computeRenderLanes() {
  const lanes = [];
  for (const tok of LANE_ORDER) {
    if (VEDANTA_LANES.has(tok)) {
      if (state.visibleLanes.has(tok)) lanes.push({ key: tok, kind: "school", token: tok });
    } else if (COMPARATOR_LANES.includes(tok)) {
      // handled below as one block
    }
  }
  // Insert comparator group lane (or expanded sub-lanes) at end.
  if (state.visibleLanes.has(COMPARATOR_GROUP_KEY)) {
    if (state.comparatorExpanded) {
      lanes.push({ key: COMPARATOR_GROUP_KEY, kind: "group", token: COMPARATOR_GROUP_KEY, expanded: true });
      for (const tok of COMPARATOR_LANES) {
        lanes.push({ key: tok, kind: "sub", token: tok });
      }
    } else {
      lanes.push({ key: COMPARATOR_GROUP_KEY, kind: "group", token: COMPARATOR_GROUP_KEY, expanded: false });
    }
  }
  state.renderLanes = lanes;
  state.laneToIndex.clear();
  lanes.forEach((l, i) => state.laneToIndex.set(l.key, i));
  // Map every comparator token to the group row when collapsed.
  if (!state.comparatorExpanded && state.laneToIndex.has(COMPARATOR_GROUP_KEY)) {
    const groupIdx = state.laneToIndex.get(COMPARATOR_GROUP_KEY);
    for (const tok of COMPARATOR_LANES) state.laneToIndex.set(tok, groupIdx);
  }
}

function laneIndex(token) {
  if (state.laneToIndex.has(token)) return state.laneToIndex.get(token);
  // Fallback: route unknown tokens to the comparator group if visible, else hide.
  if (state.laneToIndex.has(COMPARATOR_GROUP_KEY)) {
    return state.laneToIndex.get(COMPARATOR_GROUP_KEY);
  }
  return -1;
}

function isThinkerVisible(t) {
  const tok = t.school_color_token || "proto";
  if (VEDANTA_LANES.has(tok)) return state.visibleLanes.has(tok);
  return state.visibleLanes.has(COMPARATOR_GROUP_KEY);
}
function tierOf(t) {
  if (TIER_1.has(t.id)) return 1;
  if (t.dates_tier === "oral-tradition-only") return 3;
  return 2;
}

function colorFor(thinker, paletteIdx = 2) {
  const token = thinker.school_color_token || "proto";
  const school = state.schools[token];
  if (school?.color_palette) {
    const idx = Math.max(0, Math.min(4, paletteIdx));
    return school.color_palette[idx];
  }
  const base = {
    advaita: "#2563eb", vishishtadvaita: "#059669", dvaita: "#d97706",
    bhedabheda: "#9333ea", acintya: "#db2777", shuddha: "#be123c",
    avibhaga: "#0891b2", "trika-comparator": "#475569",
    "cross-tradition": "#475569", proto: "#6b7280",
    "samkhya-comparator": "#16a34a", "yoga-comparator": "#14b8a6",
    "nyaya-comparator": "#ca8a04", "navya-nyaya-comparator": "#a16207",
    "vaisesika-comparator": "#6d28d9", "mimamsa-comparator": "#7c3aed",
    "jaina-comparator": "#65a30d", "carvaka-comparator": "#57534e",
    "madhyamaka-comparator": "#7c2d12", "yogacara-comparator": "#155e75",
    "buddhist-pramana-comparator": "#3f3f46",
    "sarvastivada-comparator": "#92400e", "theravada-comparator": "#b45309",
    "tathagatagarbha-comparator": "#0e7490",
    "pasupata-comparator": "#b91c1c", "pancaratra-comparator": "#1e40af",
    "virashaiva-comparator": "#831843", "bhairava-tantra-comparator": "#4c1d95",
  };
  return base[token] || "#6b7280";
}

function shadeFor(thinker) {
  const s = thinker.sub_school_shade;
  if (typeof s === "number" && s >= 1 && s <= 5) return s;
  return 3;
}

// Network layout: vertical canvas height (used by totalHeight when in network mode).
const NETWORK_CANVAS_H = 1500;
const NETWORK_PAD_TOP = 50;
const NETWORK_PAD_BOTTOM = 60;

// Default y-band centroid for each school color token, normalized 0..1.
// Vedāntic schools cluster in the central band; comparators above/below.
// Hand-tuned so lineages naturally separate; greedy avoidance perturbs from here.
const SCHOOL_BAND = {
  // Comparators ABOVE (top third)
  "samkhya-comparator":         0.08,
  "yoga-comparator":            0.11,
  "nyaya-comparator":           0.14,
  "navya-nyaya-comparator":     0.17,
  "vaisesika-comparator":       0.20,
  "mimamsa-comparator":         0.23,
  "jaina-comparator":           0.26,
  "carvaka-comparator":         0.29,
  // Buddhist family — upper-middle
  "madhyamaka-comparator":      0.32,
  "yogacara-comparator":        0.35,
  "buddhist-pramana-comparator":0.36,
  "sarvastivada-comparator":    0.32,
  "theravada-comparator":       0.29,
  "tathagatagarbha-comparator": 0.38,
  // Vedānta — central band
  "proto":                      0.50,
  "advaita":                    0.45,
  "bhedabheda":                 0.50,
  "vishishtadvaita":            0.55,
  "dvaita":                     0.60,
  "acintya":                    0.66,
  "shuddha":                    0.62,
  "avibhaga":                   0.58,
  // Śaiva / Tantra / Vaiṣṇava-tantra — lower band
  "trika-comparator":           0.78,
  "pasupata-comparator":        0.75,
  "pancaratra-comparator":      0.72,
  "virashaiva-comparator":      0.82,
  "bhairava-tantra-comparator": 0.85,
  "cross-tradition":            0.92,
};

function computeLayout() {
  if (state.viewMode === "network") computeNetworkLayout();
  else computeLanesLayout();
}

function computeLanesLayout() {
  state.layout.clear();
  const sorted = [...state.thinkers].sort((a, b) => {
    return ((a.dates_low + a.dates_high) / 2) - ((b.dates_low + b.dates_high) / 2);
  });

  // for collision detection within same lane × shade, track placed dots
  const occupancy = new Map();   // `${lane}_${shade}` → array of {x1, x2}

  for (const t of sorted) {
    if (!isThinkerVisible(t)) continue;
    const lane = laneIndex(t.school_color_token);
    if (lane < 0) continue;
    const shade = shadeFor(t);
    const tier = tierOf(t);
    const xMid = yearToX((t.dates_low + t.dates_high) / 2);
    const x1 = yearToX(t.dates_low);
    const x2 = yearToX(t.dates_high);

    const subOffset = (shade - 3) * 11;   // -22 .. +22
    let nudge = 0;
    const key = `${lane}_${shade}`;
    const arr = occupancy.get(key) || [];
    for (const o of arr) {
      if (Math.abs(o.x - xMid) < 18) {
        nudge += (nudge >= 0 ? 8 : -8);
      }
    }
    arr.push({ x: xMid });
    occupancy.set(key, arr);

    const y = lane * LANE_H + LANE_H / 2 + subOffset + nudge;

    state.layout.set(t.id, {
      thinker: t, x: xMid, y, lane, shade, tier,
      barX1: x1, barX2: x2,
    });
  }
}

// Greedy date-ordered placement with lineage gravity + per-school band centroids.
// Deterministic given the input data. No external libs.
//
// For each thinker, in dates_low order:
//   1. desired y = blend(school-band centroid, mean-y of already-placed lineage_in)
//   2. step outward in 18 px increments from desired y until no other dot's
//      bounding box intersects within ± xPad of x.
//   3. clamp into [PAD_TOP, NETWORK_CANVAS_H - PAD_BOTTOM].
function computeNetworkLayout() {
  state.layout.clear();
  const sorted = [...state.thinkers].sort((a, b) => {
    const al = (typeof a.dates_low === "number") ? a.dates_low : 0;
    const bl = (typeof b.dates_low === "number") ? b.dates_low : 0;
    if (al !== bl) return al - bl;
    return ((a.dates_low + a.dates_high) / 2) - ((b.dates_low + b.dates_high) / 2);
  });

  const placed = []; // [{x, y, r, id}]
  const STEP = 18;
  const X_PAD = 60;
  const Y_PAD = 26;

  const usableH = NETWORK_CANVAS_H - NETWORK_PAD_TOP - NETWORK_PAD_BOTTOM;
  const yFromBand = (b) => NETWORK_PAD_TOP + b * usableH;

  for (const t of sorted) {
    if (!isThinkerVisible(t)) continue;
    const tok = t.school_color_token || "proto";
    const tier = tierOf(t);
    const xMid = yearToX((t.dates_low + t.dates_high) / 2);
    const x1 = yearToX(t.dates_low);
    const x2 = yearToX(t.dates_high);

    // Lineage gravity: average y of already-placed predecessors.
    let lineageY = null;
    let lineageN = 0;
    let lineageSum = 0;
    for (const inId of (t.lineage_in || [])) {
      const p = state.layout.get(inId);
      if (p) { lineageSum += p.y; lineageN++; }
    }
    if (lineageN > 0) lineageY = lineageSum / lineageN;

    const bandY = yFromBand(SCHOOL_BAND[tok] != null ? SCHOOL_BAND[tok] : 0.5);
    // Pull strongly toward lineage when present, else use band centroid.
    const desiredY = lineageY != null ? (0.55 * lineageY + 0.45 * bandY) : bandY;

    // Walk outward from desiredY in STEP increments, alternating sign,
    // until we find a slot with no neighbor within (X_PAD x, Y_PAD y).
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

// ---------- render: lane rail -----------
function renderLaneRail() {
  laneRailEl.innerHTML = "";
  if (state.viewMode === "network") {
    // Network view collapses the rail; legend is shown instead.
    laneRailEl.style.height = "0px";
    return;
  }
  // Per-token thinker counts (real schools only).
  const counts = new Map();
  for (const t of state.thinkers) {
    const tok = t.school_color_token || "proto";
    counts.set(tok, (counts.get(tok) || 0) + 1);
  }
  let comparatorTotal = 0;
  for (const tok of COMPARATOR_LANES) comparatorTotal += counts.get(tok) || 0;

  for (const lane of state.renderLanes) {
    const row = document.createElement("div");
    row.style.height = LANE_H + "px";
    row.dataset.lane = lane.key;

    if (lane.kind === "group") {
      row.className = "lane-row lane-row--group" + (lane.expanded ? " is-expanded" : "");
      row.setAttribute("role", "button");
      row.setAttribute("tabindex", "0");
      row.setAttribute("aria-expanded", lane.expanded ? "true" : "false");
      const groupLabel = isNarrowViewport() ? COMPARATOR_GROUP_LABEL_COMPACT : COMPARATOR_GROUP_LABEL;
      const groupCount = isNarrowViewport()
        ? `${comparatorTotal} · ${COMPARATOR_LANES.length}`
        : `${comparatorTotal} thinkers · ${COMPARATOR_LANES.length} schools`;
      row.innerHTML = `
        <span class="swatch-bar"></span>
        <div class="lane-meta">
          <span class="lane-name">${escape(groupLabel)}</span>
          <span class="lane-count">${escape(groupCount)}</span>
        </div>
        <span class="lane-chevron" aria-hidden="true">▸</span>
      `;
      const toggle = () => { state.comparatorExpanded = !state.comparatorExpanded; rerender(); };
      row.addEventListener("click", toggle);
      row.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
      });
    } else {
      const tok = lane.token;
      const display = laneDisplayName(tok);
      const swatch = state.schools[tok]?.color_palette?.[2]
                  || state.schools[tok]?.color_hex
                  || colorFor({ school_color_token: tok }, 2);
      const count = counts.get(tok) || 0;
      const subClass = lane.kind === "sub" ? " lane-row--sub" : "";
      row.className = "lane-row" + subClass;
      row.innerHTML = `
        <span class="swatch-bar" style="background:${swatch}"></span>
        <div class="lane-meta">
          <span class="lane-name">${escape(display)}</span>
          <span class="lane-count">${count} ${count === 1 ? "thinker" : "thinkers"}</span>
        </div>
      `;
    }
    laneRailEl.appendChild(row);
  }
  laneRailEl.style.height = (state.renderLanes.length * LANE_H) + "px";
}

// ---------- render: era strip -----------
function renderEraStrip() {
  eraStripEl.innerHTML = "";
  eraStripEl.style.width = totalWidth() + "px";
  for (const era of ERA_BANDS) {
    if (era.high < state.range.low || era.low > state.range.high) continue;
    const lo = Math.max(era.low, state.range.low);
    const hi = Math.min(era.high, state.range.high);
    const x = yearToX(lo);
    const w = yearToX(hi) - x;
    const el = document.createElement("div");
    el.className = "era-label";
    el.style.left = x + "px";
    el.style.width = w + "px";
    el.textContent = era.name;
    eraStripEl.appendChild(el);
  }
}

// ---------- render: era bands (svg) -----------
function renderEraBands() {
  const ns = "http://www.w3.org/2000/svg";
  const g = document.createElementNS(ns, "g");
  g.setAttribute("class", "era-bands");
  const h = plotHeight();
  for (const era of ERA_BANDS) {
    if (era.high < state.range.low || era.low > state.range.high) continue;
    const lo = Math.max(era.low, state.range.low);
    const hi = Math.min(era.high, state.range.high);
    const x = yearToX(lo);
    const w = yearToX(hi) - x;
    const r = document.createElementNS(ns, "rect");
    r.setAttribute("class", "era-band");
    r.setAttribute("x", x);
    r.setAttribute("y", 0);
    r.setAttribute("width", w);
    r.setAttribute("height", h);
    r.setAttribute("fill", era.fill);
    r.setAttribute("fill-opacity", era.fillOpacity);
    g.appendChild(r);
  }
  if (state.viewMode === "network") {
    // Faint horizontal anchor at canvas vertical-midpoint.
    const spine = document.createElementNS(ns, "line");
    spine.setAttribute("class", "network-spine");
    spine.setAttribute("x1", 0);
    spine.setAttribute("x2", totalWidth());
    spine.setAttribute("y1", h / 2);
    spine.setAttribute("y2", h / 2);
    g.appendChild(spine);
  } else {
    // lane separators
    for (let i = 1; i < state.renderLanes.length; i++) {
      const line = document.createElementNS(ns, "line");
      line.setAttribute("class", "lane-separator");
      line.setAttribute("x1", 0);
      line.setAttribute("x2", totalWidth());
      line.setAttribute("y1", i * LANE_H);
      line.setAttribute("y2", i * LANE_H);
      g.appendChild(line);
    }
  }
  svg.appendChild(g);
}

// ---------- render: lineage edges (view-aware) -----------
function renderEdges() {
  const ns = "http://www.w3.org/2000/svg";
  const g = document.createElementNS(ns, "g");
  g.setAttribute("class", "edges");
  const edgeFn = state.viewMode === "network" ? bezierEdge : manhattanEdge;

  for (const [, p] of state.layout) {
    const t = p.thinker;
    for (const targetId of (t.lineage_out || [])) {
      const target = state.layout.get(targetId);
      if (!target) continue;
      const path = edgeFn(p, target);
      const el = document.createElementNS(ns, "path");
      el.setAttribute("class", "lineage-edge");
      el.setAttribute("d", path);
      el.style.setProperty("--edge-color", colorFor(t, 2));
      el.dataset.from = t.id;
      el.dataset.to = targetId;
      g.appendChild(el);
    }
    for (const pol of (t.lineage_polemical || [])) {
      const target = state.layout.get(pol.thinker_id);
      if (!target) continue;
      const path = edgeFn(p, target);
      const el = document.createElementNS(ns, "path");
      el.setAttribute("class", "lineage-edge lineage-edge--polemical");
      el.setAttribute("d", path);
      el.dataset.from = t.id;
      el.dataset.to = pol.thinker_id;
      g.appendChild(el);
    }
  }
  svg.appendChild(g);
}

function manhattanEdge(a, b) {
  const x1 = a.x, y1 = a.y, x2 = b.x, y2 = b.y;
  if (Math.abs(y1 - y2) < 4) {
    return `M ${x1} ${y1} L ${x2} ${y2}`;
  }
  const stub = 8;
  const midX = x1 + 0.55 * (x2 - x1);
  return `M ${x1} ${y1} L ${x1} ${y1 + Math.sign(y2-y1)*stub} L ${midX} ${y1 + Math.sign(y2-y1)*stub} L ${midX} ${y2 - Math.sign(y2-y1)*stub} L ${x2} ${y2 - Math.sign(y2-y1)*stub} L ${x2} ${y2}`;
}

// Smooth cubic bezier for the network view: control points at the horizontal
// midpoint, anchored to the source/target y. Reads as an organic flow.
function bezierEdge(a, b) {
  const x1 = a.x, y1 = a.y, x2 = b.x, y2 = b.y;
  const dx = x2 - x1;
  if (Math.abs(dx) < 2) {
    return `M ${x1} ${y1} L ${x2} ${y2}`;
  }
  const cx1 = x1 + dx * 0.5;
  const cx2 = x1 + dx * 0.5;
  return `M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`;
}

// ---------- render: date-range bars (svg) -----------
function renderDateBars() {
  const ns = "http://www.w3.org/2000/svg";
  const g = document.createElementNS(ns, "g");
  g.setAttribute("class", "date-bars");
  for (const [, p] of state.layout) {
    const t = p.thinker;
    if (p.barX2 - p.barX1 < 4) continue;
    if (t.dates_tier === "oral-tradition-only") {
      const line = document.createElementNS(ns, "line");
      line.setAttribute("class", "date-bar--oral");
      line.setAttribute("x1", p.barX1);
      line.setAttribute("x2", p.barX2);
      line.setAttribute("y1", p.y);
      line.setAttribute("y2", p.y);
      line.style.setProperty("--dot-color", colorFor(t, 2));
      g.appendChild(line);
    } else {
      const r = document.createElementNS(ns, "rect");
      r.setAttribute("class", "date-bar");
      r.setAttribute("x", p.barX1);
      r.setAttribute("y", p.y - 1.5);
      r.setAttribute("width", p.barX2 - p.barX1);
      r.setAttribute("height", 3);
      r.setAttribute("rx", 1.5);
      r.style.setProperty("--dot-color", colorFor(t, 2));
      r.setAttribute("fill", colorFor(t, 2));
      r.setAttribute("fill-opacity", "0.45");
      g.appendChild(r);
    }
  }
  svg.appendChild(g);
}

// ---------- render: dots -----------
function renderDots() {
  dotsLayer.innerHTML = "";
  // for label collision, place above by default; collect bands of placed labels
  const placedAbove = []; // {y, x1, x2}
  const placedBelow = [];
  for (const [, p] of state.layout) {
    const t = p.thinker;
    const labelW = (t.name || t.id).length * 7 + 16;
    let where = "above";
    const conflictsAbove = placedAbove.some((q) => Math.abs(q.y - p.y) < 24 && !(q.x2 < p.x - labelW/2 - 4 || q.x1 > p.x + labelW/2 + 4));
    if (conflictsAbove) where = "below";
    const arr = where === "above" ? placedAbove : placedBelow;
    arr.push({ y: p.y, x1: p.x - labelW/2, x2: p.x + labelW/2 });

    const dot = document.createElement("div");
    dot.className = `thinker-dot thinker-dot--tier-${p.tier} label-${where}`;
    if (t.dates_tier === "oral-tradition-only") dot.classList.add("thinker-dot--oral");
    dot.dataset.id = t.id;
    dot.dataset.school = t.school_color_token;
    dot.dataset.shade = p.shade;
    dot.dataset.tier = p.tier;
    dot.style.left = p.x + "px";
    dot.style.top = p.y + "px";
    dot.style.setProperty("--dot-color", colorFor(t, 2));
    dot.setAttribute("tabindex", "0");
    dot.setAttribute("role", "button");
    dot.setAttribute("aria-label", t.name_iast || t.name || t.id);
    dot.innerHTML = `
      <div class="node"></div>
      <div class="label">
        <span class="name">${escape(t.name || t.id)}</span>
        <span class="dates">${formatDates(t)}</span>
      </div>
    `;
    dot.addEventListener("click", (e) => { e.stopPropagation(); openThinker(t.id); });
    dot.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openThinker(t.id); }
    });
    dot.addEventListener("mouseenter", () => onDotHover(t.id, true));
    dot.addEventListener("mouseleave", () => onDotHover(t.id, false));
    dotsLayer.appendChild(dot);
  }
}

function onDotHover(id, on) {
  dotsLayer.classList.toggle("has-hover", on);
  document.querySelectorAll(".lineage-edge").forEach((el) => {
    el.classList.toggle("is-lit", on && (el.dataset.from === id || el.dataset.to === id));
  });
}

// ---------- render: axis -----------
function renderAxis() {
  axisEl.innerHTML = "";
  axisEl.style.width = totalWidth() + "px";
  const start = Math.ceil(state.range.low / 100) * 100;
  for (let y = start; y <= state.range.high; y += 100) {
    const el = document.createElement("div");
    el.className = "year-tick";
    el.style.left = yearToX(y) + "px";
    el.textContent = y < 0 ? `${-y} BCE` : `${y} CE`;
    axisEl.appendChild(el);
  }
}

// ---------- render: orchestrator -----------
function renderAll() {
  refreshLayoutConstants();
  computeRenderLanes();
  // Reapply layout in case visibleLanes / expansion / view-mode changed.
  computeLayout();
  document.body.classList.toggle("view-network", state.viewMode === "network");
  document.body.classList.toggle("view-lanes", state.viewMode === "lanes");
  const w = totalWidth();
  const h = totalHeight();
  const ph = plotHeight();
  canvas.style.width = w + "px";
  canvas.style.height = h + "px";
  dotsLayer.style.width = w + "px";
  dotsLayer.style.height = ph + "px";
  svg.setAttribute("width", w);
  svg.setAttribute("height", ph);
  svg.style.width = w + "px";
  svg.style.height = ph + "px";
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  renderLaneRail();
  renderEraStrip();
  renderEraBands();
  renderEdges();
  renderDateBars();
  renderDots();
  renderAxis();
  renderNetworkLegend();
}

// Recompute lane order + filter and re-render. Preserves scroll position
// horizontally; vertical position resets only when lane count changes meaningfully.
function rerender() {
  const prevLeft = scroller.scrollLeft;
  renderAll();
  scroller.scrollLeft = prevLeft;
  renderFilterChips();
}

// ---------- canvas pan (drag) + wheel + zoom -----------
function wirePanZoom() {
  let isDragging = false;
  let dragStartX = 0, dragStartY = 0;
  let scrollStartX = 0, scrollStartY = 0;
  let didDrag = false;

  scroller.addEventListener("mousedown", (e) => {
    if (e.button !== 0) return;
    if (e.target.closest(".thinker-dot, .lane-row, button, a")) return;
    isDragging = true;
    didDrag = false;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    scrollStartX = scroller.scrollLeft;
    scrollStartY = scroller.scrollTop;
    scroller.style.cursor = "grabbing";
    scroller.style.userSelect = "none";
    e.preventDefault();
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - dragStartX;
    const dy = e.clientY - dragStartY;
    if (Math.abs(dx) + Math.abs(dy) > 4) didDrag = true;
    scroller.scrollLeft = scrollStartX - dx;
    scroller.scrollTop = scrollStartY - dy;
  });

  window.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      scroller.style.cursor = "";
      scroller.style.userSelect = "";
    }
  });

  // wheel: vertical wheel pans Y; shift+wheel pans X; ctrl+wheel zooms
  scroller.addEventListener("wheel", (e) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      const oldPpy = state.pxPerYear;
      const factor = e.deltaY < 0 ? 1.08 : 1/1.08;
      const newPpy = Math.max(0.6, Math.min(6, oldPpy * factor));
      if (newPpy === oldPpy) return;
      // anchor zoom on cursor x position
      const rect = scroller.getBoundingClientRect();
      const railOffset = state.viewMode === "network" ? 0 : LANE_RAIL_W;
      const cursorX = e.clientX - rect.left + scroller.scrollLeft - railOffset;
      const yearAtCursor = state.range.low + cursorX / state.pxPerYear;
      state.pxPerYear = newPpy;
      computeLayout();
      renderAll();
      const newCursorX = (yearAtCursor - state.range.low) * state.pxPerYear;
      scroller.scrollLeft = newCursorX - (e.clientX - rect.left) + railOffset;
    } else if (e.shiftKey) {
      e.preventDefault();
      scroller.scrollLeft += e.deltaY;
    }
    // otherwise: native vertical scroll behavior
  }, { passive: false });

  // touch / trackpad two-finger pan handled natively by the browser
}

// ---------- detail pane -----------
function openThinker(id) {
  const t = state.thinkersById.get(id);
  if (!t) return;
  state.activeId = id;
  document.body.classList.add("is-detail-open");
  detailPane.setAttribute("aria-hidden", "false");
  document.querySelectorAll(".thinker-dot").forEach((d) => {
    d.classList.toggle("is-active", d.dataset.id === id);
  });
  document.querySelectorAll(".lineage-edge").forEach((el) => {
    el.classList.toggle("is-lit", el.dataset.from === id || el.dataset.to === id);
  });
  detailContent.style.setProperty("--dot-color", colorFor(t, 2));
  detailContent.style.setProperty("--school-light", colorFor(t, 1));
  detailContent.innerHTML = renderDetail(t);
  detailPane.scrollTop = 0;
  scrollDotIntoView(t);
  // wire read-full buttons
  detailContent.querySelectorAll("[data-read-full]").forEach((btn) => {
    btn.addEventListener("click", () => openReader(btn.dataset.readFull, btn.dataset.thinker));
  });
}

function scrollDotIntoView(t) {
  const p = state.layout.get(t.id);
  if (!p) return;
  const paneW = scroller.clientWidth;
  const paneH = scroller.clientHeight;
  const railOffset = state.viewMode === "network" ? 0 : LANE_RAIL_W;
  // horizontal: center the dot
  const desiredLeft = Math.max(0, p.x - paneW / 2 + railOffset);
  // vertical: center the lane
  const desiredTop = Math.max(0, p.y - paneH / 2 + ERA_STRIP_H);
  scroller.scrollTo({ left: desiredLeft, top: desiredTop, behavior: "smooth" });
}

function closeDetailPane() {
  document.body.classList.remove("is-detail-open");
  detailPane.setAttribute("aria-hidden", "true");
  state.activeId = null;
  document.querySelectorAll(".thinker-dot").forEach((d) => d.classList.remove("is-active"));
  document.querySelectorAll(".lineage-edge").forEach((el) => el.classList.remove("is-lit"));
}
closeDetail.addEventListener("click", closeDetailPane);

// ---------- detail rendering -----------
function renderDetail(t) {
  return [
    renderHero(t),
    renderLineageBlock(t),
    renderEngagedWorks(t),
    renderOrphanPassages(t),
    renderComparativeBlock(t),
  ].filter(Boolean).join("");
}

function renderHero(t) {
  const tierLabel = {
    "confirmed-from-records": "Dates confirmed (records)",
    "consensus-textual": "Dates by textual consensus",
    "contested": "Dates contested",
    "oral-tradition-only": "Oral tradition only",
  }[t.dates_tier] || (t.dates_tier || "");
  const subSchool = t.sub_school ? " · " + escape(t.sub_school) : "";
  return `
    <div class="detail-hero">
      <h2>${escape(t.name_iast || t.name || t.id)}</h2>
      ${t.name && t.name !== t.name_iast ? `<p class="romanization">${escape(t.name)}</p>` : ""}
      <div class="meta-row">
        <span class="school-pill">${escape(t.school || "")}${subSchool}</span>
        ${tierLabel ? `<span class="tier-pill">${escape(tierLabel)}</span>` : ""}
      </div>
      <p class="dates-line">${escape(formatDatesLong(t))}${t.dates_notes ? " · " + md(t.dates_notes) : ""}</p>
      <div class="thesis">${md(t.core_thesis || "Core thesis: not yet written.")}</div>
    </div>
  `;
}

function renderLineageBlock(t) {
  const linkList = (ids) => (ids || []).map(linkThinker).filter(Boolean).join(", ");
  const inHTML = linkList(t.lineage_in);
  const outHTML = linkList(t.lineage_out);
  const polHTML = (t.lineage_polemical || [])
    .map((p) => {
      const link = linkThinker(p.thinker_id);
      if (!link) return "";
      return `${link} <em>(${escape(p.direction || "engages")})</em>`;
    })
    .filter(Boolean).join(", ");
  if (!inHTML && !outHTML && !polHTML) return "";
  return `
    <h3 class="section-head">Lineage</h3>
    <div class="lineage-block">
      ${inHTML ? `<div class="lin-row"><span class="lin-label">From</span>${inHTML}</div>` : ""}
      ${outHTML ? `<div class="lin-row"><span class="lin-label">To</span>${outHTML}</div>` : ""}
      ${polHTML ? `<div class="lin-row"><span class="lin-label">Polemics</span>${polHTML}</div>` : ""}
    </div>
  `;
}

function renderEngagedWorks(t) {
  const works = t.engaged_works || [];
  if (!works.length) return "";
  const allPassages = t.key_passages || [];
  const cards = works.map((w) => {
    const passages = allPassages.filter((p) => p.work_id === w.work_id);
    return renderWorkCard(w, passages, t.id);
  }).join("");
  return `<h3 class="section-head">Engaged works</h3>${cards}`;
}

function renderWorkCard(w, passages, thinkerId) {
  const ascr = (w.ascription_tier || "").replace(/-/g, " ");
  return `
    <div class="work-card" data-work-id="${escape(w.work_id)}">
      <div class="title-line">
        <span class="title">${escape(w.title_iast || w.title || w.work_id)}</span>
        ${ascr ? `<span class="ascr">${escape(ascr)}</span>` : ""}
      </div>
      <p class="summary">${md(w.summary || "")}</p>
      ${w.ascription_notes ? `<p class="ascr-notes">${md(w.ascription_notes)}</p>` : ""}
      <button class="read-full-link" data-read-full="${escape(w.work_id)}" data-thinker="${escape(thinkerId)}">Read the full work in translation</button>
      ${passages.length ? `
        <div class="passages-nested">
          <p class="nested-head">Passages from this work</p>
          ${passages.map(renderPassageCard).join("")}
        </div>` : ""}
    </div>
  `;
}

function renderOrphanPassages(t) {
  const works = new Set((t.engaged_works || []).map((w) => w.work_id));
  const orphans = (t.key_passages || []).filter((p) => !works.has(p.work_id));
  if (!orphans.length) return "";
  return `<h3 class="section-head">Other key passages</h3>${orphans.map(renderPassageCard).join("")}`;
}

function renderPassageCard(p) {
  return `
    <div class="passage-card" data-passage-id="${escape(p.passage_id || "")}" data-work-id="${escape(p.work_id || "")}">
      <p class="locus">${escape(p.locus_long || p.locus_short || "")}</p>
      ${p.sanskrit_iast ? `<p class="sanskrit">${escape(p.sanskrit_iast)}</p>` : ""}
      <p class="english">${md(p.english_close || "")}</p>
      ${p.why_this_passage ? `<p class="why">${md(p.why_this_passage)}</p>` : ""}
      ${renderPaniniDetails(p)}
    </div>
  `;
}

function renderPaniniDetails(p) {
  const pb = p.panini_breakdown;
  if (!pb) return "";
  const sections = [];
  if (pb.pada_analysis?.length) {
    sections.push(paniniTable("Pada-analysis",
      ["Pada","Stem","Pratyaya","Morphology","Gloss"],
      pb.pada_analysis.map((r) => [r.pada, r.stem, r.pratyaya || "", r.morphology, r.gloss])));
  }
  if (pb.samasa_vigrahas?.length) {
    sections.push(paniniTable("Samāsa-vigraha",
      ["Compound","Type","Resolution","Note"],
      pb.samasa_vigrahas.map((r) => [r.compound, r.type, r.resolution, r.note || ""])));
  }
  if (pb.karaka_structure?.length) {
    sections.push(paniniTable("Kāraka structure",
      ["Role","Pada","Note"],
      pb.karaka_structure.map((r) => [r.role, r.pada, r.note || ""])));
  }
  if (pb.verb_modality?.length) {
    sections.push(paniniTable("Verbal modality",
      ["Pada","Lakāra","Pada (P/Ā)","Voice","Note"],
      pb.verb_modality.map((r) => [r.pada, r.lakara, r.pada_PA, r.voice, r.note || ""])));
  }
  if (!sections.length) return "";
  return `<details><summary>Pāṇinian breakdown</summary>${sections.join("")}</details>`;
}

function paniniTable(title, headers, rows) {
  const head = headers.map((h) => `<th>${escape(h)}</th>`).join("");
  const body = rows.map((r) => `<tr>${r.map((c) => `<td>${escape(c)}</td>`).join("")}</tr>`).join("");
  return `<div class="panini-section"><h4>${escape(title)}</h4><table class="panini-table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function renderComparativeBlock(t) {
  const ids = t.comparative_claim_ids || [];
  if (!ids.length) return "";
  const cards = ids.map((cid) => {
    const claim = state.comparativeClaims.find((c) => c.claim_id === cid);
    if (!claim) return "";
    return renderComparativeCard(claim, t.id);
  }).filter(Boolean).join("");
  if (!cards) return "";
  return `<h3 class="section-head">Comparative claims</h3>${cards}`;
}

function renderComparativeCard(claim, thinkerId) {
  const otherId = claim.thinker_a === thinkerId ? claim.thinker_b : claim.thinker_a;
  const other = state.thinkersById.get(otherId);
  const otherName = other?.name_iast || other?.name || otherId;
  const verdict = claim.verdict || "contested";
  const verdictLabel = verdict.replace(/-/g, " ");
  return `
    <div class="compclaim-card" data-claim-id="${escape(claim.claim_id || "")}" data-verdict="${escape(verdict)}">
      <span class="verdict-pill">${escape(verdictLabel)}</span>
      <p class="pair">vs. ${linkThinker(otherId)} on <strong>${escape(claim.category || "")}</strong>${claim.sub_axis ? ` <em>(${escape(claim.sub_axis)})</em>` : ""}</p>
      <div class="body">
        ${claim.surface_disagreement ? `<p><em>Surface:</em> ${md(claim.surface_disagreement)}</p>` : ""}
        ${claim.world_model_unpacking?.structural_mapping ? `<p><em>Structural mapping:</em> ${md(claim.world_model_unpacking.structural_mapping)}</p>` : ""}
        ${claim.commentary ? `<p>${md(claim.commentary)}</p>` : ""}
      </div>
    </div>
  `;
}

function linkThinker(id) {
  const t = state.thinkersById.get(id);
  if (!t) return "";
  return `<a href="#" data-thinker-link="${escape(id)}">${escape(t.name_iast || t.name || id)}</a>`;
}

document.addEventListener("click", (e) => {
  const a = e.target.closest("[data-thinker-link]");
  if (a) {
    e.preventDefault();
    openThinker(a.dataset.thinkerLink);
    return;
  }
  // glossary popovers
  const term = e.target.closest("[data-term]");
  if (term) {
    e.preventDefault();
    openGlossary(term.dataset.term, term);
  }
});

// ---------- reader modal (full work translation) -----------
async function openReader(workId, thinkerId) {
  const t = state.thinkersById.get(thinkerId);
  if (!t) return;
  const work = (t.engaged_works || []).find((w) => w.work_id === workId);
  if (!work) return;
  const url = `data/full_translations/${thinkerId}__${workId}.md`;
  const r = await fetch(url);
  let body;
  if (r.ok) {
    body = await r.text();
  } else {
    // No extended translation file yet — synthesize a placeholder using what IS in the JSON.
    const passages = (t.key_passages || []).filter((p) => p.work_id === workId);
    const passagesBlock = passages.length
      ? "## Engaged passages\n\n" + passages.map((p) => {
          const sk = p.sanskrit_iast ? `> *${p.sanskrit_iast.replace(/\n/g, " ")}*` : "";
          const en = p.english_close ? p.english_close : "";
          const why = p.why_this_passage ? `\n*Why this passage:* ${p.why_this_passage}` : "";
          return `### ${p.locus_long || p.locus_short || ""}\n\n${sk}\n\n${en}${why}`;
        }).join("\n\n---\n\n")
      : "";
    body = `# ${work.title_iast || work.title}
**by ${t.name_iast || t.name}** · ${(work.genre || "").replace(/-/g, " ")} · ${work.language || "sanskrit"}

${work.summary || ""}

---

## Status of translation

A complete extended-passage translation of this work — line-by-line with full Pāṇinian breakdown per line — has not yet been produced. The corpus dispatch pipeline produces these in waves; this work is queued for a future Codex 5.4 pass.

What is currently engaged on the site:
- The work-summary above (a 100-200 word account of what the work does and where it sits in the thinker's larger position).
- ${passages.length ? `${passages.length} key-passage card${passages.length === 1 ? "" : "s"} below, each carrying the Sanskrit (IAST), a faithful English rendering, the *why-this-passage* justification, and a collapsed Pāṇinian breakdown table (pada-analysis, samāsa-vigraha, kāraka structure, verb modality).` : "No key-passage cards yet — the primary text is queued for Codex extraction."}
- The thinker's *core thesis* (in the detail panel) cites this work where it is load-bearing.

For the cited-but-not-fully-translated portions: where a standard scholarly English edition exists (Ganganatha Jha for Mīmāṃsā, Mayeda for *Upadeśa-Sāhasrī*, Thibaut / Gambhirananda for Brahma-Sūtra-Bhāṣya, Carman / Lester for Rāmānuja, Sharma for Madhva, etc.), it is referenced in the work-summary's *source_edition* field. The site does not redistribute those translations.

${passagesBlock}`;
  }
  readerContent.innerHTML = renderMarkdownFull(body);
  readerModal.classList.add("is-open");
  readerModal.setAttribute("aria-hidden", "false");
}
closeReader.addEventListener("click", () => {
  readerModal.classList.remove("is-open");
  readerModal.setAttribute("aria-hidden", "true");
});

// ---------- glossary popover -----------
function buildGlossaryRegex() {
  if (state.glossary.size === 0) return;
  const keys = [...state.glossary.keys()].sort((a, b) => b.length - a.length);
  const escaped = keys.map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  state.glossaryRegex = new RegExp(`\\b(${escaped.join("|")})\\b`, "g");
}

function openGlossary(termKey, anchorEl) {
  const entry = state.glossary.get(termKey);
  if (!entry) return;
  // close any existing popover + scrim
  document.querySelectorAll(".glossary-popover, .gloss-scrim").forEach((el) => el.remove());
  const isMobile = window.matchMedia("(max-width: 720px)").matches;
  const pop = document.createElement("div");
  pop.className = "glossary-popover";
  const perSchool = (entry.per_school || []).map((s) =>
    `<div class="gp-row"><span class="gp-school">${escape(s.school)}</span><span class="gp-def">${md(s.definition)}</span></div>`
  ).join("");
  const translatorNote = entry.translator_note
    ? `<div class="gp-translator"><span class="gp-label">Translator note</span><div>${md(entry.translator_note)}</div></div>`
    : "";
  pop.innerHTML = `
    <button class="gp-close" aria-label="Close">×</button>
    <div class="gp-term">${escape(entry.term_iast || termKey)}</div>
    ${entry.literal ? `<div class="gp-literal">Literally: <em>${escape(entry.literal)}</em></div>` : ""}
    <div class="gp-invariant"><span class="gp-label">${entry.invariant_definition && entry.invariant_definition.toLowerCase().includes("no shared invariant") ? "No invariant" : "Invariant"}</span><div>${md(entry.invariant_definition || "")}</div></div>
    ${perSchool ? `<div class="gp-perschool"><span class="gp-label">By school</span>${perSchool}</div>` : ""}
    ${translatorNote}
  `;
  let scrim = null;
  if (isMobile) {
    scrim = document.createElement("div");
    scrim.className = "gloss-scrim";
    document.body.appendChild(scrim);
    document.body.appendChild(pop);
    // mobile uses CSS-positioned fixed bottom-sheet (see style.css @media block)
    scrim.addEventListener("click", () => closeGloss());
  } else {
    document.body.appendChild(pop);
    const r = anchorEl.getBoundingClientRect();
    pop.style.position = "fixed";
    const popH = pop.offsetHeight || 240;
    const placeBelow = (r.bottom + popH + 8) < window.innerHeight;
    pop.style.top = (placeBelow ? r.bottom + 8 : Math.max(10, r.top - popH - 8)) + "px";
    pop.style.left = Math.max(10, Math.min(r.left, window.innerWidth - 400)) + "px";
  }
  function closeGloss() {
    pop.remove();
    if (scrim) scrim.remove();
    document.removeEventListener("click", outsideClose);
    document.removeEventListener("keydown", escClose);
  }
  function outsideClose(e) {
    if (!pop.contains(e.target) && e.target !== anchorEl && e.target !== scrim) {
      closeGloss();
    }
  }
  function escClose(e) { if (e.key === "Escape") closeGloss(); }
  pop.querySelector(".gp-close").addEventListener("click", closeGloss);
  // defer outside-click handler to next tick so it doesn't fire on the opening click
  setTimeout(() => document.addEventListener("click", outsideClose), 0);
  document.addEventListener("keydown", escClose);
}

// ---------- markdown helpers -----------
function escape(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

function md(s) {
  if (s == null) return "";
  let out = escape(s);
  // Bold first (longer match), then italic. Inline-italic uses lookbehind/lookahead
  // to forbid whitespace adjacent to the asterisk (avoids math-like "2 * 3"),
  // but does NOT require surrounding punctuation — so "*foo*-bar" or "(*foo*)" both work.
  out = out.replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>");
  out = out.replace(/`([^`]+?)`/g, "<code>$1</code>");
  // glossary tagging — wrap matched terms in clickable spans (after italics so we don't double-wrap inside <em>)
  if (state.glossaryRegex) {
    out = out.replace(state.glossaryRegex, (m, _g, offset, full) => {
      // Don't wrap if we're already inside a span (e.g., inside <em>...</em> the term will still render correctly without click)
      // Actually we want clicks to work everywhere, so wrap unconditionally.
      return `<span class="term" data-term="${escape(m)}">${m}</span>`;
    });
  }
  return out;
}

function renderMarkdown(s) {
  const esc = (x) => x.replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  return esc(s)
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^&gt; (.+)$/gm, "<blockquote>$1</blockquote>")
    .replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>")
    .replace(/`([^`]+?)`/g, "<code>$1</code>")
    .replace(/\n\n+/g, "</p><p>")
    .replace(/^/, "<p>") + "</p>";
}

function formatDates(t) {
  if (t.dates_low == null && t.dates_high == null) return "";
  const fmt = (y) => y < 0 ? `${-y} BCE` : `${y}`;
  if (t.dates_low === t.dates_high) return fmt(t.dates_low);
  return `${fmt(t.dates_low)}–${fmt(t.dates_high)}`;
}
function formatDatesLong(t) {
  if (t.dates_low == null) return "";
  const lo = t.dates_low, hi = t.dates_high;
  const fmt = (y) => y < 0 ? `${-y} BCE` : `${y} CE`;
  return lo === hi ? fmt(lo) : `${fmt(lo)} – ${fmt(hi)}`;
}

function showEmptyState(msg) {
  detailContent.innerHTML = `<h2>Setting up</h2><p>${escape(msg)}</p>`;
  document.body.classList.add("is-detail-open");
}

// ---------- reading mode -----------
function setReadingMode(on) {
  document.body.classList.toggle("is-reading-mode", on);
  // Update only the .btn-text span; preserve the icon SVG.
  const txt = readingModeBtn.querySelector(".btn-text");
  const label = on ? "Back to timeline" : "Reading";
  if (txt) txt.textContent = label;
  else readingModeBtn.textContent = label;
  readingModeBtn.setAttribute("aria-label", on ? "Back to timeline" : "Reading mode");
  readingModeBtn.classList.toggle("is-active", on);
  if (on && !state.activeId && state.thinkers.length) {
    const sorted = [...state.thinkers].sort((a, b) => (a.dates_low + a.dates_high)/2 - (b.dates_low + b.dates_high)/2);
    openThinker(sorted[0].id);
  }
}
readingModeBtn.addEventListener("click", () => {
  const on = !document.body.classList.contains("is-reading-mode");
  setReadingMode(on);
});

// ---------- view toggle (Lanes / Network) -----------
function wireViewToggle() {
  document.querySelectorAll(".view-toggle-btn").forEach((b) => {
    const on = b.dataset.view === state.viewMode;
    b.classList.toggle("is-active", on);
    b.setAttribute("aria-selected", on ? "true" : "false");
    b.addEventListener("click", () => setViewMode(b.dataset.view));
  });
}

// ---------- network legend (school-color key, only in network view) -----------
const networkLegendEl = document.getElementById("networkLegend");
const networkLegendListEl = document.getElementById("networkLegendList");
const networkLegendToggleEl = document.getElementById("networkLegendToggle");

function renderNetworkLegend() {
  if (!networkLegendEl) return;
  if (state.viewMode !== "network") {
    networkLegendEl.hidden = true;
    networkLegendEl.setAttribute("aria-hidden", "true");
    return;
  }
  networkLegendEl.hidden = false;
  networkLegendEl.setAttribute("aria-hidden", "false");

  // Build legend from schools that actually have visible thinkers.
  const present = new Set();
  for (const t of state.thinkers) {
    if (!isThinkerVisible(t)) continue;
    present.add(t.school_color_token || "proto");
  }
  // Stable order: Vedānta first (in LANE_ORDER), then comparators.
  const ordered = LANE_ORDER.filter((tok) => present.has(tok));

  networkLegendListEl.innerHTML = "";
  for (const tok of ordered) {
    const li = document.createElement("li");
    const color = state.schools[tok]?.color_palette?.[2]
               || state.schools[tok]?.color_hex
               || colorFor({ school_color_token: tok }, 2);
    const label = state.schools[tok]?.display_name || LANE_DISPLAY[tok] || tok;
    li.innerHTML = `<span class="swatch" style="background:${color}"></span><span>${escape(label)}</span>`;
    networkLegendListEl.appendChild(li);
  }
}

if (networkLegendToggleEl) {
  networkLegendToggleEl.addEventListener("click", () => {
    const open = networkLegendEl.classList.toggle("is-open");
    networkLegendToggleEl.setAttribute("aria-expanded", open ? "true" : "false");
  });
}

// ---------- filter drawer (school visibility) -----------
const filterBtn = document.getElementById("filterBtn");
const filterDrawer = document.getElementById("filterDrawer");
const filterChipsEl = document.getElementById("filterChips");

function renderFilterChips() {
  if (!filterChipsEl) return;
  filterChipsEl.innerHTML = "";

  // Preset row.
  const presets = document.createElement("div");
  presets.className = "filter-chip-row";
  presets.innerHTML = `
    <button class="filter-chip filter-chip--preset" data-preset="vedanta">Vedānta only</button>
    <button class="filter-chip filter-chip--preset" data-preset="all">All schools</button>
    <button class="filter-chip filter-chip--preset" data-preset="comparators">Comparators only</button>
  `;
  filterChipsEl.appendChild(presets);

  // Per-school chips.
  const chipsRow = document.createElement("div");
  chipsRow.className = "filter-chip-row";
  const makeChip = (key, label, color) => {
    const on = state.visibleLanes.has(key);
    const btn = document.createElement("button");
    btn.className = "filter-chip" + (on ? " is-on" : "");
    btn.dataset.lane = key;
    btn.style.setProperty("--chip-color", color);
    btn.innerHTML = `<span class="chip-swatch"></span>${escape(label)}`;
    btn.addEventListener("click", () => {
      if (state.visibleLanes.has(key)) state.visibleLanes.delete(key);
      else state.visibleLanes.add(key);
      rerender();
    });
    return btn;
  };
  for (const tok of LANE_ORDER) {
    if (!VEDANTA_LANES.has(tok)) continue;
    const label = state.schools[tok]?.display_name || LANE_DISPLAY[tok] || tok;
    const color = state.schools[tok]?.color_palette?.[2] || colorFor({ school_color_token: tok }, 2);
    chipsRow.appendChild(makeChip(tok, label, color));
  }
  chipsRow.appendChild(makeChip(COMPARATOR_GROUP_KEY, COMPARATOR_GROUP_LABEL, "#475569"));
  filterChipsEl.appendChild(chipsRow);

  // Wire presets.
  filterChipsEl.querySelectorAll("[data-preset]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const p = btn.dataset.preset;
      state.visibleLanes.clear();
      if (p === "vedanta") {
        for (const t of VEDANTA_LANES) state.visibleLanes.add(t);
      } else if (p === "comparators") {
        state.visibleLanes.add(COMPARATOR_GROUP_KEY);
        state.comparatorExpanded = true;
      } else {
        for (const t of VEDANTA_LANES) state.visibleLanes.add(t);
        state.visibleLanes.add(COMPARATOR_GROUP_KEY);
      }
      rerender();
    });
  });
}

if (filterBtn) {
  filterBtn.addEventListener("click", () => {
    const open = filterDrawer.classList.toggle("is-open");
    filterDrawer.setAttribute("aria-hidden", open ? "false" : "true");
    filterBtn.classList.toggle("is-active", open);
  });
  // Close drawer on outside click.
  document.addEventListener("click", (e) => {
    if (!filterDrawer.classList.contains("is-open")) return;
    if (filterDrawer.contains(e.target) || filterBtn.contains(e.target)) return;
    filterDrawer.classList.remove("is-open");
    filterDrawer.setAttribute("aria-hidden", "true");
    filterBtn.classList.remove("is-active");
  });
}

// ---------- about modal -----------
const aboutBtn = document.getElementById("aboutBtn");
const aboutModal = document.getElementById("aboutModal");
const closeAbout = document.getElementById("closeAbout");
aboutBtn.addEventListener("click", () => { aboutModal.classList.add("is-open"); aboutModal.setAttribute("aria-hidden", "false"); });
closeAbout.addEventListener("click", () => { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); });
aboutModal.addEventListener("click", (e) => {
  if (e.target === aboutModal) { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); }
});

// ---------- articles -----------
const articlesBtn = document.getElementById("articlesBtn");
const articlesModal = document.getElementById("articlesModal");
const closeArticles = document.getElementById("closeArticles");
const articlesList = document.getElementById("articlesList");
const articleReader = document.getElementById("articleReader");
const articleReaderTitle = document.getElementById("articleReaderTitle");
const articleReaderContent = document.getElementById("articleReaderContent");
const closeArticleReader = document.getElementById("closeArticleReader");
const backToArticles = document.getElementById("backToArticles");

let articlesManifest = null;

async function ensureArticlesLoaded() {
  if (articlesManifest) return;
  articlesManifest = await loadJSON("data/articles/manifest.json");
  if (!articlesManifest || !articlesManifest.articles) {
    articlesList.innerHTML = "<p class=\"articles-intro\">No articles yet.</p>";
    return;
  }
  articlesList.innerHTML = "";
  for (const a of articlesManifest.articles) {
    const row = document.createElement("div");
    row.className = "article-row";
    row.dataset.slug = a.slug;
    row.innerHTML = `
      <p class="article-title">${escape(a.title)}${a.status === "in-progress" ? ' <em style="color:#92400e;font-weight:500">(in progress)</em>' : ""}</p>
      <p class="article-subtitle">${md(a.subtitle || "")}</p>
      <p class="article-meta">${escape(a.kind || "")} · ~${a.word_count_approx || "?"} words${a.date ? " · " + escape(a.date) : ""}</p>
    `;
    row.addEventListener("click", () => openArticle(a));
    articlesList.appendChild(row);
  }
}

articlesBtn.addEventListener("click", async () => {
  await ensureArticlesLoaded();
  articlesModal.classList.add("is-open");
  articlesModal.setAttribute("aria-hidden", "false");
});
closeArticles.addEventListener("click", () => { articlesModal.classList.remove("is-open"); articlesModal.setAttribute("aria-hidden", "true"); });
articlesModal.addEventListener("click", (e) => {
  if (e.target === articlesModal) { articlesModal.classList.remove("is-open"); articlesModal.setAttribute("aria-hidden", "true"); }
});

async function openArticle(a) {
  articlesModal.classList.remove("is-open");
  articleReader.classList.add("is-open");
  articleReader.setAttribute("aria-hidden", "false");
  articleReaderTitle.textContent = a.title;
  articleReaderContent.innerHTML = "<article><p>Loading…</p></article>";
  // Articles live at data/articles/source/<slug>.md
  const r = await fetch(`data/articles/source/${a.slug}.md`);
  if (!r.ok) {
    articleReaderContent.innerHTML = `<article><h1>${escape(a.title)}</h1><p>Article body not yet uploaded.</p></article>`;
    return;
  }
  const text = await r.text();
  articleReaderContent.innerHTML = `<article>${renderMarkdownFull(text)}</article>`;
  articleReaderContent.scrollTop = 0;
}

closeArticleReader.addEventListener("click", () => {
  articleReader.classList.remove("is-open");
  articleReader.setAttribute("aria-hidden", "true");
});
backToArticles.addEventListener("click", () => {
  articleReader.classList.remove("is-open");
  articleReader.setAttribute("aria-hidden", "true");
  articlesModal.classList.add("is-open");
  articlesModal.setAttribute("aria-hidden", "false");
});

// Slightly richer markdown renderer for articles (handles tables, blockquotes, lists).
function renderMarkdownFull(src) {
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  // Pull out fenced code blocks first (preserve verbatim)
  const blocks = [];
  src = src.replace(/```([\s\S]*?)```/g, (_, body) => {
    blocks.push(`<pre><code>${esc(body)}</code></pre>`);
    return ` BLOCK${blocks.length-1} `;
  });
  // Tables (simple GFM)
  src = src.replace(/((?:^\|.*\|\s*\n)+)/gm, (m) => {
    const rows = m.trim().split("\n").map((r) => r.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
    if (rows.length < 2) return m;
    const hasSep = rows[1].every((c) => /^:?-+:?$/.test(c));
    if (!hasSep) return m;
    const head = rows[0];
    const body = rows.slice(2);
    return `<table><thead><tr>${head.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${body.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
  });
  // Standard markdown
  let out = src
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    .replace(/^&gt; (.+)$/gm, "<blockquote>$1</blockquote>")
    .replace(/^> (.+)$/gm, "<blockquote>$1</blockquote>")
    .replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>")
    .replace(/`([^`]+?)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    // paragraph splits
    .replace(/\n\n+/g, "</p><p>");
  out = "<p>" + out + "</p>";
  // restore code blocks
  out = out.replace(/ BLOCK(\d+) /g, (_, i) => blocks[+i]);
  // Don't wrap headings/blockquotes/tables in <p>
  out = out.replace(/<p>(\s*)(<h[123]|<blockquote|<table|<pre|<ul|<ol)/g, "$1$2");
  out = out.replace(/(<\/h[123]>|<\/blockquote>|<\/table>|<\/pre>|<\/ul>|<\/ol>)(\s*)<\/p>/g, "$1$2");
  return out;
}

// ---------- keyboard nav -----------
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (articleReader.classList.contains("is-open")) {
      articleReader.classList.remove("is-open");
      articleReader.setAttribute("aria-hidden", "true");
    } else if (articlesModal.classList.contains("is-open")) {
      articlesModal.classList.remove("is-open");
      articlesModal.setAttribute("aria-hidden", "true");
    } else if (aboutModal.classList.contains("is-open")) {
      aboutModal.classList.remove("is-open");
      aboutModal.setAttribute("aria-hidden", "true");
    } else if (readerModal.classList.contains("is-open")) {
      readerModal.classList.remove("is-open");
      readerModal.setAttribute("aria-hidden", "true");
    } else if (document.body.classList.contains("is-reading-mode")) {
      setReadingMode(false);
    } else {
      closeDetailPane();
    }
    return;
  }
  if (e.key === "r" && !e.metaKey && !e.ctrlKey && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
    setReadingMode(!document.body.classList.contains("is-reading-mode"));
    return;
  }
  if ((e.key === "ArrowLeft" || e.key === "ArrowRight") && state.activeId) {
    e.preventDefault();
    navigateByDate(e.key === "ArrowRight" ? 1 : -1);
  }
});

function navigateByDate(dir) {
  const sorted = [...state.thinkers].sort((a, b) => (a.dates_low + a.dates_high)/2 - (b.dates_low + b.dates_high)/2);
  const idx = sorted.findIndex((t) => t.id === state.activeId);
  if (idx < 0) return;
  const next = sorted[idx + dir];
  if (next) openThinker(next.id);
}

// ---------- responsive: re-render on viewport breakpoint changes -----------
let _lastLaneH = LANE_H;
let _lastRailW = LANE_RAIL_W;
let _resizeTimer = null;
window.addEventListener("resize", () => {
  clearTimeout(_resizeTimer);
  _resizeTimer = setTimeout(() => {
    refreshLayoutConstants();
    if (LANE_H !== _lastLaneH || LANE_RAIL_W !== _lastRailW) {
      _lastLaneH = LANE_H;
      _lastRailW = LANE_RAIL_W;
      renderAll();
    }
  }, 120);
});

// ---------- boot -----------
loadAll().then(() => {
  refreshLayoutConstants();
  _lastLaneH = LANE_H;
  _lastRailW = LANE_RAIL_W;
  wirePanZoom();
  wireViewToggle();
});
