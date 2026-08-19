#!/usr/bin/env node
/* Fetch an E-Bharatisampat public Unicode reader into raw quarantine. */
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const registry = JSON.parse(fs.readFileSync(path.join(ROOT, "data/editorial/source_candidates.json"), "utf8"));
const candidateId = process.argv[2];
if (!candidateId || process.argv.includes("--help")) {
  console.error("Usage: node scripts/fetch_ebharati_unicode_candidate.js <candidate-id>");
  process.exit(1);
}
const candidate = registry.candidates.find((item) => item.id === candidateId);
if (!candidate || candidate.provider !== "E-Bharatisampat" || !/public-unicode/i.test(candidate.access_kind || "")) {
  console.error("Candidate must be a registered E-Bharatisampat public-Unicode witness.");
  process.exit(1);
}
(async () => {
  const response = await fetch(candidate.candidate_url);
  if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`);
  const bytes = Buffer.from(await response.arrayBuffer());
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  if (!/[ऀ-ॿ]/u.test(text)) throw new Error("Reader response has no Devanāgarī signal.");
  const outputDir = path.join(ROOT, "data/sources/_intake/ebharati_unicode");
  const output = path.join(outputDir, `${candidate.id}.html`);
  if (fs.existsSync(output)) throw new Error(`Refusing to overwrite ${path.relative(ROOT, output)}`);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(output, bytes, { mode: 0o644 });
  console.log(JSON.stringify({ candidate_id: candidate.id, quarantine_path: path.relative(ROOT, output), bytes: bytes.length, sha256: crypto.createHash("sha256").update(bytes).digest("hex"), next: "Add this raw HTML file to a provenance sidecar; retain the source URL and separate page chrome before any review." }, null, 2));
})().catch((error) => { console.error(error.message); process.exitCode = 1; });
