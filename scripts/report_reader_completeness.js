#!/usr/bin/env node
"use strict";

// Read-only completeness report for the reusable Sanskrit reader datasets.
// This is intentionally a report, not a pass/fail gate: it identifies source
// acquisition and grammar work without treating absent verified data as a
// reason to invent it.

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

function loadGlobal(relativePath, name) {
  const sandbox = {};
  const source = fs.readFileSync(path.join(root, relativePath), "utf8");
  new Function("window", source)(sandbox);
  return sandbox[name];
}

function emptyCounts() {
  return { units: 0, missingDevanagari: 0, missingWordDevanagari: 0, missingGrammar: 0, missingGlossaryKeys: 0 };
}

function inspectUnit(counts, unit, label) {
  counts.units += 1;
  if (!unit.devanagari) counts.missingDevanagari += 1;
  const words = Array.isArray(unit.words) ? unit.words : [];
  if (!words.length || words.some((word) => !word.deva)) counts.missingWordDevanagari += 1;
  if (!unit.grammar || (!unit.grammar.karakaSummary && !unit.grammar.verbalModality)) counts.missingGrammar += 1;
  if (words.some((word) => word.glossaryKey === undefined)) counts.missingGlossaryKeys += 1;
  return label;
}

const verses = loadGlobal("gita/sthitaprajna/verses.js", "GITA_VERSES") || [];
const commentary = loadGlobal("gita/sthitaprajna/commentaries.js", "GITA_COMMENTARY") || {};
const mula = emptyCounts();
const voices = emptyCounts();

for (const verse of verses) inspectUnit(mula, verse, verse.locus);
for (const [locus, entries] of Object.entries(commentary)) {
  for (const entry of entries || []) inspectUnit(voices, entry, `${locus} ${entry.author || "unknown"}`);
}

function print(label, counts) {
  console.log(`${label}: ${counts.units} units`);
  console.log(`  missing top-level Devanagari: ${counts.missingDevanagari}`);
  console.log(`  missing per-word Devanagari: ${counts.missingWordDevanagari}`);
  console.log(`  missing unit grammar summary: ${counts.missingGrammar}`);
  console.log(`  units with words lacking an explicit glossaryKey field: ${counts.missingGlossaryKeys}`);
}

console.log("Sanskrit reader completeness report (informational)");
print("Mūla", mula);
print("Commentary", voices);
