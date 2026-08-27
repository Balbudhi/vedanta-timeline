/* Viṣṇu Sahasranāma — rendered in the same language as GitaReader. */
(function () {
"use strict";

let ROOT = null;
let DATA = null;
let LINKIFY = null;
let ON_THINKER = null;
let WORD_CARD = null;
let ACTIVE_NUMBER = null;
let COMMENTARY_OPEN = false;

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

function paragraphs(text) {
  return String(text || "").split(/\n\s*\n/).filter(Boolean).map(paragraph =>
    `<p>${LINKIFY ? LINKIFY(paragraph) : esc(paragraph)}</p>`
  ).join("");
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
  return stanza.names.map(name => `<span class="we vsn-we" role="button" tabindex="0" data-name-number="${name.number}">${esc(name.meaning)}</span>`).join('<span class="vsn-sep" aria-hidden="true"> · </span>');
}

function renderCommentary(stanza) {
  return stanza.names.map(name => `<section class="vsn-commentary-entry" id="vsn-commentary-${name.number}">
    <div class="voice-src"><span lang="sa-Latn">${esc((name.word_analysis || {}).citation_iast || name.citation_iast_ocr || name.surface_iast)}</span> · name ${name.number} · scan page${name.chinmayananda.scan_pages.length > 1 ? "s" : ""} ${name.chinmayananda.scan_pages.join(", ")}</div>
    <div class="voice-en">${paragraphs(name.chinmayananda.commentary)}</div>
  </section>`).join("");
}

function renderStanza(stanza) {
  return `<article class="verse vsn-verse" id="vsn-stanza-${stanza.number}">
    <header class="verse-head"><span class="verse-locus">${stanza.number}</span><span class="verse-speaker">Names ${range(stanza)}</span></header>
    <div class="verse-deva vsn-deva" lang="sa-Deva">${renderDevanagari(stanza)}</div>
    <div class="ix" data-stanza="${stanza.number}">
      <div class="ix-pada" lang="sa-Latn">${renderNames(stanza)}</div>
      <div class="ix-en">${renderEnglish(stanza)}</div>
    </div>
    <div class="verse-voices">
      <div class="voice-block vsn-commentary-block" data-stanza-number="${stanza.number}" style="--vc:#9b2226">
        <button class="voice-who voice-who-link vsn-thinker-link" type="button">Swami Chinmayananda <span class="voice-school">Advaita</span> <span class="who-go" aria-hidden="true">›</span></button>
        <div class="voice-src"><em>Thousand Ways to the Transcendental</em></div>
        <div class="vsn-commentary-content"></div>
      </div>
    </div>
  </article>`;
}

function renderVoiceBar() {
  return `<div class="voicebar">
    <span class="voicebar-label">Commentary —</span>
    <div class="voicebar-chips" role="group" aria-label="Commentary voice">
      <button class="vchip vsn-voice-chip" type="button" aria-pressed="false" style="--vc:#9b2226"><span class="vdot" aria-hidden="true"></span>Swami Chinmayananda</button>
    </div>
  </div>`;
}

function renderAudio() {
  return `<div class="recite-bar vsn-recite-bar" id="vsnReciteBar">
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

function openWordCard(number, anchor) {
  const name = DATA.stanzas.flatMap(stanza => stanza.names).find(item => item.number === Number(number));
  if (!name) return;
  closeWordCard();
  ACTIVE_NUMBER = name.number;
  ROOT.querySelectorAll(`[data-name-number="${name.number}"]`).forEach(element => element.classList.add("hi"));
  const analysis = name.word_analysis || {};
  const parts = Array.isArray(analysis.parts) && analysis.parts.length
    ? `<div class="wc-parts">${analysis.parts.map(part => `<span class="wc-part"><span class="wc-pf" lang="sa-Latn">${esc(part.form_iast)}</span><span class="wc-pg">${esc(part.gloss)}</span></span>`).join("")}</div>`
    : "";
  const root = analysis.root
    ? `<div class="wc-root"><span class="wc-pf">${esc(analysis.root.form)}</span><span class="wc-pg">: ${esc(`${analysis.root.gana}, ${analysis.root.pada} · ${analysis.root.gloss}`)}</span></div>`
    : "";
  const derivation = analysis.derivation
    ? `<div class="wc-derivation"><span class="wc-note-label">Chinmayananda</span>${esc(analysis.derivation)}</div>`
    : "";
  const compound = analysis.compound
    ? `<div class="wc-gram-cmp"><em>${esc(analysis.compound.type)}</em>: ${esc(analysis.compound.vigraha)}</div>`
    : "";
  const sandhi = analysis.sandhi && !analysis.sandhi.startsWith("No surface change")
    ? `<div class="wc-note">${esc(analysis.sandhi)}</div>`
    : "";
  const grammar = `<div class="wc-gram"><span class="wc-gram-main">${esc(analysis.morph || "")}</span><br><span class="wc-gram-stem">stem: <span lang="sa-Latn">${esc(analysis.stem || "")}</span></span><br><span class="wc-gram-affix">formation: ${esc(analysis.affix || "")}</span>${compound ? `<br>${compound}` : ""}</div>${sandhi}`;
  const read = `<button class="wc-gl vsn-read-commentary" type="button" data-name-number="${name.number}">Read Chinmayananda’s full explanation</button>`;
  const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
  const deva = analysis.citation_devanagari || name.deva;
  WORD_CARD = document.createElement("div");
  WORD_CARD.className = "wcard vsn-wcard";
  WORD_CARD.setAttribute("role", "dialog");
  WORD_CARD.innerHTML = `<button class="vsn-wcard-close" type="button" aria-label="Close">×</button><div class="wc-top"><span class="wc-word" lang="sa-Latn">${esc(citation)}</span> <span class="vsn-card-number">${name.number}</span></div><div class="vsn-card-deva" lang="sa-Deva">${esc(deva)}</div>${parts}${root}${grammar}${derivation}<div class="wc-gls">${read}</div>`;
  document.body.append(WORD_CARD);
  WORD_CARD.querySelector(".vsn-wcard-close").addEventListener("click", closeWordCard);
  WORD_CARD.querySelector(".vsn-read-commentary").addEventListener("click", () => {
    setCommentary(true);
    const entry = document.getElementById(`vsn-commentary-${name.number}`);
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
    const close = event.target.closest(".vsn-wcard-close");
    if (close) { closeWordCard(); return; }
    const read = event.target.closest(".vsn-read-commentary");
    if (read) {
      setCommentary(true);
      const entry = document.getElementById(`vsn-commentary-${read.dataset.nameNumber}`);
      closeWordCard();
      if (entry) entry.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
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

function setCommentary(open) {
  const chip = ROOT.querySelector(".vsn-voice-chip");
  COMMENTARY_OPEN = Boolean(open);
  chip.classList.toggle("is-active", COMMENTARY_OPEN);
  chip.setAttribute("aria-pressed", String(COMMENTARY_OPEN));
  ROOT.querySelectorAll(".vsn-commentary-block").forEach(block => {
      if (COMMENTARY_OPEN && block.dataset.loaded !== "true") {
        const stanza = DATA.stanzas[Number(block.dataset.stanzaNumber) - 1];
        block.querySelector(".vsn-commentary-content").innerHTML = renderCommentary(stanza);
        block.dataset.loaded = "true";
      }
      block.style.display = COMMENTARY_OPEN ? "block" : "none";
  });
}

function wireVoice() {
  const chip = ROOT.querySelector(".vsn-voice-chip");
  chip.addEventListener("click", () => {
    setCommentary(!COMMENTARY_OPEN);
    closeWordCard();
  });
  ROOT.addEventListener("click", event => {
    if (event.target.closest(".vsn-thinker-link") && ON_THINKER) ON_THINKER("chinmayananda");
  });
}

function wireAudio() {
  const bar = ROOT.querySelector(".vsn-recite-bar");
  const audio = bar.querySelector("audio");
  const play = bar.querySelector(".vsn-play");
  const progress = bar.querySelector(".vsn-progress");
  const fill = bar.querySelector(".rb-bar");
  const time = bar.querySelector(".rb-time");
  let dragging = false;
  const total = () => audio.duration || DATA.audio.duration_seconds || 0;
  const paint = () => {
    const percent = total() ? (audio.currentTime / total()) * 100 : 0;
    fill.style.width = `${percent}%`;
    progress.setAttribute("aria-valuenow", String(Math.round(percent)));
    time.textContent = `${fmtTime(audio.currentTime)} / ${fmtTime(total())}`;
  };
  play.addEventListener("click", () => audio.paused ? audio.play().catch(() => {}) : audio.pause());
  bar.querySelector(".vsn-back").addEventListener("click", () => { audio.currentTime = Math.max(0, audio.currentTime - 15); paint(); });
  bar.querySelector(".vsn-forward").addEventListener("click", () => { audio.currentTime = Math.min(total(), audio.currentTime + 15); paint(); });
  audio.addEventListener("play", () => { play.classList.add("is-playing"); bar.classList.add("is-playing"); play.setAttribute("aria-label", "Pause"); });
  audio.addEventListener("pause", () => { play.classList.remove("is-playing"); bar.classList.remove("is-playing"); play.setAttribute("aria-label", "Play"); });
  audio.addEventListener("timeupdate", () => { if (!dragging) paint(); });
  audio.addEventListener("loadedmetadata", paint);
  const seek = event => {
    const rect = progress.getBoundingClientRect();
    const fraction = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    audio.currentTime = fraction * total();
    paint();
  };
  progress.addEventListener("pointerdown", event => { dragging = true; progress.setPointerCapture(event.pointerId); seek(event); });
  progress.addEventListener("pointermove", event => { if (dragging) seek(event); });
  progress.addEventListener("pointerup", event => { dragging = false; try { progress.releasePointerCapture(event.pointerId); } catch (_) {} });
  progress.addEventListener("keydown", event => {
    if (event.key === "ArrowRight") { audio.currentTime = Math.min(total(), audio.currentTime + 5); paint(); event.preventDefault(); }
    if (event.key === "ArrowLeft") { audio.currentTime = Math.max(0, audio.currentTime - 5); paint(); event.preventDefault(); }
  });
  paint();
}

async function render(root, options) {
  options = options || {};
  ensureStyle(options.styleUrl || "assets/sahasranama.css");
  ROOT = root;
  LINKIFY = typeof options.linkifyGlossary === "function" ? options.linkifyGlossary : null;
  ON_THINKER = typeof options.onThinker === "function" ? options.onThinker : null;
  COMMENTARY_OPEN = false;
  closeWordCard();
  root.innerHTML = '<p style="color:var(--muted);font-style:italic">Opening the thousand names…</p>';
  const response = await fetch(options.dataUrl || "gita/vishnu-sahasranama/reader.json");
  if (!response.ok) throw new Error(`Could not load reader data (${response.status})`);
  DATA = await response.json();
  root.innerHTML = `<div class="gita-reader vsn-reader">${renderVoiceBar()}<div class="vsn-attribution">Mahābhārata · received chanting text collated with the BORI critical edition · commentary from Swami Chinmayananda’s <em>Thousand Ways to the Transcendental</em>, published here with permission</div>${DATA.stanzas.map(renderStanza).join("")}${renderAudio()}</div>`;
  wireWords();
  wireVoice();
  wireAudio();
}

window.SahasranamaReader = { render };
})();
