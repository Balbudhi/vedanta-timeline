#!/usr/bin/env python3
"""Run the translation stages with Codex (or Claude) workers, in parallel, each job looping
author -> code check -> independent review -> revise until accepted or MAX_ROUNDS.

    python3 scripts/gita/translate/drive.py construe --chapter 12
    python3 scripts/gita/translate/drive.py lexicon  --chapter 12
    python3 scripts/gita/translate/drive.py verse    --chapter 12
Outputs: internal/gita_pipeline/run/<run>/<stage>/<job>/{input,output,review*,events*,tool_calls}.json[l]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402
import compile as C  # noqa: E402

ROOT = HERE.parents[2]
PROMPTS = HERE / "prompts"
TOOL = HERE / "tool.py"
MAX_ROUNDS = int(os.environ.get("GITA_MAX_ROUNDS", "3"))
CHAPTER_LENGTHS = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]  # BORI (700); = lookup.CHAPTER_LENGTHS


TOOL_FREE = {"construe", "review_construe"}  # the parse card is complete: grammar first, commentaries last


def prompt(name: str, with_criteria: bool = True) -> str:
    p = (PROMPTS / f"{name}.md").read_text(encoding="utf-8")
    tool_free = name in TOOL_FREE or (name == "revise" and with_criteria is None)
    if with_criteria and name not in TOOL_FREE:
        p += "\n\n" + (PROMPTS / "criteria.md").read_text(encoding="utf-8")
    if tool_free:
        return p + ("\n\nThese instructions are complete. Read only input.json, output.json and review.json in this "
                    "folder; run no other command. A command touching any other path fails the job.")
    p += ("\n\nThese instructions are complete. Do not look for or read AGENTS.md, README, skills or any file "
          "outside this folder; the only other access you have is the tool. A command touching any other path "
          "fails the job.")
    return p.replace("TOOL", str(TOOL)) + f"\n\nTOOL = {TOOL}\n"


def codex(job: Path, text: str, out_name: str, tag: str, sandbox: str = "workspace-write") -> tuple[dict | None, float]:
    """One model session in the job folder through runner.py (Codex or Claude). With Claude the job's
    files are inlined (it has no tools); the agentic stages that need tool.py run only with Codex."""
    import runner
    if runner.RUNNER == "claude" and sandbox != "read-only":
        raise SystemExit("this stage uses tool.py and runs only with GITA_RUNNER=codex")
    files = {n: job / n for n in ("input.json", "output.json", "review.json")}
    r = runner.run(text, job, files=files, sandbox=sandbox, log=job / f"events_{tag}.jsonl",
                   env={"GITA_JOB_LOG": str(job / f"tool_calls_{tag}.jsonl")})
    (job / f"{out_name}.raw").write_text(r.raw, encoding="utf-8")
    m = re.search(r"\{.*\}", r.raw, re.S)
    try:
        return (json.loads(m.group(0)) if m else None), r.seconds
    except json.JSONDecodeError:
        return None, r.seconds


_codex = codex


def calls(job: Path) -> list[dict]:
    """Tool calls made by the author's sessions only (author and revisions), never the reviewer's."""
    out = []
    for f in sorted(job.glob("tool_calls_*.jsonl")):
        if f.stem.split("_", 2)[2].startswith(("author", "revise")):
            out += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    return out


def tokens(job: Path) -> int:
    n = 0
    for f in job.glob("events_*.jsonl"):
        for l in f.read_text(errors="ignore").splitlines():
            if '"turn.completed"' in l:
                u = (json.loads(l).get("usage") or {})
                n += u.get("input_tokens", 0) + u.get("output_tokens", 0)
    return n


def run_job(job: Path, author: str, checker, review: bool, reviewer: str = "review") -> dict:
    """author -> check -> (review) -> revise loop. Returns the job record. A tool-free stage (the parse)
    runs read-only: the model reads its folder's files and nothing else."""
    rec = {"job": job.name, "rounds": [], "seconds": 0.0}
    free = author in TOOL_FREE
    sb = "read-only" if free else "workspace-write"
    revise = prompt("revise", None if free else True)

    def codex(job, text, out_name, tag):  # noqa: F811  (the stage's sandbox)
        return _codex(job, text, out_name, tag, sb)
    if (job / "output.json").exists() and os.environ.get("GITA_REUSE_OUTPUT"):
        out, dt = json.loads((job / "output.json").read_text()), 0.0
    else:
        out, dt = codex(job, prompt(author), "output", "author")
    rec["seconds"] += dt
    for rnd in range(1, MAX_ROUNDS + 1):
        if out is None:
            rec["rounds"].append({"round": rnd, "error": "no JSON output"})
            out, dt = codex(job, prompt(author), "output", f"author{rnd}")
            rec["seconds"] += dt
            continue
        (job / "output.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        code_errs = checker(out) + check.forbidden_reads(job / f"events_{'author' if rnd == 1 else f'revise{rnd-1}'}.jsonl",
                                                         str(TOOL))
        findings, verdict = [], "accept"
        if review:
            rp = prompt(reviewer)
            if rnd > 1:
                rp += ("\n\nRE-REVIEW, round %d. `review.json` holds your previous findings and code errors; "
                       "`output.json` is the revision, with the author's `responses`. Rule on each previous finding: "
                       "resolved, or still open (a rejected finding stays open only if the author's evidence is wrong — "
                       "say why). Raise a NEW finding only for an S1 error the revision introduced. Do not re-review "
                       "unchanged parts." % rnd)
            rv, dt = codex(job, rp, f"review{rnd}", f"review{rnd}")
            rec["seconds"] += dt
            rv = rv or {"findings": [], "verdict": "revise", "error": "reviewer returned no JSON"}
            findings, verdict = rv.get("findings", []), rv.get("verdict")
        blocking = [f for f in findings if f.get("severity") in ("S1", "S2")]
        rec["rounds"].append({"round": rnd, "code_errors": code_errs, "findings": findings,
                              "blocking": len(blocking), "verdict": verdict})
        if not code_errs and not blocking:
            rec["accepted"] = True
            break
        (job / "review.json").write_text(json.dumps({"code": code_errs, "findings": findings}, ensure_ascii=False,
                                                    indent=1), encoding="utf-8")
        if rnd == MAX_ROUNDS:
            rec["accepted"] = False
            break
        new, dt = codex(job, revise, "output", f"revise{rnd}")
        rec["seconds"] += dt
        out = new or out
    rec["tokens"] = tokens(job)
    (job / "record.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def loci(ch: int) -> list[str]:
    return [f"{ch}.{v}" for v in range(1, CHAPTER_LENGTHS[ch - 1] + 1)]


def stage_dir(run: str, stage: str) -> Path:
    d = ROOT / "internal/gita_pipeline/run" / run / stage
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_outputs(d: Path) -> list[dict]:
    """Accepted outputs only: a job whose loop did not accept never feeds a later stage."""
    out = []
    for j in sorted(p for p in d.iterdir() if p.is_dir()):
        r = j / "record.json"
        if (j / "output.json").exists() and r.exists() and json.loads(r.read_text()).get("accepted"):
            out.append(json.loads((j / "output.json").read_text()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["construe", "lexicon", "verse"])
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--run", default="ch12-qual")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-review", action="store_true")
    a = ap.parse_args()
    d = stage_dir(a.run, a.stage)
    work = []
    if a.stage == "construe":
        for loc in (a.only or loci(a.chapter)):
            job = d / loc
            job.mkdir(exist_ok=True)
            inp = C.construe_input(loc)
            for f in ("record.json",):
                (job / f).unlink(missing_ok=True)
            (job / "input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=1), encoding="utf-8")
            work.append((job, "construe", (lambda o, inp=inp: check.construe(o, inp))))
        review = not a.no_review
    elif a.stage == "lexicon":
        cons = load_outputs(stage_dir(a.run, "construe"))
        fams = C.families(cons)
        batches, cur, size = [], [], 0
        for k in sorted(fams, key=lambda k: -sum(len(v) for v in fams[k]["lemmas"].values())):
            cur.append(k)
            size += len(fams[k]["lemmas"])
            if size >= 4:
                batches.append(cur)
                cur, size = [], 0
        if cur:
            batches.append(cur)
        for n, b in enumerate(batches):
            job = d / f"lex-{n:03d}"
            job.mkdir(exist_ok=True)
            inp = {"families": [C.family_input(fams[k]) for k in b]}
            (job / "input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=1), encoding="utf-8")
            work.append((job, "lexicon", (lambda o, inp=inp, job=job: check.lexicon(o, inp, calls(job)))))
        review = not a.no_review
    else:
        cons = {c["locus"]: c for c in load_outputs(stage_dir(a.run, "construe"))}
        rows = {}
        for o in load_outputs(stage_dir(a.run, "lexicon")):
            for r in o.get("rows", []):
                rows[r["sense_id"]] = r
        for u in C.units(list(cons.values())):
            if a.only and not set(u) & set(a.only):
                continue
            job = d / "-".join(u)
            job.mkdir(exist_ok=True)
            inp = C.unit_input(u, cons, rows)
            (job / "input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=1), encoding="utf-8")
            work.append((job, "verse", (lambda o, inp=inp: check.verse(o, inp, rows))))
        review = not a.no_review
    t = time.time()
    with ThreadPoolExecutor(a.jobs) as ex:
        reviewer = {"construe": "review_construe", "lexicon": "review_lexicon"}.get(a.stage, "review")
        recs = list(ex.map(lambda w: run_job(w[0], w[1], w[2], review, reviewer), work))
    summary = {"stage": a.stage, "jobs": len(recs), "wall_s": round(time.time() - t),
               "accepted": sum(1 for r in recs if r.get("accepted")),
               "rounds": [len(r["rounds"]) for r in recs], "job_s": [round(r["seconds"]) for r in recs],
               "tokens": sum(r.get("tokens", 0) for r in recs)}
    (d / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
