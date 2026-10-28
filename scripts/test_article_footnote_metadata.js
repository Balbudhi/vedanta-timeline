#!/usr/bin/env node
"use strict";

// Real footer, lookup, numbering, JSON loader and openArticle execute in a VM.
// DOM placement and Markdown parsing are outside this test's scope. The separate
// test_article_loading.js owns prompt display, DOM enrichment and navigation races.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const app = fs.readFileSync(path.join(__dirname, "../assets/app.js"), "utf8");
function section(start, end) {
  const a = app.indexOf(start), b = app.indexOf(end, a);
  assert.ok(a >= 0 && b > a, "real application section exists: " + start);
  return app.slice(a, b);
}
const code = [
  section("async function loadJSON(", "async function loadPrimitiveGraph("),
  section("async function loadCitationIndex(", "// Interpretations are distinct"),
  section("function escape(s)", "// Convert markdown emphasis"),
  section("function numberCitations(", "function renderMarkdownListBlock("),
  section("let panelNavigationVersion =", "// Markdown renderer for the article reader."),
].join("\n");
const { Element } = require('./test_helpers/article_dom');
function harness(index = null) {
  const context = {
    URL, location: { href: "https://example.org/" }, DATA_VERSION: "test",
    state: { thinkersById: new Map(), citationIndex: index },
    dpReaderMode: null, dpTabTitle: null, dpArticleHead: null,
    dpArticleBody: new Element(), window: {}, document: {},
    panelState: { loaded: {} }, router: { push() {} },
    SAHASRANAMA_READING: { slug: "sahasranama" }, GITA_READINGS: {},
    closeArticlesModal() {}, applyTabContext() {}, openPanel() { context.panelState.open = true; },
    renderMarkdownFull: text => text,
  };
  vm.createContext(context);
  vm.runInContext(code, context);
  return context;
}
function row(c, key = "new-author/new-work/new-locus") {
  return c.renderFootnoteList([{ idx: 1, key }]);
}
const failures = [];
async function test(name, run) {
  try { await run(); console.log("PASS " + name); }
  catch (e) { failures.push(name); console.error("FAIL " + name + "\n" + e.stack); }
}
(async () => {
  await test("citation prose cleanup preserves exact block and inline code spacing", () => {
    const c = harness();
    const block = '<pre><code class="language-text">F(x)    →    G(x)\n |            |\nF(y)    →    G(y)\n</code></pre>';
    const inline = '<code>x  +  y\t\t=  z</code>';
    const html = '<p>Ordinary  prose  (<a class="cite-link" href="cite://author/work/1">source</a>) , done.</p>'
      + block + '<p>Compare ' + inline + '  now.</p>';
    const result = c.numberCitations(html, { n: 0 });
    assert.ok(result.html.includes(block), "preformatted diagram is byte-for-byte preserved");
    assert.ok(result.html.includes(inline), "inline code retains intentional spaces and tabs");
    assert.ok(result.html.includes("Ordinary prose"), "prose whitespace still collapses");
    assert.ok(result.html.includes("</code> now."), "prose next to inline code still normalizes");
    assert.ok(result.html.includes('class="cite-fn"'), "prose citations are still numbered");
    assert.ok(!result.html.includes('(<sup') && !result.html.includes("</sup>)"),
      "orphan citation parentheses are still removed");
    assert.equal(result.footnotes.length, 1);
    assert.equal(result.footnotes[0].key, "author/work/1");
  });
  await test("entry metadata replaces slugs and remains escaped plain text", () => {
    const key = "new-author/new-work/new-locus";
    const c = harness({ entries: { [key]: {
      author_name: 'New <Author> & "voice"',
      work_title: "A <script>work</script>",
      locus: "Chapter <2> & appendix",
    } } });
    const html = row(c);
    assert.ok(html.includes('A &lt;script&gt;work&lt;/script&gt;'));
    assert.ok(html.includes("Chapter &lt;2&gt; &amp; appendix"));
    assert.ok(html.includes("New &lt;Author&gt; &amp; &quot;voice&quot;"));
    assert.ok(!html.includes("<script>"));
    assert.ok(!html.includes(">new-work</em>") && !html.includes(" — new-author"));
    c.state.thinkersById.set("new-author", {
      name_iast: " ", name: "", engaged_works: [{ work_id: "new-work", title_iast: " " }],
    });
    assert.ok(row(c).includes("New &lt;Author&gt;") && row(c).includes("A &lt;script&gt;"),
      "blank legacy fields do not hide nonempty entry metadata");
  });
  await test("known thinker and work retain priority; entry supplies precise locus", () => {
    const c = harness({ entries: { "known/work/key": {
      author_name: "Entry author", work_title: "Entry title", locus: "Book 3, verses 4–9",
    } } });
    c.state.thinkersById.set("known", {
      name_iast: "Known author", engaged_works: [{ work_id: "work", title_iast: "Known title" }],
    });
    const html = row(c, "known/work/key");
    assert.ok(html.includes("Known author") && html.includes("Known title"));
    assert.ok(html.includes("Book 3, verses 4–9"));
    assert.ok(!html.includes("Entry author") && !html.includes("Entry title"));
  });
  await test("missing, blank and nontext metadata preserve legacy fallbacks", () => {
    const c = harness({ entries: {
      "known/work/7": { author_name: " ", work_title: "", locus: " ", locus_short: 42 },
      "new-author/new-work/new-locus": { author_name: 42, work_title: {}, locus: [] },
    } });
    c.state.thinkersById.set("known", {
      name: "Legacy author", engaged_works: [{ work_id: "work", title: "Legacy title" }],
    });
    assert.ok(row(c, "known/work/7").includes("<em>Legacy title</em> 7"));
    assert.ok(row(c, "known/work/7").includes("Legacy author"));
    assert.ok(row(c).includes("<em>new-work</em> new-locus"));
    assert.ok(row(c, "absent/work/8").includes("<em>work</em> 8"));
    assert.equal(c.renderFootnoteList([]), "");
  });
  await test("aliases use the actual lookup and nonempty entry fallbacks", () => {
    const c = harness({ entries: { canonical: {
      author_name: "Resolved author", work_title: "Resolved work", locus: "", locus_short: "§ 12",
    } }, aliases: { "alias/work/code": "canonical" } });
    const html = row(c, "alias/work/code");
    assert.ok(html.includes("<em>Resolved work</em> § 12"));
    assert.ok(html.includes("Resolved author"));
    assert.ok(html.includes('href="cite://alias/work/code"'), "citation action retains its original key");
  });
  await test("actual metadata loader enriches footnote labels and caches successful data", async () => {
    const c = harness();
    const key = "eugenia-cheng/joy-of-abstraction/category-cheng";
    const index = JSON.parse(fs.readFileSync(path.join(__dirname, "../data/citation_index.json"), "utf8"));
    assert.equal(index.entries[key].author_name, "Eugenia Cheng");
    let release, loads = 0;
    const held = new Promise(resolve => { release = resolve; });
    c.fetch = async input => {
      if (String(input).includes("citation_index.json")) {
        loads++;
        await held;
        return { ok: true, json: async () => index };
      }
      return { ok: true, text: async () => '<p>Study <a class="cite-link" href="cite://' + key + '">source</a></p>' };
    };
    const opening = c.loadCitationIndex();
    try {
      await new Promise(setImmediate);
      assert.equal(loads, 1, "metadata consumer requests index");
      assert.ok(row(c, key).includes("<em>joy-of-abstraction</em>"), "complete fallback footer can render while metadata remains pending");
    } finally {
      release();
      await opening;
    }
    assert.ok(row(c, key).includes("The Joy of Abstraction"));
    assert.ok(row(c, key).includes("Eugenia Cheng"));
    assert.ok(row(c, key).includes(c.escape(index.entries[key].locus)));
    await c.loadCitationIndex();
    assert.equal(loads, 1, "the existing metadata cache is reused");
  });
  await test("uncited articles need no metadata request and unavailable metadata falls back", async () => {
    const c = harness();
    let indexLoads = 0;
    c.fetch = async input => {
      if (String(input).includes("citation_index.json")) {
        indexLoads++;
        return { ok: false };
      }
      return { ok: true, text: async () => "<p>Plain article.</p>" };
    };
    await c.openArticle({ slug: "plain", title: "Plain" });
    assert.equal(indexLoads, 0);
    assert.ok(c.dpArticleBody.innerHTML.includes("Plain article."));
    c.fetch = async input => {
      if (String(input).includes("citation_index.json")) {
        indexLoads++;
        return { ok: false };
      }
      return { ok: true, text: async () => '<p><a class="cite-link" href="cite://unknown/work/4">source</a></p>' };
    };
    await c.openArticle({ slug: "fallback", title: "Fallback" });
    assert.equal(indexLoads, 1);
    assert.ok(c.dpArticleBody.innerHTML.includes("<em>work</em> 4"));
    assert.ok(c.dpArticleBody.innerHTML.includes(" — unknown"));
  });
  if (failures.length) process.exitCode = 1;
})();
