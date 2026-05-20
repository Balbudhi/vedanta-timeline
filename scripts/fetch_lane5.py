#!/usr/bin/env python3
"""Lane 5 per-file external fetcher.

Strict policy:
- Per-URL fetches only — NO bulk mirrors.
- 1 req/sec throttle per host.
- Hard total-bytes cap (default 300 MB) — abort further fetches if exceeded.
- Each fetch produces a manifest entry: slug, source, url, format, license,
  sha256, size_kb, fetch_status, engaged_works_match.

Usage:
    python3 scripts/fetch_lane5.py fetch <plan.json>
    python3 scripts/fetch_lane5.py merge   (writes data/external_ingest_manifest_lane5.json)
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "external_ingest_manifest_lane5.json"
HARD_CAP_BYTES = 300 * 1024 * 1024  # 300 MB
LAST_HIT: dict[str, float] = {}


def throttle(host: str, gap: float = 1.05) -> None:
    """1 req/sec per host."""
    now = time.time()
    last = LAST_HIT.get(host, 0.0)
    delta = now - last
    if delta < gap:
        time.sleep(gap - delta)
    LAST_HIT[host] = time.time()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_one(entry: dict, total_bytes: int) -> tuple[dict, int]:
    """Fetch a single URL; return (manifest_entry, bytes_added)."""
    url = entry["url"]
    target_rel = entry["target"]
    target = ROOT / target_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    host = urlparse(url).netloc

    result = {
        "slug": entry["slug"],
        "source": entry["source"],
        "url": url,
        "format": entry.get("format"),
        "license": entry.get("license"),
        "target_path": target_rel,
        "engaged_works_match": entry.get("engaged_works_match", []),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "fetch_status": "pending",
    }

    if total_bytes >= HARD_CAP_BYTES:
        result["fetch_status"] = "skipped_cap"
        result["note"] = f"Hard cap {HARD_CAP_BYTES} bytes reached"
        return result, 0

    if target.exists() and target.stat().st_size > 0:
        result["fetch_status"] = "already_on_disk"
        result["sha256"] = sha256_file(target)
        result["size_kb"] = round(target.stat().st_size / 1024, 2)
        return result, 0

    throttle(host)

    # Use curl with timeout and follow redirects
    cmd = [
        "curl", "-fsSL",
        "--retry", "2", "--retry-delay", "3",
        "--max-time", "120",
        "-A", "Mozilla/5.0 (lane5-corpus-fetch; eeshan@berkeley)",
        "-o", str(target),
        url,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=180)
    except subprocess.CalledProcessError as e:
        result["fetch_status"] = "failed"
        result["error"] = (e.stderr or b"").decode("utf-8", "replace")[:400]
        if target.exists():
            target.unlink()
        return result, 0
    except subprocess.TimeoutExpired:
        result["fetch_status"] = "failed"
        result["error"] = "curl timeout"
        if target.exists():
            target.unlink()
        return result, 0

    size = target.stat().st_size
    result["fetch_status"] = "fetched"
    result["sha256"] = sha256_file(target)
    result["size_kb"] = round(size / 1024, 2)
    return result, size


def fetch_plan(plan_path: Path) -> None:
    plan = json.loads(plan_path.read_text())
    existing = []
    if MANIFEST_PATH.exists():
        existing = json.loads(MANIFEST_PATH.read_text()).get("lane5_additions", [])

    total = sum(int((e.get("size_kb") or 0) * 1024) for e in existing if e.get("fetch_status") == "fetched")
    out = list(existing)

    for entry in plan:
        print(f"[lane5] {entry['slug']} <- {entry['url']}", file=sys.stderr)
        rec, added = fetch_one(entry, total)
        total += added
        out.append(rec)
        print(f"  -> {rec['fetch_status']} ({rec.get('size_kb', 0)} kb)  cumulative={total/1024/1024:.1f} MB",
              file=sys.stderr)

    MANIFEST_PATH.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "corpus-chat-lane5",
        "branch": "corpus/external-unblock-2026-05-19",
        "hard_cap_mb": HARD_CAP_BYTES // 1024 // 1024,
        "cumulative_bytes_fetched": total,
        "lane5_additions": out,
    }, indent=2))
    print(f"[lane5] wrote manifest with {len(out)} entries, total={total/1024/1024:.1f} MB",
          file=sys.stderr)


def add_manifest_only(entries: list[dict]) -> None:
    """Append manifest-only entries (no fetch attempted)."""
    out = []
    if MANIFEST_PATH.exists():
        m = json.loads(MANIFEST_PATH.read_text())
        out = m.get("lane5_additions", [])
        meta = m
    else:
        meta = {"generated_at": datetime.now(timezone.utc).isoformat(),
                "generated_by": "corpus-chat-lane5",
                "branch": "corpus/external-unblock-2026-05-19",
                "hard_cap_mb": HARD_CAP_BYTES // 1024 // 1024,
                "cumulative_bytes_fetched": 0,
                "lane5_additions": []}

    for e in entries:
        e.setdefault("fetch_status", "manifest_only")
        e.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
        out.append(e)

    meta["lane5_additions"] = out
    MANIFEST_PATH.write_text(json.dumps(meta, indent=2))
    print(f"[lane5] added {len(entries)} manifest-only entries", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch_plan(Path(sys.argv[2]))
    elif cmd == "manifest_only":
        entries = json.loads(Path(sys.argv[2]).read_text())
        add_manifest_only(entries)
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
