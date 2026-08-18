#!/usr/bin/env node
"use strict";

// Read-only quality queue for thinker bios and work summaries. It does not
// judge philosophical merit; it flags records whose shape needs source/editor
// review before a normalization wave.

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "data/manifest.json"), "utf8"));
const buckets = { missingCoreThesis: [], shortCoreThesis: [], longCoreThesis: [], missingWorkSummary: [], shortWorkSummary: [], longWorkSummary: [], onDiskButUncited: [] };
const words = (value) => String(value || "").trim().split(/\s+/).filter(Boolean).length;

for (const filename of manifest.thinkers || []) {
  const thinker = JSON.parse(fs.readFileSync(path.join(root, "data", "thinkers", filename), "utf8"));
  if (thinker.display === false) continue;
  const core = words(thinker.core_thesis);
  if (!core) buckets.missingCoreThesis.push(thinker.id);
  else if (core < 70) buckets.shortCoreThesis.push(thinker.id);
  else if (core > 220) buckets.longCoreThesis.push(thinker.id);
  const text = JSON.stringify(thinker);
  const hasOnDiskWork = (thinker.engaged_works || []).some((work) => /on-disk/.test(work.source_status || ""));
  if (hasOnDiskWork && !text.includes("cite://")) buckets.onDiskButUncited.push(thinker.id);
  for (const work of thinker.engaged_works || []) {
    const count = words(work.summary);
    const label = `${thinker.id}/${work.work_id || "missing-work-id"}`;
    if (!count) buckets.missingWorkSummary.push(label);
    else if (count < 35) buckets.shortWorkSummary.push(label);
    else if (count > 230) buckets.longWorkSummary.push(label);
  }
}

console.log("Thinker content-shape report (informational)");
for (const [bucket, entries] of Object.entries(buckets)) {
  console.log(`${bucket}: ${entries.length}`);
  for (const entry of entries) console.log(`  ${entry}`);
}
