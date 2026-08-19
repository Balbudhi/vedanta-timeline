#!/usr/bin/env node
/*
 * Fetch a registered clean-digital Sanskrit candidate into quarantine.
 * It deliberately does not alter the candidate registry, manifest, or ledger.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const ROOT = path.resolve(__dirname, "..");
const CANDIDATES = JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8"));
async function main() {
  const candidateId = process.argv[2];
  if (!candidateId || process.argv.includes("--help")) throw new Error("Usage: node scripts/fetch_source_candidate.js <candidate-id>");
  const candidate = (CANDIDATES.candidates || []).find((item) => item.id === candidateId);
  if (!candidate) throw new Error(`Unknown candidate: ${candidateId}`);
  if (candidate.language !== "sanskrit") throw new Error("Only Sanskrit candidates are eligible for this intake command.");
  if (!/^https:\/\//.test(candidate.candidate_url)) throw new Error("Candidate URL must use HTTPS.");
  if (["blocked-rights", "rejected", "no-clean-digital-witness-found"].includes(candidate.acquisition_status)) throw new Error(`Candidate state does not permit retrieval: ${candidate.acquisition_status}`);
  const response = await fetch(candidate.candidate_url, { redirect: "follow" });
  if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`);
  const bytes = Buffer.from(await response.arrayBuffer());
  const prefix = bytes.subarray(0, 512).toString("utf8").trimStart();
  if (bytes.subarray(0, 4).toString("ascii") === "%PDF" || /^<!(doctype )?html/i.test(prefix) || /^<html/i.test(prefix)) throw new Error("Rejected non-text candidate response (PDF or HTML wrapper).");
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  if (text.includes("\uFFFD")) throw new Error("Rejected malformed UTF-8 candidate.");
  if (!/[\u0900-\u097Fāīūṛṝḷṅñṭḍṇśṣṃḥ]/u.test(text)) throw new Error("Rejected candidate with no Sanskrit-script or IAST signal.");
  const extension = /\.xml(?:$|\?)/i.test(candidate.candidate_url) ? "xml" : "txt";
  const dir = path.join(ROOT, "data/sources/_intake/candidates");
  fs.mkdirSync(dir, { recursive: true });
  const output = path.join(dir, `${candidate.id}.${extension}`);
  if (fs.existsSync(output)) throw new Error(`Refusing to overwrite existing quarantine file: ${path.relative(ROOT, output)}`);
  fs.writeFileSync(output, bytes, { mode: 0o644 });
  console.log(JSON.stringify({ candidate_id: candidate.id, quarantine_path: path.relative(ROOT, output), bytes: bytes.length, sha256: crypto.createHash("sha256").update(bytes).digest("hex"), next: "Inspect the header and record collation before promotion; this is not a manifest witness." }, null, 2));
}
main().catch((error) => { console.error(error.message); process.exitCode = 1; });
