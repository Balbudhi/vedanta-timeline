#!/usr/bin/env node
/*
 * Match the Sanskrit acquisition queue against Muktabodha’s CC BY-NC e-text
 * filename index. Matches are discovery leads only; inspect the individual
 * e-text’s catalogue metadata and coverage before registration or download.
 */
"use strict";

const child = require("child_process");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const indexPath = process.argv[2];
if (!indexPath || process.argv.includes("--help")) {
  console.error("Usage: node scripts/discover_muktabodha_candidates.js <muktabodha-path-index.txt> [--json]");
  process.exit(1);
}
function key(value) { return String(value || "").toLowerCase().replace(/[^a-z0-9]/g, ""); }
const queue = JSON.parse(child.execFileSync(process.execPath, [path.join(ROOT, "scripts/report_acquisition_queue.js"), "--json"], { encoding: "utf8" })).works
  .filter((work) => work.language === "sanskrit");
const textPaths = fs.readFileSync(indexPath, "utf8").split(/\r?\n/).filter((item) => item.startsWith("texts/") && item.endsWith(".txt"));
const matches = [];
for (const work of queue) {
  const workKey = key(work.work_id);
  const thinkerKey = key(work.thinker_id);
  if (workKey.length < 6 || thinkerKey.length < 5) continue;
  for (const sourcePath of textPaths) {
    const sourceKey = key(path.basename(sourcePath, ".txt"));
    if (sourceKey.includes(workKey) && sourceKey.includes(thinkerKey)) {
      matches.push({
        thinker_id: work.thinker_id,
        work_id: work.work_id,
        title_iast: work.title_iast,
        source_path: sourcePath,
        candidate_url: `https://raw.githubusercontent.com/tokushige-koyasan/muktabodha-corpus/main/${sourcePath}`,
        license: "CC-BY-NC-4.0; attribute Muktabodha",
        note: "Filename match only. Inspect Muktabodha catalogue number, edition metadata, coverage, and source text before candidate registration."
      });
    }
  }
}
const report = { queue_total: queue.length, muktabodha_etext_paths: textPaths.length, filename_matches: matches.length, candidates: matches };
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Muktabodha filename discovery: ${matches.length} possible candidate(s) for ${queue.length} Sanskrit works.`);
  for (const match of matches) console.log(`${match.thinker_id}\t${match.work_id}\t${match.source_path}`);
}
