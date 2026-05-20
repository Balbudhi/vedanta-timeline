# Source-Integrity Audit v1

**Scope.** Every file under `materials/primary_texts/sanskrit/` was probed for OCR / extraction quality. Each citation in the thinker JSONs and the extended translations was traced to a backing file and re-checked. Replacements for the worst-degraded sources have been acquired into `materials/primary_texts/sanskrit/_replaced/`; originals are preserved on disk for record.

The user's standard is the right one: a citation that cannot be defended at the level of the cited text is not a citation. Where an underlying source turned out to be unreadable, the responsible operation is either (a) replace it with a defensible edition, or (b) demote the claim from primary-text-attested to secondary-attested, with the secondary scholar named.

Heuristic detail: see `_audit_scripts/quality_probe.py`. The classification distinguishes:

- **CLEAN** — GRETIL plain-text, born-digital, or e-text with reliable IAST / Devanāgarī density.
- **ACCEPTABLE** — usable but with minor OCR artifacts; cite cautiously and verify any string before quoting.
- **DEGRADED** — extensive OCR errors or wrong-script preface; should be replaced if a better edition is findable.
- **IMAGE-ONLY** — no extractable text under a `pypdf` probe of multiple pages; the file is functionally a page-image PDF.

Heuristic limitations: (a) the IAST punctuation `||` and `/` trips the junk-token rule on a handful of clean GRETIL-style files in `comparator/` and `buddhist/`; those have been re-classified manually as CLEAN below. (b) the heuristic does not detect mixed-language files (e.g. Bengali script masquerading as Sanskrit) — one such case (`_more/CCBSSTMadhya.txt`, Bengali Caitanya-caritāmṛta) is flagged manually. (c) some "CLEAN non-GRETIL" txt files are degraded in their interior even when their first 8 KB scores well; flagged in the table.

---

## Summary counts

| Classification | TXT/HTM | PDF | Total |
|---|---:|---:|---:|
| CLEAN (incl. GRETIL plain-text, born-digital scholarly PDFs) | 124 (heuristic) + 6 (manual upgrades from DEGRADED) = 130 | 7 | **137** |
| ACCEPTABLE | 3 | 2 | **5** |
| DEGRADED | 3 (after manual upgrades) | 4 | **7** |
| IMAGE-ONLY | 0 | 41 | **41** |
| META / OTHER (epub, json, tsv) | 4 | — | 4 |
| **TOTAL audited** | | | **194 corpus files + 4 metadata** |

Replacements acquired: **42 files** in `_replaced/` (26 GRETIL plain-text e-texts; 16 archive.org djvu OCR layers, 9 of them genuinely informative on the Sanskrit body, 7 marginal — see notes per file).

---

## Citation impact (highest priority)

Cross-referencing every primary-text path mentioned in `site/data/thinkers/*.json` and `site/data/full_translations/*.md` against the classification table produced this set of *false-grounded citations*: passages whose `source_edition` field claims transcription from a file that has zero or near-zero extractable text.

| Thinker | Cited file | Status | Action |
|---|---|---|---|
| sarvajnatman | `vedanta/full_corpus/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive.pdf` | IMAGE-ONLY | Replacement djvu txt acquired (`_replaced/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt`); the OCR layer is heavily English-thesis, the Sanskrit IAST in body is severely garbled. **The four `key_passages` for Sarvajñātman cannot be re-verified from the on-disk source.** Recommend: demote each to a secondary-attested claim citing Veezhinathan 1972 with locus-only, OR re-extract from the Devanāgarī Vajhe edition (Bibliophile Impex Anandāśrama Series; not on archive.org as searchable text — only Vajhe 1924 PDF, also IMAGE-ONLY at archive). 4 passages affected. |
| vimuktatman | `vedanta/full_corpus/vimuktatman_ista_siddhi_1933_archive.pdf` | IMAGE-ONLY | Replacement djvu txt acquired (`_replaced/vimuktatman_ista_siddhi_hiriyanna_1933_archive_djvu.txt`). OCR contains substantial Devanāgarī body (≈20 K Devanāgarī lines). The five `key_passages` for Vimuktātman should be re-verified verse-by-verse against this file before any user-facing publication. 5 passages affected. |
| jayatirtha (full_translations) | `vedanta/full_corpus/madhva_brahma_sutra_bhasya_vol1_archive.pdf` | IMAGE-ONLY | Replacement acquired: `_replaced/madhva_brahma_sutra_bhasya_3comm_vol1_archive_djvu.txt` (Madhva BSB with three commentaries — Tattva-Prakāśikā by Jayatīrtha is one of them; Devanāgarī body recovered). |
| ramanuja (full_translations:shri-bhasya) | `_more/SribhasyaOfRamanujaPart1Chatuhsutri1959R.D.Karmakar.txt` | DEGRADED | GRETIL `sa_rAmAnuja-zrIbhASya-1.txt` is listed in the GRETIL index but the server returns 404 for that specific file (broken link). GRETIL `sa_rAmAnuja-vedArthasaMgraha.txt` (CLEAN) and `sa_rAmAnuja-bhagavadgItAbhASya.txt` (CLEAN) are usable for adjacent Rāmānuja extraction. For the Śrī-Bhāṣya proper: the Karmakar 1959 OCR is the best on-disk witness; flag the full_translations file with a source-quality warning and accept that any Sanskrit-IAST verbatim quotation must be verified against another edition. |
| bhaskara (full_translations) | references `vedanta/brahma_sutra.txt` and `vedanta/full_corpus/corpus_meta.tsv` | CLEAN / META | OK; the Bhaskara translation rests on Bhāskara's Brahmasūtra-Bhāṣya being summarised against the Brahma-Sūtra base text (`brahma_sutra.txt`, CLEAN). Bhāskara's `bhAskara-bhagavadAzayAnusaraNabhAsya.txt` is on GRETIL but was not acquired in this pass — recommend acquisition for any future Bhaskara extraction. |
| sureshvara (full_translations:brhadaranyaka-varttika) | references `vedanta/full_corpus/` directory | UNKNOWN | The cited file does not exist on disk — only the English archive PDF (`suresvara_brhadaranyaka_varttika_english_archive.pdf`, DEGRADED, 4 sample pages 100 words) is present. Sureśvara's Bṛhadāraṇyaka-Vārttika Sanskrit is not on GRETIL; the Mahadeva Sastri 1894 / Subrahmanya Sastri editions exist on archive.org as image-only PDFs. Recommend: demote the Sureśvara Bṛhadāraṇyaka-Vārttika translation to secondary-attested (Hino, "Suresvara's Vartika on Yajnavalkya-Maitreyi Dialogue" 1982, plus the partial Mahadeva Sastri English) until a clean Devanāgarī text is acquired. |

**Total cited files at risk: 4 directly (Sarvajñātman PDF, Vimuktātman PDF, Madhva BSB vol1 PDF, Karmakar Śrī-Bhāṣya OCR). Total `key_passages` whose primary-source attestation is unsafe: 9. Total `full_translations` files whose footer needs a source-quality flag: 4.**

---

## Replacements acquired

All replacements are in `materials/primary_texts/sanskrit/_replaced/` to preserve the originals on disk as a record. Verification status is "Devanāgarī body present" if the file contains ≥5 K Devanāgarī characters; "IAST body present" if the file is a romanised critical edition; "OCR-degraded marginal" if the OCR layer was largely English preface plus garbled Sanskrit.

### From GRETIL (plain-text e-texts, transcribed from named critical editions)

| File | Original critical edition | Status |
|---|---|---|
| `gretil_sa_mAdhva-anuvyAkhyAna.txt` | Sansknet Project transcription | CLEAN — duplicate of existing `vedanta/full_corpus/madhva_anuvyakhyana_gretil.txt`; kept for redundancy |
| `gretil_sa_mAdhva-mahAbhAratatAtparyanirNaya.txt` | Sansknet | CLEAN |
| `gretil_sa_mAdhva-kRSNAmRtamahArNava.txt` | Sansknet | CLEAN — superior to existing `vedanta/madhva_krsnamrta.txt` (which appears to be a separate older transcription) |
| `gretil_sa_jayatIrtha-nyAyasudhA.txt` | Sansknet | CLEAN — duplicate of existing `vedanta/jayatirtha_nyaya_sudha.txt`; kept |
| `gretil_sa_madhusUdanasarasvatI-siddhAntabindu.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_mandanamizra-brahmasiddhi.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_maNDanamizra-vibhramaviveka.txt` | GRETIL | **NEW** — Maṇḍana's Vibhrama-Viveka not previously on disk |
| `gretil_sa_zaMkara-upadezasAhasrI.txt` | Mayeda 1973/2006 transcription by I. Andrijanić, 2020 | CLEAN — duplicate of existing |
| `gretil_sa_zaMkara-vivekacuDAmaNi.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-Atmasiddhi.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-Izvarasiddhi.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-saMvitsiddhi.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-stotraratna.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-catuHzlokI.txt` | Sansknet | CLEAN — duplicate of existing |
| `gretil_sa_yAmuna-gItArthasaMgraha.txt` | Sansknet | **NEW** — Yāmuna's Gītārtha-Saṃgraha not previously on disk |
| `gretil_sa_rAmAnuja-vedArthasaMgraha.txt` | Sadanori Ishitobi transcription | CLEAN — supersedes `vedanta/ramanuja_vedartha_sangraha.txt` quality-wise |
| `gretil_sa_rAmAnuja-bhagavadgItAbhASya.txt` | GRETIL | CLEAN — supersedes `vedanta/ramanuja_gita_bhasya.txt` |
| `gretil_sa_jiva-gosvami-satsamdarbha.txt` | GRETIL | CLEAN — duplicate of existing `caitanya_gaudiya/jiva_sat_sandarbha.txt` |
| `gretil_sa_jIvagosvAmin-saMkalpakalpadruma.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_jIvagosvAmin-rAdhAkRSNArcanadIpikA.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_jIvagosvAmin-gopAlacampUp1-33u1-3u5-6u29.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_prabodhAnandasarasvatI-caitanyacandrAmRta.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_vyAsatIrtha-tarkatANDava-comm.txt` | GRETIL | CLEAN — duplicate of existing |
| `gretil_sa_vAcaspatimizra-bhAmati.txt` | GRETIL | CLEAN — supersedes `vedanta/vacaspati_bhamati.txt` (also CLEAN, but the GRETIL header documents the source edition explicitly) |
| `gretil_sa_gauDapAda-AgamazAstra.txt` | GRETIL | CLEAN — alternative to existing `vedanta/full_corpus/gaudapada_mandukya_karika_gretil.txt` |
| `gretil_sa_srinivasamakhi-vedantadesika-dazavidhAhetunirUpaNa.txt` | GRETIL | **NEW** — auxiliary Vedānta-Deśika text |

### From archive.org djvu OCR layers (variable quality)

| File | Underlying scholarly edition | Devanāgarī content | Verdict |
|---|---|---|---|
| `vimuktatman_ista_siddhi_hiriyanna_1933_archive_djvu.txt` | Hiriyanna 1933, Gaekwad's Oriental Series 65, Baroda Oriental Institute | YES (≈6 450 dev-line markers, ≈20 K dev-chars) | **USABLE** as Devanāgarī base; OCR has some preface noise but the verse body is recoverable. Replaces IMAGE-ONLY `vimuktatman_ista_siddhi_1933_archive.pdf`. |
| `sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt` | Veezhinathan 1972, University of Madras | NO — this is the English thesis with embedded transliterated Sanskrit (heavily OCR-corrupted) | **MARGINAL.** Recommend secondary-attribution for Sarvajñātman key passages; for a clean Devanāgarī base, the Vajhe / Bhau Sastri 1924 Anandāśrama edition is the reference but is not searchable online. |
| `padmapada_pancapadika_dli_archive_djvu.txt` | Vizianagaram Sanskrit Series, ed. Ram Shastri Bhagavatacharya | NO Devanāgarī recovered by OCR | **MARGINAL.** Same situation as Sarvajñātman; secondary-attest pending Devanāgarī acquisition. |
| `prakasatman_pancapadika_vivarana_archive_djvu.txt` | Sadhana Grantha Mandali Tenali ed. | NO Devanāgarī recovered | **MARGINAL.** |
| `suresvara_naiskarmya_siddhi_alston_archive_djvu.txt` | Alston, *The Realization of the Absolute* (Shanti Sadan, London, 1959, 2nd ed. 1971) | IAST Sanskrit + English (no Devanāgarī, but romanised Sanskrit is reliably extractable) | **USABLE** for IAST-base extraction; replaces IMAGE-ONLY `suresvara_naiskarmya_siddhi_alston_1959_archive.pdf`. |
| `vidyaranya_panchadasi_archive_djvu.txt` | M. Srinivasa Rau & K. A. Krishnaswamy Aiyar, English translation edition | NO Devanāgarī recovered by OCR; English translation usable | **MARGINAL** for Sanskrit; usable for English-paraphrase. |
| `vidyaranya_panchadashi_sanskritdocuments.pdf` | sanskritdocuments.org ITRANS-derived Devanāgarī, 120 pp | YES — clean Devanāgarī verse text | **USABLE** as primary Devanāgarī base for Pañcadaśī. Recommended replacement for `vidyaranya_panchadasi_sanskrit_modaka_tika_archive.pdf` (IMAGE-ONLY). |
| `suresvara_naishkarmyasiddhi_sanskritdocuments.pdf` | sanskritdocuments.org Devanāgarī, 66 pp | YES — clean Devanāgarī | **USABLE** as primary Devanāgarī base for Naiṣkarmya-Siddhi. Together with the Alston IAST/English file, gives full coverage. |
| `vidyaranya_jivanmukti_viveka_archive_djvu.txt` | Madhava (sic, ed.) translation w/ Sanskrit | NO Devanāgarī recovered by OCR | **MARGINAL.** |
| `vedanta_desika_tattva_mukta_kalapa_archive_djvu.txt` | Rama Misra Sastri ed., Varanasi 1900 (3 commentaries) | NO Devanāgarī (OCR fails) | **MARGINAL.** |
| `vyasatirtha_nyayamrta_advaitasiddhi_calcutta_djvu.txt` | Anantakrishna Sastri ed., Calcutta Sanskrit Series | NO Devanāgarī recovered by OCR | **MARGINAL** for Sanskrit; usable for editor's English notes. |
| `madhusudana_advaita_siddhi_anantakrishna_archive_djvu.txt` | Anantakrishna Sastri ed., Nirnaya Sagar Press 1937, with Gauḍa-Brahmānandī, Vitthaleśopadhyāya, Siddhi-Vyākhyā of Balabhadra and Caturgranthi | YES (≈10 K dev-line markers, ≈42 K total dev-chars) | **USABLE** Devanāgarī base; replaces IMAGE-ONLY `madhusudana_advaita_siddhi_vol1_part1_1917_archive.pdf`. |
| `madhva_brahma_sutra_bhasya_3comm_vol1_archive_djvu.txt` | Madhva BSB w/ Tattva-Prakāśikā (Jayatīrtha), Tātparya-Candrikā (Vyāsatīrtha), Pariṃala (Rāghavendra) | YES (≈10 K dev-line markers) | **USABLE.** Replaces IMAGE-ONLY `madhva_brahma_sutra_bhasya_vol1_archive.pdf` and partly the vol2/vol3 PDFs. |
| `madhva_brahma_sutra_bhasya_3comm_vol2_archive_djvu.txt` | same edition vol 2 | YES | **USABLE.** |
| `madhva_brahma_sutra_bhasya_3comm_vol3_archive_djvu.txt` | same edition vol 3 | YES (≈16 K dev-line markers, the densest) | **USABLE.** |
| `madhva_brahma_sutra_bhasya_with_tatvadipika_dli_archive_djvu.txt` | Madhva BSB w/ Tatva-Dīpikā of Trivikrama-Paṇḍita, ed. G. Raghavendracharya | YES (≈14 K dev-line markers) | **USABLE.** |

---

## Per-file classification (full table)

The table is large; the canonical machine-readable form is `_audit_data/quality_audit_v2.tsv`. Manual upgrades and downgrades against the heuristic are noted below.

### Manual upgrades (heuristic flagged DEGRADED but the file is in fact CLEAN)

These are GRETIL-style or born-digital IAST e-texts that the heuristic mis-classified because of high `||` and `/` punctuation density:

- `comparator/patanjali_yoga_sutra.txt` → CLEAN (Pātañjalayogasūtra; IAST verses)
- `comparator/vyasa_yoga_bhasya.txt` → CLEAN
- `comparator/vatsyayana_nyaya_bhasya.txt` → CLEAN (Nyāya-Bhāṣya, IAST critical text)
- `buddhist/vasubandhu_vimsatika.txt` → CLEAN (Viṃśatikā, IAST)
- `buddhist/candrakirti_madhyamakavatara.txt` → CLEAN (Madhyamakāvatāra, IAST)
- `buddhist/nagarjuna_vigraha_vyavartani.txt` → CLEAN (heuristic gave ACCEPTABLE; the file is GRETIL-class IAST)

### Manual downgrades (heuristic flagged CLEAN but content is degraded)

- `_more/SriBhasyaHindi01.txt` → DEGRADED (only the first 8 KB and the midpoint were sampled; the body is heavy OCR garbage with broken Devanāgarī fragments mixed with random Latin OCR substitutions)
- `_more/SriBhasyaHindi02.txt` → ACCEPTABLE (similar to vol 1 but with more recoverable Devanāgarī; usable for Hindi-Sanskrit Śrī-Bhāṣya translation but cite cautiously)
- `_more/ShriMadhvaVedanta.txt` → ACCEPTABLE (Pūrṇaprajña-Bhāṣya in Hindi-Sanskrit; OCR damage in headers, body recoverable)
- `_more/srimad-bhagavat-mahapuran-2-volume-set-sanskrit-hindi.txt` → ACCEPTABLE (Bhāgavata-Purāṇa Hindi-Sanskrit; similar profile)
- `_more/kcc_murarigupta.txt` → ACCEPTABLE (Murāri Gupta's *Kṛṣṇa-Caitanya-Caritra*; Devanāgarī recoverable)
- `_more/CCBSSTMadhya.txt` → IRREDEEMABLE-AS-SANSKRIT (this is the *Caitanya-Caritāmṛta* in Bengali script; the file is not corrupt but is wrong-script for any project that wants Sanskrit verse-attestation)
- `_kashmir_saivism/philosophy-of-madhvacarya-bnk-acrobat-ocr.txt` → ACCEPTABLE (B.N.K. Sharma 1962 *Philosophy of Sri Madhvacharya*, Acrobat OCR; usable as a secondary-source reference for Madhva but with periodic single-letter substitution errors and missing diacritics; CITE-FROM-PRINT, not from this file, for any verbatim Sharma quotation)
- `_kashmir_saivism/AdvaitasiddhiVsNyayamrta.txt` → ACCEPTABLE (B.N.K. Sharma 1994 *Advaita-Siddhi vs Nyayamṛta*; same profile)

### Heuristic-DEGRADED, confirmed DEGRADED

- `_more/SribhasyaOfRamanujaPart1Chatuhsutri1959R.D.Karmakar.txt` (Karmakar 1959; OCR fragmented, mixed Devanāgarī fragments with corrupted Latin runs)
- `sankhya_metaphysics/wezler_motegi_yuktidipika_vol1_1998.txt` (Wezler-Motegi 1998 Yukti-Dīpikā vol 1; OCR is severely damaged. The companion `wezler_motegi_yuktidipika_vol1_1998.pdf` is **CLEAN** by heuristic — the PDF retains the embedded text layer; the .txt extraction is what's broken. **Recommend re-extracting from the PDF.**)
- `vedanta/full_corpus/madhusudana_bhakti_rasayana_archive.pdf` (heuristic-DEGRADED PDF)
- `vedanta/full_corpus/padmapada_pancapadika_venkataramiah_1948_archive.pdf` (heuristic-DEGRADED PDF; the Venkataramiah English translation; supplemented now by the Vizianagaram djvu txt — both marginal)
- `vedanta/full_corpus/shankara_upadesa_sahasri_mayeda_1992_archive.pdf` (heuristic-DEGRADED PDF; the GRETIL e-text `shankara_upadesa_sahasri_gretil.txt` IS the same Mayeda edition transcribed cleanly, so this PDF is already redundant)
- `vedanta/full_corpus/suresvara_brhadaranyaka_varttika_english_archive.pdf` (heuristic-DEGRADED, very large 789 MB PDF; OCR text is sparse — likely a multi-volume scanned set with poor extraction)

### IMAGE-ONLY (full list — 41 files)

These are page-image PDFs with no usable embedded text layer. None should be cited as a primary-source extraction without prior OCR or replacement-acquisition.

```
_more/Olivelle_Early_Upanishads_bdaa8703.pdf                                                  (read failed: stream ended unexpectedly)
kala_cakra/banerjee_1985_kalacakratantra_critical.pdf
kala_cakra/carelli_1941_sekoddesatika_naropa.pdf
kala_cakra/upadhyaya_vimalaprabha_vol2.pdf
kala_cakra/vira_lokesh_chandra_1966_kalacakra_other_texts.pdf
vedanta/full_corpus/bhartrprapanca_hiriyanna_indian_antiquary_vol53_1924_archive.pdf
vedanta/full_corpus/gaudapada_mandukya_karika_shankara_bhasya_nikhilananda_archive.pdf
vedanta/full_corpus/madhusudana_advaita_siddhi_vol1_part1_1917_archive.pdf                    (REPLACED by _replaced/madhusudana_advaita_siddhi_anantakrishna_archive_djvu.txt)
vedanta/full_corpus/madhva_bhagavata_tatparya_nirnaya_archive.pdf
vedanta/full_corpus/madhva_brahma_sutra_bhasya_vol1_archive.pdf                                (REPLACED by _replaced/madhva_brahma_sutra_bhasya_3comm_vol1_archive_djvu.txt)
vedanta/full_corpus/madhva_brahma_sutra_bhasya_vol2_archive.pdf                                (REPLACED by _replaced/madhva_brahma_sutra_bhasya_3comm_vol2_archive_djvu.txt)
vedanta/full_corpus/madhva_brahma_sutra_bhasya_vol3_archive.pdf                                (REPLACED by _replaced/madhva_brahma_sutra_bhasya_3comm_vol3_archive_djvu.txt)
vedanta/full_corpus/madhva_short_polemics_upadhi_mayavada_mithyatva_tattva_archive.pdf
vedanta/full_corpus/mandana_misra_brahma_siddhi_kuppuswami_sastri_1937_archive.pdf             (already-CLEAN GRETIL txt exists for the Brahma-Siddhi: mandana_misra_brahma_siddhi_gretil.txt; PDF is now redundant)
vedanta/full_corpus/nimbarka_dasasloki_archive.pdf
vedanta/full_corpus/nimbarka_srinivasa_vedanta_parijata_kaustubha_vol1_archive.pdf
vedanta/full_corpus/nimbarka_srinivasa_vedanta_parijata_kaustubha_vol2_archive.pdf
vedanta/full_corpus/nimbarka_srinivasa_vedanta_parijata_kaustubha_vol3_archive.pdf
vedanta/full_corpus/prakasatman_pancapadika_vivarana_archive.pdf                               (REPLACED — marginal — by _replaced/prakasatman_pancapadika_vivarana_archive_djvu.txt)
vedanta/full_corpus/raghavendra_nyaya_sudha_parimala_ad1_archive.pdf
vedanta/full_corpus/raghavendra_nyaya_sudha_parimala_ad2_archive.pdf
vedanta/full_corpus/raghavendra_nyaya_sudha_parimala_ad3_archive.pdf
vedanta/full_corpus/raghavendra_nyaya_sudha_parimala_ad4_archive.pdf
vedanta/full_corpus/raghavendra_tantra_dipika_archive.pdf
vedanta/full_corpus/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive.pdf               (REPLACED — marginal — by _replaced/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt)
vedanta/full_corpus/shankara_aparokshanubhuti_munilal_archive.pdf
vedanta/full_corpus/shankara_aparokshanubhuti_sanskrit_1940_archive.pdf
vedanta/full_corpus/shankara_atmabodha_kailash_ashram_archive.pdf
vedanta/full_corpus/shankara_vivekacudamani_madhavananda_1970_archive.pdf                      (already-CLEAN GRETIL txt exists: shankara_vivekacudamani_gretil.txt)
vedanta/full_corpus/suresvara_naiskarmya_siddhi_alston_1959_archive.pdf                        (REPLACED by _replaced/suresvara_naiskarmya_siddhi_alston_archive_djvu.txt)
vedanta/full_corpus/vallabha_anubhasya_1897_archive.pdf
vedanta/full_corpus/vedanta_desika_pancaratra_raksa_1942_archive.pdf
vedanta/full_corpus/vedanta_desika_tattva_mukta_kalapa_sarvartha_siddhi_1900_archive.pdf       (REPLACED — marginal — by _replaced/vedanta_desika_tattva_mukta_kalapa_archive_djvu.txt)
vedanta/full_corpus/vidyaranya_jivanmukti_viveka_sanskrit_archive.pdf                          (REPLACED — marginal — by _replaced/vidyaranya_jivanmukti_viveka_archive_djvu.txt)
vedanta/full_corpus/vidyaranya_jivanmukti_viveka_subrahmanya_sastri_1978_archive.pdf
vedanta/full_corpus/vidyaranya_panchadasi_sanskrit_modaka_tika_archive.pdf                     (REPLACED by _replaced/vidyaranya_panchadashi_sanskritdocuments.pdf)
vedanta/full_corpus/vijnanabhiksu_vijnanamrta_bhasya_1979_archive.pdf
vedanta/full_corpus/vijnanabhiksu_yoga_varttika_1884_archive.pdf
vedanta/full_corpus/vimuktatman_ista_siddhi_1933_archive.pdf                                   (REPLACED by _replaced/vimuktatman_ista_siddhi_hiriyanna_1933_archive_djvu.txt)
vedanta/full_corpus/vyasatirtha_nyayamrta_vol1_archive.pdf                                     (REPLACED — marginal — by _replaced/vyasatirtha_nyayamrta_advaitasiddhi_calcutta_djvu.txt)
vedanta/full_corpus/yamuna_agama_pramanya_archive.pdf
```

---

## Irredeemable

A small number of files cannot be replaced from any open-access source presently identified, and any citation that depends on them must be re-attributed. Acquisition pathways noted where known.

| Source needed | What's on disk | Why irredeemable here | Pathway to genuine acquisition |
|---|---|---|---|
| **Sarvajñātman, Saṃkṣepa-Śārīraka — Devanāgarī** | Veezhinathan 1972 IMAGE-ONLY PDF (English thesis); the djvu OCR is heavily English-thesis garbage | The clean Sanskrit-Devanāgarī edition (Bhau Sastri Vajhe / Anandāśrama Sanskrit Series, 1924) is on archive.org only as page-image scan with no usable OCR layer; no GRETIL or sanskritdocuments edition. | Hand-OCR from the 1924 Anandāśrama scan, OR cite the Vajhe edition at locus-only and quote nothing verbatim |
| **Padmapāda, Pañcapādikā — Devanāgarī** | Venkataramiah PDF (DEGRADED, English translation); DLI Vizianagaram djvu txt (no Devanāgarī) | Same situation as Sarvajñātman | Hand-OCR Vizianagaram series, OR rely on Venkataramiah English translation paraphrase |
| **Prakāśātman, Pañcapādikā-Vivaraṇa — Devanāgarī** | Tenali Sadhana PDF (IMAGE-ONLY); djvu txt (marginal) | Same situation | As above |
| **Sureśvara, Bṛhadāraṇyaka-Vārttika — Sanskrit body** | English partial translation PDF (DEGRADED, very large) | The Mahadeva Sastri 1894 four-volume edition is on archive.org as image-only PDFs; no GRETIL e-text | Hand-OCR Mahadeva Sastri, OR cite via Hino 1982/1991 secondary scholarship for the Yājñavalkya-Maitreyī sections |
| **Bhartṛprapañca — Bṛhadāraṇyaka commentary fragments** | Hiriyanna 1924 *Indian Antiquary* article (IMAGE-ONLY PDF) | The fragments survive only as quotations in Śaṅkara, Sureśvara, and Ānandagiri; Hiriyanna 1924 is the principal collection. The PDF is image-only. | Hand-OCR Hiriyanna 1924, OR cite via Nakamura 1983 *Early Vedānta Philosophy* |
| **Nimbārka, Vedānta-Pārijāta-Saurabha and Śrīnivāsa, V-P-Kaustubha** | Three-volume archive PDFs (all IMAGE-ONLY) | No GRETIL; no sanskritdocuments | Hand-OCR, OR cite via Roma Bose 1940 secondary translation |
| **Vallabha, Aṇu-Bhāṣya** | 1897 archive PDF (IMAGE-ONLY) | No GRETIL Sanskrit e-text | Hand-OCR, OR cite via secondary (Mishra 1950, Marfatia 1967) |
| **Vedānta-Deśika, Tattva-Muktā-Kalāpa with Sarvārtha-Siddhi** | 1900 PDF (IMAGE-ONLY); djvu txt (marginal, no Devanāgarī recovered) | Rama Misra Sastri 1900 OCR fails on Devanāgarī | Hand-OCR, OR cite via S.M. Srinivasa Chari 2004 secondary |
| **Raghavendra, Nyāya-Sudhā-Parimala (4 vols)** | All four volume PDFs IMAGE-ONLY (the full set is ~1.1 GB on disk) | No e-text known | Hand-OCR, OR cite via secondary (B.N.K. Sharma 1981 *History of the Dvaita School of Vedānta*) |
| **Vijñānabhikṣu, Vijñānāmṛta-Bhāṣya / Yoga-Vārttika** | Both archive PDFs IMAGE-ONLY | No GRETIL Sanskrit e-text | Hand-OCR, OR cite via Larson-Bhattacharya 2008 *Encyclopedia of Indian Philosophies* vol 12 |

---

## Citations flagged for demotion or re-attribution

### Demote to secondary-attested (no clean primary on disk)

| Thinker JSON | Passage / claim | Recommended action |
|---|---|---|
| `sarvajnatman.json` → `samksepa-sariraka-1-319__partless-consciousness-alone-bears-avidya` | Sanskrit IAST and English-close cite Veezhinathan 1972 PDF (IMAGE-ONLY) | Re-source from `_replaced/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt` (verify each verse against Devanāgarī Vajhe edition before publication) OR demote to "secondary-attested via Veezhinathan 1972 thesis" with no verbatim quotation |
| `sarvajnatman.json` → `samksepa-sariraka-1-327__reflected-consciousness-and-agency` | same | same |
| `sarvajnatman.json` → `samksepa-sariraka-3-275-276__fourfold-analysis-of-tat-and-tvam` | same | same |
| `sarvajnatman.json` → `samksepa-sariraka-3-278__tvam-term-and-jiva-as-reflection` | same | same |
| `vimuktatman.json` → `is-1-1__vedanta-brahma-visaya` | Sanskrit IAST cites IMAGE-ONLY Hiriyanna 1933 PDF | Re-source from `_replaced/vimuktatman_ista_siddhi_hiriyanna_1933_archive_djvu.txt` (Devanāgarī body present; verse-by-verse verification required) |
| `vimuktatman.json` → `is-1-1__maya-anirvacaniya-avidya` | same | same |
| `vimuktatman.json` → `is-1-9__bhranti-anirvacaniyata` | same | same |
| `vimuktatman.json` → `is-1-140__atmany-eva-avidya` | same | same |
| `vimuktatman.json` → `is-1-9__jnanodaya-jivanmukti` | same | same |
| `full_translations/jayatirtha__tattva-prakashika.md` | references IMAGE-ONLY Madhva BSB vol1 PDF | Re-source from `_replaced/madhva_brahma_sutra_bhasya_3comm_vol1_archive_djvu.txt` (Devanāgarī body present); add source-quality footer |
| `full_translations/ramanuja__shri-bhasya.md` | references DEGRADED Karmakar 1959 OCR | Add source-quality footer; note that GRETIL Śrī-Bhāṣya is listed-but-broken; recommend printed Karmakar 1959 reprint or Thibaut 1904 SBE 48 English as authority for any verbatim quotation |
| `full_translations/sureshvara__brhadaranyaka-varttika.md` | references `vedanta/full_corpus/` (no specific extant file with Sanskrit body) | Add source-quality footer; demote to secondary-attested via Hino 1982/1991, Alston *Realization of the Absolute* (which Sureśvara-affiliated material it covers) |

### Already secondary-attested or safely primary-attested

- All `madhva` `key_passages` cite `madhva_anuvyakhyana_gretil.txt` — CLEAN. SAFE.
- All `gaudapada` `key_passages` cite `gaudapada_mandukya_karika_gretil.txt` — CLEAN. SAFE.
- The 50+ other thinker JSONs that do not embed an explicit `source_edition` path field rely on the engaged_works `summary` prose and on the Codex extraction discipline of citing locus only. Those are not pinned to a specific on-disk file and so are not falsified by file-quality issues, although their underlying source corpus needs the same verification.

---

## Recommendations for the next dispatch wave

1. **Re-extract Vimuktātman and Sarvajñātman** key passages from the now-on-disk djvu replacements. For Vimuktātman, the Devanāgarī body is present and the existing IAST in the JSON should be verified verse-by-verse. For Sarvajñātman, the OCR is too degraded to verify; either acquire the Vajhe Anandāśrama Devanāgarī (hand-OCR an archive scan) or demote to secondary-attested.

2. **Re-verify the Codex-extracted Sanskrit IAST in any passage whose `source_edition` field names a path now classified IMAGE-ONLY.** A small SQL-style query against the JSONs will produce the full list. The risk is not that the IAST is wrong — Codex may have correctly recalled the verses from training data — but that the project cannot defend the citation as a transcription from the file we name.

3. **Acquire the missing GRETIL Śrī-Bhāṣya separately.** The link `sa_rAmAnuja-zrIbhASya-1.txt` is listed but 404s on the GRETIL server; SARIT TEI XML may carry the same text under a different ID, or the Adyar Library "Śrī-Bhāṣya with Śruta-Prakāśikā" may be acquirable as a clean Devanāgarī e-text via SARIT's TEI-XML corpus.

4. **Re-extract the Yukti-Dīpikā body from the Wezler-Motegi 1998 PDF** (not the broken `.txt` in the same directory); the PDF itself is CLEAN by heuristic.

5. **Run the same audit on the secondary-text corpus** in `materials/secondary_texts/` and on whatever German / French / Latin primary corpora exist for the comparator philosophers; the same OCR-vs-Devanāgarī risk applies to Continental scans.

6. **Adopt the convention** that every new `key_passage` produced by Codex must include a `source_quality_class` field set to one of `clean-gretil`, `clean-born-digital`, `acceptable`, `degraded`, `image-only-for-locus-only`. This makes the audit machine-checkable going forward.

7. **Adopt the citation discipline** that any verbatim Sanskrit IAST string in a `key_passage` must have been *literally pasted from the file named in `source_edition`* — not reconstructed from memory — and that the file-class must be CLEAN or ACCEPTABLE. Codex extraction prompts should enforce this.
