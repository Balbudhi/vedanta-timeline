#!/usr/bin/env node
/*
 * Report every work whose current local witness is missing or degraded.
 * This is a worklist, not permission to scrape or promote a source.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const ACTIONABLE = new Set(["primary-text-not-in-corpus", "degraded-on-disk"]);
const candidates = JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8")).candidates || [];

function options(argv) {
  const result = { json: false, language: null, status: null };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--json") result.json = true;
    else if (value === "--language") result.language = argv[++index] || null;
    else if (value === "--status") result.status = argv[++index] || null;
    else if (value === "--help" || value === "-h") {
      console.log("Usage: node scripts/report_acquisition_queue.js [--json] [--language sanskrit] [--status missing|degraded]");
      process.exit(0);
    }
  }
  return result;
}

const rows = [];
for (const name of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((item) => item.endsWith(".json"))) {
  const file = path.join(ROOT, "data/thinkers", name);
  const thinker = JSON.parse(fs.readFileSync(file, "utf8"));
  for (const work of thinker.engaged_works || []) {
    if (!ACTIONABLE.has(work.source_status)) continue;
    const matches = candidates.filter((candidate) => candidate.thinker_id === thinker.id && candidate.work_id === work.work_id);
    rows.push({
      school: thinker.school || "Unclassified",
      thinker_id: thinker.id,
      work_id: work.work_id,
      title_iast: work.title_iast || work.title || work.work_id,
      language: work.language || "unspecified",
      source_status: work.source_status,
      ascription_tier: work.ascription_tier || "unspecified",
      entry_status: work.entry_status || "unspecified",
      record_path: path.relative(ROOT, file),
      candidate_ids: matches.map((candidate) => candidate.id),
      research_status: matches.length ? "candidate-found" : "no-clean-candidate-recorded",
    });
  }
}

const opts = options(process.argv.slice(2));
const filtered = rows.filter((row) =>
  (!opts.language || row.language === opts.language) &&
  (!opts.status || (opts.status === "missing" ? row.source_status === "primary-text-not-in-corpus" :
    opts.status === "degraded" ? row.source_status === "degraded-on-disk" : row.source_status === opts.status))
).sort((left, right) => left.school.localeCompare(right.school) || left.thinker_id.localeCompare(right.thinker_id) || left.work_id.localeCompare(right.work_id));

const report = {
  generated_by: "scripts/report_acquisition_queue.js",
  total: filtered.length,
  by_status: Object.fromEntries([...ACTIONABLE].map((status) => [status, filtered.filter((row) => row.source_status === status).length])),
  by_language: Object.fromEntries([...new Set(filtered.map((row) => row.language))].sort().map((language) => [language, filtered.filter((row) => row.language === language).length])),
  by_research_status: Object.fromEntries([...new Set(filtered.map((row) => row.research_status))].sort().map((status) => [status, filtered.filter((row) => row.research_status === status).length])),
  works: filtered,
};

if (opts.json) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Acquisition queue: ${report.total} work(s)`);
  for (const [status, count] of Object.entries(report.by_status)) console.log(`  ${status}: ${count}`);
  for (const work of report.works) console.log(`${work.school}\t${work.thinker_id}\t${work.work_id}\t${work.title_iast}\t${work.language}\t${work.source_status}\t${work.research_status}\t${work.candidate_ids.join(",")}`);
}
