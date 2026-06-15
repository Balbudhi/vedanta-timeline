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
