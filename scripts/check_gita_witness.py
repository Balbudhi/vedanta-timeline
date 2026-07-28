#!/usr/bin/env python3
"""Check every Gītā reading's commentary Sanskrit against its cited witness.

The reading data files promise that a commentator's `sanskrit` is what the
on-disk witness actually reads, and that any editorial correction is recorded
in `textualNote`. Nothing enforced that promise, so this does.

For each entry the checker resolves the witness file named in `source`,
transliterates it if it is in Devanāgarī, folds out orthography that varies
freely between editions (compound hyphens, daṇḍa style, avagraha, soft
hyphens, whitespace, word-splitting sandhi), and requires the entry's Sanskrit
to appear in it verbatim.

Exit status is non-zero when an entry diverges from its witness without a
`textualNote` saying so. Divergences that ARE documented are reported as
emendations, not failures — the point is that no change is silent.

    python3 scripts/check_gita_witness.py

Requires: indic_transliteration (for Devanāgarī witnesses).
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unicodedata

REPO = pathlib.Path(__file__).resolve().parent.parent

# Orthography that carries no textual information at this level of comparison.
_INVISIBLE = "­​‌‍"          # soft hyphen, ZWSP, ZWNJ, ZWJ
_AVAGRAHA = "’‘'`ʼ"
_PUNCT = r"[-–—|।॥!?,.;:()\[\]\"“”/&*]"

DEVANAGARI = re.compile(r"[ऀ-ॿ]")


# Reference apparatus the e-texts interleave with the text itself: GRETIL's
# "|| ys_2.7 ||" / "BhGS_3.36" / "Bhg_03.036a" sigla and the critical
# edition's "[=MBh_06,025.036a]" concordance. A passage that spans two
# numbered units has these sitting in the middle of it.
_REFS = [
    re.compile(r"\[=[^\]]*\]"),
    re.compile(r"\b[A-Za-zĀ-ž]{2,12}_\d+[.,]\d+[a-z]?\b"),
    re.compile(r"\d+"),   # bare verse numbers: GRETIL's "// 426 //", "||37||"
]


def fold(text: str) -> str:
    """Reduce Sanskrit to the bare letter stream editions agree on."""
    text = unicodedata.normalize("NFC", text)
    for pattern in _REFS:
        text = pattern.sub(" ", text)
    text = "".join(ch for ch in text if ch not in _INVISIBLE)
    text = re.sub(f"[{_AVAGRAHA}]", "", text)
    text = re.sub(_PUNCT, "", text)
    text = re.sub(r"\s+", "", text).lower()
    # Anusvāra and final -m alternate freely between printed editions
    # (mahad aśanaṃ asyeti / mahad aśanam asyeti). Fold those two together —
    # and only those two. The other nasals stay distinct, because a ṅ/ñ/ṇ/n
    # difference is a real difference in the reading.
    return text.replace("ṁ", "ṃ").replace("m", "ṃ")


MULA = "data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt"


def load_reading(path: pathlib.Path) -> tuple[dict, list]:
    """Evaluate a reading's data files and hand back its commentary and verses."""
    script = f"""
      const fs = require("fs");
      global.window = {{}};
      for (const f of {json.dumps([str(p) for p in sorted(path.glob("*.js"))])}) {{
        try {{ eval(fs.readFileSync(f, "utf8")); }} catch (e) {{}}
      }}
      const commentary = {{}}, parallels = {{}};
      let verses = [];
      for (const k in global.window) {{
        if (/COMMENTARY$/.test(k)) Object.assign(commentary, global.window[k]);
        if (/PARALLELS$/.test(k)) Object.assign(parallels, global.window[k]);
        if (/VERSES$/.test(k)) verses = global.window[k];
      }}
      // A parallel quotes another tradition's text, so it is held to the same
      // standard as a commentary entry: verbatim against its own witness.
      for (const loc in parallels) {{
        commentary[loc] = (commentary[loc] || []).concat(parallels[loc].map(p =>
          Object.assign({{}}, p, {{ author: (p.school || "parallel") + " · " + (p.work || "") }})));
      }}
      process.stdout.write(JSON.stringify({{ commentary, verses }}));
    """
    proc = subprocess.run(["node", "-e", script], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"could not evaluate {path}: {proc.stderr[:400]}")
    data = json.loads(proc.stdout or '{"commentary":{},"verses":[]}')
    return data["commentary"], data["verses"]


_witness_cache: dict[str, str] = {}


def witness(rel_path: str) -> str | None:
    """The witness file's text, transliterated to IAST if it is Devanāgarī."""
    if rel_path in _witness_cache:
        return _witness_cache[rel_path]
    # Raw OCR is not a witness. Validating against it would confirm readings
    # the scanner invented — see data/sources/_unverified_ocr/README.md.
    if "_unverified_ocr" in rel_path:
        _witness_cache[rel_path] = None
        return None
    full = REPO / rel_path
    if not full.exists():
        _witness_cache[rel_path] = None
        return None
    text = full.read_text(encoding="utf-8", errors="replace")
    # SuttaCentral Pali witnesses are JSON: {"dhp90:1": "Gataddhino visokassa, ", …}.
    # The passage runs across several keyed segments, so join the values and
    # drop the keys — otherwise no multi-line quotation can ever match.
    if full.suffix == ".json":
        try:
            text = " ".join(str(v) for v in json.loads(text).values())
        except (json.JSONDecodeError, AttributeError):
            pass
    sample = text[:200000]
    if len(DEVANAGARI.findall(sample)) > 200:
        from indic_transliteration import sanscript
        text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
    _witness_cache[rel_path] = fold(text)
    return _witness_cache[rel_path]


def source_path(entry: dict) -> str | None:
    """The witness file named in an entry's `source` field."""
    match = re.search(r"(data/sources/[^\s,;)]+)", entry.get("source", ""))
    return match.group(1) if match else None


def divergence_point(needle: str, hay: str) -> int:
    """Length of the longest prefix of `needle` still found in `hay`."""
    lo, hi = 0, len(needle)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if needle[:mid] in hay:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main() -> int:
    readings = sorted(p for p in (REPO / "gita").iterdir()
                      if p.is_dir() and (p / "commentaries.js").exists())
    verbatim = emended = 0
    failures: list[str] = []
    unresolved: list[str] = []

    # The mūla is checked against the critical edition, whose per-hemistich
    # reference tags have to come out before the verse reads continuously.
    mula_text = (REPO / MULA).read_text(encoding="utf-8") if (REPO / MULA).exists() else ""
    mula_text = re.sub(r"\[=MBh_[^\]]*\]", " ", mula_text)
    mula = fold(re.sub(r"Bhg_\d+\.\d+[a-z]?", " ", mula_text))
    mula_ok = mula_variant = 0

    for reading in readings:
        entries, verses = load_reading(reading)
        for verse in verses:
            label = f"{reading.name} {verse.get('locus', '?')} mūla"
            if not mula:
                unresolved.append(f"{label}: critical edition not on disk — {MULA}")
                break
            if fold(verse.get("iast", "")) in mula:
                mula_ok += 1
            elif verse.get("textualNote"):
                mula_variant += 1
                print(f"  variant     {label}\n              {verse['textualNote'][:110]}")
            else:
                at = divergence_point(fold(verse.get("iast", "")), mula)
                failures.append(
                    f"{label}: departs from the critical edition at char {at} "
                    f"with no textualNote\n      …{fold(verse.get('iast', ''))[max(0, at - 30):at + 20]}…")
        for locus in entries:
            for entry in entries[locus]:
                label = f"{reading.name} {locus} {entry.get('author', '?')}"
                rel = source_path(entry)
                if rel is None:
                    unresolved.append(f"{label}: `source` names no data/sources/ file")
                    continue
                hay = witness(rel)
                if hay is None:
                    unresolved.append(f"{label}: witness not on disk — {rel}")
                    continue
                needle = fold(entry.get("sanskrit", ""))
                if not needle:
                    failures.append(f"{label}: empty `sanskrit`")
                    continue
                if needle in hay:
                    verbatim += 1
                    continue
                at = divergence_point(needle, hay)
                context = needle[max(0, at - 30):at + 20]
                if entry.get("textualNote"):
                    emended += 1
                    print(f"  emendation  {label}\n              …{context}…")
                else:
                    failures.append(
                        f"{label}: diverges from {rel} at char {at}/{len(needle)} "
                        f"with no textualNote\n      …{context}…")

    print(f"\nmūla matching BORI crit.  : {mula_ok}")
    print(f"documented mūla variants : {mula_variant}")
    print(f"verbatim against witness : {verbatim}")
    print(f"documented emendations   : {emended}")
    print(f"undocumented divergences : {len(failures)}")
    if unresolved:
        print(f"\nunresolved ({len(unresolved)}) — witness not locatable, not checked:")
        for item in unresolved:
            print(f"  ? {item}")
    if failures:
        print("\nFAIL — every divergence must be recorded in `textualNote`:")
        for item in failures:
            print(f"  ! {item}")
        return 1
    print("\nAll commentary Sanskrit matches its witness. OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
