# Dāmādyupākhyāna reader — source-resolution and release record

## Controlling population

- Work: *Laghu-Yoga-Vāsiṣṭha*.
- Locus: Sthiti-prakaraṇa, sarga 2, verses 31-86.
- Narrative: the complete concise Dāma-Vyāla-Kaṭa story, including its frame and close.
- Stable IDs: `lyv-4-2-31` through `lyv-4-2-86`.
- Expected/observed source units: 56/56.
- Machine-readable packet: `data/sources/sanskrit/vedanta/laghuyogavasistha_dama_story.json`.

## Witness hierarchy

1. Controlling Laghu text: Vāsudeva Śarmā Paṇaśīkara's Nirṇaya Sāgar edition, visually checked on printed pp. 302-309 in the 1937 scan.
2. Paired transcription: Muktābodha M00351 Devanāgarī and IAST, used for exact transport and extraction.
3. Parallel historical-critical text: *Mokṣopāya*, Sthitiprakaraṇa, ed. Susanne Krause-Stinner and Peter Stephan (2012), repository GRETIL transformation.
4. Later vulgate: repository `yogavasistha_sanskritsahitya.txt`.
5. Swami Venkatesananda's 1993 English is a story locator and comparison translation only; it does not control Sanskrit or site English.

## Decisive apparatus findings

- The historical-critical *Mokṣopāya* reads `yantrapuruṣāḥ` at MU 4.9.38: *yantra* + *puruṣa*, “machine-persons / mechanical persons.”
- The later vulgate parallel reads `atyajñapuruṣāḥ` at YV 4.27.38.
- The Laghu text omits that line, while condensing the construction account into 2.44-48.
- The longer critical construction cluster, MU 4.7.34-39, supplies `cetanāmātradharmiṇaḥ`, `nirvikalpakacinmātraparispandaikakarmiṇaḥ`, `kṛtrimām`, the automatic-sequence comparison, and the half-asleep-child comparison.
- Laghu 2.33 and the printed scan read `mīmabhāsadṛḍhasthitim`; parallel witnesses and the immediately preceding verse have `bhīmabhāsa-`. The controlling reading is preserved and the variant must be displayed, never silently repaired.

## Required public artifact

The replacement is a root-text reading, not an essay. Each of the 56 units must provide:

- printed Devanāgarī saṃhitā;
- reviewed, sandhi-resolved IAST pada-pāṭha;
- one complete slotted, grammar-faithful translation produced after word review;
- per-word morphology, kāraka, compound vigraha, real morpheme segmentation, and exact Dhātupāṭha evidence for every root claim;
- every source-supported parallel derivation or nirvacana, separated by category and evidence;
- inherited semantic fields kept active when the narrative engages them, with earlier meanings distinguished from later reception;
- attached textual apparatus where the Laghu, critical, and vulgate witnesses diverge;
- bidirectional Sanskrit-English highlighting and click-open contextual cards through the shared Gītā reader.

## Interpretive method

The reader treats the work as intentional philosophical literature. Its default
hermeneutic is Aurobindonian: the grammatical and narrative surface remains
true, while the same verified language may simultaneously operate in an inward
psychological and philosophical register. Earlier grammatical formations,
lexical senses, and nirvacanas are therefore treated as part of the inherited
semantic field available to the author when the present narrative activates
them. Later readings are preserved as reception history rather than silently
backdated.

This is not an alternative to critical philology. Philology establishes which
words occur in the Laghu, critical Mokṣopāya, and later received Yoga-Vāsiṣṭha,
and in which chronological relation. The depth-reading then engages those
verified words as deliberate literature. Regular grammar, earlier nirvacana,
lexical attestation, narrative activation, later reception, and site synthesis
remain separately labelled.

The term *vulgate* in this reader means the commonly received and printed
expanded Yoga-Vāsiṣṭha. It is not a judgment of spiritual worth. The critical
Mokṣopāya preserves `yantrapuruṣāḥ`; the later received text reads
`atyajñapuruṣāḥ`; the Laghu omits the line. Swami Venkatesananda's
“robot-like working projections” is a contextual summary of the construction
and automatic-action account, not a direct translation of a printed
`yantrapuruṣa` token in his later received witness.

## Release gate

The former prose-first sample was withdrawn in commit `a529749`. The replacement reader meets the closed release gate:

- 56/56 source units and 599/599 public word analyses replay against the controlling packet;
- 409/409 exact source-script tokens map, in order, to the full reviewed pada population;
- each unit presents one complete slotted, grammar-faithful English translation; there is no duplicate unlinked translation block;
- 2.33's printed `mīma-` retained with its `bhīma-` parallel, and the critical/vulgate mechanical-person apparatus attached after 2.64;
- every cited root resolves to exact paired Prakriya source witnesses, with parallel derivations and nirvacanas kept distinct in the interactive cards;
- four independent review packets report zero concrete errors against frozen producer hashes:
  - 2.31-44: `195a2ce197e445fb3d390668a7dc757a71d943bf27d41291ec72cbd3af385b59`;
  - 2.45-58: `f1356d18163aef0e87f183f98d3c4045ffaaa59c6f102fc502d7e27c87d59b29`;
  - 2.59-72: `45b0bee4bd34ac7704ae4446316729596cc5126fa6461be2554711bba57beec7`;
  - 2.73-86: `4bc8c01cdca6ae5d23d92d222688c7e0a26012de235265f2ab6cd94b2c05df03`.
- the 12/12 inherited semantic fields, 4/4 methodology principles, and 4/4 witness-history stages independently pass at registry hash `2ab3015e0b21f5566bccd4aff9056904758770cf096ad60146a9689cb2ff62cc`.

The validator recomputes these hashes and fails closed on a stale, incomplete, or non-passing review. Publication additionally requires the deterministic content suite, responsive browser interaction QA, and a live post-deploy replay.
