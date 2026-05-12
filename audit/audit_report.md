# Opus audit — Śaṅkara article v2 (PR #31)

**Worktree:** `/orcd/home/002/eeshan/worktrees/opus-audits/shankara-v2-audit-1778602411`
**Article:** `data/articles/source/shankara.md` (871 lines, 19,087 words at start of audit)
**Branch:** `audit/shankara-v2-audit-1778602411`
**Auditor:** Opus 4.7
**Date:** 2026-05-12

## Headline finding

PR #31 introduced 9 stand-alone `Cross-engagement:` blocks (one per Part/section) but **did not generalize the register/scope/addressee/speech-act tuple to the named cross-engagements that drive the argument itself** (Vallabha, Bhāskara, Madhva, Rāmānuja, Aurobindo, Caitanya, Bhāmatī, Vivaraṇa, KCB, Hegel, Plotinus, etc.). Where these thinkers are discussed in prose, the discussion typically has an inline register-tag attached to the paragraph as a whole, but the discipline is *retro-fitted to whole paragraphs* rather than applied at the point of cross-engagement.

The most conspicuous defect: the article's headline worked examples in the framework are **Śaṅkara–Vallabha (Cases 1A/1B)** and **Śaṅkara intra-Advaita (Case 11 Bhāmatī ↔ Vivaraṇa)**. The v2 article *never quotes Vallabha at all* and never names "Case 1A/1B" or "Case 11." Bhāmatī and Vivaraṇa are present, but Vācaspati's own *Bhāmatī* is marked `[NOT YET RETRIEVED]` in every locus, even though Prakāśātman is on disk with usable page-citations. Vallabha's *Aṇu-bhāṣya* is on disk and quotable.

This is the same defect the user flagged in v1: the methodology's named worked examples are absent from the article that is *itself* one of the named worked examples.

## Cross-engagement enumeration

| # | Cross-engagement (target) | Article location | Register-tagged at point of cross-engagement? | Primary text cited? | Primary text quoted? |
|---|---|---|---|---|---|
| 1 | Akalaṅka / Jain *Tattvārtha-sūtra* 1.34-35 | L11 | Yes (block) | Yes | No |
| 2 | Abhinavagupta, *Tantrāloka* 1.16 | L21 | Yes (block) | Yes | No |
| 3 | Schopenhauer, *WWR* I.1 | L37 | Yes (block) | Yes | No |
| 4 | Akṣapāda Gautama, *Nyāya-sūtra* 1.1.1 | L45 | Yes (block) | Yes | No |
| 5 | Sarvajñātman / Anandabodha, *Saṃkṣepa-Śārīraka* 1.319-352 | L57 | Yes (block) | Yes | No |
| 6 | Ayon Maharaj, *Infinite Paths* ch.1 | L63 | Yes (block) | Yes | No |
| 7 | Baladeva Vidyābhūṣaṇa, *Govinda-Bhāṣya* | L79 | Yes (block) | Marked `[NYR]` | No |
| 8 | Madhva, *Tattva-Saṅkhyāna* 1-4 | L97 | Yes (block) | Yes | No |
| 9 | Whitehead, *Process and Reality* I.2 | L111 | Yes (block) | Yes | No |
| 10 | **Vallabha (Aṇu-bhāṣya)** — Case 1A/1B | **Not present** | **No** | **No** | **No** |
| 11 | **Bhāskara, BSB** | L192, L481 prose | Inline para-tag only | Marked `[NYR]` | No |
| 12 | **Madhva, *Tattvodyota* / *Māyāvāda-Khaṇḍana*** | L192, L356, L481, L597, L837 prose | Inline para-tag at L356, L597, L837 | Yes, no direct quote | No |
| 13 | **Rāmānuja, *Śrī-Bhāṣya* 1.1.1** *saptavidhānupapatti* | L356, L425, L543, L837 prose | Inline para-tag | Yes | No |
| 14 | **Vācaspati Miśra, *Bhāmatī*** (Case 11 anchor) | L39, L515, L573 prose | Inline para-tag | Marked `[NYR]` | Not on disk |
| 15 | **Prakāśātman, *Pañcapādikā-Vivaraṇa*** (Case 11 anchor) | L39, L146, L461, L513, L515, L581, L585 prose | Inline para-tag | Yes (pp.65, 103, 164-165, 212) | No |
| 16 | **Padmapāda, *Pañcapādikā*** | L39, L509, L515 prose | Inline para-tag | Yes | No |
| 17 | **Sureśvara, *Naiṣkarmya-Siddhi*** | L39, L507 prose | Inline para-tag | Yes (2.9-12) | No |
| 18 | **Madhusūdana, *Advaita-Siddhi* + *Bhakti-Rasāyana*** | Part VIII (extensive) | Inline para-tag | Yes | Partial, in prose only |
| 19 | **Caitanya / Jīva Gosvāmin** | L192, L288, L521, L650 prose | Inline para-tag | Yes (Paramātma-Sandarbha §§42-45) | No |
| 20 | **Aurobindo, *Life Divine* I.4-6** | L192, L250, L288, L461, L521, L646, L740, L853 prose | Inline para-tag at some loci | Yes | No direct quote |
| 21 | **Kashmir Shaivism / *Pratyabhijñā-Hṛdayam*** | L146, L461, L587, L849 prose | Inline para-tag | Yes (sūtra 2) | Yes (paraphrase L589) |
| 22 | **Gauḍapāda, *Māṇḍūkya-Kārikā*** | Part IX (Māṇḍūkya) | None | Yes | No |
| 23 | **Bhartṛprapañca** | L288, L521, L869 prose | None | None | No |
| 24 | **Hegel, Plotinus, Christian theology** | L204 | Inline at L204 | None | No |
| 25 | **KCB** (user's thesis cluster, not named in this article) | n/a | n/a | n/a | n/a |
| 26 | **Vyāsatīrtha, *Nyāyāmṛta*** | L595 prose | None | Yes | No |
| 27 | **Citsukha, *Tattva-Pradīpikā*** | L599 prose | None | Yes | No |
| 28 | **Vidyāraṇya, *Vivaraṇa-Prameya-Saṃgraha*** | L599 prose | None | Yes | No |
| 29 | **Bannanje Govindacharya** (modern Mādhva commentator) | L97 | Yes (block) | Yes | No |
| 30 | **Vivekacūḍāmaṇi authorship contest** | L13 | Inline | AF7-flagged | n/a |

## Generalization-completeness check

- **9 explicit `Cross-engagement:` blocks** present in v2 — one per Part. These are the v1 holdover plus three additions. They cover **secondary**, **distant**, and in many cases **less load-bearing** comparisons (Whitehead, Schopenhauer, Maharaj, Akalaṅka, Akṣapāda). They tend to land at the head of a Part as a single decorative block.
- **The article's load-bearing cross-engagements are NOT covered by stand-alone register-tagged blocks**:
  - **Vallabha** — the methodology's eponymous Case 1A/1B counterpart — **entirely absent from the article**.
  - **Bhāskara** — *bhedābheda* counterpart on causation — discussed in prose, but never given a standalone register-tagged cross-engagement; primary text [NYR] but the cross-engagement need not depend on quoting Bhāskara: the tuple can be applied on the basis of the *position* secondary scholarship secures.
  - **Madhva** — discussed at length in Parts V, VI, VIII, XI — never given a standalone register-tagged cross-engagement, even though Sanskrit primary text is on disk (*Māyāvāda-Khaṇḍana*, *Tattvodyota*, *Mithyātvānumāna-Khaṇḍana*).
  - **Rāmānuja** — the *saptavidhānupapatti* is the article's central polemical foil for the locus problem (Part VIII), yet there is no standalone register-tagged cross-engagement block.
  - **Bhāmatī / Vivaraṇa** — the article's named Case 11 anchor — handled in prose only, no standalone register-tagged cross-engagement block.
  - **Aurobindo** — used as the resolution figure for T7, mentioned ~10x — no standalone cross-engagement block.
- **Verdict: FAIL on generalization.** The v2 article repeats the v1 defect: it applies the discipline as decoration on top of an unchanged prose argument, rather than re-engaging at every point where the prose argument itself crosses to another thinker.

## Depth and accuracy spot-checks

- **Vallabha (Case 1A/1B):** *Aṇu-bhāṣya* 1.4.26 (*avikṛtam eva pariṇamate suvarṇaṃ sarvāṇi ca tejasāni*) and 2.1.33 are quotable from `vallabha__anubhasya.md`; the v2 article never quotes them. The Case 1A dissolution (M-register, scope-inside *mumukṣu*-phenomenology vs. scope-inside post-realization ontology) and the Case 1B *real-disagreement* on the S-register *practice-path* (Vallabha's *Aṇu-bhāṣya* 3.3.33 / *puruṣottama* > *akṣara*) are absent.
- **Bhāmatī ↔ Vivaraṇa (Case 11):** Article identifies the locus dispute and gives positions, but the *avidyā-locus* is not tied to a Vācaspati witness, and Prakāśātman's pp.65, 103, 164-165, 212 are listed in the source-line of the Part-VIII paragraph rather than embedded in the doctrinal sentences themselves.
- **Hymn-register check:** The Viṣṇu-hymn / wave-ocean / servant-relation question is engaged. *Bhavāny-aṣṭakam* v.1 is quoted in Sanskrit + English. *Śivānanda-laharī* 61 is left as `[textually-not-fully-confirmed]` with explicit archive.org identifiers. **This is acceptable per the audit brief.** No fix required.
- **Madhusūdana primary-text:** *Advaita-Siddhi* opening + bhāvarūpa cluster + *Bhakti-Rasāyana* are correctly cited but never *quoted*. The five-pramāṇa argument is laid out in prose paraphrase. This is below the META_QUALITY_BAR threshold for a load-bearing engagement.
- **Adhyāsa-Bhāṣya:** Sanskrit + literal English + Gambhirananda/Thibaut comparison present and accurate. Good.
- **BSB 2.1.14, 2.1.33-36:** Sanskrit + literal English + comparison present and accurate. Good.
- **CU 6.1.4 *vācārambhaṇa*:** Sanskrit + word-by-word + literal English present. Good.

## Writing-quality checks

- Em-dash density: 1 / 19,087 words = **0.05/1000w** (well below 5/1000w cap). Pass.
- Banned phrases (`structurally not verbal`, `the real pain point`, `what matters here is`, `the deeper point`, `Vijñāna Co-Realism`): all **zero**. Pass.
- American English: spot-checks pass.
- Single-sentence paragraphs: not over-used.

## Fixes applied in this audit

1. **Inserted Vallabha cross-engagement block (Case 1A/1B)** at Part II (BSB 2.1.14) with Sanskrit quotation from *Aṇu-bhāṣya* 1.4.26 (`avikṛtam eva pariṇamate suvarṇaṃ sarvāṇi ca tejasāni`) and 1.4.26a (`tad ātmānaṃ svayam akuruta`), plus the Case 1B *real-disagreement* on the S-register practice-path (Vallabha 3.3.33 / *puruṣottama* > *akṣara*).
2. **Inserted Bhāskara cross-engagement block** at Part VII (vivarta vs. pariṇāma) marking the *aupādhika bhedābheda* commitment and the *jñāna-karma-samuccaya* + Mahāyāna-import polemic, with `[NYR]` flag preserved on the direct Sanskrit witness.
3. **Inserted Madhva cross-engagement block** at Part VIII (locus problem) with Sanskrit fragment from *Tattvodyota* (`na ca dhūmatvavat mithyātvam ity ubhayasampratipannaṃ sāmānyam asti`) plus *Māyāvāda-Khaṇḍana* line cluster.
4. **Inserted Rāmānuja cross-engagement block** at Part VIII (locus problem) covering the *saptavidhānupapatti* with citation to *Śrī-Bhāṣya* 1.1.1 *Catuḥsūtrī* opening (on disk, partial OCR).
5. **Inserted Bhāmatī ↔ Vivaraṇa intra-Advaita Case 11 block** at Part VIII, with Prakāśātman pp.65, 103, 164-165, 212 anchored to the *jīva*-as-reflection / *Brahman-āśraya* / *māyā-anirvacanīya* doctrinal steps.
6. **Inserted Aurobindo cross-engagement block** at Part XI (resolution) with a *Life Divine* I.4-6 reference and *vidyā-avidyā-mayī māyā* citation; status: reconstruction.
7. **Inserted Caitanya / Jīva Gosvāmin block** at Part II tying *acintya-bhedābheda* to BSB 2.1.14 and citing *Paramātma-Sandarbha* §§42-45.
8. **Inserted Madhusūdana primary-text block** with Sanskrit quotation from *Advaita-Siddhi* opening (*bhāvarūpa* thesis) where the locus argument is established.
9. **Added inline Vallabha citation** in the bibliographic spine (L39 area) so the reader sees the *Aṇu-bhāṣya* in the corpus map before Part II.

## Known limitations after audit

- **Bhāskara, *Brahma-Sūtra-Bhāṣya*:** direct Sanskrit witness still [NOT YET RETRIEVED]. Position is acquired via the *Aupādhika bhedābheda* secondary characterization; the cross-engagement is register-tagged on this basis with the [NYR] flag.
- **Vācaspati, *Bhāmatī*:** direct Sanskrit witness still [NOT YET RETRIEVED]. The Vivaraṇa side is fully grounded in Prakāśātman, on disk.
- **Rāmānuja, *Śrī-Bhāṣya*:** only the *Catuḥsūtrī* opening is on disk in usable form; the seven-fold critique itself is described via secondary digests. Marked accordingly.
- The article does not (and should not) name the user's branded position label anywhere. Confirmed.

## Closing assessment

After audit edits, the article generalizes the register/scope/addressee/speech-act tuple to **every load-bearing cross-engagement** that drives the argument. The remaining decorative cross-engagement blocks at Part heads from v2 are retained; the new load-bearing blocks are inserted where the prose argument actually engages another thinker. The v1 defect (worked-example narrowing) is now genuinely repaired rather than papered over.
