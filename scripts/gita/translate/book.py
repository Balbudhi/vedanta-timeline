#!/usr/bin/env python3
"""The whole Gītā in one command: parse, translate and the owner sheet for every chapter asked for,
then one consistency pass over all of them (docs/GITA_FULL_TRANSLATION_PLAN.md §7 step 6).

    python3 scripts/gita/translate/book.py --prefix book --chapters 1-18 [--parallel 3] [--jobs 12]
    python3 scripts/gita/translate/book.py --prefix book --chapters 12,15 --stages translate,consistency

Runs are named <prefix>-chNN under internal/gita_pipeline/run/. Each stage is the existing command
(drive.py construe, pipeline.py translate / consistency / sheet), run as a subprocess so a chapter's
failure is recorded and the others continue. A stage whose output already exists is not repeated
unless --redo names it. The runner (Codex or Claude) is chosen with GITA_RUNNER, as everywhere.
Exit status is non-zero when any chapter fails a stage; book.json records every stage's outcome.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import drive  # noqa: E402

RUNS = drive.ROOT / "internal/gita_pipeline/run"
STAGES = ("construe", "translate", "consistency", "sheet")


def chapters(spec: str) -> list[int]:
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    if not out or any(not 1 <= c <= 18 for c in out):
        raise SystemExit(f"chapters must be within 1–18: {spec}")
    return sorted(set(out))


def done(run: str, stage: str, ch: int) -> bool:
    d = RUNS / run
    if stage == "construe":
        recs = [d / "construe" / f"{ch}.{v}" / "record.json" for v in range(1, drive.CHAPTER_LENGTHS[ch - 1] + 1)]
        return all(r.exists() and json.loads(r.read_text()).get("accepted") for r in recs)
    if stage == "translate":
        return (d / "translate" / "_summary_translate.json").exists()
    return False


def stage_cmd(stage: str, run: str, ch: int, a) -> list[str]:
    py = sys.executable
    if stage == "construe":
        return [py, str(HERE / "drive.py"), "construe", "--chapter", str(ch), "--run", run, "--jobs", str(a.jobs)]
    extra = ["--allow-partial-tools"] if a.allow_partial_tools else []
    return [py, str(HERE / "pipeline.py"), stage, "--run", run, "--jobs", str(a.jobs), *extra]


def run_stage(stage: str, run: str, ch: int, a, log: Path) -> dict:
    if stage not in a.redo and done(run, stage, ch):
        return {"chapter": ch, "stage": stage, "skipped": "already done"}
    t = time.time()
    with open(log, "a") as f:
        r = subprocess.run(stage_cmd(stage, run, ch, a), stdout=f, stderr=subprocess.STDOUT)
    return {"chapter": ch, "stage": stage, "exit": r.returncode, "s": round(time.time() - t)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="book")
    ap.add_argument("--chapters", default="1-18")
    ap.add_argument("--stages", default=",".join(STAGES))
    ap.add_argument("--redo", default="", help="stages to repeat even when their output exists")
    ap.add_argument("--parallel", type=int, default=3, help="chapters in flight at once")
    ap.add_argument("--jobs", type=int, default=12, help="model calls in flight per chapter")
    ap.add_argument("--allow-partial-tools", action="store_true")
    a = ap.parse_args()
    a.redo = set(filter(None, a.redo.split(",")))
    stages = [s for s in a.stages.split(",") if s]
    bad = set(stages) - set(STAGES)
    if bad:
        raise SystemExit(f"unknown stages {bad}; choose from {STAGES}")
    chs = chapters(a.chapters)
    runs = {ch: f"{a.prefix}-ch{ch:02d}" for ch in chs}
    for r in runs.values():
        (RUNS / r).mkdir(parents=True, exist_ok=True)
    book = RUNS / f"{a.prefix}-book.json"
    record: dict = {"chapters": chs, "runs": runs, "stages": []}
    failed: set[int] = set()
    for stage in stages:
        if stage == "consistency":  # once, over every chapter that reached this point
            ok = [ch for ch in chs if ch not in failed]
            t = time.time()
            with open(RUNS / f"{a.prefix}-consistency.log", "a") as f:
                r = subprocess.run([sys.executable, str(HERE / "pipeline.py"), "consistency", "--run",
                                    *[runs[c] for c in ok], "--jobs", str(a.jobs * a.parallel),
                                    *(["--allow-partial-tools"] if a.allow_partial_tools else [])],
                                   stdout=f, stderr=subprocess.STDOUT)
            record["stages"].append({"stage": stage, "chapters": ok, "exit": r.returncode, "s": round(time.time() - t)})
            if r.returncode:
                failed |= set(ok)
            continue
        todo = [ch for ch in chs if ch not in failed]
        with ThreadPoolExecutor(a.parallel) as ex:
            res = list(ex.map(lambda ch: run_stage(stage, runs[ch], ch, a, RUNS / runs[ch] / f"{stage}.log"), todo))
        for x in res:
            if x.get("exit"):
                failed.add(x["chapter"])
        record["stages"] += res
        book.write_text(json.dumps(record, indent=1), encoding="utf-8")
    record["failed_chapters"] = sorted(failed)
    book.write_text(json.dumps(record, indent=1), encoding="utf-8")
    print(json.dumps({"book": str(book), "failed_chapters": sorted(failed)}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
