#!/usr/bin/env bash
# v2 dispatcher: uses output-file presence as concurrency check.
# Each codex job is detached via setsid so it survives parent termination.

set -u
ROOT=/home/eeshan/philosophy
mkdir -p "$ROOT/handoffs/wave1_glossary_outputs"
mkdir -p "$ROOT/handoffs/wave1_glossary_logs"

MAX_CONCURRENT="${MAX_CONCURRENT:-5}"
SPEC_JSON="$ROOT/handoffs/glossary_top30_gaps.json"

dispatch_one() {
  local term="$1"
  local prompt_file="$ROOT/handoffs/wave1_glossary_prompts/${term}.prompt.md"
  local label="glossary_wave1_${term}"
  local out="$ROOT/handoffs/wave1_glossary_outputs/${term}.out.json"
  if [ -f "$out" ]; then
    echo "SKIP $term — output exists"
    return 0
  fi
  if [ ! -f "$prompt_file" ]; then
    echo "MISSING prompt for $term — skip"
    return 0
  fi
  local prompt
  prompt="$(cat "$prompt_file")"
  cd "$ROOT" && setsid nohup codex exec \
    --skip-git-repo-check --json \
    -c 'model="gpt-5.4"' \
    -c 'model_reasoning_effort="high"' \
    -c 'service_tier="fast"' \
    --add-dir "$ROOT" \
    --dangerously-bypass-approvals-and-sandbox \
    --output-last-message "$ROOT/handoffs/wave1_glossary_logs/${label}_lastmsg.txt" \
    "$prompt" \
    > "$ROOT/handoffs/wave1_glossary_logs/${label}.log" 2>&1 < /dev/null &
  disown
  echo "$(date -Iseconds)	dispatch	${label}	pid=$!" >> "$ROOT/handoffs/cron_log.tsv"
  echo "[${label}] pid=$!"
}

count_running() {
  # count distinct wave1 codex jobs by counting lastmsg files where the corresponding
  # output JSON does not yet exist
  local n=0
  for lf in "$ROOT/handoffs/wave1_glossary_logs"/glossary_wave1_*.log; do
    [ -f "$lf" ] || continue
    local term
    term=$(basename "$lf" .log)
    term="${term#glossary_wave1_}"
    if [ -f "$ROOT/handoffs/wave1_glossary_outputs/${term}.out.json" ]; then continue; fi
    # check if process still alive: lastmsg file exists only when codex EXITS, so use
    # the absence of lastmsg file plus log mtime within last 5 min as 'still running'
    if [ ! -f "$ROOT/handoffs/wave1_glossary_logs/glossary_wave1_${term}_lastmsg.txt" ]; then
      n=$((n+1))
    fi
  done
  echo "$n"
}

TERMS=$(python3 -c "import json; d=json.load(open('$SPEC_JSON'))['top30_gap_analysis']; print(' '.join(r['file'].replace('.json','') for r in d))")

for term in $TERMS; do
  while [ "$(count_running)" -ge "$MAX_CONCURRENT" ]; do
    sleep 10
  done
  dispatch_one "$term"
  sleep 1
done

echo "wave1 v2 dispatch complete."
