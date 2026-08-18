# Roster admission queue

This is a source-first queue, not a list of names to add automatically. A
candidate becomes a visible timeline entry only after its identity, dates,
authorship/transmission status, and minimum source record are sufficient for
the entry type described in [Content and source standard](CONTENT_AND_SOURCE_STANDARD.md).

## Already present — do not duplicate

- Gautama Buddha (`data/thinkers/gautama-buddha.json`) and Mahāvīra
  (`data/thinkers/mahavira.json`) are already present as canonical-teacher
  records. They are not represented as autograph authors.
- Kṛṣṇadāsa Kavirāja, Gopāla Bhaṭṭa Gosvāmī, Raghunātha dāsa Gosvāmī,
  Prabodhānanda Sarasvatī, and Parāśara Bhaṭṭar are already manifest-listed.
  Older gap notes that call them missing are historical audit artifacts, not an
  instruction to create duplicate records.
- Swami Chinmayananda and Swami Sivananda were added in the 2026-08 roster
  wave with catalogue-verified works marked `primary-text-not-in-corpus`.
  They need rights-cleared local witnesses before passage-level claims.

## Next source packet: Dharmatrāta

Dharmatrāta is the highest-priority confirmed gap from the former Abhidharma
audit. Do **not** add a record until the packet resolves which historical
Dharmatrāta is meant, distinguishes Chinese/Tibetan transmission from Sanskrit
survival, identifies the relevant Vasubandhu/Yaśomitra time-theory locus, and
records its edition/witness status. A name-only entry would conflate distinct
authors and defeat the provenance policy.

## Needs acquisition before admission

- **Śāradā Devī:** public scan witnesses are known, but original-language
  coverage and rights/edition status are not yet sufficient for a source-grounded
  philosophical-author entry.
- **Nāḍādūr Ammāḷ / Vātsya Varadaguru:** acquire and identify a stable witness
  for *Tattva-sāra* before deciding whether the record belongs in the primary
  timeline or in a reception/secondary lane.
- **Puruṣottama Prasāda:** acquire a readable, identified *Śruty-anta* witness
  and verify that the author is distinct from similarly named Nimbārka figures.

## Excluded unless an attributed philosophical text is identified

Ramakrishna and Śāradā Devī are not currently thinker records. Their public
reception materials remain valuable article and source context, but disciple
records alone do not meet the roster's author/attributed-text criterion. Do not
add either as a public thinker unless a serious philosophical text can be
identified with a documented authorship or traditional-attribution status.

The existing Buddha and Mahāvīra `canonical_teacher` records are a separate
legacy exception under review; they do not establish a general mystic or oral-
teacher category and must never be described as autograph authors.
