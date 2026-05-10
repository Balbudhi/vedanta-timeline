# philosophy_ocr

Three-engine Sanskrit OCR pipeline (Surya × Qwen2.5-VL-72B-AWQ × InternVL-2.5-78B-AWQ),
followed by Pāṇinian lexical verification (`prakriya.ocr_api`) and a Codex-5.4
judge for residual disagreements. Targets MIT ORCD's `sched_mit_sloan_gpu_r8`
partition (4×A100-40G) per `docs/SANSKRIT_OCR_FINAL_PLAN.md`.

## Smoke test

```bash
sbatch sbatch/ocr_smoke.sbatch        # Bhāskara BSB p. 50, single-page
```

Outputs land in `/orcd/home/002/eeshan/philosophy/tmp/ocr_smoke/bhaskara_p50/`.

## Full-book run (after smoke approval)

```bash
PDF_PATH=/path/to/book.pdf \
OUT_DIR=/orcd/pool/008/eeshan/philosophy_ocr/<work_slug>/ \
sbatch sbatch/ocr_book.sbatch
```

## Layout

- `config.py` — paths, model IDs, thresholds, partition presets.
- `pdf_render.py` — PyMuPDF page → PNG.
- `surya_runner.py` — Surya line OCR.
- `qwen_vl_runner.py` — Qwen2.5-VL via vLLM HTTP.
- `internvl_runner.py` — InternVL-2.5 via vLLM HTTP (Lipikar substitute).
- `lipikar_runner.py` — stub; activates when `LIPIKAR_HOME` is set.
- `consensus.py` — three-way per-line agreement.
- `verify_lexical.py` — Pāṇinian lexical / sandhi check via `prakriya.ocr_api`.
- `judge_codex.py` — Layer-3 Codex 5.4 judge (currently dry-run stub).
- `emit_ingest.py` — schema for jyotish ingest.
- `cli.py` — `philosophy_ocr ocr-page` / `ocr-book`.

## Tests

```bash
PYTHONPATH=src pytest tests/test_ocr -q
```

Tests are mocked — no GPU or model load required.
