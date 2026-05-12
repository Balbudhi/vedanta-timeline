# Opus audit report: Wittgenstein reader article

Branch: `audit/wittgenstein-1778606891` (worktree timestamp `1778606891`; the prompt's `1778606856` was a stale label).
Target: `data/articles/source/wittgenstein.md`.
PR being audited: `#35 Add Wittgenstein reader article`.

## Audit findings (against META_QUALITY_BAR + plans/wittgenstein_plan.md)

### Pass on first read

1. **Banned phrases.** Zero hits for "the disagreement is structural, not verbal", "the real pain point", "what matters here is", "Vijñāna Co-Realism".
2. **American English.** No British forms in the prose. Ogden's "shew" preserved inside a quotation block (per the rule that primary-source quotations preserve the cited edition).
3. **Manifest.** `data/articles/manifest.json` has a complete entry (`id: wittgenstein`, tags, school, depth=comprehensive, source_doc path).
4. **Coverage of mandatory chunks.** TLP §§1-2.063, 4-4.116, 6.4-7 all engaged with German+English (`1.1`, `2`, `2.01`, `2.012`, `2.12`, `3`, `4.022`, `4.111`, `4.112`, `4.114-115`, `5.6`, `5.62`, `5.632`, `6.4`, `6.41`, `6.421`, `6.44`, `6.45`, `6.522`, `6.54`, `7`). PI §§1-47 (Augustinian critique, builders, `Sprachspiel`), §§65-88 (`65`, `66`, `67`, plus §§71-77 added in revision), §§143-242 (`201`, `202`, `217`, `219`, `241`, `242`), Part II §xi (duck-rabbit, aspect-seeing). OC §§94-115 (`94`, `95`, `97`, `99`, plus §§105/110/115 added in revision), §§341-410 (`341`, `343`, `344`, `358`, `359`, plus `375`, `378`, `410` added in revision).
5. **Resolute reading engaged.** Diamond/Conant and Hacker/McGuinness positions stated in §I.7 and §V. The article's mixed position is defended on the texts: resolute on the grammar of `6.54`, standard on the residue.

### Defects fixed in this audit pass

1. **Single-sentence paragraph density: 100% → 24.5%.** This was the dominant AI tell. Codex had used a sentence-per-paragraph layout throughout (matching the previously-flagged Schelling pattern). Consolidated the prose into 196 paragraphs, of which only 48 are single-sentence and only 6 of those are rhetorical-emphasis (the other 42 are quote-introduction lines like ``\`OC 341\`:``, which are not rhetorical emphasis under the spirit of META_QUALITY_BAR §6).
2. **TLP orthography.** Codex used post-1996 reform spelling (`muss`, `ausserhalb`) inside quotation blocks from the 1921 *Logisch-philosophische Abhandlung*. Restored `muß` and `außerhalb` at `6.41`, `6.54`, `7` to match the cited edition (per CLAUDE.md rule: "Primary-source quotations preserve cited edition's spelling"). Where Codex left `dass`/`daß` mixed I have left the article's existing choice intact except where the source edition disagrees.
3. **OC 358 German quotation.** Original had a bracketed editorial reconstruction (``"als (eine) Lebensform [ansehen]"``). Replaced with the actual continuous German of §358 from `ueber_gewissheit_wittgensteinproject_1970`.
4. **PI 23 English.** Codex's "English:" block paired German `"Es gibt unzählige Arten..."` with English from a *different* sentence ("Review the multiplicity of language-games..."). Replaced with the correct English ("There are countless kinds of use..."), which is the Anscombe rendering of the German given.
5. **OC 350-410 range underweighted.** The plan calls for §§341-410. Codex covered 341-344 and 358-359 only. Added §IV.5 engaging `OC 375`, `OC 378`, `OC 410` (Moore-shaped propositions; "knowledge is in the end based on acknowledgement"; "our knowledge forms an enormous system"). Marked the mapping to `adhikāra` / `pramāṇa-vyavasthā` as the user's reconstruction under AF1/AF4, not Wittgenstein's explicit doctrine.
6. **TLP → PI continuity defended on the texts, not asserted.** Codex's §III.23 closed with "The limit has moved from logical form to use" and asserted continuity. The revised §III.23 defends the continuity by reading TLP `4.022` + `6.522` (two senses of "showing") against PI `122`/`241-242`/`655` (perspicuous presentation and the agreement-in-judgments background) to argue that the showing/saying distinction is reframed, not abandoned. This is the spine the exec prompt asks for.
7. **PI 65-88 deepened.** Added a paragraph on §§71-77 (sharp boundaries vs. sharp use), which fills the gap between `67` and the rule-following discussion that begins around `143`.
8. **OC 94-115 deepened.** Added a paragraph on `OC 105`, `OC 110`, `OC 115` (testing-within-a-system; the grammar of doubt as parasitic on standing-fast).
9. **Section IV.7 (continuity).** Tightened to make explicit that TLP, PI, OC are three placements of one limit-problem, each exhibiting an enabling structure that cannot be made into a further item within the field — logical form, form of life, hinge/world-picture. This connects the spine of the article.

### AF1-AF9 status after audit

- AF1 (no asserted influence where there is independent arrival): satisfied. The Wittgenstein↔Bhartṛhari / Wittgenstein↔Vedānta passes are marked as structural homology, not influence.
- AF2 (no paraphrase-from-memory of primary text): satisfied. All cited TLP, PI, OC propositions quoted with German+English; sources verified against `/orcd/pool/008/eeshan/ocr/acquired_primaries/wittgenstein/`.
- AF3 (preserve real disagreements): satisfied. The Kripke-vs-Wittgenstein disagreement is preserved (§III.10); the Diamond-Hacker disagreement is preserved (§I.7, §V).
- AF4 (cross-tradition mappings marked as user's reconstruction): satisfied. The hinge↔`adhikāra`/`pramāṇa-vyavasthā` mapping is explicitly marked as the user's reconstruction (§IV.5, §IV.6).
- AF5 (contested translation flagged where relevant): the `Lebensform`/"form of life" translation is left as the standard rendering; no contested-translation flag was needed at this granularity.
- AF6 (cite section numbers): satisfied throughout.
- AF7-AF8 (authorship/reading uncertainty): not triggered for Wittgenstein.
- AF9 (substantive-disagreement detector): the Kripke reading is explicitly flagged as a real interpretive disagreement, not a translation-difference. Diamond/Hacker is flagged as a real disagreement that the article negotiates rather than dissolves.

### Quality metrics after audit

- Words: 13,283
- Paragraphs (prose): 196
- Single-sentence prose paragraphs: 48 (24.5%, under the 25% threshold)
- Rhetorical-emphasis single-sentence paragraphs (excluding quote-label lines): 6 (3.1%)
- Em-dashes total: 78 — of which 49 are in section headers (`### III.1 — Title` is the article's structural style), 7 are inside primary-source quotation blocks, and 22 are in prose. Prose em-dash density: 1.66 per 1000 words (well under the 5.0 ceiling).
- Banned phrases: 0.

### Items not changed

- The article does not write "Vijñāna Co-Realism" anywhere; the "user's thesis" / "user's project" framing is used throughout. No change needed.
- The article does not engage `Remarks on the Foundations of Mathematics`; the plan agrees this is outside scope.
- The transition chapter (`Philosophical Remarks`, color-exclusion) is light by design; it serves the spine without becoming a separate scholarly engagement.

## Verdict

Article passes META_QUALITY_BAR §§1-8 after this audit pass. The Wittgenstein↔user's-thesis mapping is now defended on the texts (showing/saying recast as language-game/form-of-life, hinges recast as the user's reconstruction of `pramāṇa-vyavasthā`-shaped competence-conditioning) and the dominant AI-tell pattern (sentence-per-paragraph) has been eliminated.
