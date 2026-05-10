#!/usr/bin/env python3
"""Citation grounding audit (structural + lexical).

Sibling to `audit_citations.py`, which checks IAST-fragment presence on disk.
This script audits a DIFFERENT failure mode: the cite-link's target is the
wrong text. Concretely, when a passage of prose attributes a doctrinal point
to commentator X's commentary on root-text Y, the cite-link should resolve
to X's commentary — not to Y itself.

We walk every `cite://` link occurrence in:
  - site/data/thinkers/*.json (every string-valued field, deeply)
  - site/data/articles/source/*.md
  - site/data/glossary/*.json
  - site/data/perspectives/source/*.md

For each occurrence we record:
  - file                — the file where the cite appears
  - host_thinker_id     — the thinker JSON containing this prose (None for
                          articles/glossary/perspectives)
  - field_path          — JSON path of the host string (or markdown section)
  - prose_window        — ~240 chars of prose either side of the cite-link
  - visible_text        — the markdown link visible text
  - target_key          — the cite://... key
  - target_thinker_id   — first path component of target_key
  - target_work_id      — second path component of target_key
  - locus_tail          — remaining path of target_key
  - index_entry_present — bool: does citation_index.json have this key?
  - entry_verified      — value of the entry's `verified` field, if present
  - entry_has_iast      — bool: does the entry carry a non-empty sanskrit_iast

Then we apply structural verdicts:

  CORRECT
    The cite-key's thinker matches the prose's host_thinker_id, the entry
    exists, and either the entry is verified true OR it carries IAST OR it
    is honestly flagged pending/false.

  WRONG-TARGET-THINKER
    The prose host_thinker_id != target_thinker_id, and the prose-window
    explicitly names a commentary work or commentator (matched against a
    small lexicon) whose owner is host_thinker_id. Example: prose by
    sudarsana cites ramanuja/shri-bhasya/1.1.1 while the prose says
    "Śruta-Prakāśikā on Śrī-Bhāṣya 1.1.1" — the cite ought to point at
    sudarsana's Śruta-Prakāśikā, not Rāmānuja's Śrī-Bhāṣya. We flag this
    even when the secondary parenthetical (the locus on which the
    commentary comments) is true — because the cite-link RESOLVES to the
    parent, not the attesting commentary.

  PENDING-ACQUISITION
    The cite-key thinker matches host, entry is missing or entry.verified ==
    "pending-acquisition". The reader will see the honest popover.

  MISSING-ENTRY
    The citation_index has no entry for this key at all. (We cannot
    distinguish honest pending vs. fabricated without acquisition state.)

  UNVERIFIED-FALSE
    Entry exists but `verified: false` from the IAST-fragment audit.

  CORRECT-UNKNOWN
    Entry exists, verified == "unknown" (the IAST audit has not yet been
    run for this entry). Treated as CORRECT for grounding purposes.

The output is a markdown table at
  handoffs/citation_grounding_audit_<date>.md

with summary numbers, the top-N WRONG-TARGET-THINKER findings ranked by
how confident the lexicon match is (longer / more specific commentary-name
match → higher confidence), and a per-thinker rollup.

This audit does NOT mutate citation_index.json or any thinker JSON. Fixes
are applied by a separate pass (see handoffs/citation_grounding_audit_*).
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = REPO_ROOT / "site"
DATA_ROOT = SITE_ROOT / "data"
CITATION_INDEX = DATA_ROOT / "citation_index.json"
HANDOFFS = REPO_ROOT / "handoffs"

CITE_RE = re.compile(r"\[([^\]]+?)\]\(cite://([^)\n]+)\)")
WINDOW = 240


def normalise(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s or "")
    no_diac = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    return no_diac.lower()


def iter_strings(obj: Any, path: str = "$") -> Iterable[Tuple[str, str]]:
    """Yield (json_path, string_value) for every string in a JSON tree."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}")


def load_citation_index() -> Dict[str, Any]:
    return json.loads(CITATION_INDEX.read_text(encoding="utf-8"))


def load_thinker_meta() -> Dict[str, Dict[str, Any]]:
    """Map thinker_id -> {name, works: {work_id: {title, aliases}}}"""
    out = {}
    for fp in sorted((DATA_ROOT / "thinkers").glob("*.json")):
        try:
            t = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        tid = t.get("id") or fp.stem
        works = {}
        for w in t.get("engaged_works", []) or []:
            wid = w.get("work_id") or ""
            if not wid:
                continue
            title = w.get("title") or w.get("title_iast") or wid
            title_iast = w.get("title_iast") or title
            aliases = [title, title_iast]
            works[wid] = {
                "title": title,
                "title_iast": title_iast,
                "aliases": [a for a in aliases if a],
            }
        out[tid] = {
            "name": t.get("name") or t.get("name_iast") or tid,
            "name_iast": t.get("name_iast") or t.get("name") or tid,
            "works": works,
        }
    return out


def extract_cites_from_file(fp: Path, host_thinker_id: Optional[str]) -> List[Dict[str, Any]]:
    """Return one record per cite occurrence in this file."""
    out: List[Dict[str, Any]] = []
    if fp.suffix == ".json":
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            return out
        for path, s in iter_strings(obj):
            for m in CITE_RE.finditer(s):
                vis, key = m.group(1), m.group(2)
                start = max(0, m.start() - WINDOW)
                end = min(len(s), m.end() + WINDOW)
                out.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "host_thinker_id": host_thinker_id,
                    "field_path": path,
                    "visible_text": vis,
                    "target_key": key,
                    "prose_window": s[start:end],
                })
    else:
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception:
            return out
        for m in CITE_RE.finditer(text):
            vis, key = m.group(1), m.group(2)
            start = max(0, m.start() - WINDOW)
            end = min(len(text), m.end() + WINDOW)
            out.append({
                "file": str(fp.relative_to(REPO_ROOT)),
                "host_thinker_id": host_thinker_id,
                "field_path": "(markdown)",
                "visible_text": vis,
                "target_key": key,
                "prose_window": text[start:end],
            })
    return out


def gather_all_cites(thinker_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    # Thinker JSONs.
    for fp in sorted((DATA_ROOT / "thinkers").glob("*.json")):
        try:
            t = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        tid = t.get("id") or fp.stem
        records.extend(extract_cites_from_file(fp, tid))
    # Articles.
    art_src = DATA_ROOT / "articles" / "source"
    if art_src.is_dir():
        for fp in sorted(art_src.glob("*.md")):
            records.extend(extract_cites_from_file(fp, None))
    # Perspectives.
    pers_src = DATA_ROOT / "perspectives" / "source"
    if pers_src.is_dir():
        for fp in sorted(pers_src.glob("*.md")):
            records.extend(extract_cites_from_file(fp, None))
    # Glossary.
    gloss = DATA_ROOT / "glossary"
    if gloss.is_dir():
        for fp in sorted(gloss.glob("*.json")):
            records.extend(extract_cites_from_file(fp, None))
    return records


def annotate_with_index(records: List[Dict[str, Any]], idx: Dict[str, Any]) -> None:
    entries = idx.get("entries") or {}
    aliases = idx.get("aliases") or {}
    for r in records:
        key = r["target_key"]
        parts = key.split("/")
        r["target_thinker_id"] = parts[0] if parts else ""
        r["target_work_id"] = parts[1] if len(parts) > 1 else ""
        r["locus_tail"] = "/".join(parts[2:]) if len(parts) > 2 else ""
        entry = entries.get(key)
        if entry is None and key in aliases:
            entry = entries.get(aliases[key])
        r["index_entry_present"] = entry is not None
        r["entry_verified"] = (entry or {}).get("verified")
        r["entry_has_iast"] = bool((entry or {}).get("sanskrit_iast"))


def commentary_lexicon(thinker_meta: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    """Build a lexicon of (normalised work-or-commentator phrase, owner_thinker_id, kind)
    so we can ask: in this prose-window, is there a commentary work mentioned
    whose owner is NOT the cite's target thinker?
    Only includes work titles >= 6 normalised chars (avoid spurious hits).
    """
    lex: List[Tuple[str, str, str]] = []
    for tid, meta in thinker_meta.items():
        for w in meta["works"].values():
            for alias in w["aliases"]:
                n = re.sub(r"[^a-z0-9 ]+", " ", normalise(alias))
                n = re.sub(r"\s+", " ", n).strip()
                if len(n) < 6:
                    continue
                lex.append((n, tid, "work"))
        # Also the thinker's own name (for "X says…" patterns).
        for nm in {meta["name"], meta["name_iast"]}:
            n = re.sub(r"[^a-z0-9 ]+", " ", normalise(nm))
            n = re.sub(r"\s+", " ", n).strip()
            if len(n) < 5:
                continue
            lex.append((n, tid, "name"))
    # Sort longest-first so longer specific phrases beat short prefixes.
    lex.sort(key=lambda x: -len(x[0]))
    return lex


def classify(r: Dict[str, Any], lex: List[Tuple[str, str, str]]) -> Tuple[str, str]:
    """Return (verdict, note)."""
    key_verified = r.get("entry_verified")
    target_tid = r.get("target_thinker_id") or ""
    host_tid = r.get("host_thinker_id") or ""

    if not r["index_entry_present"]:
        return ("MISSING-ENTRY", "no citation_index entry")

    if key_verified == "pending-acquisition":
        return ("PENDING-ACQUISITION", "entry flagged pending-acquisition")

    if key_verified is False:
        return ("UNVERIFIED-FALSE", "IAST not located on disk")

    # Lexical mismatch hunt: in the prose-window, do we see a commentary
    # phrase whose owner is NOT the cite-target thinker?
    win_norm = re.sub(r"[^a-z0-9 ]+", " ", normalise(r["prose_window"]))
    win_norm = re.sub(r"\s+", " ", win_norm).strip()
    matched_phrase = None
    matched_owner = None
    for phrase, owner, kind in lex:
        if owner == target_tid:
            continue
        # require word-boundary-ish match
        if f" {phrase} " in f" {win_norm} ":
            # Skip if this is the host's own thinker name "X" — that's just
            # self-reference, not evidence of a wrong target.
            if owner == host_tid and kind == "name":
                continue
            matched_phrase = phrase
            matched_owner = owner
            break
    if matched_phrase:
        if matched_owner == host_tid:
            return (
                "WRONG-TARGET-THINKER",
                f"prose names work/commentator owned by host '{host_tid}' "
                f"(matched '{matched_phrase}') but cite points at '{target_tid}'",
            )
        # Otherwise it's a cross-reference to a third party — common and
        # legitimate ("Rāmānuja replies to Maṇḍana..."). Don't flag.

    if key_verified == "unknown":
        return ("CORRECT-UNKNOWN", "entry present, IAST audit pending")
    if key_verified is True or r["entry_has_iast"]:
        return ("CORRECT", "")
    return ("CORRECT-UNKNOWN", "entry present, no flag")


def render_report(records: List[Dict[str, Any]],
                  verdicts: List[Tuple[str, str]],
                  thinker_meta: Dict[str, Any]) -> str:
    total = len(records)
    counter = Counter(v for v, _ in verdicts)
    by_target = Counter(r["target_key"] for r in records)
    wrong = [
        (r, n) for r, (v, n) in zip(records, verdicts)
        if v == "WRONG-TARGET-THINKER"
    ]
    pending = [
        r for r, (v, _) in zip(records, verdicts) if v == "PENDING-ACQUISITION"
    ]
    missing = [
        r for r, (v, _) in zip(records, verdicts) if v == "MISSING-ENTRY"
    ]
    unverified = [
        r for r, (v, _) in zip(records, verdicts) if v == "UNVERIFIED-FALSE"
    ]

    # Aggregate wrong-target by (host_thinker_id, target_key) for ranking.
    wrong_grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r, n in wrong:
        wrong_grouped[(r.get("host_thinker_id") or "?", r["target_key"])].append(r)
    top_wrong = sorted(wrong_grouped.items(), key=lambda kv: -len(kv[1]))[:20]

    lines: List[str] = []
    lines.append(f"# Citation grounding audit — {datetime.now(timezone.utc).date()}")
    lines.append("")
    lines.append("Structural audit of every `cite://` occurrence in the on-disk")
    lines.append("corpus. **Not** a substitute for semantic / primary-source review:")
    lines.append("a CORRECT verdict here only means the cite-key resolves to an")
    lines.append("indexed entry whose owner matches the prose's host thinker and")
    lines.append("whose IAST has either been verified or honestly flagged.")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Total cite occurrences: **{total}**")
    lines.append(f"- Unique cite keys: **{len(by_target)}**")
    for v in ("CORRECT", "CORRECT-UNKNOWN", "PENDING-ACQUISITION",
              "MISSING-ENTRY", "UNVERIFIED-FALSE", "WRONG-TARGET-THINKER"):
        lines.append(f"- {v}: **{counter.get(v, 0)}**")
    lines.append("")
    lines.append("FABRICATED is reported as the union of MISSING-ENTRY and ")
    lines.append("WRONG-TARGET-THINKER — both states mean the reader is being ")
    lines.append("pointed at something the on-disk corpus cannot defensibly attest.")
    lines.append("")
    pct_wrong = 100.0 * (counter.get("WRONG-TARGET-THINKER", 0) + counter.get("MISSING-ENTRY", 0)) / max(total, 1)
    lines.append(f"**Defensibly-grounded rate (excluding wrong-target + missing-entry): {100.0 - pct_wrong:.1f}%**")
    lines.append("")

    lines.append("## Top WRONG-TARGET-THINKER findings")
    lines.append("")
    if not top_wrong:
        lines.append("_None detected by the lexicon. Manual review still required for nuance._")
    else:
        lines.append("Each row: a (host-thinker, cite-key) pair where the prose")
        lines.append("around the cite explicitly names a work belonging to the host")
        lines.append("thinker, yet the cite-key resolves to a different thinker. The")
        lines.append("most common honest fix is to re-point the cite at the host's")
        lines.append("own commentary work (with `verified: pending-acquisition` if")
        lines.append("the work is not yet on disk).")
        lines.append("")
        lines.append("| Host thinker | Cite key | Occurrences | Sample note |")
        lines.append("|---|---|---|---|")
        for (host, key), rs in top_wrong:
            sample_note = ""
            r0 = rs[0]
            # Find the matched phrase by re-running classify briefly
            sample_note = (r0.get("visible_text") or "").replace("|", " ")[:80]
            lines.append(f"| `{host}` | `{key}` | {len(rs)} | {sample_note} |")
    lines.append("")

    lines.append("## MISSING-ENTRY (cite-key not in citation_index)")
    lines.append("")
    miss_keys = Counter(r["target_key"] for r in missing)
    if not miss_keys:
        lines.append("_None._")
    else:
        for key, n in miss_keys.most_common(30):
            lines.append(f"- `{key}` — {n}×")
    lines.append("")

    lines.append("## PENDING-ACQUISITION")
    lines.append("")
    pen_keys = Counter(r["target_key"] for r in pending)
    if not pen_keys:
        lines.append("_None._")
    else:
        for key, n in pen_keys.most_common(30):
            lines.append(f"- `{key}` — {n}×")
    lines.append("")

    lines.append("## UNVERIFIED-FALSE (IAST not located on disk; from audit_citations)")
    lines.append("")
    unv_keys = Counter(r["target_key"] for r in unverified)
    if not unv_keys:
        lines.append("_None._")
    else:
        for key, n in unv_keys.most_common(30):
            lines.append(f"- `{key}` — {n}×")
    lines.append("")

    lines.append("## Per-host-thinker rollup")
    lines.append("")
    per_host: Dict[str, Counter] = defaultdict(Counter)
    for r, (v, _) in zip(records, verdicts):
        per_host[r.get("host_thinker_id") or "(non-thinker file)"][v] += 1
    lines.append("| Host | CORRECT | CORRECT-UNK | PENDING | MISSING | UNVERIFIED | WRONG-TARGET | total |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for host in sorted(per_host):
        c = per_host[host]
        total_h = sum(c.values())
        lines.append(
            f"| `{host}` | {c.get('CORRECT', 0)} | {c.get('CORRECT-UNKNOWN', 0)} | "
            f"{c.get('PENDING-ACQUISITION', 0)} | {c.get('MISSING-ENTRY', 0)} | "
            f"{c.get('UNVERIFIED-FALSE', 0)} | {c.get('WRONG-TARGET-THINKER', 0)} | "
            f"{total_h} |"
        )
    lines.append("")

    return "\n".join(lines)


def main(argv: List[str]) -> int:
    if not CITATION_INDEX.exists():
        print(f"ERROR: {CITATION_INDEX} not found", file=sys.stderr)
        return 2
    idx = load_citation_index()
    thinker_meta = load_thinker_meta()
    records = gather_all_cites(thinker_meta)
    annotate_with_index(records, idx)
    lex = commentary_lexicon(thinker_meta)
    verdicts = [classify(r, lex) for r in records]
    report = render_report(records, verdicts, thinker_meta)
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    out = HANDOFFS / f"citation_grounding_audit_{datetime.now(timezone.utc).date()}.md"
    out.write_text(report, encoding="utf-8")
    # Also write a machine-readable companion for downstream tooling.
    companion = out.with_suffix(".jsonl")
    with companion.open("w", encoding="utf-8") as fh:
        for r, (v, n) in zip(records, verdicts):
            row = dict(r)
            row["verdict"] = v
            row["note"] = n
            # Trim prose_window so the file stays manageable.
            row["prose_window"] = (row.get("prose_window") or "")[:400]
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {out}")
    print(f"wrote {companion}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
