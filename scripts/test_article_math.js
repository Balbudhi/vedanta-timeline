#!/usr/bin/env node
"use strict";

// Execute the actual Markdown and citation pipeline. No mock math renderer:
// final acceptance requires the locally vendored KaTeX referenced by index.html.
// This tests serialized HTML/MathML, not browser font loading or visual layout.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const app = fs.readFileSync(path.join(root, "assets/app.js"), "utf8");
const index = fs.readFileSync(path.join(root, "index.html"), "utf8");

function section(start, end) {
  const a = app.indexOf(start), b = app.indexOf(end, a);
  assert.ok(a >= 0 && b > a, "real application section exists: " + start);
  return app.slice(a, b);
}
const code = [
  section("// ---------- markdown helpers", "// The active chronology resolver"),
  section("// Markdown renderer for the article reader.", "// ---------- keyboard nav"),
].join("\n");

const vendorSources = [...index.matchAll(/<script\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi)]
  .map(m => m[1])
  .filter(src => /(?:^|\/)katex(?:\.min)?\.js(?:[?#]|$)/.test(src));
const vendorSource = vendorSources.find(src => !/^(?:https?:)?\/\//.test(src));
const vendorPath = process.env.KATEX_TEST_BUNDLE
  || (vendorSource && path.join(root, vendorSource.replace(/^\//, "").split(/[?#]/)[0]));
let katex = null;
let vendorError = null;
try {
  if (vendorPath) katex = require(path.resolve(vendorPath));
} catch (error) {
  vendorError = error;
}

function harness({ glossary = null, withoutKatex = false } = {}) {
  const context = { state: { glossaryRegex: glossary }, console };
  if (katex && !withoutKatex) context.katex = katex;
  context.window = context;
  vm.createContext(context);
  vm.runInContext(code, context);
  return context;
}

function render(source, options) {
  const context = harness(options);
  const before = context.renderMarkdownFull(source);
  const result = context.numberCitations(before, { n: 0 });
  return { before, html: result.html, footnotes: result.footnotes };
}

function decoded(text) {
  return text.replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#(?:39|x27);/g, "'").replace(/&amp;/g, "&");
}

function annotations(html) {
  return [...html.matchAll(/<annotation\b[^>]*encoding=["']application\/x-tex["'][^>]*>([\s\S]*?)<\/annotation>/g)]
    .map(m => decoded(m[1]).trim());
}

function assertMath(html, tex, count = 1) {
  assert.equal((html.match(/class="katex"/g) || []).length, count, "real KaTeX HTML subtree count");
  assert.ok(html.includes("katex-mathml") && html.includes("<math"), "accessible MathML accompanies visual HTML");
  assert.ok(annotations(html).includes(tex.trim()), "original TeX survives in MathML annotation");
}

// KaTeX roots contain nested spans. Match balanced span tags rather than a
// non-greedy regex that would inspect only the first child of the expression.
function mathSubtrees(html) {
  const results = [];
  const roots = /<span\b[^>]*class="katex"[^>]*>/g;
  let match;
  while ((match = roots.exec(html))) {
    const tags = /<span\b[^>]*>|<\/span>/g;
    tags.lastIndex = roots.lastIndex;
    let depth = 1, tag;
    while (depth && (tag = tags.exec(html))) depth += tag[0].startsWith("</") ? -1 : 1;
    assert.equal(depth, 0, "balanced KaTeX span subtree");
    results.push(html.slice(match.index, tags.lastIndex));
    roots.lastIndex = tags.lastIndex;
  }
  return results;
}

const failures = [];
let passes = 0;
function test(name, run) {
  try { run(); passes++; console.log("PASS " + name); }
  catch (error) { failures.push(name); console.error("FAIL " + name + "\n" + error.stack); }
}

test("current geometric-morphism code spans retain stars without crossed emphasis", () => {
  const source = "A right adjoint is written `f_*`. Thus `f⁎ ⊣ f_*`.";
  const { html } = render(source);
  assert.ok(html.includes("<code>f_*</code>"), "first literal star survives");
  assert.ok(html.includes("<code>f⁎ ⊣ f_*</code>"), "second literal star survives");
  assert.ok(!html.includes("<em>"), "two code stars do not become emphasis across spans");
});

test("inline code protects math delimiters, backslashes, stars and HTML characters", () => {
  const { html } = render('Literal `\\(f_* < g_*\\)` and `a  +  b` remain code.');
  assert.ok(html.includes("<code>\\(f_* &lt; g_*\\)</code>"));
  assert.ok(html.includes("<code>a  +  b</code>"));
  assert.equal(annotations(html).length, 0);
  assert.ok(!html.includes("<em>"));
});

test("fenced diagrams remain literal and byte-preserve intentional spacing", () => {
  const body = "\nF(x)    →    G(x)\n |            |\n\\(f_* < g_*\\)\n";
  const { html } = render("```" + body + "```\n\nAfter.");
  const block = html.match(/<pre><code[^>]*>([\s\S]*?)<\/code><\/pre>/);
  assert.ok(block, "code block remains a code block");
  assert.equal(decoded(block[1]), body);
  assert.equal(annotations(html).length, 0);
});

test("existing emphasis remains correct alongside literal underscore names", () => {
  const { html } = render("**Bold *nested* end** and *italic*. file_name remains literal.");
  assert.ok(html.includes("<strong>Bold <em>nested</em> end</strong>"));
  assert.ok(html.includes("<em>italic</em>"));
  assert.ok(html.includes("file_name"));
});

test("actual self-hosted KaTeX bundle is available and versioned", () => {
  assert.ok(katex, "missing real local KaTeX bundle" + (vendorError ? ": " + vendorError.message : ""));
  assert.equal(typeof katex.renderToString, "function");
  assert.match(katex.version, /^\d+\.\d+\.\d+/);
  assert.ok(process.env.KATEX_TEST_BUNDLE || vendorSource, "index.html references the local bundle");
  assert.ok(!vendorSources.some(src => /^(?:https?:)?\/\//.test(src)), "no remote KaTeX runtime dependency");
});

test("explicit inline notation renders actual subscripts and accessible MathML", () => {
  const tex = String.raw`f_{*}:E\to B_T`;
  const { html } = render("Before \\(" + tex + "\\) after.");
  assertMath(html, tex);
  assert.ok(html.includes("<msub>"), "subscripts are semantic math, not underscore replacement");
  assert.ok(!html.includes("katex-display"));
  assert.ok(html.includes("Before ") && html.includes(" after."));
});

test("multiline display math retains aligned rows and is not paragraph-wrapped", () => {
  const tex = String.raw`\begin{aligned}
\pi_M\circ h &= a \\
\pi_V\circ h &= b
\end{aligned}`;
  const { html } = render("Before.\n\n\\[\n" + tex + "\n\\]\n\nAfter.");
  assertMath(html, tex);
  assert.ok(html.includes('class="katex-display"'));
  assert.ok(!/<p>\s*(?:<[^>]+>\s*)*<span class="katex-display"/.test(html), "display expression is a block");
  assert.ok(html.includes("Before.") && html.includes("After."));
});

test("table math protects its internal vertical bar from cell splitting", () => {
  const tex = String.raw`\{x | P(x)\}`;
  const { html } = render("| Formula | Meaning |\n| --- | --- |\n| \\(" + tex + "\\) | selected elements |\n");
  assert.equal((html.match(/<td>/g) || []).length, 2, "math bar is not a third table cell");
  assertMath(html, tex);
  assert.ok(html.includes("selected elements"));
});

test("glossary tagging and citations affect prose without altering math", () => {
  const tex = String.raw`\operatorname{Brahman}(x)`;
  const { before, html, footnotes } = render(
    "Brahman \\(" + tex + "\\) [Source](cite://author/work/locus).",
    { glossary: /Brahman/g },
  );
  assertMath(html, tex);
  assert.equal((html.match(/data-term="Brahman"/g) || []).length, 1);
  assert.equal(footnotes.length, 1);
  assert.equal(footnotes[0].key, "author/work/locus");
  assert.deepEqual(mathSubtrees(html), mathSubtrees(before), "citation cleanup preserves complete math markup");
});

test("citation-like text and repeated spaces inside math remain literal", () => {
  const tex = String.raw`\text{a  b; [Source](cite://author/work/inside)}`;
  const { before, html, footnotes } = render("\\(" + tex + "\\) [Source](cite://author/work/outside)");
  assertMath(html, tex);
  assert.equal(footnotes.length, 1, "math source is not a second citation");
  assert.equal(footnotes[0].key, "author/work/outside");
  assert.deepEqual(mathSubtrees(html), mathSubtrees(before));
});

test("escaped and unmatched delimiters plus dollar currency stay ordinary text", () => {
  const { html } = render(String.raw`Literal \\(x_1\\), unmatched \(y_2, and $5 or $10.`);
  assert.equal(annotations(html).length, 0);
  assert.ok(html.includes("x_1") && html.includes("y_2"));
  assert.ok(html.includes("$5 or $10"));
});

test("math comparisons safely render less-than and ampersands", () => {
  const tex = String.raw`x_1 < x_2 \quad \text{A\&B}`;
  const { html } = render("\\(" + tex + "\\)");
  assertMath(html, tex);
  assert.ok(!html.includes("<x_2"));
});

test("invalid TeX leaves visible escaped source and following prose", () => {
  const tex = String.raw`\frac{1}{`;
  const { html } = render("Before \\(" + tex + "\\) after.");
  assert.ok(html.includes(tex), "invalid expression remains inspectable");
  assert.ok(html.includes("after."), "one invalid expression does not abort the article");
  assert.ok(html.includes("katex-error") || /math[^"<> ]*(?:error|fallback)|(?:error|fallback)[^"<> ]*math/.test(html), "invalid input is visibly marked as a fallback");
});

test("a missing math runtime degrades visibly without swallowing article text", () => {
  const { html } = render(String.raw`Before \(x_1\) after.`, { withoutKatex: true });
  assert.ok(html.includes("x_1") && html.includes("Before") && html.includes("after."));
  assert.equal(annotations(html).length, 0);
});

console.log(`${passes} passed; ${failures.length} failed`);
if (failures.length) process.exitCode = 1;
