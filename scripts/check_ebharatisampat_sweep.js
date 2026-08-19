#!/usr/bin/env node
/* Verify that the committed E-Bharatisampat title sweep covers every live Sanskrit gap. */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const SWEEP = path.join(ROOT, "data/editorial/catalogue_sweeps/ebharatisampat_title_sweep_2026-08-19.json");
const ACTIONABLE = new Set(["primary-text-not-in-corpus", "degraded-on-disk"]);
const key = (thinkerId, workId) => `${thinkerId}/${workId}`;

const expected = new Set();
for (const filename of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((name) => name.endsWith(".json"))) {
  const thinker = JSON.parse(fs.readFileSync(path.join(ROOT, "data/thinkers", filename), "utf8"));
  for (const work of thinker.engaged_works || []) if (work.language === "sanskrit" && ACTIONABLE.has(work.source_status)) expected.add(key(thinker.id, work.work_id));
}
const rows = JSON.parse(fs.readFileSync(SWEEP, "utf8"));
const found = new Set();
const duplicates = [];
for (const row of rows) {
  const item = row.work || {};
  const rowKey = key(item.thinker_id, item.work_id);
  if (found.has(rowKey)) duplicates.push(rowKey);
  found.add(rowKey);
}
const missing = [...expected].filter((item) => !found.has(item));
const historical = [...found].filter((item) => !expected.has(item));
if (duplicates.length) console.error(`Duplicate sweep rows: ${duplicates.join(", ")}`);
if (missing.length) console.error(`Current Sanskrit gaps absent from sweep: ${missing.join(", ")}`);
console.log(`E-Bharatisampat title sweep: ${rows.length} recorded row(s); ${expected.size} current Sanskrit gap(s); ${historical.length} historical row(s); ${missing.length} missing row(s); ${duplicates.length} duplicate(s).`);
process.exitCode = duplicates.length || missing.length ? 1 : 0;
