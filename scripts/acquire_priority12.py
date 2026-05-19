#!/usr/bin/env python3
"""Acquire the priority-12 archive.org PDFs to /nas/ucb/eeshan/digitization_queue/.

Per-work plan from docs/ACQUISITION_PATHWAYS.md §A. Downloads PDF only,
computes sha256, runs pypdf-based pdfinfo, writes metadata.json.

Lane-3 of the corpus build. Do not commit PDFs (large); commit metadata.json only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

QUEUE_ROOT = Path("/nas/ucb/eeshan/digitization_queue")
TMPDIR = "/nas/ucb/eeshan/tmp"
TODAY = "2026-05-19"
AGENT = "corpus-chat-lane3"

# (work_slug, item_id, expected_filename_in_item or None to auto-find largest .pdf)
# A.11 Śatadūṣaṇī is print-only; not in this list.
# Multi-volume entries land sequenced files (source_vol1.pdf, etc.).
PRIORITY12 = [
    # A.1 Baladeva Govinda-Bhāṣya
    {
        "slug": "baladeva_govinda_bhasya",
        "items": [{"item_id": "GovindaBhasya.KrsnadasBaba", "filename": None, "outname": "source.pdf"}],
        "tier": "A1",
    },
    # A.2 Bhāskara BSB
    {
        "slug": "bhaskara_brahma_sutra_bhasya",
        "items": [{"item_id": "BrahmaSutraBhashyaOfBhaskarNos.70185209Year1915ChowkhambaSanskritSeries",
                   "filename": None, "outname": "source.pdf"}],
        "tier": "A2",
    },
    # A.3 Citsukha Tattva-Pradīpikā
    {
        "slug": "citsukha_tattva_pradipika",
        "items": [{"item_id": "SKEw_tattva-pradipika-chitsukhi-of-chitsukhacharya-with-commentary-nayana-prasadini-b",
                   "filename": None, "outname": "source.pdf"}],
        "tier": "A3",
    },
    # A.4 Jayatīrtha Tattva-Prakāśikā (edition unverified)
    {
        "slug": "jayatirtha_tattva_prakashika",
        "items": [{"item_id": "tattva-prakasika", "filename": None, "outname": "source.pdf"}],
        "tier": "A4",
    },
    # A.5 Madhusūdana Gūḍhārtha-Dīpikā (Gambhirananda Sanskrit+English is the citable one)
    {
        "slug": "madhusudana_gudhartha_dipika",
        "items": [
            {"item_id": "tDyP_bhagavad-gita-with-gudharth-deepika-by-madhusudan-sarasvati-translated-by-swami-",
             "filename": None, "outname": "source.pdf"},
        ],
        "tier": "A5",
    },
    # A.6 Madhva Gītā-Bhāṣya — sub-volume identification pending; skip download.
    # A.7 Madhva Gītā-Tātparya-Nirṇaya (Prahlādācar 1987 PDF)
    {
        "slug": "madhva_gita_tatparya_nirnaya",
        "items": [{"item_id": "anandatirthabhagavatpadacharyavirachitahgitatatparyanirnayaheditedbydprahladachar1987",
                   "filename": None, "outname": "source.pdf"}],
        "tier": "A7",
    },
    # A.8 Madhva Nyāya-Vivaraṇa — sub-volume identification pending; skip download.
    # A.9 Sureśvara BUBV (3 vols in single archive item)
    {
        "slug": "suresvara_brhadaranyaka_varttika",
        "items": [{"item_id": "BrihadaranyakaBhashyaVartikam2", "filename": None, "outname": "source.pdf"}],
        "tier": "A9",
    },
    # A.10 Sureśvara TUBV (1889 Anandashram)
    {
        "slug": "suresvara_taittiriya_varttika",
        "items": [{"item_id": "gOtp_taitiriya-upanishad-bhashya-vartika-by-sureshvara-acharya-1889-anand-ashram-press",
                   "filename": None, "outname": "source.pdf"}],
        "tier": "A10",
    },
    # A.12 Vidyāraṇya Vivaraṇa-Prameya-Saṅgraha (2005 Dvivedī)
    {
        "slug": "vidyaranya_vivarana_prameya_sangraha",
        "items": [{"item_id": "fzFh_vivarana-prameya-sangraha-by-vidyaranya-muni-edited-by-parasa-nath-dvivedi-2005-",
                   "filename": None, "outname": "source.pdf"}],
        "tier": "A12",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ia_list_files(item_id: str) -> list[dict]:
    """Return list of file records from ia metadata."""
    cmd = ["ia", "metadata", item_id]
    env = dict(os.environ); env["TMPDIR"] = TMPDIR
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
    md = json.loads(r.stdout)
    return md.get("files", []), md.get("metadata", {})


def pick_pdf(files: list[dict]) -> str | None:
    """Pick the original (not derivative-text) PDF; fall back to largest if needed."""
    candidates = [f for f in files if f.get("name", "").lower().endswith(".pdf")]
    if not candidates:
        return None
    # Prefer source=original
    originals = [f for f in candidates if f.get("source") == "original"]
    pool = originals if originals else candidates
    pool.sort(key=lambda f: int(f.get("size", "0")), reverse=True)
    return pool[0]["name"]


def ia_download(item_id: str, filename: str, dest_dir: Path) -> Path:
    """Download a specific file from an archive.org item via curl (one req)."""
    # URL-encode the filename for the request path. archive.org accepts spaces as %20.
    from urllib.parse import quote
    url = f"https://archive.org/download/{item_id}/{quote(filename)}"
    tmp_out = dest_dir / (filename.replace(" ", "_") + ".tmp")
    cmd = [
        "curl", "-fsSL", "-A", f"corpus-chat/{TODAY} (research)",
        "--retry", "3", "--retry-delay", "2",
        "-o", str(tmp_out), url,
    ]
    print(f"  curl {url}", flush=True)
    subprocess.run(cmd, check=True)
    return tmp_out


def pdf_info(path: Path) -> dict:
    """Use pypdf to get pdfinfo-like data."""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(path), strict=False)
        info = {
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "producer": None,
            "creator": None,
            "title": None,
            "page_size": None,
        }
        try:
            meta = reader.metadata or {}
            info["producer"] = str(meta.get("/Producer") or "") or None
            info["creator"] = str(meta.get("/Creator") or "") or None
            info["title"] = str(meta.get("/Title") or "") or None
        except Exception:
            pass
        try:
            p0 = reader.pages[0]
            mb = p0.mediabox
            w = float(mb.width); h = float(mb.height)
            info["page_size"] = f"{w:.1f} x {h:.1f} pts"
        except Exception:
            pass
        return info
    except Exception as e:
        return {"error": str(e)}


def estimate_quality(pdf_path: Path, pdfinfo: dict) -> tuple[str, str, int]:
    """Heuristic quality: KB-per-page proxy for scan resolution.

    Returns (verdict, notes, ocr_friendliness_score 1-5).
    """
    size = pdf_path.stat().st_size
    pages = pdfinfo.get("pages") or 1
    kb_per_page = size / 1024 / pages
    if kb_per_page > 400:
        return ("clean", f"high KB/page proxy ({kb_per_page:.0f} KB/pg) suggests clean high-DPI scan", 4)
    if kb_per_page > 180:
        return ("moderate_bleed",
                f"moderate KB/page proxy ({kb_per_page:.0f} KB/pg); likely standard archive.org scan, some bleed", 3)
    if kb_per_page > 50:
        return ("heavy_bleed",
                f"low KB/page proxy ({kb_per_page:.0f} KB/pg); compressed or degraded scan, expect OCR difficulty", 2)
    return ("illegible",
            f"very low KB/page proxy ({kb_per_page:.0f} KB/pg); possibly text-only or severely degraded", 1)


def process_work(work: dict, force: bool = False) -> dict:
    slug = work["slug"]
    work_dir = QUEUE_ROOT / slug
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {slug} ({work['tier']}) ===", flush=True)
    item_metadata_all = []
    pdf_records = []
    for idx, item in enumerate(work["items"], start=1):
        item_id = item["item_id"]
        outname = item["outname"]
        out_path = work_dir / outname
        time.sleep(1.1)  # archive.org rate limit
        files, item_md = ia_list_files(item_id)
        item_metadata_all.append({"item_id": item_id, "ia_metadata": item_md})
        filename = item["filename"] or pick_pdf(files)
        if filename is None:
            print(f"  !! no PDF in item {item_id}", flush=True)
            continue
        if out_path.exists() and not force:
            print(f"  exists, skipping download: {out_path}", flush=True)
        else:
            tmp = ia_download(item_id, filename, work_dir)
            tmp.replace(out_path)
        size = out_path.stat().st_size
        print(f"  computing sha256...", flush=True)
        sha = sha256_file(out_path)
        info = pdf_info(out_path)
        quality, q_notes, score = estimate_quality(out_path, info)
        pdf_records.append({
            "outname": outname,
            "item_id": item_id,
            "ia_filename": filename,
            "size_bytes": size,
            "sha256": sha,
            "pdfinfo": info,
            "quality": quality,
            "quality_notes": q_notes,
            "ocr_friendliness_score": score,
        })
        print(f"  ok: {outname} {size:,} bytes, {info.get('pages')} pages, quality={quality}", flush=True)

    summary = {
        "slug": slug,
        "tier": work["tier"],
        "pdf_records": pdf_records,
        "ia_items": item_metadata_all,
    }
    # Save raw fetch summary for next-step metadata authoring
    (work_dir / "_fetch_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="restrict to one slug")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    QUEUE_ROOT.mkdir(parents=True, exist_ok=True)
    Path(TMPDIR).mkdir(parents=True, exist_ok=True)
    for work in PRIORITY12:
        if args.only and work["slug"] != args.only:
            continue
        try:
            process_work(work, force=args.force)
        except subprocess.CalledProcessError as e:
            print(f"  FAILED {work['slug']}: {e}", flush=True)
        except Exception as e:
            print(f"  ERROR {work['slug']}: {e}", flush=True)


if __name__ == "__main__":
    main()
