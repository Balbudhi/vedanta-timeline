# Digitization needed — scans we have, clean OCR pending

These works have a **good Sanskrit/vernacular SCAN available** (mostly archive.org),
but the auto-OCR `.txt` was too corrupt to trust, so it was removed from the public
corpus and the entries are marked `primary-text-not-in-corpus`. The visual source is
good — these need a **proper OCR / clean digitization pass** later, after which they
flip to on-disk and the entries can be text-grounded.

This is distinct from "need to find" (no source located at all — see the want-list in
`docs/SOURCE_COLLECTION.md` + the `ROSTER_GAPS_*.md` availability flags).

## Have a scan → OCR later (17)
| Thinker | Work | Scan source (edition) | Lang |
|---|---|---|---|
| Aruḷnandi Śivācārya | Śivajñāna-siddhiyār | archive.org (Nallaswami Pillai ed.) | Tamil |
| Umāpati Śivācārya | Śivaprakāśam | archive.org | Tamil |
| Puṇyānanda | Kāmakalāvilāsa | archive.org (Arthur Avalon ed.) | Sanskrit |
| Jñāneśvar | Jñāneśvarī | archive.org | Marathi |
| Jñāneśvar | Amṛtānubhava | archive.org (Pradhan ed.) | Marathi |
| Yaśomitra | Sphuṭārthā Abhidharmakośavyākhyā | archive.org (Wogihara 1932–36) | Sanskrit |
| Māṇikyanandi | Parīkṣāmukha | archive.org | Sanskrit |
| Bhagavadutpala | Spanda-pradīpikā | archive.org | Sanskrit |
| Rājānaka Rāma (Rāmakaṇṭha I) | Spanda-vivṛti | archive.org | Sanskrit |
| Nārāyaṇakaṇṭha | Mṛgendra-vṛtti | archive.org (Institut Français d'Indologie ed.) | Sanskrit |
| Śrīkumāra | Tattvaprakāśa-tātparyadīpikā | archive.org | Sanskrit |
| Lakṣmaṇa Deśikendra | Śāradā-tilaka | archive.org | Sanskrit |
| Vijñānabhikṣu | Sāṅkhya-Pravacana-Bhāṣya | archive.org (Kashi Sanskrit Series / Jangamwadi Math scan) | Sanskrit |
| Vijñānabhikṣu | Yoga-Vārttika | archive.org / DLI scan; title-page verification needed before OCR | Sanskrit |
| Vijñānabhikṣu | Brahma-Sūtra Vijñānāmṛta-Bhāṣyam | archive.org (Kashi Hindu University scan) | Sanskrit |
| Mahendranath Gupta (`Sri M`) | Śrī Śrī Rāmakṛṣṇa Kathāmṛta | archive.org / West Bengal Public Library Network / DLI scan | Bengali |
| Sarada Devi tradition | Śrī Śrī Māyer Kathā | archive.org / DLI scan; edition and redistribution status need verification | Bengali |

## Process
1. Re-fetch the scan (PDF/djvu) for the work.
2. Run a proper Sanskrit/vernacular OCR (not the raw archive djvu_txt).
3. Verify the output is clean, save as `data/sources/.../<file>.txt` with provenance.
4. Flip the entry's engaged_work `source_status` to on-disk and add `cite://` grounding.
