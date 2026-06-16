#!/usr/bin/env node
/* Living-website coverage report.
 *
 * The corpus is meant to get richer as sources land: every primary text on disk
 * should eventually feed a bio, a glossary entry, or a translation. This script
 * is the signal that tells us where that hasn't happened yet — so understanding
 * keeps catching up to the sources. Read-only; informational by default, with a
 * --strict flag (for CI) that exits non-zero on actionable drift.
 *
 * It reports:
 *   1. UNUSED SOURCES   — files under data/sources/ that no bio / glossary /
 *                         citation references yet (have the text, not used).
 *   2. READY-BUT-HIDDEN — thinkers with display:false but entry_status "reviewed"
 *                         (ready entries whose display flag was never flipped on).
 *   3. UNGROUNDED        — thinkers whose engaged_works claim an on-disk source
 *                         but whose bio carries zero cite:// grounding.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");

// ---- small shared helpers -------------------------------------------------
const rel = (p) => path.relative(ROOT, p);
const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
function walk(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}
const SRC_RE = /data\/sources\/[A-Za-z0-9_./-]+?\.txt/g;
function sourcePathsIn(text) { return new Set((String(text).match(SRC_RE) || [])); }

// ---- inputs ---------------------------------------------------------------
const allSources = walk(path.join(ROOT, "data/sources"))
  .filter((p) => p.endsWith(".txt")).map(rel);

const thinkerFiles = readJSON(path.join(ROOT, "data/manifest.json")).thinkers || [];
const thinkers = thinkerFiles
  .map((f) => path.join(ROOT, "data/thinkers", f))
  .filter(fs.existsSync).map(readJSON);

// Sources counted as "used": referenced by a thinker bio, a glossary entry, the
// Gītā corpus, or a citation-index entry's `source` field.
const used = new Set();
const scanForSources = (obj) => sourcePathsIn(JSON.stringify(obj)).forEach((s) => used.add(s));
thinkers.forEach(scanForSources);
for (const f of walk(path.join(ROOT, "data/glossary"))) if (f.endsWith(".json")) scanForSources(readJSON(f));
for (const f of ["verses.js", "commentaries.js", "parallels.js"]) {
  const p = path.join(ROOT, "gita/sthitaprajna", f);
  if (fs.existsSync(p)) sourcePathsIn(fs.readFileSync(p, "utf8")).forEach((s) => used.add(s));
}
const citIdx = path.join(ROOT, "data/citation_index.json");
if (fs.existsSync(citIdx)) {
  const idx = readJSON(citIdx);
  for (const e of Object.values(idx.entries || {})) sourcePathsIn(e.source || "").forEach((s) => used.add(s));
}

// ---- 1. unused sources ----------------------------------------------------
const unused = allSources.filter((s) => !used.has(s));
const byTradition = {};
for (const s of unused) {
  const key = s.split("/").slice(2, 4).join("/"); // data/sources/<lang>/<group>
  (byTradition[key] = byTradition[key] || []).push(s.split("/").pop());
}

// ---- 2. ready-but-hidden --------------------------------------------------
const readyHidden = thinkers.filter((t) => t.display === false && /reviewed/.test(t.entry_status || ""));

// ---- 3. ungrounded despite on-disk sources --------------------------------
const ungrounded = thinkers.filter((t) => {
  const s = JSON.stringify(t);
  const hasOnDiskWork = (t.engaged_works || []).some((w) => /on-disk/.test(w.source_status || ""));
  return hasOnDiskWork && !/cite:\/\//.test(s);
});

// ---- report ---------------------------------------------------------------
console.log(`Sources on disk: ${allSources.length} | referenced: ${used.size} | UNUSED: ${unused.length}\n`);
console.log("== 1. UNUSED SOURCES (text on disk, not yet feeding a bio/glossary/translation) ==");
for (const k of Object.keys(byTradition).sort())
  console.log(`  ${k}  (${byTradition[k].length}): ${byTradition[k].slice(0, 6).join(", ")}${byTradition[k].length > 6 ? " …" : ""}`);

console.log(`\n== 2. READY BUT HIDDEN (entry_status reviewed, display:false — publish candidates) — ${readyHidden.length} ==`);
for (const t of readyHidden) console.log(`  ${t.id}`);

console.log(`\n== 3. UNGROUNDED (engaged_works on disk, but zero cite:// in the bio) — ${ungrounded.length} ==`);
for (const t of ungrounded.slice(0, 40)) console.log(`  ${t.id}`);
if (ungrounded.length > 40) console.log(`  … and ${ungrounded.length - 40} more`);

// strict mode (CI): ready-but-hidden is actionable drift; unused sources are a backlog signal, not a failure.
if (process.argv.includes("--strict") && readyHidden.length) {
  console.error(`\n${readyHidden.length} reviewed entr${readyHidden.length === 1 ? "y is" : "ies are"} hidden (display:false). Flip display or downgrade status.`);
  process.exit(1);
}
console.log("\nCoverage report complete.");
