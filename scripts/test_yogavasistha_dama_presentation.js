#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const review = JSON.parse(fs.readFileSync(path.join(root, "gita/yogavasistha-dama/review.json"), "utf8"));
const enhancer = fs.readFileSync(path.join(root, "gita/yogavasistha-dama/enhancer.js"), "utf8");
const gitaReader = fs.readFileSync(path.join(root, "assets/gita.js"), "utf8");
const readerStyle = fs.readFileSync(path.join(root, "gita/yogavasistha-dama/reader.css"), "utf8");

if (review.units.length !== 56) throw new Error(`expected 56 units, found ${review.units.length}`);

let wordCount = 0;
const expectedSemanticKeys = ["purusha", "shambara", "daitya", "danava", "amara", "deva", "sura", "tridasha", "asura", "dama", "vyala", "kata", "bhima", "bhasa", "drdha"];
const semanticKeys = new Set(review.semantic_fields.fields.map(field => field.key));
const observedSemanticKeys = new Set();
if (JSON.stringify([...semanticKeys]) !== JSON.stringify(expectedSemanticKeys)) {
  throw new Error("semantic-field registry does not match the frozen population");
}
if (review.semantic_fields.methodology.principles.length < 4 || review.semantic_fields.witness_history.length !== 4) {
  throw new Error("reader methodology or witness history is incomplete");
}
const slotPattern = /\{([0-9]+(?:\s*,\s*[0-9]+)*):[^{}]+\}/g;
for (const unit of review.units) {
  const expected = unit.words.map((_, index) => index);
  const observed = unit.sourceSegments.flatMap(segment => segment.word_indices);
  const englishIndices = [...unit.english.matchAll(slotPattern)]
    .flatMap(match => match[1].split(",").map(value => Number(value.trim())))
    .sort((left, right) => left - right);
  const reconstructed = unit.sourceSegments.map(segment => segment.text).join("");
  if (JSON.stringify(observed) !== JSON.stringify(expected)) {
    throw new Error(`${unit.id}: source-script links do not cover every word once in order`);
  }
  if (reconstructed !== unit.devanagari) {
    throw new Error(`${unit.id}: source-script links do not preserve exact Devanāgarī`);
  }
  if (JSON.stringify(englishIndices) !== JSON.stringify(expected)) {
    throw new Error(`${unit.id}: English links do not cover every word exactly once`);
  }
  unit.words.forEach(word => (word.semanticFieldKeys || []).forEach(key => observedSemanticKeys.add(key)));
  for (const entry of unit.apparatus || []) {
    if (!entry.sourceSegments) continue;
    const entryExpected = entry.words.map((_, index) => index);
    const entryObserved = entry.sourceSegments.flatMap(segment => segment.word_indices);
    if (JSON.stringify(entryObserved) !== JSON.stringify(entryExpected)) {
      throw new Error(`${entry.id}: source-script links do not cover every apparatus word once`);
    }
    entry.words.forEach(word => (word.semanticFieldKeys || []).forEach(key => observedSemanticKeys.add(key)));
  }
  wordCount += unit.words.length;
}

if (!enhancer.includes("renderSourceScript")) {
  throw new Error("enhancer does not connect exact source-script segments to reviewed word indices");
}
if (!enhancer.includes("renderSemanticField")) {
  throw new Error("reader does not render the reviewed semantic fields");
}
if (enhancer.includes("renderMethodology") || enhancer.includes("Reading method and textual witnesses")) {
  throw new Error("reader must not render an editorial methodology block");
}
function publicSet(name) {
  const match = enhancer.match(new RegExp(`const ${name} = new Set\\(\\[([^\\]]*)\\]\\)`));
  if (!match) throw new Error(`missing ${name}`);
  return JSON.parse(`[${match[1]}]`);
}
if (JSON.stringify(publicSet("PUBLIC_APPARATUS_IDS")) !== JSON.stringify(["robot-reading-critical"])) {
  throw new Error("public apparatus must show only the critical Mokṣopāya reading");
}
if (enhancer.includes("history.description") || enhancer.includes("entry.sense")) {
  throw new Error("public apparatus must not repeat witness history or a second English rendering");
}
if (!enhancer.includes('new Set(["grammatical head", "narrative activation"])')) {
  throw new Error("public semantic cards must omit compound repetition and narrative character interpretation");
}
if (enhancer.includes("field.opening") || enhancer.includes("field.chronology_note")) {
  throw new Error("public semantic cards must not repeat editorial framing prose");
}
if (!enhancer.includes('/narrative activation/i.test(word.note || "")')) {
  throw new Error("obsolete narrative-activation notes must not survive into public word cards");
}
if (JSON.stringify([...observedSemanticKeys].sort()) !== JSON.stringify([...semanticKeys].sort())) {
  throw new Error("not every semantic field is attached to a public word card");
}
if (enhancer.includes("renderTranslation") || enhancer.includes("yv-final-translation")) {
  throw new Error("reader renders a duplicate unlinked translation block");
}
if (!gitaReader.includes("cardEl.contains(e.target)")
    || !gitaReader.includes("dismissCardsOnScroll")
    || !gitaReader.includes("cardEl.scrollTop += event.deltaY")) {
  throw new Error("long word cards must scroll internally without dismissing themselves");
}
if (!enhancer.includes("splitEnglishSemanticTriggers") || !enhancer.includes("renderFocusedSemanticCard")) {
  throw new Error("compound names must be individually selectable in the English line");
}
if (!enhancer.includes('new Set(["shambara", "dama", "vyala", "kata", "bhima", "bhasa", "drdha"])')) {
  throw new Error("individual English triggers must be limited to the reviewed proper-name population");
}
if (!readerStyle.includes("@media (min-width: 721px)")
    || !readerStyle.includes("width: clamp(540px, 56vw, 760px)")
    || !readerStyle.includes("overscroll-behavior: contain")) {
  throw new Error("long evidence cards must widen only on desktop and contain their own scrolling");
}

console.log(`Yoga-Vāsiṣṭha presentation: 56 units, ${wordCount} words, one linked translation layer`);
