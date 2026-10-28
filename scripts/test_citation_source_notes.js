#!/usr/bin/env node
"use strict";

// Exercise the real citation callers, with DOM placement/event plumbing stubbed.
// This checks content and safety, not browser layout. Cases separate optional
// metadata, verification states, URL schemes, known/unknown authors, and callers.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "../assets/app.js"), "utf8");
const start = source.indexOf("function lookupCitationEntry(");
const end = source.indexOf("// Pull preceding/following key_passages", start);
const escapeStart = source.indexOf("function escape(s)");
const escapeEnd = source.indexOf("// Convert markdown emphasis", escapeStart);
assert.ok(start >= 0 && end > start && escapeStart >= 0);

let popup;
const element = () => ({
  innerHTML: "", style: {}, offsetHeight: 280, addEventListener() {}, remove() {},
  querySelector(selector) {
    return this.innerHTML.includes(selector.slice(1)) ? { addEventListener() {} } : null;
  },
  querySelectorAll() { return []; },
});
const panel = element();
const context = {
  URL, panelNavigationVersion: 0,
  state: { thinkersById: new Map(), citationIndex: { entries: {} } },
  dpCitationBody: panel,
  document: {
    createElement: element,
    querySelectorAll: () => [],
    body: { appendChild(el) { if (el.className === "citation-popover") popup = el; } },
    addEventListener() {}, removeEventListener() {},
  },
  window: { matchMedia: () => ({ matches: false }), innerHeight: 900, innerWidth: 1200 },
  popoverManager: { closeAll() {}, open() {} },
  setTimeout() {}, makePopoverDraggable() {},
  loadCitationIndex: async () => {},
  collectSurroundingPassages: () => ({ before: [], after: [] }),
  citationAbsenceMessage: () => "Missing source",
};
vm.createContext(context);
vm.runInContext(source.slice(escapeStart, escapeEnd), context);
context.md = context.escape;
context.mdVerse = context.escape;
vm.runInContext(source.slice(start, end), context);
const key = "outside-author/example-work/1";
const anchor = { getBoundingClientRect: () => ({ bottom: 120, top: 100, left: 100 }) };
async function render(entry) {
  context.state.citationIndex.entries = { [key]: entry };
  await context.openCitationPopover(key, anchor);
  context.renderCitationTab(key);
  return [popup.innerHTML, panel.innerHTML];
}

(async () => {
  const legacy = { verified: true, sanskrit_iast: "ātman", english_close: "The self." };
  for (const html of await render(legacy)) {
    assert.ok(html.includes("ātman") && html.includes("The self."), "literal content preserved");
    assert.ok(!html.includes("Interpretive source note") && !html.includes("Read source"), "absent optional metadata adds no content");
  }
  assert.ok(panel.innerHTML.includes("Verified source passage"), "literal panel retains its passage label");
  const entry = {
    verified: true,
    evidence_note: 'Interpretation <script>alert("x")</script> & not a quotation',
    notes: 'Witness <img src=x onerror="x"> & scope',
    source_url: "https://example.org/text?a=1&b=2",
    author_name: "Example <Author>", work_title: "Example & Work",
  };
  for (const html of await render(entry)) {
    assert.ok(html.includes("Interpretive source note"), "interpretation is explicitly labelled");
    assert.ok(html.includes("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &amp; not a quotation"));
    assert.ok(html.includes("Witness &lt;img src=x onerror=&quot;x&quot;&gt; &amp; scope"));
    assert.ok(!html.includes("<script>") && !html.includes("<img src=x"), "metadata is text, never markup");
    assert.ok(html.includes('href="https://example.org/text?a=1&amp;b=2"'), "safe source URL remains usable and escaped");
    assert.ok(html.includes("Read source"));
    assert.ok(html.includes("Example &lt;Author&gt;") && html.includes("Example &amp; Work"));
    assert.ok(!html.includes('data-thinker-id="outside-author"'), "unknown author has no broken thinker action");
    assert.ok(!html.includes("Literal English rendering"), "interpretation is never relabelled as translation");
    assert.ok(!html.includes("Verified source passage"), "metadata-only entry is not labelled a source quotation");
  }
  for (const verified of [false, "pending-acquisition", undefined]) {
    for (const html of await render({ ...entry, verified })) {
      assert.ok(!html.includes("Interpretive source note") && !html.includes("not a quotation"), `interpretation suppressed for ${verified}`);
      assert.ok(html.includes("Witness &lt;img"), "witness/scope notes remain inspectable");
    }
  }
  for (const source_url of ["javascript:alert(1)", "data:text/html,<script>x</script>", "//example.org/path", "/local", "mailto:x@example.org", "https://", ""]) {
    for (const html of await render({ verified: true, source_url })) {
      assert.ok(!html.includes("Read source") && !html.includes('href="'), `unsafe/nonabsolute URL omitted: ${source_url}`);
    }
  }
  for (const source_url of ["http://example.org/text", "https://example.org/text#part"]) {
    for (const html of await render({ verified: true, source_url })) assert.ok(html.includes("Read source"));
  }
  for (const html of await render({ ...legacy, notes: "Edition scope.", source_url: "https://example.org/edition" })) {
    assert.ok(html.includes("The self.") && html.includes("Edition scope.") && html.includes("Read source"), "literal entries also expose edition metadata");
    assert.ok(!html.includes("Interpretive source note"));
  }
  const englishOriginal = { verified: true, source_language: "English", original_text: "An original English statement.", english_close: "An original English statement." };
  for (const html of await render(englishOriginal)) {
    assert.ok(html.includes("Original English"), "English original is named as original");
    assert.equal(html.split(englishOriginal.original_text).length - 1, 1, "English original is not duplicated as a translation");
    assert.ok(!html.includes("Literal English rendering"), "original English is not a translation");
  }
  const bengaliOriginal = { verified: true, source_language: "Bengali", original_text: "মূল পাঠ", romanized_text: "Mūla pāṭha <img>", english_close: "Root text." };
  for (const html of await render(bengaliOriginal)) {
    assert.ok(html.includes("Original Bengali (romanized)"));
    assert.ok(html.includes("Mūla pāṭha &lt;img&gt;") && !html.includes("<img>"), "romanization is escaped");
    assert.ok(html.includes("Literal English rendering") && html.includes("Root text."));
  }
  for (const html of await render({ verified: true, source_language: "Other <language>", original_text: "Witness <text>" })) {
    assert.ok(html.includes("Original Other &lt;language&gt;") && html.includes("Witness &lt;text&gt;"));
  }
  for (const html of await render({ verified: true, source_language: "Bengali", original_text: "মূল পাঠ", english_close: "Root text." })) {
    assert.ok(html.includes("মূল পাঠ") && html.includes("Original Bengali") && !html.includes("(romanized)"));
    assert.ok(html.includes("Root text.") && html.includes("Literal English rendering"));
  }
  for (const html of await render({ verified: true, source_language: "English", original_text: "English only." })) {
    assert.equal(html.split("English only.").length - 1, 1);
    assert.ok(html.includes("Original English"));
  }
  assert.ok(panel.innerHTML.includes("Verified source passage"), "an original-only record is a verified source passage");
  for (const html of await render({ ...legacy, source_language: "Sanskrit", original_text: "SHOULD NOT DUPLICATE" })) {
    assert.ok(html.includes("ātman") && !html.includes("SHOULD NOT DUPLICATE"));
  }
  for (const verified of [false, "pending-acquisition", undefined]) {
    for (const html of await render({ verified, source_language: "Bengali", original_text: "WITHHELD ORIGINAL", romanized_text: "WITHHELD ROMANIZATION" })) {
      assert.ok(!html.includes("WITHHELD"), "new original fields require verified true");
    }
  }
  for (const html of await render({ verified: true, source_language: "Sanskrit", original_text: "LEGACY ORIGINAL ONLY" })) {
    assert.ok(!html.includes("LEGACY ORIGINAL ONLY"), "Sanskrit original-only legacy behavior is unchanged");
  }
  context.state.thinkersById.set("outside-author", {
    name_iast: "Known thinker", engaged_works: [{ work_id: "example-work", title_iast: "Known work" }],
  });
  for (const html of await render(entry)) {
    assert.ok(html.includes('data-thinker-id="outside-author"'), "known thinker action retained");
    assert.ok(html.includes("Known thinker") && html.includes("Known work"), "existing identity metadata retains priority");
  }
  let mobile = false;
  const routeCalls = [];
  context.isPanelMobile = () => mobile;
  let storageWrites = 0;
  context.localStorage = { setItem() { storageWrites++; } };
  context.panelState = { loaded: {} };
  context.showTab = (tab) => routeCalls.push(["tab", tab]);
  context.openPanel = (tab) => { context.panelState.open = true; routeCalls.push(["panel", tab]); };
  context.router = { push: (route) => routeCalls.push(["route", route.kind]) };
  context.state.citationIndex.entries = { [key]: englishOriginal };
  const articleAnchor = { ...anchor, closest: (selector) => selector === ".dp-article-body" ? {} : null };
  panel.innerHTML = "ARTICLE PANEL RETAINED";
  await context.openCitationPanel(key, articleAnchor);
  assert.equal(routeCalls.length, 0, "desktop article citation must not change tabs, panel or URL");
  assert.equal(panel.innerHTML, "ARTICLE PANEL RETAINED");
  assert.equal(storageWrites, 0, "article popover does not persist a replacement citation route");
  assert.ok(popup.innerHTML.includes("Original English"), "desktop article opens source popover");
  await context.openCitationPanel(key, anchor);
  assert.deepEqual(routeCalls, [["tab", "citation"], ["panel", "citation"], ["route", "citation"]], "ordinary desktop thinker citation keeps its panel route");
  routeCalls.length = 0;
  await context.openCitationPanel(key, null);
  assert.deepEqual(routeCalls, [["tab", "citation"], ["panel", "citation"], ["route", "citation"]], "desktop route restoration without an anchor retains the citation panel");
  routeCalls.length = 0; mobile = true;
  await context.openCitationPanel(key, anchor);
  assert.equal(routeCalls.length, 0, "mobile citation keeps its existing popover route");
  console.log("Citation source notes: both callers preserve literals, escape metadata, gate interpretation, validate URLs, and resolve author actions.");
})().catch(error => { console.error(error); process.exitCode = 1; });
