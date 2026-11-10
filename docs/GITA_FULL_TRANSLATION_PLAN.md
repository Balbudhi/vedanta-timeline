# The Bhagavad-Gītā, word by word: project document

The single document for the Gītā translation: goal, method, current state, gaps,
decisions and roadmap. Rules live in the
[translation standard](SANSKRIT_TRANSLATION_STANDARD.md) and the
[English procedure](gita_briefs/ENGLISH_CRAFT.md); this document links to them and does
not restate them. Status sections are dated; "measured" means read from the code or the
local files named. Superseded process documents (the stages A–E job queue, the agent
briefs, the lexicon-first design and the pilot audits) are kept in
[`docs/history/gita/`](history/gita/).

## 1. Goal

A complete word-by-word English translation of the Bhagavad-Gītā (BORI critical text,
700 verses), published on vedanta.eeshan.xyz as one article: the Devanāgarī text, the
IAST word division with a card on every word, the English line, and a recitation synced
verse by verse. It is for readers who want to see what each Sanskrit word says and how
the verse is built, in English that reads well. It is produced by a pipeline the owner
can run with Codex, ChatGPT or Claude: code does every exact step, the model only makes
the judgements code cannot, from evidence that code puts in front of it.

The quality bar:

- **Lossless in the line.** Every word's meaning and signification is carried by the
  English line itself; nothing is parked in notes or cards.
- **Grounded.** Every grammatical claim is traceable to Pāṇini and the source library;
  every sense to Sanskrit sources; no commentator or translator is followed blindly.
- **Good English.** Exact, rhythmic, readable on first reading, using the full range of
  English where that is what the meaning needs.
- **Consistent.** The same sense of a word gets the same English across the whole book.
- **General.** The method is fixed before a chapter is translated; chapter 12 is the
  development chapter and chapter 15 the held-out test.
- **Owner's taste is final.** Publication is provisional until the owner has read it.

## 2. The translation standard in brief

The binding rules are in [`SANSKRIT_TRANSLATION_STANDARD.md`](SANSKRIT_TRANSLATION_STANDARD.md)
(the line rules in §7, preserve-or-translate in §8, other translations in §9) and in
[`ENGLISH_CRAFT.md`](gita_briefs/ENGLISH_CRAFT.md) (Sri Aurobindo's criteria for English
and the word-choice procedure, §2). In summary:

- **Lossless in the line.** Each word is rendered for what it means and what it
  signifies. The line keeps the Sanskrit's rhythm and grammar as far as English allows,
  in the sense Sri Aurobindo gives those terms.
- **Order of means.** An English word that carries the meaning; else a well-formed new
  English word (a transparent formation from real English parts); else the Sanskrit word
  kept. Rare or archaic English is used when it is exact, never as ornament; connotation
  is checked separately from meaning.
- **Several readings.** Where the grammar admits two construals, the line holds both if
  English can; otherwise a second full line is given. A second line is only for a real
  grammatical or construal fork, never for a doctrinal preference.
- **No notes layer.** Word cards explain the word (grammar, sources, other readings);
  they never hold meaning the line failed to carry. The reader shows no commentary layer.
- **Sources.** Meaning comes from Sanskrit sources; English comes from English
  dictionaries. Sanskrit–English dictionaries (Monier-Williams, Apte) only help to locate
  material. Published translations are not used in production, are kept private, and are
  never republished.
- **Sense-constant terms.** The same (lemma, sense) gets the same English everywhere;
  distinct near-synonyms get distinct English. Owner-reviewed decisions are rows of
  [`data/glossary/term_policy.json`](../data/glossary/term_policy.json) and win everywhere.
- **General across chapters.** No rule, prompt example or decision is tuned to one
  chapter's answers.

## 3. Method

The owner's order for establishing meaning is fixed: decode the Sanskrit, give each
morpheme its meaning, read the lexical texts, read the usage, and only then read the
commentaries, as witnesses. English is chosen after the meaning is settled. Code locates
and assembles evidence at every step; the model judges only where a choice remains.

### 3.1 Meaning, in the owner's order

| # | Step | What it decides | Sources (prakriya library inventory) | Code | Model | Output |
|---|---|---|---|---|---|---|
| M1 | **Decode** | Word division (sandhi split), morphology, derivation as stem (prakṛti) + affixes (pratyaya) with the sūtras that apply, compound type and analysis (vigraha), syntactic relation and kāraka | Vidyut; Aṣṭādhyāyī; Kāśikā; Siddhāntakaumudī, Laghusiddhāntakaumudī; Dhātupāṭha (root, gaṇa, pada); Uṇādisūtra and Liṅgānuśāsana | Every admissible split, analysis and derivation, each step cited to a sūtra line | Chooses among admissible analyses where the grammar leaves more than one; records real forks | One construal per verse (and any fork), every claim cited |
| M2 | **Morpheme meanings** | The meaning of the root in the sense used, of each affix, of the case (kāraka) | Dhātupāṭha artha; the Dhātuvṛttis (Mādhavīya, Kṣīrataraṅgiṇī, Dhātupradīpa) and Daiva with Puruṣakāra; affix and kāraka meaning from the grammar (Aṣṭādhyāyī and Kāśikā meaning sūtras; Vaiyākaraṇabhūṣaṇasāra, Vaiyākaraṇasiddhāntamañjūṣā, Vākyapadīya) | Joins each root to its Dhātupāṭha and Dhātuvṛtti entries; gives each affix and case its stated meaning with locus | States the composed literal meaning | Literal meaning per word, built from its parts |
| M3 | **Lexical texts** | The senses the word admits | Amarakośa with Amaraviveka; Halāyudha; Vaijayantī and Yādava; Ākhyātacandrikā (verbs); Nirukta and Nighaṇṭu; Śabdakalpadruma, Vācaspatya | Collects every entry for the lemma, each with locus (the kit's meaning pages) | Lists the senses the texts allow | Admissible senses with their sources |
| M4 | **Usage** | Which admissible sense the text uses here | Every Gītā occurrence (concordance), with counts by sense and context; the Mahābhārata (BORI critical text, acquired 2026-11-09) | Lists all occurrences and computes the statistics | Chooses the sense that fits this place | The sense at this place, with the usage behind it |
| M5 | **Commentaries, last** | Confirms or contests the choice among the senses the texts allow; supplies forks | 13 commentators in 14–16 passages per verse (Śaṅkara, Rāmānuja and Madhva from the on-disk texts and again from the gita/gita collection, with ten others) | Aligns each commentator's gloss to each word, with locus | Uses them as witnesses: what the word says (literal) is kept apart from what a commentator says it refers to; the latter never enters the line | Final literal meaning; readings that become forks |

The source inventory with each work's role and the kit's use of it is prakriya
`docs/research/INTERPRETER_VS_KIT_20261108.md` §3 (59 works). The kit's commands are
described in prakriya `docs/GITA_KIT.md`.

### 3.2 English, the line and after

| # | Step | Who | What happens |
|---|---|---|---|
| E1 | Find English by the meaning | Code (English workbench) | Searches English dictionaries by the settled meaning and the root's image; returns candidates with their matching sense, modern first sense, frequency, stress, origin and phrase frequency |
| E2 | Choose the word | Model | Follows [ENGLISH_CRAFT](gita_briefs/ENGLISH_CRAFT.md) §2 steps 3–6: kind of expression (exact word, uncommon real word, construction, formation, kept Sanskrit), meaning and connotation checked separately, decide once |
| E3 | Write the line | Model | The line pass of ENGLISH_CRAFT §2 and the standard's line rules (§7) |
| E4 | Check | Code | Every mechanical rule: coverage, nothing added, term rows, trace to evidence, compound members rendered, attested English, line rules, grammar checker |
| E5 | Review | Model, with measured facts | Reads the line aloud against the Sanskrit; blocking findings go back for revision |
| E6 | Consistency | Code groups, model decides | Every lemma rendered two ways, and every English word used for two lemmas, decided once with all places in view; first per chapter, then for the whole book; owner decisions enter `term_policy.json` |
| E7 | Publish | Code | Build the article (cards, lines, forks), validate, deploy by script; recitation aligned per verse (§3.3) |
| E8 | Owner taste review | Owner | Reads on the site; decisions flow back as term rows and rule changes |

### 3.3 Audio

One lawful, complete recitation, verse-level timing, rules in
[`AUDIO_ALIGNMENT_STANDARD.md`](AUDIO_ALIGNMENT_STANDARD.md).
`scripts/audio/align_gita_chapter.py` aligns a chapter with two acoustic models that
share nothing (MMS forced alignment and a Sanskrit wav2vec2 model), snaps boundaries to
speech gaps and marks a verse corroborated when both agree; the manifest stays
`provisional` until the owner has listened. Mastering is a format shift only
(`scripts/audio/master_encode.py`; CBR mono MP3). Lawful candidates found so far
(archive.org): A. Sakhare Maharaj, Sadhakashram Alandi (Public Domain Mark set by the
uploader; a written CC licence to be requested); B. P R Iyer (CC BY-NC-ND 4.0, usable now
as a whole-chapter file with an external timing manifest); C. Samskrita Samvadah (Public
Domain Mark; quality unverified). The choice is the owner's (§6.2).

## 4. Current implementation (measured 2026-11-10)

Paths are in vedanta-timeline unless prefixed `prakriya/`. Local working state
(`internal/`) is git-ignored and private. The code is described module by module in
[`scripts/gita/translate/README.md`](../scripts/gita/translate/README.md).

### 4.1 What exists

| Step | Code | What it does today |
|---|---|---|
| Prerequisites | `scripts/gita/build_all_packets.py` (with `scripts/gita/gitapipe/`), `scripts/gita/build_commentary_packets.py` | Per-verse packets with Vidyut analyses, `analyses.sqlite` (analyses and derivations), concordance, lemma inventory; per-verse commentary packets (14–16 passages from 13 commentators) |
| Grammar oracle | prakriya `scripts/gita_kit/grammar.py` (Vidyut 0.4.0) | Analyses 99.48% of the Gītā's 9,121 padas and derives 99.16% back with sūtra citations (`prakriya/tests/gita_kit/coverage_report.json`, regenerated 2026-11-09 after the alignment fix) |
| Meaning sources | prakriya `scripts/gita_kit/meaning.py`, `scripts/lookup/lookup.py` | Indexed Dhātuvṛttis, kośas, Nirukta/Nighaṇṭu, SKD/VCP, concordance, commentators' glosses |
| Mahābhārata | prakriya `corpus/acquisition-20261109/itihasa/mahabharata_bori_gretil/` | BORI critical text from GRETIL, cleaned to keyed IAST (18 parvans, 1,995 adhyāyas, 73,815 verses; 6.23–6.40 identical to our BORI Gītā); local, git-ignored (no redistribution licence) |
| M1 Parse | `drive.py construe`, card `compile.construe_input` | Tool-free, read-only. Grammar first: each token's padas, the engine's candidate analyses (top 8 with derivations, up to 40 more), then the commentaries last. Author, code check, grammar review, ≤3 rounds |
| M1–M5 Meaning | `sanskrit_card.py`, `affix_meanings.json`, `mbh_usage.py`; `pipeline.py` meaning call | Per word a Sanskrit-only card in the owner's order (§4.2); a code audit that no source with an entry is left out; a code check that each literal meaning is grounded in a text when one has an entry |
| E1 English workbench | `english_bench.py`, `english.py`, `english_roots.py` | Seven dictionaries; semantic index complete (44 of 44 shards, 872,157 definitions); frequency, stress, origin, book frequency; LanguageTool |
| E2–E5 Translate | `pipeline.py translate`, `prompts3/` | Per sentence unit: meaning call, English candidates by code (found by meaning first), translate call, code checks, review, ≤2 revisions. `preflight` stops a run when an English tool is missing |
| E6 Consistency | `pipeline.py consistency --run R1 [R2 …]` | One chapter or the whole book; one call per conflicting group; affected units re-translated in their own run |
| Owner sheet | `pipeline.py sheet` | Formations, kept Sanskrit, losses, challenged seeds, second lines, consistency decisions, with literal meanings |
| Whole book | `book.py` | Parse, translate and sheet for any chapters, then one consistency pass over all |
| Runners | `runner.py` | Codex (default) and Claude (`GITA_RUNNER=claude`), tool-free |
| E7 Publish | `publish.py` → `scripts/build_gita_chapter_reader.py` | Converts run records to the builder's input; fails closed (§4.4) |
| Evaluation | `compare.py` | Content-word overlap with a private reference (evaluation only) |

### 4.2 What the model is given

**Parse (M1).** The card of `compile.construe_input`, in this order: the verse; per token its padas
(found through the packet's `bori_token`; before 2026-11-10 candidates were looked up by the sandhi
surface and 3,115 of the Gītā's 8,474 tokens received none); the engine's analyses of each pada, the
top 8 with their derivation (prakṛti + pratyaya with sūtras) and up to 40 further ones; the
neighbouring verses; last, every commentary passage. No tools.

**Meaning call (M1–M5).** Per content word, `sanskrit_card.word_card` (Sanskrit only; no English term
rows or case hints):

| Section | Content |
|---|---|
| M1 decode | The chosen analysis, prakṛti (root with gaṇa, Dhātupāṭha number and artha, or stem), affixes, derivation steps of the pratyaya chapters with sūtras, compound type and vigraha |
| M2 morphemes | Dhātupāṭha entries; Dhātuvṛtti windows, 2 per work, from the Mādhavīya, Kṣīrataraṅgiṇī, Dhātupradīpa and Daiva; the meaning sūtras (with text) of every kṛt/taddhita affix, lakāra, prayoga, sanādi suffix and case |
| M3 lexical texts | Amarakośa, Amaraviveka, Halāyudha, Vaijayantī, Yādavakośa, Ākhyātacandrikā (verbs, through the root), Nirukta, Nighaṇṭu, Śabdakalpadruma, Vācaspatya: entries where the lemma is a word, ≤2 per work, ≤320 characters |
| M4 usage | Gītā places and up to six other lines; Mahābhārata: lines using the word in any form the grammar generates, by parvan, three examples |
| M5 commentaries, last | Each commentator's clause on the word in this verse |
| sources | The status of all 19 sources: shown, no entry, partial matches only, not applicable |

Compound members carry M2 and M3. Measured on ch15 (176 content words) and ch12 (145): the coverage
audit finds no source with an entry left off a card; median card 5.3 KB and 4.4 KB per word.

**Translate call (E2–E3).** The literal meaning, readings and up to 12 English candidates per word
(semantic search, image search and the reverse dictionary first; then ≤4 remembered words; then ≤2
root words), each with senses, dictionary loci, frequency, stress, origin. The prompt inserts
ENGLISH_CRAFT's five principles and §2 steps 3–6, and the standard's §7.1–§7.17, §8.1 and §8.5,
verbatim at run time.

### 4.3 Known defects

Listed in [`scripts/gita/translate/README.md`](../scripts/gita/translate/README.md#known-defects).
The defects listed here on 2026-11-09 (second lines unchecked, a loss rule that could not fire,
silent tool skips, unaccepted parses loaded, remembered words admitted unexamined, the truncated
evidence feed, English on the meaning card) are fixed and tested.

### 4.4 Publication state

- Live: chapter 12 (2026-11-08, origin/main 9c8fb7b) and chapter 5 (an older reader), plus the
  thematic readers `gita/sthitaprajna` and `gita/kama`. Chapter 12 was built from the older
  producer/reviewer files. Its audio is P R Iyer, `provisional`.
- `publish.py` converts run records into the builder's input and refuses unfinished chapters. A dry
  run on ch15-heldout gives 2,707 builder errors (pre-slot records): candidate loci (now recorded by
  new runs), grammar of manually analysed words, and fields no stage produces: a verse-level sense and
  grammar summary, five consulted secondaries (the §9 blind check), a complete independent-review
  record, the term-policy hash (§6.2).

### 4.5 Results so far

| Run | Chapter role | Parse | Translate | Overlap with reference |
|---|---|---|---|---|
| `ch12-qual` | development | agentic, old card | 16 units, 88 calls | 0.64 |
| `ch15-heldout` | held-out | agentic, old card: 112 of 279 words on an engine analysis, 167 manual; 14.6 M tokens | 19 units, 101 calls; English choices 5 retrieved, 110 remembered | 0.43 |
| `ch15-v3` (2026-11-10) | held-out | tool-free, grammar first: 221 of 261 on an engine analysis, 40 manual; 20/20 accepted; 14.3 M tokens (mostly cached) | 19 units, 102 calls, 1,113 s; English choices 75 retrieved, 66 remembered, 22 standing; code errors left in 5 units, S1/S2 findings in 5 | 0.40 |

Overlap is the mean content-word Jaccard against a local, private reference
(`internal/gita_pipeline/gold/`); it points to where to read, it is not a quality score. Chapter 12
lines appear as examples in ENGLISH_CRAFT §3, so chapter 12 is not a clean test. In `ch15-v3`, 17 of
19 units carried a second line, often several readings packed into one; a code check and a prompt
rule now allow one second line, for a grammatical fork only (not yet re-run). The reviewer still
finds commentators' readings inside some literal meanings (15.10 "experiencing" where the root and
the kośa give eating).

## 5. Gaps

State on 2026-11-10. Gaps 1–5, 7, 9–12 and 14 of the 2026-11-09 list are closed in code and tests
(§4). Open:

| # | Gap | Effect | Next step |
|---|---|---|---|
| 1 | Commentators' readings still reach some literal meanings | A line can carry an application instead of the word | Re-run ch15 with the one-fork rule; if the review keeps finding it, a code check comparing the literal's content words with M2/M3 |
| 2 | Second lines over-produced (17 of 19 units) | Lines the standard does not call for | One-fork rule (code check + prompt), re-run |
| 3 | Manually analysed words (40 of 261 in ch15) have no derivation | M1–M2 thin for those words; publication fields missing | Engine coverage of the forms the parse rejects (finite veda, vā, utkrāmantam …) |
| 4 | Publication fields no stage produces (§4.4) | Pipeline output cannot be published | Owner decisions (§6.2), then a verse-summary step |
| 5 | Usage counts by sense | Counts are by word, not by sense | Sense labels per occurrence after translation |
| 6 | Mahābhārata usage counts whole words only | Compounds and vowel-fused words uncounted | Lemmatised corpus (DCS, CC BY 4.0) as a second resource |

## 6. Decisions

### 6.1 Decided by the lead (the owner may override)

| Decision | Basis |
|---|---|
| No commentary rendering: the reader shows the mūla only; commentaries are evidence | Owner instruction; standard §2 |
| Sense-constant term rule (standard §7.7, §8) | Translate meanings, not strings; confirmation open (§6.2) |
| Devanāgarī mūla is a labelled transliteration of the BORI IAST, collated against a second witness | Standard forbids only silent script generation |
| Audio at verse level, two corroborating aligners, owner listening before `verified` | `AUDIO_ALIGNMENT_STANDARD.md` |
| Code does exact work; translation calls are tool-free and get everything on a card | Owner's requirements for speed, cost and correctness |
| Vidyut is used through the prakriya kit until a Pāṇinian interpreter exists; its output is checked against the sūtra text | Owner accepted the engine with a stated reason |
| Literal meaning and the commentators' application are kept apart; only the literal reaches the line | ch15 held-out failures (commentators' readings in the line) |
| Seed term decisions bind unless the translator records a challenge, which goes to the owner sheet | Held-out ch15: Gītā-wide terms were otherwise unknown |
| dhyāna → "meditation" (translate) | Noun and participle must pair (12.6, 12.12) |
| Chapter 12 meaning decisions (term policy `2-ch12-meaning`): upa-√ās "attend upon", pari-upa-√ās "attend wholly upon", atha with indicative protasis "If …, then …", kūṭastha kept, duḥkha "pain" where paired with sukha, ananya "undivided", ud-√vij with ablative "shrink from" | Four meaning reviews; open to the taste review |
| Published translations are out of production; private references are used only to evaluate | Standard §9 |
| Line style: standard §7.8–§7.17; public-text rule (no process vocabulary in public fields) | Standard §3.4, §7 |
| Deploy by script from a clean worktree of origin/main; the script does not push | Shared working tree |
| Dev chapter 12, held-out chapter 15; prompt examples from neither | Generality |

**Seed term decisions** (cited as "plan §4", this section's former number, in
`scripts/gita/translate/seed_terms.json` and `term_policy.json`; 54 rows, 27 kept and 27
translated, not yet owner-reviewed). Kept in Sanskrit: yoga, dharma, svadharma, guṇa,
sattva, rajas, tamas, prakṛti, puruṣa, buddhi, manas, indriya, ahaṃkāra, prajñā, kāma,
rāga, dveṣa, tṛṣṇā, rasa, samādhi, saṃsāra, māyā, yajña, tapas, bhakti, bhakta, brahman.
Translated: krodha anger, bhaya fear, moha delusion, duḥkha sorrow (or pain), sukha
pleasure, saṅga clinging, jñāna knowledge, mokṣa liberation, śānti peace, pāpa sin, puṇya
merit, saṃnyāsa renunciation, tyāga relinquishment, kṣetra field, avyakta the unmanifest,
akṣara the imperishable, īśvara the Lord, phala fruit, hetu cause, śaraṇa refuge, śraddhā
faith, siddhi perfection, deva god, jīva living being, śoka grief, dhyāna meditation, ātman
the self. karma is not a seed: its two senses (law of action, kept; plain act, "action")
are rows of `term_policy.json`. Undecided: vijñāna, kṣetrajña, yoga in the plain sense
"joining", nirvāṇa (2.72, 5.24–26, 6.15).

### 6.2 Open owner decisions

| Decision | Note |
|---|---|
| krodha: translate ("anger", current row) or keep, given the kāma–krodha pair of 3.37 | Earlier readers kept it for that reason |
| puruṣa in 15.16–19 (the puruṣottama passage): keep the Sanskrit (seed) or translate ("person") | The held-out run kept puruṣa |
| Review of the 54 seed term rows | Bind today as provisional |
| Sense-constant vs string-constant term rule | Lead chose sense-constant |
| Confirm the ENGLISH_CRAFT §4 amendments the lead applied provisionally: B (formations defined; "upbearer" attested), C (English constructions that are not devices), D ("any" for a universal under negation), F (register variants in a row's forms), G (the line pass), H (review severities), I (`found_by` on every candidate), J (the gloss gives the meaning), L (the procedure sent to the translator verbatim) | Written into the standard (§3.1, §5.1, §7.1, §7.16, §7.17, §8.3) and marked provisional, because the pipeline already works this way (H is in `prompts3/review.md`) |
| ENGLISH_CRAFT §4 amendments still open: A (no default between plain and rich), E (ṇini of habit as a present participle), K (re-test kept terms: *dveṣa* against "mislike") | The standard keeps its current text for A |
| Whether the decode step may use commentators' word lists as split candidates (the kit does today), or commentaries enter only at M5 | Owner's order puts commentaries last |
| Whether a blind check against other translations is built, or references stay evaluation-only | Standard §5.1/§9 vs current pipeline |
| Recitation source (A, B, C, or a commissioned reciter) | ch12 uses B, provisional |
| Taste review of chapter 12 on the site, and line-style calibration with it | Before more chapters are published |
| Chapter 12 rows still marked pilot: cetas, dhyāna, duḥkha/sukha (incl. adverbial sukham), the verb of dveṣa, sama, śubha/aśubha, amṛta | Non-blocking |
| sarvatraga: formation or the attested "all-pervading"; rich-word items "upbearer", "infixed", "loosed", "weigh alike" | Taste |
| karma-phala across chapter 5 and chapter 12 | Before chapter 5 is migrated |
| Whether cards show the site's synthesis meaning category publicly; Sri Aurobindo's register devices in lines | Standard §6.3, §7.17 |
| Sync the shared local checkout with origin/main (the toolchain is committed) | Needs the other agents' uncommitted work in that checkout set aside first |
| The chapter builder requires five consulted secondaries per verse: run the §9 blind check, or drop the rule for pipeline output | Blocks publication of pipeline output |
| May the pipeline's review stand as the builder's independent-review record | Blocks publication |
| Claude runner: allow paid extra usage, or Codex only | The first Claude call was refused by the account's usage control |
| Admit the Mahābhārata (IAST) to the library, or keep it as a local acquisition | Its terms grant no redistribution; it is git-ignored |

## 7. Roadmap (dependency order, no dates)

| # | Step | Depends on | Done when |
|---|---|---|---|
| 1 | Re-run ch15 (and ch12) with the one-fork rule; measure literal-meaning leaks | — | Second lines only at grammatical forks; review findings counted |
| 2 | Owner decisions for publication (§6.2) | owner | Builder rules settled |
| 3 | Verse-level sense and grammar summary; publish ch15 through `publish.py` | 1, 2 | ch15 builds fail-closed from pipeline output |
| 4 | Full-book run (`book.py --chapters 1-18`) | 3 | 700 verses translated and checked; book-wide consistency |
| 5 | Owner taste review; changes fed back as rows and rules | 4 | Owner sign-off per chapter |
| 6 | Audio for all chapters on the chosen source; owner listening | recitation decision | Every verse timed; manifests `verified` |

## 8. Map

### Documents

| Document | Role |
|---|---|
| [`SANSKRIT_TRANSLATION_STANDARD.md`](SANSKRIT_TRANSLATION_STANDARD.md) | The rules (reader, schema, grammar, meaning layer, forks, line rules, preserve or translate, other translations) |
| [`gita_briefs/ENGLISH_CRAFT.md`](gita_briefs/ENGLISH_CRAFT.md) | Sri Aurobindo's criteria and the word-choice procedure; parts are read by the code at run time |
| [`AUDIO_ALIGNMENT_STANDARD.md`](AUDIO_ALIGNMENT_STANDARD.md) | Audio timing rules |
| [`../scripts/gita/translate/README.md`](../scripts/gita/translate/README.md) | How to run the translation code, its dependencies and checks |
| [`../scripts/gita/README.md`](../scripts/gita/README.md) | Which scripts under `scripts/gita/` are current |
| prakriya `docs/GITA_KIT.md` | The kit: lookup commands, grammar and meaning oracles, tests |
| prakriya `docs/research/INTERPRETER_VS_KIT_20261108.md` §3 | Inventory of the Sanskrit library: every work, its role, the kit's use |
| [`history/gita/`](history/gita/) | Superseded plans, briefs and audits |

### Code and data

| Location | What |
|---|---|
| `scripts/gita/translate/` | Current pipeline: `drive.py` (parse), `pipeline.py` (translate, consistency, sheet), `sanskrit_card.py`, `affix_meanings.json`, `mbh_usage.py`, `evidence.py`, `english*.py`, `check.py`, `runner.py`, `book.py`, `publish.py`, `compare.py`, `prompts/`, `prompts3/`, `tests/` |
| prakriya `corpus/acquisition-20261109/itihasa/mahabharata_bori_gretil/` (local, git-ignored) | The Mahābhārata, BORI critical text |
| `scripts/gita/build_all_packets.py`, `build_commentary_packets.py`, `gitapipe/` | Verse, commentary and meaning packets |
| `scripts/build_gita_chapter_reader.py`, `scripts/deploy_gita_chapter.sh`, `scripts/gita/build_whole_gita.py` | Building and deploying readers |
| `scripts/audio/` | Recitation alignment and mastering |
| `data/glossary/term_policy.json`, `scripts/gita/translate/seed_terms.json` | Owner term decisions; seed decisions |
| `assets/gita.js`, `assets/gita.css`, `gita/ch*/` | The reader and published chapters |
| prakriya `scripts/lookup/lookup.py`, `scripts/gita_kit/` | Source lookups; grammar and meaning oracles |
| `internal/gita_pipeline/` (local, git-ignored) | Packets, runs, private references |
