#!/usr/bin/env python3
"""
Apply `school_framing` preambles to glossary entries.

The framing-status options are:
  - same_concept_different_aspect
  - real_disagreement
  - different_concepts
  - mixed

Per the methodology in
/orcd/pool/008/eeshan/philosophy_articles/scope_register_methodology/methodology/
SCOPE_REGISTER_FRAMEWORK.md, the structural BY-SCHOOL display in the popover
falsely implies that schools name *different concepts*. In most cases they name
the *same concept* under different registers, scopes, or addressees. Only where
the primary texts sustain a real disagreement (same register + same scope-inside
+ same addressee, AF1) is the difference conceptual. This script attaches a
preamble field that the renderer surfaces above the per-school breakdown.

Each `register_tag` is the operational tuple summary from the methodology's §7:
abbreviated as (primary register; addressee). Where the existing definition's
primary citations clearly fix the register/addressee, this script sets a tag.
Where they do not, the field is left unset.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
GLOSS = ROOT / "data" / "glossary"


def reorder(d: dict) -> dict:
    """Insert `school_framing` between `invariant_definition` and `per_school`."""
    if "school_framing" not in d:
        return d
    keys = list(d.keys())
    # Move school_framing right after invariant_definition.
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
# Per-term framings. Each block carries (a) the methodology judgment with
# primary-text grounding, (b) a shared_core (one or two sentences), and
# (c) a register_axes_note explaining which register/scope axis the schools
# differ on.
# -------------------------------------------------------------------------

TERMS = {
    "dharma": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "Across schools that share the *śabda* *dharma*, the term names "
                "**that which upholds an order—ritual, ethical, ontological, or "
                "soteriological—and orients its bearer toward a highest end**. "
                "Mīmāṃsā fixes the *lakṣaṇa* as *codanā-lakṣaṇo 'rtho dharmaḥ* "
                "(Jaimini 1.1.2); Vaiśeṣika fixes it as *yataḥ abhyudaya-niḥśreyasa-"
                "siddhiḥ sa dharmaḥ* (Vaiśeṣika-Sūtra 1.1.1–2). Both keep the same "
                "structural role; the schools then differ on *which* order is "
                "load-bearing and on the *register* under which *dharma* speaks "
                "(ritual-normative, social, ontological-property, motion-medium, "
                "soteriological)."
            ),
            "register_axes_note": (
                "Schools differ along the register axis (RN / Eth / M / S) and the "
                "addressee axis (*adhikārin* of ritual vs. *mumukṣu* vs. *bhakta*), "
                "not on the underlying word's structural role. Genuine "
                "disagreements survive: Mādhyamaka denies the realist *dharma*-"
                "ontology that Vaiśeṣika asserts (AF1: same register LD/M, same "
                "scope-inside *dharma*-realism, real disagreement); Jainism's "
                "*dharmāstikāya* gives *dharma* a *different concept* — motion-"
                "medium *dravya*, not normative principle."
            ),
        },
        "register_tags": {
            "Advaita": "P+S; mumukṣu",
            "Viśiṣṭādvaita": "M+S; bhakta/prapanna",
            "Tattva-vāda": "M+LD; polemicist/Tattvavādin",
            "Acintya-Bhedābheda": "AD+S; bhakta",
            "Śuddhādvaita": "M; bhakta",
            "Sāṃkhya": "C+S; mumukṣu",
            "Yoga": "Mh+S; yogin",
            "Nyāya-Vaiśeṣika": "M+E; philosophical reader",
            "Pūrva-Mīmāṃsā": "RN+SL+Eth; adhikārin of ritual",
            "Mādhyamaka": "LD+S; reflective reader",
            "Yogācāra": "Φ+E; reflective reader",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
            "Jainism": "M+C; reflective reader [different concept: motion-medium]",
        },
    },
    "karma": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "All schools that retain the *śabda* *karma* mean **action together "
                "with the residual efficacy by which it links agent, cause, and "
                "later result**. The grammar is Pāṇinian (the *kāraka* role *karman* "
                "fixes 'that which is acted upon'); the metaphysical extension is "
                "the action-trace-fruition triad. Schools then differ on (i) the "
                "carrier of residual efficacy (*apūrva*, *adṛṣṭa*, *vāsanā*, "
                "*karma-pudgala*, *kārma-mala*), (ii) whether agency belongs to "
                "*puruṣa* or to *prakṛti*/*citta*/Śiva-*śakti*, and (iii) whether "
                "*karma* itself or *jñāna*/*bhakti*/*śūnyatā* removes bondage."
            ),
            "register_axes_note": (
                "Mīmāṃsā speaks in RN+SL; Advaita and Viśiṣṭādvaita in S+E; Sāṃkhya "
                "in C+S; Buddhism in Φ+S without an enduring agent; Jainism gives "
                "*karma* a partially *different concept* (literal material "
                "*pudgala* adhering to the *jīva*). Where schools share the same "
                "register and scope (e.g., whether *karma* can directly produce "
                "*mokṣa*), the disagreement is real (Mīmāṃsā vs. Advaita on "
                "*jñāna-karma-samuccaya*; AF1)."
            ),
        },
        "register_tags": {
            "Advaita": "S+E; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin",
            "Acintya-Bhedābheda": "AD+S; bhakta",
            "Sāṃkhya": "C+S; mumukṣu",
            "Yoga": "Φ+S; yogin",
            "Nyāya-Vaiśeṣika": "M+Eth; philosophical reader",
            "Pūrva-Mīmāṃsā": "RN+SL; adhikārin",
            "Mādhyamaka": "LD+Φ+S; reflective reader",
            "Yogācāra": "Φ+E; reflective reader",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
            "Jainism": "M+S; reflective reader [partially different concept: material pudgala]",
        },
    },
    "moksa": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "Every school that retains the word *mokṣa* (or *apavarga*/"
                "*kaivalya*/*nirvāṇa*) means **the non-returning condition in which "
                "the structures that sustain saṃsāric agency, enjoyment, and "
                "compulsory embodiment no longer bind**. The differentia of *mokṣa* "
                "is therefore set by what each school takes *bandha* to be: "
                "*avidyā* (Advaita), distance from Bhagavān (Viśiṣṭādvaita, "
                "Tattva-vāda, Gauḍīya, Śuddhādvaita), *puruṣa-prakṛti-saṃyoga* "
                "(Sāṃkhya-Yoga), *duḥkha-pravṛtti-mithyājñāna* (Nyāya), "
                "*prapañca-vikalpa* (Mādhyamaka), karmic *pudgala* (Jainism), or "
                "contracted *aiśvarya* (Trika)."
            ),
            "register_axes_note": (
                "**Same concept, different aspect** with respect to the structural "
                "role 'non-returning end-state'. **Real disagreement** (AF1) "
                "between Advaita (*jīva–Brahman* identity in *mokṣa*) and "
                "Tattva-vāda (*jīveśvara-bheda* persists, with *taratamya* among "
                "the liberated; *Anuvyākhyāna* 2.3.66–69, *Viṣṇu-Tattva-Vinirṇaya* "
                "3.27) — same M-register, same scope-inside, opposing claims. "
                "Gauḍīya treats ordinary *mokṣa* as lower than *prema* "
                "(*Bhakti-Rasāmṛta-Sindhu* 1.1.11–16): real disagreement about "
                "ranking, not about what *mokṣa* itself names."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT with Advaita on jīveśvara-identity]",
            "Acintya-Bhedābheda": "AD+S; bhakta [REAL-DISAGREEMENT on prema > mokṣa]",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "M+S; mumukṣu",
            "Yoga": "S+Mh; yogin",
            "Nyāya-Vaiśeṣika": "M+S; reflective reader",
            "Mādhyamaka": "LD+S; reflective reader",
            "Yogācāra": "Φ+S; reflective reader",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
            "Jainism": "M+S; reflective reader",
        },
    },
    "brahman": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "Within Vedānta, *brahman* names **the ultimate referent of "
                "Upaniṣadic inquiry: that from which the world arises, by which it "
                "is sustained, into which it resolves, and on knowing which "
                "saṃsāra is ended** (Taittirīya 3.1.1; *janmādy asya yataḥ*, "
                "Brahma-Sūtra 1.1.2). Every Vedāntic school agrees that *brahman* "
                "is the purport of the Upaniṣads and the *jagat-kāraṇa*. They "
                "differ on whether *brahman* is *nirviśeṣa* (Advaita) or *saviśeṣa* "
                "(Viśiṣṭādvaita, Tattva-vāda, Gauḍīya, Nimbārka, Vallabha), and on "
                "how *jīva* and world stand to it (apparent appearance, real mode, "
                "real *aṃśa*, real *pariṇāma*, *acintya-bhedābheda*)."
            ),
            "register_axes_note": (
                "Vedāntic schools speak in the same M-register about the same "
                "scope-inside (*jagat-kāraṇa*, *jñeya*); they genuinely disagree "
                "(AF1) on whether differentiation belongs to *brahman* itself. "
                "Non-Vedāntic appearances are partial or *different concept*: "
                "Mīmāṃsā's *brahman*-language is ritual-priestly, not metaphysical; "
                "Sāṃkhya commentary glosses it as *avyakta/prakṛti*; Buddhists "
                "have no *brahman* as substrate but use *paramārtha/tathatā* as "
                "functional analogues."
            ),
        },
        "register_tags": {
            "Advaita-pre": "M; reflective reader",
            "Advaita": "M+E; mumukṣu [REAL-DISAGREEMENT vs. Viśiṣṭādvaita/Tattva-vāda on nirviśeṣatva]",
            "Viśiṣṭādvaita": "M+S; prapanna [REAL-DISAGREEMENT vs. Advaita on saviśeṣatva]",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT vs. Advaita on jīveśvara-bheda]",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "C; reflective reader [different concept: avyakta/prakṛti]",
            "Yoga": "Φ+M; yogin",
            "Sāṃkhya-Yoga (synthetic)": "M+S; yogin",
            "Nyāya-Vaiśeṣika": "M+E; reflective reader [functional analogue: Īśvara]",
            "Pūrva-Mīmāṃsā": "RN; adhikārin [different concept: priestly designata]",
            "Mādhyamaka": "LD+M; reflective reader [no brahman; functional analogue paramārtha/tathatā]",
            "Yogācāra": "Φ+M; reflective reader [functional analogue: tathatā/vijñaptimātratā]",
            "Pratyabhijñā / Trika": "M+S; sādhaka",
        },
    },
    "atman": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "Within the Brāhmaṇical schools, *ātman* names **the strict "
                "referent of 'I' after the body-mind complex has been bracketed: "
                "the subject for whom experience occurs and who persists through "
                "embodiment** (Bṛhadāraṇyaka 2.4, 3.7, 4.3–4). All Brāhmaṇical "
                "schools admit such a referent and treat *neti neti* (BṛU 2.3.6) "
                "as its delimitative method. They disagree on whether the witness-"
                "self is identical with *brahman* (Advaita), a real mode of "
                "*brahman* (Viśiṣṭādvaita), an eternally distinct atom-knower "
                "(Tattva-vāda, Nimbārka, Nyāya-Vaiśeṣika), or self-luminous "
                "consciousness as agent (Trika)."
            ),
            "register_axes_note": (
                "**Same concept, different aspect** among the Vedāntins on the "
                "structural role 'strict referent of I'. **Real disagreement** "
                "between Advaita and Tattva-vāda/Dvaitādvaita on whether "
                "individuation is intrinsic or *upādhi*-conditioned (AF1: same M-"
                "register, same scope-inside). Buddhist *anātman* is **a different "
                "claim about the same scope**: Mādhyamaka and Yogācāra deny that "
                "anything answering to the *ātman*-description is found, so the "
                "disagreement is real and stated within the same register (E+Φ)."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT with Advaita on jīveśvara-bheda]",
            "Bhedābheda": "M+S+RN; upāsaka",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "M+E; reflective reader (puruṣa)",
            "Yoga": "Φ+E; yogin (draṣṭṛ/puruṣa)",
            "Nyāya-Vaiśeṣika": "M+E; reflective reader (substrate of cognition)",
            "Pūrva-Mīmāṃsā": "RN+E; adhikārin",
            "Mādhyamaka": "Φ+S; reflective reader [REAL-DISAGREEMENT: anātman]",
            "Yogācāra": "Φ+E; reflective reader [REAL-DISAGREEMENT: ātman as upacāra in vijñāna-pariṇāma]",
            "Pratyabhijñā / Trika": "M+Φ; sādhaka",
            "Jainism": "M+S; reflective reader (jīva as substance with upayoga)",
        },
    },
    "jiva": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Jīva* names **the living, embodied subject as bearer of agency, "
                "enjoyership, bondage, and rebirth**: the self under the conditions "
                "of *saṃsāra* (Bṛhadāraṇyaka 4.4.5–7). Every school that retains "
                "the term agrees on this structural role; they disagree on whether "
                "individuality is *upādhi*-conditioned (Advaita, Bhāskara), real-"
                "but-modal (Viśiṣṭādvaita), eternally and intrinsically distinct "
                "(Tattva-vāda), an *aṃśa-śakti* (Nimbārka, Vallabha), or *acintya-"
                "bhedābheda* (Gauḍīya)."
            ),
            "register_axes_note": (
                "**Same concept, real disagreement** among Vedāntins on whether "
                "*jīva*'s individuation is *svarūpa*-grounded or *upādhi*-grounded "
                "(AF1: cf. Bhāskara vs. Nimbārka, methodology Case 4; Madhva vs. "
                "Advaita, methodology Case 3). Sāṃkhya-Yoga uses *puruṣa* for the "
                "functional analogue. Buddhists deny any enduring *jīva* (real "
                "disagreement, same Φ-register). Jainism treats *jīva* as a real "
                "tattva-substance enmeshed in karmic matter — partially "
                "*different concept* in its material-bondage construal."
            ),
        },
        "register_tags": {
            "Advaita": "M+S; mumukṣu",
            "Viśiṣṭādvaita": "M+S; prapanna",
            "Tattva-vāda": "M+S; Tattvavādin [REAL-DISAGREEMENT with Advaita on bhedapañcaka]",
            "Acintya-Bhedābheda": "M+AD; bhakta",
            "Dvaitādvaita": "M+S; bhakta",
            "Śuddhādvaita": "M+S; bhakta",
            "Sāṃkhya": "M; reflective reader (puruṣa)",
            "Yoga": "Φ+S; yogin (draṣṭṛ under saṃyoga)",
            "Nyāya-Vaiśeṣika": "M+E; reflective reader",
            "Pūrva-Mīmāṃsā": "RN+E; adhikārin (yajamāna)",
            "Mādhyamaka": "Φ+LD; reflective reader [REAL-DISAGREEMENT: no jīva-substance]",
            "Yogācāra": "Φ+E; reflective reader [REAL-DISAGREEMENT: jīva as upacāra]",
            "Pratyabhijñā / Trika": "M+Φ; sādhaka (contracted Śiva)",
            "Jainism": "M+S; reflective reader [partially different concept]",
        },
    },
    "maya": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Māyā* names **the power by which the One appears as many; the "
                "veiling-projecting structure that lets phenomenal multiplicity "
                "stand without compromising the unity of its source** "
                "(Śvetāśvatara 4.10; *māyāṃ tu prakṛtiṃ vidyāt māyinaṃ tu maheśvaram*). "
                "Schools that retain the term agree on this structural role; they "
                "disagree on whether *māyā* is *brahman*'s own real *śakti* "
                "(Vaiṣṇava schools, Trika), Brahman's *anirvacanīya* upādhi "
                "(Advaita), or simply *prakṛti* (Sāṃkhya-Bhikṣu reading)."
            ),
            "register_axes_note": (
                "**Real disagreement** between Advaita (*māyā* as *anirvacanīya*, "
                "*mithyā*, sublatable by *jñāna*) and Tattva-vāda (*māyā* as "
                "*Viṣṇu-saṅkalpa*, real, never sublated; *Viṣṇu-Tattva-Vinirṇaya* "
                "3.21–22) — same M-register, same scope-inside, opposing claims "
                "(AF1). **Same concept, different aspect** when the schools "
                "describe māyā's epistemic effect on *jīva* versus its causal "
                "role in cosmogony."
            ),
        },
    },
    "avidya": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Avidyā* names **the cognitive condition under which the subject "
                "misidentifies, omits, or obscures what would otherwise be "
                "manifest; the epistemic root of saṃsāric agency**. The shared "
                "structural role is the obstruction-of-vidyā. Schools differ on "
                "whether *avidyā* is *anirvacanīya* and *bhāvarūpa* (Advaita), "
                "merely the absence of right cognition (Madhva, Nyāya, Mīmāṃsā), "
                "the first link of *pratītyasamutpāda* (Buddhism), or *kleśa* among "
                "five (Yoga, YS 2.3)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Advaita's positive *bhāvarūpa* "
                "*avidyā* (Brahma-Siddhi 1.1; *Pañcapādikā-Vivaraṇa*) and Madhva's "
                "refutation of any *anirvacanīya* third category "
                "(*Mithyātvānumāna-Khaṇḍana*). **Different concept** in Buddhist "
                "*avidyā* (*pratītyasamutpāda*'s first link, not a positive "
                "*bhāva* on a substrate): the same *śabda* names different *artha* "
                "in Buddhist vs. Advaitic *pratyaya* (methodology §4)."
            ),
        },
    },
    "jnana": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Jñāna* means **cognition / knowledge as a determinate epistemic "
                "state with veridical force**, distinguished from mere *vṛtti*, "
                "*smṛti*, or *śravaṇa*. All Vedāntic and Brāhmaṇical schools treat "
                "*jñāna* as either (a) cognitive episodes whose *pramāṇa* is "
                "shared, or (b) the liberating cognition of the highest object "
                "(Brahman, Bhagavān, *tattva*, or *puruṣa-prakṛti-viveka*). Schools "
                "differ on whether liberating *jñāna* alone suffices "
                "(*jñāna-niṣṭhā*, Advaita), or requires *bhakti*/*upāsanā*/*karma* "
                "as co-operative means."
            ),
            "register_axes_note": (
                "Schools differ on register (E vs. S vs. AD) and on whether "
                "*jñāna* alone is *mokṣa-sādhana*. Real disagreement (AF1) "
                "between Advaita and Mīmāṃsā / Tattva-vāda on *jñāna-karma-"
                "samuccaya* and on whether *jñāna* without *bhakti* is sufficient. "
                "Buddhist *jñāna* (*prajñā*) names cognition of *śūnyatā*/*tathatā* "
                "— same structural role, opposed content."
            ),
        },
    },
    "bhakti": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Bhakti* names **the directed, affective-cognitive orientation of "
                "the self toward the supreme reality—Bhagavān, Iṣṭa-devatā, or "
                "Brahman—as a means and/or end of liberation**. Every theistic "
                "school agrees on this structural role (Nārada-Bhakti-Sūtra; "
                "*Bhakti-Rasāmṛta-Sindhu* 1.1.11). The schools differ on whether "
                "*bhakti* is preparatory (Advaita: *gauṇa-bhakti* under *adhikāra*), "
                "constitutive-of-*prapatti* (Viśiṣṭādvaita; Yāmuna, Vedānta "
                "Deśika), the *sahakāri* of *jñāna* (Śuddhādvaita), the supreme "
                "*puruṣārtha* above *mokṣa* (Gauḍīya; Rūpa Gosvāmī), or one of the "
                "*bhāvas* operating in the *liṅga* (Sāṃkhya, *Sāṃkhya-Kārikā* 23)."
            ),
            "register_axes_note": (
                "Same structural role; the schools speak in different registers "
                "(S/AD/Eth) and to different addressees. Madhusūdana's "
                "*Bhakti-Rasāyana* (methodology Case 7) shows that the *jñānin* "
                "and the *bhakta* register can co-exist in one author; AF8 — "
                "two-register coherence does not collapse the AD vs. S distinction."
            ),
        },
    },
    "prakrti": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Prakṛti* names **the materially manifesting principle: the "
                "*upādāna* of evolved form**, marked by the three *guṇas* "
                "(*Sāṃkhya-Kārikā* 11–13). Sāṃkhya gives the paradigm definition; "
                "Yoga inherits it; Vedāntic schools then reinterpret *prakṛti* as "
                "*brahman*'s real or modal power, not an independent substance."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Sāṃkhya (*prakṛti* "
                "*svatantra*, independent of *puruṣa*) and Vedāntic schools "
                "(*prakṛti* either *brahman*'s *śakti* or *brahman*'s *aṃśa*). "
                "Same M-register, same scope-inside ('the material principle'), "
                "opposing claims on its dependence-status."
            ),
        },
    },
    "purusa": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Puruṣa* names **the conscious witnessing pole that stands "
                "uncombined with material change, for whose sake *prakṛti* "
                "operates** (*Sāṃkhya-Kārikā* 17–19; YS 1.16, 2.20). All schools "
                "that retain the term agree on this witness-structure. Vedāntic "
                "schools then disagree on whether *puruṣa* is plural (Sāṃkhya, "
                "Yoga, Tattva-vāda, Viśiṣṭādvaita) or one with *brahman* (Advaita)."
            ),
            "register_axes_note": (
                "**Real disagreement** on plurality of *puruṣa*s (Sāṃkhya/Yoga: "
                "many; Advaita: *eka*) — same M+E register, same scope-inside, "
                "opposing claims (AF1). **Same concept, different aspect** when "
                "Vaiṣṇava schools use *Puruṣottama* in a saviśeṣa M+AD register "
                "while Sāṃkhya keeps the term strictly Φ+E."
            ),
        },
    },
    "guna": {
        "framing": {
            "framing_status": "different_concepts",
            "shared_core": (
                "The *śabda* *guṇa* is genuinely homonymous across schools and "
                "must not be conflated. (a) In Sāṃkhya-Yoga and Vedānta cosmology, "
                "*guṇa* names **one of the three modes of *prakṛti*: *sattva*, "
                "*rajas*, *tamas*** (*Sāṃkhya-Kārikā* 12–13). (b) In Vaiśeṣika, "
                "*guṇa* is **the second of the *padārthas*: an attribute inherent "
                "in a *dravya*** (*Vaiśeṣika-Sūtra* 1.1.15). (c) In theistic "
                "Vedānta, *brahman* / *Bhagavān* is endowed with *ananta-kalyāṇa-"
                "guṇa* — innumerable auspicious qualities (Rāmānuja, "
                "*Śrī-Bhāṣya* 1.1.1)."
            ),
            "register_axes_note": (
                "These are different *artha* under the same *śabda* "
                "(methodology §4: *śabda*/*artha*/*pratyaya*). The (a) cosmological "
                "*guṇa*-triad and (b) Vaiśeṣika categorial *guṇa* and (c) "
                "Vaiṣṇava *kalyāṇa-guṇa* are not register-translations of one "
                "concept; they are three distinct technical uses that share the "
                "lexeme."
            ),
        },
    },
    "vidya": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Vidyā* names **the cognitive state whose object is correctly "
                "apprehended; the rectifier of *avidyā***. In Vedānta and the "
                "Upaniṣadic background, *vidyā* is paradigmatically *brahma-vidyā* "
                "or *ātma-vidyā*; in Mīmāṃsā, *vidyā* is correct Veda-derived "
                "cognition; in Trika, *vidyā* is recognition of innate *aiśvarya*. "
                "The structural role — rectifying cognition — is shared."
            ),
            "register_axes_note": (
                "Same concept; the schools differ on *what* the *vidyā*'s object "
                "is (Brahman / Bhagavān / *tattva* / *Śiva-svarūpa*) and on "
                "whether *vidyā* is identical with *jñāna*-as-event or with "
                "*upāsanā* (Bhedābheda; methodology §1 P-register)."
            ),
        },
    },
    "pramana": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Pramāṇa* names **a means of valid cognition: that by which a "
                "cognition is established as veridical** (Nyāya-Sūtra 1.1.3; "
                "*Pramāṇa-samuccaya* 1). Every school that operates with the term "
                "agrees on this structural role. Schools differ on (i) which "
                "*pramāṇa*s are admitted (Cārvāka: 1, Buddhists: 2, Sāṃkhya/Yoga: "
                "3, Nyāya: 4, Mīmāṃsā/Vedānta: 6) and (ii) the criterion of "
                "validity (*svataḥ-prāmāṇya* vs. *parataḥ-prāmāṇya*)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on the count and on *prāmāṇya*-"
                "intrinsicism vs. extrinsicism — same E+SL register. Buddhist "
                "*pramāṇa-vyavasthā* (Dignāga, Dharmakīrti) restricts to 2 against "
                "the Brāhmaṇical multiplicity; this is a real disagreement within "
                "the shared concept, not a homonymy."
            ),
        },
    },
    "pratyaksa": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Pratyakṣa* names **direct perceptual cognition produced by "
                "sense-object contact, prior to or apart from inferential or "
                "verbal mediation** (*Nyāya-Sūtra* 1.1.4; *Pramāṇa-samuccaya* 1.3). "
                "All schools agree on this structural role. They differ on (i) "
                "whether *pratyakṣa* is *nirvikalpaka* alone or both *nirvikalpaka* "
                "and *savikalpaka*, (ii) whether *yogi-pratyakṣa* is admitted, and "
                "(iii) what the proper object of perception is (*svalakṣaṇa* vs. "
                "*sāmānya-viśeṣa-saṃyukta*)."
            ),
            "register_axes_note": (
                "Same E-register, same scope-inside. Real disagreement (AF1) "
                "between Buddhist Pramāṇavāda (*pratyakṣa* of *svalakṣaṇa* only; "
                "*Pramāṇa-samuccaya* 1.5) and Nyāya (*pratyakṣa* grasps both "
                "*sāmānya* and *viśeṣa*; *Nyāya-Sūtra* 1.1.4)."
            ),
        },
    },
    "anumana": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Anumāna* names **inferential cognition: cognition of a "
                "*sādhya* by means of a *liṅga* whose *vyāpti* with the *sādhya* "
                "is established** (*Nyāya-Sūtra* 1.1.5; *Hetu-bindu*). All schools "
                "agree on the *liṅga-paramarśa* structure. They differ on the "
                "*vyāpti*-grounding (Buddhists: *svabhāva-* and *kārya-hetu* with "
                "*tādātmya*/*tad-utpatti*; Nyāya: *sāhacarya* + *upādhi-rāhitya*) "
                "and on the number of *avayava*s (Nyāya: 5; Buddhist: 2 or 3)."
            ),
            "register_axes_note": (
                "Same LD+E register, same scope-inside. Real disagreement on "
                "*vyāpti*-formation and *avayava*-count (AF1). Buddhist anti-"
                "realist construal of *sāmānya* shifts what *liṅga*-classes "
                "mean, but the inferential structure is shared."
            ),
        },
    },
    "saksin": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Sākṣin* names **the witness-consciousness: the non-objectual "
                "subject-pole that knows mental episodes without itself being a "
                "mental episode** (BṛU 4.3.7; *Sāṃkhya-Kārikā* 19). Advaita, "
                "Sāṃkhya-Yoga, and Viśiṣṭādvaita all admit this structural role. "
                "Tattva-vāda further appeals to *sākṣi-pratyakṣa* as an epistemic "
                "ground for *jīveśvara-bheda*."
            ),
            "register_axes_note": (
                "Same Φ+E register; same scope-inside ('non-objectual subject-"
                "pole'). Real disagreement only on whether the *sākṣin* is "
                "ultimately one (Advaita) or many (Sāṃkhya, Tattva-vāda, "
                "Viśiṣṭādvaita), and on whether *sākṣi-pratyakṣa* can decide "
                "metaphysical questions (Tattva-vāda: yes; Advaita: only "
                "phenomenologically)."
            ),
        },
    },
    "adhyasa": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Adhyāsa* names **the cognitive structure by which one thing "
                "appears as another: the projection of a property onto a "
                "substrate where it does not belong** (*Adhyāsa-Bhāṣya*; *Nyāya-"
                "Sūtra* 4.2.31–34). All schools that retain the term agree on "
                "this structural role (the rope-snake schema). They disagree on "
                "(i) whether *adhyāsa* requires an *adhiṣṭhāna* and an *avidyā* "
                "(Advaita) or only false cognition (*viparyaya*, Nyāya, "
                "Prābhākara)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) between Śaṅkara's *adhyāsa* (Φ+S+M, "
                "*smṛti-rūpaḥ paratra pūrva-dṛṣṭa-avabhāsaḥ*) and Madhva's "
                "*Mithyātvānumāna-Khaṇḍana* refutation (LD+M). Methodology Case 6: "
                "the disagreement is principally at the LD-register, not at the "
                "Φ-register; the Φ-analysis of misperception is broadly shared."
            ),
        },
    },
    "sabda": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Śabda* names **the phonic-linguistic sign in its capacity to "
                "convey *artha***; the Pāṇinian–Patañjalian *Mahābhāṣya* fixes "
                "the *śabda*/*artha*/*pratyaya* triad (*Paspaśāhnika* on 1.2.45). "
                "All Brāhmaṇical schools share this structural role. Schools "
                "differ on (i) whether *śabda* is an autonomous *pramāṇa* "
                "(Mīmāṃsā, Vedānta: yes; Buddhists, Vaiśeṣika: no, reduces to "
                "*anumāna*), and (ii) whether meaning is built up phonemically "
                "(Patañjali) or grasped as *sphoṭa* (Bhartṛhari)."
            ),
            "register_axes_note": (
                "**Real disagreement** (AF1) on *śabda* as autonomous *pramāṇa* "
                "(same E-register). **Same concept, different aspect** on the "
                "*sphoṭa* vs. phonemic-buildup question — both are SL-register "
                "claims about how meaning is grasped, but they pick out different "
                "*vāc*-levels (methodology §4)."
            ),
        },
    },
    "anubhava": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Anubhava* names **first-hand experiential cognition: cognition "
                "as undergone, not merely reported or inferred**. All schools "
                "that retain the term agree on this structural role. Vedāntic "
                "schools then disagree on whether *brahmānubhava* / *aparokṣa-"
                "anubhava* is the terminus of liberating cognition (Advaita) or "
                "the *jñāna-prema* of *Bhagavad-anubhava* (Gauḍīya, "
                "Viśiṣṭādvaita)."
            ),
            "register_axes_note": (
                "Same Φ+E+S register; differing scope-inside on what the highest "
                "*anubhava*'s object is. Real disagreement only at the level of "
                "*content* of the highest experience."
            ),
        },
    },
    "vyavaharika": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Vyāvahārika* names **the operational, transactional level of "
                "reality: that on which ordinary cognition, action, and language "
                "function**, in contrast to *pāramārthika* (the highest level) "
                "and *prātibhāsika* (the merely apparent). The three-tier "
                "ontology is Advaita's; Mādhyamaka has the analogous *saṃvṛti-"
                "satya* / *paramārtha-satya* two-tier scheme; Tattva-vāda and "
                "Viśiṣṭādvaita reject the three-tier reading altogether."
            ),
            "register_axes_note": (
                "**Real disagreement** on whether the three-tier (or two-tier) "
                "ontology is required at all. Tattva-vāda denies "
                "*vyavahāra*/*paramārtha* tiering (methodology §4's "
                "*vyākaraṇa*-corrective): same M-register, opposing claims (AF1). "
                "Mādhyamaka's two-tier scheme is *analogous-but-different*: the "
                "*saṃvṛti* level is not the same concept as Advaita's "
                "*vyāvahārika*, which presupposes a positive substrate."
            ),
        },
    },
    "paramarthika": {
        "framing": {
            "framing_status": "mixed",
            "shared_core": (
                "*Pāramārthika* names **the ultimate level of reality: that which "
                "is not sublatable by any further cognition**. Advaita pairs it "
                "with *vyāvahārika*; Mādhyamaka pairs *paramārtha-satya* with "
                "*saṃvṛti-satya* (*Mūla-Madhyamaka-Kārikā* 24.8). Viśiṣṭādvaita "
                "and Tattva-vāda reject the two-tier reading and treat the world "
                "itself as *pāramārthika*."
            ),
            "register_axes_note": (
                "**Real disagreement** on the necessity of a two-tier "
                "ontology — same M-register, opposing claims (AF1). Mādhyamaka's "
                "*paramārtha* is dependent on *saṃvṛti* (MMK 24.10) and is not "
                "a positive substrate (*śūnyatā* / *prapañcopaśama*); Advaita's "
                "is *brahman* as positive substrate. **Different concept** at the "
                "level of what *paramārtha* refers to, even though the *śabda* "
                "and the structural role (uppermost truth-level) are shared."
            ),
        },
    },
    "mithya": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Mithyā* names **that which is neither absolutely real "
                "(*sat*) nor absolutely unreal (*asat*) — i.e., *sad-asad-"
                "anirvacanīya***. Advaita and its commentarial tradition develop "
                "this third category (BSB 2.1.14; *Iṣṭa-Siddhi*; *Advaita-Siddhi*). "
                "Other schools refuse the third category: Madhva argues that "
                "*mithyā* must reduce either to *sat* or to *asat* (*Mithyātvānumāna-"
                "Khaṇḍana*); Viśiṣṭādvaita and Śuddhādvaita read *jagat-mithyātva* "
                "language as figurative."
            ),
            "register_axes_note": (
                "Methodology Case 6: real disagreement (AF1) on whether *mithyā* "
                "is a coherent third category. The Advaita-Mādhyamaka apparent "
                "affinity is partial — Mādhyamaka's *śūnyatā* is not Advaita's "
                "*anirvacanīya*. Pedagogically, *mithyā* in Śaṅkara is addressed "
                "to the *mumukṣu* under *adhyāsa* (P+S+M); it does not deny the "
                "world's *vyāvahārika* operativity."
            ),
        },
    },
    "upadhi": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Upādhi* names **a limiting adjunct: a condition that delimits "
                "an entity or property without belonging to its *svarūpa***. "
                "All schools that retain the term agree on this structural role. "
                "Bhāskara's *aupādhika-bhedābheda* (methodology Case 4) uses "
                "*upādhi* to explain *jīva-Brahman bheda*; Nyāya uses it as "
                "*upādhi-rāhitya* in *vyāpti*-construction; Tattva-vāda critiques "
                "the Advaitic use as failing to ground a sufficient cause of "
                "*svarūpa-bhinnatva*."
            ),
            "register_axes_note": (
                "Same E+M register, same structural role. Real disagreement (AF1) "
                "between Bhāskara (*bheda* is *aupādhika*; dissolves at *mokṣa*) "
                "and Nimbārka (*bheda* is *svābhāvika*; persists). Methodology "
                "Case 4."
            ),
        },
    },
    "prapatti": {
        "framing": {
            "framing_status": "same_concept_different_aspect",
            "shared_core": (
                "*Prapatti* names **complete surrender to Bhagavān as the sole "
                "*upāya* and *upeya***: the *akiñcana*-*ananyagati* posture in "
                "which the *jīva* renounces self-effort and rests in divine "
                "*kṛpā* (*Stotra-Ratna* 22–24; *Nyāsa-daśaka*). Viśiṣṭādvaita "
                "(Yāmuna, Rāmānuja, Vedānta Deśika), Gauḍīya, and Vallabha all "
                "operate with this structural role. Advaita does not use "
                "*prapatti* as a primary technical term."
            ),
            "register_axes_note": (
                "Same S+AD register where used; addressee is the *bhakta*/"
                "*prapanna*. Disagreement among the theistic schools is on "
                "*prapatti*'s relation to *bhakti-yoga* (Vaḍakalai: *prapatti* "
                "as one *upāya* among many; Tenkalai: sole *upāya*). The "
                "disagreement is intra-Viśiṣṭādvaita and not at the level of "
                "concept-identity."
            ),
        },
    },
    "anatta": {
        "framing": {
            "framing_status": "different_concepts",
            "shared_core": (
                "*Anātman* / *anatta* names **the Buddhist denial that any "
                "*ātman* answering to the Upaniṣadic description is found among "
                "the *skandhas***. The structural role is denial, not "
                "affirmation; it is therefore not a positive concept in the way "
                "that Brāhmaṇical *ātman* is."
            ),
            "register_axes_note": (
                "Methodology AF1: same Φ+E register and same scope-inside as the "
                "Brāhmaṇical *ātman* discussion — this is **real disagreement** "
                "on the same question, not a register-artifact. The same *śabda* "
                "is used to mean opposed claims about whether an enduring "
                "subject-pole exists. The schools do not 'describe the same "
                "concept from different aspects'; they are answering the same "
                "*ātman*-question with opposite answers."
            ),
        },
    },
    "satkarya-vada": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Satkārya-vāda* names **the thesis that the effect pre-exists "
                "in its material cause prior to manifestation** (*Sāṃkhya-Kārikā* "
                "9). Sāṃkhya and Vedāntic schools that accept it (Viśiṣṭādvaita, "
                "Tattva-vāda's mode of it, Vallabha, Nimbārka) share the "
                "structural claim. Nyāya-Vaiśeṣika defends *asatkārya-vāda*: the "
                "effect is a genuinely new substance produced by inherence in a "
                "novel substrate."
            ),
            "register_axes_note": (
                "Same M+LD register, same scope-inside ('effect-cause modal "
                "structure'), opposing claims (AF1). Advaita's *vivarta-vāda* "
                "is **a different concept** built on *satkārya* as starting "
                "point but adding *anirvacanīya* sublatability — methodology "
                "§4."
            ),
        },
    },
    "parinama": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Pariṇāma* names **real transformation: the cause undergoes "
                "actual modification to produce the effect** (*Sāṃkhya-Kārikā* "
                "16–22; YS 3.13). Sāṃkhya, Yoga, Viśiṣṭādvaita, Tattva-vāda, "
                "Bhāskara, Nimbārka, and Vallabha (under *avikṛta-pariṇāma*) all "
                "accept *pariṇāma*-vāda in some form. Advaita defends *vivarta-"
                "vāda* against it: the cause undergoes only apparent, not real, "
                "modification."
            ),
            "register_axes_note": (
                "Real disagreement (AF1) on whether *brahman*/*prakṛti* really "
                "transforms. Same M-register, same scope-inside, opposing "
                "claims. Vallabha's *avikṛta-pariṇāma* is a third position that "
                "preserves *pariṇāma* while denying that *brahman* is altered "
                "(*Aṇu-Bhāṣya* 1.4.26; methodology Case 1)."
            ),
        },
    },
    "vivarta": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Vivarta* names **apparent transformation: the cause appears "
                "as something other than itself without undergoing real "
                "modification**, paradigmatically the rope-snake schema. "
                "Advaita's *vivarta-vāda* is the principal home of the doctrine; "
                "all *pariṇāmavādin* schools (Sāṃkhya, Viśiṣṭādvaita, Tattva-"
                "vāda, Vallabha) reject it as inadequate to *jagat-kāraṇatva*."
            ),
            "register_axes_note": (
                "Real disagreement (AF1) — same M-register, opposing claims. "
                "Madhva's polemic against *vivarta* is principally LD-register "
                "(*Mithyātvānumāna-Khaṇḍana*; methodology Case 6); Vallabha "
                "deflects it by reading *brahman*'s manifestation as *avikṛta-"
                "pariṇāma*."
            ),
        },
    },
    "bheda": {
        "framing": {
            "framing_status": "real_disagreement",
            "shared_core": (
                "*Bheda* names **real distinction: ontological difference that "
                "does not reduce to *upādhi*-conditioning**. Tattva-vāda makes "
                "*bheda* the fundamental category (*panca-bheda*: five real "
                "distinctions; *Viṣṇu-Tattva-Vinirṇaya*). Bhedābheda schools "
                "admit *bheda* and *abheda* jointly; Advaita restricts *bheda* "
                "to the *vyāvahārika* tier."
            ),
            "register_axes_note": (
                "Real disagreement (AF1) on *bheda*'s ultimacy. Methodology "
                "Cases 3–5: *aprthak-siddhi*, *bimba-pratibimba*, *aupādhika-* "
                "vs. *svābhāvika-bhedābheda*, and *acintya-bhedābheda* are four "
                "*genuinely different* M-positions on the same scope-inside "
                "(*jīva-Brahman* relation)."
            ),
        },
    },
}


def main() -> None:
    for term, payload in TERMS.items():
        apply(term, payload["framing"], payload.get("register_tags"))


if __name__ == "__main__":
    main()
