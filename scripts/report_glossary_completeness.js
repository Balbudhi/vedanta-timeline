#!/usr/bin/env node
"use strict";

// Read-only internal report for glossary fields that need sourcing or editorial
// work. Public rendering remains graceful; this report makes the unfinished
// queue explicit for contributors.

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const glossaryDir = path.join(root, "data", "glossary");
const manifest = JSON.parse(fs.readFileSync(path.join(glossaryDir, "manifest.json"), "utf8"));
const terms = manifest.terms || [];
const buckets = {
  needsLiteral: [],
  needsInvariantDefinition: [],
  needsSchoolReading: [],
  needsPrimaryLocus: [],
  needsTranslatorNote: [],
};

for (const manifestEntry of terms) {
  const key = String(manifestEntry).replace(/\.json$/i, "");
  const file = path.join(glossaryDir, `${key}.json`);
  if (!fs.existsSync(file)) {
    console.error(`Missing manifest glossary file: ${key}.json`);
    process.exitCode = 1;
    continue;
  }
  const entry = JSON.parse(fs.readFileSync(file, "utf8"));
  const name = entry.term_iast || key;
  if (!String(entry.literal || "").trim()) buckets.needsLiteral.push(name);
  if (!String(entry.invariant_definition || "").trim()) buckets.needsInvariantDefinition.push(name);
  const schools = Array.isArray(entry.per_school) ? entry.per_school : [];
  if (!schools.length) buckets.needsSchoolReading.push(name);
  if (!schools.some((school) => Array.isArray(school.primary_loci) && school.primary_loci.length)) buckets.needsPrimaryLocus.push(name);
  if (!String(entry.translator_note || "").trim()) buckets.needsTranslatorNote.push(name);
}

console.log("Glossary completeness report (informational)");
console.log(`Manifest entries: ${terms.length}`);
for (const [label, values] of Object.entries(buckets)) {
  console.log(`${label}: ${values.length}`);
  for (const value of values) console.log(`  ${value}`);
}
