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
- a complete slotted literal translation;
- a separate final translation produced only after word review;
- per-word morphology, kāraka, compound vigraha, real morpheme segmentation, and exact Dhātupāṭha evidence for every root claim;
- every source-supported parallel derivation or nirvacana, separated by category and evidence;
- attached textual apparatus where the Laghu, critical, and vulgate witnesses diverge;
- bidirectional Sanskrit-English highlighting and click-open contextual cards through the shared Gītā reader.

## Release gate

The former prose-first sample was withdrawn in commit `a529749`. Do not restore an article-manifest entry until all 56 units have exact source/pada/slot replay, complete non-placeholder grammar, full glossary coverage, apparatus placement, and an independent Sanskrit review with zero concrete errors.
