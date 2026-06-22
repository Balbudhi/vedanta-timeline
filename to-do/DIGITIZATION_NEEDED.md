# Digitization needed — scans we have, clean OCR pending

Updated 2026-06-22: bad `archive.org` OCR is not considered useful and should not be re-added. This list tracks good page-image scans or image archives only. See `docs/PRIMARY_SCAN_ACQUISITIONS_2026-06-22.md` for the files acquired in this pass and their hashes.

These works have a **good Sanskrit/vernacular SCAN available** (mostly archive.org),
but the auto-OCR `.txt` was too corrupt to trust, so it was removed from the public
corpus and the entries are marked `primary-text-not-in-corpus`. The visual source is
good — these need a **proper OCR / clean digitization pass** later, after which they
flip to on-disk and the entries can be text-grounded.

This is distinct from "need to find" (no source located at all — see the want-list in
`docs/SOURCE_COLLECTION.md` + the `ROSTER_GAPS_*.md` availability flags).

## Clean text acquired in this pass

| Thinker | Work | Source now in repo | Lang |
|---|---|---|---|
| Meykaṇḍār | Śivajñāna-bodham | Project Madurai Unicode text at `data/sources/tamil/saiva_siddhanta/meykandar_sivajnana_bodham_project_madurai.txt`; redistribution header retained | Tamil |
| Aruḷnandi Śivācārya | Śivajñāna-siddhiyār | Project Madurai Unicode text at `data/sources/tamil/saiva_siddhanta/arulnandi_sivajnana_siddhiyar_project_madurai.txt`; redistribution header retained | Tamil |

## Have a scan → OCR later (27)
| Thinker | Work | Scan source (edition) | Lang |
|---|---|---|---|
| Umāpati Śivācārya | Śivaprakāśam / Civappirakācam | Tamil scan now in repo at `data/sources/tamil/saiva_siddhanta/umapati_sivaprakasam_1908_scan.pdf`; rendered sample is legible; embedded OCR is rough | Tamil |
| Puṇyānanda | Kāmakalāvilāsa | DLI Sanskrit scan now in repo at `data/sources/sanskrit/sakta/punyananda_kamakalavilasa_1918_dli_scan.pdf`; rendered sample is clean and legible; text extraction is empty | Sanskrit |
| Jñāneśvar | Jñāneśvarī | Public Domain Mark compressed page-image/text PDF now in repo at `data/sources/marathi/jnaneshwar/jnaneshwari_rajwade_1909_text_pdf.pdf`; full 375 MB source scan cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/marathi/jnaneshwar/jnaneshwari_rajwade_1909_full_source_scan.pdf`; rendered samples are readable; OCR is rough | Marathi |
| Jñāneśvar | Amṛtānubhava | 1876 DLI Marathi scan now in repo at `data/sources/marathi/jnaneshwar/amrtanubhava_1876_dli_scan.pdf`; rendered sample is readable but needs clean OCR | Marathi |
| Yaśomitra | Sphuṭārthā Abhidharmakośavyākhyā | archive.org (Wogihara 1932–36) | Sanskrit |
| Māṇikyanandi | Parīkṣāmukha | 1909 DLI Sanskrit scan now in repo at `data/sources/sanskrit/jaina/pariksamukha_laghuvrtti_1909_dli_scan.pdf`; rendered sample is sharp; text extraction is empty | Sanskrit |
| Vyāsatīrtha / Madhusūdana Sarasvatī | Nyāyāmṛta & Advaitasiddhi with seven commentaries | Public Domain Mark Sanskrit scan split into `data/sources/sanskrit/dvaita/nyayamrta_advaitasiddhi_1934_calcutta_sanskrit_scan_part1.pdf` and `...part2.pdf`; full source cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/dvaita/nyayamrta_advaitasiddhi_1934_calcutta_sanskrit_scan.pdf`; rendered samples are legible | Sanskrit |
| Bhagavadutpala | Spanda-pradīpikā | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/kashmir_shaiva/spanda_pradipika_1898_vizianagaram_scan.pdf`; rendered sample is clear Devanāgarī; embedded OCR/text is not a verified clean transcription | Sanskrit |
| Rājānaka Rāma (Rāmakaṇṭha I) | Spanda-vivṛti | 1912 DLI Sanskrit scan now in repo at `data/sources/sanskrit/kashmir_shaiva/spandakarika_vivriti_ramakantha_1912_dli_scan.pdf`; rendered sample is high-contrast; text extraction is empty | Sanskrit |
| Nārāyaṇakaṇṭha | Mṛgendra-vṛtti / Śrī Mṛgendra Tantram | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/saiva/narayanakantha_mrgendra_tantram_scan.pdf`; rendered sample is clean and legible; text extraction is empty | Sanskrit |
| Bhojadeva / Śrīkumāra tradition | Tattvaprakāśa with Tātparyadīpikā | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/saiva/bhojadeva_tattvaprakasa_tatparyadipika_1920_tss_scan.pdf`; rendered sample is clean and legible; text extraction is empty | Sanskrit |
| Lakṣmaṇa Deśikendra | Śāradā-tilaka | archive.org | Sanskrit |
| Vijñānabhikṣu | Sāṅkhya-Pravacana-Bhāṣya | compressed Devanāgarī scan now in repo at `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_samkhya_pravacana_bhasya_kashi_scan_compressed.pdf`; full-size source cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/vijnanabhiksu/vijnanabhiksu_samkhya_pravacana_bhasya_kashi_scan.pdf` | Sanskrit |
| Vijñānabhikṣu | Yoga-Vārttika | scan now in repo at `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_yoga_varttika_1884_scan.pdf`; rendered sample is OCR-worthy | Sanskrit |
| Vijñānabhikṣu | Brahma-Sūtra Vijñānāmṛta-Bhāṣyam | compressed vol. 1 Devanāgarī scan now in repo at `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_vijnanamrta_bhasya_vol1_kashi_scan_compressed.pdf`; full JP2 source cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/vijnanabhiksu/vijnanabhiksu_vijnanamrta_bhasya_vol1_jp2.zip` | Sanskrit |
| Mahendranath Gupta (`Sri M`) | Śrī Śrī Rāmakṛṣṇa Kathāmṛta | vol. 1 scan now in repo at `data/sources/bengali/ramakrishna/ramakrishna_kathamrita_vol1_ed9_scan.pdf`; rendered sample is OCR-worthy | Bengali |
| Sarada Devi tradition | Śrī Śrī Māyer Kathā | vols. 1-2 scans cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/bengali/sarada/`; edition and redistribution status need verification before public mirroring | Bengali |
| Satchidanandendra Saraswati | Mūlāvidyānirāsaḥ / Śrī Śaṅkara Hṛdaya | DLI scan now in repo at `data/sources/sanskrit/satchidanandendra/satchidanandendra_mulavidya_nirasa_sri_sankara_hridaya_dli_scan.pdf`; rendered sample is sharp | Sanskrit |
| Sarada Devi tradition | Śrī Śrī Māyer Kathā | DLI Bengali scan now in repo at `data/sources/bengali/sarada/sarada_sri_sri_mayer_katha_dli_scan.pdf`; rendered sample is OCR-worthy | Bengali |
| Mahendranath Gupta / Swami Nikhilananda translation witness | The Gospel of Sri Ramakrishna, 1st ed. | DLI English scan split into `data/sources/english/ramakrishna/ramakrishna_gospel_nikhilananda_1942_dli_scan_part1.pdf` and `...part2.pdf`; source full PDF cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/english/ramakrishna/ramakrishna_gospel_nikhilananda_1942_dli_scan.pdf` | English |
| Rāmānuja | Śrī-bhāṣya | 1914 DLI Sanskrit scan now in repo at `data/sources/sanskrit/ramanuja/ramanuja_sri_bhashya_part_1_2_1914_dli_scan.pdf`; rendered sample is OCR-worthy | Sanskrit |
| Rāmānuja tradition | Śrī-bhāṣya-vārttika | 1907 DLI Sanskrit scan now in repo at `data/sources/sanskrit/ramanuja/ramanuja_sri_bhashya_vartika_1907_dli_scan.pdf`; lower-resolution but usable | Sanskrit |
| Jīva Gosvāmī | Sarva-saṃvādinī | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/gaudiya/jiva_sarva_samvadini_sanskrit_scan.pdf`; rendered sample is high-quality | Sanskrit |
| Baladeva Vidyābhūṣaṇa | Siddhānta-ratna, part 1 | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/baladeva/baladeva_siddhanta_ratna_part1_1924_scan.pdf`; rendered sample is high-quality | Sanskrit |
| Baladeva Vidyābhūṣaṇa | Siddhānta-ratna, part 2 | CC0 Sanskrit scan now in repo at `data/sources/sanskrit/baladeva/baladeva_siddhanta_ratna_part2_1927_scan.pdf`; rendered sample is high-quality | Sanskrit |
| Vyāsatīrtha | Tarka-tāṇḍava with Nyāya-pāda commentary | CC0 Sanskrit scan split into `data/sources/sanskrit/dvaita/vyasatirtha_tarka_tandava_nyaya_pada_1938_scan_part1.pdf`, `...part2.pdf`, and `...part3.pdf`; full 189MB source cached locally at `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/dvaita/vyasatirtha_tarka_tandava_nyaya_pada_1938_scan.pdf`; rendered samples are high-quality | Sanskrit |

## Process
1. Re-fetch the scan (PDF/djvu) for the work.
2. Run a proper Sanskrit/vernacular OCR (not the raw archive djvu_txt).
3. Verify the output is clean, save as `data/sources/.../<file>.txt` with provenance.
4. Flip the entry's engaged_work `source_status` to on-disk and add `cite://` grounding.
