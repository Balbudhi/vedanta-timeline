"""PDF page → PNG rendering via PyMuPDF."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

try:
    import pymupdf  # PyMuPDF >= 1.24 ships as the `pymupdf` import alias.
except ImportError:  # pragma: no cover
    pymupdf = None  # type: ignore[assignment]


def render_page(pdf_path: Path, page_index: int, out_path: Path, dpi: int = 300) -> Path:
    """Render ``page_index`` (0-based) of ``pdf_path`` to ``out_path`` as PNG."""

    if pymupdf is None:
        raise ImportError("pymupdf not installed; pip install pymupdf>=1.24.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf_path))
    try:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(dpi=dpi)
        pix.save(str(out_path))
    finally:
        doc.close()
    return out_path


def render_pages(pdf_path: Path, page_indices: Iterable[int], out_dir: Path, dpi: int = 300) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []
    for idx in page_indices:
        out = out_dir / f"page_{idx:04d}.png"
        rendered.append(render_page(pdf_path, idx, out, dpi=dpi))
    return rendered
