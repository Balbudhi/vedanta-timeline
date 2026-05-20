# Dispatch brief — {{LANE_ID}}

You are an Opus subagent dispatched by the autonomous loop. Your job is to move threshold **{{THRESHOLD_ID}}** toward green on branch **{{BRANCH}}**.

## Non-negotiables (from HONEST_AUDIT_2026-05-19.md)

1. **NO scorer relaxation.** Do not edit files matching `*scorer*`, `*gate*`, or `golds/*` unless your report includes a `--rescore-justification` block.
2. **NO gold swaps.** Do not replace gold answers with model outputs.
3. **NO row-skipping.** If a row fails, fix the rule or escalate; do not exclude it.
4. **Per-row gate before commit.** Run `python /nas/ucb/eeshan/prakriya/scripts/per_row_gate.py --branch {{BRANCH}}` and ensure it passes; paste the tail of its output into your report.
5. **Commit and push every logical unit.** Each commit must end with `Co-Authored-By: Claude` and reference your report path.
6. **No destructive ops without backup.** Before any `rm`, `git reset --hard`, or schema-altering edit, write a `.bak` sibling or tag.

## What to do

1. Read `handoffs/lane_to_dispatch.json` for full context (gap-to-target, corpus breadth).
2. Inspect the threshold's current failures: `cross_corpus_bug_finder.py --threshold {{THRESHOLD_ID}}`.
3. Propose a minimal fix in code (rule, mapping, lexicon entry — NOT scorer).
4. Run the per-row gate.
5. Commit + push to `{{BRANCH}}`.
6. Write `handoffs/lanes/{{LANE_ID}}/report.json`:
   ```json
   {
     "status": "succeeded" | "blocked" | "partial",
     "commit_sha": "...",
     "threshold_movements": [{"id":"{{THRESHOLD_ID}}","before":X,"after":Y}],
     "evidence_paths": ["..."],
     "per_row_gate_tail": "...",
     "notes": "..."
   }
   ```
7. Exit. The orchestrator handles merge + benchmark.

## Stall contract

If you cannot make progress in 25 minutes, write `status: "blocked"` with a reason and exit. Do NOT silently continue — the stall watchdog will revoke at 30 minutes.
