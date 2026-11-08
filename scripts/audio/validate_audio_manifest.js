#!/usr/bin/env node
"use strict";
// Validate a Gītā recitation manifest (gita/chN/audio.js) against the reader
// contract (assets/gita.js: src, reciter, attribution, verses[{locus,start,end}])
// and docs/AUDIO_ALIGNMENT_STANDARD.md (ascending, non-overlapping, honest
// timing_status).
//
//   node scripts/audio/validate_audio_manifest.js gita/ch12/audio.js \
//        --chapter 12 --verses 20 [--duration 293.04 | --mp3 gita/ch12/recitation.mp3]
//
// Without --duration the MP3 named by the manifest's `src` (next to audio.js, or
// --mp3) is probed with ffprobe. Exit code 0 on pass, 1 on failure.

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { spawnSync } = require("child_process");

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : dflt;
}

const file = process.argv[2];
if (!file) { console.error("usage: validate_audio_manifest.js audio.js --chapter N --verses M [--duration S|--mp3 FILE]"); process.exit(2); }
const chapter = arg("--chapter");
const verseCount = Number(arg("--verses"));
if (!chapter || !Number.isInteger(verseCount) || verseCount <= 0) { console.error("--chapter and --verses are required"); process.exit(2); }
const ffprobe = arg("--ffprobe", "/opt/homebrew/bin/ffprobe");

const errors = [];
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(file, "utf8"), sandbox);
const audioGlobal = Object.keys(sandbox.window).find((k) => /_AUDIO$/.test(k));
const m = audioGlobal ? sandbox.window[audioGlobal] : null;
if (!m || typeof m !== "object") { console.error("audio.js did not define a window.*_AUDIO manifest"); process.exit(1); }

for (const k of ["src", "reciter", "attribution", "licence", "source_url", "timing_status"]) {
  if (typeof m[k] !== "string" || !m[k].trim()) errors.push(`missing string field ${k}`);
}
if (!["provisional", "verified", "source-supplied"].includes(m.timing_status)) errors.push(`timing_status ${JSON.stringify(m.timing_status)} not one of provisional|verified|source-supplied`);
if (!m.method || typeof m.method !== "object") errors.push("missing method object");
else {
  for (const side of ["primary", "secondary"]) {
    const a = m.method[side];
    if (!a || !a.name || !a.licence) errors.push(`method.${side} needs name and licence`);
  }
}
const c = m.corroboration;
if (!c || typeof c !== "object") errors.push("missing corroboration");
else {
  if (c.verses_total !== verseCount) errors.push(`corroboration.verses_total ${c.verses_total} != ${verseCount}`);
  if (!Number.isInteger(c.corroborated) || c.corroborated < 0 || c.corroborated > verseCount) errors.push("corroboration.corroborated out of range");
  if (!Array.isArray(c.disagreements)) errors.push("corroboration.disagreements must be an array");
  else if (c.corroborated + c.disagreements.length !== verseCount) errors.push("corroborated + disagreements != verses_total");
}

// Duration of the published file.
let duration = arg("--duration") ? Number(arg("--duration")) : null;
if (duration === null) {
  const mp3 = arg("--mp3", path.join(path.dirname(file), m.src || ""));
  const r = spawnSync(ffprobe, ["-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", mp3], { encoding: "utf8" });
  if (r.status !== 0) errors.push(`ffprobe failed on ${mp3}: ${r.stderr.trim()}`);
  else duration = Number(r.stdout.trim());
}
if (!(duration > 0)) errors.push("could not determine mp3 duration");

// Segments.
const expected = Array.from({ length: verseCount }, (_, i) => `${chapter}.${i + 1}`);
if (!Array.isArray(m.verses)) errors.push("verses must be an array");
else {
  const loci = m.verses.map(v => v.locus);
  if (JSON.stringify(loci) !== JSON.stringify(expected)) errors.push(`loci are ${JSON.stringify(loci)}, expected ${chapter}.1..${chapter}.${verseCount} in order`);
  let prevEnd = -Infinity;
  for (const v of m.verses) {
    const ok = typeof v.start === "number" && typeof v.end === "number" && Number.isFinite(v.start) && Number.isFinite(v.end);
    if (!ok) { errors.push(`${v.locus}: start/end must be finite numbers`); continue; }
    if (v.start < 0) errors.push(`${v.locus}: start < 0`);
    if (v.end <= v.start) errors.push(`${v.locus}: end ${v.end} <= start ${v.start}`);
    if (v.start < prevEnd) errors.push(`${v.locus}: start ${v.start} overlaps previous end ${prevEnd}`);
    if (duration && v.end > duration + 1e-6) errors.push(`${v.locus}: end ${v.end} exceeds mp3 duration ${duration}`);
    prevEnd = v.end;
  }
  const words = m.verses.some(v => v.words || v.tokens);
  if (words) errors.push("public manifest must not carry word timings (standard: verse-level only)");
}

if (errors.length) {
  console.error(`FAIL ${file}`);
  for (const e of errors) console.error("  - " + e);
  process.exit(1);
}
console.log(`OK ${file}: ${m.verses.length} segments ${chapter}.1–${chapter}.${verseCount}, ` +
  `${m.verses[0].start}s–${m.verses[m.verses.length - 1].end}s within ${duration}s, ` +
  `timing_status=${m.timing_status}, corroborated ${c.corroborated}/${c.verses_total}`);
