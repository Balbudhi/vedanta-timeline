#!/usr/bin/env bash
# lane_chooser.sh — call next_lane.py and persist the result.
# Writes handoffs/lane_to_dispatch.json OR handoffs/human_escalation.md.
# Does NOT dispatch — orchestrator owns dispatch.
#
# Runs every 15 minutes via tmux session `lane-chooser`.

set -euo pipefail

REPO="${REPO:-/home/eeshan/vedanta-timeline}"
OUT="${REPO}/handoffs/lane_to_dispatch.json"
ESC="${REPO}/handoffs/human_escalation.md"
LOG="${REPO}/handoffs/lane_chooser.log"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$(dirname "$OUT")"

# Only choose if state is evaluating_scoreboard OR awaiting_benchmark with stale dispatch.
STATE_FILE="${REPO}/handoffs/loop_state.json"
CUR_STATE="unknown"
if [[ -f "$STATE_FILE" ]]; then
  CUR_STATE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("state","unknown"))' "$STATE_FILE" 2>/dev/null || echo unknown)
fi

case "$CUR_STATE" in
  awaiting_lane_completion|merging|done|all_green)
    echo "[$NOW] skip: state=$CUR_STATE" >> "$LOG"
    exit 0
    ;;
esac

set +e
OUTPUT=$(python3 "${REPO}/scripts/loop/next_lane.py" 2>>"$LOG")
RC=$?
set -e

if [[ "$RC" -eq 0 ]]; then
  TMP="$(mktemp "${OUT}.XXXX")"
  printf '%s\n' "$OUTPUT" > "$TMP"
  mv "$TMP" "$OUT"
  echo "[$NOW] chose lane; wrote $OUT" >> "$LOG"
elif [[ "$RC" -eq 2 ]]; then
  {
    echo "# Human escalation — $NOW"
    echo
    echo "next_lane.py returned BLOCKED. Payload:"
    echo
    echo '```json'
    echo "$OUTPUT"
    echo '```'
    echo
    echo "Likely cause: plateau or concurrency cap. Investigate before resuming dispatch."
  } > "$ESC"
  rm -f "$OUT"
  echo "[$NOW] BLOCKED; wrote $ESC" >> "$LOG"
else
  echo "[$NOW] next_lane.py error rc=$RC" >> "$LOG"
fi
