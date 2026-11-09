# Spoon-fed workflow (lead spec, 2026-11-09) — RETIRED rev. 2 (lexicon-first); see ../WORKFLOW.md

Principle: code finds, filters and formats everything; the model makes a few small, explicit
choices from what it is handed, in one call, with no tools and no files. Each model call gets a
card of a few KB and returns a small JSON object. Code checks every answer; a reviewer sees the
same card and the answer and may only choose from the same options.

Audit that forced this (ch12 qualification, 2026-11-09): agentic jobs with tools made 40–90 tool
calls and took 10–13 min per lexicon job on 100–300 KB inputs; they used `define` to verify
guesses (incl. "near", "sit", whole phrases) instead of finding words; every commentator gloss
became a "sense"; the self-defined loss gate was satisfied by definitions-as-renderings ("sit near
in exclusive contemplative attendance on"); manas and cetas both became "mind".

## Stage 1 — Construe (kept as built; agentic, reads all commentaries; reviewed). Output per verse:
words[{i, form, stem, root, upasargas, word_class, analysis_id|manual, compound, members, relation}],
referents, supplied, forks (grammatical kinds), continues_into_next.

## Stage 2 — Lexicon, per lemma, two model calls
2a. Code builds the SANSKRIT CARD (evidence.py sanskrit_card, ≤ ~6 KB): lemma, root, upasargas,
  affix/kind; dhatu (aupadeśika, gaṇa, artha; ≤3 Dhātuvṛtti sentences); amara group(s); kosha
  (Śabdakalpadruma / Vācaspatya, ≤600 chars); nirukta (≤3); occurrences in scope with each
  commentator's gloss clause; elsewhere (other Gītā lines). Items carry ids (D1, A1, K1, N1, O1.g2, E1).
2b. MODEL CALL "senses": per lemma 1–2 senses, core ≤6 words, range, root IMAGE cited, image_dead.
2c. Code builds the ENGLISH TABLE per sense (english.py english_table): reverse dictionary by sense
  and image, thesaurus expansion, attested derived forms; ≤32 rows.
2d. MODEL CALL "annotate", once per root family: marks each candidate (sense 0/1/2, image 0/1,
  misleads, register, pos_fits, idiomatic, rank) and names the standing sense.
2e. CODE PICKS by the owner's order (standing decision; existing word with sense+image; new word
  with both; word with sense, image lost; unresolved); REVIEW CALL "review_marks"; collisions.

## Stage 3 — Verse, per sentence unit, one model call: unit card (grammar, lexicon default +
alternates, referents, forks); line; code checks; review; one revision.

## Measured, chapter 12 (2026-11-09)
Construe ≈9 min (20 verses); lexicon 22.6 min / 469 calls (143 lemmas); verse 2.5 min / 41 calls.
Later runs: majority-of-3 marking, 580 calls, 20.8 min; verse 72 calls, 3.8 min.
Why retired (see ../WORKFLOW.md audit): words decided out of context by a code score produced odd
choices ("opposer", "bristling of hair") and translationese lines ("practice yoga", "lacked by
clinging"); ≈650 calls per chapter; worse English than one in-context call per verse.
