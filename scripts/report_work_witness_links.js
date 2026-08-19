#!/usr/bin/env node
/*
 * Audit explicit links between thinker work records and public source files.
 * A filename resemblance is a review hint only; source_paths is the evidence
 * field that lets an on-disk claim be mechanically audited.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const SOURCE_ROOT = path.join(ROOT, "data/sources");
const ON_DISK = /on-disk/;

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === "_intake") continue;
    const target = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(target, out);
    else if (entry.isFile()) out.push(path.relative(ROOT, target));
  }
  return out;
}
function key(value) {
  return String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/ś|ṣ/g, "s").replace(/ṅ|ñ|ṇ/g, "n").replace(/ṭ/g, "t").replace(/ḍ/g, "d")
    .replace(/ṛ|ṝ/g, "r").replace(/ḷ/g, "l").replace(/ṃ|ṁ/g, "m").replace(/ḥ/g, "h")
    .toLowerCase().replace(/[^a-z0-9]/g, "");
}
const sources = walk(SOURCE_ROOT);
const rows = [];
for (const name of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((item) => item.endsWith(".json"))) {
  const recordPath = path.join(ROOT, "data/thinkers", name);
  const thinker = JSON.parse(fs.readFileSync(recordPath, "utf8"));
  for (const work of thinker.engaged_works || []) {
    const declared = Array.isArray(work.source_paths) ? work.source_paths : [];
    const invalid = declared.filter((source) => !sources.includes(source));
    const thinkerKey = key(thinker.id);
    const workKeys = [work.work_id, work.title_iast, work.title].map(key).filter((value) => value.length >= 7);
    const hints = sources.filter((source) => {
      const sourceKey = key(path.basename(source, path.extname(source)));
      return sourceKey.includes(thinkerKey) && workKeys.some((workKey) => sourceKey.includes(workKey) || workKey.includes(sourceKey));
    });
    const onDisk = ON_DISK.test(work.source_status || "");
    let linkStatus = "not-applicable";
    if (declared.length && !invalid.length) linkStatus = "explicit-link-valid";
    else if (declared.length) linkStatus = "explicit-link-missing";
    else if (onDisk && hints.length) linkStatus = "needs-explicit-link; filename-hint";
    else if (onDisk) linkStatus = "needs-explicit-link; no-filename-hint";
    rows.push({ thinker_id: thinker.id, work_id: work.work_id, title_iast: work.title_iast || work.title || work.work_id,
      source_status: work.source_status || "unspecified", record_path: path.relative(ROOT, recordPath), source_paths: declared,
      invalid_source_paths: invalid, filename_hints: hints, link_status: linkStatus });
  }
}
const onDiskRows = rows.filter((row) => ON_DISK.test(row.source_status));
const report = {
  generated_by: "scripts/report_work_witness_links.js",
  on_disk_work_records: onDiskRows.length,
  explicit_links_valid: onDiskRows.filter((row) => row.link_status === "explicit-link-valid").length,
  needs_explicit_link: onDiskRows.filter((row) => row.link_status.startsWith("needs-explicit-link")).length,
  broken_explicit_links: onDiskRows.filter((row) => row.link_status === "explicit-link-missing").length,
  work_records: onDiskRows
};
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`On-disk work records: ${report.on_disk_work_records}`);
  console.log(`  explicit links valid: ${report.explicit_links_valid}`);
  console.log(`  needs explicit link: ${report.needs_explicit_link}`);
  console.log(`  broken explicit links: ${report.broken_explicit_links}`);
  for (const row of onDiskRows.filter((item) => item.link_status !== "explicit-link-valid"))
    console.log(`${row.thinker_id}\t${row.work_id}\t${row.link_status}\t${row.filename_hints.join(",")}`);
}
