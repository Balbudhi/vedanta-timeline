#!/usr/bin/env node
/* Confirm E-Bharatisampat raw HTML captures contain text payloads, not reader shells. */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "data/sources/_intake/ebharati_unicode");
const provenance = JSON.parse(fs.readFileSync(path.join(DIR, "PROVENANCE.json"), "utf8"));
let errors = 0;
for (const witness of provenance.witnesses || []) {
  const file = path.join(DIR, witness.path);
  const bytes = fs.readFileSync(file);
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  const hash = crypto.createHash("sha256").update(bytes).digest("hex");
  if (hash !== witness.sha256) { errors += 1; console.error(`${witness.candidate_id}: checksum mismatch`); }
  const devanagari = (text.match(/[\u0900-\u097f]/gu) || []).length;
  if (devanagari < 200 || !/<p\b[^>]*\bid=/i.test(text)) {
    errors += 1;
    console.error(`${witness.candidate_id}: reader shell or insufficient Devanāgarī payload`);
  }
}
console.log(`E-Bharatisampat Unicode intake: ${(provenance.witnesses || []).length} raw page(s); ${errors} error(s).`);
process.exitCode = errors ? 1 : 0;
