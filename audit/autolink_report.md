# Glossary Autolink Inventory

**Mechanism note:** the runtime renderer (`assets/app.js`,
`buildGlossaryRegex` at line 2352 and the two `state.glossaryRegex` 
calls in `md()` / `renderMarkdownFull()`) auto-wraps every occurrence
of a glossary key or alias in `<span class="term" data-term=...>`.
Authors therefore do *not* embed link wrappers in source markdown;
coverage is determined entirely by the alias lists in
`data/glossary/*.json`.

## Coverage

- Files scanned: article=54, perspective=1, thinker=165, glossary=144
- Surfaces with at least one auto-link: **336**
- Distinct glossary keys hit: **144 / 144**
- Total auto-link occurrences (will render as popovers): **26427**

### Per-kind surface counts

- articles: 53 files contain at least one auto-link
- glossary: 144 files contain at least one auto-link
- perspectives: 1 files contain at least one auto-link
- thinkers: 138 files contain at least one auto-link

### Top 15 most-used glossary entries

- `brahman` (brahman): 2961 occurrences
- `sutra` (sūtra): 1804 occurrences
- `bhasya` (bhāṣya): 1492 occurrences
- `jiva` (jīva): 1297 occurrences
- `advaita` (advaita): 1188 occurrences
- `bhakti` (bhakti): 765 occurrences
- `avidya` (avidyā): 742 occurrences
- `jnana` (jñāna): 590 occurrences
- `karma` (karma): 497 occurrences
- `sakti` (śakti): 493 occurrences
- `maya` (māyā): 482 occurrences
- `pramana` (pramāṇa): 476 occurrences
- `purusa` (puruṣa): 460 occurrences
- `prakrti` (prakṛti): 403 occurrences
- `acintya` (acintya): 398 occurrences

### Unused glossary entries (0)


## New-entry queue

- Genuinely new candidates (≥2 occurrences) queued in `audit/glossary_terms_to_create.json`: **1508**
- Low-priority diacritic singletons (deferred bucket): **1738**
- Alias-augmentation proposals (inflected forms of existing entries): **19**
- Capitalization gaps (sentence-start capitalized forms missing from alias lists): **10**
- Work-title tokens skipped (belong to citation index, not glossary): **265**
- Proper-name tokens skipped (already a thinker page): **21**
- English-adjective tokens skipped: **12**

Filters applied:

- Italicized Sanskrit token (`*term*`) is the primary precision signal.
- ≥2 occurrences OR a diacritic-bearing token.
- Stem-fold (IAST → ASCII, with terminal -s/-m/-n/-aḥ stripped) routes
  inflected forms into the alias-augmentation bucket instead of the queue.
- Work-title denylist + suffix list routes commentary names away.
- *No glosses are invented*: Agent G picks these up and authors entries
  from primary sources.

### Top 30 genuinely-new candidates

- `cit` (153 occurrences)
- `vijñāna` (123 occurrences)
- `adhikāra` (101 occurrences)
- `bhāvanā` (82 occurrences)
- `adhyāya` (76 occurrences)
- `acintya-śakti` (69 occurrences)
- `adhikaraṇa` (66 occurrences)
- `codanā` (66 occurrences)
- `vṛtti` (66 occurrences)
- `apūrva` (64 occurrences)
- `upāsanā` (63 occurrences)
- `svabhāva` (57 occurrences)
- `bhāvarūpa` (56 occurrences)
- `svarūpa` (51 occurrences)
- `kārikā` (48 occurrences)
- `īpk` (47 occurrences)
- `adhyāyas` (46 occurrences)
- `vyāpti` (45 occurrences)
- `āśraya` (43 occurrences)
- `bhakti-yoga` (42 occurrences)
- `tattva` (40 occurrences)
- `viṣaya` (40 occurrences)
- `darśana` (39 occurrences)
- `prakāśa` (38 occurrences)
- `tantrāloka` (37 occurrences)
- `abhāva` (36 occurrences)
- `bhāva` (34 occurrences)
- `samādhi` (34 occurrences)
- `jñāna-karma-samuccaya` (33 occurrences)
- `nyāya-sudhā` (33 occurrences)

### Top 20 alias-augmentation proposals

These are inflected forms of existing glossary entries. Folding their
stem into the entry's `aliases` list will make the runtime regex catch
them on next page load — no new entry needed.

- `ājñāna` → existing entry `avidya` (14 occurrences)
- `tattva-vāda` → existing entry `dvaita` (13 occurrences)
- `dharma-bhūta-jñāna` → existing entry `dharmabhuta-jnana` (7 occurrences)
- `kalyāṇa-guṇas` → existing entry `guna` (7 occurrences)
- `aparokṣa` → existing entry `aparoksa-jnana` (4 occurrences)
- `ajñana` → existing entry `avidya` (3 occurrences)
- `jñāni` → existing entry `jnana` (3 occurrences)
- `sat-kārya-vāda` → existing entry `satkarya-vada` (3 occurrences)
- `sat-cit-ānanda` → existing entry `saccidananda` (2 occurrences)
- `śābda` → existing entry `sabda` (2 occurrences)
- `acintya-bhedābheda` → existing entry `acintya` (1 occurrences)
- `brahmā` → existing entry `brahman` (1 occurrences)
- `cittavṛtti` → existing entry `citta` (1 occurrences)
- `kārma` → existing entry `karma` (1 occurrences)
- `nirguṇa-brahman` → existing entry `nirguna` (1 occurrences)
- `saguṇa-brahman` → existing entry `saguna` (1 occurrences)
- `tātparya-vṛtti` → existing entry `tatparya` (1 occurrences)
- `vivarta-vāda` → existing entry `vivarta` (1 occurrences)
- `śarīra-śarīri-bhāva` → existing entry `sarira-saririn-bhava` (1 occurrences)

## Known limitations

- The italics signal (`*term*`) is the primary precision filter. Bare
  romanized tokens (e.g. plain "karma" in casual prose) are intentionally
  not flagged; the renderer's regex still picks them up if a glossary alias
  exists, but we do not surface them as new-entry candidates.
- A token in a markdown link's display text *could* be flagged spuriously;
  inline-code and fenced-code blocks are stripped before scanning.
- Whole italicized spans are treated as the candidate lemma. Multi-word
  italic phrases (containing a space) are dropped to avoid noise; this
  may miss legitimate two-word Sanskrit titles, which surface in the
  citation index instead.
- The work-title denylist is curated, not exhaustive. Compounds ending in
  `-bhāṣya`, `-sūtra`, `-kārikā`, etc. are filtered by suffix; novel work
  names without those suffixes may slip through.
- Codex/Opus authoring step (Agent G) must confirm each candidate is a
  real Sanskrit technical term, not (e.g.) an italicized English phrase
  or a proper name already covered by the thinkers index.
