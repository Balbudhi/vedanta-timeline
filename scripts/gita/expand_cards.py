#!/usr/bin/env python3
"""Expand a verse-job output into the producer-v2 shard the builder reads (stage C).

    python3 scripts/gita/expand_cards.py VERSE_OUTPUT [--out PATH] [--review REVIEW]
        [--policy PATH] [--lexicon EXTRA_LEXICON.json] [--report PATH]

Default output: internal/sanskrit_reviews/gita/chN/producer-AA-BB.json (SCHEMAS amendment).
--review adds the review's readers_will_meet as reception lines and alternatives.
--lexicon adds gita-lexicon-v1 entries to the sense index (tests, the chapter-12 round trip).
The report (default next to the output: expand-AA-BB.report.json) holds expansion errors and the
builder's verse/card check, which the review job reads.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()


def shard_path(shard: dict) -> Path:
    return C.ROOT / f"internal/sanskrit_reviews/gita/ch{shard['chapter']}" / f"producer-{shard['range']}.json"


def expand(vpath: Path, out: Path | None = None, review: Path | None = None, policy: Path | None = None,
           lexicon: Path | None = None, report: Path | None = None, include_outputs: bool = True) -> tuple[Path, dict]:
    from gitapipe.expand import Expander
    from gitapipe import validate as V
    vo = C.read_json(vpath)
    extra = []
    if lexicon:
        extra += [e for e in C.read_json(lexicon).get("entries") or []]
    from gitapipe import lexicon as L
    extra += [e for r in vo.get("lexicon_requests") or [] if (e := L.request_entry(r))]
    ex = Expander(policy_path=policy, extra_entries=extra, include_outputs=include_outputs)
    rv = C.read_json(review) if review else None
    res = V.Result()
    shard = V.builder_check(res, ex, vo, vpath)
    if rv:   # the review's readers_will_meet become reception lines and alternatives
        shard, errs = ex.shard(vo, C.rel(vpath), C.sha256_file(vpath), review=rv, secondaries=V.secondaries_names(vo))
        res.errors += [f"expansion: {e}" for e in errs]
    out = out or shard_path(shard)
    C.write_json(out, shard, indent=1)
    rep = {"shard": C.rel(out), "shard_sha256": C.sha256_file(out), "verse_output": C.rel(vpath),
           "verse_output_sha256": C.sha256_file(vpath), "policy_sha256": shard["policy_sha256"],
           "errors": res.errors, "warnings": res.warnings, "fallback_count": shard["fallback_count"]}
    rp = report or out.with_name(out.name.replace("producer-", "expand-").replace(".json", ".report.json"))
    C.write_json(rp, rep)
    return out, rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verse_output", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--review", type=Path)
    ap.add_argument("--policy", type=Path)
    ap.add_argument("--lexicon", type=Path)
    ap.add_argument("--report", type=Path)
    a = ap.parse_args(argv)
    out, rep = expand(a.verse_output, a.out, a.review, a.policy, a.lexicon, a.report)
    print(json.dumps({k: rep[k] for k in ("shard", "shard_sha256", "fallback_count")} | {"errors": len(rep["errors"]), "warnings": len(rep["warnings"])},
                     ensure_ascii=False))
    for e in rep["errors"]:
        print("ERROR", e)
    return 1 if rep["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
