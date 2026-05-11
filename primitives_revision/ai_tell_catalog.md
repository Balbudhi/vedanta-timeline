# AI-Tell Catalog

## Method

Pass 1 used exact-string grep on `data/articles/source/*.md`.

Pass 2 used two heuristics:

- `rule-of-three` regex: `\b[^,.;:]{1,40}, [^,.;:]{1,40}, and [^,.;:]{1,40}\b`
- `triple-pile` regex: `\b[a-zA-Z-]+, [a-zA-Z-]+, [a-zA-Z-]+ [a-zA-Z-]+\b`

The exact-string lists below are exhaustive for the strings named. The heuristic lists are exhaustive for the regexes, but they include some false positives along with the real tonal problems.

## Exact-String Hits

Top counts:

- `thus`: 91
- `ultimately`: 51
- `indeed`: 29
- `represents`: 16
- `in summary`: 5
- `journey`: 5

No hits:

- `delve`
- `tapestry`
- `rich complexity`
- `leverage`
- `navigate the`
- `embark on`
- `stands at the intersection`
- `while not exhaustive`
- `though much remains to be said`
- `this article/paper does not merely`
- `the latter half of the`

Hit lists:

- `explore`: `kala-cakra-clock-structures.md:126`; `whitehead.md:283`
- `in essence`: `whitehead.md:333`
- `in conclusion`: `engagement-raghavendra__tantra-dipika.md:63`
- `it is worth noting`: `heidegger.md:202`
- `landscape of`: `derrida.md:103`
- `moreover`: `gebser.md:188,309`; `spinoza.md:424`
- `furthermore`: `caitanya.md:421`; `chaudhuri-banerji.md:349`; `medhananda.md:139`
- `encompasses`: `chaudhuri-banerji.md:587`; `husserl.md:111`; `medhananda.md:257`
- `facets`: `chaudhuri-banerji.md:657`; `gebser.md:558`
- `henceforth`: `shankara.md:9,47`
- `journey`: `aurobindo.md:364`; `caitanya.md:9`; `hegel.md:67,197,206`

`in summary`

```text
heidegger.md:196
kala-cakra-clock-structures.md:444
leibniz.md:15
madhva.md:579
prigogine.md:82
```

`ultimately`

```text
aurobindo.md:497
caitanya.md:109,413,477,531
chaudhuri-banerji.md:238,286
comparative-claims-framework.md:75
deleuze.md:82
derrida.md:115
engagement-madhusudana__bhakti-rasayana.md:23,111
engagement-madhva__mayavada-khandana.md:81
gebser.md:128,158,374,422,506
hegel.md:312,438
heidegger.md:515,533
husserl.md:435
kala-cakra-clock-structures.md:686
kc-bhattacharyya.md:244
kcb-kantian-perspectivism.md:316
leibniz.md:418
madhva.md:401,559
mcgilchrist.md:352,360
medhananda.md:119,141,295,501
mimamsa-aurobindo-v2.md:98
prigogine.md:315
primitive-model.md:73
ramanuja.md:99,389,479
samkhya-anirban.md:544
shankara.md:396,416,430,442,605,661
spinoza.md:565
vedanta-realist-history.md:248
vivekananda-ramakrishna.md:147
```

`indeed`

```text
chaudhuri-banerji.md:143,442,571
derrida.md:151
engagement-madhusudana__bhakti-rasayana.md:109
engagement-madhva__brahma-sutra-bhasya.md:96
engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha.md:84,128,140
engagement-raghavendra__tantra-dipika.md:139
engagement-vidyaranya__vivarana-prameya-sangraha.md:85,97
engagement-yamuna__agama-pramanya.md:39
gebser.md:546
hegel.md:171
heidegger.md:234
husserl.md:157,293
kala-cakra-clock-structures.md:360
kcb-kantian-perspectivism.md:307,383
mimamsa-aurobindo-v4.md:210
nietzsche.md:254
shankara.md:335,655
spinoza.md:266,424
vivekananda-ramakrishna.md:214,378
```

`thus`

```text
adorno.md:228,246,284
bergson.md:90
caitanya.md:121
chaudhuri-banerji.md:115,373,460,480,679
deleuze.md:188
derrida.md:207
engagement-madhva__bhagavata-tatparya-nirnaya.md:111
engagement-madhva__mayavada-khandana.md:23,31,49
engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha.md:51,100
engagement-raghavendra__nyaya-sudha-parimala.md:68,146,160
engagement-raghavendra__tantra-dipika.md:61
engagement-vedanta-desika__pancaratra-raksha.md:19,73,79
engagement-vijnanabhiksu__vijnanamrta-bhasya.md:49
foucault.md:258,400
gebser.md:108,382
hegel-preface.md:64,188
hegel.md:124,224,238,259,330,457
heidegger.md:168,408
kc-bhattacharyya.md:89,101,182,214,265,398,418
kala-cakra-clock-structures.md:374
leibniz.md:95,137,255
levinas.md:456,485
mcgilchrist.md:130,464
medhananda.md:95,97
mimamsa-aurobindo-v2.md:124
nietzsche.md:17,28,29,101,327,553,555,557,559,563,565,573,598,617,625,643,645,653,655,657
prigogine.md:167
ramanuja.md:449
samkhya-anirban.md:155
shankara.md:253
spinoza.md:499
vedanta-realist-history.md:135,275,897
vivekananda-ramakrishna.md:214,420
whitehead.md:297,311,374
```

`represents`

```text
bergson.md:262
chaudhuri-banerji.md:165,599,687
foucault.md:102,106,258
hegel.md:457
heidegger.md:234
leibniz.md:123,129,143,255,257
levinas.md:206
prigogine.md:118
```

## Heuristic Class 1: `rule-of-three`

Regex count: 1195.

This class is too broad to use raw. Most hits are harmless lists. The lines below are the full regex matches by file-line, grouped to keep the report readable.

```text
adorno.md: 3,23,198,246,260,266,306,320,360,368,396,412
aurobindo.md: 3,13,31,45,132,150,166,203,226,347,357,370,387,389,442,468,515,524,545,555,586,675,677,679,701,707,717,721,737,781,797,809,811,813,815,819
bergson.md: 15,35,126,208,244,250,274,278,321,355,363,365,383,389,443,451,459
caitanya.md: 9,11,15,19,23,55,61,73,119,137,151,153,163,169,171,201,203,217,259,381,463,519,547,591,609,617,619,627,633
chaudhuri-banerji.md: 3,13,17,95,99,125,206,214,218,250,256,266,270,327,363,438,488,552,587,659,669,675,679,798,808,821,899,903,911
comparative-claims-framework.md: 5,61,159
deleuze.md: 3,11,19,38,123,135,163,268,275,411,434,517,530,591,632,651,663,673,730,762,785
derrida.md: 13,17,23,27,53,73,77,91,103,107,155,161,171,223,237,260,304,340,352,354,356,394,402,414
engagement-madhusudana__bhakti-rasayana.md: 5,9,13,17,19,23,84,124,126,131,134
engagement-madhva__bhagavata-tatparya-nirnaya.md: 5,9,13,17,19,23,27,33,35,85,89,125,129,149,159,163,167
engagement-madhva__brahma-sutra-bhasya.md: 5,9,13,17,19,34,46,74,98,102,104,110,112
engagement-madhva__mayavada-khandana.md: 9,25,27,29,49,71,93,111,113
engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha.md: 15,17,19,21,88,138,140,147
engagement-raghavendra__nyaya-sudha-parimala.md: 5,9,15,17,29,31,37,39,41,47,49,51,116,150,154,156,158,160
engagement-raghavendra__tantra-dipika.md: 5,13,19,23,27,29,63,117,131,137,141,143,145,151
engagement-ramanuja__sri-bhasya.md: 5,13,15,17,21,23,25,27,29,35,37,39,65,103,113,121
engagement-vallabha__anu-bhasya.md: 13,15,17,19,67,81,99,101,107,109
engagement-vedanta-desika__pancaratra-raksha.md: 9,11,13,19,25,31,33,35,43,53,57,63,65,89,91,95,97,105
engagement-vidyaranya__vivarana-prameya-sangraha.md: 5,9,11,19,21,23,25,27,37,77,87,93
engagement-vijnanabhiksu__vijnanamrta-bhasya.md: 17,21,25,27,29,31,33,35,37,39,118,120,124,126
engagement-vijnanabhiksu__yoga-varttika.md: 5,9,13,15,17,19,21,45,60,84,92,96,104
engagement-yamuna__agama-pramanya.md: 5,9,13,25,27,53,55,79,83,85,89,93,97
foucault.md: 5,15,19,27,31,33,39,47,49,52,126,128,144,150,178,184,202,206,238,260,272,276,326,356,366,378,380,398,400,412,423,449,461,465,467,473,483,489,497,511,517
gebser.md: 27,29,33,42,70,90,132,180,192,212,222,226,262,264,288,337,374,382,453,461,471,498,530,538,567,599,712
hegel-preface.md: 58,68,100,114,178,188,200,204,248,270,284,286,296,310
hegel.md: 11,15,31,48,111,115,191,197,213,235,238,241,259,306,308,332,334,399,432,434,436,455,481,483,522,532,548,550,552,596
heidegger.md: 3,128,142,144,148,160,168,178,188,192,196,250,270,330,340,386,392,414,416,440,446,450,472,480,490,541,549,557,571
husserl.md: 11,57,67,127,133,187,223,239,251,259,261,285,299,305,307,315,319,321,325,329,331,367,377,391,399,415,417,421,427,453,463,471,475,481,487,489,497,499,501
kala-cakra-clock-structures.md: 3,68,190,224,238,244,272,274,276,296,354,398,402,404,408,412,414,416,420,434,436,468,484,506,510,530,541,552,598,602,626,644,704,768
kc-bhattacharyya.md: 5,11,15,23,38,45,105,121,128,136,170,182,236,257,303,343,359,366,382,472,498,541,551,559,561
kcb-kantian-perspectivism.md: 1,11,13,25,29,30,36,45,126,136,171,182,198,210,242,243,257,268,305,321,405,500,504,517
leibniz.md: 11,19,23,25,35,47,51,53,59,91,93,97,131,133,153,207,215,237,239,265,267,309,351,436,446,476,490,492,518,536,566,593
levinas.md: 11,25,72,108,116,126,192,266,336,420,429,465,500
madhva.md: 9,11,13,72,78,79,91,93,105,135,139,141,155,195,269,285,311,357,367,387,411,443,445,447,491,525,527,539,543,553,557,589
mcgilchrist.md: 15,23,47,59,61,75,77,79,98,100,102,130,134,144,158,170,172,182,186,196,202,208,212,238,246,256,258,270,278,284,290,294,296,302,304,322,350,354,376,388,416,420,434,436,464,494,496,498,500,502,508,514,524,526,530,532,536,551,553,555,559,563,567,571,575,577,579,581,583,585,589
medhananda.md: 3,5,13,17,33,63,69,87,105,109,119,127,135,181,187,201,233,251,257,267,271,283,299,333,343,355,359,367,371,377,407,415,419,421,451,465,477,485,534,536,558
mimamsa-aurobindo-v1.md: 33,47,53,55,67,117,201,205,221
mimamsa-aurobindo-v2.md: 37,45,68,93,98,126,140,142,211
mimamsa-aurobindo-v3.md: 13,33,48,50,52,70,76,84,86,120
mimamsa-aurobindo-v4.md: 5,17,23,35,41,56,58,60,76,80,84,96,104,108,118,130,144,146,172,174,194,212,231,232,243
nietzsche.md: 19,39,75,137,171,199,216,280,282,290,347,353,363,377,402,505,517,555,573,582,590,609,625,665,693,719,755
prigogine.md: 13,17,21,23,25,31,35,37,43,51,72,76,82,84,100,104,116,124,132,136,143,151,155,169,175,177,181,189,209,216,222,228,252,271,273,295,297,299,307,315,323,345
primitive-model.md: 74,192
ramanuja.md: 3,11,15,23,43,51,53,57,83,105,127,161,215,235,271,287,295,301,307,365,367,371,379,385,393,399,407,409,417,419,449,457,463,533,565,573,577,579,595
samkhya-anirban.md: 3,15,61,63,79,85,109,117,123,125,145,147,175,177,185,215,229,249,259,301,311,403,409,433,441,477,520,538,586,625,643,669,671,675
shankara.md: 9,11,51,81,93,181,183,187,247,345,383,527,539,605,617,638,645,653,657,671,681,689,697,707,731,772,783,805,821,853
spinoza.md: 3,11,13,21,55,59,61,188,194,296,302,348,424,451,517,551,561,589,607,615,617,627
vedanta-realist-history.md: 7,13,21,23,29,31,33,54,58,64,80,82,88,115,117,119,123,164,182,205,221,236,250,273,277,281,316,322,324,326,328,363,413,436,470,478,496,532,534,538,544,554,564,584,586,588,595,599,629,641,667,671,675,703,719,721,727,735,741,762,770,794,812,861,863,871,875,877,881,887,897,909,923,927,929
vivekananda-ramakrishna.md: 27,29,85,91,99,123,139,159,181,234,266,294,312,326,336,346,364,420,434,446,474,490,512,633,713,769,771,773,789
whitehead.md: 20,22,24,36,64,81,97,121,125,127,129,139,149,163,219,283,289,320,335,353,399,403,411,429,431,453,469,473,485,489,491,493,495
```

Worst concentration by style, not raw count:

- `aurobindo.md`
- `caitanya.md`
- `vedanta-realist-history.md`
- `whitehead.md`
- `mcgilchrist.md`
- `vivekananda-ramakrishna.md`

## Heuristic Class 2: `triple-pile`

Regex count: 1065.

Again: many false positives, but this regex catches a real tonal habit in the corpus.

```text
adorno.md: 19,31,35,36,137,210,232,242,260,270,296,306,320,336,354,360,388,396,420
aurobindo.md: 29,31,45,76,132,150,163,176,203,215,241,295,357,361,370,372,399,401,468,474,480,492,495,524,534,545,555,557,629,667,675,694,707,735,737,747,777,781,789,791,819
bergson.md: 35,56,58,64,68,146,154,206,222,230,244,250,262,270,272,274,276,278,282,298,321,327,363,373,381,383,407,443,451,459
caitanya.md: 19,153,171,201,203,259,369,381,453,531,609,617,627
chaudhuri-banerji.md: 3,13,17,51,57,95,99,125,143,147,167,206,214,242,256,266,268,270,349,357,363,373,431,571,625,635,675,693,725,778,784,821,833,835,879,889,911
comparative-claims-framework.md: 46,61,96
deleuze.md: 3,11,29,43,51,123,135,163,221,253,268,275,284,300,341,345,377,427,459,461,468,481,517,549,551,675,680,687,695,699,730,738,752
derrida.md: 11,23,29,33,53,95,99,103,123,131,143,157,171,177,193,201,205,207,221,223,229,237,239,249,254,266,286,304,316,326,346,352,354,356,396
engagement-madhusudana__bhakti-rasayana.md: 19,86,126
engagement-madhva__bhagavata-tatparya-nirnaya.md: 9,19,23,27,35,125,149,159,163
engagement-madhva__brahma-sutra-bhasya.md: 13,19,46,74,102,110
engagement-madhva__mayavada-khandana.md: 91
engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha.md: 17,19,138,140
engagement-raghavendra__nyaya-sudha-parimala.md: 5,9,27,29,31,45,116,150,158,160
engagement-raghavendra__tantra-dipika.md: 19,27,29,31,63,81,131,145
engagement-ramanuja__sri-bhasya.md: 5,15,21,23,25,27,37,113
engagement-vallabha__anu-bhasya.md: 15,101,103,107
engagement-vedanta-desika__pancaratra-raksha.md: 11,19,35,53,63,65,89,99
engagement-vidyaranya__vivarana-prameya-sangraha.md: 25,77,93
engagement-vijnanabhiksu__vijnanamrta-bhasya.md: 17,25,35,39,49,100,112,118,120,124
engagement-vijnanabhiksu__yoga-varttika.md: 5,17,45,60,96,106
engagement-yamuna__agama-pramanya.md: 53,79,83,85,87,89,97
foucault.md: 13,19,33,35,39,47,48,49,52,64,78,118,126,144,150,176,202,206,208,240,246,260,266,272,276,288,294,318,326,332,352,356,370,372,378,380,398,400,408,410,418,423,451,465,469,473,479,481,517
gebser.md: 23,27,42,70,123,130,132,160,168,178,188,212,226,257,262,264,267,303,309,337,347,374,392,398,453,471,496,498,518,530,534,550,567,579,595,712
hegel-preface.md: 58,178,184,188,210,226,248,264,270,296
hegel.md: 15,38,48,53,69,80,134,168,171,187,191,197,241,243,258,264,272,274,278,289,308,332,334,356,380,385,408,428,434,436,442,457,477,499,604,606
heidegger.md: 17,48,54,98,142,144,160,162,174,188,280,286,290,300,314,340,372,410,416,418,428,440,446,450,458,466,480,498,513,543,545,547,571
husserl.md: 9,11,27,67,75,91,111,133,137,147,239,259,263,281,305,307,319,321,325,329,351,357,367,377,403,415,417,421,433,453,463,473,475,481,487,489,493,497,499,501
kala-cakra-clock-structures.md: 29,68,96,126,224,274,402,404,406,412,414,416,420,434,468,530,541,592,598,610,626,632,658,660,734,776
kc-bhattacharyya.md: 11,15,23,38,45,59,85,105,121,144,182,230,273,303,426,476,482,551,559
kcb-kantian-perspectivism.md: 11,14,19,25,36,45,91,126,171,176,182,210,242,243,257,298,321,405,412,421,465,500
leibniz.md: 11,23,25,53,91,93,101,137,149,153,257,265,267,309,416,436,454,458,490,492,526,560
levinas.md: 11,17,19,29,31,108,116,126,162,192,198,202,262,266,270,282,336,352,356,364,404,418,420,429,465,487,500,502,503,505,509,537
madhva.md: 11,50,58,91,111,125,233,269,343,367,443,445,447,469,485,517,525,531,543
mcgilchrist.md: 13,25,47,55,59,61,75,77,81,90,91,92,100,102,130,132,134,158,172,182,196,202,206,208,210,212,238,256,258,262,264,270,272,276,278,284,288,290,294,296,302,304,306,310,322,326,350,354,358,388,416,418,420,422,434,436,494,498,500,502,524,526,530,532,536,551,559,563,567,569,571,575,577,581,583,585,589
medhananda.md: 13,17,33,69,83,87,127,187,201,207,219,233,243,251,257,267,333,359,367,371,377,409,423,451,453,465,477,534,536
mimamsa-aurobindo-v1.md: 47,53,59,98,137,205,209,211
mimamsa-aurobindo-v2.md: 37,41,68,110,126,140,142,211
mimamsa-aurobindo-v3.md: 13,50,84,86
mimamsa-aurobindo-v4.md: 35,58,76,80,104,108,118,144,146,172,174,196,212,216,232
nietzsche.md: 3,39,75,91,101,177,234,282,302,347,424,432,440,475,517,553,555,557,563,665,693,719,851
prigogine.md: 11,17,21,23,25,35,37,43,58,63,76,80,92,100,104,112,116,132,134,136,147,161,183,207,209,216,228,250,252,265,269,273,277,295,297,299,335
primitive-model.md: 126
ramanuja.md: 3,53,127,171,199,253,261,271,287,295,325,339,355,365,393,397,399,409,419,431,449,455,463,479,529,579,595
samkhya-anirban.md: 15,61,63,75,79,123,125,177,185,229,271,350,371,409,433,457,499,538,566,572,643,669
shankara.md: 73,126,162,187,206,247,349,367,505,527,569,636,638,653,655,663,673,681,689,697,699,731,750,791,815,843,853
spinoza.md: 11,13,21,59,61,156,160,162,166,252,270,362,424,451,517,551,585,587,595,615,627,649
vedanta-realist-history.md: 13,19,29,31,42,54,64,66,78,82,88,117,164,182,205,398,413,436,478,532,534,554,564,584,588,595,599,629,671,731,735,741,762,794,809,812,863,877,881,891,897,907,915,927
vivekananda-ramakrishna.md: 27,29,37,52,54,58,85,91,99,153,159,171,244,260,294,340,364,414,446,490,512,534,605,633,648,715,723,771,781
whitehead.md: 20,30,36,46,64,68,85,87,89,91,93,99,121,125,127,139,149,155,157,163,176,182,253,276,283,289,305,320,329,333,335,343,351,353,363,369,377,391,393,403,409,411,453,459,471,473,485,489,491,495
```

Most obvious offenders by file:

- `aurobindo.md`
- `deleuze.md`
- `whitehead.md`
- `vivekananda-ramakrishna.md`
- `caitanya.md`
- `chaudhuri-banerji.md`

## Priority Rewrite Set

These thirty lines are the first pass. They are all prose written for the site, not primary-text quotations.

1. `whitehead.md:283`
   Replace with: `The homology will be tested in Parts V and VI. For now, the basic architecture of *Process and Reality* is on the table: the Category of the Ultimate, the categories of existence and explanation, the categoreal obligations, actual entities, prehensions, epochal time, and God's two natures.`
2. `whitehead.md:333`
   Replace with: `Whitehead's politics, like his metaphysics, is aesthetic. Civilization advances as persuasion displaces force as the normal means of coordination.`
3. `heidegger.md:196`
   Replace with: `The user's reading of *Sein und Zeit* is direct. The book is one of the major works of twentieth-century philosophy.`
4. `heidegger.md:202`
   Replace with: `He does not describe the *Kehre* as a new doctrine. He describes it as the turn of the question at the point where the language of *Sein und Zeit* failed.`
5. `leibniz.md:15`
   Replace with: `- the *Discours de métaphysique* of 1686, sent to Antoine Arnauld through the Landgrave Ernst von Hessen-Rheinfels, together with the correspondence that ran from 1686 to 1690;`
6. `prigogine.md:82`
   Replace with: `Prigogine rejects that solution. The opening chapter sets out his alternative: irreversibility is a physical feature of the world, and twentieth-century physics must give it a formal place.`
7. `vivekananda-ramakrishna.md:147`
   Replace with: `The user's T1 and T4 receive a clear Ramakrishna statement in the elephant parable.`
8. `caitanya.md:421`
   Replace with: `The objection-thread of the *adhikaraṇa* is sharp: if Brahman is *avikārin* and *niravayava*, how can it be a cause?`
9. `husserl.md:293`
   Replace with: `The *Krisis* diagnoses a crisis of meaning. The sciences succeed in their own domain, but the meaning-ground from which they arose has dropped from view.`
10. `ramanuja.md:99`
    Replace with: `The Advaitin then retreats to "*vyāvahārika* concealment." But the whole point of the system is that the empirical level is itself the product of *avidyā*.`
11. `ramanuja.md:389`
    Replace with: `The verse is famous for its asymmetry — "all in Me, I not in them" — and each major commentator reads that asymmetry in the key of his own school.`
12. `ramanuja.md:479`
    Replace with: `For Śaṅkara, *bheda* is *vyāvahārika*; for Rāmānuja, it is real as qualification of Brahman.`
13. `madhva.md:401`
    Replace with: `The *Anuvyākhyāna* gives a dense line at 1.1.9: *oṃ* names the fullness of divine qualities, and the word *brahma* points to that same being named by *Nārāyaṇa*.`
14. `madhva.md:557`
    Replace with: `This is a striking concession on the `bhāvarūpa` point, but in the opposite direction from Madhusūdana's.`
15. `madhva.md:559`
    Replace with: `The implications are sharp. Jayatīrtha gives `avidyā` positive status, but places it in a real dependent substance under Viṣṇu's control rather than in Brahman.`
16. `aurobindo.md:495`
    Replace with: `The phrase "give oneself entirely to the Divine alone" states the position's account of total surrender. The framing is positive: surrender receives fullness, not privation.`
17. `aurobindo.md:497`
    Replace with: `The yogi does not *do* the yoga; the Mother works through the surrendered yogi.`
18. `aurobindo.md:499`
    Replace with: `Aurobindo's "Three Results" of *niṣkāma karma* complete the architecture. The actor is freed from ego-bondage, action is universalized, and the supracosmic Divine is known as the sole doer.`
19. `aurobindo.md:364`
    Replace with: `Read literally, this is a claim about the earth's cosmic history and the fate of embodied life, not an allegory of an inner ascent that leaves the world untouched.`
20. `aurobindo.md:366`
    Replace with: `The supramental does not require exit from the body. It requires the body's transformation from within.`
21. `deleuze.md:82`
    Replace with: `The structural fit with the position is close: one Real, many true registers, no genus under which those registers become mere species.`
22. `derrida.md:115`
    Replace with: `Derrida then cites Peirce as having moved far toward what he calls the deconstruction of the transcendental signified.`
23. `bergson.md:262`
    Replace with: `For Bergson, static religion answers a crisis generated by intellect itself: the mind projects death, delay, and alternative action, and fabulation counteracts that threat to cohesion.`
24. `chaudhuri-banerji.md:161`
    Replace with: `Two opponents structure the claim: Śaṅkarite dissolution into the One and impersonal universalism of the Hegelian or Deleuzean sort.`
25. `prigogine.md:118`
    Replace with: `For the generic case, Prigogine argues, one can construct a mathematically rigorous description that is intrinsically irreversible.`
26. `gebser.md:374`
    Replace with: `Gebser supplies the needed distinction. If the claim is that each *darśana* is true in its own register without a master-register above them, the relevant term is *synairesis*, not synthesis.`
27. `gebser.md:422`
    Replace with: `This is the user's T4 in Gebser's terms: each *darśana* is a real register of a larger whole, and none is licensed to absorb the rest.`
28. `kc-bhattacharyya.md:244`
    Replace with: `The first line marks the decisive point: many truths may still be reducible; alternative truths are not.`
29. `kala-cakra-clock-structures.md:686`
    Replace with: `T4 appears here as a cross-school compatibility claim: Sāṃkhya and the *kāla-cakra* materials can be read as compositional and temporal complements.`
30. `leibniz.md:418`
    Replace with: `The position also requires a stronger compossibility doctrine than Leibniz's: not only many possible worlds, but many true registers within one world.`

## First Targets by File

- `aurobindo.md`: 495, 497, 499, 364, 366
- `whitehead.md`: 283, 333
- `heidegger.md`: 196, 202
- `ramanuja.md`: 99, 389, 479
- `madhva.md`: 401, 557, 559
- `deleuze.md`: 82
- `derrida.md`: 115
- `bergson.md`: 262
- `gebser.md`: 374, 422
- `leibniz.md`: 15, 418

This set is enough to remove the most visible throat-clearing, adverbial inflation, and stock closure language from the worst lines without yet doing a line edit sweep of the whole corpus.
