# Gītā word card: meaning and fork display contract (lead interface, 2026-11-08)

> **Superseded 2026-11-08:** folded into `SANSKRIT_TRANSLATION_STANDARD.md` §2–§3, which governs. Kept for history.

This is the data interface between the producers (who write it), the builder (which
checks it) and the reader `assets/gita.js` (which shows it). It implements standard
§6.2–§6.3 on the card. The standard folds this file into §3; until then it governs.

## Word card: `meaning`

```jsonc
"meaning": {
  "image": "√ās 'to sit' with upa- 'near': to sit near, attend",      // the root's concrete image, one line
  "lines": [                                                          // ordered as below; 1–8 lines
    { "cat": "lexical",     "text": "to attend upon, wait on, serve; to sit near in reverence",  "who": "Monier-Williams", "locus": "sources/raw/upstream_data/kosha/mw.json#…" },
    { "cat": "nirvacana",   "text": "upāsanā is going near the object and staying with it long, a stream of one thought like poured oil", "who": "Śaṅkara on 12.3", "locus": "vedanta-timeline/data/sources/…/shankara_gita_bhasya.txt:8401" },
    { "cat": "commentator", "text": "dhyāyanti — they meditate", "who": "Śaṅkara on 12.1", "locus": "…:8375" },
    { "cat": "usage",       "text": "the same verb takes a sacrifice (4.25) and a teaching (12.20) as object", "who": "Gītā" },
    { "cat": "reception",   "text": "\"seek after\"", "who": "Sri Aurobindo (Roy 1938)" },
    { "cat": "synthesis",   "text": "the site's labelled reading, if any" }
  ],
  "rendering": "attend upon",                 // the English used in the line for this word
  "why": "keeps 'sit near' and 'serve'; 12.6 separates meditating (dhyāyantaḥ) from upāsate, so not 'meditate'",
  "alternatives": ["worship", "meditate on", "wait upon"]   // other renderings a reader will meet, without attribution of copyrighted text
}
```

Categories, in display order (standard §6.3; closed list): `formation` (only when the
grammar card does not already say it), `lexical` (kośa / dictionary senses),
`nirvacana` (a transmitted or commentator's etymology), `commentator` (a gloss on this
word in this verse), `usage` (the Gītā's own use elsewhere), `reception` (later
reception and modern translators — a translator is named with at most a few words of
quotation), `synthesis` (the site's own labelled reading). `text` is reader-facing
English: no pipeline vocabulary (policy row, lead, owner, gate, shard, producer,
reviewer, fallback, F-numbers, §-numbers of internal documents).

Required on every card that has a root or a compound and every preserved term;
optional on particles, pronouns and names (names carry their etymology in `parts`).

## Verse: `forks`

Each fork keeps its record (`at`, `construals[]`, `followed`, `reason_class`,
`reason`, `open`) and gains:

```jsonc
"words": [3, 4],                       // the card indices the fork concerns (for display on those cards)
"display": "The compound can also be read as 'unfastened' (a-sakta); every commentator reads 'fastened to'."   // one or two reader-facing sentences
```

The reader shows `display` under "Other readings" on the cards named in `words`, and
lists all open forks (`open: true`) under the verse. Construal details stay in the
data for the apparatus.

## Public-text rule

`gloss`, `parts[].gloss`, `rootGloss`, `note`, `meaning.*`, `forks[].display`,
`sense` and `grammar.*` are public. They are written for a reader of the site and
may not contain pipeline vocabulary. The builder refuses a chapter that violates this.
