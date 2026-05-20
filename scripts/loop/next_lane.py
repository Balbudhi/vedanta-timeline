#!/usr/bin/env python3
"""next_lane.py — deterministic lane prioritisation.

Inputs (all optional; missing files mean "no signal"):
  - handoffs/all_phases_scoreboard.json (or PRAKRIYA path) — failing thresholds with current vs target.
  - cross_corpus_bug_finder.py --summary --json — bug cluster summary (we shell out if available).
  - handoffs/loop_state.json — for concurrency caps and open-lane bookkeeping.
  - handoffs/threshold_history.jsonl — last-N measurements per threshold (for plateau detection).

Output:
  - On success: stdout JSON {"lane": {...}}, exit 0.
  - On blocked: stdout JSON {"blocked": "<reason>", "threshold_id": "..."}, exit 2.
  - On error: stderr message, exit 1.

Priority score:
  0.6 * normalized_gap_to_target + 0.3 * normalized_corpus_breadth + 0.1 * recency_penalty_inverse
"""
from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

REPO = Path(os.environ.get("REPO", "/home/eeshan/vedanta-timeline"))
PRAKRIYA = Path(os.environ.get("PRAKRIYA_REPO", "/nas/ucb/eeshan/prakriya"))
HANDOFFS = REPO / "handoffs"
PRAKRIYA_HANDOFFS = PRAKRIYA / "handoffs"

MAX_CONCURRENT_PER_THRESHOLD = 2
PLATEAU_STREAK_BLOCK = 3


def _load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _load_jsonl(p: Path):
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def load_scoreboard():
    for cand in [
        PRAKRIYA_HANDOFFS / "scoreboard" / "all_phases_scoreboard.json",
        HANDOFFS / "all_phases_scoreboard.json",
    ]:
        d = _load_json(cand)
        if d:
            return d
    return {}


def load_state():
    return _load_json(HANDOFFS / "loop_state.json") or {}


def load_history():
    return _load_jsonl(HANDOFFS / "threshold_history.jsonl")


def open_lanes_by_threshold(state):
    counts = {}
    cur = state.get("current_lane")
    if cur and cur.get("threshold_id"):
        counts[cur["threshold_id"]] = counts.get(cur["threshold_id"], 0) + 1
    for lane in (state.get("open_lanes") or []):
        tid = lane.get("threshold_id")
        if tid:
            counts[tid] = counts.get(tid, 0) + 1
    return counts


def is_plateau(history, threshold_id):
    samples = [h["value"] for h in history if h.get("threshold_id") == threshold_id]
    if len(samples) < PLATEAU_STREAK_BLOCK:
        return False
    tail = samples[-PLATEAU_STREAK_BLOCK:]
    return all(x == tail[0] for x in tail)


def candidate_thresholds(scoreboard):
    """Return list of (threshold_id, gap_to_target, corpus_breadth, last_change_ts)."""
    out = []
    for t in scoreboard.get("thresholds", []) or []:
        if t.get("passing"):
            continue
        tid = t.get("id") or t.get("name")
        if not tid:
            continue
        cur = float(t.get("current", 0) or 0)
        tgt = float(t.get("target", 0) or 0)
        gap = max(0.0, tgt - cur)
        breadth = int(t.get("corpus_breadth", 1) or 1)
        last_change = int(t.get("last_change_ts", 0) or 0)
        out.append((tid, gap, breadth, last_change))
    return out


def bug_clusters():
    """Best-effort: read cross_corpus_bug_finder summary if it exists on disk."""
    cand = PRAKRIYA_HANDOFFS / "bugs" / "summary.json"
    d = _load_json(cand)
    if not d:
        return []
    out = []
    for c in d.get("clusters", []) or []:
        cid = c.get("id") or c.get("category")
        if not cid:
            continue
        size = int(c.get("size", 0) or 0)
        corpora = int(c.get("corpus_count", 1) or 1)
        out.append((f"bug-{cid}", float(size), corpora, 0))
    return out


def score(gap, breadth, last_change, gap_max, breadth_max, now):
    g = (gap / gap_max) if gap_max > 0 else 0.0
    b = (breadth / breadth_max) if breadth_max > 0 else 0.0
    age = max(1.0, now - last_change) if last_change else 1.0
    r = 1.0 / age
    return 0.6 * g + 0.3 * b + 0.1 * r


def main():
    state = load_state()
    sb = load_scoreboard()
    history = load_history()
    occupancy = open_lanes_by_threshold(state)

    pool = candidate_thresholds(sb) + bug_clusters()
    if not pool:
        print(json.dumps({"blocked": "no_candidates", "threshold_id": None}))
        sys.exit(2)

    now = int(time.time())
    gap_max = max((g for _, g, _, _ in pool), default=1.0) or 1.0
    breadth_max = max((b for _, _, b, _ in pool), default=1.0) or 1.0

    ranked = sorted(
        pool,
        key=lambda x: score(x[1], x[2], x[3], gap_max, breadth_max, now),
        reverse=True,
    )

    for tid, gap, breadth, last_change in ranked:
        if occupancy.get(tid, 0) >= MAX_CONCURRENT_PER_THRESHOLD:
            continue
        if is_plateau(history, tid):
            print(json.dumps({"blocked": "plateau", "threshold_id": tid}))
            sys.exit(2)
        lane = {
            "id": f"lane-{tid}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime(now))}",
            "threshold_id": tid,
            "branch": f"phase-acceptance/{tid}",
            "brief_path": "scripts/loop/dispatch_brief.tmpl.md",
            "context": {
                "gap_to_target": gap,
                "corpus_breadth": breadth,
                "chosen_at": now,
            },
        }
        print(json.dumps({"lane": lane}))
        sys.exit(0)

    print(json.dumps({"blocked": "all_candidates_capped_or_plateaued", "threshold_id": None}))
    sys.exit(2)


if __name__ == "__main__":
    main()
