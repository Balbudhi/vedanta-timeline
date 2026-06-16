# Primary-Source Inventory — vedanta-timeline

Generated 2026-06-15. Read-only audit of `engaged_works` across `data/thinkers/*.json`, cross-referenced against the on-disk corpus under `data/sources/`. No thinker JSON was modified.

## 1. Summary counts

| Metric | Count |
|---|---:|
| Total `engaged_works` entries referenced | 580 |
| Already on disk (clean / acceptable / degraded) | 262 |
| Marked `primary-text-not-in-corpus` (missing) | 301 |
| Native English/Bengali originals (no Sanskrit etext needed) | 17 |
| Physical source files on disk | 137 |
| Fetched THIS batch (new .txt) | 9 |

Missing by language:

| Language | Missing |
|---|---:|
| sanskrit | 256 |
| english | 22 |
| tamil-manipravala | 12 |
| hindi | 5 |
| kannada | 2 |
| bengali | 1 |
| vraja-bhasha | 1 |
| sanskrit-vraja-mixed | 1 |
| prakrit | 1 |

## 2. Works already ON DISK

262 entries resolve to files under `data/sources/` (status `clean-on-disk` / `acceptable-on-disk` / `degraded-on-disk`). The physical tree is listed in section 5. Key clusters already present: ten principal Upaniṣads (GRETIL), Brahma-sūtra + Śaṅkara/Rāmānuja/Madhva/Vācaspati/Jayatīrtha bhāṣyas, the six-darśana root sūtras (Nyāya/Vaiśeṣika/Sāṃkhya/Yoga/Mīmāṃsā/Tattvārtha) in `comparator/`, core Kashmir-Śaiva (Abhinavagupta IPV/Tantrasāra/Paramārthasāra, Utpaladeva ĪPK, Kṣemarāja, Spanda-kārikā), Yāmuna's siddhi-trayī + Stotraratna, core Mādhyamaka/Yogācāra (Nāgārjuna MMK + Vigrahavyāvartanī, Vasubandhu Triṃśikā/Viṃśatikā, Candrakīrti Madhyamakāvatāra, Dharmakīrti Nyāyabindu + Pramāṇavārttika), and Caitanya-Gauḍīya (Rūpa, Jīva).

## 3. MISSING Sanskrit primary texts (256 unique) — feasibility

Feasibility legend: **FETCHED** = collected this batch; **GRETIL/Muktabodha/Jaina/Buddhist** = clean primary-language etext very likely freely available at the named source (filename/edition to confirm); **No clean etext** = lost, fragmentary, oral, or no digital primary-language transcription located.

| Thinker | Work (title_iast) | Tier | Feasibility / best free source |
|---|---|---|---|
| Abhinanda Yogin | Mahārtha-Mañjarī (mūla-gāthās) | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Abhinavagupta | Abhinava-Bhāratī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Abhinavagupta | Dhvanyāloka-Locana | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Abhinavagupta | Parātrīśikā-Vivaraṇa | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Abhinavagupta | Īśvara-Pratyabhijñā-Vivṛti-Vimarśinī | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Adi Sankara | Aparokṣānubhūti | school-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Adi Sankara | Bhaja-Govindam | school-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Adi Sankara | Kena-Upaniṣad-Bhāṣya (Pada-Bhāṣya and Vākya-Bhāṣya) | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Adi Sankara | Muṇḍaka-Upaniṣad-Bhāṣya | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Adi Sankara | Saundarya-Laharī | school-ascribed | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Adi Sankara | Śivānanda-Laharī | school-ascribed | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Akalanka | Aṣṭa-Sahasrī | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Akalanka | Laghīyastraya | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Akalanka | Nyāya-Viniścaya | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Akalanka | Pramāṇa-Saṅgraha | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Akalanka | Siddhi-Viniścaya | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Akalanka | Tattvārtha-Vārttika | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Akshobhya Tirtha | Tat-Tvam-Asi-Khaṇḍana | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Amrtananda-natha | Cidvilāsa-Stava | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Amrtananda-natha | Yoginī-Hṛdaya-Dīpikā | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Anandabodha | Nyāya-Dīpāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Anandabodha | Nyāya-Makaranda | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Anandabodha | Pramāṇa-Mālā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Anantakrishna Sastri | Advaita-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Anantakrishna Sastri | Advaita-Tattva-Sudhā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Anantakrishna Sastri | Vedānta-Paribhāṣā edition | securely-authored | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Anantakrishna Sastri | Vedānta-Rakṣā-Maṇi | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Anantakrishna Sastri | Śatabhūṣaṇī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Appayya Dikshita | Parimala | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Appayya Dikshita | Siddhānta-Leśa-Saṃgraha | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Appayya Dikshita | Ānanda-Laharī-Vyākhyā | traditionally-ascribed | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Appayya Dikshita | Śivārka-Maṇi-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Asanga | Abhidharma-Samuccaya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Asanga | Bodhisattva-Bhūmi | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Asanga | Mahāyāna-Saṅgraha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Asanga | Yogācāra-Bhūmi-Śāstra | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Asmarathya | Brahma-Sūtra citation fragments | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Atiśa Dīpaṅkara Śrījñāna | Bodhi-Patha-Pradīpa | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Atiśa Dīpaṅkara Śrījñāna | Madhyamakopadeśa | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Audulomi | Brahma-Sūtra citation fragments | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Baladeva Vidyabhushana | Prameya-Ratnāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Baladeva Vidyabhushana | Siddhānta-Ratnam | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bannanje Govindacharya | Mahābhārata-Tātparya-Nirṇaya Sanskrit Vyākhyāna | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Bannanje Govindacharya | Stuti-Candrikā on Vāyu-Stuti | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Bhaktivinoda Thakura | Bhāgavatārka-Marīci-Mālā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhaktivinoda Thakura | Tattva-Sūtra | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhaktivinoda Thakura | Vedānta-Adhikaraṇa-Mālā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhartrhari | Vākyapadīya | securely-authored | FETCHED this batch (GRETIL TEI) |
| Bhartrprapanca | Bṛhadāraṇyaka commentary fragments (reconstructed) | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Bhaskara | Gītā-Bhāṣya fragments | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Bhaskararaya | Saubhāgya-Bhāskara | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhaskararaya | Setubandha | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhaskararaya | Varivasyā-Rahasya | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhatta Kallata | Spanda-Sarva-Sva | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhatta Ramakantha II | Kiraṇa-Vṛtti | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhatta Ramakantha II | Mataṅga-Vṛtti | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhatta Ramakantha II | Nareśvara-Parīkṣā-Prakāśa | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Bhatta Ramakantha II | Sārdha-Tri-Śatikā-Lokulīśvarāgama-Vṛtti | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhava-Ganesha | Pradīpa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhava-Ganesha | Tattva-Yāthārthya-Dīpana | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Bhaviveka | Prajñā-Pradīpa | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Bhaviveka | Tarkajvālā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhoja-raja | Rāja-Mārtaṇḍa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhāsarvajña | Nyāya-Bhūṣaṇa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Bhāsarvajña | Nyāya-Sāra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Bodhayana | Brahma-Sūtra-Vṛtti | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Brahmadatta | Lost Upaniṣad commentary | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Brahmananda Sarasvati | Gauḍa-Brahmānandī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Brahmananda Sarasvati | Laghu-Candrikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Buddhaghosa | Aṭṭhasālinī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Buddhaghosa | Sumaṅgala-Vilāsinī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Buddhapālita | Buddhapālita-Mūlamadhyamakavṛtti | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Candrakirti | Prasanna-Padā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Chandrashekhara Bharati III | Gururāja-Sūkti-Mālikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Chandrashekhara Bharati III | Recorded oral discourses | traditionally-ascribed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Chandrashekhara Bharati III | Vivekacūḍāmaṇi-Bhāṣya | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Cidambarananda | Mahānaya-Prakāśa | lineage-attributed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Dharmakirti | Hetu-Bindu | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmakirti | Pramāṇa-Viniścaya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmakirti | Sambandha-Parīkṣā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmakirti | Vāda-Nyāya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmapāla | Triṃśikā-Vṛtti (Dharmapāla) | attributed | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmapāla | Ālambana-Parīkṣā-Vṛtti | attributed | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmaraja Adhvarindra | Vedānta-Paribhāṣā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Dharmottara | Apoha-Prakaraṇa | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dharmottara | Nyāya-Bindu-Ṭīkā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Dharmottara | Pramāṇa-Viniścaya-Ṭīkā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dignaga | Pramāṇa-Samuccaya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Dignaga | Ālambana-Parīkṣā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Gangesha Upadhyaya | Tattva-Cintāmaṇi | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Goswami Gokulnatha | Sarva-Nirṇaya-Prakaraṇa-Vivṛti | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Goswami Hariraya | Hariraya-Vivaraṇa on Ṣoḍaśa-Granthāḥ | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Haribhadra Suri | Yoga-Bindu | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Haribhadra Suri | Yoga-Dṛṣṭi-Samuccaya | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Haribhadra Suri | Ṣaḍ-Darśana-Samuccaya | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Hastamalaka | Hastāmalaka-Stotra | traditionally-ascribed | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Hemacandra Suri | Pramāṇa-Mīmāṃsā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Hemacandra Suri | Yoga-Śāstra | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Hrasvanatha | Krama-Sadbhāva | lineage-attributed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Jagadguru Ramabhadracharya | Aṣṭādhyāyī-Pradīpa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Jagadguru Ramabhadracharya | Śrīrāghavakṛpā-Bhāṣyam on Bhagavad-Gītā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Jagadguru Ramabhadracharya | Śrīrāghavakṛpā-Bhāṣyam on Brahma-Sūtra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Jagadguru Ramabhadracharya | Śrīrāghavakṛpā-Bhāṣyam on Eleven Principal Upaniṣads | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Jagadguru Ramabhadracharya | Śrīrāghavakṛpā-Bhāṣyam on Nārada-Bhakti-Sūtra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Jayanta Bhaṭṭa | Nyāya-Kalikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Jayanta Bhaṭṭa | Nyāya-Mañjarī | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Jayaratha | Tantrāloka-Viveka | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Jayatirtha | Vādāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Jiva Gosvami | Sarva-Saṃvādinī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Jnanagarbha | Satya-Dvaya-Vibhaṅga | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Jñānaśrīmitra | Jñānaśrīmitra-Nibandhāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kamalaśīla | Bhāvanā-Krama I | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Kamalaśīla | Madhyamakāloka | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Kamalaśīla | Tattva-Saṅgraha-Pañjikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kasakrtsna | Brahma-Sūtra citation fragments | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Kavi Karnapura | Alaṅkāra-Kaustubha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kavi Karnapura | Caitanya-Candrodaya-Nāṭaka | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kavi Karnapura | Ānanda-Vṛndāvana-Campū | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Keshava-Kashmiri Bhatta | Tattva-Prakāśikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Khaṇḍadeva | Bhāṭṭa-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Khaṇḍadeva | Bhāṭṭa-Kaustubha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kshemaraja | Spanda-Sandoha | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Kshemaraja | Stava-Cintāmaṇi-Ṭīkā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Kshemaraja | Śiva-Sūtra-Vimarśinī | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Kumarila Bhatta | Tantra-Vārttika | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Kundakunda | Pañcāstikāya | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Kundakunda | Pravacana-Sāra | traditionally-ascribed | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Kundakunda | Samaya-Sāra | traditionally-ascribed | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Lakshmidhara | Saundarya-Laharī-Vṛtti | securely-authored | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Lakulisha | Pāśupata-Sūtra | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Lankavatara-Sutra | Laṅkāvatāra-Sūtra | school-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Mahesvarananda | Mahārtha-Mañjarī with Parimala | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Maitreya-attributed corpus | Abhisamayālaṃkāra | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Maitreya-attributed corpus | Dharma-Dharmatā-Vibhāga | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Maitreya-attributed corpus | Madhyānta-Vibhāga | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Maitreya-attributed corpus | Mahāyāna-Sūtra-Alaṃkāra | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Malini-Vijaya-Tantra (position-entry) | Mālinī-Vijaya-Tantra | traditionally-ascribed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Mallisena | Syādvāda-Mañjarī | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Nagarjuna | Catuḥ-Stava | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Nagarjuna | Ratnāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Nagarjuna | Yukti-Ṣaṣṭikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Nagarjuna | Śūnyatā-Saptati | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Narahari Tirtha | Gītā-Bhāṣya-Vivaraṇa | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Narayana Panditacharya | Sumadhva-Vijaya | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Nathamuni | Nyāya-Tattva | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Nathamuni | Yoga-Rahasya | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Padmanabha Tirtha | Sannyāya-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Padmanabha Tirtha | Sannyāya-Ratnāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Pancaratra (position-entry) | Pauṣkara-Saṃhitā | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Pancaratra (position-entry) | Sātvata-Saṃhitā | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Prabhakara Mishra | Bṛhatī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Prashastapada | Padārtha-Dharma-Saṅgraha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Purushottama | Avaraṇa-Bhaṅga | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Purushottama | Bhāṣya-Prakāśa | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Purushottama | Prasthāna-Ratnākara | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Pārthasārathi Miśra | Nyāya-Ratna-Mālā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Pārthasārathi Miśra | Śāstra-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Raghavendra Tirtha | Prakāśa sub-commentaries | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Raghavendra Tirtha | Tarka-Tāṇḍava-Pariṃala | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Raghavendra Tirtha | Tātparya-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Raghunatha Shiromani | Padārtha-Tattva-Nirūpaṇa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Raghunatha Shiromani | Tattva-Cintāmaṇi-Dīdhiti | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Ramanuja | Gadya-Trayam | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Ramanuja | Nitya-Grantha | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Ramanuja | Vedānta-Dīpa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Ramanuja | Vedānta-Sāra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Rangaramanuja Muni | Nyāya-Siddhāñjana-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Rangaramanuja Muni | Siddhānta-Sāra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Rangaramanuja Muni | Upaniṣad-Bhāṣyāḥ | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Rangaramanuja Muni | Viṣaya-Vākya-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Rangaramanuja Muni | Śruta-Prakāśikā-Bhāva-Prakāśikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Rangaramanuja Muni | Śārīraka-Śāstra-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Ratnakīrti | Ratnakīrti-Nibandhāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sadyojyotis | Bhoga-Kārikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sadyojyotis | Mokṣa-Kārikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sadyojyotis | Nareśvara-Parīkṣā | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Sadyojyotis | Tattva-Saṅgraha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sadyojyotis | Tattva-Trayanirṇaya | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Samantabhadra | Svayambhū-Stotra | securely-authored | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Samantabhadra | Āpta-Mīmāṃsā | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Sanatana Gosvami | Bṛhad-Bhāgavatāmṛta | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sanatana Gosvami | Hari-Bhakti-Vilāsa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sanatana Gosvami | Vaiṣṇava-Toṣaṇī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sanghabhadra | Abhidharma-Samaya-Pradīpikā | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Sanghabhadra | Nyāyānusāra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Sarvajnatman | Pañca-Prakriyā | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Satchidanandendra Saraswati | Māṇḍūkya-Rahasya-Vivṛti | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Satchidanandendra Saraswati | Mūlāvidyā-Nirāsa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Satchidanandendra Saraswati | Vedānta-Prakriyā-Pratyabhijñā | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Satchidanandendra Saraswati | Śuddha-Śāṅkara-Prakriyā-Bhāskara | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Siddhasena Divākara | Nyāyāvatāra | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sivananda Yogin | Ṛju-Vimarśinī | lineage-attributed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Somananda | Śiva-Dṛṣṭi | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Sthiramati | Madhyānta-Vibhāga-Bhāṣya-Ṭīkā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Sthiramati | Triṃśikā-Bhāṣya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Sudarshana Suri | Śruta-Prakāśikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Sundara-Pandya | Lost verses cited in Naiṣkarmya-Siddhi | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Svacchanda-Tantra (position-entry) | Svacchanda-Tantra | traditionally-ascribed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Swami Karpatri | Vedārtha-Pārijāta | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Totaka | Toṭakāṣṭaka | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Totaka | Śrutisāra-Samuddharaṇa | traditionally-ascribed | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Trisirobhairava-Tantra (position-entry) | Triśirobhairava-Tantra | traditionally-ascribed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Trivikrama Pandita | Tattva-Pradīpa | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Trivikrama Pandita | Vāyu-Stuti | securely-authored | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Udayana | Nyāya-Vārttika-Tātparya-Pariśuddhi | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Udayana | Ātma-Tattva-Viveka | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Uddyotakara | Nyāya-Vārttika | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Upavarsa | Lost Vedāntic citations | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Utpaladeva | Ajaḍa-Pramātṛ-Siddhi | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Utpaladeva | Sambandha-Siddhi | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Utpaladeva | Īśvara-Siddhi | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Uttamur Viraraghavacharya | Mīmāṃsā-Nyāya-Prakāśa-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Uttamur Viraraghavacharya | Nyāya-Kusumāñjali-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Uttamur Viraraghavacharya | Nyāya-Pariśuddhi-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Uttamur Viraraghavacharya | Paramārtha-Bhūṣaṇa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Uttamur Viraraghavacharya | Sarvārtha-Siddhi-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Uttamur Viraraghavacharya | Vaiśeṣika-Rasāyana | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Uttamur Viraraghavacharya | Śrī-Bhāṣyārtha-Darpaṇa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vachaspati Misra | Nyāya-Vārttika-Tātparya-Ṭīkā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vachaspati Misra | Tattva-Vaiśāradī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vallabha-Balaka | Bālaka-Bhāṣya | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vallabhacharya | Subodhinī | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Vallabhacharya | Tattvārtha-Dīpa-Nibandha | securely-authored | Likely GRETIL Jaina tree or Jaina eLibrary; verify |
| Vallabhacharya | Ṣoḍaśa-Granthāḥ | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vasubandhu | Abhidharma-Kośa-Bhāṣya | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Vasubandhu | Karma-Siddhi-Prakaraṇa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vasubandhu | Trisvabhāva-Nirdeśa | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vedanta Deshika | Adhikaraṇa-Sārāvalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vedanta Deshika | Nyāya-Pariśuddhi | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vedanta Deshika | Nyāya-Siddhāñjana | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vedanta Deshika | Śata-Dūṣaṇī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vidyaranya | Sarva-Darśana-Saṃgraha | traditionally-ascribed | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vijayindra Tirtha | Madhva-Tantra-Mukha-Mardana | securely-authored | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Vijayindra Tirtha | Nyāyādhva-Dīpikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vijayindra Tirtha | Nyāyāmṛta-Vyākhyā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vijnana-Bhairava-Tantra (position-entry) | Vijñāna-Bhairava-Tantra | traditionally-ascribed | Likely on Muktabodha (muktabodha.org) digital library — Kashmir Śaiva/Tantra/Śākta; verify exact text |
| Vijnanabhikshu | Sāṅkhya-Pravacana-Bhāṣya | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vishvanatha Cakravarti | Mādhurya-Kādambinī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vishvanatha Cakravarti | Rāga-Vartma-Candrikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Vishvanatha Cakravarti | Sārārtha-Darśinī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vitthalanatha | Subodhinī completion | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Vitthalanatha | Vidvan-Maṇḍana | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Vyasatirtha | Tātparya-Candrikā | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Yadava-Prakasha | Lost Bhedābheda corpus | disputed | No standalone etext — lost / fragmentary / oral; reconstructable only from quoting works |
| Yashovijaya | Adhyātma-Sāra | securely-authored | GRETIL coverage partial; check GRETIL + Muktabodha + archive.org; some advaita sub-commentaries have no clean etext |
| Yashovijaya | Jaina-Tarka-Bhāṣā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Yashovijaya | Nyāya-Loka | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Yashovijaya | Pramāṇa-Mīmāṃsā-Vyākhyāna | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Āryadeva | Catuḥśataka | securely-authored | Likely GRETIL stotra collection or sanskritdocuments.org; verify |
| Śrīdhara | Nyāya-Kandalī | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Śālikanātha Miśra | Prakaraṇa-Pañcikā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Śālikanātha Miśra | Ṛju-Vimalā | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Śāntarakṣita | Madhyamakālaṅkāra | securely-authored | Likely GRETIL (corpustei or 1_sanskr Buddhist tree) or DSBC/rangjung; verify |
| Śāntarakṣita | Tattva-Saṅgraha | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |
| Śāntideva | Bodhicaryāvatāra | securely-authored | FETCHED this batch (GRETIL TEI) |
| Śāntideva | Śikṣā-Samuccaya | securely-authored | Check GRETIL (corpustei + 1_sanskr) and Muktabodha; feasibility unconfirmed |

## 4. Fetched THIS batch (2026-06-15)

All from the GRETIL TEI `corpustei` collection (CC BY-NC-SA 4.0), converted to plain UTF-8 IAST text with a provenance header. All under the 2 MB cap; each verified as real Sanskrit, not an HTML error page.

| Thinker | Work | Path (under data/sources/) | Bytes | GRETIL source file |
|---|---|---|---:|---|
| Bhartṛhari | Vākyapadīya | sanskrit/grammar/bhartrhari_vakyapadiya.txt | 227,248 | sa_bhartRhari-vAkyapadIya.xml |
| Dharmakīrti | Hetubindu | sanskrit/buddhist/dharmakirti_hetu_bindu.txt | 50,268 | sa_dharmakIrti-hetubindu.xml |
| Dharmakīrti | Pramāṇavārttika (kārikā) | sanskrit/buddhist/dharmakirti_pramana_varttika_karika.txt | 141,970 | sa_dharmakIrti-pramANavArttikakArikA.xml |
| Dharmakīrti | Saṃtānāntarasiddhi | sanskrit/buddhist/dharmakirti_santanantarasiddhi.txt | 10,319 | sa_dharmakIrti-saMtAnAntarasiddhi.xml |
| Vasubandhu | Abhidharmakośabhāṣya | sanskrit/buddhist/vasubandhu_abhidharmakosa_bhasya.txt | 1,096,424 | sa_vasubandhu-abhidharmakozabhASya.xml |
| Śāntideva | Bodhicaryāvatāra | sanskrit/buddhist/santideva_bodhicaryavatara.txt | 108,002 | sa_zAntideva-bodhicaryAvatAra.xml |
| Śāntarakṣita | Tattvasaṅgraha | sanskrit/buddhist/santaraksita_tattvasangraha.txt | 806,808 | sa_zAntarakSita-tattvasaMgraha.xml |
| Śaṅkara (school) | Saundaryalaharī | sanskrit/vedanta/sankara_school_saundaryalahari.txt | 47,406 | sa_zaMkara-saundaryalaharI.xml |
| (Upaniṣad) | Praśna-Upaniṣad w/ Śaṅkara bhāṣya | sanskrit/vedic/prasna_upanisad_sankara_bhasya_gretil.txt | 81,103 | sa_praznopaniSad-comm.xml |
| | | **TOTAL** | **2,569,548** | |

## 5. Prioritized remaining acquisition plan

Highest-value MISSING Sanskrit texts that are most-cited by major thinkers and most likely freely available. Filenames are confirmed-200 on GRETIL where noted; others need a filename probe.

### 5a. High priority — confirmed available, fetch next
- These were probed and exist on GRETIL but were deferred to keep this batch bounded, OR live in GRETIL's `1_sanskr` plaintext tree (different naming):
  - **Praśna-Upaniṣad with Śaṅkara bhāṣya** — also at `1_sanskr/1_veda/4_upa/prasupbu.htm` (101 KB) — already fetched via corpustei.
  - **Nyāya-sūtra + Vātsyāyana + Uddyotakara + Vācaspati glosses** — `1_sanskr/.../nyaya/nystik_u.htm` (1.44 MB) confirmed; the composite Nyāya commentarial stack. (Root sūtra + bhāṣya already on disk separately.)

### 5b. High priority — needs filename probe on GRETIL / Muktabodha (very likely free)
1. **Kena-Upaniṣad & Muṇḍaka-Upaniṣad with Śaṅkara bhāṣya** (Ādi Śaṅkara, securely-authored) — root Upaniṣads + Śaṅkara's pada/vākya bhāṣyas; near-certainly on GRETIL `1_sanskr/1_veda/4_upa/` (try `kenupsbu.htm`, `mundupsbu.htm`).
2. **Candrakīrti — Prasannapadā** (Madhyamaka) — GRETIL `1_sanskr` Buddhist tree or DSBC.
3. **Dignāga — Ālambanaparīkṣā; Pramāṇasamuccaya** — GRETIL/DSBC (Sanskrit reconstructions exist).
4. **Jayanta Bhaṭṭa — Nyāyamañjarī** — GRETIL `1_sanskr/6_sastra/3_phil/nyaya/`.
5. **Gaṅgeśa — Tattvacintāmaṇi** (Navya-Nyāya foundational) — GRETIL/SARIT; large, watch size.
6. **Dharmaraja Adhvarindra — Vedāntaparibhāṣā** (the standard Advaita epistemology primer) — GRETIL/sanskritdocuments.
7. **Appayya Dīkṣita — Siddhāntaleśasaṅgraha** — GRETIL/archive.org.
8. **Śrīharṣa — Khaṇḍanakhaṇḍakhādya** — GRETIL/SARIT.
9. **Maṇḍana Miśra — Vidhiviveka; Vimuktātman — Iṣṭasiddhi; Sarvajñātman — Saṃkṣepaśārīraka; Citsukha — Tattvapradīpikā** — advaita classics; partial GRETIL/Muktabodha coverage, probe each.
10. **Madhva — Brahmasūtrabhāṣya; Viṣṇutattvanirṇaya** — GRETIL/dvaita.org (dvaita.org hosts clean Devanāgarī/IAST Mādhva etexts).
11. **Hemacandra — Yogaśāstra, Pramāṇamīmāṃsā; Haribhadra — Ṣaḍdarśanasamuccaya, Yogadṛṣṭisamuccaya, Yogabindu** — Jaina eLibrary / GRETIL Jaina tree.
12. **Kashmir-Śaiva second tier** (Mahārthamañjarī, Parātrīśikāvivaraṇa, ĪPVV, Tantrāloka-Viveka by Jayaratha, Spandasarvasva, Bhāskararāya's Śākta corpus) — **Muktabodha** is the authoritative free source.

### 5c. Genuinely UNAVAILABLE as free primary-language etext
- All `[disputed]` Brahma-sūtra "citation fragments" (Asmarathya, Auḍulomi, Kāśakṛtsna, Bodhāyana, Bhartṛprapañca, Brahmadatta) — these survive only as quotations inside extant bhāṣyas; no standalone text exists to fetch.
- Modern oral/recorded discourses (e.g. Chandraśekhara Bhāratī's recorded discourses) — not etexts.
- Recently-composed works by living/20th–21st-c. authors (Bannanje Govindacharya's Sanskrit vyākhyānas, Jagadguru Rāmabhadrācārya's Śrīrāghavakṛpābhāṣyam set, Anantakrishna Sastri's editions) — under copyright; not freely redistributable plain-text.

## 6. Notes on method & licensing
- GRETIL TEI (`corpustei/`) and plaintext (`1_sanskr/`) trees are reachable from this environment over HTTP; directory autoindex is disabled (403), so filenames must be probed individually or looked up via GRETIL's bibliographic page.
- All GRETIL material is **CC BY-NC-SA 4.0**; headers in each fetched file record source URL, retrieval date, and licence.
- Muktabodha (muktabodha.org), dvaita.org, sanskritdocuments.org, and the Jaina eLibrary are the right complements for texts GRETIL lacks (Kashmir Śaiva, Mādhva, stotra, Jaina respectively).
- Pali (SuttaCentral) and Prakrit (GRETIL Jaina) layers already have seed files on disk.

## 7. Physical on-disk corpus (`data/sources/`)

```
  795,677  data/sources/english/aurobindo/the-future-poetry.txt
  953,976  data/sources/english/vivekananda_complete_works/vol_1.txt
  982,369  data/sources/english/vivekananda_complete_works/vol_2.txt
1,041,003  data/sources/english/vivekananda_complete_works/vol_3.txt
  936,331  data/sources/english/vivekananda_complete_works/vol_4.txt
  954,218  data/sources/english/vivekananda_complete_works/vol_5.txt
  967,828  data/sources/english/vivekananda_complete_works/vol_6.txt
  605,040  data/sources/english/vivekananda_complete_works/vol_7.txt
  832,901  data/sources/english/vivekananda_complete_works/vol_8.txt
  763,499  data/sources/english/vivekananda_complete_works/vol_9.txt
  946,690  data/sources/english/whitehead/adventures-of-ideas.txt
  818,875  data/sources/english/whitehead/b30010238.txt
  721,295  data/sources/english/whitehead/in.ernet.dli.2015.506439.txt
1,263,098  data/sources/english/whitehead/processrealityes0000unse.txt
  765,389  data/sources/german/adorno/DialecticOfEnlightenmentTheodorW.AdornoMaxHorkheimer.txt
  956,058  data/sources/german/adorno/TheodorAdorno-NegativeDialektik.txt
  309,761  data/sources/german/adorno/adorno_jargon.txt
  972,220  data/sources/german/adorno/theodor-adorno-dialectica-negativa-1975.txt
1,782,434  data/sources/german/freud/Freud1919Traumdeutung5teK.txt
1,117,600  data/sources/german/freud/Freud_1900_Die_Traumdeutung_k.txt
1,457,578  data/sources/german/freud/b3136696x.txt
1,226,133  data/sources/german/hegel/phaenomenologie_des_geistes.txt
1,391,964  data/sources/german/hegel/wissenschaft_der_logik.txt
1,769,757  data/sources/german/heidegger/being-and-time-martin-heidegger-1962.txt
  423,797  data/sources/german/heidegger/heidegger-what-is-metaphysics-1928.txt
1,166,672  data/sources/german/heidegger/heideggermartinseinundzeit_20200121.txt
1,439,373  data/sources/german/heidegger/martin-heidegger-ser-y-tiempo-sein-und-zeit-1927.txt
  512,520  data/sources/german/heidegger/martinheideggerparmenides.txt
  925,778  data/sources/german/husserl/HusserlErfahrungUndUrteil.txt
1,137,962  data/sources/german/husserl/IdeasPartIi.txt
  430,550  data/sources/german/husserl/husserl-edmund.-meditaciones-cartesianas-ocr-1996.txt
1,203,690  data/sources/german/husserl/ideenzueinerrein00unse.txt
1,096,854  data/sources/german/husserl/in.ernet.dli.2015.188260.txt
1,785,110  data/sources/german/husserl/logischeuntersuc00hussuoft.txt
  630,825  data/sources/german/husserl/logischeuntersuc01hussuoft.txt
3,859,547  data/sources/german/kant/grundlegung.txt
1,344,379  data/sources/german/kant/kritik_der_praktischen_vernunft.txt
1,278,435  data/sources/german/kant/kritik_der_reinen_vernunft.txt
  845,340  data/sources/german/kant/kritik_der_urteilskraft.txt
2,116,717  data/sources/german/marx/CapitalVolume1.txt
  242,794  data/sources/german/marx/ComManifesto.txt
2,067,400  data/sources/german/marx/KarlMarxDasKapitalErstausgabe1867.txt
  226,476  data/sources/german/nietzsche/_en_antichrist.txt
  408,979  data/sources/german/nietzsche/_en_beyond_good_and_evil.txt
  353,569  data/sources/german/nietzsche/_en_birth_of_tragedy.txt
  596,072  data/sources/german/nietzsche/_en_dawn_of_day.txt
  303,691  data/sources/german/nietzsche/_en_ecce_homo.txt
  358,582  data/sources/german/nietzsche/_en_genealogy_of_morals.txt
  244,197  data/sources/german/nietzsche/_en_human_all_too_human.txt
  566,777  data/sources/german/nietzsche/_en_joyful_wisdom.txt
  682,926  data/sources/german/nietzsche/_en_thus_spake_zarathustra.txt
  454,385  data/sources/german/nietzsche/_en_twilight_idols.txt
  565,302  data/sources/german/nietzsche/also_sprach_zarathustra.txt
  758,281  data/sources/german/nietzsche/der_wille_zur_macht.txt
  222,564  data/sources/german/nietzsche/ecce_homo.txt
  317,769  data/sources/german/nietzsche/geburt_der_tragoedie.txt
  425,705  data/sources/german/nietzsche/jenseits_von_gut_und_boese.txt
  613,917  data/sources/german/nietzsche/menschliches_allzumenschliches.txt
    2,462  data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json
    3,068  data/sources/pali/suttacentral/sn35.240_kummopamasutta_root-pli-ms.json
  238,374  data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt
  448,262  data/sources/sanskrit/_kashmir_saivism/AdvaitasiddhiVsNyayamrta.txt
  104,992  data/sources/sanskrit/buddhist/candrakirti_madhyamakavatara.txt
   50,268  data/sources/sanskrit/buddhist/dharmakirti_hetu_bindu.txt
  119,215  data/sources/sanskrit/buddhist/dharmakirti_pramana_varttika.txt
  141,970  data/sources/sanskrit/buddhist/dharmakirti_pramana_varttika_karika.txt
   10,319  data/sources/sanskrit/buddhist/dharmakirti_santanantarasiddhi.txt
   59,571  data/sources/sanskrit/buddhist/nagarjuna_mula_madhyamaka_karika.txt
   50,863  data/sources/sanskrit/buddhist/nagarjuna_vigraha_vyavartani.txt
  806,808  data/sources/sanskrit/buddhist/santaraksita_tattvasangraha.txt
  108,002  data/sources/sanskrit/buddhist/santideva_bodhicaryavatara.txt
1,096,424  data/sources/sanskrit/buddhist/vasubandhu_abhidharmakosa_bhasya.txt
    3,897  data/sources/sanskrit/buddhist/vasubandhu_trimsika.txt
   18,032  data/sources/sanskrit/buddhist/vasubandhu_vimsatika.txt
2,095,748  data/sources/sanskrit/caitanya_gaudiya/jiva_sat_sandarbha.txt
  383,997  data/sources/sanskrit/caitanya_gaudiya/rupa_bhakti_rasamrta_sindhu.txt
   49,907  data/sources/sanskrit/comparator/aksapada_nyaya_sutra.txt
   27,435  data/sources/sanskrit/comparator/badarayana_brahma_sutra.txt
   10,204  data/sources/sanskrit/comparator/isvarakrsna_samkhya_karika.txt
  167,641  data/sources/sanskrit/comparator/jaimini_mimamsa_sutra.txt
   23,117  data/sources/sanskrit/comparator/kanada_vaisesika_sutra.txt
   13,267  data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt
1,398,940  data/sources/sanskrit/comparator/shabara_mimamsa_sutra_bhasya.txt
   46,354  data/sources/sanskrit/comparator/umasvati_tattvartha_sutra.txt
  431,468  data/sources/sanskrit/comparator/vatsyayana_nyaya_bhasya.txt
  143,237  data/sources/sanskrit/comparator/vyasa_yoga_bhasya.txt
  227,248  data/sources/sanskrit/grammar/bhartrhari_vakyapadiya.txt
   32,798  data/sources/sanskrit/kala_cakra/abhinavagupta_tantraloka_chapter06_kalopaya_kalacakra.txt
  357,301  data/sources/sanskrit/kashmir_shaiva/abhinavagupta_ipv.txt
   15,647  data/sources/sanskrit/kashmir_shaiva/abhinavagupta_paramartha_sara.txt
  130,963  data/sources/sanskrit/kashmir_shaiva/abhinavagupta_tantrasara.txt
   42,058  data/sources/sanskrit/kashmir_shaiva/ksemaraja_pratyabhijna_hrdayam.txt
    8,058  data/sources/sanskrit/kashmir_shaiva/spanda_karika.txt
   67,922  data/sources/sanskrit/kashmir_shaiva/utpaladeva_isvara_pratyabhijna_karika.txt
  433,392  data/sources/sanskrit/mimamsa/kumarila_sloka_varttika_comm.txt
  563,090  data/sources/sanskrit/mimamsa/madhava_jaimini_nyaya_mala.txt
1,336,922  data/sources/sanskrit/mimamsa/sucaritamisra_sloka_varttika.txt
   18,598  data/sources/sanskrit/nyaya/annambhatta_tarka_sangraha.txt
1,306,849  data/sources/sanskrit/nyaya/annambhatta_tarka_sangraha_comm.txt
   24,888  data/sources/sanskrit/nyaya/dharmakirti_nyaya_bindu.txt
   51,699  data/sources/sanskrit/nyaya/nyaya_sutra_gautama.txt
  271,638  data/sources/sanskrit/nyaya/udayana_nyaya_kusumanjali.txt
   56,744  data/sources/sanskrit/samkhya/samkhya_sutra_kapila.txt
   30,837  data/sources/sanskrit/vedanta/full_corpus/gaudapada_mandukya_karika_gretil.txt
   75,602  data/sources/sanskrit/vedanta/full_corpus/madhusudana_siddhanta_bindu_gretil.txt
  252,379  data/sources/sanskrit/vedanta/full_corpus/madhva_anuvyakhyana_gretil.txt
  313,885  data/sources/sanskrit/vedanta/full_corpus/mandana_misra_brahma_siddhi_gretil.txt
  142,891  data/sources/sanskrit/vedanta/full_corpus/shankara_upadesa_sahasri_gretil.txt
   90,654  data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt
1,947,991  data/sources/sanskrit/vedanta/full_corpus/vyasatirtha_tarka_tandava_gretil.txt
  390,134  data/sources/sanskrit/vedanta/full_corpus/yamuna_atma_siddhi_gretil.txt
   19,895  data/sources/sanskrit/vedanta/full_corpus/yamuna_isvara_siddhi_gretil.txt
   30,579  data/sources/sanskrit/vedanta/full_corpus/yamuna_samvit_siddhi_gretil.txt
   13,016  data/sources/sanskrit/vedanta/full_corpus/yamuna_stotra_ratna_gretil.txt
  266,700  data/sources/sanskrit/vedanta/gretil_bhg4comm_ch2.txt
  273,944  data/sources/sanskrit/vedanta/gretil_bhg4comm_ch2_RAW.htm
2,853,356  data/sources/sanskrit/vedanta/jayatirtha_nyaya_sudha.txt
  558,459  data/sources/sanskrit/vedanta/madhva_gita_bhasya.txt
  812,269  data/sources/sanskrit/vedanta/madhva_mahabharata_tatparya.txt
  716,463  data/sources/sanskrit/vedanta/madhva_srimadhvyasa_RAW.htm
  464,403  data/sources/sanskrit/vedanta/ramanuja_gita_bhasya.txt
  146,681  data/sources/sanskrit/vedanta/ramanuja_vedartha_sangraha.txt
   47,406  data/sources/sanskrit/vedanta/sankara_school_saundaryalahari.txt
1,125,765  data/sources/sanskrit/vedanta/shankara_brahma_sutra_bhasya.txt
  528,137  data/sources/sanskrit/vedanta/shankara_gita_bhasya.txt
  547,285  data/sources/sanskrit/vedanta/shankara_gita_bhasya_RAW.htm
1,166,684  data/sources/sanskrit/vedanta/vacaspati_bhamati.txt
   64,088  data/sources/sanskrit/vedic/aitareya_upanisad_gretil.txt
  960,720  data/sources/sanskrit/vedic/brhadaranyaka_upanisad_gretil.txt
  595,524  data/sources/sanskrit/vedic/chandogya_upanisad_gretil.txt
   26,510  data/sources/sanskrit/vedic/isa_upanisad_gretil.txt
   20,418  data/sources/sanskrit/vedic/kathopanisad_gretil.txt
  184,367  data/sources/sanskrit/vedic/mandukya_upanisad_gretil.txt
   81,103  data/sources/sanskrit/vedic/prasna_upanisad_sankara_bhasya_gretil.txt
1,494,070  data/sources/sanskrit/vedic/rigveda_aufrecht_gretil.txt
   20,388  data/sources/sanskrit/vedic/svetasvatara_upanisad_gretil.txt
  156,240  data/sources/sanskrit/vedic/taittiriya_upanisad_gretil.txt
```