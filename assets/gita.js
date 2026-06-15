/* =============================================================
   Sthitaprajña — BG 2.54–72 reading engine.
   Renders window.GITA_VERSES (see gita/sthitaprajna/verses.js and
   gita/sthitaprajna/_build/DESIGN.md).

   IAST only on screen. Per verse: saṃhitā line, an interactive
   pada-pāṭha (every word tappable → Pāṇinian word-card + English
   highlight), literal English, and collapsible apparatus:
   Grammar in full · Commentary voices (voice-by-voice, equal) ·
   Aurobindo · Across traditions.
   ============================================================= */

const GLOSSARY_BASE = "../../data/glossary/";

function escapeHtml(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

/* ----- English line: {indices:phrase} → highlightable spans ----- */
function renderEnglishWithSpans(english) {
  const re = /\{([\d,\s]+):([^}]*)\}/g;
  let out = "", last = 0, m;
  while ((m = re.exec(english)) !== null) {
    if (m.index > last) out += escapeHtml(english.slice(last, m.index));
    const indices = m[1].split(",").map(s => s.trim()).filter(Boolean).join(" ");
    out += `<span class="we" data-word-i="${indices}">${escapeHtml(m[2])}</span>`;
    last = m.index + m[0].length;
  }
  if (last < english.length) out += escapeHtml(english.slice(last));
  return out;
}

/* ----- pada-pāṭha: each word a tappable span ----- */
function renderPadapatha(words) {
  return words.map(w => {
    const cls = w.translatable === false ? "w w-untranslatable" : "w";
    return `<span class="${cls}" data-word-i="${w.i}" tabindex="0">${escapeHtml(w.iast)}</span>`;
  }).join(" ");
}

/* ----- saṃhitā: plain IAST, line-broken on \n ----- */
function renderSamhita(iast) {
  return escapeHtml(iast).replace(/\n/g, "<br>");
}

/* ----- the full word-by-word grammar list (Layer 2) ----- */
function renderGrammarFull(verse) {
  const rows = verse.words.map(w => {
    const bits = [];
    if (w.stem) bits.push(`stem <em>${escapeHtml(w.stem)}</em>`);
    if (w.root) bits.push(`root <em>${escapeHtml(w.root)}</em>`);
    if (w.affix && w.affix !== "—") bits.push(escapeHtml(w.affix));
    if (w.morph) bits.push(escapeHtml(w.morph));
    if (w.karaka) bits.push(`<span class="g-karaka">${escapeHtml(w.karaka)}</span>`);
    let comp = "";
    if (w.compound) {
      comp = `<div class="g-compound">${escapeHtml(w.compound.type)}: <em>${escapeHtml(w.compound.vigraha)}</em></div>`;
    }
    return `<div class="g-row">
      <div class="g-pada">${escapeHtml(w.iast)}</div>
      <div class="g-body"><div class="g-gloss">${escapeHtml(w.gloss)}</div>
        <div class="g-morph">${bits.join(" · ")}</div>${comp}</div>
    </div>`;
  }).join("");
  const summary = [];
  if (verse.grammar && verse.grammar.karakaSummary)
    summary.push(`<p class="g-summary"><span class="g-label">Kāraka</span> ${escapeHtml(verse.grammar.karakaSummary)}</p>`);
  if (verse.grammar && verse.grammar.verbalModality)
    summary.push(`<p class="g-summary"><span class="g-label">Verbal modality</span> ${escapeHtml(verse.grammar.verbalModality)}</p>`);
  return `<div class="g-rows">${rows}</div>${summary.join("")}`;
}

/* ----- commentary: voice-by-voice, equal, unbiased ----- */
function renderCommentary(verse, vIdx) {
  const list = verse.commentaries || [];
  if (!list.length) return `<p class="apparatus-empty">No commentary on this verse is on file yet.</p>`;
  const tabs = list.map((c, k) =>
    `<button class="voice-tab${k === 0 ? " is-active" : ""}" data-voice="${k}" type="button">
       <span class="voice-name">${escapeHtml(c.author)}</span>
       <span class="voice-school">${escapeHtml(c.school || "")}</span>
     </button>`).join("");
  const panels = list.map((c, k) =>
    `<div class="voice-panel${k === 0 ? " is-active" : ""}" data-voice="${k}">
       <div class="voice-head">${escapeHtml(c.author)} · <em>${escapeHtml(c.work || "")}</em>${c.locus ? " · " + escapeHtml(c.locus) : ""}</div>
       <div class="voice-sanskrit" data-glossable>${escapeHtml(c.sanskrit)}</div>
       ${c.ourRendering ? `<div class="voice-rendering">${escapeHtml(c.ourRendering)}</div>` : ""}
     </div>`).join("");
  return `<div class="voice-tabs" role="tablist">${tabs}</div><div class="voice-panels">${panels}</div>`;
}

function renderAurobindo(verse) {
  const list = verse.aurobindo || [];
  if (!list.length) return `<p class="apparatus-empty">No Aurobindo passage indexed to this verse yet.</p>`;
  return list.map(a =>
    `<blockquote class="auro">
       <div class="auro-text">${escapeHtml(a.text)}</div>
       <cite>— Sri Aurobindo, <em>${escapeHtml(a.work || "Essays on the Gita")}</em>${a.ref ? ", " + escapeHtml(a.ref) : ""}</cite>
     </blockquote>`).join("");
}

function renderCrossTradition(verse) {
  const list = verse.crossTradition || [];
  if (!list.length) return `<p class="apparatus-empty">No cross-tradition parallel indexed to this verse yet.</p>`;
  return list.map(p =>
    `<div class="parallel">
       <div class="parallel-head">${escapeHtml(p.school || "")}${p.thinker ? " · " + escapeHtml(p.thinker) : ""} · <em>${escapeHtml(p.work || "")}</em>${p.locus ? " " + escapeHtml(p.locus) : ""}</div>
       <div class="parallel-sanskrit" data-glossable>${escapeHtml(p.sanskrit)}</div>
       ${p.ourRendering ? `<div class="parallel-rendering">${escapeHtml(p.ourRendering)}</div>` : ""}
     </div>`).join("");
}

function disclosure(label, count, innerHtml) {
  const badge = count ? `<span class="ap-count">${count}</span>` : "";
  return `<details class="apparatus">
    <summary><span class="ap-caret" aria-hidden="true"></span><span class="ap-label">${escapeHtml(label)}</span>${badge}</summary>
    <div class="ap-body">${innerHtml}</div>
  </details>`;
}

function renderVerse(verse, idx) {
  const speaker = verse.speaker === "arjuna" ? "Arjuna" : verse.speaker === "krishna" ? "Śrī Kṛṣṇa" : "";
  return `<article class="verse" id="v-${escapeHtml(verse.locus)}" data-verse-idx="${idx}">
    <header class="verse-head">
      <span class="verse-locus">${escapeHtml(verse.locus)}</span>
      ${speaker ? `<span class="verse-speaker">${escapeHtml(speaker)}</span>` : ""}
      ${verse.meter ? `<span class="verse-meter">${escapeHtml(verse.meter)}</span>` : ""}
    </header>
    <div class="verse-samhita">${renderSamhita(verse.iast)}</div>
    <div class="verse-pada">${renderPadapatha(verse.words)}</div>
    <div class="verse-english">${renderEnglishWithSpans(verse.english)}</div>
    ${verse.sense ? `<p class="verse-sense">${escapeHtml(verse.sense)}</p>` : ""}
    <div class="verse-apparatus">
      ${disclosure("Grammar in full", null, renderGrammarFull(verse))}
      ${disclosure("Commentary voices", (verse.commentaries || []).length, renderCommentary(verse))}
      ${disclosure("Aurobindo on the Gita", (verse.aurobindo || []).length, renderAurobindo(verse))}
      ${disclosure("Across traditions", (verse.crossTradition || []).length, renderCrossTradition(verse))}
    </div>
  </article>`;
}

/* =============================================================
   RENDER + WIRE
   ============================================================= */
let VERSES = [];

// Core verse data lives in verses.js (window.GITA_VERSES). The apparatus
// layers are authored independently and merged here by locus, so the
// commentary / Aurobindo / parallels workstreams never touch the same
// file: window.GITA_COMMENTARY / GITA_AUROBINDO / GITA_PARALLELS are
// optional maps { "2.54": [ … ] }.
// Commentary voices are shown voice-by-voice and EQUAL — no ranking. We
// order them chronologically (a neutral ordering, not a judgment) so no
// ācārya is privileged by being the data seed.
const VOICE_CHRONOLOGY = {
  "Śaṅkara": 700, "Abhinavagupta": 975, "Yāmuna": 1010, "Rāmānuja": 1077,
  "Madhva": 1238, "Śrīdhara": 1400, "Keśava Kāśmīrī": 1480, "Vallabha": 1490,
  "Madhusūdana": 1565, "Baladeva": 1720,
};
function voiceYear(c) {
  return VOICE_CHRONOLOGY[c.author] != null ? VOICE_CHRONOLOGY[c.author] : 9999;
}

function mergeLayers(verses) {
  const com = window.GITA_COMMENTARY || {};
  const auro = window.GITA_AUROBINDO || {};
  const par = window.GITA_PARALLELS || {};
  return verses.map(v => ({
    ...v,
    commentaries: (v.commentaries || []).concat(com[v.locus] || [])
      .slice().sort((a, b) => voiceYear(a) - voiceYear(b)),
    aurobindo: (v.aurobindo || []).concat(auro[v.locus] || []),
    crossTradition: (v.crossTradition || []).concat(par[v.locus] || []),
  }));
}

function render() {
  const root = document.getElementById("gitaRoot");
  if (!root) return;
  VERSES = mergeLayers(window.GITA_VERSES || []);
  root.innerHTML = VERSES.map((v, i) => renderVerse(v, i)).join("");
  wireWordInteractions(root);
  wireVoiceTabs(root);
  applyGlossaryToDom(root);
}

/* ----- word ↔ English highlight + word-card popover ----- */
function wordByIndex(verseEl, i) {
  const v = VERSES[+verseEl.dataset.verseIdx];
  return v && v.words.find(w => String(w.i) === String(i));
}

function activate(span) {
  const verseEl = span.closest(".verse");
  if (!verseEl) return;
  const i = span.dataset.wordI;
  span.classList.add("is-hi");
  verseEl.querySelectorAll(".we").forEach(el => {
    if (el.dataset.wordI.split(/\s+/).includes(i)) el.classList.add("is-hi");
  });
  const w = wordByIndex(verseEl, i);
  if (w) showWordCard(span, w);
}
function deactivate(span) {
  const verseEl = span.closest(".verse");
  if (!verseEl) return;
  const i = span.dataset.wordI;
  span.classList.remove("is-hi");
  verseEl.querySelectorAll(".we").forEach(el => {
    if (el.dataset.wordI.split(/\s+/).includes(i)) el.classList.remove("is-hi");
  });
  hideWordCard();
}

function wireWordInteractions(root) {
  let stickyWord = null, hoverWord = null;
  root.addEventListener("mouseover", e => {
    const w = e.target.closest(".w");
    if (!w || w === hoverWord) return;
    if (hoverWord && hoverWord !== stickyWord) deactivate(hoverWord);
    hoverWord = w; activate(w);
  });
  root.addEventListener("mouseout", e => {
    const w = e.target.closest(".w");
    if (!w) return;
    const to = e.relatedTarget;
    if (to && (w.contains(to) || (cardEl && cardEl.contains(to)))) return;
    if (w !== stickyWord) deactivate(w);
    if (hoverWord === w) hoverWord = null;
  });
  root.addEventListener("click", e => {
    const w = e.target.closest(".w");
    if (!w) return;
    e.stopPropagation();
    if (stickyWord === w) { stickyWord = null; deactivate(w); return; }
    if (stickyWord) deactivate(stickyWord);
    stickyWord = w; activate(w);
  });
  document.addEventListener("click", e => {
    if (cardEl && cardEl.contains(e.target)) return;
    if (stickyWord) { deactivate(stickyWord); stickyWord = null; }
  });
  root.addEventListener("focusin", e => { const w = e.target.closest(".w"); if (w) activate(w); });
  root.addEventListener("focusout", e => {
    const w = e.target.closest(".w");
    if (!w || w === stickyWord) return;
    deactivate(w);
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      if (stickyWord) { deactivate(stickyWord); stickyWord = null; }
      closeGlossary();
    }
  });
  window.addEventListener("scroll", () => hideWordCard(), { passive: true });
}

/* ----- word-card popover ----- */
let cardEl = null;
function ensureCard() {
  if (cardEl) return cardEl;
  cardEl = document.createElement("div");
  cardEl.className = "word-card";
  cardEl.hidden = true;
  document.body.appendChild(cardEl);
  return cardEl;
}
function showWordCard(span, w) {
  const card = ensureCard();
  const rows = [];
  rows.push(`<div class="wc-head"><span class="wc-surface">${escapeHtml(w.iast)}</span>${w.morph ? `<span class="wc-morph">${escapeHtml(w.morph)}</span>` : ""}</div>`);
  rows.push(`<div class="wc-gloss">${escapeHtml(w.gloss)}</div>`);
  const ana = [];
  if (w.stem) ana.push(`<b>stem</b> ${escapeHtml(w.stem)}`);
  if (w.root) ana.push(`<b>root</b> ${escapeHtml(w.root)}`);
  if (w.affix && w.affix !== "—") ana.push(`<b>affix</b> ${escapeHtml(w.affix)}`);
  if (ana.length) rows.push(`<div class="wc-ana">${ana.join("<br>")}</div>`);
  if (w.karaka) rows.push(`<div class="wc-karaka">${escapeHtml(w.karaka)}</div>`);
  if (w.compound) rows.push(`<div class="wc-compound"><b>${escapeHtml(w.compound.type)}</b><br>${escapeHtml(w.compound.vigraha)}</div>`);
  if (w.glossaryKey) rows.push(`<button class="wc-gloss-link" data-term="${escapeHtml(w.glossaryKey)}" type="button">Glossary ▸</button>`);
  card.innerHTML = rows.join("");
  card.hidden = false;
  positionPopover(card, span);
  const gl = card.querySelector(".wc-gloss-link");
  if (gl) gl.addEventListener("click", ev => { ev.stopPropagation(); openGlossary(gl.dataset.term, gl); });
}
function hideWordCard() { if (cardEl) cardEl.hidden = true; }

function positionPopover(el, anchor) {
  const r = anchor.getBoundingClientRect();
  el.style.left = "0px"; el.style.top = "0px";
  const er = el.getBoundingClientRect();
  const margin = 8;
  let left = r.left + r.width / 2 - er.width / 2 + window.scrollX;
  let top = r.top - er.height - 8 + window.scrollY;
  const minLeft = window.scrollX + margin;
  const maxLeft = window.scrollX + document.documentElement.clientWidth - er.width - margin;
  left = Math.max(minLeft, Math.min(maxLeft, left));
  if (top < window.scrollY + margin) top = r.bottom + 8 + window.scrollY;
  el.style.left = left + "px";
  el.style.top = top + "px";
}

/* ----- voice-by-voice commentary switcher ----- */
function wireVoiceTabs(root) {
  root.addEventListener("click", e => {
    const tab = e.target.closest(".voice-tab");
    if (!tab) return;
    const wrap = tab.closest(".ap-body");
    const k = tab.dataset.voice;
    wrap.querySelectorAll(".voice-tab").forEach(t => t.classList.toggle("is-active", t.dataset.voice === k));
    wrap.querySelectorAll(".voice-panel").forEach(p => p.classList.toggle("is-active", p.dataset.voice === k));
  });
}

/* =============================================================
   GLOSSARY — lazy popover. Loads data/glossary/<key>.json on demand
   (skips silently if absent). IAST-only display.
   ============================================================= */
const glossaryCache = new Map();
async function loadGlossary(key) {
  if (glossaryCache.has(key)) return glossaryCache.get(key);
  let entry = null;
  try {
    const res = await fetch(GLOSSARY_BASE + key + ".json");
    if (res.ok) entry = await res.json();
  } catch (_) { /* offline / missing — skip */ }
  glossaryCache.set(key, entry);
  return entry;
}

let glossEl = null;
async function openGlossary(key, anchor) {
  const entry = await loadGlossary(key);
  closeGlossary();
  glossEl = document.createElement("div");
  glossEl.className = "glossary-popover";
  if (!entry) {
    glossEl.innerHTML = `<button class="gp-close" aria-label="Close">×</button>
      <div class="gp-term">${escapeHtml(key)}</div>
      <p class="gp-def">No glossary entry yet for this term.</p>`;
  } else {
    const schools = (entry.per_school || []).map(s =>
      `<div class="gp-school"><span class="gp-school-name">${escapeHtml(s.school)}</span> ${escapeHtml(s.definition)}</div>`).join("");
    glossEl.innerHTML = `<button class="gp-close" aria-label="Close">×</button>
      <div class="gp-term">${escapeHtml(entry.term_iast || key)}</div>
      ${entry.literal ? `<div class="gp-literal">${escapeHtml(entry.literal)}</div>` : ""}
      ${entry.invariant_definition ? `<p class="gp-def">${escapeHtml(entry.invariant_definition)}</p>` : ""}
      ${schools ? `<div class="gp-schools">${schools}</div>` : ""}
      ${entry.translator_note ? `<p class="gp-note">${escapeHtml(entry.translator_note)}</p>` : ""}`;
  }
  document.body.appendChild(glossEl);
  positionPopover(glossEl, anchor);
  glossEl.querySelector(".gp-close").addEventListener("click", closeGlossary);
}
function closeGlossary() { if (glossEl) { glossEl.remove(); glossEl = null; } }

/* Linkify glossary terms inside commentary/parallel Sanskrit blocks.
   We only know exact aliases lazily, so for now we make the whole block
   selectable and rely on the word-cards for the mūla. A future pass can
   add an alias regex (see app.js buildGlossaryRegex). */
function applyGlossaryToDom(_root) { /* reserved for alias-regex linkification */ }

document.addEventListener("DOMContentLoaded", render);
