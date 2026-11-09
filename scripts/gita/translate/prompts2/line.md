You are writing the English line for one sentence of the Bhagavad-Gītā, word by word. Everything is
below; do not run commands or read files.

For each Sanskrit word you get its grammar in plain words (case, number, person; what it depends on),
the English already decided for it (default, and alternates you may use for cadence), the referents,
and any grammatical fork. Meaning is decided; your job is the English sentence.

Rules:
1. Use each word's default or one of its alternates. You may use another English form of the same
   word where English grammar needs it (a noun with "do/make" becomes the verb: never "do the
   abandonment", say "abandon"). A word with `light_verb` (√kṛ "do") and a noun object may be rendered
   together with that object as its English verb: give both words the same "english" text.
   Particles (na, eva, ca, hi, tu, api) are words too: render each.
1a. `english_case` says how English marks the word's case relation (decided by code from the case and
   its head): follow it — "freed from", not "freed by", when it says 'from'.
1b. A compound with `members` and no `english` is built from the members' decided English in the
   shape `compound_pattern` gives. Every member's English must appear in it; add nothing else but
   grammatical words.
2. Keep the grammar: case relations, agent nouns as agent nouns, voice, mood, tense; a universal
   under negation is "any".
3. ADD NOTHING. You may add only English grammatical words (the, a, is, are, who, which, of, to, in,
   by, with, from, for, he, it, that, those, there). No word may explain, intensify or interpret.
4. Keep the Sanskrit's order of ideas and its figures (repetition of a root, parallels, chiasmus)
   as far as English allows. Make it English that sounds: cadenced prose, each clause ending on a
   strong word, no chains of "of", no buried key word. It must parse on first hearing.
5. If the verses form one sentence, write one English sentence and give each verse's part.
6. A second line only if a grammatical fork is listed and one line cannot hold both readings.

Return only this JSON:
{"lines": {"12.13": "...", "12.14": "..."},
 "words": [{"locus": "12.13", "i": 0, "english": "<the exact text in the line for this word>", "rendering": "<the default or alternate used>"}],
 "alternative": null | {"fork": "...", "lines": {"12.13": "..."}}}

A word whose English is a kept Sanskrit term (e.g. "bhakta", "manas", "kūṭastha") appears in the line
as that term in italics-free plain form, inflected the English way where needed ("bhaktas"). A pronoun,
particle or other word whose English is null and has no members is rendered from its grammar as
exactly as you can, with "unresolved": true in its words entry.

Each word may carry `forbidden`: renderings the owner has ruled out for it. Never use them.
