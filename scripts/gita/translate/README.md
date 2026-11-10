# scripts/gita/translate — the Gītā translation code

This folder holds the code that translates the Bhagavad-Gītā word by word: a parse stage, a
translate stage, a consistency stage (a chapter or the whole book), the owner's decision sheet and
the bridge to the site builder. Code gathers the evidence and enforces every
rule that can be checked mechanically; a model makes the judgements, one bounded card per call.

The goal, the translation method and the project status are in
[docs/GITA_FULL_TRANSLATION_PLAN.md](../../../docs/GITA_FULL_TRANSLATION_PLAN.md). The rules are in
[docs/SANSKRIT_TRANSLATION_STANDARD.md](../../../docs/SANSKRIT_TRANSLATION_STANDARD.md) and
[docs/gita_briefs/ENGLISH_CRAFT.md](../../../docs/gita_briefs/ENGLISH_CRAFT.md). This file
describes the code as it is (read from the source, 2026-11-10).

## Modules

| File | Status | Role |
|---|---|---|
| `drive.py` | `construe`: current; `lexicon`, `verse`: retired | Parse runner: author → code check → independent review → revise, up to `GITA_MAX_ROUNDS` (3) rounds; the parse is tool-free and read-only |
| `pipeline.py` | current | `translate`, `consistency` (one run or several: the book) and `sheet` stages; the code checks; `preflight` of the English tools |
| `sanskrit_card.py` | current | The M1–M5 Sanskrit card for one word at one place, in the owner's order, with every source's status and an independent coverage `audit` |
| `affix_meanings.json` | current | The meaning sūtras of each kṛt and taddhita affix, lakāra, prayoga, sanādi suffix and case (every citation tested against the clean Aṣṭādhyāyī) |
| `mbh_usage.py` | current | Mahābhārata usage of a word: the grammar engine's paradigm matched against the BORI critical text |
| `runner.py` | current | One model call through Codex or Claude (`GITA_RUNNER`), tool-free |
| `book.py` | current | The whole book: parse, translate and sheet per chapter, then one consistency pass over all chapters |
| `publish.py` | current | Run records → the chapter builder's input (fail-closed; see Publication bridge) |
| `compile.py` | `verse_packet`, `commentary`, `construe_input`, `units`: current; `families`, `family_input`, `unit_input`: retired | Builds the parse card (grammar first, commentaries last) and the sentence units |
| `check.py` | `construe`, `verse`, `forbidden_reads` and word lists: current; `lexicon`: retired | Exact checks on job outputs |
| `evidence.py` | current (as a library) | Lemmas from the parse, and the section builders `sanskrit_card.py` uses (Dhātupāṭha and Dhātuvṛtti windows, kośa hits, SKD/VCP entries, occurrences, Gītā usage) |
| `english.py` | current | Reverse dictionary over seven English dictionaries (`english_table`) |
| `english_roots.py` | current | English words sharing a Sanskrit root through Proto-Indo-European, or carrying its image (`by_sanskrit`) |
| `english_bench.py` | current | English workbench: semantic search, word profiles, phrase frequency, line metrics, `index_state` |
| `compare.py` | current (evaluation only) | Content-word overlap of each line with a local reference translation |
| `tool.py` | retired with the agentic stages | The agents' command surface; the parse no longer uses it |
| `seed_terms.json` | current | The plan's seed term decisions (54 rows: 27 preserve, 27 translate); binding unless a translation records a challenge |
| `prompts3/` | current | `meaning`, `translate`, `review`, `consistency` prompts for `pipeline.py` |
| `prompts/` | `construe.md`, `review_construe.md`, `revise.md`: current; `criteria.md` (appended to the retired stages' prompts), `lexicon.md`, `review_lexicon.md`, `verse.md`, `review.md`: retired | Prompts for `drive.py` |
| `run.py`, `prompts2/` | retired | The lexicon-first design (see Design history) |
| `tests/` | current | `test_check`, `test_english_roots`, `test_english`, `test_evidence`, `test_pipeline`, `test_sanskrit_card`, `test_runner_book`, `test_publish` (230 passing, 3 expected failures, 2026-11-10) |

## Dependencies outside this repository

- **prakriya** checked out beside this repository (`../prakriya`): `scripts/lookup/lookup.py`
  (Sanskrit library, BORI text, commentaries, English index, sūtra text) and `scripts/gita_kit/`
  (grammar and meaning oracles), documented in prakriya `docs/GITA_KIT.md`.
- **The Mahābhārata**, BORI critical text from GRETIL, cleaned to keyed IAST:
  `prakriya/corpus/acquisition-20261109/itihasa/mahabharata_bori_gretil/` (local; the terms grant
  no redistribution, so it is not committed). Without it the card records "not in the library".
- **Python environments.** `prakriya/tmp/english/benchenv/` (numpy, wordfreq, pronouncing, ollama,
  language-tool-python, lemminflect, pytest) runs `pipeline.py`, `drive.py`, `book.py`,
  `english_bench.py`, `compare.py`, `publish.py` and the tests. `prakriya/tmp/vidyut-venv/` (Vidyut
  0.4.0) runs `mbh_usage.py forms` only.
- **English data** under `prakriya/tmp/english/`: `english.db` (seven dictionaries), `etym.db`
  (kaikki Wiktionary) and `bench/` (semantic index of 44 shards, 872,157 definitions; profiles;
  Ngram cache).
- **Ollama** running locally with `qwen3-embedding:0.6b`.
- **Java 21 + LanguageTool**; `pipeline.py` sets `JAVA_HOME` to `/opt/homebrew/opt/openjdk@21` if unset.
- **Network**: the Google Books Ngram JSON endpoint (≤1 request a second, cached); a failed request
  leaves the phrase's frequency unknown and is counted in the run summary (`ngram_failures`).
- **A model CLI**: `codex` (default) or `claude` (`GITA_RUNNER=claude`; every tool disabled, files
  inlined). The Claude backend is implemented and tested without model calls; its first live call
  was refused by the account's usage control (paid extra usage not allowed).
- **Packets** built once by `scripts/gita/build_all_packets.py` and
  `scripts/gita/build_commentary_packets.py` (see [../README.md](../README.md)).

`pipeline.py` runs `preflight` before any model call: the semantic index complete, the embedding
server answering, LanguageTool and lemminflect present. A missing tool stops the run unless
`--allow-partial-tools` is given, and the state is written to the run summary.

Environment variables: `GITA_RUNNER` (`codex` | `claude`), `GITA_MODEL` (`gpt-6-astra`),
`GITA_CLAUDE_MODEL` (`claude-opus-5-5`), `GITA_EFFORT` (`high`), `GITA_CODEX_HOME`
(`~/.codex-gita`), `GITA_MAX_CALLS` (32 concurrent calls, `pipeline.py`), `GITA_MAX_ROUNDS` (3,
`drive.py`), `GITA_REUSE_OUTPUT` (`drive.py`).

## Commands

Run from the repository root. `PY=~/Dev/prakriya/tmp/english/benchenv/bin/python`,
`VPY=~/Dev/prakriya/tmp/vidyut-venv/bin/python`.

```sh
# Prerequisites (once)
python3 scripts/gita/build_all_packets.py [--chapters 1-18] [--workers 8]
python3 scripts/gita/build_commentary_packets.py [--chapter N]

# The whole book (or any chapters): parse, translate, sheet per chapter; then one consistency pass
$PY scripts/gita/translate/book.py --prefix book --chapters 1-18 [--parallel 3] [--jobs 12]

# Or stage by stage, one chapter per run
$PY scripts/gita/translate/drive.py construe --chapter N --run RUN [--jobs 20] [--only C.V ...]
$PY scripts/gita/translate/mbh_usage.py lemmas RUN [RUN ...]          # then:
$VPY scripts/gita/translate/mbh_usage.py forms                        # Mahābhārata paradigms
$PY scripts/gita/translate/pipeline.py translate   --run RUN [--only C.V ...] [--jobs 24]
$PY scripts/gita/translate/pipeline.py consistency --run RUN [RUN ...] [--jobs 24]
$PY scripts/gita/translate/pipeline.py sheet       --run RUN [RUN ...]

# One word's Sanskrit card, as the meaning call receives it
$PY scripts/gita/translate/sanskrit_card.py RUN C.V I

# Evaluation against a local reference (never shown to the model)
$PY scripts/gita/translate/compare.py --run RUN --gold internal/gita_pipeline/gold/chN.md

# English workbench
$PY scripts/gita/translate/english_bench.py build-index            # resumable
$PY scripts/gita/translate/english_bench.py find "a meaning in plain words"
$PY scripts/gita/translate/english_bench.py profile WORD ...
$PY scripts/gita/translate/english_bench.py line "an English line"

# Tests
JAVA_HOME=/opt/homebrew/opt/openjdk@21 $PY -m pytest scripts/gita/translate/tests
```

## Data flow

1. **Parse** (`drive.py construe`), tool-free and read-only. The card (`compile.construe_input`)
   gives, in this order: the BORI verse; for each token the grammar engine's candidate analyses of
   each of its padas (tokens are mapped to padas through the packet's `bori_token`, so a
   sandhi-joined token has several), the top 8 with their derivation (prakṛti + pratyaya with
   sūtras) and up to 40 further analyses without; the neighbouring verses; and last every
   commentary passage (14–16, from 13 commentators). Output per word: analysis id (or a manual
   analysis with the reason every candidate fails), stem, root, upasargas, class, compound,
   relation; referents, supplied words, forks, `continues_into_next`. Reviewed for grammar. Only
   accepted parses are translated.
2. **Translate** (`pipeline.py translate`), per sentence unit:
   1. Code builds the unit card; each content word carries its Sanskrit card (`sanskrit_card.py`):
      M1 decode (analysis, prakṛti, affixes, derivation), M2 morpheme meanings (Dhātupāṭha entries,
      Dhātuvṛtti windows from the Mādhavīya, Kṣīrataraṅgiṇī, Dhātupradīpa and Daiva, the meaning
      sūtras of every affix and case), M3 lexical texts (Amarakośa, Amaraviveka, Halāyudha,
      Vaijayantī, Yādavakośa, Ākhyātacandrikā, Nirukta, Nighaṇṭu, Śabdakalpadruma, Vācaspatya),
      M4 usage (Gītā places and lines; Mahābhārata count, by parvan, examples), M5 the commentators'
      clauses at this verse, and every source's status. Compound members carry M2 and M3.
      `audit` checks that every kośa or Nirukta work with an entry is shown.
   2. Model call `meaning` on the Sanskrit-only view (no English term rows, no English case hints):
      per word the literal meaning with its grounds, what commentators say it refers to here, the
      root image, readings, a search phrase and remembered English words. Code checks that each
      content word has a literal meaning grounded in a text when the texts have entries; one
      correction round.
   3. Code finds up to 12 English candidates per word: semantic search, image search and the reverse
      dictionary first, then remembered words (≤4), then root words (≤2); each with its matching and
      modern senses, dictionary loci, frequency, stress, origin and, for phrases, book frequency.
   4. Model call `translate`: the prompt carries ENGLISH_CRAFT's five principles and steps 3–6, the
      standard's §7.1–§7.17, §8.1 and §8.5, verbatim from the files at run time. Returns the line,
      the slotted line (each word's English at its place), per word the English, kind (a–e),
      source, what is carried or lost and why, and a second line where a grammatical fork needs one.
   5. Code checks (below), then model call `review` with measured line facts. Code errors and S1/S2
      findings go back to `translate`, at most two revision rounds; S3 findings are stored.
3. **Consistency** (`pipeline.py consistency`), over one run or several (the book): code groups
   lemmas rendered two ways and lemmas sharing one English word across all the runs; one model call
   per group decides; units that break a decision are translated again in their own run.
4. **Sheet** (`pipeline.py sheet`): formations, Sanskrit kept, losses, challenged seed decisions,
   second lines and consistency decisions, with each word's literal meaning, for the owner.

## Code checks

Parse (`check.construe`, `check.forbidden_reads`):
- Every word has a construal.
- `analysis_id` is one of the word's candidates, or a manual analysis is given.
- The word class is valid; a stem is present; a root is a bare `√X`.
- A sandhi-joined token without one analysis gives one entry per pada.
- Each fork kind is valid; `continues_into_next` is a boolean.
- The agent touched no forbidden path and ran no command outside its folder or the tool.

Meaning (`pipeline.meaning_errors`):
- Every content word and name has a literal meaning (or "unresolved") and its grounds.
- A literal meaning grounded only in commentaries is an error when the word's M2 or M3 has entries.

Translate (`pipeline.check_unit`, `pipeline.line_errors`, `pipeline.slot_errors`):
- Every verse has a line, and a slotted line that equals it without its slots; every word's English
  is in its slot.
- The second line passes every check the first does.
- Every content word, name, particle and pronoun has non-empty English.
- An alternative line requires a grammatical fork.
- Every content token of a line belongs to some word's English (function words excepted).
- A word's English has at most its morpheme count + 2 content words.
- Every non-particle compound member has an entry in `parts`; each part's English appears in the word's English.
- A member's or a word's fixed (consistency) rendering is used.
- A term row admits the rendering; a forbidden word is reported only when no row admits it; seed rows may be challenged.
- Every content token traces to the word's candidates, literal meaning, standing English, fixed rendering or parts.
- Kind e keeps the Sanskrit lemma.
- A loss (`carried` false) says what is lost; in kinds a–c it needs a reason why neither a formation
  nor the Sanskrit serves.
- A remembered word names, in `why`, the retrieved candidate it beats.
- Without a standing row, every content token of a non-kind-e rendering is in the dictionaries.
- A kind-d formation names at least two models.
- A `?` requires a Sanskrit interrogative.
- At most one dash per line.
- No "of"-chain of three.
- No bare "whatsoever".
- No Sanskrit–English hyphenated hybrid.
- At most one kind-d formation per line.
- Every LanguageTool finding outside `LT_IGNORE` is an error (LanguageTool missing stops the run).

## Known defects

- The Gītā-usage lines (`evidence.elsewhere_section`) can include a different word that the grammar
  engine also analyses with this stem (aśvatthāmā under aśvattha).
- `mbh_usage` counts whole words only: compound members and words fused by vowel sandhi (caiva) are
  not counted; homographs the grammar's lexicon knows are excluded and counted, others are not.
  Four lemmas of chapters 12 and 15 get no paradigm (āviś, ādhā, samādhā, saṃmūḍha).
- Manually analysed words (40 of 261 in the chapter 15 parse of 2026-11-09) have no derivation.
- The consistency decisions are not written to `data/glossary/term_policy.json`; that table is the
  owner's, and only owner-approved rows go into it.
- `GITA_JOB_LOG`, `tool.py` and `check.lexicon` serve only the retired agentic stages.
- Publication: see the bridge section below for what the builder still requires.

The plan's [§5](../../../docs/GITA_FULL_TRANSLATION_PLAN.md#5-gaps) lists the gaps and their state.

## Outputs

Everything is written locally under `internal/gita_pipeline/` (private; git-ignored):
- `run/RUN/construe/C.V/` holds `input.json`, `output.json`, `review*.json`, `record.json`, event
  and tool-call logs, and `summary.json`.
- `run/RUN/translate/<unit>.json` holds the calls, the meaning card the model was given, the meaning,
  rounds, the translate card and output; `_summary_translate.json`,
  `_consistency.json` and `_summary_consistency.json` sit beside them.
- `run/RUN/DECISIONS.md` (`sheet`) and `run/RUN/COMPARE.md` (`compare.py`); `run/PREFIX-book.json`
  (`book.py`).
- `packets/usage/` holds the Mahābhārata token index, the lemma list and the paradigms.

## Design history

Three designs were built. The first gave agents tool access and disk jobs: a Gītā-wide lexicon,
then verses (the stages A–E queue in `scripts/gita/`, then `drive.py lexicon` and `verse`).
Lexicon jobs made 40–90 tool calls and took 10–13 minutes each, verified guesses instead of
finding words, and turned commentator glosses into senses. The second (`run.py`, `prompts2/`)
decided each word per lemma, out of context, by a code score over model marks: it produced odd
words, translationese lines and run-to-run variance, at about 650 calls per chapter, and its
English was worse than one in-context call per verse. The third, current design decides words and line together in one tool-free call per sentence
unit, with code checks and a consistency pass; since 2026-11-10 the parse too is tool-free, from a
grammar-first card, and the meaning call receives the Sanskrit evidence in the owner's order. The retired specifications and their audits are in
[docs/history/gita/](../../../docs/history/gita/).

## Publication bridge (`publish.py`)

`publish.py` converts one run's translate records into the input of the fail-closed chapter
builder `scripts/build_gita_chapter_reader.py`: `DIR/packet.json` (each verse's BORI IAST,
Devanāgarī, speaker and metre, from `internal/gita_pipeline/packets/verses/`), one shard
`DIR/producer-01-NN.json` (schema `gita-producer-v2`) and `DIR/independent-review-01-NN.json`
(the pipeline's review findings and the shard's sha256; `complete` and `date` have no source in the
run and are not written). Every field is copied from the run record or the verse packet, or computed
from them: Devanāgarī by transliteration; `{i:…}` slots from `output.slotted` (new runs) or by
locating each word's English in its line; root with gaṇa, pada, `root_id` and `rootGloss`, `affix`,
morpheme `parts` and `evidence` (Dhātupāṭha record, Aṣṭādhyāyī sūtra lines) from the grammar
engine's analysis of the word (`analyses.sqlite`, through the accepted parse's `analysis_id`);
wording candidates' loci from define (new runs). A field the run does not hold stays absent. The
second line becomes an open fork (reason class 5) whose `display` is that line. The mapping is in the
module docstring.

```sh
$PY scripts/gita/translate/publish.py --run RUN --chapter N --out DIR [--allow-unfinished] [--check]
$PY -m pytest scripts/gita/translate/tests/test_publish.py
```

It refuses (exit 1, nothing written) when a verse of the chapter is in no unit record or in two;
when a unit has no output, or code errors, S1/S2 review findings or meaning errors left; or when
a field the builder requires is absent, a claim lacks its own evidence, or a word's English cannot
be placed in its line unambiguously. `--allow-unfinished` writes anyway (exit 2), lists every reason
under `unfinished` on the shard and each verse, and sets `schema_version` to
`gita-producer-v2+unfinished`, which the builder refuses (B12). `--check` then runs the builder's
checks on DIR without writing anything. It never writes beside producer shards, reviews or a packet
it did not write, so it cannot mix with chapter 12's hand-made files.

Measured 2026-11-09 (`--allow-unfinished --check` into a scratch directory; both runs predate the
`slotted` lines and candidate loci): neither run can be published. `ch15-heldout`: 737 reasons
before the builder; 2,707 builder errors (B4 2,106 candidates without loci; CARD 450; B17 72; VERSE
60; B11 6; B9 6; B5 2; REVIEW 2; POLICY 1; B1, B12 one each). Of 279 cards, the 141 with an engine
analysis carry verified grammar and evidence; the 138 with a manual analysis have no `affix`, no
morpheme `parts`, and their roots no gaṇa or pada. `ch12-qual`: 586 reasons; 1,178 builder errors
(151 of 236 cards analysed). Not fillable from any run: the verse `sense` and `grammar`, five
consulted secondaries (the §9 blind check, an owner decision), the review's `complete`, the
term-policy hash, and grammar for manually analysed words.
