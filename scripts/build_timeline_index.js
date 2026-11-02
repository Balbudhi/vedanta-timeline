#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const manifestPath = path.join(repoRoot, "data", "manifest.json");
const thinkersDir = path.join(repoRoot, "data", "thinkers");
const glossaryDir = path.join(repoRoot, "data", "glossary");

function option(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1]
    ? path.resolve(process.cwd(), process.argv[index + 1])
    : fallback;
}

const outputPath = option("--output", path.join(repoRoot, "data", "timeline_index.json"));
const glossaryOutputPath = option("--glossary-output", null);
const namesOutputPath = option("--names-output", null);

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function compactVariant(variant) {
  if (!variant || typeof variant !== "object") return undefined;
  const result = {};
  for (const key of ["low", "high", "tier", "source_kind", "publication_status"]) {
    if (Object.hasOwn(variant, key)) result[key] = variant[key];
  }
  return result;
}

function compactChronology(chronology) {
  if (!chronology || typeof chronology !== "object") return undefined;
  const variants = {};
  for (const [name, variant] of Object.entries(chronology.variants || {})) {
    variants[name] = compactVariant(variant);
  }
  return {
    default_variant: chronology.default_variant,
    traditional_status: chronology.traditional_status,
    variants,
  };
}

function compactThinker(thinker) {
  const result = {
    id: thinker.id,
    name: thinker.name,
    name_iast: thinker.name_iast,
    display: thinker.display,
    school_color_token: thinker.school_color_token,
    sub_school_shade: thinker.sub_school_shade,
    dates_low: thinker.dates_low,
    dates_high: thinker.dates_high,
    dates_tier: thinker.dates_tier,
    editorial_contract: thinker.editorial_contract,
    chronology: compactChronology(thinker.chronology),
    lineage_in: thinker.lineage_in || [],
    lineage_out: thinker.lineage_out || [],
    lineage_polemical: (thinker.lineage_polemical || []).map((relation) => ({
      thinker_id: relation.thinker_id,
      direction: relation.direction,
    })),
  };
  return Object.fromEntries(Object.entries(result).filter(([, value]) => value !== undefined));
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value)}\n`);
}

const manifest = readJson(manifestPath);
const seenIds = new Set();
const fullThinkers = (manifest.thinkers || []).map((filename) => {
  const thinker = readJson(path.join(thinkersDir, filename));
  if (!thinker.id) throw new Error(`${filename}: missing thinker id`);
  if (seenIds.has(thinker.id)) throw new Error(`${filename}: duplicate thinker id ${thinker.id}`);
  seenIds.add(thinker.id);
  return thinker;
});
const thinkers = fullThinkers.map(compactThinker);

writeJson(outputPath, { schema_version: 1, thinkers });
console.log(`wrote ${thinkers.length} timeline records to ${path.relative(repoRoot, outputPath)}`);

if (namesOutputPath) {
  const names = fullThinkers.filter(t => t.display !== false).map(t => ({
    id: t.id, name: t.name, name_iast: t.name_iast, alternate_names: t.alternate_names || [],
    school: t.school, school_color_token: t.school_color_token, sub_school: t.sub_school,
    engaged_works: (t.engaged_works || []).map(w => ({
      work_id: w.work_id, title: w.title, title_iast: w.title_iast,
      alternate_titles: w.alternate_titles || [],
    })),
  }));
  writeJson(namesOutputPath, { schema_version: 1, thinkers: names });
  console.log(`wrote ${names.length} name records to ${path.relative(repoRoot, namesOutputPath)}`);
}

if (glossaryOutputPath) {
  const glossaryManifest = readJson(path.join(glossaryDir, "manifest.json"));
  const terms = (glossaryManifest.terms || []).map((filename) =>
    readJson(path.join(glossaryDir, filename))
  );
  writeJson(glossaryOutputPath, { schema_version: 1, terms });
  console.log(`wrote ${terms.length} glossary records to ${path.relative(repoRoot, glossaryOutputPath)}`);
}
