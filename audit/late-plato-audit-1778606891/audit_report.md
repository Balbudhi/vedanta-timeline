# Opus audit report — `late-plato.md`

Branch: `audit/late-plato-1778606891`
Worktree: `/orcd/home/002/eeshan/worktrees/opus-audits/late-plato-audit-1778606891`
Target: `data/articles/source/late-plato.md`
Plan: `plans/late_plato_plan.md` (heterodox aporetic-protreptic early + unfinished metaphysics late)

## 1. Quantitative checks

| Metric | Before | After | Threshold |
|---|---:|---:|---|
| Real SSP density (excluding quote lead-ins) | 9.9% | 5.5% | <25% |
| Total SSP including quote lead-ins | 9.9% | 17.2% | informational |
| Em-dash density per 1000w | 0.95 | 1.66 | <6 (and <10) |
| Greek characters in article | ~110 | 3,301 | depth requirement |
| Word count | 7,381 | 9,013 | n/a |
| Banned phrases | 0 | 0 | must be 0 |
| "Vijñāna Co-Realism" | 0 | 0 | must be 0 |
| "architecture" tells | 3 | 0 | replaced |
| "crucial" | 0 | 0 (1 introduced then removed) | replaced |

The post-audit SSP rise to 17.2% is entirely lead-in sentences before primary-text quotation blocks ("At 254d the Stranger says:") — these are scholion-style citation markers explicitly permitted by `STYLE_GUIDE_v2.md` §6. Genuine SSP density (single-sentence prose paragraphs functioning as rhetorical filler) is 5.5%.

## 2. Mandatory chunks engaged (with Greek + English + Stephanus)

All mandatory chunks from the audit checklist now carry Greek primary-text quotation with Stephanus pagination:

| Chunk | Status |
|---|---|
| Apology 21a-23b (Socratic ignorance) | Greek 21d added |
| Symposium 209e-212a (Diotima, ἐξαίφνης) | Greek 210e, 211a-b added |
| Republic VI-VII 506b-521b (ἐπέκεινα τῆς οὐσίας) | Greek 509b full sentence added |
| Sophist 237a-259d (megista genē, non-being as otherness) | Greek 237a (Parmenides fr. 7.1), 248e-249a, 254d, 256d, 258d-e added |
| Statesman 283c-287b (metron, right measure) | Greek 284e added (the two sciences of measurement) |
| Philebus 16c-17a (divine method) + 23c-31b (four kinds + mind in cause) | Greek 16c, 23c-d, 30c added |
| Timaeus 27d-29d (eternal vs becoming) + 47e-53c (chōra) + 90a-c (cultivation) | Greek 27d-28a, 29c, 29d, 48e-49a, 52a-b, 90a added |
| Laws X 887b-907d (theology) | Greek 887b, 896a, 899b added |
| Seventh Letter 341c-344d | Greek 341c-d, 342a-b, 344b added (the existing οὐδὲ μήποτε γένηται σύγγραμμα was already present, expanded to full passage) |

All Greek extracted from `/orcd/pool/008/eeshan/ocr/acquired_primaries/plato/*/plato_*_perseus_grc.xml` (Perseus betacode), converted to Unicode polytonic Greek via a small converter in `/tmp/betacode.py`.

## 3. Substantive theses

| Plan-spine claim | Defended? |
|---|---|
| Early Plato as aporetic-protreptic (not propounding a system) | Yes — Apology 21d, Theaetetus 210a-b, ladder/cave conversion-not-content reading |
| Late Plato as unfinished metaphysics | Yes — explicitly framed in conclusion |
| Five greatest kinds from Sophist 254a-259b with Greek | Yes — Greek added at 254d, 255a-b, 256d, 258d-e |
| Non-being-as-otherness as Parmenides/Heraclitus dissolution | Yes — Greek 258d-e (ἡ θατέρου φύσις); framing marked as AF4 reconstruction |
| Chōra as structural fit for *bhāvarūpa avidyā* — marked as user's reconstruction | Yes — explicit AF1, AF4 tag added in §21 |
| Seventh Letter epistemological humility | Yes — full Greek at 341c-d, 342a-b, 344b |
| AF1-AF9 discipline | Applied: §21 chōra tagged AF1/AF4; §6 Parmenides-Heraclitus framing tagged AF4; Tübingen reconstruction caveated |

## 4. Writing-quality fixes

- Scaffolding paragraphs ("The argument will move in five steps." then five SSPs of "First,..., Second,..., Third,..., Fourth,..., Fifth,...") absorbed into two normal paragraphs.
- "The case can now be stated plainly." SSP merged with following paragraph.
- "The thesis tested here has two parts." SSP merged.
- Three uses of "architecture" replaced with "construction", "scaffolding", "system".
- One inadvertent "crucial" (introduced during edit) replaced with "load-bearing".

## 5. Manifest

`data/articles/manifest.json` already contains the `late-plato` slug entry. Not modified.

## 6. Known limitations

- Section 14 (Tübingen reconstruction) names Krämer, Gaiser, Reale, Szlezák without citing specific works; this is editorial summary, not a load-bearing attribution. Acceptable under §1 of the quality bar since no Tübingen content is quoted as load-bearing here.
- Section 18 makes a structural comparison with *Bhagavad Gītā* and *Kena Upaniṣad* "lamp" / "lightning" imagery without quoting either text. The comparison is explicitly hedged ("the comparison should stop where it should") and framed as resonance, not identity. A future revision could quote Gītā 10.11 (jñānadīpa) and Kena 4.4 (vidyut) directly; current state is acceptable but at the lower bound.
- Section 16 references the "five things" (name, definition, image, knowledge, thing itself) from Seventh Letter 342a-b — Greek is now quoted directly.

## 7. Files touched

- `data/articles/source/late-plato.md` — edits in place, primary deliverable.
- `audit/late-plato-audit-1778606891/audit_report.md` — this report.

No other files modified.
