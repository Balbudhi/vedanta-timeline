# Autonomous Loop Plan — 2026-05-20

**Goal.** Keep the prakriya master-plan acceptance work progressing without a human dispatching every lane. Three tmux/cron sessions already write status markers; we add the missing pieces so the orchestrator (the active Claude Code session) only needs to *consume* state, choose, and dispatch.

---

## 0. Honest constraint summary

| Capability | Available? | Notes |
|---|---|---|
| tmux/cron tick running bash scripts | YES | 3 already live: `phases-watchdog`, `benchmark-loop`, `disk-monitor`. |
| Cron tick spawning an Opus subagent with the Agent tool | NO | The Agent tool only exists inside an active Claude Code session. Cron processes can run `claude -p` for non-interactive shots, but those sessions cannot themselves spawn nested Agents reliably; treat them as "single-shot worker", not "orchestrator". |
| `claude --help` scheduling primitive | PARTIAL | `claude agents` manages background-session lifecycle; `claude -p` runs one-shot prints. No native cron-style "run agent every N minutes" — we keep using tmux. |
| `RemoteTrigger` API | NOT FOUND in `claude --help`. The closest primitive is `claude agents --json` for listing live sessions and `claude -p` for one-shots. We design the loop around tmux-driven *nudges* + an orchestrator that reads them. If `RemoteTrigger` materialises later, the state machine is unchanged — only the dispatch path swaps from "human-in-loop reads nudge" to "trigger reads nudge". |

**Therefore**: the loop is a *cron-writes-state, orchestrator-reads-state, orchestrator-dispatches* pattern. The orchestrator is still a human-facing session, but its decisions are *fully scripted* — it reads `handoffs/loop_state.json` and follows `scripts/loop/orchestrator_brief.md`, so each turn takes seconds.

---

## 1. State machine

```
                    +-------------------+
                    |   awaiting_       |
                    |   benchmark       |<------------+
                    +---------+---------+             |
                              | benchmark-loop tick   |
                              | writes scoreboard     |
                              v                       |
                    +-------------------+             |
              +-----| evaluating_       |             |
              |     | scoreboard        |             |
              |     +---------+---------+             |
              | all-green     | failing thresholds    |
              | OR no bugs    | OR bug clusters       |
              v               v                       |
       +-----------+  +-------------------+           |
       | all_green |  | choosing_lane     |           |
       +-----+-----+  +---------+---------+           |
             |                  |                     |
             v                  v                     |
       +-----------+  +-------------------+           |
       |   done    |  | dispatching_lane  |           |
       +-----------+  +---------+---------+           |
                                |                     |
                                v                     |
                      +-------------------+           |
                      | awaiting_lane_    |           |
                      | completion        |           |
                      +---------+---------+           |
                          |          |                |
                stalled?  |          | lane committed |
                          v          v                |
                  +-----------+  +----------+         |
                  | escalate  |  | merging  |         |
                  +-----+-----+  +-----+----+         |
                        |              |              |
                        +------+-------+              |
                               |                      |
                               +----------------------+
                                  re-enter loop
```

**Persistence.** `handoffs/loop_state.json` (single source of truth, cron-readable, human-readable):

```json
{
  "state": "awaiting_lane_completion",
  "updated_at": "2026-05-20T08:00:00Z",
  "current_lane": {
    "id": "lane-bug-cluster-genitive-overgen-2026-05-20",
    "branch": "phase-acceptance/genitive-overgen",
    "threshold_id": "T-bug-001",
    "dispatched_at": "2026-05-20T07:30:00Z",
    "last_commit_at": "2026-05-20T07:42:00Z"
  },
  "open_lanes": [],
  "completed_lanes": ["lane-translator-real-..."],
  "benchmark": {
    "last_run_at": "2026-05-20T07:55:00Z",
    "all_green": false,
    "failing": ["T-translation-87", "T-vidyut-6.4.11"]
  },
  "guardrails": {
    "max_concurrent_per_threshold": 2,
    "plateau_streak_block": 3
  }
}
```

### Transitions

| From | Event | To | Writer |
|---|---|---|---|
| `awaiting_benchmark` | scoreboard json appears, mtime > last_seen | `evaluating_scoreboard` | cron (`benchmark-loop`) writes; orchestrator transitions |
| `evaluating_scoreboard` | `all_green=true` AND `bug_finder_open=0` | `all_green` | orchestrator |
| `evaluating_scoreboard` | failing thresholds OR bug clusters | `choosing_lane` | orchestrator |
| `choosing_lane` | `next_lane.py` returns a lane | `dispatching_lane` | orchestrator |
| `choosing_lane` | `next_lane.py` returns `BLOCKED` (plateau / cap hit) | `awaiting_benchmark` (with human-escalation marker) | orchestrator |
| `dispatching_lane` | Agent tool call issued | `awaiting_lane_completion` | orchestrator |
| `awaiting_lane_completion` | branch sees new commit + report marker | `merging` | orchestrator |
| `awaiting_lane_completion` | stall (>30 min no commits) | `escalate` -> back to `choosing_lane` after revoke | cron (`stall-watchdog`) writes `handoffs/stalled_lanes.json`; orchestrator acts |
| `merging` | merge + push complete | `awaiting_benchmark` | orchestrator |
| `all_green` | terminal write done | `done` | orchestrator (one-shot) |

---

## 2. Cron architecture (tmux sessions)

| Session | Tick | Script | Writes | Does NOT do |
|---|---|---|---|---|
| `phases-watchdog` (live) | 20 min | existing | `handoffs/watchdog_nudge.txt` | spawn agents |
| `benchmark-loop` (live) | 20 min | existing | `handoffs/all_phases_scoreboard.json`; exits on green | spawn agents |
| `disk-monitor` (live) | 5 min | existing | runs `free_disk.sh` if /home <100 MB | nothing else |
| **`stall-watchdog` (NEW)** | 10 min | `scripts/loop/stall_watchdog.sh` | `handoffs/stalled_lanes.json` | nothing else |
| **`lane-chooser` (NEW)** | 15 min | `scripts/loop/lane_chooser.sh` | `handoffs/lane_to_dispatch.json` | nothing else |
| **`loop-tick` (NEW)** | 5 min | `scripts/loop/loop_tick.sh` | merges inputs into `handoffs/loop_state.json` | NEVER edits code, NEVER commits |

All three new sessions are **observers** that compute state from filesystem facts. The orchestrator is the only mutator.

### Bringing them up

```bash
tmux new-session -d -s stall-watchdog 'while true; do bash /home/eeshan/vedanta-timeline/scripts/loop/stall_watchdog.sh; sleep 600; done'
tmux new-session -d -s lane-chooser   'while true; do bash /home/eeshan/vedanta-timeline/scripts/loop/lane_chooser.sh; sleep 900; done'
tmux new-session -d -s loop-tick      'while true; do bash /home/eeshan/vedanta-timeline/scripts/loop/loop_tick.sh; sleep 300; done'
```

---

## 3. Orchestrator contract

Every time the orchestrator returns to active turn, it runs this exact sequence (codified in `scripts/loop/orchestrator_brief.md`):

1. `cat handoffs/loop_state.json`
2. `cat handoffs/watchdog_nudge.txt` (if present)
3. `cat handoffs/stalled_lanes.json` (if non-empty -> handle first)
4. `df -h /home` -> if <100 MB, run `free_disk.sh` and abort dispatch
5. `cat handoffs/all_phases_scoreboard.json` -> if all-green AND `cross_corpus_bug_finder.py --summary` shows 0 -> jump to `all_green`
6. `python scripts/loop/next_lane.py` -> returns either `{"lane": {...}}` or `{"blocked": "<reason>"}`
7. If lane: dispatch via Agent tool with the strict no-gaming brief; immediately update `loop_state.json` `state=awaiting_lane_completion`
8. If blocked: write `handoffs/human_escalation.md` with the reason; do not dispatch

### The dispatch brief (template at `scripts/loop/dispatch_brief.tmpl.md`)

Every dispatched agent must:
- Run a per-row-gate equivalent BEFORE committing
- Commit and push to its `phase-acceptance/<lane-id>` branch
- Write `handoffs/lanes/<lane-id>/report.json` with `{status, commit_sha, threshold_movements, evidence_paths[]}`
- Refuse to relax scorers, swap golds, or skip rows; the brief contains the rules from `HONEST_AUDIT_2026-05-19.md`

---

## 4. Stall detection

`scripts/loop/stall_watchdog.sh` (every 10 min):
- For each branch matching `phase-acceptance/*` listed in `loop_state.json.open_lanes` + `current_lane`:
  - `git log -1 --format=%ct origin/<branch>` -> compare to `now()`
  - If `> 1800s` since last commit AND lane is `in_flight` -> append to `stalled_lanes.json`
- Output is JSON: `{"stalled": [{"lane_id": "...", "branch": "...", "last_commit_ts": ..., "age_seconds": ...}], "checked_at": "..."}`

The orchestrator on next turn revokes the stalled lane (writes `handoffs/lanes/<lane-id>/revoked.txt`), removes it from `open_lanes`, and re-queues via `next_lane.py`.

---

## 5. Lane prioritisation (`scripts/loop/next_lane.py`)

Deterministic priority function. Reads:
- `handoffs/all_phases_scoreboard.json` (failing thresholds with gap-to-target)
- `cross_corpus_bug_finder.py --summary --json` (cluster sizes by category)
- `handoffs/loop_state.json` (open lanes — for concurrency caps)
- `handoffs/threshold_history.jsonl` (last-N measurements — for plateau guardrail)

Priority score = `0.6 * normalized_gap_to_target + 0.3 * normalized_corpus_breadth + 0.1 * recency_penalty_inverse`.

Guardrails (return `BLOCKED` instead):
- If the last 3 measurements for a threshold are bit-identical -> plateau -> escalate to human
- If `open_lanes` already has 2 lanes against the chosen threshold -> skip and try next
- If chosen threshold's branch already has unmerged work -> skip

Output (stdout JSON, exit 0):
```json
{"lane": {"id": "...", "threshold_id": "...", "branch": "phase-acceptance/...", "brief_path": "scripts/loop/dispatch_brief.tmpl.md", "context": {...}}}
```
or `{"blocked": "plateau", "threshold_id": "..."}` with exit 2.

---

## 6. Termination

When `evaluating_scoreboard` sees `all_green=true` AND `bug_finder open == 0`:
1. Orchestrator writes `docs/ALL_PHASES_COMPLETE_<date>.md` summarising every accepted threshold, every merged lane, evidence pointers.
2. Orchestrator runs `scripts/loop/teardown.sh` which:
   - `tmux kill-session -t stall-watchdog`
   - `tmux kill-session -t lane-chooser`
   - `tmux kill-session -t loop-tick`
   - leaves `benchmark-loop` and `phases-watchdog` running for monitoring
3. Final commit + push on `main`.

---

## 7. RemoteTrigger investigation

`claude --help` output (this session): no `RemoteTrigger`, no native scheduler. Available primitives:
- `claude agents` — manages background-session lifecycle, lists with `--json`. Useful for the orchestrator to inspect live agents (`claude agents --json --cwd $PWD`).
- `claude -p "<prompt>"` — non-interactive print. A cron tick *could* in principle pipe a prompt to a fresh `claude -p` session; that session would have the tools its settings allow, including potentially Bash/Edit. But (a) it has no Agent tool (no nested dispatch), (b) it would burn tokens at every tick, and (c) it would race with the orchestrator. Therefore we **do not use `claude -p` from cron**; we keep cron as pure observer.

If a future `RemoteTrigger` lands, the only change is: a new tmux session `remote-dispatcher` reads `handoffs/lane_to_dispatch.json` and fires a remote agent run with the dispatch brief inlined. The state machine is unchanged.

---

## 8. Best-practices guardrails (baked into scripts)

| Guardrail | Where enforced |
|---|---|
| No dispatch if last 3 measurements identical (plateau) | `next_lane.py` |
| No more than 2 concurrent lanes per threshold | `next_lane.py` |
| No destructive ops without backup | dispatch brief + `loop_tick.sh` checks for `*.bak` siblings on touched files |
| Auto-revert on CI gate fail | `scripts/loop/post_merge_gate.sh` — runs compile + audit; on fail, `git revert <sha> --no-edit` on the integration branch and writes `handoffs/reverted/<sha>.md` |
| No silent commits | every commit must have `Co-Authored-By: Claude` AND a referenced `handoffs/lanes/<id>/report.json` |
| No scorer relaxation | dispatch brief forbids editing files matching `*scorer*`, `*gate*`, `golds/*` without an explicit `--rescore-justification` field in the report |

---

## 9. What the human-orchestrator does on next turn

1. Read `handoffs/loop_state.json`.
2. Run `python scripts/loop/next_lane.py` (or read `handoffs/lane_to_dispatch.json` already produced by cron).
3. If lane returned: dispatch the Agent tool with `scripts/loop/dispatch_brief.tmpl.md` filled in.
4. If blocked: open `handoffs/human_escalation.md` and triage.
5. Otherwise: idle until next benchmark tick.

The orchestrator's per-turn work shrinks to <60 seconds of decisions.

---

## 10. Roll-out order

1. Land this branch (`loop/autonomous-2026-05-20`) with scripts + doc.
2. **Manually run each script once** to verify outputs before starting tmux sessions.
3. Start `loop-tick` session first — it's read-only, lowest risk.
4. Start `stall-watchdog` after one clean tick.
5. Start `lane-chooser` last.
6. Watch one full cycle (benchmark -> choose -> dispatch -> merge -> benchmark) before walking away.
