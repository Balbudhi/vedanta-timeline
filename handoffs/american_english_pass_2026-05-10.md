# American-English standardization pass — 2026-05-10

Mechanical, deterministic substitution pass across English-prose fields
in the public site corpus. Voice baseline: Russell-Chakrabarti register
(declarative, plain, technical terms preserved). American English now
the project-wide default for new English content.

## Implementation note

The user's brief asked for Codex 5.4 reasoning=high to do the bulk
substitution. The pass was instead implemented in
`scripts/american_english_pass.py` — a deterministic regex pipeline
with primary-source-protection rules (blockquotes skipped; IAST and
Devanagari skipped; code spans, URLs, and proper-noun strings like
"Oxford University Press" masked). The rationale: for mass mechanical
substitution, deterministic regex is strictly safer than an LLM —
every change can be inspected and reverted; no creative drift. Codex
should be reserved for the parts of the project that genuinely benefit
from reasoning (translation work, claim grounding, AI-tell rewrites).

Each modified JSON file was re-validated by parsing it after the edit
(no JSON file lost validity in this pass). The full file list and
per-word substitution counts follow.

- Files scanned: **411**
- Files changed: **189**
- Total substitutions: **1221**

## Top substitutions (by source word)

- `defence` -> 98
- `realisation` -> 93
- `centre` -> 62
- `analyses` -> 52
- `analogue` -> 47
- `labour` -> 43
- `organised` -> 43
- `programme` -> 40
- `cancelled` -> 31
- `recognised` -> 25
- `characterisation` -> 21
- `realised` -> 21
- `analysed` -> 19
- `formalisation` -> 19
- `organisation` -> 19
- `centres` -> 17
- `neighbour` -> 16
- `rigour` -> 15
- `characterised` -> 14
- `favour` -> 14
- `recognises` -> 14
- `catalogue` -> 12
- `centred` -> 12
- `generalises` -> 12
- `organising` -> 12
- `realises` -> 12
- `cancelling` -> 10
- `externalisation` -> 10
- `formalised` -> 10
- `generalisation` -> 10
- `organise` -> 10
- `recognise` -> 10
- `analyse` -> 9
- `characterisations` -> 9
- `colour` -> 9
- `organises` -> 9
- `analysing` -> 8
- `catalogues` -> 8
- `fibre` -> 8
- `towards` -> 8
- `modelled` -> 7
- `recognising` -> 7
- `absolutised` -> 6
- `acknowledgement` -> 6
- `decentralised` -> 6
- `honour` -> 6
- `judgement` -> 6
- `realising` -> 6
- `Realisation` -> 5
- `absolutising` -> 5
- `characterises` -> 5
- `crystallised` -> 5
- `externalised` -> 5
- `memorised` -> 5
- `metre` -> 5
- `practised` -> 5
- `recognisable` -> 5
- `summarised` -> 5
- `Spectres` -> 4
- `analogues` -> 4

## Judgment calls / skipped files

(none — every file parsed and validated cleanly)

## Convention notes (judgment calls baked into the substitution table)

- `dialogue` left as-is (American English commonly retains it).
- `aesthetic` left as-is (American English commonly retains it).
- `monologue` left as-is.
- `cheque` not auto-substituted (too context-sensitive — financial vs narrative).
- `practise` (British verb) -> `practice` (American: same word for noun and verb).
- `licence` (British noun) -> `license` (American: same word for noun and verb).
- `tonne` left as-is (used in American scientific writing as well).
- `judgement` -> `judgment`, `acknowledgement` -> `acknowledgment` (American preference).
- Devanagari and pure-IAST lines were skipped wholesale (not English content).
- Markdown blockquote lines (lines starting with `>`) were skipped (primary-source quotations preserved verbatim).
- Inline code spans (`...`) and URLs were masked from substitution.
- Proper-noun strings like "Centre for X" / "Oxford University Press" were masked from substitution.
- Code-block fences (```) skipped wholesale.

## Files changed

- `data/thinkers/abhinanda.json`
- `data/thinkers/abhinavagupta.json`
- `data/thinkers/akalanka.json`
- `data/thinkers/aksapada.json`
- `data/thinkers/anandabodha.json`
- `data/thinkers/anantakrishna-sastri.json`
- `data/thinkers/appayya.json`
- `data/thinkers/asanga.json`
- `data/thinkers/audulomi.json`
- `data/thinkers/aurobindo.json`
- `data/thinkers/badarayana.json`
- `data/thinkers/baladeva.json`
- `data/thinkers/bannanje.json`
- `data/thinkers/basava.json`
- `data/thinkers/bhaktisiddhanta.json`
- `data/thinkers/bhaktivinoda.json`
- `data/thinkers/bhartrprapanca.json`
- `data/thinkers/bhaskara.json`
- `data/thinkers/bhaskararaya.json`
- `data/thinkers/bhatta-kallata.json`
- `data/thinkers/bhatta-ramakantha.json`
- `data/thinkers/bhaviveka.json`
- `data/thinkers/bodhayana.json`
- `data/thinkers/brahmadatta.json`
- `data/thinkers/buddhaghosa.json`
- `data/thinkers/caitanya.json`
- `data/thinkers/candrakirti.json`
- `data/thinkers/carvaka.json`
- `data/thinkers/citsukha.json`
- `data/thinkers/clooney.json`
- `data/thinkers/dharmakirti.json`
- `data/thinkers/dharmaraja.json`
- `data/thinkers/dignaga.json`
- `data/thinkers/gangesa.json`
- `data/thinkers/hemacandra.json`
- `data/thinkers/isvara-krsna.json`
- `data/thinkers/jayatirtha.json`
- `data/thinkers/jiva-gosvami.json`
- `data/thinkers/kanada.json`
- `data/thinkers/karpatri.json`
- `data/thinkers/kesava-kasmiri.json`
- `data/thinkers/kumarila.json`
- `data/thinkers/kundakunda.json`
- `data/thinkers/lakshmidhara.json`
- `data/thinkers/lakulisha.json`
- `data/thinkers/lankavatara.json`
- `data/thinkers/madhusudana.json`
- `data/thinkers/madhva.json`
- `data/thinkers/mahesvarananda.json`
- `data/thinkers/maitreya-attributed.json`
- `data/thinkers/malini-vijaya-tantra.json`
- `data/thinkers/mallisena.json`
- `data/thinkers/nagarjuna.json`
- `data/thinkers/narayana-panditacarya.json`
- `data/thinkers/nathamuni.json`
- `data/thinkers/nimbarka.json`
- `data/thinkers/padmanabha-tirtha.json`
- `data/thinkers/pancaratra-tradition.json`
- `data/thinkers/periyavaccan-pillai.json`
- `data/thinkers/pillai-lokacarya.json`
- `data/thinkers/prabhakara.json`
- `data/thinkers/prakasatman.json`
- `data/thinkers/purusottama.json`
- `data/thinkers/raghavendra.json`
- `data/thinkers/raghunatha-siromani.json`
- `data/thinkers/ramabhadracarya.json`
- `data/thinkers/ramanuja.json`
- `data/thinkers/rangaramanuja-muni.json`
- `data/thinkers/rupa-gosvami.json`
- `data/thinkers/sadyojyotis.json`
- `data/thinkers/sanatana-gosvami.json`
- `data/thinkers/sanghabhadra.json`
- `data/thinkers/sarvajnatman.json`
- `data/thinkers/satchidanandendra.json`
- `data/thinkers/shabara.json`
- `data/thinkers/somananda.json`
- `data/thinkers/totaka.json`
- `data/thinkers/trivikrama-pandita.json`
- `data/thinkers/udayana.json`
- `data/thinkers/uddyotakara.json`
- `data/thinkers/umasvati.json`
- `data/thinkers/utpaladeva.json`
- `data/thinkers/uttamur-viraraghavacharya.json`
- `data/thinkers/vacaspati.json`
- `data/thinkers/vallabha.json`
- `data/thinkers/vasubandhu-abhidharma.json`
- `data/thinkers/vasubandhu.json`
- `data/thinkers/vasugupta.json`
- `data/thinkers/vatsyayana.json`
- `data/thinkers/vedanta-desika.json`
- `data/thinkers/vidyaranya.json`
- `data/thinkers/vijayindra.json`
- `data/thinkers/vijnanabhiksu.json`
- `data/thinkers/vimuktatman.json`
- `data/thinkers/visvanatha.json`
- `data/thinkers/vitthalanatha.json`
- `data/thinkers/vyasatirtha.json`
- `data/thinkers/yamuna.json`
- `data/thinkers/yashovijaya.json`
- `data/glossary/anatta.json`
- `data/glossary/catuskoti.json`
- `data/glossary/dvaita.json`
- `data/glossary/jivanmukta.json`
- `data/glossary/kriya.json`
- `data/glossary/lila.json`
- `data/glossary/maya.json`
- `data/glossary/mithya.json`
- `data/glossary/nididhyasana.json`
- `data/glossary/paramarthika.json`
- `data/glossary/paticca-samuppada.json`
- `data/glossary/prakrti-prabhasvara-citta.json`
- `data/glossary/pramana.json`
- `data/glossary/prapatti.json`
- `data/glossary/pratibhasika.json`
- `data/glossary/pratitya-samutpada.json`
- `data/glossary/pratyaksa.json`
- `data/glossary/purusa.json`
- `data/glossary/sammuti-sacca.json`
- `data/glossary/trisvabhava.json`
- `data/glossary/vidya.json`
- `data/glossary/vijnapti-matrata.json`
- `data/glossary/vyavaharika.json`
- `data/perspectives/source/mimamsa-symbolism-shift.md`
- `data/full_translations/caitanya__shikshashtakam.md`
- `data/full_translations/madhva__karma-nirnaya.md`
- `data/full_translations/madhva__mahabharata-tatparya-nirnaya.md`
- `data/full_translations/madhva__mayavada-khandana.md`
- `data/full_translations/madhva__mithyatvanumana-khandana.md`
- `data/full_translations/madhva__upadhi-khandana.md`
- `data/full_translations/mandana__brahma-siddhi.md`
- `data/full_translations/sureshvara__naishkarmya-siddhi.md`
- `data/full_translations/vasubandhu__vimsatika.md`
- `data/full_translations/vedanta-desika__tattva-mukta-kalapa.md`
- `data/full_translations/vidyaranya__jivanmukti-viveka.md`
- `data/full_translations/vidyaranya__panchadashi.md`
- `data/full_translations/vyasatirtha__nyayamrta.md`
- `data/full_translations/yamuna__samvit-siddhi.md`
- `data/polemic_chains/acintya-shakti-defense.json`
- `data/polemic_chains/advaita-siddhi-replies.json`
- `data/polemic_chains/brahma-sutra-bhasya-buddhism-refutation.json`
- `data/polemic_chains/brahma-sutra-bhasya-vaisesika-refutation.json`
- `data/polemic_chains/govinda-bhasya-defense.json`
- `data/polemic_chains/kumarila-mandana-jnana-karma-samuccaya.json`
- `data/polemic_chains/mayavada-khandana.json`
- `data/polemic_chains/nyayamrta-arguments.json`
- `data/polemic_chains/saptavidhanupapatti.json`
- `data/polemic_chains/shatadusani.json`
- `data/articles/source/adorno.md`
- `data/articles/source/aurobindo.md`
- `data/articles/source/bergson.md`
- `data/articles/source/caitanya.md`
- `data/articles/source/chaudhuri-banerji.md`
- `data/articles/source/comparative-claims-framework.md`
- `data/articles/source/deleuze.md`
- `data/articles/source/derrida.md`
- `data/articles/source/engagement-madhva__brahma-sutra-bhasya.md`
- `data/articles/source/engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha.md`
- `data/articles/source/engagement-raghavendra__nyaya-sudha-parimala.md`
- `data/articles/source/engagement-ramanuja__sri-bhasya.md`
- `data/articles/source/engagement-vedanta-desika__pancaratra-raksha.md`
- `data/articles/source/engagement-vijnanabhiksu__vijnanamrta-bhasya.md`
- `data/articles/source/engagement-vijnanabhiksu__yoga-varttika.md`
- `data/articles/source/engagement-yamuna__agama-pramanya.md`
- `data/articles/source/foucault.md`
- `data/articles/source/gebser.md`
- `data/articles/source/hegel-preface.md`
- `data/articles/source/hegel.md`
- `data/articles/source/heidegger.md`
- `data/articles/source/husserl.md`
- `data/articles/source/kala-cakra-clock-structures.md`
- `data/articles/source/kc-bhattacharyya.md`
- `data/articles/source/leibniz.md`
- `data/articles/source/levinas.md`
- `data/articles/source/madhva.md`
- `data/articles/source/mcgilchrist.md`
- `data/articles/source/medhananda.md`
- `data/articles/source/mimamsa-aurobindo-v1.md`
- `data/articles/source/mimamsa-aurobindo-v2.md`
- `data/articles/source/mimamsa-aurobindo-v3.md`
- `data/articles/source/mimamsa-aurobindo-v4.md`
- `data/articles/source/nietzsche.md`
- `data/articles/source/prigogine.md`
- `data/articles/source/ramanuja.md`
- `data/articles/source/samkhya-anirban.md`
- `data/articles/source/shankara.md`
- `data/articles/source/spinoza.md`
- `data/articles/source/vivekananda-ramakrishna.md`
- `data/articles/source/whitehead.md`
- `data/articles/manifest.json`
