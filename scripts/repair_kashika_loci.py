#!/usr/bin/env python3
"""Recompute every Kāśikā locus in a producer shard with the corrected lookup tool.

Until 2026-11-08 the lookup tool applied the projection's offsets (which index
kashika_upstream.txt) to kashika_collated_clean.txt, so 'kashika' loci could land
on a neighbouring sūtra's vṛtti. This script finds each evidence item whose locus
names kashika_collated_clean.txt, reads the sūtra number from the item's claim or
quote (A.P.S), and replaces the locus with the tool's corrected value. Items with
no sūtra number are reported for the producer to fix by hand.

    python3 scripts/repair_kashika_loci.py internal/sanskrit_reviews/gita/ch12/producer-06-10.json
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "prakriya/scripts/lookup"))
import lookup

SUTRA_RE = re.compile(r"\b([1-8])\.([1-4])\.(\d{1,3})\b")

def walk(obj, fn):
    if isinstance(obj, dict):
        fn(obj)
        for v in obj.values():
            walk(v, fn)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, fn)

def main(path):
    p = Path(path); d = json.loads(p.read_text(encoding="utf-8"))
    changed, same, unfixable = [], [], []
    cache = {}
    def fix(item):
        # Kāśikā references live in `locus`, or beside a sūtra locus as `also` / `kashika`.
        for key in ("locus", "also", "kashika"):
            loc = item.get(key)
            if not isinstance(loc, str) or "kashika_collated_clean.txt" not in loc:
                continue
            # the item's own `sutra` field wins; then the sūtra number in the sister `locus`
            # (an Aṣṭādhyāyī line is cited beside its Kāśikā); then the claim/quote text.
            m = None
            # order: explicit `sutra`; the quote (it carries the sūtra's own number and text);
            # then the claim, which may mention a neighbouring rule first.
            for hay in (str(item.get("sutra", "")), item.get("quote", ""), item.get("claim", "")):
                m = SUTRA_RE.search(hay)
                if m:
                    break
            if not m:
                unfixable.append((loc, (item.get("claim") or "")[:80])); continue
            ref = ".".join(m.groups())
            if ref not in cache:
                try: cache[ref] = lookup.sutra_lookup(ref)
                except SystemExit: cache[ref] = None
            r = cache[ref]
            if not r or not r.get("kashika"):
                unfixable.append((loc, f"{ref}: no Kāśikā locus")); continue
            new = r["kashika"]
            suffix = loc[loc.find(".txt:") + 5:]
            suffix = suffix[len(suffix.split()[0]):] if suffix else ""   # keep a trailing label like " (Kāśikā)"
            if not loc.startswith(new):
                changed.append((ref, loc, new)); item[key] = new + suffix
                if key == "locus":
                    item["quote"] = r["kashika_text"][:160]
                item["locus_repaired"] = "2026-11-08 kashika offset fix"
            else:
                same.append(ref)
    walk(d, fix)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"file": str(p.name), "changed": len(changed), "unchanged": len(same), "unfixable": len(unfixable)}))
    for c in changed[:8]: print("  changed", c)
    for u in unfixable: print("  UNFIXABLE", u)

if __name__ == "__main__":
    main(sys.argv[1])
