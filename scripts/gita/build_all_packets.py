#!/usr/bin/env python3
"""Stage A (plan §7.3): every verse packet, the Gītā-wide lemma inventory and concordance,
meaning pages (one per content lemma), the shard plan and the private translations files.

    python3 scripts/gita/build_all_packets.py [--chapters 2,12 | 1-18] [--workers 8]
        [--fixture-oracle PATH] [--without-grammar] [--skip-meaning]

Writes under internal/gita_pipeline/: packets/verses/C.V.json, packets/inventory.json,
packets/concordance.json, packets/meaning/<key>.json, packets/shard_plan.json,
packets/manifest.json (counts and timings), secondaries/CH.json (review jobs only).
Fails with a clear message when the grammar or meaning oracle (prakriya scripts/gita_kit)
is absent. --without-grammar builds a labelled partial set (no analyses, no inventory).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chapters", help="e.g. 2,12 or 1-18 (default all)")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--fixture-oracle", help="canned oracle answers (tests)")
    ap.add_argument("--without-grammar", action="store_true", help="labelled partial build without the grammar oracle")
    ap.add_argument("--skip-meaning", action="store_true")
    a = ap.parse_args(argv)
    from gitapipe import stage_a, oracle
    t = time.perf_counter()
    try:
        m = stage_a.build(C.parse_chapters(a.chapters), a.workers, a.fixture_oracle, a.without_grammar, a.skip_meaning)
    except oracle.OracleUnavailable as e:
        print(f"STAGE A REFUSED: {e}", file=sys.stderr)
        return 2
    m["total_s"] = round(time.perf_counter() - t, 2)
    print(json.dumps({k: m[k] for k in ("verses", "forms", "analyses", "lemmas", "content_lemmas", "lexicon_scope",
                                         "meaning_pages", "shards", "timings_s", "total_s", "verses_without_recomposing_split")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
