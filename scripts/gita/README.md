# scripts/gita — Gītā translation scripts

The goal, method and status of the Bhagavad-Gītā translation are in
[docs/GITA_FULL_TRANSLATION_PLAN.md](../../docs/GITA_FULL_TRANSLATION_PLAN.md). The translation
code (parse, translate, consistency, English workbench, tests) is in [translate/](translate/README.md).
This folder also holds the packet builders the translation reads, the whole-Gītā article builder,
and the retired job-queue design. All outputs go under `internal/gita_pipeline/` (local, private).

## Current

| File | Role |
|---|---|
| `build_all_packets.py` with `gitapipe/stage_a.py`, `oracle.py`, `store.py`, `common.py`, `kit_worker.py` | Builds, for all 700 verses: verse packets with the Vidyut analyses (`packets/verses/C.V.json`), every analysis and derivation by id (`packets/analyses.sqlite`), the lemma inventory, the concordance, the kit's meaning pages (`packets/meaning/`), and private files of published translations (`secondaries/`, never used in production). The grammar oracle runs Vidyut in `prakriya/tmp/vidyut-venv` through `kit_worker.py` |
| `build_commentary_packets.py` | Every commentary passage per verse, with the neighbouring verses (`packets/commentary/C.V.json`); the parse stage reads it |
| `show_analysis.py` | Prints the analyses of a form, or one analysis and its derivation by id |
| `build_whole_gita.py`, `article/` | Builds the single article `gita/bhagavad-gita/` (index, reader, chapter list) from built chapters; reached through `scripts/deploy_gita_chapter.sh --whole-gita`. Not yet used: the article does not exist |

```sh
python3 scripts/gita/build_all_packets.py [--chapters 2,12 | 1-18] [--workers 8] [--skip-meaning]
python3 scripts/gita/build_commentary_packets.py [--chapter N]
python3 scripts/gita/show_analysis.py FORM | --id ANALYSIS_ID
python3 scripts/gita/build_whole_gita.py [--root DIR] [--include-legacy] [--register]
```

The site side lives in `scripts/`: `build_gita_chapter_packet.py` and
`build_gita_chapter_reader.py` (the fail-closed chapter builder, with
`test_build_gita_chapter_reader.py`), `deploy_gita_chapter.sh` (builds and commits in a clean
worktree of `origin/main`; never pushes), `audio/` (recitation alignment and encoding), and the
validators run by `scripts/run_checks.sh`: `validate_gita_slots.js`, `check_gita_terms.js` and
`check_gita_witness.py`.

## Retired: the stages A–E job queue

An earlier design ran the translation as a disk job queue worked by agents: Gītā-wide lexicon
jobs, then verse, review and fix jobs, merged into the term policy and expanded into the chapter
builder's input. It was replaced (see the plan and [translate/README.md](translate/README.md),
Design history); its documents are in [docs/history/gita/](../../docs/history/gita/). Its packet
stage is still the input described above. The following files belong to it and are not used by
the current translation:

- `run_pipeline.py` (stages A–E and the chapter-12 acceptance run), `queue.py`, `build_jobs.py`,
  `validate_job.py`;
- `gitapipe/validate.py`, `lexicon.py`, `expand.py`, `names.py`;
- `merge_lexicon.py`, `expand_cards.py`, `convert_ch12.py`;
- `tests/test_pipeline.py` (`python3 -m unittest discover -s scripts/gita/tests`).

`gitapipe/expand.py` is the only converter from translation output to the chapter builder's
input, and it reads the retired verse-job format; the current pipeline has no such converter yet.
