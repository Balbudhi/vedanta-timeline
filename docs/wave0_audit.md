# Wave 0 Audit

Wave 0 populated four registry files and 60 thinker skeletons under
`/orcd/home/002/eeshan/philosophy/site/data/`. All files validate as JSON
and all internal cross-references resolve.

## Summary counts

| Registry | Keys |
|---|---|
| `registries/schools.json` | 10 school-color tokens |
| `registries/sub_schools.json` | 45 sub-school registry entries |
| `registries/pramanas.json` | 9 pramāṇa entries |
| `registries/sub_axes.json` | 44 controlled sub-axis entries |

| Item | Count |
|---|---|
| Thinker skeleton files | 60 |
| Manifest entries | 60 |

The CORPUS_PLAN.md "coverage summary" lists 58 entries, but its actual table-row
counts add to 60 (the summary undercounts Advaita by 1 and Bhedābheda by 1).
All 60 table entries are represented; nothing was skipped or added.

## Validation checks (all pass)

1. Every thinker file is parseable JSON.
2. Every `id` matches its filename stem.
3. Every `school_color_token` is a key in `registries/schools.json`.
4. Every `sub_school` value matches the `display_name` of an entry in
   `registries/sub_schools.json`.
5. Every `lineage_in`, `lineage_out`, and `lineage_polemical[].thinker_id`
   reference resolves to a file in `thinkers/`.
6. Every `engaged_works[].work_id` is kebab-case and unique within its thinker.
7. Every entry has `entry_status: "draft"`, `entry_owner_agent: "wave0-opus"`,
   `last_verified_at: "2026-05-09"`, `last_verified_by: "wave0-opus"`.
8. The internal project codename appears nowhere in any data file (verified
   by grep across `data/`).
9. Every `dates_tier == "confirmed-from-records"` entry carries
   `dates_evidence[]`. Every `ascription_tier == "securely-authored"` work
   carries `ascription_evidence[]`.
10. `core_thesis: ""` and `engaged_works[].summary: ""` everywhere
    (Wave 1 fills these). `key_passages: []` everywhere (Wave 2 fills).

## Roster by school

### proto (8)
- `asmarathya` — Āśmarathya (−400 to −100) [Proto-bhedābheda-leaning]
- `audulomi` — Auḍulomi (−400 to −100) [Citation-only proto-Vedāntins]
- `badarayana` — Bādarāyaṇa (−200 to 200) [Sūtra-author]
- `bodhayana` — Bodhāyana (300–500) [Claimed by Viśiṣṭādvaita]
- `brahmadatta` — Brahmadatta (550–700) [Bhāvanā/jñāna hybrid]
- `kasakrtsna` — Kāśakṛtsna (−400 to −100) [Proto-Advaita-leaning]
- `sundara-pandya` — Sundara-Pāṇḍya (600–700) [Proto-Advaita]
- `upavarsa` — Upavarṣa (100–400) [Claimed by both Advaita and Viśiṣṭādvaita]

### advaita (19)
- `gaudapada` — Gauḍapāda (500–600) [Proto-Advaita]
- `mandana` — Maṇḍana Miśra (660–720) [Bhāmatī-Advaita]
- `sankara` — Ādi Śaṅkara (700–750) [Advaita (school-defining)]
- `sureshvara` — Sureśvara (720–770) [Sureśvara-line proto-Vivaraṇa]
- `padmapada` — Padmapāda (720–770) [Vivaraṇa-Advaita]
- `hastamalaka` — Hastāmalaka (750–800) [Advaita (school-defining)]
- `totaka` — Toṭaka (750–800) [Advaita (school-defining)]
- `vacaspati` — Vāchaspati Miśra (900–980) [Bhāmatī-Advaita]
- `sarvajnatman` — Sarvajñātman (900–1100) [Sureśvara-line proto-Vivaraṇa]
- `vimuktatman` — Vimuktātman (1050–1100) [Vivaraṇa-Advaita]
- `anandabodha` — Ānandabodha (1100–1200) [Vivaraṇa-Advaita]
- `prakasatman` — Prakāśātman (1200–1300) [Vivaraṇa-Advaita]
- `citsukha` — Citsukha (1200–1240) [Vivaraṇa-Advaita]
- `vidyaranya` — Vidyāraṇya (1296–1386) [Vivaraṇa-Advaita]
- `appayya` — Appayya Dīkṣita (1520–1593) [Trans-school Advaita synthesist]
- `madhusudana` — Madhusūdana Sarasvatī (1540–1640) [Vivaraṇa-Advaita]
- `dharmaraja` — Dharmarāja Adhvarīndra (1580–1620) [Vivaraṇa-pedagogical]
- `brahmananda` — Brahmānanda Sarasvatī (1650–1750) [Vivaraṇa-Advaita]
- `brahmananda-saraswati` — Brahmānanda Sarasvatī modern (1871–1953) [Modern Advaita revival]

### vishishtadvaita (7)
- `nathamuni` — Nāthamuni (823–924) [Pāñcarātra-grounded Viśiṣṭādvaita]
- `yamuna` — Yāmunācārya (916–1041) [Proto-systematic Viśiṣṭādvaita]
- `ramanuja` — Rāmānuja (1017–1137) [Viśiṣṭādvaita (school-defining)]
- `sudarsana` — Sudarśana Sūri (1200–1260) [Viśiṣṭādvaita scholastic]
- `pillai-lokacarya` — Pillai Lokācārya (1264–1369) [Tenkalai]
- `vedanta-desika` — Vedānta Deśika (1268–1369) [Vaḍakalai]
- `manavala-mamunigal` — Maṇavāḷa Māmunigaḷ (1370–1443) [Tenkalai]

### dvaita (5)
- `madhva` — Madhva (1238–1317) [Tattvavāda]
- `jayatirtha` — Jayatīrtha (1345–1388) [Dvaita scholastic]
- `vyasatirtha` — Vyāsatīrtha (1460–1539) [Navya-Dvaita]
- `vijayindra` — Vijayīndra Tīrtha (1514–1595) [Navya-Dvaita]
- `raghavendra` — Rāghavendra Tīrtha (1595–1671) [Dvaita scholastic-devotional]

### bhedabheda (6)
- `bhartrprapanca` — Bhartṛprapañca (400–600) [Proto-Bhedābheda]
- `bhaskara` — Bhāskara (750–800) [Aupādhika-Bhedābheda]
- `yadava-prakasa` — Yādava-Prakāśa (1050–1100) [Bhedābheda transitional to Viśiṣṭādvaita]
- `nimbarka` — Nimbārka (1130–1300) [Svābhāvika-Bhedābheda (Dvaitādvaita)]
- `srinivasa` — Śrīnivāsa (1250–1350) [Svābhāvika-Bhedābheda (Dvaitādvaita)]
- `kesava-kasmiri` — Keśava-Kāśmīrī Bhaṭṭa (1450–1500) [Svābhāvika-Bhedābheda (Dvaitādvaita)]

### acintya (7)
- `caitanya` — Caitanya Mahāprabhu (1486–1534) [Gauḍīya (school-founding)]
- `sanatana-gosvami` — Sanātana Gosvāmī (1488–1558) [Gauḍīya]
- `rupa-gosvami` — Rūpa Gosvāmī (1489–1564) [Gauḍīya rasa-theology]
- `jiva-gosvami` — Jīva Gosvāmī (1513–1598) [Gauḍīya systematic philosophy]
- `visvanatha` — Viśvanātha Cakravartī (1626–1708) [Gauḍīya]
- `baladeva` — Baladeva Vidyābhūṣaṇa (1700–1793) [Gauḍīya formal-Vedāntic]
- `bhaktivinoda` — Bhaktivinoda Ṭhākura (1838–1914) [Gauḍīya modern]

### shuddha (3)
- `vallabha` — Vallabhācārya (1479–1531) [Śuddhādvaita (school-defining)]
- `vitthalanatha` — Viṭṭhalanātha (1515–1585) [Puṣṭi-Mārga]
- `purusottama` — Puruṣottama (1668–1781) [Puṣṭimārga scholastic]

### avibhaga (1)
- `vijnanabhiksu` — Vijñānabhikṣu (1550–1600) [Avibhāga-Advaita]

### trika-comparator (3)
- `utpaladeva` — Utpaladeva (900–950) [Pratyabhijñā founding text]
- `abhinavagupta` — Abhinavagupta (950–1025) [Trika school-consummating]
- `ksemaraja` — Kṣemarāja (1000–1050) [Trika school-summarizing]

### cross-tradition (1)
- `bhartrhari` — Bhartṛhari (450–510) [Śabda-Advaita]

## Polemical edges captured

Per CORPUS_PLAN.md notes and the framework, the following polemical
(non-teacher/student) edges are recorded under `lineage_polemical`:

- `madhva` ↔ `madhusudana` (refutes / is-refuted-by, via Vyāsatīrtha)
- `vyasatirtha` ↔ `madhusudana` (the *Nyāyāmṛta* / *Advaita-Siddhi* exchange)
- `bhaskara` ↔ `sankara` (māyā-as-Buddhist-import polemic)
- `yadava-prakasa` ↔ `ramanuja` (teacher-then-rival, Rāmānuja's break)
- `mandana` ↔ `sureshvara` (bhāvanā / jñāna; jīva- vs. Brahman-as-locus-of-avidyā)
- `vedanta-desika` ↔ `pillai-lokacarya` (Vaḍakalai / Tenkalai monkey-cat)
- `bhartrprapanca` is-refuted-by `sankara` (Bṛhadāraṇyaka-Bhāṣya)
- `caitanya` ↔ `kesava-kasmiri` (debate-tradition conduit)
- `sankara` refutes `bhartrprapanca` (separately recorded on `sankara`)
- `madhva` refutes `sankara` (the Māyāvāda-Khaṇḍana / Mithyātvānumāna-Khaṇḍana / Upādhi-Khaṇḍana triad)
- `ramanuja` refutes `sankara` (the sapta-vidhā-anupapatti)

## Lineage cross-references — all resolve

A scripted check confirmed every `lineage_in`, `lineage_out`, and
`lineage_polemical[].thinker_id` reference points to an existing thinker file.
There are zero dangling references.

Notes on edges that needed inference from CORPUS_PLAN.md:
- `bodhayana → nathamuni → ramanuja` claimed-lineage encoded as
  `bodhayana.lineage_out = [nathamuni, ramanuja]`.
- `upavarsa` claimed by both: encoded as `lineage_out = [sankara, ramanuja]`.
- `gaudapada → govinda → sankara`: `govinda` is not in CORPUS_PLAN, so the
  intermediate node is omitted; the direct edge `gaudapada → sankara` is recorded.
- `vacaspati.lineage_out` had `amalananda` (not in CORPUS_PLAN); removed
  from the edge to avoid dangling reference.
- `utpaladeva`'s `somananda` teacher-edge is omitted for the same reason
  (Somānanda not in CORPUS_PLAN); only the lineage_out to Abhinavagupta is recorded.

## Sub-school registry coverage

All 45 sub-school registry entries in `registries/sub_schools.json` are
referenced by at least one thinker, and every `sub_school` value used by a
thinker matches a registry `display_name` exactly.

## What Wave 1 must add

For every thinker:
- `core_thesis` (100–200 words)
- For every entry in `engaged_works[]`: `summary` (100–200 words)

## What Wave 2 must add

For every thinker: `key_passages[]` (3–8 passages each, with full
`panini_breakdown`, `english_close`, `why_this_passage`, `topic_tags`,
`sub_axes`).

## Naming-rule check

The internal project codename appears nowhere in any of the 60 thinker
files, the 4 registries, the manifest, or this audit document.
