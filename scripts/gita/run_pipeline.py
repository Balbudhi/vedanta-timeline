#!/usr/bin/env python3
"""The Gītā pipeline driver (retired job-queue design; docs/history/gita/RUNBOOK.md). Every stage is idempotent; run it as
often as you like. Judgement jobs are done by agents through scripts/gita/queue.py; this script
does everything mechanical and creates the follow-up jobs.

    python3 scripts/gita/run_pipeline.py --stage A [--chapters 1-18] [--rebuild] [--workers 8] [--batch 12]
        packets, inventory, meaning pages, shard plan, translations files (once; --rebuild to redo);
        lexicon + lexicon-review jobs, --batch lemmas each (default 12)
    python3 scripts/gita/run_pipeline.py --stage B
        lexicon-fix / lexicon-rereview for 'revise'; when every batch is accepted: merge (table v3,
        installed into data/glossary/) and the verse jobs (chapter 12 only with --include-ch12)
    python3 scripts/gita/run_pipeline.py --stage C [--chapter N]
        expand every submitted verse output (cards, citations, derivations, builder report) into
        internal/sanskrit_reviews/gita/chN/ and queue its review, or its rereview after a fix
    python3 scripts/gita/run_pipeline.py --stage D [--chapter N]
        fix jobs for 'revise' verdicts (agent_ref = the producer); accepted lexicon requests merged;
        shards whose rows changed re-expanded and queued for rereview
    python3 scripts/gita/run_pipeline.py --stage E --chapters 2,3 [--no-whole-gita] [--no-deploy]
        for chapters whose shards are all accepted: builder packet, final expansion with the reviews'
        readers_will_meet, independent-review files, the builder with --check-only here; then
        scripts/deploy_gita_chapter.sh builds and commits them (+ the whole-Gītā article) in a clean
        worktree of origin/main. Nothing in this working tree's gita/, assets/ or manifest is written.
    python3 scripts/gita/run_pipeline.py --status

Acceptance run for one chapter (chapter 12 against its reviewed shards):

    python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage A   # lexicon jobs for ch12's lemmas only
    python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage B   # follow-ups; merge (never installed) + verse jobs
    python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage C   # expansion + review jobs
    python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage D   # fix / rereview
    python3 scripts/gita/run_pipeline.py --acceptance --chapter 12 --stage E   # builder check + comparison report

Everything of the acceptance run lives in internal/gita_pipeline/acceptance/ch12/ (jobs, outputs,
its own merged table, built shards, acceptance_report.json); its job ids start "acc12-" and
share the one queue, so the same workers serve it. The reviewed shards are never touched.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()

import build_jobs as BJ  # noqa: E402


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sh(cmd: list[str], check: bool = True) -> int:
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=str(C.ROOT))
    if check and r.returncode != 0:
        raise SystemExit(f"failed ({r.returncode}): {' '.join(cmd)}")
    return r.returncode


def jobs(state: str | None = None) -> list[dict]:
    out = []
    for st in ([state] if state else ["pending", "running", "done", "failed"]):
        for p in sorted((C.PIPE / "queue" / st).glob("*.json")):
            j = C.read_json(p)
            if C.in_namespace(j["id"]):
                j["_state"] = st
                out.append(j)
    return out


def output_of(j: dict | None) -> dict | None:
    if not j:
        return None
    try:
        return C.read_json(C.ROOT / j["output"])
    except (OSError, json.JSONDecodeError):
        return None


def latest_reviews(kinds: tuple[str, ...], key: str) -> dict[str, dict]:
    """key value (lexicon_job | verse_job) → the most recently created done job of those kinds."""
    best: dict[str, dict] = {}
    for j in jobs("done"):
        if j["type"] in kinds and j.get(key) and (j[key] not in best or j["created"] > best[j[key]]["created"]):
            best[j[key]] = j
    return best


def round_of(jid: str) -> int:
    m = re.search(r"-r(\d+)$", jid)
    return int(m.group(1)) if m else 0


def verse_path(vj: str) -> Path:
    return C.ns() / "out/verse" / f"{vj}.json"


def review_input(rid: str) -> dict:
    return C.read_json(C.ns() / "jobs/review" / f"{rid}.input.json")


def merge(install: bool) -> int:
    cmd = [sys.executable, "scripts/gita/merge_lexicon.py"]
    if C.NS is not None:
        cmd += ["--namespace", C.NS.name]
    elif install:
        cmd.append("--install")
    rc = sh(cmd, check=False)
    if rc != 0:
        route_conflicts()
    return rc


def route_conflicts() -> None:
    """Each merge conflict becomes a lexicon-fix of the later lexicon batch involved (agent_ref = the
    worker that wrote it) plus its rereview; a conflict between table rows or inline decisions only
    is reported for the lead."""
    q = BJ.queue_mod()
    rep = C.read_json(C.ns() / "lexicon/merge_report.json")
    lex = {j["id"]: j for j in jobs() if j["type"] == "lexicon"}
    by_batch: dict[str, list[dict]] = {}
    for c in rep.get("conflicts") or []:
        batches = sorted({lab.split()[1] for lab in (c.get("from") or {}).values() if lab.startswith("lexicon ")} |
                         {lab.split()[1] for lab in c.get("labels") or [] if lab.startswith("lexicon ")})
        if not batches:
            print("CONFLICT not routable to a lexicon batch (lead):", json.dumps(c, ensure_ascii=False))
            continue
        by_batch.setdefault(batches[-1], []).append(c)
    new = []
    for lj, cs in by_batch.items():
        num = re.search(r"lexicon-(\d+)$", lj).group(1)
        k = 1 + sum(1 for j in jobs() if j["type"] == "lexicon-fix" and j.get("lexicon_job") == lj)
        fid, rrid = f"{C.PREFIX}lexicon-fix-{num}-c{k}", f"{C.PREFIX}lexicon-rereview-{num}-c{k}"
        if q.find(fid):
            continue
        out = lex[lj]["output"] if lj in lex else C.rel(C.ns() / "out/lexicon" / f"{lj}.json")
        coll = C.ns() / "jobs/lexicon" / f"{fid}.collision.json"
        C.write_json(coll, {"schema": C.SCHEMA_LEXICON_REVIEW, "job": fid, "lexicon_job": lj,
                            "lexicon_sha256": C.sha256_file(C.ROOT / out), "verdict": "revise",
                            "findings": [{"lemma": (c.get("rows") or ["?"])[-1], "sense": c.get("id"), "severity": 1, "check": "distinctness",
                                          "says": f"{c['kind']}: {c.get('english') or c.get('id')} — rows {c.get('rows')} ({c.get('from')})",
                                          "should_be": "a distinct English word for this batch's sense (standard §7.6), or the same sense id "
                                                       "only if it is the same sense", "evidence": []} for c in cs]})
        new.append(BJ.job(fid, "lexicon-fix", "B", [out, C.rel(coll)], out, agent_ref=(lex.get(lj) or {}).get("claimed_by"), lexicon_job=lj))
        new.append(BJ.job(rrid, "lexicon-rereview", "B", [out, C.rel(coll)], C.rel(C.ns() / "out/lexicon-rereview" / f"{rrid}.json"),
                          deps=[fid], lexicon_job=lj))
    if new:
        print(json.dumps({"collisions routed to lexicon-fix": BJ.add_jobs(new)}))


def requested_lemmas() -> list[dict]:
    """Lemmas lexicon agents (top-level lexicon_requests) and verse agents (requests without a
    proposed entry) asked to have decided in a lexicon job."""
    out = []
    for j in jobs("done"):
        o = output_of(j)
        if not o:
            continue
        if j["type"] in ("lexicon", "lexicon-fix"):
            out += [{**r, "from": j["id"]} for r in o.get("lexicon_requests") or [] if isinstance(r, dict)]
        elif j["type"] in ("verse", "fix"):
            from gitapipe import lexicon as L
            out += [{**r, "from": j["id"]} for r in o.get("lexicon_requests") or [] if isinstance(r, dict) and L.request_entry(r) is None]
    from gitapipe import lexicon as L
    for e in L.inline_entries(L.accepted_verse_outputs()):
        if e["divergent"]:     # one lemma, different English in different shards: the lexicon decides it
            out.append({"lemma": e["lemma"], "from": ", ".join(e["inline_from"]),
                        "why": "decided inline with different English: " + "; ".join(
                            f"'{list(s['forms'].values())[0]}' at {', '.join(s['occurrences'])}" for s in e["senses"])})
    return out


# ---------------------------------------------------------------- stages
def stage_a(a) -> None:
    if a.rebuild or not (C.PIPE / "packets/manifest.json").is_file():
        cmd = [sys.executable, "scripts/gita/build_all_packets.py"] + (["--chapters", a.chapters] if a.chapters else []) + \
              (["--workers", str(a.workers)] if a.workers else [])
        sh(cmd)
    else:
        print("packets exist (manifest present); --rebuild to rebuild")
    lj = BJ.lexicon_jobs(a.batch, chapter=a.chapter if a.acceptance else None)
    print(json.dumps({"lexicon jobs": sum(1 for j in lj if j["type"] == "lexicon"), **BJ.add_jobs(lj)}))


def stage_b(a) -> None:
    from gitapipe import lexicon as L
    q = BJ.queue_mod()
    new = []
    lex_jobs = {j["id"]: j for j in jobs() if j["type"] == "lexicon"}
    for lj, rj in latest_reviews(("lexicon-review", "lexicon-rereview"), "lexicon_job").items():
        r = output_of(rj)
        lout = C.ROOT / lex_jobs.get(lj, {}).get("output", C.rel(C.ns() / "out/lexicon" / f"{lj}.json"))
        if not r or r.get("verdict") != "revise" or not lout.is_file() or r.get("lexicon_sha256") != C.sha256_file(lout):
            continue
        k = round_of(rj["id"]) + 1
        num = re.search(r"lexicon-(\d+)$", lj).group(1)
        fid, rrid = f"{C.PREFIX}lexicon-fix-{num}-r{k}", f"{C.PREFIX}lexicon-rereview-{num}-r{k}"
        if q.find(fid):
            continue
        snap = C.ns() / "jobs/lexicon" / f"{lj}.reviewed-r{k}.json"
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_bytes(lout.read_bytes())
        out = C.rel(lout)
        new.append(BJ.job(fid, "lexicon-fix", "B", [out, rj["output"]], out, agent_ref=lex_jobs.get(lj, {}).get("claimed_by"), lexicon_job=lj))
        new.append(BJ.job(rrid, "lexicon-rereview", "B", [out, C.rel(snap), rj["output"]],
                          C.rel(C.ns() / "out/lexicon-rereview" / f"{rrid}.json"), deps=[fid], lexicon_job=lj))
    print(json.dumps({"lexicon follow-ups": BJ.add_jobs(new)}))
    req = BJ.requested_lexicon_jobs(requested_lemmas(), a.batch)
    if req:
        print(json.dumps({"lexicon jobs for requested lemmas": BJ.add_jobs(req)}))
    accepted = {lx.get("job") for _, lx, _ in L.accepted_lexicon_outputs()}
    open_jobs = [j["id"] for j in jobs() if j["type"].startswith("lexicon") and j["_state"] in ("pending", "running", "failed")]
    print(json.dumps({"lexicon batches": len(lex_jobs), "accepted": len(accepted & set(lex_jobs)), "open lexicon jobs": len(open_jobs)}))
    if lex_jobs and set(lex_jobs) <= accepted and not open_jobs:
        if merge(install=True) != 0:
            print("STOP: the merge refused (see CONFLICT lines); route each to a lexicon-fix of the later batch")
            return
        if a.acceptance:
            chs = [a.chapter]
        else:
            chs = [c for c in C.VERSE_COUNTS if a.include_ch12 or c != 12]
        print(json.dumps({"verse jobs": BJ.add_jobs(BJ.verse_jobs(chs))}))


def shard_target(vo: dict) -> Path:
    loci = [v["locus"] for v in vo["verses"]]
    ch = int(loci[0].split(".")[0])
    rng = f"{int(loci[0].split('.')[1]):02d}-{int(loci[-1].split('.')[1]):02d}"
    base = (C.NS / "build" / f"ch{ch}") if C.NS is not None else (C.ROOT / f"internal/sanskrit_reviews/gita/ch{ch}")
    return base / f"producer-{rng}.json"


def ours(p: Path) -> bool:
    if not p.is_file():
        return True
    try:
        return C.read_json(p).get("generated_by") == "scripts/gita/expand_cards.py"
    except (OSError, json.JSONDecodeError):
        return False


def expand(vjob: str, review_out: str | None = None) -> tuple[str, str, dict] | None:
    import expand_cards
    vpath = verse_path(vjob)
    vo = C.read_json(vpath)
    target = shard_target(vo)
    if not ours(target):
        print(f"REFUSED: {C.rel(target)} was not written by this pipeline (reviewed shards are never overwritten)")
        return None
    out, rep = expand_cards.expand(vpath, target, C.ROOT / review_out if review_out else None)
    return C.rel(out), C.rel(out.with_name(out.name.replace("producer-", "expand-").replace(".json", ".report.json"))), rep


def stage_c(a) -> None:
    new = []
    done_verse = {j.get("verse_job") or j["id"] for j in jobs("done") if j["type"] in ("verse", "fix")}
    reviews: dict[str, list[dict]] = {}
    for j in jobs():
        if j["type"] in ("review", "rereview"):
            reviews.setdefault(j["verse_job"], []).append(j)
    for vj in sorted(done_verse):
        if a.chapter and C.chapter_of_job(vj) != a.chapter:
            continue
        vpath = verse_path(vj)
        if not vpath.is_file():
            continue
        sha = C.sha256_file(vpath)
        rs = sorted(reviews.get(vj, []), key=lambda j: j["created"])
        if rs and review_input(rs[-1]["id"])["verse_output_sha256"] == sha:
            continue                                   # this version is already queued or reviewed
        res = expand(vj)
        if res is None:
            continue
        shard, report, rep = res
        if rep["errors"]:
            print(f"{vj}: expansion/builder errors ({len(rep['errors'])}) — see {report}; the reviewer reads them")
        if not rs:
            new.append(BJ.review_job(vj, 0, shard, report))
        else:
            last = rs[-1]
            new.append(BJ.review_job(vj, round_of(last["id"]) + 1, shard, report, prev_review=last["output"],
                                     reviewed_snapshot=review_input(last["id"])["frozen_copy"]))
    print(json.dumps({"reviews": BJ.add_jobs(new)}))


def stage_d(a) -> None:
    q = BJ.queue_mod()
    new = []
    producers = {j["id"]: j.get("claimed_by") for j in jobs() if j["type"] == "verse"}
    for vj, rj in latest_reviews(("review", "rereview"), "verse_job").items():
        if a.chapter and C.chapter_of_job(vj) != a.chapter:
            continue
        r = output_of(rj)
        vpath = verse_path(vj)
        if not r or r.get("verdict") != "revise" or not vpath.is_file() or r.get("shard_sha256") != C.sha256_file(vpath):
            continue
        fid = vj.replace("verse-", "fix-") + f"-r{round_of(rj['id']) + 1}"
        if q.find(fid):
            continue
        new.append(BJ.job(fid, "fix", "D", [C.rel(vpath), rj["output"], *[C.rel(C.packet_path(v["locus"])) for v in C.read_json(vpath)["verses"]]],
                          C.rel(vpath), agent_ref=producers.get(vj), verse_job=vj))
    print(json.dumps({"fix jobs": BJ.add_jobs(new)}))
    req = BJ.requested_lexicon_jobs(requested_lemmas(), a.batch)
    if req:
        print(json.dumps({"lexicon jobs for requested lemmas": BJ.add_jobs(req)}))
    from gitapipe import lexicon as L
    reqs = L.accepted_requests()
    inline = L.accepted_verse_outputs()
    rep_p = C.ns() / "lexicon/merge_report.json"
    merged = set(C.read_json(rep_p).get("inputs", [])) if rep_p.is_file() else set()
    if any(f"request {j}" not in merged for j, _ in reqs) or any(
            not any(lab.startswith("inline") and j in lab for lab in merged) for j, vo in inline
            if any(w.get("sense") is None and w.get("meaning_lines") for v in vo.get("verses") or [] for w in v.get("words") or [])):
        if merge(install=True) != 0:
            print("STOP: merging the accepted lexicon requests refused (CONFLICT lines above)")
            return
        for vj, rows in rows_changed().items():
            res = expand(vj)
            rs = sorted((j for j in jobs() if j["type"] in ("review", "rereview") and j.get("verse_job") == vj), key=lambda j: j["created"])
            if res and rs:
                last = rs[-1]
                jb = BJ.review_job(vj, round_of(last["id"]) + 1, res[0], res[1], prev_review=last["output"],
                                   reviewed_snapshot=review_input(last["id"])["frozen_copy"])
                jb["note"] = f"lexicon rows changed: {rows}"
                print(json.dumps({vj: BJ.add_jobs([jb])}))


def rows_changed() -> dict[str, list[str]]:
    b = C.import_builder()
    pol = b.load_policy(C.current_policy_path())
    out = {}
    for p in sorted((C.ns() / "out/verse").glob("*.json")):
        vo = C.read_json(p)
        t = shard_target(vo)
        if not t.is_file() or not ours(t):
            continue
        used = C.read_json(t).get("rows_used") or {}
        ch = [r for r, h in used.items() if r not in pol.rows or C.canon_hash(pol.rows[r].raw) != h]
        if ch:
            out[vo["job"]] = ch
    return out


def prepare_chapter(ch: int) -> tuple[list[dict], Path] | None:
    """Final expansion (with the reviews' readers_will_meet) and the independent-review files for a
    chapter whose shards all carry an accepted review at their current version."""
    plan = C.read_json(C.PIPE / "packets/shard_plan.json")["chapters"].get(str(ch), [])
    latest = latest_reviews(("review", "rereview"), "verse_job")
    missing = []
    for s in plan:
        vj = f"{C.PREFIX}verse-{s['id']}"
        r = output_of(latest.get(vj))
        if not (r and r.get("verdict") == "accept" and verse_path(vj).is_file() and r.get("shard_sha256") == C.sha256_file(verse_path(vj))):
            missing.append(vj)
    if missing:
        print(f"chapter {ch} not ready: shards without an accepted review at their current version: {missing}")
        return None
    chdir = (C.NS / "build" / f"ch{ch}") if C.NS is not None else C.ROOT / f"internal/sanskrit_reviews/gita/ch{ch}"
    chdir.mkdir(parents=True, exist_ok=True)
    reviewed_packet = C.ROOT / f"internal/sanskrit_reviews/gita/ch{ch}/packet.json"
    if not reviewed_packet.is_file():
        sh([sys.executable, "scripts/build_gita_chapter_packet.py", str(ch)], check=False)
        if not reviewed_packet.is_file():
            raise SystemExit(f"the builder's chapter packet {C.rel(reviewed_packet)} could not be built")
    if C.NS is not None:
        shutil.copyfile(reviewed_packet, chdir / "packet.json")
    stale = rows_changed()
    for s in plan:
        vj = f"{C.PREFIX}verse-{s['id']}"
        if vj in stale:
            raise SystemExit(f"{vj}: rows {stale[vj]} changed after its review; run --stage D (rereview) first")
        rj = latest[vj]
        res = expand(vj, review_out=rj["output"])
        if res is None:
            raise SystemExit(f"{vj}: cannot write its shard")
        shard = C.ROOT / res[0]
        r = output_of(rj)
        C.write_json(shard.with_name(shard.name.replace("producer-", "independent-review-")), {
            "schema_version": "independent-sanskrit-review-v2", "converted_from": rj["output"], "review_job": rj["id"],
            "shard": shard.name, "producer_sha256": C.sha256_file(shard), "verse_output_sha256": r["shard_sha256"],
            "complete": True, "verdict": r["verdict"], "date": now(),
            "findings": [{**f, "status": f.get("status", "open")} for f in r.get("findings") or []],
            "blind_secondary_check": "in the private review file"})
    return plan, chdir


def stage_e(a) -> None:
    chapters = [a.chapter] if a.chapter else (C.parse_chapters(a.chapters) if a.chapters else None)
    if not chapters:
        raise SystemExit("--stage E needs --chapter N or --chapters LIST")
    if a.acceptance:
        acceptance_report(a.chapter)
        return
    ready = []
    for ch in chapters:
        if prepare_chapter(ch) is None:
            continue
        sh([sys.executable, "scripts/build_gita_chapter_reader.py", str(ch), "--check-only"])
        ready.append(ch)
    if not ready:
        return
    if a.no_deploy:
        print(f"checked {ready}; deploy with: sh scripts/deploy_gita_chapter.sh \"{' '.join(map(str, ready))}\" MESSAGE --whole-gita")
        return
    h = subprocess.run([sys.executable, "scripts/build_gita_chapter_reader.py", "--policy-hash"], cwd=C.ROOT,
                       capture_output=True, text=True).stdout.strip()[:12]
    label = ", ".join(map(str, ready))
    cmd = ["sh", "scripts/deploy_gita_chapter.sh", " ".join(map(str, ready)),
           f"Gītā {label}: readers from reviewed shards (policy {h})"] + ([] if a.no_whole_gita else ["--whole-gita"])
    sh(cmd)


# ---------------------------------------------------------------- the acceptance report
def acceptance_report(ch: int) -> None:
    import convert_ch12 as CV
    prep = prepare_chapter(ch)
    if prep is None:
        return
    plan, chdir = prep
    b = C.import_builder()
    ctx = b.Ctx(chapter=ch, chapter_dir=chdir, policy_path=C.current_policy_path(), complete=True)
    try:
        result = b.run(ctx)
    except b.BuildError as e:
        result = {"fallbacks": None, "public": []}
        ctx.report.err("BUILD", str(e))
    reviewed = {v["locus"]: v for sp in sorted((C.ROOT / f"internal/sanskrit_reviews/gita/ch{ch}").glob("producer-*.json"))
                if not ours(sp) for v in C.read_json(sp)["verses"]}
    built = {v["locus"]: v for sp in sorted(chdir.glob("producer-*.json")) for v in C.read_json(sp)["verses"]}
    lines, eq, n, same_split = [], collections.Counter(), 0, 0
    for loc in sorted(reviewed, key=C.locus_sort_key):
        r, x = reviewed[loc], built.get(loc)
        if not x:
            lines.append({"locus": loc, "missing": True})
            continue
        strip = lambda s: b.SLOT_RE.sub(lambda m: m.group(2), s or "")  # noqa: E731
        ra, xa = strip(r["english"]), strip(x["english"])
        lines.append({"locus": loc, "identical": ra == xa, "reviewed": ra, "acceptance": xa,
                      "diff": " ".join(t for t in difflib.ndiff(ra.split(), xa.split()) if t[:1] in "+-")})
        if [w["iast"] for w in r["words"]] == [w["iast"] for w in x["words"]]:
            same_split += 1
            for w, y in zip(r["words"], x["words"]):
                n += 1
                for f in CV.IDENTITY:
                    eq[f] += CV.get(w, f) == CV.get(y, f)
    cards = sum(len(v["words"]) for v in built.values())
    first, all_rounds = collections.Counter(), collections.Counter()
    for j in jobs("done"):
        if j["type"] in ("review", "rereview") and C.chapter_of_job(j["id"]) == ch:
            for f in (output_of(j) or {}).get("findings") or []:
                k = f"S{f.get('severity')}"
                all_rounds[k] += 1
                if j["type"] == "review":
                    first[k] += 1
    per100 = lambda c: {k: round(v * 100 / cards, 1) for k, v in sorted(c.items())} if cards else {}  # noqa: E731
    mr = C.ns() / "lexicon/merge_report.json"
    rep = {"chapter": ch, "namespace": C.rel(C.NS), "date": now(), "policy": C.rel(C.current_policy_path()),
           "builder": {"errors_by_check": ctx.report.counts(), "errors": [f"{c} {m}" for c, m, _ in ctx.report.errors][:80],
                       "fallbacks": result.get("fallbacks"), "complete_mode": True},
           "lines": {"identical": sum(1 for l in lines if l.get("identical")), "verses": len(reviewed), "per_verse": lines},
           "cards": {"acceptance": cards, "reviewed": sum(len(v["words"]) for v in reviewed.values()),
                     "verses_with_the_same_pada_split": f"{same_split}/{len(reviewed)}",
                     "field_agreement_on_those": {f: f"{eq[f]}/{n}" for f in CV.IDENTITY}},
           "findings_per_100_cards": {"first_round": per100(first), "all_rounds": per100(all_rounds),
                                      "targets": "≤ 10 findings and ≤ 1 S1 per 100 cards (audit §4.8)"},
           "lexicon": {k: v for k, v in (C.read_json(mr) if mr.is_file() else {}).items()
                       if k in ("policy_sha256", "added_senses", "changed_legacy", "conflicts")}}
    C.write_json(C.NS / "acceptance_report.json", rep)
    print(json.dumps({k: rep[k] for k in ("builder", "cards", "findings_per_100_cards")} | {"lines identical": f"{rep['lines']['identical']}/{rep['lines']['verses']}"},
                     ensure_ascii=False, indent=1)[:4000])
    print(f"written {C.rel(C.NS / 'acceptance_report.json')}")


def status() -> None:
    q = BJ.queue_mod()
    table: dict[str, dict[str, int]] = {}
    for j in jobs():
        table.setdefault(j["type"], {s: 0 for s in ("pending", "running", "done", "failed")})[j["_state"]] += 1
    ready = [j["id"] for j in jobs("pending") if all(q.find(d) and q.find(d)[0] == "done" for d in j.get("depends_on", []))]
    m = C.PIPE / "packets/manifest.json"
    print(json.dumps({"namespace": C.rel(C.NS) if C.NS else "main", "jobs": table, "judgement jobs ready": len(ready),
                      "next ready": ready[:10], "stage A": C.read_json(m).get("timings_s") if m.is_file() else "not run",
                      "policy": C.rel(C.current_policy_path())}, ensure_ascii=False, indent=1))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=list("ABCDE"))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--chapters")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--batch", type=int, default=12, help="lemmas per lexicon job (default 12)")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--include-ch12", action="store_true")
    ap.add_argument("--acceptance", action="store_true", help="the acceptance run of --chapter N (its own namespace)")
    ap.add_argument("--no-deploy", action="store_true")
    ap.add_argument("--no-whole-gita", action="store_true")
    a = ap.parse_args(argv)
    if a.acceptance:
        if not a.chapter:
            ap.error("--acceptance needs --chapter N")
        C.set_namespace(f"ch{a.chapter}")
    if a.status or not a.stage:
        status()
        return 0
    {"A": stage_a, "B": stage_b, "C": stage_c, "D": stage_d, "E": stage_e}[a.stage](a)
    status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
