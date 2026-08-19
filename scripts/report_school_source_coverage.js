#!/usr/bin/env node
/* Aggregate the thinker-first source queue by school without treating candidates as public corpus. */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const CANDIDATES = JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8")).candidates || [];
const ON_DISK = /on-disk/;
const rows = new Map();
function row(school) {
  if (!rows.has(school)) rows.set(school, { school, works: 0, public_on_disk: 0, missing: 0, degraded: 0, other: 0, candidate_backed: 0, quarantine_downloaded: 0, no_candidate: 0 });
  return rows.get(school);
}
function candidateFor(thinkerId, workId) { return CANDIDATES.filter((candidate) => candidate.thinker_id === thinkerId && candidate.work_id === workId); }
for (const filename of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((name) => name.endsWith(".json"))) {
  const thinker = JSON.parse(fs.readFileSync(path.join(ROOT, "data/thinkers", filename), "utf8"));
  const schoolRow = row(thinker.school || "Unclassified");
  for (const work of thinker.engaged_works || []) {
    schoolRow.works += 1;
    if (ON_DISK.test(work.source_status || "")) schoolRow.public_on_disk += 1;
    else if (work.source_status === "primary-text-not-in-corpus") schoolRow.missing += 1;
    else if (work.source_status === "degraded-on-disk") schoolRow.degraded += 1;
    else schoolRow.other += 1;
    if (work.source_status === "primary-text-not-in-corpus" || work.source_status === "degraded-on-disk") {
      const candidates = candidateFor(thinker.id, work.work_id);
      if (candidates.length) {
        schoolRow.candidate_backed += 1;
        if (candidates.some((candidate) => candidate.acquisition_status === "downloaded-quarantine")) schoolRow.quarantine_downloaded += 1;
      } else schoolRow.no_candidate += 1;
    }
  }
}
const report = { generated_by: "scripts/report_school_source_coverage.js", schools: [...rows.values()].sort((a, b) => a.school.localeCompare(b.school)) };
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log("School\tWorks\tOn disk\tMissing\tDegraded\tCandidate-backed\tDownloaded quarantine\tNo candidate");
  for (const item of report.schools) console.log(`${item.school}\t${item.works}\t${item.public_on_disk}\t${item.missing}\t${item.degraded}\t${item.candidate_backed}\t${item.quarantine_downloaded}\t${item.no_candidate}`);
}
