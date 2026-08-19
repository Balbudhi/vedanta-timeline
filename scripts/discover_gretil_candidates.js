#!/usr/bin/env node
/*
 * Match the current Sanskrit acquisition queue against a locally supplied
 * GRETIL path index. It only proposes candidates; it does not download or
 * register them because a filename match is not textual verification.
 */
"use strict";

const child = require("child_process");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const indexPath = process.argv[2];
if (!indexPath || process.argv.includes("--help")) {
  console.error("Usage: node scripts/discover_gretil_candidates.js <gretil-path-index.txt> [--json]");
  process.exit(1);
}
function key(value) { return String(value || "").toLowerCase().replace(/[^a-z0-9]/g, ""); }
const queue = JSON.parse(child.execFileSync(process.execPath, [path.join(ROOT, "scripts/report_acquisition_queue.js"), "--json"], { encoding: "utf8" })).works
  .filter((work) => work.language === "sanskrit");
const gretilPaths = fs.readFileSync(indexPath, "utf8").split(/\r?\n/).filter(Boolean)
  .filter((item) => item.endsWith(".xml") && item.includes("sa_"));
const matches = [];
for (const work of queue) {
  const workKey = key(work.work_id);
  const thinkerKey = key(work.thinker_id);
  if (workKey.length < 6 || thinkerKey.length < 5) continue;
  for (const sourcePath of gretilPaths) {
    const sourceKey = key(path.basename(sourcePath, ".xml"));
    if (sourceKey.includes(workKey) && sourceKey.includes(thinkerKey)) {
      matches.push({
        thinker_id: work.thinker_id,
        work_id: work.work_id,
        title_iast: work.title_iast,
        source_path: sourcePath,
        candidate_url: `https://raw.githubusercontent.com/sanskrit-texts/gretil-corpus/main/${sourcePath}`,
        note: "Filename match only. Inspect TEI header, coverage, rights, and sample readings before candidate registration."
      });
    }
  }
}
const report = { queue_total: queue.length, gretil_xml_paths: gretilPaths.length, filename_matches: matches.length, candidates: matches };
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`GRETIL filename discovery: ${matches.length} possible candidate(s) for ${queue.length} Sanskrit works.`);
  for (const match of matches) console.log(`${match.thinker_id}\t${match.work_id}\t${match.source_path}`);
}
