# CORPUS_EXPANSION_v2

Second-pass expansion of the Vedānta interactive-timeline corpus. Section A specifies new thinker entries to be added (skeleton fields prefilled, ready for Wave-0 lift into JSON files). Section B specifies augmentations of `engaged_works[]` for existing entries whose work-lists are anemic.

All dating, blindness, lineage, and bibliographic claims here are sourced from web research conducted 2026-05-09 (citations footnoted at end). Where uncertainty remains it is flagged explicitly with `dates_tier: contested` and a note. The internal project codename does not appear anywhere in this document or in the planned data files.

The user voice-dictated a request for "a blind ācārya in modern Sanskrit who wrote a massive Sanskrit corpus going over the entire canon, defending Viśiṣṭādvaita." The candidate matching every constraint is **Jagadguru Rāmabhadrācārya** (Tulsī Pīṭha, Citrakūṭa) — see §A.2 for the identification argument.

---

## Section A — New thinkers to add

### A.1 Sri Aurobindo  →  `id: aurobindo`

Confidence: high.

| field | value |
|---|---|
| `id` | `aurobindo` |
| `name` | `Sri Aurobindo` |
| `name_iast` | `Śrī Aravinda` |
| `name_devanagari` | `श्री अरविन्द` |
| `alternate_names` | `["Aurobindo Ghose", "Aravinda Ghoṣa"]` |
| `dates_low` | `1872` |
| `dates_high` | `1950` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Colonial-era civil-records; Cambridge tripos rolls; British-Indian political-trial records (Alipore 1908); Pondicherry French-Indian records.` |
| `dates_evidence` | `[{"kind":"court-record","description":"British-Indian Alipore Conspiracy Case 1908–1909 trial records."}, {"kind":"court-record","description":"Cambridge University tripos rolls 1890–1892."}]` |
| `school` | `Advaita` (with `sub_school: "Pūrṇa-Advaita / Integral Vedānta"`; see note on color token) |
| `school_color_token` | `advaita` (shade 1, lightest, to mark distance from classical Advaita) — *or* introduce a new token `purna-advaita`; recommend the former for v2 to avoid schema bump |
| `sub_school` | `Pūrṇa-Advaita / Integral Vedānta` |
| `sub_school_shade` | `1` |
| `lineage_in` | `["sankara", "ramakrishna" (if added), "vidyaranya"]` — Aurobindo cites the *Upaniṣads*, the *Gītā*, *Veda* directly; affiliates with no living lineage; treats Śaṅkara as the position to be qualified-and-completed rather than refuted. |
| `lineage_out` | `[]` (Mirra Alfassa "Mother", K.D. Sethna, Nolini Kanta Gupta, Haridas Chaudhuri, M.P. Pandit, Medhānanda are downstream — add later if they enter the corpus). |
| `lineage_polemical` | `[{"thinker_id":"sankara","direction":"refutes","note":"Aurobindo's Pūrṇa-Advaita explicitly affirms the reality of the manifest world against any reading of Śaṅkara that makes the world ultimately mithyā in the sense of unreal; he reads māyā as the differentiating-creative power of Cit-Śakti rather than as an illusion-faculty. The relation is qualified-completion, not flat refutation — but the polemical edge is real."}]` |
| `core_thesis` (draft, ~170 words) | "Sri Aurobindo's Pūrṇa-Advaita (Integral Vedānta) holds that Brahman is *Saccidānanda* whose self-multiplication is real, progressive, and teleological. The world is not *māyā* in the sense of cosmic illusion but the ordered self-manifestation of a single Reality through descending grades — *Sat*, *Cit-Tapas*, *Ānanda*, *Supermind* (Vijñāna), Mind, Life, Matter — and through a corresponding *evolutionary ascent* in which matter, life, and mind are progressive recoveries of the involved Spirit. The *jīva* is a real and irreducible *centre* of the Divine, not an apparent reflection to be cancelled. Liberation is not flight from the world but the descent of Supermind into mind, life, and body — a transformation he calls *divinisation* — which is the proper completion of Vedāntic siddhi. Against Śaṅkara, illusionism is rejected; against Rāmānuja, the *cit/acit/Īśvara* triad is preserved but reinterpreted as gradient self-poises of one *Saccidānanda*. The *Veda* itself, esoterically read, already teaches this evolutionary spirituality." |
| `engaged_works[]` | (8 entries, see below) |

**Engaged works (work titles + ascription_tier; Wave-1 fills `summary`):**

1. `the-life-divine` — *The Life Divine* (English) — `ascription_tier: securely-authored`. *Composition_dates_low: 1914, _high: 1940* (Arya serialisation 1914–1919, revised book 1939–1940). `genre: prakarana`. The systematic metaphysics; the load-bearing text for the school's ontology.
2. `essays-on-the-gita` — *Essays on the Gītā* (English) — `securely-authored`. *Comp. 1916–1920*; book 1922 (First Series), 1928 (Second Series). `genre: gita-bhashya`.
3. `the-synthesis-of-yoga` — *The Synthesis of Yoga* (English) — `securely-authored`. *Comp. 1914–1921 (Arya); revised partial 1955*. `genre: prakarana`. The integral *yoga* synthesising karma, jñāna, bhakti, and rāja.
4. `the-secret-of-the-veda` — *The Secret of the Veda* + *Hymns to the Mystic Fire* — `securely-authored`. *Comp. 1914–1917 (Arya)*. `genre: prakarana`. Esoteric symbolic re-reading of the Ṛgveda.
5. `isha-upanishad` — *Īśopaniṣad* commentary — `securely-authored`. *Comp. 1914–1915 (Arya); book c. 1921*. `genre: upanisad-bhashya`.
6. `kena-upanishad` — *Kena Upaniṣad* commentary — `securely-authored`. `genre: upanisad-bhashya`.
7. `eight-upanishads` — Translations and short commentaries on Īśa, Kena, Kaṭha, Muṇḍaka, Praśna, Māṇḍūkya, Aitareya, Taittirīya — `securely-authored`. `genre: upanisad-bhashya`.
8. `savitri` — *Savitri: A Legend and a Symbol* — `securely-authored` (book 1950–1951). `genre: prakarana` (verse-epic doctrinal exposition; flag explicitly as not-bhāṣya, but as the imaginative-doctrinal magnum opus on the same metaphysics).

**Recommendation on the school-token question.** Keep `school_color_token: advaita` and use `sub_school_shade: 1` to render Pūrṇa-Advaita as the lightest blue, visually distinct from Bhāmatī (2), Vivaraṇa (3), classical-Śaṅkara (4), Madhusūdana-late (5). Justification: (i) Aurobindo himself names the school *Advaita*; (ii) he reads Śaṅkara as a partial-truth, not as a different school; (iii) avoiding a schema bump is good engineering. If the user later wants a separate token, introduce `purna-advaita` at a v3 schema bump and set `parent_school_color_token: advaita` in `sub_schools.json`.

---

### A.2 Jagadguru Rāmabhadrācārya  →  `id: rambhadracharya` (the "blind ācārya" identification)

Confidence: high. **This is the user's blind-ācārya.** The user described "a blind ācārya in modern Sanskrit who wrote a massive Sanskrit corpus going over the entire canon, defending Viśiṣṭādvaita." Every constraint matches Rāmabhadrācārya:

- **Blind**: blind from the age of two months, never used Braille; learns by hearing and composes by dictation.
- **Modern**: born 14 January 1950; living jagadguru.
- **Massive Sanskrit corpus over the entire canon**: he authored *Śrīrāghavakṛpā-Bhāṣyam*, a Sanskrit commentary set covering the *full prasthāna-trayī* — *Brahma-Sūtra* + *Bhagavad-Gītā* + the eleven principal Upaniṣads (Īśa, Kena, Kaṭha, Praśna, Muṇḍaka, Māṇḍūkya, Aitareya, Taittirīya, Chāndogya, Bṛhadāraṇyaka, Śvetāśvatara) + the *Nārada-Bhakti-Sūtra*. The set was released by PM Vajpayee on 10 April 1998 and is described as "the first Sanskrit commentary on the prasthāna-trayī in nearly 500 years" and "the second Sanskrit prasthāna-trayī commentary in the Rāmānanda-Sampradāya" (the first being Rāmānanda's own *Ānanda-Bhāṣya*). Total output: 240+ books, 50+ papers, including a Sanskrit verse commentary on Pāṇini's *Aṣṭādhyāyī*.
- **Defending Viśiṣṭādvaita**: he is the head (jagadguru) of the **Rāmānanda Sampradāya**, whose Vedāntic affiliation is Viśiṣṭādvaita — though specifically Rāma-centric rather than Nārāyaṇa-centric. The Rāmānandīs trace their lineage to Rāmānanda (14th–15th c.), who is in turn placed in a teacher-line descending from Rāmānuja. Rāmabhadrācārya's *Śrīrāghavakṛpā-Bhāṣyam* explicitly defends Viśiṣṭādvaita as the school's reading.

The user's verbal description does not perfectly fit any other living scholar. Other candidates considered and ruled out:

- **Uttamur T. Vīrarāghavācārya** (1897–1983): authored ~185 works, magnum opus *Paramārtha-Bhūṣaṇa* defending Vedānta-Deśika. Massive Viśiṣṭādvaita corpus — but no source confirms he was blind. Recommend adding him *anyway* (see A.3 below) but he is not the user's blind-ācārya.
- **Mahāmahopādhyāya N.S. Anantakrishna Sastri** (1886–1962): defended *Advaita* (not Viśiṣṭādvaita), edited *Advaita-Siddhi*/*Nyāyāmṛta*, authored *Śatabhūṣaṇī* refuting Viśiṣṭādvaita. Wrong school.
- **Bannanje Govindācārya** (1936–2020): Dvaita not Viśiṣṭādvaita. Not blind.
- **Karpātrī** (1907–1982): Advaita, not blind.

**Identification confidence: very high. Rāmabhadrācārya is the entry the user wants.**

| field | value |
|---|---|
| `id` | `rambhadracharya` |
| `name` | `Jagadguru Rambhadracharya` |
| `name_iast` | `Jagadguru Rāmabhadrācārya` |
| `name_devanagari` | `जगद्गुरु रामभद्राचार्य` |
| `alternate_names` | `["Giridhar Mishra", "Giridhara Miśra (birth name)", "Rāmānandācārya (jagadguru-title)"]` |
| `dates_low` | `1950` |
| `dates_high` | `0` (living; use convention `0` or current-year-as-cap with note — recommend leaving `dates_high` open and flagging in `dates_notes`; if schema requires int, use `2026` and set `dates_notes` accordingly) |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Living jagadguru; born 14 January 1950 in Shandikhurd, Jaunpur (UP); blind from age two months; appointed Jagadguru Rāmānandācārya 1988, ritually anointed 1 August 1995; head of Tulsī Pīṭha, Citrakūṭa.` |
| `dates_evidence` | `[{"kind":"court-record","description":"Government of India Padma awards records (Padma Vibhūṣaṇa, Padma Bhūṣaṇa)."}, {"kind":"manuscript-colophon","description":"Tulsī Pīṭha publication colophons; release ceremony of Śrīrāghavakṛpā-Bhāṣyam by PM A.B. Vajpayee, 10 April 1998."}]` |
| `school` | `Viśiṣṭādvaita` |
| `school_color_token` | `vishishtadvaita` |
| `sub_school` | `Rāmānanda-Sampradāya (Rāma-Viśiṣṭādvaita)` |
| `sub_school_shade` | `5` (modern terminus of the Viśiṣṭādvaita color-line; visually distinct from Vaḍakalai/Tenkalai which are Nārāyaṇa-centric Śrīvaiṣṇava) |
| `lineage_in` | `["ramanuja"]` (via Rāmānanda) — flag in dates_notes that the historical chain Rāmānuja → Rāmānanda is sectarian-traditional, contested by some modern historians. |
| `lineage_out` | `[]` |
| `lineage_polemical` | `[]` |
| `core_thesis` (draft, ~165 words) | "Rāmabhadrācārya, jagadguru of the Rāmānanda Sampradāya, gives Viśiṣṭādvaita a Rāma-centric formulation: the *parabrahman* of the Upaniṣads is *Sītā-Rāma*, and the *śarīra-śarīri-bhāva* of Rāmānuja is preserved with Rāma as *śarīrin*, *cit* and *acit* as his real body. His *Śrīrāghavakṛpā-Bhāṣyam* (1998) is the first Sanskrit commentary on the full *prasthāna-trayī* in roughly five centuries and the Rāmānanda Sampradāya's second after Rāmānanda's own *Ānanda-Bhāṣya*. Methodologically he insists on Rāma as the supreme reality (*pratipādya*) of every Upaniṣad and every *sūtra* of Bādarāyaṇa, reading the *mahā-vākyas* through the body-soul template Rāmānuja established. He composes by dictation — blind from infancy and never having used Braille — and his oeuvre of 240+ books in Sanskrit, Hindi, and other languages includes a verse-commentary on Pāṇini's *Aṣṭādhyāyī*, four Sanskrit *mahā-kāvyas*, and Hindi commentaries on Tulsīdās." |

**Engaged works:**

1. `shri-raghava-kripa-bhashyam-brahma-sutra` — *Śrīrāghavakṛpā-Bhāṣyam on Brahma-Sūtra* — `securely-authored`. *Comp. by 1998*. `genre: sutra-bhashya`. `language: sanskrit`.
2. `shri-raghava-kripa-bhashyam-gita` — *Śrīrāghavakṛpā-Bhāṣyam on Bhagavad-Gītā* — `securely-authored`. *1998*. `genre: gita-bhashya`. `language: sanskrit`.
3. `shri-raghava-kripa-bhashyam-upanishads` — *Śrīrāghavakṛpā-Bhāṣyam on the Eleven Principal Upaniṣads* (Īśa, Kena, Kaṭha, Praśna, Muṇḍaka, Māṇḍūkya, Aitareya, Taittirīya, Chāndogya, Bṛhadāraṇyaka, Śvetāśvatara) — `securely-authored`. *1998*. `genre: upanisad-bhashya`. `language: sanskrit`.
4. `shri-raghava-kripa-bhashyam-narada-bhakti-sutra` — *Śrīrāghavakṛpā-Bhāṣyam on Nārada-Bhakti-Sūtra* — `securely-authored`. *1998*. `genre: sutra-bhashya`. `language: sanskrit`.
5. `ashtadhyayi-pradipa` — Sanskrit verse-commentary on Pāṇini's *Aṣṭādhyāyī* — `securely-authored`. `genre: varttika`. `language: sanskrit`. Include only insofar as it bears on his Vedāntic exegetical method.

---

### A.3 Uttamur Vīrarāghavācārya  →  `id: uttamur-viraraghavacharya`

Confidence: high. Add as a 20th-century Vaḍakalai Viśiṣṭādvaita systematic-scholastic.

| field | value |
|---|---|
| `id` | `uttamur-viraraghavacharya` |
| `name` | `Uttamur Viraraghavachariar` |
| `name_iast` | `Uttamūr Vīrarāghavācārya` |
| `alternate_names` | `["Abhinava Deśika", "Abhinava Deśikācārya", "U.V. Vīrarāghavācārya", "Uthamur Swami"]` |
| `dates_low` | `1897` |
| `dates_high` | `1983` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 26 January 1897 (Tamil Thai-Svāti) at Uttamanallur, Madhurāntakam, Tamil Nadu; died 1983. First recipient of the Government of India President's Award for Sanskrit scholarship (1960); honorific "Abhinava Deśika" awarded for his Vedānta-Deśika commentaries.` |
| `dates_evidence` | `[{"kind":"court-record","description":"Government of India President's Award for Sanskrit scholarship, 1960 (first-ever recipient)."}, {"kind":"manuscript-colophon","description":"Sri Uttamur Viraraghavachariar Centenary Trust publication records (1997 onward)."}]` |
| `school` | `Viśiṣṭādvaita` |
| `school_color_token` | `vishishtadvaita` |
| `sub_school` | `Vaḍakalai (modern systematic)` |
| `sub_school_shade` | `4` |
| `lineage_in` | `["vedanta-desika", "ramanuja"]` (textual; not gurupāramparā) |
| `lineage_out` | `[]` |
| `core_thesis` (draft, ~170 words) | "Uttamūr Vīrarāghavācārya, honoured as *Abhinava Deśika* for his commentaries on Vedānta-Deśika's corpus, is the 20th-century consolidator of Vaḍakalai Viśiṣṭādvaita scholasticism. Author of approximately 185 Sanskrit and Tamil works, his magnum opus *Paramārtha-Bhūṣaṇa* is a polemical defense of Vedānta-Deśika's positions against later Advaita and Tenkalai criticisms; his *Sarvārtha-Siddhi* commentary on Deśika's *Tattva-Muktā-Kalāpa*, his *Śrī-Bhāṣyārtha-Darpaṇa* on Rāmānuja's *Śrī-Bhāṣya*, his commentary on Nyāya-Pariśuddhi, and his glosses on Yāmuna and Nadādūr Ammāḷ together constitute the most comprehensive 20th-century re-articulation of the Vaḍakalai system. Distinctive emphases: full integration of Navya-Nyāya logical apparatus into Viśiṣṭādvaita exegesis (his *Vaiśeṣika-Rasāyana* and *Mīmāṃsā-Nyāya-Prakāśa* commentaries demonstrate this), systematic recovery of pre-Deśika Śrīvaiṣṇava sources, and unwavering defense of *upāya-vaibhava* — works (Vaḍakalai) against effortless surrender (Tenkalai) — as the soteriological backbone of the school." |

**Engaged works (10 representative):**

1. `paramartha-bhushana` — *Paramārtha-Bhūṣaṇa* — `securely-authored`. `genre: polemical-tract`. Magnum opus polemic defending Deśika.
2. `shri-bhashyartha-darpana` — *Śrī-Bhāṣyārtha-Darpaṇa* — `securely-authored`. `genre: tika`. Commentary on Rāmānuja's *Śrī-Bhāṣya*.
3. `sarvartha-siddhi-vyakhya` — Commentary on Deśika's *Sarvārtha-Siddhi* (and thereby on *Tattva-Muktā-Kalāpa*) — `securely-authored`. `genre: tika`.
4. `nyaya-parishuddhi-vyakhya` — Commentary on Deśika's *Nyāya-Pariśuddhi* — `securely-authored`. `genre: tika`.
5. `acharya-bhashya-tatparya` — Gloss on Deśika's *Īśāvāsya-Upaniṣad-Bhāṣya* — `securely-authored`. `genre: tika`.
6. `sararatha-ratna-prabha` — *Sārārtha-Ratna-Prabhā* on Deśika's *Adhikaraṇa-Sārāvalī* — `securely-authored`. `genre: tika`.
7. `nyaya-kusumanjali-vyakhya` — Commentary on Udayana's *Nyāya-Kusumāñjali* — `securely-authored`. `genre: tika`. (Demonstrates Navya-Nyāya integration.)
8. `vaisheshika-rasayana` — *Vaiśeṣika-Rasāyana* on Kaṇāda's *Vaiśeṣika-Sūtra* — `securely-authored`. `genre: tika`.
9. `mimamsa-nyaya-prakasha-vyakhya` — Commentary on Āpadeva's *Mīmāṃsā-Nyāya-Prakāśa* — `securely-authored`. `genre: tika`.
10. `prabandha-raksha` — *Prabandha-Rakṣā* (Tamil commentary on the *Nālāyira-Divya-Prabandham*) — `securely-authored`. `language: tamil-manipravala`. `genre: tika`. (For the *ubhaya-Vedānta* synthesis the school requires.)

---

### A.4 Raṅgarāmānuja Muni  →  `id: rangaramanuja`

Confidence: high. Pre-modern (16th–17th c.), but a major Viśiṣṭādvaita figure missing from the corpus.

| field | value |
|---|---|
| `id` | `rangaramanuja` |
| `name` | `Rangaramanuja Muni` |
| `name_iast` | `Raṅgarāmānuja Muni` |
| `alternate_names` | `["Upaniṣad-Bhāṣyakāra", "Raṅga-Rāmānuja"]` |
| `dates_low` | `1550` |
| `dates_high` | `1650` |
| `dates_tier` | `consensus-textual` |
| `dates_notes` | `Late 16th to mid-17th century; pupil of Pañcamabhañjana Tāta-deśika and Vatsya Anantācārya; dated by manuscript chronology and gurupāramparā.` |
| `school` | `Viśiṣṭādvaita` |
| `school_color_token` | `vishishtadvaita` |
| `sub_school` | `Vaḍakalai (Upaniṣad-bhāṣya tradition)` |
| `sub_school_shade` | `3` |
| `lineage_in` | `["vedanta-desika", "sudarsana"]` (textual) |
| `lineage_out` | `["uttamur-viraraghavacharya"]` (textually descended via the Vaḍakalai pāṭhaśālā transmission) |
| `core_thesis` (draft, ~150 words) | "Raṅgarāmānuja Muni, honoured in his school as *Upaniṣad-Bhāṣyakāra*, is the first ācārya of the Viśiṣṭādvaita tradition to compose Sanskrit *bhāṣyas* on the principal Upaniṣads — a corpus Rāmānuja himself never wrote. Working in the post-Vedānta-Deśika Vaḍakalai milieu, he produced commentaries on Kena, Kaṭha, Praśna, Muṇḍaka, Māṇḍūkya, Taittirīya, Chāndogya, Bṛhadāraṇyaka, Mantrika, Kauṣītaki, Śvetāśvatara and Mahā-Nārāyaṇa Upaniṣads, each fitting the Upaniṣadic teaching to the *śarīra-śarīrin* template Rāmānuja established for the *Brahma-Sūtra*. His *Viṣaya-Vākya-Dīpikā* glosses the Upaniṣadic passages quoted in the *Śrī-Bhāṣya*, and his *Śārīraka-Śāstra-Dīpikā* compresses Rāmānuja's whole *sūtra*-system. His one independent work *Siddhānta-Sāra* states the school's tenets in compendious form." |

**Engaged works (representative):**

1. `upanishad-bhashyas` — Sanskrit *bhāṣyas* on twelve principal Upaniṣads (Kena, Kaṭha, Praśna, Muṇḍaka, Māṇḍūkya, Taittirīya, Chāndogya, Bṛhadāraṇyaka, Mantrika, Kauṣītaki, Śvetāśvatara, Mahā-Nārāyaṇa) — `securely-authored`. `genre: upanisad-bhashya`. (Treat as a single bundle work-id with sub-loci, or 12 separate work_ids — recommend the bundle for v2.)
2. `vishaya-vakya-dipika` — *Viṣaya-Vākya-Dīpikā* — `securely-authored`. `genre: tika`.
3. `sruta-prakashika-bhava-prakashika` — *Śruta-Prakāśikā-Bhāva-Prakāśikā* (sub-commentary on Sudarśana Sūri's *Śruta-Prakāśikā*) — `securely-authored`. `genre: tika`.
4. `nyaya-siddhanjana-vyakhya` — Commentary on Vedānta-Deśika's *Nyāya-Siddhāñjana* — `securely-authored`. `genre: tika`.
5. `shariraka-shastra-dipika` — *Śārīraka-Śāstra-Dīpikā* — `securely-authored`. `genre: tika`.
6. `siddhanta-sara` — *Siddhānta-Sāra* — `securely-authored`. `genre: prakarana`.

---

### A.5 Mahāmahopādhyāya N.S. Anantakrishna Sastri  →  `id: anantakrishna-sastri`

Confidence: high. Modern Advaita; not blind, but the editor whose critical editions of *Advaita-Siddhi* and *Nyāyāmṛta* underwrite all 20th-century engagement with the polemic.

| field | value |
|---|---|
| `id` | `anantakrishna-sastri` |
| `name` | `Anantakrishna Sastri` |
| `name_iast` | `Anantakṛṣṇa Śāstrī` |
| `alternate_names` | `["Mahāmahopādhyāya N.S. Anantakrishna Sastri", "Śāstra-Ratnākara"]` |
| `dates_low` | `1886` |
| `dates_high` | `1962` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 1886, Nūrāṇi village, Pālakkad district, Kerala; trained at Chittoor pāṭhaśālā and under Harihara Śāstrī at Cidambaram from 1904; lived and taught in Kolkata; held Mahāmahopādhyāya title.` |
| `school` | `Advaita` |
| `school_color_token` | `advaita` |
| `sub_school` | `Vivaraṇa (modern editorial-polemical)` |
| `sub_school_shade` | `5` |
| `lineage_in` | `["madhusudana", "brahmananda"]` (textual; he edited their works) |
| `lineage_out` | `[]` |
| `lineage_polemical` | `[{"thinker_id":"vyasatirtha","direction":"refutes","note":"His Śatabhūṣaṇī defends Advaita against Vyāsatīrtha-line and Viśiṣṭādvaita-line critiques."}]` |
| `core_thesis` (draft, ~150 words) | "Anantakṛṣṇa Śāstrī (1886–1962), Mahāmahopādhyāya and Śāstra-Ratnākara, is the modern editor and defender of late-Advaita scholasticism whose critical editions made the *Advaita-Siddhi* / *Nyāyāmṛta* / *Tarka-Tāṇḍava* dialectical exchange newly readable in the 20th century. His own polemical writings — *Śatabhūṣaṇī* against Viśiṣṭādvaita, *Advaita-Tattva-Sudhā*, *Advaita-Dīpikā*, *Vedānta-Rakṣā-Maṇi* — defend the Vivaraṇa Brahman-as-locus-of-avidyā position against both rival Vedāntic schools and against the modern Śuddha-Śāṅkara reformism of Satchidānandendra Saraswatī. His critical editions of *Vedānta-Paribhāṣā*, of *Advaita-Siddhi* with *Laghu-Candrikā*, and of the full *Nyāyāmṛta-Advaita-Siddhi* polemical exchange remain the standard texts in the modern pāṭhaśālā curriculum. He is the principal modern editorial conduit through which Madhusūdana, Brahmānanda, Vyāsatīrtha, and the late-scholastic Advaita-Dvaita debate reaches contemporary scholarship." |

**Engaged works (representative):**

1. `shatabhushani` — *Śatabhūṣaṇī* — `securely-authored`. `genre: polemical-tract`. Hundred-fold defense of Advaita against Viśiṣṭādvaita.
2. `advaita-tattva-sudha` — *Advaita-Tattva-Sudhā* — `securely-authored`. `genre: prakarana`.
3. `advaita-dipika` — *Advaita-Dīpikā* — `securely-authored`. `genre: prakarana`.
4. `vedanta-raksha-mani` — *Vedānta-Rakṣā-Maṇi* — `securely-authored`. `genre: polemical-tract`.
5. `editions-of-advaita-siddhi-and-nyayamrita` — Critical editions of *Advaita-Siddhi* with *Laghu-Candrikā* and *Nyāyāmṛta* (Nirṇaya Sāgara / Meharchand Lachhmandas) — flag as `securely-authored` (editorial labour) with `ascription_notes` distinguishing edition-work from authorship.
6. `vedanta-paribhasha-edition` — Critical edition of Dharmarāja's *Vedānta-Paribhāṣā* — same treatment.

---

### A.6 Swāmī Satchidānandendra Saraswatī  →  `id: satchidanandendra`

Confidence: high. Modern Advaita reformer; the *Mūlāvidyā-Nirāsa* author the user named.

| field | value |
|---|---|
| `id` | `satchidanandendra` |
| `name` | `Satchidanandendra Saraswati` |
| `name_iast` | `Saccidānandendra Sarasvatī` |
| `alternate_names` | `["Subba Rao (birth name)", "Holenarsipur Swami"]` |
| `dates_low` | `1880` |
| `dates_high` | `1975` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 5 January 1880; died 5 August 1975; founder of Adhyātma-Prakāśa-Kāryālaya, Holenarsipur, Hassan district, Karnataka.` |
| `dates_evidence` | `[{"kind":"manuscript-colophon","description":"Adhyātma-Prakāśa-Kāryālaya publication records 1929 onwards."}]` |
| `school` | `Advaita` |
| `school_color_token` | `advaita` |
| `sub_school` | `Śuddha-Śāṅkara-Prakriyā (modern revisionist)` |
| `sub_school_shade` | `2` (visually distinguished from Vivaraṇa/Bhāmatī as the modern *third* Advaita strand) |
| `lineage_in` | `["sankara"]` (claims to recover *the* Śaṅkara, against Vivaraṇa and Bhāmatī alike) |
| `lineage_out` | `[]` |
| `lineage_polemical` | `[{"thinker_id":"prakasatman","direction":"refutes","note":"Mūlāvidyā-Nirāsa argues the doctrine of mūlāvidyā as material cause is post-Śaṅkaran and absent from Śaṅkara's own bhāṣyas."}, {"thinker_id":"vacaspati","direction":"refutes","note":"Likewise rejects the Bhāmatī jīva-as-locus thesis as un-Śaṅkaran."}, {"thinker_id":"anantakrishna-sastri","direction":"mutual","note":"20th-century intra-Advaita polemic; Anantakrishna-line defends the post-Śaṅkara scholastic apparatus against Holenarsipur revisionism."}]` |
| `core_thesis` (draft, ~165 words) | "Satchidānandendra Sarasvatī (1880–1975), founder of the Adhyātma-Prakāśa-Kāryālaya at Holenarsipur, is the modern Advaitin who challenged the entire post-Śaṅkara scholastic edifice as a deviation from Śaṅkara's own *bhāṣya*-method. His *Mūlāvidyā-Nirāsa* (1929, Sanskrit) argues that the doctrine of *mūlāvidyā* as a positive material-cause of the world — central to Vivaraṇa Advaita and tacitly accepted by Bhāmatī — is foreign to Śaṅkara's own *Brahma-Sūtra-Bhāṣya*, *Bṛhadāraṇyaka-Bhāṣya*, and *Upadeśa-Sāhasrī*; for Śaṅkara *avidyā* is *adhyāsa* (superimposition), not a substance. He systematised this recovery as the *Śuddha-Śāṅkara-Prakriyā* school. His extensive Sanskrit and Kannada output — *Vedānta-Prakriyā-Pratyabhijñā*, *Śuddha-Śāṅkara-Prakriyā-Bhāskara*, *Māṇḍūkya-Rahasya-Vivṛti* — re-reads the post-Śaṅkara tradition (Sureśvara, Padmapāda, Maṇḍana, Vāchaspati, Prakāśātman) selectively, accepting only what conforms to the *adhyāsa-bhāṣya* method. The intra-Advaita controversy he initiated remains live in the modern pāṭhaśālā network." |

**Engaged works:**

1. `mulavidya-nirasa` — *Mūlāvidyā-Nirāsa* (1929) — `securely-authored`. `genre: polemical-tract`. `language: sanskrit`.
2. `vedanta-prakriya-pratyabhijna` — *Vedānta-Prakriyā-Pratyabhijñā* — `securely-authored`. `genre: prakarana`. `language: sanskrit`.
3. `shuddha-shankara-prakriya-bhaskara` — *Śuddha-Śāṅkara-Prakriyā-Bhāskara* — `securely-authored`. `genre: prakarana`. `language: sanskrit`.
4. `mandukya-rahasya-vivriti` — *Māṇḍūkya-Rahasya-Vivṛti* — `securely-authored`. `genre: upanisad-bhashya`. `language: sanskrit`.
5. `salient-features-of-shankara-vedanta` — *Salient Features of Śaṅkara-Vedānta* (English) — `securely-authored`. `genre: prakarana`.

---

### A.7 Bannanje Govindācārya  →  `id: bannanje-govindacharya`

Confidence: high. Modern Dvaita Sanskrit scholar.

| field | value |
|---|---|
| `id` | `bannanje-govindacharya` |
| `name` | `Bannanje Govindacharya` |
| `name_iast` | `Bannañje Govindācārya` |
| `alternate_names` | `["Vidyāvācaspati Bannanje Govindācārya"]` |
| `dates_low` | `1936` |
| `dates_high` | `2020` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 3 August 1936, Bannañje, Udupi (Karnataka); died 13 December 2020; Tulu-speaking Śivaḷḷi Brahmin Mādhva family; Padma Śrī (2009).` |
| `dates_evidence` | `[{"kind":"court-record","description":"Government of India Padma Śrī award 2009; Saṃskṛta-Sāhitya Akademi awards."}]` |
| `school` | `Dvaita` |
| `school_color_token` | `dvaita` |
| `sub_school` | `Tattvavāda (modern philological-textual)` |
| `sub_school_shade` | `5` |
| `lineage_in` | `["madhva", "raghavendra"]` (textual; not gurupāramparā in the maṭha sense) |
| `lineage_out` | `[]` |
| `core_thesis` (draft, ~160 words) | "Bannañje Govindācārya (1936–2020) is the modern Mādhva scholar whose Sanskrit philological-philosophical output — approximately 4,000 pages of Sanskrit *vyākhyāna* across some 150 books — re-establishes Madhva's full *Sarva-Mūla-Granthāḥ* as a critically-edited, textually-stable corpus and provides Dvaita commentaries (*bhāṣya*s and *vyākhyāna*s) on the *Veda-Sūktas*, the principal Upaniṣads, the *Śata-Rudriya*, the *Brahma-Sūtra*, the *Bhagavad-Gītā*, the *Mahābhārata-Tātparya-Nirṇaya*, and the *Bhāgavata-Purāṇa*. Trained at Pūrṇaprajña Vidyāpīṭha, Bengaluru, he combined Mahāmahopādhyāya-grade traditional learning with modern critical-editorial method. Distinctive emphases: textual recovery of Madhva's intended readings against later scholastic accretion, defense of the historical and philosophical priority of the *Bhāgavata*-tradition's Mādhva interpretation, and a working reconciliation of the Udupi *aṣṭa-maṭha* sectarian apparatus with academic Indology. The principal modern conduit through whom Madhva's full corpus reaches contemporary readers." |

**Engaged works (representative):**

1. `sarva-mula-grantha-edition` — Critical edition of Madhva's *Sarva-Mūla-Granthāḥ* — `securely-authored` (editorial). `genre: tika`.
2. `mahabharata-tatparya-nirnaya-vyakhyana` — Sanskrit *vyākhyāna* on Madhva's *Mahābhārata-Tātparya-Nirṇaya* — `securely-authored`. `genre: tika`.
3. `bhagavata-vyakhyana` — Sanskrit *vyākhyāna* on the *Bhāgavata-Purāṇa* (Mādhva reading) — `securely-authored`. `genre: tika`.
4. `upanishad-bhashyas` — Mādhva commentaries (or Mādhva-tradition glosses) on the principal Upaniṣads — `securely-authored`. `genre: upanisad-bhashya`.
5. `acharya-madhva-baduku-bareha` — *Ācārya Madhva: Baḍuku-Bareha* (biographical-critical, Kannada) — `securely-authored`. `language: kannada`. `genre: prakarana`.
6. `stuti-chandrika` — *Stuti-Candrikā* on Trivikrama Paṇḍita's *Vāyu-Stuti* — `securely-authored`. `genre: tika`.

---

### A.8 Bhaktisiddhānta Sarasvatī  →  `id: bhaktisiddhanta`

Confidence: high. Modern Gauḍīya systematic.

| field | value |
|---|---|
| `id` | `bhaktisiddhanta` |
| `name` | `Bhaktisiddhanta Saraswati` |
| `name_iast` | `Bhaktisiddhānta Sarasvatī` |
| `alternate_names` | `["Bimala Prasada (birth name)", "Bhaktisiddhānta Sarasvatī Ṭhākura Prabhupāda", "Siddhānta Sarasvatī"]` |
| `dates_low` | `1874` |
| `dates_high` | `1937` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 6 February 1874, Puri, Odisha; died 1 January 1937; son of Bhaktivinoda Ṭhākura; founder of the Gauḍīya Maṭha (1920); diksha from Gaurakiśora Dāsa Bābājī.` |
| `school` | `Acintya-Bhedābheda` |
| `school_color_token` | `acintya` |
| `sub_school` | `Gauḍīya Maṭha (modern systematic-institutional)` |
| `sub_school_shade` | `5` |
| `lineage_in` | `["bhaktivinoda", "jiva-gosvami", "baladeva"]` |
| `lineage_out` | `[]` (Bhaktivedānta Swāmī Prabhupāda → ISKCON downstream — add later if entered) |
| `core_thesis` (draft, ~160 words) | "Bhaktisiddhānta Sarasvatī (1874–1937), son of Bhaktivinoda Ṭhākura and founder of the Gauḍīya Maṭha (1920), is the systematiser through whom Caitanya's *acintya-bhedābheda* enters institutional twentieth-century Vaiṣṇavism. His *Anubhāṣya* on the *Caitanya-Caritāmṛta* (1915) is the principal modern doctrinal commentary on Kṛṣṇadāsa Kavirāja's biography, articulating *acintya-śakti* as the load-bearing concept of Gauḍīya metaphysics. His Sanskrit and Bengali commentary on the *Bhāgavata-Purāṇa* (1923–1935) re-reads the text through the *Ṣaṭ-Sandarbha* of Jīva Gosvāmī, and his *Brahma-Saṃhitā* commentary fixes the school's modern reading of that pre-modern hymn. Distinctive emphases: explicit polemic against Advaita as a deviation; institutional codification of *vaiṣṇava-dīkṣā* outside hereditary lineages; vigorous use of print-publication as *bṛhad-mṛdaṅga* (the great drum of Hari-saṅkīrtana). His direct disciple A.C. Bhaktivedānta Swāmī Prabhupāda extends the lineage globally via ISKCON." |

**Engaged works:**

1. `anubhashya-caitanya-caritamrita` — *Anubhāṣya* on *Caitanya-Caritāmṛta* (1915) — `securely-authored`. `genre: tika`. `language: bengali` (with Sanskrit commentary).
2. `bhagavata-commentary` — Bengali-Sanskrit commentary on *Bhāgavata-Purāṇa* (1923–1935) — `securely-authored`. `genre: tika`.
3. `brahma-samhita-commentary` — Commentary on *Brahma-Saṃhitā* (5th adhyāya) — `securely-authored`. `genre: tika`.
4. `vaishnava-siddhanta-mala` — *Vaiṣṇava-Siddhānta-Mālā* — `securely-authored`. `genre: prakarana`.
5. `editions-and-translations-of-gosvami-corpus` — Editorial output: editions of Rūpa, Sanātana, Jīva, Viśvanātha, Baladeva — `securely-authored` (editorial).

---

### A.9 Swāmī Karpātrī (Hariharānanda Sarasvatī)  →  `id: karpatri`

Confidence: medium-high. Modern Advaita revivalist; the user explicitly named him. His doctrinal output is more polemical-popular than *bhāṣya*-grade, so flag carefully.

| field | value |
|---|---|
| `id` | `karpatri` |
| `name` | `Swami Karpatri` |
| `name_iast` | `Svāmī Karpātrī (Hariharānanda Sarasvatī)` |
| `alternate_names` | `["Hariharānanda Sarasvatī (sannyāsa-name)", "Har Narayan Ojha (birth name)", "Karpātrī Mahārāja"]` |
| `dates_low` | `1907` |
| `dates_high` | `1982` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 1907 (Vikrama Saṃvat 1964); died 1982; founder of Akhil Bhāratīya Rāma-Rājya Pariṣad (1948); active in Banaras-pāṭhaśālā Advaita network.` |
| `school` | `Advaita` |
| `school_color_token` | `advaita` |
| `sub_school` | `Daśanāmī-Sarasvatī (modern dharmic-political revivalism)` |
| `sub_school_shade` | `4` |
| `lineage_in` | `["sankara", "vidyaranya", "madhusudana"]` (textual / sectarian) |
| `lineage_out` | `[]` |
| `core_thesis` (draft, ~155 words) | "Svāmī Karpātrī (1907–1982), born Har Nārāyaṇa Ojha and ordained Hariharānanda Sarasvatī, is the 20th-century Daśanāmī-Sarasvatī ascetic-scholar whose doctrinal-political mission combined orthodox Advaita Vedānta with vigorous public defense of *varṇāśrama-dharma* and *sanātana-dharma* against modern reformism. Known for ascetic rigour (he ate only what he could hold in a single hand — *kar-pātra* — whence his name), his Sanskrit and Hindi prose output spans Advaita doctrine (*Vedārtha-Pārijāta*, *Vedānta-Mīmāṃsā* series), *bhakti*-doctrine (*Bhakti-Sudhā*, *Saṅkīrtana-Mīmāṃsā*), Mīmāṃsā-grounded ritualism (*Varṇāśrama-Maryādā*), and political theology (*Mārksavāda aur Rāmarājya*). His engagement is more polemical-revivalist than *bhāṣya*-grade scholasticism, and his philosophical position is conservative orthodox Advaita rather than original systematic; he is included here for completeness of the modern living Advaita field and for his unmatched role in shaping post-independence orthodox public discourse." |

**Engaged works:**

1. `vedartha-parijata` — *Vedārtha-Pārijāta* — `traditionally-ascribed`. `genre: prakarana`. `language: sanskrit`.
2. `vedanta-mimamsa-series` — *Vedānta-Mīmāṃsā* (multi-volume) — `securely-authored`. `genre: prakarana`. `language: hindi` (with Sanskrit citations).
3. `sankirtana-mimamsa` — *Saṅkīrtana-Mīmāṃsā* — `securely-authored`. `genre: prakarana`.
4. `varnashrama-maryada` — *Varṇāśrama-Maryādā* — `securely-authored`. `genre: polemical-tract`.
5. `marxavad-aur-ramrajya` — *Mārksavāda aur Rāmarājya* — `securely-authored`. `language: hindi`. `genre: polemical-tract`. (Include only insofar as it bears on Vedāntic public theology.)

---

### A.10 Chandraśekhara Bhāratī III (Sringeri)  →  `id: chandrashekhara-bharati`

Confidence: medium-high. Adds 20th-century Sringeri-paṭṭa Advaita continuity. Light philosophical output but doctrinally consequential.

| field | value |
|---|---|
| `id` | `chandrashekhara-bharati` |
| `name` | `Chandrashekhara Bharati III` |
| `name_iast` | `Candraśekhara Bhāratī III` |
| `alternate_names` | `["Narasiṃha Śāstrī (birth name)", "Jagadguru Śaṅkarācārya of Śṛṅgerī (1912–1954)"]` |
| `dates_low` | `1892` |
| `dates_high` | `1954` |
| `dates_tier` | `confirmed-from-records` |
| `dates_notes` | `Born 1892; sannyāsa-dīkṣā 7 April 1912 from Satyānanda Sarasvatī; jagadguru of Sringeri Śāradā Pīṭha 1912–1954.` |
| `school` | `Advaita` |
| `school_color_token` | `advaita` |
| `sub_school` | `Śṛṅgerī-paṭṭa (modern living-Advaita)` |
| `sub_school_shade` | `4` |
| `lineage_in` | `["sankara", "vidyaranya"]` (Śṛṅgerī gurupāramparā) |
| `lineage_out` | `[]` |
| `core_thesis` (draft, ~155 words) | "Candraśekhara Bhāratī III (1892–1954), Jagadguru of the Śṛṅgerī Śāradā Pīṭha 1912–1954, embodies the 20th-century continuity of the classical Advaita maṭha-tradition founded by Śaṅkara's disciple Sureśvara. His Sanskrit *Vivekacūḍāmaṇi-Bhāṣya* (commentary on the school-ascribed *Vivekacūḍāmaṇi*) is the principal philosophical text he wrote, articulating the standard Vivaraṇa-Bhāmatī-synthesis Advaita of the modern Śṛṅgerī curriculum: *adhyāsa* of *jīva* on *Brahman*, *māyā* as the *upādhi* of *Īśvara*, *jñāna-niṣṭhā* as the operative *sādhana*. His *Gururāja-Sūkti-Mālikā* (36 short Sanskrit compositions in c. 400 pages) is the doctrinal-poetic record of his upadeśa to disciples. Beyond his written corpus he is consequential as the embodied institutional witness that the unbroken Śṛṅgerī succession from Śaṅkara is doctrinally living rather than merely ceremonial — an essential datum for the timeline's modern terminus on the Advaita line." |

**Engaged works:**

1. `vivekachudamani-bhashya` — Sanskrit commentary on the school-ascribed *Vivekacūḍāmaṇi* — `securely-authored`. `genre: tika`. (Note that the *Vivekacūḍāmaṇi* itself is `school-ascribed` to Śaṅkara — see the existing Śaṅkara entry.)
2. `gururaja-sukti-malika` — *Gururāja-Sūkti-Mālikā* — `securely-authored`. `genre: stotra`/`prakarana`. `language: sanskrit`.
3. `recorded-discourses` — Recorded oral upadeśa — `traditionally-ascribed`. `genre: dialogue`.

---

### A.11 — Optional / lower priority

Recommend deferring (note as `to-evaluate` for v3):

- **Bhārati Kṛṣṇa Tīrtha** (1884–1960): Govardhan-paṭṭha jagadguru; *Vedic Mathematics* is famous but not Vedāntic; his Sanskrit doctrinal output is thin. Defer unless user pushes.
- **Dayānanda Sarasvatī** (Ārya Samāj, 1824–1883): wrote *Ṛgveda-Bhāṣya* (incomplete, mandalas 1–7.61) but his hermeneutic explicitly *rejects* Vedānta proper as a darśana — he treats the *Brahma-Sūtra* as un-Vedic. Including him as a Vedāntin misrepresents his project. **Recommend NOT adding.** If included, must be flagged `school: Cross-tradition` with `school_color_token: cross-tradition` and note that he positions himself *against* the *Brahma-Sūtra*-bhāṣya tradition.
- **Mirra Alfassa ("the Mother")**: doctrinally downstream of Aurobindo; not an independent Vedāntin. Defer.
- **Medhānanda / Sri M. P. Pandit / Haridas Chaudhuri / Nolini Kanta Gupta**: Aurobindonian lineage. The user asked specifically about Maharaj/Medhānanda. Recommendation: add Medhānanda only if the user wants the Aurobindonian line extended *and* if his published Sanskrit/English doctrinal output is substantive enough to merit a timeline node. From available evidence Medhānanda is primarily a contemplative-pedagogical figure rather than a *bhāṣyakāra*; **defer to v3 pending user confirmation**.
- **Bhārata-Tīrtha** (current Sringeri jagadguru, b. 1951) and **Vidhuśekhara Bhāratī** (current Sringeri jagadguru): living-tradition continuity; defer to v3.
- **A.C. Bhaktivedānta Swāmī Prabhupāda** (1896–1977): Gauḍīya; defer pending evaluation of whether his *Bhagavad-Gītā As It Is* and *Śrīmad-Bhāgavatam* commentary qualify as *bhāṣya*-grade Vedāntic engagement or are primarily pedagogical-popular.

---

## Section A summary table (for skeleton-generation by Wave-0 follow-up)

| id | name | dates | school | sub_school | shade | priority |
|---|---|---|---|---|---|---|
| `aurobindo` | Sri Aurobindo | 1872–1950 | Advaita | Pūrṇa-Advaita / Integral Vedānta | 1 | **must-add** |
| `rambhadracharya` | Jagadguru Rāmabhadrācārya | 1950– | Viśiṣṭādvaita | Rāmānanda-Sampradāya | 5 | **must-add (the blind ācārya)** |
| `uttamur-viraraghavacharya` | Uttamur Vīrarāghavācārya | 1897–1983 | Viśiṣṭādvaita | Vaḍakalai modern | 4 | must-add |
| `rangaramanuja` | Raṅgarāmānuja Muni | c. 1550–1650 | Viśiṣṭādvaita | Vaḍakalai (Upaniṣad-bhāṣya) | 3 | must-add |
| `anantakrishna-sastri` | Anantakrishna Sastri | 1886–1962 | Advaita | Vivaraṇa modern editorial | 5 | must-add |
| `satchidanandendra` | Satchidānandendra Sarasvatī | 1880–1975 | Advaita | Śuddha-Śāṅkara-Prakriyā | 2 | must-add |
| `bannanje-govindacharya` | Bannañje Govindācārya | 1936–2020 | Dvaita | Tattvavāda modern | 5 | must-add |
| `bhaktisiddhanta` | Bhaktisiddhānta Sarasvatī | 1874–1937 | Acintya-Bhedābheda | Gauḍīya Maṭha | 5 | must-add |
| `karpatri` | Svāmī Karpātrī | 1907–1982 | Advaita | Daśanāmī-Sarasvatī revivalism | 4 | should-add |
| `chandrashekhara-bharati` | Candraśekhara Bhāratī III | 1892–1954 | Advaita | Śṛṅgerī-paṭṭa | 4 | should-add |

**Total Section-A new entries: 10.**

(Also recommend lineage-graph edges added when these are inserted: `bhaktivinoda → bhaktisiddhanta`; `madhva → bannanje-govindacharya` (textual); `vedanta-desika → uttamur-viraraghavacharya`, `→ rangaramanuja`; `ramanuja → rambhadracharya` (via Rāmānanda); `madhusudana → anantakrishna-sastri` (textual); `prakasatman ← refutes-by satchidanandendra`.)

---

## Section B — Augmentations to existing entries

Identify thinkers whose `engaged_works[]` is anemic and specify additions. (Audited the existing 60 entries; the worst offenders are flagged below.)

### B.1 `caitanya` — currently 2 works (anemic)

Caitanya wrote almost nothing himself, so the work-list will remain short. But two additions are warranted:

- Add `work_id: rama-nanda-samvada` — *Rāmānanda-Saṃvāda* (the Caitanya–Rāmānanda Rāya dialogue preserved in *Caitanya-Caritāmṛta* 2.8) as a doctrinal-dialogue work-entry, `school-ascribed`, `genre: dialogue`, `language: bengali` — because it is the single most-cited Caitanya doctrinal source after the *Śikṣāṣṭakam* and is currently buried inside the generic "doctrine recorded by disciples" entry.
- Add `work_id: dasha-mula-shiksha` — *Daśa-Mūla-Śikṣā* (the ten foundational principles attributed to Caitanya, articulated in *Caitanya-Caritāmṛta* 2.6) as a doctrinal-summary work-entry, `school-ascribed`, `genre: prakarana`.

Net: caitanya goes from 2 → 4 work entries.

### B.2 `ramanuja` — currently 7 works; could add 2 more

- Add `work_id: nityam` — *Nityam* (sometimes treated as identical with *Nitya-Grantha*; cross-check with the existing entry to avoid duplication) — defer pending audit.
- Add `work_id: gadya-trayam-individual-entries` — *not* a new addition; the existing `gadya-trayam` already correctly bundles all three. No action.
- **Recommended addition:** `work_id: bhagavad-vishaya-tippani` — short marginalia/notes on *Bhāgavata*-passages preserved in early Śrīvaiṣṇava maṇi-pravāḷa anthologies — `traditionally-ascribed`. Low-priority; defer to v3.

Net: rāmānuja's list is actually adequate. **No urgent change.**

### B.3 `sankara` — currently rich; spot-check only

The existing Śaṅkara entry should already cover the *bhāṣya* corpus. Audit recommendation: confirm presence of *Bṛhadāraṇyaka-Bhāṣya* (cited in CORPUS_PLAN) and add explicitly if missing; confirm the *school-ascribed* layer (*Vivekacūḍāmaṇi*, *Aparokṣānubhūti*, *Saundarya-Laharī*, *Bhaja-Govindam*, *Śivānanda-Laharī*) is each a separate work-entry rather than bundled. (Bundling defeats the *ascription_filter* mechanism the *comparative_claim* schema was designed for.) **Action: spot-audit; bump to separate entries if currently bundled.**

### B.4 `madhva` — confirm full *Sarva-Mūla* coverage

CORPUS_PLAN names: *Brahma-Sūtra-Bhāṣya*, *Anuvyākhyāna*, *Gītā-Bhāṣya*, *Tattvodyota*, *Māyāvāda-Khaṇḍana*, *Mithyātvānumāna-Khaṇḍana*, *Upādhi-Khaṇḍana*, *Viṣṇu-Tattva-Vinirṇaya*, *Bhāgavata-Tātparya-Nirṇaya*, "the 37 *grantha*s of the *Sarva-Mūla*". Verify all 9 named works are individual `engaged_works[]` entries, plus add at minimum:

- `work_id: rg-bhashya` — *Ṛg-Bhāṣya* (Madhva's commentary on the first 40 sūktas of the Ṛgveda) — `securely-authored`.
- `work_id: aitareya-bhashya` — *Aitareya-Upaniṣad-Bhāṣya* — `securely-authored`.
- `work_id: chandogya-bhashya` — *Chāndogya-Upaniṣad-Bhāṣya* — `securely-authored`.
- `work_id: ten-prakaranas` — bundle the *Daśa-Prakaraṇa* (the ten short polemical treatises including those already named, plus *Kathā-Lakṣaṇa*, *Pramāṇa-Lakṣaṇa*, *Karma-Nirṇaya*, *Tattva-Saṅkhyāna*, *Tattva-Viveka*, *Sad-Ācāra-Smṛti*) — `securely-authored`.

Net: Madhva should go from c. 9 to c. 13–15 individual work-entries.

### B.5 `nimbarka` — currently underweight

CORPUS_PLAN names only *Vedānta-Pārijāta-Saurabha* and *Daśa-Ślokī*. Add:

- `work_id: krishna-stava-raja` — *Kṛṣṇa-Stava-Rāja* — `traditionally-ascribed`. `genre: stotra`.
- `work_id: mantra-rahasya-shodashi` — *Mantra-Rahasya-Ṣoḍaśī* — `traditionally-ascribed`. `genre: rahasya`.

### B.6 `vallabha` — confirm `Ṣoḍaśa-Granthāḥ` are properly enumerated

CORPUS_PLAN names *Aṇu-Bhāṣya*, *Tattvārtha-Dīpa-Nibandha*, *Subodhinī*, *Ṣoḍaśa-Granthāḥ*. The "Sixteen Treatises" should ideally be enumerated as 16 separate work_ids (or one bundle with 16 sub-loci). Recommended individual entries: *Yamunāṣṭakam*, *Bāla-Bodha*, *Siddhānta-Muktāvalī*, *Puṣṭi-Pravāha-Maryādā*, *Siddhānta-Rahasya*, *Navaratnam*, *Antaḥkaraṇa-Prabodha*, *Vivekadhairyāśraya*, *Kṛṣṇāśraya*, *Catuḥ-Ślokī*, *Bhakti-Vardhinī*, *Jala-bheda*, *Pañcapadyāni*, *Saṃnyāsa-Nirṇaya*, *Nirodha-Lakṣaṇa*, *Sevā-Phala*. **Action: bundle as one work-entry with sub-loci, given the schema's `engaged_works[]` flexibility — full enumeration would balloon the entry.**

### B.7 `vidyaranya` — add *Anubhūti-Prakāśa* and *Vivaraṇa-Prameya-Saṃgraha-Vyākhyā*

CORPUS_PLAN names *Pañcadaśī*, *Jīvanmukti-Viveka*, *Vivaraṇa-Prameya-Saṃgraha*, *Sarva-Darśana-Saṃgraha*. Add:

- `work_id: anubhuti-prakasha` — *Anubhūti-Prakāśa* (verse-summaries of each of the major Upaniṣads from Advaita standpoint) — `securely-authored` (or `traditionally-ascribed` if disputed).

### B.8 `madhusudana` — add *Vedānta-Kalpa-Latikā* and *Prasthāna-Bheda*

CORPUS_PLAN names *Advaita-Siddhi*, *Siddhānta-Bindu*, *Bhakti-Rasāyana*, *Gūḍhārtha-Dīpikā*. Add:

- `work_id: vedanta-kalpa-latika` — *Vedānta-Kalpa-Latikā* — `securely-authored`.
- `work_id: prasthana-bheda` — *Prasthāna-Bheda* (taxonomy of philosophical schools) — `securely-authored`.
- `work_id: sankshepa-shariraka-sara-samgraha` — `securely-authored`. Sub-commentary tradition-piece.

### B.9 `appayya` — add *Naya-Mañjarī* and *Catur-Mata-Sāra-Saṃgraha*

CORPUS_PLAN names *Siddhānta-Leśa-Saṃgraha*, *Parimala*, *Śivārka-Maṇi-Dīpikā*. Add:

- `work_id: naya-manjari` — *Naya-Mañjarī* (or its sub-section *Vedānta-Kalpa-Taru-Parimala*).
- `work_id: catur-mata-sara-samgraha` — *Catur-Mata-Sāra-Saṃgraha* (compendium of the four Vaiṣṇava-Vedānta systems) — `securely-authored`. (Especially valuable for the comparative-claims engine.)

### B.10 `vedanta-desika` — confirm `Sarvārtha-Siddhi` is treated as separate from `Tattva-Muktā-Kalāpa`

CORPUS_PLAN bundles them as "*Tattva-Muktā-Kalāpa* with *Sarvārtha-Siddhi*". For the comparative-claims engine this should be split: the *Kalāpa* is verse-doctrine, the *Sarvārtha-Siddhi* is Deśika's own auto-commentary. Splitting lets later subcommentaries (Uttamūr's *Sarvārtha-Siddhi-Vyākhyā*, etc.) cite the right work_id. **Action: split into two work-entries.**

### B.11 `vyasatirtha` — add *Tātparya-Candrikā* sub-pieces

CORPUS_PLAN already lists *Nyāyāmṛta*, *Tarka-Tāṇḍava*, *Tātparya-Candrikā*. Add:

- `work_id: bhedojjivana` — *Bhedojjīvana* (defense of *bheda* against Advaita's *abheda-śruti* readings) — `securely-authored`. Important for the Advaita-Dvaita ontology comparative claims.

### B.12 `bhaskara`, `nimbarka`, `bodhayana`, `yadava-prakasa`, etc. (reconstruction-only entries)

For all reconstruction-only entries (Bhartṛprapañca, Auḍulomi, Āśmarathya, Kāśakṛtsna, Brahmadatta, Bodhāyana, Upavarṣa, Sundara-Pāṇḍya, Yādava-Prakāśa), the `engaged_works[]` should explicitly list the *cited-fragment-source* as a `work_id` whose `ascription_tier: disputed` and whose `summary` notes the reconstruction is from passages cited in NamedAuthor-X. This is partially done already but should be audited for consistency. **Action: audit; uniformise the reconstruction-fragment treatment.**

### B.13 `manavala-mamunigal` — add *Yatīndra-Pravaṇa-Prabhāva* commentary-suite individually

CORPUS_PLAN bundles. For pedagogical clarity recommend separate entries for: *Mumukṣuppaḍi-Vyākhyāna*, *Tattva-Trayam-Vyākhyāna*, *Śrī-Vacana-Bhūṣaṇa-Vyākhyāna*. Each is a `tika` on a different Pillai Lokācārya *rahasya*.

---

## Section B summary

| existing thinker | action | priority |
|---|---|---|
| `caitanya` | +2 work entries (Rāmānanda-Saṃvāda; Daśa-Mūla-Śikṣā) | high |
| `madhva` | +4 to +6 work entries (Ṛg-bhāṣya, individual Upaniṣad-bhāṣyas, Daśa-Prakaraṇa) | high |
| `vidyaranya` | +1 (Anubhūti-Prakāśa) | medium |
| `madhusudana` | +2 (Vedānta-Kalpa-Latikā; Prasthāna-Bheda) | medium |
| `appayya` | +1 to +2 (Catur-Mata-Sāra-Saṃgraha esp.) | medium |
| `vedanta-desika` | split *Tattva-Muktā-Kalāpa* / *Sarvārtha-Siddhi* | high (load-bearing for comparative claims) |
| `vyasatirtha` | +1 (Bhedojjīvana) | medium |
| `nimbarka` | +1 to +2 stotra/rahasya entries | low |
| `vallabha` | bundle Ṣoḍaśa-Granthāḥ as sub-loci | medium |
| `manavala-mamunigal` | split bundled commentaries | medium |
| `sankara` | spot-audit: ensure school-ascribed stotra-corpus is per-work, not bundled | high |
| reconstruction-only entries (8) | audit for uniform fragment-source treatment | medium |

---

## Footnoted research sources (web, 2026-05-09)

1. *Sri Aurobindo* — Wikipedia; Sri Aurobindo Ashram CWSA listings (motherandsriaurobindo.in, sriaurobindoashram.org); "Modern Relevance of Aurobindo's Vedanta" (philosophy.institute); Vedantic Basis and Praxis of the Integral Advaita of Sri Aurobindo (LMU Digital Commons); Aurobindo and Indian Philosophy (satyameva.in). For school-name identification: "Aurobindo's Integral Advaita: Unity in Diversity" (philosophy.institute), corroborating that *Pūrṇa-Advaita* and *Integral Advaita* are used interchangeably; "Cutting the Knot of the World Problem" (MDPI Religions 12/9/765).
2. *Rāmabhadrācārya* — Wikipedia ("Rambhadracharya"); Tulsi Peeth publication records; tfipost.com biographical piece. Confirmed: blind from age two months, Rāmānanda-Sampradāya (Viśiṣṭādvaita), *Śrīrāghavakṛpā-Bhāṣyam* on full prasthāna-trayī released by PM Vajpayee 10 April 1998.
3. *Uttamūr Vīrarāghavācārya* — uttamurswami.org/wordpress/home/introduction/; abhinavadesika.wordpress.com/intro/; ramanuja.org/sri/BhaktiListArchives ("SrI UttamUr SwAmi - A Life Sketch"); elisafreschi.com 2018-02-09 piece. Note: blindness *not* attested by any source; not the user's blind ācārya.
4. *Raṅgarāmānuja Muni* — vishnudut1926.blogspot.com 2018-12 piece; Internet Archive: "Principal Upanishads According to Sri RangaRamanuja Muni Vol 1-3 Dr N S Anantha Rangacharya"; Hindu Blog short biography 2023-01.
5. *Anantakrishna Sastri* — hindu-blog.com 2023-03 piece; Internet Archive editions of *Vedānta-Paribhāṣā*, *Śatabhūṣaṇī*, *Advaita-Tattva-Sudhā*; PhilPapers entry. Birth year 1886 (per Hindu Blog), not 1879 as user-tentative.
6. *Satchidānandendra Sarasvatī* — Wikipedia; Springer *Journal of Indian Philosophy* article on the Mūlāvidyā controversy (Sk Arun Murthi); advaita-vision.org tag-page; adhyatmaprakasha.org publications. Dates 1880–1975 confirmed.
7. *Bannañje Govindācārya* — Wikipedia; Daijiworld.com obituary 2020-12; Star of Mysore obituary; Internet Archive: *Mahabharatha Tatparya Nirnaya Vol 1*. Dates 1936–2020 confirmed; ~150 books / ~4000 pages Sanskrit *vyākhyāna* attested.
8. *Bhaktisiddhānta Sarasvatī* — Wikipedia; *Bhaktisiddhanta Sarasvati bibliography* (Wikipedia separate entry); Gaudiya Math Wikipedia; ISKCON Delhi biographical page; dandavats.com on UNESCO recognition. Dates 1874–1937 confirmed.
9. *Swāmī Karpātrī* — Wikipedia; postagestamps.gov.in/Pdf/KM_BROCHURE.pdf (Govt of India commemorative stamp); hindupad.com; eternalbhaarat.quora.com.
10. *Candraśekhara Bhāratī III* — Wikipedia; sringeri.net/jagadgurus/sri-chandrashekhara-bharati-mahaswamiji/biography; en-academic.com.
11. *Anandagiri / Govindānanda* — advaita-vedanta.org bibliography; Internet Archive Brahmasūtra-Bhāṣya editions. (Background research; not added to corpus this round.)

---

## Notes for the Wave-0 follow-up that lifts this into JSON

1. `lineage_in` / `lineage_out` integrity: when these new entries are added, edit the *receiving* thinker's `lineage_out` accordingly (e.g., `bhaktivinoda.json` must add `bhaktisiddhanta` to its `lineage_out`). CI will fail otherwise.
2. `sub_schools.json` registry needs new keys: `purna-advaita-integral`, `ramananda-sampradaya`, `vadakalai-modern-systematic`, `vadakalai-upanishad-bhashya`, `vivarana-modern-editorial`, `shuddha-shankara-prakriya`, `tattvavada-modern`, `gaudiya-matha`, `dashanami-sarasvati-revivalism`, `shringeri-patta`. Each needs a 1–2 sentence description and the `parent_school_color_token` plus `shade`.
3. `schools.json` is **not** modified for v2 (no new top-level school tokens — see Aurobindo recommendation).
4. The `dates_high` field for the living jagadguru `rambhadracharya` requires a schema decision: either (a) extend the schema to allow `null`/`undefined` for `dates_high` (with a `is_living: true` boolean), or (b) use the current year and document in `dates_notes`. Recommendation: option (a), schema bump worth the clarity. If avoiding schema bump, use option (b) with explicit `dates_notes`.
5. `engaged_works[].key_passage_ids` should be `[]` for all new entries at insertion; Wave-2 (Codex 5.4) populates passages.
6. `entry_status` for all new entries: `draft` at insertion; lift to `reviewed` after Wave-1 fills the `core_thesis` and `summary` fields and an Opus auditor confirms.
7. `core_thesis` drafts above are sized 150–170 words to comply with the schema's 100–200 word constraint (CI rule §6.9).
