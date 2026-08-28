/* Viṣṇu Sahasranāma — rendered in the same language as GitaReader. */
(function () {
"use strict";

let ROOT = null;
let DATA = null;
let LINKIFY = null;
let ON_THINKER = null;
let WORD_CARD = null;
let ACTIVE_NUMBER = null;
let DETAILS_OPEN = false;
let DETAILS_URL = "";
let DETAILS_PROMISE = null;
let NAME_BY_NUMBER = new Map();
let CHANT_ONLY = false;
let TIMING_BY_ID = new Map();
let ACTIVE_TIMING_ID = null;
let AUDIO_ELEMENT = null;
let MODE_HOST = null;
const CHANT_VIEW_KEY = "vedanta:vishnu-sahasranama:chant-only";

function esc(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function ensureStyle(href) {
  if (document.querySelector(`link[data-sahasranama-style="${href}"]`)) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  link.dataset.sahasranamaStyle = href;
  document.head.append(link);
}

function fmtTime(seconds) {
  if (!Number.isFinite(seconds)) return "0:00";
  return `${Math.floor(seconds / 60)}:${Math.floor(seconds % 60).toString().padStart(2, "0")}`;
}

function richProse(text) {
  const link = value => LINKIFY ? LINKIFY(value) : esc(value);
  const source = String(text || "").replace(/[*†‡]+/g, "");
  const quote = /[“"]([^”"]+)[”"]/g;
  let out = "", last = 0, match;
  while ((match = quote.exec(source)) !== null) {
    out += link(source.slice(last, match.index));
    out += `<q>${link(match[1])}</q>`;
    last = match.index + match[0].length;
  }
  return out + link(source.slice(last));
}

function paragraphs(text) {
  return String(text || "").split(/\n\s*\n/).filter(Boolean)
    .map(paragraph => /^\s*[\u0900-\u097f]/.test(paragraph)
      ? `<blockquote class="vsn-source-passage">${richProse(paragraph).replace(/\n/g, "<br>")}</blockquote>`
      : `<p class="vsn-prose">${richProse(paragraph)}</p>`)
    .join("");
}

function commentaryBlocks(name) {
  const blocks = name.chinmayananda?.blocks;
  if (!Array.isArray(blocks) || !blocks.length) return paragraphs(name.chinmayananda?.commentary || "");
  return blocks.map(block => {
    if (block.type === "prose") return `<p class="vsn-prose">${richProse(block.text)}</p>`;
    if (block.type !== "gita-quote") return "";
    const hasReviewedWords = Array.isArray(block.words) && block.words.length > 0;
    const sanskrit = hasReviewedWords && window.GitaReader?.interactiveBlock
      ? window.GitaReader.interactiveBlock(block.words, block.english_slots || null, null, block.devanagari, "vsn-commentary-quote-deva")
      : `<div class="ix"><div class="ix-deva vsn-commentary-quote-deva" lang="sa-Deva">${esc(block.devanagari)}</div><div class="ix-pada" lang="sa-Latn">${esc(block.iast)}</div></div>`;
    const printed = (block.printed_loci || []).join(", ");
    const source = printed && !block.printed_loci.includes(block.canonical_locus)
      ? `${block.canonical_locus} · printed as ${printed}`
      : block.canonical_locus;
    const notes = (block.textual_notes || []).map(note => `<div class="vsn-quote-note">${esc(note)}</div>`).join("");
    return `<blockquote class="vsn-commentary-quote" data-quote-id="${esc(block.id)}">
      ${sanskrit}
      <footer class="vsn-commentary-quote-source">${esc(source)}</footer>
      ${notes}
    </blockquote>`;
  }).join("");
}

function detailFor(name) {
  return String(name?.chinmayananda?.detail || "").trim();
}

function displayDefinition(value) {
  const text = String(value || "").trim();
  if (/^["'“”‘’]/.test(text) && /["'“”‘’]$/.test(text)) return text.slice(1, -1).trim();
  return text;
}

function simpleExcerpt(name) {
  return displayDefinition(name?.meaning);
}

function pageLabel(name) {
  const pages = name.chinmayananda.scan_pages || [];
  return `p${pages.length === 1 ? "." : "p."} ${pages.join("–")}`;
}

async function ensureDetails() {
  if (!DETAILS_URL) return false;
  if (!DETAILS_PROMISE) {
    DETAILS_PROMISE = fetch(DETAILS_URL)
      .then(response => {
        if (!response.ok) throw new Error(`Could not load reader details (${response.status})`);
        return response.json();
      })
      .then(payload => {
        for (const detail of (payload.names || [])) {
          const name = NAME_BY_NUMBER.get(Number(detail.number));
          if (name) Object.assign(name, detail);
        }
        return true;
      })
      .catch(() => false);
  }
  return DETAILS_PROMISE;
}

function range(stanza) {
  const numbers = stanza.name_numbers || [];
  return numbers.length ? `${numbers[0]}–${numbers[numbers.length - 1]}` : "";
}

function renderDevanagari(stanza) {
  const lines = [0, 1].map(lineIndex => stanza.names.filter(name => name.line_index === lineIndex).map(name => {
    const form = name.deva_surface || name.deva;
    return `<span class="w vsn-deva-w" role="button" tabindex="0" data-name-number="${name.number}" aria-label="Name ${name.number}: ${esc(form)}">${esc(form)}</span>`;
  }).join(" "));
  return `${lines[0]} <span class="vsn-sep" aria-hidden="true">।</span><br>${lines[1]} <span class="vsn-sep" aria-hidden="true">॥</span>`;
}

function renderNames(stanza) {
  return stanza.names.map(name => {
    const form = (name.word_analysis || {}).citation_iast || name.citation_iast || name.surface_iast;
    return `<span class="w vsn-w" role="button" tabindex="0" data-name-number="${name.number}" aria-label="Name ${name.number}: ${esc(form)}">${esc(form)}</span>`;
  }).join(" ");
}

function renderEnglish(stanza) {
  const lines = [0, 1].map(lineIndex => {
    const names = stanza.names.filter(name => name.line_index === lineIndex);
    if (!names.length) return "";
    const rows = names.map(name => {
      const analysis = name.word_analysis || {};
      const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
      const deva = analysis.citation_devanagari || name.deva;
      const meaning = simpleExcerpt(name).replace(/[.;:]\s*$/, "");
      return `<span class="we vsn-we vsn-meaning-item" role="button" tabindex="0" data-name-number="${name.number}" aria-label="${esc(`${deva}; ${citation}: ${meaning}`)}"><span class="vsn-meaning-deva" lang="sa-Deva">${esc(deva)}</span><span class="vsn-meaning-name" lang="sa-Latn">${esc(citation)}</span><span class="vsn-meaning-text">${esc(meaning)}</span></span>`;
    }).join("");
    return `<div class="vsn-meaning-group" data-line-index="${lineIndex}">${rows}</div>`;
  }).join("");
  return `<div class="vsn-meanings">${lines}</div>`;
}

function renderDetails(stanza) {
  return stanza.names.map(name => {
    const commentary = String(name.chinmayananda?.commentary || "").trim();
    const analysis = name.word_analysis || {};
    const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
    const deva = analysis.citation_devanagari || name.deva;
    return `<section class="vsn-detail-entry" id="vsn-detail-${name.number}">
      <button class="vsn-detail-name" type="button" data-name-number="${name.number}" aria-label="Open the analysis for name ${name.number}, ${esc(citation)}">
        <span class="vsn-detail-number">${name.number}</span>
        <span class="vsn-detail-iast" lang="sa-Latn">${esc(citation)}</span>
        <span class="vsn-detail-deva" lang="sa-Deva">${esc(deva)}</span>
      </button>
      ${commentary ? `<div class="vsn-detail-copy">${commentaryBlocks(name)}</div>` : ""}
      <div class="vsn-detail-source">Swami Chinmayananda · <em>Thousand Ways to the Transcendental</em> · ${esc(pageLabel(name))}</div>
    </section>`;
  }).join("");
}

function timingPlayButton(id, label) {
  if (!TIMING_BY_ID.has(id)) return "";
  return `<button class="verse-play vsn-unit-play" type="button" data-timing-target="${esc(id)}" aria-label="Play from ${esc(label)}" title="Play from here"><span class="vp-icon" aria-hidden="true"></span></button>`;
}

function renderStanza(stanza) {
  const timingId = `stanza-${stanza.number}`;
  return `<article class="verse vsn-verse" id="vsn-stanza-${stanza.number}" data-timing-id="${timingId}">
    <header class="verse-head"><span class="verse-locus">${stanza.number}</span><span class="verse-speaker">Names ${range(stanza)}</span>${timingPlayButton(timingId, `stanza ${stanza.number}`)}</header>
    <div class="verse-deva vsn-deva" lang="sa-Deva">${renderDevanagari(stanza)}</div>
    <div class="ix" data-stanza="${stanza.number}">
      <div class="ix-pada" lang="sa-Latn">${renderNames(stanza)}</div>
      <div class="ix-en">${renderEnglish(stanza)}</div>
    </div>
    <div class="vsn-details-block" data-stanza-number="${stanza.number}" hidden>
      <div class="vsn-details-content"></div>
    </div>
  </article>`;
}

function renderPrefaceUnit(unit, groupId, groupTitle) {
  const compact = groupId === "assignment" ? " vsn-preface-unit--compact" : "";
  const interactive = unit.words?.length && unit.english && window.GitaReader?.interactiveBlock
    ? window.GitaReader.interactiveBlock(unit.words, unit.english, null, unit.devanagari, "vsn-preface-deva")
    : `<div class="verse-deva vsn-preface-deva" lang="sa-Deva">${esc(unit.devanagari).replace(/\n/g, "<br>")}</div>
       <div class="ix vsn-preface-ix"><div class="ix-pada vsn-preface-iast" lang="sa-Latn">${esc(unit.iast).replace(/\n/g, "<br>")}</div></div>`;
  const chinmayananda = unit.chinmayananda?.english;
  const label = unit.label || ({ "closing-name": "Closing", protection: "Protection" }[unit.id] || unit.id);
  const titleClass = /^\d+$/.test(label) ? "" : " vsn-preface-unit-title";
  const playbackLabel = groupTitle ? `${groupTitle} ${label}` : label;
  return `<article class="verse vsn-preface-unit${compact}" id="vsn-${esc(unit.id)}" data-timing-id="${esc(unit.id)}">
    <header class="verse-head"><span class="verse-locus${titleClass}">${esc(label)}</span>${unit.speaker ? `<span class="verse-speaker">${esc(unit.speaker)}</span>` : ""}${timingPlayButton(unit.id, playbackLabel)}</header>
    ${interactive}
    ${chinmayananda ? `<div class="voice-block vsn-preface-unit-commentary" hidden>
      <div class="voice-who">Swami Chinmayananda <span class="voice-school">Advaita</span></div>
      <div class="voice-en">${esc(chinmayananda)}</div>
    </div>` : ""}
  </article>`;
}

function renderPrefaceGroup(group) {
  const commentary = group.chinmayananda;
  const pages = commentary?.scan_pages || [];
  return `<section class="vsn-preface-group" data-preface-group="${esc(group.id)}">
    <h3 class="vsn-preface-group-title">${esc(group.title)}</h3>
    ${group.units.map(unit => renderPrefaceUnit(unit, group.id, group.title)).join("")}
    ${commentary ? `<aside class="vsn-preface-commentary" hidden>
      <div class="vsn-preface-commentary-title">${esc(commentary.title)}</div>
      <p>${esc(commentary.detail)}</p>
      <div class="vsn-detail-source">Swami Chinmayananda · <em>Thousand Ways to the Transcendental</em> · p${pages.length === 1 ? "." : "p."} ${esc(pages.join("–"))}</div>
    </aside>` : ""}
  </section>`;
}

function renderPreface() {
  const groups = DATA.preface?.groups || [];
  if (!groups.length) return "";
  return `<section class="vsn-preface" aria-labelledby="vsn-preface-title">
    <header class="vsn-section-head"><span id="vsn-preface-title">Before the thousand names</span><span>Opening in this recording</span></header>
    <p class="vsn-preface-intro">This performance begins with the invocation, the Mahābhārata dialogue, the ritual assignment, and meditation. The thousand names follow.</p>
    ${groups.map(renderPrefaceGroup).join("")}
  </section>`;
}

function renderNamesSection() {
  return `<section class="vsn-names-section" aria-labelledby="vsn-names-title">
    <header class="vsn-section-head vsn-sticky-section vsn-names-head"><span id="vsn-names-title">Names</span><span>1–1000</span></header>
    ${DATA.stanzas.map(renderStanza).join("")}
  </section>`;
}

function renderPostlude() {
  const units = DATA.postlude || [];
  if (!units.length) return "";
  return `<section class="vsn-postlude" aria-labelledby="vsn-postlude-title">
    <header class="vsn-section-head vsn-sticky-section vsn-postlude-head"><span id="vsn-postlude-title">Conclusion</span><span>As performed in this recording</span></header>
    ${units.map(unit => renderPrefaceUnit(unit, "postlude", "Conclusion")).join("")}
  </section>`;
}

function renderDetailToggle() {
  return `<button class="dp-reader-mode-btn vsn-detail-chip" type="button" aria-label="Full reading" aria-pressed="false">Full</button>
    <button class="dp-reader-mode-btn vsn-chant-chip" type="button" aria-label="Simplified reading" aria-pressed="false">Simplified</button>`;
}

function modeControl(selector) {
  return (MODE_HOST || ROOT)?.querySelector(selector);
}

function renderAttribution() {
  return `<div class="vsn-attribution">
    <div class="vsn-attribution-kicker">Source and attribution</div>
    <div class="vsn-attribution-primary"><button class="vsn-attribution-author vsn-thinker-link" type="button">Swami Chinmayananda</button> · <em>Thousand Ways to the Transcendental</em></div>
    <div class="vsn-attribution-role vsn-full-attribution"><strong>Full</strong> presents Swami Chinmayananda’s complete commentary in his words.</div>
    <div class="vsn-attribution-role vsn-simplified-attribution"><strong>Simplified</strong> is a site-generated concise reading derived from his explanations. The Simplified wording is not credited to him as a translation or quotation.</div>
    <div class="vsn-attribution-text">Sanskrit text: <em>Viṣṇusahasranāma</em>, Mahābhārata, Anuśāsanaparvan · received text collated with the BORI critical edition.</div>
  </div>`;
}

function renderAudio() {
  return `<div class="recite-bar reader-media-dock vsn-recite-bar" id="vsnReciteBar">
    <audio preload="metadata" src="${esc(DATA.audio.src)}"></audio>
    <div class="rb-controls">
      <button class="rb-skip vsn-back" type="button" aria-label="Back 15 seconds"><svg class="rb-skip-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/><text class="rb-skip-num" x="12" y="15.6" text-anchor="middle">15</text></svg></button>
      <button class="rb-play vsn-play" type="button" aria-label="Play"><span class="rb-icon" aria-hidden="true"></span></button>
      <button class="rb-skip vsn-forward" type="button" aria-label="Forward 15 seconds"><svg class="rb-skip-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V1l5 5-5 5V7c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6h2c0 4.42-3.58 8-8 8s-8-3.58-8-8 3.58-8 8-8z"/><text class="rb-skip-num" x="12" y="15.6" text-anchor="middle">15</text></svg></button>
    </div>
    <div class="rb-progress vsn-progress" role="slider" aria-label="Seek" tabindex="0" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="rb-bar"></div></div>
    <span class="rb-time">0:00 / ${fmtTime(DATA.audio.duration_seconds)}</span>
    <span class="rb-reciter">${esc(DATA.audio.performer)}</span>
  </div>`;
}

function closeWordCard() {
  if (WORD_CARD) WORD_CARD.remove();
  WORD_CARD = null;
  ACTIVE_NUMBER = null;
  if (ROOT) ROOT.querySelectorAll(".hi").forEach(element => element.classList.remove("hi"));
}

function placeCard(card, anchor) {
  const rect = anchor.getBoundingClientRect();
  const margin = 10;
  const cardRect = card.getBoundingClientRect();
  let left = rect.left;
  let top = rect.bottom + 8;
  if (left + cardRect.width > innerWidth - margin) left = innerWidth - cardRect.width - margin;
  if (top + cardRect.height > innerHeight - margin) top = Math.max(margin, rect.top - cardRect.height - 8);
  card.style.left = `${Math.max(margin, left)}px`;
  card.style.top = `${top}px`;
}

async function openWordCard(number, anchor) {
  await ensureDetails();
  const name = NAME_BY_NUMBER.get(Number(number));
  if (!name) return;
  closeWordCard();
  ACTIVE_NUMBER = name.number;
  ROOT.querySelectorAll(`[data-name-number="${name.number}"]`).forEach(element => element.classList.add("hi"));
  const analysis = name.word_analysis || {};
  const parts = Array.isArray(analysis.parts) && analysis.parts.length
    ? `<div class="wc-parts">${analysis.parts.map(part => `<span class="wc-part"><span class="wc-pf" lang="sa-Latn">${esc(part.form_iast)}</span><span class="wc-pg">${esc(part.gloss)}</span></span>`).join("")}</div>`
    : "";
  const root = analysis.root
    ? `<div class="wc-root"><span class="wc-pf">${esc(analysis.root.form)}</span><span class="wc-pg">: ${esc(`${analysis.root.gana}, ${analysis.root.pada} · ${analysis.root.gloss}`)}</span>${analysis.root.dhatupatha ? `<span class="wc-pg"><br>Dhātupāṭha ${esc(analysis.root.dhatupatha.locus)} · <span lang="sa-Deva">${esc(analysis.root.dhatupatha.artha_sanskrit)}</span></span>` : ""}</div>`
    : "";
  const compound = analysis.compound
    ? `<div class="wc-gram-cmp"><em>${esc(analysis.compound.type)}</em>: ${esc(analysis.compound.vigraha)}</div>`
    : "";
  const sandhi = analysis.sandhi && !analysis.sandhi.startsWith("No surface change")
    ? `<div class="wc-note">${esc(analysis.sandhi)}</div>`
    : "";
  const grammar = `<div class="wc-gram"><span class="wc-gram-main">${esc(analysis.morph || "")}</span><br><span class="wc-gram-stem">stem: <span lang="sa-Latn">${esc(analysis.stem || "")}</span></span><br><span class="wc-gram-affix">formation: ${esc(analysis.affix || "")}</span>${compound ? `<br>${compound}` : ""}</div>${sandhi}`;
  const definition = `<div class="wc-mean vsn-card-definition"><span class="wc-note-label">Site-generated Simplified summary</span>${esc(simpleExcerpt(name))}</div>`;
  const detail = detailFor(name);
  const explanationAction = detail
    ? `<div class="wc-gls vsn-card-detail-action"><button class="wc-gl vsn-show-detail" type="button">Show detailed explanation ↓</button></div>`
    : "";
  const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
  const deva = analysis.citation_devanagari || name.deva;
  WORD_CARD = document.createElement("div");
  WORD_CARD.className = "wcard vsn-wcard";
  WORD_CARD.setAttribute("role", "dialog");
  WORD_CARD.innerHTML = `<button class="vsn-wcard-close" type="button" aria-label="Close">×</button><div class="wc-top"><span class="wc-word" lang="sa-Latn">${esc(citation)}</span> <span class="vsn-card-number">${name.number}</span></div><div class="vsn-card-deva" lang="sa-Deva">${esc(deva)}</div>${definition}${parts}${root}${grammar}${explanationAction}`;
  document.body.append(WORD_CARD);
  WORD_CARD.querySelector(".vsn-wcard-close").addEventListener("click", closeWordCard);
  const showDetail = WORD_CARD.querySelector(".vsn-show-detail");
  if (showDetail) showDetail.addEventListener("click", async () => {
    await setChantView(false);
    const entry = document.getElementById(`vsn-detail-${name.number}`);
    closeWordCard();
    if (entry) entry.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  placeCard(WORD_CARD, anchor);
}

function wireWords() {
  const highlight = (number, on) => {
    ROOT.querySelectorAll(`[data-name-number="${number}"]`).forEach(element => element.classList.toggle("hl", on));
  };
  ROOT.addEventListener("pointerover", event => {
    const target = event.target.closest("[data-name-number]");
    if (target && ROOT.contains(target)) highlight(target.dataset.nameNumber, true);
  });
  ROOT.addEventListener("pointerout", event => {
    const target = event.target.closest("[data-name-number]");
    if (target && ROOT.contains(target)) highlight(target.dataset.nameNumber, false);
  });
  ROOT.addEventListener("focusin", event => {
    const target = event.target.closest("[data-name-number]");
    if (target && ROOT.contains(target)) highlight(target.dataset.nameNumber, true);
  });
  ROOT.addEventListener("focusout", event => {
    const target = event.target.closest("[data-name-number]");
    if (target && ROOT.contains(target) && Number(target.dataset.nameNumber) !== ACTIVE_NUMBER) highlight(target.dataset.nameNumber, false);
  });
  ROOT.addEventListener("click", event => {
    const target = event.target.closest("[data-name-number]");
    if (target && ROOT.contains(target)) {
      event.stopPropagation();
      if (ACTIVE_NUMBER === Number(target.dataset.nameNumber)) closeWordCard();
      else openWordCard(target.dataset.nameNumber, target);
    }
  });
  ROOT.addEventListener("keydown", event => {
    const target = event.target.closest(".vsn-we, .vsn-w, .vsn-deva-w");
    if (target && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      openWordCard(target.dataset.nameNumber, target);
    } else if (event.key === "Escape") closeWordCard();
  });
}

async function setDetails(open) {
  const chip = modeControl(".vsn-detail-chip");
  if (open) {
    chip?.setAttribute("aria-busy", "true");
    const loaded = await ensureDetails();
    chip?.removeAttribute("aria-busy");
    if (!loaded) return;
  }
  DETAILS_OPEN = Boolean(open);
  chip?.classList.toggle("is-active", DETAILS_OPEN);
  chip?.setAttribute("aria-pressed", String(DETAILS_OPEN));
  ROOT.querySelector(".vsn-reader")?.classList.toggle("vsn-details-open", DETAILS_OPEN);
  ROOT.querySelectorAll(".vsn-preface-commentary").forEach(block => { block.hidden = !DETAILS_OPEN; });
  ROOT.querySelectorAll(".vsn-preface-unit-commentary").forEach(block => { block.hidden = !DETAILS_OPEN; });
  ROOT.querySelectorAll(".vsn-details-block").forEach(block => {
      if (DETAILS_OPEN && block.dataset.loaded !== "true") {
        const stanza = DATA.stanzas[Number(block.dataset.stanzaNumber) - 1];
        block.querySelector(".vsn-details-content").innerHTML = renderDetails(stanza);
        block.dataset.loaded = "true";
      }
      block.hidden = !DETAILS_OPEN;
  });
}

function readChantView() {
  try { return localStorage.getItem(CHANT_VIEW_KEY) === "true"; }
  catch (_) { return false; }
}

async function setChantView(active, persist) {
  CHANT_ONLY = Boolean(active);
  ROOT.querySelector(".vsn-reader")?.classList.toggle("vsn-chant-only", CHANT_ONLY);
  const chantChip = modeControl(".vsn-chant-chip");
  const detailChip = modeControl(".vsn-detail-chip");
  chantChip?.classList.toggle("is-active", CHANT_ONLY);
  chantChip?.setAttribute("aria-pressed", String(CHANT_ONLY));
  detailChip?.classList.toggle("is-active", !CHANT_ONLY);
  detailChip?.setAttribute("aria-pressed", String(!CHANT_ONLY));
  await setDetails(!CHANT_ONLY);
  closeWordCard();
  window.GitaReader?.clearWords?.();
  if (persist !== false) {
    try { localStorage.setItem(CHANT_VIEW_KEY, String(CHANT_ONLY)); } catch (_) {}
  }
  if (CHANT_ONLY && ACTIVE_TIMING_ID) {
    ROOT.querySelector(`[data-timing-id="${CSS.escape(ACTIVE_TIMING_ID)}"]`)?.scrollIntoView({ behavior: "auto", block: "center" });
  }
}

function wireDetails() {
  modeControl(".vsn-detail-chip")?.addEventListener("click", () => setChantView(false));
  modeControl(".vsn-chant-chip")?.addEventListener("click", () => setChantView(true));
  ROOT.addEventListener("click", event => {
    if (event.target.closest(".vsn-thinker-link") && ON_THINKER) ON_THINKER("chinmayananda");
  });
}

function timingAt(seconds) {
  for (const unit of (DATA.audio.units || [])) {
    if (seconds >= unit.start && seconds < unit.end) return unit.id;
  }
  return null;
}

function setActiveTiming(id, follow) {
  if (id === ACTIVE_TIMING_ID) return;
  if (ACTIVE_TIMING_ID) {
    const previous = ROOT.querySelector(`[data-timing-id="${CSS.escape(ACTIVE_TIMING_ID)}"]`);
    previous?.classList.remove("is-reciting");
    previous?.removeAttribute("aria-current");
  }
  ACTIVE_TIMING_ID = id;
  if (!id) return;
  const active = ROOT.querySelector(`[data-timing-id="${CSS.escape(id)}"]`);
  active?.classList.add("is-reciting");
  active?.setAttribute("aria-current", "true");
  if (follow && CHANT_ONLY) active?.scrollIntoView({ behavior: "auto", block: "center" });
}

function wireAudio() {
  const bar = ROOT.querySelector(".vsn-recite-bar");
  const audio = bar.querySelector("audio");
  AUDIO_ELEMENT = audio;
  const play = bar.querySelector(".vsn-play");
  const progress = bar.querySelector(".vsn-progress");
  const fill = bar.querySelector(".rb-bar");
  const time = bar.querySelector(".rb-time");
  let dragging = false;
  let syncFrame = 0;
  const total = () => audio.duration || DATA.audio.duration_seconds || 0;
  const paint = () => {
    const percent = total() ? (audio.currentTime / total()) * 100 : 0;
    fill.style.width = `${percent}%`;
    progress.setAttribute("aria-valuenow", String(Math.round(percent)));
    time.textContent = `${fmtTime(audio.currentTime)} / ${fmtTime(total())}`;
  };
  const sync = follow => setActiveTiming(timingAt(audio.currentTime), follow);
  const tick = () => {
    if (!dragging) paint();
    sync(true);
    if (!audio.paused && !audio.ended) syncFrame = requestAnimationFrame(tick);
    else syncFrame = 0;
  };
  const startClock = () => {
    sync(true);
    if (!syncFrame) syncFrame = requestAnimationFrame(tick);
  };
  const seekTo = start => {
    const run = () => {
      audio.currentTime = start;
      sync(false);
      paint();
      audio.play().catch(() => {});
    };
    if (audio.readyState >= HTMLMediaElement.HAVE_METADATA) run();
    else audio.addEventListener("loadedmetadata", run, { once: true });
  };

  play.addEventListener("click", () => audio.paused ? audio.play().catch(() => {}) : audio.pause());
  bar.querySelector(".vsn-back").addEventListener("click", () => { audio.currentTime = Math.max(0, audio.currentTime - 15); sync(false); paint(); });
  bar.querySelector(".vsn-forward").addEventListener("click", () => { audio.currentTime = Math.min(total(), audio.currentTime + 15); sync(false); paint(); });
  audio.addEventListener("play", () => {
    play.classList.add("is-playing"); bar.classList.add("is-playing"); play.setAttribute("aria-label", "Pause"); startClock();
  });
  audio.addEventListener("pause", () => {
    play.classList.remove("is-playing"); bar.classList.remove("is-playing"); play.setAttribute("aria-label", "Play");
    if (syncFrame) cancelAnimationFrame(syncFrame); syncFrame = 0;
  });
  audio.addEventListener("timeupdate", () => { if (!dragging) paint(); sync(false); });
  audio.addEventListener("seeking", () => sync(false));
  audio.addEventListener("loadedmetadata", paint);
  audio.addEventListener("ended", () => setActiveTiming(null, false));

  const seek = event => {
    const rect = progress.getBoundingClientRect();
    const fraction = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    audio.currentTime = fraction * total();
    sync(false);
    paint();
  };
  progress.addEventListener("pointerdown", event => { dragging = true; progress.setPointerCapture(event.pointerId); seek(event); });
  progress.addEventListener("pointermove", event => { if (dragging) seek(event); });
  progress.addEventListener("pointerup", event => { dragging = false; try { progress.releasePointerCapture(event.pointerId); } catch (_) {} });
  progress.addEventListener("keydown", event => {
    if (event.key === "ArrowRight") { audio.currentTime = Math.min(total(), audio.currentTime + 5); sync(false); paint(); event.preventDefault(); }
    if (event.key === "ArrowLeft") { audio.currentTime = Math.max(0, audio.currentTime - 5); sync(false); paint(); event.preventDefault(); }
  });

  if (ROOT._vsnUnitPlayHandler) ROOT.removeEventListener("click", ROOT._vsnUnitPlayHandler);
  ROOT._vsnUnitPlayHandler = event => {
    const button = event.target.closest(".vsn-unit-play");
    if (!button) return;
    event.stopPropagation();
    const timing = TIMING_BY_ID.get(button.dataset.timingTarget);
    if (!timing) return;
    if (!audio.paused && ACTIVE_TIMING_ID === timing.id) audio.pause();
    else seekTo(timing.start);
  };
  ROOT.addEventListener("click", ROOT._vsnUnitPlayHandler);
  paint();
  sync(false);
}

async function render(root, options) {
  const startedAt = performance.now();
  options = options || {};
  ensureStyle(options.styleUrl || "assets/sahasranama.css");
  ROOT = root;
  MODE_HOST = options.modeHost || null;
  LINKIFY = typeof options.linkifyGlossary === "function" ? options.linkifyGlossary : null;
  ON_THINKER = typeof options.onThinker === "function" ? options.onThinker : null;
  DETAILS_OPEN = false;
  CHANT_ONLY = readChantView();
  if (AUDIO_ELEMENT) AUDIO_ELEMENT.pause();
  AUDIO_ELEMENT = null;
  ACTIVE_TIMING_ID = null;
  closeWordCard();
  root.innerHTML = '<p style="color:var(--muted);font-style:italic">Opening the thousand names…</p>';
  const response = await fetch(options.dataUrl || "gita/vishnu-sahasranama/reader.json");
  if (!response.ok) throw new Error(`Could not load reader data (${response.status})`);
  const fetchedAt = performance.now();
  DATA = await response.json();
  const parsedAt = performance.now();
  DETAILS_URL = options.detailsUrl || "";
  DETAILS_PROMISE = null;
  TIMING_BY_ID = new Map((DATA.audio.units || []).map(unit => [unit.id, unit]));
  NAME_BY_NUMBER = new Map(DATA.stanzas.flatMap(stanza => stanza.names).map(name => [Number(name.number), name]));
  if (MODE_HOST) {
    MODE_HOST.innerHTML = renderDetailToggle();
    MODE_HOST.hidden = false;
  }
  root.innerHTML = `<div class="gita-reader vsn-reader">${renderAttribution()}${renderPreface()}${renderNamesSection()}${renderPostlude()}${renderAudio()}</div>`;
  const renderedAt = performance.now();
  const reader = root.querySelector(".vsn-reader");
  if (reader) {
    reader.dataset.readyMs = String(Math.round(renderedAt - startedAt));
    reader.dataset.fetchMs = String(Math.round(fetchedAt - startedAt));
    reader.dataset.parseMs = String(Math.round(parsedAt - fetchedAt));
    reader.dataset.renderMs = String(Math.round(renderedAt - parsedAt));
  }
  wireWords();
  window.GitaReader?.bindWords?.(root, {
    onGlossary: options.onGlossary,
    onThinker: options.onThinker,
    linkifyGlossary: options.linkifyGlossary,
    glossaryResolve: options.glossaryResolve,
  });
  wireDetails();
  wireAudio();
  await setChantView(CHANT_ONLY, false);
}

window.SahasranamaReader = { render };
})();
