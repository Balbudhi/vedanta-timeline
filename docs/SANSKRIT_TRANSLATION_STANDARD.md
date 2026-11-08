# Sanskrit translation standard

How Sanskrit is translated and presented on this site. This is the **norm going
forward** for every Sanskrit text we render — mūla (root text) *and* commentary.

**Authority (amended 2026-11-08).** This document is the **single governing
standard** for every Sanskrit reader on the site. Its preserve-or-translate
decision table — for the Gītā, the Gītā lexicon — is
`data/glossary/term_policy.json` (§8): the table holds the decided rows; this
document holds the rules by which rows are made and applied. Project plans (for the
Gītā, [`GITA_FULL_TRANSLATION_PLAN.md`](GITA_FULL_TRANSLATION_PLAN.md)) carry scope,
stages, process, gates and measured numbers; they do not restate or change rules. A
deliberate deviation is recorded only by amending the section of this document it
changes. Checkers (`scripts/check_gita_terms.js`, `scripts/validate_gita_slots.js`,
the chapter builders and the job validators) enforce this document and the table and
nothing else; where a checker disagrees with this document, the checker is wrong and
is corrected. The Gītā word-card contract formerly in `GITA_CARD_MEANING_SCHEMA.md` is
folded into §2 and §3. Agent brief templates for the Gītā are in `docs/gita_briefs/`.
Presentation (layout, surfaces, widths, stacking) belongs to `UI_DESIGN_STANDARD.md`;
this document says what a card must contain.

The reader engine is `assets/gita.js` (`window.GitaReader`). The earlier Gītā readers
(`gita/sthitaprajna/` 2.54–72, `gita/kama/` 3.36–43, `gita/ch5/`) predate the term
table and contain known errors (§10): they show the data format, not the standard.
`gita/ch12/` becomes the reference for word cards once the owner has read it.

Sections marked *(new 2026-11-08)* or *(amended 2026-11-08)* record the consolidation
after the chapter-12 pilot (`GITA_CH12_PIPELINE_AUDIT.md`,
`TRANSLATION_PRECEDENTS_SURVEY.md`) and the owner's directions of that day.

## 1. Principle: literal, word-by-word, faithful to the grammar

The truest reading is the literal one. We translate the grammar that is actually
present and make it inspectable, rather than paraphrasing.

- **Literal, not interpretive.** No inserted nouns or subjects the Sanskrit does
  not have (e.g. do not render an implied 3rd-sg. masculine subject as "a man" —
  use "he"). Respect gender, number, person, mood and voice (passives stay passive;
  statements stay statements, §7.8). Supplied copulas ("is") for nominal sentences
  and the other function words of §7.15 are fine; content words are never supplied.
- **Every choice is significant.** Epithets and proper names are translated with
  their etymology (Keśava, Pārtha, Kaunteya, Mahābāhu…), not left as opaque names
  (form: §7.10).
- **Untranslatables stay Sanskrit** and link to the glossary, but only when the
  three tests of §8 hold for that sense; `translatable: false` suppresses a forced
  English gloss.
- **Explicit ambiguity.** Where a form or construal is genuinely ambiguous, say so
  on the card (§6.5 forks); never fake a confident single parse.
- **Grounded, never fabricated.** Sanskrit is taken verbatim from cited sources
  on disk (`data/sources/...`); transliterate faithfully; cite every source. If a
  text cannot be sourced, omit it and say so — do not invent Sanskrit.
- **Our English is our own** *(new 2026-11-08)*. It is made from the Sanskrit
  sources and the English dictionaries, never from other translations (§9). It aims
  to be richer, freer and more exact than the published translations, within §7.

## 2. The reading UX (what `GitaReader` renders)

- **Source script, then IAST, then English.** For Sanskrit, display the
  source-script saṃhitā line in Devanāgarī first; below it show the interactive
  IAST **pada-pāṭha** (sandhi-resolved, space-separated — every word a tappable
  token); below that show the **literal English**. Author and retain both
  top-level `devanagari` and `words[].deva`; never substitute a generated script
  conversion for a verified source witness.
- **Tap a word → a card** *(amended 2026-11-08)*. The card shows, in this order,
  each section omitted when empty:
  1. the word in IAST (its Devanāgarī `deva` may stand beneath it);
  2. its contextual gloss (`gloss`);
  3. the **term line**, when a table row applies, in plain words — e.g. "Kept in
     Sanskrit wherever the Gītā uses it in this sense" or "Rendered 'clinging'
     wherever *saṅga* has this sense" — written from the row, with no process
     vocabulary (§3.4);
  4. the **morpheme pieces, each translated** (`pra-` "forth" + `√bhāṣ` "to speak");
  5. the root with gaṇa and pada, the formation (pratyaya), the grammar in plain
     English with the case's force (genitive → "of"), the syntax (kāraka), and the
     samāsa-vigraha for compounds;
  6. the **sandhi** that produced the printed form;
  7. **Meaning** (§3.1 `meaning`, §6.4): the root's concrete image; the meaning lines
     in their category order, each naming its source; the English used in the line
     and why; and the other renderings a reader will meet. Whether lines of category
     `synthesis` are shown publicly is an open owner decision (plan §2.2); until it
     is made they may be recorded but are not published;
  8. **Other readings**: the `display` sentence of every fork whose `words` names
     this card (§6.5);
  9. the glossary link(s) for technical terms.

  Under the verse, the reader lists every open fork (`open: true`) by its `display`.
  A grammatical claim that could not be located in the sources is stated on the card
  in reader words ("not located in the grammatical sources"), never by an internal
  label. The card stays compact under `UI_DESIGN_STANDARD.md` (Contextual surfaces:
  one anchored, non-modal word card, max 300px); a section too long for it opens in
  the persistent reference panel, and nothing essential exists only in a popup. A
  field the target reader cannot render is not public content: a builder refuses data
  whose required display (meaning, forks) the reader cannot show.
- **Cards open on CLICK only** (never hover — hover obscures the text).
- **Cards are contextual, not modal.** A card is anchored beside its word and
  closes when the reader taps the same word, clicks away, presses Escape, or
  scrolls. It must not require a close button or support dragging. A persistent
  glossary/reference panel is a separate interaction; follow
  `docs/UI_DESIGN_STANDARD.md` for that distinction.
- **Bidirectional highlight**: tapping a Sanskrit word highlights its English,
  and tapping an English phrase highlights + cards its Sanskrit word.
- **Commentary gets the identical treatment.** A commentator's Sanskrit is
  word-by-word interactive exactly like the mūla (same `words[]` + slotted
  `english`). Commentary is shown **voice by voice**: a multi-select, colour-coded
  chooser (each commentator a colour); equal, no ranking, ordered chronologically.
  Each commentator's name links to their Thinker entry in the timeline.
  *(Amended 2026-11-08.)* A reader's plan may decide that a reader is mūla-only (the
  Gītā: plan L1). The commentators then appear only as named, located meaning lines
  on the cards (`commentator` category, §3.1) and as the traditions of fork
  construals, not as a voice layer.
- **Quoted English must keep its source boundary.** If a commentator gives an
  English translation, render that exact wording as theirs. If the site supplies
  a literal English line for an otherwise untranslated Sanskrit quotation, mark
  that line at the quote itself as site-generated and do not present it as the
  commentator's translation or quotation.
- **A source-preserving commentary view may omit visible site English.** When
  the product decision is to distinguish the commentator's translations by
  presence rather than labels, apply one rule to the entire reader: keep the
  commentator's English in its natural prose position and make every complete
  quotation a single witnessed source line. When that line is in Devanāgarī,
  keep IAST, literal meaning, and grammatical analysis in the word card rather
  than duplicating them as a second visible row. Retain the reviewed site
  rendering in data, but do not repeat or mix it into the attributed reading
  surface.
- **Normalize the public script, not the witness.** In a Devanāgarī-first
  commentary reader, a complete quotation printed only in Roman Sanskrit may
  be displayed in Devanāgarī only after its entire reviewed word population can
  deterministically produce that line. Preserve the printed Roman string in
  the source record and expose reviewed IAST in the word interaction. Never
  transliterate undiacritized OCR blindly, and never let the script used by the
  scan create a second public quote style.

### 2.1 Printed notes are claim-level evidence

A printed footnote, endnote, or source quotation is part of the author's
argument. Preserve the exact call-to-note relationship instead of collecting
notes at the end of an entry or turning them into free-standing decorative
quotation blocks.

- Attach the printed marker to the precise clause or sentence it marks and put
  the corresponding note immediately after that claim.
- Preserve the author's note text and source attribution. Editorial corrections
  or witness qualifications must be separate, concise, and unmistakably the
  site's.
- Sanskrit inside a note receives the same verified Devanāgarī and interactive
  word analysis as Sanskrit in the main commentary. The note's function remains
  evidentiary: it must visibly defend the claim that called it.
- Builders must validate the closed population of calls and notes, stable IDs,
  source order, and one-time placement. A detached, duplicated, silently moved,
  or uncalled note is a build failure.

## 3. Data schema *(amended 2026-11-08)*

### 3.1 Per word (mūla and commentary alike)

```jsonc
{
  "i": 0,                       // 0-based, contiguous, matches english {i:…} slots
  "iast": "sthitaprajñasya",    // pada-pāṭha citation form (sandhi resolved)
  "deva": "स्थितप्रज्ञस्य",        // Devanāgarī citation form (required; may be shown under the card headword)
  "gloss": "of one whose wisdom is steady",
  "parts": [                    // morpheme pieces, each translated (the layperson layer)
    {"form": "sthita", "gloss": "stood firm, steady"},
    {"form": "prajñā", "gloss": "wisdom, insight"}
  ],
  "stem": "sthita-prajña", "root": null,           // root as "√bhāṣ (bhvādi, 1Ā)" — gaṇa and pada required (§6)
  "rootGloss": null,                               // the Dhātupāṭha artha in plain English, when a root is given
  "affix": "ṅas (ṣaṣṭhī ekavacana)",               // technical Pāṇinian name
  "morph": "gen. sg. masc.",                        // rendered to plain English in the card
  "karaka": "sambandha (relational genitive)",
  "compound": { "type": "bahuvrīhi", "vigraha": "sthitā prajñā yasya saḥ", "members": ["sthita","prajñā"] },
  "sandhi": "…",                // when the printed form is a sandhi product: the junction and its sūtra(s)
  "glossaryKey": "sthitaprajna",                    // a key/alias present in data/glossary/, else null/omit
  "translatable": true,                             // false → render plain, no forced gloss
  "term": { "lemma": "prajna", "sense": "…" },      // required when a table row matches (§8.3); see below
  "note": "optional, reader-facing: an honest ambiguity or a needed clarification",
  "meaning": { /* see below */ }
}
```

`term` is `{lemma, sense}` naming the row that fixes this word's rendering. A
compound whose members match several rows carries a list `[{lemma, sense, member}]`
(`member` = the index in `compound.members`, or null for the whole word). The pilot
builder reads only the object form; the list form is the agreed extension (audit
D7) and is valid once the builder reads it.

**`meaning`** — the word's meaning layer (formerly `GITA_CARD_MEANING_SCHEMA.md`):

```jsonc
"meaning": {
  "image": "√ās 'to sit' with upa- 'near': to sit near, attend",      // the root's concrete image, one line
  "lines": [                                                          // ordered by category as below; 1–8 lines
    { "cat": "lexical",     "text": "to attend upon, wait on, serve; to sit near in reverence", "who": "Monier-Williams", "locus": "sources/raw/upstream_data/kosha/mw.json#…" },
    { "cat": "nirvacana",   "text": "upāsanā is going near the object and staying with it long, a stream of one thought like poured oil", "who": "Śaṅkara on 12.3", "locus": "vedanta-timeline/data/sources/…/shankara_gita_bhasya.txt:8411" },
    { "cat": "commentator", "text": "dhyāyanti — they meditate", "who": "Śaṅkara on 12.1", "locus": "…" },
    { "cat": "usage",       "text": "the same verb takes a sacrifice (4.25) and a teaching (12.20) as object", "who": "Gītā" },
    { "cat": "reception",   "text": "\"seek after\"", "who": "Sri Aurobindo (Roy 1938)" },
    { "cat": "synthesis",   "text": "the site's labelled reading, if any" }
  ],
  "rendering": "attend upon",                 // the English used in the line for this word
  "why": "keeps 'sit near' and 'serve'; 12.6 separates meditating (dhyāyantaḥ) from upāsate, so not 'meditate'",
  "alternatives": ["worship", "meditate on", "wait upon"]   // other renderings a reader will meet, without attribution of copyrighted text
}
```

Categories, in display order (a closed list; how they carry §6.3's six categories is
stated in §6.3): `formation` (only when the grammar fields do not already say it),
`lexical` (kośa and dictionary senses, including the Dhātuvṛttis' root senses),
`nirvacana` (a transmitted or commentator's semantic etymology), `commentator` (a
classical commentator's gloss on this word in this verse), `usage` (the text's own use
of the word, here and elsewhere), `reception` (later reception and modern translators:
a translator is named with at most a few words of quotation, §9), `synthesis` (the
site's own labelled reading). Commentators who give the same gloss share one line with
all names in `who`.

`meaning` is required on every card that has a root or a compound and on every
preserved term; it is optional on particles, pronouns and names (names carry their
etymology in `parts`). `rendering` equals the text of the slot that carries the word.

### 3.2 Per unit (verse, or commentary passage)

`locus`, `speaker`, `meter`, `iast` (saṃhitā), `devanagari`, `english` (the slotted
literal rendering — `"{0:…} {1,2:…}"` referencing `words[].i`), `sense` (one plain
paragraph, no interpretation beyond the words; stored, and not rendered in the Gītā
readers by the owner's design), `grammar` (`karakaSummary`, `verbalModality`), and
`forks[]`:

```jsonc
"forks": [ {
  "at": "akṣaram avyaktam",                     // the words concerned, as printed
  "words": [3, 4],                              // the card indices the fork concerns
  "construals": [ { "reading": "…", "grammar_basis": "…", "evidence": ["file:line", "…"], "traditions": ["Śaṅkara", "Rāmānuja"] } ],
  "followed": 0,                                // index of the construal the line follows
  "reason_class": 4,                            // 1–5, §6.5
  "reason": "…",
  "open": false,                                // true exactly when reason_class is 5
  "display": "The compound can also be read as 'unfastened' (a-sakta); every commentator reads 'fastened to'."   // one or two reader-facing sentences
} ]
```

Commentary entries carry the same complete source-script, `words[]`, and `english`
fields alongside their verbatim Sanskrit and our `ourRendering`. A reader may not
show a commentary as source-script complete until that data has been verified
against its witness.

### 3.3 Records that stay in the production files

The producer's record per word also carries, outside the public file:
`word_class` (`content` | `particle` | `pronoun` | `name` | `copula`), which decides
which records are required; `evidence[{claim, locus, quote}]` (one shape); `fallback[{claim,
kind}]` with `kind` ∈ `root | pratyaya | compound | sense | syntax | other`; and, for
every content word, `wording{sense_description, plain, rich, chosen, why,
candidates[], connotation}` where `plain` and `rich` are each `{word, source, locus,
definition}` from the headword's own dictionary entry, `rich` may instead be a
formation record `{formation, parts[{part, sense, source}], relation, paraphrase,
why_no_attested_word}` (§7.17), and `chosen` is `plain` or `rich`. These records
become public only if a reader renders them and they contain no text from another
translation (§9).

### 3.4 Public-text rule *(new 2026-11-08)*

`english`, `gloss`, `parts[].gloss`, `rootGloss`, `note`, `meaning.*`,
`forks[].display`, `sense` and `grammar.*` are public. They are written for a reader
of the site and contain no pipeline vocabulary: no "policy row", "term_policy",
"lexicon row", "lead", "owner", "gate", "shard", "job", "producer", "reviewer",
"fallback", "pilot", finding numbers (F12), or section numbers of internal documents.
They say what the word means and why it is rendered so. The builder refuses a reader
that violates this.

### 3.5 Invariants (CI-checkable, every reader)

`i` contiguous from 0; every `english` `{i:…}` slot resolves to a real word index and
every index is slotted once; the concatenated `iast` tokens faithfully represent the
source `sanskrit` (sandhi resolution only — nothing dropped or invented); every
`glossaryKey` resolves to a file in `data/glossary/`; every word a table row matches
carries `term`, and every `term` resolves to a row and sense; every root names gaṇa and
pada; every fork's `words[]` resolves, and `open` is true exactly when `reason_class`
is 5; `meaning` is present where §3.1 requires it and `meaning.rendering` matches the
word's slot; no public field carries pipeline vocabulary (§3.4); a reader marked
complete has no `fallback` of kind `root`, `pratyaya` or `compound`.

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
every technical term in the text and its commentaries is covered. Every preserved
sense in the table (§8) has a glossary entry before its row is used.

## 5. How to apply this to a new text *(amended 2026-11-08)*

1. **Witnesses.** Acquire the mūla (+ commentaries) verbatim into `data/sources/...`
   (cite).
2. **Packets and inventory (code).** Build per-unit packets — pada candidates,
   Dhātupāṭha entries, cited derivation chains, the commentators' per-word glosses,
   hits in the kośas, Dhātuvṛttis and Nirukta (§6.4), concordance of every occurrence
   — and the work-wide lemma inventory.
3. **Lexicon first: meaning is decided before production.** Each content
   lemma-sense is decided once across all its occurrences in the work, from a dossier
   (root image, senses per occurrence, the meaning sources of §6.4, the three tests of
   §8, plain/rich candidates of §7.17, English forms per grammatical category,
   distinctness), and reviewed by an independent lexicon reviewer. The decided rows
   form the table (§8.3), which is frozen by content hash for a production run.
4. **Production.** Per unit: the analysis of every word, the slotted line, forks,
   wording records and the card's meaning selections, taken from the lexicon. The
   lexicon is binding for sense; a disagreement is a row proposal, never a silent
   departure. Code expands analyses into cited cards wherever a script exists.
5. **One review pass** (§5.1) by an independent reviewer in a fresh context; the
   blind check against other translations comes last in it (§9).
6. **Fixes** by the same producer, resumed with the findings; re-review by the same
   reviewer as a diff check. Nobody else edits a producer's file.
7. **Build** fail-closed; every validator passes.
8. **Publication** is provisional. The owner's reading of the published text is the
   taste review; its changes flow back as lexicon edits (§8.3) followed by a
   mechanical sweep of every affected occurrence and a diff re-review.
9. Glossary coverage (§4). Audio per `docs/AUDIO_ALIGNMENT_STANDARD.md`; the
   supported granularity is verified verse-level timing, not inferred word or pada
   synchronization.

The Gītā's stages, job queue, numbers and briefs: plan §7 and `docs/gita_briefs/`.
Deviations from this standard should be deliberate and noted.

### 5.1 The single review pass *(new 2026-11-08)*

One reviewer checks, per unit and in one pass: (1) **grammar** — recompute pada, root
with gaṇa and pada, affix, compound and vigraha, kāraka, and try the plausible wrong
alternative; (2) **form in the line** — every mood, voice and non-finite form in the
line equals the card (§7.8–§7.9); (3) **meaning** — the line's word carries the
lexicon sense, the card shows the root image, the operative sense with its locus and
every distinct commentator gloss on the word in this verse (§6.4), and no traditional
sense is dropped without a recorded reason; (4) **readability** — the line read aloud
without a card parses on first reading (§7.16); (5) **policy fit** — whether the row
fits this occurrence (compliance itself is checked by code); (6) **forks** —
admissible construals, reason class, open state, display (§6.5); (7) **public
surface** — the rendered verse at phone width: process vocabulary, dangling
references, missing meaning or fork display; and last (8) the **blind check** against
other translations (§9). Choices made by the lead are reviewed like any other.

Severity: S1 — wrong grammar, a dropped or added meaning, a mood or form change, a line
that does not parse, a disfavoured device without a row (§7.16), process vocabulary in
a public field; S2 — richness lost that the lexicon or sources document; S3 — style.
A unit with an open S1 is not accepted.

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

### 6.1 Authority and tool boundary

"Pāṇinian" describes an analysis established from the witnessed text through
Pāṇini and the traditional grammatical sources; it does **not** describe output
merely produced by a Sanskrit parser or morphology library.

The required authority chain is: exact cited textual witness and context →
reviewed pada division → *Aṣṭādhyāyī* rule sequence → *Mahābhāṣya*, traditional
vṛtti/commentary, Dhātupāṭha, or Gaṇapāṭha where adjudication is needed → reviewed
literal English. Record the actual sources used. For a quotation, distinguish
the quoted author's translation from the site's grammatical explanation.

OCR, modern dictionaries, Vidyut, Sūtrakṛt, `prakriya`, other parsers, and
language models are non-authoritative audit aids. They may locate candidates or
flag disagreements, but may not establish a reading, choose a parse, provide a
public gloss, or certify correctness. Agreement between tools is not a
publication gate. Any analysis originating with those tools remains provisional
until independently re-derived through the authority chain above.

For closed finite readers, every public token must pass that review; sampling,
confidence scores, and aggregate parser accuracy are insufficient. Unresolved
analysis stays unpublished or is explicitly displayed as unavailable. Builders
must fail closed rather than expose provisional cards. See
`docs/GRAMMAR_ENGINE_INTEGRATION_PLAN.md` for the repository-wide tooling
boundary.

For the grammatical texts themselves, use the shared read-only source library
at `/Users/eeshan/Dev/prakriya/sources/` first. Read its `README.md` and
`manifest/clean_witnesses.json`, then consult the relevant Sanskrit under
`sources/primary/` (Aṣṭādhyāyī, Dhātupāṭha, Gaṇapāṭha, Kāśikā,
Mahābhāṣya, Siddhāntakaumudī, Uṇādi, Nirukta) and the paired `sources/raw/`
witness when collation matters. Do **not** run or rely on the unfinished
`prakriya` interpreter, generated form tables, projections, or traces. The
source library is authoritative evidence; the software is not.

A derivation chain may be cited by code from a reviewed chain table (a source
artefact built once from the Siddhāntakaumudī prakaraṇas and independently
reviewed) when the agent has asserted the analysis the chain belongs to *(new
2026-11-08)*. The agent still makes every analytical claim; code supplies the
citation. Cite the Kāśikā only where its example, counter-example or restriction
decides the analysis.

### 6.2 Parallel derivations and traditional nirvacanas

A word card must not silently choose one valid derivation and suppress another.
Show every independently supported grammatical formation and every attested
traditional *nirvacana* in parallel, with each reading's own segmentation,
root(s), affixes or compound analysis, meaning, evidence locus, and
qualification.

Keep the categories explicit. A regular grammatical formation is not the same
claim as a traditional semantic *nirvacana*, and an author's theological or
symbolic interpretation is not thereby an etymology. The latter remains in the
author's attributed prose unless a cited traditional source establishes it as
a transmitted *nirvacana*. A reading that is plausible but not yet source-backed
must be withheld or marked unresolved; it may not displace an established
analysis. Closed readers must validate the complete candidate population and
the complete public parallel-derivation population.

### 6.3 Intentional literature and the Aurobindonian depth-reading

This project does not treat Sanskrit philosophical words as inert labels whose
"ordinary" referent exhausts their force. Its governing hermeneutic is
Aurobindonian: preserve the outer, grammatical, narrative sense and read the
same verified language for its inward psychological and philosophical work.
Sri Aurobindo develops this method for the Veda as an intentional system of
double values. We extend the method—without pretending that he commented on
every later text—to Sanskrit philosophical literature whose compounds,
nirvacanas, names, and narrative structures demonstrably activate inherited
semantic fields.

The default presumption is therefore **intentional semantic activation**:

- if a grammatical formation, lexical sense, or transmitted nirvacana predates
  the work, it belonged to the inherited language available to the author;
- if the surrounding argument, image, name, or plot activates that meaning, the
  reader presents it as an intentional literary and philosophical layer unless
  contrary evidence exists;
- lack of proof that the author consulted one named grammatical book is not
  treated as proof that the inherited meaning was unavailable or irrelevant;
- a reading first attested later is preserved as reception history, not silently
  backdated into authorial intention; and
- the surface referent remains true. An inward or symbolic register does not
  erase the person, battle, ritual, deity, object, or event through which the
  text speaks.

This is not an "Aurobindo versus academia" choice. Critical philology establishes
the exact wording, witness families, chronology, and direction of transmission.
The depth-reading begins from those results and asks what the verified language
is doing as intentional literature. A public card must accordingly separate:

1. regular grammatical formation;
2. attested lexical senses;
3. pre-existing traditional nirvacanas;
4. activation by the present narrative or argument;
5. later reception and commentary; and
6. the site's explicitly labelled synthesis.

Do not suppress a supported meaning merely because another meaning is more
common in running prose. Do not collapse these categories into a fabricated
single etymology either. Chronology and evidence qualify a meaning; they do not
make the rest of the semantic field disappear.

*(Amended 2026-11-08.)* On the card the six categories are carried by the closed
`meaning` line categories of §3.1: 1 → `formation` (and the grammar fields);
2 → `lexical`; 3 → `nirvacana`; 4 → `usage` (the text's own use of the word, which is
the evidence of activation) together with the line's `rendering` and `why`;
5 → `commentator` (a classical commentator on this verse) and `reception` (later
authors and modern translators); 6 → `synthesis`. A reading first attested in a
modern author (for example a twentieth-century resegmentation) is `reception`, never
`nirvacana`. Sri Aurobindo's renderings and discussions of a verse are reception and
exegesis: they are recorded as such, they never decide a line, and his register is a
model of deliberate English (§7.17), not a source of meaning.

### 6.4 The meaning layer and its sources *(new 2026-11-08)*

The meaning layer is made from the whole Sanskrit source library, not only from
grammar. For every content lemma the lexicon dossier (§5 step 3) and the card draw on:

- **root senses** from the Dhātupāṭha and the Dhātuvṛttis — Mādhavīya Dhātuvṛtti,
  Kṣīrataraṅgiṇī, Dhātupradīpa, Daiva with Puruṣakāra;
- **nirvacanas** from the Nirukta and Nighaṇṭu, the Uṇādi vṛtti, and the
  commentators where they present an etymology;
- **synonym fields and senses** from the kośas — Amarakośa (with the Amaraviveka and
  Kṣīrasvāmin's Amarakośodghāṭana), Halāyudha, Vaijayantī, Yādavakośa — and the
  encyclopaedic dictionaries Śabdakalpadruma and Vācaspatyam, alongside Apte and
  Monier-Williams;
- **the commentators' per-word glosses** on each verse, extracted by code from every
  commentary on disk;
- **the text's own usage** of the word across all its occurrences.

The library is `/Users/eeshan/Dev/prakriya/sources/` (`primary/etymology/`,
`primary/lexica/`, `raw/upstream_data/kosha/`). A closed reader's card shows, for
every content word, the root image, the operative sense with its source locus, and
every distinct commentator gloss on that word in that verse, labelled by category. A
gloss gathered as evidence but kept off the card is a defect, not a saving. Every card
with a root or a compound shows at least one traditional or kośa voice. These sources
are evidence for meaning under §6.1: they locate and attest senses; the choice of
sense is the agent's, reviewed.

### 6.5 Forks: more than one admissible construal *(new 2026-11-08; moved from plan §13.1–13.2)*

A fork is any place where more than one construal is **grammatically admissible**: a
pada division, a sandhi resolution, a case force, a compound type, the referent of a
pronoun, an attested sense of a lemma, the scope of a negation, or a sentence boundary
across verses. Each fork records the construals with their grammar basis (sūtra,
kośa, parallel usage inside the text) and evidence loci, which traditions take which
construal, the construal the line follows, the reason class, the reason, and a
reader-facing `display` attached to the cards in `words` (§3.2).

Admissible reasons to resolve a fork, in this order and only these:

1. **Grammar excludes it**: a construal breaks Pāṇini (cite the sūtra) or sandhi.
2. **The text's own usage** settles the sense (cite the verses).
3. **Kośa**: the sense is not attested for the lemma in the kośas and dictionaries.
4. **English can stay open**: the English admits the same readings the Sanskrit
   admits.
5. **English forces a choice**: when no English keeps both readings, follow the
   reading with the strongest grammar-only support, show the alternative on the card
   with its traditions named, and mark the fork `open: true`.

A school's reading is **evidence that a construal is attested**, never a reason to
prefer it; no reason of the form "school X reads it so" is admissible. Where grammar
underdetermines and English forces a choice, the reader sees both. Readings attested
only in later reception are kept as reception (§6.3), not promoted into the fork.

## 7. Faithful rendering — rules against distortion

The English must be **literal and complete**: it renders exactly what the Sanskrit
says — every grammatical element, no more, no less — in natural English. The
recurring failure is *distortion*: silently adding, dropping, or shading meaning.
The rules below name each way that happens and forbid it. They apply to **all**
rendered text — mūla, every commentary voice, the one-line `sense`, and
`ourRendering`.

*(Amended 2026-11-08.)* The mechanical part is enforced by `node
scripts/validate_gita_slots.js` (§3 invariants), `node scripts/check_gita_terms.js`
(§7.6 and §8) and each reader's builder in check mode, all run by
`scripts/run_checks.sh`. The term checker reads only `term_policy.json`. Its legacy
hard-coded PRESERVE/TRANSLATE tables (which still preserve *krodha*, against §8) are
being retired; until they are removed, where they disagree with §8 and the table, this
document governs and the disagreement is reported, not obeyed.

### 7.1 Do not collapse meaning
Every word and grammatical feature present in `words[]` must surface in the English
— scope/quantifier words (*sarvatra* "everywhere/in all things", *api* "even",
*hi* "for"), connectives, negations, number, gender, voice, person, and case-force.
Never drop a word's force to make a sentence shorter or smoother. A slightly longer
English rendering is correct when that is what keeps the meaning whole.

### 7.2 Render the word; do not interpret it
Translate the literal word in the grammatical form it actually has — participle as
participle, passive as passive, the case in its force, the mood it has (§7.8–§7.9).
Do not replace a word with an interpretation of it. *yukta* (kta of √yuj) is "yoked /
joined / united", **not** "absorbed" (which imports an immersion the word does not
state).

### 7.3 Do not insert words the Sanskrit lacks
Add nothing not in the text. If a word's complement is implied (elliptical) in the
Sanskrit, keep it implied in the English (§7.14). *yukta* is "yoked", **not** "yoked
in yoga" — "yoga" is not in the word; the implied object stays implied, and the
glossary link carries the depth. Any genuinely needed clarifier belongs in the
word-card / glossary, never silently in the line. (No `[bracket]` inserts.) Function
words English grammar needs are not insertions (§7.15).

### 7.4 Choose the sense that fits the usage — and keep the root's image
A word has a range of senses; pick the one the context actually uses, grounded in
the commentators and the meaning sources (§6.4). Keep the image the root carries when
the Sanskrit carries it — what the body or the hand does: √ās *sit*, √yuj *yoke*,
√viś *enter*, √sthā *stand*, √dhā *place* — do not flatten it, and do not add an image
the Sanskrit lacks.
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
The table's `reserved_english` records which English word belongs to which lemma. A
word chosen only because the better one is reserved for another lemma is a finding
unless the meaning itself supports it; the remedy is a better word, not elimination.

### 7.7 Render the same sense the same way *(amended 2026-11-08)*
The unit of consistency is the (lemma, sense) pair, not the string. Each pair is
decided once in the table (§8.3) with its rendering, the English forms it may take
and its forbidden renderings, and every occurrence in every reader is checked
against that one row. When one string is used in two senses, both senses are rows,
and the card states the sense. A string-constant rule would be less consistent in the
sense that matters: it would render *karmaṇi* in 2.47 as "karma" while every
commentator glosses it as the act. Inconsistency within a word's own card is also a
distortion: card glosses may give the range but must not contradict the slot (no "the
mind" in the gloss of a word whose slot prints *manas*).

### 7.8 Mood and clause type *(new 2026-11-08)*
Render the mood and clause type that are present. An indicative stays a statement,
an optative a wish or prescription ("should"), an imperative a command. Never print a
statement as a question: the echo-question device of the chapter-12 pilot ("you are
not able … ?") is retired. A question mark needs an interrogative word or particle in
the Sanskrit (*kim*, *kva*, *katham* …).

A conditional is rendered as a conditional. Where a particle carries an attested
conditional sense, "If" renders that particle and is not an insertion: *atha* with an
indicative protasis may be rendered "If …, then …" — Apte s.v. *atha*, sense 3: "If,
supposing, now if, in case, but if … oft. followed by ततः", citing Bg 12.9 and 12.11
(`ap90.json#795`); the same holds for *cet*, *yadi* and *atha cet* (2.33, 18.58). An
indicative protasis that continues such a series without its own particle, and that
the commentators construe as a condition, may take "If" as a supplied function word
(§7.15): 12.10 *abhyāse 'py asamartho 'si*, which Śaṅkara construes "… aśakto 'si,
tarhi mat-karma-paramo bhava" (`shankara_gita_bhasya.txt:8520`). The protasis keeps
its indicative mood either way.

### 7.9 Non-finite forms *(new 2026-11-08)*
ktvā / lyap → "having …"; kta → the past participle; śatṛ / śānac → "-ing"; tumun →
"to …"; kṛtya (tavya, anīyar, yat) → "to be …". A kta in active (kartari) sense of a
verb of posture or state (ā-√śri, ā-√sthā, √sthā, ā-√viś, upa-√āsad) renders the
resulting state as English does, with the stative participle or adjective ("leaning
on", "standing in", "seated"), because the English past participle of such verbs is
not used actively ("leant on my yoga" misreads); the card names the kta. Decided
2026-11-08: 12.6 *saṃnyasya* → "having laid down … in me"; 12.11 *āśritaḥ* → "leaning
on" under the stative clause. Agent forms (tṛc, ṇvul, ṇini) take an
attested English agent noun of the same sense and register (found by §7.17
discovery); where none exists, a recorded formation (§7.17) or a construction decided
as a row (§7.16) — not an improvised calque. A form change for euphony violates §7.2;
an unavoidable one is explained on the card in reader words.

### 7.10 Epithets and vocatives *(new 2026-11-08)*
Epithets and names that carry a meaning are translated by their etymology: *pārtha*
"son of Pṛthā", *dhanaṃjaya* "winner of wealth", *kaunteya* "son of Kuntī",
*mahābāho* "mighty-armed". A vocative takes "O" with lower case after it ("O son of
Pṛthā"); the card gives the name and its formation in `parts`.

### 7.11 One English word for two Sanskrit words *(new 2026-11-08)*
When one English word renders two Sanskrit words together, it is one multi-index slot
`{i,j:…}` (12.8 *ata ūrdhvam* → `{10,11:henceforth}`). Never split an English word
across slots (`hence}{forth`) and never leave an index unslotted.

### 7.12 Preserved terms inside English syntax *(new 2026-11-08)*
A preserved term is an English noun in the line. It takes the English plural -s
("indriyas", "bhaktas") and articles as English needs. Its IAST follows the witness's
orthography (§8.4). A preserved noun is not forced into an English verb frame to
render a verb of the same root: the verb is translated unless its row records an
owner-approved verbal rendering in `forms` (§8.3), and such a frame otherwise counts as
a disfavoured device (§7.16). (The current table records "bears no dveṣa" for the verb
of *dveṣa* site-wide; it is an owner's taste item.)

### 7.13 Sentences across verses *(new 2026-11-08)*
A sentence may run across verses where the Sanskrit construes it so (12.3–4,
12.6–7, 12.13–14, 12.18–19). The earlier line ends with an em dash and the next begins
in lower case; each verse's slots map only its own words. A disputed boundary is a
fork (§6.5).

### 7.14 Elided objects and complements *(new 2026-11-08)*
What the Sanskrit leaves unsaid stays unsaid: an elided object or complement is not
supplied as a content word. Where English syntax cannot stand without an object, a
pronoun ("it", "them") may be supplied as a function word under §7.15, and the card
notes the ellipsis.

### 7.15 Supplied function words *(new 2026-11-08)*
English function words are allowed: copulas, articles, auxiliaries, prepositions,
infinitive "to", conjunctions and pronouns that English grammar requires. A function
word that renders a word's own form belongs in that word's slot ("of" in a genitive's
slot; "If" in the slot of *atha*); one that English syntax alone needs is unslotted.
Content words — nouns, verbs, adjectives, adverbs — are never supplied.

### 7.16 Readable on first reading; disfavoured devices *(new 2026-11-08)*
Every line must parse as English for a reader who opens no card. Read it aloud; if it
needs a card to be understood, rewrite it. Meaning outranks beauty, but a line that
does not parse is wrong, however literal. Exactness and readability are reconciled by
richer exact English (§7.17), English word order and the constructions §7.8–§7.15
allow — never by adding or dropping meaning.

These devices need an owner-approved row naming the device and its occurrence;
without one they are severity-1 findings:
- agent-noun calques ("the one who lifts up out of …", "relinquisher of all
  undertakings");
- adjectives forced to head a noun phrase English does not form ("this deathless
  accordant with dharma"); ordinary English substantives with "the" ("the
  imperishable", "the unmanifest") are not this device;
- archaic absolute pronouns standing without a verb ("content with whatsoever");
- Sanskrit nouns forced into English verb frames ("bears no dveṣa");
- Sanskrit–English hybrid compounds ("death-saṃsāra").

### 7.17 Register: the plain and the rich candidate *(new 2026-11-08)*
For every content word the wording record holds two candidates:

- **plain** — the plainest exact English;
- **rich** — the richest exact English: a rare, archaic or literary word attested in
  the dictionary stack, verified by the headword's own entry (`lookup.py define
  WORD`; tags obsolete, archaic, rare or dated do not disqualify), or, where the
  Sanskrit is a compound or a root image that no attested word carries, a recorded
  fused (Joycean) formation.

**Choice.** The line takes the rich candidate when it carries the meaning more exactly
*and* still reads clearly on first reading (§7.16); otherwise the plain one. Rarity is
never a reason by itself, to choose or to reject. The record states which was chosen
and why; where the plainest word is also the richest, the record says so.

**Formations.** A formation is admissible only when no attested word or short phrase
is adequate after the whole dictionary stack has been searched (plan §6). It records
its parts with each part's sense and source, the relation between them, a plain
paraphrase and the line it must read in; it is never labelled attested; it is
rejected if it adds an image, agency or claim the Sanskrit lacks. Good formations are
short, transparent and read as English. The reviewer judges the whole formation, not
its parts.

**Worked examples** (chapter 12):
- *Good:* "pangless" for *gatavyatha* (12.16) — attested: Webster 1913, "without a
  pang; painless", citing Byron (`webster1913_pg29765.txt:601678`). A literary word
  that keeps the bodily pang. (The decided line chose the plain "his trembling gone",
  which keeps √vyath's trembling; both are valid records of the rule.)
- *Good:* "houseless" for *aniketa* (12.19) — attested, exact (niketa "house,
  dwelling", negated) and free of the social sense of "homeless"; it replaced the
  stiff "without abode".
- *Good, owner's taste:* "upbearer" for *samuddhartā* (12.7) — a recorded formation
  on the attested verb "upbear" (Webster), the agent noun being ours, because no
  attested agent noun carries "lift up and out".
- *Bad:* "the summit-standing" for *kūṭastha* (12.3) — built on one member-sense of
  *kūṭa* from a thematic list of mountain words (Amarakośa 2.3.89) that no commentator
  reads for this word; it adds an image no source gives. Amarakośa's own definition of
  the lexeme is "ekarūpatayā tu yaḥ kālavyāpī sa kūṭasthaḥ" (3.1.148–149).
- *Bad:* "the undesignable" for *anirdeśya* (12.3) — offered as a formation while the
  attested "indefinable / undefinable" carries the commentators' sense
  (Monier-Williams `mw.json#7100` "undefinable"; Śaṅkara: *na nirdeṣṭuṃ śakyate*). A
  formation requires that no adequate attested word exist.
- *Owner's taste:* "the everywhere-going" for *sarvatraga* (12.3) — the literal
  formation (sarvatra + √gam) — against the attested "all-pervading",
  Monier-Williams's own gloss (`mw.json#260306`).

**Register model.** Sri Aurobindo's English is a model of deliberate register:
principles capitalised (the Immutable, the Unmanifest), abstractions such as
"equality", compound epithets — chosen, not rare for its own sake. It is a model of
how English can carry weight, not a source of meaning: his renderings are exegesis
(§6.3). Adopting one of his devices in a line (for example capitalising a principle)
is a line-style decision for the owner, not a producer's choice.

## 8. Preserve or translate — which words stay Sanskrit *(amended 2026-11-08)*

### 8.1 The rule: three tests

We translate meanings, not strings; the unit is the (lemma, sense) pair (§7.7). A
word is kept in Sanskrit (IAST, glossary-linked) for a given sense only if **all
three** hold:

1. **It is a term of the text's own system in that sense**: the text defines,
   enumerates or argues about it as a category.
2. **No English word or short phrase carries that sense without adding, dropping or
   shading** (§7.1–§7.5): "duty" drops most of *dharma*; "mind" collapses *manas*,
   *buddhi* and *citta*; "action" drops the fruit-and-law load of *karma* in its
   technical use.
3. **Keeping it loses nothing a reader needs**, because the card and the glossary
   carry the full meaning.

If any test fails, the sense is translated with one fixed rendering (and its English
forms). Two distinct Sanskrit words never share one English word (§7.6). Established
English forms count as kept: *brahman* → "Brahman", *ātman* → "the self". Use several
English words when one will not do: two precise English words beat one lossy word and
beat needlessly keeping the Sanskrit. Don't bloat the reader with Sanskrit English can
carry; don't flatten to English a term that genuinely needs its Sanskrit.

### 8.2 Disputed referents: the kūṭastha precedent

When the schools dispute what a term refers to, and translators accordingly give
mutually incompatible English, that spread is evidence that test 2 fails for every
English candidate: each English word would put one school's referent into the line.
Such a term is preserved, and the card carries all readings, each with its source
(§6.4), with a fork where the construal matters (§6.5). The test is a disagreement
about the referent, not a variety of synonyms for one agreed sense ("steady", "firm",
"steadfast" for one sense show only that English has synonyms).

Precedent: *kūṭastha* (12.3; also 6.8, 15.16), preserved. The commentators divide five
ways — what stands over māyā as its ground and witness (Śaṅkara's first reading,
Madhusūdana, Nīlakaṇṭha, Śrīdhara); standing like a heap, unmoving (Śaṅkara's
second); common to all (Rāmānuja, Vedānta Deśika); standing in space (Madhva); what
pervades time in one form (Amarakośa 3.1.148–149) — and seven published translations
give seven words (unchanging, common to all, eternal, peak-like, the Primal,
rock-seated, self-poised). All three tests hold: the Gītā uses it to define *akṣara*
(15.16) and the yogin (6.8); no English word carries it without dropping construals;
the card and glossary carry every reading.

### 8.3 The table (`data/glossary/term_policy.json`)

- **The decisions are the rows of the table** — for the Gītā, the Gītā lexicon. The
  examples in this document are illustrative; checkers read the table alone.
- A row records, per sense: the occurrences it applies to (locus and word index); the
  policy (preserve or translate); the three test results; the English **forms** per
  grammatical category (noun, plural, finite verb, participles, agent, adverb) — for a
  preserved noun, a verbal form needs an owner-approved verbal rendering or the verb is
  translated; forbidden English; the glossary key; the card's term line; the dossier
  it was decided from; and its **status** with date: `proposed` → `lexicon-reviewed`
  (decided by a lexicon agent and passed by the independent lexicon reviewer) →
  `owner-decided` (after the owner's taste review). The table also keeps
  `reserved_english` (§7.6) and a changelog.
- Production uses only `lexicon-reviewed` or `owner-decided` rows. A production run
  records the table's content hash; any change to a row lists the affected
  occurrences, which are swept mechanically and re-reviewed as a diff.
- A row is a decision, not a truth: a producer or reviewer who finds it wrong for an
  occurrence files a row proposal with the occurrences and evidence; meanwhile the row
  stands. The owner's taste review after publication may change any row; the change
  flows through the same sweep.
- The pilot's table (version `2-ch12-meaning`, 64 lemmas) predates this structure and
  is migrated to it as the Gītā lexicon (v3) in stage B of the plan.

### 8.4 Standing decisions (illustrative; the row governs where one exists)

**Preserve:** *rāga*, *dveṣa* (noun), *guṇa*, *dharma*, *kāma*, *prajñā*, *buddhi*,
*manas*, *indriya*, *yoga*, *rasa*, *ahaṃkāra*, *tṛṣṇā*, *samādhi*, *saṃsāra*, *bhakti*
and *bhakta*; *karma* in the law-of-action sense; *kūṭastha* (§8.2). Note *prajñā* (the
*sthita-prajña* title concept, ≠ buddhi, ≠ jñāna) and *buddhi* (the discriminating
faculty, kept distinct from manas/prajñā).

**Translate:** *krodha* → anger (emotion words translate; the table has no row yet —
it is added when the lexicon reaches the lemma; the earlier readers print "krodha" and
are migrated under §10); *bhaya* → fear; *moha* → delusion; *duḥkha* → sorrow, and
"pain" where it is paired with *sukha* ("pleasure and pain", 12.13, 12.18), "with
hardship" as the adverbial accusative (12.5); *sukha* → pleasure; *spṛhā* → longing;
*sneha* → affection; *prīti* → fondness; *vidheya* → governable (§7.5); *jñāna* →
knowledge; *mokṣa* → liberation; *saṅga* → clinging (the English carries the √sañj
*sticking/adhering* sense; a cited lemma — Śaṅkara's "‘saṅga’ — clinging…" — keeps the
Sanskrit); *karma* in the plain-act sense → "action / act" (2.47 *karmaṇi*; 12.6
*sarvāṇi karmāṇi*: acts and their fruit, not the law of action); *dhyāna* →
"meditation" (noun and participle pair; √dhyai with the sense-objects as object, 2.62
*dhyāyato viṣayān*, is a separate sense to be decided as its own row); upa-√ās →
"attend upon", pari-upa-√ās → "attend wholly upon"; saṃ-ni-√as with a locative of the
person → "lay down … in" (12.6; its non-finite form is owner item O12); *ananya* → "undivided"; ud-√vij with an ablative →
"shrink from", the noun *udvega* → "agitation". In set compounds keep the natural form:
*jñāna-yoga* "the yoga of knowledge", *jñāna-niṣṭhā* "steadfastness in knowledge".

**Open (owner, plan §2.2):** the *karma-phala* rendering across chapters 5 and 12.

**Orthography.** Printed IAST follows the witness: for the Gītā, BORI — *ahaṃkāra*,
*saṃnyāsa*, *saṃtuṣṭa* (BORI has 10 × *ahaṃkār*, 0 × *ahaṅkār*).

Decisions above without a row are the standing decisions of the earlier readers; each
becomes a row when the lexicon reaches its lemma, and from then the row governs.

### 8.5 The decision procedure (apply to every term)
1. List the word's attested senses (dhātu and Dhātuvṛtti, kośas, the text's usage,
   the commentators *here*: §6.4).
2. Does a plain English word — or a short phrase — carry the operative sense
   without adding, dropping, or shading anything (§7.1–§7.5)? If yes, translate.
3. If no English fits without distortion (irreducible load, or a disputed referent,
   §8.2), keep it IAST and glossary-link it.
4. Whatever you choose: apply it consistently (§7.7) and never as a different
   Sanskrit word (§7.6). When a single best choice is genuinely unclear, file a row
   proposal rather than guess.

## 9. Other translations and the private store *(new 2026-11-08)*

- **Production does not depend on other translations.** Published translations
  ("secondaries": English translations, word-for-word editions, Sri Aurobindo's
  renderings) are not read when the lexicon is decided or when lines are produced.
  Our English comes from the Sanskrit sources (§6.4) and the English dictionaries
  (§7.17). Nobody is followed blindly: not the commentators, not the translators, not
  our own first draft.
- **Blind check, last.** After our line exists, the reviewer compares it with the
  secondaries for two questions only: did we miss an admissible construal (if so, it
  becomes a fork, §6.5, decided on grammar and usage), and which renderings will
  readers meet (`meaning.alternatives`, `reception` lines). Where a secondary has
  better English for the same construal, the reviewer may say so; adopting it is a
  decision on the merits, recorded with the dictionary entry of the word, never "because
  X has it". A secondary is never authority.
- **Never republished.** No secondary's verse rendering, deviation defence or candidate
  list appears in any public file (reader data, apparatus, glossary, documentation). A
  `reception` line may name a translator and quote a few words of his rendering of
  that word; that is the only public trace.
- **Private store.** The repository is public. Every file that quotes a secondary —
  packets' secondary sections, blind-check records, deviation defences — is private:
  it lives under `internal/sanskrit_reviews/` and is git-ignored. Before writing a new
  kind of private file, confirm that `git check-ignore` covers its path; if it does
  not, the ignore rule is added first.

## 10. Cross-reader consistency and migration *(new 2026-11-08)*

All readers on the site share one table. Readers built before it (`gita/sthitaprajna/`,
`gita/kama/`, `gita/ch5/`) are migrated in one pass: `term` on every matching word, the
row's rendering applied, card glosses that contradict slots corrected, epithets
translated (§7.10), and context exceptions recorded as new sense rows, never as
one-offs. Until migrated, such a reader is listed as `legacy` in the checkers'
registry; its violations are reported, not hidden. Known items: *krodha* printed in
Sanskrit seven times (2.56, 2.62, 2.63, 3.37, 5.23, 5.26, 5.28); untranslated epithets
in 2.54–2.72; swapped slots at 2.59 and 5.11. The migration is plan task G1.5.
