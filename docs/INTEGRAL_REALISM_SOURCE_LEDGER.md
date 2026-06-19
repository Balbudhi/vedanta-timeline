# Integral Realism Source Ledger

Created: 2026-06-18

This ledger separates three things that were mixed together in the voice notes:

- what is already in the public `vedanta-timeline` corpus,
- what is already held in the private secondary corpus at `/Users/eeshan/Dev/parishishta`,
- what still needs acquisition, rights review, or page-specific extraction.

It is not a publication artifact. It is a working acquisition and source-control document for the Integral Realism project.

## Rights Rule

Do not mirror modern copyrighted books into the public repo merely because a scan is visible on the web. Use this routing:

- Public repo: public-domain primary texts, permissively licensed files, project-authored notes, and metadata for open-web sources.
- Private secondary repo: copyrighted scholarship or modern editions used for research, with provenance and non-public status.
- Library/purchase ledger: works not yet held, or works whose access is controlled by publisher, library, or borrow-only scans.
- Site prose: only page-specific paraphrase or short compliant quotation, with exact source evidence.

## Public Repo Coverage

| Figure / corpus | Current public status | Gaps |
|---|---|---|
| Sri Aurobindo | `data/thinkers/aurobindo.json`, `data/articles/source/aurobindo.md`, and `data/sources/english/aurobindo/the-future-poetry.txt` exist. | Main works are not physically mirrored: *The Life Divine*, *The Synthesis of Yoga*, *The Secret of the Veda*, *Essays on the Gita*, Upanishad writings, *Record of Yoga*. Official CWSA web/PDF access exists, but edition rights must be treated as controlled by the Sri Aurobindo Ashram Trust unless separately cleared. |
| Haridas Chaudhuri | `data/thinkers/chaudhuri.json` and `data/articles/source/chaudhuri-banerji.md` exist. | No public raw source text should be added yet. Core works are modern copyrighted books. |
| Debashish Banerji | `data/thinkers/banerji.json` and `data/articles/source/chaudhuri-banerji.md` exist. | Books are modern copyrighted. Several articles are open-access candidates for public bibliography/source metadata. |
| Swami Medhananda / Ayon Maharaj | `data/thinkers/medhananda.json` and `data/articles/source/medhananda.md` exist. | OUP books are copyrighted. Open articles should be indexed and possibly excerpted/paraphrased with source-specific care. |
| Ramakrishna / Sarada Devi / Vivekananda | Vivekananda Complete Works vols. 1-9 exist under `data/sources/english/vivekananda_complete_works/`. `data/articles/source/vivekananda-ramakrishna.md` exists. | Ramakrishna and Sarada source files are absent. Need rights review for the web editions of the *Gospel of Sri Ramakrishna*, Kathamrita, and Holy Mother sources. |
| Ramana Maharshi | `data/thinkers/ramana.json` and `data/sources/sanskrit/vedanta/ramana_upadesa_saram.txt` exist. | English editions and talks are official/open-web but modern copyrighted by edition. Use metadata or private excerpts until rights are clear. |
| Satchidanandendra Saraswati | `data/thinkers/satchidanandendra.json` exists. | No raw corpus in public repo. Adhyatma Prakasha Karyalaya hosts PDFs/TOCs, but treat as controlled open access, not public domain. |
| Vijñānabhikṣu | `data/thinkers/vijnanabhiksu.json`, related articles, and some translations exist. | Need physical source reconciliation for *Sāṅkhya-Pravacana-Bhāṣya*, *Yoga-Vārttika*, and *Vijñānāmṛta-Bhāṣya*. Public-domain Sanskrit/older editions appear obtainable, but they are not yet normalized into this corpus. |
| Kashmir Śaiva / Trika | Several Sanskrit files exist under `data/sources/sanskrit/kashmir_shaiva/`. | Need stronger mapping of source status to actual files and missing IPVV, Locana, Abhinava-Bhāratī, Śiva-Dṛṣṭi, Jayaratha, and related commentaries. |
| Mīmāṃsā | Jaimini, Śabara, Kumārila-related materials exist under `data/sources/sanskrit/comparator/` and `data/sources/sanskrit/mimamsa/`. | Prabhākara, Pārthasārathi, Śālikanātha, Khaṇḍadeva, Apadeva, Laugākṣi Bhāskara, and Clooney secondary material are still not integrated. |

## Private Corpus Coverage

The private secondary repo `/Users/eeshan/Dev/parishishta` was pulled on 2026-06-18 and was already up to date.

Already held there:

| Work | Private status |
|---|---|
| Haridas Chaudhuri, *The Philosophy of Integralism* | OCR text exists at `materials/chaudhuri/chaudhuri_1954_philosophy_of_integralism.txt`, sourced from Internet Archive DLI item `dli.ernet.425542`; marked private/non-published use. |
| Haridas Chaudhuri and Frederic Spiegelberg, eds., *The Integral Philosophy of Sri Aurobindo: A Commemorative Symposium* | OCR text exists at `materials/chaudhuri/chaudhuri_1960_integral_philosophy_aurobindo_symposium.txt`, sourced from Internet Archive DLI item `dli.ernet.528659`; marked private/non-published use. |
| Debashish Banerji, *The Alternate Nation of Abanindranath Tagore* | PDF and OCR text exist under `materials/banerji/`; private secondary use. |
| Debashish Banerji, *Seven Quartets of Becoming* | PDF and OCR text exist under `materials/banerji/`; private secondary use. |
| Benedikt Paul Göcke and Swami Medhananda, eds., *Panentheism in Indian and Western Thought* | Listed under `materials/medhananda/`; verify that the file is the actual PDF and not a pointer or partial placeholder before relying on it. |
| Arindam Chakrabarti, *Realisms Interlinked* and "Against Immaculate Perception" | Held under `materials/chakrabarti/`; useful for realism grammar, not primary evidence for the Indian figures. |

Important correction: Chaudhuri's two highest-priority works are no longer "not found." They are found in the private corpus, but they should not be published into the public source tree.

## Highest Priority Acquisition / Extraction

| Priority | Item | Current status | Destination | Why it matters |
|---|---|---|---|---|
| P0 | Chaudhuri, *The Philosophy of Integralism* | Held privately as OCR. | Private extraction notes, then public paraphrase with citations. | Direct precedent for "integralism" and pūrṇa/integral Advaita around Aurobindo. |
| P0 | Chaudhuri/Spiegelberg, *The Integral Philosophy of Sri Aurobindo* | Held privately as OCR. | Private extraction notes, then public paraphrase with citations. | Helps separate Chaudhuri's own thesis from a wider 1960 symposium reception. |
| P0 | Banerji, "Vedantic Basis and Praxis of the Integral Advaita of Sri Aurobindo" | Open access at Loyola Marymount Digital Commons. | Public bibliography/source candidate. | Directly names Integral Advaita and maps Aurobindo through Vedanta, Yoga, and Tantra. |
| P0 | Banerji, "Sri Aurobindo's Formulations of the Integral Yoga" | Open access at CIIS Digital Commons. | Public bibliography/source candidate. | Bridges Aurobindo's diary/yoga structure to later integral formulations. |
| P0 | Banerji, SABDA August 2025 essay/review passage on Upaniṣads, yugas, and "heliocentric age" | Located in SABDA August 2025 PDF; not yet represented in local corpus. | Public metadata and extraction note; acquire source context. | Corrects the earlier miss: Banerji explicitly uses heliocentric language for Sri Aurobindo's yuga/time-structure. |
| P0 | Sri Aurobindo, *The Secret of the Veda* | Official web/PDF access via Ashram-related CWSA sites; rights controlled by edition. | Public metadata; private or controlled excerpting until rights decision. | The user explicitly clarified this as the intended "Secret of the Veda" source. Needed for Veda/Mīmāṃsā/Aurobindo symbolic reading. |
| P0 | Sri Aurobindo, *The Life Divine* | Official web/PDF access exists; rights controlled by edition. | Public metadata; private extraction notes. | Core source for Realistic Advaita, evolution, involution, Supermind, and manifestation. |
| P0 | Sri Aurobindo, *The Synthesis of Yoga* | Official web/PDF access exists; rights controlled by edition. | Public metadata; private extraction notes. | Needed for practice grammar across jñāna, bhakti, karma, and integral transformation. |
| P0 | Sri Aurobindo, *Essays on the Gita* | Official/open web access exists; rights controlled by edition. | Public metadata; private extraction notes. | Needed for integral reading of action, surrender, and multiple yogas. |
| P0 | Medhananda, *Infinite Paths to Infinite Reality* | Copyrighted OUP book; not in public corpus. | Purchase/library/private secondary. | Core modern reconstruction of Ramakrishna's Vijñāna Vedanta and plural manifestation. |
| P0 | Medhananda, *Swami Vivekananda's Vedāntic Cosmopolitanism* | Copyrighted OUP book; not in public corpus. | Purchase/library/private secondary. | Needed for Vivekananda as systematic philosopher rather than flattened "Neo-Vedanta." |
| P0 | Medhananda, "Cutting the Knot of the World Problem" | Open access MDPI article. | Public bibliography/source candidate. | Useful for Ramakrishna, world-realism, manifestationism, and Aurobindo comparison. |
| P0 | Ramakrishna, *Kathamrita* / *Gospel of Sri Ramakrishna* | Public web versions exist; edition rights need review. | Rights-reviewed public or private source notes. | Needed for roof/stairs, vijñāna, servant/part/identity modes, form/formless, and `yata mat tata path`. |
| P0 | Sarada Devi source corpus | Public web excerpts and affiliated sources exist; edition rights need review. | Rights-reviewed public or private source notes. | Needed for world-as-one's-own, universal motherhood, grace, and embodied non-duality. |
| P0 | Satchidanandendra, *The Method of the Vedanta* / related APK texts | Free-hosted and IA scans exist; rights controlled by editions. | Private source notes or public metadata after rights check. | Needed for `adhyāsa`, mūlāvidyā criticism, and the ill-posed locus/origin question for avidyā. |
| P0 | Vijñānabhikṣu, *Sāṅkhya-Pravacana-Bhāṣya* | Older Sanskrit editions and scans found online. | Public-domain candidate after edition review. | Needed for cross-darśana synthesis and avibhāgādvaita / bhedābheda evidence. |
| P1 | Banerji, *Meditations on the Isha Upanishad* | Copyrighted; not yet held. | Purchase/library/private secondary. | Needed for Aurobindo + Isha-specific philosophical reading. |
| P1 | Banerji, *Integral Yoga Psychology* | Copyrighted; not yet held. | Purchase/library/private secondary. | Needed for psychology/metaphysics/transformation vocabulary. |
| P1 | Banerji, *Time-Steps of the Cosmic Horse: The Contemplative Philosophy of the Great Forest (Bṛhadāraṇyaka) Upaniṣad* | 2024 Nalanda International / D. K. Printworld book; not found in `parishishta`. | Purchase/library/private secondary. | Likely important for the cosmological/time-step model and Banerji's Veda-Upaniṣad-Aurobindo synthesis. |
| P1 | Chaudhuri, *Integral Yoga: A Concept of Harmonious and Creative Living* | Copyrighted; no verified local copy. | Purchase/library/private secondary. | Practical/ethical extension of integralism. |
| P1 | Chaudhuri, *Being, Evolution, and Immortality* | Copyrighted; IA borrow scan exists. | Library/private secondary. | Helps with evolution/immortality side of the integral thesis. |
| P1 | Timalsina, key Tantra/Sarvāmnāya writings | Bibliography exists; most are copyrighted articles/books or course materials. | Public metadata plus private extraction notes. | Needed for Śaiva-Śākta/Sarvāmnāya grammar and not-Advaita-only integration. |

## Open-Web Candidates

These can probably be represented publicly as metadata, links, and limited paraphrase. Do not bulk mirror without checking each license or site policy.

| Work | Source |
|---|---|
| Debashish Banerji, SABDA August 2025 passage on Sri Aurobindo, yugas, and "heliocentric age" | `https://www.sabda.in/pdf/news/aug2025.pdf` |
| Debashish Banerji, "Vedantic Basis and Praxis of the Integral Advaita of Sri Aurobindo" | `https://digitalcommons.lmu.edu/monsoon-sasa-journal/vol1/iss1/4/` |
| Debashish Banerji, "Sri Aurobindo's Formulations of the Integral Yoga" | `https://digitalcommons.ciis.edu/ijts-transpersonalstudies/vol37/iss1/6/` |
| Debashish Banerji, "Building an Intuitive Mentality" | `https://www.primescholars.com/articles/building-an-intuitive-mentality-the-neovedantic-knowledge-project-of-sri-aurobindo-104283.html` |
| Debashish Banerji, "Individuation, Cosmogenesis and Technology" | `https://integral-review.org/individuation-cosmogenesis-and-technology-sri-aurobindo-and-gilbert-simondon/` |
| Swami Medhananda, "Cutting the Knot of the World Problem" | `https://www.mdpi.com/2077-1444/12/9/765` |
| Sthaneshwar Timalsina / Vimarsha Foundation official bio and tradition pages | `https://www.vimarshafoundation.org/about-us`, `https://www.vimarshafoundation.org/tradition`, `https://www.vimarshafoundation.org/writings` |
| Sri Aurobindo official writings index | `https://www.sriaurobindoashram.org/sriaurobindo/writings.php` |
| Ramakrishna/Vivekananda affiliated text portal | `https://www.ramakrishnavivekananda.info/` |
| Adhyatma Prakasha Karyalaya texts | `https://adhyatmaprakasha.org/` |
| Ramanasramam official books | `https://www.gururamana.org/` |

## Name And Transcript Corrections

| Transcript / uncertain form | Working correction | Confidence |
|---|---|---|
| Haidash Chaudhary / Haridasa Shradhu | Haridas Chaudhuri | High |
| Devashishpaner / Debendranath Banerjee | Debashish Banerji | High, unless a separate figure is later intended |
| Sukira of the Vedas | Sri Aurobindo, *The Secret of the Veda* | High after user clarification |
| Gandha Bhikshu | Vijñānabhikṣu | High after user clarification |
| Acharya Staneshwar Tumulsena | Sthaneshwar Timalsina | High for Timalsina; `Tumulsena` spelling unverified |
| Sarvam Nyayam | Sarvāmnāya | High as a correction, but do not publish until source-cited |
| Satchidananda Saraswati | Satchidanandendra Saraswati | High after user clarification |
| civil novel | Unknown | Unresolved |

## Immediate Work Order

1. Extract page-specific notes from Chaudhuri's two private OCR texts.
2. Add public metadata entries for the open Banerji and Medhananda articles.
3. Rights-review Aurobindo CWSA text ingestion before mirroring anything beyond `the-future-poetry.txt`.
4. Decide whether Ramakrishna/Sarada public-web texts can be mirrored, or whether the site should use metadata plus page-specific notes.
5. Reconcile `source_status` values against actual files for Aurobindo, Ramana, Satchidanandendra, Vijñānabhikṣu, Trika, and Mīmāṃsā.
6. Build extraction packets by claim, not by author: `vijñāna`, `māyā/avidyā`, `form/formless`, `identity/modality`, `ritual-symbolic process`, `realist difference`, `manifestation`, `initiation/adhikāra`.
7. Build a dedicated `geocentric / heliocentric / third-centering` packet from Banerji's SABDA 2025 passage, Sri Aurobindo's CWSA 18 pp. 263-264, *The Human Cycle* pp. 7-14, Chaudhuri's "Ego-Centric and Cosmo-Centric Individuality" section in *The Philosophy of Integralism*, and any fuller Banerji book passages found after acquisition.
