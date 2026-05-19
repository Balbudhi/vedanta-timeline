# DSAL — Digital South Asia Library, University of Chicago (registry only)

**Homepage:** https://dsal.uchicago.edu/ (HTTP 200).
**Sanskrit dictionaries page:** https://dsal.uchicago.edu/dictionaries/
**License:** "DSAL project terms" + per-dictionary licence. DSAL
republishes scans + transcribed dictionaries by permission of the
original publishers; redistribution of the underlying XML / raw text is
typically restricted, even when browse / search access is free.

## Status

Registry-only. The two highest-value DSAL Sanskrit dictionaries are:

- **Apte Sanskrit Dictionary** — https://dsal.uchicago.edu/dictionaries/apte
  (V.S. Apte, *The Practical Sanskrit-English Dictionary*, 1890; revised
  by Gode & Karve 1957).
- **Macdonell Sanskrit Dictionary** — https://dsal.uchicago.edu/dictionaries/macdonell
  (A.A. Macdonell, *A Practical Sanskrit Dictionary*, 1924).

Monier-Williams is not hosted on DSAL — use Cologne Digital Sanskrit
Lexicon (already registered in `prakriya/sources/panini/commentarial_source_registry.json`).

DSAL provides per-headword HTML pages; raw XML is generally not
exposed for direct download (the Cologne project distributes the raw
XML under separate licence). The manifest records DSAL as
`fetch_method: "per_url_scrape"`, `fetch_status: "pending"`, but the
prakriya lexicon should prefer the Cologne XML for bulk lexical join.
