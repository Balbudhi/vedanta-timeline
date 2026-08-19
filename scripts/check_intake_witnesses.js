#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const INTAKE_ROOT = path.join(ROOT, "data/sources/_intake");
const candidates = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8")).candidates.map((candidate) => candidate.id));
let errors = 0;
function findProvenance(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name);
    if (entry.isDirectory()) findProvenance(target, out);
    else if (entry.name === "PROVENANCE.json") out.push(target);
  }
  return out;
}
const provenanceFiles = findProvenance(INTAKE_ROOT);
let checked = 0;
const pairedWitnesses = new Map();
for (const provenancePath of provenanceFiles) {
  const provenance = JSON.parse(fs.readFileSync(provenancePath, "utf8"));
  const witnessRoot = path.dirname(provenancePath);
  const witnesses = (provenance.witnesses || []).flatMap((witness) => {
    if (!witness.iast_path && !witness.devanagari_path) return [{ ...witness, script: witness.script || provenance.script }];
    return [
      { ...witness, path: witness.iast_path, sha256: witness.iast_sha256, script: "iast" },
      { ...witness, path: witness.devanagari_path, sha256: witness.devanagari_sha256, script: "devanagari" }
    ];
  });
  for (const witness of witnesses) {
    checked += 1;
  const label = witness.candidate_id || witness.path;
  if (provenance.paired_download) {
    if (!witness.script || !witness.catalog_no) {
      errors += 1;
      console.error(`${label}: paired intake requires a script and catalogue number`);
    } else {
      const key = `${provenance.paired_download}:${witness.catalog_no}`;
      if (!pairedWitnesses.has(key)) pairedWitnesses.set(key, []);
      pairedWitnesses.get(key).push({ label, script: witness.script });
    }
  }
  const target = path.resolve(witnessRoot, witness.path || "");
  if (!target.startsWith(witnessRoot + path.sep) || !fs.existsSync(target)) {
    errors += 1; console.error(`${label}: intake path missing or escapes intake root`); continue;
  }
  if (!candidates.has(witness.candidate_id)) { errors += 1; console.error(`${label}: missing source-candidate record`); }
  const bytes = fs.readFileSync(target);
  const actual = crypto.createHash("sha256").update(bytes).digest("hex");
  if (actual !== witness.sha256) { errors += 1; console.error(`${label}: checksum mismatch`); }
  if (bytes.subarray(0, 4).toString("ascii") === "%PDF") { errors += 1; console.error(`${label}: PDF is not allowed in clean-text intake`); }
  let text;
  try { text = new TextDecoder("utf-8", { fatal: true }).decode(bytes); }
  catch (_) {
    if ((witness.known_issues || []).includes("malformed-utf8")) console.warn(`${label}: documented malformed UTF-8; quarantine only`);
    else errors += 1;
    if (!(witness.known_issues || []).includes("malformed-utf8")) console.error(`${label}: malformed UTF-8`);
    continue;
  }
  if (text.includes("\uFFFD")) {
    if ((witness.known_issues || []).includes("replacement-characters")) console.warn(`${label}: documented replacement characters; quarantine only`);
    else { errors += 1; console.error(`${label}: undocumented replacement character in witness`); }
  }
  if (!/[\u0900-\u097Fāīūṛṝḷṅñṭḍṇśṣṃḥ]/u.test(text)) { errors += 1; console.error(`${label}: no Sanskrit-script or IAST signal`); }
  if (target.endsWith(".xml") && !/^\s*<\?xml[\s\S]*<TEI\b/m.test(text)) { errors += 1; console.error(`${label}: expected TEI XML root`); }
  }
}
for (const [key, witnesses] of pairedWitnesses) {
  const scripts = witnesses.map((witness) => witness.script);
  const validPair = witnesses.length === 2
    && scripts.filter((script) => script === "iast").length === 1
    && scripts.filter((script) => script === "devanagari").length === 1;
  if (!validPair) {
    errors += 1;
    console.error(`${key}: expected exactly one IAST and one Devanāgarī witness; found ${witnesses.map((witness) => `${witness.script}:${witness.label}`).join(", ")}`);
  }
}
console.log(`Intake witnesses: ${checked} checked across ${provenanceFiles.length} provenance record(s); ${errors} error(s).`);
process.exitCode = errors ? 1 : 0;
