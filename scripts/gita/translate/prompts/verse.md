# Translate one sentence of the Bhagavad-Gītā

Read `input.json`: the sentence (one or more verses), the previous and next verse, each
verse's construal (grammar already decided), every Sanskrit commentary in full, and the
lexicon rows that decide the English of its words. Run more lookups with
`python3 -I TOOL CMD ARGS` (`gloss`, `meaning`, `english "MEANING"`, `define WORD`, `sutra`).
Read no other file and no English translation of the Gītā.

The owner's standard: lossless in the line itself. The English line carries what each word means
and signifies. Nothing is moved into notes. Rhythm and grammar are kept in Sri Aurobindo's sense:
a bare and scrupulously exact rendering first; two words for one only to give the exact and
complete meaning; a double sense rendered where the original has one; the original's figures
kept; the word that makes us see; cadenced prose whose rhythm carries the thought.

V1 Read the sentence and every commentary on it in Sanskrit.
V2 Bare exact rendering. Each content word takes its row's default English (or a member of the
   row's rendering set). A word with no row: decide it by the lexicon method — meaning from the
   Sanskrit sources, `english "<meaning>"` to find words, `define` to verify — and mark it `new_row`.
V3 Carry the signification. Every active image or double sense in the row must be in the line:
   by one English word that holds both senses (preferred), by a properly formed compound, or by
   the row's doublet. Keep figures: repetition of a root, anaphora, parallels.
V4 Grammar in the line: case relations, agent nouns as agent nouns, bahuvrīhi as a description of
   its holder, voice, mood, tense; the construal's relations and referents.
V5 Rhythm and order: keep the Sanskrit's order of ideas and emphasis as far as English allows;
   cola follow the half-verses; each colon ends on a strong word; read it aloud in your head.
V6 ADD NOTHING. Every English content word renders one Sanskrit word of this sentence and carries
   that word's own meaning — not a commentator's explanation of it, not an etymology set beside
   it, not a doctrine. Supplied grammatical words ("is", "the", "who", "he") are allowed. A word
   the commentators supply (adhyāhāra) may enter only as such a grammatical word.
V7 Loss gate. Code computes, for every word, the row's signification components that your chosen
   rendering does not carry; each must be listed in `lost` with the three-step showing, or carried by
   a deviation whose `deviation_carries` you state. For every word list what the line fails to carry. A loss is a defect: go back to V2
   and revise until it is empty, or show that all three steps fail for it (existing words
   searched, new word attempted, keeping the Sanskrit fails). Accepting a loss to finish sooner
   is the failure this gate exists for.
V8 Every Sanskrit word gets a `words` entry — particles (na, eva, ca, hi, tu, api) and pronouns too;
   what the line says for it is its `english`.
V9 A second line only if the construal records a grammatical fork (not kind "doctrine") that one English line cannot hold; it
   renders the other construal in full. Never a word swap, never a doctrine.

The sentence is one English sentence; give each verse's part separately so it can be shown under
its verse.

Output exactly one JSON object and nothing else:
{"unit": ["12.13", ...],
 "lines": {"12.13": "...", "12.14": "..."},
 "alternative": null | {"fork": "...", "lines": {"12.13": "..."}},
 "words": [{"locus": "12.13", "i": n, "sanskrit": "...", "english": "<exact text of the line rendering it>",
            "sense_id": "..." | "new_row", "rendering": "<the row's rendering you used, copied exactly>", "deviation": null | "<why not the row's default>", "deviation_carries": [],
            "carried": ["..."], "lost": [] | [{"component": "...", "existing_searched": "...", "new_attempted": "...", "preserved_fails": "..."}]}],
 "new_rows": [ {row as in the lexicon schema} ]}
