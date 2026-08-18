#!/usr/bin/env node
"use strict";

// Read-only progress report for the all-figure chronology migration. A missing
// traditional record is not a license to invent dates: it is a source-research
// task that must be tracked explicitly.

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "data/manifest.json"), "utf8"));
const totals = { visible: 0, structured: 0, academic: 0, traditional: 0, explicitTraditionalStatus: 0, legacyOnly: 0 };
const needsTraditionalEvidence = [];

for (const filename of manifest.thinkers || []) {
  const thinker = JSON.parse(fs.readFileSync(path.join(root, "data", "thinkers", filename), "utf8"));
  if (thinker.display === false) continue;
  totals.visible += 1;
  const chronology = thinker.chronology;
  if (!chronology || !chronology.variants) {
    totals.legacyOnly += 1;
    needsTraditionalEvidence.push(thinker.id);
    continue;
  }
  totals.structured += 1;
  if (chronology.variants.academic) totals.academic += 1;
  if (chronology.variants.traditional) totals.traditional += 1;
  if (chronology.traditional_status) totals.explicitTraditionalStatus += 1;
  if (!chronology.variants.traditional && !chronology.traditional_status) needsTraditionalEvidence.push(thinker.id);
}

console.log("Chronology coverage report (informational)");
for (const [label, value] of Object.entries(totals)) console.log(`${label}: ${value}`);
console.log(`needs_traditional_evidence_or_status: ${needsTraditionalEvidence.length}`);
for (const id of needsTraditionalEvidence) console.log(`  ${id}`);
