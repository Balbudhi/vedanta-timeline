#!/usr/bin/env node
// Lifecycle regression using the actual app functions and controlled I/O ordering.
// DOM/layout and reader rendering are boundaries here; this is not browser visual QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(process.env.APP_SOURCE || path.join(__dirname, '../assets/app.js'), 'utf8');
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return {promise, resolve, reject}; };
const tick = async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); };
function extract(name) {
  const start = source.search(new RegExp(`(?:async )?function ${name}\\(`));
  assert.notEqual(start, -1, `missing production function ${name}`);
  return source.slice(start, source.indexOf('\n}', start) + 2);
}
const { Element } = require('./test_helpers/article_dom');
const element = (tag) => new Element(tag);

function harness() {
  const requests = [], scripts = [], readers = [], stopped = [];
  const body = element(), head = element(), detail = element(), mode = element();
  const panes = new Map(['thinker', 'article', 'translation', 'citation', 'source'].map(x => ['dpPane' + x[0].toUpperCase() + x.slice(1), element()]));
  const location = {pathname: '/', search: '?r=1', hash: ''};
  const c = {console, URL, URLSearchParams, Map, Promise, Error, DATA_VERSION: 'test',
    location, history: {replaceState(_, __, url) { location.hash = url.includes('#') ? url.slice(url.indexOf('#')) : ''; }},
    localStorage: {setItem() {}},
    sourceTabState: {activeCiteKey: null}, dpCitationBody: element(),
    isPanelMobile: () => false, loadCitationIndex: async () => {},
    renderCitationTab(key) { c.dpCitationBody.innerHTML = key; }, showTab() {},
    popoverManager: {closeAll() {}, open() {}, notifyClosed() {}},
    lookupCitationEntry: () => null, citationAbsenceMessage: () => 'Unavailable',
    makePopoverDraggable() {}, setTimeout(fn) { fn(); },
    state: {activeId: null, thinkersById: new Map([['T', {id: 'T'}]])},
    document: {body: element(), addEventListener() {}, removeEventListener() {}, querySelectorAll() { return []; }, getElementById(id) { return panes.get(id); },
      querySelector(selector) { return scripts.find(s => selector.includes(s.dataset.dyn) && !s.removed); },
      createElement: tag => element(tag),
      head: {appendChild(s) { scripts.push(s); }},
    },
    window: {matchMedia: () => ({matches: true}), GitaReader: {stopAudio() { stopped.push('gita'); }, render(root) { readers.push('gita'); root.innerHTML = 'GITA'; }, renderPassages(root) { readers.push('passages'); root.innerHTML += 'PASSAGES'; }},
      SahasranamaReader: {stopAudio() { stopped.push('sahasranama'); }, async render(root, opts) { readers.push('sahasranama'); root.innerHTML = 'SAHASRANAMA'; }}},
    dpArticleBody: body, dpArticleHead: head, dpReaderMode: mode, detailContent: detail,
    dpTabTitle: element(), dpTabBar: element(), detailPane: element(),
    panelState: {open: false, activeTab: 'thinker', loaded: {}},
    applyDetailPaneWidth() {}, clearDetailPaneWidth() {}, ensureSourceTreeRendered() {},
    setReadingMode() {}, closeArticlesModal() {}, rememberPwaRoute() {}, colorFor() {}, scrollDotIntoView() {},
    renderDetail() { return 'THINKER'; }, loadThinkerById: async () => ({id: 'T'}),
    escape: s => s, md: s => s, renderMarkdownFull: s => s,
    numberCitations: s => ({html: s, footnotes: []}), renderFootnoteList: () => '',
    linkifyGlossaryText() {}, gitaGlossaryResolve() {}, openGlossary() {},
    GITA_READINGS: {gita: {title: 'Gita', blurb: '', files: ['verses.js'], base: 'gita/', data: () => ({})}},
    SAHASRANAMA_READING: {slug: 'sahasranama', title: 'Sahasranama'},
    articlesManifest: null, perspectivesManifest: null,
    fetch(url) { const d = deferred(); requests.push({url, ...d}); return d.promise; },
  };
  c.ensureArticlesLoaded = async () => { c.articlesManifest = await (await c.fetch('manifest')).json(); };
  c.ensurePerspectivesLoaded = async () => { c.perspectivesManifest = await (await c.fetch('perspectives')).json(); };
  const functions = ['openPanel', 'closePanel', 'setPanelTab', 'applyTabContext', 'openThinker', 'loadScriptOnce', 'openGitaReading', 'openSahasranamaReading', 'openArticle', 'openCitationPanel', 'openCitationPopover'];
  // Include production lifecycle helpers when present, so pre-fix source remains runnable.
  for (const name of ['invalidateArticleLoad', 'isCurrentArticleLoad', 'showArticleLoadError', 'prepareArticle', 'openArticleBySlug', 'resolveArticleEntry', 'citationOriginal', 'renderCitationSourceNotes', 'enrichArticleFootnotes', 'footnoteMetadata']) {
    if (source.includes(`function ${name}(`)) functions.push(name);
  }
  const declarations = ['const PANEL_TABS = ["thinker", "translation", "article", "citation", "source"];'];
  for (const pattern of [/^let panelNavigationVersion = .*;$/m, /^const scriptLoads = .*;$/m]) {
    const m = source.match(pattern); if (m) declarations.push(m[0]);
  }
  const routerStart = source.indexOf('const router = {');
  const routerSource = source.slice(routerStart, source.indexOf('\n};', routerStart) + 3);
  vm.createContext(c);
  vm.runInContext(declarations.join('\n') + '\n' + functions.map(extract).join('\n') + '\n' + routerSource + '\nthis.router = router;', c);
  return {c, body, head, detail, scripts, readers, stopped, requests,
    activateTab(tab) {
      const button = element(); button.dataset.pane = tab;
      c.dpTabBar.querySelectorAll = () => [button];
      const start = source.indexOf('\nif (dpTabBar) {');
      vm.runInContext(source.slice(start, source.indexOf('\n}', start) + 2), c);
      button.emit('click');
    },
    respond(i, text) { requests[i].resolve({ok: true, text: async () => text, json: async () => text}); }};
}
const article = (slug, extra = {}) => ({slug, title: slug.toUpperCase(), ...extra});
const tests = [];
function test(name, fn) { tests.push([name, fn]); }
// Interleavings: body completion, response.text completion, navigation, manifest,
// script execution, passage/include completion, and renderer completion.
test('A → B: late body cannot overwrite B or its URL', async () => {
  const h = harness(); const a = h.c.openArticle(article('a')); const b = h.c.openArticle(article('b'));
  h.respond(1, 'BODY B'); await b; h.respond(0, 'BODY A'); await a;
  assert.match(h.body.innerHTML, /BODY B/); assert.equal(h.c.location.hash, '#/article/b');
});
test('A → thinker: late article cannot overwrite title, body or URL', async () => {
  const h = harness(); const a = h.c.openArticle(article('a')); await h.c.openThinker('T');
  const previous = h.body.innerHTML; h.respond(0, 'BODY A'); await a;
  assert.equal(h.body.innerHTML, previous); assert.equal(h.c.panelState.activeTab, 'thinker'); assert.equal(h.c.location.hash, '#/thinker/T');
});
test('close while response text is pending prevents later adoption', async () => {
  const h = harness(), text = deferred(); const a = h.c.openArticle(article('a'));
  h.requests[0].resolve({ok: true, text: () => text.promise}); await tick(); h.c.closePanel();
  const previous = h.body.innerHTML; text.resolve('LATE'); await a;
  assert.equal(h.body.innerHTML, previous); assert.equal(h.c.location.hash, ''); assert.equal(h.c.panelState.loaded.article, false);
});
test('late route manifest cannot reopen a closed panel', async () => {
  const h = harness(); h.c.router.apply({kind: 'article', slug: 'a'}); h.c.closePanel();
  h.respond(0, {articles: [article('a')]}); await tick();
  assert.equal(h.requests.length, 1); assert.equal(h.c.panelState.open, false);
});
test('late route manifest cannot replace a newer article', async () => {
  const h = harness(); h.c.router.apply({kind: 'article', slug: 'a'});
  const b = h.c.openArticle(article('b')); h.respond(1, 'BODY B'); await b;
  h.respond(0, {articles: [article('a')]}); await tick();
  assert.equal(h.requests.length, 2); assert.match(h.body.innerHTML, /BODY B/);
});
test('concurrent callers await actual script execution; failure is retryable', async () => {
  const h = harness(); let completed = 0;
  const a = h.c.loadScriptOnce('reader.js').then(() => completed++);
  const b = h.c.loadScriptOnce('reader.js').then(() => completed++);
  await tick(); assert.equal(completed, 0); assert.equal(h.scripts.length, 1);
  h.scripts[0].onload(); await Promise.all([a, b]); assert.equal(completed, 2);
  const failed = h.c.loadScriptOnce('retry.js'); h.scripts[1].onerror(); await assert.rejects(failed);
  const retry = h.c.loadScriptOnce('retry.js'); assert.equal(h.scripts.length, 3); h.scripts[2].onload(); await retry;
});
test('closed reading does not mount after delayed script', async () => {
  const h = harness(); const a = h.c.openArticle(article('a', {interactive: 'gita'}));
  h.c.closePanel(); h.scripts[0].onload(); await tick();
  for (const script of h.scripts.slice(1)) script.onload(); await a;
  assert.deepEqual(h.readers, []); assert.equal(h.c.location.hash, '');
});
test('late passage includes cannot mount in a replacement article', async () => {
  const h = harness(); const a = h.c.openArticle(article('a', {passages_doc: 'passages'}));
  h.respond(0, 'BODY A'); await tick(); h.respond(1, {passages: [], includes: ['include']}); await tick();
  const b = h.c.openArticle(article('b')); h.respond(3, 'BODY B'); await b;
  h.respond(2, {passages: [{id: 'old'}]}); await tick();
  for (const script of h.scripts) script.onload(); await a;
  assert.deepEqual(h.readers, []); assert.match(h.body.innerHTML, /BODY B/);
});
test('network failure offers a working retry', async () => {
  const h = harness(); h.body.retry = element(); const a = h.c.openArticle(article('a'));
  h.requests[0].reject(new Error('offline')); await a;
  assert.match(h.body.innerHTML, /could not|couldn.t/i); assert.match(h.body.innerHTML, /retry/i);
  h.body.querySelector('[data-article-retry]').emit('click'); await tick(); h.respond(1, 'RECOVERED'); await tick();
  assert.match(h.body.innerHTML, /RECOVERED/); assert.equal(h.c.panelState.loaded.article, true);
});
test('completed article survives temporary tab switching and close stops readers', async () => {
  const h = harness(); const a = h.c.openArticle(article('a')); h.respond(0, 'BODY A'); await a;
  h.c.setPanelTab('citation'); h.c.setPanelTab('article'); assert.match(h.body.innerHTML, /BODY A/);
  const before = h.stopped.length; h.c.closePanel(); assert.equal(h.stopped.length, before + 2);
});
test('a valid delayed manifest opens the requested article', async () => {
  const h = harness(); h.c.location.hash = '#/article/a';
  h.c.router.apply({kind: 'article', slug: 'a'});
  h.respond(0, {articles: [article('a')]}); await tick();
  assert.equal(h.requests[1].url, 'data/articles/source/a.md');
  h.respond(1, 'BODY A'); await tick(); assert.match(h.body.innerHTML, /BODY A/);
  assert.equal(h.c.location.hash, '#/article/a'); assert.equal(h.c.location.search, '?r=1');
});
test('two opens sharing a pending reader script mount only the latest reading', async () => {
  const h = harness(); const a = h.c.openArticle(article('a', {interactive: 'gita'}));
  const b = h.c.openArticle(article('b', {interactive: 'gita'}));
  assert.equal(h.scripts.length, 1); h.scripts[0].onload(); await tick();
  assert.equal(h.scripts.length, 2); h.scripts[1].onload(); await Promise.all([a, b]);
  assert.deepEqual(h.readers, ['gita']); assert.match(h.body.textContent, /GITA/);
  assert.equal(h.c.location.hash, '#/article/b'); assert.equal(h.c.panelState.loaded.article, true);
});
test('late failures do not replace the current successful article', async () => {
  const h = harness(); const a = h.c.openArticle(article('a'));
  const b = h.c.openArticle(article('b')); h.respond(1, 'BODY B'); await b;
  h.requests[0].reject(new Error('offline')); await a;
  assert.match(h.body.innerHTML, /BODY B/); assert.equal(h.c.panelState.loaded.article, true);
});
test('HTTP failure is readable and not marked loaded', async () => {
  const h = harness(); const a = h.c.openArticle(article('a'));
  h.requests[0].resolve({ok: false, status: 503}); await a;
  assert.match(h.body.innerHTML, /could not be loaded/); assert.match(h.body.innerHTML, /Retry/);
  assert.equal(h.c.panelState.loaded.article, false);
});
test('passage failure preserves prose and announces the missing material', async () => {
  const h = harness(); const a = h.c.openArticle(article('a', {passages_doc: 'passages'}));
  h.respond(0, 'BODY A'); await tick(); h.requests[1].reject(new Error('offline')); await a;
  assert.match(h.body.innerHTML, /BODY A/); assert.match(h.body.textContent, /passages could not be loaded/);
});
test('Sahasranama receives a live guard across its asynchronous render', async () => {
  const h = harness(), rendered = deferred(); let options;
  h.c.window.SahasranamaReader.render = async (_, opts) => { options = opts; await rendered.promise; };
  const a = h.c.openArticle(article('a', {interactive: 'sahasranama'}));
  h.scripts[0].onload(); await tick(); h.scripts[1].onload(); await tick();
  assert.equal(options.isCurrent(), true); h.c.closePanel(); assert.equal(options.isCurrent(), false);
  rendered.resolve(); await a;
  assert.equal(h.c.panelState.loaded.article, false); assert.equal(h.c.location.hash, '');
});
test('pending thinker completion does not clear a newer article title', async () => {
  const h = harness(), thinker = deferred(); h.c.loadThinkerById = () => thinker.promise;
  const t = h.c.openThinker('T'); const a = h.c.openArticle(article('a'));
  h.respond(0, 'BODY A'); await a; thinker.resolve({id: 'T'}); await t;
  assert.equal(h.c.dpTabTitle.textContent, 'A'); assert.equal(h.c.panelState.activeTab, 'article');
});

test('a failed perspective manifest retries without reopening the thinker in a loop', async () => {
  const h = harness(); let loads = 0, reopened = 0;
  h.c.state.activeId = 'T'; h.c.openThinker = () => { reopened++; };
  h.c.loadJSON = async () => { loads++; return loads === 1 ? null : {perspectives: []}; };
  vm.runInContext('let perspectivesLoading = null;\n' + extract('ensurePerspectivesLoaded') + '\n' + extract('renderPerspectivesBlock'), h.c);
  assert.equal(h.c.renderPerspectivesBlock({id: 'T'}), ''); await tick();
  assert.equal(loads, 1); assert.equal(reopened, 0);
  await h.c.ensurePerspectivesLoaded(); assert.equal(loads, 2); assert.ok(h.c.perspectivesManifest);
});

test('a cold citation cannot reopen the panel after close', async () => {
  const h = harness(), index = deferred(); h.c.loadCitationIndex = () => index.promise;
  h.c.openPanel('article'); const pending = h.c.openCitationPanel('T/work/1', null);
  h.c.closePanel(); index.resolve(); await pending;
  assert.equal(h.c.panelState.open, false); assert.equal(h.c.location.hash, '');
  assert.equal(h.c.sourceTabState.activeCiteKey, null);
});
test('a cold citation cannot replace a newer article', async () => {
  const h = harness(), index = deferred(); h.c.loadCitationIndex = () => index.promise;
  const pending = h.c.openCitationPanel('T/work/1', null);
  const articleLoad = h.c.openArticle(article('b')); h.respond(0, 'BODY B'); await articleLoad;
  index.resolve(); await pending;
  assert.equal(h.c.panelState.activeTab, 'article'); assert.equal(h.c.location.hash, '#/article/b');
});
test('the latest citation owns the panel when index requests finish out of order', async () => {
  const h = harness(), first = deferred(), second = deferred(); let calls = 0;
  h.c.loadCitationIndex = () => (++calls === 1 ? first : second).promise;
  const a = h.c.openCitationPanel('T/work/1', null), b = h.c.openCitationPanel('T/work/2', null);
  second.resolve(); await b; first.resolve(); await a;
  assert.equal(h.c.sourceTabState.activeCiteKey, 'T/work/2'); assert.equal(h.c.panelState.activeTab, 'citation');
  assert.equal(h.c.dpCitationBody.innerHTML, 'T/work/2'); assert.equal(h.c.location.hash, '#/thinker/T/citation/T/work/2');
});
test('selecting a citation invalidates an earlier pending article manifest', async () => {
  const h = harness(); h.c.router.apply({kind: 'article', slug: 'a'});
  await h.c.openCitationPanel('T/work/1', null);
  h.respond(0, {articles: [article('a')]}); await tick();
  assert.equal(h.requests.length, 1); assert.equal(h.c.panelState.activeTab, 'citation');
});
test('selecting a cached article tab cancels a pending citation and retains its body', async () => {
  const h = harness(); const a = h.c.openArticle(article('a')); h.respond(0, 'BODY A'); await a;
  const index = deferred(); h.c.loadCitationIndex = () => index.promise;
  const citation = h.c.openCitationPanel('T/work/1', null); h.activateTab('article');
  index.resolve(); await citation;
  assert.equal(h.c.panelState.activeTab, 'article'); assert.match(h.body.innerHTML, /BODY A/);
});
test('a cold mobile citation cannot create a sheet after closing its reader', async () => {
  const h = harness(), index = deferred(); h.c.loadCitationIndex = () => index.promise; h.c.isPanelMobile = () => true;
  h.c.openPanel('article'); const citation = h.c.openCitationPanel('T/work/1', null);
  h.c.closePanel(); index.resolve(); await citation; await tick();
  assert.equal(h.c.document.body.children.length, 0);
});

test('clicking the already-active Article tab preserves its pending load', async () => {
  const h = harness(); const a = h.c.openArticle(article('a')); h.activateTab('article');
  h.respond(0, 'BODY A'); await a;
  assert.match(h.body.innerHTML, /BODY A/); assert.equal(h.c.panelState.loaded.article, true);
});
test('article passages finish while inspecting a citation and remain on return', async () => {
  const h = harness(); const a = h.c.openArticle(article('a', {passages_doc: 'passages'}));
  h.respond(0, 'BODY A'); await tick(); h.respond(1, {passages: [], includes: ['include']}); await tick();
  await h.c.openCitationPanel('T/work/1', null);
  h.respond(2, {passages: [{id: 'current'}]}); await tick(); h.scripts[0].onload(); await a;
  assert.equal(h.c.panelState.activeTab, 'citation'); assert.equal(h.requests.length, 3);
  h.activateTab('article');
  assert.match(h.body.innerHTML, /PASSAGES/); assert.equal(h.c.panelState.loaded.article, true);
  assert.equal(h.c.panelState.activeTab, 'article'); assert.equal(h.c.location.hash, '#/article/a');
});
test('mobile reference inspection leaves article passage hydration running', async () => {
  const h = harness(); h.c.isPanelMobile = () => true;
  const a = h.c.openArticle(article('a', {passages_doc: 'passages'}));
  h.respond(0, 'BODY A'); await tick(); h.respond(1, {passages: [], includes: ['include']}); await tick();
  await h.c.openCitationPanel('T/work/1', null);
  assert.equal(h.c.document.body.children.length, 2);
  h.respond(2, {passages: [{id: 'current'}]}); await tick(); h.scripts[0].onload(); await a;
  assert.match(h.body.innerHTML, /PASSAGES/); assert.equal(h.c.panelState.loaded.article, true);
  assert.equal(h.c.panelState.activeTab, 'article'); assert.equal(h.requests.length, 3);
});

test('clicking the active Article tab does not cancel its pending manifest', async () => {
  const h = harness(); h.c.router.apply({kind: 'article', slug: 'a'}); h.activateTab('article');
  h.respond(0, {articles: [article('a')]}); await tick(); h.respond(1, 'BODY A'); await tick();
  assert.match(h.body.innerHTML, /BODY A/); assert.equal(h.c.panelState.loaded.article, true);
});
test('interrupted manifest lookup leaves a usable retry in its cached article tab', async () => {
  const h = harness(); h.body.retry = element(); h.c.router.apply({kind: 'article', slug: 'a'});
  await h.c.openCitationPanel('T/work/1', null); h.respond(0, {articles: [article('a')]}); await tick();
  assert.equal(h.c.panelState.activeTab, 'citation'); h.activateTab('article');
  assert.match(h.body.innerHTML, /Retry/); h.body.querySelector('[data-article-retry]').emit('click'); await tick();
  h.respond(1, 'BODY A'); await tick(); assert.match(h.body.innerHTML, /BODY A/);
});

test('a mobile glossary citation can open with the detail panel closed', async () => {
  const h = harness(); h.c.isPanelMobile = () => true;
  await h.c.openCitationPanel('T/work/1', null);
  assert.equal(h.c.panelState.open, false); assert.equal(h.c.document.body.children.length, 2);
});

// Existing citation-index evidence is authoritative here. These tests change no
// verification decisions; they require mobile to honor the desktop false gate.
const citationIndex = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/citation_index.json'), 'utf8'));
function citationHarness() {
  const h = harness(); h.c.state.citationIndex = citationIndex; h.c.isPanelMobile = () => true;
  vm.runInContext(['lookupCitationEntry', 'renderCitationTab', 'collectSurroundingPassages', 'mdVerse', 'convertItalic', 'escape', 'citationOriginal', 'renderCitationSourceNotes', 'enrichArticleFootnotes', 'footnoteMetadata'].map(extract).join('\n'), h.c);
  return h;
}
test('mobile and desktop withhold every explicitly unverified indexed quotation', async () => {
  assert.equal(citationIndex.entries['candrakirti/madhyamakavatara/1.2'].verified, false);
  const rejected = Object.entries(citationIndex.entries).filter(([, entry]) => entry.verified === false);
  assert.ok(rejected.length > 0);
  for (const [key, entry] of rejected) {
    const h = citationHarness(); h.c.renderCitationTab(key); await h.c.openCitationPanel(key, null);
    const mobile = h.c.document.body.children[1].innerHTML;
    for (const html of [h.c.dpCitationBody.innerHTML, mobile]) {
      assert.match(html, /Unverified/, key);
      assert.doesNotMatch(html, /Verified witness|Verified source passage/, key);
      if (entry.sanskrit_iast) assert.ok(!html.includes(h.c.mdVerse(entry.sanskrit_iast)), `${key}: Sanskrit withheld`);
      if (entry.english_close) assert.ok(!html.includes(entry.english_close), `${key}: translation withheld`);
      if (entry.verification_note) assert.ok(html.includes(h.c.escape(entry.verification_note)), `${key}: evidence note retained`);
      assert.ok(html.includes(h.c.escape(entry.locus || entry.locus_short || key.split('/').slice(2).join('/'))), `${key}: locus retained`);
    }
  }
});
test('verified and pending-acquisition quotations retain their existing distinct presentation', async () => {
  for (const status of [true, 'pending-acquisition']) {
    const [key, entry] = Object.entries(citationIndex.entries).find(([, e]) => e.verified === status && e.sanskrit_iast && e.english_close);
    const h = citationHarness(); h.c.renderCitationTab(key); await h.c.openCitationPanel(key, null);
    for (const html of [h.c.dpCitationBody.innerHTML, h.c.document.body.children[1].innerHTML]) {
      assert.ok(html.includes(h.c.mdVerse(entry.sanskrit_iast)), `${key}: permitted Sanskrit retained`);
      assert.ok(html.includes(entry.english_close), `${key}: permitted translation retained`);
      if (status === true) assert.match(html, /Verified witness|Verified source passage/);
      else { assert.match(html, /Pending/); assert.match(html, /context/); assert.doesNotMatch(html, /Verified witness|Verified source passage/); }
    }
  }
});

function enableMetadata(h) {
  h.c.loadJSON = async url => { const r = await h.c.fetch(url); return r.ok ? r.json() : null; };
  vm.runInContext(['loadCitationIndex', 'lookupCitationEntry', 'footnoteMetadata', 'renderFootnoteList', 'escape'].map(extract).join('\n'), h.c);
  Object.defineProperty(h.body, 'bodyWrites', {get: () => h.body.writes});
  h.c.numberCitations = html => ({html, footnotes: [{idx: 1, key: 'author/work/locus'}]});
  return h;
}
test('citation metadata never blocks prose and enriches only its still-current footer', async () => {
  const h = enableMetadata(harness()); const a = h.c.openArticle(article('a'));
  h.respond(0, 'READABLE PROSE'); await tick();
  assert.match(h.body.innerHTML, /READABLE PROSE/, 'prose appears while metadata request is pending');
  const footer = h.body.querySelector('.cite-fn-wrap'); assert.ok(footer);
  const writes = h.body.bodyWrites; h.body.scrollTop = 345;
  h.respond(1, {entries: {'author/work/locus': {author_name: 'Actual author', work_title: 'Actual work', locus: 'Precise locus'}}});
  await a; await tick();
  assert.match(footer.outerHTML, /Actual author/); assert.match(footer.outerHTML, /Actual work/); assert.match(footer.outerHTML, /Precise locus/);
  assert.equal(h.body.bodyWrites, writes, 'metadata must not replace body/selection nodes');
  assert.equal(h.body.scrollTop, 345, 'metadata must not reset reader scroll');
});
test('late citation metadata cannot update an abandoned article footer', async () => {
  const h = enableMetadata(harness()); const a = h.c.openArticle(article('a'));
  h.respond(0, 'BODY A'); await tick(); const footer = h.body.querySelector('.cite-fn-wrap'); assert.ok(footer); const before = footer.outerHTML;
  h.c.closePanel(); h.respond(1, {entries: {'author/work/locus': {author_name: 'Late author'}}});
  await a; await tick(); assert.equal(footer?.outerHTML, before);
});
test('concurrent citation-index consumers share one request and failed loads retry', async () => {
  const h = enableMetadata(harness());
  const first = h.c.loadCitationIndex(), second = h.c.loadCitationIndex();
  assert.equal(h.requests.length, 1); h.requests[0].resolve({ok: false}); await Promise.all([first, second]);
  const retry = h.c.loadCitationIndex(); assert.equal(h.requests.length, 2);
  h.respond(1, {entries: {}}); await retry; await h.c.loadCitationIndex(); assert.equal(h.requests.length, 2);
});

test('late metadata leaves focused or selected footnotes intact', async () => {
  for (const interaction of ['focus', 'selection']) {
    const h = enableMetadata(harness()); const a = h.c.openArticle(article('a'));
    h.respond(0, 'BODY A'); await tick(); const footer = h.body.querySelector('.cite-fn-wrap'); assert.ok(footer);
    const before = footer.outerHTML;
    if (interaction === 'focus') {
      const focus = {}; h.c.document.activeElement = focus; footer.contains = node => node === focus;
    } else {
      h.c.window.getSelection = () => ({isCollapsed: false, rangeCount: 1, getRangeAt: () => ({intersectsNode: node => node === footer})});
    }
    h.respond(1, {entries: {'author/work/locus': {author_name: 'New metadata'}}}); await a; await tick();
    assert.equal(footer.outerHTML, before, `${interaction} is not destroyed by metadata enrichment`);
  }
});
test('a rejected citation loader releases its pending request for retry', async () => {
  const h = enableMetadata(harness());
  const rejected = h.c.loadCitationIndex(); h.requests[0].reject(new Error('offline'));
  await assert.rejects(rejected, /offline/);
  const retry = h.c.loadCitationIndex(); h.respond(1, {entries: {}}); await retry;
  assert.equal(h.requests.length, 2);
});

test('background perspective metadata cannot reopen a thinker after reference navigation', async () => {
  const h = harness(), manifest = deferred(); let reopened = 0, loads = 0;
  h.c.state.activeId = 'T'; h.c.openPanel('thinker');
  h.c.openThinker = () => { reopened++; }; h.c.inlineMarkdown = text => text;
  h.c.loadJSON = async () => { loads++; return manifest.promise; };
  vm.runInContext('let perspectivesLoading = null;\n' + extract('ensurePerspectivesLoaded') + '\n' + extract('renderPerspectivesBlock'), h.c);
  h.c.renderPerspectivesBlock({id: 'T'}); await h.c.openCitationPanel('T/work/1', null);
  manifest.resolve({perspectives: [{slug: 'p', title: 'Cached perspective', for_thinker_ids: ['T']}]}); await tick();
  assert.equal(reopened, 0); assert.equal(h.c.panelState.activeTab, 'citation');
  assert.match(h.c.renderPerspectivesBlock({id: 'T'}), /Cached perspective/);
  assert.equal(loads, 1, 'the next thinker visit can use the cached manifest');
});
test('background perspective metadata refreshes its still-current thinker once', async () => {
  const h = harness(), manifest = deferred(); let reopened = 0;
  h.c.state.activeId = 'T'; h.c.openPanel('thinker'); h.c.openThinker = () => { reopened++; };
  h.c.loadJSON = () => manifest.promise;
  vm.runInContext('let perspectivesLoading = null;\n' + extract('ensurePerspectivesLoaded') + '\n' + extract('renderPerspectivesBlock'), h.c);
  h.c.renderPerspectivesBlock({id: 'T'}); manifest.resolve({perspectives: []}); await tick();
  assert.equal(reopened, 1);
});

(async () => {
  let failed = 0;
  for (const [name, fn] of tests) {
    let timeout;
    try {
      await Promise.race([fn(), new Promise((_, reject) => {
        timeout = setTimeout(() => reject(new Error('test did not settle')), 1000);
      })]);
      console.log(`PASS ${name}`);
    } catch (error) {
      failed++; console.error(`FAIL ${name}: ${error.stack}`);
    } finally {
      clearTimeout(timeout);
    }
  }
  if (failed) process.exitCode = 1;
})();
