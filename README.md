# Vedānta — A Realist Tradition

**Live site:** https://balbudhi.github.io/vedanta-timeline/

An interactive timeline of Vedāntic thinkers + the schools they engage with. Each thinker has a `core_thesis` written in the Russell–Chakrabarti register, an `engaged_works` list with summaries and ascription tiers, `key_passages` with full Pāṇinian breakdown (pada-analysis · samāsa-vigrahas · kāraka structure · lakāra/parasmaipada), and lineage edges (teacher/student/polemical) to the rest of the corpus.

The site is intentionally **non-indexed** (`robots.txt` + `noindex` meta block all crawlers). Share by direct link only.

---

## Articles

Standalone essays. Open them directly in GitHub or via the **Articles** button on the live site.

- [**Hegel's Preface to the Phenomenology — and the Vedāntic parallels**](data/articles/source/hegel-preface.md) — *Substanz als Subjekt*, Aufhebung, the speculative proposition, placed against Bhartṛprapañca, Madhva, Vyāsatīrtha, Jīva Gosvāmī, Vidyāraṇya.
- [**Mīmāṃsā as externalized yogic process — re-investigation defending the Integral-Yoga thesis**](data/articles/source/mimamsa-aurobindo-v2.md) — Stronger verdict than the v1 pass: the Mīmāṃsaka apparatus has substantial interior content (Śabara on MS 1.1.2: *so 'rthaḥ puruṣaṃ niḥśreyasena saṃyunaktīti pratijānīmahe*) that the standard externalized reading underweights. Engages Clooney 2022's *Mīmāṃsā as Introspective Literature and as Philosophy*.
- [**Mīmāṃsā/Aurobindo — first investigation (v1)**](data/articles/source/mimamsa-aurobindo-v1.md) — Initial test of three precisifications (hermeneutic / structural / causal-diagnostic).
- [**Primitive Model**](data/articles/source/primitive-model.md) — Nine structural primitives (substrate-independence, mode-status, identity-relation, causation, locus-of-avidyā, *bheda*-count, epistemic-authority, *mokṣa*-state, *bhakti*-role) and the derivation table per school.
- [**Comparative-Claims Framework**](data/articles/source/comparative-claims-framework.md) — Methodology: four-verdict schema (shared-presupposition / parallel-structure / terminological-equivalence / genuine-disagreement / contested), five claim categories, anti-pattern guards.

---

## Corpus

- [**Thinker entries**](data/thinkers/) — One JSON per thinker. Vedāntic schools (Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda, Acintya-Bhedābheda, Śuddhādvaita, Avibhāgādvaita, proto-Vedānta) plus engaged-comparator schools (Sāṃkhya, Yoga, Nyāya, Navya-Nyāya, Vaiśeṣika, Pūrva-Mīmāṃsā, Jaina, Cārvāka, Mādhyamaka, Yogācāra, Buddhist-Pramāṇa, Sarvāstivāda, Theravāda, Tathāgatagarbha, Pratyabhijñā/Trika, Kashmir Śaiva-Siddhānta, Śākta Śrīvidyā/Kālīkula, Pāśupata, Pāñcarātra, Vīraśaiva, Bhairava-tantra). Cross-tradition entries for Western interlocutors and modern scholars.
- [**Extended translations**](data/full_translations/) — One markdown file per `<thinker>__<work>` pair: line-by-line English with full Pāṇinian breakdown per line.
- [**Glossary**](data/glossary/) — ~140 Sanskrit philosophical terms. Each entry has an *invariant_definition* across schools that share genuine commitments PLUS *per_school* definitions where the schools genuinely diverge. Clickable from any term-occurrence on the live site.
- [**Polemic chains**](data/polemic_chains/) — One JSON per major refutation (saptavidhānupapatti, Nyāyāmṛta arguments, Māyāvāda-Khaṇḍana, Śatadūṣaṇī, etc.). Each chain reproduces the premise → inference → conclusion structure and traces *which positions the argument actually touches and which it leaves intact*.
- [**Comparative claims**](data/comparative_claims/) — Pairwise comparisons across the corpus.
- [**Registries**](data/registries/) — `schools.json` (color tokens + palettes), `sub_schools.json`, `pramanas.json` (epistemic-source vocabulary), `sub_axes.json` (controlled vocabulary for comparative-claim sub-axes).

---

## Project documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Full schema for thinker / engaged_work / key_passage / comparative_claim. Validation rules. Dispatch waves.
- [`docs/CORPUS_PLAN.md`](docs/CORPUS_PLAN.md) — Canonical thinker list with date tiers, school assignments, lineage edges.
- [`docs/COMPARATIVE_CLAIMS_FRAMEWORK.md`](docs/COMPARATIVE_CLAIMS_FRAMEWORK.md) — Methodology document.
- [`docs/PRIMITIVE_MODEL.md`](docs/PRIMITIVE_MODEL.md) — Analytic-primitive derivation framework.
- [`docs/HEGEL_PREFACE_REPORT.md`](docs/HEGEL_PREFACE_REPORT.md) — Source of the Hegel article.
- [`docs/MIMAMSA_AUROBINDO_HYPOTHESIS.md`](docs/MIMAMSA_AUROBINDO_HYPOTHESIS.md) and [`v2`](docs/MIMAMSA_AUROBINDO_HYPOTHESIS_v2.md) — Source of the Mīmāṃsā / Aurobindo articles.
- [`docs/AUDIT_REPORT_v1.md`](docs/AUDIT_REPORT_v1.md) — Adversarial factual audit of the corpus (chronological cascade, Aurobindo language tags, lineage reciprocity).
- [`docs/TRANSLATION_AUDIT_v1.md`](docs/TRANSLATION_AUDIT_v1.md) — Translation-quality audit (line-by-line correspondence, word-by-word completeness).
- [`docs/DESIGN_REWRITE_PLAN.md`](docs/DESIGN_REWRITE_PLAN.md) — Cladogram swim-lane visual design.
- [`docs/CORPUS_EXPANSION_v2.md`](docs/CORPUS_EXPANSION_v2.md) — Modern thinkers + the Rāmabhadrācārya identification.
- [`docs/wave0_audit.md`](docs/wave0_audit.md) — Original skeleton-population audit.

---

## Methodology

The thinker entries, work summaries, key-passage selections, Sanskrit translations with Pāṇinian breakdown, and comparative-claim analyses were composed by large language models — primarily **Claude Opus 4.7** (synthesis, comparative analysis, audit) and **OpenAI Codex GPT-5.4 reasoning=high** (primary-source extraction, Sanskrit transcription, morphological analysis) — working from primary Sanskrit texts on disk and from the standard scholarly editions cited in each entry.

The intent is to allow novel engagement with the tradition: to render every thinker on his own ground, in his own grammar, with citations to specific loci that an English-only reader can verify. Where the tradition is preserved only in citations by later authors (Auḍulomi, Āśmarathya, Kāśakṛtsna, Bodhāyana, Upavarṣa, Sundara-Pāṇḍya, Brahmadatta), the entry says so, and explains how the academic tradition derives the dating estimate.

Every claim should be verifiable against the cited primary text. Where you find a misreading, a missing citation, or a gloss that flattens what the thinker actually says, treat it as a defect of the AI synthesis, not a feature of the tradition.

---

## Site code

- [`index.html`](index.html), [`assets/style.css`](assets/style.css), [`assets/app.js`](assets/app.js) — vanilla HTML / CSS / ES-module JS. No build step. No framework. The cladogram is fully deterministic from `school_color_token` (lane), `sub_school_shade` (sub-lane), and `dates_low/high` (x-position).

---

## Hosting

Deployed via GitHub Pages from `main` branch root. Custom domain not configured; the `balbudhi.github.io/vedanta-timeline/` path is canonical.
