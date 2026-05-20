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
  "dvaita": "Tattva-vāda",
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
  "dvaita": "Tattva-vāda",
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

// One canonical color per historical period. Used by both views:
//   • the lanes view era-band overlay (full vertical stripes)
//   • the network view era-band overlay (same SVG renderer)
//   • the era-strip labels at the top (text tinted to its period color)
// Anything tagged with these era names must use the same `fill` everywhere.
// Modern caps at 2050 (current year + buffer for living thinkers); the
// chronology axis never extends past this point.
const ERA_BANDS = [
  { name: "Pre-Śaṅkara",  low: -800, high:  700, fill: "#a8a29e", fillOpacity: 0.10 },
  { name: "Classical",    low:  700, high: 1100, fill: "#94a3b8", fillOpacity: 0.12 },
  { name: "Late-Medieval",low: 1100, high: 1500, fill: "#d97706", fillOpacity: 0.08 },
  { name: "Early-Modern", low: 1500, high: 1800, fill: "#9333ea", fillOpacity: 0.07 },
  { name: "Modern",       low: 1800, high: 2050, fill: "#0891b2", fillOpacity: 0.08 },
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
// Unified panel: dp-* ids point at the five tab panes; the legacy
// readerModal / articleReader DOM nodes were removed when those flows
// migrated into the panel as tabs.
const dpTabBar = detailPane && detailPane.querySelector(".dp-tabbar");
const dpTranslationHead = document.getElementById("dpTranslationHead");
const dpTranslationBody = document.getElementById("dpTranslationBody");
const dpArticleHead = document.getElementById("dpArticleHead");
const dpArticleBody = document.getElementById("dpArticleBody");
const dpCitationBody = document.getElementById("dpCitationBody");
const dpSourceSearch = document.getElementById("dpSourceSearch");
const dpSourceTree = document.getElementById("dpSourceTree");
const dpSourceViewer = document.getElementById("dpSourceViewer");
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
  primitiveGraph: null,
  comparativeClaims: [],
  glossary: new Map(),       // term-key → entry
  glossaryRegex: null,
  citationIndex: null,       // {entries: {key: passage}, aliases: {key: targetKey}}
  range: { low: -800, high: 2050 },
  pxPerYear: PX_PER_YEAR_DEFAULT,
  layout: new Map(),         // id → {x, y, lane, shade, subRow, tier, barX1, barX2}
  clusters: [],              // [{ids: [...]}] groups of 3+ dots tight in x within a lane
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

async function loadPrimitiveGraph() {
  if (state.primitiveGraph) return state.primitiveGraph;
  state.primitiveGraph = await loadJSON("data/registries/primitive_graph.json");
  try { window.__primitiveGraph = state.primitiveGraph; } catch (_) {}
  return state.primitiveGraph;
}

async function loadThinkerById(thinkerId) {
  if (!thinkerId) return null;
  if (state.thinkersById.has(thinkerId)) return state.thinkersById.get(thinkerId);
  const thinker = await loadJSON(`data/thinkers/${thinkerId}.json`);
  if (thinker) state.thinkersById.set(thinkerId, thinker);
  return thinker;
}

async function getPrimitiveCommitments(thinkerId) {
  const thinker = await loadThinkerById(thinkerId);
  return Array.isArray(thinker?.primitive_commitments) ? thinker.primitive_commitments : [];
}

async function getCrossEngagements(thinkerId) {
  const thinker = await loadThinkerById(thinkerId);
  return Array.isArray(thinker?.cross_engagements) ? thinker.cross_engagements : [];
}

async function loadAll() {
  const manifest = await loadJSON("data/manifest.json");
  if (!manifest) {
    showEmptyState("No data yet — corpus pipeline is still populating.");
    return;
  }
  state.schools     = (await loadJSON("data/registries/schools.json"))     || {};
  state.subSchools  = (await loadJSON("data/registries/sub_schools.json")) || {};
  await loadPrimitiveGraph();

  const thinkers = await Promise.all(
    (manifest.thinkers || []).map((f) => loadJSON(`data/thinkers/${f}`))
  );
  state.thinkers = thinkers.filter(Boolean);
  state.thinkers.forEach((t) => state.thinkersById.set(t.id, t));

  // Set of "<thinker_id>__<work_id>" identifiers for which a full translation
  // markdown lives on disk under data/full_translations/. Used by
  // renderWorkCard to choose between full-translation framing and
  // "engaged passages (full work pending)" framing. Falls back to empty.
  state.fullTranslationSet = new Set();
  try {
    const ftIdx = await loadJSON("data/full_translations/index.json");
    if (ftIdx && Array.isArray(ftIdx.files)) {
      for (const fname of ftIdx.files) {
        state.fullTranslationSet.add(String(fname).replace(/\.md$/, ""));
      }
    }
  } catch (_) {}

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

  // Perspectives layer (interpretive readings, flagged as such) — load early so the
  // detail pane's Perspectives section is available on the first thinker open.
  ensurePerspectivesLoaded();

  // Citation index (clickable primary-source citations). Loaded eagerly so the
  // first click on a cite-link returns instantly; fallback handler lazy-loads
  // it if absent.
  loadCitationIndex();

  computeRange();
  computeRenderLanes();
  computeLayout();
  renderAll();
  renderFilterChips();
  updateSubtitle();
  scrollToInitialFocus();
}

try {
  window.loadPrimitiveGraph = loadPrimitiveGraph;
  window.getPrimitiveCommitments = getPrimitiveCommitments;
  window.getCrossEngagements = getCrossEngagements;
} catch (_) {}

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

// Hard upper bound on the chronology axis. Modern era caps at 2050 by
// convention (current year + ~25-year buffer for living thinkers). The
// auto-fit pass below clamps to this so a single 2050-dated thinker can't
// push the axis out to 2100.
const RANGE_HIGH_MAX = 2050;

function computeRange() {
  if (!state.thinkers.length) return;
  let lo = Infinity, hi = -Infinity;
  for (const t of state.thinkers) {
    if (typeof t.dates_low === "number") lo = Math.min(lo, t.dates_low);
    if (typeof t.dates_high === "number") hi = Math.max(hi, t.dates_high);
  }
  state.range.low = Math.floor(lo / 50) * 50 - 50;
  // Snap to the next 50-year tick above hi, then clamp to RANGE_HIGH_MAX.
  const snapped = Math.ceil(hi / 50) * 50 + 50;
  state.range.high = Math.min(snapped, RANGE_HIGH_MAX);
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

// Within-lane sub-row assignment + x-jitter fallback.
//
// Each lane is divided into N vertical micro-rows. A thinker's preferred row
// comes from its hand-tuned `sub_school_shade` (1..5 → rows around center).
// If that row is already occupied at this x, we walk outward in alternating
// up/down steps until we find a row whose nearest neighbor on that row sits
// at least MIN_X_GAP away.
//
// When the half-lane is exhausted (every available row is occupied at this x),
// we fall back to **x-jitter**: shift the dot horizontally by a small offset
// so it gets its own clickable column even within the most occupied row.
// This guarantees every dot is independently clickable even in the densest
// historical periods (e.g. advaita ~1910s, dvaita ~1280s).
//
// Output: the layout map stores y, lane, and the assigned sub-row. A second
// pass detects residual tight clusters (>= 2 dots with very close x within
// the same lane); the renderer offers hover-fan expansion for those.
const SUB_ROW_STEP_DESKTOP = 12;
const SUB_ROW_STEP_MOBILE = 10;
const MIN_X_GAP = 26;          // ~ tier-1 dot diameter + generous breathing room
const X_JITTER_STEP = 14;      // horizontal nudge when all rows are full
const CLUSTER_X_THRESHOLD = 18;
const CLUSTER_MIN_MEMBERS = 2;

function computeLanesLayout() {
  state.layout.clear();
  state.clusters = [];

  // Bucket visible thinkers by lane index.
  const byLane = new Map();
  for (const t of state.thinkers) {
    if (!isThinkerVisible(t)) continue;
    const lane = laneIndex(t.school_color_token);
    if (lane < 0) continue;
    const xMid = yearToX((t.dates_low + t.dates_high) / 2);
    const x1 = yearToX(t.dates_low);
    const x2 = yearToX(t.dates_high);
    const entry = {
      t, xMid, x1, x2,
      tier: tierOf(t),
      prefShade: shadeFor(t),
    };
    const arr = byLane.get(lane) || [];
    arr.push(entry);
    byLane.set(lane, arr);
  }

  const stepPx = LANE_H <= 72 ? SUB_ROW_STEP_MOBILE : SUB_ROW_STEP_DESKTOP;
  // Use the full half-lane down to ~4 px from the rule, since the visible dot
  // is small and labels float outside the lane band anyway.
  const MAX_OFFSET_STEPS = Math.max(3, Math.floor((LANE_H / 2 - 4) / stepPx));

  for (const [lane, items] of byLane) {
    items.sort((a, b) => a.xMid - b.xMid);

    // occupancy[rowIdx] = last placed dot's effective x for that row.
    const occupancy = new Map();

    items.forEach((item, idx) => {
      // Preferred row from sub_school_shade (1..5 → -2..+2).
      const prefRow = (item.prefShade || 3) - 3;

      // Walk outward from the preferred row, alternating up/down so adjacent
      // contemporaries fan symmetrically. Place into the first row that has
      // enough horizontal clearance from its last occupant.
      let chosen = prefRow;
      let found = false;
      for (let step = 0; step <= MAX_OFFSET_STEPS * 2 && !found; step++) {
        const candidates = step === 0
          ? [prefRow]
          : [prefRow + step, prefRow - step];
        for (const r of candidates) {
          if (Math.abs(r) > MAX_OFFSET_STEPS) continue;
          const last = occupancy.get(r);
          if (last === undefined || (item.xMid - last) >= MIN_X_GAP) {
            chosen = r;
            found = true;
            break;
          }
        }
      }

      // Fallback: every row is full at this x. Pick the row with the most
      // distant last-occupant and shift this dot horizontally by enough to
      // clear MIN_X_GAP. Alternate left/right per item so the fan is symmetric.
      let xShift = 0;
      if (!found) {
        let bestRow = prefRow;
        let bestDist = -Infinity;
        for (let r = -MAX_OFFSET_STEPS; r <= MAX_OFFSET_STEPS; r++) {
          const last = occupancy.get(r);
          const dist = last === undefined ? Infinity : (item.xMid - last);
          if (dist > bestDist) { bestDist = dist; bestRow = r; }
        }
        chosen = bestRow;
        const dir = (idx % 2 === 0) ? +1 : -1;
        xShift = dir * X_JITTER_STEP;
      }

      const effX = item.xMid + xShift;
      occupancy.set(chosen, effX);

      const y = lane * LANE_H + LANE_H / 2 + chosen * stepPx;

      state.layout.set(item.t.id, {
        thinker: item.t,
        x: effX,
        xRaw: item.xMid,
        y,
        lane,
        shade: item.prefShade,
        subRow: chosen,
        tier: item.tier,
        barX1: item.x1,
        barX2: item.x2,
      });
    });
  }

  // Detect residual tight clusters. Even with sub-rows + x-jitter, dots whose
  // visible centers land within CLUSTER_X_THRESHOLD of each other in the same
  // lane get a hover-fan affordance so each is individually clickable.
  // Clusters now include 2-member pairs (not just 3+) so even adjacent
  // contemporaries that the renderer placed close get the fan-out treatment.
  for (const [lane, items] of byLane) {
    if (items.length < CLUSTER_MIN_MEMBERS) continue;
    // Build cluster sets based on effective layout x (after jitter), grouping
    // any pair within CLUSTER_X_THRESHOLD that also shares a lane.
    const placed = items
      .map((it) => state.layout.get(it.t.id))
      .filter(Boolean)
      .sort((a, b) => a.x - b.x);
    let i = 0;
    while (i < placed.length) {
      const groupIds = [placed[i].thinker.id];
      let j = i + 1;
      while (j < placed.length && (placed[j].x - placed[j - 1].x) < CLUSTER_X_THRESHOLD) {
        groupIds.push(placed[j].thinker.id);
        j++;
      }
      if (groupIds.length >= CLUSTER_MIN_MEMBERS) {
        state.clusters.push({ ids: groupIds, lane });
      }
      i = Math.max(j, i + 1);
    }
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
    // Tint each label with its canonical period color so lanes-view and
    // network-view share the same color-vocabulary for periods.
    el.style.color = era.fill;
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

  // Map each thinker id to its cluster index (if any). Only used in lanes view —
  // network view does its own free-form placement and rarely produces stacks.
  const clusterOf = new Map();
  const denseClusters = new Set();  // clusters with 3+ members get the stack marker
  if (state.viewMode === "lanes" && Array.isArray(state.clusters)) {
    state.clusters.forEach((c, idx) => {
      for (const id of c.ids) clusterOf.set(id, idx);
      if (c.ids.length >= 3) denseClusters.add(idx);
    });
  }

  // For label collision, place above by default; collect bands of placed labels.
  const placedAbove = [];
  const placedBelow = [];
  for (const [, p] of state.layout) {
    const t = p.thinker;
    const labelW = (t.name || t.id).length * 6 + 14;
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
    const cIdx = clusterOf.get(t.id);
    if (cIdx !== undefined) {
      dot.dataset.cluster = String(cIdx);
      if (denseClusters.has(cIdx)) dot.classList.add("thinker-dot--in-cluster");
    }
    dot.style.left = p.x + "px";
    dot.style.top = p.y + "px";
    dot.style.setProperty("--dot-color", colorFor(t, 2));
    dot.setAttribute("tabindex", "0");
    dot.setAttribute("role", "button");
    dot.setAttribute("aria-label", t.name_iast || t.name || t.id);
    dot.innerHTML = `
      <div class="node"></div>
      <button type="button" class="label" tabindex="-1" aria-label="${escape(t.name_iast || t.name || t.id)}">
        <span class="name">${escape(t.name || t.id)}</span>
        <span class="dates">${formatDates(t)}</span>
      </button>
    `;
    dot.addEventListener("click", (e) => { e.stopPropagation(); openThinker(t.id); });
    // Label is a real button so a tap/click on the name tag opens the thinker.
    // We still stop propagation to keep the surrounding canvas drag handler
    // from interpreting label clicks as a pan-start.
    const labelBtn = dot.querySelector(".label");
    if (labelBtn) {
      labelBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        e.preventDefault();
        openThinker(t.id);
      });
    }
    dot.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openThinker(t.id); }
    });
    dot.addEventListener("mouseenter", () => onDotHover(t.id, true));
    dot.addEventListener("mouseleave", () => onDotHover(t.id, false));
    dotsLayer.appendChild(dot);
  }

  // Cluster hover-fan: on hovering any dot belonging to a cluster, fan the
  // whole cluster horizontally (alternating ± offsets from the cluster
  // centroid) so each member is independently clickable. Plays on top of
  // the greedy sub-row layout — most clusters disappear there, this is a
  // safety net for the densest periods.
  state.clusters.forEach((c, idx) => {
    if (c.ids.length < 2) return;
    const members = c.ids
      .map((id) => ({ id, el: dotsLayer.querySelector(`.thinker-dot[data-id="${CSS.escape(id)}"]`) }))
      .filter((m) => m.el);
    if (members.length < 2) return;
    const fanStep = 24;  // px between fanned dots — generous enough to clear labels
    const centerIdx = (members.length - 1) / 2;
    const enter = () => {
      dotsLayer.classList.add("has-cluster-fan");
      members.forEach((m, i) => {
        const dx = (i - centerIdx) * fanStep;
        m.el.classList.add("is-fanned");
        m.el.style.setProperty("--fan-dx", dx + "px");
      });
    };
    const leave = () => {
      members.forEach((m) => {
        m.el.classList.remove("is-fanned");
        m.el.style.removeProperty("--fan-dx");
      });
      dotsLayer.classList.remove("has-cluster-fan");
    };
    members.forEach((m) => {
      m.el.addEventListener("mouseenter", enter);
      m.el.addEventListener("mouseleave", (e) => {
        // Only collapse when the cursor truly leaves all cluster members.
        const to = e.relatedTarget;
        if (to && members.some((mm) => mm.el === to || mm.el.contains(to))) return;
        leave();
      });
      m.el.addEventListener("focus", enter);
      m.el.addEventListener("blur", (e) => {
        const to = e.relatedTarget;
        if (to && members.some((mm) => mm.el === to || mm.el.contains(to))) return;
        leave();
      });
    });
  });
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
  ensureResetViewButton();
}

// Recompute lane order + filter and re-render. Preserves scroll position
// in BOTH axes so toggling a chip or expanding the comparator group never
// makes the user feel the viewport shifted under them — the chronology
// axis and the visible thinkers stay where the user was looking.
function rerender() {
  const prevLeft = scroller.scrollLeft;
  const prevTop = scroller.scrollTop;
  renderAll();
  scroller.scrollLeft = prevLeft;
  scroller.scrollTop = prevTop;
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

  // wheel: vertical wheel pans Y; shift+wheel pans X; ctrl+wheel zooms.
  //
  // Smooth-zoom strategy (desktop + trackpad pinch):
  //   1. During an active zoom gesture, apply a GPU-accelerated CSS
  //      transform (translateX + scaleX) to `.canvas`. No layout recompute,
  //      no DOM teardown — just a compositor matrix update. Coalesced into
  //      requestAnimationFrame so wheel bursts (60-120/s) collapse to one
  //      paint per frame.
  //   2. When wheel events stop (~140 ms idle), "commit": fold the visual
  //      scale into state.pxPerYear, reset the transform, run the full
  //      computeLayout()+renderAll() once, and adjust scrollLeft so the
  //      year that was under the cursor stays under the cursor.
  //
  // This collapses dozens of full re-renders into one, while giving
  // immediate (60 fps) visual feedback on every wheel tick.
  let zoomActive = false;
  let zoomStartPpy = 0;
  let zoomVisualSx = 1;       // accumulated scale since zoom-start
  let zoomTx = 0;             // accumulated translateX in screen px
  let zoomScrollLeft = 0;     // scroller.scrollLeft frozen at zoom-start
  let zoomRailOffset = 0;     // canvas natural left within scroller content
  let zoomScrollerLeft = 0;   // scroller.getBoundingClientRect().left
  let zoomLastCursorX = 0;    // last clientX (for commit anchor)
  let zoomRafPending = false;
  let zoomEndTimer = 0;
  let zoomPendingFactor = 1;
  let zoomPendingCursorX = 0;
  // Re-applies the transform on the next animation frame. Multiple wheel
  // events within the same frame are coalesced into one matrix update.
  function scheduleZoomFrame() {
    if (zoomRafPending) return;
    zoomRafPending = true;
    requestAnimationFrame(() => {
      zoomRafPending = false;
      // Resolve cx under cursor in canvas coords using the CURRENT transform,
      // then apply pendingFactor about that anchor.
      const screenBase = zoomScrollerLeft - zoomScrollLeft + zoomRailOffset;
      const cursorScreenX = zoomPendingCursorX;
      const cxAnchor = (cursorScreenX - screenBase - zoomTx) / zoomVisualSx;
      const factor = zoomPendingFactor;
      zoomPendingFactor = 1;
      let newSx = zoomVisualSx * factor;
      // Clamp visual scale so it can't exceed effective pxPerYear bounds.
      const minSx = 0.6 / zoomStartPpy;
      const maxSx = 6 / zoomStartPpy;
      newSx = Math.max(minSx, Math.min(maxSx, newSx));
      if (newSx === zoomVisualSx) return;
      const newTx = cursorScreenX - screenBase - cxAnchor * newSx;
      zoomVisualSx = newSx;
      zoomTx = newTx;
      canvas.style.transform = `translateX(${newTx}px) scaleX(${newSx})`;
    });
  }
  // Folds the visual scale into pxPerYear, re-runs layout, restores scroll.
  function commitZoom() {
    if (zoomEndTimer) { clearTimeout(zoomEndTimer); zoomEndTimer = 0; }
    if (!zoomActive) return;
    const newPpy = Math.max(0.6, Math.min(6, zoomStartPpy * zoomVisualSx));
    // Compute the year that's currently under the cursor (in pre-commit coords).
    const screenBase = zoomScrollerLeft - zoomScrollLeft + zoomRailOffset;
    const cxAnchor = (zoomLastCursorX - screenBase - zoomTx) / zoomVisualSx;
    const yearAtCursor = state.range.low + (cxAnchor - PAD_LEFT) / zoomStartPpy;
    // Reset transform first so subsequent layout/render writes are crisp.
    canvas.style.transform = "";
    canvas.style.transformOrigin = "";
    canvas.style.willChange = "";
    zoomActive = false;
    if (newPpy !== state.pxPerYear) {
      state.pxPerYear = newPpy;
      computeLayout();
      renderAll();
    }
    // Restore scrollLeft so the same year stays under the cursor.
    const newCx = PAD_LEFT + (yearAtCursor - state.range.low) * state.pxPerYear;
    scroller.scrollLeft = newCx + zoomRailOffset - (zoomLastCursorX - zoomScrollerLeft);
    zoomVisualSx = 1;
    zoomTx = 0;
  }
  function startZoom(e) {
    zoomActive = true;
    zoomStartPpy = state.pxPerYear;
    zoomVisualSx = 1;
    zoomTx = 0;
    zoomScrollLeft = scroller.scrollLeft;
    const rect = scroller.getBoundingClientRect();
    zoomScrollerLeft = rect.left;
    zoomRailOffset = state.viewMode === "network" ? 0 : LANE_RAIL_W;
    canvas.style.transformOrigin = "0 0";
    canvas.style.willChange = "transform";
  }

  scroller.addEventListener("wheel", (e) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      // Normalize delta. deltaMode=1 (LINE) → multiply; deltaMode=0 (PIXEL,
      // trackpad pinch) → use raw px. Clamp to keep one tick gentle.
      const rawDelta = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
      const clampedDelta = Math.max(-50, Math.min(50, rawDelta));
      // Sensitivity matches the previous gesture: factor ≈ exp(-delta*0.0018).
      const factor = Math.exp(-clampedDelta * 0.0018);
      if (!zoomActive) startZoom(e);
      // Re-snapshot scroller scrollLeft. If the user vertical-scrolled
      // between zoom events (non-ctrl wheel may have native scroll), keep
      // the visual transform consistent by compensating tx for the shift.
      const newScrollLeft = scroller.scrollLeft;
      if (newScrollLeft !== zoomScrollLeft) {
        zoomTx += (newScrollLeft - zoomScrollLeft);
        zoomScrollLeft = newScrollLeft;
      }
      // Accumulate factor and cursor so the rAF callback handles the latest.
      zoomPendingFactor *= factor;
      zoomPendingCursorX = e.clientX;
      zoomLastCursorX = e.clientX;
      scheduleZoomFrame();
      // Reset the idle timer; commit only after the wheel burst ends.
      if (zoomEndTimer) clearTimeout(zoomEndTimer);
      zoomEndTimer = setTimeout(commitZoom, 140);
    } else if (e.shiftKey) {
      e.preventDefault();
      scroller.scrollLeft += e.deltaY;
    }
    // otherwise: native vertical scroll behavior
  }, { passive: false });

  // Safari-only pinch gestures (iOS + macOS Safari fire `gesture*` events
  // for trackpad/touch pinches in addition to wheel). Mirror the wheel
  // codepath so pinch produces the same smooth visual scale + commit
  // behaviour. Chrome / Firefox fall back to the touchmove pinch below.
  let gestureStartScale = 1;
  scroller.addEventListener("gesturestart", (e) => {
    e.preventDefault();
    gestureStartScale = e.scale || 1;
    if (!zoomActive) startZoom(e);
    zoomPendingCursorX = e.clientX || (window.innerWidth / 2);
    zoomLastCursorX = zoomPendingCursorX;
  });
  scroller.addEventListener("gesturechange", (e) => {
    e.preventDefault();
    if (!zoomActive) startZoom(e);
    // Convert absolute gesture scale into a multiplicative factor relative
    // to the last gesturechange. Without this the zoom would re-apply the
    // full pinch each frame and runaway.
    const cur = e.scale || 1;
    const factor = cur / gestureStartScale;
    gestureStartScale = cur;
    zoomPendingFactor *= factor;
    zoomPendingCursorX = e.clientX || zoomPendingCursorX;
    zoomLastCursorX = zoomPendingCursorX;
    scheduleZoomFrame();
    if (zoomEndTimer) clearTimeout(zoomEndTimer);
    zoomEndTimer = setTimeout(commitZoom, 140);
  });
  scroller.addEventListener("gestureend", (e) => {
    e.preventDefault();
    commitZoom();
  });

  // Two-finger touch pinch for non-Safari mobile (Chrome/Firefox on
  // Android). Tracks the distance between the two pointers; the ratio
  // since the last move becomes the zoom factor. Pan-while-pinching is
  // intentionally NOT supported here — the existing drag handler covers
  // single-touch pan, and a hybrid behaviour would fight Safari's
  // built-in gesture handling.
  const activeTouches = new Map();
  let pinchPrevDist = 0;
  function touchPairDist() {
    const arr = [...activeTouches.values()];
    if (arr.length < 2) return 0;
    const [a, b] = arr;
    const dx = a.x - b.x, dy = a.y - b.y;
    return Math.hypot(dx, dy);
  }
  function touchPairMidX() {
    const arr = [...activeTouches.values()];
    if (arr.length < 2) return 0;
    return (arr[0].x + arr[1].x) / 2;
  }
  scroller.addEventListener("touchstart", (e) => {
    for (const t of e.changedTouches) {
      activeTouches.set(t.identifier, { x: t.clientX, y: t.clientY });
    }
    if (activeTouches.size === 2) {
      pinchPrevDist = touchPairDist();
      if (!zoomActive) startZoom({ clientX: touchPairMidX() });
      zoomPendingCursorX = touchPairMidX();
      zoomLastCursorX = zoomPendingCursorX;
    }
  }, { passive: true });
  scroller.addEventListener("touchmove", (e) => {
    if (activeTouches.size < 2) return;
    for (const t of e.changedTouches) {
      if (activeTouches.has(t.identifier)) {
        activeTouches.set(t.identifier, { x: t.clientX, y: t.clientY });
      }
    }
    const d = touchPairDist();
    if (pinchPrevDist > 0 && d > 0) {
      const factor = d / pinchPrevDist;
      pinchPrevDist = d;
      if (!zoomActive) startZoom({ clientX: touchPairMidX() });
      zoomPendingFactor *= factor;
      zoomPendingCursorX = touchPairMidX();
      zoomLastCursorX = zoomPendingCursorX;
      scheduleZoomFrame();
      if (zoomEndTimer) clearTimeout(zoomEndTimer);
      zoomEndTimer = setTimeout(commitZoom, 140);
      e.preventDefault();
    }
  }, { passive: false });
  function clearPinch(e) {
    for (const t of e.changedTouches) activeTouches.delete(t.identifier);
    if (activeTouches.size < 2) {
      pinchPrevDist = 0;
      if (zoomActive) commitZoom();
    }
  }
  scroller.addEventListener("touchend", clearPinch, { passive: true });
  scroller.addEventListener("touchcancel", clearPinch, { passive: true });

  // If the user clicks or starts dragging mid-zoom (rare on trackpads),
  // commit immediately so hit-detection uses the final layout.
  scroller.addEventListener("pointerdown", () => {
    if (zoomActive) {
      if (zoomEndTimer) { clearTimeout(zoomEndTimer); zoomEndTimer = 0; }
      commitZoom();
    }
  }, true);

  // Hold-Space → grab cursor + drag-pan everywhere (Figma / Sketch
  // convention). The existing mousedown path already supports drag-pan on
  // empty canvas; Space-mode extends it so the user can grab through dots
  // and edges without accidentally opening a thinker entry.
  let spaceHeld = false;
  function setSpaceMode(on) {
    if (spaceHeld === on) return;
    spaceHeld = on;
    document.body.classList.toggle("is-space-pan", on);
    scroller.style.cursor = on ? "grab" : "";
  }
  window.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !e.repeat && document.activeElement === document.body) {
      e.preventDefault();
      setSpaceMode(true);
    }
  });
  window.addEventListener("keyup", (e) => {
    if (e.code === "Space") setSpaceMode(false);
  });
  window.addEventListener("blur", () => setSpaceMode(false));

  // When Space is held, every mousedown becomes a pan-drag (even over dots).
  scroller.addEventListener("mousedown", (e) => {
    if (!spaceHeld && e.button !== 1) return; // middle-click also pans
    isDragging = true;
    didDrag = false;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    scrollStartX = scroller.scrollLeft;
    scrollStartY = scroller.scrollTop;
    scroller.style.cursor = "grabbing";
    scroller.style.userSelect = "none";
    e.preventDefault();
    e.stopPropagation();
  }, true);
}

// ---------- Reset View button (Network mode) -----------
// Frames the network at default zoom + initial focus year. Visible only in
// network mode; positioned top-right of the timeline pane.
function ensureResetViewButton() {
  let btn = document.getElementById("resetViewBtn");
  if (!btn) {
    btn = document.createElement("button");
    btn.id = "resetViewBtn";
    btn.className = "reset-view-btn";
    btn.type = "button";
    btn.title = "Reset view (frames the network)";
    btn.setAttribute("aria-label", "Reset view");
    btn.textContent = "Reset view";
    btn.addEventListener("click", () => {
      state.pxPerYear = PX_PER_YEAR_DEFAULT;
      state.hasInitialScroll = false;
      computeLayout();
      renderAll();
      scrollToInitialFocus();
    });
    const pane = document.getElementById("timelinePane");
    if (pane) pane.appendChild(btn);
  }
  btn.hidden = state.viewMode !== "network";
}

// ---------- unified right-side panel (tabs) -----------
// Single panel hosts five tabs: Thinker / Translation / Article / Citation / Source.
// One tab is active at a time; the others retain their last-rendered content.
const PANEL_TABS = ["thinker", "translation", "article", "citation", "source"];
const panelState = {
  open: false,
  activeTab: "thinker",
  // content-loaded flags so we can show "(empty)" placeholders when
  // a tab is opened directly without an upstream load.
  loaded: { thinker: false, translation: false, article: false, citation: false, source: false },
  // For mobile (≤720 px): Citation falls back to the legacy bottom-sheet
  // popover so a one-line locus check doesn't take over the screen.
};

function isPanelMobile() {
  return window.matchMedia("(max-width: 720px)").matches;
}

function openPanel(tab) {
  panelState.open = true;
  document.body.classList.add("is-detail-open");
  detailPane.setAttribute("aria-hidden", "false");
  if (tab) setPanelTab(tab);
}

function closePanel() {
  panelState.open = false;
  document.body.classList.remove("is-detail-open");
  detailPane.setAttribute("aria-hidden", "true");
  state.activeId = null;
  document.querySelectorAll(".thinker-dot").forEach((d) => d.classList.remove("is-active"));
  document.querySelectorAll(".lineage-edge").forEach((el) => el.classList.remove("is-lit"));
  if (!router._suspendSerialize) {
    try { history.replaceState(null, "", location.pathname + location.search); } catch (_) {}
  }
}

function setPanelTab(tab) {
  if (!PANEL_TABS.includes(tab)) return;
  panelState.activeTab = tab;
  // Tab buttons
  if (dpTabBar) {
    dpTabBar.querySelectorAll(".dp-tab").forEach((btn) => {
      const isActive = btn.dataset.pane === tab;
      btn.classList.toggle("is-active", isActive);
      btn.setAttribute("aria-selected", isActive ? "true" : "false");
    });
  }
  // Panes
  for (const t of PANEL_TABS) {
    const pane = document.getElementById("dpPane" + t[0].toUpperCase() + t.slice(1));
    if (!pane) continue;
    const isActive = t === tab;
    pane.classList.toggle("is-active", isActive);
    pane.hidden = !isActive;
    pane.setAttribute("aria-hidden", isActive ? "false" : "true");
  }
  if (tab === "source") ensureSourceTreeRendered();
  try { localStorage.setItem("vedanta-panel-tab", tab); } catch (_) {}
}

function showTab(tab) {
  // Show the tab button (some tabs are hidden until first use, e.g.
  // Translation, Article, Citation — exposed by an action that loads
  // content into them).
  if (!dpTabBar) return;
  const btn = dpTabBar.querySelector(`.dp-tab[data-pane="${tab}"]`);
  if (btn) btn.hidden = false;
}

if (dpTabBar) {
  dpTabBar.querySelectorAll(".dp-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      const t = btn.dataset.pane;
      if (!t) return;
      setPanelTab(t);
      // When the user clicks a tab directly, reflect the active surface in
      // the URL so back / forward / reload restores the same view.
      if (t === "thinker" && state.activeId) {
        router.push({ kind: "thinker", thinkerId: state.activeId });
      } else if (t === "source" && sourceTabState.activeFilePath) {
        router.push({ kind: "source", thinkerId: state.activeId || "", sourcePath: sourceTabState.activeFilePath });
      } else if (t === "citation" && sourceTabState.activeCiteKey) {
        router.push({ kind: "citation", thinkerId: state.activeId || sourceTabState.activeCiteKey.split("/")[0], citeKey: sourceTabState.activeCiteKey });
      }
    });
  });
}

// ---------- detail pane (Thinker tab) -----------
// ---------- URL hash router (Fix 3) -----------
// Every navigable state change is mirrored in the URL hash so back / forward
// / reload / share work. Format:
//   #/thinker/<id>
//   #/thinker/<id>/translation/<work_id>
//   #/thinker/<id>/citation/<thinker>/<work>/<locus...>
//   #/thinker/<id>/source/<file_path...>
//   #/article/<slug>
//   #/perspective/<slug>
// The router is reentrancy-guarded: when we apply a parsed hash we set a
// flag so the open* handlers do not push a redundant hash update back.
const router = {
  _suspendSerialize: false,

  parse(hash) {
    const h = (hash || "").replace(/^#\/?/, "").replace(/^\/+/, "");
    if (!h) return null;
    const parts = h.split("/").filter(Boolean).map((s) => {
      try { return decodeURIComponent(s); } catch (_) { return s; }
    });
    if (parts[0] === "thinker" && parts[1]) {
      const tid = parts[1];
      if (parts[2] === "translation" && parts[3]) {
        return { kind: "translation", thinkerId: tid, workId: parts[3] };
      }
      if (parts[2] === "citation" && parts[3]) {
        return { kind: "citation", thinkerId: tid, citeKey: parts.slice(3).join("/") };
      }
      if (parts[2] === "source" && parts[3]) {
        return { kind: "source", thinkerId: tid, sourcePath: parts.slice(3).join("/") };
      }
      return { kind: "thinker", thinkerId: tid };
    }
    if (parts[0] === "article" && parts[1]) {
      return { kind: "article", slug: parts[1] };
    }
    if (parts[0] === "perspective" && parts[1]) {
      return { kind: "perspective", slug: parts[1] };
    }
    if (parts[0] === "source" && parts[1]) {
      return { kind: "source", sourcePath: parts.slice(1).join("/") };
    }
    return null;
  },

  serialize(state) {
    if (!state) return "";
    const enc = (s) => encodeURIComponent(s || "").replace(/%2F/gi, "/");
    if (state.kind === "thinker") return `#/thinker/${enc(state.thinkerId)}`;
    if (state.kind === "translation") return `#/thinker/${enc(state.thinkerId)}/translation/${enc(state.workId)}`;
    if (state.kind === "citation") {
      const tid = state.thinkerId || (state.citeKey || "").split("/")[0] || "";
      const keyParts = (state.citeKey || "").split("/").map(enc).join("/");
      return `#/thinker/${enc(tid)}/citation/${keyParts}`;
    }
    if (state.kind === "source") {
      const tid = state.thinkerId || "";
      const pathParts = (state.sourcePath || "").split("/").map(enc).join("/");
      return tid
        ? `#/thinker/${enc(tid)}/source/${pathParts}`
        : `#/source/${pathParts}`;
    }
    if (state.kind === "article") return `#/article/${enc(state.slug)}`;
    if (state.kind === "perspective") return `#/perspective/${enc(state.slug)}`;
    return "";
  },

  push(state) {
    if (this._suspendSerialize) return;
    const target = this.serialize(state);
    if (!target) return;
    if (location.hash === target) return;
    try {
      history.replaceState(null, "", target);
    } catch (_) {
      location.hash = target.replace(/^#/, "");
    }
  },

  apply(parsed) {
    if (!parsed) return;
    this._suspendSerialize = true;
    try {
      if (parsed.kind === "thinker") {
        openThinker(parsed.thinkerId);
      } else if (parsed.kind === "translation") {
        openThinker(parsed.thinkerId);
        openReader(parsed.workId, parsed.thinkerId);
      } else if (parsed.kind === "citation") {
        openThinker(parsed.thinkerId);
        openCitationPanel(parsed.citeKey, null);
      } else if (parsed.kind === "source") {
        if (parsed.thinkerId) openThinker(parsed.thinkerId);
        setPanelTab("source");
        ensureSourceTreeRendered().then(() => {
          if (parsed.sourcePath) selectSourceFile(parsed.sourcePath);
        });
      } else if (parsed.kind === "article" || parsed.kind === "perspective") {
        const list = parsed.kind === "perspective"
          ? ((perspectivesManifest && perspectivesManifest.perspectives) || [])
          : ((articlesManifest && articlesManifest.articles) || []);
        const found = list.find((a) => a.slug === parsed.slug);
        if (found) {
          openArticle({ ...found, kind: parsed.kind });
        } else if (parsed.kind === "article") {
          ensureArticlesLoaded().then(() => {
            const a = (articlesManifest && articlesManifest.articles || []).find((x) => x.slug === parsed.slug);
            if (a) openArticle(a);
          });
        } else {
          ensurePerspectivesLoaded().then(() => {
            const p = (perspectivesManifest && perspectivesManifest.perspectives || []).find((x) => x.slug === parsed.slug);
            if (p) openArticle({ ...p, kind: "perspective" });
          });
        }
      }
    } finally {
      this._suspendSerialize = false;
    }
  },
};

window.addEventListener("hashchange", () => {
  const parsed = router.parse(location.hash);
  if (parsed) router.apply(parsed);
});

function openThinker(id) {
  const t = state.thinkersById.get(id);
  if (!t) return;
  state.activeId = id;
  document.querySelectorAll(".thinker-dot").forEach((d) => {
    d.classList.toggle("is-active", d.dataset.id === id);
  });
  document.querySelectorAll(".lineage-edge").forEach((el) => {
    el.classList.toggle("is-lit", el.dataset.from === id || el.dataset.to === id);
  });
  detailContent.style.setProperty("--dot-color", colorFor(t, 2));
  detailContent.style.setProperty("--school-light", colorFor(t, 1));
  detailContent.innerHTML = renderDetail(t);
  panelState.loaded.thinker = true;
  detailContent.scrollTop = 0;
  openPanel("thinker");
  scrollDotIntoView(t);
  // wire read-full buttons
  detailContent.querySelectorAll("[data-read-full]").forEach((btn) => {
    btn.addEventListener("click", () => openReader(btn.dataset.readFull, btn.dataset.thinker));
  });
  // wire perspective open buttons
  detailContent.querySelectorAll(".perspective-open").forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.dataset.perspectiveSlug;
      const list = (perspectivesManifest && perspectivesManifest.perspectives) || [];
      const p = list.find((x) => x.slug === slug);
      if (p) openArticle({ ...p, kind: "perspective" });
    });
  });
  router.push({ kind: "thinker", thinkerId: id });
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

// Legacy alias for the close handler — close the entire unified panel.
function closeDetailPane() { closePanel(); }
closeDetail.addEventListener("click", closePanel);
["pointerdown", "pointerup", "mousedown", "mouseup", "touchstart", "touchend"].forEach((type) => {
  detailPane.addEventListener(type, (e) => {
    e.stopPropagation();
  }, true);
});

// Click-on-empty-timeline-area closes the panel. Lets the user "click back
// to the map" instead of hunting for the close button. Drag/pan and clicks
// on interactive timeline elements (dots, edges, lane rail, era strip,
// axis, view-toggle, etc.) are exempted so existing flows still work.
(function wireTimelineDismiss() {
  if (!scroller) return;
  let downX = 0, downY = 0, downOnScroller = false;
  scroller.addEventListener("pointerdown", (e) => {
    if (e.button !== 0 && e.pointerType === "mouse") { downOnScroller = false; return; }
    downX = e.clientX; downY = e.clientY;
    downOnScroller = true;
  });
  scroller.addEventListener("pointerup", (e) => {
    if (!downOnScroller) return;
    downOnScroller = false;
    if (!document.body.classList.contains("is-detail-open")) return;
    // Drag threshold: if the pointer moved >4px between down and up,
    // treat it as a pan, not a click.
    if (Math.abs(e.clientX - downX) + Math.abs(e.clientY - downY) > 4) return;
    // Don't dismiss when the user clicked an interactive timeline target;
    // their own handlers (openThinker, lineage hover, etc.) take precedence.
    const target = e.target;
    if (target && detailPane && detailPane.contains(target)) return;
    if (target && target.closest && target.closest(
      ".thinker-dot, .lineage-edge, .lane-row, .lane-rail, .era-strip, .timeline-axis, button, a, input, [role='tab']"
    )) return;
    closePanel();
  });
})();

// ---------- detail rendering -----------
function renderDetail(t) {
  return [
    renderHero(t),
    renderLineageBlock(t),
    renderEngagedWorks(t),
    renderOrphanPassages(t),
    renderComparativeBlock(t),
    renderPerspectivesBlock(t),
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
  // Number citations in the core thesis. The footnote counter is local to
  // the hero block; engaged-works cards each start their own counter so
  // numbering does not balloon across the whole entry.
  const heroCtr = { n: 0 };
  const heroRendered = numberCitations(
    md(t.core_thesis || "Core thesis: not yet written."),
    heroCtr,
  );
  const heroThesisHtml = heroRendered.html;
  const heroFootnotes = renderFootnoteList(heroRendered.footnotes);
  return `
    <div class="detail-hero">
      <h2>${escape(t.name_iast || t.name || t.id)}</h2>
      ${t.name && t.name !== t.name_iast ? `<p class="romanization">${escape(t.name)}</p>` : ""}
      <div class="meta-row">
        <span class="school-pill">${escape(t.school || "")}${subSchool}</span>
        ${tierLabel ? `<span class="tier-pill">${escape(tierLabel)}</span>` : ""}
      </div>
      <p class="dates-line">${escape(formatDatesLong(t))}${t.dates_notes ? " · " + md(t.dates_notes) : ""}</p>
      <div class="thesis">${heroThesisHtml}</div>
      ${heroFootnotes}
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
    // Flag whether a full translation .md is on disk so the work card can
    // decide between "Read the full work in translation" + suppressed
    // passage list, or surfacing the key passages with an honest
    // "(full work pending)" framing.
    const txKey = `${t.id}__${w.work_id}`;
    w.__hasFullTranslation = state.fullTranslationSet
      ? state.fullTranslationSet.has(txKey)
      : false;
    return renderWorkCard(w, passages, t.id);
  }).join("");
  return `<h3 class="section-head">Engaged works</h3>${cards}`;
}

function renderWorkCard(w, passages, thinkerId) {
  const ascr = (w.ascription_tier || "").replace(/-/g, " ");
  const status = w.source_status || "";
  const statusLabel = {
    "clean-on-disk": "Sanskrit text in our corpus",
    "acceptable-on-disk": "Sanskrit text in our corpus (OCR — usable)",
    "degraded-on-disk": "Sanskrit text on disk but degraded — locus-only",
    "primary-text-not-in-corpus": "Primary text not in our corpus",
    "english-original": "English original",
    "bengali-original": "Bengali original",
    "tamil-original": "Tamil original",
  }[status] || "";
  const statusKind = (status === "primary-text-not-in-corpus" || status === "degraded-on-disk") ? "missing" : "present";
  // Number citations in the work summary + ascription notes. One counter
  // per card so the user sees [1] [2] … fresh in each work.
  const workCtr = { n: 0 };
  const summaryRendered = numberCitations(md(w.summary || ""), workCtr);
  const ascrRendered = w.ascription_notes
    ? numberCitations(md(w.ascription_notes), workCtr)
    : { html: "", footnotes: [] };
  const allFootnotes = summaryRendered.footnotes.concat(ascrRendered.footnotes);
  // Passages section framing — depends on whether a full translation is on
  // disk. When the full work is available the user reads it via the
  // "Read the full work in translation" button; the partial passage cards
  // would be redundant. When only key_passages exist on disk, surface them
  // under an honest "Engaged passages (full work pending)" header so the
  // user knows these are selected loci, not a representative sample.
  const hasFullTx = !!w.__hasFullTranslation;
  let passagesBlock = "";
  if (passages.length && !hasFullTx) {
    passagesBlock = `
      <div class="passages-nested">
        <p class="nested-head">Engaged passages <span class="nested-sub">(full work pending)</span></p>
        ${passages.map(renderPassageCard).join("")}
      </div>`;
  }
  const readLabel = hasFullTx
    ? "Read the full work in translation"
    : "Open Translation tab (status + engaged passages)";
  return `
    <div class="work-card" data-work-id="${escape(w.work_id)}" data-source-status="${escape(status)}">
      <div class="title-line">
        <span class="title">${escape(w.title_iast || w.title || w.work_id)}</span>
        ${ascr ? `<span class="ascr">${escape(ascr)}</span>` : ""}
      </div>
      <p class="summary">${summaryRendered.html}</p>
      ${ascrRendered.html ? `<p class="ascr-notes">${ascrRendered.html}</p>` : ""}
      ${statusLabel ? `<p class="source-status source-status--${statusKind}"><span class="dot"></span>${escape(statusLabel)}</p>` : ""}
      <button class="read-full-link" data-read-full="${escape(w.work_id)}" data-thinker="${escape(thinkerId)}">${readLabel}</button>
      ${renderFootnoteList(allFootnotes)}
      ${passagesBlock}
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

// ---------- perspectives layer (interpretive readings flagged as such) -----------
let perspectivesManifest = null;
let perspectivesLoading = null;
async function ensurePerspectivesLoaded() {
  if (perspectivesManifest) return perspectivesManifest;
  if (!perspectivesLoading) {
    perspectivesLoading = loadJSON("data/perspectives/manifest.json").then((m) => {
      perspectivesManifest = m || { perspectives: [] };
      return perspectivesManifest;
    });
  }
  return perspectivesLoading;
}

function renderPerspectivesBlock(t) {
  const list = (perspectivesManifest && perspectivesManifest.perspectives) || [];
  const matches = list.filter((p) => Array.isArray(p.for_thinker_ids) && p.for_thinker_ids.includes(t.id));
  if (!matches.length) {
    // Trigger a background load and re-open the thinker once available so handlers re-bind.
    if (!perspectivesManifest) {
      ensurePerspectivesLoaded().then(() => {
        if (state.activeId === t.id) openThinker(t.id);
      });
    }
    return "";
  }
  const cards = matches.map((p) => `
    <div class="perspective-card" data-perspective-slug="${escape(p.slug)}">
      <span class="perspective-pill">PERSPECTIVE</span>
      <p class="perspective-title">${inlineMarkdown(p.title)}</p>
      ${p.subtitle ? `<p class="perspective-subtitle">${md(p.subtitle)}</p>` : ""}
      <p class="perspective-disclaimer"><em>Reading discipline.</em> An interpretive reading. The school's own self-understanding is preserved in this thinker entry; what follows is what the corpus's interpretive perspective implies about the tradition. The school may very well disagree.</p>
      <button class="perspective-open" data-perspective-slug="${escape(p.slug)}">Read perspective →</button>
    </div>
  `).join("");
  return `<h3 class="section-head">Perspectives — interpretive readings, flagged as such</h3>${cards}`;
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
  // citation panel / popover (clickable primary-source citations)
  const cite = e.target.closest("a[href^='cite://']");
  if (cite) {
    e.preventDefault();
    const key = cite.getAttribute("href").replace(/^cite:\/\//, "");
    openCitationPanel(key, cite);
    return;
  }
  // glossary popovers
  const term = e.target.closest("[data-term]");
  if (term) {
    e.preventDefault();
    openGlossary(term.dataset.term, term);
  }
});

// ---------- Translation tab (full work translation, in the unified panel) -----------
async function openReader(workId, thinkerId) {
  const t = state.thinkersById.get(thinkerId);
  if (!t) return;
  const work = (t.engaged_works || []).find((w) => w.work_id === workId);
  if (!work) return;
  // Show the tab + open it immediately with a spinner so the click feels responsive.
  showTab("translation");
  if (dpTranslationHead) {
    dpTranslationHead.innerHTML = `
      <p class="dp-eyebrow">Translation</p>
      <p class="dp-title">${escape(work.title_iast || work.title)}</p>
      <p class="dp-attrib">${escape(t.name_iast || t.name)} · ${escape((work.genre || "").replace(/-/g, " "))} · ${escape(work.language || "sanskrit")}</p>
    `;
  }
  if (dpTranslationBody) dpTranslationBody.innerHTML = "<article><p style=\"padding:0 8px;color:var(--muted);font-style:italic\">Loading…</p></article>";
  openPanel("translation");

  const url = `data/full_translations/${thinkerId}__${workId}.md`;
  const r = await fetch(url);
  let body;
  if (r.ok) {
    body = await r.text();
  } else {
    // No extended translation on disk — synthesize a placeholder from key_passages.
    const passages = (t.key_passages || []).filter((p) => p.work_id === workId);
    const passagesBlock = passages.length
      ? "## Engaged passages\n\n" + passages.map((p) => {
          const sk = p.sanskrit_iast ? `> *${p.sanskrit_iast.replace(/\n/g, " ")}*` : "";
          const en = p.english_close ? p.english_close : "";
          const why = p.why_this_passage ? `\n*Why this passage:* ${p.why_this_passage}` : "";
          return `### ${p.locus_long || p.locus_short || ""}\n\n${sk}\n\n${en}${why}`;
        }).join("\n\n---\n\n")
      : "";
    body = `${work.summary || ""}

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
  if (dpTranslationBody) {
    dpTranslationBody.innerHTML = `<article>${renderTranslationDocument(body, { thinkerId, workId, work, thinker: t })}</article>`;
    dpTranslationBody.scrollTop = 0;
    wireTranslationDisclosures(dpTranslationBody, { thinkerId, workId });
  }
  panelState.loaded.translation = true;
  router.push({ kind: "translation", thinkerId, workId });
}

// ---------- Translation document parser + reading-first renderer -----------
//
// The Translation tab now reads as a translation, not a grammar exercise.
// Each `### LOCUS` section is parsed into a structured record:
//
//   {
//     locus,                                  // verse/section identifier
//     default_translation: { lang, text },    // primary readable surface
//     iast,                                   // Sanskrit in IAST (italic)
//     devanagari,                             // optional Sanskrit in Devanāgarī
//     morphology: { wordByWord, compound, karaka, verbal },
//     note,                                   // short interpretive aside
//   }
//
// The default-language slot is parameterized: today every translation in
// the corpus is English, but the same parser will accept Hindi, Bengali,
// Tamil, Telugu, Marathi, Gujarati, Kannada, or Malayalam in future
// passes. The header convention is `**<Language> (translation):**` or
// the legacy `**English (line-by-line):**`. Whatever language the file
// supplies for its readable surface becomes the default-language slot;
// IAST and Devanāgarī always remain Sanskrit.
//
// Grammar (word-by-word table, samāsa-vigraha, kāraka structure, verbal
// modality) is hidden by default behind a single disclosure. The Note
// stays inline as a subtle italic aside because it helps the reader
// rather than cluttering the page.

// Headings we recognize as the readable default-language slot. The first
// match wins. New languages are added by listing their conventional
// English name; the renderer emits the same prose styling regardless.
const DEFAULT_LANG_HEADINGS = [
  { match: /^\*\*English\s*\(line-by-line\)\s*:\*\*\s*$/i, lang: "en" },
  { match: /^\*\*English\s*\(translation\)\s*:\*\*\s*$/i, lang: "en" },
  { match: /^\*\*English\s*:\*\*\s*$/i, lang: "en" },
  { match: /^\*\*Translation\s*\(English\)\s*:\*\*\s*$/i, lang: "en" },
  { match: /^\*\*Hindi\s*\(translation\)\s*:\*\*\s*$/i, lang: "hi" },
  { match: /^\*\*Bengali\s*\(translation\)\s*:\*\*\s*$/i, lang: "bn" },
  { match: /^\*\*Tamil\s*\(translation\)\s*:\*\*\s*$/i, lang: "ta" },
  { match: /^\*\*Telugu\s*\(translation\)\s*:\*\*\s*$/i, lang: "te" },
  { match: /^\*\*Marathi\s*\(translation\)\s*:\*\*\s*$/i, lang: "mr" },
  { match: /^\*\*Gujarati\s*\(translation\)\s*:\*\*\s*$/i, lang: "gu" },
  { match: /^\*\*Kannada\s*\(translation\)\s*:\*\*\s*$/i, lang: "kn" },
  { match: /^\*\*Malayalam\s*\(translation\)\s*:\*\*\s*$/i, lang: "ml" },
];

const SECTION_HEADINGS = {
  iast: /^\*\*Sanskrit\s*\(IAST\)\s*:\*\*\s*$/i,
  devanagari: /^\*\*Sanskrit\s*\(Devan[āa]gar[īi]\)\s*:\*\*\s*$/i,
  wordByWord: /^\*\*Word-by-word\s*:\*\*\s*$/i,
  compound: /^\*\*Compound\s+resolution\s*\(sam[āa]sa-vigraha\)\s*:\*\*\s*$/i,
  karaka: /^\*\*K[āa]raka\s+structure\s*:\*\*\s*$/i,
  verbal: /^\*\*Verbal\s+modality\s*:\*\*\s*$/i,
  note: /^\*\*Note\s*:\*\*\s*$/i,
};

// Parse a single `### LOCUS` block (the contents *after* the heading
// line) into a structured record. Returns null if the block does not
// look like a per-verse translation card — in that case the caller
// falls back to renderMarkdownFull for the raw markdown.
function parseTranslationSection(rawBody, locus) {
  const lines = rawBody.split("\n");
  const slots = {
    iast: [],
    devanagari: [],
    defaultLang: null,
    defaultText: [],
    wordByWord: [],
    compound: [],
    karaka: [],
    verbal: [],
    note: [],
  };
  let current = null;
  for (const line of lines) {
    const trimmed = line.trim();
    let matched = false;
    for (const { match, lang } of DEFAULT_LANG_HEADINGS) {
      if (match.test(trimmed)) {
        slots.defaultLang = lang;
        current = "defaultText";
        matched = true;
        break;
      }
    }
    if (matched) continue;
    for (const [key, re] of Object.entries(SECTION_HEADINGS)) {
      if (re.test(trimmed)) {
        current = key;
        matched = true;
        break;
      }
    }
    if (matched) continue;
    if (current) {
      slots[current].push(line);
    } else {
      // Content before any recognized heading — keep with the IAST
      // bucket as a fallback so it isn't silently dropped.
      slots.iast.push(line);
    }
  }
  // A real verse card must have at least an IAST block and a default-
  // language translation. If neither is present we treat this section
  // as free-form prose (e.g. an editorial aside written as "### Foo").
  const hasIast = slots.iast.join("").trim().length > 0;
  const hasDefault = slots.defaultText.join("").trim().length > 0;
  if (!hasIast && !hasDefault) return null;
  const trim = (a) => a.join("\n").trim();
  return {
    locus,
    default_translation: { lang: slots.defaultLang || "en", text: trim(slots.defaultText) },
    iast: trim(slots.iast),
    devanagari: trim(slots.devanagari),
    morphology: {
      wordByWord: trim(slots.wordByWord),
      compound: trim(slots.compound),
      karaka: trim(slots.karaka),
      verbal: trim(slots.verbal),
    },
    note: trim(slots.note),
  };
}

// Strip leading YAML-ish frontmatter (--- … ---) and return parsed
// key→value pairs alongside the remaining body.
function stripFrontmatter(src) {
  const m = /^---\s*\n([\s\S]*?)\n---\s*\n?/.exec(src);
  if (!m) return { meta: {}, body: src };
  const meta = {};
  for (const line of m[1].split("\n")) {
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line);
    if (kv) {
      let v = kv[2].trim();
      // Strip surrounding quotes (single, double, triple) — values come
      // from the python audit script which uses repr() for evidence.
      if ((v.startsWith("'") && v.endsWith("'")) || (v.startsWith('"') && v.endsWith('"'))) {
        v = v.slice(1, -1);
      }
      meta[kv[1]] = v;
    }
  }
  return { meta, body: src.slice(m[0].length) };
}

// Coverage banner. Honest about what the reader is actually looking at.
function renderCoverageBanner(meta, work, thinker) {
  const cov = (meta.coverage || "").toLowerCase();
  const title = (work && (work.title_iast || work.title)) || "the work";
  if (cov === "full") {
    return `<div class="tx-coverage tx-coverage-full"><span class="tx-coverage-tag">Full text</span> The complete <em>${escape(title)}</em>.</div>`;
  }
  if (cov === "selection") {
    return `<div class="tx-coverage tx-coverage-selection"><span class="tx-coverage-tag">Selected passages</span> An excerpt from <em>${escape(title)}</em>; the full text extends beyond what is rendered here.<button class="tx-coverage-source" data-tx-open-source="${escape(thinker ? thinker.id : "")}">Open Source tab →</button></div>`;
  }
  if (cov === "placeholder") {
    return `<div class="tx-coverage tx-coverage-placeholder"><span class="tx-coverage-tag">Acquisition queued</span> A defensible Sanskrit witness for <em>${escape(title)}</em> is not yet on disk; the page below summarizes what is and is not engaged.</div>`;
  }
  return "";
}

function slugifyLocus(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80);
}

function disclosureKey(thinkerId, workId, locus) {
  return `tx-disc:${thinkerId}:${workId}:${slugifyLocus(locus)}`;
}

function readDisclosureState(key) {
  try {
    return localStorage.getItem(key) === "open";
  } catch (_) {
    return false;
  }
}

function writeDisclosureState(key, open) {
  try {
    localStorage.setItem(key, open ? "open" : "closed");
  } catch (_) { /* private mode, etc. — silent */ }
}

// Render one parsed verse card. Reading-first hierarchy: locus, then
// default-language translation prominently, then IAST + Devanāgarī
// (when present) muted underneath, then a single disclosure for the
// grammatical breakdown, and finally the Note as a subtle italic aside.
function renderVerseCard(section, ctx) {
  const { thinkerId, workId } = ctx;
  const dKey = disclosureKey(thinkerId, workId, section.locus);
  const startOpen = readDisclosureState(dKey);
  const morph = section.morphology || {};
  const hasMorph = morph.wordByWord || morph.compound || morph.karaka || morph.verbal;

  const langClass = `tx-default-lang tx-lang-${section.default_translation.lang}`;
  const defaultBlock = section.default_translation.text
    ? `<div class="${langClass}" lang="${escape(section.default_translation.lang)}">${renderMarkdownFull(section.default_translation.text)}</div>`
    : "";
  const iastBlock = section.iast
    ? `<div class="tx-iast" lang="sa-Latn">${renderMarkdownFull(section.iast)}</div>`
    : "";
  const devBlock = section.devanagari
    ? `<div class="tx-devanagari" lang="sa-Deva">${renderMarkdownFull(section.devanagari)}</div>`
    : "";

  let morphInner = "";
  if (hasMorph) {
    const parts = [];
    if (morph.wordByWord) parts.push(`<div class="tx-morph-block tx-morph-words"><div class="tx-morph-label">Word by word</div>${renderMarkdownFull(morph.wordByWord)}</div>`);
    if (morph.compound) parts.push(`<div class="tx-morph-block"><div class="tx-morph-label">Compound resolution <span class="tx-morph-sub">(samāsa-vigraha)</span></div>${renderMarkdownFull(morph.compound)}</div>`);
    if (morph.karaka) parts.push(`<div class="tx-morph-block"><div class="tx-morph-label">Kāraka structure</div>${renderMarkdownFull(morph.karaka)}</div>`);
    if (morph.verbal) parts.push(`<div class="tx-morph-block"><div class="tx-morph-label">Verbal modality</div>${renderMarkdownFull(morph.verbal)}</div>`);
    morphInner = parts.join("");
  }

  const disclosure = hasMorph
    ? `<details class="tx-grammar"${startOpen ? " open" : ""} data-tx-disclosure="${escape(dKey)}">
         <summary><span class="tx-grammar-caret" aria-hidden="true"></span><span class="tx-grammar-label">Word-by-word and grammar</span></summary>
         <div class="tx-grammar-body">${morphInner}</div>
       </details>`
    : "";

  const noteBlock = section.note
    ? `<aside class="tx-note">${renderMarkdownFull(section.note)}</aside>`
    : "";

  return `<section class="tx-verse" data-tx-locus="${escape(section.locus)}">
    <header class="tx-verse-head"><span class="tx-locus">${escape(section.locus)}</span></header>
    ${defaultBlock}
    ${iastBlock}
    ${devBlock}
    ${disclosure}
    ${noteBlock}
  </section>`;
}

// Top-level renderer for a translation document. Splits into:
//   (1) optional YAML frontmatter (consumed for the coverage banner)
//   (2) preamble — everything before the first `### LOCUS` heading
//   (3) per-verse sections — parsed structurally where possible,
//       falling back to renderMarkdownFull when a section does not
//       look like a verse card
//   (4) trailing prose (e.g. "## Editorial closing")
function renderTranslationDocument(rawSrc, ctx) {
  const { meta, body } = stripFrontmatter(rawSrc);
  const banner = renderCoverageBanner(meta, ctx.work, ctx.thinker);

  // Split on lines that begin a verse card. Anything before the first
  // such heading is the preamble; subsequent material is split into
  // (heading-line, body-up-to-next-heading-or-h2) pairs. An H2
  // (`## …`) terminates the verse-card stream and re-opens free
  // markdown for editorial closings.
  const lines = body.split("\n");
  let preamble = [];
  const sections = []; // {locus, body}
  let trailing = []; // any content after the verse stream ends (## heading)
  let mode = "preamble";
  let cur = null;
  for (const line of lines) {
    if (mode === "preamble") {
      const h3 = /^###\s+(.+?)\s*$/.exec(line);
      if (h3) {
        mode = "section";
        cur = { locus: h3[1].trim(), body: [] };
        sections.push(cur);
        continue;
      }
      // An H2 inside the preamble keeps us in preamble mode.
      preamble.push(line);
      continue;
    }
    if (mode === "section") {
      const h3 = /^###\s+(.+?)\s*$/.exec(line);
      if (h3) {
        cur = { locus: h3[1].trim(), body: [] };
        sections.push(cur);
        continue;
      }
      const h2 = /^##\s+/.exec(line);
      if (h2) {
        // Editorial closing or similar — drop back to free-form mode.
        mode = "trailing";
        trailing.push(line);
        continue;
      }
      // Horizontal rules between sections: swallow.
      if (/^---+\s*$/.test(line) && cur && cur.body.length === 0) continue;
      cur.body.push(line);
      continue;
    }
    // mode === "trailing"
    trailing.push(line);
  }

  const preambleHtml = preamble.length
    ? `<div class="tx-preamble">${renderMarkdownFull(preamble.join("\n"))}</div>`
    : "";

  const sectionHtml = sections.map((s) => {
    const parsed = parseTranslationSection(s.body.join("\n"), s.locus);
    if (parsed) return renderVerseCard(parsed, ctx);
    // Fallback — render the section verbatim (preserves arbitrary
    // editorial content that doesn't fit the verse-card schema).
    return `<section class="tx-verse-fallback">${renderMarkdownFull(`### ${s.locus}\n\n${s.body.join("\n")}`)}</section>`;
  }).join("");

  const trailingHtml = trailing.join("\n").trim()
    ? `<div class="tx-trailing">${renderMarkdownFull(trailing.join("\n"))}</div>`
    : "";

  return banner + preambleHtml + sectionHtml + trailingHtml;
}

function wireTranslationDisclosures(root, ctx) {
  if (!root) return;
  // Persist open/closed state on toggle. Native <details> handles the
  // visual state; we just remember it in localStorage.
  root.querySelectorAll("details[data-tx-disclosure]").forEach((d) => {
    d.addEventListener("toggle", () => {
      writeDisclosureState(d.dataset.txDisclosure, d.open);
    });
  });
  // "Open Source tab →" link in the coverage banner switches tabs.
  root.querySelectorAll("[data-tx-open-source]").forEach((b) => {
    b.addEventListener("click", (e) => {
      e.preventDefault();
      if (typeof showTab === "function") showTab("source");
    });
  });
}

// ---------- popover manager (single-popover discipline) -----------
// Centralises the rule "only one popover is open at a time". Every popover
// (glossary, citation, topbar-search results) registers its close function;
// opening a new one closes whatever was open before.
//
// Without this discipline, glossary + citation could stack (closing one
// would leave the other open), and the new top-bar glossary search results
// would race against any open popover. A singleton keeps the rule cheap and
// explicit, and centralises Esc / outside-click behaviour for free.
const popoverManager = (() => {
  let activeClose = null;
  return {
    open(closeFn) {
      // Close whatever was open first. The close function is responsible
      // for removing its own DOM + scrim + listeners; we just invoke it.
      if (activeClose && activeClose !== closeFn) {
        try { activeClose(); } catch (_) {}
      }
      activeClose = closeFn;
    },
    // Called by a popover's own close function as it tears down, so the
    // manager doesn't try to re-invoke it.
    notifyClosed(closeFn) {
      if (activeClose === closeFn) activeClose = null;
    },
    closeAll() {
      if (activeClose) {
        const fn = activeClose;
        activeClose = null;
        try { fn(); } catch (_) {}
      }
    },
  };
})();

// ---------- popover drag helper -----------
// Shared between the glossary popover and the citation popover. The popover
// itself is the drag surface — there is no separate handle bar. We bail on
// interactive children (links, buttons, inputs, anything marked
// [data-no-drag]) so clicks on glossary terms, the close button, and the
// "Open thinker" button still work normally. A 4 px movement threshold lets
// the user select text without accidentally starting a drag.
//
//   • Bounds clamping keeps the popover at least partially on-screen.
//   • Optional session persistence: pass a storageKey to remember the user's
//     preferred placement across opens (via localStorage).
//
// Skipped on mobile (≤720 px): the popover is a bottom-sheet there and a
// drag would conflict with the sheet's CSS-fixed positioning.
const POP_DRAG_THRESHOLD = 4;

function makePopoverDraggable(pop, opts) {
  const isMobile = window.matchMedia("(max-width: 720px)").matches;
  if (isMobile) return;
  let armed = false;        // pointerdown landed on a draggable region
  let dragging = false;     // movement has crossed the threshold
  let startX = 0, startY = 0, startLeft = 0, startTop = 0;
  let activePointerId = null;

  function clampLeft(x, el) {
    const w = el.offsetWidth || 400;
    const minLeft = -w + 100;                       // keep >=100 px visible
    const maxLeft = window.innerWidth - 100;
    return Math.max(minLeft, Math.min(maxLeft, x));
  }
  function clampTop(y, el) {
    const minTop = 8;
    const maxTop = window.innerHeight - 80;
    return Math.max(minTop, Math.min(maxTop, y));
  }

  const key = opts && opts.storageKey;
  if (key) {
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const saved = JSON.parse(raw);
        if (saved && typeof saved.left === "number" && typeof saved.top === "number") {
          pop.style.left = clampLeft(saved.left, pop) + "px";
          pop.style.top = clampTop(saved.top, pop) + "px";
        }
      }
    } catch (_) {}
  }

  function isInteractiveTarget(target) {
    if (!target || target.nodeType !== 1) return false;
    return !!target.closest(
      "a, button, input, select, textarea, [data-no-drag], [contenteditable=''], [contenteditable='true']",
    );
  }

  // A pointerdown inside the popover's scrollbar gutter must scroll, not drag.
  function isOnScrollbar(e) {
    const r = pop.getBoundingClientRect();
    const scrollbarWidth = pop.offsetWidth - pop.clientWidth;
    return scrollbarWidth > 0 && (e.clientX > r.right - scrollbarWidth - 1);
  }

  pop.addEventListener("pointerdown", (e) => {
    if (e.button !== undefined && e.button !== 0) return; // primary button only
    if (isInteractiveTarget(e.target)) return;
    if (isOnScrollbar(e)) return;
    armed = true;
    dragging = false;
    activePointerId = e.pointerId;
    startX = e.clientX;
    startY = e.clientY;
    const r = pop.getBoundingClientRect();
    startLeft = r.left;
    startTop = r.top;
  });

  pop.addEventListener("pointermove", (e) => {
    if (!armed || e.pointerId !== activePointerId) return;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    if (!dragging) {
      if (Math.abs(dx) < POP_DRAG_THRESHOLD && Math.abs(dy) < POP_DRAG_THRESHOLD) return;
      // Don't begin a drag if the user is actively selecting text.
      const sel = window.getSelection && window.getSelection();
      if (sel && sel.toString().length > 0) { armed = false; return; }
      dragging = true;
      try { pop.setPointerCapture(e.pointerId); } catch (_) {}
      pop.classList.add("is-dragging");
      e.preventDefault();
    }
    pop.style.left = clampLeft(startLeft + dx, pop) + "px";
    pop.style.top = clampTop(startTop + dy, pop) + "px";
  });

  const endDrag = (e) => {
    if (!armed) return;
    const wasDragging = dragging;
    armed = false;
    dragging = false;
    if (wasDragging) {
      pop.classList.remove("is-dragging");
      try { pop.releasePointerCapture(e.pointerId); } catch (_) {}
      if (key) {
        try {
          const r = pop.getBoundingClientRect();
          localStorage.setItem(key, JSON.stringify({ left: r.left, top: r.top }));
        } catch (_) {}
      }
    }
    activePointerId = null;
  };
  pop.addEventListener("pointerup", endDrag);
  pop.addEventListener("pointercancel", endDrag);
}

// ---------- glossary popover -----------
// IAST-aware word boundary. Native `\b` treats IAST diacritics
// (ā, ī, ū, ṛ, ṝ, ḷ, ḹ, ṅ, ñ, ṭ, ḍ, ṇ, ś, ṣ, ṃ, ḥ) as word breaks, so
// "karman" against the term "karma" matched as `karma|n`. We instead
// require the preceding and following characters to be *not* a Latin
// letter, IAST diacritic, or digit. This makes "karman" non-matching
// for the term "karma" while keeping "karma," "karma." "(karma)"
// "*karma*" and "karma-yoga" matchable.
const IAST_LETTER_CLASS = "A-Za-z0-9āīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ";
function buildGlossaryRegex() {
  if (state.glossary.size === 0) return;
  const keys = [...state.glossary.keys()].sort((a, b) => b.length - a.length);
  const escaped = keys.map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  state.glossaryRegex = new RegExp(
    `(?<![${IAST_LETTER_CLASS}])(${escaped.join("|")})(?![${IAST_LETTER_CLASS}])`,
    "g",
  );
}

function openGlossary(termKey, anchorEl) {
  const entry = state.glossary.get(termKey);
  if (!entry) return;
  // Single-popover discipline: any other open popover (glossary, citation,
  // top-bar search results) is dismissed before this one opens.
  popoverManager.closeAll();
  // Belt-and-braces cleanup in case a popover failed to register itself.
  document.querySelectorAll(".glossary-popover, .gloss-scrim").forEach((el) => el.remove());
  const isMobile = window.matchMedia("(max-width: 720px)").matches;
  const pop = document.createElement("div");
  pop.className = "glossary-popover";
  // One footnote counter for the entire popover so [1] [2] … is continuous
  // across the invariant definition, per-school rows, and translator note.
  // Each prose block is run through `md` + `numberCitations`, which replaces
  // inline `<a class="cite-link">` anchors with `<sup class="cite-fn">[N]</sup>`
  // and accumulates the locus into `footnotes`. The footnote list is then
  // appended at the bottom of the popover with click-targets back into the
  // Citation tab popover (parity with the thinker-prose pipeline).
  const popCtr = { n: 0 };
  const invariantR = numberCitations(md(entry.invariant_definition || ""), popCtr);
  const allFootnotes = invariantR.footnotes.slice();
  const perSchool = (entry.per_school || []).map((s) => {
    const r = numberCitations(md(s.definition), popCtr);
    allFootnotes.push(...r.footnotes);
    const tag = s.register_tag
      ? `<span class="gp-regtag" title="register tuple">${escape(s.register_tag)}</span>`
      : "";
    return `<div class="gp-row"><span class="gp-school">${escape(s.school)}</span><span class="gp-def">${tag}${r.html}</span></div>`;
  }).join("");
  const translatorR = entry.translator_note
    ? numberCitations(md(entry.translator_note), popCtr)
    : { html: "", footnotes: [] };
  allFootnotes.push(...translatorR.footnotes);
  const translatorNote = entry.translator_note
    ? `<div class="gp-translator"><span class="gp-label">Translator note</span><div>${translatorR.html}</div></div>`
    : "";
  const framing = entry.school_framing;
  const framingLabel = (() => {
    if (!framing || !framing.framing_status) return "";
    switch (framing.framing_status) {
      case "same_concept_different_aspect": return "Same concept, different aspect";
      case "real_disagreement":              return "Same concept, real disagreement";
      case "different_concepts":             return "Different concepts (homonymy)";
      case "mixed":                          return "Mixed — same concept where noted; real disagreement where noted";
      default: return escape(framing.framing_status);
    }
  })();
  // Framing blocks are methodological prose; we route them through md() only,
  // not numberCitations, since the inline references are short locus mentions
  // (e.g. *Anuvyākhyāna* 2.3.66–69) rather than `cite://` anchors that need
  // footnote numbering.
  const framingBlock = framing
    ? `<div class="gp-framing"><span class="gp-label">School framing</span>
         <div class="gp-framing-status">${framingLabel}</div>
         ${framing.shared_core ? `<div class="gp-shared-core">${md(framing.shared_core)}</div>` : ""}
         ${framing.register_axes_note ? `<div class="gp-axes">${md(framing.register_axes_note)}</div>` : ""}
       </div>`
    : "";
  const footnoteList = renderFootnoteList(allFootnotes);
  // Heading: prefer the surface form the user actually clicked when it
  // differs from the canonical term_iast (alias resolution makes them
  // diverge — e.g. clicking "guṇātīta" used to silently open "guṇa";
  // clicking "sat-cit-ānanda" used to silently open "saccidānanda").
  // Show the canonical form as an eyebrow so the alias relation is
  // visible rather than masked.
  const canonical = entry.term_iast || entry.term_key || termKey;
  const surface = termKey;
  // Diacritic-insensitive equality check: distinguish "lakṣaṇa" vs
  // "lakṣaṇā" (long-vs-short -a) — those are *different* lemmas in the
  // Sanskrit grammatical tradition even when one resolves the other.
  const showAlias = String(surface).normalize("NFC") !== String(canonical).normalize("NFC");
  const heading = showAlias
    ? `<div class="gp-eyebrow">Listed under <em>${escape(canonical)}</em></div>
       <div class="gp-term">${escape(surface)}</div>`
    : `<div class="gp-term">${escape(canonical)}</div>`;
  pop.innerHTML = `
    <button class="gp-close" aria-label="Close" data-no-drag type="button">×</button>
    ${heading}
    ${entry.literal ? `<div class="gp-literal">Literally: <em>${escape(entry.literal)}</em></div>` : ""}
    <div class="gp-invariant"><span class="gp-label">${entry.invariant_definition && entry.invariant_definition.toLowerCase().includes("no shared invariant") ? "No invariant" : "Invariant"}</span><div>${invariantR.html}</div></div>
    ${perSchool ? `<div class="gp-perschool"><span class="gp-label">By school</span>${framingBlock}${perSchool}</div>` : ""}
    ${translatorNote}
    ${footnoteList}
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
    // Popover width is 420 px (see .glossary-popover in style.css); leave a
    // 10 px gutter so it never clips against the viewport's right edge or
    // is occluded by the detail-pane scrollbar.
    pop.style.left = Math.max(10, Math.min(r.left, window.innerWidth - 430)) + "px";
  }
  function closeGloss() {
    pop.remove();
    if (scrim) scrim.remove();
    document.removeEventListener("click", outsideClose);
    document.removeEventListener("keydown", escClose);
    popoverManager.notifyClosed(closeGloss);
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
  makePopoverDraggable(pop, { storageKey: "vedanta-gloss-popover-pos" });
  popoverManager.open(closeGloss);
}

// ---------- citation popover (clickable primary-source citations) -----------
async function loadCitationIndex() {
  if (state.citationIndex) return;
  const idx = await loadJSON("data/citation_index.json");
  if (idx) state.citationIndex = idx;
}

function lookupCitationEntry(key) {
  const idx = state.citationIndex;
  if (!idx || !key) return null;
  const direct = idx.entries && idx.entries[key];
  if (direct) return direct;
  const aliasTarget = idx.aliases && idx.aliases[key];
  if (aliasTarget) return idx.entries && idx.entries[aliasTarget];
  return null;
}

async function openCitationPopover(key, anchorEl) {
  await loadCitationIndex();
  // Single-popover discipline (managed centrally so we don't have to keep
  // every popover's class name in sync here). The belt-and-braces cleanup
  // below catches stragglers if a popover failed to register itself.
  popoverManager.closeAll();
  document.querySelectorAll(".citation-popover, .glossary-popover, .gloss-scrim, .cite-scrim")
    .forEach((el) => el.remove());

  const entry = lookupCitationEntry(key);
  const isMobile = window.matchMedia("(max-width: 720px)").matches;

  // Parse the key for display (thinker / work / locus)
  const parts = key.split("/");
  const tid = parts[0] || "";
  const wid = parts[1] || "";
  const loc = parts.slice(2).join("/");
  const t = state.thinkersById.get(tid);
  const thinkerName = t ? (t.name_iast || t.name) : tid;
  let workTitle = wid;
  if (t) {
    const w = (t.engaged_works || []).find((x) => x.work_id === wid);
    if (w) workTitle = w.title_iast || w.title || wid;
  }

  const pop = document.createElement("div");
  pop.className = "citation-popover";

  let bodyHtml;
  if (entry) {
    const locusDisplay = entry.locus || entry.locus_short || loc;
    const isPending = entry.verified === "pending-acquisition";
    const pendingBlock = isPending
      ? `<div class="cp-block cp-pending"><span class="cp-label">Pending acquisition</span><p>${entry.pending_target_work
          ? `<em>${escape(entry.pending_target_work)}</em>${entry.pending_target_thinker ? ` (${escape(entry.pending_target_thinker)})` : ""} is not yet on disk in clean form.`
          : `The cited work is not yet on disk in clean form.`} The claim above relies on this work; its acquisition is queued at <code>parishishta/notes/USER_NEEDED.md</code>. The text shown below is the locus on which it comments, included as context — not itself the attestation.${entry.pending_acquisition_note || entry.verification_note ? ` <em>${escape(entry.pending_acquisition_note || entry.verification_note)}</em>` : ""}</p></div>`
      : "";
    const sk = entry.sanskrit_iast
      ? `<div class="cp-block cp-sanskrit"><span class="cp-label">${isPending ? "Sanskrit (IAST) — context" : "Sanskrit (IAST)"}</span><div class="cp-sk">${escape(entry.sanskrit_iast).replace(/\n/g, "<br>")}</div></div>`
      : "";
    const en = entry.english_close
      ? `<div class="cp-block cp-english"><span class="cp-label">${isPending ? "Close English — context" : "Close English"}</span><div class="cp-en">${md(entry.english_close)}</div></div>`
      : "";
    const openWork = `<button class="cp-open-thinker" data-thinker-id="${escape(tid)}">Open ${escape(thinkerName)} →</button>`;
    bodyHtml = `
      <div class="cp-header">
        <div class="cp-locus">${escape(locusDisplay)}${isPending ? ` <span class="cp-pending-badge">Pending</span>` : ""}</div>
        <div class="cp-attrib">${escape(thinkerName)} · <em>${escape(workTitle)}</em></div>
      </div>
      ${pendingBlock}
      ${sk}
      ${en}
      <div class="cp-actions">${openWork}</div>
    `;
  } else {
    const openWork = t
      ? `<button class="cp-open-thinker" data-thinker-id="${escape(tid)}">Open ${escape(thinkerName)} →</button>`
      : "";
    bodyHtml = `
      <div class="cp-header">
        <div class="cp-locus">${escape(loc || key)}</div>
        <div class="cp-attrib">${escape(thinkerName)}${workTitle ? ` · <em>${escape(workTitle)}</em>` : ""}</div>
      </div>
      <div class="cp-block cp-pending">
        <p>Passage not yet extracted. The cited locus is named in this entry but its primary-source Sanskrit (line-by-line, with Pāṇinian breakdown) has not been transcribed into the on-disk corpus yet. Open the thinker entry below to see what <em>is</em> currently engaged.</p>
      </div>
      <div class="cp-actions">${openWork}</div>
    `;
  }

  pop.innerHTML = `<button class="cp-close" aria-label="Close" data-no-drag type="button">×</button>${bodyHtml}`;

  let scrim = null;
  if (isMobile) {
    scrim = document.createElement("div");
    scrim.className = "cite-scrim";
    document.body.appendChild(scrim);
    document.body.appendChild(pop);
    scrim.addEventListener("click", () => closeCite());
  } else {
    document.body.appendChild(pop);
    const r = anchorEl.getBoundingClientRect();
    pop.style.position = "fixed";
    const popH = pop.offsetHeight || 280;
    const placeBelow = (r.bottom + popH + 8) < window.innerHeight;
    pop.style.top = (placeBelow ? r.bottom + 8 : Math.max(10, r.top - popH - 8)) + "px";
    pop.style.left = Math.max(10, Math.min(r.left, window.innerWidth - 460)) + "px";
  }

  function closeCite() {
    pop.remove();
    if (scrim) scrim.remove();
    document.removeEventListener("click", outsideClose);
    document.removeEventListener("keydown", escClose);
    popoverManager.notifyClosed(closeCite);
  }
  function outsideClose(e) {
    if (!pop.contains(e.target) && e.target !== anchorEl && e.target !== scrim) {
      closeCite();
    }
  }
  function escClose(e) { if (e.key === "Escape") closeCite(); }
  pop.querySelector(".cp-close").addEventListener("click", closeCite);
  const openBtn = pop.querySelector(".cp-open-thinker");
  if (openBtn) {
    openBtn.addEventListener("click", () => {
      closeCite();
      openThinker(openBtn.dataset.thinkerId);
    });
  }
  setTimeout(() => document.addEventListener("click", outsideClose), 0);
  document.addEventListener("keydown", escClose);
  makePopoverDraggable(pop, { storageKey: "vedanta-cite-popover-pos" });
  popoverManager.open(closeCite);
}

// ---------- Citation tab + Source tab (in the unified panel) -----------
// Tab-shared state: manifest, file cache, active selections.
const sourceTabState = {
  manifestLoaded: false,
  manifest: null,
  fileCache: new Map(), // path -> text
  activeFilePath: null,
  activeCiteKey: null,
};

// Citation-tab entry point. Falls back to the legacy bottom-sheet popover
// on mobile (citations are short; full-screen overlay is overkill).
async function openCitationPanel(key, anchorEl) {
  if (isPanelMobile()) {
    openCitationPopover(key, anchorEl);
    return;
  }
  await loadCitationIndex();
  sourceTabState.activeCiteKey = key;
  try { localStorage.setItem("vedanta-cite-panel-cite-key", key); } catch (_) {}
  renderCitationTab(key);
  showTab("citation");
  openPanel("citation");
  panelState.loaded.citation = true;
  router.push({ kind: "citation", thinkerId: state.activeId || (key.split("/")[0] || ""), citeKey: key });
}

function renderCitationTab(key) {
  const entry = lookupCitationEntry(key);
  const parts = (key || "").split("/");
  const tid = parts[0] || "";
  const wid = parts[1] || "";
  const loc = parts.slice(2).join("/");
  const t = state.thinkersById.get(tid);
  const thinkerName = t ? (t.name_iast || t.name) : tid;
  let workTitle = wid;
  if (t) {
    const w = (t.engaged_works || []).find((x) => x.work_id === wid);
    if (w) workTitle = w.title_iast || w.title || wid;
  }

  const surrounding = collectSurroundingPassages(tid, wid, entry);
  const before = surrounding.before;
  const after = surrounding.after;

  const locusDisplay = entry ? (entry.locus || entry.locus_short || loc) : (loc || key);

  const renderContext = (passages, label) => {
    if (!passages || !passages.length) return "";
    const rows = passages.map((p) => {
      const sk = p.sanskrit_iast
        ? `<div class="ccr-sk">${escape(p.sanskrit_iast).replace(/\n/g, "<br>")}</div>`
        : "";
      const en = p.english_close
        ? `<div class="ccr-en">${md(p.english_close)}</div>`
        : "";
      return `
        <div class="cite-context-row">
          <div class="ccr-locus">${escape(p.locus_short || p.locus_long || "")}</div>
          ${sk}
          ${en}
        </div>
      `;
    }).join("");
    return `<div class="ccb-context-label">${escape(label)}</div>${rows}`;
  };

  // Honour the audit: entries flagged `verified: false` had their IAST
  // fragment checked against the on-disk source and not found. Entries
  // flagged `verified: "pending-acquisition"` point at a text we do not
  // yet hold on disk (typically: a commentary whose on-disk record only
  // covers the parent text it comments on). In either case we still show
  // the locus + attribution, but suppress the Sanskrit and the close
  // English so an unverified passage can't be mistaken for a quotation.
  const isPending = entry && entry.verified === "pending-acquisition";
  const pendingTargetWork = entry && (entry.pending_target_work || "");
  const pendingTargetThinker = entry && (entry.pending_target_thinker || "");
  const pendingNote = entry && (entry.pending_acquisition_note || entry.verification_note || "");
  const anchorHtml = entry
    ? (isPending
        ? `
      <div class="cite-passage-anchor cite-passage-anchor--pending">
        <div class="cpa-locus">Locus · ${escape(entry.locus_short || locusDisplay)}</div>
        <div class="cpa-pending">
          <strong>Pending acquisition</strong>${pendingTargetWork
            ? ` — <em>${escape(pendingTargetWork)}</em>${pendingTargetThinker ? ` (${escape(pendingTargetThinker)})` : ""} is not yet on disk in clean form.`
            : "."} The claim above relies on this work; its acquisition is queued at <code>parishishta/notes/USER_NEEDED.md</code>. The cited text shown below is the locus on which it comments, included as context — not itself the attestation.
          ${pendingNote ? `<div class="cpa-note"><em>${escape(pendingNote)}</em></div>` : ""}
        </div>
        ${entry.sanskrit_iast ? `<div class="cpa-sk cpa-sk--context">${escape(entry.sanskrit_iast).replace(/\n/g, "<br>")}</div>` : ""}
        ${entry.english_close ? `<div class="cpa-en cpa-en--context">${md(entry.english_close)}</div>` : ""}
      </div>
    `
        : entry.verified === false
        ? `
      <div class="cite-passage-anchor cite-passage-anchor--unverified">
        <div class="cpa-locus">Locus · ${escape(entry.locus_short || locusDisplay)}</div>
        <div class="cpa-pending">
          The Sanskrit passage referenced here was not located in the on-disk
          source by the citation audit. Locus and attribution are preserved;
          the passage text is withheld until it can be verified against the
          primary text. ${entry.verification_note ? `<em>${escape(entry.verification_note)}</em>` : ""}
        </div>
      </div>
    `
        : `
      <div class="cite-passage-anchor">
        <div class="cpa-locus">Locus · ${escape(entry.locus_short || locusDisplay)}</div>
        ${entry.sanskrit_iast ? `<div class="cpa-sk">${escape(entry.sanskrit_iast).replace(/\n/g, "<br>")}</div>` : ""}
        ${entry.english_close ? `<div class="cpa-en">${md(entry.english_close)}</div>` : ""}
      </div>
    `)
    : `
      <div class="cite-passage-anchor">
        <div class="cpa-locus">Locus · ${escape(locusDisplay)}</div>
        <div class="cpa-pending">Passage not yet extracted into the on-disk corpus. The locus is named in this entry; the surrounding work has not been transcribed line-by-line yet. Open the thinker entry to see what <em>is</em> currently engaged.</div>
      </div>
    `;

  const noContextNote = entry && !before.length && !after.length
    ? `<p class="ccb-note">No surrounding key-passages indexed for this work yet.</p>`
    : "";

  const actions = `
    <div class="ccb-actions">
      ${t ? `<button class="ccb-action ccb-action--primary" data-act="open-thinker" data-thinker-id="${escape(tid)}">Open ${escape(thinkerName)} →</button>` : ""}
      <button class="ccb-action" data-act="open-source" data-thinker-id="${escape(tid)}" data-work-id="${escape(wid)}">Open in Source tab →</button>
    </div>
  `;

  const pendingBadge = isPending
    ? `<span class="ccb-pending-badge" title="The cited work is not yet on disk; context shown is the locus on which it comments.">Pending acquisition</span>`
    : (entry && entry.verified === false
        ? `<span class="ccb-pending-badge ccb-pending-badge--unverified" title="Passage IAST not located in the on-disk source.">Unverified</span>`
        : "");
  dpCitationBody.innerHTML = `
    <div class="ccb-head">
      <div class="ccb-locus">${escape(locusDisplay)} ${pendingBadge}</div>
      <div class="ccb-attrib">${escape(thinkerName)}${workTitle ? ` · <em>${escape(workTitle)}</em>` : ""}</div>
    </div>
    ${renderContext(before, "Preceding context")}
    ${anchorHtml}
    ${renderContext(after, "Following context")}
    ${noContextNote}
    ${actions}
  `;
  dpCitationBody.scrollTop = 0;

  dpCitationBody.querySelectorAll(".ccb-action").forEach((btn) => {
    btn.addEventListener("click", () => {
      const act = btn.dataset.act;
      if (act === "open-thinker") {
        openThinker(btn.dataset.thinkerId);
      } else if (act === "open-source") {
        const guess = guessSourceFileForCitation(btn.dataset.thinkerId, btn.dataset.workId);
        setPanelTab("source");
        if (guess) selectSourceFile(guess);
      }
    });
  });
}

// Pull preceding/following key_passages from the same thinker+work. The citation
// entry's `source` field points at thinker_jsons/<id>.json#key_passages[N]; we
// use that index when available, else match by locus.
function collectSurroundingPassages(tid, wid, entry) {
  const empty = { before: [], after: [] };
  const t = state.thinkersById.get(tid);
  if (!t || !Array.isArray(t.key_passages)) return empty;
  const sameWork = t.key_passages.filter((p) => p.work_id === wid);
  if (sameWork.length <= 1) return empty;
  let idx = -1;
  if (entry && entry.source) {
    const m = /key_passages\[(\d+)\]/.exec(entry.source);
    if (m) {
      const globalIdx = parseInt(m[1], 10);
      const target = t.key_passages[globalIdx];
      if (target) idx = sameWork.indexOf(target);
    }
  }
  if (idx < 0 && entry) {
    idx = sameWork.findIndex((p) =>
      (p.locus_short && entry.locus_short && p.locus_short === entry.locus_short) ||
      (p.locus_long && entry.locus && p.locus_long === entry.locus));
  }
  if (idx < 0) return empty;
  const N = 2;
  return {
    before: sameWork.slice(Math.max(0, idx - N), idx),
    after:  sameWork.slice(idx + 1, idx + 1 + N),
  };
}

// ---------- Source tab ----------
// The Source tab browses the in-repo primary-text mirror at
// `data/sources/`. The full corpus (~8 GB) lives outside the site repo;
// `scripts/build_site_sources.py` syncs only the files referenced by
// citation_index.json into `site/data/sources/`, and rewrites the manifest
// to reflect what is actually shipped to GitHub Pages. Thus the manifest +
// the fetch path must agree on `data/sources/<path>` (see fetch below).
const SOURCE_FETCH_BASE = "data/sources/";

async function ensureSourceTreeRendered() {
  if (sourceTabState.manifestLoaded) return;
  if (!dpSourceTree) return;
  dpSourceTree.innerHTML = "<p class=\"dp-empty\" style=\"padding:8px 14px\">Loading manifest…</p>";
  const m = await loadJSON("data/primary_text_manifest.json");
  sourceTabState.manifest = m;
  sourceTabState.manifestLoaded = true;
  if (!m || !Array.isArray(m.files) || m.files.length === 0) {
    dpSourceTree.innerHTML = "<p class=\"dp-empty\" style=\"padding:8px 14px\">No primary-text manifest found. Run scripts/build_site_sources.py.</p>";
    return;
  }
  renderSourceTree("");
  try {
    const last = localStorage.getItem("vedanta-cite-panel-source-file");
    if (last && m.files.some((f) => f.path === last)) selectSourceFile(last);
  } catch (_) {}
}

function renderSourceTree(filter) {
  const m = sourceTabState.manifest;
  if (!m || !Array.isArray(m.files)) return;
  const f = (filter || "").trim().toLowerCase();
  const files = f
    ? m.files.filter((fl) =>
        fl.path.toLowerCase().includes(f) ||
        (fl.title || "").toLowerCase().includes(f))
    : m.files;

  const groups = {};
  for (const fl of files) {
    const lang = fl.language || "other";
    const cat = fl.category || "_root";
    if (!groups[lang]) groups[lang] = {};
    if (!groups[lang][cat]) groups[lang][cat] = [];
    groups[lang][cat].push(fl);
  }

  const langOrder = ["sanskrit", "english", "german", "french", "latin", "tibetan"];
  const langs = Object.keys(groups).sort((a, b) => {
    const ai = langOrder.indexOf(a);
    const bi = langOrder.indexOf(b);
    return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi) || a.localeCompare(b);
  });

  const html = langs.map((lang) => {
    const cats = Object.keys(groups[lang]).sort();
    const catCount = cats.reduce((n, c) => n + groups[lang][c].length, 0);
    const catsHtml = cats.map((cat) => {
      const fls = groups[lang][cat].slice().sort((a, b) =>
        (a.title || a.path).localeCompare(b.title || b.path));
      const leaves = fls.map((fl) => {
        const label = fl.title || fl.path.split("/").pop().replace(/\.[^.]+$/, "");
        const isActive = fl.path === sourceTabState.activeFilePath ? " is-active" : "";
        return `<div class="cst-leaf${isActive}" data-path="${escape(fl.path)}" title="${escape(fl.path)}">${escape(label)}</div>`;
      }).join("");
      const catLabel = cat === "_root" ? "(top level)" : cat.replace(/_/g, " ");
      const open = f ? " open" : "";
      return `
        <details class="cst-group"${open}>
          <summary><span class="cst-group-label">${escape(catLabel)}</span><span class="cst-count">${fls.length}</span></summary>
          ${leaves}
        </details>
      `;
    }).join("");
    const open = f ? " open" : (lang === "sanskrit" ? " open" : "");
    return `
      <details class="cst-group"${open}>
        <summary><span class="cst-group-label">${escape(lang)}</span><span class="cst-count">${catCount}</span></summary>
        ${catsHtml}
      </details>
    `;
  }).join("");

  dpSourceTree.innerHTML = html || "<p class=\"dp-empty\" style=\"padding:8px 14px\">No matches.</p>";
  dpSourceTree.querySelectorAll(".cst-leaf").forEach((el) => {
    el.addEventListener("click", () => selectSourceFile(el.dataset.path));
  });
}

let _sourceSearchTimer = null;
if (dpSourceSearch) {
  dpSourceSearch.addEventListener("input", () => {
    clearTimeout(_sourceSearchTimer);
    _sourceSearchTimer = setTimeout(() => renderSourceTree(dpSourceSearch.value), 120);
  });
}

async function selectSourceFile(path) {
  if (!path) return;
  sourceTabState.activeFilePath = path;
  try { localStorage.setItem("vedanta-cite-panel-source-file", path); } catch (_) {}
  dpSourceTree.querySelectorAll(".cst-leaf").forEach((el) => {
    el.classList.toggle("is-active", el.dataset.path === path);
  });
  const meta = (sourceTabState.manifest && sourceTabState.manifest.files || []).find((f) => f.path === path) || {};
  dpSourceViewer.innerHTML = `
    <div class="csv-head">
      <p class="csv-title">${inlineMarkdown(meta.title || path.split("/").pop())}</p>
      <div class="csv-meta">
        <span>${escape(meta.language || "")}</span>
        ${meta.category ? `<span>${escape(meta.category)}</span>` : ""}
        ${meta.edition ? `<span>${escape(meta.edition)}</span>` : ""}
        ${meta.line_count ? `<span>${meta.line_count} lines</span>` : ""}
        ${meta.format ? `<span>${escape(meta.format)}</span>` : ""}
      </div>
    </div>
    <p class="csv-loading">Loading…</p>
  `;
  let text = sourceTabState.fileCache.get(path);
  if (text == null) {
    try {
      const r = await fetch(SOURCE_FETCH_BASE + path);
      text = r.ok ? await r.text() : "[failed to load — file not present in site/data/sources/]";
    } catch (_) {
      text = "[failed to load]";
    }
    sourceTabState.fileCache.set(path, text);
  }
  if (sourceTabState.activeFilePath !== path) return;

  // Decide rendering strategy from `format` (set by build_site_sources.py).
  // - markdown    → renderMarkdownFull (sanskrit-aside, GFM tables, headings)
  // - plain-text / text-with-locus-marker → render line-preserving with `# `
  //   headings promoted to <h2>/<h3> so users see styled headings, not raw
  //   `#` characters. We do NOT eat asterisks in plain text: they may be
  //   editorial markup (footnote markers in djvu OCR) the user wants verbatim.
  const fmt = (meta.format || "plain-text");
  const body = document.createElement("div");
  body.className = "csv-body" + (fmt === "markdown" ? " csv-body--md" : " csv-body--pre");
  if (fmt === "markdown") {
    body.innerHTML = renderMarkdownFull(text);
  } else {
    body.innerHTML = renderPlainSourceText(text);
  }
  const loading = dpSourceViewer.querySelector(".csv-loading");
  if (loading) loading.replaceWith(body);
  dpSourceViewer.scrollTop = 0;
  router.push({ kind: "source", thinkerId: state.activeId || "", sourcePath: path });
}

// Render a plain-text source: preserve linebreaks (most files in
// data/sources/ are line-oriented GRETIL verse text or djvu OCR), recognize
// `# Heading` / `## Subheading` lines so they render as styled headings, but
// leave content otherwise verbatim. Group consecutive verse lines into <pre>
// blocks separated by headings so the user can read in chunks.
//
// GRETIL Sanskrit files begin with a boilerplate `# Header` block (license,
// publisher, contribution metadata) before the actual `# Text`. The block
// is useful for provenance but visually overwhelms the reader landing on
// the file. We collapse it into a <details> element so the actual text is
// what the user reads first.
function renderPlainSourceText(text) {
  text = collapseGretilHeader(text || "");
  const lines = text.split(/\r?\n/);
  const out = [];
  let buf = [];
  const flush = () => {
    while (buf.length && !buf[buf.length - 1].trim()) buf.pop();
    if (!buf.length) return;
    out.push(`<pre class="csv-block">${escape(buf.join("\n"))}</pre>`);
    buf = [];
  };
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, "");
    if (line === "@@CSV_GRETIL_HEADER_PLACEHOLDER@@") {
      flush();
      out.push(_pendingGretilHeaderHtml);
      _pendingGretilHeaderHtml = "";
      continue;
    }
    const m = /^(#{1,4})\s+(.+)$/.exec(line);
    if (m) {
      flush();
      const level = Math.min(4, Math.max(2, m[1].length + 1));
      out.push(`<h${level} class="csv-heading">${inlineMarkdown(m[2])}</h${level}>`);
      continue;
    }
    buf.push(line);
  }
  flush();
  return out.join("\n");
}

let _pendingGretilHeaderHtml = "";
function collapseGretilHeader(text) {
  // Match the GRETIL `# Header` block: starts with `# Header` (anywhere in
  // first 400 chars) and ends right before the next top-level `# ` heading.
  const headIdx = text.search(/(^|\n)# Header\s*\n/);
  if (headIdx < 0 || headIdx > 600) return text;
  // Find the end: the next `\n# ` (a top-level heading other than this one).
  const after = text.indexOf("\n# ", headIdx + 8);
  if (after < 0) return text;
  const block = text.slice(headIdx, after).replace(/^\n/, "");
  const before = text.slice(0, headIdx);
  const remainder = text.slice(after + 1); // keep the leading `# ` for the next heading
  _pendingGretilHeaderHtml = `<details class="csv-gretil-header"><summary>GRETIL provenance &amp; license metadata</summary><pre class="csv-block">${escape(block)}</pre></details>`;
  return before + "@@CSV_GRETIL_HEADER_PLACEHOLDER@@\n" + remainder;
}

function guessSourceFileForCitation(thinkerId, workId) {
  const m = sourceTabState.manifest;
  if (!m || !Array.isArray(m.files)) return null;
  const tid = (thinkerId || "").toLowerCase();
  const wid = (workId || "").toLowerCase().replace(/-/g, "_");
  const score = (fl) => {
    const p = fl.path.toLowerCase();
    let s = 0;
    if (tid && p.includes(tid)) s += 3;
    if (wid && p.includes(wid)) s += 5;
    if (fl.language === "sanskrit") s += 1;
    return s;
  };
  let best = null;
  let bestScore = 0;
  for (const fl of m.files) {
    const s = score(fl);
    if (s > bestScore) { bestScore = s; best = fl; }
  }
  return bestScore >= 3 ? best.path : null;
}

// ---------- markdown helpers -----------
function escape(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

// Inline-only markdown for short strings (titles, headwords, attributions,
// locus labels). Renders **bold** → <strong>, *italic* → <em>, _italic_ → <em>,
// `code` → <code>. HTML-escapes everything else. No paragraph splitting, no
// block elements, no glossary tagging — keep it cheap and predictable. Use
// for any short string that comes from a JSON manifest authored with markdown
// emphasis (most of them).
function inlineMarkdown(s) {
  if (s == null) return "";
  let out = escape(s);
  out = out.replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>");
  out = out.replace(/(^|[\s(\[])_([^_\n\s][^_\n]*?[^_\n\s]|[^_\n\s])_(?=[\s).,!?;:\]]|$)/g, "$1<em>$2</em>");
  out = out.replace(/`([^`\n]+?)`/g, "<code>$1</code>");
  return out;
}

// Pre-escape pass that rewrites two informal citation idioms into the
// canonical `[X](cite://Y)` form so the downstream URL regex can match them.
//
//   1. Angle-bracketed URLs        → `(<cite://X>)`   → `(cite://X)`
//      (markdown "autolink" punctuation that some authors typed when the URL
//      contains parens or whitespace; the angle brackets serve no purpose
//      here because the renderer already tolerates those characters.)
//   2. Footnote-bracket idiom      → `[[X](cite://Y)]` → `[X](cite://Y)`
//      (and chained variants like `[[X](cite://Y); [W](cite://Z)]`.) The
//      outer brackets become noise once the visible text is replaced by a
//      numbered superscript footnote downstream, so strip them up front.
//
// The transformation runs in source space (before HTML-escaping). It only
// touches text that already contains a `(cite://…)` URL, so non-citation
// prose is never altered.
function normalizeCitationSyntax(s) {
  if (s == null) return s;
  let out = String(s);
  out = out.replace(/\(<\s*(cite:\/\/[^>\n]+?)\s*>\)/g, "($1)");
  out = out.replace(
    /\[((?:\[[^\]]+?\]\(cite:\/\/[^)\n]+\)(?:[;,]?\s*)?)+)\]/g,
    "$1",
  );
  return out;
}

function md(s) {
  if (s == null) return "";
  // Normalize the two citation idioms before escaping so the URL regex can be
  // anchored on the literal `(cite://…)`:
  //   • angle-bracketed URLs  → `[X](<cite://…>)`  (markdown autolink form)
  //   • footnote-style outer brackets → `[[X](cite://…)]` (and chained variants)
  // Both forms appear in the on-disk JSON and were rendered as raw markdown
  // before this normalization was added.
  s = normalizeCitationSyntax(s);
  let out = escape(s);
  // Bold first (longer match), then italic. Inline-italic uses lookbehind/lookahead
  // to forbid whitespace adjacent to the asterisk (avoids math-like "2 * 3"),
  // but does NOT require surrounding punctuation — so "*foo*-bar" or "(*foo*)" both work.
  out = out.replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>");
  out = out.replace(/`([^`]+?)`/g, "<code>$1</code>");
  // Citation links: [visible](cite://thinker/work/locus). Stash the rendered
  // anchor in a placeholder so the glossary-regex pass below cannot tag tokens
  // inside the href (which would break the markup).
  const citeStash = [];
  out = out.replace(
    /\[([^\]]+?)\]\(cite:\/\/([^)\n]+)\)/g,
    (_m, visible, key) => {
      const i = citeStash.length;
      citeStash.push({ visible, key });
      return `CITE${i}`;
    },
  );
  // glossary tagging — wrap matched terms in clickable spans (after italics so we don't double-wrap inside <em>)
  if (state.glossaryRegex) {
    out = out.replace(state.glossaryRegex, (m, _g, offset, full) => {
      return `<span class="term" data-term="${escape(m)}">${m}</span>`;
    });
  }
  // Re-inflate citation links. The visible text was already HTML-escaped and
  // had italics applied; the key is HTML-safe (no entities expected).
  out = out.replace(/CITE(\d+)/g, (_m, i) => {
    const c = citeStash[+i];
    return `<a href="cite://${c.key}" class="cite-link">${c.visible}</a>`;
  });
  return out;
}

// Post-process rendered HTML: convert in-prose `<a class="cite-link" href="cite://…">…</a>`
// into a bare superscript `<sup class="cite-fn">[N]</sup>` link. The inline
// visible text is DROPPED — the locus information lives in the footnote list
// at the end of the block and in the Citation tab popover, not duplicated
// inline. This produces clean prose like "…against *avidyā*[1], including…"
// rather than "…against *avidyā* (Śruta-Prakāśikā on Śrī-Bhāṣya 1.1.1)[1]…".
//
// If the same cite key recurs in one passage, the same number is reused
// (cf. how scholarly footnotes treat repeated loci). The N counter is local
// to one call — pass a shared counter object across multiple prose blocks
// for continuous numbering across a section. Returns `{ html, footnotes }`
// so the caller can choose where to render the footnote list.
//
// A small grammatical clean-up runs after substitution: when the dropped
// visible text was wrapped in parentheses ("(see [Foo 1.1](cite://...))"),
// the surrounding parens become orphans ("()") — we strip these, along with
// dangling separators that bordered the dropped text.
function numberCitations(html, counter) {
  if (!html) return { html: "", footnotes: [] };
  const ctr = counter || { n: 0 };
  const footnotes = [];
  // Track keys already seen in this counter run so repeated cites reuse N.
  const keyToIdx = new Map();
  // Match any `<a … class="cite-link" …>…</a>`. Attribute order is not fixed
  // (md() emits `href` first; renderMarkdownFull may emit the class first).
  let out = html.replace(
    /<a\b([^>]*?\bclass="[^"]*\bcite-link\b[^"]*"[^>]*)>([\s\S]*?)<\/a>/g,
    (m, attrs, visible) => {
      const hrefMatch = /href="cite:\/\/([^"]+)"/.exec(attrs);
      if (!hrefMatch) return m;
      const key = hrefMatch[1];
      let idx = keyToIdx.get(key);
      if (idx == null) {
        ctr.n += 1;
        idx = ctr.n;
        keyToIdx.set(key, idx);
        footnotes.push({ idx, key, visible });
      }
      return `<sup class="cite-fn"><a href="cite://${key}" class="cite-fn-link" data-fn-idx="${idx}" aria-label="Footnote ${idx}">[${idx}]</a></sup>`;
    }
  );
  // Cleanup: many existing prose passages wrapped the (now-empty) inline cite
  // text in editorial parentheses, e.g. "(Śruta-Prakāśikā on [Śrī-Bhāṣya
  // 1.1.1](cite://...), Mahā-Siddhānta)". After dropping the visible text we
  // can be left with patterns like "( <sup>...</sup>, foo)" or "( <sup>...
  // </sup>)". When what remains inside the parens is purely a run of
  // superscript footnotes plus whitespace and short connective separators,
  // collapse to the superscripts alone.
  out = out.replace(
    /\(\s*((?:(?:see\s+|cf\.\s*|,\s*|;\s*|and\s+)*<sup class="cite-fn">[\s\S]*?<\/sup>\s*)+)\)/g,
    (_m, inner) => inner.trim(),
  );
  // Collapse orphan separators left adjacent to the superscripts.
  out = out.replace(/\(\s*,\s*/g, "(");
  out = out.replace(/,\s*\)/g, ")");
  out = out.replace(/\(\s*\)/g, "");
  // Tidy double spaces produced by the strip.
  out = out.replace(/[ \t]{2,}/g, " ");
  out = out.replace(/\s+([,.;:])/g, "$1");
  return { html: out, footnotes };
}

// Render a tidy footnote list, given the array produced by numberCitations.
// Each row is a numbered locus that links back into the Citation tab.
function renderFootnoteList(footnotes) {
  if (!footnotes || !footnotes.length) return "";
  const rows = footnotes.map((f) => {
    const parts = f.key.split("/");
    const tid = parts[0] || "";
    const wid = parts[1] || "";
    const loc = parts.slice(2).join("/");
    const t = state.thinkersById.get(tid);
    const thinkerName = t ? (t.name_iast || t.name || tid) : tid;
    let workTitle = wid;
    if (t) {
      const w = (t.engaged_works || []).find((x) => x.work_id === wid);
      if (w) workTitle = w.title_iast || w.title || wid;
    }
    return `<li class="cite-fn-row" id="cite-fn-${f.idx}">`
      + `<span class="cite-fn-num">[${f.idx}]</span>`
      + `<span class="cite-fn-body">`
      + `<a href="cite://${f.key}" class="cite-link cite-fn-rowlink">`
      + `<em>${escape(workTitle)}</em> ${escape(loc)}`
      + `</a>`
      + `<span class="cite-fn-attrib"> — ${escape(thinkerName)}</span>`
      + `</span>`
      + `</li>`;
  }).join("");
  return `<div class="cite-fn-wrap">`
    + `<p class="cite-fn-head">Footnotes</p>`
    + `<ol class="cite-fn-list">${rows}</ol>`
    + `</div>`;
}

function renderMarkdownListBlock(block) {
  const lines = block.trim().split("\n");
  if (!lines.length) return block;
  const ordered = /^\s*\d+\.\s+/.test(lines[0]);
  const itemRe = ordered ? /^\s*\d+\.\s+([\s\S]+)$/ : /^\s*[-+*]\s+([\s\S]+)$/;
  const items = [];
  let current = null;
  for (const line of lines) {
    const m = line.match(itemRe);
    if (m) {
      if (current != null) items.push(current.trim());
      current = m[1];
    } else if (current != null) {
      current += " " + line.trim();
    }
  }
  if (current != null) items.push(current.trim());
  if (!items.length) return block;
  const html = items.map((item) => {
    const escaped = item
      .replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]))
      .replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>")
      .replace(/`([^`]+?)`/g, "<code>$1</code>");
    return `<li>${escaped}</li>`;
  }).join("");
  return ordered ? `<ol>${html}</ol>` : `<ul>${html}</ul>`;
}

function renderMarkdownParagraphs(src) {
  return src
    .split(/\n{2,}/)
    .map((block) => {
      const trimmed = block.trim();
      if (!trimmed) return "";
      if (/^<(?:h[1-6]|blockquote|pre|ul|ol|div\b|table\b|hr\b)/.test(trimmed)) return trimmed;
      return `<p>${trimmed.replace(/\n+/g, "<br>")}</p>`;
    })
    .filter(Boolean)
    .join("\n");
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
  if (readingModeBtn) {
    const txt = readingModeBtn.querySelector(".btn-text");
    const label = on ? "Back to timeline" : "Reading";
    if (txt) txt.textContent = label;
    else readingModeBtn.textContent = label;
    readingModeBtn.setAttribute("aria-label", on ? "Back to timeline" : "Reading mode");
    readingModeBtn.classList.toggle("is-active", on);
  }
  if (on && !state.activeId && state.thinkers.length) {
    const sorted = [...state.thinkers].sort((a, b) => (a.dates_low + a.dates_high)/2 - (b.dates_low + b.dates_high)/2);
    openThinker(sorted[0].id);
  }
}
if (readingModeBtn) {
  readingModeBtn.addEventListener("click", () => {
    const on = !document.body.classList.contains("is-reading-mode");
    setReadingMode(on);
  });
}

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
const filterSoloPill = document.getElementById("filterSoloPill");

// All toggleable lane keys (Vedānta schools + the comparator group).
function allLaneKeys() {
  const keys = [];
  for (const tok of LANE_ORDER) {
    if (VEDANTA_LANES.has(tok)) keys.push(tok);
  }
  keys.push(COMPARATOR_GROUP_KEY);
  return keys;
}

function laneDisplayLabel(key) {
  if (key === COMPARATOR_GROUP_KEY) return COMPARATOR_GROUP_LABEL;
  return state.schools[key]?.display_name || LANE_DISPLAY[key] || key;
}

// "Solo" = exactly one lane is currently visible. Returns its key, or null.
function currentSoloKey() {
  if (state.visibleLanes.size !== 1) return null;
  const [only] = state.visibleLanes;
  return only;
}

function updateSoloIndicator() {
  if (!filterSoloPill) return;
  const solo = currentSoloKey();
  if (solo) {
    filterSoloPill.hidden = false;
    filterSoloPill.textContent = `Solo: ${laneDisplayLabel(solo)}`;
    filterSoloPill.setAttribute("aria-label", `Showing only ${laneDisplayLabel(solo)}. Click to show all.`);
  } else {
    filterSoloPill.hidden = true;
    filterSoloPill.textContent = "";
  }
}

function renderFilterChips() {
  if (!filterChipsEl) return;
  filterChipsEl.innerHTML = "";

  // Preset row (named presets).
  const presets = document.createElement("div");
  presets.className = "filter-chip-row";
  presets.innerHTML = `
    <button class="filter-chip filter-chip--preset" data-preset="vedanta" type="button">Vedānta only</button>
    <button class="filter-chip filter-chip--preset" data-preset="all" type="button">All schools</button>
    <button class="filter-chip filter-chip--preset" data-preset="comparators" type="button">Comparators only</button>
  `;
  filterChipsEl.appendChild(presets);

  // Bulk-action row (deselect/select all). Plain text-buttons, no chip swatches.
  const bulkRow = document.createElement("div");
  bulkRow.className = "filter-chip-row filter-bulk-row";
  bulkRow.innerHTML = `
    <button class="filter-bulk-btn" data-bulk="none" type="button">Deselect all</button>
    <button class="filter-bulk-btn" data-bulk="all" type="button">Select all</button>
  `;
  filterChipsEl.appendChild(bulkRow);

  // Per-school chips: each chip has a main toggle and a small "solo" affordance.
  const chipsRow = document.createElement("div");
  chipsRow.className = "filter-chip-row";
  const makeChip = (key, label, color) => {
    const on = state.visibleLanes.has(key);
    const wrap = document.createElement("span");
    wrap.className = "filter-chip-wrap" + (on ? " is-on" : "");

    const btn = document.createElement("button");
    btn.className = "filter-chip" + (on ? " is-on" : "");
    btn.dataset.lane = key;
    btn.type = "button";
    btn.style.setProperty("--chip-color", color);
    btn.innerHTML = `<span class="chip-swatch"></span>${escape(label)}`;
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (state.visibleLanes.has(key)) state.visibleLanes.delete(key);
      else state.visibleLanes.add(key);
      rerender();
    });

    const solo = document.createElement("button");
    solo.className = "filter-chip-solo";
    solo.type = "button";
    solo.dataset.solo = key;
    solo.setAttribute("aria-label", `Show only ${label}`);
    solo.title = `Show only ${label}`;
    solo.textContent = "solo";
    solo.addEventListener("click", (e) => {
      e.stopPropagation();
      state.visibleLanes.clear();
      state.visibleLanes.add(key);
      if (key === COMPARATOR_GROUP_KEY) state.comparatorExpanded = true;
      rerender();
    });

    wrap.appendChild(btn);
    wrap.appendChild(solo);
    return wrap;
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
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
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

  // Wire bulk actions.
  filterChipsEl.querySelectorAll("[data-bulk]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const action = btn.dataset.bulk;
      state.visibleLanes.clear();
      if (action === "all") {
        for (const k of allLaneKeys()) state.visibleLanes.add(k);
      }
      rerender();
    });
  });

  updateSoloIndicator();
}

function closeFilterDrawer() {
  if (!filterDrawer) return;
  filterDrawer.classList.remove("is-open");
  filterDrawer.setAttribute("aria-hidden", "true");
  if (filterBtn) filterBtn.classList.remove("is-active");
}

if (filterBtn) {
  filterBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    const open = filterDrawer.classList.toggle("is-open");
    filterDrawer.setAttribute("aria-hidden", open ? "false" : "true");
    filterBtn.classList.toggle("is-active", open);
  });
  // Stop drawer-internal clicks from bubbling to the document handler. This is
  // load-bearing: chip clicks call rerender(), which rebuilds the chip DOM.
  // By the time the bubbling click reaches `document`, e.target is detached
  // and `filterDrawer.contains(e.target)` is false, so the outside-click
  // branch would otherwise (incorrectly) close the drawer.
  if (filterDrawer) {
    filterDrawer.addEventListener("click", (e) => { e.stopPropagation(); });
  }
  // Close drawer on outside click only.
  document.addEventListener("click", (e) => {
    if (!filterDrawer.classList.contains("is-open")) return;
    if (filterDrawer.contains(e.target) || filterBtn.contains(e.target)) return;
    closeFilterDrawer();
  });
  // Close on Esc.
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (!filterDrawer.classList.contains("is-open")) return;
    closeFilterDrawer();
  });
}

// Clicking the solo pill restores the full default selection.
if (filterSoloPill) {
  filterSoloPill.addEventListener("click", (e) => {
    e.stopPropagation();
    state.visibleLanes.clear();
    for (const t of VEDANTA_LANES) state.visibleLanes.add(t);
    state.visibleLanes.add(COMPARATOR_GROUP_KEY);
    rerender();
  });
}

// ---------- topbar glossary search -----------
// Type-to-search over the loaded glossary. The same `openGlossary(termKey,
// anchorEl)` path that powers in-prose terms is reused, so the popover
// presentation is identical (including the surface-form / canonical-form
// header). The search input becomes the anchorEl, which keeps positioning
// sensible on desktop and lets the bottom-sheet behaviour fire on mobile.
const topbarSearchInput = document.getElementById("topbarSearchInput");
const topbarSearchResults = document.getElementById("topbarSearchResults");
const topbarSearchWrap = document.getElementById("topbarSearch");

// Normalises diacritics so "atman" matches "ātman". This is a coverage helper
// for the search field only — it does NOT alter the glossary regex used by
// the autolink pass.
function normalizeDia(s) {
  return String(s || "")
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase();
}

function topbarSearchCandidates() {
  const seen = new Set();
  const out = [];
  for (const [key, entry] of state.glossary) {
    // Skip aliases that point to the same canonical so we don't list
    // every form separately.
    const canonical = entry.term_iast || entry.term_key || key;
    if (seen.has(canonical)) continue;
    seen.add(canonical);
    out.push({
      key,
      canonical,
      literal: entry.literal || "",
      // First sentence of the invariant — used as the secondary line.
      blurb: (entry.invariant_definition || "").split(/[.\n]/)[0].slice(0, 90),
    });
  }
  return out;
}

let topbarSearchIndex = null;
function ensureTopbarSearchIndex() {
  if (topbarSearchIndex) return topbarSearchIndex;
  topbarSearchIndex = topbarSearchCandidates().map((c) => ({
    ...c,
    norm: normalizeDia(c.canonical),
    normLiteral: normalizeDia(c.literal),
  }));
  return topbarSearchIndex;
}

function renderTopbarSearchResults(q) {
  if (!topbarSearchResults) return;
  ensureTopbarSearchIndex();
  const norm = normalizeDia(q);
  if (!norm) {
    topbarSearchResults.hidden = true;
    topbarSearchResults.innerHTML = "";
    return;
  }
  // Two-tier ranking: prefix matches first, substring matches after. Cap
  // at 30 so the list stays scannable; the user can narrow further.
  const prefix = [];
  const sub = [];
  for (const c of topbarSearchIndex) {
    if (c.norm.startsWith(norm)) prefix.push(c);
    else if (c.norm.includes(norm) || c.normLiteral.includes(norm)) sub.push(c);
    if (prefix.length + sub.length >= 60) break;
  }
  const rows = prefix.concat(sub).slice(0, 30);
  if (!rows.length) {
    topbarSearchResults.innerHTML = `<p class="topbar-search-empty">No glossary entries match "${escape(q)}".</p>`;
    topbarSearchResults.hidden = false;
    return;
  }
  topbarSearchResults.innerHTML = rows.map((r, i) => `
    <button class="topbar-search-result${i === 0 ? " is-active" : ""}" data-key="${escape(r.key)}" type="button" role="option">
      <span class="ts-term">${escape(r.canonical)}</span>
      ${r.literal ? `<span class="ts-gloss">${escape(r.literal)}</span>` : (r.blurb ? `<span class="ts-gloss">${escape(r.blurb)}</span>` : "")}
    </button>
  `).join("");
  topbarSearchResults.hidden = false;
}

function closeTopbarSearch() {
  if (topbarSearchResults) {
    topbarSearchResults.hidden = true;
    topbarSearchResults.innerHTML = "";
  }
}

if (topbarSearchInput && topbarSearchResults && topbarSearchWrap) {
  topbarSearchInput.addEventListener("input", () => {
    renderTopbarSearchResults(topbarSearchInput.value);
  });
  topbarSearchInput.addEventListener("focus", () => {
    if (topbarSearchInput.value) renderTopbarSearchResults(topbarSearchInput.value);
  });
  // Keyboard navigation: ArrowDown/Up moves selection, Enter opens.
  topbarSearchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      topbarSearchInput.value = "";
      closeTopbarSearch();
      topbarSearchInput.blur();
      return;
    }
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp" && e.key !== "Enter") return;
    const items = topbarSearchResults.querySelectorAll(".topbar-search-result");
    if (!items.length) return;
    let activeIdx = -1;
    items.forEach((el, i) => { if (el.classList.contains("is-active")) activeIdx = i; });
    if (e.key === "Enter") {
      e.preventDefault();
      const target = activeIdx >= 0 ? items[activeIdx] : items[0];
      if (target) target.click();
      return;
    }
    e.preventDefault();
    let nextIdx = activeIdx;
    if (e.key === "ArrowDown") nextIdx = (activeIdx + 1) % items.length;
    if (e.key === "ArrowUp") nextIdx = (activeIdx - 1 + items.length) % items.length;
    items.forEach((el, i) => el.classList.toggle("is-active", i === nextIdx));
    items[nextIdx].scrollIntoView({ block: "nearest" });
  });
  topbarSearchResults.addEventListener("click", (e) => {
    const btn = e.target.closest(".topbar-search-result");
    if (!btn) return;
    const key = btn.dataset.key;
    closeTopbarSearch();
    openGlossary(key, topbarSearchInput);
  });
  // Outside click closes the results panel.
  document.addEventListener("click", (e) => {
    if (topbarSearchResults.hidden) return;
    if (topbarSearchWrap.contains(e.target)) return;
    if (e.target.closest(".glossary-popover")) return;
    closeTopbarSearch();
  });
}

// ---------- about modal -----------
const aboutBtn = document.getElementById("aboutBtn");
const aboutModal = document.getElementById("aboutModal");
const closeAbout = document.getElementById("closeAbout");
aboutBtn.addEventListener("click", () => { popoverManager.closeAll(); aboutModal.classList.add("is-open"); aboutModal.setAttribute("aria-hidden", "false"); });
closeAbout.addEventListener("click", () => { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); });
aboutModal.addEventListener("click", (e) => {
  if (e.target === aboutModal) { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); }
});

// ---------- articles -----------
const articlesBtn = document.getElementById("articlesBtn");
const articlesModal = document.getElementById("articlesModal");
const closeArticles = document.getElementById("closeArticles");
const articlesList = document.getElementById("articlesList");

let articlesManifest = null;

async function ensureArticlesLoaded() {
  if (articlesManifest) return;
  articlesManifest = await loadJSON("data/articles/manifest.json");
  if (!articlesManifest || !articlesManifest.articles) {
    articlesList.innerHTML = "<p class=\"articles-intro\">No articles yet.</p>";
    return;
  }
  articlesList.innerHTML = "";
  // Hide superseded articles; only show the latest of each lineage.
  const visible = articlesManifest.articles.filter((a) => a.status !== "superseded");
  // Five user-facing buckets. Superseded `perspective-investigation` drafts are
  // hidden by the `status === "superseded"` filter above; the kind label is kept
  // on disk for the historical record but does not surface as a section.
  const sectionOrder = ["perspective", "essay", "comparative", "framework", "methodology", "engagement", "other"];
  const sectionLabels = {
    "perspective": "Perspectives",
    "essay": "Per-thinker engagements",
    "comparative": "Comparative readings",
    "framework": "Frameworks & methodology",
    "methodology": "Frameworks & methodology",
    "engagement": "Text engagements",
    "other": "Other",
  };
  const sectionBlurbs = {
    "perspective": "Explicit user-position-driven readings. Flagged with the PERSPECTIVE pill and a reading-discipline preamble.",
    "essay": "Sustained reading-sessions through one thinker's primary corpus, in source language where it matters.",
    "comparative": "Paired analyses across thinkers and schools.",
    "framework": "Methodological documents underwriting the comparative work.",
    "methodology": "Methodological documents underwriting the comparative work.",
    "engagement": "Sustained walk-throughs of one Sanskrit primary work, with locus, IAST, and close English at every load-bearing passage.",
  };
  const groups = {};
  for (const a of visible) {
    const k = sectionOrder.includes(a.kind) ? a.kind : "other";
    (groups[k] = groups[k] || []).push(a);
  }
  // Sections we've already rendered (so collapsed labels like
  // framework / methodology don't print twice).
  const renderedLabels = new Set();
  for (const k of sectionOrder) {
    if (!groups[k] || !groups[k].length) continue;
    const label = sectionLabels[k];
    if (!renderedLabels.has(label)) {
      const head = document.createElement("div");
      head.className = "articles-section-head";
      head.innerHTML = `<p class="articles-section-title">${escape(label)}</p>${sectionBlurbs[k] ? `<p class="articles-section-blurb">${escape(sectionBlurbs[k])}</p>` : ""}`;
      articlesList.appendChild(head);
      renderedLabels.add(label);
    }
    for (const a of groups[k]) {
      const row = document.createElement("div");
      row.className = "article-row";
      row.dataset.slug = a.slug;
      const pillHTML = a.kind === "perspective" ? '<span class="perspective-pill perspective-pill--inline">PERSPECTIVE</span> ' : "";
      row.innerHTML = `
        <p class="article-title">${pillHTML}${md(a.title)}${a.status === "in-progress" ? ' <em style="color:#92400e;font-weight:500">(in progress)</em>' : ""}</p>
        ${a.subtitle ? `<p class="article-subtitle">${md(a.subtitle)}</p>` : ""}
        <p class="article-meta">${a.word_count_approx ? "~" + a.word_count_approx.toLocaleString() + " words" : ""}${a.date ? " · " + escape(a.date) : ""}</p>
      `;
      row.addEventListener("click", () => openArticle(a));
      articlesList.appendChild(row);
    }
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
  // Articles render in the unified panel's Article tab. The articles
  // chooser modal closes on selection (the user picked one already).
  articlesModal.classList.remove("is-open");
  articlesModal.setAttribute("aria-hidden", "true");
  showTab("article");
  if (dpArticleHead) {
    const pill = a.kind === "perspective"
      ? '<span class="perspective-pill perspective-pill--inline">PERSPECTIVE</span> '
      : "";
    const eyebrowKind = a.kind === "perspective" ? "Perspective" : (a.kind || "Article");
    dpArticleHead.innerHTML = `
      <p class="dp-eyebrow">${escape(eyebrowKind.charAt(0).toUpperCase() + eyebrowKind.slice(1))}</p>
      <p class="dp-title">${pill}${md(a.title)}</p>
      ${a.subtitle ? `<p class="dp-attrib">${md(a.subtitle)}</p>` : ""}
    `;
  }
  if (dpArticleBody) dpArticleBody.innerHTML = "<article><p style=\"color:var(--muted);font-style:italic\">Loading…</p></article>";
  openPanel("article");

  const path = a.source_doc || (a.kind === "perspective"
    ? `data/perspectives/source/${a.slug}.md`
    : `data/articles/source/${a.slug}.md`);
  const r = await fetch(path);
  if (!r.ok) {
    if (dpArticleBody) dpArticleBody.innerHTML = `<article><h1>${md(a.title)}</h1><p>Article body not yet uploaded.</p></article>`;
    return;
  }
  const text = await r.text();
  if (dpArticleBody) {
    // Render the article body, then post-process the rendered HTML to turn
    // inline `<a class="cite-link">` anchors into superscript footnote links
    // and append a footnote list at the bottom. One counter for the whole
    // article so numbering is continuous (parity with the thinker pipeline).
    const articleCtr = { n: 0 };
    const articleR = numberCitations(renderMarkdownFull(text), articleCtr);
    const fnList = renderFootnoteList(articleR.footnotes);
    dpArticleBody.innerHTML = `<article>${articleR.html}${fnList}</article>`;
    dpArticleBody.scrollTop = 0;
  }
  panelState.loaded.article = true;
  router.push({ kind: a.kind === "perspective" ? "perspective" : "article", slug: a.slug });
}

// Markdown renderer for the article reader. Beyond standard inline markdown +
// GFM tables + fenced code, this renderer:
//  (1) parses the project-local `::: sanskrit-aside` block convention and
//      emits a side-by-side panel that collapses to stacked at <=720 px;
//  (2) tags glossary terms with <span class="term"> so the global delegation
//      handler can open the glossary popover (parity with thinker prose);
//  (3) preserves cite:// links so the citation popover / panel handler fires.
function renderMarkdownFull(src) {
  // Normalize informal citation idioms (`(<cite://X>)`, `[[X](cite://Y)]`)
  // into the canonical `[X](cite://Y)` form before any escaping runs. The
  // pass is idempotent and only rewrites text that already contains a
  // `cite://` URL, so plain prose is untouched.
  src = normalizeCitationSyntax(src);
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  // Sanskrit-aside blocks — extracted before any other processing so the inner
  // panes can be rendered recursively without any of the outer-pass regexes
  // touching them.
  const asides = [];
  // The convention accepts ":::: <lang>" as the label for the left pane.
  // Recognised lang tokens: sanskrit, german, french, latin, greek, pali,
  // tibetan, arabic, hebrew. Anything else is rendered as-is, capitalised.
  src = src.replace(/^::: sanskrit-aside\s*\n([\s\S]*?)\n:::\s*$/gm, (_m, body) => {
    const langMatch = body.match(/^:::: (sanskrit|german|french|latin|greek|pali|tibetan|arabic|hebrew)\s*\n/i);
    const sourceLang = langMatch ? langMatch[1].toLowerCase() : "sanskrit";
    const skRe = new RegExp(":::: " + sourceLang + "\\s*\\n([\\s\\S]*?)(?=\\n:::: english|\\s*$)", "i");
    const skMatch = body.match(skRe);
    const enMatch = body.match(/:::: english\s*\n([\s\S]*?)$/i);
    const sk = skMatch ? skMatch[1].trim() : "";
    const en = enMatch ? enMatch[1].trim() : "";
    asides.push({ sk, en, sourceLang });
    return ` SKASIDE${asides.length - 1} `;
  });
  // Pull out fenced code blocks (preserve verbatim).
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
    return `<div class="md-table-wrap"><table><thead><tr>${head.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${body.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  });
  // Thematic breaks and contiguous markdown list blocks.
  src = src.replace(/^(?:-{3,}|\*{3,}|_{3,})\s*$/gm, "<hr>");
  src = src.replace(/((?:^\s*(?:[-+*]|\d+\.)\s+.+(?:\n|$))+)/gm, (m) => renderMarkdownListBlock(m));
  // Stash citation + plain links *before* paragraph-splitting and glossary-
  // tagging, so the tagger cannot touch tokens inside an href or anchor text.
  const citeStash = [];
  src = src.replace(
    /\[([^\]]+?)\]\(cite:\/\/([^)\n]+)\)/g,
    (_m, visible, key) => {
      const i = citeStash.length;
      citeStash.push({ visible, key });
      return ` CITESTASH${i} `;
    },
  );
  const linkStash = [];
  src = src.replace(
    /\[([^\]]+?)\]\(([^)\n]+)\)/g,
    (_m, visible, href) => {
      const i = linkStash.length;
      linkStash.push({ visible, href });
      return ` LINKSTASH${i} `;
    },
  );
  // Standard markdown
  let out = src
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    .replace(/^&gt; (.+)$/gm, "<blockquote>$1</blockquote>")
    .replace(/^> (.+)$/gm, "<blockquote>$1</blockquote>")
    .replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(?!\s)([^*\n]+?)(?<!\s)\*/g, "<em>$1</em>")
    .replace(/`([^`]+?)`/g, "<code>$1</code>");
  out = renderMarkdownParagraphs(out);
  // Glossary tagging — parity with the thinker-prose md() path. Done
  // after italics so we do not double-wrap inside <em>; before re-inflating
  // the citation/link placeholders so we do not tag inside href text.
  if (state.glossaryRegex) {
    out = out.replace(state.glossaryRegex, (m) => `<span class="term" data-term="${escape(m)}">${m}</span>`);
  }
  // Re-inflate citation + link placeholders.
  out = out.replace(/ CITESTASH(\d+) /g, (_m, i) => {
    const c = citeStash[+i];
    return `<a href="cite://${c.key}" class="cite-link">${c.visible}</a>`;
  });
  out = out.replace(/ LINKSTASH(\d+) /g, (_m, i) => {
    const l = linkStash[+i];
    return `<a href="${l.href}" target="_blank" rel="noopener">${l.visible}</a>`;
  });
  // restore code blocks and sanskrit-aside blocks
  out = out.replace(/ BLOCK(\d+) /g, (_, i) => blocks[+i]);
  out = out.replace(/ SKASIDE(\d+) /g, (_, i) => {
    const a = asides[+i];
    // Recursively render each pane so inline markdown / cite links / glossary
    // tagging work inside the panes.
    const langLabel = a.sourceLang ? a.sourceLang[0].toUpperCase() + a.sourceLang.slice(1) : "Sanskrit";
    return `<div class="sk-aside"><div class="sk-aside-pane sk-aside-sanskrit"><div class="sk-aside-label">${langLabel}</div>${renderMarkdownFull(a.sk)}</div><div class="sk-aside-pane sk-aside-english"><div class="sk-aside-label">English</div>${renderMarkdownFull(a.en)}</div></div>`;
  });
  // Don't wrap headings / blockquotes / tables / asides in <p>.
  out = out.replace(/<p>(\s*)(<h[123]|<blockquote|<div class="md-table-wrap"|<table|<pre|<ul|<ol|<div class="sk-aside|<hr)/g, "$1$2");
  out = out.replace(/(<\/h[123]>|<\/blockquote>|<\/div>|<\/table>|<\/pre>|<\/ul>|<\/ol>|<hr>)(\s*)<\/p>/g, "$1$2");
  return out;
}

// ---------- keyboard nav -----------
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (articlesModal.classList.contains("is-open")) {
      articlesModal.classList.remove("is-open");
      articlesModal.setAttribute("aria-hidden", "true");
    } else if (aboutModal.classList.contains("is-open")) {
      aboutModal.classList.remove("is-open");
      aboutModal.setAttribute("aria-hidden", "true");
    } else if (document.body.classList.contains("is-reading-mode")) {
      setReadingMode(false);
    } else if (panelState.open) {
      closePanel();
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

// ---------- detail-pane resize handle -----------
// Lets the user drag the left edge of the right-side panel to widen or
// narrow it. The chosen width persists across reloads via localStorage.
// Bounds: [360, viewport - 320 minimum canvas]. The CSS grid template
// falls back to the original clamp when no width is set.
function wireDetailPaneResize() {
  if (!detailPane) return;
  let handle = detailPane.querySelector(".dp-resize-handle");
  if (!handle) {
    handle = document.createElement("div");
    handle.className = "dp-resize-handle";
    handle.setAttribute("role", "separator");
    handle.setAttribute("aria-orientation", "vertical");
    handle.setAttribute("aria-label", "Resize panel");
    handle.tabIndex = -1;
    detailPane.insertBefore(handle, detailPane.firstChild);
  }

  function applyWidth(px) {
    const vw = window.innerWidth;
    const min = 360;
    const max = Math.max(min, vw - 320);
    const clamped = Math.min(max, Math.max(min, px));
    document.body.style.setProperty("--pane-w-detail", clamped + "px");
    return clamped;
  }

  try {
    const saved = parseFloat(localStorage.getItem("dp-width-px"));
    if (Number.isFinite(saved) && saved > 0) applyWidth(saved);
  } catch (_) {}

  let dragging = false;
  let startX = 0;
  let startW = 0;
  handle.addEventListener("pointerdown", (e) => {
    dragging = true;
    startX = e.clientX;
    startW = detailPane.getBoundingClientRect().width;
    try { handle.setPointerCapture(e.pointerId); } catch (_) {}
    handle.classList.add("is-dragging");
    document.body.classList.add("is-resizing-pane");
    e.preventDefault();
  });
  handle.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    // Pane grows to the LEFT as the handle moves left.
    const dx = startX - e.clientX;
    applyWidth(startW + dx);
  });
  const endDrag = (e) => {
    if (!dragging) return;
    dragging = false;
    handle.classList.remove("is-dragging");
    document.body.classList.remove("is-resizing-pane");
    try { handle.releasePointerCapture(e.pointerId); } catch (_) {}
    const w = detailPane.getBoundingClientRect().width;
    try { localStorage.setItem("dp-width-px", String(Math.round(w))); } catch (_) {}
  };
  handle.addEventListener("pointerup", endDrag);
  handle.addEventListener("pointercancel", endDrag);

  window.addEventListener("resize", () => {
    const cur = parseFloat(getComputedStyle(detailPane).width);
    if (Number.isFinite(cur)) applyWidth(cur);
  });
}

// ---------- boot -----------
loadAll().then(() => {
  refreshLayoutConstants();
  _lastLaneH = LANE_H;
  _lastRailW = LANE_RAIL_W;
  wirePanZoom();
  wireViewToggle();
  wireDetailPaneResize();
  // Deep-link / reload / share: apply any hash present at boot.
  const initialParsed = router.parse(location.hash);
  if (initialParsed) router.apply(initialParsed);
});
