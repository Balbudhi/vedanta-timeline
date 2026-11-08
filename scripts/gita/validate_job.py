#!/usr/bin/env python3
"""Validate one job output (the command named in every job's `validate`).

    python3 scripts/gita/validate_job.py TYPE OUTPUT [--json] [--no-builder]

TYPE: lexicon | lexicon-fix | lexicon-review | lexicon-rereview | verse | fix | review | rereview.
Schema and referential checks per docs/gita_briefs/SCHEMAS.md (with its amendments); a verse
output is also expanded and run through the builder's verse and card checks. Exit 0 = valid.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("type")
    ap.add_argument("output", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-builder", action="store_true", help="verse: skip the expansion + builder check")
    a = ap.parse_args(argv)
    from gitapipe import validate as V
    fn = V.VALIDATORS.get(a.type)
    if fn is None:
        ap.error(f"unknown type {a.type}; one of {sorted(V.VALIDATORS)}")
    p = a.output if a.output.is_absolute() else C.ROOT / a.output
    C.namespace_from_path(p)           # an acceptance run's outputs live in their own namespace
    if not p.is_file():
        print(f"INVALID: {a.output} does not exist")
        return 1
    try:
        res = fn(p, run_builder=not a.no_builder) if a.type in ("verse", "fix") else fn(p)
    except json.JSONDecodeError as e:
        print(f"INVALID: {a.output} is not valid JSON ({e})")
        return 1
    if a.json:
        print(json.dumps({"errors": res.errors, "warnings": res.warnings}, ensure_ascii=False, indent=1))
    else:
        for w in res.warnings:
            print("WARN", w)
        for e in res.errors:
            print("ERROR", e)
        print(("VALID" if not res.errors else f"INVALID: {len(res.errors)} error(s)") + f" ({a.type} {a.output})")
    return 0 if not res.errors else 1


if __name__ == "__main__":
    sys.exit(main())
