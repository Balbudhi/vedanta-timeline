#!/usr/bin/env node
/*
 * Enforces the opt-in v1 editorial contract.  Legacy content is intentionally
 * not rejected wholesale: a record becomes subject to the contract only when
 * it declares `editorial_contract: "v1"`.  This lets approved source batches
 * migrate safely while making every new standardized public claim traceable.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const LEDGER_PATH = path.join(ROOT, "data/editorial/source_ledger.json");
const CONTRACT_PATH = path.join(ROOT, "data/editorial/authoring_contract.json");
const CITATION_INDEX_PATH = path.join(ROOT, "data/citation_index.json");
const CITE = /^cite:\/\/[^\s)\]>,]+/;

function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8")); }
function jsonFiles(dir) {
  return fs.readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => path.join(dir, name));
}
function add(errors, label, message) { errors.push(`${label}: ${message}`); }
function isNonEmpty(value) { return typeof value === "string" && value.trim().length > 0; }

function validateClaim(claim, label, contract, prefixSet, citationIndex, errors, requireVerifiedWitness = false) {
  if (!claim || typeof claim !== "object" || Array.isArray(claim)) {
    add(errors, label, "claim must be an object"); return;
  }
  for (const key of contract.claim.required) if (!isNonEmpty(claim[key]) && !Array.isArray(claim[key])) add(errors, label, `missing ${key}`);
  if (!contract.claim.allowed_statuses.includes(claim.status)) add(errors, label, `unknown claim status ${JSON.stringify(claim.status)}`);
  const requiresCitation = claim.status !== "pending-acquisition" && claim.status !== "private-rights-restricted";
  if ((!Array.isArray(claim.citations) || claim.citations.length === 0) && requiresCitation) {
    add(errors, label, "requires at least one cite:// locus"); return;
  }
  for (const cite of claim.citations || []) {
    if (!isNonEmpty(cite) || !CITE.test(cite)) add(errors, label, `invalid citation ${JSON.stringify(cite)}`);
    else if (!prefixSet.some((prefix) => cite.startsWith(prefix))) add(errors, label, `citation is not covered by a ledger prefix: ${cite}`);
    else {
      const key = cite.replace(/^cite:\/\//, "");
      const alias = citationIndex.aliases && citationIndex.aliases[key];
      const citationEntry = citationIndex.entries && (citationIndex.entries[key] || (alias && citationIndex.entries[alias]));
      if (!citationEntry) {
        add(errors, label, `citation is not resolvable in data/citation_index.json: ${cite}`);
      } else if (requireVerifiedWitness && contract.claim.public_statuses.includes(claim.status) && citationEntry.verified !== true) {
        add(errors, label, `public claim needs a verified citation witness: ${cite}`);
      }
    }
  }
  if (contract.claim.public_statuses.includes(claim.status) && claim.evidence_level === "site-synthesis") {
    add(errors, label, "a public verified/disputed claim cannot use site-synthesis as its only evidence level");
  }
}

function validateEntry(file, type, ledgerIds, prefixSet, citationIndex, contract, errors) {
  const record = readJson(file);
  if (!(contract.supported_contracts || [contract.opt_in_value]).includes(record.editorial_contract)) return false;
  const label = path.relative(ROOT, file);
  const template = contract[`${type}_entry`];
  for (const key of template.required) {
    if (!Array.isArray(record[key]) || record[key].length === 0) add(errors, label, `v1 ${type} entry requires non-empty ${key}`);
  }
  for (const sourceId of record.source_record_ids || []) if (!ledgerIds.has(sourceId)) add(errors, label, `unknown source_record_id ${sourceId}`);
  const claimField = type === "thinker" ? "intro_claims" : "definition_claims";
  for (const [index, claim] of (record[claimField] || []).entries()) {
    validateClaim(claim, `${label} ${claimField}[${index}]`, contract, prefixSet, citationIndex, errors, record.editorial_contract === "v2");
  }
  if (record.editorial_contract === "v2") {
    for (const key of template.v2_required || []) {
      if (!record[key] || (Array.isArray(record[key]) && record[key].length === 0)) {
        add(errors, label, `v2 ${type} entry requires non-empty ${key}`);
      }
    }
    const sectionField = type === "thinker" ? "argument_sections" : "exposition_sections";
    const minimum = type === "thinker" ? template.minimum_argument_sections : template.minimum_exposition_sections;
    if (!Array.isArray(record[sectionField]) || record[sectionField].length < minimum) {
      add(errors, label, `v2 ${type} entry requires at least ${minimum} ${sectionField}`);
    }
    for (const [index, section] of (record[sectionField] || []).entries()) {
      const sectionLabel = `${label} ${sectionField}[${index}]`;
      if (!isNonEmpty(section?.id)) add(errors, sectionLabel, "missing id");
      if (!isNonEmpty(section?.title)) add(errors, sectionLabel, "missing title");
      if (!Array.isArray(section?.claims) || section.claims.length === 0) add(errors, sectionLabel, "requires claims");
      for (const [claimIndex, claim] of (section?.claims || []).entries()) {
        validateClaim(claim, `${sectionLabel}.claims[${claimIndex}]`, contract, prefixSet, citationIndex, errors, true);
      }
    }
    const legacyField = type === "thinker" ? "core_thesis" : "invariant_definition";
    const coverage = record.legacy_coverage && record.legacy_coverage[legacyField];
    if (!coverage || !["fully-migrated", "retained-below", "intentionally-omitted"].includes(coverage.status)) {
      add(errors, label, `v2 ${type} entry requires ${legacyField} legacy coverage status`);
    } else if (coverage.status === "fully-migrated" && (!Array.isArray(coverage.mapped_sections) || coverage.mapped_sections.length === 0)) {
      add(errors, label, `fully-migrated ${legacyField} requires mapped_sections`);
    } else if (coverage.status === "intentionally-omitted" && !isNonEmpty(coverage.reason)) {
      add(errors, label, `intentionally-omitted ${legacyField} requires reason`);
    }
    const dependencyAreas = record.editorial_dependencies?.review_areas;
    const updateEvents = record.editorial_dependencies?.update_when;
    if (!Array.isArray(dependencyAreas) || dependencyAreas.length === 0 || !dependencyAreas.every(isNonEmpty)) {
      add(errors, label, "v2 entry requires non-empty editorial_dependencies.review_areas");
    }
    if (!Array.isArray(updateEvents) || updateEvents.length === 0 || !updateEvents.every(isNonEmpty)) {
      add(errors, label, "v2 entry requires non-empty editorial_dependencies.update_when");
    }
  }
  return true;
}

function main() {
  const errors = [];
  const ledger = readJson(LEDGER_PATH);
  const contract = readJson(CONTRACT_PATH);
  const citationIndex = readJson(CITATION_INDEX_PATH);
  const ledgerIds = new Set();
  const prefixSet = [];
  for (const [index, source] of (ledger.sources || []).entries()) {
    const label = `source_ledger.sources[${index}]`;
    for (const key of contract.source_record.required) {
      if (!source[key] || (Array.isArray(source[key]) && source[key].length === 0)) add(errors, label, `missing ${key}`);
    }
    if (!isNonEmpty(source.id)) continue;
    if (ledgerIds.has(source.id)) add(errors, label, `duplicate id ${source.id}`);
    ledgerIds.add(source.id);
    const sourcePath = path.resolve(ROOT, source.source_path || "");
    if (!source.source_path || !sourcePath.startsWith(ROOT + path.sep) || !fs.existsSync(sourcePath)) add(errors, label, `source_path does not exist in repo: ${source.source_path}`);
    for (const prefix of source.stable_cite_prefixes || []) {
      if (!isNonEmpty(prefix) || !prefix.startsWith("cite://")) add(errors, label, `invalid stable cite prefix ${JSON.stringify(prefix)}`);
      else prefixSet.push(prefix);
    }
  }
  let optedIn = 0;
  for (const file of jsonFiles(path.join(ROOT, "data/thinkers"))) if (validateEntry(file, "thinker", ledgerIds, prefixSet, citationIndex, contract, errors)) optedIn += 1;
  for (const file of jsonFiles(path.join(ROOT, "data/glossary"))) if (validateEntry(file, "glossary", ledgerIds, prefixSet, citationIndex, contract, errors)) optedIn += 1;
  for (const error of errors) console.error(`ERROR: ${error}`);
  console.log(`Editorial contract: ${ledgerIds.size} source record(s); ${optedIn} opted-in public entry/entries checked.`);
  process.exitCode = errors.length ? 1 : 0;
}

main();
