# Orchestrator per-turn checklist

The orchestrator (the active Claude Code session that has the Agent tool) MUST follow this on every turn until `loop_state.json.state == "done"`.

## 1. Read state (60 seconds total)

```bash
cat handoffs/loop_state.json
cat handoffs/watchdog_nudge.txt 2>/dev/null || true
cat handoffs/stalled_lanes.json 2>/dev/null || true
df -h /home | tail -1
```

## 2. Handle blockers first

- If `/home` free < 100 MB: run `bash /nas/ucb/eeshan/free_disk.sh` and re-check. Do NOT dispatch on a full disk.
- If `stalled_lanes.json` has entries:
  - For each stalled lane, write `handoffs/lanes/<lane-id>/revoked.txt` with reason + timestamp.
  - Remove from `loop_state.json.open_lanes`.
  - Re-queue the threshold via `next_lane.py`.
- If `handoffs/human_escalation.md` exists: read it, triage, then `mv` it to `handoffs/escalations/<date>.md` after handling.

## 3. Check for completion

```bash
cat handoffs/all_phases_scoreboard.json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("all_green"))'
```

If `True` AND `cross_corpus_bug_finder --summary` reports 0 open clusters:
- Write `docs/ALL_PHASES_COMPLETE_$(date +%Y-%m-%d).md`.
- Run `bash scripts/loop/teardown.sh`.
- Set `loop_state.json.state = "done"`. STOP.

## 4. Choose next lane

```bash
python3 scripts/loop/next_lane.py
```

- Exit 0 with `{"lane": ...}` -> dispatch.
- Exit 2 with `{"blocked": ...}` -> write `handoffs/human_escalation.md`, do not dispatch.

## 5. Dispatch (the only action that requires the Agent tool)

Fill in `scripts/loop/dispatch_brief.tmpl.md` substitutions:
- `{{LANE_ID}}`, `{{THRESHOLD_ID}}`, `{{BRANCH}}`

Invoke the Agent tool with that brief. Immediately after the call returns (or once the agent has started its work):

```bash
python3 -c '
import json, sys, time
p = "handoffs/loop_state.json"
d = json.load(open(p))
d["state"] = "awaiting_lane_completion"
d["current_lane"] = {...}  # fill from chosen lane
d["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(d, open(p,"w"), indent=2)
'
```

## 6. After lane reports back

- Read `handoffs/lanes/<lane-id>/report.json`.
- Run `bash scripts/loop/post_merge_gate.sh <lane-id>` — compile + audit.
- On gate pass: merge to integration branch, push, set state -> `awaiting_benchmark`.
- On gate fail: `git revert <sha>` on the integration branch, write `handoffs/reverted/<sha>.md`, re-queue.

## 7. Idle

If state == `awaiting_benchmark` and no nudge: nothing to do this turn. The cron sessions will update state by the next turn.

---

## Best-practices checklist (paste into every dispatch decision)

- [ ] Read `loop_state.json`
- [ ] Disk free > 100 MB
- [ ] No unhandled stalls
- [ ] No unhandled `human_escalation.md`
- [ ] Benchmark snapshot age < 30 min (else trigger fresh `prakriya benchmark`)
- [ ] `next_lane.py` returned a lane (not BLOCKED)
- [ ] Dispatch brief filled with strict no-gaming rules
- [ ] `loop_state.json` updated atomically to `awaiting_lane_completion`
- [ ] Task list updated with current lane
