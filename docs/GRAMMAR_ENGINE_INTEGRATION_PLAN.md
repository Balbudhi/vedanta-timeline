# Grammar Engine Integration Plan

How the in-progress Pāṇinian grammar engine at `~/Dev/prakriya/` (repo: `Balbudhi/prakriya`) should integrate into this site when ready. Research and design only — no code lands from this document.

Source references for this plan:
- `~/Dev/prakriya/README.md`
- `~/Dev/prakriya/OPUS_BRIEF_2026-05-19.md`
- `~/Dev/prakriya/docs/MASTER_PLAN_2026-05-19.md` (esp. §B, the integration seam)
- `~/Dev/prakriya/docs/prakriya_engine_architecture.md`
- `~/Dev/prakriya/docs/scholar-parity-gaps-and-next-steps.md`
- `~/Dev/prakriya/src/prakriya/ocr_api.py` (the public seam)
- `~/Dev/prakriya/src/prakriya/panini_prakriya/` (engine internals)
- `docs/ARCHITECTURE.md` (this repo — `KeyPassage.panini_breakdown` schema)
- `assets/app.js` (consumer site, 4479 LOC, vanilla ES-module)

---

## §1 What the engine does

`prakriya` is a **Pāṇinian derivation engine in Python 3.12**, split from `Balbudhi/jyotish` on 2026-05-10. It has two complementary halves. The **generative half** (`src/prakriya/panini_prakriya/engine.py` and siblings: `angasya.py`, `vikarana.py`, `tin_pratyaya.py`, `sup_pratyaya.py`, `ac_sandhi.py`, `tripadi.py`, `subanta.py`, `lit_prakriya.py`, `lun_prakriya.py`, `karaka.py`) takes a semantic spec — root, lakāra, person, number, prayoga, or for nominals stem + liṅga + vibhakti + vacana — and produces a surface form by ordered application of Aṣṭādhyāyī sūtras, emitting a step-by-step prakriyā trace (sūtra id sequence). See `prakriya_engine_architecture.md` §"Input → Output" for the canonical example (`{√bhū, laṭ, prathama, ekavacana, kartari} → bhavati` with trace `[1.3.1, 3.2.123, 3.4.78, 1.3.9, 3.1.68, 1.3.9, 7.3.84, 6.1.78]`). The **analytic half** (`src/prakriya/ocr_api.py`) is the stable v0.1 public seam: `tokenize`, `parse_sandhi`, `lexically_resolvable`, `derive_pada`, `load_dictionaries`, plus the semantic-layer outputs `derive_meaning*` / `derive_translation_context`. The engine bundles ~29 MB of data (`src/prakriya/data/`: dhātupāṭha, gaṇapāṭha, paradigm tables, MW/Apte/Heritage/Whitney/Cologne lexicon indexes) and ~1.9 MB of TOML rule packs (`src/prakriya/panini_family_specs/`). Compiled rules total ~3,890 (per `prakriya_engine_architecture.md`).

**Current completion state (per `OPUS_BRIEF_2026-05-19.md` and `cron_state.json`):** the engine is **partial, under active coverage push**. Of the 12 Aṣṭādhyāyī clusters, clusters 2/3/4/5/6/8/10 are in flight with batches landed; cluster_9 (saṃhitā/tripādī) is paused; clusters 1 (kṛt), 7 (kāraka), 11 (svara), 12 (Vedic) are untouched. The acceptance target (`MASTER_PLAN_2026-05-19.md` §A.4) is `deferred_rules = 0`, `pytest tests/test_panini_prakriya.py` ≥ 600 passed (currently 319), and ≥99% match against `vidyut-prakriya` on the held-out cross-validation. **What it can do today:** subanta inflection for the bundled paradigms (~300 surfaces), tiṅanta for covered roots via lakāra-by-lakāra families, sandhi splits, dictionary lookup (bundled lexicon ~2k roots; external Cologne/MW/Apte/Heritage indexes are scaffolded in `ocr_api.load_dictionaries` but the XML data is not yet checked in — see `BUNDLED_LEXICON_NOTE`). **What it cannot do today:** complete kṛt derivation (cluster_1 blocked on the `vidyut_prakriya_probe` oracle path), sentence-level kāraka assignment (cluster_7 blocked on `assign_karakas` extension), accent (cluster_11), and Vedic forms (cluster_12). The semantic / translation-context layer (`semantics.py`, `lexicon.py`) has 38 passing tests but no LLM-fallback wired for polysemy yet. **No correction-proposal entry point exists** — `MASTER_PLAN_2026-05-19.md` §B.2 specifies one (`propose_correction`) that has not yet landed.

Engineering posture: Python 3.12, `uv`-managed venv, ~600+ pytest tests, regression-gated cluster apply loop driven by Codex 5.4 (`handoffs/dispatch_cluster.sh`). The engine is **Python-only**; there is no Rust core in `prakriya` itself (it depends on the `vidyut` Python package, which wraps a Rust crate, but vidyut is consulted as an oracle / witness, not as the runtime). This Python-only fact is load-bearing for §3 and §4.

---

## §2 Why it matters for the vedanta-timeline

The site already ships hand-authored Pāṇinian breakdowns in every `KeyPassage.panini_breakdown` (`docs/ARCHITECTURE.md` §3): `pada_analysis[]`, `samasa_vigrahas[]`, `karaka_structure[]`, `verb_modality[]`. These are authored once by an LLM and frozen. The engine adds value in five concrete UI surfaces:

1. **Inline tooltips on arbitrary Sanskrit tokens, not just glossary keys.** Today, hovering `ābhāsa` inside a `core_thesis` paragraph gets a glossary popover only because the regex matches a known alias from `data/glossary/abhasa.json`. Hovering an inflected form like `ābhāsasya`, `ābhāsayoḥ`, `cidābhāsena` typically misses — the alias list cannot enumerate every case-number form. With the engine, `lexically_resolvable(token)` + `derive_pada(token)` returns the stem `ābhāsa` (so the glossary regex's coverage gap closes) and the case/number for the tooltip header line ("genitive singular of ābhāsa").

2. **Live derivation view on `key_passages`.** Currently `KeyPassage.panini_breakdown.pada_analysis[].morphology` is a hand-authored string like `"genitive singular, masculine"`. The engine can serve a **derivation trace** for the same `pada` — the actual sūtra sequence (e.g., `[4.1.2, 7.1.12, 6.1.110]`) — gated behind a "show derivation" toggle. Reader who wants to verify the analysis sees the rules. Reader who doesn't, doesn't.

3. **Samāsa-vigraha generation for compounds the author didn't pre-gloss.** `KeyPassage.panini_breakdown.samasa_vigrahas` is populated only for selected compounds. Many `core_thesis` paragraphs and `english_close` fields contain compound terms (`brahmātmaikya`, `māyāvāda-khaṇḍana`, `cidacid-viśiṣṭa`) without a vigraha entry. The engine's compound recursion (`MASTER_PLAN` §C, Phase γ.4) returns the constituent tree.

4. **Sandhi-undo + morphology display in `data/full_translations/`.** These files (`baladeva__govinda-bhasya.md`, `caitanya__shikshashtakam.md`, etc.) carry line-by-line English. Where the human author did **not** insert a word-by-word breakdown, the engine can supply one on demand from `tokenize` + `parse_sandhi` + `derive_pada`.

5. **A "grammar lab" surface.** A new route (e.g., `/lab/`) where a reader pastes an arbitrary verse and receives full Pāṇinian analysis. Concretely: `tokenize → parse_sandhi (best split) → derive_pada per token → assemble karaka_structure → emit a KeyPassage-shaped JSON the site renders with the existing breakdown component.` This is the user-facing payoff that converts the site from a fixed corpus into a verifiable reading tool against any Sanskrit text.

The **trust-model fit** is exact. The site's stated voice (README.md): "every claim should be verifiable against the cited primary text." Hand-authored breakdowns are LLM synthesis. Engine-authored breakdowns carry a deterministic sūtra trace, re-derivable from the engine version pinned in the data file. Engine output strengthens, rather than weakens, the verifiability claim.

---

## §3 Three integration architectures

### (a) Pre-baked build-time index

Run `prakriya` offline over every Sanskrit string in `data/` (every `key_passage.sanskrit_iast`, every glossary `term_iast`, every line in `data/full_translations/*.md`). Emit a single static `data/grammar_index.json` keyed by (string, token-offset). Site loads + memoizes at runtime.

- **Engineering effort:** ~3 days. A Python script in `scripts/` walks the data tree, calls `prakriya.ocr_api.tokenize` + `derive_pada` per token, writes JSON. CI re-runs on every content commit.
- **Runtime latency:** O(1) lookup, no network. Bundled JSON ~3–10 MB uncompressed for the current corpus (rough estimate: ~500 passages × ~30 tokens × ~500 bytes/token = ~7.5 MB; gzip → ~1.5 MB).
- **Infrastructure cost:** zero. Works on GitHub Pages as-is.
- **Bundle / load cost:** lazy-load the JSON only when a tooltip is invoked, or shard by thinker-id (one file per thinker, ~50 KB each).
- **Pros:** zero runtime cost, no service infra, no privacy issue, offline-capable, deterministic, audit-trail per analysis is built once.
- **Cons:** stale on content changes (mitigated by CI rebuild), **cannot analyse arbitrary user input** (kills the §2.5 "grammar lab"), rebuild cost grows with corpus, engine-version pinning required so the JSON does not drift from the engine that produced it.

### (b) Serverless API

Deploy `prakriya` as a small HTTPS service (Cloudflare Workers Python, Fly.io, Hetzner box, or a Render/Railway free-tier Python container). Site calls `POST /analyze {text: "..."}` at runtime.

- **Engineering effort:** ~1 week. Wrap `ocr_api` in a FastAPI app, containerize, deploy. Add request signing or rate-limit (the site is non-indexed but the API endpoint is public).
- **Runtime latency:** per the engine's own perf note (`prakriya_engine_architecture.md` §Performance): ~150 µs per derivation in Python, ~150 ms for 1k forms. Network round-trip dominates: 100–300 ms p95 from a US-east edge. **Cold-start risk** if hosted on a scale-to-zero platform; first request after idle can be 2–5 s for a 29 MB data load.
- **Infrastructure cost:** ~$5–10/month on a small VM with the data loaded into memory; free on Cloudflare Workers if a Pyodide port is feasible (unlikely for 29 MB of data + transformer-style dictionaries).
- **Pros:** handles arbitrary user input → enables the "grammar lab" §2.5, supports `propose_correction` once it lands (`MASTER_PLAN` §B.2), centralized engine-version pinning.
- **Cons:** the site is **intentionally non-indexed and dependency-minimal** (`README.md` + `robots.txt`). An outbound API breaks that posture — every reader hit logs to your server. Mitigation: anonymous, no logs, document the privacy contract. Also: hosting cost is small but non-zero and ongoing; if the box dies the lab feature dies.

### (c) Client-side WASM (Pyodide)

Compile / ship the engine to run in the browser. Since `prakriya` is Python, the only realistic browser runtime is **Pyodide**.

- **Engineering effort:** ~2 weeks of fighting Pyodide. The engine has ~29 MB of data + 1.9 MB of TOML + a Python dependency graph that almost certainly includes packages without Pyodide wheels (`vidyut` ships a Rust extension; `pydantic`, `lxml`, etc. exist on Pyodide but the dhātupāṭha XML pipeline may not).
- **Runtime characteristics:** Pyodide cold-start ~3–5 s (the CPython WASM runtime is ~10 MB compressed). Plus 29 MB of engine data. Plus ~5 MB of Python source. **First-derivation budget: 15–30 s** including data load. Per-derivation latency after warm: comparable to native Python.
- **Bundle size:** prohibitive for casual readers. Site currently is a thin SPA; adding 40+ MB of WASM + data violates the "intentionally lean" posture.
- **Pros:** no server, no privacy issue, works offline once cached.
- **Cons:** Pyodide cold-start, bundle size, and the dependency-port headache (especially `vidyut`'s Rust bindings) make this the **least realistic option** given a Python engine. Would become realistic if the engine were rewritten in Rust and compiled to WASM directly (the `vidyut-prakriya` Rust crate already targets this, but `prakriya` itself is Python by design — see `prakriya_engine_architecture.md` §"Why Python Is Sufficient Initially").

---

## §4 Recommended architecture: (a) primary + (b) for the lab

**Pre-bake the corpus, serverless-API the lab.** The engine is Python, the site is static, the corpus is finite and known at build time — that's exactly the shape (a) was made for. Use (b) **only** for the `/lab/` route where arbitrary user input is the whole point. Skip (c): Pyodide loses on bundle size and dependency-port effort, and would only be revisited if the engine moves to Rust.

Concretely:

- **For every Sanskrit token already in `data/`** (passages, translations, glossary aliases) → bake into `data/grammar_index.json` at build time. Lookup is O(1), no outbound traffic, GitHub Pages stays self-contained.
- **For arbitrary input from the reader** (the lab, plus any future "annotate this verse I pasted" feature) → call a serverless `prakriya` endpoint. Document this as the **one and only outbound dependency**, gated behind an opt-in UI affordance so the site's default-reading experience remains zero-network.
- **Engine-version pinning:** every cached entry in `grammar_index.json` carries a `prakriya_version` field. CI fails if the entry's version is older than the currently-pinned engine. The lab API also returns its `prakriya_version` and the site displays it next to the analysis ("derived by prakriya v0.7.2; sūtras cited resolve against Aṣṭādhyāyī standard numbering").

Justification rooted in §1: because the engine is **Python with 29 MB of data**, options (a) and (b) are realistic and (c) is not. Because the site is **deliberately lean and non-indexed**, the default surfaces should not phone home — that pushes the *primary* path to (a). Because the *value* of the lab surface (§2.5) is exactly the case (a) cannot handle, (b) earns its place as a narrowly-scoped supplement.

---

## §5 Phased rollout

### Phase 1 — Glossary inflected-form coverage (MVP)

**Engineering work.** Add `scripts/build_glossary_inflection_index.py` that, for every glossary entry's `term_iast`, calls `prakriya.ocr_api` to enumerate the case/number/gender paradigm (or the principal-parts paradigm for verbal roots) and emits `data/glossary_inflections.json` mapping every inflected form back to its `term_key`. Extend `assets/app.js`'s glossary regex to consult this map before falling back to the static alias list.

**Integration point.** `assets/app.js` — wherever the current glossary popover is summoned (search the file for the glossary-detection routine; it lives in the same code path that currently matches `aliases[]`).

**Success criterion.** A representative sample of 30 inflected forms drawn from `data/full_translations/` that *currently* miss the glossary popover all hit it after Phase 1. No regression on currently-matching aliases.

**Why this is the right MVP.** It is the **engine feature with the lowest dependency on engine completion** — subanta inflection of bundled paradigms already works in the engine today. It closes the user's already-raised regex-coverage complaint. It needs no API hosting (build-time index only). It validates the build-time pipeline end-to-end.

### Phase 2 — Inline grammar tooltips on Sanskrit tokens in `key_passages` + `articles`

**Engineering work.** Extend the build-time script to walk every `key_passage.sanskrit_iast`, every `english_close` Sanskrit term, and every Sanskrit string in `data/articles/source/*.md`. Per token, call `prakriya.ocr_api.tokenize` + `derive_pada` + bundled-lexicon lookup. Emit `data/grammar_index.json`. Add a new UI element to `assets/app.js`: a tooltip on any IAST-detected Sanskrit token (not just glossary keys) that displays the morphology + gloss from the index.

**Integration point.** New rendering layer in `assets/app.js` that wraps Sanskrit tokens in `<span data-pada-id="...">`. Tooltip component reuses the glossary-popover style for visual continuity.

**Success criterion.** Every Sanskrit token in 5 representative passages has an actionable tooltip; tokens for which the engine returns no analysis (kṛt forms still uncovered, etc.) fall back gracefully with a "not yet analyzed" affordance rather than a broken popover.

### Phase 3 — Grammar lab (`/lab/`)

**Engineering work.** Deploy a thin FastAPI wrapper around `prakriya.ocr_api` to Fly.io or Hetzner ($5/mo box, ~512 MB RAM is enough). Endpoint: `POST /analyze {text}` → returns a `KeyPassage.panini_breakdown`-shaped JSON. New route in the site at `/lab/`: textarea, "analyze" button, render output using the existing `panini_breakdown` component.

**Integration point.** New file `assets/lab.js` + new HTML page. Reuse the breakdown-rendering CSS already in `assets/style.css`.

**Success criterion.** A reader pastes a verse from outside the corpus (e.g., a Subhāṣitāvalī verse the site does not cover) and receives an analysis whose `verdict_status` (engine returns this) is `derived` for ≥80% of tokens; the remaining `unresolved` tokens flag explicitly rather than guess.

**Risk gate.** Phase 3 only ships when the engine reaches ≥99% vidyut cross-validation (`MASTER_PLAN` §A.4). Otherwise the lab is unreliable and undermines the verifiability voice.

### Phase 4 — Engine-authored breakdowns on new `key_passage` entries

**Engineering work.** When the user authors a new `key_passage`, the build pipeline calls the engine to **generate** `panini_breakdown.pada_analysis`, `samasa_vigrahas`, and `karaka_structure` (the last only once cluster_7 lands). The hand-authored breakdown becomes optional; if present, a CI step diffs human against engine and reports disagreements. If absent, the engine fills in.

**Integration point.** A new validator in the existing CI (`docs/ARCHITECTURE.md` §6 validation rules) that calls the engine and either writes the breakdown to the JSON or compares against the existing hand-authored breakdown.

**Success criterion.** A new `key_passage` can be added with only `sanskrit_iast` + `english_close` + `why_this_passage`, and the published entry has a full `panini_breakdown` from the engine. Existing entries pass an engine-vs-human diff at ≤5% morphology-tag mismatch.

---

## §6 Authoring contract

The engine must commit to the following so the site can trust its output and display it under the site's voice:

1. **Every analysis carries the sūtra sequence that produced it.** `derive_pada` and the lab endpoint return a `derivation.steps[]` field with the sūtra ids applied. The site shows them.
2. **Every analysis is independently re-derivable.** The engine version is pinned in `data/grammar_index.json` (build-time) and returned in the lab API response (runtime). A reader with the same engine version reproduces the same trace bitwise.
3. **Explicit ambiguity, never silent guessing.** When the engine cannot uniquely derive a form (multiple analyses possible, or polysemy unresolved), it returns a ranked list with confidences, not a top-1. The site renders the top-1 by default with an "alternatives" affordance — never collapses an ambiguous form into a confident-looking single analysis.
4. **Coverage is honest.** A token the engine cannot analyze returns `verdict: "unresolved"` with a category (e.g., `kṛt_not_yet_supported`, `vedic_form`, `unknown_root`). The site does not paper over these with fallback heuristics; it surfaces them as "not yet analyzed" so the reader is not misled.
5. **Sūtra numbering is the standard Aṣṭādhyāyī numbering** (book.chapter.sūtra, e.g., `7.3.84`). No internal engine ids leak into user-facing output.
6. **No remote LLM in the analysis path.** The site never displays an analysis that was produced by a black-box API call. The engine is deterministic on the analysis path; an LLM may be used during engine *development* (Codex 5.4 batches in the cron loop) but the runtime that produces the breakdowns the site renders is rule-based and re-derivable. This honors both the site's verifiability voice and the engine's own §"non-negotiable" policy (`panini-and-prakriya-index.md`).
7. **Versioned data assets.** The dhātupāṭha, gaṇapāṭha, and lexicon files have explicit version stamps. When they bump, `grammar_index.json` regenerates and the bump is noted in the site's release log.

---

## §7 Risks

| Risk | Mechanism | Mitigation |
|---|---|---|
| Engine produces a wrong analysis → ships under the site's voice. | Engine coverage is incomplete (clusters 1/7/11 untouched), so edge-case tokens can return plausible-looking but incorrect output. | Pre-author audit on every new `grammar_index.json` build; sample 50 random tokens, manual spot-check. Version-pin and require ≥99% vidyut cross-validation before Phase 3 ships. Public derivation trace on every analysis so readers can audit. |
| Engine produces too many results for ambiguous tokens → UI clutter. | Same surface form derivable from multiple roots / multiple case-number combinations. | Confidence-ranked top-1 default; "show alternatives" affordance for the rest. Engine returns confidence in `[0,1]` per `MASTER_PLAN` §B.2's `CorrectionCandidate.confidence` pattern — extend the same idea to `derive_pada`. |
| `grammar_index.json` bundle size on GitHub Pages → slow first paint. | Naive bake across whole corpus could hit ~10 MB JSON. | Shard by thinker-id (~50 KB each); lazy-load only when a tooltip is summoned on that thinker's page. Defer the grammar layer entirely behind a user gesture so the timeline view's first paint is unaffected. |
| Engine version drifts from cited primary-text editions → analyses don't match what the reader sees. | Engine pinned to one Aṣṭādhyāyī text edition; site cites passages from many editions (`KeyPassage.source_edition`). | `source_edition` is already required (`docs/ARCHITECTURE.md` §3); add a parallel `prakriya_version` + `astadhyayi_edition_id` next to it. CI flags mismatches. |
| Lab API hosting goes down → `/lab/` 500s. | Single-instance Fly.io / Hetzner box. | The lab is non-essential; degrade gracefully to "lab temporarily offline" banner. Core site (Phases 1–2 + 4) is build-time and unaffected. |
| Engine ships under-tested kṛt / kāraka after cluster_1/cluster_7 land. | Per `OPUS_BRIEF` and `MASTER_PLAN` §A.4, cluster_1 + cluster_7 are still in-flight; their first green is not their final-quality. | Gate Phase 2 inline-tooltip rollout on cluster_1 ≥ executable; gate Phase 3 lab on full vidyut cross-validation ≥ 99%. Phase 4 (auto-authored breakdowns) gates on cluster_7 + scholar-grade checklist all-green. |
| Engine privacy regression in lab API. | Lab endpoint receives raw user-pasted Sanskrit text, potentially personal commentary. | No logs by contract; document explicitly in `/lab/` page. Endpoint behind a known-good operator only. |
| Build-pipeline cost grows as corpus expands. | Each new `key_passage` re-bakes the index. | Incremental cache by `(passage_id, prakriya_version)`; only re-bake what changed since the last commit. |

