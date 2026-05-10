// Vedānta timeline app — vanilla ES module.
// Loads the data manifest, renders a horizontal-scroll timeline of thinkers,
// opens a detail pane on click. White background, simple, no framework.

const PX_PER_YEAR = 1.6;          // tunable: width per year on the timeline
const TIMELINE_PAD_LEFT = 80;     // px padding on left side of timeline
const TIMELINE_PAD_RIGHT = 80;
const ROW_BAND = 28;              // px between rows when stacking dots to avoid overlap
const TOP_PAD = 60;               // top padding for first row of dots

const stage = document.getElementById("stage");
const detailPane = document.getElementById("detailPane");
const detailContent = document.getElementById("detailContent");
const closeDetail = document.getElementById("closeDetail");
const closeReader = document.getElementById("closeReader");
const readerModal = document.getElementById("readerModal");
const readerContent = document.getElementById("readerContent");
const scroller = document.getElementById("timelineScroller");
const dotsLayer = document.getElementById("timelineDots");
const axisEl = document.getElementById("timelineAxis");
const svg = document.getElementById("timelineSvg");
const legendEl = document.getElementById("legend");

let state = {
  thinkers: [],
  thinkersById: new Map(),
  schools: {},
  subSchools: {},
  comparativeClaims: [],
  range: { low: -800, high: 1900 },
  activeId: null,
};

async function loadJSON(path) {
  try {
    const r = await fetch(path);
    if (!r.ok) return null;
    return await r.json();
  } catch (e) {
    return null;
  }
}

async function loadAll() {
  // Manifest lists every thinker file plus registry paths.
  const manifest = await loadJSON("data/manifest.json");
  if (!manifest) {
    showEmptyState("No data yet. Run the corpus dispatch waves to populate /site/data/.");
    return;
  }

  state.schools = (await loadJSON("data/registries/schools.json")) || {};
  state.subSchools = (await loadJSON("data/registries/sub_schools.json")) || {};

  const thinkerFiles = manifest.thinkers || [];
  const loaded = await Promise.all(
    thinkerFiles.map((f) => loadJSON(`data/thinkers/${f}`))
  );
  state.thinkers = loaded.filter(Boolean);
  state.thinkers.forEach((t) => state.thinkersById.set(t.id, t));

  const claimFiles = manifest.comparative_claims || [];
  const claims = await Promise.all(
    claimFiles.map((f) => loadJSON(`data/comparative_claims/${f}`))
  );
  state.comparativeClaims = claims.filter(Boolean);

  computeRange();
  renderLegend();
  renderTimeline();
}

function computeRange() {
  if (state.thinkers.length === 0) return;
  let lo = Infinity, hi = -Infinity;
  for (const t of state.thinkers) {
    if (typeof t.dates_low === "number") lo = Math.min(lo, t.dates_low);
    if (typeof t.dates_high === "number") hi = Math.max(hi, t.dates_high);
  }
  state.range.low = Math.floor(lo / 50) * 50 - 50;
  state.range.high = Math.ceil(hi / 50) * 50 + 50;
}

function yearToX(y) {
  return TIMELINE_PAD_LEFT + (y - state.range.low) * PX_PER_YEAR;
}

function totalWidth() {
  return TIMELINE_PAD_LEFT + (state.range.high - state.range.low) * PX_PER_YEAR + TIMELINE_PAD_RIGHT;
}

function colorFor(thinker) {
  const token = thinker.school_color_token || "proto";
  const school = state.schools[token];
  if (!school || !school.color_palette) {
    return defaultColorFor(token);
  }
  const shade = (thinker.sub_school_shade || 3) - 1;
  return school.color_palette[Math.max(0, Math.min(4, shade))];
}

function defaultColorFor(token) {
  const map = {
    advaita: "#2563eb", vishishtadvaita: "#059669", dvaita: "#d97706",
    bhedabheda: "#9333ea", acintya: "#db2777", shuddha: "#be123c",
    avibhaga: "#0891b2", "trika-comparator": "#475569",
    "cross-tradition": "#475569", proto: "#6b7280",
  };
  return map[token] || "#6b7280";
}

function renderLegend() {
  const tokens = new Set(state.thinkers.map((t) => t.school_color_token || "proto"));
  legendEl.innerHTML = "";
  for (const tok of tokens) {
    const sw = document.createElement("span");
    sw.className = "swatch";
    sw.style.setProperty("--swatch", defaultColorFor(tok));
    const display = state.schools[tok]?.display_name || tok;
    sw.textContent = display;
    legendEl.appendChild(sw);
  }
}

function renderTimeline() {
  const width = totalWidth();
  scroller.style.width = "100%";
  dotsLayer.style.width = width + "px";
  axisEl.style.width = width + "px";
  svg.setAttribute("width", width);
  svg.setAttribute("height", "100%");
  svg.style.width = width + "px";

  // Year ticks
  const ticks = [];
  const startTick = Math.ceil(state.range.low / 100) * 100;
  for (let y = startTick; y <= state.range.high; y += 100) {
    ticks.push(y);
  }
  axisEl.innerHTML = "";
  for (const y of ticks) {
    const el = document.createElement("div");
    el.className = "year-tick";
    el.style.left = yearToX(y) + "px";
    el.textContent = y < 0 ? `${-y} BCE` : `${y} CE`;
    axisEl.appendChild(el);
  }

  // Sort thinkers by their midpoint, then place into rows greedily to avoid overlap.
  const sorted = [...state.thinkers].sort((a, b) => {
    return ((a.dates_low + a.dates_high) / 2) - ((b.dates_low + b.dates_high) / 2);
  });
  const rowEnds = []; // rightmost x in each row
  const placements = [];
  for (const t of sorted) {
    const x = yearToX((t.dates_low + t.dates_high) / 2);
    const labelW = (t.name || t.id).length * 7 + 18;
    let row = -1;
    for (let i = 0; i < rowEnds.length; i++) {
      if (rowEnds[i] + 12 < x - labelW / 2) { row = i; break; }
    }
    if (row === -1) { row = rowEnds.length; rowEnds.push(0); }
    rowEnds[row] = x + labelW / 2;
    placements.push({ thinker: t, x, row });
  }

  // Render lineage edges in SVG (behind dots).
  const ns = "http://www.w3.org/2000/svg";
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const placementsById = new Map();
  for (const p of placements) placementsById.set(p.thinker.id, p);
  for (const p of placements) {
    for (const targetId of (p.thinker.lineage_out || [])) {
      const target = placementsById.get(targetId);
      if (!target) continue;
      const path = document.createElementNS(ns, "path");
      const x1 = p.x, y1 = TOP_PAD + p.row * ROW_BAND;
      const x2 = target.x, y2 = TOP_PAD + target.row * ROW_BAND;
      const cx = (x1 + x2) / 2;
      path.setAttribute("d", `M ${x1} ${y1} C ${cx} ${y1}, ${cx} ${y2}, ${x2} ${y2}`);
      path.setAttribute("fill", "none");
      path.setAttribute("stroke", colorFor(p.thinker));
      path.setAttribute("stroke-opacity", "0.35");
      path.setAttribute("stroke-width", "1.5");
      svg.appendChild(path);
    }
    for (const pol of (p.thinker.lineage_polemical || [])) {
      const target = placementsById.get(pol.thinker_id);
      if (!target) continue;
      const path = document.createElementNS(ns, "path");
      const x1 = p.x, y1 = TOP_PAD + p.row * ROW_BAND;
      const x2 = target.x, y2 = TOP_PAD + target.row * ROW_BAND;
      const cx = (x1 + x2) / 2;
      path.setAttribute("d", `M ${x1} ${y1} C ${cx} ${y1}, ${cx} ${y2}, ${x2} ${y2}`);
      path.setAttribute("fill", "none");
      path.setAttribute("stroke", "#aaa");
      path.setAttribute("stroke-dasharray", "3 3");
      path.setAttribute("stroke-width", "1");
      svg.appendChild(path);
    }
  }

  // Render dots
  dotsLayer.innerHTML = "";
  for (const p of placements) {
    const t = p.thinker;
    const dot = document.createElement("div");
    dot.className = "thinker-dot";
    if (t.dates_tier === "oral-tradition-only") dot.classList.add("tier-oral");
    if (t.dates_tier === "contested") dot.classList.add("tier-contested");
    dot.style.left = p.x + "px";
    dot.style.top = (TOP_PAD + p.row * ROW_BAND) + "px";
    dot.style.setProperty("--dot-color", colorFor(t));
    dot.dataset.id = t.id;
    dot.innerHTML = `
      <div class="node"></div>
      <div class="label">${escape(t.name || t.id)}<span class="dates">${formatDates(t)}</span></div>
    `;
    dot.addEventListener("click", () => openThinker(t.id));
    dotsLayer.appendChild(dot);
  }
}

function formatDates(t) {
  if (t.dates_low == null && t.dates_high == null) return "";
  const lo = t.dates_low, hi = t.dates_high;
  const fmt = (y) => y < 0 ? `${-y} BCE` : `${y}`;
  if (lo === hi) return ` · ${fmt(lo)}`;
  return ` · ${fmt(lo)}–${fmt(hi)}${hi >= 0 ? "" : " BCE"}`;
}

function openThinker(id) {
  const t = state.thinkersById.get(id);
  if (!t) return;
  state.activeId = id;
  document.querySelectorAll(".thinker-dot").forEach((d) => {
    d.classList.toggle("active", d.dataset.id === id);
  });
  detailContent.style.setProperty("--dot-color", colorFor(t));
  detailContent.innerHTML = renderDetail(t);
  stage.classList.add("detail-open");
  detailPane.setAttribute("aria-hidden", "false");
  detailPane.scrollTop = 0;
  // Scroll the dot into approximate center of the (now-narrower) timeline pane.
  const dotEl = document.querySelector(`.thinker-dot[data-id="${id}"]`);
  if (dotEl) {
    const left = parseFloat(dotEl.style.left);
    const paneW = scroller.clientWidth;
    scroller.scrollTo({ left: Math.max(0, left - paneW / 2), behavior: "smooth" });
  }
  // Wire up read-full buttons after render
  detailContent.querySelectorAll("[data-read-full]").forEach((btn) => {
    btn.addEventListener("click", () => openReader(btn.dataset.readFull, btn.dataset.thinker));
  });
}

function closeDetailPane() {
  stage.classList.remove("detail-open");
  detailPane.setAttribute("aria-hidden", "true");
  state.activeId = null;
  document.querySelectorAll(".thinker-dot").forEach((d) => d.classList.remove("active"));
}
closeDetail.addEventListener("click", closeDetailPane);

function renderDetail(t) {
  const tier = t.dates_tier || "unknown";
  const tierLabel = {
    "confirmed-from-records": "Dates confirmed (records)",
    "consensus-textual": "Dates by textual consensus",
    "contested": "Dates contested",
    "oral-tradition-only": "Oral tradition only",
  }[tier] || tier;

  const works = (t.engaged_works || []).map(renderWork).join("");
  const passages = (t.key_passages || []).map((p) => renderPassage(p, t.id)).join("");
  const claims = (t.comparative_claim_ids || []).map((cid) => {
    const claim = state.comparativeClaims.find((c) => c.claim_id === cid);
    return claim ? renderComparativeClaim(claim, t.id) : "";
  }).join("");

  const lineageIn = (t.lineage_in || []).map((id) => linkThinker(id)).join(", ");
  const lineageOut = (t.lineage_out || []).map((id) => linkThinker(id)).join(", ");
  const polemic = (t.lineage_polemical || []).map((p) => `${linkThinker(p.thinker_id)} <em>${escape(p.direction)}</em>`).join(", ");

  return `
    <h2>${escape(t.name_iast || t.name || t.id)}</h2>
    <div class="meta">
      <span class="school-pill">${escape(t.school || "")}${t.sub_school ? " · " + escape(t.sub_school) : ""}</span>
      <span class="tier-pill">${escape(tierLabel)}</span>
      <span>${escape(t.dates_notes || "")}</span>
    </div>

    <p class="thesis">${escape(t.core_thesis || "Core thesis: not yet written.")}</p>

    ${(lineageIn || lineageOut || polemic) ? `
      <h3>Lineage</h3>
      <p>${lineageIn ? `<strong>From:</strong> ${lineageIn}<br>` : ""}
         ${lineageOut ? `<strong>To:</strong> ${lineageOut}<br>` : ""}
         ${polemic ? `<strong>Polemics:</strong> ${polemic}` : ""}</p>
    ` : ""}

    ${works ? `<h3>Engaged works</h3>${works}` : ""}
    ${passages ? `<h3>Key passages</h3>${passages}` : ""}
    ${claims ? `<h3>Comparative claims</h3>${claims}` : ""}
  `;
}

function renderWork(w) {
  const ascr = (w.ascription_tier || "").replace(/-/g, " ");
  return `
    <div class="work">
      <div class="title-line">
        <span class="title">${escape(w.title_iast || w.title || w.work_id)}</span>
        <span class="ascr">${escape(ascr)}</span>
      </div>
      <p>${escape(w.summary || "")}</p>
      ${w.ascription_notes ? `<p class="why" style="margin:4px 0 0">${escape(w.ascription_notes)}</p>` : ""}
    </div>
  `;
}

function renderPassage(p, thinkerId) {
  const morph = (p.panini_breakdown?.pada_analysis || []).map((pa) =>
    `<strong>${escape(pa.pada)}</strong> &lt;${escape(pa.stem)}${pa.pratyaya ? "+" + escape(pa.pratyaya) : ""}&gt; ${escape(pa.morphology)} — ${escape(pa.gloss)}`
  ).join("\n");
  const samasa = (p.panini_breakdown?.samasa_vigrahas || []).map((s) =>
    `<strong>${escape(s.compound)}</strong> [${escape(s.type)}]: ${escape(s.resolution)}${s.note ? ` (${escape(s.note)})` : ""}`
  ).join("\n");
  const karaka = (p.panini_breakdown?.karaka_structure || []).map((k) =>
    `${escape(k.role)}: <strong>${escape(k.pada)}</strong>${k.note ? ` (${escape(k.note)})` : ""}`
  ).join("\n");
  const verb = (p.panini_breakdown?.verb_modality || []).map((v) =>
    `<strong>${escape(v.pada)}</strong>: ${escape(v.lakara)} / ${escape(v.pada_PA)} / ${escape(v.voice)}${v.note ? ` (${escape(v.note)})` : ""}`
  ).join("\n");

  const breakdown = [
    morph && `<div><em>Pada-analysis</em>:\n${morph}</div>`,
    samasa && `<div><em>Samāsa-vigraha</em>:\n${samasa}</div>`,
    karaka && `<div><em>Kāraka structure</em>:\n${karaka}</div>`,
    verb && `<div><em>Verbal modality</em>:\n${verb}</div>`,
  ].filter(Boolean).join("\n\n");

  return `
    <div class="passage">
      <div class="locus">${escape(p.locus_long || p.locus_short || "")}</div>
      <div class="sanskrit">${escape(p.sanskrit_iast || "")}</div>
      <div class="english">${escape(p.english_close || "")}</div>
      ${breakdown ? `<details><summary>Pāṇinian breakdown</summary><div class="panini">${breakdown}</div></details>` : ""}
      ${p.why_this_passage ? `<div class="why">Why this passage: ${escape(p.why_this_passage)}</div>` : ""}
      ${p.work_id ? `<button class="read-full" data-read-full="${escape(p.work_id)}" data-thinker="${escape(thinkerId)}">Read the full work in translation</button>` : ""}
    </div>
  `;
}

function renderComparativeClaim(claim, thinkerId) {
  const otherId = claim.thinker_a === thinkerId ? claim.thinker_b : claim.thinker_a;
  const verdictClass = `verdict-${claim.verdict}`;
  const verdictLabel = (claim.verdict || "").replace(/-/g, " ");
  return `
    <div class="compclaim">
      <div class="pair">vs. ${linkThinker(otherId)} on <strong>${escape(claim.category)}</strong> (${escape(claim.sub_axis || "")})
        <span class="verdict ${verdictClass}">${escape(verdictLabel)}</span>
      </div>
      <p><em>Surface:</em> ${escape(claim.surface_disagreement || "")}</p>
      <p><em>World-model:</em> ${escape(claim.world_model_unpacking?.structural_mapping || "")}</p>
      <p>${escape(claim.commentary || "")}</p>
    </div>
  `;
}

function linkThinker(id) {
  const t = state.thinkersById.get(id);
  if (!t) return `<span>${escape(id)}</span>`;
  return `<a href="#" data-thinker-link="${escape(id)}">${escape(t.name_iast || t.name || id)}</a>`;
}

document.addEventListener("click", (e) => {
  const a = e.target.closest("[data-thinker-link]");
  if (a) {
    e.preventDefault();
    openThinker(a.dataset.thinkerLink);
  }
});

async function openReader(workId, thinkerId) {
  const t = state.thinkersById.get(thinkerId);
  if (!t) return;
  const work = (t.engaged_works || []).find((w) => w.work_id === workId);
  if (!work) return;
  // Try to load a full-translation file at data/full_translations/<thinker>__<work>.md
  const url = `data/full_translations/${thinkerId}__${workId}.md`;
  const r = await fetch(url);
  let body = "";
  if (r.ok) {
    body = await r.text();
  } else {
    body = `# ${work.title_iast || work.title}\n\nFull translation not yet produced. The corpus pipeline produces engaged-passage translations first; a full Pāṇinian-rich translation of this work has not been generated.\n\nSee the engaged passages in the detail panel.`;
  }
  readerContent.innerHTML = renderMarkdown(body);
  readerModal.classList.add("open");
  readerModal.setAttribute("aria-hidden", "false");
}
closeReader.addEventListener("click", () => {
  readerModal.classList.remove("open");
  readerModal.setAttribute("aria-hidden", "true");
});

function renderMarkdown(md) {
  // Minimal markdown renderer (headings, paragraphs, italics, code, blockquotes).
  // Avoids pulling a library; intentionally narrow.
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  return esc(md)
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

function escape(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

function showEmptyState(msg) {
  detailContent.innerHTML = `<h2>Setting up</h2><p>${escape(msg)}</p>`;
  stage.classList.add("detail-open");
}

loadAll();
