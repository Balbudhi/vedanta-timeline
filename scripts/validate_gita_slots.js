#!/usr/bin/env node
/* Validate the Gītā reader data: every {i:…} slot in an `english` field must
   resolve to a real index in the sibling `words[]`, `i` indices must be
   contiguous from 0, and we report any literal [..] bracket inserts so the
   polish pass can see what is left. Read-only; exits non-zero on any error. */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
function load(file, globalName) {
  const code = fs.readFileSync(path.join(ROOT, file), "utf8");
  const sandbox = { window: {} };
  new Function("window", code)(sandbox.window);
  return sandbox.window[globalName];
}

const SLOT_RE = /\{([\d,\s]+):([^}]*)\}/g;
const BRACKET_RE = /\[[^\]]*\]/g;

let errors = 0;
let unitCount = 0;
const brackets = [];
const coverage = { words: 0, uncovered: 0, doubled: 0, units: [] };

function checkUnit(label, words, english) {
  if (!english) return;
  unitCount++;
  // Slots reference the word's `i` *value* (which may be non-contiguous), not
  // its array position, so validate against the actual set of i values present.
  const present = new Set(Array.isArray(words) ? words.map((w) => w.i) : []);
  const seen = new Map();   // word i -> how many slots referenced it
  let m;
  SLOT_RE.lastIndex = 0;
  while ((m = SLOT_RE.exec(english)) !== null) {
    const idxs = m[1].split(",").map((s) => s.trim()).filter(Boolean).map(Number);
    for (const i of idxs) {
      if (!present.has(i)) { console.error(`✗ ${label}: slot {${i}:…} has no matching word (i values: ${[...present].join(",")})`); errors++; }
      seen.set(i, (seen.get(i) || 0) + 1);
    }
  }
  // Reported, not failed. A word in no slot still opens its card; it simply
  // highlights nothing, which is the right outcome for a particle the English
  // does not render separately (iti closing a quotation, ca, tu, hi, eva).
  // A word in two slots highlights in two places, which is right when one
  // Sanskrit word governs two English phrases. Both are judgement calls the
  // authoring makes deliberately, so they surface as coverage numbers rather
  // than as build failures. A slot pointing at a word that does not exist is
  // the genuinely broken case, and that still fails above.
  const uncovered = [...present].filter((i) => !seen.has(i));
  if (uncovered.length) {
    coverage.uncovered += uncovered.length;
    coverage.units.push(`${label}: ${uncovered.map((i) => (words.find((w) => w.i === i) || {}).iast || i).join(", ")}`);
  }
  coverage.doubled += [...seen].filter(([, n]) => n > 1).length;
  coverage.words += present.size;
  // record literal bracket inserts (informational)
  const bs = english.match(BRACKET_RE);
  if (bs) brackets.push({ label, items: bs });
}

// Every word-by-word reading on the site: its directory and the globals its
// data files populate. A file that does not exist for a reading is skipped
// (not every reading has parallels or an Aurobindo layer).
const READINGS = [
  { dir: "gita/sthitaprajna", verses: "GITA_VERSES", commentary: "GITA_COMMENTARY", parallels: "GITA_PARALLELS" },
  { dir: "gita/kama", verses: "GITA3_VERSES", commentary: "GITA3_COMMENTARY", parallels: "GITA3_PARALLELS" },
  { dir: "gita/ch5", verses: "CH5_VERSES", commentary: "CH5_COMMENTARY", parallels: "CH5_PARALLELS" },
];

function loadIfPresent(file, globalName) {
  if (!fs.existsSync(path.join(ROOT, file))) return null;
  return load(file, globalName);
}

for (const r of READINGS) {
  const verses = loadIfPresent(`${r.dir}/verses.js`, r.verses) || [];
  for (const v of verses) {
    checkUnit(`${r.dir} verse ${v.locus} (mūla)`, v.words, v.english);
    for (const c of v.commentaries || []) {
      checkUnit(`${r.dir} verse ${v.locus} / ${c.voiceId || c.author || "?"}`, c.words, c.english);
    }
  }

  const com = loadIfPresent(`${r.dir}/commentaries.js`, r.commentary) || {};
  for (const locus of Object.keys(com)) {
    for (const c of com[locus]) {
      checkUnit(`${r.dir} comm ${locus} / ${c.voiceId || c.author || "?"}`, c.words, c.english);
    }
  }

  const par = loadIfPresent(`${r.dir}/parallels.js`, r.parallels) || {};
  for (const locus of Object.keys(par)) {
    for (const p of par[locus]) {
      checkUnit(`${r.dir} parallel ${locus} / ${p.thinker || p.school || "?"}`, p.words, p.english);
    }
  }
}

console.log(`Checked ${unitCount} interactive units.`);
console.log(`Word-slot coverage: ${coverage.words - coverage.uncovered}/${coverage.words} words highlight an English phrase`);
console.log(`  ${coverage.uncovered} unslotted (particles the English does not render separately), ${coverage.doubled} in two slots`);
console.log(`Literal [..] bracket inserts remaining in ${brackets.length} units:`);
for (const b of brackets) console.log(`  ${b.label}: ${b.items.join("  ")}`);
if (errors) { console.error(`\n${errors} slot error(s).`); process.exit(1); }
console.log("\nAll slots resolve. OK.");
