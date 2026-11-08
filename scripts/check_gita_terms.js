#!/usr/bin/env node
/* Deterministic term-consistency checker for the Gītā readers.
   Readers are discovered (gita/<dir>/verses.js). A reader built under the term
   policy (data/glossary/term_policy.json, v1 `terms` or v2 `lemmas`) is governed
   by the policy alone: P (rendering), R (reserved English), A, E and F. The
   legacy hard-coded tables below apply only to the three pre-policy readers in
   LEGACY until they are migrated. For legacy readers it flags:
     A. glossaryKey pointing at a different concept than the word is
        (with a whitelist of legitimate synonym/epithet maps);
     B. a word rendered in its English slot as a DIFFERENT preserve-term's
        IAST (e.g. a cetas word printed "manas");
     C. a TRANSLATE term left in IAST in the English;
     D. a PRESERVE term flattened to its forbidden English word.
   Read-only. Exits non-zero if any violation. */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
function load(file, g) { const c = fs.readFileSync(path.join(ROOT, file), "utf8"); const w = {}; new Function("window", c)(w); return w[g]; }

// Pre-policy readers: the only readers the legacy PRESERVE/TRANSLATE tables govern.
const LEGACY = new Set(["sthitaprajna", "kama", "ch5"]);
// canonical term -> how to detect it on a word stem, and its policy (legacy readers only)
const PRESERVE = {
  raga:    { det: /(^|-)(rāga|rāg)/, iast: "rāga", bad: ["passion"] },
  dvesa:   { det: /dveṣ/,            iast: "dveṣa", bad: ["aversion", "hatred"] },
  guna:    { det: /(^|-)guṇa/,       iast: "guṇa", bad: [] },
  dharma:  { det: /(^|-)dharma/,     iast: "dharma", bad: ["duty"] },
  kama:    { det: /(^|-)kāma/,       iast: "kāma", bad: [] },
  prajna:  { det: /prajñā/,          iast: "prajñā", bad: ["wisdom", "insight"] },
  buddhi:  { det: /(^|-)buddh/,      iast: "buddhi", bad: ["intellect"] },
  karma:   { det: /(^|-)karma/,      iast: "karma", bad: ["action"] },
  manas:   { det: /(^|-)(manas|mano|manaḥ|manā)/, iast: "manas", bad: ["mind"] },
  indriya: { det: /indriy/,          iast: "indriya", bad: ["sense", "senses"] },
  yoga:    { det: /(^|-)yoga/,       iast: "yoga", bad: [] },
  rasa:    { det: /(^|-)rasa/,       iast: "rasa", bad: ["relish"] },
  ahankara:{ det: /ahaṅkār/,         iast: "ahaṅkāra", bad: ["I-maker", "I-making"] },
  trsna:   { det: /(^|-)tṛṣṇā/,      iast: "tṛṣṇā", bad: [] },
  krodha:  { det: /(^|-)krodh/,      iast: "krodha", bad: ["anger", "wrath"] },
};
const TRANSLATE = {
  bhaya:  { det: /(^|-)bhay/,             en: "fear",      iast: "bhaya" },
  moha:   { det: /(saṃmoh|(^|-)moha|mūḍh|vimuh|vimoh)/, en: "delusion", iast: "moha" },
  sprha:  { det: /spṛh/,                  en: "longing",   iast: "spṛhā" },
  sneha:  { det: /sneh/,                  en: "affection", iast: "sneha" },
  jnana:  { det: /(^|-)jñāna/,            en: "knowledge", iast: "jñāna" },
  moksa:  { det: /(^|-)(mokṣa|mukti)/,    en: "liberation", iast: "mokṣa" },
  sanga:  { det: /(^|-)saṅga/,            en: "clinging",  iast: "saṅga" },
};
// legit glossaryKey synonym/epithet maps (word root -> allowed key)
const SYN = {
  visnu: [/hari/, /vāsudev/, /acyut/, /janārdan/, /mukund/, /kṛṣṇ/, /keśav/, /govind/, /viṣṇu/, /madhusūdan/, /mādhav/],
  citta: [/cetas|cetaḥ|ceto|cittas|^citt/],
  buddhi: [/dhī|dhīḥ|sthitadh/],
  sruti: [/ved(a|e|ena|aiḥ|am)/, /śruti/],
  moksa: [/mukt|apavarg|mumukṣ|mokṣ/],
  jiva: [/deh(in|a|e|inaḥ)/],
  dehin: [/deh/],
  jnana: [/vidvān|sarvajñ|bodh|vyajān|vipaścit|jña(ḥ|m|ān)|jñāt/],
  prajna: [/vipaścit/],
  smrti: [/smar|smṛ/],
  isvara: [/īś|īśvar|īśit/],
  visaya: [/viṣay|indriyārth|arth/],
  atman: [/ātm|svarūp|pratyag/],
  kartr: [/kāraka|kartṛ|kart/],
  sat: [/saty|sad|sat/],
  anu: [/aṇu|anu/],
  bhagavan: [/bhagav|paripūrṇ/],
  nirodha: [/nirudh|nirodh/],
  bheda: [/bhinn|bhid|bhed/],
  krodha: [/kop/],                                  // kopa is a plain synonym of krodha
  saksin: [/draṣṭ|dṛś|sākṣ/],                       // draṣṭṛ, the seer, = the sākṣin
  jnanendriya: [/śrotr|cakṣu|ghrāṇ|rasan|tvac/],    // a named sense-power → its category
};
function detectTerms(w) {
  const hay = [w.stem, w.iast, ...(w.parts || []).map(p => p.form)].filter(Boolean).join(" ");
  const terms = [];
  for (const [t, d] of Object.entries(PRESERVE)) if (d.det.test(hay)) terms.push(t);
  for (const [t, d] of Object.entries(TRANSLATE)) if (d.det.test(hay)) terms.push(t);
  return terms;
}
// Load the glossary so Check A can test real lexical relatedness (word shares a
// >=4-char run with the key's term_iast or any alias) — the proven low-noise test.
const MAN = JSON.parse(fs.readFileSync(path.join(ROOT, "data/glossary/manifest.json"), "utf8"));
const KEY_FORMS = {};
for (const fn of MAN.terms) { const p = path.join(ROOT, "data/glossary", fn); if (!fs.existsSync(p)) continue; const d = JSON.parse(fs.readFileSync(p, "utf8")); KEY_FORMS[d.term_key] = [d.term_iast || d.term_key, ...(d.aliases || [])]; }
const normd = s => (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z]/g, "");
function sharesRun(a, b) { for (let L = Math.min(a.length, b.length); L >= 4; L--) for (let i = 0; i + L <= b.length; i++) if (a.includes(b.substr(i, L))) return true; return false; }
function keyAllowedFor(key, w /*, terms */) {
  if (!key) return true;
  const wf = normd([w.stem, w.iast, ...(w.parts || []).map(p => p.form)].filter(Boolean).join(""));
  for (const f of (KEY_FORMS[key] || [key])) { const nf = normd(f); if (nf && (sharesRun(wf, nf) || sharesRun(nf, wf))) return true; }
  const hay = [w.stem, w.iast, ...(w.parts || []).map(p => p.form)].filter(Boolean).join(" ");
  for (const re of (SYN[key] || [])) if (re.test(hay)) return true;
  return false;
}

// gather english phrase text per word index, per unit
function phrasesByIndex(english) {
  const map = {};
  const re = /\{([\d,\s]+):([^}]*)\}/g; let m;
  while ((m = re.exec(english)) !== null) {
    const txt = m[2];
    for (const i of m[1].split(",").map(s => s.trim()).filter(Boolean)) (map[i] = map[i] || []).push(txt);
  }
  return map;
}
const ALL_PRESERVE_IAST = Object.entries(PRESERVE);

// ---- sense-constant policy mode (data/glossary/term_policy.json) -----------
// A word that carries `term: {lemma, sense}` is checked against the policy row
// instead of the legacy PRESERVE/TRANSLATE tables above: a preserved sense must
// print its IAST and none of its forbidden English; a translated sense must use
// one of its fixed renderings and never its Sanskrit. Readers built under the
// policy (gita/ch12 onward) carry `term` on every matching word; the builder
// enforces presence, this checker enforces rendering on every occurrence.
// Both policy structures are read (audit §5.4): v1 {terms: {lemma: {match, senses: {s: {english,…}}}}}
// and v2 {lemmas: {lemma: {senses: {s: {forms: {category: [...]}, status,…}}}}, reserved_english}.
// v2 `forms` are flattened here (any category); the builder checks them per category.
function normalizePolicy(raw) {
  const rows = raw.lemmas || raw.terms;
  if (!rows) throw new Error("term_policy.json has neither `terms` (v1) nor `lemmas` (v2)");
  const out = { structure: raw.lemmas ? "v2" : "v1", rows: {}, reserved: {} };
  for (const [lemma, r] of Object.entries(rows)) {
    const senses = {};
    for (const [sn, sr] of Object.entries(r.senses || {})) {
      const english = sr.forms ? [...new Set(Object.values(sr.forms).flat())] : (sr.english || []);
      const iast = sr.iast || (sr.policy === "preserve" ? r.lemma_iast : undefined);
      senses[sn] = { ...sr, english, iast, iast_forms: sr.iast_forms || (iast ? [iast] : []) };
    }
    out.rows[lemma] = { ...r, senses };
  }
  const owner = (v) => out.rows[v] ? v : (Object.keys(out.rows).find((k) => out.rows[k].lemma_iast === v ||
    Object.values(out.rows[k].senses).some((x) => x.iast === v)) || v);
  for (const [w, v] of Object.entries(raw.reserved_english || {})) out.reserved[w] = owner(v);
  return out;
}
const POLICY = normalizePolicy(JSON.parse(fs.readFileSync(path.join(ROOT, "data/glossary/term_policy.json"), "utf8")));
let P = 0, R = 0;
function policyCheck(label, w, phrases) {
  const t = w.term; if (!t) return false;
  const row = POLICY.rows[t.lemma]; const srow = row && row.senses[t.sense];
  if (!srow) { console.log(`P ${label} [${w.i}] ${w.iast}: term ${JSON.stringify(t)} not in policy`); P++; return true; }
  if (!phrases) return true;
  const low = phrases.toLowerCase();
  const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  if (srow.policy === "preserve") {
    if (!(srow.iast_forms || [srow.iast]).some((f) => phrases.includes(f))) { console.log(`P ${label} [${w.i}] ${w.iast}: preserved ${t.lemma}/${t.sense} must print "${srow.iast}" — "${phrases}"`); P++; }
    for (const bad of srow.forbidden_english || []) if (new RegExp(`\\b${esc(bad.toLowerCase())}\\b`).test(low)) { console.log(`P ${label} [${w.i}] ${w.iast}: preserved ${t.lemma} rendered "${bad}" — "${phrases}"`); P++; }
  } else {
    if (!(srow.english || []).some((e) => new RegExp(`\\b${esc(e.toLowerCase())}\\b`).test(low))) { console.log(`P ${label} [${w.i}] ${w.iast}: translated ${t.lemma}/${t.sense} must use one of ${JSON.stringify(srow.english)} — "${phrases}"`); P++; }
    for (const bad of srow.forbidden_english || []) if (new RegExp(`(?<![‘'"“])\\b${esc(bad.toLowerCase())}\\b`).test(low)) { console.log(`P ${label} [${w.i}] ${w.iast}: translated ${t.lemma} uses forbidden "${bad}" — "${phrases}"`); P++; }
  }
  return true;
}

let A = 0, B = 0, C = 0, D = 0;
const escRe = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
function ownLemmas(w) { return new Set([w.term && w.term.lemma, ...(w.terms || []).map((t) => t && t.lemma)].filter(Boolean)); }
// R: a reserved English word (v2 reserved_english) printed in the slot of a different lemma.
function reservedCheck(label, w, phrases) {
  if (!phrases) return;
  const low = phrases.toLowerCase().replace(/“[^”]*”|‘[^’]*’|"[^"]*"/g, " ");
  for (const [word, owner] of Object.entries(POLICY.reserved)) {
    if (new RegExp(`(?<![A-Za-z])${escRe(word.toLowerCase())}(?![A-Za-z])`).test(low) && !ownLemmas(w).has(owner)) {
      console.log(`R ${label} [${w.i}] ${w.iast}: reserved "${word}" (for ${owner}) printed for another lemma — "${phrases}"`); R++;
    }
  }
}
function checkUnit(label, words, english, legacy) {
  const pmap = english ? phrasesByIndex(english) : {};
  for (const w of words || []) {
    const phr = (pmap[w.i] || []).join(" ");
    if (!legacy) {
      // policy-governed reader: the policy alone decides renderings
      policyCheck(label, w, phr);
      reservedCheck(label, w, phr);
      if (w.glossaryKey && !keyAllowedFor(w.glossaryKey, w)) { console.log(`A ${label} [${w.i}] ${w.iast}: glossaryKey="${w.glossaryKey}" unrelated`); A++; }
      continue;
    }
    if (policyCheck(label, w, phr)) {
      if (w.glossaryKey && !keyAllowedFor(w.glossaryKey, w)) { console.log(`A ${label} [${w.i}] ${w.iast}: glossaryKey="${w.glossaryKey}" unrelated`); A++; }
      continue;
    }
    const terms = detectTerms(w);
    // A: glossaryKey concept mismatch
    if (w.glossaryKey && !keyAllowedFor(w.glossaryKey, w)) {
      console.log(`A ${label} [${w.i}] ${w.iast}: glossaryKey="${w.glossaryKey}" unrelated (detected: ${terms.join(",")||"-"})`); A++;
    }
    const phrases = (pmap[w.i] || []).join(" ");
    if (!phrases) continue;
    // metalinguistic / naming words ("the word moha", "called X", "denotes Y")
    // cite a term as a lemma rather than use it — skip rendering checks for them.
    if (/śabda|saṃjñ|vāci|ākhya|nāma|ity|iti/.test(w.iast || "")) continue;
    // single-term words only for rendering checks (compounds are too noisy)
    if (terms.length === 1) {
      const t = terms[0];
      if (PRESERVE[t]) {
        const d = PRESERVE[t];
        const hasIast = phrases.includes(d.iast) || new RegExp(d.iast.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(phrases);
        for (const badw of d.bad) if (new RegExp(`\\b${badw}\\b`, "i").test(phrases) && !phrases.includes(d.iast)) { console.log(`D ${label} [${w.i}] ${w.iast} (${t}): rendered "${badw}" not IAST — "${phrases}"`); D++; }
      } else if (TRANSLATE[t]) {
        const d = TRANSLATE[t];
        const esc2 = d.iast.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const quoted = new RegExp("[‘'\"“]\\s*" + esc2).test(phrases);   // cited lemma, not used
        if (!quoted && new RegExp(esc2).test(phrases)) { console.log(`C ${label} [${w.i}] ${w.iast} (${t}): left IAST "${d.iast}" — should be "${d.en}" — "${phrases}"`); C++; }
      }
      // B: rendered as a DIFFERENT preserve-term's IAST (but not when that IAST is
      // a quoted lemma — ‘rasa’, "the word X" — which legitimately cites the word)
      for (const [ot, od] of ALL_PRESERVE_IAST) {
        if (ot === t) continue;
        if (!phrases.includes(od.iast)) continue;
        const hay = [w.stem, w.iast, ...(w.parts || []).map(p => p.form)].filter(Boolean).join(" ");
        if (od.det.test(hay)) continue;                       // word actually is that term too
        // A compound legitimately prints its own members — §8 keeps the natural
        // form for set compounds (jñāna-yoga → "the yoga of knowledge"). The
        // joined `hay` misses this because the det patterns anchor at ^ or "-"
        // and an inflected member reads "yogāya", not "yoga"; so test each
        // morpheme piece and compound member on its own as well.
        const pieces = [...(w.parts || []).map(p => p.form), ...((w.compound && w.compound.members) || [])].filter(Boolean);
        if (pieces.some((pc) => od.det.test(pc))) continue;   // that term is a member of this compound
        const quoted = new RegExp("[‘'\"“]\\s*" + od.iast.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(phrases);
        if (quoted) continue;                                 // cited lemma, not used
        console.log(`B ${label} [${w.i}] ${w.iast} (${t}): slot prints other term "${od.iast}" — "${phrases}"`); B++;
      }
    }
  }
}

// Every word-by-word reading on the site, discovered (audit B16): each gita/<dir>/verses.js
// and the globals its data files populate (X_VERSES → X_COMMENTARY, X_PARALLELS). Missing
// files are skipped, so a reading without parallels needs no special-casing here.
// Non-Gītā texts that share the reader (Yoga-Vāsiṣṭha, Sahasranāma) have their own
// vocabulary decisions and are not governed by the Gītā term policy.
const NON_GITA = new Set(["yogavasistha-dama", "vishnu-sahasranama"]);
const READINGS = fs.readdirSync(path.join(ROOT, "gita")).sort().filter((d) => !NON_GITA.has(d)).flatMap((d) => {
  const f = path.join(ROOT, "gita", d, "verses.js");
  if (!fs.existsSync(f)) return [];
  const m = fs.readFileSync(f, "utf8").match(/window\.(\w+)_VERSES\s*=/);
  if (!m) return [];
  const pre = m[1];
  return [{ dir: `gita/${d}`, verses: `${pre}_VERSES`, commentary: `${pre}_COMMENTARY`, parallels: `${pre}_PARALLELS` }];
});
const loadIfPresent = (f, g) => (fs.existsSync(path.join(ROOT, f)) ? load(f, g) : null);
const ALL = READINGS.map((r) => ({
  tag: r.dir.split("/").pop(),
  legacy: LEGACY.has(r.dir.split("/").pop()),
  verses: loadIfPresent(`${r.dir}/verses.js`, r.verses) || [],
  commentary: loadIfPresent(`${r.dir}/commentaries.js`, r.commentary) || {},
  parallels: loadIfPresent(`${r.dir}/parallels.js`, r.parallels),
}));

for (const RD of ALL) {
  for (const v of RD.verses) { checkUnit(`${RD.tag} v${v.locus}`, v.words, v.english, RD.legacy); for (const c of v.commentaries || []) checkUnit(`${RD.tag} v${v.locus}/${c.voiceId||c.author}`, c.words, c.english, RD.legacy); }
  for (const loc of Object.keys(RD.commentary)) for (const c of RD.commentary[loc]) checkUnit(`${RD.tag} c${loc}/${c.voiceId||c.author}`, c.words, c.english, RD.legacy);
}

// ---- card-field hygiene (the word-card pop-up) ---------------------------
// The small pop-up is gloss-LISTS only: synonyms, stem, and a plain Sanskrit
// root line. Two things must never appear in the card fields (gloss, parts[].gloss,
// rootGloss): cross-language etymology/cognates (those live behind "Explain"), and
// single-word collapses of a loaded concept term (the whole point of the redesign).
let E = 0, F = 0;
// E: cross-language cognate / etymology prose leaking into a card field.
const BANNED_ETYM = /\b(Latin|Greek|Proto-Indo|PIE)\b|cognate with|\bkin to\b|English ['‘’"]/;
// F: a loaded PRESERVE concept glossed as a single bare word (no sense list).
// Match the part form EXACTLY to a concept stem (not a substring — "buddha"
// 'awakened' is not buddhi, "karmayoga" is not karma), and flag only a truly
// single-token gloss (a multi-word phrase like "the yoga of action" is fine).
const PRES_FORMS = new Set(["raga", "dvesa", "guna", "dharma", "kama", "prajna", "buddhi", "karma", "manas", "mano", "indriya", "yoga", "rasa", "ahankara", "trsna", "krodha"]);
// Policy-governed readers: the loaded concepts are the policy's preserved senses.
const POLICY_PRES_FORMS = new Set(Object.values(POLICY.rows).flatMap((r) => Object.values(r.senses))
  .filter((s) => s.policy === "preserve").flatMap((s) => [s.iast, ...(s.iast_forms || [])]).filter(Boolean).map(normd));
let CONCEPTS = PRES_FORMS;
const concept = (form) => CONCEPTS.has(normd(form));
const collapsed = (s) => s && !/[\s,;/]/.test(s);
function checkCardFields(label, words) {
  for (const w of words || []) {
    const fields = [["gloss", w.gloss], ["rootGloss", w.rootGloss], ...(w.parts || []).map((p) => [`part:${p.form}`, p.gloss])];
    for (const [fld, val] of fields) {
      if (val && BANNED_ETYM.test(val)) { console.log(`E ${label} [${w.i}] ${w.iast} ${fld}: cross-language etymology in card — "${val}"`); E++; }
    }
    for (const p of w.parts || []) {
      if (concept(p.form) && collapsed(p.gloss)) { console.log(`F ${label} [${w.i}] ${w.iast} part:${p.form}: loaded term collapsed to one sense — "${p.gloss}"`); F++; }
    }
  }
}
function eachParallelWords(node, cb) {
  if (Array.isArray(node)) node.forEach((n) => eachParallelWords(n, cb));
  else if (node && typeof node === "object") { if (Array.isArray(node.words)) cb(node.words); for (const v of Object.values(node)) if (v && typeof v === "object") eachParallelWords(v, cb); }
}
for (const R of ALL) {
  CONCEPTS = R.legacy ? PRES_FORMS : POLICY_PRES_FORMS;
  for (const v of R.verses) { checkCardFields(`${R.tag} v${v.locus}`, v.words); for (const c of v.commentaries || []) checkCardFields(`${R.tag} v${v.locus}/${c.voiceId||c.author}`, c.words); }
  for (const loc of Object.keys(R.commentary)) for (const c of R.commentary[loc]) checkCardFields(`${R.tag} c${loc}/${c.voiceId||c.author}`, c.words);
  if (R.parallels) eachParallelWords(R.parallels, (words) => checkCardFields(`${R.tag} parallel`, words));
}

console.log(`\nReaders: ${ALL.map((r) => r.tag + (r.legacy ? " (legacy tables)" : " (policy)")).join(", ")}; policy ${POLICY.structure}`);
console.log(`P(policy)=${P}  R(reserved English)=${R}  A(glossaryKey mismatch)=${A}  B(prints other term)=${B}  C(translate left IAST)=${C}  D(preserve flattened)=${D}  E(card etymology)=${E}  F(card single-word collapse)=${F}`);
const total = P + R + A + B + C + D + E + F;
if (total) { console.error(`\n${total} term-consistency violation(s).`); process.exit(1); }
console.log("Term consistency OK.");
