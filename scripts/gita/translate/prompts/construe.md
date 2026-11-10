# Construe one verse of the Bhagavad-Gītā

Read `input.json` in the current directory; it is complete, and you run no other command. It holds,
in this order: the verse (BORI critical text); for each token the grammar engine's candidate analyses
of each of its padas (a sandhi-joined token has several, listed in `padas`), each with its derivation
(prakṛti + pratyaya with the sūtras that introduce each affix); the previous and next verse; and LAST
every Sanskrit commentary on the verse in full. Candidates marked `further` are the engine's other
analyses of the form (finite verbs, participles and indeclinables first), given without derivation;
choose one when it is right rather than writing a manual analysis. Read no other file, and no English translation.

Work in that order. First decide the grammar from the candidates, their derivations, agreement and the
syntax of the verse. Then read the commentaries as witnesses: to confirm your construal, to find where
they construe the words differently (forks), and what they supply. A commentator's reading does not
replace a construal the grammar requires.

Decide the grammar; do not translate.

1. For each word choose the analysis the verse's grammar requires: give its candidate `id`. If no
   candidate is right, give `manual` with kind, stem, root, gram, krt, taddhita and the sūtra that
   licenses it, and say in `manual.why` why every candidate fails. For a token with several padas,
   give `manual.padas`: one {pada, analysis_id or gram, stem, root, word_class} per pada.
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
