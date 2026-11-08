#!/usr/bin/env python3
"""Convert data/glossary/term_policy.json from the v1 structure to v2 (audit §5.4), deterministically.

    python3 scripts/migrate_term_policy_v2.py                    # print the per-row diff; write nothing
    python3 scripts/migrate_term_policy_v2.py --unified          # also print a unified diff of the JSON
    python3 scripts/migrate_term_policy_v2.py --out PATH         # write the v2 file to PATH (the lead decides when)

v1: {version, rule, detectors_note, terms: {lemma: {match, senses: {s: {policy, english|iast, …, review?}}}}, changelog?}
v2: {version: "2", rule, detectors_note, reserved_english, lemmas: {lemma: {lemma_iast, detect, occurrences,
     dossier, senses: {s: {policy, forms|iast, forbidden_english, glossaryKey, status, applies_to, decided, …}}}}, changelog}

What the conversion decides by rule, and prints for review:
  - translate senses: `english` becomes `forms: {"any": english}` (one list for every grammatical
    category). Per-category forms are a decision; the builder accepts "any" until they are split.
  - status: `review: pilot` → "pilot"; every other sense → --default-status (default
    "lexicon-reviewed": the v1 rows went through the chapter-12 independent reviews; lead,
    2026-11-08). The builder refuses rows still "proposed".
  - reserved_english: every translate rendering that belongs to exactly one lemma is reserved
    for it (standard §7.6 distinctness); renderings shared by two lemmas are listed, not reserved.
  - occurrences, applies_to, detect.root_ids and detect.upasargas: collected from the producer
    shards (internal/sanskrit_reviews/gita/ch*/producer-*.json) whose cards declare `term`.
  - lemma_iast: the preserved sense's IAST when there is one, else null (to fill).
Running it on a v2 file prints "already v2" and changes nothing.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_gita_chapter_reader as B  # noqa: E402

STATUSES = ("proposed", "pilot", "lexicon-reviewed", "owner-decided")


def collect_uses(shard_paths: list[Path]) -> dict[str, dict]:
    """lemma → {occurrences, senses: {sense: [loci]}, root_ids, upasargas} from cards declaring term/terms."""
    uses: dict[str, dict] = {}
    for sp in sorted(shard_paths):
        try:
            sh = json.loads(sp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for v in sh.get("verses") or []:
            for i, w in enumerate(v.get("words") or []):
                at = f"{v.get('locus')}[{i}]"
                for t in [w.get("term")] + list(w.get("terms") or []):
                    if not isinstance(t, dict) or not t.get("lemma"):
                        continue
                    u = uses.setdefault(t["lemma"], {"occurrences": [], "senses": {}, "root_ids": [], "upasargas": []})
                    if at not in u["occurrences"]:
                        u["occurrences"].append(at)
                    u["senses"].setdefault(t.get("sense"), [])
                    if at not in u["senses"][t.get("sense")]:
                        u["senses"][t.get("sense")].append(at)
                    if t is w.get("term") and w.get("root_id"):
                        if w["root_id"] not in u["root_ids"]:
                            u["root_ids"].append(w["root_id"])
                        ups = B.card_upasargas(w)
                        if ups and ups not in u["upasargas"]:
                            u["upasargas"].append(ups)
    key = lambda at: tuple(int(x) for x in at.replace("[", ".").rstrip("]").split("."))  # noqa: E731
    for u in uses.values():
        u["occurrences"].sort(key=key)
        for s in u["senses"].values():
            s.sort(key=key)
    return uses


def reserved_from(terms: dict) -> tuple[dict[str, str], dict[str, list[str]]]:
    owners: dict[str, set[str]] = {}
    for lemma, row in terms.items():
        for s in (row.get("senses") or {}).values():
            if s.get("policy") == "translate":
                for e in s.get("english") or []:
                    owners.setdefault(e, set()).add(lemma)
    reserved = {e: next(iter(ls)) for e, ls in sorted(owners.items()) if len(ls) == 1}
    shared = {e: sorted(ls) for e, ls in sorted(owners.items()) if len(ls) > 1}
    return reserved, shared


def migrate(v1: dict, uses: dict[str, dict], default_status: str = "lexicon-reviewed") -> tuple[dict, dict]:
    """Return (v2 policy, notes). Pure: the same inputs give the same output."""
    if "lemmas" in v1:
        return v1, {"already_v2": True}
    if "terms" not in v1:
        raise SystemExit("not a v1 term policy: no `terms`")
    reserved, shared = reserved_from(v1["terms"])
    notes = {"shared_renderings": shared, "lemma_iast_missing": [], "status": {}, "forms_any": 0, "no_occurrences": []}
    lemmas = {}
    for lemma, row in v1["terms"].items():
        u = uses.get(lemma, {})
        senses = {}
        for sname, s in (row.get("senses") or {}).items():
            out = {"policy": s.get("policy")}
            if s.get("policy") == "preserve":
                out["iast"] = s.get("iast")
                if s.get("iast_forms"):
                    out["iast_forms"] = s["iast_forms"]
            else:
                out["forms"] = {"any": list(s.get("english") or [])}
                notes["forms_any"] += 1
            for k in ("forbidden_english", "glossaryKey", "note"):
                if k in s:
                    out[k] = s[k]
            out["status"] = "pilot" if s.get("review") == "pilot" else default_status
            notes["status"][f"{lemma}/{sname}"] = out["status"]
            out["applies_to"] = list((u.get("senses") or {}).get(sname, []))
            out["decided"] = None
            senses[sname] = out
        preserve_iast = next((s.get("iast") for s in (row.get("senses") or {}).values() if s.get("policy") == "preserve" and s.get("iast")), None)
        if not preserve_iast:
            notes["lemma_iast_missing"].append(lemma)
        if not u.get("occurrences"):
            notes["no_occurrences"].append(lemma)
        lemmas[lemma] = {"lemma_iast": preserve_iast,
                         "detect": {"match": row.get("match"), "root_ids": list(u.get("root_ids") or []),
                                    "upasargas": list(u.get("upasargas") or [])},
                         "occurrences": list(u.get("occurrences") or []),
                         "dossier": None,
                         "senses": senses}
    v2 = {"version": "2",
          "migrated_from": {"version": v1.get("version"), "policy_sha256": B.policy_content_hash(v1)},
          "rule": v1.get("rule"),
          "detectors_note": ("Rows are matched by the lemma the card declares (term.lemma). detect.root_ids and "
                             "detect.upasargas make an undeclared occurrence an error; detect.match is a linter regex "
                             "(a warning). forms map a grammatical category to the admitted English; 'any' applies "
                             "to every category not listed."),
          "reserved_english": reserved,
          "lemmas": lemmas,
          "changelog": list(v1.get("changelog") or []) + [{"version": "2", "by": "scripts/migrate_term_policy_v2.py",
                                                           "changes": "structure v1 → v2 (audit §5.4); content unchanged"}]}
    return v2, notes


def row_diff(v1: dict, v2: dict) -> list[str]:
    lines = []
    for lemma, row in v1["terms"].items():
        new = v2["lemmas"][lemma]
        ch = [f"occurrences {len(new['occurrences'])}", f"root_ids {new['detect']['root_ids'] or '—'}"]
        for sname, s in new["senses"].items():
            old = row["senses"][sname]
            what = f"forms.any={s['forms']['any']}" if "forms" in s else f"iast={s.get('iast')}"
            was = f"english={old.get('english')}" if "english" in old else f"iast={old.get('iast')}"
            ch.append(f"{sname}: {was} → {what}; status {s['status']}" + (f" (was review: {old['review']})" if old.get("review") else "")
                      + f"; applies_to {len(s['applies_to'])}")
        lines.append(f"~ {lemma}: " + " | ".join(ch))
    return lines


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path, default=B.ROOT / "data/glossary/term_policy.json")
    ap.add_argument("--shards", nargs="*", type=Path, help="producer shards to collect occurrences from "
                    "(default internal/sanskrit_reviews/gita/ch*/producer-*.json)")
    ap.add_argument("--default-status", choices=STATUSES, default="lexicon-reviewed")
    ap.add_argument("--out", type=Path, help="write the v2 policy here (nothing is written otherwise)")
    ap.add_argument("--unified", action="store_true", help="print a unified diff of the two JSON texts")
    a = ap.parse_args(argv)
    v1 = json.loads(a.policy.read_text(encoding="utf-8"))
    shards = a.shards if a.shards is not None else sorted(B.ROOT.glob("internal/sanskrit_reviews/gita/ch*/producer-*.json"))
    v2, notes = migrate(v1, collect_uses(shards), a.default_status)
    if notes.get("already_v2"):
        print("already v2; nothing to do")
        return 0
    old_txt = json.dumps(v1, ensure_ascii=False, indent=2) + "\n"
    new_txt = json.dumps(v2, ensure_ascii=False, indent=2) + "\n"
    print(f"policy {a.policy}: v1 {v1.get('version')!r} ({B.policy_content_hash(v1)[:12]}) → v2 ({B.policy_content_hash(v2)[:12]})")
    print(f"rows {len(v2['lemmas'])}; senses {len(notes['status'])}; translate senses given forms.any: {notes['forms_any']}")
    status_counts: dict[str, int] = {}
    for st in notes["status"].values():
        status_counts[st] = status_counts.get(st, 0) + 1
    print(f"status: {status_counts}")
    print(f"reserved_english: {len(v2['reserved_english'])} renderings reserved; shared by two or more lemmas (not reserved): {notes['shared_renderings']}")
    print(f"lemma_iast to fill (no preserved sense): {len(notes['lemma_iast_missing'])}")
    print(f"rows with no occurrence in the shards: {notes['no_occurrences']}")
    print("+ top-level: reserved_english, migrated_from; terms → lemmas; changelog entry appended")
    for line in row_diff(v1, v2):
        print(line)
    if a.unified:
        sys.stdout.writelines(difflib.unified_diff(old_txt.splitlines(True), new_txt.splitlines(True), "term_policy.v1.json", "term_policy.v2.json"))
    if a.out:
        a.out.write_text(new_txt, encoding="utf-8")
        print(f"written {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
