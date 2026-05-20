#!/usr/bin/env bash
# post_merge_gate.sh — run compile + audit on a freshly-merged lane.
# On failure: auto-revert and write handoffs/reverted/<sha>.md.
#
# Usage: bash post_merge_gate.sh <lane-id>

set -euo pipefail

LANE_ID="${1:-}"
if [[ -z "$LANE_ID" ]]; then
  echo "usage: $0 <lane-id>" >&2
  exit 2
fi

REPO="${REPO:-/home/eeshan/vedanta-timeline}"
PRAKRIYA="${PRAKRIYA_REPO:-/nas/ucb/eeshan/prakriya}"
REPORT="${REPO}/handoffs/lanes/${LANE_ID}/report.json"
REVERT_DIR="${REPO}/handoffs/reverted"
mkdir -p "$REVERT_DIR"

if [[ ! -f "$REPORT" ]]; then
  echo "no report at $REPORT" >&2
  exit 2
fi

SHA=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("commit_sha",""))' "$REPORT")
if [[ -z "$SHA" ]]; then
  echo "no commit_sha in report" >&2
  exit 2
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
FAIL=0

# Gate 1: compile (light — python syntax pass over the touched files)
if [[ -d "$PRAKRIYA" ]]; then
  pushd "$PRAKRIYA" >/dev/null
  if ! python3 -m compileall -q . 2>/tmp/compile.err; then
    echo "[$NOW] gate=compile FAIL" >&2
    FAIL=1
  fi
  popd >/dev/null
fi

# Gate 2: audit (cross_corpus_bug_finder must not regress)
if [[ "$FAIL" -eq 0 && -f "$PRAKRIYA/scripts/cross_corpus_bug_finder.py" ]]; then
  if ! python3 "$PRAKRIYA/scripts/cross_corpus_bug_finder.py" --summary --json > /tmp/audit.json 2>/tmp/audit.err; then
    echo "[$NOW] gate=audit FAIL" >&2
    FAIL=1
  fi
fi

if [[ "$FAIL" -eq 1 ]]; then
  {
    echo "# Reverted $SHA — $NOW"
    echo
    echo "Lane: $LANE_ID"
    echo
    echo "## compile.err"
    [[ -f /tmp/compile.err ]] && cat /tmp/compile.err || echo "(none)"
    echo
    echo "## audit.err"
    [[ -f /tmp/audit.err ]] && cat /tmp/audit.err || echo "(none)"
  } > "${REVERT_DIR}/${SHA}.md"
  if [[ -d "$PRAKRIYA/.git" ]]; then
    git -C "$PRAKRIYA" revert --no-edit "$SHA" || echo "revert failed; manual intervention required" >&2
  fi
  exit 1
fi

echo "[$NOW] gate=PASS lane=$LANE_ID sha=$SHA"
exit 0
