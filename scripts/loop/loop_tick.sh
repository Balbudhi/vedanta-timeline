#!/usr/bin/env bash
# loop_tick.sh — read-only state aggregator.
# Merges scoreboard, watchdog nudge, stalled lanes, and known open lanes into
# handoffs/loop_state.json. NEVER edits code, NEVER commits, NEVER spawns agents.
#
# Runs every 5 minutes via tmux session `loop-tick`.

set -euo pipefail

REPO="${REPO:-/home/eeshan/vedanta-timeline}"
HANDOFFS="${HANDOFFS:-/nas/ucb/eeshan/prakriya/handoffs}"
STATE_FILE="${REPO}/handoffs/loop_state.json"
SCOREBOARD="${HANDOFFS}/scoreboard/all_phases_scoreboard.json"
NUDGE="${HANDOFFS}/watchdog_nudge.txt"
STALLED="${REPO}/handoffs/stalled_lanes.json"
LANE_TO_DISPATCH="${REPO}/handoffs/lane_to_dispatch.json"
LOG="${REPO}/handoffs/loop_tick.log"

mkdir -p "$(dirname "$STATE_FILE")"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Read previous state (or seed)
if [[ -f "$STATE_FILE" ]]; then
  PREV="$(cat "$STATE_FILE")"
else
  PREV='{"state":"awaiting_benchmark","open_lanes":[],"completed_lanes":[]}'
fi

# Compute facts (defensive: missing files are fine)
SCOREBOARD_PRESENT=false
ALL_GREEN=false
if [[ -f "$SCOREBOARD" ]]; then
  SCOREBOARD_PRESENT=true
  if grep -q '"all_green"[[:space:]]*:[[:space:]]*true' "$SCOREBOARD" 2>/dev/null; then
    ALL_GREEN=true
  fi
fi

NUDGE_PRESENT=false
[[ -f "$NUDGE" ]] && NUDGE_PRESENT=true

STALL_COUNT=0
if [[ -f "$STALLED" ]]; then
  STALL_COUNT=$(grep -c '"lane_id"' "$STALLED" 2>/dev/null || echo 0)
fi

# Derive next state — DO NOT override an in-flight lane unless stalled.
if echo "$PREV" | grep -q '"state"[[:space:]]*:[[:space:]]*"awaiting_lane_completion"'; then
  if [[ "$STALL_COUNT" -gt 0 ]]; then
    NEXT_STATE="escalate"
  else
    NEXT_STATE="awaiting_lane_completion"
  fi
elif [[ "$ALL_GREEN" == "true" ]]; then
  NEXT_STATE="all_green"
elif [[ "$SCOREBOARD_PRESENT" == "true" ]]; then
  NEXT_STATE="evaluating_scoreboard"
else
  NEXT_STATE="awaiting_benchmark"
fi

# Emit atomic write
TMP="$(mktemp "${STATE_FILE}.XXXX")"
cat > "$TMP" <<EOF
{
  "state": "$NEXT_STATE",
  "updated_at": "$NOW",
  "facts": {
    "scoreboard_present": $SCOREBOARD_PRESENT,
    "all_green": $ALL_GREEN,
    "watchdog_nudge_present": $NUDGE_PRESENT,
    "stalled_lane_count": $STALL_COUNT,
    "lane_to_dispatch_ready": $([[ -f "$LANE_TO_DISPATCH" ]] && echo true || echo false)
  },
  "_previous": $(printf '%s' "$PREV")
}
EOF
mv "$TMP" "$STATE_FILE"

echo "[$NOW] state=$NEXT_STATE all_green=$ALL_GREEN stall=$STALL_COUNT" >> "$LOG"
