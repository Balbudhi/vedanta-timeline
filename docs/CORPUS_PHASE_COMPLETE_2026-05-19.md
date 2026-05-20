# Corpus phase complete — 2026-05-19

Single-session run by the corpus chat (sibling to the prakriya chat) on `rnn.ist.berkeley.edu`. Nine lanes dispatched as parallel Opus subagents. Every lane closed; nothing left in flight from this session.

This document is the handoff: what landed, where it is, what's still gated, and what the prakriya chat needs to pick up.

---

## 1. Branches shipped — 9 PRs ready

All branches off `origin/main` (commit `3538552`). Each is independently mergeable; no cross-branch dependencies.

| Branch | Commits | Purpose |
|---|---:|---|
| `corpus/direct-ingest-2026-05-19` | 10 | Lane 1 — 52 plain-text Sanskrit primaries → per-verse JSON (`data/ingested/`). 63 287 verses / ~1.58M tokens, paired Devanāgarī + IAST. |
| `corpus/external-ingest-2026-05-19` | 6 | Lane 2 — external-source manifest + SARIT 10-text TEI sample. (Original bulk-mirror commits superseded by the `c32bfb3` corrective per-file-only policy after user flag.) |
| `corpus/digitization-prep-2026-05-19` | 15 | Lane 3 — 9 of 12 priority PDFs + per-work metadata; §B 267-text inventory; `ACQUISITION_PATHWAYS.md` status column. |
| `corpus/audit-2026-05-19` | 2 | Lane 4 — corpus-wide audit + 4 punch-list markdowns. |
| `corpus/external-unblock-2026-05-19` | 4 | Lane 5 — egangotri KSTS PDFs (Muktabodha substitute), Cologne MW+Apte, GRETIL Aṣṭādhyāyī three-witness stack + 25 engaged-works plaintexts. |
| `corpus/dcs-gold-2026-05-19` | 1 | Lane 6 — DCS → prakriya morphology gold (build script + handoff doc; large JSONL stays on /nas). |
| `corpus/digitization-specs-2026-05-19` | 1 | Lane 7 — phase-2 spec JSON for all 9 priority PDFs (Phase-1-complete sentinel absent → no OCR ran). |
| `corpus/expansion-2026-05-19` | 10 | Lane 8 — 34 new `engaged_works[]` entries (18 §B Sanskrit + 16 §C Western). No new thinker files — Lane 4's "must-author 4" already existed under id-variants; recorded as `alternate_names`. |
| `corpus/mahabharata-2026-05-19` | 8 | Lane 9 — entire Bhandarkar Critical Edition Mahābhārata, 18 parvans, 73 898 verses, paired Devanāgarī + IAST. ~25 MB committed JSON. |

Worktrees: `/nas/ucb/eeshan/corpus_worktrees/<lane>/` — keep until PRs merge.

## 2. Corpus state after this session

### 2a. Plain-text Sanskrit corpus (Lane 1 + Lane 9 + Lane 5 GRETIL)

| Source | Texts | Verses / tokens | Repo location |
|---|---:|---:|---|
| `data/sources/sanskrit/` (pre-existing) | 52 | — (raw text) | (already on `main`) |
| `data/ingested/` (Lane 1) | 52 | 63 287 verses · ~1.58M tokens | `corpus/direct-ingest-…` |
| `data/ingested/mahabharata/` (Lane 9) | 1 (18 parvans) | 73 898 verses · ~1.23M whitespace-tokens | `corpus/mahabharata-…` |
| `data/external/gretil/files/` (Lane 5) | 31 | — (HTML/plain) | `corpus/external-unblock-…` |
| `data/external/sarit/` (Lane 2) | 10 TEI | — | `corpus/external-ingest-…` |
| `data/external/cologne/` (Lane 5) | MW + Apte | — (lexicon) | `corpus/external-unblock-…` |

**Combined ingested verse count: ~137 000 verses across ~85 distinct works.** Every verse carries paired Devanāgarī + IAST.

Tokenizer note: all verses recorded as `tokenizer: "fallback_whitespace"` because `prakriya.ocr_api.tokenize` is unimportable on rnn (Python-3.10+ `@dataclass(slots=True)` in `panini_prakriya/conflict.py` vs rnn's 3.8/3.9). When prakriya unblocks this, a single re-tokenization pass over `data/ingested/` will swap in proper Pāṇinian tokens without re-fetching anything.

### 2b. Off-repo artifacts (large, on /nas, not in git)

| Artifact | Path | Size | Notes |
|---|---|---:|---|
| DCS morphology gold | `/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl` | 3.4 GB | 5.7M tokens, 270 works. sha256 `9a6e7cb1…`. Handoff: `docs/dcs_morphology_handoff_2026-05-19.md`. |
| DCS source dump | `/nas/ucb/eeshan/corpus_worktrees/external-ingest/data/external/dcs/dump/` | 720 MB | OliverHellwig/sanskrit shallow clone, CC BY 3.0. |
| Priority-12 PDFs | `/nas/ucb/eeshan/digitization_queue/<slug>/source.pdf` | 1.6 GB total | 9 PDFs acquired; metadata.json per work committed to `corpus/digitization-prep-…`. |
| Phase-2 spec PNGs | `/nas/ucb/eeshan/corpus_worktrees/digitization-specs/data/digitization_specs/<slug>/p{1..5}.png` | ~150 MB | First-5-page renders at 200 DPI for visual quality. |
| egangotri KSTS PDFs | `/nas/ucb/eeshan/corpus_worktrees/external-unblock/data/external/muktabodha_via_egangotri/` | 77 MB | 7 PDFs (Tantrāloka, IPV pt.1+2, etc.). |

These are GitHub-incompatible (file-size or sensible repo-size); manifest entries in the repo point at the on-disk paths + sha256.

### 2c. Thinker corpus

- 165 thinker JSONs total (pre-existing; Lane 4 audited all).
- 34 new `engaged_works[]` entries across 19 thinkers (Lane 8). No new thinker files this session — Lane 4's "must-author 4" all existed under id-variants.
- Outstanding: `vyasa.json` (the MBh-compiler Vyāsa, distinct from `vyasa-bhasya.json` the YS-Bhāṣya author) — Lane 9 surfaced this; flagged for next authoring pass.

### 2d. Audit findings (Lane 4)

- 11 thinkers (Western/modern) still have empty `engaged_works[]` after Lane 8 — Lane 8 deferred per Western-thinker format-precedent ambiguity; partial fix landed in §C.
- 265 engaged-work entries marked stub; 253 lack any on-disk / translation / ingested linkage.
- **70 `data/full_translations/*.md` files; only 10 pass the four-layer (Sanskrit + IAST + English + commentary) contract.** 53 missing Devanāgarī, 14 missing commentary reference, 12 carry honest-acknowledgment-stub markers. This is the largest single quality gap in the corpus.

## 3. Hard blockers — needing user / next-session attention

1. **`prakriya.ocr_api.tokenize` unimportable on rnn.** `panini_prakriya/conflict.py` uses `@dataclass(slots=True)` (Python 3.10+); rnn ships 3.8/3.9. Prakriya chat: either drop `slots=True` from that file, or provision Python ≥3.10 on rnn. Until then every ingest lane runs fallback whitespace tokenization.
2. **Phase-1-complete sentinel absent.** `/nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md` does not exist. Lane 7 correctly held at spec-only; **no OCR has run, by design.** Phase 2 unblocks when the prakriya chat lands the sentinel.
3. **3 priority-12 deferred + 1 print-only:**
   - A.4 Jayatīrtha *Tattva-Prakāśikā* — edition unverified (PDF is text-PDF-shaped, not a scan).
   - A.6 Madhva *Gītā-Bhāṣya* + A.8 Madhva *Nyāya-Vivaraṇa* — Sarvamūla sub-volume needs hand-ID on the Madhwapracharavedike Google Sites index (not API-scrapable).
   - A.11 Vedānta-Deśika *Śatadūṣaṇī* — print only; Chaukhamba ASIN B00KIT4Q3U for purchase.
4. **Indica-et-Buddhica TEI paths 404** after the operator's `.org → .com` migration. Wayback Machine recovery flagged as next-wave action.
5. **Muktabodha registration deferred** — IFP-Pondicherry Śaiva-Siddhānta bundle is unique-to-Muktabodha (no archive.org backup). One contact-form submission unlocks it.
6. **id-variant alias gap in `audit_corpus.py`.** Lane 4's audit checks v2-ids against on-disk filenames literally and missed `rambhadracharya ≈ ramabhadracarya` etc. Lane 8 documented the correct mapping; the script should be patched (low-risk: add an alias dict).

## 4. Handoff to the prakriya chat

Three things the prakriya chat needs to know, in priority order:

### 4a. Consume the DCS morphology gold

- Path: `/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl` (3.4 GB, sha256 `9a6e7cb1…`).
- Sample: 50 rows committed at `data/dcs_morphology_gold/sample.jsonl` on branch `corpus/dcs-gold-2026-05-19`.
- Tuple shapes match `cross_validate_tinanta_fixture.json` and `krdanta_vidyut_gold.json` exactly:
  - tinanta: `[root_slp1, gana, lakara, purusha, vacana, pada]`
  - krdanta: `[root, krt, linga, vibhakti, vacana]`
  - subanta: `[stem_slp1, linga, vibhakti, vacana]`
- For the §A.4 ≥99% match-rate gate: use `require_gana=True`. That subset is 129 k tinanta rows (the 27% of tinanta tokens where gaṇa is unambiguously resolvable from prakriya's dhātupāṭha) — statistically ample. The remaining 73% are genuine ambiguities, not Lane-6 bugs.
- Full handoff brief with `cross_validate_vidyut.py` diff sketch + caveats: `docs/dcs_morphology_handoff_2026-05-19.md` (on `corpus/dcs-gold-…`).
- **Cross-corpus join opportunity:** DCS tags the Mahābhārata at 1.35M tokens; Lane 9 ingested the full BORI CE MBh at 73 898 verses. Both keyed on `(parva, adhyāya, verse)`. Joining them gives the first end-to-end translation-engine training pair (Sanskrit verse → morphology-tagged tokens → eventually English).

### 4b. Unblock the Python-version issue

If you intend Lane-1-style ingest passes to use proper Pāṇinian tokenization (not whitespace fallback), drop `@dataclass(slots=True)` from `src/prakriya/panini_prakriya/conflict.py` or pin rnn to Python ≥3.10. A single re-tokenization pass over `data/ingested/` then refreshes 137k verses without re-fetching.

### 4c. Drop the Phase-1-complete sentinel when ready

Write `/nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md` when:
- `audit-compiled` reports `deferred_rules = 0`
- vidyut cross-validation ≥99.0% against the DCS gold's `require_gana=True` subset
- The 12-probe scholar-grade set in `37_traditional_scholar_grade_checklist.md` clears

When the sentinel lands, Lane 7's spec JSONs at `data/digitization_specs/` are ready inputs for the Phase-2 OCR runs. Recommended Phase-2 dev target (Lane 3 + Lane 7 concur): **Sureśvara *Taittirīya-Vārttika*** — 225 pp, clean scan, ~7.5 h on 4×A100, Balasubramanian-1974 ground-truth comparator available.

## 5. Recommended next-wave actions (low-friction, high-leverage)

In priority order:

1. **Merge the 9 PRs** (or pick the safe subset). All branches off `main` at `3538552`; no cross-branch deps. Suggested merge order: Lane 4 (audits, doc-only) → Lane 1 (ingested JSON) → Lane 9 (MBh) → Lane 8 (thinker enrichments) → Lane 3 (digitization metadata) → Lane 5 + Lane 2 (external sources) → Lane 7 (specs) → Lane 6 (DCS handoff).
2. **Add `vyasa.json`** — Vyāsa-the-MBh-compiler (distinct from `vyasa-bhasya.json`). Single thinker file; engaged_works pointing at the Lane-9 MBh ingestion.
3. **Patch `audit_corpus.py`** with the id-variant alias map (see commit messages on `corpus/expansion-2026-05-19`).
4. **Tackle the full_translations four-layer gap.** 60/70 files need either a Devanāgarī layer added (53), a commentary reference (14), or replacement of stub markers (12). This is content-authoring work, not infrastructure.
5. **Muktabodha registration** — one contact form, unlocks the IFP-Pondicherry Śaiva-Siddhānta bundle.
6. **Wayback-Machine pull** of `indica-et-buddhica.org/repositorium/` TEI tree.
7. **Lane-5-followup:** archive.org search for Pradīpa / Uddyota / Bālamanoramā / Tattvabodhinī (KSTS / Anandāśrama / Nirṇaya-Sāgara scans). User lifted the 300 MB cap; IPV-Vivṛti-Vimarśinī parts 1-3 (KSTS 60/62/65, ~100 MB) now fetchable.

## 6. Hard constraints respected (re-asserted)

- **No bulk-library mirrors.** GRETIL bulk (1.14 GB unpacked + 296 MB zip) deleted from /nas after user flag. All subsequent fetches per-URL, slug-tracked, manifest-registered.
- **GitHub-compatibility:** all committed files <100 MB; largest single committed artifact is `parva_12_shanti.json` at 8.4 MB. Large binaries (PDFs, DCS dump, render PNGs, the 3.4 GB DCS gold JSONL) stay on /nas with manifest pointers.
- **`src/philosophy_ocr/` untouched.** That's the prakriya chat's lane.
- **`/nas/ucb/eeshan/prakriya/` read-only.** No writes from any lane.
- **No OCR runs.** Phase 2 hard-gated on the not-yet-present sentinel.
- **`/home`** (100% full) never touched. All work staged on /nas (83 TB free); `TMPDIR=/nas/ucb/eeshan/tmp`.
- **Opus subagents only.** No Sonnet dispatch.

End of phase.
