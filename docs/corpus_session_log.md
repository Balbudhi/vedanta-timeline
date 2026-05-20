# Corpus session log

Tracks the corpus-chat (sibling to prakriya-chat) sessions on rnn.ist.berkeley.edu.
Each session block: timestamp, lanes touched, what landed, what's next.

---

## Session 2026-05-19 — kickoff (corpus chat)

**Operator:** corpus chat (Opus, claude-opus-4-7).
**Sibling:** prakriya chat (tmux session `prakriya`) — compiler + philosophy_ocr lane.
**Mandate:** four parallel lanes — direct-ingest, external-ingest, digitization-prep, audit.

### Ground state observed

- `/home` 100% full (469M free). All work staged under `/nas/ucb/eeshan/`.
- `~/vedanta-timeline` checked out on `feature/ocr-pipeline`; `data/sources/sanskrit/` (52 files) lives on `origin/main`.
- `~/vedanta-timeline` worktrees created under `/nas/ucb/eeshan/corpus_worktrees/{direct-ingest,external-ingest,digitization-prep,audit}`, each on its own `corpus/<lane>-2026-05-19` branch off `origin/main`.
- Sibling-owned: `src/philosophy_ocr/` (prakriya chat owns; do not touch); `/nas/ucb/eeshan/prakriya/` (read-only for this chat).
- Digitization sink: `/nas/ucb/eeshan/digitization_queue/` created.
- `TMPDIR=/nas/ucb/eeshan/tmp` for all temp work.

### Dispatched (in parallel, all Opus)

- **Lane 1** direct-ingest: 30+ plain-text Sanskrit primaries + BhG → tokenize/normalize via `prakriya.ocr_api` → per-verse JSON under `data/ingested/`.
- **Lane 2** external-ingest: DCS/TITUS/Muktabodha/Indica-et-Buddhica/IA/Vedic Heritage/DSAL/GRETIL/SARIT → `data/external_ingest_manifest.json` + easy-fetch into `data/external/<source>/`.
- **Lane 3** digitization-prep: download 12 priority PDFs to `/nas/ucb/eeshan/digitization_queue/`; build per-work metadata; update `docs/ACQUISITION_PATHWAYS.md` §A status; §B 267-text inventory. **NO OCR runs.**
- **Lane 4** audit: thinker engaged_works[] completeness, CORPUS_EXPANSION_v2 vs v1 punch-list, `data/full_translations/*.md` malformed-flag pass.

### Constraints (re-asserted to each lane)

- NEVER touch `src/philosophy_ocr/`.
- NEVER write to `/nas/ucb/eeshan/prakriya/`.
- NEVER start OCR runs (Phase 2 gated on grammar engine + ground-truth validation).
- Opus only for subagents; never Sonnet.
- One feature branch per lane; PRs to be opened at user's discretion.

### Lane 4 — landed (2026-05-19, ~7 min wall)

**Branch:** `corpus/audit-2026-05-19` pushed; commits `406f520` (audit script), `98e556a` (4 markdowns).

**Outputs:**
- `scripts/audit_corpus.py`
- `docs/audit_thinker_engaged_works_2026-05-19.md`
- `docs/audit_corpus_expansion_v2_punch_list_2026-05-19.md`
- `docs/audit_full_translations_2026-05-19.md`
- `docs/audit_external_source_followup_2026-05-19.md`

**Scope audited:** 165 thinkers, 52 Sanskrit source files, 70 full_translations.

**Schema correction recorded:** field is `source_status` (not `primary_text_status` as the mandate phrased it); stub-equivalent values are `primary-text-not-in-corpus` and `degraded-on-disk`.

**Key findings:**
- 11 thinkers have empty `engaged_works[]` (all Western/modern: Bergson, Deleuze, Derrida, Foucault, Gebser, Leibniz, Levinas, McGilchrist, Medhananda, Prigogine, Anirvan).
- 265 engaged-work entries are stubs; 253 lack any on-disk / translation / ingested linkage.
- 70 full_translations checked: **only 10 pass all four layers**; 53 missing Devanāgarī, 14 missing commentary reference, 12 carry honest-acknowledgment-stub markers.
- v2 punch-list: 4 must-author thinkers (`rambhadracharya`, `rangaramanuja`, `bannanje-govindacharya`, `chandrashekhara-bharati`) — three have near-variant IDs already on disk; ID-reconciliation decision needed before authoring.
- 19 free-URL texts identified for Lane-2 follow-up (mostly archive.org).

**Top-5 highest-leverage gaps:**
1. `rambhadracharya` (the blind ācārya) — must-author next pass; *Śrīrāghavakṛpā-Bhāṣyam* corpus acquirable.
2. Vidyāraṇya *Vivaraṇa-Prameya-Saṅgraha* — degraded-on-disk; 2005 Dvivedī PDF is a one-shot replacement (Lane 3 acquires).
3. Bannañje *Sarvamūla* mirror — unlocks five priority-12 + ~30 §B.1 works in one operation.
4. The four-layer contract is failing across >75% of `data/full_translations/`.
5. v2 ID-variant reconciliation (`rangaramanuja-muni` vs `rangaramanuja`; `bannanje` vs `bannanje-govindacharya`).

### Lane 2 — landed (2026-05-19, ~16 min wall)

**Branch:** `corpus/external-ingest-2026-05-19` pushed; 5 commits (`3fde8bf` DCS, `56ca5a8` GRETIL, `533fb91` SARIT, `dc7a4a4` registry READMEs, `29a6f5a` manifest).

**Pulled (1.86 GB total, staged on /nas, gitignored):**
- **DCS** (CC BY 3.0) — `OliverHellwig/sanskrit@04e0778` shallow clone, 720 MB. CoNLL-U + DCS MISC keys (`LemmaId`, `OccId`, `Unsandhied`); compound members carry `Case=Cpd`. SCHEMA.md committed.
- **GRETIL** (usage-with-attribution) — `1_sanskr.zip` 296 MB → 3 741 files / 1.14 GB unpacked. README inventories 30 priority Sanskrit primaries across Vyākaraṇa/Mīmāṃsā/Nyāya/Vaiśeṣika/Sāṃkhya/Yoga/Vedānta/Buddhist/Kashmir-Śaiva/Vedic.
- **SARIT** (CC BY) — 10 TEI XMLs (~20 MB) committed: Vākyapadīya, Pātañjala-Yogaśāstra, Vātsyāyana Nyāya-Bhāṣya, Siddhānta-Kaumudī, Tantra-Vārttika, Nyāya-Mañjarī, Padārtha-Dharma-Saṃgraha, Sarva-Darśana-Saṃgraha, Tattva-Vaiśāradī, Pramāṇa-Vārttika-Vṛtti. (`sarit-pm` endpoint was 502; GitHub mirror used.)

**Manifest-only (registered, not fetched):**
- Internet Archive — 20 slugs registered (Mahābhāṣya Kielhorn, Anandāśrama Kāśikā, KSTS Pratyabhijñā-Vimarśinī, Naiṣkarmya-Siddhi, Pañcapādikā-Vivaraṇa, etc.); explicit non-overlap with Lane 3's priority-12.
- TITUS — Rigveda Padapāṭha, Atharvaveda, Taittirīya-Saṃhitā, Sāmaveda URLs.
- Vedic Heritage Portal — SPA scraping route documented.
- DSAL — Apte + Macdonell URLs (Cologne preferred for bulk XML).

**Blocked:**
- Muktabodha — registration required (`fetch_method: manual_registration_required`).
- Indica et Buddhica — server ECONNREFUSED 2026-05-19.
- DSAL bulk XML — publisher restriction.

**Lane 1 / prakriya cross-validation hand-offs:**
- Consume DCS conllu corpus first (lemma + morphology gold).
- GRETIL `1_sanskr/6_sastra/1_gram/pmbhassu.htm` (Mahābhāṣya 6.4 MB) + `panini_u.htm` as Witness B against SanskritDocuments witness.
- SARIT `bhartrhari-vakyapadiya.xml` and `bhattojidiksita-siddhantakaumudi.xml` extend witness layer C.

**Manifest:** `data/external_ingest_manifest.json` — 9 sources, 67 text entries, `already_in_corpus` flag set per text vs `data/sources/sanskrit/`.

### Lane 1 — landed (2026-05-19, ~22 min wall)

**Branch:** `corpus/direct-ingest-2026-05-19` pushed; 10 commits (pipeline + 8 category batches + manifest).

**Ingested:** 51/51 input files in `data/sources/sanskrit/` → 52 per-work JSONs (gautama-nyaya-sutra kept alongside aksapada-nyaya-sutra as a duplicate edition pending dedup decision). **63 287 verses / ~1.58M approx tokens.** Manifest at `data/ingested/_manifest.json`.

**Structure recovered: 34/52 works.** Six segmenters: `verse_marker`, `numbered_prefix`, `comma_dotted`, `pipe_inline`, `parenthetical_marker`, `prose_paragraph` (fallback). Remaining 18 are bhāṣyas left at paragraph granularity; sūtra-anchored re-segmentation is a Lane-4 / Codex follow-up.

**Normalization:** `indic-transliteration` 2.3.82 installed to `/nas/ucb/eeshan/tmp/pylocal`; every verse carries both `sanskrit_devanagari` and `sanskrit_iast`.

**⚠ Cross-chat note for prakriya-chat:** `prakriya.ocr_api.tokenize` is NOT usable on rnn. `prakriya/panini_prakriya/conflict.py` uses `@dataclass(slots=True)` which requires Python 3.10+; rnn ships 3.8/3.9. Lane 1 used `tokenizer = "fallback_whitespace"` (whitespace + danda). prakriya-chat needs to either (a) drop `slots=True` from that dataclass or (b) provision Python ≥ 3.10 on rnn for the ocr_api entry points to be importable here.

**TODO recorded in manifest:** `~/Dev/Gita/` BhG JSON is local-machine-only, not on rnn; ingest deferred until the directory is sync'd.

**Lane-4 follow-ups embedded as caveats per JSON:**
1. `sharma-advaitasiddhi-vs-nyayamrta.json` is misfiled — actually B.N.K. Sharma's *secondary English* scholarship under `data/sources/sanskrit/_kashmir_saivism/`. Decide: move out, or keep with secondary marker.
2. `annambhatta-tarka-sangraha-dipika.json` interleaves mūla + Dīpikā + Bālapriyā at prose-paragraph; re-segment by `ants_NXY`.
3. `gautama-nyaya-sutra.json` vs `aksapada-nyaya-sutra.json` — same text, dedupe.
4. `spanda-karika.json` — ascription contested (Vasugupta vs Bhaṭṭa Kallaṭa); provisionally `bhatta-kallata`.
5. Šaṅkara BSB, Vāchaspati Bhāmatī, Rāmānuja Gītā-Bhāṣya / Vedārtha-Saṃgraha, Jayatīrtha Nyāya-Sudhā, Vyāsatīrtha Tarka-Tāṇḍava, Kumārila Śloka-Vārttika, Sucaritamiśra — all prose-paragraph; need sūtra-anchored re-segmentation.

### Lane 2 — corrective scope policy (2026-05-19, user-flagged over-pull)

**Issue:** Lane 2's brief was too broad. The agent mirrored the full GRETIL Sanskrit zip (1.14 GB unpacked, 3 741 files) when the project only engages ~30 specific files. User flagged.

**Action:**
- Deleted `data/external/gretil/1_sanskr/` (1.14 GB) and `1_sanskr.zip` (296 MB) from `/nas`. Files were already gitignored — no history rewrite needed.
- Rewrote `data/external/gretil/README.md` with the revised policy: fetch only files appearing in `engaged_works[]`, priority-12, or v2 punch-list. Commit `c32bfb3` pushed.
- **DCS dump (720 MB) retained** — autonomous-drive Lane 6 explicitly consumes it as the morphology gold for prakriya cross-validation.
- SARIT 10 specifically-picked TEI files (20 MB) retained — those were targeted, not bulk.

**Standing rule going forward:** No bulk-library mirrors. Per-file fetch only, slug-tracked, manifest-registered. The project-relevant external subset is on the order of **~50-100 MB total**, not gigabytes.

### Lane 3 — landed (2026-05-19, ~25 min wall)

**Branch:** `corpus/digitization-prep-2026-05-19` pushed; 15 commits.

**Priority-12 PDFs:** 9/12 acquired (1.6 GB total at `/nas/ucb/eeshan/digitization_queue/<slug>/source.pdf`):
- Baladeva *Govinda-Bhāṣya* (58 MB, 364 pp, heavy bleed)
- Bhāskara *BSB* (74 MB, 268 pp, moderate)
- Citsukha *Tattva-Pradīpikā* (220 MB, 412 pp, clean)
- Jayatīrtha *Tattva-Prakāśikā* (904 KB, 328 pp, text-PDF — **edition unverified**)
- Madhusūdana *Gūḍhārtha-Dīpikā* (479 MB, 1052 pp, Gambhirananda Sanskrit+English, clean)
- Madhva *Gītā-Tātparya-Nirṇaya* (11 MB, 371 pp, Prahlādācar 1987)
- Sureśvara *Bṛhadāraṇyaka-Vārttika* (46 MB, 968 pp, Anandāśrama 3-vol)
- Sureśvara *Taittirīya-Vārttika* (195 MB, 225 pp, clean — **recommended Phase-2 dev target**)
- Vidyāraṇya *Vivaraṇa-Prameya-Saṃgraha* (480 MB, 946 pp, 2005 Dvivedī critical, clean)

**Deferred (3) + print-only (1):**
- A.6 / A.8 Madhva *Gītā-Bhāṣya* + *Nyāya-Vivaraṇa* — Bannañje Sūtra-Prasthānam sub-volume needs hand-ID on Madhwapracharavedike index (Google Sites; not API-scrapable). 3 candidate items ruled out.
- A.4 Jayatīrtha — edition unverified; PDF is text-PDF-shaped, not a scan.
- A.11 Vedānta-Deśika *Śatadūṣaṇī* — print only; metadata.json carries Amazon ASIN B00KIT4Q3U for Chaukhamba purchase.

**§B inventory:** `data/digitization_queue_267.json` — 66 entries across 10 baskets, P0/P1/P2 priority via `data/thinkers/*.json` engaged_works cross-reference. (P0=0 because no work hits n≥3 engaged_works threshold; P1=35; P2=31.) Remaining ~200 §B "etc." entries deferred — need institutional-catalogue harvest (Muktabodha, Adyar Library Series, Madhwapracharavedike).

**Doc update:** `docs/ACQUISITION_PATHWAYS.md` — per-entry status line under §A.1..A.12, compact §A status table, §B per-basket summary table.

**Tool-stack notes:**
- No system `pdfinfo` / `pdftoppm` — used `pypdf` + KB/page heuristic for visual-quality proxy.
- `internetarchive` package not pre-installed; installed `--user` to `~/.local/bin/ia` and used curl fallback. PATH not modified globally.

### Autonomous-drive mode — Lanes 5/6/7/8 dispatching

All original lanes 1-4 complete. User issued autonomous-drive directive (no-wait, four parallel Opus subagents):
- **Lane 5** — unblock external blockers (Muktabodha via IA mirror; Indica-et-Buddhica retry; DSAL→Cologne; GRETIL Aṣṭādhyāyī commentary stack as per-file fetches).
- **Lane 6** — wire DCS → prakriya cross-validation gold (`dcs_morphology_gold.jsonl`). Produces on /nas; PRs the wire-up; never writes into `/nas/ucb/eeshan/prakriya/`.
- **Lane 7** — digitization specs (per-work `digitization_specs/<slug>.json`) on the 9 acquired PDFs. Waits on `prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md` sentinel before any OCR.
- **Lane 8** — author missing thinker.json entries from Lane 4's v2 punch-list. Branch `corpus/expansion-2026-05-19`.

No-bulk-mirror rule binding on all lanes. All Opus subagents.

### Lane 7 — landed (2026-05-19, ~6 min wall)

**Branch:** `corpus/digitization-specs-2026-05-19` pushed; commit `6610f23`.

**Sentinel state:** `/nas/ucb/eeshan/prakriya/docs/PHASE_1_COMPLETE_2026-05-19.md` **absent**. Lane 7 ran in spec-build-only mode; no OCR invoked; `src/philosophy_ocr/` untouched. `docs/PHASE_2_OCR_GATED.md` records the gate state.

**Output:** all 9 priority-12 work specs at `data/digitization_specs/<slug>.json` + `_summary.json` + per-slug README + p1–p5 PNGs at 200 DPI on /nas (gitignored, 1.8–21 MB/slug). Builder `scripts/build_digitization_spec.py` uses PyMuPDF + PIL + numpy.

**Spec contents:** sha256, file size, page count + dims, text-layer vs image-scan + embedded-DPI estimate, page-3 visual heuristic (mean intensity / edge density / skew), normalized `quality_class`, structural expectations, ground-truth-comparator lookup against Lane 1's ingested manifest, phase2_run_plan at 30 pp/hr on `sched_mit_sloan_gpu_r8`.

**Lane-3 vs Lane-7 quality reclassifications:** heuristic agreed on 7/9. Two soft band-1 disagreements (TUBV, vidyaranya); Lane 3's class retained as authoritative. Initial p1 false-positive `heavy_bleed` on title pages was fixed by switching to p3 scoring.

**OCR-readiness ranking (1=easiest, recommended Phase-2 progression):**
1. `suresvara_taittiriya_varttika` — 225 pp, clean, 7.5 h. **Confirmed Phase-2 dev target.**
2. `bhaskara_brahma_sutra_bhasya` — 268 pp, moderate, 8.9 h.
3. `citsukha_tattva_pradipika` — 412 pp, clean, 13.7 h.
4. `vidyaranya_vivarana_prameya_sangraha` — 946 pp, clean, 31.5 h.
5. `madhusudana_gudhartha_dipika` — 1052 pp, clean, 35.1 h.
6. `madhva_gita_tatparya_nirnaya` — 371 pp, text_pdf (edition-unverified).
7. `jayatirtha_tattva_prakashika` — 328 pp, text_pdf (edition-unverified).
8. `baladeva_govinda_bhasya` — 364 pp, heavy bleed + Hindi anvaya rows.
9. `suresvara_brhadaranyaka_varttika` — 968 pp, moderate bleed, three-text Anandāśrama layout.

**Comparator finding:** zero overlap between the 9 priority works and Lane 1's 52 ingested texts — validates that these works genuinely need OCR (none of them are already-clean-digital).

### Policy correction (2026-05-19, user-clarified)

- **No 300 MB cap on Lane 5** — that was my over-restriction. Removed for Lane 9 and any future lanes.
- **GitHub-compatibility binding for committed artifacts:** individual file <100 MB hard, <50 MB soft. Plain-text Sanskrit (incl. full MBh) commits to the repo. Large binaries (PDFs, DCS dump, render PNGs, large JSONL gold) stay on /nas with manifest pointers.
- **Mahābhārata added** — Lane 9 dispatched: Bhandarkar critical edition per-parva, source HTML + clean text + per-verse JSON committed (~15-25 MB total, comfortably under limits).

### Lane 8 — landed (2026-05-19, ~11 min wall)

**Branch:** `corpus/expansion-2026-05-19` pushed; 10 commits.

**§A — must-author = all already authored under id-variants.** Lane 4's audit checked v2-id strings against on-disk filenames and missed the spelling variants. All 4 v2 targets already exist with full v2-recommended engaged_works:

| v2 id | Existing file | works covered |
|---|---|---|
| `rambhadracharya` | `ramabhadracarya.json` | 5/5 |
| `rangaramanuja` | `rangaramanuja-muni.json` | 6/6 |
| `bannanje-govindacharya` | `bannanje.json` | 6/6 |
| `chandrashekhara-bharati` | `candrasekhara-bharati.json` | 3/3 |

Lane 8 added each v2-id to the existing file's `alternate_names` (e.g., `"rambhadracharya (v2-id-variant)"`) — non-breaking, lineage cross-refs preserved. No file renames (would chase 100+ `lineage_in/out` references).

**§B — 8 thinkers enriched (18 new engaged_works):** caitanya +2, madhva +4, nimbarka +2, vidyaranya +1, madhusudana +3, appayya +2, vyasatirtha +1, manavala-mamunigal +2. (`vedanta-desika` no-op — split already present.)

**§C — Western/modern (11 thinkers, 16 entries):** format precedent pulled from `heidegger.json` / `whitehead.json` (genre=monograph, non-Sanskrit language, ascription_tier=securely-authored). Single batch commit.

**Schema:** all 165 thinker files JSON-parse clean. New entries use spec-compliant enums (`ascription_tier ∈ {securely-authored, traditionally-ascribed, school-ascribed, disputed}`; `entry_status="draft"`; `source_status="primary-text-not-in-corpus"`). No biographical claims fabricated.

**Recommendation:** update Lane 4's `audit_corpus.py` to recognise id-variants via an alias map (lower-risk than renaming 4 files and chasing lineage refs). Filed as next-wave follow-up.

### Lane 5 — landed (2026-05-19, ~14 min wall)

**Branch:** `corpus/external-unblock-2026-05-19` pushed; 4 commits. **131.6 MB total fetched** (under the now-rescinded 300 MB cap; rule respected before the user lifted it).

- **(a) Muktabodha → egangotri/archive.org:** 7 KSTS PDFs (77.2 MB) for engaged Kashmir-Śaiva works — Tantrāloka, Paramārtha-Sāra, Tantrasāra, IPV pt.1+2, Pratyabhijñā-Hṛdayam, Śiva-Sūtra-Vimarśinī. PDFs gitignored, sha256 in manifest. Muktabodha registration deferred; `data/external/muktabodha/REGISTRATION.md` records the path.
- **(b) Indica-et-Buddhica:** site reachable (Lane 2's ECONNREFUSED was transient), but the operator restructured: `.org → .com` and `/repositorium` + `/textus` TEI paths now 404. `STATUS.md` records the diagnosis + Wayback / GitHub-mirror / contact-publisher recovery routes.
- **(c) DSAL → Cologne:** all 4 zips fetched (33.9 MB) — MW XML + text, Apte XML + text. MW zips >10 MB gitignored; Apte zips small enough to commit in-repo. README documents SLP1 schema vs prakriya's bundled lexicon.
- **(d) GRETIL per-file:** 31 files (20.3 MB). Aṣṭādhyāyī three-witness stack (Pāṇini A + Patañjali B + Kāśikā C + Laghu-Siddhānta-Kaumudī) + 25 engaged-works plaintexts across Vasubandhu, Dharmakīrti, Candrakīrti, Nāgārjuna, Asaṅga, Dignāga, Abhinavagupta, Kṣemarāja, Utpaladeva, Vasugupta, Bhartṛhari, Jaimini, Maṇḍana-Miśra, Vācaspati, Udayana. 2 GRETIL 404s (Vākyapadīya split, Tantra-Vārttika pt.2) — re-probe next session.

**Manifest:** `data/external_ingest_manifest_lane5.json` — 55 entries (42 fetched, 2 failed, 8 manifest-only, 1 archived-unavailable, 2 GRETIL 404). Tooling: `scripts/fetch_lane5.py` (per-URL, 1 req/s/host throttle, sha256, manifest emit) + per-task plans under `scripts/lane5_plans/`.

**Follow-ups for next wave:**
- Archive.org search for Pradīpa / Uddyota / Bālamanoramā / Tattvabodhinī (KSTS / Anandāśrama / Nirṇaya-Sāgara scans) — needed to complete Pāṇinian layer-C.
- Wayback-Machine pull of the legacy `indica-et-buddhica.org/repositorium/` TEI tree.
- Muktabodha registration → IFP-Pondicherry Śaiva-Siddhānta bundle (unique; no archive.org backup).
- Optional: IPV-Vivṛti-Vimarśinī parts 1-3 (KSTS 60/62/65, ~100 MB total) — engaged work, manifest-only this run; user lifted the cap so this is now fetchable in a follow-up.

### Lane 6 — landed (2026-05-19, ~15 min wall)

**Branch:** `corpus/dcs-gold-2026-05-19` pushed.

**Gold artifact (on /nas, outside repo):**
- `/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl`
- **5 688 416 tokens / 3.4 GB** — 15 900 CoNLL-U files across 270 distinct works.
- sha256 `9a6e7cb155aa19a32c8b1af95de7a586f4abda2ea9ccaa8efa3c73f87bdc1215`. Build wall clock 338 s.

**Per-kind counts:** subanta 2.86M · indeclinable 1.03M · compound_range 1.02M · compound_member 792k · tinanta 524k · krdanta 484k.

**Gaṇa resolution: 27.05 %** (129 002 / 476 859 tinanta tuples). The remaining 73 % are genuinely gaṇa-ambiguous lemmas in prakriya's bundled dhātupāṭha (`vac` ∈ {2,10}, `hf` ∈ {1,3}, `as` ∈ {1,2,4}…) or out-of-inventory roots. Leading-upasarga stripping pass handles compound roots like `udDf`, `pravac`, `samanuSI`.

**Top-10 corpus coverage:** Mahābhārata 1.35M tokens · Rāmāyaṇa 307k · Suśrutasaṃhitā 181k · Ṛgveda 179k · Śatapathabrāhmaṇa 166k · Liṅgapurāṇa 157k · Matsyapurāṇa 152k · Skandapurāṇa-Revākhaṇḍa 138k · Kathāsaritsāgara 135k · Aṣṭāṅgahṛdayasaṃhitā 130k.

**Wire-up artifacts (committed):**
- `scripts/build_dcs_morphology_gold.py` (re-runnable, no args)
- `data/dcs_morphology_gold/README.md` · `sample.jsonl` (first 50 rows) · `coverage_report.json`
- `docs/dcs_morphology_handoff_2026-05-19.md` — PR-style brief for prakriya-chat with integration sketch + caveats + §A.4 acceptance plan.

**For prakriya-chat:**
1. Tuple shapes match `cross_validate_tinanta_fixture.json` / `krdanta_vidyut_gold.json` exactly: `[root_slp1, gana, lakara, purusha, vacana, pada]` · `[root, krt, linga, vibhakti, vacana]` · `[stem_slp1, linga, vibhakti, vacana]`.
2. `require_gana=True` for the §A.4 ≥99% pass — subset is 129k tinanta rows, statistically ample.
3. ~8% krdanta rows have `krt=null`; skip.
4. `Voice=Pass → pada=atmanepada + prayoga=karmani` standard; ~1-3% may diverge.
5. 96% of DCS unsandhi'd forms carry `UnsandhiedReconstructed=True`; treat surface-roundtrip divergence as soft.
6. The prakriya repo was not modified (read-only by mandate); the handoff sketches the `scripts/cross_validate_vidyut.py` diff but does not land it.

### Lane 9 — landed (2026-05-19, ~8 min wall)

**Branch:** `corpus/mahabharata-2026-05-19` pushed; 8 commits.

**Source verified:** GRETIL per-parvan files (`mbh_NN_u.htm`) — per-file header attests "Electronic text © Bhandarkar Oriental Research Institute, Pune, India, 1999" on the Tokunaga/Smith digitization. **This is the Bhandarkar Critical Edition.** Encoding is IAST (despite the `_u.htm` suffix; not SLP1).

**Ingested: all 18 parvans, 73 898 verses** (matches canonical ~74k for the BORI CE constituted text + folded apparatus):
Ādi 7208 · Sabhā 2402 · Vana 10324 · Virāṭa 1829 · Udyoga 6070 · Bhīṣma 5412 · Droṇa 8157 · Karṇa 3874 · Śalya 3317 · Sauptika 774 · Strī 731 · Śānti 12873 · Anuśāsana 6542 · Aśvamedhika 2745 · Āśramavāsika 1064 · Mausala 274 · Mahāprasthānika 107 · Svargārohaṇa 195.

**Sizes (all GitHub-compatible):**
- Source HTML + cleaned text: ~18 MB committed.
- Ingested JSON (IAST + Devanāgarī per verse): ~25 MB.
- Largest single file: `parva_12_shanti.json` at 8.4 MB. No splits needed.

**Tokens:** ~1.23M whitespace-tokens (Sanskrit morpheme count would be ~1.8M; whitespace keeps compounds whole — same `tokenizer: "fallback_whitespace"` convention as Lane 1). Apparatus passages (`*NNNN_LL`) and variants (`@NNN_LL`) folded onto the constituted verse-id; downstream signal: `pada_count > 2`.

**Blocker:** `data/thinkers/vyasa.json` does not exist. Existing `vyasa-bhasya.json` is the Yoga-Sūtra-Bhāṣya author. Lane 9 declined to author Vyāsa (mandate-scoped to ingest, not thinker-authoring); flagged for a Lane-8-followup to add Vyāsa with `engaged_works[] = [mahabharata]`, `ascription_tier: "traditional-multi-author"`.

**Cross-corpus join opportunity:** Lane 6's DCS gold tags the Mahābhārata at 1.35M tokens. The join (DCS lemma+morphology ↔ Lane 9 verse JSON) is one script — both keyed on `(parva, adhyāya, verse)`. This is the first translation-engine training-pair candidate end-to-end.

### All 9 lanes closed. Writing CORPUS_PHASE_COMPLETE_2026-05-19.md next.
