# Sanskrit translation standard

How Sanskrit is translated and presented on this site. This is the **norm going
forward** for every Sanskrit text we render — mūla (root text) *and* commentary.
The reference implementation is the Bhagavad-Gītā 2.54–72 reading
(`gita/sthitaprajna/`, engine `assets/gita.js` = `window.GitaReader`).

## 1. Principle: literal, word-by-word, faithful to the grammar

The truest reading is the literal one. We translate the grammar that is actually
present and make it inspectable, rather than paraphrasing.

- **Literal, not interpretive.** No inserted nouns or subjects the Sanskrit does
  not have (e.g. do not render an implied 3rd-sg. masculine subject as "a man" —
  use "he"). Respect gender, number, person, and voice (passives stay passive).
  Supplied copulas ("is") for nominal sentences are fine.
- **Every choice is significant.** Epithets and proper names are translated with
  their etymology (Keśava, Pārtha, Kaunteya, Mahābāhu…), not left as opaque names.
- **Untranslatables stay Sanskrit** and link to the glossary (brahman, yoga,
  ātman, dharma, prajñā…); `translatable: false` suppresses a forced English gloss.
- **Explicit ambiguity.** Where a form is genuinely ambiguous, say so in the
  word card; never fake a confident single parse.
- **Grounded, never fabricated.** Sanskrit is taken verbatim from cited sources
  on disk (`data/sources/...`); transliterate faithfully; cite every source. If a
  text cannot be sourced, omit it and say so — do not invent Sanskrit.

## 2. The reading UX (what `GitaReader` renders)

- **IAST only on screen.** Devanāgarī is authored and kept in the data
  (`words[].deva`, top-level `devanagari`) but not displayed.
- Per unit: a **saṃhitā** line (natural, sandhi'd) for reading, then an
  interactive **pada-pāṭha** (sandhi-resolved, space-separated — every word a
  tappable token), then the **literal English**.
- **Tap a word → a card** with: the word; its whole-word gloss; the
  **morpheme pieces, each translated** (`pra-` "forth" + `√bhāṣ` "to speak");
  the grammar in plain English (case/number/gender or tense/voice, with the
  case's force, e.g. genitive → "of"); the samāsa-vigraha for compounds; and a
  link into the glossary for technical terms.
- **Cards open on CLICK only** (never hover — hover obscures the text).
- **Bidirectional highlight**: tapping a Sanskrit word highlights its English,
  and tapping an English phrase highlights + cards its Sanskrit word.
- **Commentary gets the identical treatment.** A commentator's Sanskrit is
  word-by-word interactive exactly like the mūla (same `words[]` + slotted
  `english`). Commentary is shown **voice by voice**: a multi-select, colour-coded
  chooser (each commentator a colour); equal, no ranking, ordered chronologically.
  Each commentator's name links to their Thinker entry in the timeline.

## 3. Data schema

Per word object (mūla and commentary alike):

```jsonc
{
  "i": 0,                       // 0-based, contiguous, matches english {i:…} slots
  "iast": "sthitaprajñasya",    // pada-pāṭha citation form (sandhi resolved)
  "deva": "स्थितप्रज्ञस्य",        // Devanāgarī citation form (kept; not displayed)
  "gloss": "of one whose wisdom is steady",
  "parts": [                    // morpheme pieces, each translated (the layperson layer)
    {"form": "sthita", "gloss": "stood firm, steady"},
    {"form": "prajñā", "gloss": "wisdom, insight"}
  ],
  "stem": "sthita-prajña", "root": null,           // (root as "√bhāṣ")
  "affix": "ṅas (ṣaṣṭhī ekavacana)",               // technical Pāṇinian name
  "morph": "gen. sg. masc.",                        // rendered to plain English in the card
  "karaka": "sambandha (relational genitive)",
  "compound": { "type": "bahuvrīhi", "vigraha": "sthitā prajñā yasya saḥ", "members": ["sthita","prajñā"] },
  "glossaryKey": "sthitaprajna",                    // a key/alias present in data/glossary/, else null/omit
  "translatable": true                              // false → render plain, no forced gloss
}
```

Per unit: `iast` (saṃhitā), `devanagari`, `english` (the slotted literal
rendering — `"{0:…} {1,2:…}"` referencing `words[].i`), and `grammar`
(`karakaSummary`, `verbalModality`). Commentary entries carry the same
`words[]` + `english`, alongside their verbatim `sanskrit` and our `ourRendering`.

Invariants (CI-checkable): `i` contiguous from 0; every `english` `{i:…}` slot
resolves to a real word index; the concatenated `iast` tokens faithfully
represent the source `sanskrit` (sandhi resolution only — nothing dropped or
invented); every `glossaryKey` resolves to a file in `data/glossary/`.

## 4. Glossary

Use **the site's existing glossary** (`data/glossary/*.json`, the searchable
popover in `assets/app.js`). Embedded readers delegate the glossary link to that
popover (`GitaReader.render(root, {onGlossary, onThinker, glossaryBase})`); the
standalone page uses a matching popover.

Glossary entries are **encyclopedic**: neutral academic register, no
editorializing, consistent house style. Each gives the **traditional grammatical
meaning/derivation** (`literal`), a tradition-wide `invariant_definition` with
claims anchored to real loci (verified against on-disk texts where possible),
`per_school` readings, and a genuine `translator_note` (never page-rendering
instructions, never a recap of the passage at hand). **Add terms as needed** so
every technical term in the text and its commentaries is covered.

## 5. How to apply this to a new text

1. Acquire the mūla + commentaries verbatim into `data/sources/...` (cite).
2. Produce the per-unit data (Opus agents, batched): `words[]` + slotted
   `english` for the mūla and for each commentary, following §3.
3. Audit independently: grammar/morphology, literalness (§1), verbatim fidelity,
   and glossary coverage.
4. Render with `GitaReader` (standalone page + in-app Article via `app.js`).
5. Ensure glossary coverage (§4).

Deviations from this standard should be deliberate and noted.

## 6. Pāṇinian formalism (strict)

Every word breakdown must follow Pāṇini and traditional vyākaraṇa to the letter.
The English may read smoothly, but the grammatical fields must be formally exact.

- **Root (`root`)** — cite the verbal root in its dhātupāṭha form with its **gaṇa**
  (class) and pada: e.g. `√bhū (bhvādi, 1P)`, `√vā (adādi, 2P, 'to blow')`,
  `√hu (juhotyādi, 3P)`, `√as (adādi, 2P)`. Not a loose romanized stem.
- **Affix (`affix`)** — name the **pratyaya**, not just the case. Nominal endings
  are the **sup** series (su, au, jas; am, auṭ, śas; ṭā, bhyām, bhis; ṅe…; ṅasi…;
  ṅas…; ṅi, os, sup) given with their **vibhakti** (prathamā … saptamī) and
  **vacana** (eka/dvi/bahu). Finite verbs take **tiṅ** endings (tip, tas, jhi…).
  Primary derivatives carry their **kṛt** affix (kta, ktavatu, ktvā, lyap, tumun,
  śatṛ, śānac, tavya, anīyar, ṇvul, tṛc…); secondary derivatives their
  **taddhita**. Give the Pāṇinian name plus a plain-English label.
- **Morphology (`morph`)** — state vibhakti + vacana + liṅga (or tense/mood +
  person + number for verbs) in traditional terms with an English gloss.
- **Sandhi** — when a surface form is a euphonic product, note it (and, where
  useful, the operative rule), so the split in `parts[]` is honest.
- **Compound (`compound`)** — classify strictly: tatpuruṣa (incl. its sub-types),
  karmadhāraya, dvigu, bahuvrīhi, dvandva, avyayībhāva — with a correct
  **vigraha** and the member list.
- **Kāraka (`karaka`)** — assign per Pāṇini's kāraka-sūtras: kartṛ, karman,
  karaṇa, sampradāna, apādāna, adhikaraṇa — matched to the actual case and
  governing verb, not guessed from English.
- **`parts[]`** — the morpheme split must be real and complete (prefix(es) +
  root + affix(es); stem + ending), each piece with an accurate gloss; no piece
  conflated or mislabeled. Even particles get a clear, complete, concise gloss.
- **No fabrication** — if a root/affix is genuinely uncertain, give the best
  standard analysis and flag it; never invent a dhātu or pratyaya.

## 7. Faithful rendering — rules against distortion

The English must be **literal and complete**: it renders exactly what the Sanskrit
says — every grammatical element, no more, no less — in natural English. The
recurring failure is *distortion*: silently adding, dropping, or shading meaning.
The rules below name each way that happens and forbid it. They apply to **all**
rendered text — mūla, every commentary voice, the one-line `sense`, and
`ourRendering`. Two scripts enforce the mechanical part and must both pass after
any edit: `node scripts/validate_gita_slots.js` (slot integrity) and
`node scripts/check_gita_terms.js` (term policy, §7.6 + §8).

### 7.1 Do not collapse meaning
Every word and grammatical feature present in `words[]` must surface in the English
— scope/quantifier words (*sarvatra* "everywhere/in all things", *api* "even",
*hi* "for"), connectives, negations, number, gender, voice, person, and case-force.
Never drop a word's force to make a sentence shorter or smoother. A slightly longer
English rendering is correct when that is what keeps the meaning whole.

### 7.2 Render the word; do not interpret it
Translate the literal word in the grammatical form it actually has — participle as
participle, passive as passive, the case in its force. Do not replace a word with
an interpretation of it. *yukta* (kta of √yuj) is "yoked / joined / united", **not**
"absorbed" (which imports an immersion the word does not state).

### 7.3 Do not insert words the Sanskrit lacks
Add nothing not in the text. If a word's complement is implied (elliptical) in the
Sanskrit, keep it implied in the English. *yukta* is "yoked", **not** "yoked in
yoga" — "yoga" is not in the word; the implied object stays implied, and the
glossary link carries the depth. Any genuinely needed clarifier belongs in the
word-card / glossary, never silently in the line. (No `[bracket]` inserts.)

### 7.4 Choose the sense that fits the usage — and keep the root's image
A word has a range of senses; pick the one the context actually uses, grounded in
the commentators (their Sanskrit + our renderings sit beside each unit). Keep the
image the root carries when the Sanskrit carries it; do not flatten it, and do not
add an image the Sanskrit lacks.
- *saṃ-√yam* → "rein in / curb" (the sense-horses), not flat "restrain".
- *√car* taking an object (*viṣayān caran*) → "engaging the sense-objects", not the
  merely spatial "moving among" — the philosophical sense is engagement, not
  locomotion. (Where *√car* is intransitive of the wandering senses, "roving" is
  right — so judge per usage.)

### 7.5 Match the connotation; do not shade it
Pick the English whose connotation matches the Sanskrit's, and reject words that
import a wrong overtone. *vidheya* ("to be directed, governable") is "governable /
self-governed", not "biddable" (servility). *sneha* is the warm love-bond
"affection" (Madhusūdana: the bond by which another's loss/gain becomes one's own),
not the mild "fondness".

### 7.6 Never render one Sanskrit word as a *different* Sanskrit word
A word is rendered either in its **own** IAST or in English — never as a different
Sanskrit term. Do not print *saṅga* for *sneha*, or *manas* for *cetas*. Distinct
near-synonyms get **distinct** English words; never collapse two Sanskrit words into
one (e.g. *sneha* "affection" vs *prīti* "fondness"; *spṛhā* "longing" vs *tṛṣṇā*).

### 7.7 Render the same word the same way
Translate a given word consistently across the mūla and all commentaries, unless
the context genuinely shifts its sense. Inconsistency (e.g. *saṅga* as "saṅga" in
one place, "attachment" in another) is itself a distortion.

## 8. Preserve or translate — which words stay Sanskrit

Keep a term in Sanskrit only when a plain English word cannot carry its meaning.
Decide per term and apply it consistently; the lists below are the current
decisions — extend them deliberately, never ad hoc.

- **Preserve in IAST** (irreducible philosophical load / root-imagery English can't
  hold), glossary-linked: *rāga, dveṣa, guṇa, dharma, kāma, saṅga, prajñā, buddhi,
  manas, indriya, karma, jñāna, yoga, rasa, ahaṅkāra, tṛṣṇā, samādhi, mokṣa,
  saṃsāra*. Established renderings kept: *ātman* → "the self", *brahman* → "Brahman".
- **Translate** (plain English carries it fully): *krodha* → anger, *bhaya* → fear,
  *moha* → delusion, *duḥkha* → sorrow, *sukha* → pleasure, *spṛhā* → longing,
  *sneha* → affection, *prīti* → fondness, *vidheya* → governable / disciplined.
- **Use multiple English words when one will not do** — two precise English words
  beat one lossy word, and beat needlessly keeping the Sanskrit. Keep the Sanskrit
  only when even several English words would still distort.
- **Don't bloat** the reader with Sanskrit English can carry; **don't flatten** to
  English a term that genuinely needs its Sanskrit.

### The decision procedure (apply to every term)
1. List the word's attested senses (dhātu + usage + the commentators *here*).
2. Does a plain English word — or a short phrase — carry the operative sense
   without adding, dropping, or shading anything (§7.1–§7.5)? If yes, translate.
3. If no English fits without distortion (irreducible load), keep it IAST and
   glossary-link it.
4. Whatever you choose: apply it consistently (§7.7) and never as a different
   Sanskrit word (§7.6). When a single best choice is genuinely unclear, leave the
   current rendering and flag it rather than guess.
