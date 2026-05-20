#!/usr/bin/env bash
# start_sessions.sh — bring up the 3 new tmux sessions.
# Idempotent: skips any session that already exists.

set -euo pipefail

REPO="${REPO:-/home/eeshan/vedanta-timeline}"

declare -A SESSIONS=(
  [loop-tick]="while true; do bash ${REPO}/scripts/loop/loop_tick.sh; sleep 300; done"
  [stall-watchdog]="while true; do bash ${REPO}/scripts/loop/stall_watchdog.sh; sleep 600; done"
  [lane-chooser]="while true; do bash ${REPO}/scripts/loop/lane_chooser.sh; sleep 900; done"
)

for name in "${!SESSIONS[@]}"; do
  if tmux has-session -t "$name" 2>/dev/null; then
    echo "[skip] $name already running"
  else
    tmux new-session -d -s "$name" "${SESSIONS[$name]}"
    echo "[start] $name"
  fi
done

tmux ls
