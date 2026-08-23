"""Apply alias-augmentation proposals from the inventory script.

Conservative policy:
- Only apply variants whose IAST-folded form has the same stem as the entry's
  `term_key` (modulo terminal -s, -m, -n, -aḥ, -am).
- Skip compound proposals where the variant contains a hyphen segment that is
  NOT in the entry's term_key stem (e.g. `kalyāṇa-guṇas` for `guna` — the
  qualifier `kalyāṇa-` is not part of the lemma).
- Preserve existing alias ordering; append new aliases in order of first
  occurrence count (descending).
- Idempotent: re-running the script with no new proposals is a no-op.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_DIR = os.path.join(ROOT, "data", "glossary")
QUEUE_PATH = os.path.join(ROOT, "audit", "glossary_terms_to_create.json")

_IAST_FOLD = str.maketrans({
    "ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṝ": "r", "ḷ": "l", "ḹ": "l",
    "ṅ": "n", "ñ": "n", "ṭ": "t", "ḍ": "d", "ṇ": "n",
    "ś": "s", "ṣ": "s", "ṃ": "m", "ḥ": "h",
    "Ā": "a", "Ī": "i", "Ū": "u", "Ṛ": "r", "Ṝ": "r", "Ḷ": "l", "Ḹ": "l",
    "Ṅ": "n", "Ñ": "n", "Ṭ": "t", "Ḍ": "d", "Ṇ": "n",
    "Ś": "s", "Ṣ": "s", "Ṃ": "m", "Ḥ": "h",
})


def fold(s):
    return s.lower().translate(_IAST_FOLD)


def stem(s):
    s = fold(s)
    for suf in ("s", "m", "n"):
        if len(s) > 3 and s.endswith(suf):
            return s[:-1]
    if s.endswith("ah"):
        return s[:-2]
    if s.endswith("am"):
        return s[:-2]
    return s


def main():
    queue = json.load(open(QUEUE_PATH, encoding="utf-8"))
    proposals = queue.get("alias_augmentation_proposals", [])

    # Known homonyms — variants that look like inflections but actually refer
    # to a different lexeme. Maintained manually based on translator-note
    # warnings in the glossary entries themselves.
    HOMONYM_EXCLUSIONS = {
        # `brahmā` (the creator deity, masc.) is NOT `brahman` (the neutral
        # absolute). The brahman.json translator_note explicitly disambiguates.
        ("brahman", "brahmā"),
        # `kārma` (adjectival "of karma") is acceptable but rare; left for
        # editorial review rather than automatic addition.
        ("karma", "kārma"),
        # `śābda` (adjectival "verbal/scriptural") differs from `śabda` (word,
        # the testimony pramāṇa); keep separate.
        ("sabda", "śābda"),
    }

    by_target = {}
    for p in proposals:
        by_target.setdefault(p["existing_key"], []).append(p)

    applied = []
    skipped = []
    files_changed = 0

    for term_key, props in by_target.items():
        path = os.path.join(GLOSSARY_DIR, term_key + ".json")
        if not os.path.exists(path):
            for p in props:
                skipped.append({"variant": p["variant"], "reason": "missing-file", "target": term_key})
            continue
        with open(path, encoding="utf-8") as f:
            entry = json.load(f)
        existing_aliases = list(entry.get("aliases", []))
        existing_set = set(existing_aliases)
        new_aliases = []
        key_stem = stem(term_key)
        for p in sorted(props, key=lambda x: -x["occurrences"]):
            variant = p["variant"]
            if variant in existing_set:
                continue
            if (term_key, variant) in HOMONYM_EXCLUSIONS:
                skipped.append({
                    "variant": variant,
                    "target": term_key,
                    "reason": "homonym exclusion — distinct lexeme per translator note",
                    "occurrences": p["occurrences"],
                })
                continue

            # Conservative same-stem check.
            v_folded = fold(variant)
            v_stem = stem(variant)

            # Allow if (a) folded variant differs from term_key only by IAST
            # diacritics, or (b) variant stem matches key stem after suffix
            # strip, or (c) variant is the entry's term_iast itself.
            keep = False
            if v_stem == key_stem:
                keep = True
            if entry.get("term_iast") and variant == entry["term_iast"]:
                keep = True
            # Allow hyphenated compounds when the compound matches a known
            # variant form of the lemma (e.g. `tattva-vāda` ↔ `dvaita`,
            # `vivarta-vāda` ↔ `vivarta`) — flagged but kept since the
            # editorial intent is captured by the proposal itself.
            if "-" in variant and v_stem.startswith(key_stem):
                keep = True
            # Special: variant differs only in vāda-suffix attached to key.
            if v_folded.replace("-", "") == fold(term_key) + "vada":
                keep = True

            if keep:
                new_aliases.append(variant)
                applied.append({"target": term_key, "variant": variant, "occurrences": p["occurrences"]})
            else:
                skipped.append({
                    "variant": variant,
                    "target": term_key,
                    "reason": "stem mismatch — needs editorial review",
                    "occurrences": p["occurrences"],
                })

        if new_aliases:
            entry["aliases"] = existing_aliases + new_aliases
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)
                f.write("\n")
            files_changed += 1

    # Capitalization gap pass — always safe (just add a Title-case alias).
    cap_applied = []
    for entry_cg in queue.get("capitalization_gaps", []):
        tok = entry_cg["capitalized_token"]
        tgt = entry_cg["existing_key"]
        path = os.path.join(GLOSSARY_DIR, tgt + ".json")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            entry = json.load(f)
        aliases = list(entry.get("aliases", []))
        if tok in aliases:
            continue
        aliases.append(tok)
        entry["aliases"] = aliases
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
            f.write("\n")
        cap_applied.append({"target": tgt, "variant": tok, "occurrences": entry_cg["occurrences"]})
        files_changed += 1

    report_path = os.path.join(ROOT, "audit", "alias_augmentation_applied.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "applied": applied,
            "capitalization_applied": cap_applied,
            "skipped_for_review": skipped,
            "files_changed": files_changed,
        }, f, indent=2, ensure_ascii=False)

    print(f"Files modified: {files_changed}")
    print(f"Aliases applied (inflection/variant): {len(applied)}")
    print(f"Capitalization gaps applied: {len(cap_applied)}")
    print(f"Skipped (review needed): {len(skipped)}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
