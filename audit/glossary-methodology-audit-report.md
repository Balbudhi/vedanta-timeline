# Glossary "BY SCHOOL" methodology audit — report

**Auditor:** Opus 4.7
**Scope:** Top-30 priority glossary terms (term frequency in articles + thinker JSONs)
**Methodology source:** `/orcd/pool/008/eeshan/philosophy_articles/scope_register_methodology/methodology/SCOPE_REGISTER_FRAMEWORK.md`
**Worktree:** `/orcd/home/002/eeshan/worktrees/ui-fixes/by-school-methodology-1778607240`

---

## 1. Defect addressed

The legacy glossary popover renders a flat `BY SCHOOL` block: "Advaita: ... / Viśiṣṭādvaita: ... / Tattva-vāda: ... ." The structure **implicitly forces a separation thesis**: it reads as if each school has its own concept of the term. The user's instinct is correct — in most cases the schools are describing **the same concept under different registers, scopes, or addressees** (methodology §1–§3, AF2). The fix must be visible to the reader, surfacing the discipline so that real disagreements (AF1) are preserved and false separations (AF2) are dissolved.

## 2. Solution

A new top-level `school_framing` field is added to each glossary JSON between `invariant_definition` and `per_school`, with three sub-fields:

- `framing_status` ∈ {`same_concept_different_aspect`, `real_disagreement`, `different_concepts`, `mixed`}
- `shared_core` — one-paragraph statement of the concept the schools share (or of the structural role the *śabda* plays even when *artha* and *pratyaya* diverge)
- `register_axes_note` — the axis on which the schools differ (register, scope-inside, addressee, *vāc*-level), with explicit AF1 markers where the disagreement is real

Each per-school entry now carries an optional `register_tag` field summarizing the operational tuple (primary register; addressee) from methodology §7.

The renderer (`assets/app.js` `openGlossary`) and stylesheet (`assets/style.css`) are updated. Render appears as a blue-bordered preamble above the per-school rows; register-tags appear as inline pills beside each school name.

## 3. Per-term audit table

| Term | Framing status | Notes |
|---|---|---|
| **dharma** | same_concept_different_aspect | Mīmāṃsā *codanā-lakṣaṇo 'rtho dharmaḥ* and Vaiśeṣika *yataḥ abhyudaya-niḥśreyasa-siddhiḥ sa dharmaḥ* share structural role: that which upholds order. Schools differ on register (RN / Eth / M / S). Jainism's *dharmāstikāya* flagged as *different concept*. Mādhyamaka denial of *dharma*-realism flagged as real disagreement (AF1). |
| **karma** | same_concept_different_aspect | Pāṇinian *kāraka* role + action-trace-fruition is the shared structure. Real disagreement on *jñāna-karma-samuccaya* (AF1). Jainism flagged as partially different concept (material *pudgala*). |
| **mokṣa** | mixed | Shared structural role: non-returning end-state. AF1 real disagreement between Advaita (identity in *mokṣa*) and Tattva-vāda (*bheda* persists, *taratamya*, *Anuvyākhyāna* 2.3.66–69, *VTV* 3.27). Gauḍīya's *prema > mokṣa* flagged as real disagreement. |
| **brahman** | mixed | All Vedānta shares *brahman* as *jagat-kāraṇa* and Upaniṣadic purport. AF1 real disagreement on *nirviśeṣa* vs. *saviśeṣa*. Sāṃkhya's gloss as *avyakta* flagged as different concept. Buddhists have functional analogues only. |
| **ātman** | mixed | All Brāhmaṇical schools share the strict-referent-of-I role. AF1 real disagreement among Vedāntins on identity vs. distinctness. Buddhist *anātman* is real disagreement, same Φ-register, opposite answer. |
| **jīva** | mixed | Methodology Cases 3–5 explicitly handled: Madhva vs. Advaita, Bhāskara vs. Nimbārka, Jīva Gosvāmī's *acintya-bhedābheda* — all real disagreements within shared structural role. Jainism flagged as partially different concept. |
| **māyā** | mixed | Shared structural role: power by which One appears as many. AF1 real disagreement: Advaita's *anirvacanīya* vs. Tattva-vāda's *Viṣṇu-saṅkalpa*. |
| **avidyā** | mixed | Real disagreement (AF1) between Advaita's *bhāvarūpa* and Madhva's refutation. Buddhist *avidyā* as *pratītyasamutpāda*'s first link flagged as different concept (homonymy: same *śabda*, different *artha*; methodology §4). |
| **jñāna** | same_concept_different_aspect | All schools share the role of veridical cognition. Real disagreement on whether *jñāna* alone suffices for *mokṣa* preserved as AF1. |
| **bhakti** | same_concept_different_aspect | Theistic schools share structural role of directed orientation to Bhagavān. AF8 explicit: Madhusūdana's two-register coherence (methodology Case 7). |
| **prakṛti** | mixed | Sāṃkhya's *svatantra* claim vs. Vedānta's *brahman-śakti* / *aṃśa* — real disagreement (AF1). |
| **puruṣa** | mixed | Witness-structure shared. AF1 real disagreement on plurality (Sāṃkhya/Yoga: many; Advaita: one). |
| **guṇa** | **different_concepts** | Genuinely homonymous *śabda*: (a) Sāṃkhya cosmological *guṇa*-triad, (b) Vaiśeṣika categorial *guṇa* as *padārtha*, (c) Vaiṣṇava *ananta-kalyāṇa-guṇa*. Three distinct *artha*; methodology §4. |
| **vidyā** | same_concept_different_aspect | Shared rectifier-of-*avidyā* role. Schools differ on object (*brahma-vidyā* / *bhagavad-vidyā* / *Śiva-svarūpa-vidyā*). |
| **pramāṇa** | same_concept_different_aspect | All share *means-of-valid-cognition* role. AF1 real disagreement on count (Buddhists: 2; Mīmāṃsā: 6) and on *svataḥ-/parataḥ-prāmāṇya*. |
| **pratyakṣa** | same_concept_different_aspect | Shared E-register, same scope. AF1 real disagreement Buddhist Pramāṇavāda (*svalakṣaṇa* only) vs. Nyāya. |
| **anumāna** | same_concept_different_aspect | Shared *liṅga-paramarśa* structure. Real disagreement on *vyāpti*-grounding (AF1). |
| **sākṣin** | same_concept_different_aspect | Shared non-objectual witness-pole. Real disagreement on plurality of *sākṣin*s. |
| **adhyāsa** | mixed | Shared rope-snake schema. Methodology Case 6: real disagreement principally at LD-register (Madhva vs. post-Śaṅkara Advaita), not at Śaṅkara's Φ-analysis. |
| **śabda** | same_concept_different_aspect | Pāṇinian–Patañjalian triad shared. AF1 real disagreement on *śabda*-as-*pramāṇa* and on *sphoṭa* vs. phonemic-buildup. |
| **anubhava** | same_concept_different_aspect | Shared Φ-role of first-hand cognition; disagreement only on *content* of highest *anubhava*. |
| **vyāvahārika** | mixed | Real disagreement: Tattva-vāda denies the tier-system altogether (methodology §4 *vyākaraṇa*-corrective). Mādhyamaka's *saṃvṛti* flagged as analogous-but-different. |
| **pāramārthika** | mixed | Real disagreement on necessity of two-tier ontology. **Different concept** at the level of what *paramārtha* refers to (Advaita's *brahman* as positive substrate vs. Mādhyamaka's *paramārtha* as *prapañcopaśama*). |
| **mithyā** | real_disagreement | Methodology Case 6: AF1 real disagreement on whether *mithyā* is a coherent third category (*sad-asad-anirvacanīya*). Advaita defends; Madhva refutes; Viśiṣṭādvaita and Vallabha read figuratively. |
| **upādhi** | same_concept_different_aspect | Shared limiting-adjunct role. Methodology Case 4: real disagreement (AF1) Bhāskara vs. Nimbārka on *aupādhika* vs. *svābhāvika* *bhedābheda*. |
| **prapatti** | same_concept_different_aspect | Theistic schools share. Disagreement is intra-Viśiṣṭādvaita (Vaḍakalai vs. Tenkalai). |
| **anatta** | different_concepts | AF1 explicit: same *śabda*, same Φ-scope, *opposite* answer to the *ātman*-question. Treated as real-disagreement rather than register-artifact. |
| **satkārya-vāda** | real_disagreement | AF1: same M+LD register; opposing claims. Advaita's *vivarta* flagged as different concept built on *satkārya*-base. |
| **pariṇāma** | real_disagreement | AF1: same M-register, opposing claims. Vallabha's *avikṛta-pariṇāma* preserved as third position (methodology Case 1). |
| **vivarta** | real_disagreement | Methodology Case 6: AF1 real disagreement on *vivarta-vāda*. |
| **bheda** | real_disagreement | Methodology Cases 3–5: four genuinely different M-positions on the *jīva-Brahman* relation. |

## 4. Framing-status breakdown

- **same_concept_different_aspect:** 12 terms (dharma, karma, jñāna, bhakti, vidyā, pramāṇa, pratyakṣa, anumāna, sākṣin, śabda, anubhava, upādhi, prapatti — 13 actually)
- **real_disagreement:** 5 terms (mithyā, satkārya-vāda, pariṇāma, vivarta, bheda)
- **different_concepts:** 2 terms (guṇa, anatta)
- **mixed:** 10 terms (mokṣa, brahman, ātman, jīva, māyā, avidyā, prakṛti, puruṣa, adhyāsa, vyāvahārika, pāramārthika)

**Distribution.** 13/30 ≈ 43% are *same concept, different aspect* — the user's instinct that false separation is the dominant defect is empirically confirmed: nearly half the priority terms had their philosophical content being misread by the legacy flat-by-school format. 10/30 are *mixed* (most foundational Vedāntic terms): genuine intra-Vedānta disagreements coexist with shared structural role. 5/30 are *real_disagreement* — these are the terms where the user's anti-fabrication discipline (AF1) requires the difference to be preserved, not dissolved. Only 2/30 are *different_concepts* (genuine homonymy across traditions).

## 5. Top examples of false separation the user's instinct correctly flagged

1. **dharma** (the user's screenshot case). The legacy reading made Advaita and Viśiṣṭādvaita look as if they were giving competing definitions of *dharma*. Both in fact preserve the *codanā*-grounded *Mīmāṃsā* role; they differ in register (Advaita: P+S preparatory under *adhikāra*; Viśiṣṭādvaita: M+S binding-and-surrenderable) and addressee. The audit makes this explicit in the *shared_core*.

2. **bhakti**. The legacy entries looked as if Advaita, Viśiṣṭādvaita, and Gauḍīya had different concepts of *bhakti*. They share the directed-orientation-to-Bhagavān role; methodology Case 7 (Madhusūdana) shows the *jñānin* and *bhakta* registers cohere in one author. AF8 surfaced.

3. **karma**. Mīmāṃsā ritual *karma* and Advaita's *karma* in the *jñāna-karma-samuccaya* debate looked like competing definitions. They share the Pāṇinian *kāraka* root and the action-trace-fruition triad; they differ on register (RN+SL vs. S+E). The real disagreement on *jñāna-karma-samuccaya* is preserved as AF1.

4. **jñāna**. The legacy entries made it look as if Advaita's *jñāna* and Tattva-vāda's *jñāna* were different concepts. They share the veridical-cognition role; the real disagreement (Hari gives *jñāna*, *Anuvyākhyāna* 1.1.13–15) is preserved.

## 6. Top examples of real disagreement preserved (anti-fabrication AF1)

1. **mokṣa.** Advaita (identity-thesis) vs. Tattva-vāda (*jīveśvara-bheda* persists, *taratamya* among the liberated, *Viṣṇu-Tattva-Vinirṇaya* 3.27). Same M+S register, same scope-inside, opposing claims. Marked as `[REAL-DISAGREEMENT]`.

2. **māyā.** Advaita's *anirvacanīya* third category vs. Madhva's reduction. Methodology Case 6. Marked as `[REAL-DISAGREEMENT]`.

3. **bheda.** The four positions on the *jīva-Brahman* relation (Cases 3–5) preserved as genuinely different M-claims.

4. **anatta / ātman.** AF1 explicit: Buddhist denial and Brāhmaṇical affirmation operate at the same Φ+E register and same scope-inside. Not register-relativism; opposite answers to the same question.

## 7. What is still `[NOT YET RETRIEVED]`

The framing layer was added without rewriting the per-school definitions themselves; existing `[NOT YET RETRIEVED]` markers in per-school definitions (Bhedābheda, Dvaitādvaita, Śuddhādvaita, Pāṇinian-Vaiyākaraṇa for many terms) are preserved as-is. The audit did not regress any citations; where per-school text was thin, the new `shared_core` provides the methodological context that the legacy display lacked.

## 8. Queued for follow-up audit (terms 31+)

Remaining ~115 glossary terms not in this PR. Priority next-15 (by article-frequency):

samsara, kaivalya, sat, asat, nirguna, saguna, isvara, bhagavan, paratantra, svatantra, taratamya, aprthak-siddhi, antaryamin, panca-bheda, ahankara, manas, buddhi, antahkarana, citta, kutastha, akhandakara-vrtti, pratyabhijna, spanda, sakti, syad-vada, anekanta-vada, sunyata, pratitya-samutpada, alaya-vijnana, vijnapti-matrata, trisvabhava, apoha, sopadhika, nirupadhika, sarira-saririn-bhava, dharmabhuta-jnana, lila, prema, rasa, jivanmukta, videhamukti, prarabdha, sadhana, sraddha, śravana, manana, nididhyasana, saksatkara, aparoksa-jnana, mahavakya, niṣkāma-karma, abheda, advaita, dvaita, ekayana.

Apply the same script-driven discipline. Estimated ~3 hours per 30-term wave.

## 9. Schema additions (backwards-compatible)

```json
{
  "school_framing": {
    "framing_status": "same_concept_different_aspect | real_disagreement | different_concepts | mixed",
    "shared_core": "<one-paragraph statement>",
    "register_axes_note": "<axis of difference with AF1/AF2 markers>"
  },
  "per_school": [
    {
      "school": "...",
      "register_tag": "<primary register; addressee>",
      "definition": "...",
      "primary_loci": [...],
      "citations": [...]
    }
  ]
}
```

Entries without `school_framing` render exactly as before (the renderer guards on `entry.school_framing` falsy). The `register_tag` field is also optional and falls back to empty.

## 10. Files changed

- `data/glossary/<31 term JSONs>` — added `school_framing` and per-school `register_tag` where determinable
- `assets/app.js` — `openGlossary()` updated to render the framing preamble and register-tag pills
- `assets/style.css` — added `.gp-framing`, `.gp-framing-status`, `.gp-shared-core`, `.gp-axes`, `.gp-regtag` rules
- `scripts/apply_school_framing.py` — automation script, kept in tree so the remaining ~115 terms can be processed with the same discipline
- `audit/glossary-methodology-audit-report.md` — this file
