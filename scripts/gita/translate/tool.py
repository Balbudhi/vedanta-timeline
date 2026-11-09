#!/usr/bin/env python3
"""The one command surface a translation agent uses (production mode).

Serves the Sanskrit library and the English dictionaries; never serves an English
translation of the Gītā (published, gita/gita, or this site's earlier lines). Every call
is appended to $GITA_JOB_LOG (JSON lines) so validators can check what was consulted.

    T=scripts/gita/translate/tool.py
    python3 -I $T dhatu ROOT            Dhātupāṭha artha + Dhātuvṛttis (Sanskrit)
    python3 -I $T meaning LEMMA         kośas, Dhātuvṛtti, Nirukta, Gītā concordance, commentator glosses
    python3 -I $T kosha WORD            Śabdakalpadruma, Vācaspatyam, Śabdārthacintāmaṇi (Sanskrit–Sanskrit)
    python3 -I $T amara|unadi|linga WORD
    python3 -I $T sutra N.N.N           sūtra, Kāśikā span, adhikāras
    python3 -I $T gita CH.V             BORI verse + every Sanskrit commentary on it
    python3 -I $T gloss CH.V            each word's clauses in every commentary
    python3 -I $T concord LEMMA         Gītā occurrences (Sanskrit lines only)
    python3 -I $T analyze FORM | split CH.V
    python3 -I $T english "a meaning in plain words"   find English words BY MEANING (reverse dictionary)
    python3 -I $T define WORD           verify an English word in seven dictionaries
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRAKRIYA = ROOT.parent / "prakriya"
LOOKUP = PRAKRIYA / "scripts/lookup/lookup.py"
KIT = PRAKRIYA / "scripts/gita_kit/gita_kit.py"
sys.path.insert(0, str(LOOKUP.parent))

DROP_MEANING_SECTIONS = ("## site renderings", "## dictionaries")  # prior English; S–E dictionaries


def _run(args: list[str]) -> str:
    r = subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True, cwd=PRAKRIYA)
    return r.stdout + (r.stderr if r.returncode else "")


def _drop_sections(text: str, drop: tuple[str, ...]) -> str:
    out, skip = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            skip = line.startswith(drop)
        if not skip:
            out.append(line)
    return "\n".join(out)


def _strip_keys(obj, keys: set[str]):
    if isinstance(obj, dict):
        return {k: _strip_keys(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_keys(v, keys) for v in obj]
    return obj


def run(cmd: str, rest: list[str]) -> str:
    if cmd == "dhatu":
        return json.dumps(_strip_keys(json.loads(_run([str(LOOKUP), "dhatu", *rest])), {"artha_english"}),
                          ensure_ascii=False, indent=1)
    if cmd == "meaning":
        return _drop_sections(_run([str(KIT), "meaning", "page", *rest]), DROP_MEANING_SECTIONS)
    if cmd == "kosha":
        return _run([str(LOOKUP), "kosha", *rest, "--dict", "skd,vcp,shs"])
    if cmd in ("amara", "unadi", "linga", "sutra", "gloss", "define", "english", "cheda"):
        return _run([str(LOOKUP), cmd, *rest])
    if cmd == "gita":
        import lookup
        r = _strip_keys(lookup.gita_lookup(rest[0]), {"english_translations", "translations", "word_meanings"})
        return json.dumps(r, ensure_ascii=False, indent=1)
    if cmd == "concord":
        import lookup
        r = _strip_keys(lookup.concord_lookup(rest[0]), {"rendering", "renderings", "english", "reader_cards", "cards", "gloss"})
        return json.dumps(r, ensure_ascii=False, indent=1)
    if cmd in ("analyze", "split", "derive"):
        return _run([str(KIT), "grammar", cmd, *rest])
    raise SystemExit(f"unknown command {cmd!r}; see the docstring of {__file__}")


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, rest = sys.argv[1], sys.argv[2:]
    out = run(cmd, rest)
    log = os.environ.get("GITA_JOB_LOG")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": time.time(), "cmd": cmd, "args": rest, "bytes": len(out.encode())},
                               ensure_ascii=False) + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
