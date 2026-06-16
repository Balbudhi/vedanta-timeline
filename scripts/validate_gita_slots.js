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

function checkUnit(label, words, english) {
  if (!english) return;
  unitCount++;
  // Slots reference the word's `i` *value* (which may be non-contiguous), not
  // its array position, so validate against the actual set of i values present.
  const present = new Set(Array.isArray(words) ? words.map((w) => w.i) : []);
  let m;
  SLOT_RE.lastIndex = 0;
  while ((m = SLOT_RE.exec(english)) !== null) {
    const idxs = m[1].split(",").map((s) => s.trim()).filter(Boolean).map(Number);
    for (const i of idxs) {
      if (!present.has(i)) { console.error(`✗ ${label}: slot {${i}:…} has no matching word (i values: ${[...present].join(",")})`); errors++; }
    }
  }
  // record literal bracket inserts (informational)
  const bs = english.match(BRACKET_RE);
  if (bs) brackets.push({ label, items: bs });
}

const verses = load("gita/sthitaprajna/verses.js", "GITA_VERSES");
for (const v of verses) {
  checkUnit(`verse ${v.locus} (mūla)`, v.words, v.english);
  for (const c of v.commentaries || []) {
    checkUnit(`verse ${v.locus} / ${c.voiceId || c.author || "?"}`, c.words, c.english);
  }
}

const com = load("gita/sthitaprajna/commentaries.js", "GITA_COMMENTARY");
for (const locus of Object.keys(com)) {
  for (const c of com[locus]) {
    checkUnit(`comm ${locus} / ${c.voiceId || c.author || "?"}`, c.words, c.english);
  }
}

console.log(`Checked ${unitCount} interactive units.`);
console.log(`Literal [..] bracket inserts remaining in ${brackets.length} units:`);
for (const b of brackets) console.log(`  ${b.label}: ${b.items.join("  ")}`);
if (errors) { console.error(`\n${errors} slot error(s).`); process.exit(1); }
console.log("\nAll slots resolve. OK.");
