#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const review = JSON.parse(fs.readFileSync(path.join(root, "gita/yogavasistha-dama/review.json"), "utf8"));
const enhancer = fs.readFileSync(path.join(root, "gita/yogavasistha-dama/enhancer.js"), "utf8");

if (review.units.length !== 56) throw new Error(`expected 56 units, found ${review.units.length}`);

let wordCount = 0;
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
  for (const entry of unit.apparatus || []) {
    if (!entry.sourceSegments) continue;
    const entryExpected = entry.words.map((_, index) => index);
    const entryObserved = entry.sourceSegments.flatMap(segment => segment.word_indices);
    if (JSON.stringify(entryObserved) !== JSON.stringify(entryExpected)) {
      throw new Error(`${entry.id}: source-script links do not cover every apparatus word once`);
    }
  }
  wordCount += unit.words.length;
}

if (!enhancer.includes("renderSourceScript")) {
  throw new Error("enhancer does not connect exact source-script segments to reviewed word indices");
}
if (enhancer.includes("renderTranslation") || enhancer.includes("yv-final-translation")) {
  throw new Error("reader renders a duplicate unlinked translation block");
}

console.log(`Yoga-Vāsiṣṭha presentation: 56 units, ${wordCount} words, one linked translation layer`);
