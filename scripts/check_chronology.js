#!/usr/bin/env node
"use strict";

// Chronology foundation check. It executes the resolver copied from the live
// browser module (rather than a second implementation) and checks both its
// structured-data contract and every real legacy thinker record.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const appPath = path.join(ROOT, "assets/app.js");
const app = fs.readFileSync(appPath, "utf8");
const start = app.indexOf("const CHRONOLOGY_MODES =");
const end = app.indexOf("function setViewMode", start);
if (start < 0 || end < 0) throw new Error("Could not locate chronology resolver in assets/app.js.");

const context = {
  location: { search: "" },
  localStorage: { value: null, getItem() { return this.value; } },
  URLSearchParams,
};
vm.createContext(context);
vm.runInContext(`const CURRENT_YEAR = 2026; const state = { chronologyMode: null }; const chronologyToggle = null;\n${app.slice(start, end)}\nthis.resolve = resolveChronology; this.requested = requestedChronologyMode;`, context);

let failures = 0;
function check(condition, message) {
  if (condition) return;
  failures++;
  console.error(`FAIL: ${message}`);
}

// URL selection is intentionally stronger than an older local preference.
context.location.search = "?chronology=traditional";
context.localStorage.value = "academic";
check(context.requested() === "traditional", "URL chronology selection must override localStorage");
context.location.search = "?chronology=not-a-mode";
check(context.requested() === "academic", "valid localStorage chronology selection must be used when URL is invalid");

const academicTraditional = {
  dates_low: 100, dates_high: 200, dates_tier: "legacy-tier",
  chronology: {
    default_variant: "academic",
    variants: {
      academic: { low: 700, high: 750, tier: "consensus-textual", source_kind: "critical", notes: "Academic evidence." },
      traditional: { low: 788, high: 820, tier: "oral-tradition-only", source_kind: "hagiography", notes: "Traditional evidence." },
    },
  },
};
const traditional = context.resolve(academicTraditional, "traditional");
check(traditional.low === 788 && traditional.high === 820, "traditional mode must use its stored range");
check(traditional.tier === "oral-tradition-only" && traditional.sourceKind === "hagiography", "resolver must return selected variant metadata");
check(!traditional.availability.isFallback && traditional.availability.traditional, "available traditional range must not be marked fallback");

const missingTraditional = {
  dates_low: 700, dates_high: 750,
  chronology: { default_variant: "academic", variants: { academic: { low: 700, high: 750, tier: "consensus-textual" } } },
};
const fallback = context.resolve(missingTraditional, "traditional");
check(fallback.low === 700 && fallback.high === 750, "missing traditional variant must use an actual stored fallback range");
check(fallback.availability.isFallback && !fallback.availability.traditional && fallback.availability.effective === "academic", "missing traditional variant must be explicitly marked, never synthesized");

const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, "data/manifest.json"), "utf8"));
let legacyCount = 0;
let structuredCount = 0;
for (const filename of manifest.thinkers || []) {
  const filePath = path.join(ROOT, "data/thinkers", filename);
  check(fs.existsSync(filePath), `manifest thinker is missing: ${filename}`);
  if (!fs.existsSync(filePath)) continue;
  const thinker = JSON.parse(fs.readFileSync(filePath, "utf8"));
  if (thinker.chronology != null) {
    structuredCount++;
    const chronology = thinker.chronology;
    check(["academic", "traditional"].includes(chronology.default_variant), `${filename}: chronology.default_variant must be academic or traditional`);
    check(chronology.variants && typeof chronology.variants === "object", `${filename}: chronology.variants must be an object`);
    for (const [mode, variant] of Object.entries(chronology.variants || {})) {
      check(["academic", "traditional"].includes(mode), `${filename}: unsupported chronology variant ${mode}`);
      check(variant && typeof variant.low === "number", `${filename}: ${mode}.low must be numeric`);
      check(variant && (typeof variant.high === "number" || variant.high === null), `${filename}: ${mode}.high must be numeric or null`);
    }
  } else {
    legacyCount++;
    const resolved = context.resolve(thinker, "academic");
    if (typeof thinker.dates_low === "number") {
      check(resolved.low === thinker.dates_low && resolved.high === thinker.dates_high, `${filename}: legacy dates must resolve unchanged`);
      check(resolved.availability.legacy, `${filename}: legacy resolution must advertise its availability`);
    }
  }
}

if (failures) process.exit(1);
console.log(`Chronology check passed: ${legacyCount} legacy thinkers preserved; ${structuredCount} structured thinkers validated.`);
