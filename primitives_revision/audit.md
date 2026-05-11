# Audit of `primitive-model.md` and `comparative-claims-framework.md`

## Scope

This audit checks four things:

1. Whether `data/articles/source/primitive-model.md` states positions that the on-disk thinker articles actually support.
2. Whether `data/articles/source/comparative-claims-framework.md` stages disagreements with enough care.
3. Whether the framework over-centers "the user's" position where a neutral apparatus should speak in its own voice.
4. Whether the current corpus collapses the "ontologized grammar" line into Nietzsche's grammar critique.

Line references below are to on-disk files.

## Executive Findings

1. The current apparatus treats a sub-school map as though it were a neutral primitive grammar. `primitive-model.md` does not only define axes; it assigns values in ways that import later Advaita, later polemics, and reconstruction claims directly into earlier figures. The clearest case is the Śaṅkara row at `primitive-model.md:143`, which loads Bhāmatī, Vivaraṇa, and "later" avidyā options into "Śaṅkara-bhāṣya" itself.
2. Madhva is not well served by the current table. The label `hierarchical-dependent` at `primitive-model.md:151` catches one structural feature, but the row strips out the work done by `svatantra/paratantra`, `tāratamya`, `viśeṣa`, and the positive ontological status of `bheda`. The causation entry is also too neat against the source article.
3. The framework overstates convergence between Advaita and Tattva-vāda. The claim that Madhva's `svatantra/paratantra` and Advaita's `pāramārthika/vyāvahārika` "carve the same hierarchy" at `primitive-model.md:179`, `primitive-model.md:196`, and `comparative-claims-framework.md:16` is too strong for the article corpus on disk.
4. Several thinker rows are asserted with a confidence that the corpus does not justify. For many named figures there is no standalone `data/articles/source/<id>.md` at all. The table still assigns settled primitive-values.
5. The framework scarcely addresses the Western comparators the site now needs. Outside a passing comparator-row for Abhinavagupta at `primitive-model.md:158` and a Trika comparison note at `comparative-claims-framework.md:120`, the present apparatus has not even tried to encode Hegel, Nietzsche, Schopenhauer, Spinoza, Kant, Heidegger, Husserl, Wittgenstein, Leibniz, Deleuze, K.C. Bhattacharyya, Whitehead, or Bergson.
6. "The user's" thesis, polemic, line, or prohibition is named too often. A framework document should mark a live dispute only where the position belongs to a single author rather than to the apparatus as such.
7. The current corpus does, in places, reduce the "ontologized grammar" complaint to Nietzsche's grammar line. Hegel's article is more careful than that in some sections, but the framing sentence at `hegel.md:38` and the reuse of that frame elsewhere encourage the flattening the user objected to.

## Files Read

Framework files read in full:

- `data/articles/source/primitive-model.md`
- `data/articles/source/comparative-claims-framework.md`

Vedāntic and comparator source articles checked:

- `data/articles/source/shankara.md`
- `data/articles/source/ramanuja.md`
- `data/articles/source/madhva.md`
- `data/articles/source/caitanya.md`
- `data/articles/source/vivekananda-ramakrishna.md`
- `data/articles/source/aurobindo.md`
- `data/articles/source/hegel.md`
- `data/articles/source/nietzsche.md`
- `data/articles/source/spinoza.md`
- `data/articles/source/heidegger.md`
- `data/articles/source/husserl.md`
- `data/articles/source/kc-bhattacharyya.md`
- `data/articles/source/whitehead.md`
- `data/articles/source/bergson.md`
- `data/articles/source/leibniz.md`
- `data/articles/source/deleuze.md`

Thinker JSON files checked for every named figure in scope.

## Framework-Level Problems

### 1. The table treats later intra-school disputes as if they were first-order primitive facts

- `primitive-model.md:143` assigns to "Advaita — Śaṅkara-bhāṣya" three rival avidyā-locus positions: `brahman-as-locus (Vivaraṇa) / jiva-as-locus (Bhāmatī) / tritiya-padartha (later)`.
- The source article says the opposite. `shankara.md:24` states that developed `vivarta` language is later and that Sureśvara avoids it. `shankara.md:815-823` says the locus problem is not formally solved in Śaṅkara and that Bhāmatī and Vivaraṇa are later attempts. The article is explicit that these are later systematizations, not settled Śaṅkara-bhāṣya positions.
- Result: the row misrepresents Śaṅkara by conflating the bhāṣya layer with later Advaita architecture.

### 2. The table often presents analogy as doctrine

- `primitive-model.md:117-130` is valuable as a list of analogies, but many later assignments rely on those analogies as if the analogy itself fixed the primitive-value.
- `primitive-model.md:133` warns that analogy-citation alone never settles doctrine. The table then ignores its own warning by making row-level assignments that are under-argued in the article corpus.

### 3. The pairwise convergence section is stronger than the evidence

- `primitive-model.md:179`, `primitive-model.md:182`, and `primitive-model.md:196` push the line that Madhva and Advaita share the same two-tier structure and differ only on the modal status of the dependent tier.
- `comparative-claims-framework.md:16` and `comparative-claims-framework.md:93-96` say much the same.
- The Madhva article does not permit that reduction. `madhva.md:70-95` makes `svatantra/asvatantra` an aseity-structure with real plural dependents. `madhva.md:101-113` and `madhva.md:181-185` make `pañcabheda` positively real and non-sublatable. `madhva.md:203-227` adds `viśeṣa` as a load-bearing ontological device. This is not just a relabeling of `pāramārthika/vyāvahārika`.

### 4. The framework speaks as if it already had a cross-tradition grammar for Western thinkers; it does not

- `primitive-model.md` names no Western thinker other than the comparator row for Abhinavagupta at `primitive-model.md:158`.
- `comparative-claims-framework.md` names none of Hegel, Nietzsche, Schopenhauer, Spinoza, Kant, Heidegger, Husserl, Wittgenstein, Leibniz, Deleuze, K.C. Bhattacharyya, Whitehead, or Bergson in its worked examples or categories.
- The present apparatus therefore cannot do the job the project now needs from it.

## Vedāntic Thinker Audit

### Śaṅkara

Framework claim:

- `primitive-model.md:143` assigns `one`, `mithya-not-asat`, `numerical-identity`, `vivarta`, and a menu of later avidyā-locus options to "Śaṅkara-bhāṣya."

What the article says:

- `shankara.md:21-25` states four corrections: `mithyā` is not `asat`; there is a three-tier ontology; Śaṅkara does not use `vivarta` as a developed technical term; and `bheda-śrutis` are taken seriously.
- `shankara.md:146-148` stresses `ananyatva`, not flat `abheda`, in the effect-cause relation.
- `shankara.md:315-317` says difference is affirmed at the `vyāvahārika` level, not erased.
- `shankara.md:815-823` says the avidyā-locus problem is a later debate rather than a settled bhāṣya claim.

Audit judgment:

- `mithya-not-asat` is supported.
- `numerical-identity` is too blunt if read without the article's care about `ananyatva`, witness-consciousness, and pedagogical register.
- `vivarta` is too confident when attached directly to Śaṅkara.
- The avidyā-locus menu is a misrepresentation if presented as Śaṅkara's own assignment.

### Maṇḍana

Framework claim:

- `primitive-model.md:145` gives Maṇḍana `jiva-as-locus`, `sruti-coordinate-with-anubhava`, and `coordinate-with-jnana`.

What the JSON says:

- `mandana.json:40` makes `jīva`-locus avidyā and `prasaṅkhyāna` central.
- `mandana.json:487-490`, `mandana.json:772`, and `mandana.json:1149` support the `jīva`-locus and post-vākya contemplative assimilation.

Audit judgment:

- The row is directionally closer than the Śaṅkara row.
- The row still oversimplifies by compressing Maṇḍana's `prasaṅkhyāna` doctrine into a generic `coordinate-with-jnana`.
- There is no standalone `data/articles/source/mandana.md`, so the framework states settled primitive-values without a source article on disk.

### Sureśvara

Framework claim:

- `primitive-model.md:144` gives Sureśvara `brahman-as-locus`, `vivarta`, and `preparatory-only`.

What the JSON says:

- `sureshvara.json:30` supports `jñānād eva`, Brahman-locus avidyā, and rejection of `jñāna-karma-samuccaya`.
- `sureshvara.json:48` and `sureshvara.json:73` repeat that profile.

Audit judgment:

- The broad profile is supported by the JSON.
- The `vivarta` label remains too quick if the frame is supposed to distinguish Śaṅkara's own bhāṣya layer from later Vivaraṇa hardening.
- There is no standalone `data/articles/source/sureshvara.md`, so the row is under-supported at the article layer.

### Vāchaspati

Framework claim:

- `primitive-model.md:147` assigns a Bhāmatī row with `jiva-as-locus`.

What the JSON says:

- `vacaspati.json` was checked; the `core_thesis` supports jīva-locus avidyā and the Bhāmatī line.

Audit judgment:

- This row is plausible as a sub-school row.
- There is no standalone `data/articles/source/vacaspati.md`. The framework still presents the row as settled without an article on disk.

### Prakāśātman

Framework claim:

- `primitive-model.md:146` assigns a Vivaraṇa row with Brahman-locus avidyā and a substance-empty reflection reading.

What the JSON says:

- `prakasatman.json` supports the Vivaraṇa line and Brahman-locus avidyā.

Audit judgment:

- Plausible as a sub-school row.
- No standalone `data/articles/source/prakasatman.md` exists, so the row again outruns the article layer.

### Madhusūdana

Framework status:

- No dedicated row in `primitive-model.md`, though the comparative framework names him at `comparative-claims-framework.md:111`, `comparative-claims-framework.md:117`.

What the JSON says:

- `madhusudana.json:836-844`, `madhusudana.json:1044`, `madhusudana.json:1077-1086`, and `madhusudana.json:1270-1286` show that bhakti is not a mere preparatory aid in his corpus.

Audit judgment:

- The apparatus cannot speak cleanly about Madhusūdana because he appears in comparison prompts but not in the primitive assignment table.
- Any new grammar must account for his Advaita plus strong bhakti integration.

### Vidyāraṇya

Framework status:

- No dedicated row in `primitive-model.md`, though he is invoked in `comparative-claims-framework.md:94`.

What the JSON says:

- `vidyaranya.json:48` gives a clear Vivaraṇa profile.
- `vidyaranya.json:90` and `vidyaranya.json:111` make `jīvanmukti`, `vāsanā-kṣaya`, and pedagogical synthesis central.
- `vidyaranya.json:132-140` and `vidyaranya.json:314-333` support the twofold `prakṛti` mapping of māyā and avidyā.

Audit judgment:

- The present framework uses Vidyāraṇya polemically without ever assigning him a row.
- That is a design gap, not a minor omission.

### Rāmānuja

Framework claim:

- `primitive-model.md:148` assigns `one-with-internal-distinctions`, `real-dependent-mode`, `aṃśa-aprthak-siddha`, `body-soul-causation`, and bhakti as constitutive of saving cognition.

What the article says:

- `ramanuja.md:19` states one Brahman qualified by real modes under inseparable qualification.
- `ramanuja.md:49-51` puts the positive doctrine and anti-avidyā critique together.
- `ramanuja.md:559-567` and nearby sections distinguish him both from Śaṅkara and from stronger pluralists.

Audit judgment:

- This row is mostly sound.
- Two compressions need notice. First, `1-internal` at `primitive-model.md:148` is too schematic for a body-soul ontology. Second, the comparison claim at `primitive-model.md:182` that Viśiṣṭādvaita and Tattva-vāda may be "terminological on P1" goes too far against the article's insistence on the specific `śarīra-śarīrī` relation.

### Madhva

Framework claim:

- `primitive-model.md:151` assigns `hierarchical-dependent`, `real-dependent-mode`, `bimba-pratibimba-with-eternal-distinction`, `nimitta-and-upādāna-by-real-dependence`, `5-pañca-bheda`, domain-specific pramāṇa pluralism, and bhakti as constitutive.
- `primitive-model.md:179`, `primitive-model.md:182`, and `primitive-model.md:196` then argue that Madhva and Advaita share the same two-tier substrate structure.
- `comparative-claims-framework.md:74-96` uses the same line in worked-example form.

What the article says:

- `madhva.md:11` rejects the lazy label "dualism" because Madhva's system is one independent reality and many dependents.
- `madhva.md:24-25` defines the `svatantra/paratantra` split.
- `madhva.md:35` introduces `viśeṣa` as a real self-differentiating factor.
- `madhva.md:39-40` introduces `bimba-pratibimba` and `pañcabheda`.
- `madhva.md:58-60` says ontology is structured by `pañcabheda` plus `viśeṣa`.
- `madhva.md:70-95` says dependence is continuous, asymmetrical, and constitutive of the dependent's reality.
- `madhva.md:89` says the dependents are real-distinct entities, not body-modes.
- `madhva.md:95` says `pañcabheda` follows from the basic architecture and is not a detachable add-on.
- `madhva.md:101-113` says the five differences are real and non-sublatable.
- `madhva.md:139-145` says `prakṛti` is material cause and Viṣṇu efficient cause, complicating the table's `nimitta-and-upādāna-by-real-dependence`.
- `madhva.md:153-157` adds intrinsic jīva-differences.
- `madhva.md:181-185` makes real difference necessary for intelligibility of practice.
- `madhva.md:203-227` gives `viśeṣa` a positive ontological role.
- `madhva.md:537-547` and `madhva.md:557-559` show the later school preserving the same architecture.
- `madhva.md:615` says this is not a symmetric dualism.

Audit judgment:

- The label `hierarchical-dependent` is accurate as a first pass. It is better than "dualism."
- It is still an oversimplification if it is then used to claim isomorphism with Advaita's two-tier ontology.
- The table underplays four things that the article treats as load-bearing: `svatantra/paratantra` as aseity-structure, `tāratamya`, `viśeṣa`, and `bheda` as a positive ontological fact.
- The causation entry is weak. The article's own wording at `madhva.md:139-145` makes `prakṛti` the material cause and Viṣṇu the efficient cause, which does not fit neatly under `nimitta-and-upādāna-by-real-dependence`.
- The comparison verdict at `primitive-model.md:196` is too strong. The live disagreement is not just P2 `mode_status`; P1 itself is differently built once `viśeṣa`, real plurality, and non-sublatable difference are kept in view.

### Vyāsatīrtha

Framework status:

- No dedicated row; named only in `comparative-claims-framework.md:111`.

What the JSON says:

- `vyasatirtha.json:50` gives the full Navya-Tattva-vāda profile.
- `vyasatirtha.json:68` and `vyasatirtha.json:88` show that his importance is not only doctrinal repetition of Madhva but a new formal dialectical register.

Audit judgment:

- The present framework cannot state what is distinctive in Vyāsatīrtha because it has no primitive for inferential form, dialectical register, or technical metalanguage.

### Bhāskara

Framework claim:

- `primitive-model.md:152` gives Bhāskara `real-pariṇāma`, `bhedabheda-svabhavika (via aupādhika)`, and `constitutive-of-saving-cognition (jñāna-karma-samuccaya)`.

What the JSON says:

- `bhaskara.json:33` supports real transformation, real world, conditional difference by `upādhi`, and `jñāna-karma-samuccaya`.
- `bhaskara.json:51` confirms the same picture.

Audit judgment:

- Broadly supported.
- The row compresses Bhāskara's central anti-Advaita charge and realist argument into a small tuple. That is acceptable in a true primitive grammar, but the current table does not state that this is a compression from a richer position.
- No standalone `data/articles/source/bhaskara.md` exists, so the support is JSON-only.

### Yādava Prakāśa

Framework claim:

- `primitive-model.md:153` gives Yādava a settled `bhedabheda-svabhavika` row and even says `identity-without-distinction` in some readings.

What the JSON says:

- `yadava-prakasa.json:29` states that he is reconstructed almost entirely through hostile witness and that every reconstruction must mark this dependence.

Audit judgment:

- The row is too confident. The source material itself says reconstruction is hostage to hostile testimony.
- This is a strawman risk built into the current apparatus.

### Nimbārka

Framework claim:

- `primitive-model.md:154` gives Nimbārka `one-with-internal-distinctions`, `real-dependent-mode`, and `bhedabheda-svabhavika`.

What the JSON says:

- `nimbarka.json` supports `svābhāvika-bhedābheda` and a stable triadic ontology of Brahman, cit, and acit.

Audit judgment:

- The row trends too close to Rāmānuja by using `one-with-internal-distinctions` and `real-dependent-mode` as the primary labels.
- Nimbārka needs to be kept distinct from both Viśiṣṭādvaita and Gauḍīya `acintya` loading.
- No standalone `data/articles/source/nimbarka.md` exists.

### Vallabha

Framework claim:

- `primitive-model.md:156` gives Vallabha `real-pariṇāma (avikṛta)`, an `aṃśa`-style identity, and `tirodhāna-śakti` rather than avidyā.

What the JSON says:

- `vallabha.json` supports `avikṛta-pariṇāma`, world-reality, and a strong bhakti path.

Audit judgment:

- The row is broadly plausible.
- No standalone `data/articles/source/vallabha.md` exists, so the support is again JSON-only.

### Caitanya / Jīva Gosvāmī

Framework claim:

- `primitive-model.md:155` gives `one-with-internal-distinctions`, `acintya-bhedabheda`, `acintya-śakti-pariṇāma`, and `sole-and-self-sufficient-means`.

What the article and JSON say:

- `caitanya.md:495-505` distinguishes Madhva from Gauḍīya doctrine with unusual clarity.
- `caitanya.md:525-539` distinguishes Caitanya from Rāmānuja and Nimbārka.
- `caitanya.json:43` and `jiva-gosvami.json` support `acintya-śakti` as the load-bearing concept.

Audit judgment:

- The row is much closer to the article corpus than the Madhva row.
- The entry `sole-and-self-sufficient-means` is too strong if it flattens the full Gauḍīya discipline into a slogan. The article stresses `bhakti-rasa`, `nāma-saṅkīrtana`, and a doctrinal account of `acintya`, not just a dispensability claim.

### Vivekānanda

Framework status:

- No row in `primitive-model.md`.

What the article and JSON say:

- `vivekananda-ramakrishna.md:434-438` says the four yogas converge at the same `vijñāna` landing.
- `vivekananda.json:130` defines Practical Vedānta as metaphysical, not merely ethical rhetoric.

Audit judgment:

- The framework omits Vivekananda even though the article corpus gives material for several new primitives: register plurality, action, manifestation, and post-identity return to the world.

### Ramakrishna

Framework status:

- No row in `primitive-model.md`.

What the article and JSON say:

- `vivekananda-ramakrishna.md:637-656` and `vivekananda-ramakrishna.md:747-749` present the roof-and-stairs doctrine and personal-impersonal bivalence.
- `ramakrishna.json:52` gives the same core thesis.

Audit judgment:

- The omission is serious because Ramakrishna's article already provides material for `temporal_mode`, register discipline, and bivalent reality.

### Aurobindo

Framework status:

- No row in `primitive-model.md`.

What the article and JSON say:

- `aurobindo.json:41` makes real manifestation, Supermind, and evolutionary ascent central.
- `aurobindo.md` repeatedly treats evolution as cosmological fact rather than as a merely pedagogical or dialectical trope.

Audit judgment:

- The current apparatus has no primitive for real evolution, no primitive for process as orthogonal to substance, and no way to state Aurobindo's place without distorting him into a late Vedānta variant.

### Abhinavagupta

Framework claim:

- `primitive-model.md:158` gives Trika a comparator row using `acintya-bhedabheda (svātantrya-ābhāsa)` and `pratyabhijna-recognition`.

What the JSON says:

- `abhinavagupta.json:44` and `abhinavagupta.json:61` make a very different case: one `Anuttara` consciousness, `svātantrya`, `vimarśa`, `ābhāsa`, real manifestation, graded `upāyas`, and a positive account of aesthetics.

Audit judgment:

- The row is reductive. It pulls Trika too close to `acintya-bhedābheda`.
- There is no standalone `data/articles/source/abhinavagupta.md`, so the row is under-supported at the article layer.

## Western Thinker Audit

### Present framework coverage

- Hegel: no characterization in the framework files.
- Nietzsche: no characterization in the framework files.
- Schopenhauer: no characterization in the framework files.
- Spinoza: no characterization in the framework files.
- Kant: no characterization in the framework files.
- Heidegger: no characterization in the framework files.
- Husserl: no characterization in the framework files.
- Wittgenstein: no characterization in the framework files.
- Leibniz: no characterization in the framework files.
- Deleuze: no characterization in the framework files.
- K.C. Bhattacharyya: no characterization in the framework files.
- Whitehead: no characterization in the framework files.
- Bergson: no characterization in the framework files.

The framework therefore does not misstate most of these figures because it does not try to state them at all. The problem is absence.

### Hegel

What the article and JSON say:

- `hegel.json:39` states substance as subject, truth as mediated whole, and becoming through determinate negation.
- `hegel.md:80-89`, `hegel.md:109-115`, and `hegel.md:241-247` make becoming, mediation, and logic-metaphysics central.

Audit judgment:

- The current apparatus has no primitives for `temporal_mode`, relation to perspectivism, or the difference between process and substance as orthogonal rather than rival.
- Hegel is one of the clearest cases showing that the old nine-axis scheme is too Vedānta-specific.

### Nietzsche

What the article and JSON say:

- `nietzsche.json:221` makes interpretation, grammar critique, and affirmation central.
- `hegel.md:138-148` uses Nietzsche as the grammar-critique foil.

Audit judgment:

- The framework has no primitive for perspectivism, no primitive for truth-modal plurality, and no way to mark Nietzsche's refusal of totalizing sublation.

### Schopenhauer

What the JSON says:

- `schopenhauer.json:26` distinguishes world as representation from world as will and treats plurality as phenomenal.

Audit judgment:

- No framework coverage.
- A future graph needs a primitive for modal structure of truth and one for phenomenality without flat illusionism.

### Spinoza

What the JSON says:

- `spinoza.json:39` gives one substance, real modes, immanent causation, and necessity.

Audit judgment:

- No framework coverage.
- Spinoza also shows why "substance" and "process" must be separable primitives: one can have one-substance metaphysics without static ontology.

### Kant

What the JSON says:

- `kant.json:65` gives transcendental idealism, empirical realism, and the appearance/thing-in-itself split.

Audit judgment:

- No framework coverage.
- The graph will need a better way to mark register and domain restrictions.

### Heidegger

What the JSON says:

- `heidegger.json:78` gives Being/beings, Dasein, and truth as unconcealment.

Audit judgment:

- No framework coverage.

### Husserl

What the JSON says:

- `husserl.json:104` gives intentional constitution and transcendental reduction.

Audit judgment:

- No framework coverage.

### Wittgenstein

What the corpus state shows:

- `data/thinkers/wittgenstein.json` was not found.
- No source article is on disk.

Audit judgment:

- The framework cannot cover Wittgenstein at present and should not pretend that it can.

### Leibniz

What the JSON says:

- `leibniz.json` is on disk and was checked for relevant metaphysical markers.

Audit judgment:

- No framework coverage.
- Leibniz will matter for the new `relation_to_perspectivism` primitive, since many irreducible viewpoints coexist without collapsing into one flat relativism.

### Deleuze

What the article and JSON say:

- `deleuze.json` is on disk and was checked.
- The project now needs Deleuze because the user explicitly asked for a sublation example where a critique may subsume a target in one register and fail to do so in another.

Audit judgment:

- No framework coverage at all.
- This is a central absence for the revision.

### K.C. Bhattacharyya

What the article and JSON say:

- `kc-bhattacharyya.json:117` gives freedom from object, alternative forms of the Absolute, and graded subjectivity.
- `kc-bhattacharyya.md:236`, `kc-bhattacharyya.md:305`, `kc-bhattacharyya.md:331`, and `kc-bhattacharyya.md:529` resist any one grammar of ultimacy.

Audit judgment:

- No framework coverage.
- This is one of the strongest arguments for a new primitive such as `scope_of_grammar`.

### Whitehead

What the JSON says:

- `whitehead.json:65` gives actual occasions, process, and concrescence.

Audit judgment:

- No framework coverage.
- The new graph needs `temporal_mode` and `register_of_evolution` partly for Whitehead.

### Bergson

What the article and JSON say:

- `bergson.md` and `bergson.json` treat duration and becoming as central.

Audit judgment:

- No framework coverage.
- The absence confirms that the old model has no place for durée, process, or real novelty.

## User-Reference Inventory

Every "user" reference found in the two framework files:

### In `primitive-model.md`

- `primitive-model.md:34`
- `primitive-model.md:172`
- `primitive-model.md:179`
- `primitive-model.md:181`
- `primitive-model.md:188`
- `primitive-model.md:194`

Audit judgment:

- Only `primitive-model.md:188` may be defensible as a note about a live comparative use of Trika in the project.
- The rest should be stripped or recast in framework voice.

### In `comparative-claims-framework.md`

- `comparative-claims-framework.md:5`
- `comparative-claims-framework.md:94`
- `comparative-claims-framework.md:96`
- `comparative-claims-framework.md:100`
- `comparative-claims-framework.md:111`
- `comparative-claims-framework.md:113`
- `comparative-claims-framework.md:116`
- `comparative-claims-framework.md:120`
- `comparative-claims-framework.md:126`
- `comparative-claims-framework.md:128`
- `comparative-claims-framework.md:159`

Audit judgment:

- `comparative-claims-framework.md:5` is the deepest problem. It defines the whole method as a user's conviction rather than as the apparatus's own disciplined procedure.
- `comparative-claims-framework.md:94`, `comparative-claims-framework.md:96`, and `comparative-claims-framework.md:126-128` hard-wire the user's polemical positions into what should be neutral comparative machinery.

## "Ontologized Grammar" Audit

### The flattening does occur

The strongest evidence is in `hegel.md`:

- `hegel.md:38` frames the issue through Nietzsche's "faith in grammar" remark and then reads Hegel as the sophisticated symptom.
- `hegel.md:138-148` treats Hegel and Nietzsche as two responses to the same grammar problem.
- `hegel.md:245` calls the move from logical category to ontological truth "the original sin of 'ontologized grammar'."

The same compression appears elsewhere:

- `aurobindo.md:767-769` ties Hegel's category error to Nietzsche's grammar line and then extends it to later comparators.
- `chaudhuri-banerji.md:877` says the sharper move is the user's synthesis of K.C.B., Nietzsche, Chomsky, and Sapolsky around Hegel's mistake.

### The corpus also contains the resources not to flatten it

- `hegel.md:42` says Hegel is himself a critic of ordinary predicative grammar.
- `hegel.md:121-146` gives the speculative proposition as Hegel's internal critique of subject-predicate judgment.
- `kc-bhattacharyya.md:236`, `kc-bhattacharyya.md:305`, `kc-bhattacharyya.md:331`, `kc-bhattacharyya.md:339`, and `kc-bhattacharyya.md:529` make the broader point that no single grammar of ultimacy can absorb all alternatives.

Audit judgment:

- The current corpus is not uniformly crude here.
- Still, the headline framing often pushes the reader toward "Nietzsche on grammar" as the master key, which is the reduction the user rejects.
- The revised framework should distinguish:
  - Nietzsche's claim about grammar generating substance-metaphysics.
  - Bhartṛhari and the Vyākaraṇa claim that language or conceptual articulation is constitutive of reality.
  - The stronger project complaint that one mode of articulation has been mistaken for the Real's own structure.

## Specific Misread or Overreach List

1. `primitive-model.md:143` misrepresents Śaṅkara by assigning later Advaita locus debates to "Śaṅkara-bhāṣya."
2. `primitive-model.md:143-145` overstates `vivarta` as a clean primitive across Śaṅkara, Sureśvara, and Maṇḍana against `shankara.md:24`.
3. `primitive-model.md:151` oversimplifies Madhva by flattening `svatantra/paratantra`, `tāratamya`, `viśeṣa`, and positive `bheda`.
4. `primitive-model.md:151` gives Madhva a causation value that fits poorly with `madhva.md:139-145`.
5. `primitive-model.md:153` is too confident about Yādava despite `yadava-prakasa.json:29`.
6. `primitive-model.md:154` drifts Nimbārka too close to Rāmānuja.
7. `primitive-model.md:158` drifts Abhinavagupta too close to Gauḍīya `acintya-bhedābheda`.
8. `primitive-model.md:179`, `primitive-model.md:182`, and `primitive-model.md:196` overstate Advaita-Madhva convergence.
9. `comparative-claims-framework.md:16` and `comparative-claims-framework.md:93-96` carry the same overstatement into the verdict schema.
10. `comparative-claims-framework.md:5` makes the method sound like a personal thesis rather than a comparative discipline.

## What the Revision Must Fix

1. Replace the axis-table voice with a graph voice that distinguishes primitive-nodes, thinker commitments, and critique/subsumption edges.
2. Add primitives for process, evolution, perspectivism, truth-modality, and grammar-scope.
3. Separate metaphysical, epistemic, soteriological, and methodological registers before assigning values.
4. Treat unsupported thinkers as unsupported rather than as settled tuples.
5. Rebuild the Madhva section around `svatantra/paratantra`, `tāratamya`, `viśeṣa`, and `pañcabheda`, not around a thin "dependent hierarchy" shorthand.
6. Strip most "user" references from the apparatus.
7. State the "ontologized grammar" issue in a way that does not collapse it into Nietzsche's narrower claim.
