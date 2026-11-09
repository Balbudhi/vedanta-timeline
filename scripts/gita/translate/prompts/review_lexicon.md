# Review lexicon rows (independent reviewer)

You did not write this. Read `input.json` (the word families: occurrences with commentator
glosses, the Dhātupāṭha entry, meaning pages, every other Gītā occurrence) and `output.json`
(the author's rows), and the criteria below. These rows bind every verse of the Gītā, so a wrong
row is wrong everywhere. Run `python3 -I TOOL CMD ARGS` (`dhatu`, `meaning`, `kosha`, `amara`,
`unadi`, `gloss`, `concord`, `english "MEANING"`, `define WORD`). Read no other file and no
English translation of the Gītā.

Check each row, citing the criterion id:
1. M1 Is the sense established from the Sanskrit sources, and does it fit every occurrence it
   claims (check the verses in `elsewhere_in_gita` too)? Is a distinct sense wrongly merged, or
   one sense wrongly split?
2. M2 Is `signification` right — is an active image missing, or is an inactive one (or a
   commentator's alternative reading) listed as if it were the word's own value?
3. W1 Search the dictionaries yourself by the sense (`english "<sense>"`, `english "<image>"`):
   is there an existing English word or a properly formed new word that carries more than the
   default? Name it with its `define` entry. This is the main check.
4. Over-claiming: does each rendering really carry what its `carries` says? Check with `define`.
   A rendering claiming the image when its current English sense does not carry it (M5) is S1.
5. W5 connotation; W4 not English; W7 an invented word that fails the formation tests.
6. L1 a loss showing that skips a real candidate (name it).
7. W6 the same English used for two different senses, or one sense given two Englishes.

Output exactly one JSON object and nothing else:
{"findings": [{"id": "F1", "criterion": "W1", "severity": "S1|S2|S3", "sense_id": "...",
               "says": "...", "evidence": "...", "fix": "..."}],
 "verdict": "accept" | "revise"}
("accept" only if there is no S1 or S2.)
