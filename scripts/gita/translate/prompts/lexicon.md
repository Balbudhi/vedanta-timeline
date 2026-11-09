# Decide the English for one family of Sanskrit words (lexicon)

Read `input.json`: a word family (one root, or one stem), its occurrences in scope with each
verse and every commentator's gloss there, the Dhātupāṭha entry, and each lemma's meaning page
(kośas, Dhātuvṛttis, Nirukta, Gītā concordance, glosses). All Sanskrit. Run more lookups with
`python3 -I TOOL CMD ARGS`: `dhatu`, `meaning`, `kosha`, `amara`, `unadi`, `linga`, `concord`,
`gloss`, `english "MEANING"`, `define WORD`. Read no other file and no English translation of
the Gītā. Your decisions bind every verse: each verse job must use what you decide here.

The owner's standard. A translation is lossless when the English line itself carries what each
word means and what it signifies — its sense here, its root image, the tradition's reading.
Meaning is never moved into notes. Rhythm and grammar are kept in Sri Aurobindo's sense.

Work through these steps for each distinct sense of each lemma:

L1 Meaning from Sanskrit. Establish the sense from the Sanskrit sources: the root's artha and
   Dhātuvṛtti, the kośas, Nirukta, Uṇādi, and how the commentators gloss it at each occurrence.
   Do not take meaning from an English dictionary. Assign every distinct gloss to a sense or
   reject it with a reason (e.g. bhakta "boiled rice" is a real sense that does not occur here).
L2 Signification. State the root image and what the word signifies beyond its bare sense. An
   image is active when a commentator glosses by it, the root repeats in the passage, or the
   verse's figure uses it. Active signification must be carried.
L3 Find the English BY MEANING, never by first guess. Run `english "<the sense in plain
   words>"` and `english "<the root image>"` (and variations), read what the dictionaries
   return, then `define` every candidate you would use. A word you thought of yourself is
   admissible only after you have searched and `define`d it; say so.
L4 Choose the form, in the owner's order:
   a. an existing English word that carries meaning and signification. Rare or older real words
      are fair game when more exact; plain is never the default; rare is never for its own sake.
   b. if no word carries it whole, a new English word properly formed from real English parts:
      head last, legible at first hearing, one coherent image, adding nothing (Aurobindo: words
      "properly formed and not ugly or unintelligible"; never a made-up comic-book word).
   c. keep the Sanskrit only when nothing in English can carry it.
   Among candidates: carries meaning and signification whole > reads at first hearing > keeps
   the image > sounds best > fits scripture read aloud.
L5 Connotation, separately. Reject a word whose modern associations are wrong (e.g. "worship"
   for upāsanā imports a cult; "devotee" loses √bhaj's sharing).
L6 One English root per Sanskrit root where English allows, so the repetition is heard.
L7 Loss gate. `signification` lists the components (sense, image, double value) that must be carried
   where active; each rendering states exactly which it `carries` — code computes what a line loses
   from this, so over-claiming is a defect the reviewer checks against the dictionaries. For the chosen
   default, list what it fails to carry. A loss is a defect: revise
   until the list is empty, or show for each loss that all three steps fail — the existing
   words searched (with the queries), a new word attempted (and why it fails), and why keeping
   the Sanskrit fails or loses more.

Output exactly one JSON object and nothing else:
{"family": "...",
 "rows": [{"sense_id": "lemma.short", "lemmas": ["stem", ...],
   "sense": "<our decided meaning, in English, citing the Sanskrit loci it rests on>",
   "image": "...", "signification": ["..."],
   "glosses": {"assigned": n, "rejected": [{"who": "...", "text": "...", "why": "..."}]},
   "searches": [{"query": "...", "useful": ["..."]}],
   "candidates": [{"english": "...", "form": "existing|new|preserved", "carries": "...", "loses": "...", "define": "attested|new"}],
   "default": "...",
   "rendering_set": [{"english": "<the default and up to 3 other exact candidates>", "carries": ["<which of signification[] this rendering carries>"]}],
   "forms": {"verb": "...", "noun": "...", "agent": "..."},
   "form": "existing|new|preserved", "why": "...",
   "loss": [] | [{"component": "...", "existing_searched": "...", "new_attempted": "...", "preserved_fails": "..."}],
   "occurrences": ["12.1", ...]}]}
