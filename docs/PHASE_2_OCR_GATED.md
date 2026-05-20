# Phase-2 OCR Gated — Lane-7 Status, 2026-05-19

## Sentinel check (HARD GATE)

```
$ ls /nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md
ls: cannot access ... : No such file or directory
```

The prakriya-chat Phase-1 completion sentinel does **not** exist as of
2026-05-19. Per Lane-7's mandate, this means:

- Phase-2 OCR runs are blocked.
- Lane-7 has completed spec-building only.
- No OCR was invoked; `philosophy_ocr` was not modified.

## What Lane-7 did instead

- Built 9 per-work `data/digitization_specs/<slug>.json` digitization specs
  for the priority-12 PDFs Lane 3 acquired.
- Rendered the first five pages of each PDF at 200 DPI to
  `data/digitization_specs/<slug>/p{1..5}.png` (gitignored).
- Recorded per-PDF SHA-256, byte size, page count, page dimensions,
  text-layer vs image-scan classification, an embedded-DPI estimate, a
  page-3 visual-quality heuristic (mean intensity + edge density + skew
  search), structural expectations from Lane-3 metadata, ground-truth
  comparator status, and a Phase-2 run plan keyed to the
  `sched_mit_sloan_gpu_r8` partition.

## How to unblock Phase-2

When the prakriya-chat finalises Phase 1 and writes the sentinel at
`/nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md`, Lane-7's
recommended Phase-2 entry point is:

1. Run a ground-truth-validation OCR on
   `suresvara_taittiriya_varttika` first 10 pages (smallest clean target).
2. Score resolution-rate against Balasubramanian 1974 (Lane-3 metadata
   names this as the comparator).
3. If resolution-rate >= 0.95, proceed to full-book OCR on the OCR-readiness
   ranking in `data/digitization_specs/_summary.json`.

Three-engine + judge pipeline lives at
`/home/eeshan/vedanta-timeline/src/philosophy_ocr/` (do not modify; invoke
via its CLI only). Throughput estimate: ~30 pages/hr on 4x A100-40G.
