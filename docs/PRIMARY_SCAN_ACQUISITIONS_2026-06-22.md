# Primary Scan Acquisitions — 2026-06-22

This pass keeps bad OCR out of the public corpus. A file counts as acquired here only if it is a useful page-image scan or image archive that can support a later OCR/transcription pass.

## Added to this repo

| Work | Local path | Source | sha256 | Size | Status |
|---|---|---|---|---:|---|
| Vijñānabhikṣu, *Sāṅkhya-Pravacana-Bhāṣya* | `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_samkhya_pravacana_bhasya_kashi_scan_compressed.pdf` | `https://archive.org/details/AJdS_samkhya-darshan-with-pravachan-bhashya-of-gyan-bhikshu-no.-67-kashi-sanskrit-series` | `7497239db2a6eb3df4ad0ab82739277cc5772bd18e751046369c3b76a569cbf2` | 50,303,369 | Compressed image PDF on disk; rendered sample is legible Devanāgarī; needs clean Sanskrit OCR/transcription. Full-size source scan retained locally; see below. |
| Vijñānabhikṣu, *Yoga-Vārttika* (1884 Sanskrit edition) | `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_yoga_varttika_1884_scan.pdf` | `https://archive.org/details/yogavartikavigyanabhikshuramakrishnasastripatvardhankesavasastri1884_202003_300_C` | `b04053ab1b0773d0a482586e728b8432a2aed483a8d82585b3878a387592adcb` | 20,915,349 | Image PDF on disk; rendered sample is legible; needs clean Sanskrit OCR/transcription. |
| Vijñānabhikṣu, *Vijñānāmṛta-Bhāṣya*, vol. 1 | `data/sources/sanskrit/vijnanabhiksu/vijnanabhiksu_vijnanamrta_bhasya_vol1_kashi_scan_compressed.pdf` | `https://archive.org/details/NXwz_brahma-sutra-vigyana-amrita-bhashyam-of-vigyana-bhikshu-with-pt.-kedar-natha-tri` | `4ec0199c3b2bf8c3b447ed8a8f663d00ad9c0053c8672a3711c631c6d9387f27` | 91,940,862 | Compressed from the 405-page JP2 image archive at 1600px max dimension; rendered sample is legible Devanāgarī; needs clean Sanskrit OCR/transcription. Full JP2 archive retained locally; see below. |
| *Śrī Śrī Rāmakṛṣṇa Kathāmṛta*, vol. 1, 9th ed. | `data/sources/bengali/ramakrishna/ramakrishna_kathamrita_vol1_ed9_scan.pdf` | `https://archive.org/details/dli.bengal.10689.16806` | `751e75027aa467bf292f1dd7e2a5b87d50dc55fb054c9952d0ff32e23499d919` | 10,232,125 | Image PDF on disk; rendered sample is legible; needs clean Bengali OCR/transcription. |

## Acquired to local cache, not Git

These are useful image or text sources, but they are either over GitHub's normal single-file limit or need rights/storage review before mirroring.

| Work | Local cache path | Source | sha256 | Size | Why not committed |
|---|---|---|---|---:|---|
| Vijñānabhikṣu, *Sāṅkhya-Pravacana-Bhāṣya* full source scan | `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/vijnanabhiksu/vijnanabhiksu_samkhya_pravacana_bhasya_kashi_scan.pdf` | `https://archive.org/details/AJdS_samkhya-darshan-with-pravachan-bhashya-of-gyan-bhikshu-no.-67-kashi-sanskrit-series` | `0783a4cf450a353586edade19b2319f7642bdc1369a2a9f19ea5e6c212111745` | 122,285,987 | Full-resolution source retained locally; compressed derivative is in Git. |
| Vijñānabhikṣu, *Vijñānāmṛta-Bhāṣya*, vol. 1 full JP2 source | `/Users/eeshan/Dev/source-acquisitions/primary_texts/sanskrit/vijnanabhiksu/vijnanabhiksu_vijnanamrta_bhasya_vol1_jp2.zip` | `https://archive.org/details/NXwz_brahma-sutra-vigyana-amrita-bhashyam-of-vigyana-bhikshu-with-pt.-kedar-natha-tri` | `14c213a4276596f5327f81affb2345adf84df7e8b3ab2d29d8a73a58a98708be` | 393,392,857 | Full-resolution JP2 source retained locally; compressed derivative is in Git. |
| *Śrī Śrī Māyer Kathā*, vol. 1 | `/Users/eeshan/Dev/source-acquisitions/primary_texts/bengali/sarada/sri_sri_mayer_katha_vol1_scan.pdf` | `https://archive.org/details/ShriShriMayerKatha` | `cfa7686e0ebd3ff8045a6a072e7d151de8d611b4eed293a2d807dd21adcbb922` | 15,940,999 | Rights/redistribution status needs review before public mirroring. |
| *Śrī Śrī Māyer Kathā*, vol. 2 | `/Users/eeshan/Dev/source-acquisitions/primary_texts/bengali/sarada/sri_sri_mayer_katha_vol2_scan.pdf` | `https://archive.org/details/ShriShriMayerKatha` | `00cca195e5f06bf28f0749fe6c1fe96eea8b7029df78f3046302a7fa19dd5b20` | 20,560,018 | Rights/redistribution status needs review before public mirroring. |

## Clean text / controlled editions cached locally

These are better than OCR for research, but they are not mirrored into the public repo until rights are clear.

| Corpus | Local cache path | Source | Status |
|---|---|---|---|
| *Śrī Śrī Rāmakṛṣṇa Kathāmṛta* Unicode HTML | `/Users/eeshan/Dev/source-acquisitions/primary_texts/bengali/ramakrishna/official_portal/unicode_pages/` | `https://ramakrishnavivekananda.info/kathamrita/unicodekathamrita/` | 523 chapter HTML files cached; use privately against the scan; license for wholesale mirroring is not declared. |
| Sri Aurobindo official PDFs: *The Secret of the Veda*, *Essays on the Gita*, *The Life Divine*, *The Synthesis of Yoga* | `/Users/eeshan/Dev/source-acquisitions/primary_texts/english/aurobindo/` | `https://www.sriaurobindoashram.org/sriaurobindo/writings.php` | High-quality official controlled editions; use for private citation/page work and public metadata links, not bulk public mirroring. |

## Rejected

Internet Archive `*_djvu.txt` OCR for the Sanskrit and Bengali scans was checked and rejected for this pass. It is not clean enough to ground translations or claims and was not retained in the repo.
