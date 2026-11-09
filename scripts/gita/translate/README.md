# scripts/gita/translate — the Gītā translation code

This folder holds the code that translates the Bhagavad-Gītā word by word: a parse stage, a
translate stage and a chapter consistency stage. Code gathers the evidence and enforces every
rule that can be checked mechanically; a model makes the judgements, one bounded card per call.

The goal, the translation method and the project status are in
[docs/GITA_FULL_TRANSLATION_PLAN.md](../../../docs/GITA_FULL_TRANSLATION_PLAN.md). The rules are in
[docs/SANSKRIT_TRANSLATION_STANDARD.md](../../../docs/SANSKRIT_TRANSLATION_STANDARD.md) and
[docs/gita_briefs/ENGLISH_CRAFT.md](../../../docs/gita_briefs/ENGLISH_CRAFT.md). This file
describes the code as it is (read from the source, 2026-11-09).

## Modules

| File | Status | Role |
|---|---|---|
| `drive.py` | `construe`: current; `lexicon`, `verse`: retired | Agent runner: author → code check → independent review → revise, up to `GITA_MAX_ROUNDS` (3) rounds |
| `pipeline.py` | current | `translate`, `consistency` and `sheet` stages; the code checks |
| `compile.py` | `verse_packet`, `commentary`, `construe_input`, `units`: current; `families`, `family_input`, `unit_input`: retired | Builds job inputs from the packets |
| `check.py` | `construe`, `verse`, `forbidden_reads` and word lists: current; `lexicon`: retired | Exact checks on job outputs |
| `evidence.py` | current | The Sanskrit card per lemma (`sanskrit_card`) from the prakriya lookup layer |
| `english.py` | current | Reverse dictionary over seven English dictionaries (`english_table`) |
| `english_roots.py` | current | English words sharing a Sanskrit root through Proto-Indo-European, or carrying its image (`by_sanskrit`) |
| `english_bench.py` | current | English workbench: semantic search, word profiles, phrase frequency, line metrics |
| `compare.py` | current (evaluation only) | Content-word overlap of each line with a local reference translation |
| `tool.py` | current (used by the construe agent) | The agents' command surface over the Sanskrit library and English dictionaries; logs every call |
| `seed_terms.json` | current | The plan's seed term decisions (54 rows: 27 preserve, 27 translate); binding unless a translation records a challenge |
| `prompts3/` | current | `meaning`, `translate`, `review`, `consistency` prompts for `pipeline.py` |
| `prompts/` | `construe.md`, `review_construe.md`, `revise.md`, `criteria.md`: current; `lexicon.md`, `review_lexicon.md`, `verse.md`, `review.md`: retired | Agent prompts for `drive.py`; `criteria.md` is appended to every one |
| `run.py`, `prompts2/` | retired | The lexicon-first design (see Design history) |
| `tests/` | current | 103 test functions (some parametrized): `test_check` 10, `test_english_roots` 25, `test_english` 19, `test_evidence` 19, `test_pipeline` 30 |

Several docstrings still cite "WORKFLOW.md"; that document now lives in
[docs/history/gita/](../../../docs/history/gita/), and this README replaces it.

## Dependencies outside this repository

- **prakriya** checked out at `~/Dev/prakriya` (the path is hard-coded): `scripts/lookup/lookup.py`
  (Sanskrit library, BORI text, commentaries, English index) and `scripts/gita_kit/` (grammar and
  meaning oracles; the grammar oracle runs Vidyut from `prakriya/tmp/vidyut-venv`). The kit is
  documented in prakriya `docs/GITA_KIT.md`.
- **Python environment** `prakriya/tmp/english/benchenv/` (numpy, wordfreq, pronouncing, ollama,
  language-tool-python, pytest; lemminflect optional). Run `pipeline.py`, `english_bench.py`,
  `compare.py` and the tests with `prakriya/tmp/english/benchenv/bin/python`.
- **English data** under `prakriya/tmp/english/`: `english.db` (seven dictionaries), `etym.db`
  (from the kaikki Wiktionary dump) and `bench/` (semantic index, profiles, Ngram cache).
- **Ollama** running locally with `qwen3-embedding:0.6b` (one embedding call per semantic query).
  The semantic index is partly built: 27 of 44 shards, so `find` searches about 540,000 of 872,157
  definitions (a uniform sample; `english_bench.py build-index` resumes the build).
- **Java 21 + LanguageTool** (`language_tool_python`); `pipeline.py` sets `JAVA_HOME` to
  `/opt/homebrew/opt/openjdk@21` if unset.
- **Network**: the Google Books Ngram JSON endpoint (`books.google.com/ngrams/json`, at most one
  request a second, cached in `bench/ngram_cache.sqlite`).
- **codex CLI**, run with an isolated `CODEX_HOME` (default `~/.codex-gita`). Codex is the only
  model runner implemented; there is no Claude or ChatGPT runner.
- **Packets** built once by `scripts/gita/build_all_packets.py` and
  `scripts/gita/build_commentary_packets.py` (see [../README.md](../README.md)).

Environment variables: `GITA_MODEL` (default `gpt-6-astra`), `GITA_EFFORT` (`high`),
`GITA_CODEX_HOME` (`~/.codex-gita`), `GITA_MAX_CALLS` (32 concurrent model calls, `pipeline.py`),
`GITA_MAX_ROUNDS` (3, `drive.py`), `GITA_REUSE_OUTPUT` (`drive.py`: reuse an existing output).

## Commands

Run from the repository root. `PY=~/Dev/prakriya/tmp/english/benchenv/bin/python`.

```sh
# Prerequisites (once)
python3 scripts/gita/build_all_packets.py [--chapters 1-18] [--workers 8]
python3 scripts/gita/build_commentary_packets.py [--chapter N]

# Stage 1, parse (agentic; codex with tool.py)
python3 scripts/gita/translate/drive.py construe --chapter N --run RUN [--jobs 10] [--only C.V ...] [--no-review]

# Stage 2, translate; stage 3, chapter consistency; the owner's decision sheet
$PY scripts/gita/translate/pipeline.py translate   --run RUN [--only C.V ...] [--jobs 24]
$PY scripts/gita/translate/pipeline.py consistency --run RUN [--jobs 24]
$PY scripts/gita/translate/pipeline.py sheet       --run RUN

# Evaluation against a local reference (never shown to the model)
$PY scripts/gita/translate/compare.py --run RUN --gold internal/gita_pipeline/gold/chN.md

# English workbench
$PY scripts/gita/translate/english_bench.py build-index            # resumable
$PY scripts/gita/translate/english_bench.py build-profiles
$PY scripts/gita/translate/english_bench.py find "a meaning in plain words"
$PY scripts/gita/translate/english_bench.py profile WORD ...
$PY scripts/gita/translate/english_bench.py line "an English line"
$PY scripts/gita/translate/english_bench.py ngram "phrase one" "phrase two"

# Tests (test_english* and test_evidence skip when their databases are absent)
$PY -m pytest scripts/gita/translate/tests
```

One run is one chapter: `pipeline.py` translates every construal under `run/RUN/construe/`.

## Data flow

1. **Parse** (`drive.py construe`). Input per verse: the BORI text, neighbouring verses, the word
   split, the Vidyut candidate analyses (no derivations, no sūtras) and every commentary passage in
   full (14–16 passages from 13 commentators). The agent may call `tool.py`. Output per word:
   analysis id or manual analysis, stem, root, upasargas, class, compound and vigraha, members,
   relation; plus referents, supplied words, forks and `continues_into_next`. Reviewed for grammar.
2. **Translate** (`pipeline.py translate`), per sentence unit (a verse, merged with the next when
   the sentence continues):
   1. Code builds the unit card: the parse, plus per content word `evidence_at` (≤2 Dhātupāṭha
      entries, the first Amarakośa group cut to 220 characters, the first Śabdakalpadruma or
      Vācaspatya entry cut to 260, ≤7 commentator gloss clauses at this verse, ≤3 other Gītā lines),
      member evidence, ≤6 English words sharing the root, and standing term rows.
   2. Model call `meaning` (no tools): per word the literal meaning, what commentators say it refers
      to here, the root image, readings, a ≤6-word search phrase and remembered English words.
   3. Code finds ≤10 English candidates per word (remembered words, semantic search, the reverse
      dictionary, root words), each with its matching and modern first sense, frequency, stress,
      origin and, for phrases, book frequency.
   4. Model call `translate`: the prompt carries ENGLISH_CRAFT's five principles and steps 3–6 and
      the standard's §7.1–§7.16 verbatim, read from the files at run time. Returns the line(s) and
      per word the English, kind (a–e), source, what is carried or lost, and why.
   5. Code checks (below), then model call `review` with measured line facts. Code errors and
      S1/S2 findings go back to `translate`, at most two revision rounds, each re-checked and
      re-reviewed; S3 findings are stored.
3. **Consistency** (`pipeline.py consistency`), per chapter: code groups lemmas rendered two ways
   and lemmas sharing one English word; one model call per group decides; units whose renderings
   differ are translated again with the decision fixed.

## Code checks

Parse (`check.construe`, `check.forbidden_reads`):
- Every word has a construal.
- `analysis_id` is one of the word's candidates, or a manual analysis is given.
- The word class is valid; a stem is present; a root is a bare `√X`.
- Each fork kind is valid; `continues_into_next` is a boolean.
- The agent touched no forbidden path and ran no command outside its folder or the tool.

Translate (`pipeline.check_unit`, `pipeline.line_errors`):
- Every verse has a line.
- Every content word, name, particle and pronoun has non-empty English.
- An alternative line requires a grammatical fork.
- Every content token of a line belongs to some word's English (function words excepted).
- A word's English has at most its morpheme count + 2 content words.
- Every non-particle compound member has an entry in `parts`; each part's English appears in the word's English.
- A member's or a word's fixed (consistency) rendering is used.
- A term row admits the rendering; a forbidden word is reported only when no row admits it; seed rows may be challenged.
- Every content token traces to the word's candidates, literal meaning, standing English, fixed rendering or parts.
- Kind e keeps the Sanskrit lemma.
- Without a standing row, every content token of a non-kind-e rendering is in the dictionaries.
- A kind-d formation names at least two models.
- A `?` requires a Sanskrit interrogative.
- At most one dash per line.
- No "of"-chain of three.
- No bare "whatsoever".
- No Sanskrit–English hyphenated hybrid.
- At most one kind-d formation per line.
- Every LanguageTool finding outside `LT_IGNORE` is an error.

## Known defects

- **Second lines are unchecked.** `alternative` lines pass through none of the line or word checks.
- **The loss rule cannot fire.** The check for an unexplained loss tests `step == "existing"`, a
  field the translate schema does not have. `sheet` likewise reads `step`, `means` and `signifies`,
  so it lists only losses and consistency decisions.
- **Silent skips when a tool is missing.** Each is a bare `except`: no semantic search or profiles
  when `english_bench` fails; no grammar check when LanguageTool or Java is missing; no lemminflect
  stemming when it is not installed; no phrase frequency when the network fails.
- **Unaccepted construals are used.** `pipeline.load` reads every `construe/*/output.json` and
  ignores `record.json.accepted` (`drive.load_outputs` does filter).
- **The trace check admits any remembered word**, because remembered words become candidates.
- **The evidence feed is truncated.** `evidence.sanskrit_card` builds more than `evidence_at`
  sends, and the meaning card also carries English. What reaches the model and what does not is
  measured in the plan, [§4.2](../../../docs/GITA_FULL_TRANSLATION_PLAN.md#42-what-the-model-is-actually-given).
- The `translate` prompt omits ENGLISH_CRAFT steps 1–2, standard §7.17 and §8.
- Consistency covers one chapter; decisions are not written to `data/glossary/term_policy.json`.
- No converter turns `run/RUN/translate/*.json` into the site's chapter build inputs, so pipeline
  output cannot yet be published.

The plan's [§5](../../../docs/GITA_FULL_TRANSLATION_PLAN.md#5-gaps) ranks these with the other gaps.

## Outputs

Everything is written locally under `internal/gita_pipeline/` (private; ignored by the working
tree's `.gitignore`, a rule not yet on `origin/main`):
- `run/RUN/construe/C.V/` holds `input.json`, `output.json`, `review*.json`, `record.json`, event
  and tool-call logs, and `summary.json`.
- `run/RUN/translate/<unit>.json` holds the calls, rounds, card and output; `_summary_translate.json`,
  `_consistency.json` and `_summary_consistency.json` sit beside them.
- `run/RUN/DECISIONS.md` (`sheet`) and `run/RUN/COMPARE.md` (`compare.py`).

## Design history

Three designs were built. The first gave agents tool access and disk jobs: a Gītā-wide lexicon,
then verses (the stages A–E queue in `scripts/gita/`, then `drive.py lexicon` and `verse`).
Lexicon jobs made 40–90 tool calls and took 10–13 minutes each, verified guesses instead of
finding words, and turned commentator glosses into senses. The second (`run.py`, `prompts2/`)
decided each word per lemma, out of context, by a code score over model marks: it produced odd
words, translationese lines and run-to-run variance, at about 650 calls per chapter, and its
English was worse than one in-context call per verse. The third, current design keeps the agentic
parse and decides words and line together in one tool-free call per sentence unit, with code
checks and a consistency pass. The retired specifications and their audits are in
[docs/history/gita/](../../../docs/history/gita/).
