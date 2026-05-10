# Master Plan — Session-wide audit, 2026-05-10

Audit performed by Opus sub-agent against the live session
`09e05c25-9cc3-495e-af08-68212ae1a525.jsonl` (6,278 lines, 2026-05-08 → 2026-05-10),
the in-flight agent pool, the open PRs, and the on-disk handoffs.

This file is the new source of truth for what the user has asked for, what is in flight,
what is done, and what has been silently dropped.

---

## 1. Session-scope user asks (chronological)

Below is every distinct user ask in this session, in chronological order, with verdict.
Voice-dictation artifacts are preserved in spirit but not verbatim.

| # | Date / time (UTC) | Ask (one-line) | Verdict |
|---|---|---|---|
| 1 | 2026-05-09 00:09 | Per-thinker pages render as raw HTML (file links, not webpages) — fix to be a real, video-mode-enabled site. | DONE (site rebuilt; index works; per-thinker pages render). |
| 2 | 2026-05-09 02:23 | Reorient: build a unified terms / perspectives reference that engages each thinker's primary terms in original language; tell user what primary texts you DO and DO NOT have; fix index page. | DONE (glossary infrastructure + thinker-by-thinker primary-text inventory in `handoffs/audit_sections/`). |
| 3 | 2026-05-09 02:42 | Sankhya: download Anirban Bandyopadhyay's papers, Nanobrain, Medium essays, YouTube — and engage seriously. | PARTIALLY DONE. 12 PDFs + 34 markdown summaries collected. Nanobrain still paywalled (user must email Anirban). Medium essays Cloudflare-blocked. Two key papers post-2022 still missing. |
| 4 | 2026-05-09 03:22 | "Status of all the tasks I gave you" — wants a consolidated to-do/status summary. | DONE recurringly via handoffs/PHASE_*.md and now this file. |
| 5 | 2026-05-09 03:25 | Switch sub-agent dispatch from broken Codex to OpenAI / fix dispatch yourself. | DONE. Codex dispatch repaired; project rule (CLAUDE.md) explicitly limits sub-agents to Codex-5.4-high or Opus. |
| 6 | 2026-05-09 03:56 | Make a list of everything to transfer; first have Opus download everything it can find online. | DONE. `handoffs/text_acquisition_report.md` (255 of 279 fetched). |
| 7 | 2026-05-09 06:13–06:19 | Don't fetch secondary scholarship for Upaniṣads (use primaries); don't read Sanskrit personally — translate everything; for missing items have Opus find OCR-able copies. Defer Sankhya engagement until sources are in. | DONE / IN-FLIGHT. Translation pass is what Wave-2/3/5 was. Acquisition for the remaining items is the OCR pipeline (in-flight). |
| 8 | 2026-05-09 ≈08:30 | Build cladogram-quality timeline UI with two views (Lanes + Network), sticky lanes, era backgrounds, color-coded by school, 133-thinker scope. | DONE. Live at https://balbudhi.github.io/vedanta-timeline/. |
| 9 | 2026-05-09 ≈10:00 | Pāṇinian-rigor Sanskrit translations (line-by-line + word-by-word with samāsa-vigraha + kāraka structure + lakāra/parasmaipada); never collapse `guṇa = quality`, `nirguṇa = without qualities`. | PARTIALLY DONE. Engaged-passage translations meet this for v1. **"Full translation" tab is the central drop** — see §6. |
| 10 | 2026-05-10 03:55 | Confirm primary-text downloads complete; site styling improved; translations everywhere. | PARTIALLY DONE — see §6 (full-translations are still acknowledgment stubs for ~30+ works). |
| 11 | 2026-05-10 04:04 | UI: scrolling broken in some panels; ensure other-school engagement (esp. Sāṃkhya / karma-as-causality) on parity with Vedānta entries; populate full-translation tab; populate more thinkers per school where possible. | IN-FLIGHT (Article-reorg agent + rigor-pass agents address parity; full-translation parity is **DROPPED** — see §6). |
| 12 | 2026-05-10 05:48 | OCR / reconstruction sources are bad; have Opus find better witnesses; never cite a text we don't have. | IN-FLIGHT (Sanskrit OCR pipeline = Phase C; secondary-citation audit done; Lipikar acquisition plan written). |
| 13 | 2026-05-10 06:19 | Stop framing schools as "non-Vedāntin"; engage on each school's own terms; acknowledge degraded sources rather than hiding them; don't waste tokens OCR-ing what's already lost — find better copies. | DONE on framing. OCR strategy resolved by Phase C plan (better copies + multi-engine OCR + Pāṇinian validator). |
| 14 | 2026-05-10 06:31 | Mīmāṃsā article: externalization is a school of practice (not failure / not consciousness-decline); engage Francis Clooney; merge Hegel main + secondary into single readable Hegel article (not too much German). | DONE. Mīmāṃsā Perspective v4 delivered + symbolism-shift Perspective written. Clooney engagement added. Hegel merged + extended past first 10 pages. |
| 15 | 2026-05-10 06:41 | Don't weaken anything; keep working on Mīmāṃsā (v4 → v5 if needed); apply same depth across all entries. | IN-FLIGHT (Mīmāṃsā v5 not yet started; depth-of-engagement audit ran; Mīmāṃsā Perspective is now the canonical visible article — superseded versions hidden). |
| 16 | 2026-05-10 06:45 | Articles list missing many existing essays (Spinoza, Leibniz, etc.); duplicate Mīmāṃsā showing; remove redundant top-bar "redo" button; set up a continuous looping job to add sources / improve translations / hunt factual inaccuracies / strip AI-voice. | DONE on listing & dedup (Articles Reorganization agent in flight finishes the rest). Looping continuous-improvement job is **PARTIALLY DROPPED** — there is no scheduled cron / loop currently active; manual autopush only. |
| 17 | 2026-05-10 07:01–07:12 | Avoid superficial readings; engage *all* of the German text on Hegel (not just first lines); apply Spinoza-level rigor to every timeline entry; for missing primaries have Codex hunt; UI must acknowledge gaps where text is missing. | IN-FLIGHT (Rigor-pass for 5 clusters all DONE; depth-audit DONE; Hegel-extension DONE. Acknowledgment-on-UI requires the citation panel — IN-FLIGHT). |
| 18 | 2026-05-10 13:26 | "Why did you stop working — what is done? Did you do everything?" | This audit answers it. |
| 19 | 2026-05-10 13:45 | Don't insert placeholders; honestly acknowledge what we don't have; clarify what "perspective" thing means. | DONE. 12 placeholder full_translations replaced by honest stubs. Perspective layer documented. |
| 20 | 2026-05-10 14:28 | Hunt Indian universities / sampradāya publishers / libraries for missing primaries. | IN-FLIGHT (`missing_sources_acquisition_report.md` + `lipikar_acquisition_plan_2026-05-10.md` cover this). |
| 21 | 2026-05-10 14:35 | Even for thinkers we have primaries for, every metaphysical claim must cite a primary passage that the reader can open via the citation number. | IN-FLIGHT. Backend done (claim-grounding audit added `quoted_by` arrays to 13 priority files). UI side = the **citation panel** (in-flight). Mass conversion of remaining ~85 thinkers TBD. |
| 22 | 2026-05-10 14:46 | (Auto context-summary message — restated the project constraints.) | n/a. |
| 23 | 2026-05-10 14:48–14:51 | Use the user's GitHub `jyotish` (or its OCR engine) for OCR. Confirm `jyotish` exists as private repo; if its grammar engine is incomplete, finish + optimise; use cluster GPUs + good vision models; allow OCR to feed translations. | IN-FLIGHT. `Balbudhi/jyotish` confirmed private. Grammar engine extracted to new `Balbudhi/prakriya` repo (PR #7 jyotish-side awaits review; prakriya repo has 840 tests passing). OCR pipeline (`philosophy_ocr` package) scaffolded as PR #1 in vedanta-timeline. Phase C smoke test BLOCKED on cluster quota — see §4. |
| 24 | 2026-05-10 14:54–15:01 | Move grammar engine to its own lowercase repo (`prakriya`); plan-and-walk-me-through changes before making them; optimise for cluster + vision models; finish the grammar engine to "scholar-team replacement" quality. | DONE (extraction). End-state plan IN-FLIGHT (Sanskrit-compiler-end-state-plan agent). |
| 25 | 2026-05-10 16:16 | Why "Dvaita" not the school's own name (Tattva-vāda)? Make exonym fix across all schools. Add citations for every glossary entry. Add a right-side panel with Source/Citation tabs to read primaries while reading articles; make the design choice fit existing aesthetic. | IN-FLIGHT — Tattva-vāda rename agent + Other-school exonym audit DONE; Glossary expansion 4-of-30 done (26 pending Codex output); Citation panel UX redesign agent IN-FLIGHT. |
| 26 | 2026-05-10 16:28 | Use IIT-Delhi Sanskrit Linux toolchain (Lipikar etc.) to reach scholar-team-replacement OCR + translation quality. | IN-FLIGHT (Lipikar plan DONE; toolchain survey IN-FLIGHT). |
| 27 | 2026-05-10 16:29 | This audit task. | IN-PROGRESS — this document. |

---

## 2. In-flight sub-agents

The 9–10 background Opus agents launched but not yet completed at audit time. All wrote
output to `/tmp/claude-179878/-orcd-home-002-eeshan-philosophy/09e05c25-9cc3-495e-af08-68212ae1a525/tasks/<agentId>.output`.
None has completed yet (output files all show only the spawn header — 139 bytes).

| agentId | Description | User-ask covered | Status | Output file | Fallback if it dies |
|---|---|---|---|---|---|
| `ae807ef9a3a0cd02e` | Phase C resume — two-engine smoke (Surya + Qwen2.5-VL-72B-AWQ) | #23 (OCR pipeline first GPU run) | Running. **Hard-blocked on quota**: scratch ≈150 GB / pool fileset cap; venv install fails at ~4 GB. Spawned 12:21 UTC. | `…/ae807ef9a3a0cd02e.output` | Re-dispatch with explicit user-approved cleanup of axiom-coder/lean-cp-corpus on scratch (≥80 GB needed). |
| `abbcec4d962abbd27` | Tattva-vāda rename audit (Dvaita → Tattva-vāda across 2,790 string occurrences in 242 JSON / 77 MD files) | #25 | Running. 12:22 UTC. | `…/abbcec4d962abbd27.output` | Re-dispatch with reduced scope (one tier at a time: thinkers → glossary → articles). |
| `a1dc434e22fa7ef34` | Glossary by-school expansion + citation backfill (30 terms) | #25 (citations on glossary) | Running. 4 of 30 terms done by Codex; 26 pending. | `…/a1dc434e22fa7ef34.output` | Re-dispatch the 26 pending Codex jobs individually if dispatcher stalls. |
| `abb21527ad9fe4074` | Citation panel UX redesign (right-side panel, Source / Citation tabs) | #21, #25 | Running. Design doc landed at `handoffs/citation_panel_design.md`; implementation pending. | `…/abb21527ad9fe4074.output` | Re-dispatch with explicit branch name `feature/citation-panel`. |
| `ad8c0c477667858d1` | Other-school exonym audit (28 schools) | #25 | Running. Audit doc landed at `handoffs/school_name_exonym_audit.md`; rename actions still TBD per school. | `…/ad8c0c477667858d1.output` | Re-dispatch only the schools that need rename. |
| `ab3924a0a646efce3` | Push prakriya scholar-parity forward (finish grammar engine to "team-of-scholars" quality) | #24 | Running. 12:24 UTC. | `…/ab3924a0a646efce3.output` | Re-dispatch with explicit module list (sandhi, kāraka, lakāra, samāsa). |
| `a8e4f0e32e2977058` | Article reorganization + rewrite + UX (5 sections; hide Mīmāṃsā v1–v4; tighten subtitles; strip "redo" button; fix scroll) | #11, #16 | Running. Audit landed at `handoffs/articles_audit.md`; PR work TBD. | `…/a8e4f0e32e2977058.output` | Re-dispatch with the audit doc as input — only the implementation step remains. |
| `ab563dd5524b29d87` | Sanskrit compiler end-state plan (what does the engine look like once done?) | #24, #26 | Running. 12:27 UTC. | `…/ab563dd5524b29d87.output` | Re-dispatch with current `Balbudhi/prakriya` HEAD as starting point. |
| `a976419d63ec4bb5d` | Lipikar + Linux Sanskrit toolchain survey | #26 | Running. Acquisition plan landed at `handoffs/lipikar_acquisition_plan_2026-05-10.md`; toolchain survey itself still TBD. | `…/a976419d63ec4bb5d.output` | Re-dispatch with the acquisition plan as input — survey + integration plan only. |
| `a8473bf877bc1efa7` | Master-plan audit of session (this document) | #27 | DONE — this file. | `…/a8473bf877bc1efa7.output` | n/a. |

**Recently completed (last hour):**
- Replace placeholder full_translations with honest stubs → DONE.
- Comprehensive acquisition-pathway research → DONE (`missing_sources_acquisition_report.md`).
- Claim-grounding audit (priority 13 thinker files) → DONE.
- Clickable-citation infrastructure (backend + UI + prose conversion) → DONE.
- 5 rigor-passes (Advaita 28 / Vaiṣṇava 45 / Trika+Śaiva+Śākta 18 / Comparator+Buddhist+Jain 36 / Modern 6) → DONE.
- Perspectives layer + Mīmāṃsā Perspective entry → DONE.

---

## 3. Open PRs awaiting review

| PR | Title | Branch | What it does | Merge verdict |
|---|---|---|---|---|
| **`Balbudhi/jyotish#7`** | Extract Sanskrit grammar engine to `prakriya` repo | `extract-prakriya` | Moves 117 src + 30 test + 63 doc files (128 commits preserved via `git filter-repo`) to new private repo `Balbudhi/prakriya`. Updates jyotish CLI to import from `prakriya.*`. **840 tests pass in prakriya, 72 in jyotish.** | **READY TO MERGE.** Blocks #1: `philosophy_ocr.lexical_verifier` calls `prakriya.ocr_api`, so vedanta-timeline #1 cannot run end-to-end until prakriya is on PyPI or referenced as a git submodule. |
| **`Balbudhi/vedanta-timeline#1`** | Add `philosophy_ocr` package + SBATCH for 3-engine OCR pipeline | `feature/ocr-pipeline` | Adds `philosophy_ocr` (config, pdf_render, three engine runners, consensus aligner, lexical verifier, Codex judge, ingest emitter, typer CLI) + sbatch + 5 unit tests (all pass via `PYTHONPATH=src`). | **HOLD until smoke test passes.** Phase C blocked on cluster quota; smoke test (Bhāskara p.50) still pending; agent's user-side test plan checkbox unticked. Once smoke passes, merge. |
| `Balbudhi/prakriya` (new repo, no PR yet) | n/a — bootstrap commit `f1044ca` is the initial state on `main`. | n/a | New private repo for the Pāṇinian grammar engine. | n/a — repo is independent. |

**No open PRs on `Balbudhi/vedanta-timeline` other than #1.**

---

## 4. Storage / cluster state

Quota snapshot at audit time (2026-05-10 ≈12:31 UTC):

| Filesystem | Used | Quota | Avail | Notes |
|---|---|---|---|---|
| `/home/eeshan` (NFS, hard cap 200 G) | **168 G** | 195 G soft / 200 G hard | 27 G grace | 758k of 1000k inodes used. **Tight.** |
| `/orcd/scratch/orcd/009/eeshan` | **≈148 G** | undocumented per-user ≈150 G | **negligible — venv install fails at +4 GB** | Hidden NFS-server quota — `quota -s` doesn't see it. |
| `/orcd/pool/008/eeshan` | **441 G / 1024 G** | 1 TB soft cap, but fileset-quota blocks small writes near 437 G | 583 G `df` headroom but **un-writable** | Hidden fileset quota also undocumented. |

**Imminent walls:**

1. **Scratch is the choke point.** Two-engine OCR venv (Surya + Qwen2.5-VL-72B-AWQ) needs ≈ 50–55 G total (venv + models). Three-engine (adds InternVL-2.5-78B-AWQ) needs another ≈45 G. Today, **neither fits** without reclaiming ≥ 80 G.
2. **Home is 27 G off the hard cap.** Any new agent that writes large files into `/home/eeshan/philosophy/` risks tripping the hard cap and locking the home tree.

**Required user decision** (from `PHASE_C_PROGRESS.md`):
- Approve deletion of one or more on scratch:
  - `axiom-coder/` (89 GB total: hf_model_mirror 22 G, lean-lake-cache 34 G, datasets 30 G).
  - `lean_cp_corpus_raw/` (32 GB).
  - `semanticist/` (17 GB).
- OR raise scratch quota via ORCD ticket (1–3 day turnaround).
- OR run the two-engine smoke only (saves ≈45 G but still needs ≈ 50 G headroom).

---

## 5. Risks / collisions

Concurrent parallel agents and PRs that may step on each other:

1. **Glossary expansion + Tattva-vāda rename + Exonym audit all touch `site/data/glossary/*.json`.** The glossary expansion agent is rewriting per-term JSON; the Tattva-vāda rename agent is doing string-replace across the whole `site/data/` tree. **If both write the same file in any order, last-writer-wins.** Mitigation: serialise — let Tattva-vāda finish first (string-replace; idempotent), then glossary expansion (semantic edits). Currently both running in parallel.
2. **Article reorganization + Citation panel UX both touch `assets/app.js`.** Article-reorg adds glossary tagger to `renderMarkdownFull`, removes "redo" button, renames sections, adjusts scroll. Citation panel adds new DOM/event-handler code + CSS classes. Likely conflicts: `renderMarkdownFull`, click-delegation around line 1262, z-index hierarchy. Mitigation: merge Article-reorg first (smaller surface), rebase Citation panel.
3. **`vedanta-timeline` autopush + parallel agents committing to `main`.** Eight autopushes happened in a 30-minute window (PUSHED 565b090, 2d3422b, 3ea521f, 034851c, e23c746, 2239e0c, 50188b1, 941c38a, 984e7ab, 06be9b6, 02eaa81). Parallel agents may all try to push to `main` and collide; the autopush process appears to be working OK but is racing. Mitigation: switch parallel-write agents to feature branches; let autopush only watch `main`.
4. **`Balbudhi/jyotish#7` is blocking `Balbudhi/vedanta-timeline#1` end-to-end.** `philosophy_ocr.lexical_verifier` imports from `prakriya.ocr_api`; the jyotish PR is the canonical extraction. Until #7 merges (or `prakriya` is published), the vedanta-timeline OCR pipeline is non-runnable. **No agent has assumed #7 is merged**, but the smoke-test agent will discover this when it tries to import.
5. **`prakriya` extraction has not had a code review.** It's a 1-shot Codex extraction with 840 tests passing — but it's a massive surface (117 src + 30 test + 63 docs files). Worth at least a smoke review before merging #7.
6. **Sanskrit-compiler-end-state-plan agent vs. push-prakriya-scholar-parity agent.** Both are about the prakriya repo. Plan agent should write spec; push-parity should implement. If push-parity races ahead without the spec, the engine may grow in a direction the plan would have chosen against. Mitigation: park push-parity until plan lands.

---

## 6. Dropped or incomplete asks

These are asks where the user said "do X" and currently nothing is doing X (no in-flight agent, no queued task, no completed deliverable that fully satisfies the ask):

1. **DROP — Continuous-improvement looping job.** Ask 16 (2026-05-10 06:45): *"have a looping job where you're constantly adding sources or working on translation or working on extracting and making sure everything has no factual inaccuracies or you got better job of representing everyone's views."* The autopush loop is purely a git-push watchdog; there is **no scheduled / looping content-improvement agent** running. There was no `/loop` or `cron` invocation in this session. **This is the single most important DROPPED ask.**

2. **DROP — Full translations parity.** Asks 9, 10, 11. Pāṇinian-rigor full translations were promised for every primary work in the corpus. Today: (a) engaged-passage translations exist via the `quoted_by` infrastructure for ~13 priority thinkers; (b) **the "Full Translation" tab on the website still says "full translation not yet generated" for almost all works**; (c) 12 fabricated-placeholder full-translations were just replaced by honest acknowledgment stubs, but no replacement workflow has been queued to actually produce real ones. Codex / Opus dispatch for full-text Pāṇinian-rich translations is **not running**.

3. **DROP — Frances Clooney / Mīmāṃsā engagement deepening (v5).** Ask 14–15: user asked to deepen Mīmāṃsā with Clooney engagement and to keep going to v5 if v4 still has weaknesses. Mīmāṃsā Perspective (symbolism-shift) is the visible canonical article, and Clooney was added to v4. **No v5 dispatch.** This may be acceptable — Perspective v1 is already the canonical visible essay — but the user explicitly said "keep working on it until just good as it can be."

4. **DROP — Wave 9 acquisition completion check.** A wave-9 acquisition log exists (`handoffs/wave9_logs/acquire.log`) but the most recent activity is in the past, and no agent has reported a final tally for "what archive.org PDFs got OCR-ready and what's still PDF-only." Subsumed under the Phase C OCR pipeline once that unblocks.

5. **DROP — Citations from glossary entries to primary text.** Ask 25: every glossary entry should have citations. Wave-1 covered 4 of 30 terms; the remaining 26 prompts are written and queued but Codex dispatch hasn't progressed. **No agent is currently working through the queue.**

6. **DROP — Mass `quoted_by` audit.** Claim-grounding audit covered 13 of 133 thinker files (priority list). The remaining ~110 files still carry `primary-text-not-in-corpus` flags without `quoted_by` arrays. The agent explicitly listed this as "out of scope for this pass" — needs a continuation wave.

7. **DROP — UX acknowledgement of missing texts.** Ask 17: the UI should *show* the user when a thinker's primary text is missing. The `source_status` flag was added to thinker JSONs (50+ flags across 18 Trika/Śaiva files alone) but the **UI does not yet surface these flags to the reader.** No agent is owning this. Likely a small `app.js` patch.

8. **DROP — Scrolling fix.** Ask 11: user could not see the whole karma article on his computer; said panels should scroll. Article-reorg agent is in flight and may handle this, but it's not explicitly in that agent's brief.

9. **DROP — Sāṃkhya / karma engagement parity.** Ask 11: user pointed out karma was being read narrowly through Vedānta and asked for a Sāṃkhya-rooted account of causality and a serious rebuild of under-represented schools (Sāṃkhya, Yoga, Mīmāṃsā, etc., where there are only 1–2 thinkers). The rigor-passes added depth on existing entries but did not add new thinkers per under-represented school. **No active acquisition agent for Sāṃkhya / Yoga / Pūrva-Mīmāṃsā more-thinkers.**

10. **DROP — Anirban full-corpus closure.** Ask 3: 6 paywalled Anirban papers, the *Nanobrain* book, Medium essays, and YouTube transcripts are still missing. Email to Anirban (suggested in `handoffs/anirban_user_provisions_needed.md`) has not been sent.

11. **DROP — Daniel Garber / Melamed / Lærke / Macherey / Garrett / Curley acquisition.** Ask 6: many of these are now on disk (`completion_pass_report.md`), but Curley *Spinoza*, Garrett *Nature and Necessity*, Goldenbaum, Lærke *Leibniz lecteur de Spinoza*, Olivelle *Upaniṣads*, Pollock *Rasa Reader*, Halbfass, Torella, Rukmani are all still in the unfetched tier. (User already deferred Pollock as secondary; the rest remain.)

12. **DROP — Maharaj OUP monographs.** Two by Swami Medhananda (Vivekananda 2018, Sri Ramakrishna 2022). Already flagged in `text_acquisition_report.md`. User must provide.

13. **DROP — French primary editions of Deleuze / Derrida / Foucault / Levinas / Meillassoux.** Spanish translations downloaded; French originals still missing. The Hegel article work used German originals; the Deleuze article does **not** currently use the French originals.

14. **DROP — IIT-Delhi `linux-sanskrit-toolchain` integration with `prakriya`.** Ask 26: integrate IIT-Delhi tools (Saṃsādhanī, parsers, etc.) with the prakriya engine. Toolchain survey is in flight; **integration plan is not.**

---

## 7. Master plan going forward

### Hard blockers (must complete before anything else moves)

1. **Cluster quota.** User must approve scratch cleanup or quota-raise ticket. Without this, OCR pipeline (= every downstream Sanskrit translation improvement) is stuck. Estimated unblock: 1 hour with user approval.
2. **Phase C two-engine smoke test.** Pre-requisite for merging vedanta-timeline #1. Estimated 1–2 hours after quota unblocks (model download on `mit_data_transfer` partition is immediate; smoke test on `sched_mit_sloan_gpu_r8` queues to ≤ 2026-05-12 17:07).
3. **Merge `Balbudhi/jyotish#7`.** User code review needed. Without this, `prakriya` is not a public dependency for the OCR pipeline. ~30 min user-time.

### Independent parallel tracks (move without waiting)

A. **Articles UX track** (one agent owns this): finish article reorganisation, add side-by-side Sanskrit / English convention, remove redo button, fix scrolling, ship article-reorg PR.

B. **Citation infrastructure track**: complete the right-side citation panel implementation; ensure `cite://` resolves correctly; add the missing-text UI flag; mass-extend `quoted_by` to remaining ~110 thinker files (continuation of claim-grounding audit).

C. **Glossary track**: finish the 26 remaining Codex glossary expansions; backfill citations for every term per school.

D. **School-name endonym track**: finish exonym audit + rename for the schools where verdict was EXONYMIC-FLATTENING (the audit doc lists each).

E. **OCR + grammar engine track**: Phase C smoke → Phase D scale-out → grammar engine end-state plan → integrate IIT-Delhi toolchain.

F. **Acquisition track**: hunt missing primaries (Maharaj, Anirban paywalled, French originals, Curley/Garrett/Lærke etc.); produce per-source pathway notes.

G. **Continuous-improvement loop**: stand up a `/loop` or `cron` job to keep an Opus agent running on accuracy-audit / register-fix / new-thinker-acquisition while the main agent sleeps. **Currently missing.**

H. **Full-translation parity track**: produce real Pāṇinian-rich full translations for the 30+ works whose tab still reads "not yet produced". This is a multi-week Codex / Opus dispatch.

### Sequencing dependencies

- E depends on the three hard blockers above. Until OCR works, F's "find better OCR copies" pathway is blunted.
- B's citation panel, A's articles UX, and the website autopush race for `assets/app.js` and `assets/style.css`. Serialise: A → B.
- C and D both edit glossary / school metadata; do them sequentially: D (rename) → C (expansion + citations).
- G should be set up early — every other track benefits from continuous improvement.

---

## 8. Recommendations to the main agent

### Tasks the main agent should mark completed but hasn't
- Articles inventory + audit (DONE on disk; agent can move to "implementation" sub-task).
- Tattva-vāda rename audit doc (DONE on disk; rename action still TBD).
- Lipikar acquisition plan (DONE; mark "research" complete, move to "execution").
- Anirban corpus collection (12 PDFs + 34 markdown notes; flag as DONE with `provisions_needed.md` outstanding).
- 5 rigor-passes (all DONE).
- Replace fabricated full_translations with stubs (DONE).
- Claim-grounding audit (DONE for the 13 priority files; mark "Phase 1 complete; Phase 2 = remaining 110 files" and re-dispatch only Phase 2).

### Tasks the main agent should re-dispatch because the original agent died or stalled
- **Phase C OCR smoke (`ae807ef9a3a0cd02e`)** — re-dispatch *after* user approves scratch cleanup. Don't re-dispatch into the same quota wall.
- **Glossary expansion Wave-2 (Codex)** — 26 of 30 terms pending; re-dispatch the 26 individually.

### New agents that should be dispatched for dropped asks
- **Continuous-improvement loop (`/loop` skill, 30–60 min interval)**: pick a stale article, run `simplify` + a register-audit, push fix; pick a stale `quoted_by`-missing thinker, run claim-grounding audit, push fix; pick a stale "not yet produced" full-translation, dispatch Codex.
- **Full-translation generation Wave**: per-work Codex dispatch with Pāṇinian-rich translation prompt template; start with the 13 priority thinkers' top 3 works each.
- **`quoted_by` continuation Wave**: extend claim-grounding audit to the remaining 110 thinker JSONs.
- **UX missing-text flag**: small `app.js` agent — surface `source_status: primary-text-not-in-corpus` in the thinker detail pane.
- **Sāṃkhya / Yoga / Pūrva-Mīmāṃsā more-thinkers acquisition**: hunt for additional thinkers in under-represented schools and add JSON entries.
- **Anirban email draft + send**: human action; main agent should produce the draft and put it in front of the user for one-click send.

### Tasks that should be cleaned up / merged / deleted
- Mīmāṃsā v1, v2, v3, v4 markdown files: hidden in manifest; consider archiving to `site/data/articles/source/_superseded/`.
- All `wave_*_logs/*_lastmsg.txt` files older than 24 h: archive.
- Outdated Monitor watchdogs (`bergnnxem`, `bmssmgbk8`, `b2p296gtk`, `blv52ipjz` are all sequential autopush re-arms — only the latest is needed). Cancel the inactive ones.
- `MASTER_STATUS.md` (older than this file's audit) is stale relative to the current state of the website; either update or move to `_archive/`.

---

*End of master plan. This file is the source of truth as of 2026-05-10 ≈12:35 UTC.
The next session should read this first.*
