# GRETIL — Göttingen Register of Electronic Texts in Indian Languages

**Source:** https://gretil.sub.uni-goettingen.de/gretil.html
**Bulk Sanskrit zip:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr.zip
**License:** GRETIL itself does not surface a single licence statement on
the front page or via `LICENSE.txt`; the site explicitly offers per-language
bulk-download zips (Sanskrit, Pali, Prakrit, NIA, Dravidian, Old Javanese,
Tibetan, secondary resources), and individual texts retain the encoders'
own attribution headers. The de-facto policy is "usage permitted with
attribution to GRETIL and the original encoder"; redistribution of derived
work should preserve those headers.

Contact for explicit licensing: `gretil@sub.uni-goettingen.de`.

## Fetch record

- Fetched: 2026-05-19 23:34 UTC by corpus-chat-lane2.
- Method: `curl -fsSL https://gretil.sub.uni-goettingen.de/gretil/1_sanskr.zip`.
- File: `1_sanskr.zip`, size **295 862 698 bytes (≈282 MB)**.
- SHA-256 (recorded in `1_sanskr.zip.sha256`):
  `ae0cbaed61c874173fdabd7b0d7773d4fd095a40e1c0d04682764ce053e3aaf4`.
- Unpacked into `1_sanskr/` — **3 741 files, 1.14 GB on disk**.

The zip and the unpacked tree are *not* committed (excluded via
`.gitignore` at worktree root). They live on `/nas` next to this README.

## Tree shape (top-level subdirs under `1_sanskr/`)

| Subdir         | Size | Content                                                  |
|----------------|-----:|----------------------------------------------------------|
| `1_veda/`      |  15M | Saṃhitā / Brāhmaṇa / Āraṇyaka / Upaniṣad corpus.         |
| `2_epic/`      |  34M | Mahābhārata, Rāmāyaṇa, Harivaṃśa.                        |
| `3_purana/`    |  23M | Mahā- and Upa-Purāṇas.                                   |
| `4_rellit/`    |  33M | Religious literature (Jaina, Śaiva, Vaiṣṇava, Buddhist). |
| `5_poetry/`    |  30M | Kāvya, alaṃkāra, drama.                                  |
| `6_sastra/`    |  57M | Śāstra: grammar, lexicography, philosophy, dharma, jyotiṣa, … |
| `7_fromindonesia/` | 117K | Sanskrit excerpts from Indonesian Jaina-Buddhist literature. |
| `tei/`         | 371M | GRETIL's TEI-XML edition of selected works + plain-text and HTML transformations. |

## 30 priority Sanskrit primaries (already on disk; relative paths inside `1_sanskr/`)

Most of these are in the standard `*u.htm` (Unicode IAST/Devanāgarī) form;
where a paired `*p` exists it is the Padapāṭha. The 30 picks below
cover the spine the prakriya pipeline + the vedanta-timeline site need
and that are *not* already in `vedanta-timeline/data/sources/sanskrit/`.

### Vyākaraṇa (Pāṇini grammar tradition)

1. `6_sastra/1_gram/panini_u.htm` — Aṣṭādhyāyī (177 KB) [witness B for prakriya]
2. `6_sastra/1_gram/varlghku.htm` — Laghu-Siddhānta-Kaumudī (267 KB)
3. `6_sastra/1_gram/paribhsu.htm` — Paribhāṣenduśekhara (169 KB)
4. `6_sastra/1_gram/pmbh_1su.htm` — Patañjali Mahābhāṣya, Paspaśāhnika sample (1.9 MB)
5. `6_sastra/1_gram/pmbhassu.htm` — Patañjali Mahābhāṣya, full (6.4 MB)
6. `6_sastra/1_gram/vakyp1au.htm` — Bhartṛhari Vākyapadīya kāṇḍa 1 (295 KB)

### Mīmāṃsā

7. `6_sastra/3_phil/mimamsa/jaimsutu.htm` — Jaimini-Sūtra (202 KB)
8. `6_sastra/3_phil/mimamsa/mimslovu.htm` — Kumārila Ślokavārttika (468 KB)
9. `6_sastra/3_phil/mimamsa/sabbha1u.htm` — Śabara-Bhāṣya book 1 (48 KB)

### Nyāya

10. `6_sastra/3_phil/nyaya/nystik_u.htm` — Nyāya-Sūtra w/ vārttika (1.4 MB)
11. `6_sastra/3_phil/nyaya/nysu51au.htm` — Nyāya-Sūtra adhikaraṇa 5.1 (34 KB)
12. `6_sastra/3_phil/nyaya/udnyku1u.htm` — Udayana Nyāya-Kusumāñjali (52 KB)
13. `6_sastra/3_phil/nyaya/nvtp1_1u.htm` — Vācaspati Nyāyavārttika-Tātparya-Ṭīkā (634 KB)

### Vaiśeṣika / Sāṃkhya / Yoga

14. `6_sastra/3_phil/vaisesik/vaisessu.htm` — Vaiśeṣika-Sūtra (31 KB)
15. `6_sastra/3_phil/samkhya/iskar_u.htm` — Īśvarakṛṣṇa Sāṃkhya-Kārikā (16 KB)
16. `6_sastra/3_phil/samkhya/samkhsuu.htm` — Sāṃkhya-Sūtra (67 KB)
17. `6_sastra/3_phil/yoga/patyog_u.htm` — Pātañjala-Yoga-Sūtra (19 KB)
18. `6_sastra/3_phil/yoga/yogsubhu.htm` — Vyāsa Yoga-Bhāṣya (212 KB)

### Vedānta

19. `6_sastra/3_phil/vedanta/brahms2u.htm` — Brahma-Sūtra (35 KB)
20. `6_sastra/3_phil/vedanta/brahmsuu.htm` — Brahma-Sūtra alt (35 KB)
21. `6_sastra/3_phil/vedanta/bbdip11u.htm` — Madhva Brahma-Sūtra commentary I (376 KB)
22. `6_sastra/3_phil/vedanta/bhgsbh_u.htm` — Bhagavad-Gītā-Bhāṣya (Śaṅkara) (540 KB)
23. `6_sastra/3_phil/advaita/motik_pu.htm` — Maṇḍana Brahmasiddhi commentary (1.5 MB)

### Buddhist Sanskrit

24. `6_sastra/3_phil/buddh/asabhs_u.htm` — Asaṅga Abhidharmasamuccaya-Bhāṣya (231 KB)
25. `tei/sa_nAgArjuna-mUlamadhyamakakArikA.xml` — Nāgārjuna MMK (TEI)
26. `tei/sa_nAgArjuna-vigrahavyAvartanI.xml` — Nāgārjuna Vigraha-Vyāvartanī (TEI)
27. `tei/sa_madhyamakAvatAra-1-5.xml` — Candrakīrti Madhyamakāvatāra ch. 1-5 (TEI)

### Kashmir Śaiva

28. `6_sastra/3_phil/saiva/abhmal1u.htm` — Abhinavagupta Mālinīvijaya-vārttika I (153 KB)
29. `6_sastra/3_phil/saiva/tantralu.htm` — Abhinavagupta Tantrāloka (906 KB)
30. `tei/sa_abhinavagupta-IzvarapratyabhijJAvimarzinI.xml` — Abhinavagupta Īśvara-Pratyabhijñā-Vimarśinī (TEI)

### Vedic (high-volume, register-only — file sizes are MB-class)

- `1_veda/1_sam/1_rv/rv_hn01u.htm` — Rigveda Maṇḍala 1 Saṃhitāpāṭha (337 KB)
- `1_veda/1_sam/1_rv/rvpp_01u.htm` — Rigveda Maṇḍala 1 Padapāṭha (396 KB)
- `1_veda/1_sam/avs___u.htm` — Atharvaveda Śaunaka (1.0 MB)

(Lane 1's Sanskrit-primaries worktree should **not** re-download these
GRETIL files — the bulk zip already covers the entire site as of
2020-09-15; subsequent updates are incremental.)

## What the prakriya pipeline should consume next

1. `panini_u.htm` is the primary Witness B against the
   SanskritDocuments HTML already in `prakriya/sources/panini/`. Run a
   line-level diff and store divergence pairs as the manuscript-control
   record.
2. `pmbhassu.htm` (full Mahābhāṣya) is the highest-leverage commentary
   layer; ingest as plain text into the `commentarial_validation_corpus`.
3. `varlghku.htm` is the pedagogical fall-back when the Mahābhāṣya is
   silent — the example-rich later derivations.
4. The `tei/` subdirectory's XML files carry encoded apparatus structure
   that maps cleanly onto the prakriya engine's witness-tier abstraction;
   prefer TEI over the `*u.htm` form where both exist.
