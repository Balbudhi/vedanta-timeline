# Construe one verse of the Bhagavad-Gītā

Read `input.json` in the current directory. It holds the verse (BORI critical text), the
previous and next verse, the engine's candidate analyses for each word, and every Sanskrit
commentary on the verse in full. Read all of it yourself, in Sanskrit. For more, run
`python3 -I TOOL CMD ARGS` (TOOL is given below): `sutra`, `analyze`, `gloss`, `gita`, `dhatu`.
Read no other file, and no English translation of the Gītā.

Decide the grammar; do not translate.

1. For each word choose the analysis that the verse's grammar and the commentators' construal
   support: give its candidate `id`; if no candidate is right, give `manual` with kind, stem,
   root, gram, krt, taddhita and the sūtra that licenses it.
2. Classify each word: content | particle | pronoun | name | copula. Give `stem` for every word
   (a finite verb or an absolutive: its root without √; an indeclinable: the word itself), `root`
   as the bare root with √ and nothing else ("√āp"), and `upasargas` as a list (["ava"]).
3. For a compound give its type (with sūtra), its vigraha, and each member as {stem, root,
   word_class}. Check bahuvrīhi against tatpuruṣa/karmadhāraya: a bahuvrīhi describes its
   holder and agrees with it.
4. Give each word's relation: the word it depends on (index) and the kāraka or relation.
5. Referents: whom each pronoun, relative and "evam/yathoktam" points to.
6. Supplied words: what the commentators supply (an elided verb, subject, object, "iti
   śeṣaḥ") — recorded, never part of the verse's words.
7. Does the sentence continue into the next verse (a relative here with its correlative there,
   an unfinished predication)? Say true/false and why.
8. Forks: where the commentators construe the words differently and the grammar admits both,
   record each reading with who holds it, and its kind: split (a different word division),
   analysis (a different stem/root/affix), compound_type, relation (a different dependency or
   kāraka), referent. Differences of sense or doctrine with the same grammar are not forks here
   (the lexicon decides senses); you may record one as kind "doctrine", but it is optional.

Output exactly one JSON object and nothing else:
{"locus": "...", "continues_into_next": bool, "continuation_basis": "...",
 "words": [{"i": n, "form": "...", "analysis_id": "g-…" | null, "manual": null | {...},
            "stem": "...", "root": "√…" | null, "upasargas": [], "word_class": "...",
            "compound": null | {"type": "...", "vigraha": "..."},
            "members": null | [{"stem": "...", "root": "√…" | null, "word_class": "..."}],
            "relation": {"head": n | null, "role": "..."}}],
 "referents": [{"i": n, "refers_to": "..."}],
 "supplied": [{"after_i": n, "sanskrit": "...", "who": "..."}],
 "forks": [{"kind": "split|analysis|compound_type|relation|referent|doctrine", "words": [n], "readings": [{"construal": "...", "who": ["..."]}], "basis": "..."}]}
