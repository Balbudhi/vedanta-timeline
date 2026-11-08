#!/usr/bin/env python3
"""Merge the accepted lexicon outputs (and accepted verse-job lexicon requests) into the term
policy v3 (plan §7.4; SCHEMAS.md amendments).

    python3 scripts/gita/merge_lexicon.py [--no-requests] [--legacy-status proposed|pilot|owner-decided]
                                          [--install] [--allow-conflicts]

Writes internal/gita_pipeline/lexicon/term_policy.v3.json and merge_report.json. --install
also writes data/glossary/term_policy.json and the builder's policy snapshot (refused while a
conflict involving a new row stands). Legacy v1 rows are migrated by
scripts/migrate_term_policy_v2.py's migrate() (`review: pilot` → pilot, others → --legacy-status, default lexicon-reviewed).
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
    ap.add_argument("--no-requests", action="store_true")
    ap.add_argument("--legacy-status", default="lexicon-reviewed", choices=("proposed", "pilot", "lexicon-reviewed", "owner-decided"))
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--allow-conflicts", action="store_true")
    ap.add_argument("--namespace", help="e.g. ch12: merge the acceptance run's outputs into its own table (never installed)")
    ap.add_argument("--policy", type=Path, default=C.POLICY, help="the table to start from (default data/glossary/term_policy.json)")
    a = ap.parse_args(argv)
    from gitapipe import lexicon as L
    C.set_namespace(a.namespace)
    if a.namespace and a.install:
        ap.error("an acceptance namespace is never installed into data/glossary/")
    out_dir = C.ns() / "lexicon"
    with L.Lock(out_dir / "merge.lock"):
        base = C.read_json(a.policy)
        outs = [(f"lexicon {lx.get('job')}", e, {"job": lx.get("job"), "sha256": C.sha256_file(p), "review": rv.get("job")})
                for p, lx, rv in L.accepted_lexicon_outputs() for e in lx.get("entries") or [] if not e.get("skip")]
        if not a.no_requests:
            outs += [(f"request {job}", e, {"verse_job": job, "request": True})
                     for job, req in L.accepted_requests() if (e := L.request_entry(req))]
            # content words decided inline in verse jobs whose review accepted them
            outs += [(f"inline {', '.join(e['inline_from'])}", {k: v for k, v in e.items() if k != "inline_from"},
                      {"inline": e["inline_from"]}) for e in L.inline_entries(L.accepted_verse_outputs()) if not e["divergent"]]
        v3, rep = L.merge(base, outs, a.legacy_status)
        rep["inputs"] = sorted({o[0] for o in outs})
        new_conf = rep["conflicts"]
        # the table the pipeline works against changes only when the merge is clean
        target = out_dir / ("term_policy.v3.json" if not new_conf or a.allow_conflicts else "term_policy.v3.refused.json")
        C.write_json(target, v3, indent=2)
        rep["written"] = C.rel(target)
        C.write_json(out_dir / "merge_report.json", rep)
        print(json.dumps({"policy_sha256": rep["policy_sha256"], "rows": len(v3["lemmas"]), "inputs": len(rep["inputs"]),
                          "added": len(rep["added_senses"]), "enriched_legacy": len(rep["enriched_legacy"]),
                          "changed_legacy": len(rep["changed_legacy"]), "conflicts": len(new_conf),
                          "warnings": len(rep["warnings"]), "senses_the_builder_refuses": len(rep["senses_not_admitted_by_builder"])},
                         ensure_ascii=False))
        for c in new_conf:
            print("CONFLICT", json.dumps(c, ensure_ascii=False))
        if a.install:
            if new_conf and not a.allow_conflicts:
                print("NOT INSTALLED: resolve the conflicts (a lexicon-fix on the later batch) first")
                return 1
            C.write_json(C.POLICY, v3, indent=2)
            b = C.import_builder()
            snap = b.write_policy_snapshot(C.ROOT, C.POLICY)
            print(f"installed {C.rel(C.POLICY)} (policy {rep['policy_sha256'][:12]}); snapshot {C.rel(snap)}")
    return 1 if new_conf and not a.allow_conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
