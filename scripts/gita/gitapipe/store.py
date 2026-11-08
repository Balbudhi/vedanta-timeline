"""The analysis store: every Analysis the oracle returned (whole, as the oracle gave it) and its
Derivation, keyed by the oracle's analysis id and deduplicated across the Gītā
(`internal/gita_pipeline/packets/analyses.sqlite`). Verse packets carry one-line summaries;
the expander and the validators read the full records here.

Derivation steps are stored compactly ({sutra, result, source, ashtadhyayi}); the Aṣṭādhyāyī
text of a step is re-read from its line by the expander, never stored twice."""
from __future__ import annotations

import json
import sqlite3
import zlib
from pathlib import Path

from . import common as C
from . import names as N


def store_path() -> Path:
    return C.PIPE / "packets/analyses.sqlite"


def compact_derivation(d: dict | None) -> dict | None:
    if not isinstance(d, dict):
        return None
    out = {k: d.get(k) for k in ("analysis_id", "form_expected", "form_derived", "matches", "alternatives", "engine", "error", "scope")
           if d.get(k) is not None}
    out["steps"] = [{"sutra": s.get("sutra"), "result": s.get("result"), "source": s.get("source"),
                     "ashtadhyayi": s.get("ashtadhyayi")} for s in d.get("steps") or []]
    if d.get("final_member_derivation"):
        out["final_member_derivation"] = compact_derivation(d["final_member_derivation"])
    return out


def summary(a: dict) -> dict:
    """One-line view of an Analysis for the verse packet (no field is chosen or dropped from the store)."""
    d = a.get("dhatu") or {}
    root = None
    if d.get("root"):
        root = f"√{d['root']} {d.get('gana_name') or ''} {d.get('gana') or ''} {d.get('pada') or ''}".strip()
        if d.get("upasargas"):
            root += " + " + "-".join(u for u in d["upasargas"] if isinstance(u, str))
        if d.get("sanadi"):
            root += " + " + "-".join(str(x) for x in d["sanadi"])
    gram = " ".join(str(x) for x in (a.get("lakara"), a.get("purusha"), a.get("vibhakti"), a.get("vacana"), a.get("linga"),
                                     a.get("pada") if a.get("kind") == "tinanta" else None, a.get("prayoga") if a.get("prayoga") not in (None, "kartari") else None)
                    if x)
    der = a.get("derivation") or {}
    return {"id": a["id"], "kind": a.get("kind"), "stem": a.get("stem"), "root": root, "gram": gram or None,
            "krt": a.get("krt"), "taddhita": a.get("taddhita"), "members": [m if isinstance(m, str) else (m or {}).get("form") or (m or {}).get("stem")
                                                                             for m in a.get("members") or []] or None,
            "word_class": N.word_class(a), "source": a.get("source"), "derives": der.get("matches")}


class Store:
    def __init__(self, path: Path | None = None, write: bool = False) -> None:
        self.path = Path(path or store_path())
        if not write and not self.path.is_file():
            raise FileNotFoundError(f"analysis store {self.path} missing: run stage A")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.con = sqlite3.connect(str(self.path), timeout=60)
        if write:
            self.con.execute("pragma journal_mode=wal")
            self.con.execute("create table if not exists analyses (id text primary key, form text, analysis blob, derivation blob)")
        self._cache: dict[str, tuple[dict, dict | None]] = {}

    def put_many(self, rows: list[tuple[str, str, dict, dict | None]]) -> int:
        cur = self.con.executemany(
            "insert or replace into analyses values (?,?,?,?)",
            [(i, f, zlib.compress(json.dumps(a, ensure_ascii=False).encode()),
              zlib.compress(json.dumps(d, ensure_ascii=False).encode()) if d is not None else None) for i, f, a, d in rows])
        self.con.commit()
        return cur.rowcount

    def get(self, aid: str) -> tuple[dict, dict | None] | None:
        if aid in self._cache:
            return self._cache[aid]
        r = self.con.execute("select analysis, derivation from analyses where id=?", (aid,)).fetchone()
        if r is None:
            return None
        val = (json.loads(zlib.decompress(r[0])), json.loads(zlib.decompress(r[1])) if r[1] else None)
        self._cache[aid] = val
        return val

    def count(self) -> int:
        return self.con.execute("select count(*) from analyses").fetchone()[0]
