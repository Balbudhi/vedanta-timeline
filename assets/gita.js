/* =============================================================
   Bhagavad-Gītā 2.54–72 — reading engine.
   Renders window.GITA_VERSES (verses.js). Apparatus layers merge in
   by locus and are presented as ONE unified, selectable set of
   voices: the ācāryas (commentaries.js), Sri Aurobindo (aurobindo.js),
   and the cross-tradition parallels (parallels.js) — pick a name, see
   that voice across every verse. IAST only on screen.
   ============================================================= */

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

// Glossary entries use *italic* / **bold** markdown. Escape first, then render
// emphasis so asterisks don't show literally.
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
function plainMorph(m) {
  let s = " " + m + " ";
  for (const [re, full] of ABBR) s = s.replace(re, full);
  return s.trim();
}
const CASE_SENSE = {
  genitive: "of", instrumental: "by / with", locative: "in / on",
  dative: "to / for", ablative: "from", accusative: "the object",
  nominative: "the subject", vocative: "one addressed",
};
function caseSense(plain) {
  return CASE_SENSE[plain.split(/[ ,]/)[0]] || null;
}

/* ---------- English line: {indices:phrase} → highlightable spans ---------- */
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
    return `<span class="${cls}" data-wi="${w.i}" tabindex="0">${esc(w.iast)}</span>`;
  }).join(" ");
}

/* =============================================================
   VOICES — unify commentary + Aurobindo + parallels into one set.
   Each voice: { id, name, school, year, render(locusEntry|entries) }
   ============================================================= */
const VOICE_YEAR = {
  "Śaṅkara": 700, "Abhinavagupta": 975, "Rāmānuja": 1077,
  "Madhva (Ānandatīrtha)": 1238, "Madhva": 1238,
  "Śrīdhara Svāmī": 1400, "Śrīdhara": 1400,
  "Keśava Kāśmīrī": 1480,
  "Madhusūdana Sarasvatī": 1565, "Madhusūdana": 1565,
  "Baladeva": 1720, "Sri Aurobindo": 1916,
};
function voiceYear(name) { return VOICE_YEAR[name] != null ? VOICE_YEAR[name] : 9000; }

// Build, per verse, a map voiceId -> html block. Returns {voices:Set, byVerse:{locus:{voiceId:html}}}
function buildVoices(verses) {
  const com = window.GITA_COMMENTARY || {};
  const auro = window.GITA_AUROBINDO || {};
  const par = window.GITA_PARALLELS || {};
  const meta = {};               // voiceId -> {id,name,school,year,order}
  const byVerse = {};

  function ensure(id, name, school, year) {
    if (!meta[id]) meta[id] = { id, name, school: school || "", year: year != null ? year : 9000 };
  }
  function add(locus, id, html) {
    (byVerse[locus] = byVerse[locus] || {})[id] = html;
  }

  for (const v of verses) {
    const locus = v.locus;
    // commentary ācāryas (inline + commentaries.js)
    const coms = (v.commentaries || []).concat(com[locus] || []);
    for (const c of coms) {
      const id = "ac:" + c.author;
      ensure(id, c.author, c.school, voiceYear(c.author));
      add(locus, id, `
        <div class="voice-src">${esc(c.work || "")}${c.locus ? " · " + esc(c.locus) : ""}</div>
        <div class="voice-sa" lang="sa-Latn">${esc(c.sanskrit)}</div>
        ${c.ourRendering ? `<div class="voice-en">${esc(c.ourRendering)}</div>` : ""}`);
    }
    // Sri Aurobindo (English only)
    const au = auro[locus] || [];
    if (au.length) {
      ensure("aurobindo", "Sri Aurobindo", "Integral Yoga", voiceYear("Sri Aurobindo"));
      add(locus, "aurobindo", au.map(a =>
        `<div class="voice-src">${esc(a.work || "Essays on the Gita")}${a.ref ? " · " + esc(a.ref) : ""}</div>
         <div class="voice-en">${esc(a.text)}</div>`).join('<hr class="voice-rule">'));
    }
    // Cross-tradition parallels (one combined voice)
    const ps = par[locus] || [];
    if (ps.length) {
      ensure("parallels", "Across traditions", "parallel", 9500);
      add(locus, "parallels", ps.map(p =>
        `<div class="voice-src">${esc(p.school || "")}${p.thinker ? " · " + esc(p.thinker) : ""} · ${esc(p.work || "")}${p.locus ? " " + esc(p.locus) : ""}</div>
         <div class="voice-sa" lang="sa-Latn">${esc(p.sanskrit)}</div>
         ${p.ourRendering ? `<div class="voice-en">${esc(p.ourRendering)}</div>` : ""}`).join('<hr class="voice-rule">'));
    }
  }
  const voices = Object.values(meta).sort((a, b) =>
    (a.year - b.year) || a.name.localeCompare(b.name));
  return { voices, byVerse };
}

/* =============================================================
   RENDER
   ============================================================= */
let VERSES = [], VOICES = [], BYVERSE = {};
const VOICE_KEY = "gita-voice";

function speakerLabel(s) {
  return s === "arjuna" ? "Arjuna" : s === "krishna" ? "Kṛṣṇa" : "";
}

function renderVerse(v, idx) {
  const sp = speakerLabel(v.speaker);
  const vb = BYVERSE[v.locus] || {};
  const blocks = VOICES.map(voice =>
    vb[voice.id]
      ? `<div class="voice-block" data-voice="${esc(voice.id)}">
           <div class="voice-who">${esc(voice.name)}${voice.school && voice.school !== "parallel" ? ` <span class="voice-school">${esc(voice.school)}</span>` : ""}</div>
           ${vb[voice.id]}
         </div>`
      : "").join("");
  return `<article class="verse" id="v-${esc(v.locus)}" data-vidx="${idx}">
    <header class="verse-head">
      <span class="verse-locus">${esc(v.locus)}</span>${sp ? `<span class="verse-speaker">${esc(sp)}</span>` : ""}
    </header>
    <div class="verse-sa" lang="sa-Latn">${esc(v.iast).replace(/\n/g, "<br>")}</div>
    <div class="verse-pada" lang="sa-Latn">${renderPada(v.words)}</div>
    <div class="verse-en">${renderEnglish(v.english)}</div>
    ${blocks ? `<div class="verse-voices">${blocks}</div>` : ""}
  </article>`;
}

function renderVoiceBar() {
  if (!VOICES.length) return "";
  const chips = VOICES.map(voice =>
    `<button class="vchip" data-voice="${esc(voice.id)}" type="button" aria-pressed="false">${esc(voice.name)}</button>`).join("");
  return `<div class="voicebar" id="voicebar">
    <span class="voicebar-label" id="voicebarLabel">Read alongside:</span>
    <div class="voicebar-chips" role="group" aria-labelledby="voicebarLabel">
      <button class="vchip vchip-none" data-voice="" type="button" aria-pressed="true">Translation only</button>
      ${chips}
    </div>
  </div>`;
}

function render() {
  const root = document.getElementById("gitaRoot");
  if (!root) return;
  VERSES = window.GITA_VERSES || [];
  const built = buildVoices(VERSES);
  VOICES = built.voices; BYVERSE = built.byVerse;

  const slot = document.getElementById("voicebarSlot");
  if (slot) slot.innerHTML = renderVoiceBar();
  root.innerHTML = VERSES.map((v, i) => renderVerse(v, i)).join("");
  wireWords(root);
  wireVoiceBar();

  // restore persisted voice
  let saved = "";
  try { saved = localStorage.getItem(VOICE_KEY) || ""; } catch (_) {}
  setActiveVoice(saved && VOICES.some(v => v.id === saved) ? saved : "");
}

/* ---------- voice selection (global, sticky, consistent) ---------- */
function setActiveVoice(id) {
  const stage = document.getElementById("gitaStage");
  if (stage) stage.setAttribute("data-voice", id);
  let activeName = "Translation only";
  document.querySelectorAll(".vchip").forEach(c => {
    const on = (c.dataset.voice || "") === id;
    c.classList.toggle("is-active", on);
    c.setAttribute("aria-pressed", on ? "true" : "false");
    if (on) activeName = c.textContent.trim();
  });
  const status = document.getElementById("voiceStatus");
  if (status) status.textContent = id ? `Showing ${activeName} alongside each verse.` : "Translation only.";
  // Show only the chosen voice's block under each verse (global + consistent).
  document.querySelectorAll(".voice-block").forEach(b => {
    b.style.display = (id && b.dataset.voice === id) ? "block" : "none";
  });
  document.querySelectorAll(".verse-voices").forEach(wrap => {
    const sel = id ? `.voice-block[data-voice="${(window.CSS && CSS.escape) ? CSS.escape(id) : id}"]` : null;
    wrap.style.display = (sel && wrap.querySelector(sel)) ? "block" : "none";
  });
  try { localStorage.setItem(VOICE_KEY, id); } catch (_) {}
}
function wireVoiceBar() {
  const bar = document.getElementById("voicebar");
  if (!bar) return;
  bar.addEventListener("click", e => {
    const chip = e.target.closest(".vchip");
    if (!chip) return;
    setActiveVoice(chip.dataset.voice || "");
  });
}

/* =============================================================
   WORD ↔ English highlight + word-card
   ============================================================= */
function wordOf(verseEl, i) {
  const v = VERSES[+verseEl.dataset.vidx];
  return v && v.words.find(w => String(w.i) === String(i));
}
function activate(span) {
  const ve = span.closest(".verse"); if (!ve) return;
  const i = span.dataset.wi;
  span.classList.add("hi");
  ve.querySelectorAll(".we").forEach(el => { if (el.dataset.wi.split(/\s+/).includes(i)) el.classList.add("hi"); });
  const w = wordOf(ve, i); if (w) showCard(span, w);
}
function deactivate(span) {
  const ve = span.closest(".verse"); if (!ve) return;
  const i = span.dataset.wi;
  span.classList.remove("hi");
  ve.querySelectorAll(".we").forEach(el => { if (el.dataset.wi.split(/\s+/).includes(i)) el.classList.remove("hi"); });
  hideCard();
}
let sticky = null, hover = null;
function wireWords(root) {
  root.addEventListener("mouseover", e => {
    const w = e.target.closest(".w"); if (!w || w === hover) return;
    if (hover && hover !== sticky) deactivate(hover);
    hover = w; activate(w);
  });
  root.addEventListener("mouseout", e => {
    const w = e.target.closest(".w"); if (!w) return;
    const to = e.relatedTarget;
    if (to && (w.contains(to) || (cardEl && cardEl.contains(to)))) return;
    if (w !== sticky) deactivate(w);
    if (hover === w) hover = null;
  });
  root.addEventListener("click", e => {
    const w = e.target.closest(".w"); if (!w) return;
    e.stopPropagation();
    if (sticky === w) { sticky = null; deactivate(w); return; }
    if (sticky) deactivate(sticky);
    sticky = w; activate(w);
  });
  document.addEventListener("click", e => {
    if (cardEl && cardEl.contains(e.target)) return;
    if (glossEl && glossEl.contains(e.target)) return;
    if (sticky) { deactivate(sticky); sticky = null; }
  });
  root.addEventListener("focusin", e => { const w = e.target.closest(".w"); if (w) activate(w); });
  root.addEventListener("focusout", e => { const w = e.target.closest(".w"); if (!w || w === sticky) return; deactivate(w); });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      if (glossEl) { closeGlossary(); return; }      // close glossary first
      if (sticky) { deactivate(sticky); sticky = null; }
    }
  });
  window.addEventListener("scroll", () => { hideCard(); }, { passive: true });
}

let cardEl = null;
function ensureCard() {
  if (cardEl) return cardEl;
  cardEl = document.createElement("div");
  cardEl.className = "wcard";
  cardEl.setAttribute("role", "tooltip");
  cardEl.hidden = true;
  // Leaving the card (when no word is pinned) clears the hover state so the
  // card + highlight don't linger after the pointer moves away.
  cardEl.addEventListener("mouseleave", () => {
    if (sticky) return;
    if (hover) { deactivate(hover); hover = null; }
    else hideCard();
  });
  document.body.appendChild(cardEl);
  return cardEl;
}
function showCard(span, w) {
  const card = ensureCard();
  const rows = [];
  rows.push(`<div class="wc-top"><span class="wc-word" lang="sa-Latn">${esc(w.iast)}</span></div>`);
  rows.push(`<div class="wc-mean">${esc(w.gloss)}</div>`);

  // built-from pieces (translated morphemes)
  const parts = w.parts && w.parts.length ? w.parts
    : (w.compound && w.compound.members ? w.compound.members.map(f => ({ form: f, gloss: "" })) : null);
  if (parts && (parts.length > 1 || (parts[0] && parts[0].gloss))) {
    rows.push(`<div class="wc-parts">${parts.map(p =>
      `<span class="wc-part"><span class="wc-pf" lang="sa-Latn">${esc(p.form)}</span>${p.gloss ? `<span class="wc-pg">${esc(p.gloss)}</span>` : ""}</span>`).join("")}</div>`);
  }

  // grammar in plain English
  const gram = [];
  if (w.morph) {
    const plain = plainMorph(w.morph);
    const cs = caseSense(plain);
    gram.push(`<span class="wc-gram-main">${esc(plain)}</span>${cs ? ` <span class="wc-gram-sense">→ “${esc(cs)}”</span>` : ""}`);
  }
  if (w.compound) gram.push(`<span class="wc-gram-cmp">${esc(w.compound.type)}: <span lang="sa-Latn">${esc(w.compound.vigraha)}</span></span>`);
  if (gram.length) rows.push(`<div class="wc-gram">${gram.join("<br>")}</div>`);

  if (w.glossaryKey) rows.push(`<button class="wc-gl" data-term="${esc(w.glossaryKey)}" type="button">More in glossary →</button>`);

  card.innerHTML = rows.join("");
  card.style.visibility = "hidden";   // measure off-screen to avoid a top-left flash
  card.hidden = false;
  place(card, span);
  card.style.visibility = "visible";
  const gl = card.querySelector(".wc-gl");
  if (gl) gl.addEventListener("click", ev => { ev.stopPropagation(); openGlossary(gl.dataset.term, gl); });
}
function hideCard() { if (cardEl) cardEl.hidden = true; }

function place(el, anchor) {
  const r = anchor.getBoundingClientRect();
  el.style.left = "0px"; el.style.top = "0px";
  const er = el.getBoundingClientRect();
  const margin = 10;
  let left = r.left + r.width / 2 - er.width / 2 + window.scrollX;
  let top = r.top - er.height - 10 + window.scrollY;
  const minL = window.scrollX + margin;
  const maxL = window.scrollX + document.documentElement.clientWidth - er.width - margin;
  left = Math.max(minL, Math.min(maxL, left));
  if (top < window.scrollY + margin) top = r.bottom + 10 + window.scrollY;
  const maxT = window.scrollY + window.innerHeight - er.height - margin;
  if (top > maxT) top = Math.max(window.scrollY + margin, maxT);
  el.style.left = left + "px"; el.style.top = top + "px";
}

/* ---------- glossary popover (lazy) ---------- */
const GLOSS_BASE = "../../data/glossary/";
const glossCache = new Map();
async function loadGloss(key) {
  if (glossCache.has(key)) return glossCache.get(key);
  let e = null;
  try { const r = await fetch(GLOSS_BASE + key + ".json"); if (r.ok) e = await r.json(); } catch (_) {}
  glossCache.set(key, e); return e;
}
let glossEl = null, glossReturnFocus = null;
async function openGlossary(key, anchor) {
  const e = await loadGloss(key);
  closeGlossary();
  glossReturnFocus = anchor || null;
  glossEl = document.createElement("div");
  glossEl.className = "gpop";
  glossEl.setAttribute("role", "dialog");
  glossEl.setAttribute("aria-modal", "false");
  glossEl.setAttribute("aria-labelledby", "gpTerm");
  if (!e) {
    glossEl.innerHTML = `<button class="gp-x" aria-label="Close glossary">×</button><div class="gp-term" id="gpTerm">${esc(key)}</div><p class="gp-def">No glossary entry yet.</p>`;
  } else {
    glossEl.innerHTML = `<button class="gp-x" aria-label="Close glossary">×</button>
      <div class="gp-term" id="gpTerm" lang="sa-Latn">${esc(e.term_iast || key)}</div>
      ${e.literal ? `<div class="gp-lit">${mdInline(e.literal)}</div>` : ""}
      ${e.invariant_definition ? `<p class="gp-def">${mdInline(e.invariant_definition)}</p>` : ""}
      ${e.translator_note ? `<p class="gp-note">${mdInline(e.translator_note)}</p>` : ""}`;
  }
  document.body.appendChild(glossEl);
  place(glossEl, anchor);
  const x = glossEl.querySelector(".gp-x");
  x.addEventListener("click", closeGlossary);
  x.focus();
}
function closeGlossary() {
  if (!glossEl) return;
  glossEl.remove(); glossEl = null;
  if (glossReturnFocus && glossReturnFocus.focus) { try { glossReturnFocus.focus(); } catch (_) {} }
  glossReturnFocus = null;
}
window.addEventListener("scroll", () => { if (glossEl) closeGlossary(); }, { passive: true });

/* ---------- close / back ---------- */
function wireClose() {
  const b = document.getElementById("gitaClose");
  if (!b) return;
  b.addEventListener("click", () => {
    // referrer is always empty (meta no-referrer), so gate on history depth.
    if (history.length > 1) history.back();
    else window.location.href = "../../";
  });
}

document.addEventListener("DOMContentLoaded", () => { render(); wireClose(); });
