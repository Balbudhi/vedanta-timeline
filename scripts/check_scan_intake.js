#!/usr/bin/env node
/* Verify quarantine scan files remain present, PDFs, and byte-identical to provenance.
 *
 * The scans are Git LFS objects.  A checkout that does not fetch LFS content --
 * CI, or a clone made with GIT_LFS_SKIP_SMUDGE -- leaves a ~130-byte pointer
 * file in place of each PDF.  Integrity is not checkable against a pointer, so
 * those are reported as skips rather than as 18 spurious failures. */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "data/sources/_scan_intake");
const LFS_POINTER = "version https://git-lfs.github.com/spec/v1";
let errors = 0;
let skipped = 0;
function walk(dir, out = []) { for (const entry of fs.readdirSync(dir, { withFileTypes: true })) { const target = path.join(dir, entry.name); if (entry.isDirectory()) walk(target, out); else if (entry.name === "PROVENANCE.json") out.push(target); } return out; }
let checked = 0;
for (const source of walk(DIR)) {
  const base = path.dirname(source);
  const provenance = JSON.parse(fs.readFileSync(source, "utf8"));
  for (const witness of provenance.witnesses || []) {
    checked += 1;
    const file = path.resolve(base, witness.path || "");
    if (!file.startsWith(base + path.sep) || !fs.existsSync(file)) { errors += 1; console.error(`${witness.catalog_no || witness.path}: missing scan`); continue; }
    const bytes = fs.readFileSync(file);
    const label = witness.catalog_no || witness.path;
    if (bytes.subarray(0, LFS_POINTER.length).toString("utf8") === LFS_POINTER) {
      skipped += 1;
      console.log(`${label}: Git LFS pointer, object not fetched — integrity not checkable here`);
      continue;
    }
    if (bytes.subarray(0, 4).toString("ascii") !== "%PDF") { errors += 1; console.error(`${label}: expected PDF`); }
    const hash = crypto.createHash("sha256").update(bytes).digest("hex");
    if (hash !== witness.sha256) { errors += 1; console.error(`${label}: checksum mismatch`); }
  }
}
console.log(`Scan intake: ${checked} scan witness(es); ${errors} error(s); ${skipped} skipped (LFS object not fetched).`);
process.exitCode = errors ? 1 : 0;
