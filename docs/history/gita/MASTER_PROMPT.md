# Master prompt: paste this to translate, review and build the whole Gītā

> **Retired (2026-11-09).** This runs the stages A–E job queue, which is no longer used. Do not follow it; see [README.md](README.md) for the current documents.

Paste everything between the lines into an agent that has shell access (OpenAI Codex,
ChatGPT with a code environment, Claude Code). Set N (parallel workers) and PUSH
(yes lets the lead publish each passing chapter provisionally, plan L15; no leaves
every push to you).

---

You are the lead of the Bhagavad-Gītā translation pipeline in the repository
`/Users/eeshan/Dev/vedanta-timeline`. Your goal: all 700 verses translated word by word,
reviewed, built into the readers `gita/chN/` and the whole-Gītā article
`gita/bhagavad-gita/`, checked, and committed for publication.
N = 16 parallel workers (fewer if your runtime allows fewer). PUSH = no.

The translation's English comes from the Sanskrit tradition and the dictionaries:
richer, freer and more exact than published translations; rare, archaic or fused
words only when they carry the meaning more exactly. Code has generated every
analysis, derivation and piece of evidence; agents only judge. The review must be
trustworthy: independent, recomputed, never "a translation says so".

1. Read `docs/gita_briefs/RUNBOOK.md` in full. It gives every command and governs
   where this prompt is brief. Read `AGENTS.md` (shared working tree: stage by path,
   never touch other agents' edits).
2. Run the setup checks of RUNBOOK §1. If any fails, stop and report.
3. Run stage A (`python3 scripts/gita/run_pipeline.py --stage A`) and the
   private-store check of RUNBOOK §2. If it prints a path, stop and report.
4. Spawn the worker pools of RUNBOOK §3–§4 as parallel sub-agents or tasks. Give each
   worker this instruction, with its NAME and POOL filled in:

   > You are worker NAME in the POOL pool of the Gītā pipeline, repository
   > `/Users/eeshan/Dev/vedanta-timeline`. Loop as in `docs/gita_briefs/RUNBOOK.md`
   > §3: claim with `python3 scripts/gita/queue.py next --type T --worker NAME` for the
   > types of your pool (authors: lexicon-fix, fix, lexicon, verse; reviewers:
   > lexicon-rereview, rereview, lexicon-review, review); for each job read and follow
   > the brief named in the job record exactly; write only the job's `output` path;
   > run the job's `validate` command until it passes; then
   > `python3 scripts/gita/queue.py submit ID`. Never edit any other file, never run
   > stage scripts, never commit or push. Never read or search for any published
   > translation of the Gītā unless you are doing a review or rereview job, and then
   > only the secondaries file in its inputs, only after the brief's checks 1–7.
   > After four jobs, or when no job of your types is pending or running, stop and
   > report the job ids you finished and any problem.

5. Drive the stages as RUNBOOK §5 says: stage B until the lexicon is merged and
   frozen; then replace the pools for stages C–D; re-run `run_pipeline.py --stage B`,
   `--stage C`, `--stage D` every few minutes; replace each worker that stops with a
   new one under a new name in the same pool. Never edit a worker's output yourself.
6. As each chapter's shards are all accepted, check it with stage E (RUNBOOK §5 step
   3), then deploy it with `scripts/deploy_gita_chapter.sh` (RUNBOOK §7), which builds
   in a clean worktree; never build for publication or commit in the main checkout.
   The script commits but does not push. With PUSH = yes, run the printed push
   command, verify the live files (RUNBOOK §7), then deploy the next chapter. With
   PUSH = no, give the owner the printed push command and deploy the next chapter only
   after `git fetch origin main` shows that commit on origin/main (each deploy builds
   on origin/main).
7. Stop and report (RUNBOOK §10) on any setup or validator failure you cannot fix
   within the brief, a job failing twice, a private path not ignored, a chapter over
   the quality halt, or any need to write outside a job's output path.
8. Finish (RUNBOOK §11): every chapter checked and deployed,
   `sh scripts/run_checks.sh` with 0 failures, the golden tests passing, `run_pipeline.py --status`
   clean, and a summary: chapters committed or published with commit and policy hash,
   lexicon size, jobs by type, findings per 100 cards per chapter, open forks, agent
   and wall time, and what remains for the owner's taste review.

If your runtime cannot run sub-agents or parallel tasks, be a single worker yourself:
after step 3, loop RUNBOOK §3 with NAME `solo` over all eight job types in the order
lexicon-fix, lexicon-rereview, lexicon, lexicon-review, fix, rereview, verse, review,
running the stage commands of step 5 between jobs; review jobs then lack an
independent reviewer, so say so in the summary.

---
