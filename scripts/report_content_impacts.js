#!/usr/bin/env node
/*
 * Given changed paths, show the public records that cite a changed witness.
 * It is a review notice, not an automatic rewrite: source acquisition can
 * reveal a need to revise a thinker, work, glossary term, or school reading,
 * but never authorizes the revision by itself.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const LEDGER = JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_ledger.json"), "utf8"));
const CITE_PATTERN = /cite:\/\/[^\s)\]>,]+/g;

function parseArgs(argv) {
  const paths = [];
  let json = false;
  for (const arg of argv) {
    if (arg === "--json") json = true;
    else if (arg === "--help" || arg === "-h") {
      console.log("Usage: node scripts/report_content_impacts.js [--json] [--changed repo/path ...]");
      process.exit(0);
    } else if (arg === "--changed") continue;
    else paths.push(arg.replace(/^\.\//, ""));
  }
  return { json, paths };
}
function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(file) : entry.name.endsWith(".json") ? [file] : [];
  });
}
function citations(value) {
  const found = new Set();
  const visit = (node) => {
    if (typeof node === "string") for (const match of node.matchAll(CITE_PATTERN)) found.add(match[0]);
    else if (Array.isArray(node)) node.forEach(visit);
    else if (node && typeof node === "object") Object.values(node).forEach(visit);
  };
  visit(value);
  return [...found];
}
function recordLabel(file, record) {
  if (file.includes(`${path.sep}thinkers${path.sep}`)) return `thinker:${record.id || path.basename(file, ".json")}`;
  if (file.includes(`${path.sep}glossary${path.sep}`)) return `term:${record.term_key || path.basename(file, ".json")}`;
  return path.relative(ROOT, file);
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const changed = new Set(options.paths);
  const sources = (LEDGER.sources || []).filter((source) => !changed.size || changed.has(source.source_path));
  const records = [...walk(path.join(ROOT, "data/thinkers")), ...walk(path.join(ROOT, "data/glossary"))]
    .map((file) => ({ file, record: JSON.parse(fs.readFileSync(file, "utf8")) }));
  const report = sources.map((source) => {
    const impacted = records.filter(({ record }) => citations(record).some((cite) =>
      (source.stable_cite_prefixes || []).some((prefix) => cite.startsWith(prefix))
    )).map(({ file, record }) => recordLabel(file, record));
    return { source_id: source.id, source_path: source.source_path, review_areas: source.review_areas || [], impacted_records: impacted.sort() };
  });
  if (options.json) console.log(JSON.stringify({ changed_paths: options.paths, impacts: report }, null, 2));
  else if (!report.length) console.log("No ledger source matches the supplied changed paths.");
  else for (const item of report) {
    console.log(`\n${item.source_id} (${item.source_path})`);
    console.log(`  review areas: ${item.review_areas.join(", ") || "none declared"}`);
    console.log(`  affected entries: ${item.impacted_records.join(", ") || "none found"}`);
  }
}

main();
