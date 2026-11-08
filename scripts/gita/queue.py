#!/usr/bin/env python3
"""Orchestrator-neutral job queue for the Gītā translation pipeline.

Any agent runtime (Claude Code subagents or Workflow, OpenAI Codex tasks, a human)
drives the pipeline the same way:

    python3 scripts/gita/queue.py status                      # counts per type and state
    python3 scripts/gita/queue.py next --type lexicon --worker codex-3
        -> prints the claimed job as JSON (brief, inputs, output, validate) or "NONE"
    ... the worker reads the brief, writes the output file ...
    python3 scripts/gita/queue.py submit JOB_ID               # runs the validator; done or failed
    python3 scripts/gita/queue.py claim JOB_ID --worker W     # claim a specific job (fix jobs routed by agent_ref)
    python3 scripts/gita/queue.py release JOB_ID              # give a claimed job back
    python3 scripts/gita/queue.py add JOBS.json               # add jobs (used by the stage builders)
    python3 scripts/gita/queue.py show JOB_ID

A job is a JSON file in internal/gita_pipeline/queue/<state>/<id>.json:

    {"id": "lexicon-0007", "type": "lexicon", "stage": "B",
     "brief": "docs/gita_briefs/LEXICON_BRIEF.md",
     "inputs": ["internal/gita_pipeline/lexicon/jobs/lexicon-0007.input.json"],
     "output": "internal/gita_pipeline/lexicon/out/lexicon-0007.json",
     "validate": "python3 scripts/gita/validate_job.py lexicon internal/gita_pipeline/lexicon/out/lexicon-0007.json",
     "depends_on": ["packets-all"], "attempts": 0, "claimed_by": null, "log": []}

States are directories (pending, running, done, failed); a claim is an atomic
rename pending -> running, so concurrent workers never take the same job. A job is
claimable only when every job in depends_on is done. submit runs the validator with
the repository root as working directory; exit 0 moves the job to done, otherwise to
failed with the validator's output in the log (a failed job can be re-queued with
`retry`). Paths in a job are relative to the repository root.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "internal/gita_pipeline/queue"
STATES = ("pending", "running", "done", "failed")


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def ensure() -> None:
    for s in STATES:
        (QUEUE / s).mkdir(parents=True, exist_ok=True)


def find(job_id: str) -> tuple[str, Path] | None:
    for s in STATES:
        p = QUEUE / s / f"{job_id}.json"
        if p.exists():
            return s, p
    return None


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, job: dict) -> None:
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, p)


def done_ids() -> set[str]:
    return {p.stem for p in (QUEUE / "done").glob("*.json")}


def cmd_add(path: str) -> None:
    ensure()
    jobs = json.loads(Path(path).read_text(encoding="utf-8"))
    added = skipped = 0
    for j in jobs:
        for k in ("id", "type", "brief", "inputs", "output", "validate"):
            if k not in j:
                raise SystemExit(f"job missing {k}: {j}")
        if find(j["id"]):
            skipped += 1
            continue
        j.setdefault("depends_on", [])
        j.setdefault("attempts", 0)
        j.setdefault("claimed_by", None)
        j.setdefault("log", [])
        j.setdefault("agent_ref", None)   # for fix jobs: the worker that produced the shard
        j["created"] = now()
        save(QUEUE / "pending" / f"{j['id']}.json", j)
        added += 1
    print(json.dumps({"added": added, "already_present": skipped}))


def cmd_next(job_type: str | None, worker: str) -> None:
    ensure()
    ready = done_ids()
    for p in sorted((QUEUE / "pending").glob("*.json")):
        job = load(p)
        if job_type and job["type"] != job_type:
            continue
        if any(d not in ready for d in job.get("depends_on", [])):
            continue
        target = QUEUE / "running" / p.name
        try:
            os.rename(p, target)  # atomic claim
        except FileNotFoundError:
            continue  # another worker took it
        job["claimed_by"] = worker
        job["attempts"] = job.get("attempts", 0) + 1
        job["log"].append({"t": now(), "event": "claimed", "by": worker})
        save(target, job)
        print(json.dumps(job, ensure_ascii=False, indent=1))
        return
    print("NONE")


def cmd_claim(job_id: str, worker: str) -> None:
    """Claim a specific pending job (used to route a fix job back to the agent that
    wrote the shard: the fix job's `agent_ref` names it)."""
    hit = find(job_id)
    if not hit or hit[0] != "pending":
        raise SystemExit(f"{job_id} is not pending ({hit[0] if hit else 'unknown'})")
    _, p = hit
    job = load(p)
    if any(d not in done_ids() for d in job.get("depends_on", [])):
        raise SystemExit(f"{job_id} has unfinished dependencies")
    target = QUEUE / "running" / p.name
    os.rename(p, target)
    job["claimed_by"] = worker
    job["attempts"] = job.get("attempts", 0) + 1
    job["log"].append({"t": now(), "event": "claimed", "by": worker})
    save(target, job)
    print(json.dumps(job, ensure_ascii=False, indent=1))


def cmd_submit(job_id: str) -> int:
    hit = find(job_id)
    if not hit or hit[0] != "running":
        raise SystemExit(f"{job_id} is not running ({hit[0] if hit else 'unknown'})")
    _, p = hit
    job = load(p)
    out = ROOT / job["output"]
    if not out.exists():
        job["log"].append({"t": now(), "event": "submit-refused", "why": "output missing"})
        save(p, job)
        print(f"REFUSED: output {job['output']} does not exist")
        return 1
    r = subprocess.run(job["validate"], shell=True, cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout + r.stderr)[-4000:]
    if r.returncode == 0:
        job["log"].append({"t": now(), "event": "done", "validator": tail[-800:]})
        save(p, job)
        os.replace(p, QUEUE / "done" / p.name)
        print(f"DONE {job_id}")
        return 0
    job["log"].append({"t": now(), "event": "failed", "validator": tail})
    save(p, job)
    os.replace(p, QUEUE / "failed" / p.name)
    print(f"FAILED {job_id}\n{tail}")
    return 1


def cmd_move(job_id: str, frm: tuple[str, ...], to: str, event: str) -> None:
    hit = find(job_id)
    if not hit or hit[0] not in frm:
        raise SystemExit(f"{job_id} not in {frm}")
    _, p = hit
    job = load(p)
    job["log"].append({"t": now(), "event": event})
    job["claimed_by"] = None if to == "pending" else job.get("claimed_by")
    save(p, job)
    os.replace(p, QUEUE / to / p.name)
    print(f"{event.upper()} {job_id}")


def cmd_status() -> None:
    ensure()
    table: dict[str, dict[str, int]] = {}
    for s in STATES:
        for p in (QUEUE / s).glob("*.json"):
            t = load(p)["type"]
            table.setdefault(t, {k: 0 for k in STATES})[s] += 1
    print(json.dumps(table, indent=1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add"); s.add_argument("path")
    s = sub.add_parser("next"); s.add_argument("--type"); s.add_argument("--worker", default=os.environ.get("USER", "worker"))
    s = sub.add_parser("submit"); s.add_argument("job_id")
    s = sub.add_parser("claim"); s.add_argument("job_id"); s.add_argument("--worker", default=os.environ.get("USER", "worker"))
    s = sub.add_parser("release"); s.add_argument("job_id")
    s = sub.add_parser("retry"); s.add_argument("job_id")
    s = sub.add_parser("show"); s.add_argument("job_id")
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "add":
        cmd_add(a.path)
    elif a.cmd == "next":
        cmd_next(a.type, a.worker)
    elif a.cmd == "submit":
        return cmd_submit(a.job_id)
    elif a.cmd == "claim":
        cmd_claim(a.job_id, a.worker)
    elif a.cmd == "release":
        cmd_move(a.job_id, ("running",), "pending", "released")
    elif a.cmd == "retry":
        cmd_move(a.job_id, ("failed",), "pending", "retried")
    elif a.cmd == "show":
        hit = find(a.job_id)
        print(json.dumps(load(hit[1]), ensure_ascii=False, indent=1) if hit else "UNKNOWN")
    elif a.cmd == "status":
        cmd_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
