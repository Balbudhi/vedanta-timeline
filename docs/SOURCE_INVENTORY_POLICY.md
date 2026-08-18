# Source inventory policy

`data/primary_text_manifest.json` is the public repository's inventory of the
source witnesses it actually ships beneath `data/sources/`. It is not a count
of all works discussed by the project, a bibliography of works held privately,
or evidence that a particular passage has been proofread.

Run the read-only report with:

```sh
node scripts/check_source_inventory.js
```

The report reads only the manifest and tests its listed paths against the
working tree. It does not regenerate the manifest, contact a source URL, edit
metadata, consult older inventories, or promote a witness based on a matching
filename.

## What the totals mean

- **Manifest records** are entries in `files`, regardless of format or
  completeness.
- **In-repo witness files** are manifest entries whose relative `path` resolves
  to a regular file below the manifest's `root` directory. A missing path, a
  directory, an escaping `../` path, or an absolute path does not count.
- **Text-formatted witnesses** are the above files whose actual `format` is
  `plain-text`, `html-visible-text-capture`, `wikitext`,
  `text-with-locus-marker`, or `web-transcription`. This is a format count, not
  a claim that every line has been checked.
- **Image-PDF scan witnesses** are in-repo files with the actual format
  `image-pdf-scan`. They remain useful page witnesses but are not silently
  counted as clean searchable text.
- **Verification metadata** means only that a non-empty
  `verification_status` field exists. It is not a verified/citable count.
- **Citation-safe declared** means that `verification_status` literally uses
  the phrase “citation-safe.” A conditional statement such as “citation-safe
  after passage-level comparison” is reported separately and is **not**
  current citation-grade status.
- **Citation-grade** is counted only when the manifest itself declares a
  present, unconditional citation-safe status. The validator does not infer it
  from `format`, `source_url`, `edition`, a phrase such as “clean,” or records
  elsewhere in the repository.
- **Verified** is counted only from a `verified: true` manifest field. The
  current manifest does not define that field, so the report says “not
  available” rather than inventing a total from prose.

This deliberately conservative distinction prevents the public inventory from
turning a working transcription, a scan, or a status that names future
collation into a citation claim.

## Path integrity

Every `files[].path` must be a relative path below the manifest's `root`
(currently `data/sources/`). An absolute path is always stale and nonportable,
even if it happened to resolve on the machine that produced it. The validator
lists the record number, title, and path and exits non-zero for absolute,
escaping, missing, or non-file paths. It also exits non-zero when the manifest
shape or declared `file_count` disagrees with the actual `files` array.

Use paths relative to `root`, for example:

```json
{ "path": "sanskrit/vedanta/example.txt" }
```

Never record a developer-machine location such as
`/Users/name/project/data/sources/...`, a `file:` URL, or a Windows drive path.

## Public, private, and quarantine boundaries

The public manifest may list only witnesses that are actually committed under
`data/sources/` and may lawfully be published by this repository. Keep
rights-unresolved or privately acquired files outside this tree and record only
non-infringing provenance notes in the appropriate private records. Do not add
private absolute paths to this manifest.

`data/sources/_unverified_ocr/` is a public quarantine for search aids, not a
citation corpus. A quarantined OCR may help locate a passage, but it cannot
support a quotation until its reading has been checked against the named scan
or edition and a clean, provenance-bearing witness has been created or updated.
The source state and citation requirements in
`docs/CONTENT_AND_SOURCE_STANDARD.md` remain binding; this report measures
inventory integrity, not textual correctness.
