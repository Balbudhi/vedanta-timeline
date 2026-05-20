#!/usr/bin/env python3

import json
import re
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINKERS_DIR = ROOT / "data" / "thinkers"
REGISTRY_PATH = ROOT / "data" / "registries" / "primitive_graph.json"


def c(primitive, value, register, confidence="medium", notes=None):
    item = {
        "primitive": primitive,
        "value": value,
        "register": register,
        "confidence": confidence,
    }
    if notes:
        item["notes"] = notes
    return item


PRIMITIVES = {
    "substrate_structure": {
        "label": "Substrate Structure",
        "category": "metaphysical",
        "description": "The basic ontological architecture of what is self-standing and what is dependent.",
        "values": [
            "one-self-standing",
            "one-qualified-by-real-internal-distinctions",
            "one-independent-plus-real-dependents",
            "many-coordinate-reals",
            "process-field-with-no-enduring-substrate",
            "anti-essential-relationality",
            "suspended-or-refused",
        ],
    },
    "manifestation_status": {
        "label": "Manifestation Status",
        "category": "metaphysical",
        "description": "The status of the world, appearance, or finite objectivity relative to what grounds it.",
        "values": [
            "self-standing-real",
            "dependent-real",
            "sublatable-not-null",
            "real-transformation",
            "expressive-manifestation",
            "conventionally-real-without-own-being",
            "socially-or-discursively-stabilized",
            "suspended-or-unfixed",
        ],
    },
    "identity_relation": {
        "label": "Identity Relation",
        "category": "metaphysical",
        "description": "The formal relation between ultimate reality, self, and world where unity and difference are both at issue.",
        "values": [
            "numerical-identity",
            "non-otherness",
            "body-soul-qualification",
            "image-original-similarity",
            "natural-difference-non-difference",
            "inconceivable-difference-non-difference",
            "self-expression-or-appearance",
            "no-single-relation-stated",
        ],
    },
    "individuation_status": {
        "label": "Individuation Status",
        "category": "metaphysical",
        "description": "The standing of the individual as individual.",
        "values": [
            "reducible-to-the-whole",
            "qualified-mode",
            "irreducible-dependent",
            "expressive-singularity",
            "transcendental-pole",
            "produced-or-fractured",
            "not-central",
        ],
    },
    "causation_model": {
        "label": "Causation Model",
        "category": "metaphysical",
        "description": "How the finite order issues from its ground, if it does.",
        "values": [
            "appearance-without-real-change",
            "real-transformation",
            "unchanged-ground-with-changing-power",
            "body-soul-causation",
            "efficient-material-split",
            "immanent-expression",
            "processual-concrescence",
            "dependent-co-arising",
            "not-a-cosmogonic-system",
        ],
    },
    "selfhood_structure": {
        "label": "Selfhood Structure",
        "category": "phenomenological",
        "description": "What kind of self or subject is treated as real or operative.",
        "values": [
            "substantial-self",
            "witness-self",
            "relational-self",
            "psychic-individual",
            "transcendental-ego",
            "dasein",
            "split-or-produced-subject",
            "no-enduring-self",
        ],
    },
    "constitution_structure": {
        "label": "Constitution Structure",
        "category": "phenomenological",
        "description": "How subject-object articulation is constituted, or refused, at the level of experience itself.",
        "values": [
            "subject-object-duality-taken-as-basic",
            "intentional-noesis-noema-correlation",
            "storehouse-transformation-of-cognitive-flow",
            "reflexive-self-manifestation",
            "dependent-arising-without-constituting-subject",
            "withheld",
        ],
    },
    "finite_cognition_model": {
        "label": "Finite Cognition Model",
        "category": "epistemological",
        "description": "The account of error, finitude, obscuration, or interpretation.",
        "values": [
            "adhyasa-or-superimposition",
            "positive-ignorance",
            "real-dependent-veiling",
            "contraction-or-obscuration",
            "storehouse-transformation",
            "intentional-constitution",
            "perspectival-interpretation",
            "genealogically-produced-illusion",
            "no-unified-model-given",
        ],
    },
    "epistemic_authority": {
        "label": "Epistemic Authority",
        "category": "epistemological",
        "description": "The dominant source or ordered set of sources by which load-bearing claims are warranted.",
        "values": [
            "scripture-dominant",
            "scripture-plus-transformative-experience",
            "plural-pramana-realism",
            "ritual-injunction",
            "dialectical-immanence",
            "phenomenological-reduction",
            "genealogical-critique",
            "deconstructive-reading",
            "comparative-theological-reading",
            "no-single-authority",
        ],
    },
    "determination_operator": {
        "label": "Determination Operator",
        "category": "logical-dialectical",
        "description": "The main operator by which determinacy or difference is articulated.",
        "values": [
            "negation-and-contradiction",
            "non-sublatable-difference",
            "difference-without-negation",
            "exclusion-or-apoha",
            "self-expression",
            "differential-deferral",
            "genealogical-exposure",
            "ritual-specification",
            "dependent-co-arising",
        ],
    },
    "method_of_critique": {
        "label": "Method of Critique",
        "category": "logical-dialectical",
        "description": "The operative procedure by which claims are advanced, tested, or dismantled.",
        "values": [
            "commentarial-exegesis",
            "formal-proof-or-inference",
            "prasanga-anti-thesis",
            "phenomenological-reduction",
            "dialectical-development",
            "genealogy",
            "deconstruction",
            "comparative-reading",
            "mixed-or-layered",
        ],
    },
    "semantic_mediation": {
        "label": "Semantic Mediation",
        "category": "semantic-linguistic",
        "description": "How language or sign mediates access to reality, action, or objecthood.",
        "values": [
            "language-tracks-reality",
            "language-binds-action",
            "language-constitutes-object-domain",
            "language-differentially-defers-presence",
            "language-as-creative-manifestation",
            "language-subordinate-to-non-propositional-knowing",
        ],
    },
    "temporal_mode": {
        "label": "Temporal Mode",
        "category": "metaphysical",
        "description": "Whether being is framed as substance, process, disclosure, or a layered combination.",
        "values": [
            "substance-primary",
            "process-primary",
            "both-orthogonal",
            "timeless-ground-with-dependent-time",
            "historical-disclosure",
            "no-decision-given",
        ],
    },
    "register_of_evolution": {
        "label": "Register of Evolution",
        "category": "historical-genealogical",
        "description": "How emergence, ascent, or historic transformation is treated.",
        "values": [
            "no-evolution",
            "sublative-becoming",
            "real-cosmological-evolution",
            "durational-creative-growth",
            "graded-manifestation-without-evolution",
            "genealogical-historicization",
            "not-applicable",
        ],
    },
    "modal_structure_of_truth": {
        "label": "Modal Structure of Truth",
        "category": "epistemological",
        "description": "How truth is distributed when multiple standpoints or levels are in play.",
        "values": [
            "single-absolute-truth",
            "hierarchical-standpoint-truth",
            "alternative-irreducible-truths",
            "standpoint-conditioned-realism",
            "paraconsistent-or-both-held",
            "context-indexed-without-final-hierarchy",
        ],
    },
    "relation_to_perspectivism": {
        "label": "Relation to Perspectivism",
        "category": "epistemological",
        "description": "How plurality of viewpoints or standpoints is treated.",
        "values": [
            "sublated-into-higher-whole",
            "irreducible-true-perspectives",
            "partial-perspectives-ranked",
            "standpoint-conditioned-realism",
            "perspectives-as-symptoms",
            "no-perspectivism-claim",
        ],
    },
    "standpoint_predication": {
        "label": "Standpoint Predication",
        "category": "semantic-linguistic",
        "description": "How predication itself is qualified, ranked, or multiplied across standpoints.",
        "values": [
            "single-unqualified-predication",
            "hierarchically-ranked-predication",
            "standpoint-indexed-predication",
            "sevenfold-conditioned-predication",
            "profile-adumbrational-predication",
            "withheld",
        ],
    },
    "normative_order_source": {
        "label": "Normative Order Source",
        "category": "ritual-normative",
        "description": "Where obligation or binding normativity is sourced.",
        "values": [
            "scriptural-injunction",
            "divine-command-or-grace",
            "ethical-life-in-institutions",
            "disciplinary-power",
            "class-structured-social-relation",
            "self-legislating-subject",
            "not-a-central-axis",
        ],
    },
    "social_formation_model": {
        "label": "Social Formation Model",
        "category": "political-social",
        "description": "How institutions, social form, or collective structures generate subjects and objectivity.",
        "values": [
            "not-central",
            "recognitive-institutional",
            "commodity-fetish-social-form",
            "disciplinary-production-of-subjects",
            "performative-norm-repetition",
            "civilizational-structure-shift",
        ],
    },
    "affective_motive_force": {
        "label": "Affective Motive Force",
        "category": "ethical",
        "description": "What fundamentally moves life, practice, or transformation.",
        "values": [
            "knowledge",
            "devotion",
            "will-to-power",
            "bliss-or-delight",
            "desire-and-drive",
            "ethical-obligation-to-the-other",
            "aesthetic-rapture",
            "not-central",
        ],
    },
    "practice_path": {
        "label": "Practice Path",
        "category": "soteriological",
        "description": "The dominant practical path by which transformation or release is pursued.",
        "values": [
            "knowledge-discipline",
            "devotion-and-grace",
            "ritual-observance",
            "meditative-discipline",
            "reduction-or-attentive-description",
            "transformative-integration",
            "critical-genealogical-work",
            "not-soteric",
        ],
    },
    "soteric_end": {
        "label": "Soteric End",
        "category": "soteriological",
        "description": "The final end aimed at or described by the thinker.",
        "values": [
            "identity-with-ground",
            "service-with-distinction-preserved",
            "loving-participation",
            "isolation-or-discriminative-release",
            "recognition-or-freedom",
            "transformation-of-life",
            "ethical-vigilance-without-final-fusion",
            "not-soteriological",
        ],
    },
}


DEPENDENCIES = [
    {"from": "substrate_structure", "to": "manifestation_status"},
    {"from": "substrate_structure", "to": "identity_relation"},
    {"from": "manifestation_status", "to": "causation_model"},
    {"from": "selfhood_structure", "to": "finite_cognition_model"},
    {"from": "selfhood_structure", "to": "constitution_structure"},
    {"from": "constitution_structure", "to": "finite_cognition_model"},
    {"from": "epistemic_authority", "to": "method_of_critique"},
    {"from": "determination_operator", "to": "semantic_mediation"},
    {"from": "temporal_mode", "to": "register_of_evolution"},
    {"from": "modal_structure_of_truth", "to": "relation_to_perspectivism"},
    {"from": "modal_structure_of_truth", "to": "standpoint_predication"},
    {"from": "normative_order_source", "to": "social_formation_model"},
    {"from": "practice_path", "to": "soteric_end"},
]


BASE_PROFILES = {
    "Advaita": [
        c("substrate_structure", "one-self-standing", "metaphysical"),
        c("manifestation_status", "sublatable-not-null", "metaphysical"),
        c("identity_relation", "non-otherness", "metaphysical"),
        c("selfhood_structure", "witness-self", "phenomenological"),
        c("finite_cognition_model", "adhyasa-or-superimposition", "epistemological"),
        c("epistemic_authority", "scripture-dominant", "epistemological"),
        c("modal_structure_of_truth", "hierarchical-standpoint-truth", "epistemological"),
        c("practice_path", "knowledge-discipline", "soteriological"),
        c("soteric_end", "identity-with-ground", "soteriological"),
    ],
    "Viśiṣṭādvaita": [
        c("substrate_structure", "one-qualified-by-real-internal-distinctions", "metaphysical"),
        c("manifestation_status", "dependent-real", "metaphysical"),
        c("identity_relation", "body-soul-qualification", "metaphysical"),
        c("individuation_status", "qualified-mode", "metaphysical"),
        c("causation_model", "body-soul-causation", "metaphysical"),
        c("epistemic_authority", "scripture-dominant", "epistemological"),
        c("normative_order_source", "divine-command-or-grace", "ethical"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "service-with-distinction-preserved", "soteriological"),
        c("modal_structure_of_truth", "single-absolute-truth", "epistemological"),
    ],
    "Tattva-vāda": [
        c("substrate_structure", "one-independent-plus-real-dependents", "metaphysical"),
        c("manifestation_status", "dependent-real", "metaphysical"),
        c("identity_relation", "image-original-similarity", "metaphysical"),
        c("individuation_status", "irreducible-dependent", "metaphysical"),
        c("causation_model", "efficient-material-split", "metaphysical"),
        c("finite_cognition_model", "real-dependent-veiling", "epistemological"),
        c("epistemic_authority", "plural-pramana-realism", "epistemological"),
        c("determination_operator", "non-sublatable-difference", "logical-dialectical"),
        c("method_of_critique", "formal-proof-or-inference", "methodological"),
        c("modal_structure_of_truth", "single-absolute-truth", "epistemological"),
        c("relation_to_perspectivism", "partial-perspectives-ranked", "epistemological"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "service-with-distinction-preserved", "soteriological"),
    ],
    "Acintya-Bhedābheda": [
        c("substrate_structure", "one-independent-plus-real-dependents", "metaphysical"),
        c("manifestation_status", "dependent-real", "metaphysical"),
        c("identity_relation", "inconceivable-difference-non-difference", "metaphysical"),
        c("individuation_status", "irreducible-dependent", "metaphysical"),
        c("causation_model", "unchanged-ground-with-changing-power", "metaphysical"),
        c("epistemic_authority", "scripture-dominant", "epistemological"),
        c("modal_structure_of_truth", "single-absolute-truth", "epistemological"),
        c("relation_to_perspectivism", "partial-perspectives-ranked", "epistemological"),
        c("affective_motive_force", "devotion", "soteriological"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "loving-participation", "soteriological"),
    ],
    "Bhedābheda": [
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("identity_relation", "natural-difference-non-difference", "metaphysical"),
        c("epistemic_authority", "scripture-dominant", "epistemological", "low"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "identity-with-ground", "soteriological", "low"),
    ],
    "Śuddhādvaita": [
        c("substrate_structure", "one-self-standing", "metaphysical"),
        c("manifestation_status", "real-transformation", "metaphysical"),
        c("identity_relation", "self-expression-or-appearance", "metaphysical"),
        c("causation_model", "real-transformation", "metaphysical"),
        c("epistemic_authority", "scripture-dominant", "epistemological"),
        c("affective_motive_force", "devotion", "soteriological"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "loving-participation", "soteriological"),
    ],
    "Pratyabhijñā/Trika": [
        c("substrate_structure", "one-self-standing", "metaphysical"),
        c("manifestation_status", "expressive-manifestation", "metaphysical"),
        c("identity_relation", "self-expression-or-appearance", "metaphysical"),
        c("selfhood_structure", "relational-self", "phenomenological"),
        c("constitution_structure", "reflexive-self-manifestation", "phenomenological"),
        c("finite_cognition_model", "contraction-or-obscuration", "epistemological"),
        c("epistemic_authority", "scripture-plus-transformative-experience", "epistemological"),
        c("determination_operator", "self-expression", "logical-dialectical"),
        c("semantic_mediation", "language-as-creative-manifestation", "semantic-linguistic"),
        c("affective_motive_force", "aesthetic-rapture", "aesthetic"),
        c("practice_path", "transformative-integration", "soteriological"),
        c("soteric_end", "recognition-or-freedom", "soteriological"),
    ],
    "Pūrva-Mīmāṃsā": [
        c("epistemic_authority", "ritual-injunction", "epistemological"),
        c("determination_operator", "ritual-specification", "logical-dialectical"),
        c("method_of_critique", "commentarial-exegesis", "methodological"),
        c("semantic_mediation", "language-binds-action", "semantic-linguistic"),
        c("normative_order_source", "scriptural-injunction", "ritual-normative"),
        c("practice_path", "ritual-observance", "soteriological"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "Nyāya": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("manifestation_status", "self-standing-real", "metaphysical"),
        c("selfhood_structure", "substantial-self", "phenomenological"),
        c("epistemic_authority", "plural-pramana-realism", "epistemological"),
        c("method_of_critique", "formal-proof-or-inference", "methodological"),
        c("semantic_mediation", "language-tracks-reality", "semantic-linguistic"),
        c("modal_structure_of_truth", "single-absolute-truth", "epistemological"),
        c("practice_path", "knowledge-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    "Navya-Nyāya": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("manifestation_status", "self-standing-real", "metaphysical"),
        c("selfhood_structure", "substantial-self", "phenomenological"),
        c("epistemic_authority", "plural-pramana-realism", "epistemological"),
        c("method_of_critique", "formal-proof-or-inference", "methodological"),
        c("semantic_mediation", "language-tracks-reality", "semantic-linguistic"),
        c("practice_path", "knowledge-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    "Vaiśeṣika": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("manifestation_status", "self-standing-real", "metaphysical"),
        c("selfhood_structure", "substantial-self", "phenomenological"),
        c("semantic_mediation", "language-tracks-reality", "semantic-linguistic"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological", "low"),
    ],
    "Jaina": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("manifestation_status", "self-standing-real", "metaphysical"),
        c("epistemic_authority", "plural-pramana-realism", "epistemological"),
        c("modal_structure_of_truth", "standpoint-conditioned-realism", "epistemological"),
        c("relation_to_perspectivism", "irreducible-true-perspectives", "epistemological"),
        c("standpoint_predication", "standpoint-indexed-predication", "semantic-linguistic"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    "Sāṅkhya": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("manifestation_status", "real-transformation", "metaphysical"),
        c("causation_model", "real-transformation", "metaphysical"),
        c("selfhood_structure", "substantial-self", "phenomenological"),
        c("temporal_mode", "substance-primary", "metaphysical"),
        c("practice_path", "knowledge-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    "Yoga": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical"),
        c("selfhood_structure", "substantial-self", "phenomenological"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    "Process Philosophy": [
        c("substrate_structure", "process-field-with-no-enduring-substrate", "metaphysical"),
        c("manifestation_status", "dependent-real", "metaphysical"),
        c("causation_model", "processual-concrescence", "metaphysical"),
        c("temporal_mode", "process-primary", "metaphysical"),
        c("register_of_evolution", "durational-creative-growth", "historical-genealogical", "low"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "Phenomenology": [
        c("epistemic_authority", "phenomenological-reduction", "epistemological"),
        c("method_of_critique", "phenomenological-reduction", "methodological"),
    ],
    "German Idealism": [
        c("method_of_critique", "dialectical-development", "methodological"),
        c("modal_structure_of_truth", "single-absolute-truth", "epistemological", "low"),
    ],
    "Critical Theory": [
        c("method_of_critique", "dialectical-development", "methodological"),
        c("social_formation_model", "commodity-fetish-social-form", "political-social", "low"),
    ],
    "Integral Yoga": [
        c("manifestation_status", "real-transformation", "metaphysical"),
        c("temporal_mode", "both-orthogonal", "metaphysical"),
        c("register_of_evolution", "real-cosmological-evolution", "historical-genealogical"),
        c("affective_motive_force", "bliss-or-delight", "soteriological"),
        c("practice_path", "transformative-integration", "soteriological"),
        c("soteric_end", "transformation-of-life", "soteriological"),
    ],
    "Neo-Vedanta": [
        c("manifestation_status", "expressive-manifestation", "metaphysical"),
        c("epistemic_authority", "scripture-plus-transformative-experience", "epistemological"),
        c("practice_path", "transformative-integration", "soteriological"),
    ],
    "Avibhāgādvaita": [
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "medium"),
        c("identity_relation", "natural-difference-non-difference", "metaphysical", "low"),
        c("causation_model", "unchanged-ground-with-changing-power", "metaphysical", "low"),
        c("epistemic_authority", "scripture-dominant", "epistemological", "medium"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "identity-with-ground", "soteriological", "low"),
    ],
    "proto-Vedānta": [
        c("epistemic_authority", "scripture-dominant", "epistemological", "low"),
        c("method_of_critique", "commentarial-exegesis", "methodological", "low"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "identity-with-ground", "soteriological", "low"),
    ],
    "Modern Philosophy": [
        c("method_of_critique", "mixed-or-layered", "methodological", "low"),
        c("soteric_end", "not-soteriological", "soteriological", "medium"),
    ],
    "Continental Philosophy": [
        c("method_of_critique", "genealogy", "historical-genealogical", "low"),
        c("soteric_end", "not-soteriological", "soteriological", "medium"),
    ],
    "Bhairava-tantra": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("epistemic_authority", "scripture-plus-transformative-experience", "epistemological", "low"),
        c("practice_path", "transformative-integration", "soteriological", "low"),
        c("soteric_end", "recognition-or-freedom", "soteriological", "low"),
    ],
    "Pāśupata": [
        c("substrate_structure", "one-independent-plus-real-dependents", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological", "low"),
    ],
    "Pāñcarātra": [
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("epistemic_authority", "scripture-dominant", "epistemological", "low"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "service-with-distinction-preserved", "soteriological", "low"),
    ],
    "Vīraśaiva": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("affective_motive_force", "devotion", "soteriological"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "transformation-of-life", "soteriological", "low"),
    ],
    "Cārvāka": [
        c("manifestation_status", "self-standing-real", "metaphysical"),
        c("epistemic_authority", "no-single-authority", "epistemological"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "Comparative Philosophy": [
        c("method_of_critique", "comparative-reading", "methodological"),
    ],
    "Contemporary Philosophy": [
        c("social_formation_model", "performative-norm-repetition", "political-social"),
    ],
    "Modern Vedanta": [
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "identity-with-ground", "soteriological", "low"),
    ],
}


SUBSCHOOL_RULES = [
    ("Vivaraṇa", [
        c("finite_cognition_model", "positive-ignorance", "epistemological"),
    ]),
    ("Bhāmatī", [
        c("finite_cognition_model", "positive-ignorance", "epistemological"),
    ]),
    ("Navya-Tattva-vāda", [
        c("method_of_critique", "formal-proof-or-inference", "methodological", "high"),
    ]),
]


SET_OVERRIDES = {
    frozenset({"nagarjuna", "candrakirti", "bhaviveka"}): [
        c("substrate_structure", "anti-essential-relationality", "metaphysical"),
        c("manifestation_status", "conventionally-real-without-own-being", "metaphysical"),
        c("causation_model", "dependent-co-arising", "metaphysical"),
        c("selfhood_structure", "no-enduring-self", "phenomenological"),
        c("constitution_structure", "dependent-arising-without-constituting-subject", "phenomenological"),
        c("determination_operator", "dependent-co-arising", "logical-dialectical"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    frozenset({"dignaga", "dharmakirti"}): [
        c("manifestation_status", "conventionally-real-without-own-being", "metaphysical"),
        c("selfhood_structure", "no-enduring-self", "phenomenological"),
        c("epistemic_authority", "no-single-authority", "epistemological"),
        c("determination_operator", "exclusion-or-apoha", "logical-dialectical"),
        c("method_of_critique", "formal-proof-or-inference", "methodological"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    frozenset({"asanga", "vasubandhu", "lankavatara", "maitreya-attributed"}): [
        c("manifestation_status", "conventionally-real-without-own-being", "metaphysical"),
        c("selfhood_structure", "no-enduring-self", "phenomenological"),
        c("constitution_structure", "storehouse-transformation-of-cognitive-flow", "phenomenological"),
        c("finite_cognition_model", "storehouse-transformation", "epistemological"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
    frozenset({"sanghabhadra", "vasubandhu-abhidharma", "buddhaghosa"}): [
        c("substrate_structure", "process-field-with-no-enduring-substrate", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("selfhood_structure", "no-enduring-self", "phenomenological"),
        c("practice_path", "meditative-discipline", "soteriological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological"),
    ],
}


THINKER_OVERRIDES = {
    "aurobindo": [
        c("manifestation_status", "real-transformation", "metaphysical", "high"),
        c("causation_model", "real-transformation", "metaphysical", "high"),
        c("selfhood_structure", "psychic-individual", "phenomenological", "high"),
        c("temporal_mode", "both-orthogonal", "metaphysical", "high"),
        c("register_of_evolution", "real-cosmological-evolution", "historical-genealogical", "high"),
        c("affective_motive_force", "bliss-or-delight", "soteriological", "high"),
        c("practice_path", "transformative-integration", "soteriological", "high"),
        c("soteric_end", "transformation-of-life", "soteriological", "high"),
    ],
    "kc-bhattacharyya": [
        c("selfhood_structure", "relational-self", "phenomenological"),
        c("epistemic_authority", "no-single-authority", "epistemological"),
        c("modal_structure_of_truth", "alternative-irreducible-truths", "epistemological", "high"),
        c("relation_to_perspectivism", "irreducible-true-perspectives", "epistemological", "high"),
        c("normative_order_source", "self-legislating-subject", "ethical"),
    ],
    "ramakrishna": [
        c("identity_relation", "self-expression-or-appearance", "metaphysical"),
        c("manifestation_status", "expressive-manifestation", "metaphysical"),
        c("modal_structure_of_truth", "context-indexed-without-final-hierarchy", "epistemological"),
        c("relation_to_perspectivism", "irreducible-true-perspectives", "epistemological"),
        c("affective_motive_force", "devotion", "soteriological"),
        c("practice_path", "devotion-and-grace", "soteriological"),
        c("soteric_end", "loving-participation", "soteriological"),
    ],
    "vivekananda": [
        c("identity_relation", "self-expression-or-appearance", "metaphysical"),
        c("manifestation_status", "expressive-manifestation", "metaphysical"),
        c("normative_order_source", "divine-command-or-grace", "ethical", "low"),
        c("practice_path", "transformative-integration", "soteriological"),
        c("soteric_end", "transformation-of-life", "soteriological", "low"),
    ],
    "chaudhuri": [
        c("register_of_evolution", "real-cosmological-evolution", "historical-genealogical", "high"),
        c("social_formation_model", "civilizational-structure-shift", "political-social", "low"),
    ],
    "the-mother": [
        c("selfhood_structure", "psychic-individual", "phenomenological"),
        c("register_of_evolution", "real-cosmological-evolution", "historical-genealogical", "high"),
        c("practice_path", "transformative-integration", "soteriological", "high"),
        c("soteric_end", "transformation-of-life", "soteriological", "high"),
    ],
    "hegel": [
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
        c("individuation_status", "reducible-to-the-whole", "metaphysical", "high"),
        c("determination_operator", "negation-and-contradiction", "logical-dialectical", "high"),
        c("temporal_mode", "process-primary", "metaphysical", "high"),
        c("register_of_evolution", "sublative-becoming", "historical-genealogical", "high"),
        c("relation_to_perspectivism", "sublated-into-higher-whole", "epistemological", "high"),
        c("normative_order_source", "ethical-life-in-institutions", "ethical", "high"),
        c("social_formation_model", "recognitive-institutional", "political-social", "high"),
        c("soteric_end", "recognition-or-freedom", "soteriological", "high"),
    ],
    "heidegger": [
        c("substrate_structure", "anti-essential-relationality", "phenomenological", "medium"),
        c("selfhood_structure", "dasein", "phenomenological", "high"),
        c("semantic_mediation", "language-subordinate-to-non-propositional-knowing", "semantic-linguistic"),
        c("temporal_mode", "historical-disclosure", "phenomenological", "high"),
        c("soteric_end", "not-soteriological", "soteriological", "high"),
    ],
    "husserl": [
        c("individuation_status", "transcendental-pole", "phenomenological"),
        c("selfhood_structure", "transcendental-ego", "phenomenological", "high"),
        c("constitution_structure", "intentional-noesis-noema-correlation", "phenomenological", "high"),
        c("finite_cognition_model", "intentional-constitution", "epistemological", "high"),
        c("relation_to_perspectivism", "standpoint-conditioned-realism", "epistemological"),
        c("standpoint_predication", "profile-adumbrational-predication", "semantic-linguistic", "medium"),
        c("practice_path", "reduction-or-attentive-description", "soteriological"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "adorno": [
        c("finite_cognition_model", "genealogically-produced-illusion", "political-social", "low"),
        c("normative_order_source", "class-structured-social-relation", "political-social"),
        c("social_formation_model", "commodity-fetish-social-form", "political-social", "high"),
        c("affective_motive_force", "aesthetic-rapture", "aesthetic"),
        c("soteric_end", "ethical-vigilance-without-final-fusion", "ethical", "high"),
    ],
    "marx": [
        c("manifestation_status", "socially-or-discursively-stabilized", "political-social"),
        c("finite_cognition_model", "genealogically-produced-illusion", "political-social"),
        c("normative_order_source", "class-structured-social-relation", "political-social", "high"),
        c("social_formation_model", "commodity-fetish-social-form", "political-social", "high"),
        c("method_of_critique", "genealogy", "historical-genealogical", "low"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "spinoza": [
        c("substrate_structure", "one-self-standing", "metaphysical", "high"),
        c("manifestation_status", "dependent-real", "metaphysical"),
        c("identity_relation", "self-expression-or-appearance", "metaphysical"),
        c("causation_model", "immanent-expression", "metaphysical", "high"),
        c("temporal_mode", "substance-primary", "metaphysical"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "schopenhauer": [
        c("manifestation_status", "conventionally-real-without-own-being", "metaphysical"),
        c("identity_relation", "self-expression-or-appearance", "metaphysical", "low"),
        c("affective_motive_force", "desire-and-drive", "phenomenological"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological", "low"),
    ],
    "whitehead": [
        c("substrate_structure", "process-field-with-no-enduring-substrate", "metaphysical", "high"),
        c("causation_model", "processual-concrescence", "metaphysical", "high"),
        c("temporal_mode", "process-primary", "metaphysical", "high"),
        c("register_of_evolution", "durational-creative-growth", "historical-genealogical", "medium"),
    ],
    "butler": [
        c("selfhood_structure", "split-or-produced-subject", "phenomenological"),
        c("normative_order_source", "disciplinary-power", "political-social", "low"),
        c("social_formation_model", "performative-norm-repetition", "political-social", "high"),
        c("method_of_critique", "genealogy", "historical-genealogical", "low"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "freud": [
        c("selfhood_structure", "split-or-produced-subject", "phenomenological"),
        c("affective_motive_force", "desire-and-drive", "phenomenological", "high"),
        c("soteric_end", "not-soteriological", "soteriological"),
    ],
    "bhartrhari": [
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
        c("semantic_mediation", "language-as-creative-manifestation", "semantic-linguistic", "high"),
        c("epistemic_authority", "no-single-authority", "epistemological", "low"),
    ],
    "candrakirti": [
        c("method_of_critique", "prasanga-anti-thesis", "methodological", "high"),
    ],
    "bhaviveka": [
        c("method_of_critique", "formal-proof-or-inference", "methodological", "medium"),
    ],
    "nagarjuna": [
        c("method_of_critique", "prasanga-anti-thesis", "methodological", "medium"),
    ],
    "kundakunda": [
        c("standpoint_predication", "standpoint-indexed-predication", "semantic-linguistic", "high"),
    ],
    "akalanka": [
        c("standpoint_predication", "sevenfold-conditioned-predication", "semantic-linguistic", "high"),
    ],
    "yashovijaya": [
        c("standpoint_predication", "sevenfold-conditioned-predication", "semantic-linguistic", "high"),
    ],
    "clooney": [
        c("epistemic_authority", "comparative-theological-reading", "epistemological", "high"),
        c("method_of_critique", "comparative-reading", "methodological", "high"),
    ],
    "coomaraswamy": [
        c("semantic_mediation", "language-as-creative-manifestation", "aesthetic", "low"),
        c("affective_motive_force", "aesthetic-rapture", "aesthetic"),
    ],
    "bhaskararaya": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("epistemic_authority", "scripture-plus-transformative-experience", "epistemological", "low"),
        c("practice_path", "devotion-and-grace", "soteriological", "low"),
    ],
    "lakshmidhara": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("practice_path", "devotion-and-grace", "soteriological", "low"),
    ],
    "abhinanda": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("practice_path", "meditative-discipline", "soteriological", "low"),
    ],
    "mahesvarananda": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("practice_path", "transformative-integration", "soteriological", "low"),
    ],
    "bhatta-ramakantha": [
        c("substrate_structure", "one-independent-plus-real-dependents", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("practice_path", "devotion-and-grace", "soteriological", "low"),
    ],
    "sadyojyotis": [
        c("substrate_structure", "one-independent-plus-real-dependents", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("practice_path", "meditative-discipline", "soteriological", "low"),
    ],
    "maharaj": [
        c("epistemic_authority", "comparative-theological-reading", "epistemological", "low"),
    ],
    "basava": [
        c("affective_motive_force", "devotion", "soteriological", "medium"),
        c("practice_path", "devotion-and-grace", "soteriological", "medium"),
        c("soteric_end", "transformation-of-life", "soteriological", "low"),
    ],
    "nietzsche": [
        c("selfhood_structure", "no-enduring-self", "phenomenological", "high"),
        c("finite_cognition_model", "perspectival-interpretation", "epistemological", "high"),
        c("epistemic_authority", "genealogical-critique", "epistemological", "high"),
        c("relation_to_perspectivism", "perspectives-as-symptoms", "epistemological", "high"),
        c("affective_motive_force", "will-to-power", "ethical", "high"),
    ],
    "macherey": [
        c("epistemic_authority", "comparative-theological-reading", "epistemological", "low"),
        c("method_of_critique", "comparative-reading", "methodological", "medium"),
        c("social_formation_model", "commodity-fetish-social-form", "political-social", "low"),
    ],
    "melamed": [
        c("method_of_critique", "comparative-reading", "methodological", "low"),
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
        c("causation_model", "immanent-expression", "metaphysical", "low"),
    ],
    "vijnanabhiksu": [
        c("practice_path", "meditative-discipline", "soteriological", "medium"),
    ],
    "bhava-ganesa": [
        c("practice_path", "meditative-discipline", "soteriological", "low"),
    ],
    "badarayana": [
        c("substrate_structure", "one-self-standing", "metaphysical", "low"),
    ],
    "asmarathya": [
        c("identity_relation", "natural-difference-non-difference", "metaphysical", "low"),
    ],
    "audulomi": [
        c("identity_relation", "non-otherness", "metaphysical", "low"),
    ],
    "bodhayana": [
        c("identity_relation", "body-soul-qualification", "metaphysical", "low"),
    ],
    "brahmadatta": [
        c("finite_cognition_model", "positive-ignorance", "epistemological", "low"),
    ],
    "kasakrtsna": [
        c("identity_relation", "non-otherness", "metaphysical", "low"),
    ],
    "sundara-pandya": [
        c("identity_relation", "non-otherness", "metaphysical", "low"),
    ],
    "upavarsa": [
        c("epistemic_authority", "scripture-dominant", "epistemological", "low"),
        c("normative_order_source", "scriptural-injunction", "ritual-normative", "low"),
    ],
    "malini-vijaya-tantra": [
        c("manifestation_status", "expressive-manifestation", "metaphysical", "low"),
        c("practice_path", "transformative-integration", "soteriological", "low"),
    ],
}


ARTICLE_EVIDENCE = {
    "sankara": "data/articles/source/shankara.md",
    "ramanuja": "data/articles/source/ramanuja.md",
    "madhva": "data/articles/source/madhva.md",
    "caitanya": "data/articles/source/caitanya.md",
    "aurobindo": "data/articles/source/aurobindo.md",
    "kc-bhattacharyya": "data/articles/source/kc-bhattacharyya.md",
    "vivekananda": "data/articles/source/vivekananda-ramakrishna.md",
    "ramakrishna": "data/articles/source/vivekananda-ramakrishna.md",
    "chaudhuri": "data/articles/source/chaudhuri-banerji.md",
    "hegel": "data/articles/source/hegel.md",
    "heidegger": "data/articles/source/heidegger.md",
    "husserl": "data/articles/source/husserl.md",
    "whitehead": "data/articles/source/whitehead.md",
    "spinoza": "data/articles/source/spinoza.md",
    "adorno": "data/articles/source/adorno.md",
}


ARTICLE_STUBS = {
    "bergson": {
        "name": "Henri Bergson",
        "school": "Modern Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/bergson.md`.",
    },
    "deleuze": {
        "name": "Gilles Deleuze",
        "school": "Continental Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/deleuze.md`.",
    },
    "derrida": {
        "name": "Jacques Derrida",
        "school": "Continental Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/derrida.md`.",
    },
    "foucault": {
        "name": "Michel Foucault",
        "school": "Critical Theory",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/foucault.md`.",
    },
    "gebser": {
        "name": "Jean Gebser",
        "school": "Cross-tradition",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/gebser.md`.",
    },
    "leibniz": {
        "name": "G. W. Leibniz",
        "school": "Modern Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/leibniz.md`.",
    },
    "levinas": {
        "name": "Emmanuel Levinas",
        "school": "Phenomenology",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/levinas.md`.",
    },
    "mcgilchrist": {
        "name": "Iain McGilchrist",
        "school": "Cross-tradition",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/mcgilchrist.md`.",
    },
    "medhananda": {
        "name": "Swami Medhananda",
        "school": "Comparative Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/medhananda.md`.",
    },
    "prigogine": {
        "name": "Ilya Prigogine",
        "school": "Process Philosophy",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/prigogine.md`.",
    },
    "anirban": {
        "name": "Anirvan",
        "school": "Sāṅkhya",
        "core_thesis": "Article-backed thinker stub created during primitives_v2 Phase 2 from `data/articles/source/sankhya-anirban.md`.",
    },
}


STUB_OVERRIDES = {
    "bergson": [
        c("substrate_structure", "process-field-with-no-enduring-substrate", "metaphysical", "low"),
        c("selfhood_structure", "psychic-individual", "phenomenological"),
        c("temporal_mode", "process-primary", "metaphysical", "high"),
        c("register_of_evolution", "durational-creative-growth", "historical-genealogical", "high"),
        c("method_of_critique", "mixed-or-layered", "methodological"),
    ],
    "deleuze": [
        c("individuation_status", "expressive-singularity", "metaphysical", "high"),
        c("determination_operator", "difference-without-negation", "logical-dialectical", "high"),
        c("method_of_critique", "mixed-or-layered", "methodological"),
    ],
    "derrida": [
        c("epistemic_authority", "deconstructive-reading", "epistemological", "high"),
        c("determination_operator", "differential-deferral", "logical-dialectical", "high"),
        c("method_of_critique", "deconstruction", "methodological", "high"),
        c("semantic_mediation", "language-differentially-defers-presence", "semantic-linguistic", "high"),
        c("modal_structure_of_truth", "paraconsistent-or-both-held", "epistemological"),
    ],
    "foucault": [
        c("manifestation_status", "socially-or-discursively-stabilized", "political-social", "high"),
        c("selfhood_structure", "split-or-produced-subject", "phenomenological", "high"),
        c("finite_cognition_model", "genealogically-produced-illusion", "political-social"),
        c("epistemic_authority", "genealogical-critique", "epistemological", "high"),
        c("determination_operator", "genealogical-exposure", "historical-genealogical", "high"),
        c("method_of_critique", "genealogy", "historical-genealogical", "high"),
        c("normative_order_source", "disciplinary-power", "political-social", "high"),
        c("social_formation_model", "disciplinary-production-of-subjects", "political-social", "high"),
        c("practice_path", "critical-genealogical-work", "ethical", "medium"),
    ],
    "gebser": [
        c("temporal_mode", "historical-disclosure", "historical-genealogical"),
        c("register_of_evolution", "graded-manifestation-without-evolution", "historical-genealogical", "high"),
        c("social_formation_model", "civilizational-structure-shift", "political-social", "medium"),
    ],
    "leibniz": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical", "low"),
        c("manifestation_status", "dependent-real", "metaphysical", "low"),
        c("causation_model", "immanent-expression", "metaphysical", "low"),
        c("temporal_mode", "substance-primary", "metaphysical", "medium"),
    ],
    "levinas": [
        c("selfhood_structure", "relational-self", "phenomenological", "medium"),
        c("normative_order_source", "not-a-central-axis", "ethical", "low"),
        c("social_formation_model", "not-central", "political-social", "high"),
        c("affective_motive_force", "ethical-obligation-to-the-other", "ethical", "high"),
        c("soteric_end", "ethical-vigilance-without-final-fusion", "ethical", "high"),
    ],
    "mcgilchrist": [
        c("social_formation_model", "civilizational-structure-shift", "political-social", "high"),
        c("temporal_mode", "both-orthogonal", "metaphysical", "low"),
        c("individuation_status", "expressive-singularity", "phenomenological", "low"),
    ],
    "medhananda": [
        c("epistemic_authority", "comparative-theological-reading", "epistemological", "high"),
        c("method_of_critique", "comparative-reading", "methodological", "high"),
        c("modal_structure_of_truth", "context-indexed-without-final-hierarchy", "epistemological"),
        c("relation_to_perspectivism", "irreducible-true-perspectives", "epistemological"),
    ],
    "prigogine": [
        c("substrate_structure", "process-field-with-no-enduring-substrate", "metaphysical", "medium"),
        c("causation_model", "processual-concrescence", "metaphysical", "low"),
        c("temporal_mode", "process-primary", "metaphysical", "high"),
        c("register_of_evolution", "real-cosmological-evolution", "historical-genealogical", "high"),
    ],
    "anirban": [
        c("substrate_structure", "many-coordinate-reals", "metaphysical", "low"),
        c("causation_model", "real-transformation", "metaphysical", "low"),
        c("practice_path", "knowledge-discipline", "soteriological", "low"),
        c("soteric_end", "isolation-or-discriminative-release", "soteriological", "low"),
    ],
}


CITE_RE = re.compile(r"cite://([^)\s>]+)")


def evidence_for(thinker_id, data):
    cites = []
    for field in ("core_thesis", "summary"):
        text = data.get(field)
        if isinstance(text, str):
            cites.extend(CITE_RE.findall(text))
    for work in data.get("engaged_works", [])[:3]:
        summary = work.get("summary", "")
        cites.extend(CITE_RE.findall(summary))
    cites = list(dict.fromkeys(cites))[:4]
    out = [{"kind": "thinker_json", "ref": f"data/thinkers/{thinker_id}.json", "field": "core_thesis"}]
    if cites:
        out.append({"kind": "primary", "refs": [f"cite://{ck}" for ck in cites]})
    if thinker_id in ARTICLE_EVIDENCE:
        out.append({"kind": "source_article", "ref": ARTICLE_EVIDENCE[thinker_id]})
    return out


def merge_commitments(items):
    merged = {}
    for item in items:
        key = (item["primitive"], item["register"])
        merged[key] = item
    return list(sorted(merged.values(), key=lambda x: (x["primitive"], x["register"])))


def apply_profile(thinker):
    items = []
    school = thinker.get("school")
    sub_school = thinker.get("sub_school", "")
    if school in BASE_PROFILES:
        items.extend(deepcopy(BASE_PROFILES[school]))
    for token, rule in SUBSCHOOL_RULES:
        if token in sub_school:
            items.extend(deepcopy(rule))
    thinker_id = thinker["id"]
    for ids, rule in SET_OVERRIDES.items():
        if thinker_id in ids:
            items.extend(deepcopy(rule))
    if thinker_id in THINKER_OVERRIDES:
        items.extend(deepcopy(THINKER_OVERRIDES[thinker_id]))
    return merge_commitments(items)


def attach_evidence(thinker_id, thinker, commitments):
    ev = evidence_for(thinker_id, thinker)
    for item in commitments:
        item["evidence"] = deepcopy(ev)
    return commitments


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_registry():
    return {
        "version": "v2-phase5",
        "status": "draft",
        "description": "Machine-readable registry for the primitives_v2 comparative grammar.",
        "registers": [
            "metaphysical",
            "epistemological",
            "phenomenological",
            "semantic-linguistic",
            "logical-dialectical",
            "aesthetic",
            "ritual-normative",
            "ethical",
            "political-social",
            "historical-genealogical",
            "soteriological",
        ],
        "edge_types": [
            "commitment",
            "dependency",
            "cross-engagement",
            "critique",
            "subsumption",
            "register-shift",
            "terminological-near-match",
        ],
        "primitives": PRIMITIVES,
        "dependencies": DEPENDENCIES,
    }


def ensure_article_stubs():
    for thinker_id, meta in ARTICLE_STUBS.items():
        path = THINKERS_DIR / f"{thinker_id}.json"
        if path.exists():
            continue
        payload = {
            "id": thinker_id,
            "name": meta["name"],
            "name_iast": meta["name"],
            "school": meta["school"],
            "entry_status": "stub-from-article-phase2",
            "core_thesis": meta["core_thesis"],
            "primitive_commitments": [],
            "cross_engagements": [],
        }
        write_json(path, payload)


def main():
    ensure_article_stubs()
    for path in sorted(THINKERS_DIR.glob("*.json")):
        thinker = json.loads(path.read_text(encoding="utf-8"))
        commitments = apply_profile(thinker)
        if path.stem in STUB_OVERRIDES:
            commitments = merge_commitments(commitments + deepcopy(STUB_OVERRIDES[path.stem]))
        commitments = attach_evidence(path.stem, thinker, commitments)
        thinker["primitive_commitments"] = commitments
        thinker.setdefault("cross_engagements", [])
        write_json(path, thinker)
    write_json(REGISTRY_PATH, build_registry())


if __name__ == "__main__":
    main()
