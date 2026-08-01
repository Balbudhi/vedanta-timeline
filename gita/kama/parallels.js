/* =============================================================
   Bhagavad-Gītā 3.36–43 — "Across traditions" parallels.
   window.GITA3_PARALLELS — keyed by verse locus.
   Schema + policy: docs/SANSKRIT_TRANSLATION_STANDARD.md; design note
   gita/sthitaprajna/_build/DESIGN.md ("Across traditions", "Commentary
   vs. parallel").

   These are not Gītā commentary — no Buddhist or Jain author wrote on
   this passage. Each entry is a separate text in another tradition that
   speaks to this exact theme (kāma/krodha as one enemy arising from
   rajas; desire veiling knowledge; the graded hierarchy of indriya,
   manas, buddhi, and what stands beyond; the injunction to restrain and
   overcome), presented as a thematic parallel, attributed, never
   derived from the Gītā, and mapped to the verse it most closely
   illuminates. No forced matches: entries are included only where a
   tradition genuinely addresses this theme, not for coverage's own sake.

   Every `sanskrit` field (Sanskrit, Pali-cognate Prakrit) is verbatim
   from the cited on-disk source, in its own orthography and its own
   punctuation convention (Sanskrit daṇḍa | / ||; the Uttarajjhayana
   GRETIL file's own | / // marks) — only the file's internal citation
   apparatus (e.g. "ys_2.7", "kau_3.3/1,3.3", verse numerals) is
   dropped, exactly as the sthitaprajna parallels.js does for Pali
   sutta/verse tags. `ourRendering` is a literal English translation by
   this project — no source's translation is reproduced.

   Entry shape (mirrors gita/sthitaprajna/parallels.js exactly):
     { school, thinker, work, locus,
       sanskrit:<verbatim>, ourRendering:<literal English>, source:<path>,
       words:[ … ], english:<slotted literal rendering> }
   ============================================================= */

window.GITA3_PARALLELS = {
  "3.37": [
    {
      "school": "Yoga (Pātañjala)",
      "thinker": "Patañjali",
      "work": "Yoga-sūtra",
      "locus": "2.3",
      "sanskrit": "avidyāsmitārāgadveṣābhiniveśāḥ kleśāḥ ||",
      "ourRendering": "Ignorance, I-am-ness, attraction, aversion, and clinging-to-life are the kleśas.",
      "source": "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.3)",
      "words": [
        {
          "i": 0,
          "iast": "avidyāsmitārāgadveṣābhiniveśāḥ",
          "gloss": "ignorance, I-am-ness, attraction, aversion, and clinging-to-life",
          "parts": [
            {
              "form": "avidyā",
              "gloss": "ignorance, not-knowing — the misapprehension of the transient, impure, painful and not-self as the eternal, pure, pleasant and self"
            },
            {
              "form": "asmitā",
              "gloss": "I-am-ness, egoity — the sense of identity between the seer and the instrument of seeing"
            },
            {
              "form": "rāga",
              "gloss": "attraction, the coloring that follows on pleasure"
            },
            {
              "form": "dveṣa",
              "gloss": "aversion, the recoil that follows on pain"
            },
            {
              "form": "abhiniveśa",
              "gloss": "clinging to life, the instinctive will to go on being"
            }
          ],
          "stem": "avidyā-asmitā-rāga-dveṣa-abhiniveśa",
          "root": "abhi-ni-√viś (tudādi, 6P, 'to enter into, to settle upon')",
          "affix": "su (prathamā bahuvacana)",
          "morph": "nom. pl. masc.",
          "karaka": "kartṛ (subject of the implied copula)",
          "compound": {
            "type": "dvandva (itaretara)",
            "vigraha": "avidyā ca asmitā ca rāgaś ca dveṣaś ca abhiniveśaś ca",
            "members": [
              "avidyā",
              "asmitā",
              "rāga",
              "dveṣa",
              "abhiniveśa"
            ]
          },
          "translatable": true
        },
        {
          "i": 1,
          "iast": "kleśāḥ",
          "gloss": "kleśa — the afflictions",
          "parts": [
            {
              "form": "√kliś",
              "gloss": "to torment, to trouble, to afflict"
            },
            {
              "form": "-a",
              "gloss": "(ghañ, the action-noun: 'the afflicting')"
            }
          ],
          "stem": "kleśa",
          "root": "√kliś (divādi, 4P / kryādi, 9U, 'to torment, to afflict')",
          "affix": "jas (prathamā bahuvacana)",
          "morph": "nom. pl. masc.",
          "karaka": "predicate nominative (of the implied copula)",
          "glossaryKey": "klesa",
          "translatable": false
        }
      ],
      "english": "{0:Ignorance, I-am-ness, attraction, aversion, and clinging-to-life} are {1:the kleśas}."
    },
    {
      "school": "Yoga (Pātañjala)",
      "thinker": "Patañjali",
      "work": "Yoga-sūtra",
      "locus": "2.7–2.8",
      "sanskrit": "sukhānuśayī rāgaḥ || duḥkhānuśayī dveṣaḥ ||",
      "ourRendering": "Rāga is that which follows upon pleasure; dveṣa is that which follows upon pain.",
      "source": "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.7–2.8)",
      "words": [
        {
          "i": 0,
          "iast": "sukhānuśayī",
          "gloss": "following upon pleasure, clinging in the wake of happiness",
          "parts": [
            {
              "form": "sukha",
              "gloss": "pleasure, ease, happiness"
            },
            {
              "form": "anu-√śī",
              "gloss": "to lie down after, to lie latent in the wake of"
            },
            {
              "form": "-in",
              "gloss": "(taddhita ini: 'the one who —')"
            }
          ],
          "stem": "sukha-anuśayin",
          "root": "anu-√śī (adādi, 2Ā, 'to lie down after, to lie latent upon')",
          "affix": "in (taddhita ini) + su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "attribute of rāgaḥ (predicate adjective)",
          "compound": {
            "type": "tatpuruṣa (upapada)",
            "vigraha": "sukham anuśete yaḥ saḥ",
            "members": [
              "sukha",
              "anuśayin"
            ]
          },
          "translatable": true
        },
        {
          "i": 1,
          "iast": "rāgaḥ",
          "gloss": "rāga — attraction, the coloring toward the pleasant",
          "parts": [
            {
              "form": "√rañj",
              "gloss": "to be dyed, to be colored, to be attached"
            },
            {
              "form": "-a",
              "gloss": "(ghañ, the action-noun: 'the coloring')"
            }
          ],
          "stem": "rāga",
          "root": "√rañj (raji rāge, bhvādi, 1U, 'to be dyed, to be attached')",
          "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "kartṛ (subject of the implied copula)",
          "glossaryKey": "raga",
          "translatable": false
        },
        {
          "i": 2,
          "iast": "duḥkhānuśayī",
          "gloss": "following upon pain, clinging in the wake of suffering",
          "parts": [
            {
              "form": "duḥkha",
              "gloss": "pain, suffering, sorrow"
            },
            {
              "form": "anu-√śī",
              "gloss": "to lie down after, to lie latent in the wake of"
            },
            {
              "form": "-in",
              "gloss": "(taddhita ini: 'the one who —')"
            }
          ],
          "stem": "duḥkha-anuśayin",
          "root": "anu-√śī (adādi, 2Ā, 'to lie down after, to lie latent upon')",
          "affix": "in (taddhita ini) + su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "attribute of dveṣaḥ (predicate adjective)",
          "compound": {
            "type": "tatpuruṣa (upapada)",
            "vigraha": "duḥkham anuśete yaḥ saḥ",
            "members": [
              "duḥkha",
              "anuśayin"
            ]
          },
          "glossaryKey": "duhkha",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "dveṣaḥ",
          "gloss": "dveṣa — aversion, the recoil from the painful",
          "parts": [
            {
              "form": "√dviṣ",
              "gloss": "to hate, to be hostile toward"
            },
            {
              "form": "-a",
              "gloss": "(ghañ, the action-noun: 'the recoiling')"
            }
          ],
          "stem": "dveṣa",
          "root": "√dviṣ (adādi, 2P, 'to hate, to feel aversion')",
          "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "kartṛ (subject of the implied copula)",
          "glossaryKey": "dvesa",
          "translatable": false
        }
      ],
      "english": "{1:Rāga} is {0:that which follows upon pleasure}; {3:dveṣa} is {2:that which follows upon pain}."
    },
    {
      "school": "Sāṅkhya",
      "thinker": "Īśvarakṛṣṇa",
      "work": "Sāṅkhya-kārikā",
      "locus": "13",
      "sanskrit": "sattvaṃ laghu prakāśakam iṣṭam upaṣṭambhakaṃ calaṃ ca rajaḥ | guru varaṇakam eva tamaḥ pradīpavac cārthato vṛttiḥ ||",
      "ourRendering": "Sattva is light and illuminating — so held; rajas is stimulating and mobile; tamas alone is heavy and enveloping — and, as to purpose, their functioning is like a lamp's.",
      "source": "data/sources/sanskrit/comparator/isvarakrsna_samkhya_karika.txt (sāṅkhya-kārikā 13)",
      "words": [
        {
          "i": 0,
          "iast": "sattvam",
          "gloss": "sattva — the guṇa of lucidity",
          "parts": [
            {
              "form": "sat",
              "gloss": "being, existing (present participle of √as)"
            },
            {
              "form": "-tva",
              "gloss": "(taddhita tva: abstract noun, 'the state of being')"
            }
          ],
          "stem": "sattva",
          "root": "√as (adādi, 2P, 'to be, to exist')",
          "affix": "tva (taddhita) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "kartṛ (subject of the implied copula)",
          "glossaryKey": "sattva",
          "translatable": false
        },
        {
          "i": 1,
          "iast": "laghu",
          "gloss": "light, buoyant",
          "parts": [
            {
              "form": "laghu",
              "gloss": "light, buoyant, quick"
            }
          ],
          "stem": "laghu",
          "root": null,
          "affix": "su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of sattvam",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "prakāśakam",
          "gloss": "illuminating",
          "parts": [
            {
              "form": "pra-",
              "gloss": "forth, fully"
            },
            {
              "form": "√kāś",
              "gloss": "to shine, to become manifest"
            },
            {
              "form": "-aka",
              "gloss": "(ṇvul, agentive: 'that which makes —')"
            }
          ],
          "stem": "prakāśaka",
          "root": "pra-√kāś (bhvādi, 1Ā, 'to shine, to become manifest')",
          "affix": "ṇvul (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of sattvam",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "iṣṭam",
          "gloss": "held to be, so regarded",
          "parts": [
            {
              "form": "√iṣ",
              "gloss": "to wish; (in this idiom) to hold, to deem"
            },
            {
              "form": "-ta",
              "gloss": "(kta, past passive participle: 'held to be —')"
            }
          ],
          "stem": "iṣṭa",
          "root": "√iṣ (tudādi, 6P, 'to wish, to hold as')",
          "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.; past passive participle",
          "karaka": "predicate adjective of sattvam, in apposition",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "upaṣṭambhakam",
          "gloss": "stimulating, that which props into motion",
          "parts": [
            {
              "form": "upa-",
              "gloss": "toward, up"
            },
            {
              "form": "√stambh",
              "gloss": "to prop up, to make firm; to incite"
            },
            {
              "form": "-aka",
              "gloss": "(ṇvul, agentive: 'that which —')"
            }
          ],
          "stem": "upaṣṭambhaka",
          "root": "upa-√stambh (kryādi, 9P, 'to prop up, to incite')",
          "affix": "ṇvul (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of rajaḥ",
          "translatable": true
        },
        {
          "i": 5,
          "iast": "calam",
          "gloss": "mobile, restless",
          "parts": [
            {
              "form": "√cal",
              "gloss": "to move, to stir, to shake"
            },
            {
              "form": "-a",
              "gloss": "(kṛt ac, adjectival: 'moving')"
            }
          ],
          "stem": "cala",
          "root": "√cal (bhvādi, 1P, 'to move, to stir, to shake')",
          "affix": "ac (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of rajaḥ",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "ca",
          "gloss": "and",
          "parts": [
            {
              "form": "ca",
              "gloss": "and (enclitic)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable conjunction",
          "karaka": "joins upaṣṭambhakam and calam",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "rajaḥ",
          "gloss": "rajas — the guṇa of motion and passion",
          "parts": [
            {
              "form": "√rañj",
              "gloss": "to be colored, to be excited, to be stirred"
            },
            {
              "form": "-as",
              "gloss": "(asun, the neuter noun ending)"
            }
          ],
          "stem": "rajas",
          "root": "√rañj (bhvādi, 1Ā, 'to be colored, to be excited, to be stirred')",
          "affix": "asun (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "kartṛ (subject of the implied copula, second clause)",
          "glossaryKey": "rajas",
          "translatable": false
        },
        {
          "i": 8,
          "iast": "guru",
          "gloss": "heavy",
          "parts": [
            {
              "form": "guru",
              "gloss": "heavy, weighty"
            }
          ],
          "stem": "guru",
          "root": null,
          "affix": "su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of tamaḥ",
          "translatable": true
        },
        {
          "i": 9,
          "iast": "varaṇakam",
          "gloss": "enveloping, obstructing",
          "parts": [
            {
              "form": "√vṛ",
              "gloss": "to cover, to obstruct, to veil"
            },
            {
              "form": "-aṇaka",
              "gloss": "(ṇvul, agentive: 'that which —')"
            }
          ],
          "stem": "varaṇaka",
          "root": "√vṛ (kryādi, 9U, 'to cover, to obstruct, to veil')",
          "affix": "ṇvul (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate adjective of tamaḥ",
          "translatable": true
        },
        {
          "i": 10,
          "iast": "eva",
          "gloss": "alone, indeed",
          "parts": [
            {
              "form": "eva",
              "gloss": "indeed, alone (restrictive)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable restrictive particle",
          "translatable": true
        },
        {
          "i": 11,
          "iast": "tamaḥ",
          "gloss": "tamas — the guṇa of dullness and inertia",
          "parts": [
            {
              "form": "√tam",
              "gloss": "to become faint, to lose energy, to be stupefied"
            },
            {
              "form": "-as",
              "gloss": "(asun, the neuter noun ending)"
            }
          ],
          "stem": "tamas",
          "root": "√tam (divādi, 4P, 'to become faint, to be stupefied')",
          "affix": "asun (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "kartṛ (subject of the implied copula, third clause)",
          "glossaryKey": "tamas",
          "translatable": false
        },
        {
          "i": 12,
          "iast": "pradīpavat",
          "gloss": "like a lamp",
          "parts": [
            {
              "form": "pra-",
              "gloss": "forth, fully"
            },
            {
              "form": "√dīp",
              "gloss": "to blaze, to flame, to shine"
            },
            {
              "form": "-a",
              "gloss": "(the noun-forming vowel: 'the blazing thing, the lamp')"
            },
            {
              "form": "-vat",
              "gloss": "(taddhita vati: 'like, in the manner of')"
            }
          ],
          "stem": "pradīpa-vat",
          "root": "pra-√dīp (divādi, 4Ā, 'to blaze, to flame, to shine')",
          "affix": "vati (taddhita)",
          "morph": "indeclinable (adverb of comparison)",
          "karaka": "upamāna (standard of comparison)",
          "translatable": true
        },
        {
          "i": 13,
          "iast": "ca",
          "gloss": "and",
          "parts": [
            {
              "form": "ca",
              "gloss": "and"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable conjunction",
          "translatable": true
        },
        {
          "i": 14,
          "iast": "arthataḥ",
          "gloss": "as to purpose, functionally",
          "parts": [
            {
              "form": "artha",
              "gloss": "purpose, aim, meaning"
            },
            {
              "form": "-tas",
              "gloss": "(taddhita tasil: 'with respect to —')"
            }
          ],
          "stem": "artha",
          "root": null,
          "affix": "tasil (taddhita)",
          "morph": "indeclinable, ablative-force adverb",
          "karaka": "adverbial ('with respect to purpose')",
          "translatable": true
        },
        {
          "i": 15,
          "iast": "vṛttiḥ",
          "gloss": "the functioning",
          "parts": [
            {
              "form": "√vṛt",
              "gloss": "to turn, to occur, to operate, to function"
            },
            {
              "form": "-ti",
              "gloss": "(ktin, feminine action-noun: 'the functioning')"
            }
          ],
          "stem": "vṛtti",
          "root": "√vṛt (bhvādi, 1Ā, 'to turn, to occur, to function')",
          "affix": "ktin (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. fem.",
          "karaka": "kartṛ (subject of the implied copula, in the comparison clause)",
          "translatable": true
        }
      ],
      "english": "{0:Sattva} is {1:light} and {2:illuminating} — {3:so held}; {7:rajas} is {4:stimulating} {6:and} {5:mobile}; {11:tamas} {10:alone} is {8:heavy} and {9:enveloping} — {13:and}, {14:as to purpose}, {15:their functioning} is {12:like a lamp's}."
    }
  ],
  "3.39": [
    {
      "school": "Jainism",
      "thinker": "Uttarādhyayana",
      "work": "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 23 Kesigoyamijjaṃ (Keśi–Gautama dialogue)",
      "locus": "23.48",
      "sanskrit": "bhavataṇhā layā vuttā | bhīmā bhīmaphalodayā / tam uddhiccā jahānāyaṃ | viharāmi jahāsuhaṃ //",
      "ourRendering": "The craving for continued existence is called a creeper — fearsome, its fruit's arising terrible. Having uprooted that, as I have learned, I fare at ease.",
      "source": "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 23.48)",
      "words": [
        {
          "i": 0,
          "iast": "bhavataṇhā",
          "gloss": "the craving for continued existence",
          "parts": [
            {
              "form": "bhava",
              "gloss": "becoming, worldly existence, continued existence in saṃsāra"
            },
            {
              "form": "taṇhā",
              "gloss": "craving, thirst (Skt tṛṣṇā)"
            }
          ],
          "stem": "bhava-taṇhā",
          "root": "√tṛṣ (Prakrit; Skt √tṛṣ, divādi, 4P, 'to thirst, to crave')",
          "affix": "-ā (nom. sg. fem., Prakrit ā-stem; Skt bhava-tṛṣṇā)",
          "morph": "Prakrit nom. sg. fem.",
          "karaka": "kartṛ of the passive vuttā ('is called')",
          "compound": {
            "type": "tatpuruṣa (ṣaṣṭhī)",
            "vigraha": "bhavassa taṇhā (Skt: bhavasya tṛṣṇā)",
            "members": [
              "bhava",
              "taṇhā"
            ]
          },
          "glossaryKey": "trsna",
          "translatable": true
        },
        {
          "i": 1,
          "iast": "layā",
          "gloss": "a creeper, a vine",
          "parts": [
            {
              "form": "layā",
              "gloss": "creeper, vine (Skt latā)"
            }
          ],
          "stem": "layā",
          "root": null,
          "affix": "-ā (nom. sg. fem.; Skt latā)",
          "morph": "Prakrit nom. sg. fem.",
          "karaka": "predicate nominative (of vuttā)",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "vuttā",
          "gloss": "is called, is said",
          "parts": [
            {
              "form": "√vac",
              "gloss": "to speak, to say, to call"
            },
            {
              "form": "-tā",
              "gloss": "(past passive participle; Skt uktā)"
            }
          ],
          "stem": null,
          "root": "√vac (Prakrit; Skt √vac, adādi, 2P, 'to speak, to call')",
          "affix": "-tā (past passive participle; Skt -uktā)",
          "morph": "Prakrit nom. sg. fem.; past passive participle",
          "karaka": "the verb (copula supplied); kartṛ bhavataṇhā",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "bhīmā",
          "gloss": "fearsome, terrible",
          "parts": [
            {
              "form": "√bhī",
              "gloss": "to fear, to be afraid"
            },
            {
              "form": "-ma",
              "gloss": "(kṛt: 'fearsome, terrible')"
            }
          ],
          "stem": "bhīma",
          "root": "√bhī (juhotyādi, 3P, 'to fear')",
          "affix": "-ā (nom. sg. fem.; Skt bhīmā)",
          "morph": "Prakrit nom. sg. fem.",
          "karaka": "attribute of layā",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "bhīmaphalodayā",
          "gloss": "whose fruit's arising is terrible",
          "parts": [
            {
              "form": "bhīma",
              "gloss": "fearsome, terrible"
            },
            {
              "form": "phala",
              "gloss": "fruit, result"
            },
            {
              "form": "ud-√i",
              "gloss": "to arise, to come forth"
            },
            {
              "form": "-a",
              "gloss": "(the action-noun ending: 'the arising')"
            }
          ],
          "stem": "bhīma-phala-udaya",
          "root": "ud-√i (adādi, 2P, 'to arise, to come forth')",
          "affix": "-ā (nom. sg. fem.)",
          "morph": "Prakrit nom. sg. fem.",
          "karaka": "attribute of layā",
          "compound": {
            "type": "bahuvrīhi",
            "vigraha": "bhīmaḥ phalasya udayo yasyāḥ sā (Skt: bhīmaḥ phalodayo yasyāḥ sā)",
            "members": [
              "bhīma",
              "phala",
              "udaya"
            ]
          },
          "translatable": true
        },
        {
          "i": 5,
          "iast": "tam",
          "gloss": "that (the creeper)",
          "parts": [
            {
              "form": "ta",
              "gloss": "that (Skt tad)"
            }
          ],
          "stem": "ta",
          "root": null,
          "affix": "-ṃ (acc. sg. fem.; Skt tām)",
          "morph": "Prakrit acc. sg. fem.",
          "karaka": "karman of uddhiccā",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "uddhiccā",
          "gloss": "having uprooted",
          "parts": [
            {
              "form": "ud-",
              "gloss": "up, out"
            },
            {
              "form": "√dhṛ",
              "gloss": "to hold; (with ud-) to lift up, to pull out, to uproot"
            },
            {
              "form": "-iccā",
              "gloss": "(absolutive: 'having —ed'; Skt -tvā/-ṛtya)"
            }
          ],
          "stem": null,
          "root": "ud-√dhṛ (Prakrit; Skt ud-√dhṛ, bhvādi, 1U, 'to lift up, to uproot')",
          "affix": "-iccā (Prakrit absolutive; Skt uddhṛtya)",
          "morph": "Prakrit absolutive",
          "karaka": "prior action of the same kartṛ as viharāmi",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "jahānāyaṃ",
          "gloss": "as it is known, as I have learned",
          "parts": [
            {
              "form": "jahā",
              "gloss": "as, in the manner that (Skt yathā)"
            },
            {
              "form": "nāya",
              "gloss": "known (Skt jñāta, past participle of √jñā)"
            }
          ],
          "stem": "jahā-nāya",
          "root": "√jñā (kryādi, 9U, 'to know')",
          "affix": "-ṃ (adverbial; Skt yathā-jñātam)",
          "morph": "Prakrit adverbial (Skt yathājñātam)",
          "translatable": true
        },
        {
          "i": 8,
          "iast": "viharāmi",
          "gloss": "I fare, I dwell (as a mendicant)",
          "parts": [
            {
              "form": "vi-",
              "gloss": "about, around"
            },
            {
              "form": "√hṛ",
              "gloss": "to carry; (with vi-) to move about, to fare"
            },
            {
              "form": "-āmi",
              "gloss": "(1st person singular present)"
            }
          ],
          "stem": null,
          "root": "vi-√hṛ (Prakrit; Skt vi-√hṛ, bhvādi, 1U, 'to move about, to fare')",
          "affix": "-āmi (Prakrit present, 1st sg.)",
          "morph": "Prakrit pres. 1st sg.",
          "karaka": "the verb; kartṛ 'I' (the muni)",
          "translatable": true
        },
        {
          "i": 9,
          "iast": "jahāsuhaṃ",
          "gloss": "at ease, as one pleases",
          "parts": [
            {
              "form": "jahā",
              "gloss": "as, in the manner that (Skt yathā)"
            },
            {
              "form": "suha",
              "gloss": "ease, happiness, pleasure (Skt sukha)"
            }
          ],
          "stem": "jahā-suha",
          "root": null,
          "affix": "-ṃ (adverbial; Skt yathāsukham)",
          "morph": "Prakrit adverbial (Skt yathāsukham)",
          "translatable": true
        }
      ],
      "english": "{1:A creeper} {2:is called} {0:the craving for continued existence} — {3:fearsome}, {4:whose fruit's arising is terrible}. {5:That} {6:having uprooted}, {7:as I have learned}, {8:I fare} {9:at ease}."
    }
  ],
  "3.41": [
    {
      "school": "Jainism",
      "thinker": "Uttarādhyayana",
      "work": "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 4 Asaṃkhaya",
      "locus": "4.12",
      "sanskrit": "rakkhijja kohaṃ viṇaejja māṇaṃ | māyaṃ na seve payahejja lohaṃ //",
      "ourRendering": "Let him restrain anger, let him dispel pride; let him not resort to deceit, let him abandon greed.",
      "source": "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 4.12)",
      "words": [
        {
          "i": 0,
          "iast": "rakkhijja",
          "gloss": "let him restrain, let him guard against",
          "parts": [
            {
              "form": "√rakkh",
              "gloss": "to guard, to protect, to keep watch over, to hold in check"
            },
            {
              "form": "-ijja",
              "gloss": "(optative, 3rd singular: 'let him —')"
            }
          ],
          "stem": null,
          "root": "√rakkh (Prakrit; Skt √rakṣ, bhvādi, 1P, 'to guard, to keep in check')",
          "affix": "-ijja (Prakrit optative, 3rd sg.; Skt rakṣet)",
          "morph": "Prakrit opt. 3rd sg.",
          "karaka": "the verb; kartṛ the monk (understood), karman kohaṃ",
          "translatable": true
        },
        {
          "i": 1,
          "iast": "kohaṃ",
          "gloss": "anger",
          "parts": [
            {
              "form": "√kroh",
              "gloss": "to be angry, to grow wroth"
            },
            {
              "form": "-a",
              "gloss": "(the action-noun ending: 'the being-angry')"
            }
          ],
          "stem": "koha",
          "root": "√kroh (Prakrit; Skt √krudh, divādi, 4P, 'to be angry')",
          "affix": "-ṃ (acc. sg.; Skt krodham)",
          "morph": "Prakrit acc. sg. masc.",
          "karaka": "karman of rakkhijja",
          "glossaryKey": "krodha",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "viṇaejja",
          "gloss": "let him dispel, let him remove",
          "parts": [
            {
              "form": "vi-",
              "gloss": "away, apart"
            },
            {
              "form": "√nī",
              "gloss": "to lead; (with vi-) to lead away, to discipline away"
            },
            {
              "form": "-ejja",
              "gloss": "(optative, 3rd singular: 'let him —')"
            }
          ],
          "stem": null,
          "root": "vi-√nī (Prakrit; Skt vi-√nī, bhvādi, 1U, 'to lead away, to remove')",
          "affix": "-ejja (Prakrit optative, 3rd sg.; Skt vinayet)",
          "morph": "Prakrit opt. 3rd sg.",
          "karaka": "the verb; karman māṇaṃ",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "māṇaṃ",
          "gloss": "pride",
          "parts": [
            {
              "form": "√man",
              "gloss": "to think; to esteem oneself, to be proud"
            },
            {
              "form": "-a",
              "gloss": "(the action-noun ending: 'the esteeming-oneself, pride')"
            }
          ],
          "stem": "māṇa",
          "root": "√man (Prakrit; Skt √man, divādi, 4Ā, 'to think, to esteem oneself')",
          "affix": "-ṃ (acc. sg.; Skt mānam)",
          "morph": "Prakrit acc. sg. masc.",
          "karaka": "karman of viṇaejja",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "māyaṃ",
          "gloss": "deceit",
          "parts": [
            {
              "form": "māyā",
              "gloss": "deceit, guile, illusion-making"
            }
          ],
          "stem": "māyā",
          "root": null,
          "affix": "-ṃ (acc. sg.; Skt māyām)",
          "morph": "Prakrit acc. sg. fem.",
          "karaka": "karman of seve",
          "translatable": true
        },
        {
          "i": 5,
          "iast": "na",
          "gloss": "not",
          "parts": [
            {
              "form": "na",
              "gloss": "not"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "Prakrit indeclinable (negation)",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "seve",
          "gloss": "let him resort to, let him practise",
          "parts": [
            {
              "form": "√sev",
              "gloss": "to resort to, to practise, to cultivate"
            },
            {
              "form": "-e",
              "gloss": "(optative, 3rd singular: 'let him —')"
            }
          ],
          "stem": null,
          "root": "√sev (Prakrit; Skt √sev, bhvādi, 1Ā, 'to resort to, to practise')",
          "affix": "-e (Prakrit optative, 3rd sg.; Skt sevet)",
          "morph": "Prakrit opt. 3rd sg.",
          "karaka": "the verb; karman māyaṃ",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "payahejja",
          "gloss": "let him abandon, let him cast off",
          "parts": [
            {
              "form": "pa-",
              "gloss": "forth, away (Skt pra-)"
            },
            {
              "form": "√hā",
              "gloss": "to leave, to abandon, to let go, to cast off"
            },
            {
              "form": "-ejja",
              "gloss": "(optative, 3rd singular: 'let him —')"
            }
          ],
          "stem": null,
          "root": "pa-√hā (Prakrit; Skt pra-√hā, juhotyādi, 3P, 'to abandon, to cast off')",
          "affix": "-ejja (Prakrit optative, 3rd sg.; Skt prajahyāt)",
          "morph": "Prakrit opt. 3rd sg.",
          "karaka": "the verb; karman lohaṃ",
          "note": "The same root and sense as BG 3.41's prajahi (pra-√hā, 'cast off') — this Prakrit optative is its verbal counterpart.",
          "translatable": true
        },
        {
          "i": 8,
          "iast": "lohaṃ",
          "gloss": "greed",
          "parts": [
            {
              "form": "√lubh",
              "gloss": "to covet, to desire greedily"
            },
            {
              "form": "-a",
              "gloss": "(the action-noun ending: 'the coveting, greed')"
            }
          ],
          "stem": "loha",
          "root": "√lubh (Prakrit; Skt √lubh, divādi, 4P, 'to covet, to be greedy')",
          "affix": "-ṃ (acc. sg.; Skt lobham)",
          "morph": "Prakrit acc. sg. masc.",
          "karaka": "karman of payahejja",
          "translatable": true
        }
      ],
      "english": "{0:Let him restrain} {1:anger}, {2:let him dispel} {3:pride}; {5:let him not} {6:resort to} {4:deceit}, {7:let him abandon} {8:greed}."
    }
  ],
  "3.42": [
    {
      "school": "Vedānta (Upaniṣadic)",
      "thinker": "Kaṭha Upaniṣad",
      "work": "Kaṭha Upaniṣad",
      "locus": "1.3.3",
      "sanskrit": "ātmānaṃ rathinaṃ viddhi śarīraṃ ratham eva tu / buddhiṃ tu sārathiṃ viddhi manaḥ pragraham eva ca //",
      "ourRendering": "Know the self as the chariot-rider, and the body, surely, as the chariot itself; know buddhi as the charioteer, and manas as the reins.",
      "source": "data/sources/sanskrit/vedic/katha_upanisad_sankara_bhasya_gretil.txt (Kaṭha Up. 1.3.3)",
      "words": [
        {
          "i": 0,
          "iast": "ātmānam",
          "gloss": "the self",
          "parts": [
            {
              "form": "ātman",
              "gloss": "the self, oneself"
            }
          ],
          "stem": "ātman",
          "root": null,
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "karman of viddhi",
          "glossaryKey": "atman",
          "translatable": true
        },
        {
          "i": 1,
          "iast": "rathinam",
          "gloss": "the possessor of the chariot, the rider",
          "parts": [
            {
              "form": "ratha",
              "gloss": "chariot"
            },
            {
              "form": "-in",
              "gloss": "(taddhita ini: 'the one who has —')"
            }
          ],
          "stem": "rathin",
          "root": null,
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "predicate accusative with viddhi",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "viddhi",
          "gloss": "know!",
          "parts": [
            {
              "form": "√vid",
              "gloss": "to know, to understand"
            },
            {
              "form": "-dhi",
              "gloss": "(hi, 2nd singular imperative)"
            }
          ],
          "stem": null,
          "root": "√vid (adādi, 2P, 'to know')",
          "affix": "hi (loṭ, madhyama-puruṣa ekavacana)",
          "morph": "2nd sg. imperative parasmaipada",
          "karaka": "the verb",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "śarīram",
          "gloss": "the body",
          "parts": [
            {
              "form": "śarīra",
              "gloss": "body"
            }
          ],
          "stem": "śarīra",
          "root": null,
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. neut.",
          "karaka": "karman of the same viddhi",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "ratham",
          "gloss": "the chariot",
          "parts": [
            {
              "form": "ratha",
              "gloss": "chariot"
            }
          ],
          "stem": "ratha",
          "root": null,
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "predicate accusative",
          "translatable": true
        },
        {
          "i": 5,
          "iast": "eva",
          "gloss": "indeed, surely",
          "parts": [
            {
              "form": "eva",
              "gloss": "indeed, precisely (restrictive)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable restrictive particle",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "tu",
          "gloss": "but, now",
          "parts": [
            {
              "form": "tu",
              "gloss": "but, now, however"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable adversative particle",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "buddhim",
          "gloss": "buddhi",
          "parts": [
            {
              "form": "√budh",
              "gloss": "to wake, to understand"
            },
            {
              "form": "-ti",
              "gloss": "(ktin, feminine action-noun)"
            }
          ],
          "stem": "buddhi",
          "root": "√budh (bhvādi, 1U, 'to wake, to understand')",
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. fem.",
          "karaka": "karman of viddhi (second occurrence)",
          "glossaryKey": "buddhi",
          "translatable": false
        },
        {
          "i": 8,
          "iast": "tu",
          "gloss": "but",
          "parts": [
            {
              "form": "tu",
              "gloss": "but, however"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable adversative particle",
          "translatable": true
        },
        {
          "i": 9,
          "iast": "sārathim",
          "gloss": "the charioteer",
          "parts": [
            {
              "form": "sa-rathi",
              "gloss": "one who goes with the chariot, the charioteer"
            }
          ],
          "stem": "sārathi",
          "root": null,
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "predicate accusative with viddhi",
          "translatable": true
        },
        {
          "i": 10,
          "iast": "viddhi",
          "gloss": "know!",
          "parts": [
            {
              "form": "√vid",
              "gloss": "to know, to understand"
            },
            {
              "form": "-dhi",
              "gloss": "(hi, 2nd singular imperative)"
            }
          ],
          "stem": null,
          "root": "√vid (adādi, 2P, 'to know')",
          "affix": "hi (loṭ, madhyama-puruṣa ekavacana)",
          "morph": "2nd sg. imperative parasmaipada",
          "karaka": "the verb (second occurrence)",
          "translatable": true
        },
        {
          "i": 11,
          "iast": "manaḥ",
          "gloss": "manas",
          "parts": [
            {
              "form": "√man",
              "gloss": "to think"
            },
            {
              "form": "-as",
              "gloss": "(asun, neuter noun ending)"
            }
          ],
          "stem": "manas",
          "root": "√man (divādi, 4Ā, 'to think')",
          "affix": "asun (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "kartṛ of the implied copula",
          "glossaryKey": "manas",
          "translatable": false
        },
        {
          "i": 12,
          "iast": "pragraham",
          "gloss": "the reins",
          "parts": [
            {
              "form": "pra-",
              "gloss": "forth"
            },
            {
              "form": "√grah",
              "gloss": "to seize, to grasp, to hold"
            },
            {
              "form": "-a",
              "gloss": "(the instrument-noun ending: 'that which grips')"
            }
          ],
          "stem": "pragraha",
          "root": "pra-√grah (kryādi, 9U, 'to seize, to hold')",
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "predicate accusative (understood viddhi)",
          "translatable": true
        },
        {
          "i": 13,
          "iast": "eva",
          "gloss": "indeed",
          "parts": [
            {
              "form": "eva",
              "gloss": "indeed (restrictive)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable restrictive particle",
          "translatable": true
        },
        {
          "i": 14,
          "iast": "ca",
          "gloss": "and",
          "parts": [
            {
              "form": "ca",
              "gloss": "and"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable conjunction",
          "translatable": true
        }
      ],
      "english": "{2:Know} {0:the self} {1:as the chariot-rider}; {3:the body}, {5:indeed}, {6:but}, as {4:the chariot}. {10:Know} {7:buddhi}, {8:but}, {9:as the charioteer}; {11:manas}, {13:indeed}, {14:and}, as {12:the reins}."
    },
    {
      "school": "Vedānta (Upaniṣadic)",
      "thinker": "Kaṭha Upaniṣad",
      "work": "Kaṭha Upaniṣad",
      "locus": "1.3.4",
      "sanskrit": "indriyāṇi hayān āhur viṣayāṃs teṣu gocarān / ātmendriyamanoyuktaṃ bhoktety āhur manīṣiṇaḥ //",
      "ourRendering": "The indriyas, they call horses; the objects, what they range over. The self joined with the indriyas and the mind — this the wise call 'the experiencer.'",
      "source": "data/sources/sanskrit/vedic/katha_upanisad_sankara_bhasya_gretil.txt (Kaṭha Up. 1.3.4)",
      "words": [
        {
          "i": 0,
          "iast": "indriyāṇi",
          "gloss": "the indriyas",
          "parts": [
            {
              "form": "indra",
              "gloss": "Indra, the ruling power"
            },
            {
              "form": "-iya",
              "gloss": "(taddhita: 'belonging to Indra')"
            }
          ],
          "stem": "indriya",
          "root": null,
          "affix": "śas (dvitīyā bahuvacana)",
          "morph": "acc. pl. neut.",
          "karaka": "karman of āhuḥ",
          "glossaryKey": "indriya",
          "translatable": false
        },
        {
          "i": 1,
          "iast": "hayān",
          "gloss": "horses",
          "parts": [
            {
              "form": "haya",
              "gloss": "horse"
            }
          ],
          "stem": "haya",
          "root": null,
          "affix": "as (dvitīyā bahuvacana)",
          "morph": "acc. pl. masc.",
          "karaka": "predicate accusative with āhuḥ",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "āhuḥ",
          "gloss": "they call",
          "parts": [
            {
              "form": "āha-",
              "gloss": "(the substitute stem prescribed for √brū in this ending)"
            },
            {
              "form": "-uḥ",
              "gloss": "(3rd person plural)"
            }
          ],
          "stem": null,
          "root": "√brū (adādi, 2U, 'to say, to call'; with the āha- substitute)",
          "affix": "jhi (laṭ, prathama-puruṣa bahuvacana)",
          "morph": "3rd pl. pres. indic.",
          "karaka": "the verb; kartṛ unnamed ('they', those who know)",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "viṣayān",
          "gloss": "the objects",
          "parts": [
            {
              "form": "vi-",
              "gloss": "apart, across"
            },
            {
              "form": "√si",
              "gloss": "to bind; the range a faculty covers"
            },
            {
              "form": "-aya",
              "gloss": "(the derivational ending: 'the domain')"
            }
          ],
          "stem": "viṣaya",
          "root": null,
          "affix": "as (dvitīyā bahuvacana)",
          "morph": "acc. pl. masc.",
          "karaka": "karman of the second, elided āhuḥ",
          "glossaryKey": "visaya",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "teṣu",
          "gloss": "among these (the indriyas)",
          "parts": [
            {
              "form": "tad",
              "gloss": "that (anaphoric)"
            }
          ],
          "stem": "tad",
          "root": null,
          "affix": "su (saptamī bahuvacana)",
          "morph": "loc. pl. masc.",
          "karaka": "adhikaraṇa (locus of ranging)",
          "translatable": true
        },
        {
          "i": 5,
          "iast": "gocarān",
          "gloss": "what they range over",
          "parts": [
            {
              "form": "go",
              "gloss": "cow; (here, by extension) the ranging faculty"
            },
            {
              "form": "√car",
              "gloss": "to move, to range, to graze"
            },
            {
              "form": "-a",
              "gloss": "(agent-noun ending: 'what is ranged over')"
            }
          ],
          "stem": "gocara",
          "root": "√car (bhvādi, 1P, 'to move, to range, to graze')",
          "affix": "as (dvitīyā bahuvacana)",
          "morph": "acc. pl. masc.",
          "karaka": "predicate accusative in apposition to viṣayān",
          "compound": {
            "type": "tatpuruṣa",
            "vigraha": "goḥ (indriyasya) caraḥ",
            "members": [
              "go",
              "cara"
            ]
          },
          "translatable": true
        },
        {
          "i": 6,
          "iast": "ātmendriyamanoyuktam",
          "gloss": "the self joined with the indriyas and the mind",
          "parts": [
            {
              "form": "ātman",
              "gloss": "the self"
            },
            {
              "form": "indriya",
              "gloss": "the senses"
            },
            {
              "form": "manas",
              "gloss": "the mind"
            },
            {
              "form": "√yuj",
              "gloss": "to join, to yoke"
            },
            {
              "form": "-ta",
              "gloss": "(kta, past passive participle: 'joined')"
            }
          ],
          "stem": "ātma-indriya-manas-yukta",
          "root": "√yuj (rudhādi, 7U, 'to join, to yoke')",
          "affix": "am (dvitīyā ekavacana)",
          "morph": "acc. sg. masc.",
          "karaka": "karman of the closing āhuḥ (the thing named 'experiencer')",
          "compound": {
            "type": "tatpuruṣa (with a dvandva first member)",
            "vigraha": "ātmā ca indriyāṇi ca manaś ca — tair yuktam",
            "members": [
              "ātman",
              "indriya",
              "manas",
              "yukta"
            ]
          },
          "translatable": true
        },
        {
          "i": 7,
          "iast": "bhoktā",
          "gloss": "the experiencer",
          "parts": [
            {
              "form": "√bhuj",
              "gloss": "to enjoy, to experience, to undergo"
            },
            {
              "form": "-tṛ",
              "gloss": "(tṛc, agentive: 'the one who —')"
            }
          ],
          "stem": "bhoktṛ",
          "root": "√bhuj (rudhādi, 7U, 'to enjoy, to experience')",
          "affix": "tṛc (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "predicate nominative, the name given to ātmendriyamanoyuktam",
          "note": "The verse gives bhoktā iti (by sandhi, bhoktety) as the quoted name.",
          "translatable": true
        },
        {
          "i": 8,
          "iast": "iti",
          "gloss": "thus (closing the quoted name)",
          "parts": [
            {
              "form": "iti",
              "gloss": "thus, so (quotative)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable quotative",
          "translatable": true
        },
        {
          "i": 9,
          "iast": "āhuḥ",
          "gloss": "they call",
          "parts": [
            {
              "form": "āha-",
              "gloss": "(the substitute stem prescribed for √brū in this ending)"
            },
            {
              "form": "-uḥ",
              "gloss": "(3rd person plural)"
            }
          ],
          "stem": null,
          "root": "√brū (adādi, 2U, 'to say, to call'; with the āha- substitute)",
          "affix": "jhi (laṭ, prathama-puruṣa bahuvacana)",
          "morph": "3rd pl. pres. indic.",
          "karaka": "the verb; kartṛ manīṣiṇaḥ",
          "translatable": true
        },
        {
          "i": 10,
          "iast": "manīṣiṇaḥ",
          "gloss": "the wise, the sagacious",
          "parts": [
            {
              "form": "manīṣā",
              "gloss": "reflection, wise consideration"
            },
            {
              "form": "-in",
              "gloss": "(taddhita ini: 'the one who has —')"
            }
          ],
          "stem": "manīṣin",
          "root": "√man (divādi, 4Ā, 'to think')",
          "affix": "in (taddhita) + as (prathamā bahuvacana)",
          "morph": "nom. pl. masc.",
          "karaka": "kartṛ of āhuḥ",
          "translatable": true
        }
      ],
      "english": "{2:They call} {0:the indriyas} {1:horses}; {3:the objects}, {5:what is ranged over} {4:among them}. {6:The self joined with the indriyas and the mind} — {10:the wise} {9:call} {8:thus}: {7:'the experiencer.'}"
    },
    {
      "school": "Vedānta (Upaniṣadic)",
      "thinker": "Kaṭha Upaniṣad",
      "work": "Kaṭha Upaniṣad",
      "locus": "1.3.10",
      "sanskrit": "indriyebhyaḥ parā hy arthā arthebhyaś ca paraṃ manaḥ / manasas tu parā buddhir buddher ātmā mahān paraḥ //",
      "ourRendering": "Higher, surely, than the indriyas are the objects; and higher than the objects is manas; but higher than manas is buddhi; higher than buddhi is the ātman, the great one, the higher.",
      "source": "data/sources/sanskrit/vedic/katha_upanisad_sankara_bhasya_gretil.txt (Kaṭha Up. 1.3.10)",
      "words": [
        {
          "i": 0,
          "iast": "indriyebhyaḥ",
          "gloss": "than the indriyas",
          "parts": [
            {
              "form": "indriya",
              "gloss": "the powers of sense and action"
            },
            {
              "form": "-bhyaḥ",
              "gloss": "(ablative plural: 'than')"
            }
          ],
          "stem": "indriya",
          "root": null,
          "affix": "bhyas (pañcamī bahuvacana)",
          "morph": "abl. pl. neut.",
          "karaka": "standard of comparison (ablative) with parāḥ",
          "glossaryKey": "indriya",
          "translatable": false
        },
        {
          "i": 1,
          "iast": "parāḥ",
          "gloss": "higher",
          "parts": [
            {
              "form": "para",
              "gloss": "higher, further, beyond"
            }
          ],
          "stem": "para",
          "root": null,
          "affix": "as (prathamā bahuvacana)",
          "morph": "nom. pl. masc.",
          "karaka": "predicate of arthāḥ",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "hi",
          "gloss": "surely, indeed",
          "parts": [
            {
              "form": "hi",
              "gloss": "for, surely, indeed"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable emphatic particle",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "arthāḥ",
          "gloss": "the objects",
          "parts": [
            {
              "form": "√arth",
              "gloss": "to seek, to aim at, to desire"
            },
            {
              "form": "-a",
              "gloss": "(the object-noun ending: 'the aimed-at thing, the object')"
            }
          ],
          "stem": "artha",
          "root": "√arth (curādi, 10U, 'to seek, to aim at')",
          "affix": "as (prathamā bahuvacana)",
          "morph": "nom. pl. masc.",
          "karaka": "kartṛ of the implied copula",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "arthebhyaḥ",
          "gloss": "than the objects",
          "parts": [
            {
              "form": "artha",
              "gloss": "the object"
            },
            {
              "form": "-ebhyaḥ",
              "gloss": "(ablative plural: 'than')"
            }
          ],
          "stem": "artha",
          "root": null,
          "affix": "bhyas (pañcamī bahuvacana)",
          "morph": "abl. pl. masc.",
          "karaka": "standard of comparison (ablative) with param",
          "translatable": true
        },
        {
          "i": 5,
          "iast": "ca",
          "gloss": "and",
          "parts": [
            {
              "form": "ca",
              "gloss": "and"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable conjunction",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "param",
          "gloss": "higher",
          "parts": [
            {
              "form": "para",
              "gloss": "higher, further, beyond"
            }
          ],
          "stem": "para",
          "root": null,
          "affix": "am (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "predicate of manaḥ",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "manaḥ",
          "gloss": "manas",
          "parts": [
            {
              "form": "√man",
              "gloss": "to think"
            },
            {
              "form": "-as",
              "gloss": "(asun, neuter noun ending)"
            }
          ],
          "stem": "manas",
          "root": "√man (divādi, 4Ā, 'to think')",
          "affix": "asun (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. neut.",
          "karaka": "kartṛ of the implied copula",
          "glossaryKey": "manas",
          "translatable": false
        },
        {
          "i": 8,
          "iast": "manasaḥ",
          "gloss": "than manas",
          "parts": [
            {
              "form": "√man",
              "gloss": "to think"
            },
            {
              "form": "-as",
              "gloss": "(asun, neuter noun ending)"
            },
            {
              "form": "-aḥ",
              "gloss": "(ablative singular: 'than')"
            }
          ],
          "stem": "manas",
          "root": "√man (divādi, 4Ā, 'to think')",
          "affix": "as (pañcamī ekavacana)",
          "morph": "abl. sg. neut.",
          "karaka": "standard of comparison (ablative) with parā",
          "glossaryKey": "manas",
          "translatable": false
        },
        {
          "i": 9,
          "iast": "tu",
          "gloss": "but",
          "parts": [
            {
              "form": "tu",
              "gloss": "but, however"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "indeclinable adversative particle",
          "translatable": true
        },
        {
          "i": 10,
          "iast": "parā",
          "gloss": "higher",
          "parts": [
            {
              "form": "para",
              "gloss": "higher, further, beyond"
            },
            {
              "form": "-ā",
              "gloss": "(feminine ending, agreeing with buddhi)"
            }
          ],
          "stem": "para",
          "root": null,
          "affix": "ā (prathamā ekavacana, strī)",
          "morph": "nom. sg. fem.",
          "karaka": "predicate of buddhiḥ",
          "translatable": true
        },
        {
          "i": 11,
          "iast": "buddhiḥ",
          "gloss": "buddhi",
          "parts": [
            {
              "form": "√budh",
              "gloss": "to wake, to understand"
            },
            {
              "form": "-ti",
              "gloss": "(ktin, feminine action-noun)"
            }
          ],
          "stem": "buddhi",
          "root": "√budh (bhvādi, 1U, 'to wake, to understand')",
          "affix": "ktin (kṛt) + su (prathamā ekavacana)",
          "morph": "nom. sg. fem.",
          "karaka": "kartṛ of the implied copula",
          "glossaryKey": "buddhi",
          "translatable": false
        },
        {
          "i": 12,
          "iast": "buddheḥ",
          "gloss": "than buddhi",
          "parts": [
            {
              "form": "√budh",
              "gloss": "to wake, to understand"
            },
            {
              "form": "-ti",
              "gloss": "(ktin, feminine action-noun)"
            },
            {
              "form": "-eḥ",
              "gloss": "(ablative singular: 'than')"
            }
          ],
          "stem": "buddhi",
          "root": "√budh (bhvādi, 1U, 'to wake, to understand')",
          "affix": "as (pañcamī ekavacana)",
          "morph": "abl. sg. fem.",
          "karaka": "standard of comparison (ablative) with paraḥ",
          "glossaryKey": "buddhi",
          "translatable": false
        },
        {
          "i": 13,
          "iast": "ātmā",
          "gloss": "the ātman, the self",
          "parts": [
            {
              "form": "ātman",
              "gloss": "the self"
            }
          ],
          "stem": "ātman",
          "root": null,
          "affix": "su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "kartṛ of the implied copula",
          "glossaryKey": "atman",
          "translatable": true
        },
        {
          "i": 14,
          "iast": "mahān",
          "gloss": "the great (one)",
          "parts": [
            {
              "form": "mahat",
              "gloss": "great, vast"
            }
          ],
          "stem": "mahat",
          "root": null,
          "affix": "su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "attribute of ātmā",
          "translatable": true
        },
        {
          "i": 15,
          "iast": "paraḥ",
          "gloss": "higher",
          "parts": [
            {
              "form": "para",
              "gloss": "higher, further, beyond"
            }
          ],
          "stem": "para",
          "root": null,
          "affix": "su (prathamā ekavacana)",
          "morph": "nom. sg. masc.",
          "karaka": "predicate of ātmā",
          "translatable": true
        }
      ],
      "english": "{1:Higher}, {2:surely}, {0:than the indriyas}, are {3:the objects}; {5:and}, {4:than the objects}, {6:higher} is {7:manas}; {9:but}, {8:than manas}, {10:higher} is {11:buddhi}; {12:than buddhi} is {13:the ātman}, {14:the great one}, {15:the higher}."
    }
  ],
  "3.43": [
    {
      "school": "Jainism",
      "thinker": "Uttarādhyayana",
      "work": "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 23 Kesigoyamijjaṃ (Keśi–Gautama dialogue)",
      "locus": "23.38",
      "sanskrit": "egappā ajie sattū | kasāyā indiyāṇi ya / te jiṇittu jahānāyaṃ | viharāmi ahaṃ muṇī //",
      "ourRendering": "One's own self, unconquered, is the enemy — the passions and the senses. Having conquered those, as I have learned, I, a sage, fare at ease.",
      "source": "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 23.38)",
      "words": [
        {
          "i": 0,
          "iast": "egappā",
          "gloss": "one's own self, the single self",
          "parts": [
            {
              "form": "ega",
              "gloss": "one, single, alone (Skt eka)"
            },
            {
              "form": "appā",
              "gloss": "self, soul (Skt ātman)"
            }
          ],
          "stem": "ega-appā",
          "root": null,
          "affix": "-ā (nom. sg. masc.; Skt ekātmā)",
          "morph": "Prakrit nom. sg. masc.",
          "karaka": "kartṛ of the implied copula",
          "compound": {
            "type": "karmadhāraya",
            "vigraha": "ekaś cāsāv ātmā ca (Skt: eka ātmā)",
            "members": [
              "ega",
              "appā"
            ]
          },
          "translatable": true
        },
        {
          "i": 1,
          "iast": "ajie",
          "gloss": "unconquered",
          "parts": [
            {
              "form": "a-",
              "gloss": "not (negative prefix)"
            },
            {
              "form": "√ji",
              "gloss": "to conquer, to win, to overcome"
            },
            {
              "form": "-ya",
              "gloss": "(past passive participle; Skt -ta)"
            }
          ],
          "stem": "ajiya",
          "root": "√ji (Prakrit; Skt √ji, bhvādi, 1P, 'to conquer')",
          "affix": "-e (nom. sg. masc.; Skt ajitaḥ)",
          "morph": "Prakrit nom. sg. masc.; past passive participle, negated",
          "karaka": "predicate of egappā",
          "translatable": true
        },
        {
          "i": 2,
          "iast": "sattū",
          "gloss": "the enemy",
          "parts": [
            {
              "form": "√sad",
              "gloss": "to fall, to perish"
            },
            {
              "form": "-tru",
              "gloss": "(uṇādi affix: 'the one who makes another fall')"
            }
          ],
          "stem": "sattu",
          "root": "√sad (Prakrit; Skt √śad, bhvādi, 1P, 'to fall away, to perish')",
          "affix": "-ū (nom. sg. masc.; Skt śatruḥ)",
          "morph": "Prakrit nom. sg. masc.",
          "karaka": "predicate nominative",
          "translatable": true
        },
        {
          "i": 3,
          "iast": "kasāyā",
          "gloss": "the passions",
          "parts": [
            {
              "form": "kasāya",
              "gloss": "the passions — anger, pride, deceit and greed (Skt kaṣāya, lit. 'tint, dye, astringent taste')"
            }
          ],
          "stem": "kasāya",
          "root": null,
          "affix": "-ā (nom. pl. masc.; Skt kaṣāyāḥ)",
          "morph": "Prakrit nom. pl. masc.",
          "karaka": "kartṛ, in apposition to sattū (naming what the enemy is)",
          "translatable": true
        },
        {
          "i": 4,
          "iast": "indiyāṇi",
          "gloss": "the senses",
          "parts": [
            {
              "form": "indiya",
              "gloss": "the powers of sense and action (Skt indriya)"
            }
          ],
          "stem": "indiya",
          "root": null,
          "affix": "-āṇi (nom. pl. neut.; Skt indriyāṇi)",
          "morph": "Prakrit nom. pl. neut.",
          "karaka": "kartṛ, in apposition to sattū, coordinate with kasāyā",
          "glossaryKey": "indriya",
          "translatable": false
        },
        {
          "i": 5,
          "iast": "ya",
          "gloss": "and",
          "parts": [
            {
              "form": "ya",
              "gloss": "and (Skt ca)"
            }
          ],
          "stem": null,
          "root": null,
          "affix": null,
          "morph": "Prakrit indeclinable (conjunction; Skt ca)",
          "translatable": true
        },
        {
          "i": 6,
          "iast": "te",
          "gloss": "those",
          "parts": [
            {
              "form": "ta",
              "gloss": "that (Skt tad)"
            }
          ],
          "stem": "ta",
          "root": null,
          "affix": "-e (acc. pl. masc.; Skt tān)",
          "morph": "Prakrit acc. pl. masc.",
          "karaka": "karman of jiṇittu",
          "translatable": true
        },
        {
          "i": 7,
          "iast": "jiṇittu",
          "gloss": "having conquered",
          "parts": [
            {
              "form": "√ji",
              "gloss": "to conquer, to overcome"
            },
            {
              "form": "-ittu",
              "gloss": "(absolutive: 'having —ed')"
            }
          ],
          "stem": null,
          "root": "√ji (Prakrit; Skt √ji, bhvādi, 1P, 'to conquer')",
          "affix": "-ittu (Prakrit absolutive; Skt jitvā)",
          "morph": "Prakrit absolutive",
          "karaka": "prior action of the same kartṛ as viharāmi",
          "translatable": true
        },
        {
          "i": 8,
          "iast": "jahānāyaṃ",
          "gloss": "as it is known, as I have learned",
          "parts": [
            {
              "form": "jahā",
              "gloss": "as, in the manner that (Skt yathā)"
            },
            {
              "form": "nāya",
              "gloss": "known (Skt jñāta, past participle of √jñā)"
            }
          ],
          "stem": "jahā-nāya",
          "root": "√jñā (kryādi, 9U, 'to know')",
          "affix": "-ṃ (adverbial; Skt yathā-jñātam)",
          "morph": "Prakrit adverbial (Skt yathājñātam)",
          "translatable": true
        },
        {
          "i": 9,
          "iast": "viharāmi",
          "gloss": "I fare, I dwell",
          "parts": [
            {
              "form": "vi-",
              "gloss": "about, around"
            },
            {
              "form": "√hṛ",
              "gloss": "to carry; (with vi-) to move about, to fare"
            },
            {
              "form": "-āmi",
              "gloss": "(1st person singular present)"
            }
          ],
          "stem": null,
          "root": "vi-√hṛ (Prakrit; Skt vi-√hṛ, bhvādi, 1U, 'to move about, to fare')",
          "affix": "-āmi (Prakrit present, 1st sg.)",
          "morph": "Prakrit pres. 1st sg.",
          "karaka": "the verb",
          "translatable": true
        },
        {
          "i": 10,
          "iast": "ahaṃ",
          "gloss": "I",
          "parts": [
            {
              "form": "ahaṃ",
              "gloss": "I (Skt aham)"
            }
          ],
          "stem": "ahaṃ",
          "root": null,
          "affix": null,
          "morph": "Prakrit nom. sg. (Skt aham)",
          "karaka": "kartṛ of viharāmi, expressed for emphasis",
          "translatable": true
        },
        {
          "i": 11,
          "iast": "muṇī",
          "gloss": "sage",
          "parts": [
            {
              "form": "muṇi",
              "gloss": "sage, silent ascetic (Skt muni)"
            }
          ],
          "stem": "muṇi",
          "root": null,
          "affix": "-ī (nom. sg. masc.; Skt muniḥ)",
          "morph": "Prakrit nom. sg. masc.",
          "karaka": "predicate nominative, in apposition to ahaṃ",
          "translatable": true
        }
      ],
      "english": "{0:One's own self}, {1:unconquered}, is {2:the enemy} — {3:the passions} {5:and} {4:the senses}. {7:Having conquered} {6:those}, {8:as I have learned}, {9:I fare}, {10:I}, {11:a sage}."
    }
  ]
};
