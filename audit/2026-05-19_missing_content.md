# Missing content audit — 2026-05-19

## Stub-emitting code paths in `assets/app.js`

1. **`md(t.core_thesis || "Core thesis: not yet written.")`** (line 1824) — fires when
   a thinker JSON has no `core_thesis` field. Audit result: **0 thinkers hit this**.
   All 200+ thinkers have substantial core_thesis text. (False-positive matches on
   the substring "not yet" within real prose were ruled out.)

2. **`tx-coverage-placeholder` banner** (line 2306) — fires when a full-translation
   markdown file has YAML frontmatter `coverage: placeholder`. Audit result:
   **12 placeholder files**, all are intentional summary-of-status pages that
   describe the work without translating it. Banner message is correct.

3. **Synthesized translation stub** (line 2115-2140) — fires when
   `data/full_translations/<thinkerId>__<workId>.md` does **not** exist. Renders:
   `work.summary` (always present) followed by a "Status of translation:
   not yet produced" notice. Audit result: **463 (thinker, work) pairs hit this** —
   457 with no key_passages and 6 with key_passages but no extended translation.
   This is by-design for most engaged works.

4. **`cp-pending` citation card** (line 2827-2829) — fires when a citation entry
   has `pending_target_work` set. Audit result: **4 entries, all for
   Sudarśana Sūri's *Śruta-Prakāśikā***. Genuinely pending acquisition.

5. **Passage-not-extracted card** (line 2858, 3025) — fires per the citation
   pending flag. Same 4 entries as above.

## Genuinely missing content

### Works with key_passages but no extended translation file

These 6 (thinker, work_id) pairs would benefit from a `data/full_translations/`
file — the citations already exist but the extended translation page falls back
to a synthesis.

- **sankara** / `mandukya-bhasya` — *Mandukya-Upanisad-Bhashya with Gaudapada-Karika-Bhashya* — 2 key passage(s)
- **sarvajnatman** / `samksepa-sariraka` — *Samkshepa-Shariraka* — 4 key passage(s)
- **vallabha** / `anu-bhasya` — *Anu-Bhashya* — 4 key passage(s)
- **vijnanabhiksu** / `yoga-varttika` — *Yoga-Varttika* — 2 key passage(s)
- **vimuktatman** / `ista-siddhi` — *Ishta-Siddhi* — 5 key passage(s)
- **yamuna** / `siddhi-trayam` — *Siddhi-Trayam* — 3 key passage(s)

### Placeholder summary files (12 — intentional, no action needed)

Each has 1700-2300 chars of summary text explaining what the work does and why
the Sanskrit isn't on disk. Banner correctly labels them "Acquisition queued".

- `data/full_translations/baladeva__govinda-bhasya.md`
- `data/full_translations/bhaskara__brahma-sutra-bhasya.md`
- `data/full_translations/citsukha__tattva-pradipika.md`
- `data/full_translations/jayatirtha__tattva-prakashika.md`
- `data/full_translations/madhusudana__gudhartha-dipika.md`
- `data/full_translations/madhva__gita-bhasya.md`
- `data/full_translations/madhva__gita-tatparya.md`
- `data/full_translations/madhva__nyaya-vivarana.md`
- `data/full_translations/sureshvara__brhadaranyaka-varttika.md`
- `data/full_translations/sureshvara__taittiriya-varttika.md`
- `data/full_translations/vedanta-desika__shata-dushani.md`
- `data/full_translations/vidyaranya__vivarana-prameya-samgraha.md`

### Pending citation acquisitions (4 — intentional)

- `sudarsana/shruta-prakashika/1.1.1`
- `sudarsana/shruta-prakashika/2.1.9-2.3.43`
- `sudarsana/shruta-prakashika/2.2.1-32`
- `sudarsana/shruta-prakashika/3.2.24-4.1.1-2`

All four are loci of Śruta-Prakāśikā by Sudarśana Sūri, queued at
`parishishta/notes/USER_NEEDED.md`.

## Findings — wiring vs missing-content

- **Wiring bugs found: 0.** Every stub-emitter resolves to a data source that is
  either correctly populated or correctly flagged as pending.
- **Genuinely missing content: 6 extended translation files** (listed above) plus
  the 4 Śruta-Prakāśikā loci. No silent stubs hiding extant English content.
- **Caveat:** the synthesized-translation path (#3 above) shows the work summary
  followed by a "Status of translation: not yet produced" notice. When a user
  clicks a work that has only a summary, the page reads as a stub even though
  the summary is real English content. This is a messaging-clarity issue in
  `assets/app.js` (lines 2125-2140), not a data issue — leaving to UI agent.