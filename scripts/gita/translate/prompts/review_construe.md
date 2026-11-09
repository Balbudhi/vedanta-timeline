# Review a construal (independent reviewer)

You did not write this. Read `input.json` (the verse, the engine's candidate analyses, every
Sanskrit commentary) and `output.json` (the author's construal). Verify it against the grammar
and the commentaries; run `python3 -I TOOL sutra N`, `analyze FORM`, `gloss CH.V`, `dhatu ROOT`
as needed. Read no other file and no English translation.

Check: each word's analysis (stem, root, affix, case/number/gender, person/tense) and the sūtra
cited for any manual analysis; word class; compound type and vigraha (bahuvrīhi vs tatpuruṣa/
karmadhāraya — a bahuvrīhi agrees with its holder); each word's relation and kāraka; agreement
(every adjective with its noun, every finite verb with a subject); referents; supplied words;
whether the sentence continues into the next verse; forks — every GRAMMATICAL disagreement
among the commentators (a different split, analysis, compound type, relation or referent)
recorded with who holds it, and each fork's kind correct.

Scope: grammar only. These are NOT construal findings, because the lexicon stage receives every
commentator's gloss of every occurrence and decides senses there: a commentator's different
sense of a word (amarṣa, udvega, aniketa …), a doctrinal explanation, the purport, why a teaching
is given. Do not report them.

Output exactly one JSON object and nothing else:
{"findings": [{"id": "F1", "severity": "S1|S2|S3", "i": n | null, "says": "...", "evidence": "...", "fix": "..."}],
 "verdict": "accept" | "revise"}
S1: a wrong analysis, compound type, relation, referent or sentence boundary; a missing
grammatical fork that changes the English. S2: a wrong sūtra citation; a fork of the wrong kind. ("accept" only if no S1/S2.)
