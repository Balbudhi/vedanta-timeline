# Gītā translation: superseded documents

These are dated records of earlier designs, audits and research for the Gītā translation. They are not current guidance; follow the documents in the last column.

Current documents:

- [`docs/GITA_FULL_TRANSLATION_PLAN.md`](../../GITA_FULL_TRANSLATION_PLAN.md): the project (goal, method, current state, gaps, roadmap).
- [`docs/SANSKRIT_TRANSLATION_STANDARD.md`](../../SANSKRIT_TRANSLATION_STANDARD.md): the translation rules.
- [`docs/gita_briefs/ENGLISH_CRAFT.md`](../../gita_briefs/ENGLISH_CRAFT.md): the procedure for choosing English.
- [`scripts/gita/translate/README.md`](../../../scripts/gita/translate/README.md): the translation code and how to run it.

| File | What it was | Date | Why superseded | Replaced by |
|---|---|---|---|---|
| [GITA_CH12_PIPELINE_AUDIT.md](GITA_CH12_PIPELINE_AUDIT.md) | Audit of the chapter-12 pilot run (time, cost, quality) with proposed amendments | 2026-11-08 | Amendments were applied to the plan and standard or dropped; the job-queue process it audited is retired | Plan; standard |
| [TRANSLATION_PRECEDENTS_SURVEY.md](TRANSLATION_PRECEDENTS_SURVEY.md) | Survey of how this repository already translated and presented Sanskrit, checked against the chapter-12 reader | 2026-11-08 | Its proposed amendments were folded into the standard | Standard |
| [GITA_CARD_MEANING_SCHEMA.md](GITA_CARD_MEANING_SCHEMA.md) | Data contract for a word card's meaning and fork display | 2026-11-08 | Folded into the standard §2–§3 | Standard |
| [RUNBOOK.md](RUNBOOK.md) | Commands for the job-queue pipeline (stages A–E, worker pools, deployment) | 2026-11-08 | The job queue of tool-using agents was retired: a lexicon job took 40–90 tool calls and 10–13 minutes | `scripts/gita/translate/README.md` |
| [MASTER_PROMPT.md](MASTER_PROMPT.md) | Paste-in prompt for an agent to run the job-queue pipeline end to end | 2026-11-08 | Runs the retired job queue | Plan; `scripts/gita/translate/README.md` |
| [SCHEMAS.md](SCHEMAS.md) | Grammar and meaning tool interface, and the job input/output schemas of the job queue | 2026-11-08 | Job schemas retired with the queue; the tool list named a `verse packet` command that does not exist | `scripts/gita/translate/README.md`; prakriya `docs/GITA_KIT.md` for the tool interface |
| [BHAKTI_POSTMORTEM.md](BHAKTI_POSTMORTEM.md) | Lessons from an earlier song-translation pipeline, applied to the Gītā design | 2026-11-08 | Its recommendations assume the lexicon-first design, since retired | Plan |
| [LITERARY_PRINCIPLES.md](LITERARY_PRINCIPLES.md) | Research notes on translation theory and English word formation | 2026-11-08 | Treats losslessness as shared between the line and notes; the standard now requires the meaning to be carried in the line, with no notes layer. Quotations marked [P] were never checked | ENGLISH_CRAFT; standard |
| [WORKFLOW_lexicon_first.md](WORKFLOW_lexicon_first.md) | Second pipeline design: code chose each word's English out of context by scoring model-supplied marks; the line was assembled afterwards | 2026-11-09 | Retired the same day after chapter-12 runs: odd word choices, stilted lines, run-to-run variance | Plan; `scripts/gita/translate/README.md` |
| [WORKFLOW_2026-11-09.md](WORKFLOW_2026-11-09.md) | Third pipeline design (`pipeline.py`: a meaning call and an English call per sentence, code checks, review, consistency pass), with an audit of the second design | 2026-11-09 | The design is current; this document is replaced by the plan (design, gaps) and the code README (operation). Some claims in it overstate what the code sends to the model | Plan; `scripts/gita/translate/README.md` |

Links inside these records point to paths as they were when written; several targets have since moved into this folder or been retired. Paths under `internal/` name local, git-ignored working files that are not published. Owner statements in these records are paraphrased.

Two records still serve current code as reference: `scripts/build_gita_chapter_reader.py` cites [GITA_CH12_PIPELINE_AUDIT.md](GITA_CH12_PIPELINE_AUDIT.md) §5.7 (builder checks B1–B18) and [GITA_CARD_MEANING_SCHEMA.md](GITA_CARD_MEANING_SCHEMA.md) as its contract, and `scripts/deploy_gita_chapter.sh` cites the audit's §5.8. Until those docstrings are updated, read the builder's checks there; the governing rules are in the standard.

## Retired, kept at their original paths

`docs/gita_briefs/LEXICON_BRIEF.md`, `VERSE_BRIEF.md` and `REVIEW_BRIEF.md` were the agent briefs for the job queue's lexicon, verse and review jobs (2026-11-08). They are superseded like the files above, but stay where they are because the retired queue code (`scripts/gita/gitapipe/common.py`, `scripts/gita/queue.py`) still writes those paths into job records. `PRODUCER_BRIEF.md`, a one-line redirect to `VERSE_BRIEF.md`, was deleted.
