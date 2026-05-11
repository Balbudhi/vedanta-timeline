# Primitive Graph

## §1 — What the graph is for

The graph is not a winner-picking machine.


It does three narrower things.

1. It gives a load-bearing claim a stable address.
2. It separates disagreements of register from disagreements of ontology.
3. It keeps the corpus from treating one sub-school vocabulary as the hidden grammar of every other thinker.

The unit of comparison is not "the whole thinker."

The unit is:

- a primitive
- a value on that primitive
- a register in which that value is asserted
- an evidence trail

That discipline matters because the corpus is no longer only Vedānta-on-Vedānta.

Śaṅkara, Madhva, Rāmānuja, and Jīva Gosvāmī can still be compared on substrate, manifestation, selfhood, and release. But Hegel, Nietzsche, Husserl, Heidegger, Derrida, Foucault, Whitehead, Bergson, Prigogine, Adorno, Levinas, and Mīmāṃsā do not all enter at the same point. Some are primarily metaphysical. Some are methodological. Some are political-social. Some are soteriological only in a stretched sense. Some refuse the very kind of closure another thinker is trying to secure.

The graph therefore has to do two jobs at once:

- be thin enough to avoid importing one system into another
- be wide enough to cover the whole corpus without leaving half the site in a residual "miscellaneous comparator" bin

The current document is built for that wider task.

## §2 — Reading discipline

The graph is governed by six rules.


### Rule 1 — Read the closest stable textual layer first

If a thinker has a source article in `data/articles/source/`, the article is the first assignment layer.


If a thinker does not yet have a source article, use the thinker's JSON only at the level it can actually support:

- `core_thesis`
- `summary`
- `engaged_works`

Do not let a late sub-school dispute rewrite an earlier author.

Śaṅkara is not assigned a settled Bhāmatī or Vivaraṇa locus doctrine simply because later Advaita needs one. The audit in `primitives_revision/audit.md` settled that point and this graph keeps it settled.

### Rule 2 — Keep article claims distinct from school defaults

Some thinkers can inherit a school profile with little distortion.


Examples:

- Padmapāda and Prakāśātman within the Vivaraṇa line
- Jayatīrtha and Vyāsatīrtha within Tattva-vāda
- Baladeva within Gauḍīya Vedānta

Some thinkers cannot.

Examples:

- Śaṅkara against later Advaita
- Appayya across multiple doctrinal roles
- Vivekananda across changing universal-religion formulations
- Ramakrishna against neat "Neo-Vedānta" reduction

Where inheritance would flatten a thinker, assign the thinker directly.

### Rule 3 — A primitive is not a thesis

The primitive is the slot where a thesis is located.


`substrate_structure` is not "Advaita." `genealogical-critique` is not "Nietzsche." `disciplinary-production-of-subjects` is not "Foucault." The primitive is thinner than the doctrine and has to stay thinner than the doctrine.

### Rule 4 — Register comes before verdict

Before comparing two claims, tag the register.


The allowed registers for this graph are:

- metaphysical
- epistemological
- phenomenological
- semantic-linguistic
- logical-dialectical
- aesthetic
- ritual-normative
- ethical
- political-social
- historical-genealogical
- soteriological

If two claims differ because one is soteriological and the other metaphysical, the graph must say so before it says anything about agreement or disagreement.

### Rule 5 — Do not force total coverage where the source basis is thin

Every thinker need not have a substantive value on every primitive.


The graph therefore permits a global non-substantive token:

- `withheld`

`withheld` is not a philosophical value. It means only that the present corpus does not justify a stronger assignment.

Use it when:

- the source basis is too thin
- the primitive is not central to the thinker
- the text does not settle between two live options

### Rule 6 — Mixed profiles are real and must be recorded as such

Some thinkers speak in more than one durable register.


Examples:

- Vivekananda's practical Advaita and his universal-religion rhetoric
- Ramakrishna's `neti neti` ascent and `vijñāna` return
- Appayya's Bhāmatī role and his Śaiva role
- Abhinavagupta's philosophical and ritual-aesthetic articulation

Where the mixed profile is load-bearing, record more than one commitment rather than collapsing the thinker into a false single-value summary.

## §3 — Primitive nodes

The graph now uses twenty-two primitives.


Each primitive has:

- a definition
- a bounded value range
- a read-off rule
- a register-scope
- anchor cases drawn from `data/articles/source/`

### P1 — `substrate_structure`

Definition:


The basic ontological architecture of what is self-standing, what is dependent, and whether there is any ultimate substrate at all.

Value range:

- `one-self-standing`
- `one-qualified-by-real-internal-distinctions`
- `one-independent-plus-real-dependents`
- `many-coordinate-reals`
- `process-field-with-no-enduring-substrate`
- `anti-essential-relationality`
- `suspended-or-refused`

Read-off rule:

Read from the passages where the thinker states what is basic in reality: Brahman, substance, process, Dasein, relation, event, or the refusal of any substrate-language. Use explicit architecture claims, not devotional tone or isolated metaphor.

Register-scope:

- metaphysical
- phenomenological when the architecture is disclosed through lived structure
- soteriological when liberation is described as a shift in ontological standing

Anchor cases:

- Śaṅkara: `one-self-standing`; see `shankara.md`, "Part II — *Tad-ananyatva* and the Clay-Pot Argument" and "Part VI — *Mithyā* ≠ *Asat*."
- Rāmānuja: `one-qualified-by-real-internal-distinctions`; see `ramanuja.md`, "Viśiṣṭādvaita — the doctrine in one sentence" and "Part II — *Aprthak-siddhi* and the Body-Soul Framework."
- Madhva: `one-independent-plus-real-dependents`; see `madhva.md`, the opening ontology sections on `svatantra/paratantra` and the later `pañcabheda` discussions.
- Spinoza: `one-self-standing`; see `spinoza.md`, the opening treatment of `Deus sive Natura`.
- Whitehead: `process-field-with-no-enduring-substrate`; see `whitehead.md`, the opening exposition of actual occasions and the later discussion of process as metaphysical basicness.

### P2 — `manifestation_status`

Definition:


The status of the world, appearance, finite entities, or social objects relative to what grounds them.

Value range:

- `self-standing-real`
- `dependent-real`
- `sublatable-not-null`
- `real-transformation`
- `expressive-manifestation`
- `conventionally-real-without-own-being`
- `socially-or-discursively-stabilized`
- `suspended-or-unfixed`

Read-off rule:

Read from explicit claims about whether the world is real, dependent, sublatable, transformed, expressed, conventionally valid, or produced by discursive or institutional fixation. This primitive is about status, not causal pathway.

Register-scope:

- metaphysical
- epistemological
- political-social when objectivity is treated as institutionally produced
- aesthetic when manifestation is treated as expressive disclosure

Anchor cases:

- Śaṅkara: `sublatable-not-null`; see `shankara.md`, "Part VI — *Mithyā* ≠ *Asat*" and the `bādhita` discussion in Part V.
- Madhva: `dependent-real`; see `madhva.md`, the architecture and `pañcabheda` sections where the world is insisted upon as real and non-sublatable.
- Aurobindo: `real-transformation`; see `aurobindo.md`, the main `Life Divine` sections on involution, evolution, and manifestation.
- Vivekananda-Ramakrishna: `expressive-manifestation`; see `vivekananda-ramakrishna.md`, the `vijñāna` discussions on roof and stairs.
- Foucault: `socially-or-discursively-stabilized`; see `foucault.md`, the disciplinary and genealogical sections where object-domains arise through practices and power.

### P3 — `identity_relation`

Definition:


The formal relation between ultimate reality, self, world, and finite being where unity and difference are both at issue.

Value range:

- `numerical-identity`
- `non-otherness`
- `body-soul-qualification`
- `image-original-similarity`
- `natural-difference-non-difference`
- `inconceivable-difference-non-difference`
- `self-expression-or-appearance`
- `no-single-relation-stated`

Read-off rule:

Read from explicit formulas used to gloss identity and difference: `tat tvam asi`, `ananyatva`, `aprthak-siddhi`, `bimba-pratibimba`, `svābhāvika-bhedābheda`, `acintya-bhedābheda`, expression, mode, or appearance. Do not infer from broad monist or pluralist labels.

Register-scope:

- metaphysical
- soteriological
- aesthetic where relation is described as expression

Anchor cases:

- Śaṅkara: `non-otherness`; see `shankara.md`, the `ananyatva` argument in Part II.
- Rāmānuja: `body-soul-qualification`; see `ramanuja.md`, Part II and the `mat-sthāni sarva-bhūtāni` discussion.
- Madhva: `image-original-similarity`; see `madhva.md`, the sections on `bimba-pratibimba`.
- Caitanya/Jīva line: `inconceivable-difference-non-difference`; see `caitanya.md`, the opening formalization of `acintya-bhedābheda`.
- Vivekananda-Ramakrishna: `self-expression-or-appearance`; see `vivekananda-ramakrishna.md`, the return-from-`neti` sections.

### P4 — `individuation_status`

Definition:

The standing of the individual as individual: dissolved, retained, qualified, singularized, produced, or made central only in a limited register.

Value range:

- `reducible-to-the-whole`
- `qualified-mode`
- `irreducible-dependent`
- `expressive-singularity`
- `transcendental-pole`
- `produced-or-fractured`
- `not-central`

Read-off rule:

Read from claims about what becomes of the individual self, subject, or singular existent. This primitive asks about the standing of individuation itself, not just about whether a thinker mentions persons.

Register-scope:

- metaphysical
- phenomenological
- ethical
- political-social
- soteriological

Anchor cases:

- Hegel: `reducible-to-the-whole`; see `hegel.md`, "Substanz als Subjekt" and the reading notes on Spirit and mediation.
- Rāmānuja: `qualified-mode`; see `ramanuja.md`, Part II on the body-soul framework.
- Madhva: `irreducible-dependent`; see `madhva.md`, the real-difference and `jīva`-hierarchy sections.
- Deleuze: `expressive-singularity`; see `deleuze.md`, the sections on difference, singularity, and anti-Hegelian individuation.
- Husserl: `transcendental-pole`; see `husserl.md`, the reduction and constitution sections.
- Foucault: `produced-or-fractured`; see `foucault.md`, the disciplinary and subject-formation sections.

### P5 — `causation_model`

Definition:

How the world, finite order, experience, or manifestation issues from its ground, if it does.

Value range:

- `appearance-without-real-change`
- `real-transformation`
- `unchanged-ground-with-changing-power`
- `body-soul-causation`
- `efficient-material-split`
- `immanent-expression`
- `processual-concrescence`
- `dependent-co-arising`
- `not-a-cosmogonic-system`

Read-off rule:

Read from causal chapters, cosmological passages, or explicit denials of cosmogonic explanation. Keep distinct the status of the world and the mechanism by which it appears or unfolds.

Register-scope:

- metaphysical
- cosmological
- soteriological when the causal account constrains release

Anchor cases:

- Śaṅkara: `appearance-without-real-change`; see `shankara.md`, "Part VII — *Vivarta* vs *Pariṇāma*" with the built-in warning against reading late technical hardening back into Śaṅkara.
- Rāmānuja: `body-soul-causation`; see `ramanuja.md`, Part II and the `prakṛti` discussions in Part IV.
- Madhva: `efficient-material-split`; see `madhva.md`, the cosmological sections where `prakṛti` is material cause and Viṣṇu efficient cause.
- Caitanya/Jīva line: `unchanged-ground-with-changing-power`; see `caitanya.md`, the sections on `acintya-śakti`.
- Whitehead: `processual-concrescence`; see `whitehead.md`, the exposition of prehension and concrescence.
- Spinoza: `immanent-expression`; see `spinoza.md`, the early `Ethics` architecture and mode-language sections.

### P6 — `selfhood_structure`

Definition:

What kind of self, subject, or locus of disclosure is treated as real or operative.

Value range:

- `substantial-self`
- `witness-self`
- `relational-self`
- `psychic-individual`
- `transcendental-ego`
- `dasein`
- `split-or-produced-subject`
- `no-enduring-self`

Read-off rule:

Read from explicit subject-analyses: `ātman`, witness-consciousness, ego, Dasein, subject-as-freedom, split subject, or the denial of enduring selfhood. Avoid collapsing this primitive into mere ethics or politics.

This is the primitive on which `ātman` and `anātman` first part company. Do not try to smuggle that dispute into `manifestation_status`. A no-self claim is not, by itself, a claim that appearances are unreal; it is a claim about what sort of subject there is, or is not, for whom appearance occurs.

Register-scope:

- phenomenological
- metaphysical
- epistemological
- soteriological

Anchor cases:

- Śaṅkara: `witness-self`; see `shankara.md`, the `sākṣi-cetana` discussions in Part I.
- Bergson: `psychic-individual`; see `bergson.md`, "The deep self and the surface self."
- Husserl: `transcendental-ego`; see `husserl.md`, the `Ideas I` sections on reduction and constituting consciousness.
- Heidegger: `dasein`; see `heidegger.md`, the opening analysis of Being and Dasein.
- Foucault: `split-or-produced-subject`; see `foucault.md`, the disciplinary and self-formation sections.
- Nietzsche: `no-enduring-self`; see `nietzsche.md`, the anti-doer passages and the critique of subject grammar.

### P6A — `constitution_structure`

Definition:

How subject, object, world, and appearing are bound together before the later questions of truth, error, or liberation arise.

Value range:

- `subject-object-duality-taken-as-basic`
- `intentional-noesis-noema-correlation`
- `storehouse-transformation-of-cognitive-flow`
- `reflexive-self-manifestation`
- `dependent-arising-without-constituting-subject`
- `withheld`

Read-off rule:

Use this primitive only when the text gives a real architecture of appearing itself. Husserl's noesis/noema relation, Yogācāra's `ālaya`-based transformation of cognitive flow, and Trika's reflexive self-manifestation belong here. Do not reduce those to a generic theory of error. They are not merely accounts of what goes wrong in finite cognition; they are accounts of how a world is there at all.

Register-scope:

- phenomenological
- epistemological
- metaphysical where appearing is itself ontologized

Anchor cases:

- Husserl: `intentional-noesis-noema-correlation`; see `husserl.md`, the `Ideas I` reduction and constitution sections.
- Asaṅga and Vasubandhu: `storehouse-transformation-of-cognitive-flow`; see their JSON entries on `vijñapti-mātratā`, `ālaya-vijñāna`, and the `trisvabhāva` sequence.
- Abhinavagupta: `reflexive-self-manifestation`; see `abhinavagupta.json`, where `prakāśa-vimarśa` and `ābhāsa` do more than explain illusion.
- Candrakīrti: `dependent-arising-without-constituting-subject`; use only with care, and only where the point is precisely that no constituting subject stands behind the dependent nexus.

### P7 — `finite_cognition_model`

Definition:

The account of error, finitude, obscuration, interpretation, or bounded knowing.

Value range:

- `adhyasa-or-superimposition`
- `positive-ignorance`
- `real-dependent-veiling`
- `contraction-or-obscuration`
- `storehouse-transformation`
- `intentional-constitution`
- `perspectival-interpretation`
- `genealogically-produced-illusion`
- `no-unified-model-given`

Read-off rule:

Read from arguments about illusion, ignorance, contraction, interpretation, constitution, ideology, or genealogical masking. Do not confuse moral failure with epistemic structure unless the thinker explicitly binds the two.

Register-scope:

- epistemological
- phenomenological
- metaphysical
- political-social
- soteriological

Anchor cases:

- Śaṅkara: `adhyasa-or-superimposition`; see `shankara.md`, Part I.
- Later Advaita cases on the site: `positive-ignorance`; compare the Madhusūdana material discussed inside `shankara.md`, Part VIII, with the relevant JSON-only authors.
- Madhva: `real-dependent-veiling`; see `madhva.md`, the anti-`mithyātva` sections and the later-school notes.
- Husserl: `intentional-constitution`; see `husserl.md`, the reduction and constitution chapters.
- Asaṅga and Vasubandhu: `storehouse-transformation`; use where the issue is the dualizing habit-flow itself rather than the larger architecture of constitution.
- Nietzsche: `perspectival-interpretation`; see `nietzsche.md`, the sections on truth, force, and interpretation.
- Foucault: `genealogically-produced-illusion`; see `foucault.md`, the genealogy sections where truth-effects arise from regimes of practice.

### P8 — `epistemic_authority`

Definition:

The dominant source or ordered set of sources by which the thinker warrants load-bearing claims.

Value range:

- `scripture-dominant`
- `scripture-plus-transformative-experience`
- `plural-pramana-realism`
- `ritual-injunction`
- `dialectical-immanence`
- `phenomenological-reduction`
- `genealogical-critique`
- `deconstructive-reading`
- `comparative-theological-reading`
- `no-single-authority`

Read-off rule:

Read from explicit pramāṇa claims, methodological prefaces, argument-forms, and statements about what kind of access is final. Ask what the thinker treats as decisive when the stakes rise.

Register-scope:

- epistemological
- methodological
- soteriological

Anchor cases:

- Śaṅkara: `scripture-dominant`; see `shankara.md`, "Part IV — *Tat Tu Samanvayāt*."
- Vivekananda-Ramakrishna: `scripture-plus-transformative-experience`; see `vivekananda-ramakrishna.md`, the `vijñāna` and multiform-practice discussions.
- Madhva: `plural-pramana-realism`; see `madhva.md`, the sections on `pramāṇa`, `sākṣi`, and anti-`anirvacanīya` argument.
- Husserl: `phenomenological-reduction`; see `husserl.md`, the opening `Ideas` sections.
- Hegel: `dialectical-immanence`; see `hegel.md`, the `Phenomenology` and `Logic` openings.
- Nietzsche: `genealogical-critique`; see `nietzsche.md`, the `Genealogy` sections.
- Derrida: `deconstructive-reading`; see `derrida.md`, the writing, presence, and supplement sections.
- Medhananda: `comparative-theological-reading`; see `medhananda.md`, the methodological opening and later pluralism chapters.

### P9 — `determination_operator`

Definition:

The principal operator by which determinacy, difference, or intelligibility is articulated.

Value range:

- `negation-and-contradiction`
- `non-sublatable-difference`
- `difference-without-negation`
- `exclusion-or-apoha`
- `self-expression`
- `differential-deferral`
- `genealogical-exposure`
- `ritual-specification`
- `dependent-co-arising`

Read-off rule:

Read from the passages where the thinker says what makes one thing determinately this rather than that: contradiction, difference, expression, spacing, ritual rule, dependence, or exposure of contingent origin.

Register-scope:

- logical-dialectical
- metaphysical
- semantic-linguistic
- historical-genealogical

Anchor cases:

- Hegel: `negation-and-contradiction`; see `hegel.md`, "Sein, Nichts, Werden" and the `Wesen` section on contradiction.
- Madhva: `non-sublatable-difference`; see `madhva.md`, the `pañcabheda` and `viśeṣa` sections.
- Deleuze: `difference-without-negation`; see `deleuze.md`, the anti-Hegel and repetition sections.
- Buddhist-pramāṇa comparators later in the JSON layer will take `exclusion-or-apoha`; the article-backed comparative pressure point for that value is the anti-essential language work discussed against realism in `derrida.md` and the conceptual-fixity worries tracked in `nietzsche.md`, though the primary assignments will come from the Dignāga and Dharmakīrti JSON materials.
- Vivekananda-Ramakrishna: `self-expression`; see `vivekananda-ramakrishna.md`, the `vijñāna` passages where the many are read as the One's own display.
- Derrida: `differential-deferral`; see `derrida.md`, the sections on `différance`, writing, and supplement.
- Foucault: `genealogical-exposure`; see `foucault.md`, the genealogical procedure sections.
- Mīmāṃsā material: `ritual-specification`; see `mimamsa-aurobindo-v4.md`, the discussions of injunction and act-formation.

### P10 — `method_of_critique`

Definition:

The operative procedure by which the thinker advances, tests, or dismantles claims.

Value range:

- `commentarial-exegesis`
- `formal-proof-or-inference`
- `prasanga-anti-thesis`
- `phenomenological-reduction`
- `dialectical-development`
- `genealogy`
- `deconstruction`
- `comparative-reading`
- `mixed-or-layered`

Read-off rule:

Read from how the work proceeds, not just from what it concludes. A thinker can be metaphysically close to another thinker and methodologically far apart.

Register-scope:

- methodological
- logical-dialectical
- epistemological
- historical-genealogical

Anchor cases:

- Rāmānuja: `commentarial-exegesis`; see `ramanuja.md`, Part I and Part III.
- Madhva: `formal-proof-or-inference`; see `madhva.md`, the anti-Advaita and `mithyātva` critique sections.
- Candrakīrti: `prasanga-anti-thesis`; use where the refusal of `svatantra-anumāna` is itself load-bearing, not a footnote to a general dialectic.
- Husserl: `phenomenological-reduction`; see `husserl.md`, the reductions.
- Hegel: `dialectical-development`; see `hegel.md`, the movement from `Phenomenology` to `Logic`.
- Nietzsche: `genealogy`; see `nietzsche.md`, the `Genealogy` discussions.
- Derrida: `deconstruction`; see `derrida.md`, the writing/presence chapters.
- Medhananda: `comparative-reading`; see `medhananda.md`, the comparative-theological frame.
- Aurobindo: `mixed-or-layered`; see `aurobindo.md`, where commentary, metaphysical construction, and yogic report are braided rather than cleanly separated.

### P11 — `semantic_mediation`

Definition:

How language, sign, sentence, or proposition mediates access to reality, action, or objecthood.

Value range:

- `language-tracks-reality`
- `language-binds-action`
- `language-constitutes-object-domain`
- `language-differentially-defers-presence`
- `language-as-creative-manifestation`
- `language-subordinate-to-non-propositional-knowing`

Read-off rule:

Read from explicit claims about scriptural sentence-force, speculative predication, language as house of Being, signifying difference, performative institution, or language's subordination to direct realization.

Register-scope:

- semantic-linguistic
- epistemological
- ritual-normative
- phenomenological

Anchor cases:

- Mīmāṃsā-Aurobindo materials: `language-binds-action`; see `mimamsa-aurobindo-v4.md`, the injunction and ritual-language arguments.
- Hegel: `language-constitutes-object-domain`; see `hegel.md`, "The speculative sentence."
- Heidegger: `language-subordinate-to-non-propositional-knowing`; see `heidegger.md`, the Being/language sections where ordinary predication is displaced by disclosure.
- Derrida: `language-differentially-defers-presence`; see `derrida.md`, the writing and `différance` sections.
- Vivekananda-Ramakrishna: `language-as-creative-manifestation`; see `vivekananda-ramakrishna.md`, where symbol, deity-form, and language of practice are treated as mode-shaping rather than merely descriptive.
- Nyāya-leaning realist material in the corpus: `language-tracks-reality`; compare the explicit realist passages in `madhva.md` and `ramanuja.md`.

### P12 — `temporal_mode`

Definition:

Whether being is framed as substance, process, historical unfolding, disclosure, or an orthogonal combination of timeless and temporal orders.

Value range:

- `substance-primary`
- `process-primary`
- `both-orthogonal`
- `timeless-ground-with-dependent-time`
- `historical-disclosure`
- `no-decision-given`

Read-off rule:

Read from the passages where the thinker treats becoming, duration, historicity, actual occasion, eternal ground, or disclosure in time as constitutive.

Register-scope:

- metaphysical
- phenomenological
- cosmological
- historical-genealogical

Anchor cases:

- Bergson: `process-primary`; see `bergson.md`, the `durée` and creative evolution sections.
- Whitehead: `process-primary`; see `whitehead.md`, the opening treatment of actual occasions.
- Hegel: `process-primary`; see `hegel.md`, the Becoming and Spirit sections.
- Madhva: `timeless-ground-with-dependent-time`; see `madhva.md`, the sections where time is real yet dependent.
- Aurobindo: `both-orthogonal`; see `aurobindo.md`, where timeless Sachchidananda and evolutionary manifestation are both retained.
- Heidegger: `historical-disclosure`; see `heidegger.md`, the temporality and history of Being sections.

### P13 — `register_of_evolution`

Definition:

How, if at all, emergence, ascent, development, or historic transformation is treated.

Value range:

- `no-evolution`
- `sublative-becoming`
- `real-cosmological-evolution`
- `durational-creative-growth`
- `graded-manifestation-without-evolution`
- `genealogical-historicization`
- `not-applicable`

Read-off rule:

Read from explicit accounts of history, cosmological development, duration, emergence, involution/evolution, or genealogy. Do not import an evolutionary model where the thinker gives only hierarchy or rank.

Register-scope:

- cosmological
- metaphysical
- historical-genealogical
- soteriological
- political-social

Anchor cases:

- Hegel: `sublative-becoming`; see `hegel.md`, the Spirit/history line.
- Aurobindo: `real-cosmological-evolution`; see `aurobindo.md`, the core `Life Divine` sections.
- Bergson: `durational-creative-growth`; see `bergson.md`, Part III.
- Prigogine: `real-cosmological-evolution`; see `prigogine.md`, the bifurcation and self-organization chapters.
- Gebser: `graded-manifestation-without-evolution`; see `gebser.md`, the structures of consciousness.
- Foucault: `genealogical-historicization`; see `foucault.md`, the genealogy and historical-formation sections.

### P14 — `modal_structure_of_truth`

Definition:

How truth is distributed when more than one valid standpoint, level, or mode is in play.

Value range:

- `single-absolute-truth`
- `hierarchical-standpoint-truth`
- `alternative-irreducible-truths`
- `standpoint-conditioned-realism`
- `paraconsistent-or-both-held`
- `context-indexed-without-final-hierarchy`

Read-off rule:

Read from explicit treatment of standpoint, rank-order, contradiction, or alternative valid formulations. Ask how the thinker handles apparent conflict when two modes of discourse both claim authority.

Register-scope:

- epistemological
- metaphysical
- semantic-linguistic
- soteriological

Anchor cases:

- Śaṅkara: `hierarchical-standpoint-truth`; see `shankara.md`, the three-tier ontology and `bādhita` discussions.
- K.C. Bhattacharyya: `alternative-irreducible-truths`; see `kc-bhattacharyya.md`, the sections on alternative absolutes.
- Madhva: `single-absolute-truth`; see `madhva.md`, the anti-`anirvacanīya` and anti-equivocation sections.
- Ramakrishna/Vivekananda material: `context-indexed-without-final-hierarchy` in the plural-path register; see `vivekananda-ramakrishna.md` and `medhananda.md`.
- Derrida: `paraconsistent-or-both-held` only in the weak structural sense that presence is never simply discarded yet never secured; see `derrida.md`.
- K.C. Bhattacharyya's Kantian supplement article: compare `kcb-kantian-perspectivism.md` once it is tracked into the manifest; for now the main article supplies the stronger anchor.

### P15 — `relation_to_perspectivism`

Definition:

How a thinker treats plurality of viewpoints, standpoints, or partial disclosures.

Value range:

- `sublated-into-higher-whole`
- `irreducible-true-perspectives`
- `partial-perspectives-ranked`
- `standpoint-conditioned-realism`
- `perspectives-as-symptoms`
- `no-perspectivism-claim`

Read-off rule:

Read from explicit claims about whether perspectives are preserved, ranked, superseded, symptomatic, or treated as necessary but partial.

Register-scope:

- epistemological
- phenomenological
- historical-genealogical
- political-social

Anchor cases:

- Hegel: `sublated-into-higher-whole`; see `hegel.md`, especially the Preface logic carried through the reader.
- K.C. Bhattacharyya: `irreducible-true-perspectives`; see `kc-bhattacharyya.md`, the alternative-absolute sections.
- Madhva: `partial-perspectives-ranked`; see `madhva.md`, the hierarchy and real-difference discussions, especially where `tāratamya` bears epistemic weight.
- Husserl: `standpoint-conditioned-realism`; see `husserl.md`, the constitution analyses where objectivity is built through profiles without collapsing to sheer relativism.
- Nietzsche: `perspectives-as-symptoms`; see `nietzsche.md`, the interpretation and force analyses.
- Medhananda: `irreducible-true-perspectives` in the pluralist theological register; see `medhananda.md`.

### P15A — `standpoint_predication`

Definition:

How predication itself is qualified, indexed, or multiplied once more than one valid standpoint is admitted.

Value range:

- `single-unqualified-predication`
- `hierarchically-ranked-predication`
- `standpoint-indexed-predication`
- `sevenfold-conditioned-predication`
- `profile-adumbrational-predication`
- `withheld`

Read-off rule:

Use this primitive when the text is not merely saying that perspectives differ, but is specifying how predication changes under that difference. This is where the Jaina `naya` / `syādvāda` / `anekānta` family belongs. `modal_structure_of_truth` says how many truth-levels are in play; `standpoint_predication` says what sort of assertion is licensed from each standpoint. That is the distinction the older graph blurred.

Register-scope:

- semantic-linguistic
- epistemological
- logical-dialectical

Anchor cases:

- Kundakunda: `standpoint-indexed-predication`; see the JSON entry on `niścaya-naya` and `vyavahāra-naya`.
- Akalaṅka and Yaśovijaya: `sevenfold-conditioned-predication`; use where `syādvāda` is doing explicit logical work rather than serving as a loose pluralist slogan.
- Śaṅkara: `hierarchically-ranked-predication`; only where the `vyāvahārika/pāramārthika` difference is overtly governing what may be said.
- Husserl: `profile-adumbrational-predication`; use sparingly, and only where objectivity is built through adumbrated profiles rather than a single unqualified view.

### P16 — `normative_order_source`

Definition:

Where obligation, order, rightful conduct, or binding normativity is sourced.

Value range:

- `scriptural-injunction`
- `divine-command-or-grace`
- `ethical-life-in-institutions`
- `disciplinary-power`
- `class-structured-social-relation`
- `self-legislating-subject`
- `not-a-central-axis`

Read-off rule:

Read from the passages where the thinker says why one must do what one must do. Ask whether normativity is given by injunction, divine relation, ethical institutions, power, class structure, autonomy, or is not a primary axis.

Register-scope:

- ritual-normative
- ethical
- political-social
- soteriological

Anchor cases:

- Mīmāṃsā material: `scriptural-injunction`; see `mimamsa-aurobindo-v4.md`, the ritual-language chapters.
- Rāmānuja: `divine-command-or-grace`; see `ramanuja.md`, the `prapatti` and devotional-obedience passages.
- Hegel: `ethical-life-in-institutions`; see `hegel.md`, the `Philosophy of Right` section.
- Foucault: `disciplinary-power`; see `foucault.md`, the discipline and biopower sections.
- Adorno/Marx line: `class-structured-social-relation`; see `adorno.md`, the exchange and social-totality passages, with the Marx JSON supplying the stricter primary social-theory wording in later assignments.
- K.C. Bhattacharyya's Kantian horizon: `self-legislating-subject`; compare `kc-bhattacharyya.md` with the dedicated Kantian perspective article.

### P17 — `social_formation_model`

Definition:

How institutions, power, social form, or collective structures generate subjects and appearances of objectivity.

Value range:

- `not-central`
- `recognitive-institutional`
- `commodity-fetish-social-form`
- `disciplinary-production-of-subjects`
- `performative-norm-repetition`
- `civilizational-structure-shift`

Read-off rule:

Read from passages on institution, law, labor, power, discipline, media, symbolic order, or civilizational pattern. Do not infer from occasional political remark alone.

Register-scope:

- political-social
- historical-genealogical
- ethical
- phenomenological

Anchor cases:

- Hegel: `recognitive-institutional`; see `hegel.md`, the family/civil-society/state sections.
- Adorno: `commodity-fetish-social-form`; see `adorno.md`, the exchange and culture-industry sections.
- Foucault: `disciplinary-production-of-subjects`; see `foucault.md`, the prison, discipline, and biopolitics sections.
- McGilchrist: `civilizational-structure-shift`; see `mcgilchrist.md`, the hemisphere/culture and institutional drift sections.
- Levinas: `not-central`; see `levinas.md`, where ethics outruns institutional social theory even when politics enters.

### P18 — `affective_motive_force`

Definition:

What fundamentally moves life, practice, transformation, or critique.

Value range:

- `knowledge`
- `devotion`
- `will-to-power`
- `bliss-or-delight`
- `desire-and-drive`
- `ethical-obligation-to-the-other`
- `aesthetic-rapture`
- `not-central`

Read-off rule:

Read from the motive force the thinker repeatedly returns to when explaining why transformation happens or why practice sustains itself. This is not simply an emotion word-count exercise.

Register-scope:

- ethical
- soteriological
- aesthetic
- political-social
- phenomenological

Anchor cases:

- Śaṅkara: `knowledge`; see `shankara.md`, especially the reading notes and `mahāvākya`-centered passages.
- Caitanya/Jīva line: `devotion`; see `caitanya.md`, the `bhakti-rasa` and `acintya-bhedābheda` sections.
- Nietzsche: `will-to-power`; see `nietzsche.md`, the interpretation and valuation sections.
- Aurobindo: `bliss-or-delight`; see `aurobindo.md`, the Sachchidananda and delight-of-being sections.
- Levinas: `ethical-obligation-to-the-other`; see `levinas.md`, the face and responsibility sections.
- Adorno: `aesthetic-rapture` only in a guarded sense; see `adorno.md`, the mimesis and aesthetic-resistance passages.

### P19 — `practice_path`

Definition:

The dominant practical path by which transformation, clarification, or release is pursued.

Value range:

- `knowledge-discipline`
- `devotion-and-grace`
- `ritual-observance`
- `meditative-discipline`
- `reduction-or-attentive-description`
- `transformative-integration`
- `critical-genealogical-work`
- `not-soteric`

Read-off rule:

Read from the actual path-structure: study, contemplation, devotion, ritual, phenomenological reduction, integrated yoga, or critical work that is not salvation-talk but still functions as a path of transformation.

Register-scope:

- soteriological
- epistemological
- ethical
- ritual-normative

Anchor cases:

- Śaṅkara: `knowledge-discipline`; see `shankara.md`, the reading notes and scripture/cognition sections.
- Rāmānuja: `devotion-and-grace`; see `ramanuja.md`, the `Gītā` and `prapatti` passages.
- Mīmāṃsā material: `ritual-observance`; see `mimamsa-aurobindo-v4.md`.
- Husserl: `reduction-or-attentive-description`; see `husserl.md`.
- Aurobindo: `transformative-integration`; see `aurobindo.md`, the Integral Yoga and supramental transformation sections.
- Foucault: `critical-genealogical-work`; see `foucault.md`, where critique and self-practice are bound together.
- Nietzsche: `not-soteric`; see `nietzsche.md`, where style of life matters without a fixed liberation schema.

### P20 — `soteric_end`

Definition:

The final end aimed at or described by the thinker, where such an end is present.

Value range:

- `identity-with-ground`
- `service-with-distinction-preserved`
- `loving-participation`
- `isolation-or-discriminative-release`
- `recognition-or-freedom`
- `transformation-of-life`
- `ethical-vigilance-without-final-fusion`
- `not-soteriological`

Read-off rule:

Read from the explicit terminus of the path: mokṣa, recognition, participation, transformed terrestrial life, ethical wakefulness, or the absence of any liberation telos.

Register-scope:

- soteriological
- ethical
- phenomenological
- political-social where freedom is institutional and concrete

Anchor cases:

- Śaṅkara: `identity-with-ground`; see `shankara.md`, the closing notes and the Upaniṣad-bhāṣya selections.
- Madhva: `service-with-distinction-preserved`; see `madhva.md`, the `bhakti`, `aparokṣa-jñāna`, and liberation sections.
- Caitanya/Jīva line: `loving-participation`; see `caitanya.md`, the `rasa` and Kṛṣṇa-participation passages.
- Hegel: `recognition-or-freedom`; see `hegel.md`, the Spirit and `Philosophy of Right` sections.
- Aurobindo: `transformation-of-life`; see `aurobindo.md`, the supramental and gnostic-being sections.
- Levinas: `ethical-vigilance-without-final-fusion`; see `levinas.md`, the infinity and responsibility passages.
- Adorno: `not-soteriological` in the strict sense, but compare the negative horizon of reconciliation in `adorno.md`.

## §4 — Dependency edges

The graph is not only a bag of primitive labels.

Some primitives are downstream from others. The dependency edges below matter because they tell the later commitment table when two values should move together and when they should not.

### D1 — `substrate_structure` → `manifestation_status`

A thinker's account of what is basic constrains the status assigned to world and finite being.

Examples:

- Śaṅkara's `one-self-standing` architecture constrains `manifestation_status` toward `sublatable-not-null`.
- Madhva's `one-independent-plus-real-dependents` constrains it toward `dependent-real`.
- Whitehead's process architecture constrains it toward event-reality rather than static manifestation language.

### D2 — `substrate_structure` → `identity_relation`

The relation between whole and part cannot float free of the basic architecture.

Examples:

- Rāmānuja's body-soul qualification depends on `one-qualified-by-real-internal-distinctions`.
- Madhva's `image-original-similarity` depends on `one-independent-plus-real-dependents`.
- Caitanya's `inconceivable-difference-non-difference` depends on a real plurality that is neither strict identity nor mere external dualism.

### D3 — `manifestation_status` ↔ `causation_model`

These two primitives are linked but not identical.

The world can be `dependent-real` under more than one causal model. It can be `sublatable-not-null` under an appearance model. It can be `expressive-manifestation` under an immanent-expression model. Keep the distinction clean.

### D4 — `selfhood_structure` → `constitution_structure` → `finite_cognition_model`

A witness-self, transcendental ego, Dasein, produced subject, or no-self position tends first to shape how appearing is constituted, and only then to shape what counts as illusion, obscuration, or finite error.

Examples:

- witness-self often pairs with superimposition or obscuration
- transcendental ego with intentional constitution
- Yogācāra with storehouse-transformation and dualizing projection
- produced subject with discipline or genealogy
- no-enduring-self with dependent process or anti-substantialist phenomenology

### D5 — `epistemic_authority` ↔ `method_of_critique`

The authority source and the working method often track one another but not always.

Examples:

- Śaṅkara: scripture-dominant with commentarial-exegetical method
- Husserl: reduction as both authority and method
- Nietzsche: genealogy as method and critique-source
- Medhananda: comparative theological reading as method, but with devotional and textual commitments still alive inside it

### D6 — `determination_operator` ↔ `semantic_mediation`

If difference is produced by contradiction, by `viśeṣa`, by writing, by injunction, or by differential deferral, language and determination will usually move together. This is where Hegel, Madhva, Mīmāṃsā, Derrida, and Bhartṛhari-type later assignments become comparable without being homogenized.

### D7 — `temporal_mode` → `register_of_evolution`

Not every process ontology yields an evolution doctrine, but the temporal framing constrains the available options.

Examples:

- Bergson's duration makes `durational-creative-growth` available.
- A timeless-ground model can still permit evolution, but only by adding a layered account, as in Aurobindo.
- Heidegger's historical disclosure is not cosmological evolution.

### D8 — `modal_structure_of_truth` ↔ `relation_to_perspectivism` ↔ `standpoint_predication`

The truth structure constrains how perspectives are ranked, held apart, or folded into a whole. Where the thinker goes further and says what may be asserted from each standpoint, `standpoint_predication` becomes the third necessary node.

Examples:

- Hegel's whole invites `sublated-into-higher-whole`.
- K.C. Bhattacharyya's alternative absolutes invite `irreducible-true-perspectives`.
- Nietzsche's force-diagnostic stance invites `perspectives-as-symptoms`.
- Jaina standpoint-realism requires both `standpoint-conditioned-realism` and a distinct predicative rule-set; otherwise the grammar slides back into a lazy label of relativism.

### D9 — `normative_order_source` → `social_formation_model`

Where normativity is sourced often shapes how society is modeled.

Examples:

- Hegel's ethical life pairs with recognitive institutions.
- Foucault's power-model pairs with disciplinary production.
- Mīmāṃsā's injunction model pairs more with ritual order than with a thick social-formation theory.

### D10 — `practice_path` → `soteric_end`

The path does not mechanically fix the end, but it narrows the plausible endpoints.

Examples:

- knowledge-discipline tends toward identity or witness-disclosure
- devotion-and-grace tends toward service or loving participation
- transformative integration tends toward transformation of life
- reduction can aim at clarification without traditional salvation

## §5 — Commitment edges

A thinker commitment is recorded as a structured edge:

- thinker
- primitive
- value
- register
- confidence
- evidence

The edge is the real atomic unit of the later JSON field `primitive_commitments`.

### Confidence levels

Use three confidence levels in later assignment work.

- `high`: explicit and repeated in source article or primary-text-backed JSON
- `medium`: clear but compressed, or inherited from a well-defined school profile with local confirmation
- `low`: provisionally assigned from sparse evidence and liable to revision

### Evidence policy

Each commitment should cite one of:

- source article section
- primary-text `cite://...` reference already present in source article or thinker JSON
- both when available

### Mixed assignments

When a thinker genuinely sustains two values in different registers, record them as two separate commitment objects with distinct register tags rather than fusing them into a hybrid value.

Examples:

- Ramakrishna can support both a strict ascent-language and a return-language.
- Appayya can take Bhāmatī-line and Śaiva-line values in different textual roles.
- Vivekananda's institutional and soteriological voices do not always collapse into one comparative claim.

## §6 — Cross-engagement edges

Phase 3 of the rollout depends on one further edge type:

- `cross-engagement`

This is not a primitive-value claim.

It is a short passage inserted into an article at the point where a load-bearing claim is made. The passage names another thinker who engages the same primitive-axis and says what kind of engagement is happening.

Allowed relation labels:

- `agrees`
- `disagrees`
- `subsumes`
- `sharpens`
- `transposes-register`
- `shares-axis-different-end`

### Cross-engagement passage rule

Each later passage should be:

- 30 to 80 words
- attached to a specific article location
- tagged with the relevant primitive
- tagged with the operative register
- supported by a primary citation for the comparison thinker

### Register discipline for cross-engagement

Do not say "same claim" when the sameness is only verbal.

Examples:

- Hegel and Śaṅkara can share a whole/part pressure point without sharing a soteriology.
- Madhva and Levinas can both preserve irreducibility, but in radically different registers.
- Derrida and later Advaita can both attack naive presence-talk while moving toward very different metaphysical consequences.

## §7 — Four verdicts for comparisons

The graph still needs verdicts, but the verdict now applies to a pair of commitments, not to whole thinkers.

### V1 — `shared-axis`

The two claims are genuinely on the same primitive and in the same register, even if they differ in value.

Example:

- Śaṅkara and Madhva on `manifestation_status` in the metaphysical register.

### V2 — `terminological-near-match`

The wording looks close, but the architecture underneath is different.

Example:

- general "non-duality" talk across Śaṅkara, Rāmānuja, and Vivekananda.

### V3 — `genuine-disagreement`

The claims sit on the same primitive, in the same register, with incompatible values.

Example:

- Madhva versus Śaṅkara on whether finite difference is sublatable.

### V4 — `register-shift`

The apparent clash dissolves once the register is tagged correctly.

Example:

- Adorno's anti-totalization warnings and Aurobindo's metaphysics of manifestation are not one clean yes/no argument until the register is identified.

## §8 — Worked comparisons

### Example A — Śaṅkara and Madhva

Shared axis:

- `substrate_structure`
- `manifestation_status`
- `finite_cognition_model`
- `epistemic_authority`
- `soteric_end`

Why the disagreement is real:

- Śaṅkara's article grounds `substrate_structure` in `one-self-standing`, while Madhva's grounds it in `one-independent-plus-real-dependents`.
- Śaṅkara's `manifestation_status` is `sublatable-not-null`, while Madhva's is `dependent-real`.
- Madhva treats `bheda` as positive and non-sublatable; Śaṅkara treats difference as valid within `vyavahāra` and sublated in liberating knowledge.

Why the disagreement is not reducible to one axis:

The old framework's temptation was to say both carve the same hierarchy and disagree only about the modal status of the lower level. That is too weak against the actual `madhva.md` treatment of `svatantra/paratantra`, `viśeṣa`, and `pañcabheda`.

Verdict:

- `genuine-disagreement`

### Example B — Hegel and Deleuze

Shared axis:

- `determination_operator`
- `temporal_mode`
- `individuation_status`

Why the disagreement is real:

- Hegel makes contradiction and mediated negation the motor of determinacy.
- Deleuze makes difference primary without letting it be exhausted by contradiction.

Why the disagreement is not only semantic:

The difference reaches ontology, individuation, and history. It is not a mere vocabulary fight about dynamism.

Verdict:

- `genuine-disagreement`

### Example C — K.C. Bhattacharyya and Hegel

Shared axis:

- `modal_structure_of_truth`
- `relation_to_perspectivism`

Why the encounter matters:

- Hegel moves toward a totalized intelligibility in which partial views are aufgehoben.
- K.C. Bhattacharyya keeps alternative absolutes genuinely irreducible.

Verdict:

- `genuine-disagreement`

### Example D — Foucault and Mīmāṃsā

Shared axis:

- `normative_order_source`
- `semantic_mediation`

Why the apparent nearness is mostly false:

- Both care about the production of binding practice.
- Mīmāṃsā grounds bindingness in scriptural injunction.
- Foucault grounds it in historically contingent dispositifs and power-relations.

Verdict:

- `register-shift` followed by `genuine-disagreement`

### Example E — Nāgārjuna and Candrakīrti

Shared axis:

- `selfhood_structure`
- `constitution_structure`
- `method_of_critique`
- `determination_operator`

What the graph must not do:

- It must not encode emptiness as one more weak value under world-status alone.
- It must not treat `prasaṅga` as a decorative polemical style.

Why the new grammar helps:

- `selfhood_structure = no-enduring-self` names the `anātman` pressure directly.
- `constitution_structure = dependent-arising-without-constituting-subject` marks the refusal to posit a constituting self behind appearance.
- `method_of_critique = prasanga-anti-thesis` distinguishes Candrakīrti's anti-`svatantra` procedure from Bhāviveka's inferential strategy.

Verdict:

- Nāgārjuna and Candrakīrti share the main anti-essential pressure.
- Candrakīrti and Bhāviveka are in `genuine-disagreement` on method even where they share the larger Mādhyamaka objective.

### Example F — Husserl and Yogācāra

Shared axis:

- `constitution_structure`
- `finite_cognition_model`
- `relation_to_perspectivism`

Why the comparison is real:

- Both refuse the fiction of a brute object standing there before all lived articulation.
- Both give a structured account of how world-appearance is built.

Why the comparison must stop short of identity:

- Husserl's noesis/noema correlation is not an `ālaya-vijñāna`.
- Yogācāra's transformed flow of consciousness is not a transcendental ego under another name.

Verdict:

- `shared-axis`
- followed, in most concrete claims, by `genuine-disagreement`

### Example G — Jaina plural realism against easy relativism

Shared axis:

- `modal_structure_of_truth`
- `relation_to_perspectivism`
- `standpoint_predication`

Why the old graph was too weak:

- `standpoint-conditioned-realism` by itself can still be misread as "many views, none final."
- The Jaina texts say something sharper: reality is many-sided, and predication must be qualified accordingly.

Why the new primitive matters:

- `standpoint_predication = standpoint-indexed-predication` for `naya`
- `standpoint_predication = sevenfold-conditioned-predication` for `syādvāda`

Verdict:

- `genuine-disagreement` with any system that insists on unqualified single-predication at the same level of discourse

## §9 — Register discipline

The graph will fail if it lets one register quietly occupy the whole field.

Three warnings matter most for this corpus.

### 1. Metaphysical vocabulary often migrates into soteriological prose

Ramakrishna, Vivekananda, and many Bhakti thinkers use identity-language, manifestation-language, and path-language in close sequence. The later assignment table has to keep those strands tagged rather than flattening them.

### 2. Political-social analysis is not a disguised ontology by default

Foucault, Adorno, and Marx-adjacent material may have metaphysical implications, but their primary commitments are often about practice, institution, social form, and subject-production. The graph should not force them into a pseudo-Vedāntic substrate debate if the article does not do so.

### 3. Phenomenology is not automatically a metaphysical refusal

Husserl and Heidegger are methodologically restrictive in distinctive ways, but that does not mean "no ontology." It means the ontology is accessed under a special discipline. The graph can record that through `epistemic_authority`, `method_of_critique`, `selfhood_structure`, and `temporal_mode`.

## §10 — Failure modes this framework rejects

### F1 — Importing later school solutions into earlier authors

This is the clearest old failure and remains forbidden.

Examples:

- later Advaita avidyā-locus doctrines read back into Śaṅkara
- later systematizing glosses treated as if they were original first-order commitments

### F2 — Treating every similarity as convergence

If two thinkers both say "non-dual," "whole," "difference," "freedom," or "manifestation," the graph still has to ask:

- which primitive?
- which register?
- which value?

Without that discipline, the corpus slides back into slogan-comparison.

### F3 — Overfitting the graph to one local polemic

The user's frustrations about previous primitive work were justified. The graph cannot be a disguised instrument for one Madhva/Advaita complaint, one Nietzsche-on-grammar complaint, or one Aurobindo-centered synthetic thesis. It has to stay general enough to survive contact with the entire corpus.

### F4 — Forcing Western comparators into leftover status

Hegel, Nietzsche, Husserl, Heidegger, Whitehead, Bergson, Derrida, Foucault, Adorno, Levinas, and Prigogine now have enough article weight that the graph must be able to locate them directly.

### F5 — Confusing article support with school rumor

Where the article corpus is strong, use it.

Where only the JSON is available, say so.

Where neither layer settles the issue, use `withheld`.

## §11 — How the later JSON field should look

Each thinker JSON now carries a `primitive_commitments` array and a `cross_engagements` array.

The commitment object should stay this thin:

```json
{
  "primitive": "substrate_structure",
  "value": "one-independent-plus-real-dependents",
  "register": "metaphysical",
  "citation_locus": "cite://madhva/tattva-sankhyana/1-4",
  "confidence": "high"
}
```

The cross-engagement object should mirror the inline article passage without dragging the whole paragraph into the registry:

```json
{
  "counter_thinker": "sankara",
  "primitive": "manifestation_status",
  "agreement_type": "genuine-disagreement",
  "register": "metaphysical",
  "brief": "Śaṅkara marks the world as sublatable under brahma-jñāna rather than as fully real in its dependent standing.",
  "citations": ["cite://sankara/brahma-sutra-bhasya/1.1.1"],
  "source_article": "data/articles/source/madhva.md",
  "source_locus": "madhva.md:175"
}
```

If the commitment is mixed by register, store two objects.

If the evidence is too thin, lower the confidence. Use `withheld` only when the data model truly needs an explicit non-assignment.

## §12 — How article cross-engagement passages should be written

Each source article will gain short cross-engagement passages tied to the primitive-axis currently under discussion.

The passage should:

- name the other thinker
- name the shared primitive
- say whether the relation is agreement, disagreement, subsumption, sharpening, or register-shift
- cite a primary text for the comparison thinker

Example template:

> Cross-engagement: Rāmānuja presses the same `identity_relation` axis, but reads the `jīva` as a real body-mode of Brahman rather than as non-different witness-consciousness ([Śrī-bhāṣya 1.1.1](cite://ramanuja/sri-bhasya/1.1.1)). The disagreement is metaphysical, not merely devotional.

That is the level of granularity later Phase 3 work should target.

## §13 — Article-level plug-in examples

### Example A — Śaṅkara article

Minimum high-confidence commitments:

- `substrate_structure = one-self-standing`
- `manifestation_status = sublatable-not-null`
- `identity_relation = non-otherness`
- `selfhood_structure = witness-self`
- `finite_cognition_model = adhyasa-or-superimposition`
- `epistemic_authority = scripture-dominant`
- `practice_path = knowledge-discipline`
- `soteric_end = identity-with-ground`

Cross-engagement targets that article should naturally host:

- Madhva on `manifestation_status`
- Rāmānuja on `identity_relation`
- Husserl on `selfhood_structure`
- Derrida on `semantic_mediation`
- Aurobindo on `manifestation_status` and `practice_path`

### Example B — Hegel article

Minimum high-confidence commitments:

- `substrate_structure = one-self-standing` only if the article insists on absolute Spirit as self-grounding whole; otherwise use `withheld` and let `temporal_mode`, `determination_operator`, and `modal_structure_of_truth` carry the load
- `individuation_status = reducible-to-the-whole`
- `determination_operator = negation-and-contradiction`
- `method_of_critique = dialectical-development`
- `temporal_mode = process-primary`
- `register_of_evolution = sublative-becoming`
- `relation_to_perspectivism = sublated-into-higher-whole`
- `normative_order_source = ethical-life-in-institutions`
- `social_formation_model = recognitive-institutional`
- `soteric_end = recognition-or-freedom`

Cross-engagement targets that article should naturally host:

- Deleuze on `determination_operator`
- Nietzsche on `relation_to_perspectivism`
- Adorno on `social_formation_model`
- K.C. Bhattacharyya on `modal_structure_of_truth`
- Aurobindo on `register_of_evolution`

### Example C — Foucault article

Minimum high-confidence commitments:

- `manifestation_status = socially-or-discursively-stabilized`
- `selfhood_structure = split-or-produced-subject`
- `finite_cognition_model = genealogically-produced-illusion`
- `epistemic_authority = genealogical-critique`
- `determination_operator = genealogical-exposure`
- `method_of_critique = genealogy`
- `normative_order_source = disciplinary-power`
- `social_formation_model = disciplinary-production-of-subjects`
- `practice_path = critical-genealogical-work`
- `soteric_end = not-soteriological`

Cross-engagement targets that article should naturally host:

- Nietzsche on genealogy
- Butler on performative repetition
- Adorno on social totality
- Mīmāṃsā on binding practice
- Heidegger on disclosure versus historical formation

## §14 — Corpus-wide adequacy check

This grammar counts as adequate only if it can house the following clusters without strain.

### Cluster 1 — Vedānta school disputes

Needed primitives:

- `substrate_structure`
- `manifestation_status`
- `identity_relation`
- `causation_model`
- `selfhood_structure`
- `practice_path`
- `soteric_end`

### Cluster 2 — Trika and Śaiva comparators

Needed primitives:

- `manifestation_status`
- `selfhood_structure`
- `finite_cognition_model`
- `semantic_mediation`
- `affective_motive_force`
- `practice_path`

### Cluster 3 — Mīmāṃsā, Nyāya, and pramāṇa traditions

Needed primitives:

- `epistemic_authority`
- `method_of_critique`
- `semantic_mediation`
- `normative_order_source`
- `determination_operator`

### Cluster 4 — German idealism, phenomenology, and deconstruction

Needed primitives:

- `selfhood_structure`
- `determination_operator`
- `method_of_critique`
- `temporal_mode`
- `modal_structure_of_truth`
- `relation_to_perspectivism`
- `semantic_mediation`

### Cluster 5 — Genealogy, critical theory, and social diagnosis

Needed primitives:

- `finite_cognition_model`
- `epistemic_authority`
- `method_of_critique`
- `normative_order_source`
- `social_formation_model`
- `practice_path`

### Cluster 6 — Process, emergence, and evolutionary metaphysics

Needed primitives:

- `substrate_structure`
- `causation_model`
- `temporal_mode`
- `register_of_evolution`
- `soteric_end` where a transformed-life endpoint exists

The present set covers all six clusters.

## §15 — Closing constraint

The graph has one final discipline.

When the corpus does not support a strong claim, do not compensate with stylistic confidence.

The later phases can be ambitious only if the assignments remain reversible:

- revise a value when a better article exists
- split a value by register when the article demands it
- withhold a value when the evidence is thin

That is how the graph stays general instead of turning into another selective map.
