# Gītā pipeline runbook: from packets to a published reader

The exact commands, in order, for one orchestrator (the "lead": a human, Claude Code,
Codex) and its workers. Governing decision: prakriya
`docs/TRANSLATION_PIPELINE_SPEC.md` §0.6 (code generates every analysis, derivation and
piece of evidence; agents only judge). Rules: `docs/SANSKRIT_TRANSLATION_STANDARD.md`.
Stages: `docs/GITA_FULL_TRANSLATION_PLAN.md` §7. Job I/O: `SCHEMAS.md`. The machinery
and its data paths: `scripts/gita/README.md`. Run every command from
`/Users/eeshan/Dev/vedanta-timeline` unless a path says otherwise.

## Roles

- **Lead**: runs every script below, spawns and replaces workers, reads the status,
  stops and reports. Never edits a worker's output.
- **Worker**: loops the queue for its pool's job types, follows the job's `brief`, writes
  only the job's `output`, runs the job's `validate`, submits. Never runs stage scripts,
  never commits, never pushes.
- **Human (or the lead, if authorised)**: pushes each deploy commit.

The main checkout holds the owner's and other agents' uncommitted edits. Nothing is
built for publication, committed or pushed in it: publication happens only through
`scripts/deploy_gita_chapter.sh`, in a clean worktree of `origin/main`.

## Commands

Mechanical work is never a queue job; the driver does it. Every stage is idempotent.

| Command | Does |
| --- | --- |
| `python3 scripts/gita/run_pipeline.py --stage A` then `python3 scripts/gita/build_commentary_packets.py` | verse packets (700), lemma inventory, meaning pages, shard plan, private translations files; lexicon and lexicon-review jobs |
| `… --stage B` | `lexicon-fix` / `lexicon-rereview` for `revise` verdicts; when every batch is accepted: merge (table v3, installed, hash frozen) and the verse jobs |
| `… --stage C [--chapter N]` | expands each submitted verse output (cards, citations, derivations, builder report); queues its review, or its rereview after a fix |
| `… --stage D [--chapter N]` | `fix` jobs for `revise` verdicts (`agent_ref` = the producer); merges accepted lexicon requests; re-expands shards whose rows changed and queues their rereview |
| `… --stage E --chapter N` | for a chapter whose shards are all accepted: final expansion with the reviews' `readers_will_meet`, review files, builder **`--check-only`** |
| `… --status` | jobs by type and state, stage progress |
| `python3 scripts/gita/queue.py status \| show ID \| release ID \| retry ID` | the queue |
| `python3 scripts/gita/show_analysis.py FORM` | every reading of a form (for a lead's diagnosis) |

Chapter 12 (already published from its pilot shards) gets verse jobs only with
`--include-ch12` on stage B. Job types and briefs: `lexicon`, `lexicon-fix` →
`LEXICON_BRIEF.md` Part A; `lexicon-review`, `lexicon-rereview` → Part B; `verse`, `fix`
→ `VERSE_BRIEF.md`; `review`, `rereview` → `REVIEW_BRIEF.md`.

## 1. Setup checks (all must pass; otherwise stop and report)

```sh
cd /Users/eeshan/Dev/vedanta-timeline
git status --short > "${TMPDIR:-/tmp}/gita-scope-before.txt"   # others' edits: leave them alone
python3 -m pytest /Users/eeshan/Dev/prakriya/tests/lookup /Users/eeshan/Dev/prakriya/tests/gita_kit
python3 /Users/eeshan/Dev/prakriya/scripts/lookup/lookup.py selftest kashika
python3 -m unittest discover -s scripts/gita/tests
command -v node && sh scripts/run_checks.sh               # read-only checks; the tree is green
python3 scripts/gita/run_pipeline.py --status
```

## 2. Stage A (code; measured 3 min 33 s with 8 workers)

```sh
python3 scripts/gita/run_pipeline.py --stage A
python3 scripts/gita/run_pipeline.py --status
```

Measured 2026-11-08: 700 verses, 127,779 analyses, 1,092 lemmas → 139 lexicon jobs,
153 shards (149 without chapter 12). Under the lead's later scope (≥ 3 occurrences,
table rows, system terms, requests) the lexicon is ≈300 lemmas (≈38 jobs); the rest are
decided inline in verse jobs (VERSE_BRIEF step 5a). Record the re-measured count. Private-store check (standard §9): review
outputs and translations files quote published translations and must be git-ignored
(`internal/gita_pipeline/` is). Stop if this prints a path:

```sh
python3 -c "import json,glob;[print(p) for f in glob.glob('internal/gita_pipeline/queue/*/*.json') for j in [json.load(open(f))] for p in ([j['output']] if j['type'] in ('review','rereview') else [])+[i for i in j['inputs'] if 'secondar' in i]]" \
  | git check-ignore --stdin --no-index -nv | grep '^::'
```

## 3. The worker loop (every worker, every stage)

Each worker has a unique name used in one pool only (`auth-1`…, `rev-1`…); a name is
never reused in the other pool, so nobody reviews their own work.

```
repeat:
  for T in <pool types, in priority order>:
      JOB = python3 scripts/gita/queue.py next --type T --worker NAME
      if JOB != NONE: break
  if every type said NONE:
      if the status shows jobs of these types pending or running: wait 3–5 min, repeat
      else: exit and tell the lead
  follow JOB.brief with JOB.inputs → write JOB.output (only that path)
  run JOB.validate; repair the output until it passes (at most 3 runs)
  python3 scripts/gita/queue.py submit JOB.id
```

Pools: **authors** take `lexicon-fix, fix, lexicon, verse` (fixes first); **reviewers**
take `lexicon-rereview, rereview, lexicon-review, review`. A worker that has done four
jobs exits and the lead starts a fresh one under a new name in the same pool. Fix jobs
carry `agent_ref` (the producer's worker name); where the runtime can resume that
worker, the lead may route the fix to it; the briefs work either way.

## 4. Workers per job type (N = concurrency the runtime allows; plan default 16)

| Phase | Authors | Reviewers | Basis |
| --- | --- | --- | --- |
| Stage B (lexicon) | ¾ N (12) | ¼ N (4) | ≈6 agent-min per lemma to author (≈48 per 8-lemma job); review assumed ≈⅓ of that |
| Stages C–D (verses) | ½ N (8) | ½ N (8) | pilot targets per 5-verse shard: produce ≈25 + fix ≈8 min; review ≈25 + re-review ≈5 min |

Rebalance at the B→C boundary: when stage B has merged, end the stage-B workers and
start the C–D pools with new names.

## 5. Stage order and the lead's loop

1. **B, lexicon.** Start the stage-B pools. Every 5 min (or after a few submits):
   `run_pipeline.py --stage B`, then `--status`. Stage B ends when the merge has run:
   `data/glossary/term_policy.json` is v3 and verse jobs are pending. If the merge
   prints `STOP: the merge refused`, each CONFLICT line names two batches; queue a
   `lexicon-fix` of the later batch with the collision as its finding if you can
   (`queue.py add`), else stop and report.
2. **C–D, verses.** Start the C–D pools. Every 5 min: `--stage C`, `--stage D`,
   `--status`. A shard is accepted when its latest review or re-review says `accept`.
3. **E, check per chapter**, as soon as all of a chapter's shards are accepted:

```sh
python3 scripts/gita/run_pipeline.py --stage E --chapter N   # builder --check-only: no ERROR
sh scripts/run_checks.sh                                       # 0 failures
```

Chapters do not wait for each other after stage B.

## 6. Failed validator

- Before submit: the worker repairs its output against the message (up to 3 runs).
- After submit (`FAILED`, job in `failed/`): the lead reads `queue.py show ID`; if the
  message is something the brief covers, `queue.py retry ID` (the output file stays;
  the next claimer repairs it). A job that fails a second time, or a validator that
  rejects a field the brief requires, is a stop-and-report.
- A builder ERROR in stage E: map it to the shard and word; queue a `fix` for that
  shard if you can (`queue.py add`), else stop and report. Never hand-edit a shard,
  packet, expanded card, the table or `gita/chN/`.

## 7. Deploy and publication (one chapter at a time; the script commits, never pushes)

```sh
H=$(python3 scripts/build_gita_chapter_reader.py --policy-hash | cut -c1-12)
sh scripts/deploy_gita_chapter.sh N "Gītā N: reader from reviewed shards (policy $H)"
```

The script fetches `origin/main` into a fresh worktree, runs the real build there,
copies only the chapter's files and the table, registers the reader as `provisional`,
registers the whole-Gītā article `gita/bhagavad-gita/` (chapter chooser, chapters
loaded lazily; registered once, idempotent), runs the checks in the worktree and
commits. It prints the push command; **the human or the authorised lead runs it**, then
the printed `worktree remove`. Push chapter N before deploying the next (each deploy
starts from the current `origin/main`). After the push, verify:

```sh
curl -sI https://vedanta.eeshan.xyz/gita/chN/verses.js | head -1              # 200
curl -sI https://vedanta.eeshan.xyz/gita/bhagavad-gita/ | head -1              # 200
```

## 8. Resume after interruption

The queue is on disk (`internal/gita_pipeline/queue/{pending,running,done,failed}`).

```sh
python3 scripts/gita/run_pipeline.py --status
ls internal/gita_pipeline/queue/running/          # each: python3 scripts/gita/queue.py release ID
ls internal/gita_pipeline/queue/failed/           # each: queue.py show ID, then retry or report
git worktree list                                 # a deploy worktree left behind: push or remove (lead)
```

Then re-run the current stage command and start fresh workers with new names. A
released job's partial output is kept; its next worker continues it.

## 9. Cost and time (projected from the chapter-12 pilot; plan §10, audit §4.8)

- Measured in the pilot: 21.3 agent-min per verse; 115 min wall for 20 verses at 4
  concurrent shards; 28.7 findings and 3.3 S1 per 100 cards.
- Lexicon: ≈300 lemmas × ≈6 agent-min ≈ 30 agent-h, plus review (assumed ≈⅓,
  ≈10 agent-h); ≈2.5 h wall at 16 workers (12 authors, 4 reviewers). The pilot rate
  predates the meaning pages; treat it as an upper bound and re-estimate after the
  first 10 batches.
- Inline decisions: ≈790 lemmas (1,092 − 300), one or two occurrences each, assumed
  ≈3 agent-min each in the verse job (≈40 agent-h) plus ≈⅓ of that in review
  (≈13 agent-h).
- Verses: 680 × ≈12.6 agent-min ≈ 143 agent-h including review and fixes, plus the
  inline decisions above, plus a 5% post-scale audit ≈7 agent-h: ≈203 agent-h; ≈13 h
  wall at 16 workers.
- Total ≈ 245 agent-h (≈300 with the whole inventory in the lexicon), ≈ 15–16 h wall
  at 16 workers, before owner time. Re-estimate from the first chapter's measured
  times.
- Money: no paid API call; every lookup is local. Spend is the agent runtime's own
  usage; the lead reports it if the runtime shows it.
- Quality halt per chapter: > 10 findings or > 1 S1 per 100 cards in first-round
  reviews → stop that chapter and report (plan §10). Count:

```sh
python3 -c "import json,glob,collections as C;t=C.Counter()
for f in glob.glob('internal/gita_pipeline/queue/done/review-*.json'):
  j=json.load(open(f));r=json.load(open(j['output']))
  for x in r['findings']: t[(j['id'].split('-')[1],'S%s'%x['severity'])]+=1
print(sorted(t.items()))"
```

## 10. Stop and report

Any setup check failing; a private path not ignored; a job failing twice; a validator
rejecting a field a brief requires; a merge conflict you cannot route; a builder ERROR
that cannot be mapped to a shard; a chapter over the quality halt; any need to write
outside a job's output path or the driver's own outputs, or to build or commit in the
main checkout. Report: the stage, `--status`, the job id, the exact message, what was
tried.

## 11. Finish

When every chapter has passed stage E and been deployed: `sh scripts/run_checks.sh`
(0 failures), the tests of §1 again, `--status` (nothing pending, running or failed),
and a summary: chapters committed or published (provisional) with commit and policy
hash, the whole-Gītā article's state, lexicon size, jobs by type, findings per 100 cards
per chapter, open forks, lexicon requests merged, wall and agent time, and anything left
for the owner's taste review.
