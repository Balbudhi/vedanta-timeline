#!/usr/bin/env python3
"""Create queue jobs from the stage-A products (idempotent: a job id already in the queue is kept).

    python3 scripts/gita/build_jobs.py lexicon [--batch 8]        # lexicon + lexicon-review jobs (stage A)
    python3 scripts/gita/build_jobs.py verse [--chapters 2,12]    # verse jobs from the shard plan (stage B, after the merge)
    python3 scripts/gita/build_jobs.py review VERSE_JOB           # the review (or rereview) of an expanded shard (stage C)

Job records follow scripts/gita/queue.py: {id, type, stage, brief, inputs, output, validate,
depends_on, agent_ref}. Inputs are self-contained files under internal/gita_pipeline/jobs/.
Lexicon batches: inventory lemmas in scope, grouped by table row, system terms and high weight
first, about eight lemmas per job. Verse jobs: the shard plan (sentence units, about 60 cards).
Review jobs carry the private translations file; their outputs are under private/ (git-ignored).
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()


def queue_mod():
    spec = importlib.util.spec_from_file_location("gita_queue", C.GITA_SCRIPTS / "queue.py")
    q = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(q)
    q.QUEUE = C.PIPE / "queue"
    return q


def add_jobs(jobs: list[dict]) -> dict:
    q = queue_mod()
    q.ensure()
    added = kept = 0
    for j in jobs:
        if q.find(j["id"]):
            kept += 1
            continue
        j.setdefault("depends_on", [])
        j.setdefault("attempts", 0)
        j.setdefault("claimed_by", None)
        j.setdefault("agent_ref", None)
        j.setdefault("log", [])
        j["created"] = q.now()
        q.save(q.QUEUE / "pending" / f"{j['id']}.json", j)
        added += 1
    return {"added": added, "already_present": kept}


def validate_cmd(kind: str, out: str) -> str:
    return f"python3 scripts/gita/validate_job.py {kind} {out}"


def job(jid: str, kind: str, stage: str, inputs: list[str], output: str, deps=(), **extra) -> dict:
    return {"id": jid, "type": kind, "stage": stage, "brief": C.BRIEFS[kind], "inputs": inputs, "output": output,
            "validate": validate_cmd(kind, output), "depends_on": list(deps), **extra}


# ---------------------------------------------------------------- stage A → B
def lexicon_jobs(batch: int = 12, chapter: int | None = None) -> list[dict]:
    """chapter: only the in-scope lemmas that occur in that chapter (the acceptance run)."""
    inv = C.read_json(C.PIPE / "packets/inventory.json")
    pol_path = C.current_policy_path()
    pol = C.read_json(pol_path)
    rows = pol.get("lemmas") or pol.get("terms") or {}
    groups: dict[str, list[dict]] = {}
    for e in inv["lemmas"]:
        if e["in_lexicon_scope"] and (chapter is None or any(v.startswith(f"{chapter}.") for v in e["verses"])):
            groups.setdefault(e["rows"][0] if e["rows"] else e["key"], []).append(e)
    order = sorted(groups.values(), key=lambda g: (not any(x["system"] for x in g), -max(x["weight"] for x in g), g[0]["lemma"]))
    batches, cur = [], []
    for g in order:
        if cur and len(cur) + len(g) > batch:
            batches.append(cur)
            cur = []
        cur += g
    if cur:
        batches.append(cur)
    return make_lexicon_jobs(batches, 1, pol_path, pol, inv.get("policy_sha256"))


def existing_lexicon_lemmas() -> tuple[set[str], int]:
    """Lemmas already given to a lexicon job of this namespace, and the highest job number."""
    seen, top = set(), 0
    for p in (C.ns() / "jobs/lexicon").glob("*.input.json"):
        d = C.read_json(p)
        top = max(top, int(re.search(r"lexicon-(\d+)", d["job"]).group(1)))
        seen |= {C.nfc(x["lemma"]) for x in d.get("lemmas") or []}
    return seen, top


def requested_lexicon_jobs(requests: list[dict], batch: int = 12) -> list[dict]:
    """Lexicon jobs for lemmas a lexicon or verse agent requested ({lemma, why, from}) that no job has yet."""
    inv = C.read_json(C.PIPE / "packets/inventory.json")
    by = {C.nfc(e["lemma"]): e for e in inv["lemmas"]}
    by_key = {C.latin_key(e["lemma"]): e for e in inv["lemmas"]}
    seen, top = existing_lexicon_lemmas()
    todo, done = [], set()
    for r in requests:
        lem = C.nfc(r.get("lemma") or "")
        if not lem or lem in seen or lem in done:
            continue
        done.add(lem)
        e = by.get(lem) or by_key.get(C.latin_key(lem))
        e = dict(e) if e else {"key": lem, "lemma": lem, "roots": [], "forms": [], "verses": [], "occurrences": [], "frequency": 0,
                               "weight": 0, "rows": [], "glossary_key": None, "prior_renderings": [], "meaning_page": ""}
        e["requested"] = {"why": r.get("why") or r.get("reason"), "from": r.get("from")}
        todo.append(e)
    batches = [todo[k:k + batch] for k in range(0, len(todo), batch)]
    pol_path = C.current_policy_path()
    return make_lexicon_jobs(batches, top + 1, pol_path, C.read_json(pol_path), inv.get("policy_sha256"))


def make_lexicon_jobs(batches: list[list[dict]], start: int, pol_path, pol: dict, inv_sha) -> list[dict]:
    rows = pol.get("lemmas") or pol.get("terms") or {}
    jobs = []
    for k, b in enumerate(batches, start):
        jid = f"{C.PREFIX}lexicon-{k:04d}"
        inp = C.ns() / "jobs/lexicon" / f"{jid}.input.json"
        lemmas = []
        for e in b:
            lemmas.append({"lemma": e["lemma"], "roots": e["roots"], "forms": e["forms"], "verses": e["verses"],
                           "occurrences": [o["at"] for o in e["occurrences"]], "frequency": e["frequency"], "weight": e["weight"],
                           "rows": e["rows"], "existing_rows": {r: rows[r] for r in e["rows"] if r in rows},
                           "glossary_key": e["glossary_key"], "prior_renderings": e["prior_renderings"], "meaning_page": e["meaning_page"],
                           **({"requested": e["requested"]} if e.get("requested") else {})})
        C.write_json(inp, {"job": jid, "lemmas": lemmas, "policy": C.rel(pol_path), "policy_sha256": inv_sha,
                           "reserved_english": pol.get("reserved_english") or {},
                           "note": "Decide each lemma once for the whole Gītā. An inventory lemma that only a wrong analysis "
                                   "produced gets an entry {lemma, skip: reason}."})
        pages = [e["meaning_page"] for e in b if e["meaning_page"] and (C.ROOT / e["meaning_page"]).is_file()]
        out = C.rel(C.ns() / "out/lexicon" / f"{jid}.json")
        jobs.append(job(jid, "lexicon", "B", [C.rel(inp), *pages, C.rel(pol_path)], out))
        rid = f"{C.PREFIX}lexicon-review-{k:04d}"
        jobs.append(job(rid, "lexicon-review", "B", [out, C.rel(inp), *pages, C.rel(pol_path)],
                        C.rel(C.ns() / "out/lexicon-review" / f"{rid}.json"), deps=[jid], lexicon_job=jid))
    return jobs


# ---------------------------------------------------------------- stage B → C
def fairness(ch: int, loci: list[str]) -> dict:
    b = C.import_builder()
    return {"verses_needing_a_fork": sorted(set(loci) & b.REQUIRED_FORK_VERSES.get(ch, set()), key=C.locus_sort_key),
            "words_needing_a_fork": [{"locus": l, "word_starts": k} for l, k in b.FAIRNESS_WORDS.get(ch, []) if l in loci]}


def verse_jobs(chapters: list[int] | None = None) -> list[dict]:
    plan = C.read_json(C.PIPE / "packets/shard_plan.json")
    inv = C.read_json(C.PIPE / "packets/inventory.json")
    pol_path = C.current_policy_path()
    by_verse: dict[str, set] = {}
    for e in inv["lemmas"]:
        for v in e["verses"]:
            by_verse.setdefault(v, set()).add(e["rows"][0] if e["rows"] else e["lemma"])
    jobs = []
    for ch_s, shards in plan["chapters"].items():
        ch = int(ch_s)
        if chapters and ch not in chapters:
            continue
        for sh in shards:
            jid = f"{C.PREFIX}verse-{sh['id']}"
            inp = C.ns() / "jobs/verse" / f"{jid}.input.json"
            lem = sorted(set().union(*(by_verse.get(v, set()) for v in sh["verses"])))
            C.write_json(inp, {"job": jid, "chapter": ch, "verses": sh["verses"], "range": sh["range"],
                               "cards_estimate": sh["cards_estimate"], "sentence_units": sh["units"],
                               "packets": [C.rel(C.packet_path(v)) for v in sh["verses"]],
                               "lexicon": C.rel(pol_path), "lexicon_rows_and_lemmas": lem, "fairness": fairness(ch, sh["verses"]),
                               "policy_sha256": C.import_builder().load_policy(pol_path).sha256})
            jobs.append(job(jid, "verse", "C", [C.rel(inp), *[C.rel(C.packet_path(v)) for v in sh["verses"]], C.rel(pol_path)],
                            C.rel(C.ns() / "out/verse" / f"{jid}.json"), chapter=ch, range=sh["range"]))
    return jobs


# ---------------------------------------------------------------- stage C → D
def review_job(verse_job: str, round_: int, shard: str, report: str, prev_review: str | None = None,
               reviewed_snapshot: str | None = None) -> dict:
    ch = C.chapter_of_job(verse_job)
    vout = C.rel(C.ns() / "out/verse" / f"{verse_job}.json")
    kind = "review" if round_ == 0 else "rereview"
    rid = verse_job.replace("verse-", f"{kind}-") + (f"-r{round_}" if round_ else "")
    snap = C.ns() / "private/snapshots" / f"{rid}.verse.json"
    snap.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(C.ROOT / vout, snap)
    inp = C.ns() / "jobs/review" / f"{rid}.input.json"
    vo = C.read_json(C.ROOT / vout)
    C.write_json(inp, {"job": rid, "verse_job": verse_job, "verse_output": vout, "verse_output_sha256": C.sha256_file(C.ROOT / vout),
                       "frozen_copy": C.rel(snap), "expanded_shard": shard, "expansion_report": report,
                       "packets": [C.rel(C.packet_path(v["locus"])) for v in vo.get("verses") or []],
                       "secondaries": f"internal/gita_pipeline/secondaries/{ch}.json",
                       "previous_review": prev_review, "shard_as_reviewed": reviewed_snapshot,
                       "fairness": fairness(ch, [v["locus"] for v in vo.get("verses") or []]),
                       "note": "Open the secondaries only after checks 1–7 are written (REVIEW_BRIEF)."})
    inputs = [C.rel(inp), vout, shard, report, f"internal/gita_pipeline/secondaries/{ch}.json"] + \
             ([prev_review] if prev_review else []) + ([reviewed_snapshot] if reviewed_snapshot else [])
    return job(rid, kind, "D", inputs, C.rel(C.ns() / "private/out" / kind / f"{rid}.json"), verse_job=verse_job,
               created_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=("lexicon", "verse"))
    ap.add_argument("--batch", type=int, default=12, help="lemmas per lexicon job (default 12)")
    ap.add_argument("--chapters")
    a = ap.parse_args(argv)
    jobs = lexicon_jobs(a.batch) if a.what == "lexicon" else verse_jobs(C.parse_chapters(a.chapters) if a.chapters else None)
    print(json.dumps({"jobs": len(jobs), **add_jobs(jobs)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
