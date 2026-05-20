#!/usr/bin/env bash
# teardown.sh — called exactly once when all-green + zero open bug clusters.
# Kills the loop-specific tmux sessions; leaves benchmark-loop + phases-watchdog
# for ongoing monitoring.

set -euo pipefail

REPO="${REPO:-/home/eeshan/vedanta-timeline}"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

for s in loop-tick stall-watchdog lane-chooser; do
  if tmux has-session -t "$s" 2>/dev/null; then
    tmux kill-session -t "$s"
    echo "[$NOW] killed tmux session: $s"
  fi
done

# Final state stamp
python3 - <<PY
import json, time, os
p = os.path.join("${REPO}", "handoffs", "loop_state.json")
try:
    d = json.load(open(p))
except Exception:
    d = {}
d["state"] = "done"
d["terminated_at"] = "${NOW}"
json.dump(d, open(p, "w"), indent=2)
PY

echo "[$NOW] loop terminated."
