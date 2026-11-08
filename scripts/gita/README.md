# scripts/gita — the whole-Gītā translation pipeline (deterministic machinery)

Governing decisions: prakriya `docs/TRANSLATION_PIPELINE_SPEC.md` §0 and §0.6 (code
generates every analysis and derivation, the agent only chooses; Vidyut is a provisional
engine behind the oracle interface); `docs/gita_briefs/SCHEMAS.md` (the job schemas this
code implements); `docs/SANSKRIT_TRANSLATION_STANDARD.md` §2–§3 (card contract, public
text); `docs/GITA_FULL_TRANSLATION_PLAN.md` §7 (stages A–E); `docs/GITA_CH12_PIPELINE_AUDIT.md`
§4. This file is the plan, written before the code, and the runbook.

## What an agent runtime does (docs/gita_briefs/RUNBOOK.md)

```
python3 scripts/gita/run_pipeline.py --stage A [--batch 12]   # packets etc. (once); lexicon + lexicon-review jobs
workers loop: python3 scripts/gita/queue.py next --type T --worker NAME  →  follow the job's brief  →  run its validate  →  queue.py submit ID
python3 scripts/gita/run_pipeline.py --stage B        # lexicon-fix/-rereview for 'revise'; requested lemmas → new lexicon jobs;
                                                      # when all accepted: merge (v3, installed; a collision queues a lexicon-fix) + verse jobs
python3 scripts/gita/run_pipeline.py --stage C        # expand each submitted verse output; queue its review (or rereview after a fix)
python3 scripts/gita/run_pipeline.py --stage D        # fix jobs (agent_ref = the producer); accepted requests and inline decisions merged;
                                                      # one lemma decided inline differently in two shards → a lexicon job; changed rows → rereview
python3 scripts/gita/run_pipeline.py --stage E --chapters 2,3   # builder --check-only here; then scripts/deploy_gita_chapter.sh
                                                      # builds + commits them and the whole-Gītā article in a clean worktree (never pushes)
python3 scripts/gita/run_pipeline.py --status
```

Acceptance run of chapter 12 against its reviewed shards (namespace internal/gita_pipeline/acceptance/ch12/,
job ids `acc12-…`, same queue and workers, its own merged table, never installed, reviewed shards untouched):

```
python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage A    # lexicon jobs for chapter 12's lemmas only
  … workers …
python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage B    # → verse jobs for 12.1–20 when the lexicon is accepted
python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage C    # → review jobs
python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage D    # → fix / rereview
python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage E    # builder (complete mode) + acceptance_report.json
```

Lexicon scope (lead, 2026-11-08): lemmas of weight ≥ 3 (occurrences not shared with a pronoun/particle
reading or another content lemma), every lemma matching a table row or a glossary (system) term, and every
requested lemma. Other content words are decided inline in the verse job (SCHEMAS "Inline sense fields");
merge records them as lexicon entries once their verse review accepts.

Helpers: `show_analysis.py FORM | --id ID`, `validate_job.py TYPE OUTPUT`, `expand_cards.py`, `merge_lexicon.py
[--namespace ch12]`, `build_whole_gita.py [--root WORKTREE --register]`, `convert_ch12.py` (round trip).

## Components

| File | Stage | Does |
| --- | --- | --- |
| `gitapipe/common.py` | all | paths, atomic JSON io, hashing, loci, verse counts, the import guard for `queue.py`'s name |
| `gitapipe/store.py`, `show_analysis.py` | A | every Analysis and compact Derivation by id (`packets/analyses.sqlite`, deduplicated across the Gītā); verse packets carry ranked one-line summaries (≤ 8 shown per pada, every id kept) |
| `gitapipe/oracle.py` | A | the oracle seam: prakriya `scripts/gita_kit/` grammar (`analyze`, `derive`, `split`) and meaning (`page`), imported in process when possible, else the `gita_kit.py` CLI; a clear error when a module is absent; a fixture oracle for tests |
| `build_all_packets.py` | A | per verse packet; Gītā-wide lemma inventory, concordance, meaning pages (deduplicated), shard plan, manifest with timings |
| `build_jobs.py` | A→D | queue jobs: lexicon (≈8 lemmas, grouped by table row, system terms and high weight first) + lexicon-review; verse (the shard plan, ≈60 cards, sentence units; chapter 12 only with --include-ch12); review/rereview (input: the frozen verse output, its expanded shard and builder report, the private translations file) |
| `gitapipe/validate.py`, `validate_job.py TYPE OUTPUT` | B–D | schema + referential checks per job type; a verse output is also expanded and run through the builder's card/verse checks |
| `gitapipe/lexicon.py`, `merge_lexicon.py` | B | reviewed lexicon outputs → term policy v3 (v2 structure, superset of the current table, legacy rows migrated by `migrate_term_policy_v2.migrate`), conflicts reported |
| `gitapipe/expand.py`, `expand_cards.py` | C | verse output + packet + lexicon → producer-v2 shard the existing builder accepts |
| `convert_ch12.py` | test | the reviewed chapter-12 producer shards → verse outputs + a lexicon, for the round trip |
| `run_pipeline.py --stage E` | E | final expansion with the reviews' readers_will_meet, independent-review files from gita-review-v1, the builder (check, then build), the whole-Gītā index |
| `build_whole_gita.py` | E | the single `gita/bhagavad-gita/` article: chapter index + lazy loader; `--register --root WORKTREE` adds the app/manifest entry there |
| `run_pipeline.py` | all | the driver |

## Data flow and paths (all under `internal/gita_pipeline/`)

```
BORI (lookup.bori_lines) ──────────────────────┐
oracle grammar.split / analyze / derive ───────┼─▶ packets/verses/C.V.json        (no secondaries)
lookup.gloss_lookup (Sanskrit commentators) ───┘        │
oracle analyses + derivations ──────────────────────────┼─▶ packets/analyses.sqlite (by id)
                                                         ├─▶ packets/inventory.json   lemma → occurrences, freq, row, priority
oracle meaning.page (once per lemma) ───────────────────┼─▶ packets/meaning/<key>.json
                                                         ├─▶ packets/concordance.json, packets/shard_plan.json, packets/manifest.json
build_jobs ─▶ jobs/<type>/<id>.input.json + queue/pending/<id>.json
   lexicon       → out/lexicon/<id>.json          (gita-lexicon-v1)
   lexicon-review→ out/lexicon-review/<id>.json   (gita-lexicon-review-v1)
   merge (stage B, D) → lexicon/term_policy.v3.json + lexicon/merge_report.json; --install writes data/glossary/term_policy.json
   verse         → out/verse/<id>.json            (gita-verse-v1)
   expand (C)    → internal/sanskrit_reviews/gita/chN/producer-AA-BB.json + expand-AA-BB.report.json
   review        → private/out/review/<id>.json   (gita-review-v1; quotes secondaries)
   stage E       → internal/sanskrit_reviews/gita/chN/independent-review-AA-BB.json → builder → gita/chN/
secondaries/CH.json (stage A; review jobs only). The whole of internal/gita_pipeline/ is git-ignored.
```


## Contracts implemented (from SCHEMAS.md and the briefs), with the gaps filled

- **Analysis ids** are the oracle's. A word's `analysis` id must be one of the packet's
  analyses of that pada form (or of the member form for compound members); a manual
  analysis must carry every Analysis field with `source: "manual"`.
- **Sense ids** are `<row>.<sense>`; the row key is the prefix. Valid ids: the current
  table's rows (`lemma.sense`), accepted lexicon outputs, and the output's own
  `lexicon_requests` (VERSE_BRIEF).
- **Forms keys** of a lexicon sense map to the builder's grammatical categories:
  `verb`, `verb+X`, `finite` → `finite`; `noun`, `plural`, `predicate`, `adjective`,
  `adverb` → `noun`; `participle_past`, `participle_present`, `absolutive`, `infinitive`,
  `agent` as named. Finite forms are given their regular English inflections (-s, -ed,
  -ing) so that the builder's form check (B8) admits an inflected slot.
- **Optional display overrides** in a verse word (`gloss`, `parts`, `root_gloss`, `morph`,
  `affix`, `sandhi`, `word_class`, `form_note`, `meaning_why`, `claims`): used verbatim when
  present, else generated. They exist so that reviewed cards (chapter 12) round-trip; a
  producer normally omits them.
- **Card generation**: `deva` by transliteration of the pada; `stem`, `root` "√r (gaṇa,
  NP)", `root_id`, `rootGloss` (Dhātupāṭha `artha_english`), `affix` (Pāṇinian names: kṛt or
  taddhita + sup/tiṅ), `morph` (plain English), `parts` (upasargas, root, affixes), `term` and
  `glossaryKey` from the row, `meaning` (lexicon image and lines + this verse's commentator
  lines, in category order, at most 8), `wording` (lexicon plain/rich/chosen/why),
  `evidence` (Dhātupāṭha record + each derivation step's sūtra line + sūtras the producer
  named), `fallback` for what stays underived, `derivation` (shard only), verse `grammar`
  from the kārakas and the finite/non-finite forms.
- **Review conversion**: a `gita-review-v1` whose `shard_sha256` equals the verse output's
  sha256 and whose verdict is accept becomes the builder's `independent-review-AA-BB.json`
  with `producer_sha256` = the expanded shard's hash; the build refuses when a row the shard
  uses changed after the review (sweep + rereview).

## Tests (`scripts/gita/tests/`, `python3 -m unittest discover -s scripts/gita/tests`)

1. Oracle seam: absent module → clear error; fixture oracle → normalised Analysis /
   Derivation / split.
2. Stage A on a fixture chapter (two verses, fixture oracle, real BORI and gloss): packet
   shape, no secondaries anywhere, recomposition of split candidates, inventory counts.
3. Job creation: batching, priorities, dependencies, input files, validator commands.
4. Validators: each job type accepts a good output and rejects one plausible defect per
   check (unknown analysis id, unknown sense, padas that drop a syllable, unresolved slot,
   secondary quoted, pipeline vocabulary, S1 with accept, wrong sha).
5. Merge: legacy rows kept, new rows `lexicon-reviewed`, English collision reported,
   unaccepted outputs ignored.
6. Chapter-12 round trip: convert the reviewed shards to verse outputs, expand, run the
   builder: the same lines, card-by-card equality on the identity fields, and no builder
   error class the original shards do not also have.
7. Whole-Gītā article: chapter index from built chapters; registration idempotent in a
   temporary root; the loader parses (node).

## Measured (2026-11-08)

- Stage A, all 700 verses, 8 workers: 3 min 45 s wall (verse packets 82 s, meaning pages 141 s);
  `internal/gita_pipeline/packets/manifest.json` has the timings and counts.
- Jobs under the lead's scope: 704 lexicon lemmas (457 of weight ≥ 3, 247 row/system terms) → 65 lexicon
  + 65 lexicon-review jobs at 12 lemmas a job (90 at 8); 153 shards = 149 verse jobs without chapter 12.
  Acceptance run of chapter 12: 12 lexicon jobs (130 lemmas), 4 verse jobs, 4 reviews.
- Chapter-12 round trip (`convert_ch12.py`): 20/20 lines identical; builder errors identical to the original
  shards' (2 × B10, reader side); 232/244 cards on oracle analysis ids; the same 8 blocking fallbacks
  (7 enclitic me/te derivations the oracle does not reproduce + 1 manual) plus one non-blocking flag per
  compound (samāsa is the analyst's claim).
- The acceptance flow A→E, run end to end in a scratch pipeline with simulated workers (oracle with enclitic
  me/te and nañ readings): 20/20 lines, 20/20 splits; builder in complete mode B8 14, B10 2, B18 1 (the one manual
  analysis). The 14 B8 come from the simulation's synthetic lexicon requests (forms copied from card glosses; match
  patterns that do not detect compound members), not from the pipeline (logs/simulated_acceptance_report.json).
- Tests: `python3 -m unittest discover -s scripts/gita/tests` (18) and `scripts/test_build_gita_chapter_reader.py` (72).
