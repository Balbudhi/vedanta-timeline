#!/usr/bin/env node
/*
 * Read-only audit of data/primary_text_manifest.json.
 *
 * This deliberately does not consult the citation index, thinker records, or
 * historical inventories.  It reports what the manifest itself can establish
 * about its own public witnesses, and fails only for manifest/path integrity
 * problems that make that report unreliable.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");
const DEFAULT_MANIFEST = "data/primary_text_manifest.json";
const TEXT_FORMATS = new Set([
  "plain-text",
  "html-visible-text-capture",
  "wikitext",
  "text-with-locus-marker",
  "web-transcription",
]);

function usage() {
  console.log("Usage: node scripts/check_source_inventory.js [--json] [--manifest <repo-relative-path>]");
}

function parseArgs(argv) {
  const options = { json: false, manifest: DEFAULT_MANIFEST };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--json") {
      options.json = true;
    } else if (arg === "--manifest") {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error("--manifest requires a path");
      options.manifest = value;
      index += 1;
    } else if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return options;
}

function isAbsolutePath(value) {
  // path.isAbsolute() is platform-specific. The manifest must stay portable,
  // so reject POSIX, Windows drive, UNC, and file-URL spellings everywhere.
  return (
    path.isAbsolute(value) ||
    /^[A-Za-z]:[\\/]/.test(value) ||
    /^\\\\/.test(value) ||
    /^file:/i.test(value)
  );
}

function isWithin(parent, child) {
  const relative = path.relative(parent, child);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
}

function label(record, index) {
  const title = typeof record.title === "string" && record.title.trim() ? record.title.trim() : "untitled";
  return `#${index + 1} (${title})`;
}

function classifyCitationStatus(status) {
  if (typeof status !== "string") return { declaredSafe: false, currentGrade: false };

  const declaredSafe = /\bcitation[- ]safe\b/i.test(status);
  // A statement that a witness becomes citation-safe only *after* comparison,
  // collation, or another future action is not a present citation-grade claim.
  const conditional = /\bcitation[- ]safe\b[\s\S]*\b(?:after|when|once|pending|if)\b/i.test(status);
  return { declaredSafe, currentGrade: declaredSafe && !conditional };
}

function countBy(records, selector) {
  const counts = new Map();
  for (const record of records) {
    const key = selector(record || {});
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort(([left], [right]) => left.localeCompare(right)));
}

function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    usage();
    process.exit(2);
  }

  const manifestPath = path.resolve(REPO_ROOT, options.manifest);
  if (!isWithin(REPO_ROOT, manifestPath)) {
    console.error("ERROR: --manifest must be inside the repository.");
    process.exit(2);
  }

  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch (error) {
    console.error(`ERROR: cannot read manifest ${path.relative(REPO_ROOT, manifestPath)}: ${error.message}`);
    process.exit(2);
  }

  const errors = [];
  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) {
    errors.push("manifest must be a JSON object");
  }
  if (!Array.isArray(manifest.files)) {
    errors.push("manifest.files must be an array");
  }
  if (typeof manifest.root !== "string" || !manifest.root.trim()) {
    errors.push("manifest.root must be a non-empty relative path");
  }
  if (errors.length) {
    for (const error of errors) console.error(`ERROR: ${error}`);
    process.exit(1);
  }

  const records = manifest.files;
  const sourceRoot = path.resolve(REPO_ROOT, manifest.root);
  if (isAbsolutePath(manifest.root) || !isWithin(REPO_ROOT, sourceRoot)) {
    errors.push(`manifest.root is not a repository-relative path: ${manifest.root}`);
  }

  const staleAbsolutePaths = [];
  const invalidRelativePaths = [];
  const missingFiles = [];
  const nonFiles = [];
  let inRepoFiles = 0;
  let textWitnesses = 0;
  let scanWitnesses = 0;
  let verificationMetadata = 0;
  let declaredCitationSafe = 0;
  let citationGrade = 0;
  let explicitVerified = 0;
  let verifiedFieldPresent = false;

  for (let index = 0; index < records.length; index += 1) {
    const record = records[index];
    if (!record || typeof record !== "object" || Array.isArray(record)) {
      errors.push(`${label({}, index)} is not an object`);
      continue;
    }

    if (typeof record.verification_status === "string" && record.verification_status.trim()) {
      verificationMetadata += 1;
      const citation = classifyCitationStatus(record.verification_status);
      if (citation.declaredSafe) declaredCitationSafe += 1;
      if (citation.currentGrade) citationGrade += 1;
    }
    if (Object.hasOwn(record, "verified")) {
      verifiedFieldPresent = true;
      if (record.verified === true) explicitVerified += 1;
    }

    if (typeof record.path !== "string" || !record.path.trim()) {
      errors.push(`${label(record, index)} has no non-empty path`);
      continue;
    }

    if (isAbsolutePath(record.path)) {
      staleAbsolutePaths.push({ record: label(record, index), path: record.path });
      continue;
    }

    const witnessPath = path.resolve(sourceRoot, record.path);
    if (!isWithin(sourceRoot, witnessPath)) {
      invalidRelativePaths.push({ record: label(record, index), path: record.path });
      continue;
    }

    try {
      const stat = fs.statSync(witnessPath);
      if (!stat.isFile()) {
        nonFiles.push({ record: label(record, index), path: record.path });
      } else {
        inRepoFiles += 1;
        if (TEXT_FORMATS.has(record.format)) textWitnesses += 1;
        if (record.format === "image-pdf-scan") scanWitnesses += 1;
      }
    } catch (error) {
      if (error.code === "ENOENT") {
        missingFiles.push({ record: label(record, index), path: record.path });
      } else {
        errors.push(`${label(record, index)} could not be inspected: ${error.message}`);
      }
    }

  }

  if (typeof manifest.file_count !== "number") {
    errors.push("manifest.file_count must be a number");
  } else if (manifest.file_count !== records.length) {
    errors.push(`manifest.file_count is ${manifest.file_count}, but files contains ${records.length} record(s)`);
  }

  const report = {
    manifest: path.relative(REPO_ROOT, manifestPath),
    manifestRecords: records.length,
    declaredFileCount: manifest.file_count,
    inRepoWitnessFiles: inRepoFiles,
    textWitnesses,
    imagePdfScanWitnesses: scanWitnesses,
    otherWitnessFormats: inRepoFiles - textWitnesses - scanWitnesses,
    verificationMetadataRecords: verificationMetadata,
    citationSafeDeclaredRecords: declaredCitationSafe,
    citationGradeRecords: citationGrade,
    explicitVerifiedRecords: verifiedFieldPresent ? explicitVerified : null,
    formats: countBy(records, (record) => record.format || "(missing)"),
    staleAbsolutePaths,
    invalidRelativePaths,
    missingFiles,
    nonFiles,
    errors,
  };

  if (options.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log("Source inventory report (manifest-only)");
    console.log(`Manifest: ${report.manifest}`);
    console.log("");
    console.log(`Manifest records: ${report.manifestRecords}`);
    console.log(`Declared file_count: ${report.declaredFileCount}`);
    console.log(`In-repo witness files: ${report.inRepoWitnessFiles}`);
    console.log(`Text-formatted witnesses: ${report.textWitnesses}`);
    console.log(`Image-PDF scan witnesses: ${report.imagePdfScanWitnesses}`);
    console.log(`Other witness formats: ${report.otherWitnessFormats}`);
    console.log("");
    console.log("Citation readiness (from verification_status only):");
    console.log(`  Records with verification metadata: ${report.verificationMetadataRecords}`);
    console.log(`  Records declaring a citation-safe condition: ${report.citationSafeDeclaredRecords}`);
    console.log(`  Records currently declared citation-grade: ${report.citationGradeRecords}`);
    console.log(
      `  Records with verified: true: ${report.explicitVerifiedRecords === null ? "not available (no verified field in manifest records)" : report.explicitVerifiedRecords}`,
    );
    console.log("");
    console.log("Formats:");
    for (const [format, count] of Object.entries(report.formats)) console.log(`  ${format}: ${count}`);

    const groups = [
      ["Stale absolute manifest paths", report.staleAbsolutePaths],
      ["Escaping relative manifest paths", report.invalidRelativePaths],
      ["Missing in-repo witness files", report.missingFiles],
      ["Manifest paths that are not files", report.nonFiles],
    ];
    for (const [heading, entries] of groups) {
      console.log(`\n${heading}: ${entries.length}`);
      for (const entry of entries) console.log(`  ${entry.record}: ${entry.path}`);
    }
    console.log(`\nIntegrity errors: ${report.errors.length}`);
    for (const error of report.errors) console.log(`  ${error}`);
  }

  if (staleAbsolutePaths.length) errors.push(`${staleAbsolutePaths.length} stale absolute manifest path(s)`);
  if (invalidRelativePaths.length) errors.push(`${invalidRelativePaths.length} escaping relative manifest path(s)`);
  if (missingFiles.length) errors.push(`${missingFiles.length} missing manifest witness file(s)`);
  if (nonFiles.length) errors.push(`${nonFiles.length} manifest path(s) that are not regular files`);

  if (errors.length) process.exit(1);
}

main();
