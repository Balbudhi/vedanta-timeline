#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "assets/app.js"), "utf8");
function section(start, end) {
  const a = source.indexOf(start), b = source.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `application section exists: ${start}`);
  return source.slice(a, b);
}
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));
const thinkers = read("data/manifest.json").thinkers.map(f => read(`data/thinkers/${f}`));
const state = {
  thinkersById: new Map(thinkers.map(t => [t.id, t])),
  schools: read("data/registries/schools.json"), subSchools: read("data/registries/sub_schools.json"),
  glossary: new Map([
    ["atman", { term_key: "atman", term_iast: "ātman", aliases: ["Atma"], literal: "self" }],
    ["sneha", read("data/glossary/sneha.json")],
  ]),
  chronologyMode: "academic", glossaryRegex: null,
};
const escape = s => String(s ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll('"', "&quot;");
const context = { state, escape, md: escape, numberCitations: s => ({ html: s, footnotes: [] }),
  renderFootnoteList: () => "", resolveChronology: () => ({ availability: {} }),
  formatDatesLong: () => "1130–1300", chronologyModeLabel: x => x,
};
vm.createContext(context);
vm.runInContext([
  section("// ---------- name metadata", "function renderHero("),
  section("function renderHero(", "function renderLineageBlock("),
  section("function isModernCopyrightAuthor(", "function renderOrphanPassages("),
  section("function normalizeDia(", "// Topbar Glossary button:"),
].join("\n"), context);
const thinker = id => state.thinkersById.get(id);

// Expectations come from the recorded identities and the requested recognition
// flow, not from the rendering algorithm. A blanket parenthesis strip must fail.
let html = context.renderHero(thinker("nimbarka"));
assert.match(html, /class="school-pill">Svābhāvika-Bhedābheda \/ Dvaitādvaita<\/span>/);
assert.doesNotMatch(html, /Also called|class="name-aliases"/);
assert.match(html, /Niyamānanda/);
assert.doesNotMatch(html, /class="romanization"/);
assert.match(html, /<details[^>]*>[\s\S]*<summary>Names and classification<\/summary>/);
assert.match(context.renderHero(thinker("madhva")), /Ānandatīrtha/);
assert.match(context.renderHero(thinker("kesava-misra")), /Prācīna-Nyāya/);
assert.match(context.renderHero({ ...thinker("nimbarka"), sub_school: "School (reconstructed)", alternate_names: [] }), /School \(reconstructed\)/);
assert.doesNotMatch(context.renderHero(thinker("mallavadin")), /Malliṣena/);
assert.match(context.renderHero({ ...thinker("nimbarka"), alternate_names: ['<img src=x>', 'Name (contested)'] }), /&lt;img/);
assert.match(context.renderHero({ ...thinker("nimbarka"), alternate_names: ['Name (contested)'] }), /Name \(contested\)/);
state.schools.test = { display_name: "Advaita", aliases: ["Family alias"] };
assert.equal(context.schoolNames({ school_color_token: "test", sub_school: "Viśiṣṭādvaita" })
  .groups.map(g => g.join(" / ")).join(" · "), "Advaita / Family alias · Viśiṣṭādvaita",
  "a family alias stays with its family; Advaita is not a repeated whole word in Viśiṣṭādvaita");
state.schools.test = { display_name: "Advaita" };
assert.equal(context.schoolNames({ school_color_token: "test", sub_school: "Viśiṣṭādvaita" }).groups.length, 2);
delete state.schools.test;

const work = thinker("badarayana").engaged_works.find(w => w.work_id === "brahma-sutra");
assert.match(context.renderWorkCard(work, [], "badarayana"), /Vedānta-Sūtra/);
const v2 = context.renderWorkCard({ work_id: "test", title: "Test", alternate_titles: ["Other title"],
  __entryContract: "v2", summary: "WITHHELD SUMMARY", ascription_notes: "WITHHELD NOTE" }, [], "ramanuja");
assert.doesNotMatch(v2, /WITHHELD/);
assert.match(v2, /Other title/);
const qualified = context.renderWorkCard({ work_id: "test", title: "Test", reader_source_note: "Selected passages only.",
  source_status_note: "PRIVATE EDITORIAL INSTRUCTION" }, [], "nimbarka");
assert.match(qualified, /Selected passages only/);
assert.doesNotMatch(qualified, /PRIVATE EDITORIAL/);
const constituent = thinker("ramanuja").engaged_works.find(w => w.work_id === "gadya-trayam");
assert.doesNotMatch(context.renderWorkTitle(constituent), /Śaraṇāgati/);
assert.match(context.renderWorkNames(constituent), /Related titles/);

// The real build must produce discovery metadata independently of which thinker
// profiles have already been opened. Hidden thinkers must not become search hits.
const { execFileSync } = require("node:child_process");
const os = require("node:os");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "name-index-test-"));
try {
  execFileSync(process.execPath, ["scripts/build_timeline_index.js", "--output", path.join(tmp, "timeline.json"),
    "--names-output", path.join(tmp, "names.json")], { cwd: root });
  const data = JSON.parse(fs.readFileSync(path.join(tmp, "names.json")));
  context.installNameIndex(data);
  const results = q => context.rankSearchResults(q);
  assert.ok(results("dvaitadvaita").some(r => r.thinkerId === "nimbarka"));
  assert.equal(results("anandatirtha")[0].thinkerId, "madhva");
  assert.ok(results("vedanta sutra").some(r => r.thinkerId === "badarayana" && r.workId === "brahma-sutra"));
  assert.equal(results("atma")[0].kind, "term");
  assert.ok(results("tender love").some(r => r.canonical === "sneha"), "full glossary literals remain searchable beyond preview length");
  assert.ok(!results("Malliṣena").some(r => r.thinkerId === "mallavadin"));
  for (const t of thinkers.filter(t => t.display === false)) {
    assert.ok(!data.thinkers.some(x => x.id === t.id), `${t.id}: hidden entry stays hidden`);
  }
  assert.ok(data.thinkers.every(t => !Object.hasOwn(t, "core_thesis")), "index is compact metadata only");
} finally { fs.rmSync(tmp, { recursive: true, force: true }); }
console.log("name discovery: profile/work metadata, safety gates, generated corpus and alias search passed");
