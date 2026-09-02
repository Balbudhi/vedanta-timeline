/* Reading-specific additions layered on the shared GitaReader. */
(function () {
  "use strict";

  const byLocus = new Map();
  const semanticFields = new Map();
  const PUBLIC_APPARATUS_IDS = new Set(["robot-reading-critical"]);
  let semanticBundle = null;

  function rootLabel(root) {
    if (!root || typeof root !== "object") return root || null;
    const qualifiers = [root.gana, root.pada].filter(Boolean).join(" · ");
    return `${root.form}${qualifiers ? ` · ${qualifiers}` : ""}`;
  }

  function prepareWords(words) {
    return (words || []).map((source) => {
      const word = structuredClone(source);
      if (word.root && typeof word.root === "object") {
        word.rootRecord = structuredClone(word.root);
        word.rootGloss = word.root.gloss || word.rootGloss || "";
        word.root = rootLabel(word.root);
      }
      word.semanticFields = (word.semanticFieldKeys || [])
        .map((key) => semanticFields.get(key))
        .filter(Boolean)
        .map((field) => structuredClone(field));
      return word;
    });
  }

  function prepare(verses, bundle) {
    byLocus.clear();
    semanticFields.clear();
    semanticBundle = bundle ? structuredClone(bundle) : null;
    for (const field of semanticBundle?.fields || []) semanticFields.set(field.key, field);
    return (verses || []).map((source) => {
      const verse = structuredClone(source);
      verse.words = prepareWords(source.words);
      verse.apparatus = (source.apparatus || []).map((entry) => ({
        ...structuredClone(entry),
        words: prepareWords(entry.words),
      }));
      byLocus.set(verse.locus, verse);
      return verse;
    });
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function renderSourceScript(container, segments) {
    if (!container || !segments?.length) return;
    container.replaceChildren();
    for (const segment of segments) {
      if (segment.word_indices?.length) {
        const word = el("span", "wsg w-deva", segment.text);
        word.dataset.wi = segment.word_indices.join(" ");
        word.tabIndex = 0;
        word.setAttribute("role", "button");
        word.setAttribute("lang", "sa-Deva");
        container.append(word);
        continue;
      }
      const pieces = segment.text.split("\n");
      pieces.forEach((piece, index) => {
        if (piece) container.append(document.createTextNode(piece));
        if (index < pieces.length - 1) container.append(document.createElement("br"));
      });
    }
  }

  function renderTextualNotes(notes) {
    if (!notes || !notes.length) return null;
    const wrap = el("aside", "yv-textual-notes");
    wrap.setAttribute("aria-label", "Textual notes");
    for (const note of notes) {
      const block = el("div", "yv-textual-note");
      block.append(el("div", "yv-layer-label", "Textual note"));
      if (note.printed_and_transcribed) block.append(el("div", "yv-note-row", `Printed: ${note.printed_and_transcribed}`));
      if (note.parallel_reading) block.append(el("div", "yv-note-row", `Parallel: ${note.parallel_reading}`));
      wrap.append(block);
    }
    return wrap;
  }

  function renderApparatus(verse) {
    const entries = (verse.apparatus || []).filter((entry) =>
      PUBLIC_APPARATUS_IDS.has(entry.id)
      && (entry.status === "producer-complete" || entry.public_ready === true)
    );
    if (!entries.length) return null;
    const section = el("section", "yv-apparatus");
    section.setAttribute("aria-label", "Textual apparatus");
    for (const entry of entries) {
      const details = el("details", "yv-apparatus-block");
      const witness = entry.id === "robot-reading-critical"
        ? "Earlier Kashmirian Mokṣopāya reading"
        : entry.id === "robot-reading-vulgate"
          ? "Later received Yoga-Vāsiṣṭha reading"
          : entry.witness;
      const summary = el("summary", "yv-apparatus-summary", `${witness} · ${entry.locus}`);
      details.append(summary);
      if (entry.devanagari && entry.words?.length && entry.english && window.GitaReader) {
        const holder = el("div", "yv-apparatus-reading");
        holder.dataset.yvApparatusId = entry.id;
        holder.innerHTML = window.GitaReader.interactiveBlock(entry.words, entry.english, null, entry.devanagari);
        renderSourceScript(holder.querySelector(".ix-deva"), entry.sourceSegments);
        details.append(holder);
      }
      if (entry.script_normalization) {
        details.append(el("div", "yv-apparatus-provenance", "Script note: Devanāgarī normalized from the critical edition's IAST."));
      } else if (entry.status_reason) {
        details.append(el("div", "yv-apparatus-provenance", entry.status_reason));
      }
      const witnessId = entry.id === "robot-reading-critical"
        ? "mokshopaya-critical"
        : entry.id === "robot-reading-vulgate"
          ? "yogavasistha-vulgate"
          : null;
      const history = semanticBundle?.witness_history?.find((item) => item.id === witnessId);
      if (history) details.append(el("div", "yv-apparatus-provenance", history.description));
      if (entry.sense) details.append(el("div", "yv-apparatus-sense", entry.sense));
      section.append(details);
    }
    return section;
  }

  function evidenceLine(label, value) {
    if (!value) return null;
    const row = el("div", "yv-evidence-row");
    row.append(el("span", "yv-evidence-key", label));
    row.append(document.createTextNode(String(value)));
    return row;
  }

  function renderDerivation(derivation) {
    const block = el("div", "yv-derivation");
    block.append(el("div", "yv-derivation-label", derivation.label || derivation.category || derivation.kind || "Supported analysis"));
    const main = derivation.analysis || derivation.formation || derivation.segmentation || "";
    if (main) block.append(el("div", "yv-derivation-main", main));
    for (const root of derivation.roots || []) {
      block.append(evidenceLine("Root", rootLabel(root)));
      const dhatu = root.dhatupatha || {};
      block.append(evidenceLine("Dhātupāṭha", [dhatu.locus, dhatu.aupadeshika_devanagari, dhatu.artha_sanskrit].filter(Boolean).join(" · ")));
    }
    if (derivation.meaning) block.append(evidenceLine("Meaning", derivation.meaning));
    if (derivation.qualification) block.append(evidenceLine("Qualification", derivation.qualification));
    if (derivation.evidence) block.append(evidenceLine("Evidence", Array.isArray(derivation.evidence) ? derivation.evidence.join("; ") : derivation.evidence));
    return block;
  }

  function renderSemanticField(field) {
    const block = el("section", "yv-semantic-field");
    block.append(el("div", "yv-semantic-heading", `${field.lemma_iast} · inherited semantic field`));
    block.append(el("div", "yv-semantic-opening", field.opening));
    if (field.chronology_note) block.append(el("div", "yv-semantic-chronology", field.chronology_note));
    for (const reading of field.readings || []) {
      const item = el("div", "yv-semantic-reading");
      item.append(el("div", "yv-derivation-label", reading.category));
      if (reading.formation) item.append(el("div", "yv-derivation-main", reading.formation));
      item.append(evidenceLine("Meaning", reading.meaning));
      if (reading.source_label) {
        item.append(evidenceLine("Source", [reading.source_label, reading.source_locus].filter(Boolean).join(" · ")));
      }
      if (reading.qualification) item.append(evidenceLine("Qualification", reading.qualification));
      block.append(item);
    }
    return block;
  }

  function appendWordEvidence(card, word) {
    if (!card || !word || card.querySelector(`.yv-word-evidence[data-yv-word="${word.i}"]`)) return;
    const section = el("section", "yv-word-evidence");
    section.dataset.yvWord = String(word.i);
    if (word.rootRecord) {
      section.append(el("div", "yv-layer-label", "Root evidence"));
      const root = word.rootRecord;
      section.append(evidenceLine("Root", rootLabel(root)));
      const dhatu = root.dhatupatha || {};
      section.append(evidenceLine("Dhātupāṭha", [dhatu.locus, dhatu.aupadeshika_devanagari, dhatu.artha_sanskrit].filter(Boolean).join(" · ")));
    }
    const derivations = word.parallelDerivations || word.derivations || [];
    if (derivations.length) {
      section.append(el("div", "yv-layer-label", "Parallel supported analyses"));
      derivations.forEach((derivation) => section.append(renderDerivation(derivation)));
    }
    if (word.semanticFields?.length) {
      section.append(el("div", "yv-layer-label", "Intentional semantic field"));
      word.semanticFields.forEach((field) => section.append(renderSemanticField(field)));
    }
    if (section.childElementCount) card.append(section);
  }

  function clampCardToViewport(card) {
    const gutter = 10;
    const rect = card.getBoundingClientRect();
    const top = Math.max(gutter, Math.min(rect.top, window.innerHeight - rect.height - gutter));
    const left = Math.max(gutter, Math.min(rect.left, window.innerWidth - rect.width - gutter));
    card.style.top = `${top}px`;
    card.style.left = `${left}px`;
  }

  function enhanceCard(root, event) {
    const trigger = event.target.closest(".w, .we, .wsg");
    if (!trigger || !root.contains(trigger)) return;
    queueMicrotask(() => {
      const card = document.querySelector(".wcard:not([hidden])");
      const article = trigger.closest(".verse");
      const locus = article?.querySelector(".verse-locus")?.textContent?.trim();
      const verse = byLocus.get(locus);
      if (!card || !verse) return;
      const indices = String(trigger.dataset.wi || "").split(/\s+/).filter(Boolean).map(Number);
      const apparatusId = trigger.closest("[data-yv-apparatus-id]")?.dataset.yvApparatusId;
      const words = apparatusId
        ? verse.apparatus.find((entry) => entry.id === apparatusId)?.words || []
        : verse.words;
      indices.forEach((index) => appendWordEvidence(card, words.find((word) => word.i === index)));
      clampCardToViewport(card);
    });
  }

  function ensureStylesheet() {
    if (document.querySelector('link[data-yv-dama-style]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "gita/yogavasistha-dama/reader.css?v=20260901-yv-dama-v2";
    link.dataset.yvDamaStyle = "1";
    document.head.append(link);
  }

  function afterRender(root, verses) {
    ensureStylesheet();
    for (const verse of verses || []) {
      const article = [...root.querySelectorAll(".verse")].find((node) => node.querySelector(".verse-locus")?.textContent?.trim() === verse.locus);
      if (!article) continue;
      const ix = article.querySelector(":scope > .ix");
      renderSourceScript(ix?.querySelector(".ix-deva"), verse.sourceSegments);
      let anchor = ix;
      for (const layer of [renderTextualNotes(verse.textualNotes), renderApparatus(verse)]) {
        if (!layer) continue;
        anchor.insertAdjacentElement("afterend", layer);
        anchor = layer;
      }
    }
    root.addEventListener("click", (event) => enhanceCard(root, event));
  }

  window.YVDamaEnhancer = { prepare, afterRender };
})();
