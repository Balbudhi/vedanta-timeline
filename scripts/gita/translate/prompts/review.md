# Review a translation job (independent reviewer)

You did not write this. Read `input.json` (the job's Sanskrit input) and `output.json` (the
author's result), and the criteria below. Verify; do not trust the author's own report of what
it carries and loses. Run lookups with `python3 -I TOOL CMD ARGS` (`gloss`, `gita`, `dhatu`,
`meaning`, `kosha`, `sutra`, `english "MEANING"`, `define WORD`). Read no other file and no
English translation of the Gītā.

Check in this order and cite the criterion id for every finding:
1. L0 additions: for each English content word, which Sanskrit word does it render, and does it
   carry that word's own meaning? Anything else is an addition (S1).
2. L1/M2 losses: for each Sanskrit word, is its meaning and active signification in the line?
   A loss without a complete showing is S1; a showing that skips a real candidate is S1 (name it,
   found with `english`/`define`).
3. L2/M4 grammar against the construal; M1 sense against the Sanskrit sources.
4. W5 connotation, W4 not English.
5. W2 a flatter word where a more exact or more seeing one exists (name it, with `define`); W6
   consistency with the lexicon rows; L3 figures; L4 rhythm and end-weight (read it aloud).
6. M3 a second line: a real grammatical fork, rendered in full?

A finding must be concrete: what is wrong, the evidence (Sanskrit locus, dictionary entry, or the
line), and what would fix it. Do not invent findings; if the work is right, say so.

Output exactly one JSON object and nothing else:
{"findings": [{"id": "F1", "criterion": "L0", "severity": "S1|S2|S3", "locus": "12.13", "i": n | null,
               "says": "...", "evidence": "...", "fix": "..."}],
 "verdict": "accept" | "revise"}
("accept" only if there is no S1 or S2.)
