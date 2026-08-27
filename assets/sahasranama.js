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

function detailFor(name) {
  return String(name?.chinmayananda?.detail || "").trim();
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
  return stanza.names.map(name => `<span class="we vsn-we" role="button" tabindex="0" data-name-number="${name.number}">${esc(name.meaning)}</span>`).join('<span class="vsn-sep" aria-hidden="true"> · </span>');
}

function renderDetails(stanza) {
  return stanza.names.map(name => {
    const detail = detailFor(name);
    if (!detail) return "";
    const analysis = name.word_analysis || {};
    const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
    const deva = analysis.citation_devanagari || name.deva;
    return `<section class="vsn-detail-entry" id="vsn-detail-${name.number}">
      <button class="vsn-detail-name" type="button" data-name-number="${name.number}" aria-label="Open the analysis for name ${name.number}, ${esc(citation)}">
        <span class="vsn-detail-number">${name.number}</span>
        <span class="vsn-detail-iast" lang="sa-Latn">${esc(citation)}</span>
        <span class="vsn-detail-deva" lang="sa-Deva">${esc(deva)}</span>
      </button>
      <div class="vsn-detail-copy">${paragraphs(detail)}</div>
      <div class="vsn-detail-source">Swami Chinmayananda · <em>Thousand Ways to the Transcendental</em> · ${esc(pageLabel(name))}</div>
    </section>`;
  }).join("");
}

function renderStanza(stanza) {
  return `<article class="verse vsn-verse" id="vsn-stanza-${stanza.number}">
    <header class="verse-head"><span class="verse-locus">${stanza.number}</span><span class="verse-speaker">Names ${range(stanza)}</span></header>
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

function renderDetailToggle() {
  return `<div class="voicebar vsn-viewbar">
    <span class="voicebar-label">View —</span>
    <div class="voicebar-chips" role="group" aria-label="Reader detail">
      <button class="vchip vsn-detail-chip" type="button" aria-pressed="false"><span class="vsn-detail-icon" aria-hidden="true">+</span>Detailed explanations</button>
    </div>
  </div>`;
}

function renderAttribution() {
  return `<div class="vsn-attribution">
    <div class="vsn-attribution-kicker">Traditional Advaita reading</div>
    <div class="vsn-attribution-primary"><button class="vsn-attribution-author vsn-thinker-link" type="button">Swami Chinmayananda</button> · <em>Thousand Ways to the Transcendental</em></div>
    <div class="vsn-attribution-role">English definitions and commentary</div>
    <div class="vsn-attribution-text">Sanskrit text: <em>Viṣṇusahasranāma</em>, Mahābhārata, Anuśāsanaparvan · received text collated with the BORI critical edition</div>
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
    ? `<div class="wc-root"><span class="wc-pf">${esc(analysis.root.form)}</span><span class="wc-pg">: ${esc(`${analysis.root.gana}, ${analysis.root.pada} · ${analysis.root.gloss}`)}</span></div>`
    : "";
  const compound = analysis.compound
    ? `<div class="wc-gram-cmp"><em>${esc(analysis.compound.type)}</em>: ${esc(analysis.compound.vigraha)}</div>`
    : "";
  const sandhi = analysis.sandhi && !analysis.sandhi.startsWith("No surface change")
    ? `<div class="wc-note">${esc(analysis.sandhi)}</div>`
    : "";
  const grammar = `<div class="wc-gram"><span class="wc-gram-main">${esc(analysis.morph || "")}</span><br><span class="wc-gram-stem">stem: <span lang="sa-Latn">${esc(analysis.stem || "")}</span></span><br><span class="wc-gram-affix">formation: ${esc(analysis.affix || "")}</span>${compound ? `<br>${compound}` : ""}</div>${sandhi}`;
  const definition = `<div class="wc-mean vsn-card-definition"><span class="wc-note-label">Chinmayananda’s definition</span>${esc(name.meaning)}</div>`;
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
    await setDetails(true);
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
  const chip = ROOT.querySelector(".vsn-detail-chip");
  if (open) {
    chip.setAttribute("aria-busy", "true");
    const loaded = await ensureDetails();
    chip.removeAttribute("aria-busy");
    if (!loaded) return;
  }
  DETAILS_OPEN = Boolean(open);
  chip.classList.toggle("is-active", DETAILS_OPEN);
  chip.setAttribute("aria-pressed", String(DETAILS_OPEN));
  const icon = chip.querySelector(".vsn-detail-icon");
  if (icon) icon.textContent = DETAILS_OPEN ? "−" : "+";
  ROOT.querySelectorAll(".vsn-details-block").forEach(block => {
      if (DETAILS_OPEN && block.dataset.loaded !== "true") {
        const stanza = DATA.stanzas[Number(block.dataset.stanzaNumber) - 1];
        block.querySelector(".vsn-details-content").innerHTML = renderDetails(stanza);
        block.dataset.loaded = "true";
      }
      block.hidden = !DETAILS_OPEN;
  });
}

function wireDetails() {
  const chip = ROOT.querySelector(".vsn-detail-chip");
  chip.addEventListener("click", async () => {
    await setDetails(!DETAILS_OPEN);
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
  const startedAt = performance.now();
  options = options || {};
  ensureStyle(options.styleUrl || "assets/sahasranama.css");
  ROOT = root;
  LINKIFY = typeof options.linkifyGlossary === "function" ? options.linkifyGlossary : null;
  ON_THINKER = typeof options.onThinker === "function" ? options.onThinker : null;
  DETAILS_OPEN = false;
  closeWordCard();
  root.innerHTML = '<p style="color:var(--muted);font-style:italic">Opening the thousand names…</p>';
  const response = await fetch(options.dataUrl || "gita/vishnu-sahasranama/reader.json");
  if (!response.ok) throw new Error(`Could not load reader data (${response.status})`);
  const fetchedAt = performance.now();
  DATA = await response.json();
  const parsedAt = performance.now();
  DETAILS_URL = options.detailsUrl || "";
  DETAILS_PROMISE = null;
  NAME_BY_NUMBER = new Map(DATA.stanzas.flatMap(stanza => stanza.names).map(name => [Number(name.number), name]));
  root.innerHTML = `<div class="gita-reader vsn-reader">${renderAttribution()}${renderDetailToggle()}${DATA.stanzas.map(renderStanza).join("")}${renderAudio()}</div>`;
  const renderedAt = performance.now();
  const reader = root.querySelector(".vsn-reader");
  if (reader) {
    reader.dataset.readyMs = String(Math.round(renderedAt - startedAt));
    reader.dataset.fetchMs = String(Math.round(fetchedAt - startedAt));
    reader.dataset.parseMs = String(Math.round(parsedAt - fetchedAt));
    reader.dataset.renderMs = String(Math.round(renderedAt - parsedAt));
  }
  wireWords();
  wireDetails();
  wireAudio();
}

window.SahasranamaReader = { render };
})();
