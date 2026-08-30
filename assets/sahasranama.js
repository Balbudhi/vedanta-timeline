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
const PILOT_WORD_CORRECTIONS = {
  // The witnessed surface is यतोऽव्ययः. The existing source segments preserve
  // it, while this one card's IAST token was serialized as "yatas".
  "cm-vs-fn-p020-n01-quote-0": { 4: { iast: "yataḥ", deva: "यतः" } },
};
const PILOT_SITE_LITERALS = {
  // The printed citation is a fragment rather than a separately verified
  // primary-text locus. Keep the supplied reading explicitly site-attributed.
  "cm-vs-fn-p020-n01-quote-0": {
    englishSlots: "{0:He} {1:alone}, {2:the Self of all beings}, {3:of universal form}; {4:from whom}; {5:imperishable}.",
    note: "Literal translation — site; printed fragment",
  },
  "cm-vs-fn-p020-n03": {
    englishSlots: "{0:Brahman} {1:indeed} {2:is this} {3:universe}; {4:this}, {5:the highest}; {6:the Person} {7:indeed} {8:is this} {9:universe}.",
    note: "Literal translation — site; printed fragment",
  },
  "name-2-paragraph-1": {
    englishSlots: "{0:Because} {2:this} {3:entire universe} {1:is pervaded} {5:by the power} {4:of} {6:the great Self}; {7:therefore} {10:Viṣṇu} {8,9:is indeed called}, {11:from √viś}, {12:the root}, {13:‘to enter’}.",
    note: "Site literal",
  },
};
const PILOT_ENGLISH_SLOT_OVERRIDES = {
  // Keep the final compound of Gītā 6.29 inspectable word by word: the old
  // single English span made sarvatra, sama, and darśanaḥ one opaque target.
  "name-1-paragraph-2-span-0": "{9,10,11:The self whose mind is joined in yoga} {8:sees} {3:the Self} {0,1,2:abiding in all beings} {6:and} {4,5:all beings} {7:in the Self}; {12:everywhere}, {13:the same}, {14:one who sees}.",
};
const INLINE_SANSKRIT_REPAIRS = {
  "1:0": [{
    id: "name-1-paragraph-0-repair-ity",
    text: "ity",
    language: "sa-Latn",
    start: 354,
    end: 357,
    source_segments: [{ text: "ity", word_indices: [0] }],
    words: [{
      i: 0, iast: "iti", deva: "इति", gloss: "thus; so",
      parts: [{ form: "iti", gloss: "thus; so" }], stem: "iti",
      affix: "indeclinable; no inflection", morph: "indeclinable quotative particle",
    }],
  }],
  "114:0": [
    {
      id: "name-114-paragraph-0-repair-karoti",
      text: "karoti", language: "sa-Latn", start: 438, end: 444,
      source_segments: [{ text: "karoti", word_indices: [0] }],
      words: [{
        i: 0, iast: "karoti", deva: "करोति", gloss: "makes; does",
        parts: [{ form: "√kṛ", gloss: "make; do" }, { form: "laṭ + tip", gloss: "present active third-person singular" }],
        stem: "√kṛ", root: "√kṛ", rootGloss: "make; do",
        affix: "laṭ + tip (prathamapuruṣa ekavacana)", morph: "present active third-person singular verb",
      }],
    },
    {
      id: "name-114-paragraph-0-repair-iti",
      text: "iti", language: "sa-Latn", start: 445, end: 448,
      source_segments: [{ text: "iti", word_indices: [0] }],
      words: [{
        i: 0, iast: "iti", deva: "इति", gloss: "thus; so",
        parts: [{ form: "iti", gloss: "thus; so" }], stem: "iti",
        affix: "indeclinable; no inflection", morph: "indeclinable quotative particle",
      }],
    },
  ],
};
const INLINE_WORD_OVERRIDES = {
  "name-750-paragraph-0-ascii-0": {
    0: {
      iast: "loka", deva: "लोक", gloss: "world; field of experience",
      parts: [{ form: "√lok", gloss: "see; behold" }, { form: "a", gloss: "nominal stem formation" }],
      stem: "loka", root: "√lok", rootGloss: "see; behold",
      affix: "a (nominal stem formation)", morph: "masculine nominal stem used in English prose",
      note: "bhvādi (1); ātmanepada · Dhātupāṭha 01.0080: दर्शने",
    },
  },
  "name-2-paragraph-1-iast-22": {
    0: { iast: "purāṇas", deva: "पुराणाः", gloss: "the ancient narratives", parts: [{ form: "purāṇa", gloss: "ancient; old" }, { form: "jas", gloss: "nominative plural" }], stem: "purāṇa", affix: "jas (prathamā bahuvacana)", morph: "nominative plural masculine adjective used substantively", note: "lexical adjective/title; no verbal-root derivation is asserted" },
  },
  "name-2-paragraph-1-iast-55": {
    0: { iast: "purāṇa", deva: "पुराण", gloss: "ancient narrative", parts: [{ form: "purāṇa", gloss: "ancient; old" }], stem: "purāṇa", affix: "citation stem; no inflection asserted", morph: "lexical adjective/title used as a work designation", note: "no verbal-root derivation is asserted" },
  },
};
const INLINE_ITEM_OVERRIDES = {
  "name-2-paragraph-2-span-1": {
    words: [
      { i: 0, iast: "yat", deva: "यत्", gloss: "whatever; which", parts: [{ form: "yad", gloss: "which; whatever" }, { form: "am", gloss: "nominative/accusative singular neuter" }], stem: "yad", affix: "am (prathamā/dvitīyā ekavacana)", morph: "nominative or accusative singular neuter relative pronoun" },
      { i: 1, iast: "kiñ", deva: "किञ्", gloss: "anything", parts: [{ form: "kim", gloss: "what" }, { form: "am", gloss: "nominative/accusative singular neuter" }], stem: "kim", affix: "am (prathamā/dvitīyā ekavacana)", morph: "nominative or accusative singular neuter interrogative pronoun" },
      { i: 2, iast: "ca", deva: "च", gloss: "and; at all", parts: [{ form: "ca", gloss: "and; at all" }], stem: "ca", affix: "indeclinable; no inflection", morph: "indeclinable connective particle" },
      { i: 3, iast: "jagatyām", deva: "जगत्याम्", gloss: "in the moving world", parts: [{ form: "jagatī", gloss: "the moving world" }, { form: "ṅi", gloss: "locative singular" }], stem: "jagatī", affix: "ṅi (saptamī ekavacana)", morph: "locative singular feminine noun" },
      { i: 4, iast: "jagat", deva: "जगत्", gloss: "the moving world", parts: [{ form: "√gam", gloss: "go; move" }, { form: "śatṛ", gloss: "present active participial suffix" }], stem: "jagat", root: "√gam", rootGloss: "go; move", affix: "śatṛ (present active participial formation)", morph: "neuter participial noun" },
    ],
    source_segments: [
      { text: "यत्किञ्च ", word_indices: [0, 1, 2], group_gloss: "whatever at all" },
      { text: "जगत्यां ", word_indices: [3] },
      { text: "जगत्…", word_indices: [4] },
    ],
  },
};
const PILOT_DERIVATION_ROWS = {
  // Transcribed from Chinmayananda's printed note on p. 137 (PDF 141).
  "cm-vs-fn-p141-n01": {
    devanagari: "भुनक्ति इति भोक्ता",
    englishSlots: "{0:He protects} {1:thus}; {2:Protector}.",
    words: [
      { i: 0, iast: "bhunakti", deva: "भुनक्ति", gloss: "he protects", parts: [{ form: "√bhuj", gloss: "protect" }, { form: "laṭ + tip", gloss: "present active third-person singular" }], stem: "√bhuj", root: "√bhuj", rootGloss: "protect; enjoy; consume", affix: "laṭ + tip (prathamapuruṣa ekavacana)", morph: "present active third-person singular verb", note: "rudhādi (7); parasmaipada · Dhātupāṭha 07.0017: पालनाभ्यवहारयोः" },
      { i: 1, iast: "iti", deva: "इति", gloss: "thus; so", parts: [{ form: "iti", gloss: "thus; so" }], stem: "iti", affix: "indeclinable; no inflection", morph: "indeclinable quotative particle" },
      { i: 2, iast: "bhoktā", deva: "भोक्ता", gloss: "protector", parts: [{ form: "√bhuj", gloss: "protect" }, { form: "tṛc", gloss: "agent-forming suffix" }, { form: "su", gloss: "nominative singular" }], stem: "bhoktṛ", root: "√bhuj", rootGloss: "protect; enjoy; consume", affix: "tṛc + su (prathamā ekavacana)", morph: "nominative singular masculine agent noun", note: "rudhādi (7); parasmaipada · Dhātupāṭha 07.0017: पालनाभ्यवहारयोः" },
    ],
    sourceSegments: [{ text: "भुनक्ति ", word_indices: [0] }, { text: "इति ", word_indices: [1] }, { text: "भोक्ता", word_indices: [2] }],
  },
};
let DEEP_LINK_NAME = null;
let RANGE_OBSERVER = null;
let RANGE_ACTIVE_STANZA = null;
let DETAILS_OBSERVER = null;

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

function inlineSanskritReading(item) {
  const inline = window.GitaReader?.interactiveInline
    ? window.GitaReader.interactiveInline(item.words || [], item.text, item.source_segments || null, item.language)
    : esc(item.text);
  return inline;
}

function hasTextBoundary(source, start, end) {
  const isLetter = value => /[A-Za-zĀ-ỹÑñ]/u.test(value || "");
  return !isLetter(source[start - 1]) && !isLetter(source[end]);
}

function richProse(text, inlineSanskrit, options = {}) {
  const link = value => LINKIFY ? LINKIFY(value) : esc(value);
  let source = String(text || "");
  const originalSource = source;
  const markers = [];
  const suppress = options.suppressInlineIds || new Set();
  if (Array.isArray(inlineSanskrit) && inlineSanskrit.length) {
    for (const [index, item] of [...inlineSanskrit].sort((a, b) => b.start - a.start).entries()) {
      // A detection span inside an English word (for example, "ity" in
      // "Reality") is an audit candidate, not public Sanskrit.
      // Some legacy annotations predate prose splitting; never append a stale
      // offset to the end of a later block.
      if (originalSource.slice(item.start, item.end) !== item.text) continue;
      if (!hasTextBoundary(originalSource, item.start, item.end)) continue;
      if (suppress.has(item.id)) {
        source = source.slice(0, item.start) + source.slice(item.end);
        continue;
      }
      // Private-use delimiters plus digits survive glossary linkification;
      // alphabetic marker text can itself be mistaken for a glossary alias.
      const marker = `\uE000${index}\uE001`;
      markers.push({ marker, item });
      source = source.slice(0, item.start) + marker + source.slice(item.end);
    }
  }
  source = source.replace(/[*†‡]+/g, "")
    .replace(/[‘’'“”"]\s*[‘’'“”"]\s*\./g, ".")
    .replace(/[‘’'“”"]\s*\./g, ".")
    .replace(/\.\s*\./g, ".");
  const quote = /[“"]([^”"]+)[”"]/g;
  let out = "", last = 0, match;
  while ((match = quote.exec(source)) !== null) {
    out += link(source.slice(last, match.index));
    out += `<q>${link(match[1])}</q>`;
    last = match.index + match[0].length;
  }
  out += link(source.slice(last));
  for (const { marker, item } of markers) {
    const inline = inlineSanskritReading(item);
    out = out.split(marker).join(inline);
  }
  return out;
}

const SANSKRIT_WORD_RE = /[A-Za-zĀ-ỹ'’\-]+/g;
const SANSKRIT_MARKER_RE = /[āīūṛṝḷṅñṭḍṇśṣṃṁऽ]/;
const ENGLISH_HINT_RE = /^(?:a|an|and|as|at|be|by|for|from|he|her|his|in|into|is|it|its|of|on|or|that|the|their|them|there|these|this|to|with|you|your)$/i;

function looksLikeSanskritParagraph(text) {
  const value = String(text || "").trim();
  if (!value) return false;
  if (/^[\u0900-\u097f]/.test(value)) return true;
  const words = value.match(SANSKRIT_WORD_RE) || [];
  if (words.length < 3) return false;
  let markerCount = 0;
  let englishCount = 0;
  for (const word of words) {
    if (SANSKRIT_MARKER_RE.test(word) || /^'?oṃ$/i.test(word) || /^'?om$/i.test(word)) markerCount++;
    if (ENGLISH_HINT_RE.test(word)) englishCount++;
  }
  return markerCount >= 2 && markerCount >= englishCount;
}

function renderSanskritParagraph(block, context = {}) {
  const value = String(block.text || "").trim();
  const inlineSanskrit = block.inline_sanskrit;
  const citation = value.match(/\s+[—–]\s+((?:(?:[A-ZĀ-Ž][A-Za-zĀ-ỹÑñ'’.\-]*\s*){0,3})(?:Upaniṣad|Up\.|Purāṇa|Parva|Veda|Smṛti|Mahābhārata|Bhāgavata|Gītā|Kaṭha|Katha|Chāndogya|Taittirīya|Aitareya|Bṛhadāraṇyaka|Śvetāśvatara|Muṇḍaka|Mundaka|Harivaṃśa|Kośa|śāstra|Vyāsa|Īśa|Ṛg)[^—–]*?)\.?$/i);
  const body = citation ? value.slice(0, citation.index).trim() : value;
  const source = citation ? citation[1].trim().replace(/\.$/, "") : "";
  if (block.display_devanagari) {
    const literal = siteLiteral(block, context);
    const display = presentationDisplayWords(block, context);
    const sanskrit = Array.isArray(display.words) && display.words.length && window.GitaReader?.interactiveBlock
      ? window.GitaReader.interactiveBlock(
          display.words,
          literal?.englishSlots || null,
          null,
          block.display_devanagari,
          "vsn-commentary-quote-deva",
          display.sourceSegments,
        )
      : `<div class="ix"><div class="ix-deva vsn-commentary-quote-deva" lang="sa-Deva">${esc(block.display_devanagari)}</div></div>`;
    const before = block.display_before ? `<p class="vsn-prose">${richProse(block.display_before)}</p>` : "";
    const after = block.display_after ? `<p class="vsn-prose">${richProse(block.display_after)}</p>` : "";
    const displaySource = String(block.display_citation || source).trim();
    return `${before}<blockquote class="vsn-source-passage vsn-sanskrit-source-passage">
      <div class="vsn-source-passage-text">${sanskrit}</div>
      ${literal?.text ? `<div class="vsn-source-translation">${esc(literal.text)}</div>` : ""}
      ${literal ? `<div class="vsn-site-translation-note">${esc(literal.note)}</div>` : ""}
      ${displaySource ? `<footer class="vsn-commentary-quote-source">${esc(displaySource)}</footer>` : ""}
    </blockquote>${after}`;
  }
  const standalone = Array.isArray(inlineSanskrit) && inlineSanskrit.length === 1 &&
    /^[\u0900-\u097f]/u.test(value) && Array.isArray(inlineSanskrit[0].words) && inlineSanskrit[0].words.length;
  if (standalone && window.GitaReader?.interactiveBlock) {
    const item = inlineSanskrit[0];
    const literal = siteLiteral(block, context);
    const words = presentationStandaloneWords(item, context);
    const sourceSegments = context.nameNumber === 2 && item?.id === "name-2-paragraph-1-span-0"
      ? [{ text: "यस्माद् ", word_indices: [0] }, { text: "विष्टम् ", word_indices: [1] }, { text: "इदं ", word_indices: [2] }, { text: "सर्वं ", word_indices: [3] }, { text: "तस्य ", word_indices: [4] }, { text: "शक्त्या ", word_indices: [5] }, { text: "महात्मनः। ", word_indices: [6] }, { text: "तस्माद् ", word_indices: [7] }, { text: "एवोच्यते ", word_indices: [8, 9] }, { text: "विष्णुर्विशेर्धातोः ", word_indices: [10, 11, 12] }, { text: "प्रवेशनात्॥", word_indices: [13] }]
      : item.source_segments || null;
    const sanskrit = window.GitaReader.interactiveBlock(words, literal?.englishSlots || null, null, value, "vsn-commentary-quote-deva", sourceSegments);
    const translation = literal ? `${literal.text ? `<div class="vsn-source-translation">${esc(literal.text)}</div>` : ""}<div class="vsn-site-translation-note">${esc(literal.note)}</div>` : `<div class="vsn-translation-pending">Literal English not yet published</div>`;
    return `<blockquote class="vsn-source-passage vsn-sanskrit-source-passage"><div class="vsn-source-passage-text">${sanskrit}</div>${translation}</blockquote>`;
  }
  const bodyAnnotations = Array.isArray(inlineSanskrit)
    ? inlineSanskrit.filter(item => item.start < body.length && item.end <= body.length)
    : inlineSanskrit;
  const bodyHtml = richProse(body, bodyAnnotations).replace(/\n/g, "<br>");
  return `<blockquote class="vsn-source-passage vsn-sanskrit-source-passage">
    <div class="vsn-source-passage-text">${bodyHtml}</div>
    ${source ? `<footer class="vsn-commentary-quote-source">${esc(source)}</footer>` : ""}
  </blockquote>`;
}

function looksLikeStandaloneInteractiveSanskrit(text, inlineSanskrit) {
  if (!Array.isArray(inlineSanskrit) || !inlineSanskrit.length) return false;
  const value = String(text || "");
  const isLetter = char => /[A-Za-zĀ-ỹÑñ\u0900-\u097f]/u.test(char);
  const totalLetters = [...value].filter(isLetter).length;
  if (!totalLetters) return false;
  const covered = new Set();
  for (const item of inlineSanskrit) {
    for (let index = item.start; index < item.end; index++) {
      if (isLetter(value[index] || "")) covered.add(index);
    }
  }
  const ratio = covered.size / totalLetters;
  const trimmed = value.trimStart();
  const startsQuoted = /^[“"‘']/.test(trimmed);
  const withoutOpeningPunctuation = trimmed.replace(/^[“"‘'\s(]+/, "");
  const startsDevanagari = /^[\u0900-\u097f]/u.test(withoutOpeningPunctuation);
  const firstInteractive = Math.min(...inlineSanskrit.map(item => item.start));
  const citationOnly = !startsQuoted && !startsDevanagari &&
    /^(?=[^\n]*[IVXLC\d])(?:[A-Za-zĀ-ỹÑñ'’.,-]+\s+){0,5}(?:Upaniṣad|Up\.|Brāhmaṇa|Purāṇa|Parva|Gītā|Veda|Smṛti|Mahābhārata|Kaṭha|Katha|Mundaka|Muṇḍaka)\b/iu.test(trimmed);
  if (citationOnly) return false;
  return ratio >= 0.55 && (
    startsDevanagari
    || startsQuoted
    || firstInteractive <= 3
  );
}

function conciseQuoteSource(block) {
  let source = String(block.canonical_locus || "").trim();
  source = source.split(/\s+·\s+/)[0];
  source = source.replace(/\s*\((?:printed|locus|not independently|witness)[^)]*\)\s*$/i, "");
  source = source.replace(/\s*;\s*(?:no independent|not independently|printed witness).*$/i, "");
  if (source.length > 84) source = source.split(/[.;]/)[0].trim();
  return source || "Chinmayananda commentary";
}

function paragraphs(text) {
  return String(text || "").split(/\n\s*\n/).filter(Boolean)
    .map(paragraph => looksLikeSanskritParagraph(paragraph)
      ? renderSanskritParagraph({text: paragraph})
      : `<p class="vsn-prose">${richProse(paragraph)}</p>`)
    .join("");
}

function compactReplayKey(value) {
  return String(value || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "");
}

function quoteSourceLabel(block) {
  if (PILOT_DERIVATION_ROWS[block?.id]) return "Printed derivation";
  if (block?.id === "cm-vs-fn-p020-n01") return "Printed citation · Viṣṇu Purāṇa 1.2.69";
  const quote = (block.blocks || []).find(child => child.type === "gita-quote" || child.type === "sanskrit-quote");
  if (!quote) return "Chinmayananda’s note";
  return /printed by chinmayananda|not independently verified/i.test(String(quote.canonical_locus || ""))
    ? "Printed explanatory citation"
    : conciseQuoteSource(quote);
}

function citationKind(block) {
  return /printed by chinmayananda|not independently verified/i.test(String(block?.canonical_locus || ""))
    ? "printed" : "verified";
}

function siteLiteral(block, context = {}) {
  return PILOT_SITE_LITERALS[block?.id] || PILOT_SITE_LITERALS[context.footnoteId] || PILOT_SITE_LITERALS[`name-${context.nameNumber}-paragraph-${block?.source_paragraph_index}`] || "";
}

function presentationEnglishSlots(block) {
  return PILOT_ENGLISH_SLOT_OVERRIDES[block?.id] || block?.english_slots || null;
}

function presentationDisplayWords(block, context = {}) {
  if (context.footnoteId === "cm-vs-fn-p141-n02") {
    return {
      words: [
        { i: 0, iast: "bhuṅkte", deva: "भुङ्क्ते", gloss: "he enjoys", parts: [{ form: "√bhuj", gloss: "enjoy; consume" }, { form: "laṭ + ta", gloss: "present middle third-person singular" }], stem: "√bhuj", root: "√bhuj", rootGloss: "protect; enjoy; consume", affix: "laṭ + ta (prathamapuruṣa ekavacana)", morph: "present middle third-person singular verb", note: "rudhādi (7); ātmanepada · Dhātupāṭha 07.0017: पालनाभ्यवहारयोः" },
        { i: 1, iast: "iti", deva: "इति", gloss: "thus; so", parts: [{ form: "iti", gloss: "thus; so" }], stem: "iti", affix: "indeclinable; no inflection", morph: "indeclinable quotative particle" },
        { i: 2, iast: "bhoktā", deva: "भोक्ता", gloss: "enjoyer", parts: [{ form: "√bhuj", gloss: "enjoy; consume" }, { form: "tṛc", gloss: "agent-forming suffix" }, { form: "su", gloss: "nominative singular" }], stem: "bhoktṛ", root: "√bhuj", rootGloss: "protect; enjoy; consume", affix: "tṛc + su (prathamā ekavacana)", morph: "nominative singular masculine agent noun", note: "rudhādi (7); parasmaipada · Dhātupāṭha 07.0017: पालनाभ्यवहारयोः" },
      ],
      sourceSegments: [{ text: "भुङ्क्ते ", word_indices: [0] }, { text: "इति ", word_indices: [1] }, { text: "भोक्ता", word_indices: [2] }],
    };
  }
  if (context.footnoteId !== "cm-vs-fn-p020-n03") {
    return { words: block.display_words || [], sourceSegments: block.display_source_segments || null };
  }
  const word = (i, iast, deva, gloss, parts, stem, affix, morph) => ({ i, iast, deva, gloss, parts, stem, affix, morph });
  return {
    words: [
      word(0, "brahma", "ब्रह्म", "Brahman; the absolute", [{ form: "brahman", gloss: "Brahman; the absolute" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "brahman", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter noun"),
      word(1, "eva", "एव", "indeed; precisely", [{ form: "eva", gloss: "indeed; precisely" }], "eva", "indeclinable; no inflection", "indeclinable emphatic particle"),
      word(2, "idam", "इदम्", "this", [{ form: "idam", gloss: "this" }], "idam", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter demonstrative pronoun"),
      word(3, "viśvam", "विश्वम्", "universe; all", [{ form: "viśva", gloss: "all; universe" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "viśva", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter noun"),
      word(4, "idam", "इदम्", "this", [{ form: "idam", gloss: "this" }], "idam", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter demonstrative pronoun"),
      word(5, "variṣṭham", "वरिष्ठम्", "the most excellent; highest", [{ form: "vara", gloss: "excellent; choice" }, { form: "iṣṭha", gloss: "superlative suffix" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "variṣṭha", "iṣṭha (superlative) + am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter superlative adjective"),
      word(6, "puruṣaḥ", "पुरुषः", "the Person", [{ form: "puruṣa", gloss: "person; personhood" }, { form: "su", gloss: "nominative singular" }], "puruṣa", "su (prathamā ekavacana)", "nominative singular masculine noun; visarga is resolved before eva"),
      word(7, "eva", "एव", "indeed; precisely", [{ form: "eva", gloss: "indeed; precisely" }], "eva", "indeclinable; no inflection", "indeclinable emphatic particle"),
      word(8, "idam", "इदम्", "this", [{ form: "idam", gloss: "this" }], "idam", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter demonstrative pronoun"),
      word(9, "viśvam", "विश्वम्", "universe; all", [{ form: "viśva", gloss: "all; universe" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "viśva", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter noun"),
    ],
    sourceSegments: [
      { text: "ब्रह्मैवेदं ", word_indices: [0, 1, 2] }, { text: "विश्वम् ", word_indices: [3] }, { text: "इदं ", word_indices: [4] }, { text: "वरिष्ठं ", word_indices: [5] }, { text: "पुरुष ", word_indices: [6] }, { text: "एवेदं ", word_indices: [7, 8] }, { text: "विश्वम्", word_indices: [9] },
    ],
  };
}

function presentationStandaloneWords(item, context = {}) {
  if (!(context.nameNumber === 2 && item?.id === "name-2-paragraph-1-span-0")) return item.words;
  const word = (i, iast, deva, gloss, parts, stem, affix, morph, extra = {}) => ({ i, iast, deva, gloss, parts, stem, affix, morph, ...extra });
  return [
    word(0, "yasmād", "यस्माद्", "because; from whom", [{ form: "yad", gloss: "which; who" }, { form: "ṅasi", gloss: "ablative singular" }], "yad", "ṅasi (pañcamī ekavacana)", "ablative singular relative pronoun used adverbially"),
    word(1, "viṣṭam", "विष्टम्", "pervaded", [{ form: "√viś", gloss: "enter; pervade" }, { form: "kta", gloss: "past passive participle" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "viṣṭa", "kta + am (prathamā/dvitīyā ekavacana)", "past passive participle, nominative or accusative singular neuter", { root: "√viś", rootGloss: "enter; pervade", note: "tudādi (6); parasmaipada · Dhātupāṭha 06.0160: प्रवेशने" }),
    word(2, "idam", "इदं", "this", [{ form: "idam", gloss: "this" }], "idam", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter demonstrative pronoun"),
    word(3, "sarvam", "सर्वं", "all; the whole", [{ form: "sarva", gloss: "all" }, { form: "am", gloss: "nominative/accusative singular neuter" }], "sarva", "am (prathamā/dvitīyā ekavacana)", "nominative or accusative singular neuter adjective"),
    word(4, "tasya", "तस्य", "of him", [{ form: "tad", gloss: "that; he" }, { form: "ṅas", gloss: "genitive singular" }], "tad", "ṅas (ṣaṣṭhī ekavacana)", "genitive singular demonstrative pronoun"),
    word(5, "śaktyā", "शक्त्या", "by power", [{ form: "śakti", gloss: "power; capacity" }, { form: "ṭā", gloss: "instrumental singular" }], "śakti", "ṭā (tṛtīyā ekavacana)", "instrumental singular feminine noun"),
    word(6, "mahātmanaḥ", "महात्मनः", "of the great Self", [{ form: "mahā", gloss: "great" }, { form: "ātman", gloss: "self" }, { form: "ṅas", gloss: "genitive singular" }], "mahātman", "ṅas (ṣaṣṭhī ekavacana)", "genitive singular masculine compound noun"),
    word(7, "tasmād", "तस्माद्", "therefore", [{ form: "tad", gloss: "that" }, { form: "ṅasi", gloss: "ablative singular" }], "tad", "ṅasi (pañcamī ekavacana)", "ablative singular pronoun used adverbially"),
    word(8, "eva", "एव", "indeed; precisely", [{ form: "eva", gloss: "indeed; precisely" }], "eva", "indeclinable; no inflection", "indeclinable emphatic particle"),
    word(9, "ucyate", "उच्यते", "is called", [{ form: "√vac", gloss: "speak; call" }, { form: "ya + laṭ + ta", gloss: "present passive third-person singular" }], "√vac", "ya + laṭ + ta (prathamapuruṣa ekavacana)", "present passive third-person singular verb", { root: "√vac", rootGloss: "speak; call" }),
    word(10, "viṣṇuḥ", "विष्णुः", "Viṣṇu", [{ form: "viṣṇu", gloss: "the all-pervading one" }, { form: "su", gloss: "nominative singular" }], "viṣṇu", "su (prathamā ekavacana)", "nominative singular masculine proper name; visarga is resolved before viśeḥ", { root: "√viś", rootGloss: "enter; pervade", note: "traditional nirvacana; Dhātupāṭha 06.0160: प्रवेशने" }),
    word(11, "viśeḥ", "विशेः", "of viś", [{ form: "√viś", gloss: "enter; pervade" }, { form: "ṅas", gloss: "genitive singular" }], "viś", "ṅas (ṣaṣṭhī ekavacana)", "genitive singular root citation", { root: "√viś", rootGloss: "enter; pervade", note: "tudādi (6); parasmaipada · Dhātupāṭha 06.0160: प्रवेशने" }),
    word(12, "dhātoḥ", "धातोः", "of the verbal root", [{ form: "dhātu", gloss: "verbal root" }, { form: "ṅas", gloss: "genitive singular" }], "dhātu", "ṅas (ṣaṣṭhī ekavacana)", "genitive singular masculine noun"),
    word(13, "praveśanāt", "प्रवेशनात्", "from entering", [{ form: "pra", gloss: "forth; into" }, { form: "√viś", gloss: "enter" }, { form: "lyuṭ", gloss: "action-noun suffix" }, { form: "ṅasi", gloss: "ablative singular" }], "praveśana", "lyuṭ + ṅasi (pañcamī ekavacana)", "ablative singular action noun", { root: "√viś", rootGloss: "enter; pervade", note: "tudādi (6); parasmaipada · Dhātupāṭha 06.0160: प्रवेशने" }),
  ];
}

function presentationInlineSanskrit(block, context = {}) {
  return [...(block?.inline_sanskrit || []), ...(INLINE_SANSKRIT_REPAIRS[`${context.nameNumber}:${block?.source_paragraph_index}`] || [])]
    .map(item => {
      const itemOverride = INLINE_ITEM_OVERRIDES[item.id];
      if (itemOverride) return { ...item, ...itemOverride };
      const changes = INLINE_WORD_OVERRIDES[item.id];
      return changes ? { ...item, words: item.words.map(word => changes[word.i] ? { ...word, ...changes[word.i] } : word) } : item;
    })
    .sort((a, b) => a.start - b.start);
}

function presentationWords(block) {
  const corrections = PILOT_WORD_CORRECTIONS[block?.id];
  if (!corrections) return block?.words || [];
  return (block.words || []).map(word => corrections[word.i] ? { ...word, ...corrections[word.i] } : word);
}

function renderPilotDerivationRow(block) {
  const row = PILOT_DERIVATION_ROWS[block.id];
  if (!row) return "";
  const blockHtml = window.GitaReader?.interactiveBlock
    ? window.GitaReader.interactiveBlock(row.words, row.englishSlots, null, row.devanagari, "vsn-commentary-quote-deva", row.sourceSegments)
    : `<div class="vsn-derivation-deva" lang="sa-Deva">${esc(row.devanagari)}</div>`;
  return `<div class="vsn-derivation-row">${blockHtml}<div class="vsn-site-translation-note">Literal translation — site; printed derivation</div></div>`;
}

function quotedWordForms(block) {
  const forms = new Set();
  for (const child of block?.blocks || []) {
    if (child.type !== "gita-quote" && child.type !== "sanskrit-quote") continue;
    for (const word of child.words || []) forms.add(String(word.iast || "").replace(/[’']/g, "").toLowerCase().replace(/ḥ$/u, ""));
  }
  return forms;
}

function renderFootnoteCall(call, labels) {
  return "";
}

function renderCommentaryBlock(block, context = {}) {
  if (block.type === "prose") {
    const inlineSanskrit = presentationInlineSanskrit(block, context);
    const presentedBlock = { ...block, inline_sanskrit: inlineSanskrit };
    const calls = Array.isArray(block.footnote_calls)
      ? block.footnote_calls.map(call => renderFootnoteCall(call, context.footnoteLabels)).join("")
      : "";
    if (block.display_devanagari || looksLikeStandaloneInteractiveSanskrit(block.text, inlineSanskrit)) {
      return `${renderSanskritParagraph(presentedBlock, context)}${calls}`;
    }
    return `<p class="vsn-prose">${richProse(block.text, inlineSanskrit, {
      normalizedSanskrit: context.normalizedSanskrit,
      suppressInlineIds: context.suppressInlineIds,
    })}${calls}</p>`;
  }
  if (block.type === "footnote") {
    const pilotDerivation = renderPilotDerivationRow(block);
    if (pilotDerivation) {
      return `<aside class="vsn-footnote vsn-evidence-thread vsn-derivation-note" id="${esc(block.id)}" role="note" data-print-marker="${esc(block.marker)}" aria-label="${esc(`Printed derivation; note ${block.marker}`)}">
        <header class="vsn-evidence-head"><span>Printed derivation</span><span>Chinmayananda p. ${esc(block.printed_page)}</span></header>
        <div class="vsn-footnote-body">${pilotDerivation}</div>
      </aside>`;
    }
    const children = Array.isArray(block.blocks) ? block.blocks : [];
    const proseKey = compactReplayKey(children.filter(child => child.type === "prose").map(child => child.text).join(" "));
    const body = children.map(child => {
      const englishKey = compactReplayKey(child.english);
      return renderCommentaryBlock(child, {
        inFootnote: true,
        showEnglish: Boolean(englishKey && !proseKey.includes(englishKey)),
        footnoteId: block.id,
        nameNumber: context.nameNumber,
      });
    }).join("");
    const applies = Array.isArray(block.additional_name_numbers) && block.additional_name_numbers.length
      ? ` · also names ${block.additional_name_numbers.join(", ")}`
      : "";
    const sourceLabel = quoteSourceLabel(block) === "Chinmayananda’s note" ? "Chinmayananda" : quoteSourceLabel(block);
    const quote = children.find(child => child.type === "gita-quote" || child.type === "sanskrit-quote");
    const kind = citationKind(quote);
    return `<aside class="vsn-footnote vsn-evidence-thread vsn-evidence-thread--${kind}" id="${esc(block.id)}" role="note" data-print-marker="${esc(block.marker)}" aria-label="${esc(`${sourceLabel}; printed note ${block.marker}`)}">
      <header class="vsn-evidence-head"><span>${esc(sourceLabel)}</span><span>Chinmayananda p. ${esc(block.printed_page)}${esc(applies)}</span></header>
      <div class="vsn-footnote-body">${body}</div>
    </aside>`;
  }
  if (block.type === "source-note") {
    return `<p class="vsn-footnote-citation">${esc(block.text)}</p>`;
  }
  if (block.type !== "gita-quote" && block.type !== "sanskrit-quote") return "";
  const hasReviewedWords = Array.isArray(block.words) && block.words.length > 0;
  const displayEnglish = block.display_english === true || context.showEnglish;
  const literal = siteLiteral(block, context);
  const visibleEnglish = displayEnglish ? presentationEnglishSlots(block) : (literal?.englishSlots || null);
  const sanskrit = hasReviewedWords && window.GitaReader?.interactiveBlock
    ? window.GitaReader.interactiveBlock(presentationWords(block), visibleEnglish, null, block.devanagari, "vsn-commentary-quote-deva", block.source_segments || null)
    : `<div class="ix"><div class="ix-deva vsn-commentary-quote-deva" lang="sa-Deva">${esc(block.devanagari)}</div><div class="ix-pada" lang="sa-Latn">${esc(block.iast)}</div></div>`;
  const source = quoteSourceLabel({ blocks: [block] });
  const provenance = visibleEnglish && block.english_source === "site-literal-translation"
    ? `<div class="vsn-site-translation-note">Literal translation — site</div>`
    : literal ? `${literal.text ? `<div class="vsn-source-translation">${esc(literal.text)}</div>` : ""}<div class="vsn-site-translation-note">${esc(literal.note)}</div>` : "";
  const sourceFooter = context.inFootnote ? "" : `<footer class="vsn-commentary-quote-source">${esc(source)}</footer>`;
  return `<blockquote class="vsn-commentary-quote" data-quote-id="${esc(block.id)}">
    ${sanskrit}
    ${provenance}
    ${sourceFooter}
  </blockquote>`;
}

function commentaryBlocks(name) {
  const sourceBlocks = name.chinmayananda?.blocks;
  const blocks = Array.isArray(sourceBlocks) ? [...sourceBlocks] : sourceBlocks;
  if (!Array.isArray(blocks) || !blocks.length) return paragraphs(name.chinmayananda?.commentary || "");
  if (name.number === 2) {
    const sourceIndex = blocks.findIndex((block, index) =>
      block.type === "prose" && /Viṣṇu Purāṇa \(3-1\) says:\s*$/.test(block.text || "") &&
      blocks[index + 1]?.type === "footnote" && blocks[index + 2]?.type === "prose" &&
      /^[\u0900-\u097f]/u.test(String(blocks[index + 2].text || "").trim()));
    if (sourceIndex >= 0) {
      const [note] = blocks.splice(sourceIndex + 1, 1);
      blocks.splice(sourceIndex + 2, 0, note);
    }
  }
  const footnoteLabels = new Map(blocks.filter(block => block.type === "footnote").map(block => [block.id, quoteSourceLabel(block)]));
  const items = [];
  let currentClaim = null;
  const flush = () => {
    if (!currentClaim) return;
    items.push(`<section class="vsn-claim">${currentClaim.prose}${currentClaim.evidence.length ? `<div class="vsn-claim-evidence">${currentClaim.evidence.join("")}</div>` : ""}</section>`);
    currentClaim = null;
  };
  for (let index = 0; index < blocks.length; index++) {
    const block = blocks[index];
    const next = blocks[index + 1];
    const quotedForms = next?.type === "footnote" ? quotedWordForms(next) : new Set();
    // Name 1 repeats this particular source verse verbatim in the prose and
    // immediately in its printed note. Other notes may share vocabulary with
    // their calling sentence, so broad lexical suppression would lose prose.
    const inlineSanskrit = presentationInlineSanskrit(block, { nameNumber: name.number });
    const quotedItems = name.number === 1 && next?.id === "cm-vs-fn-p020-n01" && block.type === "prose"
      ? inlineSanskrit.filter(item => (item.words || []).some(word => quotedForms.has(String(word.iast || "").replace(/[’']/g, "").toLowerCase().replace(/ḥ$/u, ""))))
      : [];
    // A source may record a sandhied word differently in the prose token and
    // in the reviewed note. Once its beginning/end are known, remove the whole
    // contiguous in-prose quotation instead of exposing a broken remnant.
    const quoteStart = quotedItems.length ? Math.min(...quotedItems.map(item => item.start)) : null;
    const matchedQuoteEnd = quotedItems.length ? Math.max(...quotedItems.map(item => item.end)) : null;
    const quoteEnd = matchedQuoteEnd == null ? null : (() => {
      const sentenceEnd = String(block.text || "").indexOf(".", matchedQuoteEnd);
      return sentenceEnd >= 0 ? sentenceEnd : matchedQuoteEnd;
    })();
    const suppressInlineIds = new Set(
      quoteStart == null ? [] : inlineSanskrit
        .filter(item => item.start >= quoteStart && item.end <= quoteEnd)
        .map(item => item.id)
    );
    const rendered = renderCommentaryBlock(block, {
      footnoteLabels,
      nameNumber: name.number,
      suppressInlineIds,
    });
    if (block.type === "prose") {
      flush();
      currentClaim = { prose: rendered, evidence: [] };
      continue;
    }
    if (block.type === "footnote") {
      if (!currentClaim) {
        items.push(rendered);
        continue;
      }
      currentClaim.evidence.push(rendered);
      if (next?.type !== "footnote") flush();
      continue;
    }
    flush();
    items.push(rendered);
  }
  flush();
  return items.join("");
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

function derivationSourceLabel(source) {
  const value = String(source || "");
  if (value.includes("chinmayananda")) return "Chinmayananda scan";
  if (value.includes("ashtadhyayi")) return "Aṣṭādhyāyī";
  if (value.includes("dhatupatha")) return "Dhātupāṭha";
  if (value.includes("nirukta")) return "Nirukta";
  if (value.includes("nighantu")) return "Nighaṇṭu";
  if (value.includes("unadi")) return "Uṇādi";
  if (value.includes("amarakosha")) return "Amarakośa";
  if (value.includes("mbh731") || value.includes("titus.uni-frankfurt.de")) return "Mahābhārata";
  if (value.includes("bhanapcorner") || value.includes("incarnation14")) return "Traditional commentary";
  if (value.includes("Vishnu_Sahasra_Nama_Swami_Tapasyananda")) return "Śaṅkara commentary (Tapasyananda)";
  if (value.includes("/manu.html") || value.includes("manusm")) return "Manusmṛti";
  if (value.includes("kashika")) return "Kāśikā";
  if (value.includes("mahabhashya")) return "Mahābhāṣya";
  const filename = value.split("/").pop() || value;
  return filename.replace(/\.(?:json|txt|htm|html|pdf)$/i, "").replace(/[_-]+/g, " ");
}

function renderParallelDerivation(derivation) {
  const parts = Array.isArray(derivation.parts) && derivation.parts.length
    ? `<div class="wc-parts">${derivation.parts.map(part => `<span class="wc-part"><span class="wc-pf" lang="sa-Latn">${esc(part.form)}</span><span class="wc-pg">${esc(part.gloss)}</span></span>`).join("")}</div>`
    : "";
  const roots = Array.isArray(derivation.roots)
    ? derivation.roots.map(root => `<div class="wc-root"><span class="wc-pf">${esc(root.form)}</span><span class="wc-pg">: ${esc(`${root.gana}, ${root.pada} · ${root.gloss}`)}</span>${root.dhatupatha ? `<span class="wc-pg"><br>Dhātupāṭha ${esc(root.dhatupatha.locus)} · <span lang="sa-Deva">${esc(root.dhatupatha.artha_sanskrit)}</span></span>` : ""}</div>`).join("")
    : "";
  const sources = Array.isArray(derivation.evidence)
    ? derivation.evidence.map(item => `${derivationSourceLabel(item.source)} ${item.locus}`).filter(Boolean)
    : [];
  const kind = derivation.kind === "traditional-nirvacana" ? "Traditional nirvacana" : "Alternative grammatical derivation";
  return `<section class="wc-derivation wc-derivation--${esc(derivation.kind)}">
    <div class="wc-derivation-label">${esc(kind)}</div>
    <div class="wc-derivation-title">${esc(derivation.label)}</div>
    <div class="wc-derivation-text">${esc(derivation.meaning)}</div>
    ${parts}${roots}
    <div class="wc-gram"><span class="wc-gram-main">${esc(derivation.morphology)}</span><br><span class="wc-gram-affix">formation: ${esc(derivation.formation)}</span></div>
    <div class="wc-note">${esc(derivation.qualification)}</div>
    ${sources.length ? `<div class="wc-derivation-evidence">${sources.map(source => `<span>${esc(source)}</span>`).join("")}</div>` : ""}
  </section>`;
}

function parallelDerivationBlocks(analysis, primaryContent) {
  const alternatives = Array.isArray(analysis.parallel_derivations)
    ? analysis.parallel_derivations
    : [];
  if (!alternatives.length) return primaryContent;
  return `<div class="wc-derivations">
    <section class="wc-derivation wc-derivation--primary">
      <div class="wc-derivation-label">Primary grammatical formation</div>
      ${primaryContent}
    </section>
    ${alternatives.map(renderParallelDerivation).join("")}
  </div>`;
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
    const calls = Array.isArray(name.root_footnote_calls)
      ? name.root_footnote_calls.map(call => `<sup class="vsn-root-footnote-call" aria-label="Chinmayananda source note ${esc(call.marker)}">${esc(call.marker)}</sup>`).join("")
      : "";
    return `<span class="w vsn-deva-w" role="button" tabindex="0" data-name-number="${name.number}" aria-label="Name ${name.number}: ${esc(form)}">${esc(form)}</span>${calls}`;
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
    <header class="vsn-section-head vsn-sticky-section vsn-names-head"><span id="vsn-names-title">Names</span><span id="vsn-names-range" aria-live="polite">1–9</span></header>
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
    <div class="vsn-attribution-role vsn-full-attribution"><strong>Full:</strong> Chinmayananda’s prose; untranslated Sanskrit is clickable.</div>
    <div class="vsn-attribution-role vsn-simplified-attribution"><strong>Simplified:</strong> site-generated, not his wording.</div>
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
  card.style.left = "0px";
  card.style.top = "0px";
  const cardRect = card.getBoundingClientRect();
  const minLeft = window.scrollX + margin;
  const maxLeft = window.scrollX + document.documentElement.clientWidth - cardRect.width - margin;
  let left = rect.left + rect.width / 2 - cardRect.width / 2 + window.scrollX;
  let top = rect.top - cardRect.height - 10 + window.scrollY;
  left = Math.max(minLeft, Math.min(maxLeft, left));
  if (top < window.scrollY + margin) top = rect.bottom + 10 + window.scrollY;
  const maxTop = window.scrollY + window.innerHeight - cardRect.height - margin;
  if (top > maxTop) top = Math.max(window.scrollY + margin, maxTop);
  card.style.left = `${left}px`;
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
  const derivations = parallelDerivationBlocks(analysis, `${parts}${root}${grammar}`);
  const definition = `<div class="wc-mean vsn-card-definition">${esc(simpleExcerpt(name))}</div>`;
  const detail = detailFor(name);
  const explanationAction = detail
    ? `<div class="wc-gls vsn-card-detail-action"><button class="wc-gl vsn-show-detail" type="button">Read Chinmayananda’s explanation ↓</button></div>`
    : "";
  const citation = analysis.citation_iast || name.citation_iast || name.surface_iast;
  const deva = analysis.citation_devanagari || name.deva;
  WORD_CARD = document.createElement("div");
  WORD_CARD.className = "wcard vsn-wcard";
  WORD_CARD.setAttribute("role", "tooltip");
  WORD_CARD.innerHTML = `<div class="wc-top"><span class="wc-word" lang="sa-Latn">${esc(citation)}</span> <span class="vsn-card-number">${name.number}</span></div><div class="vsn-card-deva" lang="sa-Deva">${esc(deva)}</div>${definition}${derivations}${explanationAction}`;
  document.body.append(WORD_CARD);
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
  document.addEventListener("click", event => {
    if (WORD_CARD?.contains(event.target)) return;
    closeWordCard();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeWordCard();
  });
  ROOT.closest(".dp-pane-body")?.addEventListener("scroll", closeWordCard, { passive: true });
  document.addEventListener("scroll", closeWordCard, { passive: true, capture: true });
  window.addEventListener("scroll", closeWordCard, { passive: true });
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
      block.hidden = !DETAILS_OPEN;
  });
  if (DETAILS_OPEN) {
    const scrollRoot = ROOT?.closest(".dp-pane-body") || ROOT;
    if (!DETAILS_OBSERVER && "IntersectionObserver" in window) {
      DETAILS_OBSERVER = new IntersectionObserver(entries => {
        if (!DETAILS_OPEN) return;
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const block = entry.target;
          if (block.dataset.loaded === "true") continue;
          const stanza = DATA.stanzas[Number(block.dataset.stanzaNumber) - 1];
          if (!stanza) continue;
          block.querySelector(".vsn-details-content").innerHTML = renderDetails(stanza);
          block.dataset.loaded = "true";
        }
      }, { root: scrollRoot, rootMargin: "220px 0px 220px 0px", threshold: 0.01 });
    }
    if (DETAILS_OBSERVER) {
      DETAILS_OBSERVER.disconnect();
      ROOT.querySelectorAll(".vsn-details-block").forEach(block => DETAILS_OBSERVER.observe(block));
      ROOT.querySelectorAll(".vsn-details-block").forEach(block => {
        const rect = block.getBoundingClientRect();
        const rootRect = scrollRoot.getBoundingClientRect();
        const visible = rect.bottom > rootRect.top - 220 && rect.top < rootRect.bottom + 220;
        if (visible && block.dataset.loaded !== "true") {
          const stanza = DATA.stanzas[Number(block.dataset.stanzaNumber) - 1];
          if (stanza) {
            block.querySelector(".vsn-details-content").innerHTML = renderDetails(stanza);
            block.dataset.loaded = "true";
          }
        }
      });
    }
  } else if (DETAILS_OBSERVER) {
    DETAILS_OBSERVER.disconnect();
  }
}

function updateNameRange(stanza) {
  if (!stanza || RANGE_ACTIVE_STANZA === stanza.number) return;
  RANGE_ACTIVE_STANZA = stanza.number;
  const numbers = stanza.name_numbers || [];
  const first = numbers[0];
  const last = numbers[numbers.length - 1];
  const label = first && last ? `${first}–${last}` : "1–1000";
  const range = ROOT?.querySelector("#vsn-names-range");
  if (range) range.textContent = label;
  if (!DEEP_LINK_NAME && first) writeDeepLinkName(first);
}

function writeDeepLinkName(number) {
  const value = Number(number);
  if (!Number.isInteger(value) || value < 1 || value > 1000) return;
  try {
    const url = new URL(window.location.href);
    if (url.searchParams.get("vsn") === String(value)) return;
    url.searchParams.set("vsn", String(value));
    window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
  } catch (_) {}
}

function readDeepLinkName() {
  try {
    const value = Number(new URLSearchParams(window.location.search).get("vsn"));
    return Number.isInteger(value) && value >= 1 && value <= 1000 ? value : null;
  } catch (_) {
    return null;
  }
}

function wireNameRange() {
  RANGE_OBSERVER?.disconnect();
  const scrollRoot = ROOT?.closest(".dp-pane-body") || null;
  let frame = 0;
  const syncFromScroll = () => {
    frame = 0;
    if (!scrollRoot) return;
    const focusY = scrollRoot.scrollTop + 78;
    let verse = null;
    for (const candidate of ROOT.querySelectorAll(".vsn-verse")) {
      if (candidate.offsetTop > focusY) break;
      verse = candidate;
    }
    if (verse) updateNameRange(DATA.stanzas[Number(verse.dataset.stanzaNumber) - 1]);
  };
  if (scrollRoot) {
    if (scrollRoot._vsnRangeScrollHandler) scrollRoot.removeEventListener("scroll", scrollRoot._vsnRangeScrollHandler);
    scrollRoot._vsnRangeScrollHandler = () => { if (!frame) frame = requestAnimationFrame(syncFromScroll); };
    scrollRoot.addEventListener("scroll", scrollRoot._vsnRangeScrollHandler, { passive: true });
  }
  if (!("IntersectionObserver" in window)) return;
  RANGE_OBSERVER = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!visible) return;
    const stanza = DATA.stanzas[Number(visible.target.dataset.stanzaNumber) - 1];
    updateNameRange(stanza);
  }, { root: scrollRoot, rootMargin: "-12% 0px -78% 0px", threshold: 0 });
  ROOT.querySelectorAll(".vsn-verse").forEach(verse => RANGE_OBSERVER.observe(verse));
  syncFromScroll();
}

async function openDeepLinkedName() {
  const number = DEEP_LINK_NAME;
  if (!number) return;
  await setChantView(false, false);
  requestAnimationFrame(() => {
    const target = ROOT?.querySelector(`#vsn-detail-${CSS.escape(String(number))}`) || ROOT?.querySelector(`[data-name-number="${CSS.escape(String(number))}"]`);
    if (!target) return;
    target.classList.add("vsn-deep-link-target");
    target.scrollIntoView({ behavior: "auto", block: "start" });
    const stanza = DATA.stanzas.find(item => (item.name_numbers || []).some(value => Number(value) === number));
    updateNameRange(stanza);
    writeDeepLinkName(number);
    DEEP_LINK_NAME = null;
    window.setTimeout(() => target.classList.remove("vsn-deep-link-target"), 1200);
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
  RANGE_ACTIVE_STANZA = null;
  CHANT_ONLY = readChantView();
  DEEP_LINK_NAME = readDeepLinkName();
  if (DEEP_LINK_NAME) CHANT_ONLY = false;
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
  wireNameRange();
  await setChantView(CHANT_ONLY, false);
  await openDeepLinkedName();
}

window.SahasranamaReader = { render };
})();
