#!/usr/bin/env node
/* Word-card meaning layer and fork display (docs/GITA_CARD_MEANING_SCHEMA.md).
   Pure markup checks against the real reader; layout is checked in-browser. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");

let card;
const context = {window: {scrollX: 0, scrollY: 0, innerHeight: 844}, document: {
  addEventListener() {}, documentElement: {clientWidth: 390}, body: {appendChild() {}}, querySelectorAll() {return [];},
  createElement() {
    card = {style: {}, setAttribute() {}, addEventListener() {}, getClientRects() {return [];}, matches() {return false;},
      contains(target) {return target === this;}, querySelectorAll() {return [];},
      getBoundingClientRect() {return {width: 300, height: 300};}};
    return card;
  }
}};
const source = fs.readFileSync(path.join(__dirname, "../assets/gita.js"), "utf8");
// Test-only access to the reader's own formatters; no production export added.
vm.runInNewContext(source.replace("window.GitaReader = {",
  "window.meaningTest = {showCard, showGroupCard, renderVerse, meaningPanelHtml, indexWordForks," +
  " setTermPolicy: p => { TERM_POLICY = p; }}; window.GitaReader = {"), context);
const t = context.window.meaningTest;
const anchor = {textContent: "x", dataset: {}, closest() {return null;}, getClientRects() {return [];},
  getBoundingClientRect() {return {left: 20, top: 400, bottom: 430, width: 80};}};
const cardHtml = w => { t.showCard(anchor, w); return card.innerHTML; };
const before = (html, a, b) => {
  const i = html.indexOf(a), j = html.indexOf(b);
  assert.ok(i >= 0 && j >= 0, `both ${a} and ${b} present`);
  return i < j;
};

t.setTermPolicy({
  bhakti: {senses: {devotee: {policy: "preserve", iast: "bhakta"}}},
  upasana: {senses: {"wait-upon": {policy: "translate", english: ["attend upon", "wait on"]}}},
});

const long = "a sense long enough that it cannot sit inside a three-hundred-pixel card without crowding the grammar above it, so it waits for the panel";
const word = {
  i: 1, iast: "paryupāsate", gloss: "attend upon", morph: "3rd pl. present",
  sandhi: "tvām + paryupāsate → tvāṃ paryupāsate (8.3.23)",
  term: {lemma: "upasana", sense: "wait-upon"},
  meaning: {
    image: "√ās 'to sit' with upa- 'near': to sit near, attend",
    lines: [
      {cat: "lexical", text: "to attend upon, wait on, serve", who: "Monier-Williams", locus: "sources/raw/kosha/mw.json#x"},
      {cat: "formation", text: "upa + √ās, ātmanepada"},
      {cat: "nirvacana", text: long, who: "Śaṅkara on 12.3"},
      {cat: "commentator", text: "dhyāyanti — they meditate", who: "Śaṅkara on 12.1"},
      {cat: "usage", text: "takes a sacrifice (4.25) as object", who: "Gītā"},
      {cat: "reception", text: "\"seek after\" <b>", who: "Sri Aurobindo"},
      {cat: "synthesis", text: "sitting near as service"},
      {cat: "policy-row", text: "PIPELINE VOCABULARY"},
    ],
    rendering: "attend upon",
    why: "keeps 'sit near' and 'serve'",
    alternatives: ["worship", "meditate on"],
  },
};
const plain = {i: 0, iast: "ye", gloss: "who", morph: "nom. pl. masc.", stem: "yad"};
const verse = {
  locus: "12.1", speaker: "arjuna", english: "{0:who} {1:attend upon}", words: [plain, word],
  forks: [
    {at: "pari", construals: [], followed: 0, reason: "INTERNAL REASON", open: false,
      words: [1], display: "pari can also mean 'to the exclusion of others'."},
    {at: "referent", construals: [], followed: 0, reason: "x", open: true,
      words: [0, 1], display: "The two accusatives can name one object or two."},
    {at: "order", construals: [], followed: 0, reason: "x", open: true, display: "The verse order admits a second reading."},
    {at: "no display", construals: [], followed: 0, reason: "HIDDEN OPEN", open: true, words: [1]},
  ],
};
t.indexWordForks([verse]);

// --- word card ---
const html = cardHtml(word);
assert.match(html, /<div class="wc-term">Rendered ‘attend upon’ throughout<\/div>/);
assert.ok(before(html, 'class="wc-mean"', 'class="wc-term"'), "term note follows the gloss");
assert.match(html, /sandhi: tvām \+ paryupāsate → tvāṃ paryupāsate \(8\.3\.23\)/);
assert.ok(before(html, 'class="wc-gram"', "wc-meaning"), "meaning follows grammar");
assert.match(html, /class="wm-image">√ās &#39;to sit&#39; with upa- &#39;near&#39;: to sit near, attend</);
assert.ok(before(html, "wm-image", "wm-lines"), "image is under grammar, above the list");
// Inline: the first three short lines in display order; the long one waits for the panel.
const inline = [...html.matchAll(/<span class="wm-cat">([^<]+)<\/span>/g)].map(m => m[1]);
assert.deepEqual(inline, ["Formation", "Dictionary", "Commentator"]);
assert.match(html, /Monier-Williams/);
assert.doesNotMatch(html, /cannot sit inside/);
assert.doesNotMatch(html, /mw\.json/, "loci are data, not card text");
assert.doesNotMatch(html, /PIPELINE VOCABULARY|policy-row/, "unknown categories are not shown");
assert.match(html, /<button class="wm-more" type="button" data-mwi="1" aria-haspopup="dialog">All meanings \(7\) →<\/button>/);
assert.match(html, /Also rendered: worship · meditate on/);
// Other readings: forks naming this card, with display, open or not.
assert.match(html, /Other readings/);
assert.match(html, /pari can also mean &#39;to the exclusion of others&#39;\./);
assert.match(html, /The two accusatives can name one object or two\./);
assert.doesNotMatch(html, /verse order admits/, "a fork without words stays off the card");
assert.doesNotMatch(html, /INTERNAL REASON|HIDDEN OPEN/);

const plainHtml = cardHtml(plain);
assert.match(plainHtml, /The two accusatives can name one object or two\./);
assert.doesNotMatch(plainHtml, /pari can also mean/);
assert.doesNotMatch(plainHtml, /wc-term|wc-meaning|wm-|sandhi:/);

const preserved = {i: 5, iast: "bhaktāḥ", gloss: "bhaktas", term: {lemma: "bhakti", sense: "devotee"}};
assert.match(cardHtml(preserved), /<div class="wc-term">Kept in Sanskrit across the Gītā<\/div>/);
const unknownTerm = {i: 6, iast: "x", gloss: "x", term: {lemma: "nope", sense: "none"}};
assert.doesNotMatch(cardHtml(unknownTerm), /wc-term/, "an unmatched term shows nothing");

// A short meaning needs no panel.
const short = {i: 7, iast: "y", gloss: "y", meaning: {lines: [{cat: "lexical", text: "short", who: "Apte"}]}};
const shortHtml = cardHtml(short);
assert.match(shortHtml, /Dictionary/);
assert.doesNotMatch(shortHtml, /wm-more|wm-image|Also rendered/);

// Group card carries the same layer for each word.
t.showGroupCard(anchor, [plain, word]);
assert.match(card.innerHTML, /wm-image/);
assert.match(card.innerHTML, /data-mwi="1"/);
assert.match(card.innerHTML, /sandhi: tvām/);

// --- panel ---
const panel = t.meaningPanelHtml(word);
assert.match(panel, /<button class="gp-x" type="button" aria-label="Close meanings">×<\/button>/);
assert.match(panel, /id="gpTerm"/);
const labels = [...panel.matchAll(/<span class="gp-school">([^<]+)<\/span>/g)].map(m => m[1]);
assert.deepEqual(labels, ["Formation", "Dictionary", "Etymology", "Commentator", "In the Gītā", "Translators", "This site’s reading"]);
assert.match(panel, /cannot sit inside/);
assert.match(panel, /&quot;seek after&quot; &lt;b&gt;/, "text is escaped");
assert.match(panel, /Why ‘attend upon’/);
assert.match(panel, /keeps &#39;sit near&#39; and &#39;serve&#39;/);
assert.match(panel, /Rendered ‘attend upon’ throughout/);
assert.match(panel, /pari can also mean/);
assert.doesNotMatch(panel, /PIPELINE VOCABULARY|mw\.json|INTERNAL REASON/);

// --- verse: open forks under the verse ---
const verseHtml = t.renderVerse(verse, {});
const block = /<details class="verse-readings">([\s\S]*?)<\/details>/.exec(verseHtml);
assert.ok(block, "open forks render a collapsible block");
assert.match(block[1], /<summary>Other readings \(2\)<\/summary>/);
assert.match(block[1], /The two accusatives can name one object or two\./);
assert.match(block[1], /The verse order admits a second reading\./);
assert.doesNotMatch(block[1], /pari can also mean/, "a settled fork is not listed under the verse");
assert.ok(before(verseHtml, 'class="ix"', "verse-readings"), "the block follows the verse text");

// --- graceful absence: the published readers without the new fields ---
for (const [dir, global] of [["sthitaprajna", "GITA_VERSES"], ["kama", "GITA3_VERSES"], ["ch5", "CH5_VERSES"], ["ch12", "CH12_VERSES"]]) {
  const sandbox = {window: {}};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, `../gita/${dir}/verses.js`), "utf8"), sandbox);
  const verses = sandbox.window[global];
  assert.ok(Array.isArray(verses) && verses.length, `${dir} verses load`);
  t.indexWordForks(verses);
  t.setTermPolicy(null);
  for (const v of verses) {
    const open = (v.forks || []).some(f => f.open && f.display);
    assert.equal(/verse-readings/.test(t.renderVerse(v, {})), open, `${dir} ${v.locus} readings block only for displayable open forks`);
    for (const w of v.words) {
      const h = cardHtml(w);
      if (!w.meaning) assert.doesNotMatch(h, /wc-meaning|wm-/, `${dir} ${w.iast}`);
      if (!w.sandhi) assert.doesNotMatch(h, /sandhi:/, `${dir} ${w.iast}`);
      assert.doesNotMatch(h, /wc-term/, `${dir} ${w.iast}: no term note without the policy`);
    }
  }
}
console.log("Meaning display: term, sandhi, meanings, panel and other readings render; absent fields add nothing.");
