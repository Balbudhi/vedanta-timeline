# Integral Realism Research Project Plan

Created: 2026-06-18

This organizes the pasted voice note into a working project for `vedanta-timeline`. It is a planning artifact, not a published thesis page. The standard for eventual site changes remains: primary-source grounded, explicit uncertainty markers, no flattening of real disagreements, and no reader-facing claims that outrun sources.

Follow-up consolidation files:

- `docs/INTEGRAL_REALISM_SOURCE_LEDGER.md` records what is already in the public repo, what is already in the private `parishishta` corpus, what is still missing, and where each item should live.
- `docs/INTEGRAL_REALISM_GRAMMAR.md` formalizes the broader non-Advaita-only grammar: identity, modality, manifestation, practice, register, adhikāra, and heliocentric/geocentric/mandalic centering.

## Current Repo And Deployment State

- Local repo: `/Users/eeshan/Dev/vedanta-timeline`.
- Local branch during follow-up pass: `main` at `442eb96`, matching `origin/main`.
- Live site check: `https://vedanta.eeshan.xyz/` returned HTTP 200 from GitHub Pages on 2026-06-18.
- Berkeley `rnn` host: local SSH config has `Host rnn` -> `rnn.ist.berkeley.edu`; `/home/eeshan/vedanta-timeline` exists there.
- Berkeley `rnn` state during the earlier cluster check: checked out branch was `loop/autonomous-2026-05-20` at `eb1c767`, not `main`; the worktree was divergent from live `main`, so it should be treated as archival/background work, not as the latest website.
- Berkeley docs checked:
  - Neuro Cluster login docs identify `axon.neuro.berkeley.edu` and 2-step login.
  - Berkeley BRC/Savio docs identify `hpc.brc.berkeley.edu`, one-time password auth, optional SSH certificates, and SLURM for jobs.
  - The local project clue is the custom `rnn` host, not the public BRC/Savio host.

## Site Architecture Relevant To This Project

- Runtime is static vanilla HTML/CSS/JS: `index.html`, `assets/app.js`, `assets/style.css`; no build step for the main site shell.
- Thinkers live in `data/thinkers/*.json`. `engaged_works[].source_status` is the immediate source-readiness flag.
- Articles live in `data/articles/source/*.md` and are exposed only if registered in `data/articles/manifest.json`.
- Perspective essays live in `data/perspectives/source/*.md` and `data/perspectives/manifest.json`.
- Source texts mirrored into the public repo live in `data/sources/`.
- Extended translations live in `data/full_translations/`.
- Source-tab wiring uses `data/primary_text_manifest.json` and fetches under `data/sources/`; current evidence suggests some manifest/status entries are stale against the physical tree.
- Existing tracking files:
  - `to-do/HANDOFF.md`
  - `to-do/ACQUISITION_NEEDED.md`
  - `to-do/DIGITIZATION_NEEDED.md`
  - `docs/SOURCE_COLLECTION.md`
  - `docs/PRIMARY_SOURCE_INVENTORY.md`
  - `docs/SECONDARY_SOURCE_AUDIT.md`
  - `docs/ACQUISITION_PATHWAYS.md`

## Core Thesis To Preserve

The voice note argues for a synthesis that is stronger than generic pluralism. The working claim is that Hindu/Indian traditions are not merely many partially true schools, but a layered, realist, practice-oriented field in which apparently conflicting traditions often preserve different registers of the same absolute reality.

The central interpretive contrast:

- Bad reading to test and critique: Śaṅkara/Advaita as only `nirguṇa Brahman`, anti-`saguṇa`, anti-`māyā`, anti-form, or world-hating.
- Proposed reading: Advaita is an agentic, practice-centered discipline of identity-realization. Its negations are often method instructions or standpoint grammar, not final hatred of form, world, God, or `māyā`.
- Non-duality should be modeled as non-duality of form and formlessness, Śiva and Śakti, identity and modality, being and becoming.
- `māyā` is false only relative to the limited egoic world-model, not sheer nothingness. The question "where does māyā arise?" may itself be malformed in some Advaita sub-school readings.
- The absolute experience may be one in kind, while post-realization expression differs by modality, temperament, path, and register.
- Traditions such as Madhva's Tattvavāda, Kashmir Śaivism, Mīmāṃsā, Tantra, Jyotiṣa, Bhāgavata traditions, Ramakrishna, Aurobindo, Vivekananda, Ramana, and others should be read as preserving real aspects/registers rather than as mere lower errors.

The product goal is a primary-source-backed grammar or visual model capable of showing harmony without erasing disagreement.

## Concepts Needing Formalization

1. Identity versus modality: Śiva as identity, Śakti as modality; Brahman/ātman realization versus divine expressive modes.
2. Form versus formlessness: early `neti neti` practice versus post-realization return to forms as real expressions.
3. Realism: define whether this means ontological realism, layered/standpoint realism, devotional realism, pragmatic realism, or a structured combination.
4. `māyā` / `avidyā`: distinguish false-as-egoic-misreading, sublatable appearance, creative Śakti, positive ignorance, self-veiling, and ill-posed locus questions.
5. Absolute experience and plural expression: clarify whether sameness is phenomenological, metaphysical, soteriological, or hermeneutic.
6. Register/layer model: keep real disagreements visible while identifying false oppositions caused by scope/register mismatch.
7. Heliocentric / geocentric / third model: this is central. Debashish Banerji's explicit "heliocentric age" language is now located in a SABDA August 2025 passage keyed to Sri Aurobindo's CWSA 18 pp. 263-264 and *The Human Cycle* pp. 7-14. Chaudhuri's private OCR has the parallel distinction "Ego-Centric and Cosmo-Centric Individuality." Need the exact Aurobindo/Chaudhuri/Banerji source packet before publication.
8. Practice versus ontology: mark when a text is giving a sādhana instruction rather than a complete metaphysical denial.
9. Tradition as self-correction: test the theological/historical claim that later traditions are divine corrections of misreadings, rather than merely independent schools.
10. Visual grammar: likely a graph/matrix of identity, modality, standpoint, practice, and manifestation status rather than another long essay.

## People And Traditions To Research First

Primary modern cluster:

- Haridas Chaudhuri
- Debashish Banerji
- Sri Aurobindo
- Swami Medhananda / Ayon Maharaj

Classical/traditional support and challenge cluster:

- Śaṅkara and post-Śaṅkara Advaita sub-schools
- Sureśvara, Padmapāda, Vācaspati Miśra, Prakāśātman, Madhusūdana, Satchidanandendra
- Madhva and Tattvavāda
- Rāmānuja and Viśiṣṭādvaita
- Caitanya / Jīva Gosvāmin / Baladeva
- Vijñānabhikṣu
- Kashmir Śaivism / Trika / Pratyabhijñā
- Mīmāṃsā, especially Śabara/Kumārila and symbolic/externalized ritual readings
- Ramakrishna, Sarada Devi, Vivekananda
- Ramana Maharshi
- Vedic, Upaniṣadic, Purāṇic, Āgamic, Tantric, Jyotiṣa, and Bhāgavata corpora

Comparative later/deferred cluster:

- Hegel and sublation
- Nāgārjuna/Madhyamaka and expanding śūnyatā
- Spinoza and one-substance metaphor
- Deleuze/Whitehead/Bergson/McGilchrist/Gebser only after Indian grounding is stable
- Clooney on Mīmāṃsā, as secondary scholarship to evaluate, not as substitute for primary grounding
- Swami Dayananda's treatment of other Vedāntas, targeted for critique after source collection

## Transcript Uncertainties To Resolve

- "civil novel" at the opening: likely transcription error; determine intended thesis name.
- "Haidash Chaudhuri" / "Haridasa Shradhu": Haridas Chaudhuri.
- "Debendranath Banerjee" / "Devashishpaner": likely Debashish Banerji unless a separate figure is later intended.
- "Sukira of the Vedas": Sri Aurobindo's *The Secret of the Veda*.
- "Gandha Bhikshu": Vijñānabhikṣu.
- "Acharya Staneshwar Tumulsena" / "Acharya Tamalsana": Sthaneshwar Timalsina; `Tumulsena` spelling remains unverified.
- "Sarvam Nyayam" / "Nepali Sarvam Nyayam tradition": probably Sarvāmnāya, especially the Nepali Sarvāmnāya / Śaiva-Śākta transmission context around Timalsina and Vimarsha Foundation; source-cite before publishing.
- "lunocentric" or third cosmology model: unresolved as a source term. The working formalization is geocentric, heliocentric, and mandalic/aperspectival/integral centering, with Banerji's heliocentric-language source now located.
- "Swami Sachchidananda": Satchidanandendra Saraswati in the Advaita `mūlāvidyā` context.

## Current Source Status For Priority Figures

### Chaudhuri

- Entry: `data/thinkers/chaudhuri.json`.
- Article: `data/articles/source/chaudhuri-banerji.md`.
- Gaps:
  - *The Philosophy of Integralism* and the 1960 *Aurobindo Symposium* proceedings are now confirmed in the private `parishishta` OCR corpus.
  - They remain `primary-text-not-in-corpus` for the public website and should not be mirrored into `data/sources/`.
  - Need page-specific extraction notes before the entry/article should be treated as grounded.

### Debashish Banerji

- Entry: `data/thinkers/banerji.json`.
- Article: `data/articles/source/chaudhuri-banerji.md`.
- Gaps:
  - *Seven Quartets of Becoming* and *The Alternate Nation of Abanindranath Tagore* are confirmed in the private `parishishta` corpus.
  - *Meditations on the Isha Upanishad*, *Integral Yoga Psychology*, and *Critical Posthumanism and Planetary Futures* remain acquisition/library targets.
  - Need open-access papers too, especially those on Integral Advaita, Integral Yoga, Identity Consciousness, Supermind, Simondon/Deleuze, and posthumanism.

### Sri Aurobindo

- Entry: `data/thinkers/aurobindo.json`.
- Articles: `data/articles/source/aurobindo.md`, `data/articles/source/mimamsa-aurobindo-v*.md`.
- Physical English source currently confirmed in repo: `data/sources/english/aurobindo/the-future-poetry.txt`.
- Gaps:
  - Many CWSA volumes are implied by entries/docs but not physically present under `data/sources/` in this checkout.
  - Need rights-reviewed access or private extraction notes for *The Life Divine*, *The Synthesis of Yoga*, *The Secret of the Veda*, Upaniṣad writings, Essays on the Gītā, and Record of Yoga excerpts relevant to Banerji.

### Medhananda / Ayon Maharaj

- Entry: `data/thinkers/medhananda.json`.
- Article: `data/articles/source/medhananda.md`.
- Gaps:
  - OUP books are `primary-text-not-in-corpus`.
  - Need exact passages on Vijñāna Vedānta, Ramakrishna, Vivekananda, manifestationism, Hick, Aurobindo, Śaṅkara, māyā, and personal/impersonal divine.

### Ramakrishna / Sarada Devi / Vivekananda

- Vivekananda entry exists; `data/sources/english/vivekananda_complete_works/` is present.
- Article: `data/articles/source/vivekananda-ramakrishna.md`.
- Gaps:
  - No `data/thinkers/ramakrishna.json`.
  - No `Kathāmṛta` / *Gospel of Sri Ramakrishna* source file found.
  - No Holy Mother / Sarada Devi source file found.
  - Need source grounding for roof/staircase, seven-hole flute, bhāva plurality, servant/part/identity modes, and post-realization return to līlā.

### Ramana

- Entry: `data/thinkers/ramana.json`.
- Physical source found: `data/sources/sanskrit/vedanta/ramana_upadesa_saram.txt`.
- Gaps:
  - Entry still marks `Upadeśa Sāram` and Tamil works as not in corpus.
  - Need source grounding for turiya, self-inquiry, identity beyond waking/dream/deep sleep, and the "fire burning itself out" image if intended.

### Satchidanandendra

- Entry: `data/thinkers/satchidanandendra.json`.
- Gaps:
  - Works are `primary-text-not-in-corpus`.
  - Need exact source for the claim that the locus/origin question for avidyā is ill-posed or appearance-based.

### Madhusūdana

- Entry: `data/thinkers/madhusudana.json`.
- Full translations exist for several works.
- Physical source clearly present for `madhusudana_siddhanta_bindu_gretil.txt`; some JSON/manifest references to additional clean source files appear physically absent.
- Gaps:
  - Verify availability of *Advaita-siddhi* and *Bhakti-rasāyana* source files.
  - Use these to test the claim that classical Advaita already preserves bhakti and positive/robust accounts of avidyā.

### Kashmir Śaivism / Trika

- Several source files exist under `data/sources/sanskrit/kashmir_shaiva/`.
- Gaps:
  - Some entries still mark available-looking files as missing.
  - Off-disk priorities include Abhinavagupta IPVV, Locana, Abhinava-Bhāratī, Kṣemarāja Śiva-Sūtra-Vimarśinī, Somānanda Śiva-Dṛṣṭi, and Jayaratha Tantrāloka-Viveka.
  - Need map of `spanda`, `svātantrya`, Śiva/Śakti, self-veiling, and manifestation as modality.

### Mīmāṃsā

- Physical sources exist for Jaimini, Śabara, and Kumārila-related material.
- Current perspective article: `data/perspectives/source/mimamsa-symbolism-shift.md`.
- Gaps:
  - Prabhākara, Pārthasārathi, Śālikanātha, Khaṇḍadeva, Apadeva, Laugākṣi Bhāskara mostly remain missing.
  - Clooney secondary works are not on disk.
  - Need careful comparison of Aurobindo's Vedic symbolism and Mīmāṃsā's ritual/hermeneutic apparatus.

### Vijñānabhikṣu

- Entry: `data/thinkers/vijnanabhiksu.json`.
- Articles and full translation exist.
- Gaps:
  - Physical source files for *Vijñānāmṛta-Bhāṣya* / *Yoga-Vārttika* appear absent despite clean-on-disk signals.
  - *Sāṅkhya-Pravacana-Bhāṣya* remains missing.
  - Important because the note invokes a prior synthesis project and may have garbled "Gandha Bhikshu" as Vijñānabhikṣu.

## Research Workstreams

### 1. Corpus Reconciliation

Goal: make `source_status`, `data/primary_text_manifest.json`, and physical `data/sources/` agree.

Tasks:

- Run/inspect `scripts/check_coverage.js`.
- Audit every priority figure above for `source_status` versus physical source file.
- Mark false `clean-on-disk` claims as defects or restore the missing source files.
- Rebuild the source manifest only after source paths are correct.
- Keep secondary sources out of the public Source tab unless licensing and project policy allow them.

### 2. Acquisition Ledger

Goal: convert the vague "we need their books/papers" into a source-by-source ledger.

Tasks:

- Extend `to-do/ACQUISITION_NEEDED.md` or create a structured acquisition CSV/MD for modern English works.
- Columns: figure, work, kind, priority, reason, current status, candidate location, rights status, corpus destination, next action.
- Start with Chaudhuri, Banerji, Medhananda, Aurobindo, Ramakrishna/Sarada, Ramana, Satchidanandendra.
- Distinguish "owned locally/private", "public scan", "public text", "library-only", "purchase needed", "citation-only".

### 3. Thesis Extraction Matrix

Goal: preserve every claim from the pasted note but separate source facts from hypotheses.

Suggested table columns:

- Claim ID
- Claim
- Status: textual claim / interpretive hypothesis / theological synthesis / product idea
- Figures involved
- Primary sources needed
- Secondary sources useful
- Current confidence
- Publication readiness

Initial claim clusters:

- Advaita is not nirguṇa-only.
- Māyā is not crude nonexistence.
- Negation is often practice instruction.
- Form/formless non-duality is the target.
- Śiva/Śakti is identity/modality grammar.
- Madhva protects a realist register.
- Kashmir Śaivism is modality-focused, not incomplete Advaita.
- Ramakrishna's vijñāna preserves multiple divine relations after realization.
- Aurobindo/Chaudhuri/Banerji preserve a modern integral version of this grammar.
- Medhananda is both ally and target: strong on Ramakrishna/Vivekananda manifestationism, possibly weak on Śaṅkara if he accepts a bad Advaita contrast.

### 4. Śaṅkara And Advaita Defense Packet

Goal: test the central polemic against bad Advaita readings.

Tasks:

- Collect passages from Śaṅkara bhāṣyas on `nirguṇa`, `saguṇa`, `īśvara`, `māyā`, `adhyāsa`, `vyāvahārika`, `pāramārthika`, devotion, and practice.
- Collect devotional works attributed to Śaṅkara separately and mark authorship tier honestly.
- Map Bhāmatī, Vivaraṇa, Satchidanandendra, Madhusūdana, and other sub-school positions on avidyā/māyā.
- Explicitly distinguish traditional Advaita claims from later simplifications and hostile caricatures.

### 5. Integral / Vijñāna Cluster Packet

Goal: determine exactly what Chaudhuri, Banerji, Aurobindo, and Medhananda already say.

Tasks:

- Ground `data/articles/source/chaudhuri-banerji.md` in held source texts or convert it into a research note until sources are acquired.
- Extract Banerji's heliocentric/geocentric model from the SABDA August 2025 passage and then search the missing Banerji books, especially *Time-Steps of the Cosmic Horse*, for fuller development.
- Compare Chaudhuri's `pūrṇa-advaita`, Banerji's Integral Advaita, Aurobindo's Supermind, Medhananda's Vijñāna Vedānta, and Ramakrishna's vijñāna.
- Identify where each misreads or underreads Śaṅkara, if they do.

### 6. Tradition-Integration Packet

Goal: show exactly how the synthesis handles real differences.

Tasks:

- Madhva/Tattvavāda: identify realism-preserving claims and anti-"you are God" polemics; test whether the target is actual Advaita or a straw Advaita.
- Rāmānuja/Viśiṣṭādvaita: map body-of-God and qualified non-duality as a register, not a "lower" truth.
- Caitanya/Gauḍīya: map `acintya-bhedābheda` as difference/non-difference grammar.
- Kashmir Śaiva/Trika: map `svātantrya`, `spanda`, self-veiling, and Śiva/Śakti.
- Mīmāṃsā/Veda: test ritual-symbolic/externalized yogic process thesis against Śabara/Kumārila and Aurobindo.
- Ramana: map self-inquiry and turiya without turning it into world-negating formlessness.

### 7. Website Product Model

Goal: make the site show the project without overclaiming.

First artifact should be a research matrix, not a final manifesto.

Potential UI/data additions:

- A "Project: Integral Realism" article hidden/unpublished until source-backed.
- A comparative matrix page with statuses and uncertainty.
- New primitives in `data/registries/primitive_graph.json` only after they are stable.
- A visualization of register/scope/identity/modality axes.
- Source-readiness badges for modern English works, since several key modern sources are not public-domain or not in corpus.

## Immediate Next Actions

1. Reconcile source manifest/status for the priority figures, because the current repo has obvious status/path drift.
2. Build a structured acquisition ledger for Chaudhuri, Banerji, Aurobindo, Medhananda, Ramakrishna/Sarada, Ramana, Satchidanandendra, Madhusūdana, Trika, Mīmāṃsā, and Vijñānabhikṣu.
3. Identify the garbled transcript names before they enter public docs.
4. Create a claim matrix from the pasted note and tag each claim as source-backed, hypothesis, or synthesis.
5. Do a Śaṅkara packet first, because the core thesis depends on whether the bad modern reading is actually bad.
6. Then do the Chaudhuri/Banerji/Aurobindo/Medhananda packet, because those figures are the nearest published precedents and competitors.
7. Only after those packets, design the graphical grammar.

## Publication Rules

- Do not publish the pasted-note rhetoric as site prose.
- Do not call a modern work "grounded" until its actual text is on disk or cited with page-specific access.
- Do not collapse real doctrinal contradictions into harmony; mark register, scope, and actual disagreement.
- Do not use "Vijñāna Vedānta", "Integral Advaita", "Pūrṇa-Advaita", and the user's synthesis as interchangeable.
- Do not treat secondary scholarship as primary evidence for a thinker's own doctrine.
- Preserve uncertainty where the transcript is unclear.
