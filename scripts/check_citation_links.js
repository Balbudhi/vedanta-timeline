#!/usr/bin/env node
"use strict";

// Verify that every cite:// reference in public authored data resolves through
// the citation index (direct entry or alias). This checks navigability and
// provenance linkage; it does not itself certify a claim's interpretation.

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
const strict = process.argv.includes("--strict");
const index = JSON.parse(fs.readFileSync(path.join(root, "data/citation_index.json"), "utf8"));
const targets = new Set(Object.keys(index.entries || {}));
for (const [alias, target] of Object.entries(index.aliases || {})) {
  if (targets.has(target)) targets.add(alias);
}

function walk(directory, output = []) {
  if (!fs.existsSync(directory)) return output;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(file, output);
    else if (/\.(json|md|js)$/i.test(entry.name)) output.push(file);
  }
  return output;
}

const roots = ["data/thinkers", "data/glossary", "data/articles/source", "data/perspectives/source", "data/full_translations"];
const dangling = [];
let references = 0;
for (const relative of roots) {
  for (const file of walk(path.join(root, relative))) {
    const text = fs.readFileSync(file, "utf8");
    const seen = new Set();
    for (const match of text.matchAll(/cite:\/\/([^\s\]\)"'<>,]+)/g)) {
      const key = match[1].replace(/[.,;:]+$/, "");
      if (seen.has(key)) continue;
      seen.add(key);
      references += 1;
      if (!targets.has(key)) dangling.push(`${path.relative(root, file)} → ${key}`);
    }
  }
}

console.log(`Citation-link check: ${references} unique file-level references, ${dangling.length} unresolved.`);
for (const item of dangling) console.error(`  ${item}`);
if (strict && dangling.length) process.exit(1);
