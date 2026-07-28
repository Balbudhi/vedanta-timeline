# Unverified OCR — not citable

Everything in this directory is **raw, uncorrected OCR**. It is here as a
starting point for proofreading, not as a witness.

**Nothing in this directory may be cited by a reading, an article, or a thinker
entry until it has been proofread against the printed scan it came from.**
`scripts/check_gita_witness.py` deliberately does not treat these files as
witnesses; an entry whose `source` points here will be reported as unresolved
rather than silently validated against corrupt text.

The reason for the rule is that OCR failure is not random noise — it produces
real Sanskrit words that are the wrong ones, and those survive every check
short of reading the page. In `abhinavagupta_gitartha_sangraha.txt`, for
instance, the OCR turns *praśnaḥ* ("question") into *praṇavaḥ* ("the syllable
Oṃ"), which is a grammatical, plausible-looking, completely wrong reading.
Running heads and footnote apparatus are also interleaved into the body text.

## Contents

### `abhinavagupta_gitartha_sangraha.txt`

Abhinavagupta's *Gītārtha-saṅgraha* (Kashmir Śaiva / Trika, c. 10th c.),
Devanāgarī. From archive.org item
`ShrimadBhagavtaGitaWithTheGitarthaSangrahaOfAbhinavaguptaDr.S.Satyanarayan`
(ed. S. Śaṅkaranārāyaṇan, Tirupati, 1985), licence **CC0 1.0**. Fetched
2026-07-28.

Two things to know before working with it:

1. The OCR is heavily degraded — see above.
2. Abhinavagupta transmits the **Kashmirian recension**, whose verse
   numbering does not track the vulgate. Its "3.38" is not the vulgate's
   3.38. Loci cannot be mapped across mechanically; each one has to be
   aligned by reading.

This is the only commentary named in `gita/sthitaprajna/_build/DESIGN.md`
that the project still has no usable text for, and it is the one most worth
having — it is the only genuinely cross-darśana voice on the list.

## Not committed

Two further acquisitions are held out of the repo entirely, in
`_acquisition_holding/` (gitignored), because their archive.org items state no
licence at all and this repository is public:

- Keśava Kāśmīrī, *Tattva-prakāśikā* (Nimbārka) — `archive.org/details/tattva-prakasika-kesava-kasmiri`
- Nīlakaṇṭha, *Bhāva-dīpa* — `archive.org/details/gita-nilakantha`

Both are also raw OCR. The underlying compositions are long out of copyright;
what is unestablished is the status of these particular scans.
