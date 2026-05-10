// Vedānta interactive timeline.
// Cladogram swim-lanes + sticky lane rail + manhattan-routed lineage edges.
// Detail pane: hero thesis, nested work→passage cards, Pāṇinian tables.
// Canvas-style 2D pan (drag) + wheel scroll + zoom.
// Sanskrit-term popover glossary (loads from data/glossary/).
// Vanilla ES module. No framework, no build step.

// ---------- layout constants (kept in sync with style.css :root) -----------
const TOPBAR_H = 40;
const LANE_H = 96;
const LANE_RAIL_W = 168;
const ERA_STRIP_H = 24;
const AXIS_H = 28;

const PX_PER_YEAR_DEFAULT = 1.9;
const PAD_LEFT = 60;
const PAD_RIGHT = 80;

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
  "trika-comparator",
  "cross-tradition",
];

const LANE_DISPLAY = {
  "proto": "Proto-Vedānta",
  "advaita": "Advaita",
  "bhedabheda": "Bhedābheda",
  "vishishtadvaita": "Viśiṣṭādvaita",
  "dvaita": "Dvaita (Tattvavāda)",
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
  "trika-comparator": "Pratyabhijñā / Trika",
  "cross-tradition": "Cross-tradition",
};

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
};

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
  computeLayout();
  renderAll();
  updateSubtitle();
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
  return LANE_ORDER.length * LANE_H + AXIS_H + 8;
}
function laneIndex(token) {
  const i = LANE_ORDER.indexOf(token);
  return i < 0 ? LANE_ORDER.length - 1 : i;
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
  };
  return base[token] || "#6b7280";
}

function shadeFor(thinker) {
  const s = thinker.sub_school_shade;
  if (typeof s === "number" && s >= 1 && s <= 5) return s;
  return 3;
}

function computeLayout() {
  state.layout.clear();
  const sorted = [...state.thinkers].sort((a, b) => {
    return ((a.dates_low + a.dates_high) / 2) - ((b.dates_low + b.dates_high) / 2);
  });

  // for collision detection within same lane × shade, track placed dots
  const occupancy = new Map();   // `${lane}_${shade}` → array of {x1, x2}

  for (const t of sorted) {
    const lane = laneIndex(t.school_color_token);
    const shade = shadeFor(t);
    const tier = tierOf(t);
    const xMid = yearToX((t.dates_low + t.dates_high) / 2);
    const x1 = yearToX(t.dates_low);
    const x2 = yearToX(t.dates_high);

    const subOffset = (shade - 3) * 11;   // -22 .. +22
    let nudge = 0;
    const key = `${lane}_${shade}`;
    const arr = occupancy.get(key) || [];
    const myWidth = (t.name || t.id).length * 7 + 40;
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

// ---------- render: lane rail -----------
function renderLaneRail() {
  laneRailEl.innerHTML = "";
  const counts = new Map();
  for (const t of state.thinkers) {
    const k = laneIndex(t.school_color_token);
    counts.set(k, (counts.get(k) || 0) + 1);
  }
  for (let i = 0; i < LANE_ORDER.length; i++) {
    const tok = LANE_ORDER[i];
    const display = state.schools[tok]?.display_name || LANE_DISPLAY[tok] || tok;
    const swatch = state.schools[tok]?.color_palette?.[2]
                || state.schools[tok]?.color_hex
                || "#888";
    const count = counts.get(i) || 0;
    const row = document.createElement("div");
    row.className = "lane-row";
    row.dataset.lane = tok;
    row.style.height = LANE_H + "px";
    row.innerHTML = `
      <span class="swatch-bar" style="background:${swatch}"></span>
      <div class="lane-meta">
        <span class="lane-name">${escape(display)}</span>
        <span class="lane-count">${count} ${count === 1 ? "thinker" : "thinkers"}</span>
      </div>
    `;
    laneRailEl.appendChild(row);
  }
  laneRailEl.style.height = (LANE_ORDER.length * LANE_H) + "px";
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
    r.setAttribute("height", LANE_ORDER.length * LANE_H);
    r.setAttribute("fill", era.fill);
    r.setAttribute("fill-opacity", era.fillOpacity);
    g.appendChild(r);
  }
  // lane separators
  for (let i = 1; i < LANE_ORDER.length; i++) {
    const line = document.createElementNS(ns, "line");
    line.setAttribute("class", "lane-separator");
    line.setAttribute("x1", 0);
    line.setAttribute("x2", totalWidth());
    line.setAttribute("y1", i * LANE_H);
    line.setAttribute("y2", i * LANE_H);
    g.appendChild(line);
  }
  svg.appendChild(g);
}

// ---------- render: lineage edges (manhattan) -----------
function renderEdges() {
  const ns = "http://www.w3.org/2000/svg";
  const g = document.createElementNS(ns, "g");
  g.setAttribute("class", "edges");

  for (const [, p] of state.layout) {
    const t = p.thinker;
    for (const targetId of (t.lineage_out || [])) {
      const target = state.layout.get(targetId);
      if (!target) continue;
      const path = manhattanEdge(p, target);
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
      const path = manhattanEdge(p, target);
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
  const w = totalWidth();
  const h = totalHeight();
  canvas.style.width = w + "px";
  canvas.style.height = h + "px";
  dotsLayer.style.width = w + "px";
  dotsLayer.style.height = (LANE_ORDER.length * LANE_H) + "px";
  svg.setAttribute("width", w);
  svg.setAttribute("height", LANE_ORDER.length * LANE_H);
  svg.style.width = w + "px";
  svg.style.height = (LANE_ORDER.length * LANE_H) + "px";
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  renderLaneRail();
  renderEraStrip();
  renderEraBands();
  renderEdges();
  renderDateBars();
  renderDots();
  renderAxis();
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
      const cursorX = e.clientX - rect.left + scroller.scrollLeft - LANE_RAIL_W;
      const yearAtCursor = state.range.low + cursorX / state.pxPerYear;
      state.pxPerYear = newPpy;
      computeLayout();
      renderAll();
      const newCursorX = (yearAtCursor - state.range.low) * state.pxPerYear;
      scroller.scrollLeft = newCursorX - (e.clientX - rect.left) + LANE_RAIL_W;
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
  // horizontal: center the dot
  const desiredLeft = Math.max(0, p.x - paneW / 2 + LANE_RAIL_W);
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
  const body = r.ok
    ? await r.text()
    : `# ${work.title_iast || work.title}\n\nFull translation not yet produced. The corpus pipeline produces engaged-passage Pāṇinian translations first; a full translation of this work has not been generated.\n\nSee the engaged passages in the detail panel.`;
  readerContent.innerHTML = renderMarkdown(body);
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
  // close any existing popover
  document.querySelectorAll(".glossary-popover").forEach((el) => el.remove());
  const pop = document.createElement("div");
  pop.className = "glossary-popover";
  const perSchool = (entry.per_school || []).map((s) =>
    `<div class="gp-row"><span class="gp-school">${escape(s.school)}</span><span class="gp-def">${md(s.definition)}</span></div>`
  ).join("");
  pop.innerHTML = `
    <button class="gp-close" aria-label="Close">×</button>
    <div class="gp-term">${escape(entry.term_iast || termKey)}</div>
    ${entry.literal ? `<div class="gp-literal">Literally: <em>${escape(entry.literal)}</em></div>` : ""}
    <div class="gp-invariant"><span class="gp-label">Invariant</span><div>${md(entry.invariant_definition || "")}</div></div>
    ${perSchool ? `<div class="gp-perschool"><span class="gp-label">By school</span>${perSchool}</div>` : ""}
  `;
  document.body.appendChild(pop);
  const r = anchorEl.getBoundingClientRect();
  pop.style.position = "fixed";
  pop.style.top = (r.bottom + 8) + "px";
  pop.style.left = Math.max(10, r.left) + "px";
  pop.querySelector(".gp-close").addEventListener("click", () => pop.remove());
  document.addEventListener("click", function once(e) {
    if (!pop.contains(e.target) && e.target !== anchorEl) {
      pop.remove();
      document.removeEventListener("click", once);
    }
  });
}

// ---------- markdown helpers -----------
function escape(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

function md(s) {
  if (s == null) return "";
  let out = escape(s);
  // bold first (longer match), then italic
  out = out.replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/(^|[\s(\[—,;:])\*([^*\n]+?)\*(?=[\s.,;:!?)\]—]|$)/g, "$1<em>$2</em>");
  out = out.replace(/`([^`]+?)`/g, "<code>$1</code>");
  // glossary tagging — wrap matched terms in clickable spans
  if (state.glossaryRegex) {
    out = out.replace(state.glossaryRegex, (m) => `<span class="term" data-term="${escape(m)}">${m}</span>`);
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
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, "<code>$1</code>")
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
  readingModeBtn.textContent = on ? "Back to timeline" : "Reading mode";
  if (on && !state.activeId && state.thinkers.length) {
    const sorted = [...state.thinkers].sort((a, b) => (a.dates_low + a.dates_high)/2 - (b.dates_low + b.dates_high)/2);
    openThinker(sorted[0].id);
  }
}
readingModeBtn.addEventListener("click", () => {
  const on = !document.body.classList.contains("is-reading-mode");
  setReadingMode(on);
});

// ---------- about modal -----------
const aboutBtn = document.getElementById("aboutBtn");
const aboutModal = document.getElementById("aboutModal");
const closeAbout = document.getElementById("closeAbout");
aboutBtn.addEventListener("click", () => { aboutModal.classList.add("is-open"); aboutModal.setAttribute("aria-hidden", "false"); });
closeAbout.addEventListener("click", () => { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); });
aboutModal.addEventListener("click", (e) => {
  if (e.target === aboutModal) { aboutModal.classList.remove("is-open"); aboutModal.setAttribute("aria-hidden", "true"); }
});

// ---------- keyboard nav -----------
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (readerModal.classList.contains("is-open")) {
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

// ---------- boot -----------
loadAll().then(() => wirePanZoom());
