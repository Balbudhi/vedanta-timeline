#!/usr/bin/env node
/* Compare the current Sanskrit gap queue to the disjoint work-partition audits. */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "data/editorial/catalogue_sweeps");
const FILES = [
  "advaita-queue-acquisition-audit.json",
  "vaishnava-queue-acquisition-audit.json",
  "dvaita-queue-acquisition-audit.json",
  "buddhist-jain-queue-acquisition-audit.json",
  "darsanas-queue-acquisition-audit.json",
  "saiva-regional-queue-acquisition-audit.json",
  "cross-residual-queue-acquisition-audit.json"
];
const ACTIONABLE = new Set(["primary-text-not-in-corpus", "degraded-on-disk"]);
const key = (thinker, work) => `${thinker}/${work}`;
function auditRows(audit) { return audit.works || audit.rows || audit.records || []; }

const expected = new Set();
for (const name of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((name) => name.endsWith(".json"))) {
  const thinker = JSON.parse(fs.readFileSync(path.join(ROOT, "data/thinkers", name), "utf8"));
  for (const work of thinker.engaged_works || []) if (work.language === "sanskrit" && ACTIONABLE.has(work.source_status)) expected.add(key(thinker.id, work.work_id));
}
const owners = new Map();
for (const file of FILES) {
  const audit = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf8"));
  for (const row of auditRows(audit)) {
    const rowKey = row.key || row.work_key || key(row.thinker_id, row.work_id);
    if (!rowKey || rowKey === "undefined/undefined") continue;
    if (!owners.has(rowKey)) owners.set(rowKey, []);
    owners.get(rowKey).push(file);
  }
}
const missing = [...expected].filter((item) => !owners.has(item));
const duplicate = [...owners.entries()].filter(([, files]) => files.length > 1);
const historical = [...owners.keys()].filter((item) => !expected.has(item));
const report = { current_sanskrit_gaps: expected.size, audited_current_gaps: expected.size - missing.length, missing, duplicate, historical };
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Partition coverage: ${report.audited_current_gaps}/${report.current_sanskrit_gaps} current Sanskrit gaps audited.`);
  if (missing.length) console.log(`Missing: ${missing.join(", ")}`);
  if (duplicate.length) console.log(`Duplicate shard ownership: ${duplicate.map(([item, files]) => `${item} (${files.join(", ")})`).join("; ")}`);
  if (historical.length) console.log(`Historical rows (no longer current): ${historical.length}`);
}
// Shared boundary figures can legitimately be audited in more than one shard;
// duplicate ownership is reported for reconciliation but is not a coverage failure.
process.exitCode = missing.length ? 1 : 0;
