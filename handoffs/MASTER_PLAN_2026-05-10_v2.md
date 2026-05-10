# Master Plan v2 — 2026-05-10 18:24 UTC

Supersedes `MASTER_PLAN_2026-05-10.md` (which was written ~12:35 UTC).
Verified against: `gh pr list`, `git log site/`, in-flight agent jsonl files
under `/tmp/claude-179878/...09e05c25.../tasks/`, `handoffs/cron_log.tsv`,
`handoffs/loop_log.md`, on-disk handoff docs.

Voice: Russell-Chakrabarti register — direct, declarative, philosophically
precise, no rhetorical inflation. American English (this is now the
project-wide convention; see §6).

---

## 1. Done in this session (chronological since v1)

Verified by merged-PR list and git log on `Balbudhi/vedanta-timeline` `main`,
plus the new `Balbudhi/prakriya` repo.

Since v1 of the master plan (12:35 UTC), the following landed:

| When (UTC) | What | Where |
|---|---|---|
| 16:40 | Glossary Wave 1 merged: 30 top terms with by-school expansion + primary-source citations. | PR #2 vedanta-timeline |
| 16:51 | Tattva-vāda rename merged (Dvaita → Tattva-vāda; preserve as alias). | PR #3 |
| 16:54 | Articles UX: manifest reorganization, superseded essays hidden, word-click fix, Sanskrit-alongside-English. | PR #4 |
| 17:07 | Citation panel (separate panel) merged. | PR #5 |
| 17:20 | Hotfix: removed unresolved merge-conflict markers in `app.js`. | PR #6 |
| 17:27 | Wave-10 corpus acquisition merged: 22 archive.org PDFs (~1.08 GB) + SuttaCentral bilara-data + Ratnagotravibhāga GRETIL plain text + 22 SBATCH scripts queued. | PR #7 |
| 17:35 | Unified right-side panel (Thinker / Article / Translation / Citation / Source tabs) — supersedes #5. | PR #8 |
| 17:38 | Panel UX fixes: overflow safety, visible close button, click-outside-to-close. | PR #9 |
| 18:02 | Numbered superscript citations + secondary-source distinction + verified-flag rendering. | PR #10 |
| 18:19 | Translation tab — reading-first render, collapsible grammar, partial-text honesty + glossary word-boundary fix. | PR #11 |
| 18:22 | AI-tell + unsupported-claim audit + article-title markdown escapes. | PR #12 |
| (separate repo) | Phase α prakriya scholar-parity merged: 1370 passed / 10 failed; 25 kṛt rules + 15 luṅ rules. | PR #3 prakriya |
| (separate repo) | User's 91-commit local-push reconciliation finalized. | PR #2 prakriya merged |
| (cluster) | Churro-3B swap completed (replaces Qwen2.5-VL-72B as primary OCR engine). | `handoffs/churro_swap_handoff_2026-05-10.md` |
| (cluster) | OCR hallucination postprocess pipeline shipped (Churro → Qwen → Codex three-stage). | `handoffs/wave10_postprocess_smoke_2026-05-10.md` |
| (cluster) | 22 OCR jobs running on `mit_preemptable` queue using Churro-3B. | `handoffs/ocr_logs/` |
| (cluster) | Cron continuous-improvement loop running hourly (cron_id `5200985f`). | `handoffs/loop_log.md`, `handoffs/cron_log.tsv` |
| (cluster) | Quota wall on `/orcd/scratch` partially relieved (or worked around — Churro-3B is small enough). | implicit in OCR jobs running |

**v1's "Hard blockers" status check.** The v1 plan named three hard blockers:
1. Cluster quota — RELIEVED (or routed around: Churro-3B is much smaller than Qwen2.5-VL-72B-AWQ).
2. Phase C two-engine smoke test — SUPERSEDED by Churro pipeline; PR #1 (philosophy_ocr scaffold) still open but no longer the critical path.
3. Merge `Balbudhi/jyotish#7` (extract prakriya) — DONE (prakriya repo now has its own PRs, including the scholar-parity merge).

**v1's "Single most important DROP" status check.** v1 said the missing
continuous-improvement loop was the biggest drop. It is now running
(cron `5200985f`). RESOLVED.

---

## 2. In flight (sub-agents and background jobs)

Eight Opus sub-agents launched ~14:00 UTC, all still writing as of 14:24
local (= 18:24 UTC). Output files are large (147 KB to 1.2 MB jsonl), but
none has emitted a final user-visible report yet.

| agentId | Task | Last activity (UTC) | Output size |
|---|---|---|---|
| `abdd4163650816788` | Translation-tab redesign (reading-first, collapsible grammar, partial-text honesty, glossary word-boundary fix). **Note**: PR #11 covers most of this — agent may be doing post-merge polish or follow-up. | 18:19 | 1.22 MB |
| `ae9d4657b4eea43a8` | Phase γ meaning engine (`SemanticFeatureBundle` + dictionary integration) for prakriya. | 18:24 | 433 KB |
| `a54ecac2a6d975c32` | Source tab fix + content-mirror expansion (more primary-text PDFs/HTML reachable from the panel). | 18:22 | 413 KB |
| `a08852a5a21b661ee` | AI-tell + accuracy audit at Sanskrit-grammarian standard. **Note**: PR #12 covered an initial pass — this agent may be the deeper continuation. Has emitted at least one `end_turn`. | 18:22 | 553 KB |
| `a02cdab88142fdc7d` | Modesty-acknowledgment audit + acquisition wishlist + Codex hunt (Japanese, German, EFEO, Taishō, BDRC, Bannañje 5–9, Pandurangi). | 18:24 | 272 KB |
| `af2156b0507447600` | OCR pipeline architecture critique. Has emitted at least one `end_turn`; may be near complete. | 18:20 | 267 KB |
| `a0834513ee3468331` | Public/private corpus split + secondary-engagement workflow. **This is the canonical owner of the new two-tier rule.** | 18:24 | 222 KB |
| `a7eedf069d1b8cdd3` | Glossary Wave 2 finalization (the 26 remaining terms after Wave 1 shipped 30; per-term Codex jobs already dispatched per `cron_log.tsv`). | 18:22 | 147 KB |

**Open PRs:**
- `vedanta-timeline#1` — `philosophy_ocr` package + 3-engine SBATCH. Open since 15:47 UTC. **No longer critical path** (Churro pipeline is operational without it). Decide: merge as scaffolding, or close as superseded by the Churro shell pipeline.

**Background workers:**
- 22 SLURM jobs on `mit_preemptable` running Churro-3B OCR over wave-10 PDFs.
- Cron `5200985f` — hourly continuous-improvement loop (last tick logged at 17:30 UTC, merged PR #7).
- Per-term Codex glossary Wave-2 dispatchers (anatta, catuṣkoṭi, paramārtha-satya, pratyakṣa, viśeṣa, syād-vāda, pratītya-samutpāda, spanda, pratyabhijñā, svalakṣaṇa — 10 of 26 dispatched per `cron_log.tsv`; 16 still queued).

---

## 3. Pending tasks not yet dispatched

Drawn from explicit user asks across this session that have neither a
completed deliverable nor an active in-flight agent.

1. **Two-tier corpus rule formalization in `CLAUDE.md`.** The user just
   established this rule (public primary / private secondary). Until
   `a0834513ee3468331` lands its writeup, the rule is not yet codified
   in the project conventions doc. After the agent reports, the main
   agent must add the tier definitions to `CLAUDE.md` so future
   sub-agents inherit it automatically.

2. **American-English standardization** — Deliverable 2 of this brief
   (in progress; see §6).

3. **Russell-Chakrabarti register baseline.** No formal style sheet
   exists for the register. The AI-tell audit (PR #12) is the closest
   proxy, but the user's stated baseline (Russell-Chakrabarti — clean
   declarative philosophical prose) is not yet pinned. Pending: short
   style sheet in `docs/STYLE_REGISTER.md` (or analogous) that
   sub-agents read.

4. **Mass `quoted_by` continuation wave.** Phase 1 covered 13 priority
   thinker files. Remaining ~110 thinker JSONs still carry
   `primary-text-not-in-corpus` flags without `quoted_by` arrays. Not
   currently dispatched.

5. **Full-translation parity (real Pāṇinian-rich translations).** ~30+
   works still show "full translation not yet generated." Codex-dispatch
   workflow has not been queued. The new translation-tab UX (PR #11)
   honestly acknowledges partial coverage; producing the actual
   translations is the next wave.

6. **UX missing-text flag.** `source_status: primary-text-not-in-corpus`
   is present on 50+ thinker JSONs but the front end may or may not
   surface it post-#8. Spot-check needed; if not surfaced, small
   `app.js` patch.

7. **Sāṃkhya / Yoga / Pūrva-Mīmāṃsā more-thinkers acquisition.** Still
   unaddressed. Under-represented schools have only 1–2 thinkers each.

8. **Anirban full-corpus closure.** 6 paywalled papers, *Nanobrain*
   book, Medium essays, YouTube transcripts. User-action needed (email
   draft to Anirban). Main agent should produce the draft.

9. **French primary editions of Deleuze / Derrida / Foucault / Levinas
   / Meillassoux.** Spanish translations on disk; French originals
   still missing.

10. **IIT-Delhi `linux-sanskrit-toolchain` integration with prakriya.**
    Acquisition plan exists (`lipikar_acquisition_plan_2026-05-10.md`);
    integration plan still TBD. May be subsumed by Phase γ meaning
    engine in due course.

11. **Maharaj OUP monographs** (Medhananda *Vivekananda* 2018, *Sri
    Ramakrishna* 2022). User-provision required.

12. **Curley *Spinoza*, Garrett *Nature and Necessity*, Goldenbaum,
    Lærke *Leibniz lecteur de Spinoza*, Olivelle *Upaniṣads*, Halbfass,
    Torella, Rukmani.** Still in unfetched tier.

---

## 4. The two-tier corpus rule (public primary / private secondary)

This is a HARD rule the user set in this session. The owning agent
(`a0834513ee3468331`) is in flight; its forthcoming deliverable is
canonical. Until then, the working understanding the main agent should
preserve is:

- **Public corpus** = primary texts in original language, ancient/medieval
  commentaries, edited critical editions whose copyright permits public
  display. These live in `site/data/sources/`,
  `site/data/full_translations/`, `site/data/perspectives/source/`,
  `site/data/articles/source/` and their JSON manifests. Reachable from
  the website's right-side panel.
- **Private corpus** = modern secondary scholarship (Maharaj,
  Medhananda, Halbfass, Garrett, Lærke, Curley, etc.), copyrighted PDFs
  acquired for engagement. These should NOT appear on the public site.
  They live outside the `site/` git tree (e.g.,
  `materials/secondary/...`) and are referenced only in private
  engagement notes (`engagements/...`) for the user's own reading.
- **Secondary-engagement workflow** = the user reads private secondary
  texts; sub-agents may extract claims from them in `engagements/`
  notes; only public primaries are quoted on the public site.
- **Site = public-only.** Nothing copyrighted-secondary surfaces on
  https://balbudhi.github.io/vedanta-timeline/.

The agent's writeup is expected to give exact directory layout, the
manifest schema for "this is a private secondary text we've engaged
but won't display," and the exact CLAUDE.md addition. Main agent
should read that report when it lands and update CLAUDE.md.

---

## 5. American-English standard for new English content

Authoritative for this project from now:

- **Spelling** — American: `analyze`, `color`, `center`, `defense`,
  `realize`, `behavior`, `program`, `meter`, `organize`, `recognize`,
  `theater`, `traveler`, `labor`, `favorite`, `honor`, `rumor`. Not:
  `analyse`, `colour`, `centre`, `defence`, `realise`, `behaviour`,
  `programme`, `metre`, etc.
- **Word choice** — `while` (not `whilst`), `among` (not `amongst`),
  `toward` (not `towards`), `forward` (not `forwards`), `learned` (not
  `learnt`), `gotten` where natural.
- **Punctuation** — Oxford / serial comma. Periods and commas inside
  quote marks (American convention) when the quoted text is integrated
  into the sentence; for direct primary-source citations preserve the
  cited edition's punctuation exactly. Double quotes (not single) for
  primary direct quotation; single quotes for nested.
- **Exemptions** — Sanskrit / IAST / Devanāgarī / German / French /
  Latin / Pāli text is preserved verbatim. Author names, publishing
  house names, and titles in any language are preserved verbatim.
  Block-quote primary-source passages (any language) are preserved
  verbatim down to spelling — a British author's "colour" stays
  "colour" in the quoted block.

The first standardization sweep (Deliverable 2 of this brief) covers
existing prose; from this point forward sub-agents writing new English
content default to American.

---

## 6. Russell-Chakrabarti register baseline

Working description, to be formalized in a style sheet later:

- **Russell** — declarative, plain, sentences earn their length. No
  filler. Disagreements stated and defended, not insinuated. Technical
  terms used precisely; if a term needs gloss, glossed once and reused.
- **Arindam Chakrabarti** — Sanskrit-philological precision plus
  English clarity. Sanskrit / Pāli technical terms preserved (IAST) and
  glossed once with parenthetical English; later uses leave the term
  bare. Engages opposing positions as live philosophical claims, not
  curiosities. Citations dense; primary sources foregrounded.
- **No-go register markers** — "It is interesting to note that...",
  "fascinating", "rich tradition", "vibrant", "tapestry",
  "perhaps the most striking", AI-tell hedges ("In essence, ...",
  "It's worth noting that ...", "Ultimately, ...").
- **No-go content moves** — collapsing technical terms to one-word
  English (`guṇa` ≠ "quality"; `nirguṇa` ≠ "without qualities";
  `mithyā` ≠ "false / illusory"); treating any school's metaphysics as
  a metaphor for some other school's; "non-Vedāntin" as a category;
  "the Eastern view"; presenting Madhva as "dualism" without the
  endonym; gods-as-symbols flattening of Mīmāṃsā.

The AI-tell audit (PR #12) operationalized part of this. Pinning a
fuller style sheet is a §3 pending item.

---

## 7. Sequencing constraints

Hard ordering, derived from technical and content dependencies:

1. **Two-tier corpus rule writeup → CLAUDE.md update.** Until the rule
   is in CLAUDE.md, sub-agents may inadvertently mix public and
   private corpus material. Block this on `a0834513ee3468331`.

2. **Meaning engine (`SemanticFeatureBundle`) → bulk corpus cleanup.**
   The user explicitly sequenced this: meaning-engine pipeline maturity
   first, then mass-clean of OCR'd corpus through it. Don't dispatch a
   "clean every OCR'd PDF through the prakriya engine" wave until
   Phase γ stabilizes.

3. **English content standard → multilingual content.** American-English
   pass + register baseline first, then expansion to other languages
   (German Hegel / Schopenhauer, French Deleuze / Derrida, Sanskrit
   primary translations). Don't redo German content until English is
   the stable target.

4. **`quoted_by` continuation → full-translation parity.** Quoted-by
   arrays anchor every metaphysical claim to a specific primary
   passage; that anchoring is the input to per-passage translation
   work. Cover the corpus with `quoted_by` first.

5. **OCR throughput stabilization → full-translation parity for
   OCR'd-only works.** For thinkers whose primaries we only have via
   OCR, cleaning OCR is upstream of translation.

6. **Glossary Wave 2 finalization → glossary citation backfill.** Wave
   2 expands; citation backfill comes after expansion lands.

---

## 8. Risks and collisions among in-flight agents

1. **Agent `a0834513ee3468331` (corpus split) and existing
   `site/data/` layout.** If the agent decides any current-public
   content should be private (e.g., a fair-use snippet from a modern
   secondary work), there will be deletions in `site/data/` along with
   refactor of `materials/`. Coordinate via PR; don't auto-merge.

2. **Agent `ae9d4657b4eea43a8` (Phase γ meaning engine) and prakriya
   `main`.** Phase α landed at 1370 / 10. Phase γ adds
   `SemanticFeatureBundle` — a new public surface. May break dependent
   imports in `philosophy_ocr.lexical_verifier` and
   `prakriya.ocr_api`. Main agent should run prakriya tests before
   merging.

3. **Agents `a08852a5a21b661ee` (AI-tell deeper pass) and
   `a02cdab88142fdc7d` (modesty audit) both rewrite English prose
   across `data/articles/source/` and `data/perspectives/source/`.**
   Last-writer-wins on overlapping files. American-English pass
   (Deliverable 2) also touches the same files. Recommend serializing:
   land American-English pass first (mechanical substitution, low
   conflict risk), then let the audit agents rebase.

4. **Agent `a54ecac2a6d975c32` (Source tab + content mirror) and the
   primary-text manifest (`data/primary_text_manifest.json`).** May
   add or shift entries; cross-check with the corpus-split agent's
   public/private decisions.

5. **Cron continuous-improvement loop (`5200985f`).** Could push to
   `main` while a feature agent is mid-PR. Already happened during the
   v1 → v2 window (autopush commits intermixed with merges). Risk is
   low (autopush is data-only; agents work on branches), but worth
   monitoring.

6. **OCR SLURM jobs vs cluster quota.** 22 jobs concurrent on
   `mit_preemptable` — preemption events are expected; jobs should
   checkpoint. If a wave fails silently, Churro outputs may be
   incomplete; postprocess pipeline (Churro → Qwen → Codex) catches
   most but not all hallucination.

---

## 9. Single ordered roadmap (next 24–48 h)

This is the order in which the orchestrator / cron should pick tasks.

1. **Land American-English pass.** PR `feature/american-english-pass`.
   Mechanical, low-conflict, broadens the substrate for everything
   that follows. (In progress in this session as Deliverable 2.)
2. **Wait on `a0834513ee3468331` to land its public/private corpus
   split writeup, then update `CLAUDE.md` with the rule.** Block
   downstream agents on the rule landing.
3. **Land deeper AI-tell + modesty pass** (`a08852a5a21b661ee`,
   `a02cdab88142fdc7d`) once the American-English pass merges (rebase).
4. **Land Source-tab + content-mirror expansion** (`a54ecac2a6d975c32`).
5. **Land Glossary Wave 2 finalization** (`a7eedf069d1b8cdd3`); then
   dispatch the citation backfill for the 26 new terms.
6. **Phase γ meaning engine merges in `prakriya`**
   (`ae9d4657b4eea43a8`), with the test suite green.
7. **OCR architecture critique writeup acted on** (`af2156b0507447600`)
   — adjust the postprocess pipeline based on findings.
8. **Translation-tab follow-up** (`abdd4163650816788`) merges any
   post-#11 polish.
9. **Decide PR #1 (philosophy_ocr scaffold) — merge as documentation
   or close as superseded** by the Churro shell pipeline. Either way,
   stop blocking.
10. **Mass `quoted_by` continuation wave** — extend claim-grounding
    audit to the remaining ~110 thinker JSONs, in batches by school.
11. **Full-translation parity wave** — Codex-dispatch real
    Pāṇinian-rich translations for the priority-13 thinkers' top 3
    works each, then expand.
12. **UX missing-text flag** verification post-#8 (small fix if
    needed).
13. **Sāṃkhya / Yoga / Pūrva-Mīmāṃsā more-thinkers acquisition** —
    hunt + add JSON entries.
14. **Anirban / Maharaj / French / Curley / Garrett / Lærke / Halbfass
    / Torella / Rukmani acquisition** — user-action drafts plus Codex
    hunts.
15. **IIT-Delhi toolchain integration plan** for prakriya.

---

## 10. Drops verified against full-session asks

A re-scan of the user's chronologically asked items (compared against
v1's table and asks in the current brief) finds:

- v1 listed 13 drops. Of those:
  - DROP #1 (continuous-improvement loop) — RESOLVED (cron `5200985f`).
  - DROP #5 (glossary citation backfill) — IN-FLIGHT
    (`a7eedf069d1b8cdd3` for finalization; per-term Codex dispatchers
    in `cron_log.tsv`).
  - DROP #6 (`quoted_by` continuation) — STILL DROPPED.
  - DROPs #2, #7, #8, #9, #10, #11, #12, #13, #14 — STILL DROPPED.
- New asks since v1:
  - American-English standardization — IN-PROGRESS (Deliverable 2 of
    this brief).
  - Russell-Chakrabarti register baseline — IN-PROGRESS (proxied by
    PR #12; full style sheet pending).
  - Two-tier corpus rule — IN-FLIGHT (`a0834513ee3468331`).
  - Master-plan refresh — IN-PROGRESS (this document).

**Single biggest still-dropped ask:** `quoted_by` mass continuation
(remaining ~110 thinker files). Without this, the citation infrastructure
(now well-built UI-side) is unevenly populated.

---

*End of v2 master plan. 2026-05-10 18:24 UTC.*
