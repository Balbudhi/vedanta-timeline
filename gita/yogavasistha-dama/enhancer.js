/* Reading-specific additions layered on the shared GitaReader. */
(function () {
  "use strict";

  const byLocus = new Map();
  const semanticFields = new Map();
  const PUBLIC_APPARATUS_IDS = new Set(["robot-reading-critical"]);
  const HIDDEN_SEMANTIC_READING_CATEGORIES = new Set(["grammatical head", "narrative activation"]);
  const INDIVIDUAL_ENGLISH_NAME_KEYS = new Set(["shambara", "dama", "vyala", "kata", "bhima", "bhasa", "drdha"]);
  let semanticBundle = null;

  function rootLabel(root) {
    if (!root || typeof root !== "object") return root || null;
    const qualifiers = [root.gana, root.pada].filter(Boolean).join(" · ");
    return `${root.form}${qualifiers ? ` · ${qualifiers}` : ""}`;
  }

  function prepareWords(words) {
    return (words || []).map((source) => {
      const word = structuredClone(source);
      if (/narrative activation/i.test(word.note || "")) delete word.note;
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
      if (history?.source_label) {
        details.append(el("div", "yv-apparatus-provenance", `Source: ${history.source_label}.`));
      }
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

  function evidenceKey(value) {
    return String(value || "").normalize("NFC").trim().toLowerCase();
  }

  function publicSemanticReadings(field, derivations) {
    const existingFormations = new Set((derivations || [])
      .map((derivation) => derivation.analysis || derivation.formation || derivation.segmentation)
      .filter(Boolean)
      .map(evidenceKey));
    const existingMeanings = new Set((derivations || [])
      .map((derivation) => derivation.meaning)
      .filter(Boolean)
      .map(evidenceKey));
    return (field.readings || []).filter((reading) => {
      if (HIDDEN_SEMANTIC_READING_CATEGORIES.has(evidenceKey(reading.category))) return false;
      if (reading.formation && existingFormations.has(evidenceKey(reading.formation))) return false;
      return !reading.meaning || !existingMeanings.has(evidenceKey(reading.meaning));
    });
  }

  function renderSemanticField(field, derivations) {
    const readings = publicSemanticReadings(field, derivations);
    if (!readings.length) return null;
    const block = el("section", "yv-semantic-field");
    block.append(el("div", "yv-semantic-heading", field.lemma_iast));
    for (const reading of readings) {
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

  function appendEnglishTrigger(fragment, text, source, semanticKey = "") {
    if (!text) return;
    if (!/[\p{L}\p{N}]/u.test(text)) {
      fragment.append(document.createTextNode(text));
      return;
    }
    const span = el("span", semanticKey ? "we yv-semantic-trigger" : "we", text);
    span.dataset.wi = source.dataset.wi;
    span.tabIndex = 0;
    span.setAttribute("role", "button");
    if (semanticKey) {
      span.dataset.yvSemanticKey = semanticKey;
      span.setAttribute("aria-label", `${text}: show the attested Sanskrit meanings`);
    }
    fragment.append(span);
  }

  function splitEnglishSemanticTriggers(root) {
    for (const source of [...root.querySelectorAll(".verse .we")]) {
      const locus = source.closest(".verse")?.querySelector(".verse-locus")?.textContent?.trim();
      const verse = byLocus.get(locus);
      const indices = String(source.dataset.wi || "").split(/\s+/).filter(Boolean).map(Number);
      if (!verse || indices.length !== 1) continue;
      const word = verse.words.find((item) => item.i === indices[0]);
      const fields = (word?.semanticFields || []).filter((field) =>
        field.lemma_iast && INDIVIDUAL_ENGLISH_NAME_KEYS.has(field.key)
      );
      if (!fields.length) continue;
      const byLemma = new Map(fields.map((field) => [evidenceKey(field.lemma_iast), field]));
      const alternatives = [...byLemma.values()]
        .sort((left, right) => right.lemma_iast.length - left.lemma_iast.length)
        .map((field) => field.lemma_iast.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
      const pattern = new RegExp(alternatives.join("|"), "giu");
      const text = source.textContent || "";
      const matches = [...text.matchAll(pattern)];
      if (!matches.length) continue;
      const fragment = document.createDocumentFragment();
      let cursor = 0;
      for (const match of matches) {
        appendEnglishTrigger(fragment, text.slice(cursor, match.index), source);
        const field = byLemma.get(evidenceKey(match[0]));
        appendEnglishTrigger(fragment, match[0], source, field?.key || "");
        cursor = match.index + match[0].length;
      }
      appendEnglishTrigger(fragment, text.slice(cursor), source);
      source.replaceWith(fragment);
    }
  }

  function renderFocusedSemanticCard(card, field) {
    const top = el("div", "wc-top");
    const lemma = el("span", "wc-word", field.lemma_iast);
    lemma.setAttribute("lang", "sa-Latn");
    top.append(lemma);
    const evidence = el("section", "yv-word-evidence");
    evidence.append(el("div", "yv-layer-label", "Attested meanings"));
    const semantic = renderSemanticField(field, []);
    if (semantic) evidence.append(semantic);
    card.replaceChildren(top, evidence);
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
    const semanticBlocks = (word.semanticFields || [])
      .map((field) => renderSemanticField(field, derivations))
      .filter(Boolean);
    if (semanticBlocks.length) {
      section.append(el("div", "yv-layer-label", "Attested meanings"));
      semanticBlocks.forEach((block) => section.append(block));
    }
    if (section.childElementCount) card.append(section);
  }

  function clampCardToViewport(card, trigger) {
    if (window.GitaReader?.repositionCard && trigger) {
      window.GitaReader.repositionCard(card, trigger);
      return;
    }
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
      const focusedSemanticKey = trigger.dataset.yvSemanticKey;
      if (focusedSemanticKey) {
        const word = words.find((item) => item.i === indices[0]);
        const field = word?.semanticFields?.find((item) => item.key === focusedSemanticKey);
        if (field) renderFocusedSemanticCard(card, field);
        clampCardToViewport(card, trigger);
        return;
      }
      indices.forEach((index) => appendWordEvidence(card, words.find((word) => word.i === index)));
      clampCardToViewport(card, trigger);
    });
  }

  function ensureStylesheet() {
    if (document.querySelector('link[data-yv-dama-style]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "gita/yogavasistha-dama/reader.css?v=20260901-yv-dama-v3";
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
    splitEnglishSemanticTriggers(root);
    root.addEventListener("click", (event) => enhanceCard(root, event));
  }

  window.YVDamaEnhancer = { prepare, afterRender };
})();
