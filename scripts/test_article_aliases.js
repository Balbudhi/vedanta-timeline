#!/usr/bin/env node
"use strict";

// Real route parsing/application, JSON loading, picker construction,
// openArticle, Markdown rendering, URL serialization and Share/PWA code.
// Network, clipboard and DOM operations are controlled boundaries. This is
// not browser layout/history-engine coverage or proof of content integration.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const app = fs.readFileSync(path.join(root, "assets/app.js"), "utf8");
const canonicalSlug = "vedanta-category-theory";
const oldSlug = "vedanta-category-research-plan";
const canonicalPath = "data/articles/source/vedanta-category-theory.md";

function section(start, end) {
  const a = app.indexOf(start), b = app.indexOf(end, a);
  assert.ok(a >= 0 && b > a, "real application section exists: " + start);
  return app.slice(a, b);
}
const code = [
  section("const DATA_VERSION =", "async function loadPrimitiveGraph("),
  section("// ---------- URL hash router", "function setUrlViewState("),
  section("function closePanel()", "function setPanelTab("),
  section("// ---------- markdown helpers", "// The active chronology resolver"),
  section("// ---------- articles -----------", 'articlesBtn.addEventListener("click"'),
  section("async function openArticle(", "// Markdown renderer for the article reader."),
  section("// Markdown renderer for the article reader.", "// ---------- keyboard nav"),
  section("async function copyCurrentViewUrl(", 'const dpFullscreenBtn ='),
  `globalThis.testApi = {
    router, ensureArticlesLoaded, openArticle, closePanel, restorePwaRoute,
    setArticles(value) { articlesManifest = value; },
    setPerspectives(value) { perspectivesManifest = value; }
  };`,
].join("\n");

function canonical() {
  return { slug: canonicalSlug, title: "Canonical unified course", kind: "methodology",
    source_doc: canonicalPath, aliases: [oldSlug] };
}
function fixture() {
  // A distractor comes first: silently choosing the first entry must fail.
  return { articles: [
    { slug: "unrelated", title: "Unrelated article", source_doc: "data/articles/source/unrelated.md" },
    canonical(),
  ] };
}
function deferred() {
  let resolve;
  const promise = new Promise(done => { resolve = done; });
  return { promise, resolve };
}
const settle = () => new Promise(resolve => setImmediate(resolve));

function element(tag = "div") {
  const classes = new Set(), handlers = new Map();
  let html = "";
  return {
    tag, handlers, children: [], dataset: {}, attributes: {}, textContent: "", hidden: false, scrollTop: 0,
    className: "", style: {},
    classList: { add: (...xs) => xs.forEach(x => classes.add(x)), remove: (...xs) => xs.forEach(x => classes.delete(x)), contains: x => classes.has(x) },
    get innerHTML() { return html; },
    set innerHTML(value) { html = value; this.children = []; },
    setAttribute(key, value) { this.attributes[key] = value; },
    appendChild(child) { this.children.push(child); },
    replaceChildren(...children) { this.children = children; },
    addEventListener(name, handler) { handlers.set(name, handler); },
  };
}

function harness({ manifest = fixture(), warm = false, holdManifest = false, bodyFails = false,
  installed = false, nativeShare = false, cancelShare = false } = {}) {
  const nodes = new Map();
  const node = id => {
    if (!nodes.has(id)) nodes.set(id, element());
    return nodes.get(id);
  };
  let current = new URL("https://example.test/site/?r=1" + (installed ? "&app=vedanta" : ""));
  const location = {
    get href() { return current.href; },
    get pathname() { return current.pathname; },
    get search() { return current.search; },
    get hash() { return current.hash; },
    set hash(value) { current.hash = value; },
  };
  const replacements = [], requests = [], copies = [], shares = [], openedThinkers = [];
  const saved = new Map();
  const manifestGate = deferred();
  let pendingManifest = holdManifest;
  const context = {
    URL, URLSearchParams, console, location,
    history: { length: 2, pushState(_state, _title, url) {
      this.length++; current = new URL(url, current);
    }, replaceState(_state, _title, url) {
      replacements.push(String(url)); current = new URL(url, current);
    } },
    localStorage: { getItem: key => saved.get(key) ?? null, setItem: (key, value) => saved.set(key, value), removeItem: key => saved.delete(key) },
    navigator: { clipboard: { writeText: async url => { copies.push(url); } } },
    document: { title: "Timeline", body: element("body"), getElementById: node,
      createElement: tag => element(tag), querySelectorAll: () => [] },
    window: { matchMedia: query => ({ matches: nativeShare && query === "(pointer: coarse)" }) },
    state: { glossaryRegex: null, activeId: null, thinkersById: new Map() },
    panelState: { open: false, loaded: {} },
    dpReaderMode: null, dpTabTitle: node("title"), dpArticleHead: node("head"), dpArticleBody: node("body"), detailPane: node("detailPane"),
    perspectivesManifest: null,
    SAHASRANAMA_READING: { slug: "sahasranama" }, GITA_READINGS: {},
    applyTabContext() {}, clearDetailPaneWidth() {}, setReadingMode() {},
    openPanel(tab) { context.panelState.open = true; context.panelState.activeTab = tab; },
    openThinker(id) { openedThinkers.push(id); context.state.activeId = id; context.panelState.activeTab = "thinker"; },
    openReader() {}, openCitationPanel() {},
    ensurePerspectivesLoaded: async () => { throw new Error("Unexpected cold perspective load in this harness"); },
    loadCitationIndex: async () => { throw new Error("Routing fixtures deliberately contain no citations"); },
    showReaderControlStatus(message) { context.controlStatus = message; },
    fetch: async input => {
      const url = new URL(String(input), location.href);
      requests.push(url.pathname);
      if (url.pathname.endsWith("/data/articles/manifest.json")) {
        if (pendingManifest) await manifestGate.promise;
        return { ok: true, json: async () => JSON.parse(JSON.stringify(manifest)) };
      }
      if (url.pathname.endsWith("/" + canonicalPath)) {
        return { ok: !bodyFails, text: async () => "# Unified fixture\n\nCanonical body marker." };
      }
      if (url.pathname.endsWith("/data/articles/source/unrelated.md")) {
        return { ok: true, text: async () => "Unrelated body marker." };
      }
      if (url.pathname.endsWith("/data/perspectives/source/separate.md")) {
        return { ok: true, text: async () => "Separate perspective marker." };
      }
      throw new Error("Unexpected fetch: " + url.pathname);
    },
  };
  if (nativeShare) context.navigator.share = async payload => {
    shares.push(payload);
    if (cancelShare) { const error = new Error("cancelled"); error.name = "AbortError"; throw error; }
  };
  vm.createContext(context);
  vm.runInContext(code, context);
  if (warm) context.testApi.setArticles(JSON.parse(JSON.stringify(manifest)));
  return {
    context, requests, replacements, copies, shares, saved, openedThinkers, node,
    releaseManifest() { pendingManifest = false; manifestGate.resolve(); },
    async navigate(hash) {
      location.hash = hash;
      context.testApi.router.apply(context.testApi.router.parse(location.hash));
      await settle();
    },
    async share() { await node("dpShare").handlers.get("click")(); },
  };
}

function assertCanonical(h) {
  assert.ok(h.context.dpArticleBody.innerHTML.includes("Canonical body marker."));
  assert.equal(h.context.dpTabTitle.textContent, "Canonical unified course");
  assert.equal(h.context.location.hash, "#/article/" + canonicalSlug);
  assert.ok(h.requests.some(url => url.endsWith("/" + canonicalPath)));
  assert.ok(!h.requests.some(url => url.includes("/source/" + oldSlug)), "never fetch the archive by its alias");
}

const failures = [];
let passes = 0;
async function test(name, run) {
  try { await run(); passes++; console.log("PASS " + name); }
  catch (error) { failures.push(name); console.error("FAIL " + name + "\n" + error.stack); }
}

(async () => {
  await test("warm alias runs real openArticle and normalizes its final URL", async () => {
    const h = harness({ warm: true });
    await h.navigate("#/article/" + oldSlug);
    assertCanonical(h);
    assert.ok(!h.requests.some(url => url.endsWith("/manifest.json")), "warm path uses the loaded manifest");
  });

  await test("cold bookmark waits for actual manifest loading then opens canonical source", async () => {
    const h = harness({ holdManifest: true });
    await h.navigate("#/article/" + oldSlug);
    assert.equal(h.requests.length, 1);
    assert.ok(h.requests[0].endsWith("/data/articles/manifest.json"));
    assert.ok(!h.context.dpArticleBody.innerHTML.includes("Canonical body marker."));
    h.releaseManifest(); await settle();
    assertCanonical(h);
  });

  await test("canonical slug continues to work through both warm and cold branches", async () => {
    for (const warm of [false, true]) {
      const h = harness({ warm });
      await h.navigate("#/article/" + canonicalSlug);
      assertCanonical(h);
      assert.equal(h.requests.filter(url => url.endsWith("/" + canonicalPath)).length, 1);
    }
  });

  await test("unknown and partial alias matches select no article", async () => {
    for (const slug of ["missing", oldSlug + "-extra", "category-research"]) {
      const h = harness({ warm: true });
      await h.navigate("#/article/" + slug);
      assert.equal(h.context.dpArticleBody.innerHTML, "");
      assert.equal(h.requests.length, 0);
      assert.equal(h.context.location.hash, "#/article/" + slug);
    }
  });

  await test("ambiguous aliases and canonical-slug collisions never select by manifest order", async () => {
    const collision = fixture();
    collision.articles[0].aliases = [oldSlug];
    for (const articles of [collision.articles, [...collision.articles].reverse()]) {
      const h = harness({ warm: true, manifest: { articles } });
      await h.navigate("#/article/" + oldSlug);
      assert.equal(h.context.dpArticleBody.innerHTML, "");
      assert.equal(h.requests.length, 0);
    }
    const overlap = fixture();
    overlap.articles[1].aliases.push("unrelated");
    const h = harness({ warm: true, manifest: overlap });
    await h.navigate("#/article/unrelated");
    assert.equal(h.context.dpArticleBody.innerHTML, "");
  });

  await test("malformed optional aliases cannot become substring matches or crash routing", async () => {
    for (const aliases of [oldSlug, null, {}, [42]]) {
      const manifest = fixture(); manifest.articles[1].aliases = aliases;
      const h = harness({ warm: true, manifest });
      await h.navigate("#/article/" + oldSlug);
      assert.equal(h.context.dpArticleBody.innerHTML, "");
    }
  });

  await test("actual picker renders one canonical course row and its handler loads that course", async () => {
    const h = harness();
    await h.context.testApi.ensureArticlesLoaded();
    const rows = h.node("articlesList").children.filter(child => child.className === "article-row");
    assert.equal(rows.filter(row => row.dataset.slug === canonicalSlug).length, 1);
    assert.equal(rows.filter(row => row.dataset.slug === oldSlug).length, 0);
    await rows.find(row => row.dataset.slug === canonicalSlug).handlers.get("click")();
    assertCanonical(h);
  });

  await test("canonical replacement preserves pathname/query, PWA state and clipboard Share", async () => {
    const h = harness({ installed: true });
    await h.navigate("#/article/" + oldSlug);
    assertCanonical(h);
    assert.equal(h.context.location.pathname, "/site/");
    assert.equal(h.context.location.search, "?r=1&app=vedanta");
    assert.equal(h.context.history.length, 2, "normalization replaces; it does not add a redirect entry");
    assert.equal(h.saved.get("vedanta:pwa:last-route:v1"), "#/article/" + canonicalSlug);
    await h.share();
    assert.equal(h.copies[0], h.context.location.href);
    assert.ok(h.copies[0].endsWith("#/article/" + canonicalSlug));
    const replacements = h.replacements.length;
    await h.navigate(h.context.location.hash);
    assert.equal(h.replacements.length, replacements, "reapplying canonical route does not normalize again");
  });

  await test("native Share uses canonical URL and cancellation never copies silently", async () => {
    const h = harness({ nativeShare: true, cancelShare: true });
    await h.navigate("#/article/" + oldSlug);
    assertCanonical(h);
    await h.share();
    assert.equal(h.shares.length, 1);
    assert.equal(h.shares[0].url, h.context.location.href);
    assert.equal(h.copies.length, 0);
  });

  await test("late manifest does not reopen an alias after a newer thinker route", async () => {
    for (const slug of [oldSlug, canonicalSlug]) {
      const h = harness({ holdManifest: true });
      await h.navigate("#/article/" + slug);
      await h.navigate("#/thinker/newer");
      h.releaseManifest(); await settle();
      assert.deepEqual(h.openedThinkers, ["newer"]);
      assert.equal(h.context.panelState.activeTab, "thinker", "stale " + slug);
      assert.equal(h.context.location.hash, "#/thinker/newer");
      assert.ok(!h.requests.some(url => url.endsWith("/" + canonicalPath)));
    }
  });

  await test("late manifest does not reopen the reader after actual closePanel", async () => {
    for (const slug of [oldSlug, canonicalSlug]) {
      const h = harness({ holdManifest: true });
      await h.navigate("#/article/" + slug);
      h.context.testApi.closePanel();
      h.releaseManifest(); await settle();
      assert.equal(h.context.panelState.open, false, "stale " + slug);
      assert.equal(h.context.location.hash, "");
      assert.ok(!h.requests.some(url => url.endsWith("/" + canonicalPath)));
    }
  });

  await test("failed canonical body does not fall back to archived companion", async () => {
    const h = harness({ bodyFails: true });
    await h.navigate("#/article/" + oldSlug);
    assert.ok(h.context.dpArticleBody.innerHTML.includes("Article body not yet uploaded."));
    assert.ok(!h.context.dpArticleBody.innerHTML.includes("Canonical body marker."));
    assert.ok(!h.requests.some(url => url.includes("/source/" + oldSlug)));
  });

  await test("unrelated article and separate perspective retain source and route kind", async () => {
    const h = harness({ warm: true });
    await h.navigate("#/article/unrelated");
    assert.ok(h.context.dpArticleBody.innerHTML.includes("Unrelated body marker."));
    h.context.testApi.setPerspectives({ perspectives: [{ slug: "separate", title: "Separate perspective" }] });
    await h.navigate("#/perspective/separate");
    assert.ok(h.context.dpArticleBody.innerHTML.includes("Separate perspective marker."));
    assert.equal(h.context.location.hash, "#/perspective/separate");
    assert.ok(h.context.dpArticleHead.innerHTML.includes("perspective-pill"));
  });

  await test("publication merge gate: actual manifest has one course and old bookmark alias", () => {
    const manifest = JSON.parse(fs.readFileSync(path.join(root, "data/articles/manifest.json"), "utf8"));
    const owners = manifest.articles.filter(entry => entry.slug === canonicalSlug);
    assert.equal(owners.length, 1);
    assert.equal(manifest.articles.filter(entry => entry.slug === oldSlug).length, 0,
      "pending content integration: do not keep an independent companion entry");
    assert.ok(Array.isArray(owners[0].aliases) && owners[0].aliases.includes(oldSlug));
    assert.equal(owners[0].source_doc, canonicalPath);
    assert.ok(fs.existsSync(path.join(root, canonicalPath)));
    // This only establishes manifest ownership, not that the content was merged.
  });

  console.log(`${passes} passed; ${failures.length} failed`);
  if (failures.length) process.exitCode = 1;
})();
