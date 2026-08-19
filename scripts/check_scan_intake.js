#!/usr/bin/env node
/* Verify quarantine scan files remain present, PDFs, and byte-identical to provenance. */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "data/sources/_scan_intake");
let errors = 0;
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
    if (bytes.subarray(0, 4).toString("ascii") !== "%PDF") { errors += 1; console.error(`${witness.catalog_no || witness.path}: expected PDF`); }
    const hash = crypto.createHash("sha256").update(bytes).digest("hex");
    if (hash !== witness.sha256) { errors += 1; console.error(`${witness.catalog_no || witness.path}: checksum mismatch`); }
  }
}
console.log(`Scan intake: ${checked} scan witness(es); ${errors} error(s).`);
process.exitCode = errors ? 1 : 0;
