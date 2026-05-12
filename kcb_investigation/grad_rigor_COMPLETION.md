# Grad Rigor Completion Report

## Acquired Texts

Primary acquisitions and canonical working witnesses were consolidated under `/orcd/pool/008/eeshan/ocr/acquired_primaries/`.

Core Kant corpus acquired or copied into the acquisition tree:

- *Critique of Pure Reason*:
  - Norman Kemp Smith English OCR witness from archive.org
  - German local witness copied into acquisition tree
- *Critique of Practical Reason*:
  - Abbott public-domain Gutenberg text
- *Critique of Judgment*:
  - Bernard public-domain Gutenberg text
- *Prolegomena*:
  - Carus public-domain Gutenberg text
  - important correction: Gutenberg `#4363` was wrong; the correct text used is `#52821`

Core K. C. Bhattacharyya corpus acquired:

- *Studies in Philosophy* I (archive.org OCR + PDF)
- *Studies in Philosophy* II (archive.org OCR + PDF)
- *Studies in Vedantism* (archive.org OCR + PDF)
- *Swaraj in Ideas* (BJP digital library PDF)
- *The Subject as Freedom*:
  - no standalone archive.org scan surfaced from the documented search attempts
  - the 1958 reprint in *Studies in Philosophy* II is the canonical working witness

Core Sri Aurobindo corpus copied into the acquisition tree from existing CWSA text witnesses:

- *The Life Divine* I-II
- *The Synthesis of Yoga* I-II
- *Letters on Yoga* I-IV
- *Essays on the Gita*

Core Hegel corpus acquired:

- *Phänomenologie des Geistes*:
  - German text witness
  - Baillie English OCR witness from archive.org
- *Wissenschaft der Logik*:
  - German text witness
- *Enzyklopädie*:
  - German HTML witness from hegel.de
  - Wallace public-domain English translations of *Logic* and *Philosophy of Mind*

Core Jaina and Vedānta comparator corpus acquired:

- Umāsvāti, *Tattvārtha-sūtra*:
  - Sanskrit witness copied from local corpus
  - Tatia English witness from archive.org
- Malliṣeṇa, *Syādvāda-mañjarī*:
  - archive OCR witness from Sanskrit-Hindi edition
- Hemacandra, *Pramāṇa-mīmāṃsā*:
  - archive OCR witness
  - important failed route documented: Deccan handle/bitstream redirected to `/jspui/error.html`
- Vidyānanda, *Aṣṭasahasrī*:
  - archive OCR witness
- Śaṅkara, *Brahma-sūtra-bhāṣya*:
  - Sanskrit witness copied from local corpus
  - Thibaut English witness from Gutenberg
- Rāmānuja, *Śrī-bhāṣya*:
  - Thibaut English witness from Gutenberg

The detailed per-file provenance, sha256 values, line counts, and URL attempts are recorded in:

- `/orcd/pool/008/eeshan/ocr/acquired_primaries/MANIFEST.md`

## Reading Notes Summary

Quotation-grade notes were compiled in:

- `/orcd/pool/008/eeshan/ocr/acquired_primaries/READING_NOTES.md`

The notes now contain working chunks for:

- KCB on Jaina anekānta, alternative truths, and anti-Hegelian non-totalization
- KCB on subjectivity, psychic fact, introspection, and freedom
- Umāsvāti on `pramāṇa`, `naya`, `dravya`, `paryāya`, and `utpādavyayadhrauvyuktam sat`
- Malliṣeṇa on the sevenfold predication
- Śaṅkara's anti-Jaina polemic at *Brahma-sūtra-bhāṣya* 2.2.33-35
- Rāmānuja's parallel anti-Jaina polemic
- Kant on the Transcendental Aesthetic, Antinomy, and `Sein ist offenbar kein reales Prädikat`
- Kant on the moral law as the `ratio cognoscendi` of freedom and the "fact of reason"
- Aurobindo on knowledge by identity, Supermind, and the Infinite's free self-determination
- Hegel on substance-as-subject, the whole, and the opening move from being to becoming

The most important negative documentary result is also recorded there:

- a direct sweep of the acquired Aurobindo corpus did **not** find a substantive explicit engagement with Kant by name
- apparent `kant` hits were proper names, not philosophical discussion
- the Aurobindo-Kant section of the article is therefore marked as structural reconstruction, not direct historical debate

## Article Rewrite Delta

Target file:

- `/orcd/home/002/eeshan/philosophy/site/data/articles/source/kcb-kantian-perspectivism.md`

Main changes relative to the prior thinner draft:

- removed the old underdocumented posture that relied on missing-text caveats where primaries are now in hand
- hardened the Aurobindo section with direct *Life Divine* evidence on knowledge by identity and an explicit negative search result on Kant-by-name
- rebuilt the Jaina section around acquired primary witnesses:
  - Umāsvāti
  - Malliṣeṇa
  - KCB's pp. 331ff. reconstruction
  - Śaṅkara
  - Rāmānuja
- strengthened the being/becoming section with direct Kant and Hegel citations in German and English
- expanded section 9 into documentary reading-note cards keyed to actual loci, so the article now contains an internal re-entry map tied to the acquired corpus
- corrected stale claims in the article that Malliṣeṇa or the Vedānta anti-Jaina loci were unavailable

The revised article is still argumentative rather than archival.
But it is now answerable, at its load-bearing points, to acquired primary witnesses rather than to memory or placeholder summaries.

## Line Count Comparison

- Previous article line count before rewrite pass: `1843`
- Current article line count after rewrite pass: `2502`
- Net increase: `+659`

The new count clears the user's minimum target of 2500 lines.

## Remaining Caveats

- The standalone 1930 scan of *The Subject as Freedom* was searched for and not found in a clean downloadable form; the article therefore works from the secure reprint in *Studies in Philosophy* II.
- The acquired *Syādvāda-mañjarī* witness is usable but noisy; it is a Sanskrit-Hindi OCR witness, not a fresh critical edition.
- The acquired *Pramāṇa-mīmāṃsā* witness likewise comes from archive OCR after the Deccan repository route failed.
- The article is now significantly more documentary than before, but it still stages some structural comparisons:
  - especially KCB-to-Aurobindo
  - and Aurobindo-to-Kant
- Those structural comparisons are now explicitly labeled as such inside the article, rather than being allowed to masquerade as direct historical engagements.
