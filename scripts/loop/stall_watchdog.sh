#!/usr/bin/env bash
# stall_watchdog.sh — detect lanes with >30 min of no commits.
# Writes handoffs/stalled_lanes.json; does NOT touch state machine directly.
#
# Runs every 10 minutes via tmux session `stall-watchdog`.

set -euo pipefail

REPO="${REPO:-/home/eeshan/vedanta-timeline}"
PRAKRIYA_REPO="${PRAKRIYA_REPO:-/nas/ucb/eeshan/prakriya}"
STATE_FILE="${REPO}/handoffs/loop_state.json"
OUT="${REPO}/handoffs/stalled_lanes.json"
LOG="${REPO}/handoffs/stall_watchdog.log"
STALL_SECONDS="${STALL_SECONDS:-1800}"  # 30 min

mkdir -p "$(dirname "$OUT")"
NOW_TS=$(date -u +%s)
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Lanes to check: parse open_lanes + current_lane.branch from loop_state.json.
# Use Python for robust JSON parsing.
LANES_JSON="$(python3 - <<'PY' 2>/dev/null || echo '[]'
import json, os, sys
p = os.environ.get("STATE_FILE")
try:
    d = json.load(open(p))
except Exception:
    print("[]"); sys.exit(0)
lanes = []
cur = d.get("current_lane")
if cur and cur.get("branch"):
    lanes.append({"lane_id": cur.get("id","unknown"), "branch": cur["branch"]})
for l in d.get("open_lanes", []) or []:
    if isinstance(l, dict) and l.get("branch"):
        lanes.append({"lane_id": l.get("id","unknown"), "branch": l["branch"]})
print(json.dumps(lanes))
PY
)"

# Iterate, query the prakriya repo for last commit timestamp per branch.
STALLED_ITEMS=()
if [[ -d "$PRAKRIYA_REPO/.git" ]]; then
  git -C "$PRAKRIYA_REPO" fetch --quiet --all 2>/dev/null || true
fi

while read -r LANE_ID BRANCH; do
  [[ -z "${BRANCH:-}" ]] && continue
  LAST_TS=0
  if [[ -d "$PRAKRIYA_REPO/.git" ]]; then
    LAST_TS=$(git -C "$PRAKRIYA_REPO" log -1 --format=%ct "origin/$BRANCH" 2>/dev/null || echo 0)
  fi
  AGE=$((NOW_TS - LAST_TS))
  if [[ "$LAST_TS" -gt 0 && "$AGE" -gt "$STALL_SECONDS" ]]; then
    STALLED_ITEMS+=("{\"lane_id\":\"$LANE_ID\",\"branch\":\"$BRANCH\",\"last_commit_ts\":$LAST_TS,\"age_seconds\":$AGE}")
  fi
done < <(echo "$LANES_JSON" | python3 -c 'import json,sys
for x in json.load(sys.stdin):
    print(x["lane_id"], x["branch"])')

# Emit atomic JSON
TMP="$(mktemp "${OUT}.XXXX")"
{
  echo "{"
  echo "  \"checked_at\": \"$NOW_ISO\","
  echo -n "  \"stalled\": ["
  IFS=,; echo -n "${STALLED_ITEMS[*]:-}"; unset IFS
  echo "]"
  echo "}"
} > "$TMP"
mv "$TMP" "$OUT"

echo "[$NOW_ISO] stall_count=${#STALLED_ITEMS[@]}" >> "$LOG"
