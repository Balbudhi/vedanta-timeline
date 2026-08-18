#!/usr/bin/env node
"use strict";

// Structural integrity check for the visible thinker graph.  It deliberately
// validates stable identifiers and registry references, rather than comparing
// legacy free-text labels that now resolve through school_color_token.

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(ROOT, relative), "utf8"));
const manifest = readJson("data/manifest.json");
const schools = readJson("data/registries/schools.json");
const failures = [];
const entityKinds = new Set(["historical_author", "canonical_teacher", "reconstructed_position", "comparator"]);

function fail(message) { failures.push(message); }
function expectArray(value, label) { if (!Array.isArray(value)) fail(`${label} must be an array`); return Array.isArray(value) ? value : []; }

const thinkers = [];
const ids = new Map();
for (const filename of expectArray(manifest.thinkers, "manifest.thinkers")) {
  if (typeof filename !== "string" || !filename.endsWith(".json")) {
    fail(`manifest thinker entry is not a JSON filename: ${String(filename)}`);
    continue;
  }
  const relative = path.join("data", "thinkers", filename);
  let thinker;
  try { thinker = readJson(relative); } catch (error) { fail(`${relative}: ${error.message}`); continue; }
  if (!thinker.id || typeof thinker.id !== "string") fail(`${filename}: missing string id`);
  if (ids.has(thinker.id)) fail(`${filename}: duplicate id ${thinker.id} (also ${ids.get(thinker.id).filename})`);
  ids.set(thinker.id, { filename, thinker });
  thinkers.push({ filename, thinker });
  if (path.basename(filename, ".json") !== thinker.id) fail(`${filename}: id must match filename stem (${thinker.id})`);
  if (!schools[thinker.school_color_token]) fail(`${filename}: unknown school_color_token ${String(thinker.school_color_token)}`);
  if (thinker.entity_kind != null && !entityKinds.has(thinker.entity_kind)) fail(`${filename}: unsupported entity_kind ${thinker.entity_kind}`);
  if (thinker.display !== false && typeof thinker.dates_low !== "number") fail(`${filename}: visible thinker dates_low must be numeric`);
  if (thinker.display !== false && !(typeof thinker.dates_high === "number" || thinker.dates_high === null || thinker.dates_high === 0)) fail(`${filename}: visible thinker dates_high must be numeric, null, or legacy 0`);
  const workIds = new Set();
  for (const work of thinker.engaged_works == null ? [] : expectArray(thinker.engaged_works, `${filename}.engaged_works`)) {
    if (!work || typeof work.work_id !== "string" || !work.work_id) fail(`${filename}: engaged work missing work_id`);
    else if (workIds.has(work.work_id)) fail(`${filename}: duplicate work_id ${work.work_id}`);
    else workIds.add(work.work_id);
  }
}

for (const { filename, thinker } of thinkers) {
  for (const field of ["lineage_in", "lineage_out"]) {
    for (const id of thinker[field] == null ? [] : expectArray(thinker[field], `${filename}.${field}`)) {
      if (!ids.has(id)) fail(`${filename}: ${field} references missing thinker ${id}`);
      if (id === thinker.id) fail(`${filename}: ${field} may not self-reference`);
    }
  }
  for (const edge of thinker.lineage_polemical == null ? [] : expectArray(thinker.lineage_polemical, `${filename}.lineage_polemical`)) {
    if (!edge || !ids.has(edge.thinker_id)) fail(`${filename}: polemical edge references missing thinker ${edge && edge.thinker_id}`);
    if (edge && edge.thinker_id === thinker.id) fail(`${filename}: polemical edge may not self-reference`);
  }
}

if (failures.length) {
  console.error(`Thinker reference check failed: ${failures.length} issue(s).`);
  for (const message of failures) console.error(`  ${message}`);
  process.exit(1);
}

console.log(`Thinker reference check passed: ${thinkers.length} records, ${Object.keys(schools).length} school tokens.`);
