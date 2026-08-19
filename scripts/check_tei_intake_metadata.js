#!/usr/bin/env node
/* Ensure quarantined TEI candidates retain the editorial metadata required for review. */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const INTAKE = path.join(ROOT, "data/sources/_intake");
const candidates = new Map(JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8"))
  .candidates.map((candidate) => [candidate.id, candidate]));

function provenanceFiles(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name);
    if (entry.isDirectory()) provenanceFiles(target, out);
    else if (entry.name === "PROVENANCE.json") out.push(target);
  }
  return out;
}
let checked = 0;
let errors = 0;
for (const provenancePath of provenanceFiles(INTAKE)) {
  const provenance = JSON.parse(fs.readFileSync(provenancePath, "utf8"));
  const root = path.dirname(provenancePath);
  for (const witness of provenance.witnesses || []) {
    const candidate = candidates.get(witness.candidate_id);
    if (!candidate || !/TEI/i.test(candidate.access_kind || "")) continue;
    const witnessPath = witness.path || witness.iast_path;
    if (!witnessPath || !/\.xml$/i.test(witnessPath)) { errors += 1; console.error(`${witness.candidate_id}: TEI candidate has no XML witness path`); continue; }
    checked += 1;
    const text = fs.readFileSync(path.join(root, witnessPath), "utf8");
    const required = ["<TEI", "<teiHeader", "<titleStmt", "<publicationStmt", "<sourceDesc"];
    const missing = required.filter((marker) => !text.includes(marker));
    if (missing.length) { errors += 1; console.error(`${witness.candidate_id}: missing TEI metadata marker(s): ${missing.join(", ")}`); }
    const hasLicenceStatement = /<licence\b/i.test(text) || /<availability\b[\s\S]{0,800}Creative Commons/i.test(text);
    if (!hasLicenceStatement) { errors += 1; console.error(`${witness.candidate_id}: no TEI licence or Creative Commons availability statement`); }
  }
}
console.log(`TEI intake metadata: ${checked} witness(es) checked; ${errors} error(s).`);
process.exitCode = errors ? 1 : 0;
