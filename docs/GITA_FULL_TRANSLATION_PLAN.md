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
| M4 | **Usage** | Which admissible sense the text uses here | Every Gītā occurrence (concordance), with counts by sense and context; the Mahābhārata (not yet in the library) | Lists all occurrences and computes the statistics | Chooses the sense that fits this place | The sense at this place, with the usage behind it |
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

## 4. Current implementation (measured 2026-11-09)

Paths are in vedanta-timeline unless prefixed `prakriya/`. Local working state
(`internal/`) is git-ignored and private.

### 4.1 What exists

| Step | Code | What it does today |
|---|---|---|
| Prerequisites | `scripts/gita/build_all_packets.py` (with `scripts/gita/gitapipe/`), `scripts/gita/build_commentary_packets.py` | Per-verse packets with Vidyut analyses, `analyses.sqlite` (full analyses and derivations), concordance, lemma inventory, 4,712 kit meaning pages; per-verse commentary packets (14–16 passages) |
| Grammar oracle | prakriya `scripts/gita_kit/grammar.py` (Vidyut 0.4.0) | Analyses 99.5% of the Gītā's words and derives 99.2% back with sūtra citations (`prakriya/tests/gita_kit/coverage_report.json`, generated before the 2026-11-09 alignment fix) |
| Meaning oracle | prakriya `scripts/gita_kit/meaning.py` | Meaning pages from the Dhātuvṛttis, kośas, Nirukta/Nighaṇṭu, SKD/VCP, concordance and commentators' glosses; on 300 frequent lemmas: kośa 235, Dhātuvṛtti 164 of 164 verbal, Nirukta/Nighaṇṭu 203, SKD/VCP 289 |
| M1 Parse | `scripts/gita/translate/drive.py construe` | An agent (Codex, with a command tool, `tool.py`) per verse: author, code check, grammar-only review, at most 3 rounds. ch12 and ch15: 20/20 verses accepted each |
| M2–M5 + E2–E5 Translate | `scripts/gita/translate/pipeline.py translate`, prompts in `prompts3/` | Per sentence unit: a tool-free "meaning" call, English candidates by code, a "translate" call, code checks, a "review" call, at most 2 revisions |
| E1 English workbench | `scripts/gita/translate/english_bench.py`, `english.py`, `english_roots.py` | Seven sources indexed (Webster 1913, GCIDE, Wiktionary, OEWN 2025, Roget 1911, Moby, WordNet 3.1); semantic search (qwen3-embedding via Ollama); wordfreq, CMUdict/IPA stress, etymology origin, Google Books Ngram (network), LanguageTool |
| E4 Checks | `scripts/gita/translate/check.py`, `pipeline.check_unit` | The exact rules listed in E4; 103 test functions in `scripts/gita/translate/tests/` (as of 2026-11-09; not re-run for this document) |
| E6 Consistency | `pipeline.py consistency` | One chapter per run; one call per conflicting group; affected units re-translated with the decision fixed |
| Owner sheet | `pipeline.py sheet` | Writes `DECISIONS.md` for the owner |
| Evaluation | `scripts/gita/translate/compare.py` | Content-word overlap with a private reference (evaluation only, never in prompts) |
| E7 Publish | `scripts/build_gita_chapter_reader.py`, `scripts/deploy_gita_chapter.sh`, `scripts/gita/build_whole_gita.py`, `scripts/audio/` | Fail-closed chapter builder (from producer/reviewer files); deploy from a clean worktree of origin/main (prints the push command; does not push); whole-article builder (not yet used) |

Only `codex exec` is coded as a model runner (`pipeline.call`, `drive.codex`); there is
no Claude or ChatGPT runner yet.

### 4.2 What the model is actually given

**Parse (M1).** The agent sees the Vidyut candidate analyses (at most 8 shown per word),
with no derivations and no sūtras, and every commentary passage in full (14–16) before
any lexical evidence (`compile.construe_input`). It may run `tool.py` commands.

**Meaning call (M2–M5).** `pipeline.evidence_at` sends, per content word:

| Evidence | Sent | Not sent |
|---|---|---|
| Root | ≤2 Dhātupāṭha arthas | Dhātuvṛtti texts (built by `evidence.sanskrit_card`, then dropped); affix meanings (exist nowhere in code); kāraka beyond a `relation` field and an English case hint |
| Lexical texts | first Amarakośa group, cut to 220 characters; first SKD/VCP entry, cut to 260 | Amaraviveka (excluded by a work filter), Halāyudha, Vaijayantī, Yādava, Ākhyātacandrikā, Nirukta and Nighaṇṭu, the 4,712 meaning pages; verbs get no Amara at all |
| Usage | ≤3 other Gītā lines | counts and statistics; other loci; the Mahābhārata |
| Commentaries | ≤7 gloss clauses at this verse, beside the lexical lines | the rest; no staged "last" position |

The card also carries English (root-cognate English words, standing English renderings),
although this step is meant to use Sanskrit sources only.

**Translate call (E2–E3).** Gets the literal meaning, readings and up to 10 English
candidates per word, in this order: the model's own remembered words, semantic search,
keyword search, root cognates. The prompt inserts ENGLISH_CRAFT's five principles and §2
steps 3–6, and the standard §7.1–§7.16, verbatim at run time; it does not insert
ENGLISH_CRAFT steps 1–2, standard §7.17 or §8.

**English workbench state.** The semantic index holds 27 of 44 shards (about 540,000 of
872,157 definitions; `prakriya/tmp/english/bench/`); no build is running. In the
held-out ch15 run, of the 115 word choices the model labelled neither `grammar` (function
words) nor `standing` (term rows), it labelled 110 `found_by: remembered` and 5 `retrieved`
(`internal/gita_pipeline/run/ch15-heldout/translate/*.json`).

### 4.3 Known check defects

Listed with their code locations in
[`scripts/gita/translate/README.md`](../scripts/gita/translate/README.md#known-defects):
second lines unchecked, a loss rule that cannot fire, silent skips when a tool is
missing, a trace check that admits any remembered word, and unaccepted construals loaded.
Each is a gap in §5.

### 4.4 Publication state

- Live: chapter 12 (2026-11-08, origin/main commit 9c8fb7b) and chapter 5 (an older
  reader that predates the standard), plus the thematic readers `gita/sthitaprajna` and
  `gita/kama`. Chapter 12 was built by `build_gita_chapter_reader.py` from the older
  producer/reviewer files, not by `pipeline.py`. Its audio is P R Iyer, `provisional`.
- Pipeline output cannot yet be published: nothing converts
  `run/<run>/translate/*.json` into the builder's input, and the whole-article page
  `gita/bhagavad-gita/` has not been built.
- Repository (2026-11-09): the toolchain (`scripts/gita/`, including `translate/`), these
  documents and the ignore rules that keep `internal/gita_pipeline/` and the private
  requirement files out of git are on origin/main. The shared local checkout's `main` is
  behind origin/main and holds untracked copies of these files; it needs a sync (move the
  untracked copies aside, then fast-forward).

### 4.5 Results so far

| Run | Chapter role | Translate | Consistency | Overlap with reference |
|---|---|---|---|---|
| `ch12-qual` | development | 16 units, 88 calls, 616 s | 4 groups, 3 units redone, 7/9 placements compliant | 0.64 |
| `ch15-heldout` | held-out | 19 units, 101 calls, 888 s | 12 groups, 9 units redone, 42/46 compliant | 0.43 |

Parse of ch15: 682 s, 14.6 M tokens. Overlap is the mean content-word Jaccard against a
local, private reference (`internal/gita_pipeline/gold/`); it points to where to read,
it is not a quality score. Chapter 12 lines appear as examples in ENGLISH_CRAFT §3, so
chapter 12 is not a clean test. Commentary lookups for chapters 13–18 were off by one
verse until 2026-11-09 (fixed in prakriya `scripts/lookup/lookup.py` `gita_verse_id`,
test `tests/lookup/test_gita_alignment.py`, uncommitted); ch15 was re-parsed after the
fix, while 95 of the 4,712 meaning pages and the grammar coverage report predate it.

## 5. Gaps

Ranked by effect on the translation.

| # | Gap | Effect on the translation | Where | Fix |
|---|---|---|---|---|
| 1 | The meaning call gets a capped fraction of the library (§4.2) | Senses the texts give are never seen; the model fills in from memory | `pipeline.evidence_at`, `evidence.amara_section` | Feed the meaning pages and Dhātuvṛttis in full (compact, deduplicated), in the owner's order; a coverage check that every inventory source with an entry for the lemma reaches the card or is recorded as absent |
| 2 | No derivation and no affix or kāraka meanings | Meaning is not built from the morphemes; suffix force can be lost | `compile.construe_input`, `pipeline.unit_card`; no affix table exists | Send `grammar derive` steps with sūtras; build an affix and kāraka meaning table cited to the grammar |
| 3 | Order inverted: the parse reads all commentaries first; the meaning call mixes glosses with lexical lines | Commentators' readings can steer grammar and sense before the texts are heard | `drive.py construe`, `prompts3/meaning.md` | Grammar-first parse from code candidates; commentaries as a final, separate witness stage |
| 4 | English chosen mostly from memory; index 27/44; tool failures silent | Words are not found by meaning; dictionary breadth is unused; a run can skip checks without saying so | `pipeline.candidates`, `trace_errors`, `grammar`, `english_bench._index` | Finish the index; fail loudly when a tool is missing; rank retrieved words first and record why a remembered word wins; cache phrase frequencies before the run |
| 5 | Second lines unchecked | A fork line can add or drop meaning undetected | `pipeline.check_unit`, `line_errors` | Apply every word and line check to `alternative` |
| 6 | Usage thin: 3 lines, no statistics, no Mahābhārata | Sense at a place is chosen without the text's own usage pattern | `evidence.elsewhere_section`; `mbh: null` in packets | Counts by sense from the concordance; acquire the Mahābhārata |
| 7 | English in the meaning card | The Sanskrit-only step is primed with English | `pipeline.unit_card` | Remove English from that card |
| 8 | No publication bridge | Pipeline output cannot reach the site | `build_gita_chapter_reader.py`, `scripts/gita/build_whole_gita.py` | A converter to the builder's card format (meaning lines, evidence, derivation), then the whole article |
| 9 | Consistency per chapter only; decisions not merged | The book can render one sense two ways across chapters | `pipeline.py consistency` | A whole-book pass; owner-approved decisions written to `term_policy.json` |
| 10 | Loss rule and owner sheet read absent fields | Lost significations are not surfaced to the owner | `pipeline.check_unit`, `pipeline.sheet` | Align schema, check and sheet; unit tests |
| 11 | No whole-book driver; unaccepted construals loaded | Manual chapter-by-chapter runs; a rejected parse can be translated | `drive.main`, `pipeline.load` | One driver over 18 chapters; load accepted construals only |
| 12 | Codex is the only runner; the parse is agentic | Not runnable from Claude or ChatGPT; parse cost 14.6 M tokens for one chapter | `pipeline.call`, `drive.codex` | A runner interface with Codex and Claude backends; a tool-free parse card |
| 13 | The shared local checkout is behind origin/main | Local runs use files that differ from the published ones until synced | git state (§4.4) | Sync the shared checkout (§6.2) |
| 14 | Stale derived data after the alignment fix | 95 meaning pages and the coverage report may carry neighbour-verse glosses for ch13–18 | `internal/gita_pipeline/packets/meaning/`, `prakriya/tests/gita_kit/coverage_report.json` | Rebuild both |

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

## 7. Roadmap (dependency order, no dates)

| # | Step | Depends on | Done when |
|---|---|---|---|
| 0 | Sync the shared local checkout with origin/main (toolchain, documents and private ignore rules are committed) | owner | `git status` clean for these paths |
| 1 | Evidence feed in the owner's order (gaps 1, 2, 3, 7) with a coverage check; rebuild stale meaning pages | 0 | Every inventory source with an entry reaches the card or is recorded as absent; derivations and affix meanings on the card; no English in the meaning card; unit tests |
| 2 | Acquire the Mahābhārata (clean, provenance recorded per `CLEAN_SANSKRIT_ACQUISITION.md`); usage statistics for the Gītā and the epic | 1 (card format) | Per-lemma counts by sense on the card |
| 3 | Grammar-first parse: a tool-free card from code candidates and derivations; commentaries only as witnesses; load accepted construals only | 1 | ch12 and ch15 re-parsed; grammar review passes |
| 4 | English retrieval: full index, loud failures, retrieved-first ranking, cached phrase data; checks on second lines; fix the loss rule and owner sheet | — | ch12 dev and ch15 held-out re-run; found-vs-remembered measured; tests |
| 5 | Publication bridge: pipeline output → builder cards → whole article (`gita/bhagavad-gita/`) | 1, 3, 4 | ch12 and ch15 build fail-closed from pipeline output |
| 6 | Full-book run: one driver over 18 chapters; Claude and Codex runners; one prompt the owner can paste | 5 | 700 verses translated and checked |
| 7 | Whole-book consistency; owner-approved decisions into `term_policy.json` | 6 | No unresolved conflicts across chapters |
| 8 | Owner taste review; changes fed back as rows and rules | 7 | Owner sign-off per chapter |
| 9 | Audio for all chapters on the chosen source; owner listening | recitation decision | Every verse timed; manifests `verified` |

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
| `scripts/gita/translate/` | Current pipeline: `drive.py` (parse), `pipeline.py` (translate, consistency, sheet), `evidence.py`, `english*.py`, `check.py`, `compare.py`, `prompts3/`, `tests/` |
| `scripts/gita/build_all_packets.py`, `build_commentary_packets.py`, `gitapipe/` | Verse, commentary and meaning packets |
| `scripts/build_gita_chapter_reader.py`, `scripts/deploy_gita_chapter.sh`, `scripts/gita/build_whole_gita.py` | Building and deploying readers |
| `scripts/audio/` | Recitation alignment and mastering |
| `data/glossary/term_policy.json`, `scripts/gita/translate/seed_terms.json` | Owner term decisions; seed decisions |
| `assets/gita.js`, `assets/gita.css`, `gita/ch*/` | The reader and published chapters |
| prakriya `scripts/lookup/lookup.py`, `scripts/gita_kit/` | Source lookups; grammar and meaning oracles |
| `internal/gita_pipeline/` (local, git-ignored) | Packets, runs, private references |
