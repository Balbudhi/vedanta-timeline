#!/usr/bin/env python3
"""
Wave 2 of the BY-SCHOOL framing audit.

Extends `scripts/apply_school_framing.py` (Wave 1, PR #44) to the next tier of
glossary entries. Same schema:

    school_framing = {
        framing_status: same_concept_different_aspect | real_disagreement |
                        different_concepts | mixed
        shared_core:    one-paragraph statement of structural agreement
        register_axes_note:
                        the operational axes (register / scope / addressee)
                        on which the schools diverge
    }

Each `per_school` entry receives a `register_tag` keyed on the operational
tuple from `SCOPE_REGISTER_FRAMEWORK.md` §1 / §7 (primary register; addressee).
Tags include explicit `[REAL-DISAGREEMENT ...]` annotations where AF1 holds.
Where the primary-text basis for a school's slot is unrecoverable in this
worktree, the register_tag is omitted (skipped, not invented).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
GLOSS = ROOT / "data" / "glossary"


def reorder(d: dict) -> dict:
    if "school_framing" not in d:
        return d
    keys = list(d.keys())
    if "invariant_definition" in keys and "per_school" in keys:
        new_order = []
        inserted = False
        for k in keys:
            if k == "school_framing":
                continue
            new_order.append(k)
            if k == "invariant_definition" and not inserted:
                new_order.append("school_framing")
                inserted = True
        return {k: d[k] for k in new_order}
    return d


def apply(term: str, framing: dict, register_tags: Optional[dict] = None) -> None:
    path = GLOSS / f"{term}.json"
    if not path.exists():
        print(f"  SKIP {term}: not found")
        return
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    d["school_framing"] = framing
    if register_tags:
        for entry in d.get("per_school", []):
            tag = register_tags.get(entry.get("school"))
            if tag is not None:
                entry["register_tag"] = tag
    d = reorder(d)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  OK   {term}")


# -------------------------------------------------------------------------
# Wave 2 framings. Each term carries (a) methodology judgment grounded in
# the cited primary texts already present in each entry's per_school block,
# (b) a shared_core, and (c) a register_axes_note that names the operational
# divergence axes.
# -------------------------------------------------------------------------

TERMS = {
    # ---- 1. Core being / non-being ----
    "sat": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Sat* names **what stands up under ontological and causal "
                "analysis: the determinate referent of *asti***. All schools "
                "that use the term agree on this structural role — *sat* is "
                "not the bare copula but what survives scrutiny. They differ "
                "on (i) whether *sat* in the strict sense belongs only to "
                "the unconditioned (Advaita) or also to dependent reals "
                "(Viśiṣṭādvaita, Tattva-vāda, Śuddhādvaita, Sāṃkhya, Nyāya-"
                "Vaiśeṣika, Yoga, Jainism, Trika), (ii) whether effects "
                "pre-exist in the cause (*satkārya-vāda*) or arise anew "
                "(*asatkārya-vāda*), and (iii) whether the *sat*/*asat* "
                "binary is exhaustive (most schools: yes) or admits an "
                "*anirvacanīya* third (Advaita)."
            ),
            "register_axes_note": (
                "Schools differ along the M-register axis (which entities "
                "carry *sattā* in the strict sense) and the LD-register axis "
                "(what *sat* as a predicate can support). **Real "
                "disagreement** (AF1) between Advaita (*sat* in the strict "
                "sense only of Brahman; *Māṇḍūkya-Bhāṣya* 7) and Tattva-vāda "
                "(*sat* of the *bhedapañcaka*; *Anuvyākhyāna* 1.4.111–112) — "
                "same M-register, same scope-inside, opposing claims. "
                "**Different concept** in Mādhyamaka and Yogācāra: *sat* is "
                "framed inside the two-truths / *arthakriyā-sāmarthya* "
                "economy, not the substance-attribute economy of the "
                "Brāhmaṇical schools."
            ),
        },
        "register_tags": {
            "Advaita": "M+E; mumukṣu [REAL-DISAGREEMENT with realist Vedāntas on strict-sense sat]",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT with Advaita on bhedapañcaka-sattva]",
            "Bhedābheda": "M+S; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "M+C; mumukṣu (satkārya-vāda)",
            "Yoga": "M+Φ; yogin (dharmin persistence)",
            "Nyāya-Vaiśeṣika": "M+E; reflective reader (sattā as sāmānya)",
            "Pūrva-Mīmāṃsā": "E+RN; adhikārin",
            "Mādhyamaka": "LD+M; reflective reader [different framing: two-truths]",
            "Yogācāra": "E+M; reflective reader [different framing: arthakriyā-sat]",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
            "Jainism": "M+C; reflective reader (sat as utpāda-vyaya-dhrauvya)",
            "Pāṇinian-Vaiyākaraṇa": None,
        },
    },
    "asat": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Asat* names **what is excluded from *sat* under the "
                "criterion the school imposes on being**. Advaita treats "
                "*asat* strictly (the rabbit's horn, *vandhyā-putra*: what "
                "cannot even appear), so the world is *mithyā* and not "
                "*asat* (BSB 2.1.14). Sāṃkhya excludes *asat* from causal "
                "production altogether (*nāsato vidyate bhāvaḥ*; "
                "*Sāṃkhya-Kārikā* 9). Tattva-vāda allows only the *sat*/"
                "*asat* binary and locates *mithyātva* under *asat*-equivalent "
                "(*Mithyātvānumāna-Khaṇḍana*)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether the *sat*/*asat* "
                "binary is exhaustive: Advaita inserts *anirvacanīya* "
                "between them; Tattva-vāda denies the third. Same M+LD "
                "register, same scope-inside, opposing claims. Sāṃkhya's "
                "use is principally causal-modal (what can be produced), "
                "not ontological-classificatory — a register-difference "
                "from the Advaita/Tattva-vāda contest."
            ),
        },
        "register_tags": {
            "Advaita": "M+LD; mumukṣu",
            "Sāṃkhya": "M+C; mumukṣu (causal-modal use)",
            "Tattva-vāda": "M+LD; Tattvavādin [REAL-DISAGREEMENT on binary exhaustiveness]",
        },
    },
    "anirvacaniya": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Anirvacanīya* names **what cannot be fixed as either *sat* "
                "or *asat* without distortion**. Advaita develops the third "
                "category to handle *māyā*, *avidyā*, and the objects of "
                "error (Maṇḍana's *Brahma-Siddhi* 1.1; *Iṣṭa-Siddhi*; "
                "*Advaita-Siddhi*). Nyāya, Viśiṣṭādvaita, and Tattva-vāda "
                "refuse the category and read every cognition's object as "
                "*sat* (with possible mislocation) or *asat*."
            ),
            "register_axes_note": (
                "AF1 — same M+LD register, same scope-inside (the modal "
                "status of objects of error), opposing claims. Madhva's "
                "*Mithyātvānumāna-Khaṇḍana* is the paradigm LD attack: "
                "*anirvacanīya* either reduces to *sat* or to *asat*, or "
                "issues in *anavasthā*. The Advaitic reply (*Advaita-Siddhi*) "
                "is that the binary itself fails as a *prameya*-exhaustive "
                "schema. Methodology Case 6: the disagreement is genuine, "
                "not register-artifactual."
            ),
        },
        "register_tags": {
            "Advaita": "M+LD; polemicist/mumukṣu",
            "Nyāya, Viśiṣṭādvaita, and Tattva-vāda (rejection)": "M+LD; polemicist [REAL-DISAGREEMENT: third category rejected]",
        },
    },
    "abheda": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Abheda* names **non-difference: the identity-relation in "
                "which two terms are not distinct in *svarūpa***. All "
                "Vedāntic schools admit *abheda*-language in scripture "
                "(*tat tvam asi*; *neha nānāsti kiñcana*); they differ on "
                "whether *abheda* is the ultimate truth (Advaita), one of "
                "two simultaneous truths held together (Bhedābheda, "
                "Acintya-Bhedābheda, Dvaitādvaita), or only a relational "
                "*aupacārika* gloss on the *sāmānādhikaraṇya* between "
                "*śarīrin* and *śarīra* (Viśiṣṭādvaita) or on *sādṛśya* "
                "(Tattva-vāda)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Advaita (*abheda* "
                "alone is *pāramārthika*) and Tattva-vāda (*abheda*-texts "
                "must be read as *sādṛśya* under *bhedapañcaka*; *Anuvy.* "
                "2.3.66–69). **Same concept, different aspect** between "
                "Advaita and Bhedābheda / Dvaitādvaita / Gauḍīya where "
                "*abheda* is one of two simultaneously real aspects rather "
                "than the sole ultimate. Methodology Cases 3–5."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu [REAL-DISAGREEMENT with Tattva-vāda on abheda-ultimacy]",
            "Viśiṣṭādvaita": "M+SL; prapanna (sāmānādhikaraṇya reading)",
            "Tattva-vāda": "M+LD; Tattvavādin [REAL-DISAGREEMENT: sādṛśya, not svarūpābhidā]",
            "Bhedābheda / Acintya-Bhedābheda": "M+S; bhakta (both bheda and abheda)",
        },
    },

    # ---- 2. Cit-ānanda compound ----
    "saccidananda": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Sac-cid-ānanda* is **the Upaniṣadic *svarūpa-lakṣaṇa* of "
                "Brahman: being, consciousness, bliss as the *svarūpa*-"
                "indicators of the ultimate** (Taittirīya 2.1; "
                "*Bṛhadāraṇyaka* 3.9.28's *vijñānam ānandaṃ brahma*). All "
                "Vedāntic schools agree on the structural role — these "
                "three terms pick out the *svarūpa* of Brahman, not three "
                "separate attributes. Schools differ on whether the triad "
                "is a *svarūpa-lakṣaṇa* of the *nirviśeṣa* Absolute "
                "(Advaita), an *aṃśa* of Bhagavān's infinite *kalyāṇa-"
                "guṇas* (Viśiṣṭādvaita, Tattva-vāda), or the *svarūpa-"
                "śakti* of Bhagavān taking the threefold form *sandhinī / "
                "saṃvit / hlādinī* (Gauḍīya)."
            ),
            "register_axes_note": (
                "Same M-register, same scope-inside (Brahman's *svarūpa*), "
                "differing aspects. Real disagreement only at the level of "
                "whether the triad exhausts Brahman's *svarūpa* (Advaita) "
                "or is one cluster within an infinite-*guṇa* *svarūpa* "
                "(Viśiṣṭādvaita / Tattva-vāda / Vallabha)."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu (svarūpa-lakṣaṇa of nirviśeṣa-brahman)",
            "Viśiṣṭādvaita": "M+S; prapanna (aṃśa of ananta-kalyāṇa-guṇa)",
            "Tattva-vāda (Dvaita)": "M+S; Tattvavādin",
            "Śuddhādvaita (Vallabha)": "M+S; bhakta",
        },
    },
    "saguna": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Saguṇa* names **Brahman / Bhagavān as endowed with "
                "*guṇa*s: attributes, powers, or auspicious qualities**. "
                "Advaita treats *saguṇa-brahman* as the *upāsanā*-object "
                "for the *mumukṣu*, ultimately resolving into *nirguṇa-"
                "brahman*. Viśiṣṭādvaita, Tattva-vāda, and Gauḍīya treat "
                "*saguṇa* as Brahman's *svarūpa*-itself, the infinite "
                "*kalyāṇa-guṇas* being non-different from the *svarūpin* "
                "(*Śrī-Bhāṣya* 1.1.1; *Brahma-Sūtra-Bhāṣya* 1.1.1)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether *saguṇa* is "
                "*upāsanā*-relative (Advaita: P+S register, addressed to "
                "the *mumukṣu* under *adhyāsa*) or *svarūpa*-itself "
                "(theistic Vedāntas: M+S register). Same scope-inside "
                "(Brahman's relation to attributes), opposing claims on "
                "ontological status."
            ),
        },
        "register_tags": {
            "Advaita": "P+S; mumukṣu (upāsanā-relative)",
            "Viśiṣṭādvaita": "M+S; prapanna [REAL-DISAGREEMENT with Advaita: saguṇatva is svarūpa]",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },
    "nirguna": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Nirguṇa* names **Brahman as free of *prākṛta-guṇa* "
                "(*sattva*-*rajas*-*tamas*) and of any limiting predication "
                "that would compromise its non-duality or its ultimacy**. "
                "Advaita treats *nirguṇa-brahman* as the *pāramārthika* "
                "Absolute, free of *all* differentiating attributes. "
                "Viśiṣṭādvaita and Tattva-vāda read *nirguṇa* as denial of "
                "*prākṛta-guṇa* only — Brahman is *nirguṇa* in the sense of "
                "transcending material qualities while bearing *aprākṛta-"
                "kalyāṇa-guṇas* (*Vedārtha-Saṅgraha* §§7-12)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on the scope of *nirguṇa*'s "
                "denial. Same M-register, same scope-inside, opposing "
                "claims: Advaita denies *all* attributes; theistic Vedāntas "
                "deny only *prākṛta*-attributes. Methodology Case 1: the "
                "two readings are not register-translations of one claim, "
                "they are competing M-readings of *nirguṇa-vākyas*."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu [REAL-DISAGREEMENT: total attribute-denial]",
            "Viśiṣṭādvaita": "M+SL; prapanna [REAL-DISAGREEMENT: only prākṛta-guṇa denied]",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },

    # ---- 3. Iśvara / Bhagavān / antaryāmin / śakti / līlā cluster ----
    "isvara": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Īśvara* names **the lord: the ruling-conscious principle "
                "with sovereign agency over the world**. The structural "
                "role — ruling-conscious-agent — is shared across schools "
                "that retain the term. Advaita treats *Īśvara* as *saguṇa-"
                "brahman* under *māyā*, with *upāsanā*-status. "
                "Viśiṣṭādvaita and Tattva-vāda identify *Īśvara* with "
                "Bhagavān as the *paratattva* itself. Yoga admits *Īśvara* "
                "as a special *puruṣa* untouched by *kleśa-karma-vipāka* "
                "(*YS* 1.24); Nyāya argues for *Īśvara* as the maker-"
                "knower from *sthiti-pralaya-ādi-kāraṇāt*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on ontological status: "
                "Advaita's *Īśvara* is *vyāvahārika* relative to *nirguṇa-"
                "brahman*; theistic Vedāntas' *Īśvara* is *pāramārthika*. "
                "Yoga's *Īśvara* is **a different concept** at the M-level: "
                "a special *puruṣa* among many, not a *jagat-kāraṇa* in "
                "Vedāntic sense. Nyāya-Vaiśeṣika's *Īśvara* is also "
                "**different in scope**: efficient cause, not material "
                "cause."
            ),
        },
        "register_tags": {
            "Advaita": "P+S; mumukṣu (Īśvara as saguṇa-brahman, upāsanā-relative)",
            "Viśiṣṭādvaita": "M+S; prapanna [REAL-DISAGREEMENT with Advaita on pāramārthikatva]",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Bhedābheda": "M+S; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "C; reflective reader [no Īśvara; nirīśvara]",
            "Yoga": "M+S; yogin [different concept: viśeṣa-puruṣa, YS 1.24]",
            "Nyāya-Vaiśeṣika": "M+LD; reflective reader (efficient cause)",
            "Pūrva-Mīmāṃsā": "RN; adhikārin [no Īśvara role]",
            "Mādhyamaka": "LD; reflective reader [Īśvara-pratiṣedha]",
            "Yogācāra": "Φ; reflective reader [no creator-Īśvara]",
            "Pratyabhijñā / Trika": "M+S; sādhaka (Maheśvara as parā-saṃvit)",
            "Jainism": "M+C; reflective reader [no creator-Īśvara]",
            "Pāṇinian-Vaiyākaraṇa": None,
        },
    },
    "bhagavan": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Bhagavān* names **the supreme person possessed of the six "
                "*bhaga*s: *aiśvarya*, *vīrya*, *yaśas*, *śrī*, *jñāna*, "
                "*vairāgya*** (*Viṣṇu-Purāṇa* 6.5.74). All theistic Vedāntic "
                "schools agree on the structural role — *Bhagavān* is the "
                "*paratattva* in personal form. Advaita treats *Bhagavān*-"
                "discourse as the *upāsanā* surface of *saguṇa-brahman*, "
                "resolved at the *pāramārthika* tier into *nirguṇa-brahman*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether *Bhagavān*-"
                "discourse is *pāramārthika* (Viśiṣṭādvaita, Tattva-vāda, "
                "Gauḍīya, Vallabha, Nimbārka) or *vyāvahārika* / *upāsanā*-"
                "relative (Advaita). Same M-register, same scope-inside, "
                "opposing claims on ultimate ontological status. **Same "
                "concept, different aspect** when AD-register *stotra* "
                "speech is in view: methodology Cases 1 and 7 (Madhusūdana's "
                "*Bhakti-Rasāyana* shows the AD-register survives the "
                "*jñāna*-completion in Advaita itself)."
            ),
        },
        "register_tags": {
            "Advaita Vedānta": "P+S+AD; mumukṣu and stotrakāra [Bhagavān as upāsanā-relative + AD-survivor]",
            "Viśiṣṭādvaita": "M+AD+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },
    "antaryamin": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Antaryāmin* names **the inner ruler: the conscious "
                "principle that resides in and governs all selves and "
                "elements**, fixed in the *Antaryāmi-Brāhmaṇa* of "
                "*Bṛhadāraṇyaka* 3.7. All Vedāntic schools that engage the "
                "passage agree on the structural role — the *antaryāmin* is "
                "what governs from within. They differ on the relation "
                "between *antaryāmin* and *jīva*: identity-as-witness "
                "(Advaita), *śarīra-śarīrin* (Viśiṣṭādvaita: BṛU 3.7 is "
                "the locus classicus), eternal-distinct controller "
                "(Tattva-vāda), the supreme person dwelling in the "
                "*hṛdaya* as *Paramātman* (Gauḍīya)."
            ),
            "register_axes_note": (
                "Same M+Φ register; same scope-inside (the inner-ruler "
                "relation). Real disagreement only on whether the *antar-"
                "yāmin*-*jīva* relation is *aprthak-siddhi* "
                "(Viśiṣṭādvaita), *bimba-pratibimba* (Tattva-vāda), or "
                "*aupādhika* identity (Advaita). Methodology Cases 3 and 4."
            ),
        },
        "register_tags": {
            "Advaita": "M+Φ; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna (aprthak-siddhi, methodology Case 3)",
            "Tattva-vāda": "M+S; Tattvavādin (bimba-pratibimba)",
            "Acintya-Bhedābheda": "M+AD; bhakta (Paramātman in hṛdaya)",
        },
    },
    "sakti": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Śakti* names **a power: a capacity to produce a "
                "determinate effect that belongs intrinsically to its "
                "*śaktimat***. The structural role — power-of-an-agent — is "
                "shared across Vedāntic and Śaiva schools. Schools differ "
                "on whether *śakti* is (i) Brahman's own *svarūpa-śakti* "
                "(Viśiṣṭādvaita, Tattva-vāda, Gauḍīya, Vallabha, Nimbārka), "
                "(ii) *māyā-śakti* of indeterminate ontological status "
                "(Advaita), (iii) Śiva's *svātantrya* / *spanda* / *vimarśa* "
                "(Trika), or (iv) a *sāmarthya* attached to substance-"
                "attribute relations (Nyāya-Vaiśeṣika)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on the ontological status of "
                "*śakti*: Trika's *svātantrya-śakti* is identical with the "
                "*śaktimat* and is the ultimate (Utpaladeva, *ĪPK* 1.5; "
                "*Pratyabhijñā-Hṛdaya* 1); Advaita treats *māyā-śakti* as "
                "*anirvacanīya*; Tattva-vāda treats *śakti* as real, "
                "dependent, and *bheda*-related. Same M-register, same "
                "scope-inside, opposing claims. Vaiyākaraṇa *śakti* is "
                "the SL-register notion of semantic potency, **a different "
                "concept** (Bhartṛhari *VP* III).",
            ),
        },
        "register_tags": {
            "Advaita": "M+LD; polemicist (māyā-śakti as anirvacanīya)",
            "Viśiṣṭādvaita": "M+S; prapanna (svarūpa-śakti)",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT: śakti as bheda-related]",
            "Acintya-Bhedābheda": "M+AD; bhakta (acintya-śakti, methodology Case 5)",
            "Pratyabhijñā / Trika": "M+S; sādhaka [REAL-DISAGREEMENT: svātantrya-śakti as ultimate]",
            "Pāṇinian-Vaiyākaraṇa": "SL; reflective reader [different concept: semantic potency]",
        },
    },
    "lila": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Līlā* names **the sport-like spontaneity by which Brahman "
                "or Bhagavān manifests the world without ulterior purpose**, "
                "fixed by *Brahma-Sūtra* 2.1.33 (*lokavat tu līlā-"
                "kaivalyam*). All schools commenting on the sūtra agree on "
                "the *aprayojanatva* of the creating act. They differ on "
                "whether *līlā* is *vyāvahārika* surface (Advaita: BSB "
                "2.1.33–34) or the constructive M-thesis that the post-"
                "realization world is real divine play (Vallabha: *Aṇu-"
                "Bhāṣya* 2.1.33; Gauḍīya: *Bhāgavata* 10; Trika: *spanda* "
                "as Śiva's *līlā*)."
            ),
            "register_axes_note": (
                "Same M-register on the *aprayojanatva* claim; different "
                "scope-inside on which world is being described — "
                "*mumukṣu*-phenomenology (Advaita) vs. post-realization "
                "ontology (Vallabha, Gauḍīya). Methodology Case 1: the "
                "register-reading dissolves the apparent contradiction. "
                "**Real disagreement** survives only at the S-register on "
                "whether *līlā* itself is *prayojana* (Vallabha)."
            ),
        },
        "register_tags": {
            "Advaita": "P+M; mumukṣu (BSB 2.1.33–34, methodology Case 1)",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Trika / Kashmir Śaivism": "M+S; sādhaka (spanda as Śiva's līlā)",
        },
    },

    # ---- 4. Mukti cluster ----
    "kaivalya": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Kaivalya* names **the alone-standing condition in which "
                "*puruṣa* / *ātman* / *jīva* abides without further "
                "involvement in *prakṛti* or *saṃsāra***. The structural "
                "role — solitary, non-returning culmination — is shared. "
                "Schools differ on what the alone-standing self stands "
                "alone *with*: the *kūṭastha* witness identical to Brahman "
                "(Advaita), Bhagavān-related *kaiṅkarya* (Viśiṣṭādvaita), "
                "the *paratantra-jīva* in *taratamya* with Hari (Tattva-"
                "vāda), or *puruṣa* in pure *cit*-standing apart from "
                "*prakṛti* (Sāṃkhya-Yoga; *Sāṃkhya-Kārikā* 68; *YS* 4.34)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on the *kaivalya*-state's "
                "content. Sāṃkhya-Yoga's *kaivalya* is *jīveśvara-bheda* "
                "without an *Īśvara*-role; Advaita's *kaivalya* is *jīva-"
                "brahman-aikya*. Same M+S register, same scope-inside "
                "(non-returning terminus), opposing claims on what is "
                "realized. **Same concept, different aspect** between "
                "Viśiṣṭādvaita and Acintya-Bhedābheda where *kaivalya* is "
                "rejected as the highest end and *prema-mukti* is preferred."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu (jīva-brahman-aikya)",
            "Viśiṣṭādvaita": "M+S; prapanna [REAL-DISAGREEMENT: kaivalya lower than Bhagavat-prāpti]",
            "Tattva-vāda": "M+S; Tattvavādin (taratamya among the kaivalin)",
            "Bhedābheda": "M+S; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta [REAL-DISAGREEMENT: prema > kaivalya]",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "M+S; mumukṣu [REAL-DISAGREEMENT: puruṣa-isolation, no Īśvara]",
            "Yoga": "S+Mh; yogin (YS 4.34)",
            "Nyāya-Vaiśeṣika": "M+S; reflective reader",
            "Pūrva-Mīmāṃsā": "RN; adhikārin [partially different concept]",
            "Mādhyamaka": "LD+S; reflective reader [functional analogue: nirvāṇa]",
            "Yogācāra": "Φ+S; reflective reader",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
            "Jainism": "M+S; reflective reader (kevala-jñāna context)",
            "Pāṇinian-Vaiyākaraṇa": None,
        },
    },
    "jivanmukta": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Jīvanmukta* names **one who is released while still "
                "embodied: the realized self in whom liberating cognition "
                "has occurred yet whose *prārabdha-karma* still sustains "
                "the body**. Advaita is the principal home of the doctrine "
                "(*Upadeśa-Sāhasrī*; *Pañcadaśī* VII; *Jīvanmukti-Viveka*). "
                "Viśiṣṭādvaita admits a parallel state under *kaiṅkarya* of "
                "the *prapanna*. Tattva-vāda restricts liberation to "
                "*videhamukti*: there is no *jīvanmukti* in the strict "
                "Advaitic sense (*Brahma-Sūtra-Bhāṣya* 4). Trika's *jīvan-"
                "mukta* is the *pratyabhijñā*-recognizer who acts as Śiva-"
                "*svarūpa*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Advaita and Tattva-"
                "vāda on the very possibility of liberation-in-body: same "
                "M+S register, opposing claims. **Same concept, different "
                "aspect** between Advaita and Trika where both admit "
                "embodied liberation but differ on whether the realized "
                "agent is *kūṭastha-witness* or *Śiva-svarūpa* active "
                "agent."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; jīvanmukta (Φ+S in self-description)",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT: only videhamukti]",
            "Trika / Kashmir Śaivism": "M+S; sādhaka (jīvanmukta as Śiva-svarūpa)",
        },
    },
    "videhamukti": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Videhamukti* names **release at body-fall: the cessation "
                "of further embodiment when *prārabdha-karma* exhausts**. "
                "All Vedāntic schools accept the structural role — *mokṣa* "
                "becomes complete at body-fall. Advaita pairs *videhamukti* "
                "with *jīvanmukti* (the latter being already-released, the "
                "former being the body-final terminus). Tattva-vāda treats "
                "*videhamukti* as the *only* genuine release (no embodied "
                "liberation) and ranks the released *jīvas* in *taratamya*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether *videhamukti* is "
                "the unique liberation-state (Tattva-vāda) or a culmination "
                "of an already-realized *jīvanmukti* (Advaita). Same M+S "
                "register, opposing claims. Viśiṣṭādvaita reads *vide-"
                "hamukti* as entry into *parama-pada* with *kaiṅkarya* "
                "(*śaraṇāgati-gadya*; *Vaikuṇṭha-gadya*) — same concept, "
                "different content."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT: only mode of release]",
        },
    },

    # ---- 5. Pedagogical / soteriological method ----
    "mahavakya": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Mahāvākya* names **a great sentence: one of the four "
                "Upaniṣadic *vākyas* (*tat tvam asi*, *aham brahmāsmi*, "
                "*ayam ātmā brahma*, *prajñānam brahma*) whose function is "
                "to convey *brahmavidyā***. Advaita treats them as *jñāna-"
                "siddha-vākyas* whose *tātparya* is direct identity-"
                "instruction (*Upadeśa-Sāhasrī*; *Naiṣkarmya-Siddhi*). "
                "Viśiṣṭādvaita reads them as *aikya* under *sāmānādhi-"
                "karaṇya* of *śarīrin*-*śarīra* (*Vedārtha-Saṅgraha* §§7-12). "
                "Tattva-vāda reads them under *sādṛśya* and *aṃśa*-relation, "
                "with *neṣṭa-tādātmya* (*Anuvyākhyāna*). Bhāskara reads them "
                "under *aupādhika-bhedābheda*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on the *tātparya* and the "
                "*vākyārtha* of the same Upaniṣadic *śabda*s. Same SL+S "
                "register, same scope-inside (what the *vākya* means), "
                "opposing readings. Methodology §4: the same *śabda* "
                "carries different *artha* and different *pratyaya* in "
                "each school's hermeneutic frame; but here the schools "
                "*disagree* on which reading is correct rather than "
                "addressing different scopes."
            ),
        },
        "register_tags": {
            "Advaita": "SL+S; mumukṣu (jñāna-siddha, direct aikya)",
            "Viśiṣṭādvaita": "SL+S; prapanna [REAL-DISAGREEMENT: sāmānādhikaraṇya reading]",
            "Tattva-vāda": "SL+LD; Tattvavādin [REAL-DISAGREEMENT: sādṛśya reading]",
            "Bhedābheda (Bhāskara)": "SL+S; upāsaka (aupādhika reading, Case 4)",
        },
    },
    "upaya": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Upāya* names **a means: the operational path or technique "
                "whose deployment brings about a determinate end**. The "
                "structural role is shared. Vedāntic schools dispute "
                "*which* *upāya* effects *mokṣa* — *jñāna* alone (Advaita), "
                "*bhakti-yoga* with *prapatti* (Viśiṣṭādvaita), *prapatti* "
                "alone (Tenkalai Śrīvaiṣṇavism), *rāgānuga-bhakti* "
                "(Gauḍīya). Trika maps four *upāya*s by adhikāra "
                "(*ānavopāya*, *śāktopāya*, *śāmbhavopāya*, *anupāya*; "
                "*Tantrāloka* I, II). Mahāyāna's *upāya-kauśalya* is **a "
                "different concept**: the bodhisattva's pedagogical "
                "skillful-means, not the path of one's own release."
            ),
            "register_axes_note": (
                "**Same concept, different aspect** within Vedānta: schools "
                "agree on the structural role and disagree on which *upāya* "
                "is *mokṣa-sādhana*. **Different concept** in Mahāyāna where "
                "*upāya* is the bodhisattva's pedagogical resource "
                "(*Saddharma-Puṇḍarīka* 2; *Vimalakīrti-Nirdeśa*). Trika's "
                "four *upāyas* are P+Mh: pedagogically scoped to "
                "*adhikāra*."
            ),
        },
        "register_tags": {
            "Advaita": "S+P; mumukṣu (jñāna-niṣṭhā)",
            "Viśiṣṭādvaita": "S+P; prapanna (bhakti-yoga + prapatti)",
            "Acintya-Bhedābheda": "S+AD; bhakta (rāgānuga-bhakti)",
            "Mahāyāna Buddhism": "P+S; bodhisattva [different concept: upāya-kauśalya]",
            "Trika / Kashmir Śaivism": "P+Mh; sādhaka (four upāyas by adhikāra)",
        },
    },
    "saksatkara": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Sākṣātkāra* names **immediate realization: the direct, "
                "non-mediated cognition of the highest object that "
                "constitutes liberating knowledge**, paralleling *aparokṣa-"
                "jñāna*. Advaita identifies *sākṣātkāra* with *brahmā-"
                "nubhava* (*Upadeśa-Sāhasrī*). Viśiṣṭādvaita identifies it "
                "with *Bhagavat-sākṣātkāra* (*Śrī-Bhāṣya* 1.1.1). Tattva-"
                "vāda identifies it with *aparokṣa-jñāna* of Hari, granted "
                "by his *prasāda*. Gauḍīya identifies it with *darśana* in "
                "*prema-rasa*."
            ),
            "register_axes_note": (
                "Same Φ+E+S register; same scope-inside (non-mediated "
                "terminal cognition). Real disagreement only on the *object* "
                "of *sākṣātkāra*: *nirviśeṣa-brahman*, *Bhagavān*, Hari-"
                "*aṃśa*, *Bhagavat-prema-mūrti*. Methodology Case 2: "
                "Φ-continuity does not entail S-continuity."
            ),
        },
        "register_tags": {
            "Advaita": "Φ+E+S; mumukṣu (brahmānubhava)",
            "Viśiṣṭādvaita": "Φ+S; prapanna (Bhagavat-sākṣātkāra)",
            "Tattva-vāda (Dvaita)": "Φ+S; Tattvavādin (Hari-prasāda)",
            "Acintya-Bhedābheda": "Φ+AD; bhakta (prema-darśana)",
        },
    },
    "pratibhasika": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Prātibhāsika* names **the merely apparent: the third tier "
                "in Advaita's *vyāvahārika*/*pāramārthika*/*prātibhāsika* "
                "ontology, fixed by *Pañcadaśī* VI and *Vedānta-Paribhāṣā* "
                "I**, where *prātibhāsika* objects (rope-snake, shell-silver) "
                "are sublatable by another *vyāvahārika* cognition, not "
                "merely by *brahmajñāna*. Nyāya rejects the three-tier "
                "ontology and reads error as *anyathā-khyāti* on real "
                "constituents. Tattva-vāda similarly rejects the third "
                "tier and explains the same cases as defective *jñāna* of "
                "real items."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether a *prātibhāsika* "
                "tier is required at all (Advaita vs. Nyāya, Tattva-vāda). "
                "Same M+E register, opposing claims. Methodology §4's "
                "*vyākaraṇa*-corrective is relevant: the *vyāvahārika* / "
                "*prātibhāsika* split exists because Advaita needs a tier "
                "for error-objects distinct from the *vyāvahārika* world; "
                "schools that read error differently (mislocation, "
                "anyathā-khyāti) do not need the tier."
            ),
        },
        "register_tags": {
            "Advaita": "M+E; mumukṣu (three-tier ontology)",
            "Nyāya": "E+LD; reflective reader [REAL-DISAGREEMENT: anyathā-khyāti, no third tier]",
            "Tattva-vāda": "E+LD; Tattvavādin [REAL-DISAGREEMENT: no third tier]",
        },
    },

    # ---- 6. Internal organ cluster ----
    "ahankara": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Ahaṃkāra* names **the I-maker: the cognitive function "
                "that appropriates experience as 'mine' and constitutes "
                "the empirical agent-self**. Sāṃkhya-Yoga gives the "
                "paradigm definition: *ahaṃkāra* is the *prakṛti*-evolute "
                "between *mahat* and the *tanmātras* (*Sāṃkhya-Kārikā* "
                "22–25). Advaita inherits the Sāṃkhya analysis and "
                "identifies *ahaṃkāra* with one mode of the *antaḥkaraṇa*. "
                "Viśiṣṭādvaita and Tattva-vāda treat *ahaṃkāra* as a real "
                "*prakṛti*-function whose appropriations are *upādhi*-"
                "relative."
            ),
            "register_axes_note": (
                "Same Φ+M register, same scope-inside (I-making function). "
                "Real disagreement only at the M-level on whether the "
                "*ahaṃkāra* belongs to a *jīva* eternally distinct from "
                "*Īśvara* (Tattva-vāda, Viśiṣṭādvaita) or to the *adhyāsa*-"
                "ridden seeker whose I-appropriation will dissolve at "
                "*jñāna* (Advaita)."
            ),
        },
        "register_tags": {
            "Sāṃkhya / Yoga": "M+Φ; mumukṣu / yogin (prakṛti-evolute)",
            "Advaita": "Φ+S; mumukṣu (antaḥkaraṇa-mode dissolving in jñāna)",
            "Viśiṣṭādvaita": "M+Φ; prapanna (real upādhi of jīva)",
            "Tattva-vāda": "M+Φ; Tattvavādin (real prakṛti-function)",
        },
    },
    "antahkarana": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Antaḥkaraṇa* names **the inner instrument: the composite "
                "cognitive apparatus comprising *manas*, *buddhi*, "
                "*ahaṃkāra* (and in Advaita *citta*)** that mediates "
                "between *jñātā* and *jñeya*. Sāṃkhya-Yoga formalizes it "
                "as the threefold *antaḥkaraṇa* (*Sāṃkhya-Kārikā* 33). "
                "Advaita reads the *antaḥkaraṇa* as the *upādhi* that "
                "individuates the *kūṭastha-sākṣin* into the *jīva*. "
                "Viśiṣṭādvaita and Tattva-vāda treat the *antaḥkaraṇa* as "
                "an *aprākṛta* or *prākṛta* instrument truly belonging to "
                "the *jīva*."
            ),
            "register_axes_note": (
                "Same Φ+M register; same scope-inside (inner instrument "
                "between subject and object). Real disagreement only at "
                "the M-level on whether the *antaḥkaraṇa* is *upādhi* "
                "(Advaita) or *svarūpa*-related instrument (theistic "
                "Vedāntas). Methodology Case 4 register-pattern."
            ),
        },
        "register_tags": {
            "Sāṃkhya / Yoga": "M+Φ; yogin (threefold antaḥkaraṇa)",
            "Advaita": "Φ+M; mumukṣu (upādhi individuating sākṣin)",
            "Viśiṣṭādvaita": "M+Φ; prapanna",
            "Tattva-vāda (Dvaita)": "M+Φ; Tattvavādin",
        },
    },
    "buddhi": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Buddhi* names **the determinative cognitive function: "
                "the *adhyavasāya*-faculty that fixes its object as "
                "*idam*-such-and-such**, paradigmatically defined at "
                "*Sāṃkhya-Kārikā* 23 (*adhyavasāyo buddhiḥ*) and at *YS* "
                "2.6. All Brāhmaṇical schools accept the structural role. "
                "Advaita treats *buddhi* as a *vṛtti*-bearing *upādhi* "
                "whose *akhaṇḍākāra-vṛtti* is the proximate locus of "
                "*brahma-jñāna*. Viśiṣṭādvaita and Tattva-vāda treat "
                "*buddhi* as a real *prakṛti*-evolute proper to the "
                "*jīva*."
            ),
            "register_axes_note": (
                "Same Φ+E register, same scope-inside. Real disagreement "
                "only at the M-level on whether *buddhi* is an *upādhi* "
                "or an integral *prakṛti*-evolute of the *jīva* — same "
                "pattern as *antaḥkaraṇa* and *ahaṃkāra*."
            ),
        },
        "register_tags": {
            "Advaita": "Φ+E; mumukṣu",
            "Viśiṣṭādvaita": "M+Φ; prapanna",
            "Tattva-vāda": "M+Φ; Tattvavādin",
            "Bhedābheda": "M+Φ; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },
    "manas": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Manas* names **the sense-coordinating cognitive function: "
                "the inner sense (*antar-indriya*) that synthesizes "
                "discrete sense-data and presents them to *buddhi***. "
                "*Sāṃkhya-Kārikā* 27 fixes *manas* as the *saṅkalpaka* "
                "function. *Nyāya-Sūtra* 1.1.16 treats it as an atomic "
                "internal sense. All Brāhmaṇical schools share the "
                "structural role."
            ),
            "register_axes_note": (
                "Same Φ+E register, same scope-inside. Real disagreement "
                "only at the M-level: Nyāya-Vaiśeṣika treats *manas* as "
                "*aṇu* (atomic), Sāṃkhya as a *prakṛti*-evolute, Advaita "
                "as an *upādhi*-mode. Methodology AF1 holds on the *aṇu* "
                "question between Nyāya and Sāṃkhya."
            ),
        },
        "register_tags": {
            "Advaita": "Φ+M; mumukṣu (upādhi-mode)",
            "Viśiṣṭādvaita": "M+Φ; prapanna",
            "Tattva-vāda": "M+Φ; Tattvavādin",
            "Bhedābheda": "M+Φ; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },
    "citta": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Citta* names **the mental continuum: the field of "
                "cognitive episodes whose stabilization is the "
                "soteriological target**. Yoga gives the paradigm "
                "definition with *yogaś citta-vṛtti-nirodhaḥ* (*YS* 1.2). "
                "Buddhist *citta* (especially in Yogācāra) names the "
                "cognitive stream itself, structured by *vāsanā* and "
                "potentially identical with *ālaya-vijñāna* (*Triṃśikā* "
                "1–5). Advaita treats *citta* as one of the four "
                "*antaḥkaraṇa*-functions: the *anusandhāna*-faculty."
            ),
            "register_axes_note": (
                "**Different concept** at the M-level between Yogācāra's "
                "*citta-mātra* (mind-only, vijñapti-stream) and Vedāntic "
                "*citta* (one cognitive function within the *antaḥkaraṇa* "
                "of a substantial *jīva*). Same Φ-register on the *vṛtti*-"
                "stream description. Yoga's *citta* is operationally "
                "neutral between these readings (Patañjali's *YS* does "
                "not commit on whether *citta* is *prākṛta-pariṇāma* or "
                "*vijñapti*-mātra)."
            ),
        },
        "register_tags": {
            "Advaita": "Φ+M; mumukṣu (antaḥkaraṇa-function)",
            "Viśiṣṭādvaita": "M+Φ; prapanna",
            "Tattva-vāda": "M+Φ; Tattvavādin",
            "Bhedābheda": "M+Φ; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
        },
    },

    # ---- 7. Substance-relation cluster ----
    "amsa": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Aṃśa* names **a part: a constituent that stands in a "
                "part-whole relation to its whole**. The structural role is "
                "shared. Vedāntic schools dispute the *jīva*'s status as "
                "*aṃśa* of Brahman: Viśiṣṭādvaita and Tattva-vāda treat the "
                "*jīva* as real *aṃśa*; Nimbārka and Vallabha treat the "
                "*jīva* as *svābhāvika* *aṃśa* / *aṃśa-śakti*; Advaita "
                "treats the *jīva* as *aṃśa* of Brahman only "
                "*aupacārikally*, since Brahman is *niravayava*."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on whether Brahman can have "
                "*aṃśas* at all. Same M-register, same scope-inside. "
                "Advaita reads BS 2.3.43 (*aṃśo nānā-vyapadeśāt*) as a "
                "*pedagogical* surface; theistic Vedāntas read the same "
                "sūtra as a constructive M-thesis. Methodology Cases 3–5."
            ),
        },
        "register_tags": {
            "Advaita": "P+M; mumukṣu (aṃśa as aupacārika)",
            "Viśiṣṭādvaita": "M+S; prapanna [REAL-DISAGREEMENT: jīva as real aṃśa]",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Bhedābheda": "M+S; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta (svābhāvika aṃśa)",
            "Śuddhādvaita": "M+S; bhakta (aṃśa-śakti)",
        },
    },

    # ---- 8. Buddhist cluster ----
    "sunyata": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Śūnyatā* names **the emptiness of *svabhāva*: the "
                "ontological structure that no dharma has self-standing "
                "essential nature**, fixed by *Mūla-Madhyamaka-Kārikā* "
                "24.18 (*yaḥ pratītyasamutpādaḥ śūnyatāṃ tāṃ pracakṣmahe*). "
                "Mādhyamaka and Yogācāra share the structural role. They "
                "differ on whether *śūnyatā* is (i) the absence of "
                "*svabhāva* alone (Mādhyamaka) or (ii) the *parinispanna* "
                "absence of *parikalpita* on the *paratantra* substrate "
                "(Yogācāra, *Madhyānta-Vibhāga* I.1)."
            ),
            "register_axes_note": (
                "Same LD+M register, same scope-inside, real disagreement "
                "on substrate: Yogācāra's *śūnyatā* presupposes *para-"
                "tantra-svabhāva* as bearer; Mādhyamaka's *śūnyatā* "
                "presupposes none (*sarva-dharma-nairātmya*). Methodology "
                "AF1 holds. **Real disagreement** with Advaita: Advaita's "
                "*nirviśeṣa-brahman* is a positive substrate; Mādhyamaka's "
                "*śūnyatā* is non-substantialist (*Madhyamakāvatāra* 6)."
            ),
        },
        "register_tags": {
            "Mādhyamaka": "LD+M; reflective reader (no svabhāva)",
            "Yogācāra": "M+E; reflective reader (parinispanna on paratantra)",
            "Advaita": "M+LD; mumukṣu [REAL-DISAGREEMENT: positive substrate vs. śūnya]",
            "Viśiṣṭādvaita and Tattva-vāda (Dvaita)": "M+LD; polemicist [REAL-DISAGREEMENT: śūnya-vāda rejected]",
        },
    },
    "pratitya-samutpada": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Pratītya-samutpāda* names **dependent co-arising: the "
                "ontological-causal structure by which every conditioned "
                "*dharma* arises in dependence on others** (*Mahāvagga* "
                "I.1; *MMK* 24.18). All Buddhist schools share the "
                "structural role; Mādhyamaka reads it as the criterion of "
                "*śūnyatā*. Yogācāra reads the twelvefold chain through "
                "the *ālaya-vijñāna*'s *vāsanā*-conditioning. Vedānta "
                "(Bādarāyaṇa, Śaṅkara) engages the doctrine polemically at "
                "BS 2.2.18–27."
            ),
            "register_axes_note": (
                "Same LD+M register within Buddhism, differing scope-"
                "inside on whether the chain depends on a *vijñāna-"
                "pariṇāma* substrate. **Real disagreement** with Vedānta: "
                "Vedānta requires a Brahman-substrate the Buddhist doctrine "
                "denies. Methodology AF1: BS 2.2.18–27 is a genuine LD+M "
                "disagreement, not a register-artifact."
            ),
        },
        "register_tags": {
            "Mādhyamaka": "LD+M; reflective reader (śūnyatā-criterion)",
            "Yogācāra": "M+Φ; reflective reader (ālaya-conditioning)",
            "Vedānta (Bādarāyaṇa, Śaṅkara)": "LD+M; polemicist [REAL-DISAGREEMENT: substrate required]",
        },
    },
    "catuskoti": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Catuṣkoṭi* names **the four-cornered exhaustion of "
                "predicational positions: P, ¬P, both, neither**. "
                "Mādhyamaka uses *catuṣkoṭi* to refuse every metaphysical "
                "position on ultimate questions (*MMK* 25.17; Candrakīrti). "
                "Nyāya rejects the third and fourth corners as logically "
                "incoherent. Advaita selectively endorses the negative "
                "corners as part of *neti neti*-praxis (*BṛU* 2.3.6)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Mādhyamaka's "
                "endorsement and Nyāya's rejection of the four-corner "
                "schema. Same LD-register, opposing claims. Advaita's use "
                "is **a different operation**: not exhaustive predicational "
                "negation but apophatic withdrawal from objectivation "
                "(methodology Case 2 register pattern)."
            ),
        },
        "register_tags": {
            "Mādhyamaka": "LD; reflective reader (prasaṅga-discipline)",
            "Nyāya": "LD; reflective reader [REAL-DISAGREEMENT: third/fourth corners incoherent]",
            "Advaita": "S+Φ; mumukṣu [different operation: apophatic withdrawal]",
        },
    },
    "syad-vada": {
        "framing": {
            "framing_status": "different_concepts",
            "shared_core": (
                "*Syād-vāda* names **the Jain seven-fold conditioned-"
                "predication: every claim is qualified by *syāt* ('from a "
                "standpoint') and distributed across seven modes** "
                "(*Sūtra-kṛtāṅga*; Akalaṅka's *Aṣṭa-śatī*). The Brāhma-"
                "ṇical schools cited in the entry do not have an internal "
                "doctrine answering to *syād-vāda*; they engage it "
                "polemically. Methodology Case 8 takes *syādvāda* as a "
                "discipline-of-predication, not a metaphysical thesis."
            ),
            "register_axes_note": (
                "**Different concept** outside Jainism: when Advaita, "
                "Viśiṣṭādvaita, Tattva-vāda, etc. discuss *syād-vāda* "
                "they engage the Jain doctrine as *pūrva-pakṣa* and "
                "refuse its discipline. *Syād-vāda* is SL+LD+E in "
                "register (methodology §1 SL); the Brāhmaṇical engagement "
                "is LD. Genuine cross-tradition convergence with "
                "Nietzschean perspectivism is partial (Case 8); convergence "
                "with KCB's alternative-absolutes is closer (KCB explicitly "
                "endorses the Jain naya-pluralism)."
            ),
        },
        "register_tags": {
            "Jainism": "SL+LD+E; reflective reader (syādvāda-discipline)",
            "Advaita": "LD; polemicist [REAL-DISAGREEMENT: rejected]",
            "Viśiṣṭādvaita": "LD; polemicist [REAL-DISAGREEMENT: rejected]",
            "Tattva-vāda": "LD; polemicist [REAL-DISAGREEMENT: rejected]",
        },
    },

    # ---- 9. Position-school names ----
    "advaita": {
        "framing": {
            "framing_status": "different_concepts",
            "shared_core": (
                "*Advaita* in the per-school entry's invariant sense names "
                "**a non-duality thesis: the position that the ultimate is "
                "without internal differentiation and without a real "
                "second**. The classical Advaita-Vedānta of Śaṅkara is the "
                "principal home (*Brahma-Sūtra-Bhāṣya*; *Upadeśa-"
                "Sāhasrī*). Other schools listed in the entry engage "
                "*advaita*-language only to reject, qualify, or "
                "reinterpret it: the *śabda* is the same but the doctrinal "
                "position differs. Methodology AF1: this is a "
                "school-position label, not a concept-with-different-"
                "aspects."
            ),
            "register_axes_note": (
                "**Different concepts**: the per-school entries gloss "
                "*advaita* as the doctrinal position each school holds "
                "(Advaita: *jīva-brahman-aikya*; Viśiṣṭādvaita: *śarīra-"
                "śarīrin* unity; Tattva-vāda: *bhedapañcaka*, not unity; "
                "etc.). These are competing M-positions, not different "
                "aspects of one shared concept. Methodology AF1 applies "
                "globally to the term."
            ),
        },
    },
    "dvaita": {
        "framing": {
            "framing_status": "different_concepts",
            "shared_core": (
                "*Dvaita* in the per-school entry's invariant sense names "
                "**a duality thesis: the position that the *jīva* and "
                "*Īśvara* are eternally distinct, with the world's "
                "*bheda*s real and beginningless**. The classical home is "
                "Madhva's Tattva-vāda (*Brahma-Sūtra-Bhāṣya* 1.1.1; *Anu-"
                "vyākhyāna*; *Viṣṇu-Tattva-Vinirṇaya*). Other schools "
                "listed engage *dvaita*-language by rejection or "
                "reinterpretation. Like *advaita*, the per-school entries "
                "list competing M-positions rather than aspects of one "
                "concept."
            ),
            "register_axes_note": (
                "**Different concepts** across the per-school slots: each "
                "school's gloss of *dvaita* is its own doctrinal counter-"
                "position. **Real disagreement** at the M-register among "
                "the listed positions on whether *bheda* is ultimate "
                "(Tattva-vāda: yes; Advaita: no). Methodology Case 3 / "
                "Case 6."
            ),
        },
    },
    "bhedabheda": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Bhedābheda* names **the position that *jīva-Brahman* is "
                "simultaneously different and non-different**. The "
                "structural role is shared by Bhāskara, Yādava-Prakāśa, "
                "Nimbārka (*Dvaitādvaita*), and Caitanya / Jīva Gosvāmī "
                "(*Acintya-Bhedābheda*). They disagree on (i) whether "
                "*bheda* is *aupādhika* (Bhāskara) or *svābhāvika* "
                "(Nimbārka), and (ii) whether the *bhedābheda* relation is "
                "fully analyzable (Bhāskara, Nimbārka) or *acintya* "
                "(Caitanya, Jīva Gosvāmī)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) at the M-register among the "
                "four *bhedābheda* sub-positions: same scope-inside (the "
                "*jīva*-Brahman relation), opposing claims on the *bheda*-"
                "*abheda* simultaneity's structural ground. Methodology "
                "Cases 4 and 5 — *aupādhika* vs. *svābhāvika* vs. *acintya*."
            ),
        },
        "register_tags": {
            "Bhedābheda (Bhāskara)": "M+E; reflective reader (aupādhika, Case 4)",
            "Yādava-Prakāśa": "M+E; reflective reader",
            "Dvaitādvaita (Nimbārka)": "M+S; bhakta (svābhāvika, Case 4) [REAL-DISAGREEMENT with Bhāskara]",
            "Acintya-Bhedābheda": "M+AD; bhakta (acintya, Case 5) [REAL-DISAGREEMENT with both]",
        },
    },
    "acintya": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Acintya* names **what cannot be exhausted by *cintā* / "
                "conceptual analysis: that whose structure resists full "
                "logical reduction**. Gauḍīya theology develops *acintya-"
                "śakti* as the constructive M-thesis that the *bheda-"
                "abheda* simultaneity is held by inconceivable power "
                "(Jīva Gosvāmī, *Sat-Sandarbha*). *Bhāgavata Vaiṣṇava* "
                "theology uses *acintya* more broadly to mark "
                "*aprākṛta*-aspects of Hari. Methodology AF4: *acintya* "
                "is *not* a universal solvent — it is a determinate "
                "philosophical move."
            ),
            "register_axes_note": (
                "Same M-register, differing scope: the *acintya-śakti* "
                "of Gauḍīya is the *jīva-Brahman* relation; the broader "
                "*Bhāgavata* use names *aprākṛta*-attributes of Hari. "
                "Methodology Case 5: the *acintya* move is genuine "
                "philosophical position, refusing reduction without "
                "collapsing into obscurantism."
            ),
        },
        "register_tags": {
            "Acintya-Bhedābheda": "M+AD; bhakta (acintya-śakti, Case 5)",
            "Bhāgavata Vaiṣṇava Theology": "M+AD; bhakta (aprākṛta-aspects)",
        },
    },
}


def main() -> None:
    for term, payload in TERMS.items():
        apply(term, payload["framing"], payload.get("register_tags"))


if __name__ == "__main__":
    main()
