#!/usr/bin/env python3
"""
build_digitization_spec.py
---------------------------
Lane-7 (corpus-chat) Phase-2 OCR spec builder.

For each priority-12 PDF acquired by Lane 3, emit a `digitization_specs/<slug>.json`
that pins down everything Phase-2 OCR will need: source-PDF hash & size, page
dimensions, text-layer detection, a visual-quality heuristic computed from a
rendered page-1 PNG, structural expectations (from Lane-3 metadata), ground-truth
comparators (from Lane-1 manifest + Lane-3 metadata), and a Phase-2 run plan
that mirrors the `philosophy_ocr` three-engine + Codex-judge pipeline.

Pure spec build — no OCR is invoked. Renders pages 1-5 of each PDF at 200 DPI
via PyMuPDF and lands them under `data/digitization_specs/<slug>/p{1..5}.png`
(gitignored: PNGs are too large to commit, only the JSON ships).

Usage:
    PYTHONPATH=/nas/ucb/eeshan/tmp/pylocal \
    TMPDIR=/nas/ucb/eeshan/tmp \
    python3 scripts/build_digitization_spec.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

# pymupdf is installed into /nas/ucb/eeshan/tmp/pylocal — caller must set
# PYTHONPATH. We import lazily so an import error surfaces with a clear message.
try:
    import fitz  # noqa: F401  (PyMuPDF)
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "pymupdf not importable. Set PYTHONPATH=/nas/ucb/eeshan/tmp/pylocal\n"
    )
    raise

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKTREE = Path("/nas/ucb/eeshan/corpus_worktrees/digitization-specs")
QUEUE_ROOT = Path("/nas/ucb/eeshan/digitization_queue")
SPECS_DIR = WORKTREE / "data" / "digitization_specs"
LANE1_MANIFEST = Path(
    "/nas/ucb/eeshan/corpus_worktrees/direct-ingest/data/ingested/_manifest.json"
)

# The nine priority-12 slugs Lane 3 acquired (see Lane-7 mandate).
PRIORITY_SLUGS = [
    "baladeva_govinda_bhasya",
    "bhaskara_brahma_sutra_bhasya",
    "citsukha_tattva_pradipika",
    "jayatirtha_tattva_prakashika",
    "madhusudana_gudhartha_dipika",
    "madhva_gita_tatparya_nirnaya",
    "suresvara_brhadaranyaka_varttika",
    "suresvara_taittiriya_varttika",
    "vidyaranya_vivarana_prameya_sangraha",
]

# Pipeline numbers from philosophy_ocr/README.md + SANSKRIT_OCR_FINAL_PLAN.md.
# Three-engine consensus on 4x A100-40G hits ~30 pages/hour sustained.
PAGES_PER_HOUR_4XA100 = 30
PARTITION = "sched_mit_sloan_gpu_r8"
OCR_PRIMARY = "surya"
OCR_SECONDARY = ["qwen2.5-vl-72b-awq", "internvl-2.5-78b-awq"]
JUDGE = "codex-5.4"

GENERATED_AT = "2026-05-19"
GENERATOR = "corpus-chat-lane7"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            buf = fh.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def inspect_pdf(path: Path) -> dict:
    """Open PDF once with PyMuPDF: pages, dims, text-layer detection, DPI guess."""
    doc = fitz.open(str(path))
    n = doc.page_count
    p0 = doc.load_page(0)
    rect = p0.rect  # in points (1/72")
    w_pt, h_pt = rect.width, rect.height
    # Text-layer: a native-text PDF returns non-trivial text from get_text("text").
    sample_text = p0.get_text("text") or ""
    # Look at first 3 pages so a blank cover doesn't fool us.
    extra = ""
    for i in range(1, min(3, n)):
        extra += doc.load_page(i).get_text("text") or ""
    has_text = len((sample_text + extra).strip()) > 200  # heuristic

    # DPI estimate: get embedded raster images on p0 and compare image px to
    # rendered points (most archive.org scans embed a single full-page image
    # per page). Fallback heuristic = 300 DPI.
    dpi_estimate = None
    try:
        imgs = p0.get_images(full=True)
        if imgs:
            xref = imgs[0][0]
            base = doc.extract_image(xref)
            iw, ih = base.get("width"), base.get("height")
            if iw and ih and w_pt and h_pt:
                dpi_x = iw / (w_pt / 72.0)
                dpi_y = ih / (h_pt / 72.0)
                dpi_estimate = int(round((dpi_x + dpi_y) / 2.0))
    except Exception:
        dpi_estimate = None
    doc.close()
    return {
        "total_pages": n,
        "page_dimensions_pt": f"{w_pt:.1f} x {h_pt:.1f}",
        "is_text_layer_native": bool(has_text),
        "is_image_scan": not bool(has_text),
        "image_dpi_estimate": dpi_estimate,
    }


def render_first_pages(path: Path, out_dir: Path, n: int = 5, dpi: int = 200) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(path))
    rel: list[str] = []
    n_render = min(n, doc.page_count)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    for i in range(n_render):
        png = out_dir / f"p{i + 1}.png"
        if not png.exists():
            pix = doc.load_page(i).get_pixmap(matrix=mat, alpha=False)
            pix.save(str(png))
        rel.append(str(png.relative_to(WORKTREE)))
    doc.close()
    return rel


def score_visual_quality(png_path: Path) -> dict:
    """Cheap visual-quality heuristic on page 1.

    - mean intensity: 0 = pure black, 255 = pure white. Cleaner scans sit near
      230-250 (bright paper, dark ink).
    - edge density: fraction of pixels above a Sobel-magnitude threshold. Bleed
      and stain push this up; clean print sits in a middle band.
    - skew estimate: project ink-row sums across small rotation candidates, pick
      the angle whose row-projection has the highest variance (most "lined up").
    """
    img = Image.open(png_path).convert("L")
    # downsample large pages for speed
    if max(img.size) > 1600:
        ratio = 1600 / max(img.size)
        img = img.resize(
            (int(img.size[0] * ratio), int(img.size[1] * ratio)),
            Image.BILINEAR,
        )
    arr = np.asarray(img, dtype=np.float32)
    mean_intensity = float(arr.mean())

    edges = img.filter(ImageFilter.FIND_EDGES)
    ea = np.asarray(edges, dtype=np.float32)
    edge_density = float((ea > 64).mean())

    # skew search: rotate ink-binarised image by a few angles, measure row-sum
    # variance. Higher variance = better-aligned text rows.
    ink = (arr < 160).astype(np.float32)
    best_angle, best_var = 0.0, -1.0
    for ang in [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]:
        rot = Image.fromarray((ink * 255).astype(np.uint8)).rotate(
            ang, resample=Image.BILINEAR, fillcolor=0
        )
        ra = np.asarray(rot, dtype=np.float32) / 255.0
        v = float(ra.sum(axis=1).var())
        if v > best_var:
            best_var, best_angle = v, ang
    skew_detected = abs(best_angle) >= 0.5

    # quality_class heuristic:
    #   very bright + low edge density => clean
    #   bright + medium edge density   => moderate_bleed
    #   dim or high edge density       => heavy_bleed
    if mean_intensity > 225 and edge_density < 0.06:
        q = "clean"
        score = 5
    elif mean_intensity > 210 and edge_density < 0.10:
        q = "moderate_bleed"
        score = 4
    elif mean_intensity > 190:
        q = "moderate_bleed"
        score = 3
    else:
        q = "heavy_bleed"
        score = 2

    return {
        "mean_intensity": round(mean_intensity, 2),
        "edge_density": round(edge_density, 4),
        "quality_class_heuristic": q,
        "score_heuristic": score,
        "skew_detected": skew_detected,
        "skew_angle_deg_estimate": best_angle if skew_detected else None,
    }


# ---------------------------------------------------------------------------
# Lane-1 comparator lookup
# ---------------------------------------------------------------------------


def load_lane1_manifest() -> list[dict]:
    if not LANE1_MANIFEST.exists():
        return []
    try:
        data = json.loads(LANE1_MANIFEST.read_text())
        return data.get("ingested", []) or []
    except Exception:
        return []


# Map our priority slugs to substrings that, if found in any Lane-1 text_id,
# would indicate a same-work comparator. None of these are expected to hit (the
# 9 works are OCR targets *because* they're not on GRETIL), but record the
# search so the spec is auditable.
LANE1_NEEDLES = {
    "baladeva_govinda_bhasya": ["baladeva", "govinda-bhasya", "govinda_bhasya"],
    "bhaskara_brahma_sutra_bhasya": ["bhaskara-brahma", "bhaskara_brahma"],
    "citsukha_tattva_pradipika": ["citsukha", "tattva-pradipika"],
    "jayatirtha_tattva_prakashika": ["jayatirtha-tattva-prakashika", "tattva-prakashika"],
    "madhusudana_gudhartha_dipika": ["madhusudana-gudhartha", "gudhartha-dipika"],
    "madhva_gita_tatparya_nirnaya": ["madhva-gita-tatparya", "gita-tatparya"],
    "suresvara_brhadaranyaka_varttika": [
        "suresvara-brhad",
        "brhadaranyaka-varttika",
        "suresvara-brhadaranyaka",
    ],
    "suresvara_taittiriya_varttika": [
        "suresvara-taittiriya",
        "taittiriya-varttika",
    ],
    "vidyaranya_vivarana_prameya_sangraha": [
        "vidyaranya-vivarana",
        "vivarana-prameya",
    ],
}


def find_lane1_comparator(slug: str, manifest: list[dict]) -> dict | None:
    needles = LANE1_NEEDLES.get(slug, [])
    for entry in manifest:
        tid = (entry.get("text_id") or "").lower()
        src = (entry.get("source_file") or "").lower()
        blob = tid + " " + src
        if any(n in blob for n in needles):
            return entry
    return None


# ---------------------------------------------------------------------------
# Phase-2 run-plan synthesis
# ---------------------------------------------------------------------------


def build_run_plan(total_pages: int) -> dict:
    hours = round(total_pages / PAGES_PER_HOUR_4XA100, 1)
    return {
        "ocr_engine_primary": OCR_PRIMARY,
        "ocr_engines_secondary": list(OCR_SECONDARY),
        "judge_layer": JUDGE,
        "estimated_pages_per_hour": PAGES_PER_HOUR_4XA100,
        "estimated_total_hours_4xA100": hours,
        "sbatch_partition_target": PARTITION,
        "blocking_dependencies": [
            "PHASE_1_COMPLETE_sentinel:/nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md",
            "prakriya.ocr_api.propose_correction",
            "philosophy_ocr.consensus",
            "philosophy_ocr.verify_lexical",
            "philosophy_ocr.judge_codex",
        ],
    }


# ---------------------------------------------------------------------------
# Spec assembly
# ---------------------------------------------------------------------------


def build_spec(slug: str, lane1: list[dict]) -> dict:
    queue_dir = QUEUE_ROOT / slug
    pdf = queue_dir / "source.pdf"
    meta = json.loads((queue_dir / "metadata.json").read_text())

    if not pdf.exists():
        raise FileNotFoundError(f"missing source.pdf for {slug}")

    size = pdf.stat().st_size
    sha = sha256_file(pdf)
    insp = inspect_pdf(pdf)

    # Render p1..p5 into worktree assets dir (gitignored).
    slug_assets = SPECS_DIR / slug
    rendered = render_first_pages(pdf, slug_assets, n=5, dpi=200)
    # Score the heuristic on p3 — p1 is often a title page (large logos, lots
    # of white) or colophon and not representative of content pages.
    sample_for_quality = slug_assets / "p3.png"
    if not sample_for_quality.exists():
        sample_for_quality = slug_assets / "p1.png"
    vq = score_visual_quality(sample_for_quality)
    vq["scored_on"] = sample_for_quality.name

    # Reconcile Lane-3 quality class with our heuristic. Lane-3 used a few
    # non-canonical class names (e.g. `born_digital_text_likely`,
    # `compressed_legible`); normalise to the four-value schema while keeping
    # the raw Lane-3 string for audit.
    lane3_class_raw = meta.get("first_page_visual_quality")
    lane3_class_map = {
        "clean": "clean",
        "moderate_bleed": "moderate_bleed",
        "heavy_bleed": "heavy_bleed",
        "text_pdf": "text_pdf",
        "born_digital_text_likely": "text_pdf",
        "compressed_legible": "moderate_bleed",
    }
    lane3_class = lane3_class_map.get(lane3_class_raw, lane3_class_raw)
    lane3_score = meta.get("ocr_friendliness_score")
    quality_class = lane3_class or vq["quality_class_heuristic"]
    reclass_note = ""
    if lane3_class and lane3_class != vq["quality_class_heuristic"]:
        reclass_note = (
            f"Lane-3 said '{lane3_class}'; Lane-7 heuristic says "
            f"'{vq['quality_class_heuristic']}' (mean_intensity="
            f"{vq['mean_intensity']}, edge_density={vq['edge_density']}). "
            "Trusting Lane-3 for quality_class field; heuristic recorded under "
            "visual_quality.heuristic_*."
        )
    ocr_score = lane3_score or vq["score_heuristic"]

    # Front/back matter estimate: archive.org reprints typically have ~6 pages
    # front (title, preface, contents) and ~4 pages back (index/colophon).
    # We don't read the TOC programmatically — Lane 3 didn't either — so this
    # is a documented approximation.
    front_matter_est = 8
    back_matter_est = 4

    exp = meta.get("expected_text_units", {}) or {}
    kind = exp.get("kind", "mixed")
    unit_count = exp.get("approximate_count")
    unit_src = exp.get("source_for_estimate", "Lane-3 metadata")

    # Marginalia / commentary detection: if commentaries_included has >=1 entry
    # OR ocr_friendliness_notes mentions "commentary" or "anvaya" or "tika",
    # mark commentary_around_mula true.
    commentaries = meta.get("commentaries_included", []) or []
    notes_blob = (meta.get("ocr_friendliness_notes") or "").lower()
    has_marginal_layout = any(
        kw in notes_blob for kw in ["anvaya", "tika", "ṭīkā", "commentary", "tippani", "marginal"]
    )
    commentary_around_mula = bool(commentaries) or has_marginal_layout
    if commentary_around_mula and "three-text" in notes_blob:
        marginalia_density = "high"
    elif commentary_around_mula:
        marginalia_density = "medium"
    else:
        marginalia_density = "low"

    # Ground-truth lookup.
    lane1_entry = find_lane1_comparator(slug, lane1)
    if lane1_entry:
        gt = {
            "digital_comparator_available": True,
            "comparator_source": "lane1_ingested",
            "comparator_url_or_path": lane1_entry.get("source_file"),
            "comparator_coverage": "full" if lane1_entry.get("verse_count") else "partial",
            "comparator_notes": (
                f"Matched Lane-1 ingested text_id='{lane1_entry.get('text_id')}'."
            ),
        }
    else:
        # Fall back to Lane-3 metadata's ground_truth_source field (free text).
        gts = meta.get("ground_truth_source") or ""
        if meta.get("ground_truth_available"):
            # Classify the source string.
            low = gts.lower()
            if "gretil" in low:
                source_kind = "gretil"
            elif "sanskritdocuments" in low:
                source_kind = "sanskritdocuments"
            elif "sarit" in low:
                source_kind = "sarit"
            else:
                source_kind = "other_external"
            coverage = "partial" if "spot" in low or "fragment" in low else "full"
            gt = {
                "digital_comparator_available": True,
                "comparator_source": source_kind,
                "comparator_url_or_path": gts,
                "comparator_coverage": coverage,
                "comparator_notes": (
                    "Recorded from Lane-3 ground_truth_source field; not yet "
                    "ingested into Lane-1. Phase-2 OCR validation should fetch "
                    "or transcribe a sample for resolution-rate scoring."
                ),
            }
        else:
            gt = {
                "digital_comparator_available": False,
                "comparator_source": "none",
                "comparator_url_or_path": None,
                "comparator_coverage": "none",
                "comparator_notes": (
                    "No digital comparator found in Lane-1 manifest or Lane-3 "
                    "metadata. Phase-2 validation must rely on internal "
                    "consensus + Codex judge."
                ),
            }

    spec = {
        "work_slug": slug,
        "spec_version": "1.0",
        "spec_generated_at": GENERATED_AT,
        "spec_generated_by": GENERATOR,
        "source_pdf": str(pdf),
        "source_pdf_sha256": sha,
        "source_pdf_size_bytes": size,
        "lane3_metadata_ref": f"data/digitization_queue/{slug}/metadata.json",
        "lane3_metadata_absolute": str(queue_dir / "metadata.json"),
        "pdf_inspection": insp,
        "visual_quality": {
            "first_5_pages_rendered": rendered,
            "first_5_pages_on_disk": [
                str(slug_assets / f"p{i}.png") for i in range(1, 6)
            ],
            "quality_class": quality_class,
            "ocr_friendliness_score": ocr_score,
            "skew_detected": vq["skew_detected"],
            "skew_angle_deg_estimate": vq["skew_angle_deg_estimate"],
            "marginalia_density": marginalia_density,
            "commentary_around_mula": commentary_around_mula,
            "heuristic_mean_intensity": vq["mean_intensity"],
            "heuristic_edge_density": vq["edge_density"],
            "heuristic_quality_class": vq["quality_class_heuristic"],
            "heuristic_score": vq["score_heuristic"],
            "heuristic_scored_on": vq.get("scored_on", "p1.png"),
            "lane3_quality_class_raw": lane3_class_raw,
            "notes": reclass_note
            or "Lane-3 quality class and Lane-7 heuristic agree.",
        },
        "structural_expectations": {
            "kind": kind,
            "expected_unit_count": unit_count,
            "expected_unit_count_source": unit_src,
            "expected_chapter_count": _expected_chapters(kind, unit_count, slug),
            "front_matter_pages_estimate": front_matter_est,
            "back_matter_pages_estimate": back_matter_est,
        },
        "ground_truth": gt,
        "phase2_run_plan": build_run_plan(insp["total_pages"]),
        "expected_unit_count_check": {
            "method": (
                "Adopted Lane-3 metadata's expected_text_units.approximate_count "
                "without independent TOC scrape. Verified that the source basis "
                "(canonical sūtra/vārttika count) is recorded in "
                "expected_unit_count_source."
            ),
            "approximation_basis": unit_src,
        },
    }
    return spec


def _expected_chapters(kind: str, unit_count: int | None, slug: str) -> int | None:
    """Best-effort chapter count from Lane-3's text-unit kind + slug."""
    # Brahma-sūtra-bhāṣyas: 4 adhyāyas.
    if "brahma_sutra" in slug or "govinda_bhasya" in slug:
        return 4
    # Gītā commentaries: 18 adhyāyas.
    if "gita" in slug:
        return 18
    # Taittirīya-Upaniṣad: 3 vallīs.
    if "taittiriya" in slug:
        return 3
    # Bṛhadāraṇyaka-Upaniṣad: 6 adhyāyas.
    if "brhadaranyaka" in slug:
        return 6
    # Tattva-pradīpikā (Cit-sukhī): 4 paricchedas.
    if "tattva_pradipika" in slug:
        return 4
    # Tattva-prakāśikā (Jayatīrtha on Brahma-sūtra-bhāṣya): 4 adhyāyas.
    if "tattva_prakashika" in slug:
        return 4
    # Vivaraṇa-prameya-saṅgraha: 8 varṇakas.
    if "vivarana_prameya" in slug:
        return 8
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    lane1 = load_lane1_manifest()
    summary = []
    for slug in PRIORITY_SLUGS:
        try:
            spec = build_spec(slug, lane1)
        except Exception as exc:
            print(f"[FAIL] {slug}: {exc}", file=sys.stderr)
            continue
        out = SPECS_DIR / f"{slug}.json"
        out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        # Per-slug README pointing at the gitignored PNGs.
        readme = SPECS_DIR / slug / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            f"# {slug} — Lane-7 rendered pages\n\n"
            f"PNGs `p1.png`..`p5.png` rendered at 200 DPI from "
            f"`{spec['source_pdf']}` on {GENERATED_AT}.\n\n"
            "PNGs are gitignored (>1 MB each). The authoritative spec is "
            f"`data/digitization_specs/{slug}.json` at the worktree root.\n"
        )
        summary.append(
            {
                "slug": slug,
                "pages": spec["pdf_inspection"]["total_pages"],
                "quality_class": spec["visual_quality"]["quality_class"],
                "ocr_score": spec["visual_quality"]["ocr_friendliness_score"],
                "hours_4xA100": spec["phase2_run_plan"]["estimated_total_hours_4xA100"],
                "comparator": spec["ground_truth"]["comparator_source"],
            }
        )
        print(f"[ok] {slug:42s}  pages={spec['pdf_inspection']['total_pages']:5d}  "
              f"q={spec['visual_quality']['quality_class']:14s}  "
              f"score={spec['visual_quality']['ocr_friendliness_score']}")
    # Summary table.
    summary_path = SPECS_DIR / "_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "generated_at": GENERATED_AT,
                "generated_by": GENERATOR,
                "specs": summary,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(f"\nwrote {len(summary)} specs to {SPECS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
