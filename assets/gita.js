/* =============================================================
   Bhagavad-Gītā 2.54–72 — reading engine (embeddable).
   GitaReader.render(rootEl, opts) renders the interactive reading into
   rootEl. Used both by the standalone page (gita/sthitaprajna/) and by
   the timeline app's Article pane (assets/app.js), so it opens as a
   normal in-app article.

   - mūla AND every commentator's Sanskrit are word-clickable: tap a word
     → a card with its piece-by-piece translation + grammar, and the
     English below highlights. Cards open on CLICK only (never hover).
   - Voices (ācāryas · Aurobindo · other traditions) are multi-select and
     colour-coded; pick several at once.
   IAST only on screen.
   ============================================================= */
(function () {
"use strict";

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}
function mdInline(s) {
  return esc(s)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

/* ---------- grammar jargon → plain English ---------- */
const ABBR = [
  [/\bnom\./g, "nominative"], [/\bacc\./g, "accusative"], [/\binstr\./g, "instrumental"],
  [/\bdat\./g, "dative"], [/\babl\./g, "ablative"], [/\bgen\./g, "genitive"],
  [/\bloc\./g, "locative"], [/\bvoc\./g, "vocative"],
  [/\bsg\./g, "singular"], [/\bpl\./g, "plural"], [/\bdu\./g, "dual"],
  [/\bmasc\./g, "masculine"], [/\bfem\./g, "feminine"], [/\bneut\./g, "neuter"],
  [/\bindic\./g, "indicative"], [/\bpres\./g, "present"], [/\bpart\./g, "participle"],
  [/\bppp\./g, "past participle"], [/\bopt\./g, "optative"],
];
function plainMorph(m) { let s = " " + m + " "; for (const [re, full] of ABBR) s = s.replace(re, full); return s.trim(); }
const CASE_SENSE = {
  genitive: "of", instrumental: "by / with", locative: "in / on",
  dative: "to / for", ablative: "from", accusative: "the object",
  nominative: "the subject", vocative: "one addressed",
};
function caseSense(plain) { return CASE_SENSE[plain.split(/[ ,]/)[0]] || null; }

/* ---------- interactive word scope registry ---------- */
// Every word-clickable block (a mūla verse OR a commentary passage) is a
// "scope": its words live in SCOPES[id]; the block carries data-wscope=id.
let SCOPE_N = 0;
const SCOPES = Object.create(null);
function newScope(words) { const id = "s" + (++SCOPE_N); SCOPES[id] = words; return id; }

function renderEnglish(english) {
  const re = /\{([\d,\s]+):([^}]*)\}/g;
  let out = "", last = 0, m;
  while ((m = re.exec(english)) !== null) {
    if (m.index > last) out += esc(english.slice(last, m.index));
    const idx = m[1].split(",").map(s => s.trim()).filter(Boolean).join(" ");
    out += `<span class="we" data-wi="${idx}">${esc(m[2])}</span>`;
    last = m.index + m[0].length;
  }
  if (last < english.length) out += esc(english.slice(last));
  return out;
}
function renderPada(words) {
  return words.map(w => {
    const cls = w.translatable === false ? "w w-name" : "w";
    return `<span class="${cls}" data-wi="${w.i}" tabindex="0" role="button">${esc(w.iast)}</span>`;
  }).join(" ");
}

/* An interactive Sanskrit block: tappable pada line + slotted English.
   Used for the mūla and for any commentary entry that carries words[]+english. */
function interactiveBlock(words, english, saFallback) {
  const id = newScope(words);
  const pada = renderPada(words);
  const en = english ? renderEnglish(english) : "";
  return `<div class="ix" data-wscope="${id}">
    <div class="ix-pada" lang="sa-Latn">${pada}</div>
    ${en ? `<div class="ix-en">${en}</div>` : ""}
  </div>`;
}

/* ---------- voices ---------- */
const VOICE_YEAR = {
  "Śaṅkara": 700, "Abhinavagupta": 975, "Rāmānuja": 1077,
  "Madhva (Ānandatīrtha)": 1238, "Madhva": 1238,
  "Śrīdhara Svāmī": 1400, "Śrīdhara": 1400, "Keśava Kāśmīrī": 1480,
  "Madhusūdana Sarasvatī": 1565, "Madhusūdana": 1565,
  "Baladeva": 1720, "Sri Aurobindo": 1916,
};
function vYear(n) { return VOICE_YEAR[n] != null ? VOICE_YEAR[n] : 9000; }
// commentator → timeline thinker id (so the reader can see who they are)
const VOICE_THINKER = {
  "Śaṅkara": "sankara", "Rāmānuja": "ramanuja",
  "Madhva (Ānandatīrtha)": "madhva", "Madhva": "madhva",
  "Śrīdhara Svāmī": "sridhara", "Śrīdhara": "sridhara",
  "Madhusūdana Sarasvatī": "madhusudana", "Madhusūdana": "madhusudana",
  "Sri Aurobindo": "aurobindo",
};
// distinct, theme-safe colours assigned in voice order
const PALETTE = ["#b8860b", "#1d7874", "#9b2226", "#3a5a98", "#6a4c93", "#4d7c2f", "#a15c2b", "#7d5fa3"];

// Resolve entries for a verse, expanding combined-range keys like "2.62-63"
// (which cover 2.62 AND 2.63) to each verse they span.
function chNum(s) { const m = /^(\d+)\.(\d+)$/.exec(s); return m ? [+m[1], +m[2]] : null; }
function entriesFor(map, loc) {
  const out = (map[loc] || []).slice();
  const cn = chNum(loc); if (!cn) return out;
  for (const key in map) {
    const r = /^(\d+)\.(\d+)-(\d+)$/.exec(key);
    if (r && +r[1] === cn[0] && cn[1] >= +r[2] && cn[1] <= +r[3]) out.push(...map[key]);
  }
  return out;
}

function buildVoices(verses, data) {
  const com = data.commentary || {}, auro = data.aurobindo || {}, par = data.parallels || {};
  const meta = {}, byVerse = {};
  const ensure = (id, name, school, year) => { if (!meta[id]) meta[id] = { id, name, school: school || "", year: year != null ? year : 9000, thinkerId: VOICE_THINKER[name] || null }; };
  const add = (loc, id, entry) => { (byVerse[loc] = byVerse[loc] || {})[id] = entry; };

  for (const v of verses) {
    const loc = v.locus;
    for (const c of (v.commentaries || []).concat(entriesFor(com, loc))) {
      const id = "ac:" + c.author;
      ensure(id, c.author, c.school, vYear(c.author));
      add(loc, id, { kind: "commentary", data: c });
    }
    const au = entriesFor(auro, loc);
    if (au.length) { ensure("aurobindo", "Sri Aurobindo", "Integral Yoga", vYear("Sri Aurobindo")); add(loc, "aurobindo", { kind: "aurobindo", list: au }); }
    const ps = entriesFor(par, loc);
    if (ps.length) { ensure("parallels", "Other traditions", "parallel", 9500); add(loc, "parallels", { kind: "parallels", list: ps }); }
  }
  const voices = Object.values(meta).sort((a, b) => (a.year - b.year) || a.name.localeCompare(b.name));
  voices.forEach((vc, i) => { vc.color = PALETTE[i % PALETTE.length]; });
  return { voices, byVerse };
}

/* ---------- per-verse + voice rendering ---------- */
function speakerLabel(s) { return s === "arjuna" ? "Arjuna" : s === "krishna" ? "Kṛṣṇa" : ""; }

function renderVoiceInner(entry) {
  if (entry.kind === "aurobindo") {
    return entry.list.map(a =>
      `<div class="voice-src">${esc(a.work || "Essays on the Gita")}${a.ref ? " · " + esc(a.ref) : ""}</div>
       <div class="voice-en">${esc(a.text)}</div>`).join('<hr class="voice-rule">');
  }
  if (entry.kind === "parallels") {
    return entry.list.map(p => {
      const body = (p.words && p.english)
        ? interactiveBlock(p.words, p.english)
        : `<div class="voice-sa" lang="sa-Latn">${esc(p.sanskrit)}</div>${p.ourRendering ? `<div class="voice-en">${esc(p.ourRendering)}</div>` : ""}`;
      return `<div class="voice-src">${esc(p.school || "")}${p.thinker ? " · " + esc(p.thinker) : ""} · ${esc(p.work || "")}${p.locus ? " " + esc(p.locus) : ""}</div>${body}`;
    }).join('<hr class="voice-rule">');
  }
  // commentary
  const c = entry.data;
  const body = (c.words && c.english)
    ? interactiveBlock(c.words, c.english)
    : `<div class="voice-sa" lang="sa-Latn">${esc(c.sanskrit)}</div>${c.ourRendering ? `<div class="voice-en">${esc(c.ourRendering)}</div>` : ""}`;
  return `<div class="voice-src">${esc(c.work || "")}${c.locus ? " · " + esc(c.locus) : ""}</div>${body}`;
}

function renderVerse(v, vb) {
  const sp = speakerLabel(v.speaker);
  const muIx = interactiveBlock(v.words, v.english);
  const blocks = (VOICES || []).map(voice => {
    const entry = vb[voice.id];
    if (!entry) return "";
    const who = (voice.thinkerId && HOST_THINKER)
      ? `<button class="voice-who voice-who-link" data-thinker="${esc(voice.thinkerId)}" type="button">${esc(voice.name)}${voice.school && voice.school !== "parallel" ? ` <span class="voice-school">${esc(voice.school)}</span>` : ""} <span class="who-go" aria-hidden="true">›</span></button>`
      : `<div class="voice-who">${esc(voice.name)}${voice.school && voice.school !== "parallel" ? ` <span class="voice-school">${esc(voice.school)}</span>` : ""}</div>`;
    return `<div class="voice-block" data-voice="${esc(voice.id)}" style="--vc:${voice.color}">
        ${who}
        ${renderVoiceInner(entry)}
      </div>`;
  }).join("");
  return `<article class="verse" id="v-${esc(v.locus)}">
    <header class="verse-head"><span class="verse-locus">${esc(v.locus)}</span>${sp ? `<span class="verse-speaker">${esc(sp)}</span>` : ""}</header>
    <div class="verse-sa" lang="sa-Latn">${esc(v.iast).replace(/\n/g, "<br>")}</div>
    ${muIx}
    ${blocks ? `<div class="verse-voices">${blocks}</div>` : ""}
  </article>`;
}

function renderVoiceBar() {
  if (!VOICES.length) return "";
  const chips = VOICES.map(voice =>
    `<button class="vchip" data-voice="${esc(voice.id)}" type="button" aria-pressed="false" style="--vc:${voice.color}">
       <span class="vdot" aria-hidden="true"></span>${esc(voice.name)}</button>`).join("");
  return `<div class="voicebar"><span class="voicebar-label" id="vbLabel">Commentary —</span>
    <div class="voicebar-chips" role="group" aria-labelledby="vbLabel">${chips}</div></div>`;
}

/* ---------- state ---------- */
let VERSES = [], VOICES = [], BYVERSE = {}, ROOT = null, GLOSS_BASE = "../../data/glossary/";
let HOST_GLOSSARY = null;   // when embedded, the app's real glossary popover
let HOST_THINKER = null;    // when embedded, opens a thinker in the Thinker tab
const VOICE_KEY = "gita-voices";
let active = new Set();

function readActive() {
  try { const a = JSON.parse(localStorage.getItem(VOICE_KEY) || "[]"); return new Set(Array.isArray(a) ? a : []); }
  catch (_) { return new Set(); }
}
function writeActive() { try { localStorage.setItem(VOICE_KEY, JSON.stringify([...active])); } catch (_) {} }

function applyActive() {
  document.querySelectorAll(".vchip").forEach(c => {   // chips may live in #voicebarSlot (standalone) or in ROOT (embed)
    const on = active.has(c.dataset.voice);
    c.classList.toggle("is-active", on);
    c.setAttribute("aria-pressed", on ? "true" : "false");
  });
  ROOT.querySelectorAll(".voice-block").forEach(b => {
    b.style.display = active.has(b.dataset.voice) ? "block" : "none";
  });
  ROOT.querySelectorAll(".verse-voices").forEach(wrap => {
    const any = [...wrap.children].some(b => b.style.display === "block");
    wrap.style.display = any ? "block" : "none";
  });
}
function toggleVoice(id) {
  if (active.has(id)) active.delete(id); else active.add(id);
  writeActive(); applyActive();
}

/* ---------- public render ---------- */
function render(root, opts) {
  opts = opts || {};
  ROOT = root;
  GLOSS_BASE = opts.glossaryBase || GLOSS_BASE;
  HOST_GLOSSARY = typeof opts.onGlossary === "function" ? opts.onGlossary : null;
  HOST_THINKER = typeof opts.onThinker === "function" ? opts.onThinker : null;
  VERSES = window.GITA_VERSES || [];
  const built = buildVoices(VERSES, {
    commentary: window.GITA_COMMENTARY, aurobindo: window.GITA_AUROBINDO, parallels: window.GITA_PARALLELS,
  });
  VOICES = built.voices; BYVERSE = built.byVerse;

  const bar = renderVoiceBar();
  const versesHtml = VERSES.map(v => renderVerse(v, BYVERSE[v.locus] || {})).join("");
  if (opts.voicebarSlot) { opts.voicebarSlot.innerHTML = bar; root.innerHTML = versesHtml; }
  else { root.innerHTML = `<div class="gita-reader">${bar}${versesHtml}</div>`; }

  wireWords();
  wireVoiceBar();
  active = readActive();
  applyActive();
}

/* ---------- word ↔ English highlight + card (CLICK ONLY) ---------- */
let sticky = null;
function scopeOf(span) { return span.closest("[data-wscope]"); }
function wordOf(span) {
  const sc = scopeOf(span); if (!sc) return null;
  const ws = SCOPES[sc.dataset.wscope]; if (!ws) return null;
  return ws.find(w => String(w.i) === String(span.dataset.wi));
}
function activate(span) {
  const sc = scopeOf(span); if (!sc) return;
  const i = span.dataset.wi;
  span.classList.add("hi");
  sc.querySelectorAll(".we").forEach(el => { if (el.dataset.wi.split(/\s+/).includes(i)) el.classList.add("hi"); });
  const w = wordOf(span); if (w) showCard(span, w);
}
function deactivate(span) {
  const sc = scopeOf(span); if (!sc) return;
  const i = span.dataset.wi;
  span.classList.remove("hi");
  sc.querySelectorAll(".we").forEach(el => { if (el.dataset.wi.split(/\s+/).includes(i)) el.classList.remove("hi"); });
  hideCard();
}
function clearSticky() { if (sticky) { deactivate(sticky); sticky = null; } }

function pinWord(w) {
  if (sticky === w) { clearSticky(); return; }
  if (sticky) deactivate(sticky);
  sticky = w; activate(w);
}
function wireWords() {
  ROOT.addEventListener("click", e => {
    const who = e.target.closest(".voice-who-link");
    if (who) { e.stopPropagation(); if (HOST_THINKER) HOST_THINKER(who.dataset.thinker); return; }
    const w = e.target.closest(".w");
    if (w) { e.stopPropagation(); pinWord(w); return; }
    // bidirectional: click an English phrase → highlight + card its Sanskrit word
    const we = e.target.closest(".we");
    if (we) {
      e.stopPropagation();
      const sc = we.closest("[data-wscope]"); if (!sc) return;
      const firstI = we.dataset.wi.split(/\s+/)[0];
      const wspan = sc.querySelector(`.w[data-wi="${firstI}"]`);
      if (wspan) pinWord(wspan);
    }
  });
  ROOT.addEventListener("keydown", e => {
    const w = e.target.closest(".w"); if (!w) return;
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); w.click(); }
  });
  document.addEventListener("click", e => {
    if (cardEl && cardEl.contains(e.target)) return;
    if (glossEl && glossEl.contains(e.target)) return;
    clearSticky();
  });
  document.addEventListener("keydown", e => {
    if (e.key !== "Escape") return;
    if (glossEl) { closeGlossary(); return; }
    clearSticky();
  });
  window.addEventListener("scroll", hideCard, { passive: true, capture: true });
}

let cardEl = null;
function ensureCard() {
  if (cardEl) return cardEl;
  cardEl = document.createElement("div");
  cardEl.className = "wcard"; cardEl.setAttribute("role", "tooltip"); cardEl.hidden = true;
  document.body.appendChild(cardEl);
  return cardEl;
}
function showCard(span, w) {
  const card = ensureCard();
  const rows = [];
  rows.push(`<div class="wc-top"><span class="wc-word" lang="sa-Latn">${esc(w.iast)}</span></div>`);
  rows.push(`<div class="wc-mean">${esc(w.gloss)}</div>`);
  const parts = w.parts && w.parts.length ? w.parts
    : (w.compound && w.compound.members ? w.compound.members.map(f => ({ form: f, gloss: "" })) : null);
  if (parts && (parts.length > 1 || (parts[0] && parts[0].gloss))) {
    rows.push(`<div class="wc-parts">${parts.map(p =>
      `<span class="wc-part"><span class="wc-pf" lang="sa-Latn">${esc(p.form)}</span>${p.gloss ? `<span class="wc-pg">${esc(p.gloss)}</span>` : ""}</span>`).join("")}</div>`);
  }
  const gram = [];
  if (w.morph) { const plain = plainMorph(w.morph); const cs = caseSense(plain);
    gram.push(`<span class="wc-gram-main">${esc(plain)}</span>${cs ? ` <span class="wc-gram-sense">→ “${esc(cs)}”</span>` : ""}`); }
  if (w.compound) gram.push(`<span class="wc-gram-cmp">${esc(w.compound.type)}: <span lang="sa-Latn">${esc(w.compound.vigraha)}</span></span>`);
  if (gram.length) rows.push(`<div class="wc-gram">${gram.join("<br>")}</div>`);
  if (w.glossaryKey) rows.push(`<button class="wc-gl" data-term="${esc(w.glossaryKey)}" type="button">${esc(w.iast)} in the glossary →</button>`);
  card.innerHTML = rows.join("");
  card.style.visibility = "hidden"; card.hidden = false; place(card, span); card.style.visibility = "visible";
  const gl = card.querySelector(".wc-gl");
  if (gl) gl.addEventListener("click", ev => {
    ev.stopPropagation();
    // Embedded: use the site's real glossary popover. Standalone: our own.
    if (HOST_GLOSSARY) HOST_GLOSSARY(gl.dataset.term, gl);
    else openGlossary(gl.dataset.term, gl);
  });
}
function hideCard() { if (cardEl) cardEl.hidden = true; }

function place(el, anchor) {
  const r = anchor.getBoundingClientRect();
  el.style.left = "0px"; el.style.top = "0px";
  const er = el.getBoundingClientRect();
  const margin = 10;
  let left = r.left + r.width / 2 - er.width / 2 + window.scrollX;
  let top = r.top - er.height - 10 + window.scrollY;
  const minL = window.scrollX + margin, maxL = window.scrollX + document.documentElement.clientWidth - er.width - margin;
  left = Math.max(minL, Math.min(maxL, left));
  if (top < window.scrollY + margin) top = r.bottom + 10 + window.scrollY;
  const maxT = window.scrollY + window.innerHeight - er.height - margin;
  if (top > maxT) top = Math.max(window.scrollY + margin, maxT);
  el.style.left = left + "px"; el.style.top = top + "px";
}

function wireVoiceBar() {
  const barEl = ROOT.querySelector(".voicebar") || document.querySelector("#voicebarSlot .voicebar");
  if (!barEl) return;
  barEl.addEventListener("click", e => { const chip = e.target.closest(".vchip"); if (chip) toggleVoice(chip.dataset.voice); });
}

/* ---------- glossary popover ---------- */
const glossCache = new Map();
async function loadGloss(key) {
  if (glossCache.has(key)) return glossCache.get(key);
  let e = null;
  try { const r = await fetch(GLOSS_BASE + key + ".json"); if (r.ok) e = await r.json(); } catch (_) {}
  glossCache.set(key, e); return e;
}
let glossEl = null, glossReturn = null;
async function openGlossary(key, anchor) {
  const e = await loadGloss(key);
  closeGlossary(); glossReturn = anchor || null;
  glossEl = document.createElement("div");
  glossEl.className = "gpop"; glossEl.setAttribute("role", "dialog"); glossEl.setAttribute("aria-labelledby", "gpTerm");
  if (!e) glossEl.innerHTML = `<button class="gp-x" aria-label="Close glossary">×</button><div class="gp-term" id="gpTerm">${esc(key)}</div><p class="gp-def">No glossary entry yet.</p>`;
  else {
    const perSchool = (e.per_school || []).map(s =>
      `<div class="gp-row"><span class="gp-school">${esc(s.school)}</span><span class="gp-def">${mdInline(s.definition)}</span></div>`).join("");
    glossEl.innerHTML = `<button class="gp-x" aria-label="Close glossary">×</button>
      <div class="gp-term" id="gpTerm" lang="sa-Latn">${esc(e.term_iast || key)}</div>
      ${e.literal ? `<div class="gp-lit">${mdInline(e.literal)}</div>` : ""}
      ${e.invariant_definition ? `<p class="gp-def">${mdInline(e.invariant_definition)}</p>` : ""}
      ${perSchool ? `<div class="gp-schools">${perSchool}</div>` : ""}
      ${e.translator_note ? `<div class="gp-note"><span class="gp-note-label">Translator note</span>${mdInline(e.translator_note)}</div>` : ""}`;
  }
  document.body.appendChild(glossEl);
  place(glossEl, anchor);
  const x = glossEl.querySelector(".gp-x"); x.addEventListener("click", closeGlossary); x.focus();
}
function closeGlossary() {
  if (!glossEl) return;
  glossEl.remove(); glossEl = null;
  if (glossReturn && glossReturn.focus) { try { glossReturn.focus(); } catch (_) {} }
  glossReturn = null;
}
window.addEventListener("scroll", () => { if (glossEl) closeGlossary(); }, { passive: true, capture: true });

/* ---------- expose ---------- */
window.GitaReader = { render };

// Standalone page bootstrap (no-op inside the app, where #gitaRoot is absent).
document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("gitaRoot");
  if (!root) return;
  render(root, { glossaryBase: "../../data/glossary/", voicebarSlot: document.getElementById("voicebarSlot") });
  const b = document.getElementById("gitaClose");
  if (b) b.addEventListener("click", () => { if (history.length > 1) history.back(); else window.location.href = "../../"; });
});
})();
