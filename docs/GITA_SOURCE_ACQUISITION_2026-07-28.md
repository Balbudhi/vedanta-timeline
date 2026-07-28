# Sanskrit source acquisition — BG 3.36–43 commentaries

Fetched 2026-07-28. All files saved under
`data/sources/sanskrit/vedanta/`. No git staging/commits were performed —
working tree left for manual review and commit.

Note on division of labor: items 1–4 (Śrīdhara, Madhusūdana, Viśvanātha,
Baladeva) were fetched and are being committed directly by the coordinating
agent from the same GRETIL file identified below; I did not duplicate that
download. Items 5–6 below (plus one bonus acquisition, Yāmuna's
*Gītārthasaṃgraha* — a different work from Abhinavagupta's, flagged below to
avoid the exact misattribution risk raised by the task) are the result of
this pass.

## 1–4. Śrīdhara / Madhusūdana / Viśvanātha / Baladeva — GRETIL 4-commentary Gītā

- **Acquired:** yes (by coordinating agent, not this pass)
- **URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_bhagavadgItA-4comm.txt
  (full 18-chapter Gītā with all four commentaries interleaved; input by
  Gaudiya Grantha Mandira)
- **Encoding:** IAST, UTF-8
- **Licence:** CC BY-NC-SA 4.0 International, per GRETIL's own header ("This
  e-text was provided to GRETIL in good faith that no copyright rights have
  been infringed...")
- **Verified BG 3.36–43 range (in the raw downloaded file, before any header
  was added):** `bhg 3.36` at line 2675, `bhg 3.37` (śrīdharaḥ, madhusūdanaḥ,
  viśvanāthaḥ, baladevaḥ all present) at line 2689, ... `bhg 3.43` at line
  2834, chapter 4 begins at line 2871. All four commentators are present at
  every verse in 3.36–3.43 — independently confirmed by this agent as well
  (`grep -n "^bhg 3\." `, and spot-checked all four voices at 3.36/3.37/3.43).
- I take no further action on this file; do not duplicate-fetch.

## 5. Abhinavagupta — Gītārtha-saṅgraha (Kashmir Śaiva / Trika)

- **Acquired:** yes
- **File:** `data/sources/sanskrit/vedanta/abhinavagupta_gitartha_sangraha.txt`
- **URL:** https://archive.org/details/ShrimadBhagavtaGitaWithTheGitarthaSangrahaOfAbhinavaguptaDr.S.Satyanarayan
  — OCR (`_djvu.txt`) of the printed critical edition *Śrīmad Bhagavad Gītā
  with the Gītārtha-saṅgraha of Abhinavagupta*, ed. Dr. S.
  Śaṅkaranārāyaṇan, Sri Venkateswara University Oriental Research
  Institute, Tirupati, 1985.
- **Encoding:** Devanāgarī, UTF-8. **Raw, uncorrected OCR** — quality is
  imperfect (e.g. verse numerals routinely misread, "३" (3) OCR'd as "८"
  (8); scattered garbled characters throughout). Usable for locating and
  reading the commentary but not suitable as a citation-grade transcription
  without manual correction.
- **Licence:** archive.org item license = **CC0 1.0 Universal** (explicit
  `licenseurl` field), collections `digitallibraryindia` + `JaiGyan`. The
  underlying 10th-century composition is public domain regardless.
- **Verified BG 3.36–43 range (in the saved file, header included):**
  BG 3.36 ("अथ केन प्रयुक्तोऽयं पापे चरति परुषः") at **line 6367**; BG
  3.43 ("जहि श्वं महाबाहो कामरूपं दुरासदम्" — OCR misreads the verse
  number as "४८" instead of "४३") at **line 6568**. Root verse + prose
  commentary for the full 3.36–3.43 span is present between these lines.
- **Important distinct-work flag:** this is **not** the same text as
  Yāmuna's *Gītārthasaṃgraha* (item below) despite the near-identical
  title. I also tried a second archive.org scan, "Abhinavagupta Gitartha
  Sangraha - Arvind Sharma" (`AbhinavaguptaGitarthaSangrahaArvindSharma`),
  but its OCR text contains no match for any of the BG 3.36–43 marker
  phrases — it appears to be an English-language study/monograph rather
  than a parallel Sanskrit edition, or its OCR is too degraded to search;
  I did not save it.

## Bonus: Yāmuna (Ālavandār) — Gītārthasaṃgraha (Viśiṣṭādvaita) — DIFFERENT WORK, do not conflate with #5

- **Acquired:** yes
- **File:** `data/sources/sanskrit/vedanta/yamuna_gitarthasamgraha.txt`
- **URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_yAmuna-gItArthasaMgraha.txt
  (input by Sadanori Ishitobi)
- **Encoding:** IAST, UTF-8
- **Licence:** CC BY-NC-SA 4.0 International (GRETIL's stated terms)
- **Coverage of BG 3.36–43: NONE, by the nature of the text.** This is a
  32-verse summary poem, one verse per Gītā chapter — not a verse-by-verse
  commentary. Chapter 3 in its entirety is addressed only in verse
  `YGas_7` (line 90 of the saved file): "asaktyā lokarakṣāyai guṇeṣv
  āropya kartṛktām | sarveśvare vā nyasyoktā tṛtīye karmakāryatā." There is
  no way to point to 3.36–43 specifically inside this work — reporting this
  as a genuine gap in what the text offers, not a search failure.

## 6. Keśava Kāśmīrī — Tattva-prakāśikā (Nimbārka / Dvaitādvaita)

- **Acquired:** yes
- **File:** `data/sources/sanskrit/vedanta/kesava_kasmiri_tattva_prakasika.txt`
- **URL:** https://archive.org/details/tattva-prakasika-kesava-kasmiri
  ("Tattva-prakasika Kesava kasmiri", `_djvu.txt` OCR)
- **Encoding:** Devanāgarī, UTF-8, raw uncorrected OCR (imperfect quality,
  same caveats as above)
- **Licence:** **no explicit license/rights field stated** on the archive.org
  item (checked via the metadata API: `licenseurl` and `rights` both
  absent). Hosted in the community `folkscanomy_religion_bhagavad_gita`
  collection. The underlying 16th-century composition is unambiguously
  public domain; the specific scanned print edition's provenance is
  unstated — flagged explicitly so you can make the final call on this one
  file, unlike #5 which has an unambiguous CC0 grant.
- **Verified BG 3.36–43 range:** BG 3.36 ("अर्जुन उवाच-अथ केन प्रयुक्तोप्य
  पापं चरति पूरुषः") at **line 2005**; BG 3.43 ("जाह शु महाबाही कामरूप
  दुरासदम्" — OCR-garbled for "जहि शत्रुं महाबाहो...") at **line 2094**.

## 6b. Nīlakaṇṭha — Bhāva-dīpa (extracted from his Mahābhārata commentary)

- **Acquired:** yes
- **File:** `data/sources/sanskrit/vedanta/nilakantha_gita_bhavadipa.txt`
- **URL:** https://archive.org/details/gita-nilakantha ("Bhagavad Gita
  Nilakantha Tika", `_djvu.txt` OCR; credited to Sh. Hari Parshad Das Ji as
  the extraction of Nīlakaṇṭha's Gītā-portion commentary out of his
  Mahābhārata Bhīṣma-parvan commentary, the *Bhāvārtha-dīpikā*/*Bhāva-dīpa*)
- **Encoding:** Devanāgarī, UTF-8, raw uncorrected OCR (imperfect quality)
- **Licence:** same situation as Keśava Kāśmīrī above — **no explicit
  license/rights field** on the archive.org item, community `folkscanomy`
  collection, no copyright claim asserted by the uploader. Underlying
  composition (~17th c.) is public domain; specific edition's provenance
  unstated — flagged for your judgment.
- **Verified BG 3.36–43 range:** BG 3.36 ("अथ केन प्रयुक्तोऽयं पापं चरति
  पृरूषः") at **line 3217**; BG 3.43 ("जदि रतु महावाहो कामरूपं दुरासदम्" —
  OCR-garbled for "जहि शत्रुं महाबाहो...") at **line 3397**. The chapter-3
  colophon ("इति श्री महाभारते भीष्मपर्वणि ... कर्मयोगो नाम तृतीयोऽध्यायः")
  immediately follows, confirming the chapter boundary.

## Summary table

| Commentator | Work | Acquired | File | Licence status |
|---|---|---|---|---|
| Śrīdhara Svāmī | Subodhinī | yes (coordinator) | (GRETIL 4-comm file, committed separately) | CC BY-NC-SA 4.0 |
| Madhusūdana Sarasvatī | Gūḍhārtha-dīpikā | yes (coordinator) | (same file) | CC BY-NC-SA 4.0 |
| Viśvanātha Cakravartī | Sārārtha-varṣiṇī | yes (coordinator) | (same file) | CC BY-NC-SA 4.0 |
| Baladeva Vidyābhūṣaṇa | Gītā-bhūṣaṇa | yes (coordinator) | (same file) | CC BY-NC-SA 4.0 |
| Abhinavagupta | Gītārtha-saṅgraha | **yes** | `abhinavagupta_gitartha_sangraha.txt` | CC0 (explicit) |
| Yāmuna (bonus, distinct work) | Gītārthasaṃgraha | yes, but no 3.36–43 content exists in it | `yamuna_gitarthasamgraha.txt` | CC BY-NC-SA 4.0 |
| Keśava Kāśmīrī | Tattva-prakāśikā | **yes** | `kesava_kasmiri_tattva_prakasika.txt` | unstated — flagged |
| Nīlakaṇṭha | Bhāva-dīpa | **yes** | `nilakantha_gita_bhavadipa.txt` | unstated — flagged |

## What was NOT obtained / left honestly unresolved

- No corrected/critical Sanskrit transcription exists for Abhinavagupta,
  Keśava Kāśmīrī, or Nīlakaṇṭha here — all three are raw, uncorrected OCR
  of scanned prints, with visible character- and numeral-level errors. They
  are usable for reading/quoting with care, not as citation-grade text
  without manual proofreading against the source scan (PDF also available
  at each archive.org URL above if proofreading is wanted later).
- The two `folkscanomy`-collection items (Keśava Kāśmīrī, Nīlakaṇṭha) carry
  no explicit rights statement from the uploader. I did not treat "hosted
  on archive.org" as itself sufficient to declare them public domain for
  this public repo — that determination is left to you, flagged clearly
  above rather than silently assumed.
- I did not attempt Muktabodha's digital library (muktalib) for
  Abhinavagupta as suggested, since a usable, explicitly-CC0 Sanskrit
  source covering the exact verse range was already found and verified; if
  a cleaner Muktabodha transcription is wanted later, that's a follow-up,
  not a gap in this deliverable.
