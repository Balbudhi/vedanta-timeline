"""Command-line entry point for philosophy_ocr.

Subcommands:
  ocr-page  PDF + page index → smoke output (single-page three-engine consensus).
  ocr-book  PDF + out dir → full-book pass (resumable).
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .config import SMOKE_OUTPUT_ROOT
from .consensus import consensus_for_page, render_agreement_table
from .emit_ingest import write_results
from .internvl_runner import run_internvl
from .pdf_render import render_page
from .qwen_vl_runner import run_qwen_vl
from .surya_runner import run_surya
from .verify_lexical import lexical_flag_rate, verify_lines


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("ocr-page")
def ocr_page(
    pdf: Path = typer.Option(..., exists=True, readable=True),
    page: int = typer.Option(..., help="0-based page index."),
    out: Path = typer.Option(SMOKE_OUTPUT_ROOT / "page"),
    tensor_parallel: int = typer.Option(2),
) -> None:
    """Single-page three-engine smoke test."""

    out.mkdir(parents=True, exist_ok=True)
    png = render_page(pdf, page, out / f"page_{page:04d}.png")

    surya_lines = run_surya(png)
    (out / "surya.json").write_text(
        json.dumps([line.__dict__ for line in surya_lines], ensure_ascii=False, indent=2)
    )

    qwen = run_qwen_vl(png)
    (out / "qwen_vl.json").write_text(
        json.dumps(
            {"devanagari": qwen.devanagari, "iast": qwen.iast, "tags": qwen.structure_tags},
            ensure_ascii=False,
            indent=2,
        )
    )

    internvl = run_internvl(png)
    (out / "internvl.json").write_text(
        json.dumps(
            {"devanagari": internvl.devanagari, "iast": internvl.iast, "tags": internvl.structure_tags},
            ensure_ascii=False,
            indent=2,
        )
    )

    consensus = consensus_for_page(surya_lines, qwen, internvl)
    table = render_agreement_table(consensus)
    (out / "page_0050_agreement.md").write_text(table)
    (out / "consensus.json").write_text(
        json.dumps([c.__dict__ for c in consensus], ensure_ascii=False, indent=2)
    )

    verdicts = verify_lines([c.surya_text for c in consensus])
    flag_rate = lexical_flag_rate(verdicts)

    write_results(
        {
            "pdf": str(pdf),
            "page": page,
            "consensus": [c.__dict__ for c in consensus],
            "lexical_flag_rate": flag_rate,
        },
        out,
    )

    typer.echo(table)
    typer.echo(f"\nlexical_flag_rate={flag_rate:.3f}  (lines={len(consensus)})")


@app.command("ocr-book")
def ocr_book(
    pdf: Path = typer.Option(..., exists=True, readable=True),
    out: Path = typer.Option(...),
    vllm_port: int = typer.Option(8000),
    tensor_parallel: int = typer.Option(2),
    resume: bool = typer.Option(True),
) -> None:
    """Full-book pass — scaffold; implementation lands after smoke approval."""

    raise typer.Exit(
        "ocr-book is not yet wired; gated on smoke-test approval per Phase C."
    )


def main() -> None:  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
