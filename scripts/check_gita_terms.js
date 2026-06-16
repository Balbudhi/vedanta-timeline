#!/usr/bin/env node
/* Deterministic term-consistency checker for the Gītā reader.
   Enforces the agreed preserve/translate policy across every word in
   verses.js + commentaries.js, and flags:
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

// canonical term -> how to detect it on a word stem, and its policy
const PRESERVE = {
  raga:    { det: /(^|-)(rāga|rāg)/, iast: "rāga", bad: ["passion"] },
  dvesa:   { det: /dveṣ/,            iast: "dveṣa", bad: ["aversion", "hatred"] },
  guna:    { det: /(^|-)guṇa/,       iast: "guṇa", bad: [] },
  dharma:  { det: /(^|-)dharma/,     iast: "dharma", bad: ["duty"] },
  kama:    { det: /(^|-)kāma/,       iast: "kāma", bad: [] },
  prajna:  { det: /prajñā/,          iast: "prajñā", bad: ["wisdom", "insight"] },
  buddhi:  { det: /(^|-)buddh/,      iast: "buddhi", bad: ["intellect"] },
  karma:   { det: /(^|-)karma/,      iast: "karma", bad: ["action"] },
  manas:   { det: /(^|-)(manas|mano|manaḥ|manā)/, iast: "manas", bad: [] },
  indriya: { det: /indriy/,          iast: "indriya", bad: [] },
  yoga:    { det: /(^|-)yoga/,       iast: "yoga", bad: [] },
  rasa:    { det: /(^|-)rasa/,       iast: "rasa", bad: ["relish"] },
  ahankara:{ det: /ahaṅkār/,         iast: "ahaṅkāra", bad: ["I-maker", "I-making"] },
  trsna:   { det: /(^|-)tṛṣṇā/,      iast: "tṛṣṇā", bad: [] },
};
const TRANSLATE = {
  krodha: { det: /(^|-)krodh/,            en: "anger",     iast: "krodha" },
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

let A = 0, B = 0, C = 0, D = 0;
function checkUnit(label, words, english) {
  const pmap = english ? phrasesByIndex(english) : {};
  for (const w of words || []) {
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
        const quoted = new RegExp("[‘'\"“]\\s*" + od.iast.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(phrases);
        if (quoted) continue;                                 // cited lemma, not used
        console.log(`B ${label} [${w.i}] ${w.iast} (${t}): slot prints other term "${od.iast}" — "${phrases}"`); B++;
      }
    }
  }
}

const V = load("gita/sthitaprajna/verses.js", "GITA_VERSES");
for (const v of V) { checkUnit(`v${v.locus}`, v.words, v.english); for (const c of v.commentaries || []) checkUnit(`v${v.locus}/${c.voiceId||c.author}`, c.words, c.english); }
const C2 = load("gita/sthitaprajna/commentaries.js", "GITA_COMMENTARY");
for (const loc of Object.keys(C2)) for (const c of C2[loc]) checkUnit(`c${loc}/${c.voiceId||c.author}`, c.words, c.english);

console.log(`\nA(glossaryKey mismatch)=${A}  B(prints other term)=${B}  C(translate left IAST)=${C}  D(preserve flattened)=${D}`);
const total = A + B + C + D;
if (total) { console.error(`\n${total} term-consistency violation(s).`); process.exit(1); }
console.log("Term consistency OK.");
