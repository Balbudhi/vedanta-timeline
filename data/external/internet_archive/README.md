# Internet Archive — Sanskrit holdings (registry only)

**Homepage:** https://archive.org/
**Sanskrit collection portal:** https://archive.org/details/sanskritlanguage
**License:** Per-item — public-domain / CC-* / unknown. The
`archive.org/metadata/<id>` API exposes `metadata.licenseurl` and
`metadata.rights` for each item; consumers MUST honour the per-item
value (none of the Anandāśrama / DLI scans below carry an explicit
`licenseurl`; they are scanned pre-1928 editions and treated as
public-domain under US copyright). Attribution to "Internet Archive"
plus the original print publisher (Ānandāśrama, Chowkhamba, KSTS, etc.)
is the conventional minimum.

This directory stages **no PDFs/djvu/text** in this run. Lane 2's job
here is registry-only: the 20 archive.org item slugs below are recorded
in `data/external_ingest_manifest.json` (`source_id: "internet_archive"`)
with their direct PDF + djvu-text URLs and `fetch_status: pending`.

## Owner split

- The **priority-12 acquisition basket** (`docs/ACQUISITION_PATHWAYS.md` §A)
  is owned by **Lane 3**. Lane 2 does NOT register any of those 12 here
  to avoid double-fetch. Specifically excluded: GovindaBhasya.KrsnadasBaba,
  BrahmaSutraBhashyaOfBhaskar*, SKEw_tattva-pradipika-chitsukhi*,
  tattva-prakasika, bhagavad-gita-gudhartha-dipika*, madhwapracharavedike,
  anandatirthabhagavatpadacharyavirachitahgita*, the Madhva Sarvamūla
  Nyāya-Vivaraṇa volume, BrihadaranyakaBhashyaVartikam (both), gOtp_…,
  fzFh_vivarana-prameya-sangraha…. (See manifest for the unambiguous
  cross-reference list.)
- Lane 2 here registers 20 other Sanskrit primaries (Anandāśrama,
  Chowkhamba, KSTS, DLI) that are *not* on the priority-12 list and that
  the prakriya OCR-correction pipeline + vedanta-timeline citation panel
  would want next.

## File-naming convention on archive.org

Every public-domain item exposes:

- `https://archive.org/download/<ID>/<ID>.pdf` — image-container PDF.
- `https://archive.org/download/<ID>/<ID>_djvu.txt` — OCR plain-text (Tesseract).
- `https://archive.org/download/<ID>/<ID>_djvu.xml` — OCR hOCR-style XML.
- `https://archive.org/download/<ID>/<ID>_text.pdf` — extra PDF with text layer (sometimes).

The `_djvu.txt` URL is the direct-ingest plain-text feed; the
`.pdf` URL is the OCR-correction lane feedstock.
