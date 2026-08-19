# GitHub source audit

GitHub is useful for finding and inspecting textual witnesses, but a repository
is not automatically an authority. This audit records the current
thinker-first results and the exact intake posture for each route.

## Acquisition route: SARIT

[`sarit/SARIT-corpus`](https://github.com/sarit/SARIT-corpus) is the strongest
GitHub route currently found. Its individual TEI files contain named
editorial/edition information and a per-file Creative Commons licence. The
official TEI, including its header, is the witness; plaintext derivatives are
only aids for search.

The first quarantine batch covers existing gaps for Jñānaśrīmitra,
Ratnakīrti, Prajñākaragupta, Manorathanandin, Śāntarakṣita, Hemacandra,
Pūjyapāda, Prabhācandra, Mallavādin, and Akalaṅka. See the candidate registry
and `data/sources/_intake/candidates/PROVENANCE.json`. Parsed XML and UTF-8
are recorded; no file is public or citation-safe until it has a source packet,
root/commentary segmentation where applicable, and sampled collation.

SARIT also contains five edited Jitāri treatises. This makes Jitāri a roster
**review prospect**, not an automatically added thinker.

## Discovery and comparison routes

| Route | What it supplies | Rule |
|---|---|---|
| [`tokushige-koyasan/muktabodha-corpus`](https://github.com/tokushige-koyasan/muktabodha-corpus) | 499 IAST Muktabodha derivatives with a useful catalogue. | Comparison mirror only; the official, newer user download remains the raw intake source. |
| [`project-vyasa/muktabodha.org`](https://github.com/project-vyasa/muktabodha.org) | An incomplete paired-script processing pipeline, currently publishing only *Yogavāsiṣṭha*. | Do not ingest. Its data are older Muktabodha archives and its transformations need independent review. |
| [`sanskrit/raw_etexts`](https://github.com/sanskrit/raw_etexts) | Broad school-specific discovery index, including Mādhva Sarvamūla, eBhāratī-derived Śrīvaiṣṇava, and Advaita files. | Never import directly: the repository is unlicensed and explicitly non-proofread. Follow embedded upstream edition/serial metadata to a rights-cleared source. |
| [`PramodJUS/Vedanta_Repo`](https://github.com/PramodJUS/Vedanta_Repo) and [`PramodJUS/Vadavali`](https://github.com/PramodJUS/Vadavali) | Useful catalogue of Dvaita commentarial works. | Do not import: their text is scraped from an upstream all-rights-reserved site. |
| [Old IITK Gita Supersite](https://old.gitasupersite.in/srimad?language=dv&field_chapter_value=2&field_nsutra_value=47&show_mool=1&scjaya=1&scmad=1&choose=1) | Direct reader presentation of Madhva and Jayatīrtha Gītā commentaries. | Reader/collation lead only until terms and permission for any acquisition are established. |

## Specific leads from the discovery layer

These are useful because they point to present thinker gaps, but must clear
the normal upstream-identity and rights gate before a candidate is registered
or a file is fetched:

- Madhva: *Karma-Nirṇaya*, *Tattva-Saṅkhyāna*, and alternate witnesses for
  *Tattvodyota* and *Viṣṇu-Tattva-Vinirṇaya*.
- Vedānta Deśika: *Nyāyapariśuddhi*; Raṅgarāmānuja: *Bhāvaprakāśikā*.
- Appayya Dīkṣita: *Ānandalaharī* with *Candrikā*; Śrī Harṣa:
  *Khaṇḍanakhaṇḍakhādya*.
- Modern Dvaita records named in scraped catalogues are title-discovery
  material, not grounds for new thinker entries.

## Direct eBhāratī check

The eBhāratī record behind the `raw_etexts` Appayya lead identifies a 1908
edition, editor, and serial number, so it is useful bibliographic evidence.
Its Download PDF/Word/Text controls, however, redirect to sign-in and the
site states that its material is all rights reserved. Do not use a GitHub copy
as a workaround or register it as a reusable text witness. Treat eBhāratī as
a metadata/permission lead until the rightsholder grants a suitable access or
reuse route.

No source route changes roster membership. A potential new thinker requires a
separate author/date/attribution review and a theory-bearing work, per the
roster policy.
