# Secondary-Source & Editorializing Audit — data/thinkers/*.json

Read-only audit of the **reader-facing prose** (`core_thesis`, top-level `summary`,
and each `engaged_works[].summary`) across all 194 thinker entries. Scope and standard
are set by the Karpātrī regrounding (commit `03e84b1`) and
`docs/SANSKRIT_TRANSLATION_STANDARD.md` / `docs/ARCHITECTURE.md`.

**What is flagged:** (1) a doctrinal/biographical claim whose *authority rests on a
modern scholar* (author-year parentheticals, "X argues", "the standard secondary
reading is …") rather than a primary text; (2) editorializing / value-judgments
("the single most important", "magnum opus", "included here for completeness", "not
original"); (3) doctrinal claims with **no primary `cite://` grounding** in the prose.

**What is NOT flagged (legitimate):**
- Scholar citations in `ascription_notes` / `ascription_evidence` / `dates_evidence`
  (those fields are *about* the state of scholarship — expected and correct).
- Naming a critical **edition** for provenance (e.g. "Thibaut, SBE 34"; "Kuppuswami
  Sastri, Madras 1937"; "Mayeda's 1973 critical edition") — that is documentary, not
  interpretive over-reliance.
- Doctrinal "more X than Y" comparisons between *primary* works/positions (e.g.
  "more conservative than Mīmāṃsā", "more compact than the *Nirṇaya*") — these are
  substantive philosophical claims, not value-judgments about the entry.
- Plain-text primary references (BṛU 2.3.6, BSB 1.1.4) that are not wrapped in a
  `cite://` link still count as primary grounding; they are a LOW formatting gap, not
  a secondary-reliance finding.

---

## Summary table

| Severity | Count | Meaning |
|---|---:|---|
| HIGH | 4 | Prose authority rests on a secondary source for a doctrinal claim, or heavy/structural editorializing in `core_thesis`. |
| MED | 9 | Secondary-as-authority parenthetical(s) attached to doctrinal claims, or a clear value-judgment, recoverable by deletion/regrounding. |
| LOW | 11 | A single soft editorial word, an edition-citation that reads as authority, or doctrinal prose with no `cite://` link but plain primary refs present. |
| CLEAN (prose) | ~170 | No secondary-reliance or editorializing detected in prose. (Many of these still appear in the no-`cite://` collection-priority list below.) |

Note: "CLEAN (prose)" is independent of primary-source *coverage*. **78 entries carry
zero `cite://` link anywhere in their prose** — see the final section; that is the
collection backlog, not a prose-quality defect per se.

---

## HIGH

### 1. `clooney.json` — HIGH (special category: entry is *about* a modern scholar)
14 scholar-name hits, but this is a **distinct case**: Francis X. Clooney is himself the
subject, so his monographs ARE the primary texts and citing them is correct. The genuine
problems are the meta/editorial framing and the admission that the primary texts are not
in corpus:
- core_thesis: *"Honest scope: Clooney's monographs are not held in this corpus on disk;
  the engagement here proceeds via published reviews … and the published bibliographic
  and abstract record of each title …"* — the entry concedes it is built on **reviews and
  abstracts**, i.e. secondary-of-secondary, not the primary works.
- ew `hindu-catholic-priest-scholar`: *"The book is included here, despite being
  autobiographical rather than primarily scholarly, because it is the most extended
  first-person statement …"* — meta-commentary about the entry + soft value-judgment
  ("the most extended").
- **Primary fix:** these works exist and are obtainable (Vienna 1990, SUNY 1993, OUP
  2001/2008, Springer 2022). Ground summaries in the actual monographs, drop the
  "included here" framing and the reviews-and-abstracts apparatus.

### 2. `sankara.json` — HIGH (doctrinal authority on scholars + value-judgment)
- ew `mandukya-bhasya`: *"Modern scholarship has questioned the unity of the four
  *prakaraṇas* — **Hacker's stylometric work and King's *Early Advaita Vedānta and
  Buddhism* (1995)** raise the strongest doubts about *prakaraṇa* 4 …"* — authorship
  doubt sourced to scholars *in the work summary* (this belongs in `ascription_notes`).
- ew `vivekacudamani`: *"**Paul Hacker's stylometric work argues against** Śaṅkara's
  authorship"* + *"the single most influential Advaita primer in the living tradition"*
  (value-judgment).
- ew `isa-bhasya`: *"the **single most important** short text for the school's
  *jñāna-karma-vibhāga* doctrine"* (value-judgment).
- ew `bhagavad-gita-bhasya`: *"**Hacker, Mayeda, and Halbfass treat it as such.** Mayeda
  1992 is on disk; the Hacker and Halbfass monographs are referenced as field-orientation."*
  — authenticity authority resting on three modern scholars in the summary.
- **Primary fix:** move authorship-doubt sentences to `ascription_notes`; reground the
  doctrinal points in the bhāṣyas themselves (already heavily cited, 14 `cite://`); delete
  "single most important / most influential."

### 3. `appayya.json` — HIGH (repeated structural value-judgment, the core claim)
- core_thesis: *"He is **the single most important** late-medieval source for the
  structured comparative reading of competing Advaita sub-positions."*
- ew `siddhanta-lesha-samgraha`: *"the indispensable reference … and **the single most
  important** pre-modern source for the structured study of intra-school disagreement."*
- The "single most important" claim is the load-bearing sentence of the entry, stated
  twice. **Primary fix:** the *Siddhānta-Leśa-Saṅgraha* itself lists the sub-positions it
  surveys (Vivaraṇa, Bhāmatī, etc.); describe what the text *does* (a survey of N
  contested loci) rather than ranking it.

### 4. `vedanta-desika.json` — HIGH (secondary-as-authority in core_thesis, zero own-text `cite://`)
- core_thesis opens: *"Vedānta Deśika is the systematiser … (**Clooney's *Beyond Compare*,
  2008, is the standard English-language secondary engagement** with Deśika's
  *Rahasya-Traya-Sāra*, paired with Francis de Sales' *Treatise on the Love of God*)."*
- ew `rahasya-traya-sara`: same Clooney-as-standard-reading parenthetical repeated.
- The rest of the prose is densely primary (Nyāya-Pariśuddhi, Śatadūṣaṇī, RTS adhikāra
  numbers) but **carries no `cite://` link at all** — all references are plain-text.
- **Primary fix:** delete the two Clooney parentheticals (his reading is not the
  authority for Deśika's own positions); convert the plain RTS / Śatadūṣaṇī references to
  `cite://` links.

---

## MED

### `ramanuja.json` — MED
- core_thesis: *"Rāmānuja gives Viśiṣṭādvaita its school-defining form (**Clooney's
  *Theology After Vedānta*, 1993, is the standard English-language secondary reading** of
  the *Śrī-Bhāṣya* methodology)."*
- ew `shri-bhasya`: *"**Clooney's *Theology After Vedānta* (1993) remains the standard
  English-language secondary reading** of the work as a constructive theological argument."*
- Fix: drop both parentheticals; the *Śrī-Bhāṣya* is on disk (7 `cite://`) — ground in it.

### `srinivasa.json` — MED
- core_thesis: *"*svābhāvika-bhedābheda* becomes defensible as a developed Vedāntic
  position rather than as a sectarian slogan (**Dasgupta, *History of Indian Philosophy*,
  vol. …**)."*
- ew `vedanta-kaustubha`: *"the operative doctrinal text of the Nimbārka line and the
  standard reference … (**Dasgupta …**)."*
- Fix: the *Vedānta-Kaustubha* is clean-on-disk (14 `cite://`); the defensibility claim
  should rest on the text's own argument, not on Dasgupta.

### `nimbarka.json` — MED
- ew `vedanta-parijata-saurabha`: *"the school-defining text and the obligatory reference
  … (**Dasgupta, *History of Indian Philosophy*, vol. …**)."*
- ew `dasa-shloki`: *"this is the most direct first-person datum available (**Dasgupta …**)."*
- Fix: drop Dasgupta as warrant; the *Pārijāta-Saurabha* is clean-on-disk.

### `vijnanabhiksu.json` — MED
- ew `vijnanamrta-bhasya`: *"the principal source for *avibhāga-advaita* and the **most
  ambitious** early-modern Vedānta–Sāṅkhya–Yoga reconciliation (**so Dasgupta …**)."*
- Combines a value-judgment ("most ambitious") with Dasgupta-as-warrant. Heavy
  `cite://` coverage (28) exists — reground; delete "most ambitious / so Dasgupta."

### `rangaramanuja-muni.json` — MED
- core_thesis & three engaged-works summaries lean on *"Carman, *The Theology of
  Rāmānuja*, 1974, ch. …"* repeatedly as the warrant for the bhāṣya-coverage-gap claim.
- Fix: the gap is a documentary fact (which Upaniṣads Rāmānuja did/didn't comment on) —
  state it from the primary commentarial record, not from Carman.

### `yadava-prakasa.json` — MED
- core_thesis & ew `lost-bhedabheda-corpus`: *"the proximate Vaiṣṇava *bhedābheda*
  against which Viśiṣṭādvaita defines itself (**Carman … 1974, ch. …**)"*; teacher-of-
  Rāmānuja claim sourced to *Guru-Paramparā-Prabhāva* (good) **and** Carman.
- Fix: keep the guru-paramparā documentary source; drop Carman as doctrinal warrant.

### `bodhayana.json` — MED
- core_thesis: *"it positions Rāmānuja's exposition as **derivative from Bodhāyana, not
  original** to himself"* (value-laden framing) + *"**van Buitenen and Carman treat** the
  three as probably distinct historical figures …"* (historical claim resting on scholars
  in core_thesis).
- Fix: move the van Buitenen/Carman identification debate to `ascription_notes`; restate
  the Rāmānuja-relation neutrally (Rāmānuja cites the *vṛtti-kāra*).

### `kasakrtsna.json` — MED
- core_thesis: *"**Nakamura (vol. I, 1949) and Sharma (1965) note** that *avasthiti* is
  grammatically ambiguous between strict identity … and inherent presence …"* — the
  central interpretive move (the two readings) is attributed to two modern scholars in
  core_thesis. Entry has **zero `cite://`** (only plain BS 1.4.20–22 refs).
- Mitigation: the grammatical ambiguity is genuinely a primary-text observation; the
  scholar names are dispensable. Fix: state the ambiguity from the sūtra-text and
  Śaṅkara/Bhāskara's divergent bhāṣyas (both primary, both already named), drop the
  Nakamura/Sharma attribution; add `cite://badarayana/brahma-sutra/1.4.22` links.

### `bhartrprapanca.json` — MED
- core_thesis closes with a full paragraph on *"**Hiriyanna's 1924 reconstruction
  methodology** … is itself part of what can be philosophically engaged"* — a modern
  scholar's method is made a topic of the reader-facing thesis. Entry has **zero `cite://`**
  (plain BṛU refs only).
- Mitigation: for a fragments-only figure the reconstruction problem is legitimately part
  of the story, but it belongs in `ascription_notes`, not core_thesis. Fix: ground the
  four doctrinal commitments in the BṛU passages + the Śaṅkara/Sureśvara citation-record
  (primary), move the Hiriyanna-methodology discussion to ascription fields.

---

## LOW

| File | Issue (quoted) | Note |
|---|---|---|
| `vidyaranya.json` | ew `sarva-darshana-samgraha`: *"the **single most influential** pre-modern Indian doxography"* | One value-judgment; rest is well-cited (7 `cite://`). Restate as "the most widely circulated" → or describe coverage. |
| `madhva.json` | ew `anuvyakhyana`: *"developed here **more fully than anywhere else** in Madhva's corpus"* | Comparison is *within Madhva's own corpus* — borderline-OK; soften to factual. 11 `cite://`. |
| `kundakunda.json` | ew `samaya-sara`: *"**arguably the most-studied** Jaina philosophical work in the modern period"* | Single hedge-word value-judgment; delete "arguably the most-studied." |
| `uttamur-viraraghavacharya.json` | core_thesis: *"The **magnum opus** *Paramārtha-Bhūṣaṇa* …"* | Replace "magnum opus" with "principal work." 22 `cite://` otherwise. |
| `aurobindo.json` | ew `savitri`: *"It is **included here because no inventory of his Vedāntic engagement is complete without it**."* | Meta-commentary about the entry; delete the sentence. 11 `cite://`. |
| `kesava-kasmiri.json` | ew `kaustubha-prabha`: *"opponents whose apparatus is **more developed than** the *māyā-vāda* Nimbārka could have addressed"* | Doctrinal-historical comparison, mostly fine; verify it is not editorial. |
| `sundara-pandya.json` | core_thesis: *"give the negative theses … **more sharply than** the positive epistemology"* + *"Sastri, ed., *Naiṣkarmya-Siddhi*, 1925, introduction"* | "more sharply" is a textual observation (OK); Sastri ref is an **edition** (OK). Net LOW — only flagged for review. 21 `cite://`. |
| `totaka.json` | ew `srutisara-samuddharana`: *"(**Pollock, *The Language of the Gods*, 2006**, on stylistic dating …)"* | Dating-method citation; better placed in `dates_evidence` / `ascription_notes`. |
| `gaudapada.json` | ew `mandukya-karika`: *"(King 1995)"* | Authorship/strata point; move to `ascription_notes`. 11 `cite://` otherwise clean. |
| `jaimini.json` | ew `mimamsa-sutra`: *"**Clooney's *Thinking Ritually* (1990) is the standard English-language secondary reading** …"* | Drop the parenthetical; the sūtra is the primary. Only 1 `cite://` in prose. |
| `bhava-ganesa.json` | core_thesis: *"the Bhikṣu-tradition would be attested only … and in **Dasgupta's later reconstruction**"* | Dasgupta named as the reconstruction source in prose; minor, move to notes. 9 `cite://`. |
| `nathamuni.json` | core_thesis: *"(**Clooney's *Seeing Through Texts*, 1996**, is the standard English-language secondary engagement …)"* | Fragments-only figure (oral-tradition dating); drop Clooney parenthetical, keep the reconstruction caveat in ascription. Zero `cite://`. |
| `manavala-mamunigal.json`, `pillai-lokacarya.json` | core_thesis each: *"(**Clooney's *Seeing Through Texts*, 1996**, is the standard English-language secondary engagement with the Tenkalai *vyākhyāna*-tradition …)"* | Same Clooney parenthetical pattern; drop it. pillai has 22 `cite://`, manavala 3. |
| `hastamalaka.json` | ew: *"the historical Hastāmalaka cannot be securely identified … (**Hacker, "Notes on the *Mādhavīya-Śaṅkara-Vijaya*", 1947**)"* | Identification caveat belongs in `ascription_notes`. Zero `cite://`. |
| `mandana.json` | ew `brahma-siddhi`: *"Kuppuswami Sastri (Madras, 1937)"* | **Edition** citation — legitimate provenance, not a finding. Listed only to mark as reviewed-clean. |
| `badarayana.json` | ew `brahma-sutra`: *"Standard editions: Thibaut (SBE 34, 38), Deussen …"* | **Edition** citations — legitimate. Reviewed-clean. |

---

## Collection priority — entries with NO primary `cite://` grounding in prose (78)

These carry **zero `cite://` link** in `core_thesis` / any `engaged_works[].summary`.
Two sub-classes; the first is the real backlog.

### A. Vedānta / engaged-tradition figures making doctrinal claims with no primary cite — collect primary texts
These are in-corpus doctrinal players whose own works exist and should be cited:
- `vedanta-desika` (also HIGH above — plain RTS/Śatadūṣaṇī refs, convert to `cite://`)
- `mandana` (Brahma-Siddhi; edition known — convert plain refs to `cite://`)
- `nathamuni` (fragments/oral — needs reconstruction-grounding caveat, low collectability)
- `bhartrprapanca`, `kasakrtsna`, `audulomi`-class proto/fragment figures: ground in the
  *Brahma-Sūtra* / *Bṛhadāraṇyaka* loci they are reconstructed from (plain refs → `cite://`).
- `upavarsa`, `bodhayana` (proto-Vedānta / vṛtti-kāra — fragments; ground in BS citation record)
- `brahmananda` (sub-commentary on *Advaita-Siddhi* — collect text)
- `gokulnatha` (Śuddhādvaita), `jiva-gosvami` (Acintya-Bhedābheda — *Ṣaṭ-Sandarbha* exists, high collectability)
- `parthasarathi`, `salikanatha`, `prabhakara`, `khandadeva` (Mīmāṃsā — texts exist, collectable)
- `prashastapada`, `sridhara`, `bhasarvajna`, `jayanta-bhatta`, `raghunatha-siromani` (Nyāya/Vaiśeṣika — texts exist)
- `vyasa-bhasya`, `bhojaraja` (Yoga — *Yoga-Bhāṣya* / *Rāja-Mārtaṇḍa* exist, high collectability)
- Pāśupata/Śaiva: `kaundinya`, `lakulisha`, `basava`, `allama-prabhu`, `pancaratra-tradition`
- Bhairava-tantra cluster: `ksemaraja`, `amrtananda`, `svacchanda-tantra`, `vijnana-bhairava-tantra`,
  `malini-vijaya-tantra`, `trisirobhairava-tantra`, `cidambarananda`, `hrasvanatha`, `sivananda-yogin`
- Tattvavāda: `aksobhya-tirtha`, `narahari-tirtha`, `narayana-panditacarya` (texts exist)
- Jaina: `mallisena`, `yashovijaya`, `samantabhadra`, `siddhasena-divakara`
- `hastamalaka` (single short stotra; fragments-only attribution)

### B. Cross-tradition / comparator figures (Buddhist, Jaina-logic, Western) — lower priority
For these the entry's job is structural comparison; primitive_commitments legitimately
point at the texts they engage rather than a Vedāntic primary. Still ideally get a
`cite://` to the figure's *own* primary text where it exists:
- Buddhist: `nagarjuna`, `aryadeva`, `buddhapalita`, `bhaviveka`, `candrakirti`, `jnanagarbha`,
  `santaraksita`, `kamalasila`, `santideva`, `atisha`, `asanga`, `vasubandhu`,
  `vasubandhu-abhidharma`, `sthiramati`, `dharmapala`, `maitreya-attributed`, `lankavatara`,
  `dignaga`, `dharmakirti`, `dharmottara`, `jnanasrimitra`, `ratnakirti`, `sanghabhadra`,
  `buddhaghosa`
- Western/modern comparators (no Indic primary expected; prose is interpretive overlay):
  `foucault`, `derrida`, `deleuze`, `levinas`, `bergson`, `leibniz`, `prigogine`, `gebser`,
  `mcgilchrist`, `medhananda`, `anirban`, `abhinanda`, `banerji`

---

## Biographical / factual notes
No impossible dates or obvious factual errors surfaced in the prose triage. `karpatri.json`
(the reference fix) is excluded from findings — already regrounded in `03e84b1`.
