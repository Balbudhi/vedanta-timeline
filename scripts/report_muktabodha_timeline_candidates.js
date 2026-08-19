#!/usr/bin/env node
/*
 * Identify Muktabodha catalogue records that could affect the thinker timeline.
 * This deliberately reports candidates; it never edits the roster.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const metadataPath = process.argv[2];
if (!metadataPath || process.argv.includes("--help")) {
  console.error("Usage: node scripts/report_muktabodha_timeline_candidates.js <muktabodha_metadata.json> [--tradition <label>] [--json]");
  process.exit(1);
}
function key(value) {
  return String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/ś|ṣ/g, "s").replace(/ṅ|ñ|ṇ/g, "n").replace(/ṭ/g, "t").replace(/ḍ/g, "d").replace(/ṛ|ṝ/g, "r").replace(/ḷ/g, "l").replace(/ṃ|ṁ/g, "m").replace(/ḥ/g, "h")
    .toLowerCase().replace(/[^a-z0-9]/g, "");
}
const roster = fs.readdirSync(path.join(ROOT, "data/thinkers")).filter((name) => name.endsWith(".json")).map((name) => JSON.parse(fs.readFileSync(path.join(ROOT, "data/thinkers", name), "utf8")));
const rosterKeys = new Set(roster.flatMap((thinker) => [thinker.id, thinker.name, thinker.name_iast, ...(thinker.alternate_names || [])].map(key)).filter(Boolean));
const data = JSON.parse(fs.readFileSync(metadataPath, "utf8"));
const traditionIndex = process.argv.indexOf("--tradition");
const tradition = traditionIndex === -1 ? null : process.argv[traditionIndex + 1] || null;
const ritual = /(paddhati|puja|pūjā|vidhi|arcana|diksa|dīkṣā|kavaca|mantra|stotra|stuti|nity|utsava|pratistha|pratiṣṭhā|homa|snana|snāna|vrata)/i;
const rows = Object.values(data).map((record) => {
  const author = String(record.Author || "").trim();
  const title = String(record["Uniform title"] || "").trim();
  const authorKnown = author && rosterKeys.has(key(author));
  const ritualOnly = ritual.test(`${title} ${record.Genre || ""} ${record.Description || ""}`);
  return {
    catalog_no: record["Catalog number"], title, author: author || null,
    traditions: record.Traditions || [], genre: record.Genre || null,
    source_description: record.Description || null,
    roster_status: !author ? "anonymous-or-unidentified" : authorKnown ? "existing-roster-match" : "named-author-needs-review",
    relevance: ritualOnly ? "ritual-library-only-until-shown-otherwise" : "potential-thinker-or-text-entry"
  };
});
const scopedRows = tradition ? rows.filter((row) => row.traditions.includes(tradition)) : rows;
const report = {
  generated_by: "scripts/report_muktabodha_timeline_candidates.js",
  tradition_filter: tradition,
  total_catalogue_records: scopedRows.length,
  named_nonritual_authors_not_in_roster: scopedRows.filter((row) => row.roster_status === "named-author-needs-review" && row.relevance === "potential-thinker-or-text-entry"),
  existing_thinker_texts: scopedRows.filter((row) => row.roster_status === "existing-roster-match" && row.relevance === "potential-thinker-or-text-entry"),
  ritual_or_anonymous_records: scopedRows.filter((row) => row.relevance !== "potential-thinker-or-text-entry" || row.roster_status === "anonymous-or-unidentified")
};
if (process.argv.includes("--json")) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Muktabodha timeline review${tradition ? ` (${tradition})` : ""}: ${report.total_catalogue_records} catalogue records.`);
  console.log(`Named non-ritual authors not in roster: ${report.named_nonritual_authors_not_in_roster.length}`);
  console.log(`Existing roster thinker texts: ${report.existing_thinker_texts.length}`);
  for (const row of report.named_nonritual_authors_not_in_roster) console.log(`${row.catalog_no}\t${row.author}\t${row.title}\t${row.traditions.join("; ")}`);
}
