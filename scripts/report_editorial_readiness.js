#!/usr/bin/env node
/*
 * Produces the worklist for an approved editorial batch. It reports concrete
 * missing inputs and migration state; it never licenses an automatic rewrite.
 */

"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");

function readDirectory(relative) {
  const dir = path.join(ROOT, relative);
  return fs.readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => ({
    path: `${relative}/${name}`,
    record: JSON.parse(fs.readFileSync(path.join(dir, name), "utf8")),
  }));
}

function main() {
  const json = process.argv.includes("--json");
  const thinkers = readDirectory("data/thinkers");
  const glossary = readDirectory("data/glossary");
  const textsNotInCorpus = [];
  for (const { path: file, record } of thinkers) {
    for (const work of record.engaged_works || []) {
      if (work.source_status === "primary-text-not-in-corpus") textsNotInCorpus.push({
        thinker_id: record.id,
        work_id: work.work_id,
        title_iast: work.title_iast || work.title || work.work_id,
        file,
      });
    }
  }
  const report = {
    generated_by: "scripts/report_editorial_readiness.js",
    profile_contract_migration: thinkers.filter(({ record }) => record.editorial_contract !== "v1").map(({ record, path: file }) => ({ id: record.id, file })),
    encyclopedia_contract_migration: glossary.filter(({ record }) => record.editorial_contract !== "v1").map(({ record, path: file }) => ({ term_key: record.term_key, file })),
    primary_texts_not_in_public_corpus: textsNotInCorpus,
  };
  if (json) return console.log(JSON.stringify(report, null, 2));
  console.log(`Profile records awaiting structured-contract migration: ${report.profile_contract_migration.length}`);
  console.log(`Encyclopedia records awaiting structured-contract migration: ${report.encyclopedia_contract_migration.length}`);
  console.log(`Named primary works not yet in the public corpus: ${report.primary_texts_not_in_public_corpus.length}`);
  console.log("Use --json for the exact batch lists. This is a review queue, not permission to auto-rewrite.");
}

main();
