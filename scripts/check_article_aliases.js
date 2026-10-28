#!/usr/bin/env node
"use strict";

// Validate article-route ownership independently of picker visibility. An old
// bookmark is a direct alias of one entry, never another independent entry.
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const args = process.argv.slice(2);
const validArgs = args.length === 0 || (args.length === 2 && args[0] === "--manifest");
if (!validArgs) {
  console.error("Usage: node scripts/check_article_aliases.js [--manifest <path>]");
  process.exitCode = 1;
} else {
  const file = args.length ? path.resolve(args[1]) : path.join(root, "data/articles/manifest.json");
  try {
    const manifest = JSON.parse(fs.readFileSync(file, "utf8"));
    const errors = [];
    const validSlug = value => typeof value === "string" && value.length > 0 && !/[\s/?#]/.test(value);
    if (!manifest || !Array.isArray(manifest.articles)) {
      errors.push("articles must be an array");
    } else {
      const slugs = new Map();
      const aliases = new Map();
      // Collect every canonical slug first so collisions cannot depend on
      // whether an alias's owner appears before or after the other entry.
      manifest.articles.forEach((entry, index) => {
        if (!entry || typeof entry !== "object" || Array.isArray(entry)) {
          errors.push(`articles[${index}] must be an object`);
          return;
        }
        if (!validSlug(entry.slug)) {
          errors.push(`articles[${index}].slug must be a nonempty single route segment without whitespace`);
          return;
        }
        if (slugs.has(entry.slug)) {
          errors.push(`articles[${index}].slug duplicates "${entry.slug}" from articles[${slugs.get(entry.slug)}]`);
        } else {
          slugs.set(entry.slug, index);
        }
      });
      manifest.articles.forEach((entry, index) => {
        if (!entry || typeof entry !== "object" || Array.isArray(entry) || entry.aliases === undefined) return;
        if (!Array.isArray(entry.aliases)) {
          errors.push(`articles[${index}].aliases must be an array when present`);
          return;
        }
        entry.aliases.forEach((alias, aliasIndex) => {
          const location = `articles[${index}].aliases[${aliasIndex}]`;
          if (!validSlug(alias)) {
            errors.push(`${location} must be a nonempty single route segment without whitespace`);
            return;
          }
          if (slugs.has(alias)) {
            errors.push(`${location} "${alias}" conflicts with canonical articles[${slugs.get(alias)}].slug`);
          }
          if (aliases.has(alias)) {
            errors.push(`${location} "${alias}" duplicates ${aliases.get(alias)}`);
          } else {
            aliases.set(alias, location);
          }
        });
      });
      if (!errors.length) console.log(`Article aliases: ${manifest.articles.length} canonical entries, ${aliases.size} aliases; ownership valid.`);
    }
    if (errors.length) {
      console.error(`Invalid article manifest: ${file}`);
      errors.forEach(error => console.error("  " + error));
      process.exitCode = 1;
    }
  } catch (error) {
    console.error(`Could not validate article manifest ${file}: ${error.message}`);
    process.exitCode = 1;
  }
}
