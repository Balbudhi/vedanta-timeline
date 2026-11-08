"""Shared paths and small exact helpers for the whole-Gītā pipeline.

Import guard: `scripts/gita/queue.py` shadows the standard library's `queue` module when
`scripts/gita` is the first entry of sys.path (the default for `python3 scripts/gita/X.py`),
and `concurrent.futures`, `multiprocessing` and `logging.handlers` import `queue`. Every entry
script calls `fix_sys_path()` before importing anything that may import `queue`.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent            # scripts/gita/gitapipe
GITA_SCRIPTS = HERE.parent                         # scripts/gita
ROOT = GITA_SCRIPTS.parents[1]                     # vedanta-timeline
PRAKRIYA = Path(os.environ.get("GITA_PRAKRIYA", ROOT.parent / "prakriya"))
PIPE = Path(os.environ.get("GITA_PIPELINE_DIR", ROOT / "internal/gita_pipeline"))

GITA_KIT = PRAKRIYA / "scripts/gita_kit"
LOOKUP_DIR = PRAKRIYA / "scripts/lookup"
VIDYUT_PY = PRAKRIYA / "tmp/vidyut-venv/bin/python"
DHATUPATHA = PRAKRIYA / "sources/raw/panini/lexica/dhatupatha.json"
POLICY = ROOT / "data/glossary/term_policy.json"
GLOSSARY = ROOT / "data/glossary"

# Verse counts of the BORI Bhagavad-Gītā (700 verses); checked against BORI by stage A.
VERSE_COUNTS = {1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47, 7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
                13: 34, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78}

SCHEMA_LEXICON = "gita-lexicon-v1"
SCHEMA_LEXICON_REVIEW = "gita-lexicon-review-v1"
SCHEMA_VERSE = "gita-verse-v1"
SCHEMA_REVIEW = "gita-review-v1"
SCHEMA_PACKET = "gita-verse-packet-v1"
SCHEMA_PRODUCER = "gita-producer-v2"

BRIEFS = {
    "lexicon": "docs/gita_briefs/LEXICON_BRIEF.md", "lexicon-fix": "docs/gita_briefs/LEXICON_BRIEF.md",
    "lexicon-review": "docs/gita_briefs/LEXICON_BRIEF.md", "lexicon-rereview": "docs/gita_briefs/LEXICON_BRIEF.md",
    "verse": "docs/gita_briefs/VERSE_BRIEF.md", "fix": "docs/gita_briefs/VERSE_BRIEF.md",
    "review": "docs/gita_briefs/REVIEW_BRIEF.md", "rereview": "docs/gita_briefs/REVIEW_BRIEF.md",
}
JUDGEMENT_TYPES = set(BRIEFS)
MECHANICAL_TYPES = {"lexicon-merge", "expand", "build"}


def fix_sys_path() -> None:
    """Move scripts/gita (and its realpath) behind the standard library on sys.path."""
    target = str(GITA_SCRIPTS)
    sys.path[:] = [p for p in sys.path if not (p and Path(p).resolve() == GITA_SCRIPTS)]
    sys.path.append(target)


def import_builder():
    """scripts/build_gita_chapter_reader.py as a module (the fail-closed builder)."""
    p = str(ROOT / "scripts")
    if p not in sys.path:
        sys.path.append(p)
    import build_gita_chapter_reader as builder  # noqa: E402
    return builder


def import_lookup():
    p = str(LOOKUP_DIR)
    if p not in sys.path:
        sys.path.append(p)
    import lookup  # noqa: E402
    return lookup


# ---------------------------------------------------------------- io
def read_json(p: Path | str) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write_json(p: Path | str, data: Any, indent: int | None = 1) -> Path:
    """Atomic write (temporary file in the same directory, then rename)."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=p.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=indent))
        f.write("\n")
    os.chmod(tmp, 0o644)
    os.replace(tmp, p)
    return p


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path | str) -> str:
    return sha256_bytes(Path(p).read_bytes())


def canon_hash(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def rel(p: Path | str) -> str:
    p = Path(p).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- Sanskrit text keys
def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")


def latin_key(s: str) -> str:
    """Accent-, hyphen- and case-free ASCII key (the builder's latin_key)."""
    s = unicodedata.normalize("NFD", s or "").lower()
    s = re.sub(r"[̀-ͯ]", "", s)
    return re.sub(r"[^a-z]", "", s)


def form_key(s: str) -> str:
    """Key of a pada form: NFC IAST without hyphens, spaces, avagraha or daṇḍas."""
    return re.sub(r"[\s\-'’ऽ|।॥]", "", nfc(s)).lower()


def lemma_file_key(lemma: str, root: str | None = None) -> str:
    """Filesystem-safe deterministic key for a meaning page."""
    base = latin_key(lemma) or "x"
    tag = canon_hash([nfc(lemma), nfc(root or "")])[:8]
    return f"{base}-{tag}"


def verse_locus(ch: int, v: int) -> str:
    return f"{ch}.{v}"


def parse_verse_locus(s: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})", (s or "").strip())
    if not m:
        return None
    ch, v = int(m.group(1)), int(m.group(2))
    return (ch, v) if ch in VERSE_COUNTS and 1 <= v <= VERSE_COUNTS[ch] else None


OCC_RE = re.compile(r"^(\d{1,2}\.\d{1,2})(?:(?::|\[)(\d+)\]?)?$")


def parse_occurrence(s: str) -> tuple[str, int | None] | None:
    """'12.1' | '12.1:5' | '12.1[5]' → ('12.1', 5|None); None when malformed or out of range."""
    m = OCC_RE.match((s or "").strip())
    if not m or not parse_verse_locus(m.group(1)):
        return None
    return m.group(1), (int(m.group(2)) if m.group(2) is not None else None)


def locus_sort_key(locus: str) -> tuple[int, int]:
    ch, v = locus.split(".")
    return int(ch), int(v)


def all_loci(chapters: list[int] | None = None) -> list[str]:
    chs = chapters or sorted(VERSE_COUNTS)
    return [verse_locus(c, v) for c in chs for v in range(1, VERSE_COUNTS[c] + 1)]


def parse_chapters(spec: str | None) -> list[int]:
    if not spec:
        return sorted(VERSE_COUNTS)
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = (int(x) for x in part.split("-"))
            out += list(range(a, b + 1))
        elif part:
            out.append(int(part))
    bad = [c for c in out if c not in VERSE_COUNTS]
    if bad:
        raise SystemExit(f"no such chapter(s): {bad}")
    return sorted(set(out))


# ---------------------------------------------------------------- pipeline paths
def packet_path(locus: str) -> Path:
    return PIPE / "packets/verses" / f"{locus}.json"


def meaning_path(key: str) -> Path:
    return PIPE / "packets/meaning" / f"{key}.json"


# A namespace keeps one run's jobs, outputs, lexicon and built shards apart (the chapter-12
# acceptance run: internal/gita_pipeline/acceptance/ch12/, job ids prefixed "acc12-"); packets,
# translations files and the queue stay shared.
NS: Path | None = None
PREFIX = ""


def set_namespace(name: str | None) -> None:
    global NS, PREFIX
    if not name:
        NS, PREFIX = None, ""
        return
    NS = PIPE / "acceptance" / name
    PREFIX = "acc" + re.sub(r"\D", "", name) + "-"


def namespace_from_path(p: Path | str) -> None:
    m = re.search(r"internal/gita_pipeline/acceptance/([^/]+)/", str(Path(p).resolve()))
    set_namespace(m.group(1) if m else None)


def ns() -> Path:
    return NS or PIPE


def in_namespace(job_id: str) -> bool:
    return job_id.startswith(PREFIX) if PREFIX else not job_id.startswith("acc")


def chapter_of_job(job_id: str) -> int | None:
    m = re.search(r"(?:verse|review|rereview|fix)-(\d+)-", job_id)
    return int(m.group(1)) if m else None


def merged_policy_path() -> Path:
    return ns() / "lexicon/term_policy.v3.json"


def current_policy_path() -> Path:
    """The table the pipeline works against: the merged v3 when it exists, else the site's."""
    p = merged_policy_path()
    return p if p.is_file() else POLICY
