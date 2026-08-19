#!/usr/bin/env node
/*
 * Match a local Muktabodha metadata export to currently missing/degraded
 * thinker works. It is a discovery report only: a match never promotes a
 * download or changes a thinker record.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const ACTIONABLE = new Set(["primary-text-not-in-corpus", "degraded-on-disk"]);
const metadataPath = process.argv[2];

if (!metadataPath || process.argv.includes("--help") || process.argv.includes("-h")) {
  console.error("Usage: node scripts/match_muktabodha_to_acquisition_queue.js <muktabodha_metadata.json> [--iast-root path] [--devanagari-root path] [--json]");
  process.exit(1);
}

function key(value) {
  return String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/ś|ṣ/g, "s").replace(/ṅ|ñ|ṇ/g, "n").replace(/ṭ/g, "t").replace(/ḍ/g, "d")
    .replace(/ṛ|ṝ/g, "r").replace(/ḷ/g, "l").replace(/ṃ|ṁ/g, "m").replace(/ḥ/g, "h")
    .toLowerCase().replace(/[^a-z0-9]/g, "");
}

function authorKeys(thinker) {
  return new Set([thinker.id, thinker.name, thinker.name_iast, ...(thinker.alternate_names || [])]
    .map(key).filter((value) => value.length >= 5));
}

function titleMatch(work, record) {
  const target = key(work.title_iast || work.title || work.work_id);
  const actual = key(record["Uniform title"] || record["Main title"]);
  if (target.length < 7 || actual.length < 7) return null;
  if (target === actual) return "exact-title";
  if (target.length >= 10 && actual.includes(target)) return "catalogue-title-contains-work";
  if (actual.length >= 10 && target.includes(actual)) return "work-title-contains-catalogue";
  return null;
}

function option(name) {
  const index = process.argv.indexOf(name);
  return index === -1 ? null : process.argv[index + 1] || null;
}

function directFiles(root) {
  if (!root || !fs.existsSync(root)) return [];
  return fs.readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isFile()).map((entry) => path.join(root, entry.name));
}

function fileSignal(file) {
  const bytes = fs.readFileSync(file);
  let validUtf8 = true;
  let text = "";
  try { text = new TextDecoder("utf-8", { fatal: true }).decode(bytes); }
  catch (_) { validUtf8 = false; }
  return { path: file, valid_utf8: validUtf8, replacement_characters: validUtf8 && text.includes("\uFFFD") };
}

const iastFiles = directFiles(option("--iast-root"));
const devanagariFiles = directFiles(option("--devanagari-root"));
function downloadedWitnesses(catalogNo) {
  const marker = new RegExp(`(^|[\\s-])${String(catalogNo).replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")}([\\s-]|$)`, "i");
  return {
    iast: iastFiles.filter((file) => marker.test(path.basename(file))).map(fileSignal),
    devanagari: devanagariFiles.filter((file) => marker.test(path.basename(file))).map(fileSignal)
  };
}

const metadata = Object.values(JSON.parse(fs.readFileSync(metadataPath, "utf8")));
const matches = [];
for (const name of fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((entry) => entry.endsWith(".json"))) {
  const thinker = JSON.parse(fs.readFileSync(path.join(ROOT, "data/thinkers", name), "utf8"));
  const names = authorKeys(thinker);
  for (const work of thinker.engaged_works || []) {
    if (!ACTIONABLE.has(work.source_status)) continue;
    for (const record of metadata) {
      if (!names.has(key(record.Author))) continue;
      const matchKind = titleMatch(work, record);
      if (!matchKind) continue;
      matches.push({
        thinker_id: thinker.id,
        school: thinker.school || "Unclassified",
        work_id: work.work_id,
        expected_title: work.title_iast || work.title || work.work_id,
        source_status: work.source_status,
        catalog_no: record["Catalog number"],
        catalog_title: record["Uniform title"] || record["Main title"],
        catalog_author: record.Author || null,
        traditions: record.Traditions || [],
        match_kind: matchKind,
        downloaded_witnesses: downloadedWitnesses(record["Catalog number"]),
        action: "inspect paired raw download, coverage, named edition, and sample loci before candidate registration"
      });
    }
  }
}
matches.sort((a, b) => a.thinker_id.localeCompare(b.thinker_id) || a.work_id.localeCompare(b.work_id) || a.catalog_no.localeCompare(b.catalog_no));
const report = {
  generated_by: "scripts/match_muktabodha_to_acquisition_queue.js",
  metadata_path: metadataPath,
  matches,
  note: "Strict author-and-title matches only. This is an intake worklist, not evidence that the witness is complete, clean, or citation-safe."
};
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Muktabodha strict acquisition matches: ${matches.length}`);
  for (const match of matches) console.log(`${match.thinker_id}\t${match.work_id}\t${match.catalog_no}\t${match.catalog_title}\t${match.match_kind}`);
}
