# Vedic Heritage Portal — Government of India (registry only)

**Homepage:** https://vedicheritage.gov.in/ (HTTP 200, Apache, full
ACAO + Content-Security-Policy).
**License:** Government of India portal — "Terms & Conditions",
"Copyright Policy" and "Disclaimer" pages are linked from the footer.
Attribution to "Vedic Heritage Portal, Ministry of Culture, Government
of India" is required. Bulk download is not advertised; per-asset
download is permitted for research use.

## Status

Registry-only. The portal organises content into:

- **Samhitas** — four Vedas with multiple recension traditions.
- **Brāhmaṇas** — ritual + exegetical texts.
- **Āraṇyakas** — forest treatises.
- **Upaniṣads** — philosophical Upaniṣadic corpus.
- **Vedāṅgas** — auxiliary disciplines (kalpa, śikṣā, vyākaraṇa, …).
- **Rituals** and **Upavedas**.

Each Vedic branch surfaces audio recitations (Plyr-served), video, and
text PDFs through per-Maṇḍala / per-Brāhmaṇa pages. Direct per-file
PDFs were not enumerated by the homepage on this run (the front page is
a SPA-style index); future scraping needs to walk each Maṇḍala page and
collect the embedded `.pdf` / `.mp3` URLs.

The manifest records the source with `fetch_method: "per_url_scrape"`
and `fetch_status: "pending"`. Lane 2 deliberately does not fetch
audio (out of scope: prakriya is a text engine).
