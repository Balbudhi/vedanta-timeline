#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const FILE = path.join(ROOT, "data/editorial/source_candidates.json");
const REQUIRED = ["id", "thinker_id", "work_id", "title_iast", "language", "provider", "candidate_url", "access_kind", "coverage", "quality_tier", "rights_status", "acquisition_status", "review_status"];
const STATES = new Set(["discovered", "retrieval-confirmed", "downloaded-quarantine", "normalized-working", "collated-sample", "accepted-public-witness", "rejected", "blocked-rights", "no-clean-digital-witness-found"]);
const QUALITY = new Set(["candidate-clean", "candidate-clean-reconstruction", "needs-manual-assessment"]);
const DISALLOWED = new Set(["pdf", "image-pdf-scan", "ocr", "translation"]);
const record = JSON.parse(fs.readFileSync(FILE, "utf8"));
let failures = 0;
const ids = new Set();
for (const [index, candidate] of (record.candidates || []).entries()) {
  const label = `source_candidates[${index}]`;
  for (const field of REQUIRED) if (typeof candidate[field] !== "string" || !candidate[field].trim()) {
    failures += 1; console.error(`${label}: missing ${field}`);
  }
  if (ids.has(candidate.id)) { failures += 1; console.error(`${label}: duplicate id ${candidate.id}`); }
  ids.add(candidate.id);
  if (candidate.language !== "sanskrit") { failures += 1; console.error(`${label}: candidate must be Sanskrit`); }
  if (!/^https:\/\//.test(candidate.candidate_url || "")) { failures += 1; console.error(`${label}: candidate_url must be HTTPS`); }
  if (!STATES.has(candidate.acquisition_status)) { failures += 1; console.error(`${label}: invalid acquisition_status`); }
  if (!QUALITY.has(candidate.quality_tier)) { failures += 1; console.error(`${label}: invalid quality_tier`); }
  if (DISALLOWED.has(candidate.access_kind)) { failures += 1; console.error(`${label}: PDF/OCR/translation is not a clean Sanskrit candidate`); }
  if (candidate.acquisition_status === "accepted-public-witness") { failures += 1; console.error(`${label}: public promotion belongs in manifest + ledger, not candidate registry`); }
}
console.log(`Source candidates: ${(record.candidates || []).length} candidate witness record(s); ${failures} error(s).`);
process.exitCode = failures ? 1 : 0;
