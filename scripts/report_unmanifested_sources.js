#!/usr/bin/env node
"use strict";

// Read-only reverse inventory: public files under data/sources that are not
// represented in primary_text_manifest.json. They are candidates for metadata
// intake, not automatically citation-ready witnesses.

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "data/primary_text_manifest.json"), "utf8"));
const sourceRoot = path.resolve(root, manifest.root);
const ignoredNames = new Set([".DS_Store", "README.md"]);
const json = process.argv.includes("--json");

function walk(directory, out = []) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory() && entry.name !== "_intake") walk(absolute, out);
    else if (entry.isFile() && !ignoredNames.has(entry.name)) out.push(absolute);
  }
  return out;
}

const listed = new Set((manifest.files || []).map((record) => record && record.path).filter(Boolean));
const files = walk(sourceRoot).map((absolute) => path.relative(sourceRoot, absolute));
const unmanifested = files.filter((relative) => !listed.has(relative)).sort();

const report = {
  generated_by: "scripts/report_unmanifested_sources.js",
  source_files_on_disk: files.length,
  manifest_records: listed.size,
  unmanifested_files: unmanifested,
  note: "Quarantine intake is intentionally excluded. These records are candidates for metadata review, not citation-ready witnesses."
};
if (json) console.log(JSON.stringify(report, null, 2));
else {
  console.log("Unmanifested public-source report (informational)");
  console.log(`Source files on disk: ${files.length}`);
  console.log(`Manifest records: ${listed.size}`);
  console.log(`Unmanifested files: ${unmanifested.length}`);
  for (const relative of unmanifested) console.log(`  ${relative}`);
}
