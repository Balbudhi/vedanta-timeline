/* =============================================================
   Bhagavad-Gītā 5 — the adhyāya entire, verses 1–29.
   window.CH5_VERSES — one object per verse.
   Schema + policy: docs/SANSKRIT_TRANSLATION_STANDARD.md (§3 data, §6
   Pāṇinian formalism, §7 faithful rendering, §8 preserve/translate).
   Site renders IAST only; words[].deva / devanagari are kept for local use.
   Interactive line = pada-pāṭha built from words[]; `iast` = saṃhitā.

   Mūla: data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt
     (BORI critical edition of the Mahābhārata; Tokunaga et al., revised by
      John Smith, via GRETIL). Every verse checked verbatim against it.

   Root text only — this reading carries no commentary layer.
   ============================================================= */

window.CH5_VERSES = [
  {
    "locus": "5.1",
    "speaker": "arjuna",
    "meter": "anuṣṭubh",
    "devanagari": "संन्यासं कर्मणां कृष्ण पुनर् योगं च शंससि ।\nयच् छ्रेय एतयोर् एकं तन् मे ब्रूहि सुनिश्चितम् ॥",
    "iast": "saṃnyāsaṃ karmaṇāṃ kṛṣṇa punar yogaṃ ca śaṃsasi |\nyac chreya etayor ekaṃ tan me brūhi suniścitam ||",
    "sense": "Arjuna puts it to Kṛṣṇa directly: you commend both the renunciation of karmas and yoga — tell me decisively which one of the two is better.",
    "english": "{6:You praise} {0:renunciation} {1:of karmas}, {2:O Kṛṣṇa}, {5:and} {3:again} {4:yoga}. {7:Which} {10:one} {9:of these two} {8:is better} — {11:that} {13:tell} {12:to me} {14:decisively}.",
    "words": [
      {
        "i": 0,
        "deva": "संन्यासम्",
        "iast": "saṃnyāsam",
        "gloss": "renunciation, the complete laying-down (of action)",
        "stem": "saṃnyāsa",
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "ghañ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of śaṃsasi",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "parts": [
          {
            "form": "sam-",
            "gloss": "together, completely"
          },
          {
            "form": "ni-",
            "gloss": "down"
          },
          {
            "form": "√as",
            "gloss": "to throw, to cast"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the casting down')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "कर्मणाम्",
        "iast": "karmaṇām",
        "gloss": "of karmas, of actions",
        "stem": "karman",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "man (kṛt) + ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. neut.",
        "karaka": "sambandha (genitive qualifying saṃnyāsam)",
        "glossaryKey": "karma",
        "translatable": false,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act, to perform"
          },
          {
            "form": "-man",
            "gloss": "(kṛt manin, the neuter action/result noun: 'the doing, the deed')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "कृष्ण",
        "iast": "kṛṣṇa",
        "gloss": "Kṛṣṇa (proper name)",
        "stem": "kṛṣṇa",
        "root": null,
        "affix": "su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kṛṣṇa",
            "gloss": "Kṛṣṇa (proper name, not an epithet built on another word)"
          }
        ],
        "note": "Unlike vārṣṇeya/kaunteya/mahābāho, this is the bare personal name, not a patronymic or descriptive epithet — kept as the name rather than translated."
      },
      {
        "i": 3,
        "deva": "पुनर्",
        "iast": "punar",
        "gloss": "again, once more",
        "stem": "punar",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb",
        "karaka": "— (adverbial, modifying śaṃsasi)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "punar",
            "gloss": "again, once more, back"
          }
        ]
      },
      {
        "i": 4,
        "deva": "योगम्",
        "iast": "yogam",
        "gloss": "yoga",
        "stem": "yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "ghañ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of śaṃsasi (second object, joined to saṃnyāsam by ca)",
        "glossaryKey": "yoga",
        "translatable": false,
        "parts": [
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite, to harness"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the yoking')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins yogam to saṃnyāsam as the second object)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "शंससि",
        "iast": "śaṃsasi",
        "gloss": "you praise, you commend, you proclaim",
        "stem": null,
        "root": "√śaṃs (bhvādi, 1P)",
        "rootGloss": "to praise, to proclaim, to recite, to declare, to commend",
        "affix": "tiṅ — laṭ, madhyama-puruṣa ekavacana, parasmaipada",
        "morph": "present indic., 2 sg., parasmaipada",
        "karaka": "kriyā (main verb); kartṛ 'you' (Kṛṣṇa, understood), karman saṃnyāsam and yogam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√śaṃs",
            "gloss": "to praise, to proclaim, to declare, to commend"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-si",
            "gloss": "(2nd person singular, parasmaipada)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "यत्",
        "iast": "yat",
        "gloss": "which",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut. (relative pronoun)",
        "karaka": "kartṛ of the implied copula, correlate of tat",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "which, what (the relative stem)"
          }
        ],
        "sandhi": "yac chreya ← yat + śreyaḥ (t + ś → c ch)"
      },
      {
        "i": 8,
        "deva": "श्रेयः",
        "iast": "śreyaḥ",
        "gloss": "better, more beneficial, the more excellent",
        "stem": "śreyas",
        "root": null,
        "affix": "īyasun (taddhita, comparative degree) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; comparative degree",
        "karaka": "predicate (of yat … ekam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "śreyas",
            "gloss": "better, more excellent, more beneficial (a suppletive comparative, historically tied to praśasya 'good')"
          }
        ],
        "sandhi": "śreya etayoḥ ← śreyaḥ + etayoḥ (visarga elided before a following vowel other than a)"
      },
      {
        "i": 9,
        "deva": "एतयोः",
        "iast": "etayoḥ",
        "gloss": "of these two",
        "stem": "etad",
        "root": null,
        "affix": "os (ṣaṣṭhī dvivacana)",
        "morph": "gen. dual masc.",
        "karaka": "sambandha (partitive genitive with ekam: 'one of these two')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "etad",
            "gloss": "this, this here (the nearer demonstrative)"
          },
          {
            "form": "-os",
            "gloss": "(genitive dual: 'of the two')"
          }
        ]
      },
      {
        "i": 10,
        "deva": "एकम्",
        "iast": "ekam",
        "gloss": "the one, one (of the two)",
        "stem": "eka",
        "root": null,
        "affix": "am (prathamā ekavacana, neut.)",
        "morph": "nom. sg. neut.",
        "karaka": "subject-apposition to yat ('the one which')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eka",
            "gloss": "one, a single one"
          }
        ]
      },
      {
        "i": 11,
        "deva": "तत्",
        "iast": "tat",
        "gloss": "that",
        "stem": "tad",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of brūhi, resuming yat … ekam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, it (the anaphoric demonstrative)"
          }
        ],
        "sandhi": "tan me ← tat + me (t → n before m)"
      },
      {
        "i": 12,
        "deva": "मे",
        "iast": "me",
        "gloss": "to me, for me",
        "stem": "asmad",
        "root": null,
        "affix": "ṅe (caturthī ekavacana, enclitic)",
        "morph": "dat. sg. (enclitic pronoun)",
        "karaka": "sampradāna (the one told, dative)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "me",
            "gloss": "to me, me (unstressed enclitic, never first in its clause)"
          }
        ]
      },
      {
        "i": 13,
        "deva": "ब्रूहि",
        "iast": "brūhi",
        "gloss": "tell!, say!, speak!",
        "stem": null,
        "root": "√brū (adādi, 2P)",
        "rootGloss": "to say, to speak, to tell, to declare",
        "affix": "hi (loṭ, madhyama-puruṣa ekavacana)",
        "morph": "2nd sg. imperative parasmaipada",
        "karaka": "kriyā; kartṛ 'you' (Kṛṣṇa, understood), karman tat",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√brū",
            "gloss": "to say, to speak, to tell, to declare"
          },
          {
            "form": "-hi",
            "gloss": "(2nd-singular imperative, athematic)"
          }
        ]
      },
      {
        "i": 14,
        "deva": "सुनिश्चितम्",
        "iast": "suniścitam",
        "gloss": "decisively, with certainty, definitely",
        "stem": "su-niścita",
        "root": "√ci (svādi, 5U)",
        "rootGloss": "to gather, to collect; (with ni-) to ascertain, to determine, to settle",
        "affix": "kta (niṣṭhā) + am (dvitīyā ekavacana, adverbial)",
        "morph": "acc. sg. neut.; adverbial",
        "karaka": "kriyā-viśeṣaṇa (adverbial accusative modifying brūhi)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "su-",
            "gloss": "well, thoroughly, properly"
          },
          {
            "form": "ni-",
            "gloss": "down, fully (determinative prefix)"
          },
          {
            "form": "√ci",
            "gloss": "to gather, to collect; to ascertain, to determine"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Arjuna's question. saṃnyāsam and yogam — two direct karmans of śaṃsasi ('you praise'), joined by ca; karmaṇām — sambandha (genitive) qualifying saṃnyāsam; kṛṣṇa — āmantraṇa (voc.). Second half: yat … ekam — the relative-clause subject ('the one which'), with śreyaḥ predicate and etayoḥ a partitive genitive ('of these two'); tat — karman of brūhi, resuming the relative clause; me — sampradāna (dative, 'to me'); suniścitam — adverbial accusative modifying brūhi.",
      "verbalModality": "Two finite verbs: śaṃsasi (laṭ, 2 sg., 'you praise' — a present-tense report of what Kṛṣṇa has been doing) and brūhi (loṭ, 2 sg. imperative, 'tell!' — Arjuna's direct demand). The question turns on the imperative: he wants a decision, not more praise of both."
    }
  },
  {
    "locus": "5.2",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "संन्यासः कर्मयोगश् च निःश्रेयसकराव् उभौ ।\nतयोस् तु कर्मसंन्यासात् कर्मयोगो विशिष्यते ॥",
    "iast": "saṃnyāsaḥ karmayogaś ca niḥśreyasakarāv ubhau |\ntayos tu karmasaṃnyāsāt karmayogo viśiṣyate ||",
    "sense": "Kṛṣṇa answers: renunciation and karma-yoga both bring about the highest good, but of the two, karma-yoga is superior to the mere renunciation of karma.",
    "english": "{0:Renunciation} {2:and} {1:karma-yoga} — {4:both} {3:bring about the highest good}. {6:But} {5:of these two}, {8:karma-yoga} {9:is superior} {7:to the renunciation of karma}.",
    "words": [
      {
        "i": 0,
        "deva": "संन्यासः",
        "iast": "saṃnyāsaḥ",
        "gloss": "renunciation, the complete laying-down (of action)",
        "stem": "saṃnyāsa",
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula (subject, with karmayogaḥ, of niḥśreyasakarau)",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "parts": [
          {
            "form": "sam-",
            "gloss": "together, completely"
          },
          {
            "form": "ni-",
            "gloss": "down"
          },
          {
            "form": "√as",
            "gloss": "to throw, to cast"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the casting down')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "कर्मयोगः",
        "iast": "karma-yogaḥ",
        "gloss": "karma-yoga, the yoga of action",
        "stem": "karma-yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, joined to saṃnyāsaḥ by ca",
        "glossaryKey": "karma-yoga",
        "translatable": false,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "karmaṇo yogaḥ",
          "members": [
            "karma",
            "yoga"
          ]
        },
        "parts": [
          {
            "form": "karma",
            "gloss": "karma, action, deed, the law of action"
          },
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          }
        ]
      },
      {
        "i": 2,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins karmayogaḥ to saṃnyāsaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 3,
        "deva": "निःश्रेयसकरौ",
        "iast": "niḥśreyasa-karau",
        "gloss": "productive of the highest good, bringing about beatitude",
        "stem": "niḥśreyasa-kara",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to bring about",
        "affix": "aṭ (kṛt, upapada) + au (prathamā dvivacana)",
        "morph": "nom. dual masc.",
        "karaka": "predicate of saṃnyāsaḥ and karmayogaḥ (dual, agreeing with the pair)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "upapada tatpuruṣa (kṛt-compound)",
          "vigraha": "niḥśreyasaṃ karataḥ iti niḥśreyasakarau",
          "members": [
            "niḥśreyasa",
            "kara"
          ]
        },
        "parts": [
          {
            "form": "niḥ-",
            "gloss": "out, beyond (intensive prefix: 'beyond which there is nothing')"
          },
          {
            "form": "śreyas",
            "gloss": "better, more excellent (comparative degree, used absolutely: 'the highest good')"
          },
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to bring about"
          },
          {
            "form": "-a",
            "gloss": "(kṛt ac/aṭ, agent noun: 'the maker of —')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "उभौ",
        "iast": "ubhau",
        "gloss": "both",
        "stem": "ubha",
        "root": null,
        "affix": "au (prathamā dvivacana, sarvanāma declension)",
        "morph": "nom. dual masc.",
        "karaka": "in apposition to saṃnyāsaḥ … karmayogaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ubha",
            "gloss": "both (of two)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "तयोः",
        "iast": "tayoḥ",
        "gloss": "of these two, of the two",
        "stem": "tad",
        "root": null,
        "affix": "os (ṣaṣṭhī dvivacana)",
        "morph": "gen. dual masc.",
        "karaka": "sambandha ('of these two')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, it (the anaphoric demonstrative)"
          },
          {
            "form": "-os",
            "gloss": "(genitive dual: 'of the two')"
          }
        ]
      },
      {
        "i": 6,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, however",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (marks the contrast with line 1)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tu",
            "gloss": "but, however, on the other hand"
          }
        ]
      },
      {
        "i": 7,
        "deva": "कर्मसंन्यासात्",
        "iast": "karma-saṃnyāsāt",
        "gloss": "than the renunciation of karma",
        "stem": "karma-saṃnyāsa",
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "ghañ (kṛt) + ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. masc.",
        "karaka": "apādāna (ablative of comparison, governed by viśiṣyate)",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "karmaṇaḥ saṃnyāsaḥ",
          "members": [
            "karma",
            "saṃnyāsa"
          ]
        },
        "parts": [
          {
            "form": "karma",
            "gloss": "karma, action, deed"
          },
          {
            "form": "sam-",
            "gloss": "together, completely"
          },
          {
            "form": "ni-",
            "gloss": "down"
          },
          {
            "form": "√as",
            "gloss": "to throw, to cast"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the casting down')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "कर्मयोगः",
        "iast": "karma-yogaḥ",
        "gloss": "karma-yoga, the yoga of action",
        "stem": "karma-yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of viśiṣyate",
        "glossaryKey": "karma-yoga",
        "translatable": false,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "karmaṇo yogaḥ",
          "members": [
            "karma",
            "yoga"
          ]
        },
        "parts": [
          {
            "form": "karma",
            "gloss": "karma, action, deed, the law of action"
          },
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          }
        ]
      },
      {
        "i": 9,
        "deva": "विशिष्यते",
        "iast": "viśiṣyate",
        "gloss": "is distinguished, is superior, excels",
        "stem": null,
        "root": "√śiṣ (rudhādi, 7P)",
        "rootGloss": "to leave over, to leave remaining",
        "affix": "vi- (prefix) + yak (bhāve/karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "present indic. passive, 3 sg.",
        "karaka": "kriyā; kartṛ karmayogaḥ, apādāna karmasaṃnyāsāt",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "vi-",
            "gloss": "apart, distinctly"
          },
          {
            "form": "√śiṣ",
            "gloss": "to leave remaining; (passive, with vi-) to stand apart, to excel"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Two nominal/passive sentences. Line 1: saṃnyāsaḥ and karmayogaḥ — joint kartṛ of the implied copula, with niḥśreyasakarau ubhau as predicate (dual, agreeing with the pair). Line 2: tayoḥ — sambandha ('of these two'); karmasaṃnyāsāt — apādāna (ablative of comparison) governed by viśiṣyate; karmayogaḥ — kartṛ of viśiṣyate.",
      "verbalModality": "One finite verb, viśiṣyate (laṭ, passive, 3 sg. — 'is distinguished, is superior'), stating the comparison as a present fact. Line 1 has no finite verb at all — a nominal sentence with an implied copula."
    }
  },
  {
    "locus": "5.3",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "ज्ञेयः स नित्यसंन्यासी यो न द्वेष्टि न काङ्क्षति ।\nनिर्द्वंद्वो हि महाबाहो सुखं बन्धात् प्रमुच्यते ॥",
    "iast": "jñeyaḥ sa nityasaṃnyāsī yo na dveṣṭi na kāṅkṣati |\nnirdvaṃdvo hi mahābāho sukhaṃ bandhāt pramucyate ||",
    "sense": "He is to be known as the constant renunciant who neither feels dveṣa nor desires; free from the pairs of opposites, O Arjuna, he is easily released from bondage.",
    "english": "{1:He} is {0:to be known as} {2:the eternal renunciant} — {3:who} {4:neither} {5:feels dveṣa} {6:nor} {7:longs for anything}. {9:For}, {10:O mighty-armed one}, {8:free from the dualities}, he {13:is released} {11:easily} {12:from bondage}.",
    "words": [
      {
        "i": 0,
        "deva": "ज्ञेयः",
        "iast": "jñeyaḥ",
        "gloss": "to be known, knowable",
        "stem": "jñeya",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to understand, to recognize, to become acquainted with",
        "affix": "yat (kṛtya, gerundive) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; gerundive (verbal adjective of obligation)",
        "karaka": "predicate of sa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ya",
            "gloss": "(kṛtya yat, gerundive: 'to be —ed, fit to be —ed')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "स",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ (subject of the implied copula)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (nom. masc. demonstrative)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "नित्यसंन्यासी",
        "iast": "nitya-saṃnyāsī",
        "gloss": "the eternal renunciant, the perpetual renouncer",
        "stem": "nitya-saṃnyāsin",
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "in (taddhita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate of sa, in apposition with jñeyaḥ",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "compound": {
          "type": "karmadhāraya",
          "vigraha": "nityaś ca asau saṃnyāsī ca — nityasaṃnyāsī",
          "members": [
            "nitya",
            "saṃnyāsin"
          ]
        },
        "parts": [
          {
            "form": "nitya",
            "gloss": "eternal, perpetual, constant, permanent"
          },
          {
            "form": "saṃnyāsin",
            "gloss": "renunciant, one who has laid down all action"
          }
        ],
        "note": "Śaṅkara reads nitya-saṃnyāsī as the one who is always, constitutionally a renunciant — not by the outward mark of the āśrama but because he is already free of dveṣa and kāṅkṣā, so there is nothing left in him to renounce afresh."
      },
      {
        "i": 3,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who, the one who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc. (relative pronoun)",
        "karaka": "kartṛ of dveṣṭi / kāṅkṣati; correlate of sa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "pratiṣedha (negates dveṣṭi)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not"
          }
        ]
      },
      {
        "i": 5,
        "deva": "द्वेष्टि",
        "iast": "dveṣṭi",
        "gloss": "hates, recoils from, feels aversion",
        "stem": null,
        "root": "√dviṣ (adādi, 2P)",
        "rootGloss": "to hate, to dislike, to be hostile to, to recoil from",
        "affix": "tiṅ — laṭ, prathama-puruṣa ekavacana, parasmaipada (adādi, athematic)",
        "morph": "present indic., 3 sg., parasmaipada",
        "karaka": "kriyā; kartṛ yaḥ",
        "glossaryKey": "dvesa",
        "translatable": true,
        "parts": [
          {
            "form": "√dviṣ",
            "gloss": "to hate, to recoil from, to feel aversion toward"
          }
        ]
      },
      {
        "i": 6,
        "deva": "न",
        "iast": "na",
        "gloss": "not, nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "pratiṣedha (negates kāṅkṣati)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, nor"
          }
        ]
      },
      {
        "i": 7,
        "deva": "काङ्क्षति",
        "iast": "kāṅkṣati",
        "gloss": "desires, longs for, craves, wishes for",
        "stem": null,
        "root": "√kāṅkṣ (bhvādi, 1P)",
        "rootGloss": "to desire, to long for, to crave, to wish for",
        "affix": "tiṅ — laṭ, prathama-puruṣa ekavacana, parasmaipada",
        "morph": "present indic., 3 sg., parasmaipada",
        "karaka": "kriyā; kartṛ yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√kāṅkṣ",
            "gloss": "to desire, to long for, to crave, to wish for"
          }
        ]
      },
      {
        "i": 8,
        "deva": "निर्द्वंद्वः",
        "iast": "nirdvaṃdvaḥ",
        "gloss": "free from the pairs of opposites, released from the dualities",
        "stem": "nir-dvaṃdva",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate/attribute of sa",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (privative, nir-)",
          "vigraha": "na vidyante dvaṃdvāni yasya saḥ",
          "members": [
            "dvaṃdva"
          ]
        },
        "parts": [
          {
            "form": "nir-",
            "gloss": "without, free from (privative prefix)"
          },
          {
            "form": "dvaṃdva",
            "gloss": "pair, duality; a pair of opposites (heat/cold, pleasure/pain)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "हि",
        "iast": "hi",
        "gloss": "for, indeed, because",
        "stem": "hi",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable causal/emphatic particle",
        "karaka": "— (hetu-dyotaka nipāta)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "hi",
            "gloss": "for, indeed, because"
          }
        ]
      },
      {
        "i": 10,
        "deva": "महाबाहो",
        "iast": "mahābāho",
        "gloss": "O mighty-armed one",
        "stem": "mahā-bāhu",
        "root": null,
        "affix": "su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mahāntau bāhū yasya saḥ",
          "members": [
            "mahat",
            "bāhu"
          ]
        },
        "parts": [
          {
            "form": "mahā-",
            "gloss": "great, vast (the compounding form of mahat)"
          },
          {
            "form": "bāhu",
            "gloss": "arm"
          }
        ]
      },
      {
        "i": 11,
        "deva": "सुखम्",
        "iast": "sukham",
        "gloss": "easily, readily",
        "stem": "sukha",
        "root": null,
        "affix": "am (dvitīyā ekavacana, used adverbially)",
        "morph": "acc. sg. neut.; adverbial",
        "karaka": "kriyā-viśeṣaṇa (adverbial accusative modifying pramucyate)",
        "glossaryKey": "sukha",
        "translatable": true,
        "parts": [
          {
            "form": "su-",
            "gloss": "good, well, easy (the auspicious prefix)"
          },
          {
            "form": "-kha",
            "gloss": "(traditionally 'axle-hole, hub' — hence 'running smoothly')"
          }
        ],
        "note": "Here sukham is the adverbial accusative ('easily'), not the noun 'pleasure' — Śaṅkara glosses it sukhena. Flagging the sense choice: elsewhere on this site sukha is rendered 'pleasure' as a noun; this occurrence is adjectival/adverbial and is rendered accordingly per §7.4 (choose the sense the usage requires)."
      },
      {
        "i": 12,
        "deva": "बन्धात्",
        "iast": "bandhāt",
        "gloss": "from bondage, from the bond",
        "stem": "bandha",
        "root": "√bandh (kryādi, 9P)",
        "rootGloss": "to bind, to tie, to fetter, to fasten",
        "affix": "ghañ (kṛt) + ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. masc.",
        "karaka": "apādāna (ablative of separation, governed by pramucyate)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√bandh",
            "gloss": "to bind, to tie, to fetter"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the binding, the bond')"
          }
        ]
      },
      {
        "i": 13,
        "deva": "प्रमुच्यते",
        "iast": "pramucyate",
        "gloss": "is released, is set free, is liberated",
        "stem": null,
        "root": "√muc (tudādi, 6U)",
        "rootGloss": "to release, to set free, to loosen, to let go",
        "affix": "pra- (prefix) + yak (bhāve/karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "present indic. passive, 3 sg.",
        "karaka": "kriyā (main verb, passive); kartṛ sa, apādāna bandhāt",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, completely"
          },
          {
            "form": "√muc",
            "gloss": "to release, to set free, to loosen"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "sa — kartṛ, predicate jñeyaḥ (gerundive, 'is to be known'), in apposition with nitya-saṃnyāsī; yaḥ — kartṛ of the subordinate clause governing dveṣṭi and kāṅkṣati, correlate of sa; nirdvaṃdvaḥ — a further predicate adjective of sa; mahābāho — āmantraṇa; sukham — adverbial accusative modifying pramucyate; bandhāt — apādāna (ablative of separation) governed by pramucyate.",
      "verbalModality": "jñeyaḥ is a gerundive (obligation: 'is to be known'), not a finite verb — the verse opens with a prescription, not a report. dveṣṭi and kāṅkṣati are both laṭ (present, 3 sg.), negated; pramucyate is laṭ passive, 3 sg. — the release is stated as a standing present fact, not a future promise."
    }
  },
  {
    "locus": "5.4",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "सांख्ययोगौ पृथग् बालाः प्रवदन्ति न पण्डिताः ।\nएकम् अप्य् आस्थितः सम्यग् उभयोर् विन्दते फलम् ॥",
    "iast": "sāṃkhyayogau pṛthag bālāḥ pravadanti na paṇḍitāḥ |\nekam apy āsthitaḥ samyag ubhayor vindate phalam ||",
    "sense": "Only the unlearned say Sāṅkhya and yoga are different; one who is truly established in even one of the two obtains the fruit of both.",
    "english": "{2:The unlearned} {3:proclaim} {0:Sāṅkhya and yoga} {1:as separate} — {4:not} {5:the learned}. {7:Even} {8:one who is established} {6:in one} {9:fully} {11:obtains} {12:the fruit} {10:of both}.",
    "words": [
      {
        "i": 0,
        "deva": "सांख्ययोगौ",
        "iast": "sāṃkhya-yogau",
        "gloss": "Sāṅkhya and yoga",
        "stem": "sāṃkhya-yoga",
        "root": null,
        "affix": "au (prathamā/dvitīyā dvivacana)",
        "morph": "acc. dual masc.",
        "karaka": "karman of pravadanti",
        "glossaryKey": "sankhya",
        "translatable": false,
        "compound": {
          "type": "dvandva (itaretara)",
          "vigraha": "sāṃkhyaś ca yogaś ca sāṃkhyayogau",
          "members": [
            "sāṃkhya",
            "yoga"
          ]
        },
        "parts": [
          {
            "form": "sāṃkhya",
            "gloss": "Sāṅkhya (the enumeration philosophy); knowledge, reasoning, discrimination"
          },
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          }
        ]
      },
      {
        "i": 1,
        "deva": "पृथक्",
        "iast": "pṛthak",
        "gloss": "separately, differently, apart",
        "stem": "pṛthak",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb",
        "karaka": "predicate adverb, describing the object sāṃkhyayogau as pravadanti presents it",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pṛthak",
            "gloss": "separately, apart, differently, individually"
          }
        ]
      },
      {
        "i": 2,
        "deva": "बालाः",
        "iast": "bālāḥ",
        "gloss": "the unlearned, the untaught; children, fools",
        "stem": "bāla",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of pravadanti",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "bāla",
            "gloss": "child, young one; fool, the untaught, the undiscerning"
          }
        ],
        "note": "Śaṅkara glosses bālāḥ as avivekinaḥ, 'those without discrimination' — not literally children. Rendered 'the unlearned' to hold the contrast with paṇḍitāḥ, 'the learned'."
      },
      {
        "i": 3,
        "deva": "प्रवदन्ति",
        "iast": "pravadanti",
        "gloss": "proclaim, declare, assert",
        "stem": null,
        "root": "√vad (bhvādi, 1P)",
        "rootGloss": "to speak, to say, to assert",
        "affix": "pra- (prefix) + tiṅ — laṭ, prathama-puruṣa bahuvacana, parasmaipada",
        "morph": "present indic., 3 pl., parasmaipada",
        "karaka": "kriyā; kartṛ bālāḥ, karman sāṃkhyayogau",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, out"
          },
          {
            "form": "√vad",
            "gloss": "to speak, to say, to assert"
          },
          {
            "form": "-anti",
            "gloss": "(3rd person plural, parasmaipada)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "pratiṣedha (negates the elided pravadanti as applied to paṇḍitāḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not"
          }
        ]
      },
      {
        "i": 5,
        "deva": "पण्डिताः",
        "iast": "paṇḍitāḥ",
        "gloss": "the learned, the wise",
        "stem": "paṇḍita",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of the elided pravadanti, negated",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "paṇḍita",
            "gloss": "learned, wise, skilled; a scholar"
          }
        ],
        "note": "The verb is elided in this clause, carried over from the first: 'not [do] the learned [proclaim them separate]'."
      },
      {
        "i": 6,
        "deva": "एकम्",
        "iast": "ekam",
        "gloss": "one (of the two)",
        "stem": "eka",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of āsthitaḥ, used transitively ('having taken up one')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eka",
            "gloss": "one, a single one"
          }
        ]
      },
      {
        "i": 7,
        "deva": "अपि",
        "iast": "api",
        "gloss": "even, also",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (concessive, over ekam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "api",
            "gloss": "even, also; although"
          }
        ],
        "sandhi": "apy āsthitaḥ ← api + āsthitaḥ (i → y before a dissimilar vowel)"
      },
      {
        "i": 8,
        "deva": "आस्थितः",
        "iast": "āsthitaḥ",
        "gloss": "established in, steadied in, resorted to",
        "stem": "āsthita",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to remain, to be established",
        "affix": "ā- (prefix) + kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle, used substantively",
        "karaka": "kartṛ of vindate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ā-",
            "gloss": "toward, fully"
          },
          {
            "form": "√sthā",
            "gloss": "to stand, to remain, to be established"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "सम्यक्",
        "iast": "samyak",
        "gloss": "properly, rightly, fully, correctly",
        "stem": "samyac",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb",
        "karaka": "— (adverbial, modifying vindate)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "samyak",
            "gloss": "properly, rightly, fully, correctly"
          }
        ]
      },
      {
        "i": 10,
        "deva": "उभयोः",
        "iast": "ubhayoḥ",
        "gloss": "of both",
        "stem": "ubhaya",
        "root": null,
        "affix": "os (ṣaṣṭhī dvivacana)",
        "morph": "gen. dual",
        "karaka": "sambandha (genitive qualifying phalam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ubhaya",
            "gloss": "both (of the two)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "विन्दते",
        "iast": "vindate",
        "gloss": "obtains, finds, gains",
        "stem": null,
        "root": "√vid (tudādi, 6U)",
        "rootGloss": "to find, to obtain, to get",
        "affix": "tiṅ — laṭ, prathama-puruṣa ekavacana, ātmanepada",
        "morph": "present indic., 3 sg., ātmanepada",
        "karaka": "kriyā; kartṛ āsthitaḥ, karman phalam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√vid",
            "gloss": "to find, to obtain, to get"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      },
      {
        "i": 12,
        "deva": "फलम्",
        "iast": "phalam",
        "gloss": "the fruit, the result",
        "stem": "phala",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of vindate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "phala",
            "gloss": "fruit; result, outcome, consequence"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "bālāḥ — kartṛ of pravadanti; sāṅkhyayogau — karman (acc. dual); pṛthak — predicate adverb of the object; na paṇḍitāḥ — the second, negated kartṛ, verb elided. Second sentence: āsthitaḥ — kartṛ of vindate (a substantive participle, 'one who is established'); ekam — karman of āsthitaḥ; ubhayoḥ — sambandha ('of both') qualifying phalam; phalam — karman of vindate.",
      "verbalModality": "pravadanti (laṭ, 3 pl.) states what the unlearned habitually do; vindate (laṭ, 3 sg. ātmanepada) states what the one truly established gets — both present-tense generalizations, not single events."
    }
  },
  {
    "locus": "5.5",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "यत् सांख्यैः प्राप्यते स्थानं तद् योगैर् अपि गम्यते ।\nएकं सांख्यं च योगं च यः पश्यति स पश्यति ॥",
    "iast": "yat sāṃkhyaiḥ prāpyate sthānaṃ tad yogair api gamyate |\nekaṃ sāṃkhyaṃ ca yogaṃ ca yaḥ paśyati sa paśyati ||",
    "sense": "The station reached by the followers of Sāṅkhya is the very one reached by the followers of yoga; he who sees Sāṅkhya and yoga as one truly sees.",
    "english": "{3:The station} {0:which} {2:is attained} {1:by the followers of Sāṅkhya} — {4:that} {6:too} {7:is reached} {5:by the followers of yoga}. {13:He who} {14:sees} {9:Sāṅkhya} {12:and} {11:yoga} {10:both} {8:as one} — {15:he} {16:sees}.",
    "words": [
      {
        "i": 0,
        "deva": "यत्",
        "iast": "yat",
        "gloss": "which",
        "stem": "yad",
        "root": null,
        "affix": "am (dvitīyā/prathamā ekavacana neut.)",
        "morph": "nom. sg. neut. (relative pronoun)",
        "karaka": "kartṛ-correlate, agreeing with sthānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "which, what (the relative stem)"
          }
        ]
      },
      {
        "i": 1,
        "deva": "सांख्यैः",
        "iast": "sāṃkhyaiḥ",
        "gloss": "by the followers of Sāṅkhya",
        "stem": "sāṃkhya",
        "root": null,
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. masc.",
        "karaka": "kartā (the agent in the instrumental, required by the passive prāpyate)",
        "glossaryKey": "sankhya",
        "translatable": true,
        "parts": [
          {
            "form": "sāṃkhya",
            "gloss": "Sāṅkhya (the enumeration philosophy); knowledge, reasoning, discrimination"
          },
          {
            "form": "-aiḥ",
            "gloss": "(instrumental plural: 'by')"
          }
        ],
        "note": "Instrumental of agent with a passive verb. Śaṅkara glosses sāṅkhyaiḥ as sāṅkhyair jñānibhiḥ, 'by the Sāṅkhyas, i.e. by the knowers' — the followers of the Sāṅkhya path, not the doctrine as an abstract instrument."
      },
      {
        "i": 2,
        "deva": "प्राप्यते",
        "iast": "prāpyate",
        "gloss": "is attained, is obtained, is reached",
        "stem": null,
        "root": "√āp (svādi, 5U)",
        "rootGloss": "to obtain, to attain, to get, to reach",
        "affix": "pra- (prefix) + yak (bhāve/karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "present indic. passive, 3 sg.",
        "karaka": "kriyā; karman sthānam (nom., as passive subject), kartā sāṃkhyaiḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, fully"
          },
          {
            "form": "√āp",
            "gloss": "to obtain, to attain, to get, to reach"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          }
        ]
      },
      {
        "i": 3,
        "deva": "स्थानम्",
        "iast": "sthānam",
        "gloss": "the station, the place, the standing",
        "stem": "sthāna",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to remain, to be established",
        "affix": "lyuṭ (kṛt) + am (prathamā ekavacana neut.)",
        "morph": "nom. sg. neut.",
        "karaka": "karman of the passive prāpyate, standing in the nominative",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sthā",
            "gloss": "to stand, to remain, to be established"
          },
          {
            "form": "-āna",
            "gloss": "(lyuṭ, the action/place-noun: 'the standing, the place')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "तत्",
        "iast": "tat",
        "gloss": "that",
        "stem": "tad",
        "root": null,
        "affix": "am (prathamā ekavacana neut.)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ-correlate, resuming sthānam as karman of the passive gamyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, it (the anaphoric demonstrative)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "योगैः",
        "iast": "yogaiḥ",
        "gloss": "by the followers of yoga",
        "stem": "yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. masc.",
        "karaka": "kartā (the agent in the instrumental, required by the passive gamyate)",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          },
          {
            "form": "-aiḥ",
            "gloss": "(instrumental plural: 'by')"
          }
        ],
        "note": "Parallel to sāṅkhyaiḥ: instrumental plural of agent, read (with the commentators) as 'by the followers of yoga', not as an abstract instrument."
      },
      {
        "i": 6,
        "deva": "अपि",
        "iast": "api",
        "gloss": "also, too, even",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (emphatic, over yogaiḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "api",
            "gloss": "also, too, even"
          }
        ]
      },
      {
        "i": 7,
        "deva": "गम्यते",
        "iast": "gamyate",
        "gloss": "is reached, is gone to, is arrived at",
        "stem": null,
        "root": "√gam (bhvādi, 1P)",
        "rootGloss": "to go, to move, to reach",
        "affix": "yak (bhāve/karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "present indic. passive, 3 sg.",
        "karaka": "kriyā; karman tat (nom., as passive subject), kartā yogaiḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√gam",
            "gloss": "to go, to move, to reach"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "एकम्",
        "iast": "ekam",
        "gloss": "as one, one",
        "stem": "eka",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "predicate accusative, complement of paśyati ('sees X as one')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eka",
            "gloss": "one, a single one"
          }
        ]
      },
      {
        "i": 9,
        "deva": "सांख्यम्",
        "iast": "sāṃkhyam",
        "gloss": "Sāṅkhya",
        "stem": "sāṃkhya",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of paśyati",
        "glossaryKey": "sankhya",
        "translatable": false,
        "parts": [
          {
            "form": "sāṃkhya",
            "gloss": "Sāṅkhya (the enumeration philosophy); knowledge, reasoning, discrimination"
          }
        ]
      },
      {
        "i": 10,
        "deva": "च",
        "iast": "ca",
        "gloss": "both (correlative ca … ca)",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (first member of the ca … ca correlative pair)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "योगम्",
        "iast": "yogam",
        "gloss": "yoga",
        "stem": "yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of paśyati, joined to sāṃkhyam by ca … ca",
        "glossaryKey": "yoga",
        "translatable": false,
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          }
        ]
      },
      {
        "i": 12,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (second member of the ca … ca correlative pair)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 13,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "he who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc. (relative pronoun)",
        "karaka": "kartṛ of the first paśyati, correlate of sa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ]
      },
      {
        "i": 14,
        "deva": "पश्यति",
        "iast": "paśyati",
        "gloss": "sees",
        "stem": null,
        "root": "√dṛś (bhvādi, 1P; present-stem suppletion paśyati)",
        "rootGloss": "to see, to behold; to perceive, to understand truly",
        "affix": "tiṅ — laṭ, prathama-puruṣa ekavacana, parasmaipada",
        "morph": "present indic., 3 sg., parasmaipada",
        "karaka": "kriyā; kartṛ yaḥ, karman ekam (sāṃkhyam … yogam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√dṛś",
            "gloss": "to see, to behold, to perceive"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, parasmaipada)"
          }
        ]
      },
      {
        "i": 15,
        "deva": "स",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the second paśyati, correlate of yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (nom. masc. demonstrative)"
          }
        ]
      },
      {
        "i": 16,
        "deva": "पश्यति",
        "iast": "paśyati",
        "gloss": "sees",
        "stem": null,
        "root": "√dṛś (bhvādi, 1P; present-stem suppletion paśyati)",
        "rootGloss": "to see, to behold; to perceive, to understand truly",
        "affix": "tiṅ — laṭ, prathama-puruṣa ekavacana, parasmaipada",
        "morph": "present indic., 3 sg., parasmaipada",
        "karaka": "kriyā; kartṛ sa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√dṛś",
            "gloss": "to see, to behold, to perceive"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, parasmaipada)"
          }
        ],
        "note": "The verb is repeated for the same subject-type rather than intensified by an adverb — the repetition itself is the emphasis ('he sees … he [really] sees'), rendered literally without inserting a word the Sanskrit does not have."
      }
    ],
    "grammar": {
      "karakaSummary": "sthānam — karman of the passive prāpyate, standing in the nominative; sāṅkhyaiḥ — the agent in the instrumental (kartā tṛtīyā, required by the passive); tat — the correlative subject of the second clause, resuming sthānam; yogaiḥ — its instrumental agent. Third sentence: yaḥ — kartṛ of paśyati; ekam — predicate accusative complement ('as one'); sāṅkhyam and yogam — the two karmans of paśyati, joined by ca … ca; sa — kartṛ of the second paśyati, correlate of yaḥ.",
      "verbalModality": "Two passive presents (prāpyate, gamyate) state the equivalence of the two paths as a standing fact; the closing paśyati … paśyati (both laṭ, 3 sg., active) repeats the same verb for the same subject-type, the repetition itself doing the philosophical work."
    }
  },
  {
    "locus": "5.6",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "संन्यासस् तु महाबाहो दुःखम् आप्तुम् अयोगतः ।\nयोगयुक्तो मुनिर् ब्रह्म नचिरेणाधिगच्छति ॥",
    "iast": "saṃnyāsas tu mahābāho duḥkham āptum ayogataḥ |\nyogayukto munir brahma nacireṇādhigacchati ||",
    "sense": "But renunciation without yoga is hard to attain, O Arjuna; the sage who is yoked to yoga reaches Brahman without delay.",
    "english": "{1:But} {0:renunciation}, {2:O mighty-armed one}, is {3:hard} {4:to attain} {5:without yoga}; {7:the sage} {6:yoked with yoga} {11:attains} {8:Brahman} {9:not} {10:after a long time}.",
    "words": [
      {
        "i": 0,
        "deva": "संन्यासः",
        "iast": "saṃnyāsaḥ",
        "gloss": "renunciation, the complete laying-down (of action)",
        "stem": "saṃnyāsa",
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula ('is hard')",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "parts": [
          {
            "form": "sam-",
            "gloss": "together, completely"
          },
          {
            "form": "ni-",
            "gloss": "down"
          },
          {
            "form": "√as",
            "gloss": "to throw, to cast"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the casting down')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, however",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (marks the contrast with 5.5)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tu",
            "gloss": "but, however, on the other hand"
          }
        ]
      },
      {
        "i": 2,
        "deva": "महाबाहो",
        "iast": "mahābāho",
        "gloss": "O mighty-armed one",
        "stem": "mahā-bāhu",
        "root": null,
        "affix": "su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mahāntau bāhū yasya saḥ",
          "members": [
            "mahat",
            "bāhu"
          ]
        },
        "parts": [
          {
            "form": "mahā-",
            "gloss": "great, vast (the compounding form of mahat)"
          },
          {
            "form": "bāhu",
            "gloss": "arm"
          }
        ]
      },
      {
        "i": 3,
        "deva": "दुःखम्",
        "iast": "duḥkham",
        "gloss": "hard, difficult",
        "stem": "duḥkha",
        "root": null,
        "affix": "am (prathamā ekavacana neut., predicative)",
        "morph": "nom./acc. sg. neut.; predicate adjective governing the infinitive āptum",
        "karaka": "predicate of saṃnyāsaḥ, with the idiomatic '— + infinitive' construction ('hard to —')",
        "glossaryKey": "duhkha",
        "translatable": true,
        "parts": [
          {
            "form": "duḥ-",
            "gloss": "bad, difficult, ill (the pejorative prefix)"
          },
          {
            "form": "-kham",
            "gloss": "(traditionally 'axle-hole, hub' — an ill-fitting axle-hole, hence 'rough, hard')"
          }
        ],
        "note": "duḥkham āptum is the same idiom as sukham (5.3): a neuter accusative-like adjective governing an infinitive, 'hard to attain'. Rendered 'hard' (predicate adjective) rather than the noun 'sorrow' — flagging the sense choice per §7.4."
      },
      {
        "i": 4,
        "deva": "आप्तुम्",
        "iast": "āptum",
        "gloss": "to attain, to obtain, to get",
        "stem": null,
        "root": "√āp (svādi, 5U)",
        "rootGloss": "to obtain, to attain, to get, to reach",
        "affix": "tumun (kṛt, infinitive)",
        "morph": "infinitive",
        "karaka": "the action qualified by duḥkham",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√āp",
            "gloss": "to obtain, to attain, to get, to reach"
          },
          {
            "form": "-tum",
            "gloss": "(tumun, the infinitive affix: 'to —')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "अयोगतः",
        "iast": "ayogataḥ",
        "gloss": "without yoga, not by way of yoga",
        "stem": "a-yoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach",
        "affix": "nañ (negative prefix) + tasil (taddhita, pañcamyarthe: 'from, by way of')",
        "morph": "indeclinable adverb, ablative sense, negated",
        "karaka": "apādāna-tulya (ablative-sense adverbial of means, negated), qualifying āptum",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "a-",
            "gloss": "not (negative prefix nañ)"
          },
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          },
          {
            "form": "-tas",
            "gloss": "(taddhita tasil, pañcamyarthe: 'from, by means of'; negated here: 'not through, without')"
          }
        ]
      },
      {
        "i": 6,
        "deva": "योगयुक्तः",
        "iast": "yoga-yuktaḥ",
        "gloss": "yoked with yoga, disciplined by yoga, joined to yoga",
        "stem": "yoga-yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite, to harness, to engage",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle in compound",
        "karaka": "predicate of muniḥ",
        "glossaryKey": "yoga",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (tṛtīyā)",
          "vigraha": "yogena yuktaḥ",
          "members": [
            "yoga",
            "yukta"
          ]
        },
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga, discipline, method, union, spiritual practice"
          },
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite, to harness"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "मुनिः",
        "iast": "muniḥ",
        "gloss": "sage, contemplative (one given to mananam)",
        "stem": "muni",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of adhigacchati",
        "glossaryKey": "muni",
        "translatable": true,
        "parts": [
          {
            "form": "muni",
            "gloss": "sage, seer; the silent one, the contemplative"
          }
        ]
      },
      {
        "i": 8,
        "deva": "ब्रह्म",
        "iast": "brahma",
        "gloss": "Brahman",
        "stem": "brahman",
        "root": "√bṛh (bhvādi, 1P)",
        "rootGloss": "to grow, to expand, to increase, to swell",
        "affix": "manin (kṛt) + am (dvitīyā ekavacana; the stem's final -an drops before the ending: brahman + am → brahma)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of adhigacchati",
        "glossaryKey": "brahman",
        "translatable": true,
        "parts": [
          {
            "form": "brahman",
            "gloss": "the Absolute, Brahman; the supreme reality; sacred utterance, sacred lore"
          }
        ],
        "note": "Traditional derivation from √bṛh 'to grow, to expand' — Brahman as the ever-vast, that beyond which nothing is greater."
      },
      {
        "i": 9,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "pratiṣedha (negates cireṇa, forming the idiom 'not after long' = 'soon')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not"
          }
        ]
      },
      {
        "i": 10,
        "deva": "चिरेण",
        "iast": "cireṇa",
        "gloss": "after a long time, at length",
        "stem": "cira",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana, temporal)",
        "morph": "instr. sg. neut.; temporal instrumental",
        "karaka": "kāla-viṣayaka tṛtīyā (temporal instrumental) modifying adhigacchati, negated by na",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "cira",
            "gloss": "long, of long duration"
          },
          {
            "form": "-eṇa",
            "gloss": "(instrumental singular, temporal: 'after —, in the course of —')"
          }
        ]
      },
      {
        "i": 11,
        "deva": "अधिगच्छति",
        "iast": "adhigacchati",
        "gloss": "attains, reaches",
        "stem": null,
        "root": "√gam (bhvādi, 1P)",
        "rootGloss": "to go, to move, to reach; with adhi-, to attain, to reach fully, to comprehend",
        "affix": "adhi- (prefix) + tiṅ — laṭ, prathama-puruṣa ekavacana, parasmaipada",
        "morph": "present indic., 3 sg., parasmaipada",
        "karaka": "kriyā (main verb); kartṛ muniḥ, karman brahma",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "adhi-",
            "gloss": "over, up to, fully"
          },
          {
            "form": "√gam",
            "gloss": "to go, to move, to attain"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "saṃnyāsaḥ — kartṛ of the implied copula ('is hard'); duḥkham — predicate adjective governing the infinitive āptum; ayogataḥ — an ablative-sense adverb qualifying the whole clause ('without yoga'); mahābāho — āmantraṇa. Second clause: muniḥ — kartṛ of adhigacchati, qualified by the predicate compound yoga-yuktaḥ; brahma — karman of adhigacchati; cireṇa — temporal instrumental, negated by na.",
      "verbalModality": "No finite verb in the first clause — duḥkham āptum is a predicate-adjective-plus-infinitive construction, stating a standing difficulty rather than an event. adhigacchati (laṭ, 3 sg.) closes the verse as a present-tense fact: the yoked sage simply arrives, without delay."
    }
  },
  {
    "locus": "5.7",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "योगयुक्तो विशुद्धात्मा विजितात्मा जितेन्द्रियः ।\nसर्वभूतात्मभूतात्मा कुर्वन्न् अपि न लिप्यते ॥",
    "iast": "yogayukto viśuddhātmā vijitātmā jitendriyaḥ |\nsarvabhūtātmabhūtātmā kurvann api na lipyate ||",
    "sense": "One yoked in yoga, purified and self-mastered in mind, senses conquered, whose self has become the self of all beings — even while acting, he is not stained.",
    "english": "{0:Yoked in yoga}, {1:pure in self}, {2:self-conquered}, {3:the indriyas conquered}, {4:whose self has become the self of all beings} — {6:even} {5:while acting}, he {7:is not} {8:stained}.",
    "words": [
      {
        "i": 0,
        "deva": "योगयुक्तः",
        "iast": "yogayuktaḥ",
        "gloss": "yoked in yoga, disciplined through yoga",
        "stem": "yoga-yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite; to apply oneself, to engage",
        "affix": "kta (niṣṭhā, on yukta) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle, compounded",
        "karaka": "attribute of the implied subject (kartṛ of lipyate)",
        "glossaryKey": "yoga",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (tṛtīyā)",
          "vigraha": "yogena yuktaḥ",
          "members": [
            "yoga",
            "yukta"
          ]
        },
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga — disciplined practice, the yoking of oneself (kept in Sanskrit)"
          },
          {
            "form": "yukta",
            "gloss": "yoked, joined, united (past passive participle of √yuj)"
          }
        ],
        "sandhi": "yogayukto viśuddhātmā ← yogayuktaḥ + viśuddhātmā (visarga → o before a voiced consonant, here v)"
      },
      {
        "i": 1,
        "deva": "विशुद्धात्मा",
        "iast": "viśuddhātmā",
        "gloss": "whose self is (thoroughly) purified, pure in self",
        "stem": "viśuddha-ātman",
        "root": "√śudh (divādi, 4P)",
        "rootGloss": "to become clean, to become pure",
        "affix": "kta (niṣṭhā, on viśuddha) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of the implied subject, in apposition with yoga-yuktaḥ",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "viśuddhaḥ ātmā yasya saḥ",
          "members": [
            "viśuddha",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "vi-",
            "gloss": "thoroughly, completely"
          },
          {
            "form": "√śudh",
            "gloss": "to become clean, to become pure"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "self"
          }
        ]
      },
      {
        "i": 2,
        "deva": "विजितात्मा",
        "iast": "vijitātmā",
        "gloss": "whose self is (fully) conquered, self-mastered",
        "stem": "vijita-ātman",
        "root": "√ji (bhvādi, 1P)",
        "rootGloss": "to conquer, to win, to overcome",
        "affix": "kta (niṣṭhā, on vijita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of the implied subject, in apposition",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "vijitaḥ ātmā yena saḥ",
          "members": [
            "vijita",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "vi-",
            "gloss": "thoroughly, completely"
          },
          {
            "form": "√ji",
            "gloss": "to conquer, to win, to overcome"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "self"
          }
        ]
      },
      {
        "i": 3,
        "deva": "जितेन्द्रियः",
        "iast": "jitendriyaḥ",
        "gloss": "whose indriyas are conquered, senses mastered",
        "stem": "jita-indriya",
        "root": "√ji (bhvādi, 1P)",
        "rootGloss": "to conquer, to win, to overcome",
        "affix": "kta (niṣṭhā, on jita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of the implied subject, in apposition",
        "glossaryKey": "indriya",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "jitāni indriyāṇi yena saḥ",
          "members": [
            "jita",
            "indriya"
          ]
        },
        "parts": [
          {
            "form": "jita",
            "gloss": "conquered, overcome, mastered (past passive participle of √ji)"
          },
          {
            "form": "indriya",
            "gloss": "indriya — a power of sense or action (kept in Sanskrit)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "सर्वभूतात्मभूतात्मा",
        "iast": "sarvabhūtātmabhūtātmā",
        "gloss": "whose self has become the self of all beings",
        "stem": "sarva-bhūta-ātma-bhūta-ātman",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "kta (niṣṭhā, on each bhūta) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of the implied subject, in apposition — the compound's climactic fifth epithet",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "sarveṣu bhūteṣu ātma-bhūtaḥ ātmā yasya saḥ",
          "members": [
            "sarva",
            "bhūta",
            "ātma-bhūta",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "sarva",
            "gloss": "all, every"
          },
          {
            "form": "bhūta",
            "gloss": "being, creature (past participle of √bhū: 'that which has come to be')"
          },
          {
            "form": "ātma-bhūta",
            "gloss": "become the self, identified as the self"
          },
          {
            "form": "ātman",
            "gloss": "self (the head noun)"
          }
        ],
        "note": "From body (yoga-yukta), through mind and inner self (viśuddhātmā, vijitātmā) and the outer senses (jitendriyaḥ), the four epithets build to this fifth and widest: the self realized as one with the self in every being."
      },
      {
        "i": 5,
        "deva": "कुर्वन्",
        "iast": "kurvan",
        "gloss": "doing, acting",
        "stem": "kurvat",
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the implied subject (kartṛ of lipyate); kartṛ of an unstated karman ('action')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kuru-",
            "gloss": "(the present stem of √kṛ, class 8: 'do—')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, the present active participle suffix: '—ing')"
          }
        ],
        "sandhi": "kurvann api ← kurvan + api (n doubled before a vowel after a short vowel)"
      },
      {
        "i": 6,
        "deva": "अपि",
        "iast": "api",
        "gloss": "even, although",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (concessive particle over kurvan)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "api",
            "gloss": "even, also; although (concessive, after a participle)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "negates lipyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no (simple negation)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "लिप्यते",
        "iast": "lipyate",
        "gloss": "is smeared, is stained, is defiled",
        "stem": null,
        "root": "√lip (tudādi, 6U)",
        "rootGloss": "to smear, to anoint, to stain",
        "affix": "yak (karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. passive",
        "karaka": "the verb; the implied subject ('he') stands as its passive kartā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√lip",
            "gloss": "to smear, to anoint, to stain"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "One sentence built on five nominative epithets of an unstated subject ('he') — yoga-yuktaḥ, viśuddhātmā, vijitātmā, jitendriyaḥ, sarvabhūtātmabhūtātmā — all in apposition, kartṛ of the finite verb lipyate. kurvan (śatṛ) is a concessive present participle of the same subject. api marks the concession; na negates lipyate.",
      "verbalModality": "One finite verb, lipyate (laṭ, present passive) — a flat denial, stated as standing fact. The concurrent present participle kurvan keeps the action simultaneous: the non-attachment holds even now, while he acts."
    }
  },
  {
    "locus": "5.8",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "नैव किं चित् करोमीति युक्तो मन्येत तत्त्ववित् ।\nपश्यञ् शृण्वन् स्पृशञ् जिघ्रन्न् अश्नन् गच्छन् स्वपञ् श्वसन् ॥",
    "iast": "naiva kiṃ cit karomīti yukto manyeta tattvavit |\npaśyañ śṛṇvan spṛśañ jighrann aśnan gacchan svapañ śvasan ||",
    "sense": "The disciplined knower of reality should think, 'I do nothing at all,' even while seeing, hearing, touching, smelling, eating, moving, sleeping, and breathing.",
    "english": "{5:The yoked one}, {7:the knower of reality}, should {6:think} {4:thus}: '{0:Not} {1:at all} {3:do I do} {2:anything}' — {8:seeing}, {9:hearing}, {10:touching}, {11:smelling}, {12:eating}, {13:moving}, {14:sleeping}, {15:breathing}.",
    "words": [
      {
        "i": 0,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "negates karomi, within the quoted thought",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no (simple negation)"
          }
        ],
        "sandhi": "naiva ← na + eva (a + e → ai)"
      },
      {
        "i": 1,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, at all (emphatic)",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "emphasizes na ('not at all')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, just, only, at all (emphatic particle)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "किंचित्",
        "iast": "kiṃcit",
        "gloss": "anything, something (at all)",
        "stem": "kiṃcit",
        "root": null,
        "affix": "cit (nipāta, indefinitizing particle) attached to kim",
        "morph": "acc. sg. neut. (indefinite pronoun)",
        "karaka": "karman of karomi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kim",
            "gloss": "what? (the interrogative stem, here used indefinitely)"
          },
          {
            "form": "cit",
            "gloss": "(the indefinitizing particle: 'some—, any—')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "करोमि",
        "iast": "karomi",
        "gloss": "I do, I act",
        "stem": null,
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "mip (laṭ, uttama-puruṣa ekavacana)",
        "morph": "1st sg. pres. indic. parasmaipada",
        "karaka": "the verb of the quoted thought; kartṛ the speaker himself, karman kiṃcit",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "karo-",
            "gloss": "(the present stem of √kṛ, class 8: 'do—')"
          },
          {
            "form": "-mi",
            "gloss": "(1st person singular, active)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "इति",
        "iast": "iti",
        "gloss": "thus (closing the quotation)",
        "stem": "iti",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable quotative particle",
        "karaka": "marks the preceding as a direct quotation, karman of manyeta",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "iti",
            "gloss": "thus, so (marks the end of a quotation or the content of a thought)"
          }
        ],
        "sandhi": "karomīti ← karomi + iti (i + i → ī)"
      },
      {
        "i": 5,
        "deva": "युक्तः",
        "iast": "yuktaḥ",
        "gloss": "yoked, disciplined; one who is yukta",
        "stem": "yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite; to apply oneself, to engage",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle",
        "karaka": "attribute of the implied kartṛ of manyeta, in apposition with tattvavit",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ],
        "sandhi": "yukto manyeta ← yuktaḥ + manyeta (visarga → o before a voiced consonant, here m)"
      },
      {
        "i": 6,
        "deva": "मन्येत",
        "iast": "manyeta",
        "gloss": "should think, would deem",
        "stem": null,
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "īṭ (liṅ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. optative (vidhi-liṅ), ātmanepada",
        "karaka": "the verb; kartṛ yuktaḥ tattvavit, karman the quoted thought",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√man",
            "gloss": "to think, to consider, to have in mind"
          },
          {
            "form": "-ya-",
            "gloss": "(the present-stem marker of the divādi class)"
          },
          {
            "form": "-īta",
            "gloss": "(liṅ, 3rd person singular optative, ātmanepada; manyīta → manyeta)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "तत्त्ववित्",
        "iast": "tattvavit",
        "gloss": "one who knows reality, a knower of the real",
        "stem": "tattva-vid",
        "root": "√vid (adādi, 2P)",
        "rootGloss": "to know, to be aware of, to understand",
        "affix": "kvip (kṛt, zero-affix agent noun) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of manyeta, in apposition with yuktaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (upapada, dvitīyā)",
          "vigraha": "tattvaṃ vetti saḥ — tattva-vit",
          "members": [
            "tattva",
            "vid"
          ]
        },
        "parts": [
          {
            "form": "tattva",
            "gloss": "reality, the true nature of a thing, the real"
          },
          {
            "form": "√vid",
            "gloss": "to know, to understand"
          },
          {
            "form": "-vit",
            "gloss": "(kvip, the zero-affix kṛt: 'the one who knows —')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "पश्यन्",
        "iast": "paśyan",
        "gloss": "seeing",
        "stem": "paśyat",
        "root": "√dṛś (bhvādi, 1P; paśya- is the suppletive present stem)",
        "rootGloss": "to see, to look at, to behold",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject (yuktaḥ tattvavit); the first of eight, listing his ordinary bodily activity",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "paśya-",
            "gloss": "(the present-stem substitute for √dṛś: 'see—')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, present active participle: '—ing')"
          }
        ],
        "sandhi": "paśyañ śṛṇvan ← paśyan + śṛṇvan (n → ñ before a palatal consonant, here ś)"
      },
      {
        "i": 9,
        "deva": "शृण्वन्",
        "iast": "śṛṇvan",
        "gloss": "hearing",
        "stem": "śṛṇvat",
        "root": "√śru (svādi, 5P)",
        "rootGloss": "to hear, to listen",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "śṛṇu-",
            "gloss": "(the present stem of √śru, class 5: 'hear—')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing', with u → v before the vowel-initial suffix)"
          }
        ]
      },
      {
        "i": 10,
        "deva": "स्पृशन्",
        "iast": "spṛśan",
        "gloss": "touching",
        "stem": "spṛśat",
        "root": "√spṛś (tudādi, 6P)",
        "rootGloss": "to touch",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√spṛś",
            "gloss": "to touch"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ],
        "sandhi": "spṛśañ jighran ← spṛśan + jighran (n → ñ before a palatal consonant, here j)"
      },
      {
        "i": 11,
        "deva": "जिघ्रन्",
        "iast": "jighran",
        "gloss": "smelling",
        "stem": "jighrat",
        "root": "√ghrā (juhotyādi, 3P)",
        "rootGloss": "to smell",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ji-",
            "gloss": "(the reduplication syllable of the juhotyādi class)"
          },
          {
            "form": "ghra-",
            "gloss": "(the present stem of √ghrā: 'smell—', vowel shortened)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ],
        "sandhi": "jighrann aśnan ← jighran + aśnan (n doubled before a vowel after a short vowel)"
      },
      {
        "i": 12,
        "deva": "अश्नन्",
        "iast": "aśnan",
        "gloss": "eating",
        "stem": "aśnat",
        "root": "√aś (kryādi, 9P)",
        "rootGloss": "to eat, to consume, to devour",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "aśnā-",
            "gloss": "(the present stem of √aś, class 9: 'eat—')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing', stem vowel shortened before the consonantal ending)"
          }
        ]
      },
      {
        "i": 13,
        "deva": "गच्छन्",
        "iast": "gacchan",
        "gloss": "going, moving about",
        "stem": "gacchat",
        "root": "√gam (bhvādi, 1P)",
        "rootGloss": "to go, to move",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√gam",
            "gloss": "to go, to move"
          },
          {
            "form": "-accha-",
            "gloss": "(śa, the present-stem marker of the bhvādi class, with the root's irregular gam → gacch)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ]
      },
      {
        "i": 14,
        "deva": "स्वपन्",
        "iast": "svapan",
        "gloss": "sleeping",
        "stem": "svapat",
        "root": "√svap (adādi, 2P)",
        "rootGloss": "to sleep",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√svap",
            "gloss": "to sleep"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, present active participle: '—ing')"
          }
        ],
        "sandhi": "svapañ śvasan ← svapan + śvasan (n → ñ before a palatal consonant, here ś)"
      },
      {
        "i": 15,
        "deva": "श्वसन्",
        "iast": "śvasan",
        "gloss": "breathing",
        "stem": "śvasat",
        "root": "√śvas (adādi, 2P)",
        "rootGloss": "to breathe",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject; the eighth and last of the list",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√śvas",
            "gloss": "to breathe"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, present active participle: '—ing')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "manyeta (liṅ, optative) is the main verb, its kartṛ the compound subject yuktaḥ tattvavit; its karman is the quoted thought naiva kiṃcit karomi — itself built on the finite karomi (kartṛ the speaker himself, karman kiṃcit). Eight further present participles (paśyan…śvasan), all nom. sg. masc., are concessive attributes of the same subject, listing the ordinary acts of the body he continues to perform.",
      "verbalModality": "manyeta is optative (liṅ) — an instruction in what he 'should' think, not a report of fact. Inside the quotation, karomi is a plain present indicative. The eight participles are all present active (śatṛ), holding the whole list of bodily acts as concurrent with the thought."
    }
  },
  {
    "locus": "5.9",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "प्रलपन् विसृजन् गृह्णन्न् उन्मिषन् निमिषन्न् अपि ।\nइन्द्रियाणीन्द्रियार्थेषु वर्तन्त इति धारयन् ॥",
    "iast": "pralapan visṛjan gṛhṇann unmiṣan nimiṣann api |\nindriyāṇīndriyārtheṣu vartanta iti dhārayan ||",
    "sense": "Talking, releasing, grasping, opening and closing the eyes — through it all, holding to the thought that it is only the indriyas moving among their own objects.",
    "english": "{0:Speaking}, {1:releasing}, {2:grasping}, {3:opening the eyes}, {4:closing the eyes} — {5:even so} — {10:holding} {9:that} '{6:the indriyas} {8:move} {7:among the objects of the indriyas}.'",
    "words": [
      {
        "i": 0,
        "deva": "प्रलपन्",
        "iast": "pralapan",
        "gloss": "speaking, talking, conversing",
        "stem": "pralapat",
        "root": "√lap (bhvādi, 1P)",
        "rootGloss": "to speak, to talk, to prattle",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject, continuing the list from 5.8",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, out (an extending prefix)"
          },
          {
            "form": "√lap",
            "gloss": "to speak, to talk, to prattle"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "विसृजन्",
        "iast": "visṛjan",
        "gloss": "releasing, letting go, emitting",
        "stem": "visṛjat",
        "root": "√sṛj (tudādi, 6P)",
        "rootGloss": "to emit, to let go, to release; to create",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "vi-",
            "gloss": "apart, away (dispersive prefix)"
          },
          {
            "form": "√sṛj",
            "gloss": "to emit, to let go, to release"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ],
        "note": "Paired here with the body's ordinary acts (5.8's list continues), visṛjan carries √sṛj's plain sense of releasing/letting go, not the cosmological 'emitting, creating' the same root carries elsewhere in the Gītā."
      },
      {
        "i": 2,
        "deva": "गृह्णन्",
        "iast": "gṛhṇan",
        "gloss": "grasping, taking hold of, receiving",
        "stem": "gṛhṇat",
        "root": "√grah (kryādi, 9U)",
        "rootGloss": "to seize, to grasp, to take hold of, to receive",
        "affix": "śnā (vikaraṇa, kryādi class) + śatṛ (kṛt)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√grah",
            "gloss": "to seize, to grasp, to take hold of"
          },
          {
            "form": "-ṇā-",
            "gloss": "(śnā, the present-stem infix of the kryādi class, reduced to -ṇ- before the consonantal ending)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ],
        "sandhi": "gṛhṇann unmiṣan ← gṛhṇan + unmiṣan (n doubled before a vowel after a short vowel)"
      },
      {
        "i": 3,
        "deva": "उन्मिषन्",
        "iast": "unmiṣan",
        "gloss": "opening the eyes, blinking open",
        "stem": "unmiṣat",
        "root": "√miṣ (bhvādi, 1P)",
        "rootGloss": "to blink, to open the eyes",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject, paired with nimiṣan",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ud-",
            "gloss": "up, open (the prefix, as un- before m)"
          },
          {
            "form": "√miṣ",
            "gloss": "to blink, to open the eyes"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "निमिषन्",
        "iast": "nimiṣan",
        "gloss": "closing the eyes, blinking shut",
        "stem": "nimiṣat",
        "root": "√miṣ (bhvādi, 1P)",
        "rootGloss": "to blink, to open or close the eyes",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; present active participle",
        "karaka": "concessive attribute of the subject, paired with unmiṣan",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ni-",
            "gloss": "down, shut (the prefix, closing)"
          },
          {
            "form": "√miṣ",
            "gloss": "to blink, to open or close the eyes"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ: '—ing')"
          }
        ],
        "sandhi": "nimiṣann api ← nimiṣan + api (n doubled before a vowel after a short vowel)"
      },
      {
        "i": 5,
        "deva": "अपि",
        "iast": "api",
        "gloss": "even, also",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (concessive particle closing the five-participle list)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "api",
            "gloss": "even, also; although (concessive)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "इन्द्रियाणि",
        "iast": "indriyāṇi",
        "gloss": "the indriyas — the powers of sense and action",
        "stem": "indriya",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. neut.",
        "karaka": "kartṛ of vartante",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          {
            "form": "indra",
            "gloss": "Indra; the lord, the ruling power"
          },
          {
            "form": "-iya",
            "gloss": "(taddhita ghac: 'belonging to Indra' — hence a power of the indwelling ruler)"
          }
        ],
        "sandhi": "indriyāṇīndriyārtheṣu ← indriyāṇi + indriyārtheṣu (i + i → ī)"
      },
      {
        "i": 7,
        "deva": "इन्द्रियार्थेषु",
        "iast": "indriyārtheṣu",
        "gloss": "among the objects of the indriyas",
        "stem": "indriya-artha",
        "root": null,
        "affix": "sup (saptamī bahuvacana)",
        "morph": "loc. pl. masc.",
        "karaka": "adhikaraṇa (locus) of vartante",
        "glossaryKey": "visaya",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "indriyāṇām arthāḥ",
          "members": [
            "indriya",
            "artha"
          ]
        },
        "parts": [
          {
            "form": "indriya",
            "gloss": "indriya — a power of sense or action (kept in Sanskrit)"
          },
          {
            "form": "artha",
            "gloss": "object, purpose; the thing aimed at or apprehended"
          }
        ],
        "note": "The repetition — the indriyas moving among the indriyas' own objects — is in the Sanskrit itself: what is held in mind is that only sense meets sense-object, nothing more, no self in it."
      },
      {
        "i": 8,
        "deva": "वर्तन्ते",
        "iast": "vartante",
        "gloss": "move, occupy themselves, are engaged",
        "stem": null,
        "root": "√vṛt (bhvādi, 1Ā)",
        "rootGloss": "to turn, to move, to revolve; to be engaged, to occupy oneself",
        "affix": "jha (laṭ, prathama-puruṣa bahuvacana ātmanepada)",
        "morph": "3rd pl. pres. indic. ātmanepada",
        "karaka": "the verb of the embedded clause; kartṛ indriyāṇi, adhikaraṇa indriyārtheṣu",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√vṛt",
            "gloss": "to turn, to move; to be engaged, to occupy oneself"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-nte",
            "gloss": "(3rd person plural, ātmanepada)"
          }
        ],
        "sandhi": "vartanta iti ← vartante + iti (word-final e shortens to a before iti)"
      },
      {
        "i": 9,
        "deva": "इति",
        "iast": "iti",
        "gloss": "that (introducing the content of the thought)",
        "stem": "iti",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable quotative particle",
        "karaka": "marks the preceding clause as the content held by dhārayan",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "iti",
            "gloss": "thus, so (marks the content of a thought held in mind)"
          }
        ]
      },
      {
        "i": 10,
        "deva": "धारयन्",
        "iast": "dhārayan",
        "gloss": "holding in mind, maintaining the thought, sustaining",
        "stem": "dhārayat",
        "root": "√dhṛ (bhvādi, 1P)",
        "rootGloss": "to hold, to bear, to sustain",
        "affix": "ṇic (causative) + śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; causative present active participle",
        "karaka": "the verse's main participle; kartṛ the same implied subject (tattvavit), karman the whole preceding clause",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√dhṛ",
            "gloss": "to hold, to bear, to sustain"
          },
          {
            "form": "-aya-",
            "gloss": "(ṇic, the causative marker: 'to make—hold', hence 'to maintain')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, present active participle: '—ing')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Five more concessive present participles (pralapan…nimiṣan) continue the subject from 5.8, followed by api. dhārayan, the verse's main participle, governs the embedded clause indriyāṇi indriyārtheṣu vartante iti — vartante (laṭ) with kartṛ indriyāṇi and adhikaraṇa indriyārtheṣu.",
      "verbalModality": "No independent finite verb for the subject himself — only the embedded vartante, which describes the indriyas, not him. The whole sentence (spanning 5.8–5.9) is a chain of participles culminating in dhārayan: he does nothing but hold this understanding."
    }
  },
  {
    "locus": "5.10",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "ब्रह्मण्य् आधाय कर्माणि सङ्गं त्यक्त्वा करोति यः ।\nलिप्यते न स पापेन पद्मपत्रम् इवाम्भसा ॥",
    "iast": "brahmaṇy ādhāya karmāṇi saṅgaṃ tyaktvā karoti yaḥ |\nlipyate na sa pāpena padmapatram ivāmbhasā ||",
    "sense": "Whoever acts having consigned his works to Brahman and given up clinging is not stained by evil, as a lotus-leaf is not wetted by water.",
    "english": "{6:Whoever}, {0:in Brahman} {1:having placed} {2:karmas}, {4:having abandoned} {3:clinging}, {5:acts} — {9:he} {7:is} {8:not} {10:stained by evil}, {12:as} {11:a lotus-leaf} {13:by water}.",
    "words": [
      {
        "i": 0,
        "deva": "ब्रह्मणि",
        "iast": "brahmaṇi",
        "gloss": "in Brahman",
        "stem": "brahman",
        "root": "√bṛh (bhvādi, 1P)",
        "rootGloss": "to grow, to swell, to become great, to expand",
        "affix": "manin (kṛt, unādi) + ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa (locus) of ādhāya",
        "glossaryKey": "brahman",
        "translatable": true,
        "parts": [
          {
            "form": "√bṛh",
            "gloss": "to grow, to swell, to become great, to expand (the traditional derivation)"
          },
          {
            "form": "-man",
            "gloss": "(unādi manin, forming the primary noun: 'the vast, the great')"
          },
          {
            "form": "-i",
            "gloss": "(locative singular: 'in, upon')"
          }
        ],
        "note": "Neuter Brahman, the impersonal absolute — distinct from masculine brahmā (the creator-god) and from brāhmaṇa (a brahmin)."
      },
      {
        "i": 1,
        "deva": "आधाय",
        "iast": "ādhāya",
        "gloss": "having placed, having laid down, having consigned",
        "stem": null,
        "root": "√dhā (juhotyādi, 3U)",
        "rootGloss": "to place, to put, to lay; to bestow, to set down",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (yaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ā-",
            "gloss": "unto, upon, towards"
          },
          {
            "form": "√dhā",
            "gloss": "to place, to put, to lay"
          },
          {
            "form": "-ya",
            "gloss": "(lyap: 'having —ed', the absolutive used when the root carries a prefix)"
          }
        ],
        "sandhi": "brahmaṇy ādhāya ← brahmaṇi + ādhāya (i → y before a dissimilar vowel)",
        "note": "The absolutive fixes the order: the consigning of works into Brahman comes first; the acting that follows is done from within that prior disposition, not the reverse."
      },
      {
        "i": 2,
        "deva": "कर्माणि",
        "iast": "karmāṇi",
        "gloss": "karmas, actions, works",
        "stem": "karman",
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "man (kṛt) + śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "karman of ādhāya",
        "glossaryKey": "karma",
        "translatable": false,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act"
          },
          {
            "form": "-man",
            "gloss": "(the kṛt affix forming the neuter action-noun: 'the doing, the deed')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "सङ्गम्",
        "iast": "saṅgam",
        "gloss": "clinging, attachment",
        "stem": "saṅga",
        "root": "√sañj (bhvādi, 1P)",
        "rootGloss": "to cling, to adhere, to stick to",
        "affix": "ghañ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of tyaktvā",
        "glossaryKey": "sanga",
        "translatable": true,
        "parts": [
          {
            "form": "√sañj",
            "gloss": "to cling, to adhere, to stick to"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the sticking, the clinging')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "त्यक्त्वा",
        "iast": "tyaktvā",
        "gloss": "having abandoned, having given up, having relinquished",
        "stem": null,
        "root": "√tyaj (bhvādi, 1P)",
        "rootGloss": "to abandon, to give up, to relinquish, to leave",
        "affix": "ktvā (kṛt, absolutive)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (yaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√tyaj",
            "gloss": "to abandon, to give up, to relinquish"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "करोति",
        "iast": "karoti",
        "gloss": "does, acts, performs",
        "stem": null,
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ yaḥ, karman karmāṇi (carried over)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "karo-",
            "gloss": "(the present stem of √kṛ, class 8: 'do—')"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who, whoever",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of ādhāya, tyaktvā, karoti; correlative antecedent of sa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative pronoun stem)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "लिप्यते",
        "iast": "lipyate",
        "gloss": "is smeared, is stained, is defiled",
        "stem": null,
        "root": "√lip (tudādi, 6U)",
        "rootGloss": "to smear, to anoint, to stain",
        "affix": "yak (karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. passive",
        "karaka": "the verb; sa stands as its passive kartā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√lip",
            "gloss": "to smear, to anoint, to stain"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "negates lipyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no (simple negation)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "स",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of lipyate; correlative resuming yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, he (the anaphoric/correlative demonstrative)"
          }
        ]
      },
      {
        "i": 10,
        "deva": "पापेन",
        "iast": "pāpena",
        "gloss": "by evil, by sin",
        "stem": "pāpa",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of lipyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pāpa",
            "gloss": "evil, wrong, sin"
          },
          {
            "form": "-ena",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ]
      },
      {
        "i": 11,
        "deva": "पद्मपत्रम्",
        "iast": "padmapatram",
        "gloss": "a lotus-leaf",
        "stem": "padma-patra",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartā of the elided lipyate, in the simile clause (upamāna)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "padmasya patram",
          "members": [
            "padma",
            "patra"
          ]
        },
        "parts": [
          {
            "form": "padma",
            "gloss": "lotus"
          },
          {
            "form": "patra",
            "gloss": "leaf, petal"
          }
        ]
      },
      {
        "i": 12,
        "deva": "इव",
        "iast": "iva",
        "gloss": "as, like",
        "stem": "iva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle of comparison",
        "karaka": "— (marks the whole clause as a simile)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "iva",
            "gloss": "like, as if, as it were"
          }
        ]
      },
      {
        "i": 13,
        "deva": "अम्भसा",
        "iast": "ambhasā",
        "gloss": "by water",
        "stem": "ambhas",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of the elided lipyate, parallel to pāpena",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ambhas",
            "gloss": "water"
          },
          {
            "form": "-ā",
            "gloss": "(instrumental singular of a neuter -as stem: 'by, with')"
          }
        ],
        "sandhi": "padmapatram ivāmbhasā ← padmapatram + iva + ambhasā (a + a → ā)"
      }
    ],
    "grammar": {
      "karakaSummary": "yaḥ (kartṛ) governs three predicates: the absolutive ādhāya (karman karmāṇi, locus brahmaṇi), the absolutive tyaktvā (karman saṅgam), and the finite karoti. The correlative sa resumes the subject as kartṛ of lipyate; pāpena is karaṇa. The simile clause (padmapatram iva ambhasā) elides its own verb, understood as the same lipyate; padmapatram stands as its nominative subject, ambhasā as its karaṇa.",
      "verbalModality": "Two absolutives (ādhāya, tyaktvā) sequence prior acts before the two present-tense finite verbs, karoti and lipyate (the second negated) — the placing and the relinquishing are done, and then, as an ongoing present fact, he acts without being stained."
    }
  },
  {
    "locus": "5.11",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "कायेन मनसा बुद्ध्या केवलैर् इन्द्रियैर् अपि ।\nयोगिनः कर्म कुर्वन्ति सङ्गं त्यक्त्वात्मशुद्धये ॥",
    "iast": "kāyena manasā buddhyā kevalair indriyair api |\nyoginaḥ karma kurvanti saṅgaṃ tyaktvātmaśuddhaye ||",
    "sense": "Yogins act with body, with manas, with buddhi, even with the bare indriyas alone, having given up clinging, for the purification of the self.",
    "english": "{6:Yogins} {8:perform} {7:karma} {0:with the body}, {1:with manas}, {2:with buddhi}, {5:even} {3:with the indriyas} {4:alone} — {10:having given up} {9:clinging} — {11:for the purification of the self}.",
    "words": [
      {
        "i": 0,
        "deva": "कायेन",
        "iast": "kāyena",
        "gloss": "by/with the body",
        "stem": "kāya",
        "root": "√ci (svādi, 5U)",
        "rootGloss": "to gather, to heap up, to accumulate",
        "affix": "ghañ (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of kurvanti",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ci",
            "gloss": "to gather, to heap up, to accumulate (the traditional derivation)"
          },
          {
            "form": "-āya",
            "gloss": "(ghañ, the result-noun with vṛddhi: 'that which is accumulated' — the body)"
          },
          {
            "form": "-ena",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "मनसा",
        "iast": "manasā",
        "gloss": "manas — the faculty that intends, hesitates and turns things over",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "asun (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of kurvanti",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          {
            "form": "√man",
            "gloss": "to think, to consider, to have in mind"
          },
          {
            "form": "-as",
            "gloss": "(asun, the neuter action/agent noun)"
          },
          {
            "form": "-ā",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "बुद्ध्या",
        "iast": "buddhyā",
        "gloss": "buddhi — the faculty that discriminates and settles a matter",
        "stem": "buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ktin (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. fem.",
        "karaka": "karaṇa of kurvanti",
        "glossaryKey": "buddhi",
        "translatable": false,
        "parts": [
          {
            "form": "√budh",
            "gloss": "to wake, to be aware of, to understand"
          },
          {
            "form": "-ti",
            "gloss": "(ktin, the feminine action-noun: 'the awakening / the understanding')"
          },
          {
            "form": "-ā",
            "gloss": "(instrumental singular of an i-stem, as -yā: 'by, with')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "केवलैः",
        "iast": "kevalaiḥ",
        "gloss": "alone, mere, unaided — by themselves",
        "stem": "kevala",
        "root": null,
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. masc.",
        "karaka": "attribute of indriyaiḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kevala",
            "gloss": "alone, only, mere; isolated, unaccompanied"
          },
          {
            "form": "-aiḥ",
            "gloss": "(instrumental plural: 'by, with')"
          }
        ],
        "note": "kevala marks the indriyas as acting bare, on their own — without an ego's 'I do this' riding on top of them, continuing the stance of 5.8–9."
      },
      {
        "i": 4,
        "deva": "इन्द्रियैः",
        "iast": "indriyaiḥ",
        "gloss": "the indriyas — the powers of sense and action",
        "stem": "indriya",
        "root": null,
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. neut.",
        "karaka": "karaṇa of kurvanti",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          {
            "form": "indra",
            "gloss": "Indra; the lord, the ruling power"
          },
          {
            "form": "-iya",
            "gloss": "(taddhita ghac: 'belonging to Indra' — hence a power of the indwelling ruler)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "अपि",
        "iast": "api",
        "gloss": "even",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (emphasizes kevalair indriyaiḥ, the fourth and most reduced karaṇa)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "api",
            "gloss": "even, also"
          }
        ]
      },
      {
        "i": 6,
        "deva": "योगिनः",
        "iast": "yoginaḥ",
        "gloss": "yogins, the disciplined",
        "stem": "yogin",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite; to apply oneself, to engage",
        "affix": "ini (taddhita) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of kurvanti",
        "glossaryKey": "yoga",
        "translatable": false,
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga — disciplined practice (kept in Sanskrit)"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'the one who has —')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "कर्म",
        "iast": "karma",
        "gloss": "karma, action",
        "stem": "karman",
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "man (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of kurvanti",
        "glossaryKey": "karma",
        "translatable": false,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act"
          },
          {
            "form": "-man",
            "gloss": "(the kṛt affix forming the neuter action-noun: 'the doing, the deed')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "कुर्वन्ति",
        "iast": "kurvanti",
        "gloss": "do, perform, undertake",
        "stem": null,
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "jhi (laṭ, prathama-puruṣa bahuvacana)",
        "morph": "3rd pl. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ yoginaḥ, karman karma, karaṇa kāyena/manasā/buddhyā/indriyaiḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kurv-",
            "gloss": "(the present stem of √kṛ, class 8, before a vowel-initial ending: 'do—')"
          },
          {
            "form": "-anti",
            "gloss": "(3rd person plural, active)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "सङ्गम्",
        "iast": "saṅgam",
        "gloss": "clinging, attachment",
        "stem": "saṅga",
        "root": "√sañj (bhvādi, 1P)",
        "rootGloss": "to cling, to adhere, to stick to",
        "affix": "ghañ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of tyaktvā",
        "glossaryKey": "sanga",
        "translatable": true,
        "parts": [
          {
            "form": "√sañj",
            "gloss": "to cling, to adhere, to stick to"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the sticking, the clinging')"
          }
        ]
      },
      {
        "i": 10,
        "deva": "त्यक्त्वा",
        "iast": "tyaktvā",
        "gloss": "having abandoned, having given up, having relinquished",
        "stem": null,
        "root": "√tyaj (bhvādi, 1P)",
        "rootGloss": "to abandon, to give up, to relinquish, to leave",
        "affix": "ktvā (kṛt, absolutive)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (yoginaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√tyaj",
            "gloss": "to abandon, to give up, to relinquish"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ],
        "sandhi": "saṅgaṃ tyaktvātmaśuddhaye ← tyaktvā + ātmaśuddhaye (ā + ā → ā)"
      },
      {
        "i": 11,
        "deva": "आत्मशुद्धये",
        "iast": "ātmaśuddhaye",
        "gloss": "for the purification of the self",
        "stem": "ātma-śuddhi",
        "root": "√śudh (divādi, 4P)",
        "rootGloss": "to become clean, to become pure",
        "affix": "ktin (kṛt) + ṅe (caturthī ekavacana)",
        "morph": "dat. sg. fem.",
        "karaka": "sampradāna (purpose) of kurvanti",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "ātmanaḥ śuddhiḥ, tasyai",
          "members": [
            "ātman",
            "śuddhi"
          ]
        },
        "parts": [
          {
            "form": "ātman",
            "gloss": "self"
          },
          {
            "form": "√śudh",
            "gloss": "to become clean, to become pure"
          },
          {
            "form": "-ti",
            "gloss": "(ktin, the feminine action-noun: 'the purifying, the purification')"
          },
          {
            "form": "-e",
            "gloss": "(dative singular: 'for, for the sake of')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "yoginaḥ (kartṛ) governs kurvanti (finite verb), with karma as karman and four instrumentals in series as karaṇa (kāyena, manasā, buddhyā, indriyaiḥ, the last qualified by kevalaiḥ and api). tyaktvā (absolutive) sequences the prior relinquishing of saṅgam; ātmaśuddhaye (dative) states the purpose.",
      "verbalModality": "One finite verb, kurvanti (laṭ, present plural) — a general, ongoing description of what yogins do. The absolutive tyaktvā again fixes the abandoning of clinging as prior to, and the standing condition for, the acting."
    }
  },
  {
    "locus": "5.12",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "युक्तः कर्मफलं त्यक्त्वा शान्तिम् आप्नोति नैष्ठिकीम् ।\nअयुक्तः कामकारेण फले सक्तो निबध्यते ॥",
    "iast": "yuktaḥ karmaphalaṃ tyaktvā śāntim āpnoti naiṣṭhikīm |\nayuktaḥ kāmakāreṇa phale sakto nibadhyate ||",
    "sense": "The yoked one, having given up the fruit of karma, attains the final peace; the undisciplined one, driven by kāma's working and clinging to the fruit, is bound.",
    "english": "{0:The yoked one}, {2:having given up} {1:the fruit of karma}, {4:attains} {5:the final} {3:peace}; {6:the undisciplined one}, {7:through the working of kāma}, {9:clinging} {8:to the fruit}, {10:is bound}.",
    "words": [
      {
        "i": 0,
        "deva": "युक्तः",
        "iast": "yuktaḥ",
        "gloss": "yoked, disciplined; one who is yukta",
        "stem": "yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite; to apply oneself, to engage",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle",
        "karaka": "kartṛ of āpnoti",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "कर्मफलम्",
        "iast": "karmaphalam",
        "gloss": "the fruit of karma",
        "stem": "karma-phala",
        "root": "√phal (bhvādi, 1P)",
        "rootGloss": "to burst open, to ripen, to bear fruit",
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of tyaktvā",
        "glossaryKey": "karma",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "karmaṇaḥ phalam",
          "members": [
            "karma",
            "phala"
          ]
        },
        "parts": [
          {
            "form": "karma",
            "gloss": "karma — action, and its binding result (kept in Sanskrit)"
          },
          {
            "form": "phala",
            "gloss": "fruit, result; the ripened outcome of an action"
          }
        ]
      },
      {
        "i": 2,
        "deva": "त्यक्त्वा",
        "iast": "tyaktvā",
        "gloss": "having abandoned, having given up, having relinquished",
        "stem": null,
        "root": "√tyaj (bhvādi, 1P)",
        "rootGloss": "to abandon, to give up, to relinquish, to leave",
        "affix": "ktvā (kṛt, absolutive)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (yuktaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√tyaj",
            "gloss": "to abandon, to give up, to relinquish"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "शान्तिम्",
        "iast": "śāntim",
        "gloss": "peace, tranquility",
        "stem": "śānti",
        "root": "√śam (divādi, 4P)",
        "rootGloss": "to become calm, to be pacified, to grow quiet",
        "affix": "ktin (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. fem.",
        "karaka": "karman of āpnoti",
        "glossaryKey": "santi",
        "translatable": true,
        "parts": [
          {
            "form": "√śam",
            "gloss": "to become calm, to be pacified, to grow quiet"
          },
          {
            "form": "-ti",
            "gloss": "(ktin, the feminine action-noun: 'the becoming calm, peace')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "आप्नोति",
        "iast": "āpnoti",
        "gloss": "attains, reaches, obtains",
        "stem": null,
        "root": "√āp (svādi, 5P)",
        "rootGloss": "to obtain, to reach, to attain",
        "affix": "tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ yuktaḥ, karman śāntim",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√āp",
            "gloss": "to obtain, to reach, to attain"
          },
          {
            "form": "-no-",
            "gloss": "(śnu, the present-stem infix of the svādi class)"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "नैष्ठिकीम्",
        "iast": "naiṣṭhikīm",
        "gloss": "final, absolute, grounded in steadfastness",
        "stem": "naiṣṭhikī",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to stand firm, to abide, to be situated",
        "affix": "ṭhaK (taddhita) + ṅīp (strī-pratyaya) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. fem.",
        "karaka": "attribute of śāntim",
        "glossaryKey": "nistha",
        "translatable": true,
        "parts": [
          {
            "form": "ni-√sthā",
            "gloss": "steadfastness, being grounded (niṣṭhā, ni + √sthā)"
          },
          {
            "form": "-ika",
            "gloss": "(taddhita ṭhaK, with vṛddhi: 'belonging to, resulting from —')"
          }
        ],
        "note": "naiṣṭhikī qualifies śānti as the final, settled peace — grounded in steadfast discipline, not a passing calm."
      },
      {
        "i": 6,
        "deva": "अयुक्तः",
        "iast": "ayuktaḥ",
        "gloss": "undisciplined, not yoked",
        "stem": "a-yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to join, to unite; to apply oneself, to engage",
        "affix": "nañ + kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; negated past passive participle",
        "karaka": "kartṛ of nibadhyate",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "a-",
            "gloss": "not (the negative prefix nañ)"
          },
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "कामकारेण",
        "iast": "kāmakāreṇa",
        "gloss": "through the working of kāma, by desire's action",
        "stem": "kāma-kāra",
        "root": "√kṛ (ḍukṛñ, tanādi, 8U)",
        "rootGloss": "to do, to make, to act",
        "affix": "ghañ (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "hetu (cause) / karaṇa of nibadhyate",
        "glossaryKey": "kama",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (tṛtīyā)",
          "vigraha": "kāmena kāraḥ",
          "members": [
            "kāma",
            "kāra"
          ]
        },
        "parts": [
          {
            "form": "kāma",
            "gloss": "kāma — desire as craving, the wanting that reaches for its object (kept in Sanskrit)"
          },
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun with guṇa: 'the doing, the working')"
          }
        ],
        "note": "kāma-kāra names desire not as passive craving but as an active force that does something to the agent — the direct contrast to the yukta's tyaktvā."
      },
      {
        "i": 8,
        "deva": "फले",
        "iast": "phale",
        "gloss": "in the fruit, upon the result",
        "stem": "phala",
        "root": "√phal (bhvādi, 1P)",
        "rootGloss": "to burst open, to ripen, to bear fruit",
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa (locus) of saktaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√phal",
            "gloss": "to burst open, to ripen, to bear fruit"
          },
          {
            "form": "-a",
            "gloss": "(the result-noun ending: 'that which ripens' — the fruit)"
          },
          {
            "form": "-e",
            "gloss": "(locative singular: 'in, upon')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "सक्तः",
        "iast": "saktaḥ",
        "gloss": "clinging, attached, stuck",
        "stem": "sakta",
        "root": "√sañj (bhvādi, 1P)",
        "rootGloss": "to cling, to adhere, to stick to",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive participle",
        "karaka": "predicate attribute of the implied subject (ayuktaḥ), kartā of nibadhyate",
        "glossaryKey": "sanga",
        "translatable": true,
        "parts": [
          {
            "form": "√sañj",
            "gloss": "to cling, to adhere, to stick to"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed', hence 'stuck, clinging')"
          }
        ],
        "sandhi": "sakto nibadhyate ← saktaḥ + nibadhyate (visarga → o before a voiced consonant, here n)"
      },
      {
        "i": 10,
        "deva": "निबध्यते",
        "iast": "nibadhyate",
        "gloss": "is bound, is fettered",
        "stem": null,
        "root": "√bandh (kryādi, 9U)",
        "rootGloss": "to bind, to tie, to fetter",
        "affix": "ni- (prefix) + yak (karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. passive",
        "karaka": "the verb; the implied ayuktaḥ stands as its passive kartā, kāmakāreṇa as hetu",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ni-",
            "gloss": "down, fast (intensifying the binding)"
          },
          {
            "form": "√bandh",
            "gloss": "to bind, to tie, to fetter"
          },
          {
            "form": "-ya-",
            "gloss": "(yak, the passive marker, with the root's nasal dropped: badh-)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Two parallel clauses. First: yuktaḥ (kartṛ) — tyaktvā (absolutive, karman karma-phalam) — āpnoti (finite verb, karman śāntim naiṣṭhikīm). Second: ayuktaḥ (kartṛ) — kāma-kāreṇa (hetu/karaṇa) — phale (adhikaraṇa) — saktaḥ (predicate participle) — nibadhyate (finite verb, passive).",
      "verbalModality": "Two finite verbs in direct contrast: āpnoti (active, 'attains') for the yukta, nibadhyate (passive, 'is bound') for the ayukta — the grammar itself enacts the difference between an agent's attainment and a patient's being acted upon."
    }
  },
  {
    "locus": "5.13",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "सर्वकर्माणि मनसा संन्यस्यास्ते सुखं वशी ।\nनवद्वारे पुरे देही नैव कुर्वन् न कारयन् ॥",
    "iast": "sarvakarmāṇi manasā saṃnyasyāste sukhaṃ vaśī |\nnavadvāre pure dehī naiva kurvan na kārayan ||",
    "sense": "Having mentally renounced all karma, the self-controlled one dwells at ease — the embodied one, in the nine-gated city of the body, neither acting nor causing anything to be done.",
    "english": "{2:Having renounced} {0:all karmas} {1:by manas}, {5:the master of himself} {3:dwells} {4:at ease} — {8:the embodied one}, {7:in the city} {6:of nine gates}, {9:not} {10:at all} {11:acting}, {12:nor} {13:causing to act}.",
    "words": [
      {
        "i": 0,
        "deva": "सर्वकर्माणि",
        "iast": "sarva-karmāṇi",
        "gloss": "all karma, every action",
        "stem": "sarva-karman",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "karman of saṃnyasya",
        "glossaryKey": "karma",
        "translatable": true,
        "compound": {
          "type": "karmadhāraya",
          "vigraha": "sarvāṇi karmāṇi",
          "members": [
            "sarva",
            "karman"
          ]
        },
        "parts": [
          {
            "form": "sarva",
            "gloss": "all, every, entire"
          },
          {
            "form": "karman",
            "gloss": "karma — action, deed, work; rite, performance"
          }
        ],
        "note": "karma is kept untranslated throughout per house policy (§8); sarva- is the only translated element of the compound."
      },
      {
        "i": 1,
        "deva": "मनसा",
        "iast": "manasā",
        "gloss": "manas — with the mind, mentally",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of saṃnyasya",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          {
            "form": "√man",
            "gloss": "to think, to consider, to have in mind"
          },
          {
            "form": "-as",
            "gloss": "(asun, the neuter action-noun suffix)"
          },
          {
            "form": "-ā",
            "gloss": "(instrumental singular ending on a consonant stem: 'by, with')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "संन्यस्य",
        "iast": "saṃnyasya",
        "gloss": "having renounced, having laid down completely",
        "stem": null,
        "root": "√as (divādi, 4P)",
        "rootGloss": "to throw, to cast",
        "affix": "lyap (the ktvā-absolutive after a prefixed root)",
        "morph": "absolutive (gerund); indeclinable",
        "karaka": "prior action to āste; its kartṛ is vaśī/dehī, its karman sarva-karmāṇi",
        "glossaryKey": "samnyasa",
        "translatable": true,
        "parts": [
          {
            "form": "sam-",
            "gloss": "completely, together"
          },
          {
            "form": "ni-",
            "gloss": "down"
          },
          {
            "form": "√as",
            "gloss": "to throw, to cast"
          },
          {
            "form": "-ya",
            "gloss": "(lyap, the absolutive suffix after a prefixed root: 'having —ed')"
          }
        ],
        "sandhi": "saṃnyasyāste ← saṃnyasya + āste (a + ā → ā)"
      },
      {
        "i": 3,
        "deva": "आस्ते",
        "iast": "āste",
        "gloss": "sits, remains, abides, dwells",
        "stem": null,
        "root": "√ās (adādi, 2Ā)",
        "rootGloss": "to sit, to remain, to abide, to dwell",
        "affix": "ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ vaśī (= dehī)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ās",
            "gloss": "to sit, to remain, to abide, to dwell"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ],
        "note": "Śaṅkara glosses āste as tiṣṭhati, 'simply remains as he is' — not literal sitting."
      },
      {
        "i": 4,
        "deva": "सुखम्",
        "iast": "sukham",
        "gloss": "happily, at ease, in comfort",
        "stem": "sukha",
        "root": null,
        "affix": "am (dvitīyā ekavacana, used adverbially)",
        "morph": "acc. sg. neut. (adverbial)",
        "karaka": "kriyā-viśeṣaṇa (adverbial accusative) on āste",
        "glossaryKey": "sukha",
        "translatable": true,
        "parts": [
          {
            "form": "sukha",
            "gloss": "ease, comfort, happiness, pleasure"
          },
          {
            "form": "-am",
            "gloss": "(accusative singular, used adverbially: 'happily, at ease')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "वशी",
        "iast": "vaśī",
        "gloss": "the self-controlled one, master of himself",
        "stem": "vaśin",
        "root": null,
        "affix": "ini (taddhita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of āste, in apposition with dehī",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "vaśa",
            "gloss": "will, control, dominion, power"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'the one who has —')"
          }
        ],
        "note": "Śaṅkara glosses vaśī as jitendriya, 'one who has mastered the senses' — the same subject as dehī."
      },
      {
        "i": 6,
        "deva": "नवद्वारे",
        "iast": "nava-dvāre",
        "gloss": "nine-gated, having nine gates",
        "stem": "nava-dvāra",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "viśeṣaṇa (attribute) of pure",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "nava dvārāṇi yasya tat (puram)",
          "members": [
            "nava",
            "dvāra"
          ]
        },
        "parts": [
          {
            "form": "nava",
            "gloss": "nine"
          },
          {
            "form": "dvāra",
            "gloss": "gate, door"
          }
        ],
        "note": "The nine gates are the body's apertures — traditionally the two eyes, two ears, two nostrils, the mouth, and the two lower openings."
      },
      {
        "i": 7,
        "deva": "पुरे",
        "iast": "pure",
        "gloss": "in the city, in the citadel",
        "stem": "pura",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa — where the dehī abides",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pura",
            "gloss": "city, citadel, stronghold"
          }
        ],
        "note": "Śaṅkara glosses pura as the body itself, called a 'city' as the dwelling-place of its ruler, the dehin."
      },
      {
        "i": 8,
        "deva": "देही",
        "iast": "dehī",
        "gloss": "the embodied one, the one who has a body",
        "stem": "dehin",
        "root": null,
        "affix": "ini (taddhita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of āste, in apposition with vaśī",
        "glossaryKey": "dehin",
        "translatable": true,
        "parts": [
          {
            "form": "deha",
            "gloss": "body"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'the one who has —')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates kurvan, with eva)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no"
          }
        ],
        "sandhi": "naiva ← na + eva (a + e → ai)"
      },
      {
        "i": 10,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, even, at all",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (intensifies na, over kurvan)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, even, just, at all (emphatic)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "कुर्वन्",
        "iast": "kurvan",
        "gloss": "doing, acting",
        "stem": null,
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; pres. act. part.",
        "karaka": "viśeṣaṇa (attribute) of dehī, descriptive of manner",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act, to perform"
          },
          {
            "form": "-u-",
            "gloss": "(the 8th-class present-stem vikaraṇa, as kuru-/kurv- before a vowel)"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, the present active participle: '—ing')"
          }
        ]
      },
      {
        "i": 12,
        "deva": "न",
        "iast": "na",
        "gloss": "not, nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates kārayan)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no; nor (continuing the negation)"
          }
        ]
      },
      {
        "i": 13,
        "deva": "कारयन्",
        "iast": "kārayan",
        "gloss": "causing to act, making [another] do",
        "stem": null,
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "ṇic (causative) + śatṛ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; causative pres. act. part.",
        "karaka": "viśeṣaṇa (attribute) of dehī, descriptive of manner",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act, to perform"
          },
          {
            "form": "-ay-",
            "gloss": "(ṇic, the causative marker: 'to make —')"
          },
          {
            "form": "-at",
            "gloss": "(śatṛ, present active participle: '—ing')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "sarva-karmāṇi manasā saṃnyasya — absolutive clause: sarva-karmāṇi karman of saṃnyasya, manasā its karaṇa. āste — main verb; its kartṛ is vaśī, in apposition with dehī; sukham — adverbial accusative on āste. nava-dvāre — viśeṣaṇa of pure (loc.), adhikaraṇa of the dehī's abiding. na eva kurvan, na kārayan — two negated present participles in apposition to dehī, describing the manner of that abiding.",
      "verbalModality": "One finite verb, āste (laṭ, present indicative, ātmanepada) — the state is presented as ongoing fact. saṃnyasya (absolutive) marks a completed renunciation prior to that state; kurvan and kārayan are present participles, both negated, describing what does not accompany the abiding."
    }
  },
  {
    "locus": "5.14",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "न कर्तृत्वं न कर्माणि लोकस्य सृजति प्रभुः ।\nन कर्मफलसंयोगं स्वभावस् तु प्रवर्तते ॥",
    "iast": "na kartṛtvaṃ na karmāṇi lokasya sṛjati prabhuḥ |\nna karmaphalasaṃyogaṃ svabhāvas tu pravartate ||",
    "sense": "The self as sovereign creates neither agency nor karmas for the world, nor the linking of karma to its fruit; that is the work of one's own nature operating by itself.",
    "english": "{6:The Lord} {5:creates} {0:neither} {1:agency} {2:nor} {3:karmas} {4:for the world}, {7:nor} {8:the union of karma with its fruit}; {10:but} {9:own-nature} {11:operates}.",
    "words": [
      {
        "i": 0,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates kartṛtvam, as object of sṛjati)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no"
          }
        ]
      },
      {
        "i": 1,
        "deva": "कर्तृत्वम्",
        "iast": "kartṛtvam",
        "gloss": "agency, the state of being an agent",
        "stem": "kartṛtva",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "tva (taddhita, bhāva) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of sṛjati",
        "glossaryKey": "kartr",
        "translatable": true,
        "parts": [
          {
            "form": "kartṛ",
            "gloss": "agent, doer, the one who acts"
          },
          {
            "form": "-tva",
            "gloss": "(taddhita: abstract-noun suffix, 'the state/quality of being —')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "न",
        "iast": "na",
        "gloss": "nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates karmāṇi, coordinate object of sṛjati)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no; nor"
          }
        ]
      },
      {
        "i": 3,
        "deva": "कर्माणि",
        "iast": "karmāṇi",
        "gloss": "karmas, actions",
        "stem": "karman",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "karman of sṛjati (coordinate with kartṛtvam)",
        "glossaryKey": "karma",
        "translatable": false,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to act, to perform"
          },
          {
            "form": "-man",
            "gloss": "(manin, the kṛt affix forming an action-noun: 'that which is done')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "लोकस्य",
        "iast": "lokasya",
        "gloss": "of the world, for the world's people",
        "stem": "loka",
        "root": null,
        "affix": "ṅas (ṣaṣṭhī ekavacana)",
        "morph": "gen. sg. masc.",
        "karaka": "sambandha (genitive standing in for the dative of purpose — 'for the sake of the world')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "loka",
            "gloss": "world, people, the created realm"
          }
        ],
        "note": "Śaṅkara reads lokasya as ṣaṣṭhī caturthy-arthe — a genitive doing dative work, 'for the world's sake'."
      },
      {
        "i": 5,
        "deva": "सृजति",
        "iast": "sṛjati",
        "gloss": "creates, brings forth, emits",
        "stem": null,
        "root": "√sṛj (tudādi, 6P)",
        "rootGloss": "to emit, to create, to bring forth, to let loose",
        "affix": "tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ prabhuḥ, karman kartṛtvam / karmāṇi / karma-phala-saṃyogam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sṛj",
            "gloss": "to emit, to create, to bring forth, to let loose"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "प्रभुः",
        "iast": "prabhuḥ",
        "gloss": "the Lord, the master, the sovereign one",
        "stem": "prabhu",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "u (kṛt, ku-pratyaya) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of sṛjati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, before; pre-eminently"
          },
          {
            "form": "√bhū",
            "gloss": "to be, to become, to arise"
          },
          {
            "form": "-u",
            "gloss": "(ku, the kṛt affix forming an agent/quality noun without guṇa: 'the one who is —')"
          }
        ],
        "note": "Śaṅkara reads prabhu here as the self (ātman), sovereign over the body — not, in this verse, a name for the supreme Lord."
      },
      {
        "i": 7,
        "deva": "न",
        "iast": "na",
        "gloss": "nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates karma-phala-saṃyogam, third coordinate object of sṛjati)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no; nor"
          }
        ]
      },
      {
        "i": 8,
        "deva": "कर्मफलसंयोगम्",
        "iast": "karma-phala-saṃyogam",
        "gloss": "the union of karma and its fruit",
        "stem": "karma-phala-saṃyoga",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to set to a task",
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of sṛjati (third coordinate object)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (double ṣaṣṭhī: 'the union of the fruit of karma')",
          "vigraha": "karmaṇaḥ phalaṃ karma-phalam; karma-phalasya saṃyogaḥ karma-phala-saṃyogaḥ, tam",
          "members": [
            "karman",
            "phala",
            "saṃyoga"
          ]
        },
        "parts": [
          {
            "form": "karman",
            "gloss": "karma — action, deed, work"
          },
          {
            "form": "phala",
            "gloss": "fruit, result, consequence"
          },
          {
            "form": "sam-√yuj",
            "gloss": "to join together, to unite, to connect"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun ending: 'the union')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "स्वभावः",
        "iast": "svabhāvaḥ",
        "gloss": "own-nature, inherent nature",
        "stem": "svabhāva",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of pravartate",
        "glossaryKey": "svabhava",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī: 'one's own nature')",
          "vigraha": "svasya bhāvaḥ svabhāvaḥ",
          "members": [
            "sva",
            "bhāva"
          ]
        },
        "parts": [
          {
            "form": "sva",
            "gloss": "own, one's own"
          },
          {
            "form": "bhāva",
            "gloss": "state, condition, nature, being"
          }
        ],
        "sandhi": "svabhāvas tu ← svabhāvaḥ + tu (visarga → s before t)"
      },
      {
        "i": 10,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, however",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (marks contrast with the preceding negations)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tu",
            "gloss": "but, however, on the other hand"
          }
        ]
      },
      {
        "i": 11,
        "deva": "प्रवर्तते",
        "iast": "pravartate",
        "gloss": "operates, proceeds, functions, sets to work",
        "stem": null,
        "root": "√vṛt (bhvādi, 1Ā)",
        "rootGloss": "to turn, to revolve; to proceed, to go on, to function, to operate",
        "affix": "ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ svabhāvaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, onward"
          },
          {
            "form": "√vṛt",
            "gloss": "to turn, to revolve; to proceed, to function"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Three coordinate objects of one verb: kartṛtvam, karmāṇi, karma-phala-saṃyogam — all karman of sṛjati, each negated by its own na; prabhuḥ — kartṛ of sṛjati; lokasya — sambandha (genitive doing dative work, 'for the world'). Second clause: svabhāvaḥ — kartṛ of pravartate; tu — adversative, setting the clause against the first.",
      "verbalModality": "Two finite verbs in the present indicative (laṭ): sṛjati (parasmaipada), negated three times over — what the Lord does not do; pravartate (ātmanepada), stated positively — what one's own nature does by itself."
    }
  },
  {
    "locus": "5.15",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "नादत्ते कस्य चित् पापं न चैव सुकृतं विभुः ।\nअज्ञानेनावृतं ज्ञानं तेन मुह्यन्ति जन्तवः ॥",
    "iast": "nādatte kasya cit pāpaṃ na caiva sukṛtaṃ vibhuḥ |\najñānenāvṛtaṃ jñānaṃ tena muhyanti jantavaḥ ||",
    "sense": "The pervading self takes on neither anyone's evil nor even anyone's good; knowledge is covered over by ignorance, and that is why creatures are deluded.",
    "english": "{9:The pervading self} {0,1:does not take on} {2,3:anyone's} {4:evil}, {5,6,7:nor even} {8:the good}. {12:Knowledge} {11:is covered} {10:by ignorance}; {13:by that}, {15:creatures} {14:are deluded}.",
    "words": [
      {
        "i": 0,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates ādatte)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no"
          }
        ],
        "sandhi": "nādatte ← na + ādatte (a + ā → ā)"
      },
      {
        "i": 1,
        "deva": "आदत्ते",
        "iast": "ādatte",
        "gloss": "takes on, incurs, appropriates",
        "stem": null,
        "root": "√dā (juhotyādi, 3U)",
        "rootGloss": "to give; (with ā-) to take, to receive, to appropriate",
        "affix": "ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ vibhuḥ, karman pāpam / sukṛtam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ā-",
            "gloss": "toward, unto (reverses the sense of √dā 'give' to 'take')"
          },
          {
            "form": "√dā",
            "gloss": "to give; to take, to receive"
          },
          {
            "form": "-tte",
            "gloss": "(3rd person singular, ātmanepada, reduplicated class, weak grade)"
          }
        ],
        "note": "√dā's parasmaipada gives 'give' (dadāti); its ātmanepada 'take for oneself' (datte) — a textbook example of the voice split."
      },
      {
        "i": 2,
        "deva": "कस्य",
        "iast": "kasya",
        "gloss": "of whom, of anyone",
        "stem": "kim",
        "root": null,
        "affix": "ṅas (ṣaṣṭhī ekavacana)",
        "morph": "gen. sg. masc./neut.",
        "karaka": "sambandha (whose evil / good it is)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ka-",
            "gloss": "the interrogative stem: who?, what? (indefinite with cit)"
          },
          {
            "form": "-sya",
            "gloss": "(genitive singular: 'of')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "चित्",
        "iast": "cit",
        "gloss": "-ever, any, some",
        "stem": "cit",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable indefinizing particle",
        "karaka": "— (turns kasya into the indefinite 'anyone's')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "cit",
            "gloss": "(enclitic particle making a preceding interrogative indefinite: 'any-, some-')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "पापम्",
        "iast": "pāpam",
        "gloss": "evil, sin, a wrong deed",
        "stem": "pāpa",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of ādatte",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pāpa",
            "gloss": "evil, bad, wrong; evil-doing, wickedness, sin"
          }
        ]
      },
      {
        "i": 5,
        "deva": "न",
        "iast": "na",
        "gloss": "nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates, with ca eva, the second object sukṛtam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not, no"
          }
        ],
        "sandhi": "na caiva ← na + ca + eva (ca + eva → caiva, a + e → ai)"
      },
      {
        "i": 6,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins the second negated object to the first)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "एव",
        "iast": "eva",
        "gloss": "even, indeed",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasizes sukṛtam: 'not even the good')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, even, just, at all (emphatic)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "सुकृतम्",
        "iast": "sukṛtam",
        "gloss": "a good deed, merit",
        "stem": "su-kṛta",
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to do, to make, to act, to perform",
        "affix": "kta (niṣṭhā) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.; past passive part. used as noun",
        "karaka": "karman of ādatte (coordinate with pāpam)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "karmadhāraya (avyaya-pūrvapada)",
          "vigraha": "su kṛtam",
          "members": [
            "su",
            "kṛta"
          ]
        },
        "parts": [
          {
            "form": "su-",
            "gloss": "well, good"
          },
          {
            "form": "√kṛ",
            "gloss": "to do, to make, to perform"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed', substantivized as 'the well-done thing')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "विभुः",
        "iast": "vibhuḥ",
        "gloss": "the pervading one, the all-pervading sovereign self",
        "stem": "vibhu",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "u (kṛt, ku-pratyaya) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of ādatte",
        "glossaryKey": "vibhu",
        "translatable": true,
        "parts": [
          {
            "form": "vi-",
            "gloss": "through, throughout, all-pervading"
          },
          {
            "form": "√bhū",
            "gloss": "to be, to become, to pervade"
          },
          {
            "form": "-u",
            "gloss": "(ku, the kṛt affix forming an agent/quality noun without guṇa: 'the one who is —')"
          }
        ],
        "note": "The same self named prabhuḥ in 5.14 — here named for its pervasiveness rather than its lordship."
      },
      {
        "i": 10,
        "deva": "अज्ञानेन",
        "iast": "ajñānena",
        "gloss": "by ignorance, by non-knowledge",
        "stem": "a-jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "nañ + lyuṭ (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of āvṛtam",
        "glossaryKey": "avidya",
        "translatable": true,
        "parts": [
          {
            "form": "a-",
            "gloss": "not, without (negative prefix)"
          },
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the knowing')"
          },
          {
            "form": "-ena",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ],
        "sandhi": "ajñānenāvṛtam ← ajñānena + āvṛtam (a + ā → ā)"
      },
      {
        "i": 11,
        "deva": "आवृतम्",
        "iast": "āvṛtam",
        "gloss": "covered, enveloped",
        "stem": "āvṛta",
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; past passive part.",
        "karaka": "predicate of jñānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ā-",
            "gloss": "all over, right around"
          },
          {
            "form": "√vṛ",
            "gloss": "to cover, to enclose, to veil"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 12,
        "deva": "ज्ञानम्",
        "iast": "jñānam",
        "gloss": "knowledge",
        "stem": "jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "lyuṭ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "the one qualified by āvṛtam (grammatical subject of the nominal predication)",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the knowing')"
          }
        ]
      },
      {
        "i": 13,
        "deva": "तेन",
        "iast": "tena",
        "gloss": "by that",
        "stem": "tad",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa / hetu of muhyanti",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, it (the anaphoric demonstrative)"
          },
          {
            "form": "-ena",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ],
        "note": "Refers back to ajñānena — 'by that [ignorance]'."
      },
      {
        "i": 14,
        "deva": "मुह्यन्ति",
        "iast": "muhyanti",
        "gloss": "are deluded, become bewildered, go astray",
        "stem": null,
        "root": "√muh (divādi, 4P)",
        "rootGloss": "to be confused, to be bewildered, to err, to go astray",
        "affix": "jhi (laṭ, prathama-puruṣa bahuvacana)",
        "morph": "3rd pl. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ jantavaḥ",
        "glossaryKey": "moha",
        "translatable": true,
        "parts": [
          {
            "form": "√muh",
            "gloss": "to be confused, to be bewildered, to err, to go astray"
          },
          {
            "form": "-ya-",
            "gloss": "(śyan, the present-stem marker of the divādi class)"
          },
          {
            "form": "-nti",
            "gloss": "(3rd person plural, active)"
          }
        ]
      },
      {
        "i": 15,
        "deva": "जन्तवः",
        "iast": "jantavaḥ",
        "gloss": "creatures, living beings",
        "stem": "jantu",
        "root": "√jan (divādi, 4Ā)",
        "rootGloss": "to be born, to arise, to come into being",
        "affix": "tu (kṛt) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of muhyanti",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√jan",
            "gloss": "to be born, to arise, to come into being"
          },
          {
            "form": "-tu",
            "gloss": "(kṛt tu-pratyaya: 'that which is born, the creature')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Two clauses. First: vibhuḥ — kartṛ of ādatte; pāpam and sukṛtam — its two karman, each negated (kasya cit — sambandha, whose evil/good); ca eva — 'and even', over the second object. Second: jñānam — subject qualified by the predicate participle āvṛtam; ajñānena — karaṇa; tena — karaṇa/hetu of muhyanti; jantavaḥ — kartṛ of muhyanti.",
      "verbalModality": "ādatte — laṭ, present indicative, ātmanepada, negated: a standing non-fact about the pervading self. āvṛtam — a past passive participle with no finite verb, stating a condition. muhyanti — laṭ, present indicative, parasmaipada, 3rd plural: the resulting, ongoing bewilderment of creatures."
    }
  },
  {
    "locus": "5.16",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "ज्ञानेन तु तद् अज्ञानं येषां नाशितम् आत्मनः ।\nतेषाम् आदित्यवज् ज्ञानं प्रकाशयति तत्परम् ॥",
    "iast": "jñānena tu tad ajñānaṃ yeṣāṃ nāśitam ātmanaḥ |\nteṣām ādityavaj jñānaṃ prakāśayati tatparam ||",
    "sense": "But those whose ignorance of the self has been destroyed by knowledge — for them knowledge, like the sun, reveals that supreme reality.",
    "english": "{1:But} {4:of whom} {2:that} {3:ignorance} {6:of the self} {0:by knowledge} {5:has been destroyed} — {7:for them}, {9:knowledge}, {8:like the sun}, {10:reveals} {11:that} {12:supreme}.",
    "words": [
      {
        "i": 0,
        "deva": "ज्ञानेन",
        "iast": "jñānena",
        "gloss": "by knowledge",
        "stem": "jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "lyuṭ (kṛt) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of nāśitam",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the knowing')"
          },
          {
            "form": "-ena",
            "gloss": "(instrumental singular: 'by, with')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, however",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (adversative, turning from the deluded creatures of 5.15)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tu",
            "gloss": "but, however, on the other hand"
          }
        ]
      },
      {
        "i": 2,
        "deva": "तद्",
        "iast": "tat",
        "gloss": "that",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana, irregular pronominal neuter)",
        "morph": "nom. sg. neut.",
        "karaka": "viśeṣaṇa (attribute) of ajñānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that (the anaphoric/correlative demonstrative)"
          }
        ],
        "sandhi": "tad ajñānam ← tat + ajñānam (t → d before a vowel, voicing assimilation)"
      },
      {
        "i": 3,
        "deva": "अज्ञानम्",
        "iast": "ajñānam",
        "gloss": "ignorance, non-knowledge",
        "stem": "a-jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "nañ + lyuṭ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "the one qualified by nāśitam (grammatical subject of the passive)",
        "glossaryKey": "avidya",
        "translatable": true,
        "parts": [
          {
            "form": "a-",
            "gloss": "not, without (negative prefix)"
          },
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the knowing')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "येषाम्",
        "iast": "yeṣām",
        "gloss": "of whom, whose",
        "stem": "yad",
        "root": null,
        "affix": "ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "sambandha — antecedent of the relative clause, correlated with teṣām",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative pronoun)"
          },
          {
            "form": "-eṣām",
            "gloss": "(genitive plural: 'of, whose')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "नाशितम्",
        "iast": "nāśitam",
        "gloss": "destroyed, made to perish",
        "stem": "nāśita",
        "root": "√naś (divādi, 4P)",
        "rootGloss": "to perish, to be lost, to disappear",
        "affix": "ṇic (causative) + kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; causative past passive part.",
        "karaka": "predicate of ajñānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√naś",
            "gloss": "to perish, to be lost, to disappear"
          },
          {
            "form": "-it-",
            "gloss": "(ṇic, causative marker, with iṭ-augment: 'to make —')"
          },
          {
            "form": "-a",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 6,
        "deva": "आत्मनः",
        "iast": "ātmanaḥ",
        "gloss": "of the self",
        "stem": "ātman",
        "root": null,
        "affix": "ṅas (ṣaṣṭhī ekavacana)",
        "morph": "gen. sg. masc.",
        "karaka": "sambandha (objective genitive with ajñānam — ignorance whose object is the self)",
        "glossaryKey": "atman",
        "translatable": true,
        "parts": [
          {
            "form": "ātman",
            "gloss": "the self, the innermost self"
          }
        ]
      },
      {
        "i": 7,
        "deva": "तेषाम्",
        "iast": "teṣām",
        "gloss": "of them, for them",
        "stem": "tad",
        "root": null,
        "affix": "ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "sambandha — correlative of yeṣām, functioning as the beneficiary of prakāśayati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, this one (the anaphoric/correlative demonstrative)"
          },
          {
            "form": "-eṣām",
            "gloss": "(genitive plural: 'of, for')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "आदित्यवत्",
        "iast": "ādityavat",
        "gloss": "like the sun",
        "stem": "āditya-vat",
        "root": null,
        "affix": "vati (taddhita, upamāna) — avyaya",
        "morph": "indeclinable adverb of comparison",
        "karaka": "upamāna (standard of comparison) qualifying prakāśayati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "āditya",
            "gloss": "the sun, Āditya (son of Aditi)"
          },
          {
            "form": "-vat",
            "gloss": "(taddhita vati: 'like, in the manner of')"
          }
        ],
        "sandhi": "ādityavaj jñānam ← ādityavat + jñānam (t → j before j)"
      },
      {
        "i": 9,
        "deva": "ज्ञानम्",
        "iast": "jñānam",
        "gloss": "knowledge",
        "stem": "jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "lyuṭ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ of prakāśayati",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the knowing')"
          }
        ]
      },
      {
        "i": 10,
        "deva": "प्रकाशयति",
        "iast": "prakāśayati",
        "gloss": "illumines, reveals, makes shine forth",
        "stem": null,
        "root": "√kāś (bhvādi, 1Ā)",
        "rootGloss": "to shine, to be bright, to appear, to be visible",
        "affix": "pra- + ṇic (causative) + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. causative parasmaipada",
        "karaka": "the verb; kartṛ jñānam, karman tat param",
        "glossaryKey": "prakasa",
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, fully"
          },
          {
            "form": "√kāś",
            "gloss": "to shine, to be bright, to appear"
          },
          {
            "form": "-aya-",
            "gloss": "(ṇic, causative marker: 'to make —')"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "तत्",
        "iast": "tat",
        "gloss": "that",
        "stem": "tad",
        "root": null,
        "affix": "am (dvitīyā ekavacana, irregular pronominal neuter)",
        "morph": "acc. sg. neut.",
        "karaka": "viśeṣaṇa (attribute) of param",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that (the anaphoric demonstrative)"
          }
        ],
        "note": "The saṃhitā prints tatparam as one orthographic unit (t + p causes no audible sandhi); read here as two words, tat and param, both accusative and agreeing, the object of prakāśayati — following Śaṅkara, who glosses the pair as paramātma-tattvam, not as the separate compound tat-para ('devoted to that') that appears elsewhere in this same passage (5.17)."
      },
      {
        "i": 12,
        "deva": "परम्",
        "iast": "param",
        "gloss": "the supreme, the highest",
        "stem": "para",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of prakāśayati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "para",
            "gloss": "highest, supreme, beyond; the further/other side"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "A relative-correlative sentence (yad … tad). Relative clause: tad ajñānam — nom., subject qualified by the predicate participle nāśitam; yeṣām — sambandha, the antecedent 'whose'; ātmanaḥ — sambandha, objective genitive with ajñānam; jñānena — karaṇa of nāśitam; tu — adversative. Correlative clause: teṣām — sambandha correlating with yeṣām, the beneficiary; jñānam — kartṛ of prakāśayati; tat param — karman (demonstrative + adjective, both accusative); ādityavat — upamāna, comparing the illumination to the sun.",
      "verbalModality": "One passive/predicative participle, nāśitam, with no finite copula (a standing result: the ignorance is gone), and one finite causative verb, prakāśayati (laṭ, present indicative) — knowledge is depicted as actively, continuously illuminating."
    }
  },
  {
    "locus": "5.17",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "तद्बुद्धयस् तदात्मानस् तन्निष्ठास् तत्परायणाः ।\nगच्छन्त्य् अपुनरावृत्तिं ज्ञाननिर्धूतकल्मषाः ॥",
    "iast": "tadbuddhayas tadātmānas tanniṣṭhās tatparāyaṇāḥ |\ngacchanty apunarāvṛttiṃ jñānanirdhūtakalmaṣāḥ ||",
    "sense": "Their understanding, their mind, their foundation, and their final goal all fixed on That — their impurities shaken off by knowledge — such people go to the state of never returning.",
    "english": "{0:Those whose buddhi is fixed on That}, {1:whose self is on That}, {2:who are grounded in That}, {3:for whom That is the final goal} — {6:their impurities shaken off by knowledge} — {4:attain} {5:non-return}.",
    "words": [
      {
        "i": 0,
        "deva": "तद्बुद्धयः",
        "iast": "tad-buddhayaḥ",
        "gloss": "those whose buddhi is fixed on That",
        "stem": "tad-buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of gacchanti (first of four coordinate attributive compounds)",
        "glossaryKey": "buddhi",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "tasmin (brahmaṇi) buddhir yeṣāṃ te",
          "members": [
            "tad",
            "buddhi"
          ]
        },
        "parts": [
          {
            "form": "tad",
            "gloss": "that (Brahman, understood from the discourse)"
          },
          {
            "form": "buddhi",
            "gloss": "buddhi — the discriminating, understanding faculty"
          }
        ],
        "note": "The referent of tad across all four epithets is Brahman, understood from context, not restated."
      },
      {
        "i": 1,
        "deva": "तदात्मानः",
        "iast": "tad-ātmānaḥ",
        "gloss": "those whose mind is fixed on That",
        "stem": "tad-ātman",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of gacchanti (second coordinate compound)",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "tasmin (brahmaṇi) ātmā (manaḥ) yeṣāṃ te",
          "members": [
            "tad",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "tad",
            "gloss": "that (Brahman, understood)"
          },
          {
            "form": "ātman",
            "gloss": "the self; here, the inner disposition turned toward"
          }
        ],
        "note": "Śaṅkara glosses this ātman as antaḥkaraṇa, the inner faculty (mind) turned wholly toward Brahman — not the metaphysical self as elsewhere."
      },
      {
        "i": 2,
        "deva": "तन्निष्ठाः",
        "iast": "tan-niṣṭhāḥ",
        "gloss": "those grounded, steadfast, established in That",
        "stem": "tad-niṣṭhā",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to remain, to be established",
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of gacchanti (third coordinate compound)",
        "glossaryKey": "nistha",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "tasmin (brahmaṇi) niṣṭhā yeṣāṃ te",
          "members": [
            "tad",
            "niṣṭhā"
          ]
        },
        "parts": [
          {
            "form": "tad",
            "gloss": "that (Brahman, understood)"
          },
          {
            "form": "ni-",
            "gloss": "down, firmly"
          },
          {
            "form": "√sthā",
            "gloss": "to stand, to remain, to be established"
          },
          {
            "form": "-ā",
            "gloss": "(the feminine action-noun ending: 'the standing, steadfastness')"
          }
        ],
        "sandhi": "tan-niṣṭhāḥ ← tad + niṣṭhāḥ (d → n before a following n, nasal assimilation)"
      },
      {
        "i": 3,
        "deva": "तत्परायणाः",
        "iast": "tat-parāyaṇāḥ",
        "gloss": "those for whom That is the final goal, whose refuge is That",
        "stem": "tat-parāyaṇa",
        "root": "√i (adādi, 2P)",
        "rootGloss": "to go",
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of gacchanti (fourth coordinate compound)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with an internal karmadhāraya, tad + para)",
          "vigraha": "tat paramam ayanaṃ yeṣāṃ te",
          "members": [
            "tad",
            "para",
            "ayana"
          ]
        },
        "parts": [
          {
            "form": "tad",
            "gloss": "that (Brahman, understood)"
          },
          {
            "form": "para",
            "gloss": "highest, supreme, ultimate"
          },
          {
            "form": "ā-",
            "gloss": "unto, toward"
          },
          {
            "form": "√i",
            "gloss": "to go"
          },
          {
            "form": "-ana",
            "gloss": "(kṛt: forming an action/place-noun, 'the going-toward, the resort, the goal')"
          }
        ],
        "sandhi": "tat-parāyaṇāḥ ← tad + parāyaṇāḥ (d → t before a following voiceless consonant)"
      },
      {
        "i": 4,
        "deva": "गच्छन्ति",
        "iast": "gacchanti",
        "gloss": "go, proceed, attain, reach",
        "stem": null,
        "root": "√gam (bhvādi, 1P)",
        "rootGloss": "to go, to proceed, to attain, to reach",
        "affix": "jhi (laṭ, prathama-puruṣa bahuvacana)",
        "morph": "3rd pl. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ = the four coordinate compounds (i0–3), karman apunarāvṛttim",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√gam",
            "gloss": "to go, to proceed, to attain, to reach"
          },
          {
            "form": "-cha-",
            "gloss": "(śa, the present-stem marker, with the ch of gacchati)"
          },
          {
            "form": "-nti",
            "gloss": "(3rd person plural, active)"
          }
        ],
        "sandhi": "gacchanty apunarāvṛttim ← gacchanti + apunarāvṛttim (i → y before a following vowel)"
      },
      {
        "i": 5,
        "deva": "अपुनरावृत्तिम्",
        "iast": "apunarāvṛttim",
        "gloss": "non-return, the state of not coming back",
        "stem": "a-punar-āvṛtti",
        "root": "√vṛt (bhvādi, 1Ā)",
        "rootGloss": "to turn, to revolve; to return, to recur",
        "affix": "nañ + ktin (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. fem.",
        "karaka": "karman of gacchanti",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (nañ-tatpuruṣa negating punar-āvṛtti)",
          "vigraha": "na punaḥ āvṛttiḥ apunarāvṛttiḥ, tām",
          "members": [
            "a",
            "punar",
            "āvṛtti"
          ]
        },
        "parts": [
          {
            "form": "a-",
            "gloss": "not, without (negative prefix)"
          },
          {
            "form": "punar",
            "gloss": "again, back"
          },
          {
            "form": "ā-",
            "gloss": "back, toward"
          },
          {
            "form": "√vṛt",
            "gloss": "to turn, to revolve; to return, to recur"
          },
          {
            "form": "-ti",
            "gloss": "(ktin, the feminine action-noun: 'the turning back, the return')"
          }
        ],
        "note": "The 'return' in view is rebirth: not coming back into the cycle of birth and death."
      },
      {
        "i": 6,
        "deva": "ज्ञाननिर्धूतकल्मषाः",
        "iast": "jñāna-nirdhūta-kalmaṣāḥ",
        "gloss": "those whose impurities have been shaken off by knowledge",
        "stem": "jñāna-nirdhūta-kalmaṣa",
        "root": "√dhū (svādi, 5U)",
        "rootGloss": "to shake, to shake off, to remove",
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of gacchanti (fifth coordinate epithet, placed after the verb)",
        "glossaryKey": "jnana",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (built on an internal tṛtīyā tatpuruṣa: jñānena nirdhūtam)",
          "vigraha": "jñānena nirdhūtaṃ kalmaṣaṃ yeṣāṃ te",
          "members": [
            "jñāna",
            "nirdhūta",
            "kalmaṣa"
          ]
        },
        "parts": [
          {
            "form": "jñāna",
            "gloss": "knowledge"
          },
          {
            "form": "nir-",
            "gloss": "out, away, completely"
          },
          {
            "form": "√dhū",
            "gloss": "to shake, to shake off, to remove"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          },
          {
            "form": "kalmaṣa",
            "gloss": "impurity, moral stain, sin"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "One sentence built almost entirely on nominal apposition. Five bahuvrīhi compounds — tad-buddhayaḥ, tad-ātmānaḥ, tan-niṣṭhāḥ, tat-parāyaṇāḥ, jñāna-nirdhūta-kalmaṣāḥ — all nom. pl. masc., all kartṛ of the one finite verb gacchanti; apunarāvṛttim — karman.",
      "verbalModality": "One finite verb, gacchanti (laṭ, present indicative, parasmaipada, 3rd plural) — a general, ongoing truth about such people, carried almost entirely by piled-up compound epithets rather than by finite predication."
    }
  },
  {
    "locus": "5.18",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "विद्याविनयसंपन्ने ब्राह्मणे गवि हस्तिनि ।\nशुनि चैव श्वपाके च पण्डिताः समदर्शिनः ॥",
    "iast": "vidyāvinayasaṃpanne brāhmaṇe gavi hastini |\nśuni caiva śvapāke ca paṇḍitāḥ samadarśinaḥ ||",
    "sense": "The wise look with the same eye on a learned and humble brahmin, a cow, an elephant, a dog, and even an outcaste who cooks dogs.",
    "english": "{9:The wise} {10:see with an equal eye} {1:a brahmin} {0:endowed with learning and humility}, {2:a cow}, {3:an elephant}, {8:and} {4:a dog}, {5:and} {6:even} {7:an outcaste}.",
    "words": [
      {
        "i": 0,
        "deva": "विद्याविनयसंपन्ने",
        "iast": "vidyā-vinaya-saṃpanne",
        "gloss": "endowed with learning and humility",
        "stem": "vidyā-vinaya-saṃpanna",
        "root": "√pad (divādi, 4Ā)",
        "rootGloss": "to go, to fall; (with sam-) to be accomplished, to be endowed with, to attain",
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "viśeṣaṇa (attribute) of brāhmaṇe; together with the four other loci, viṣaya-saptamī (locative of respect) governed by sama-darśinaḥ",
        "glossaryKey": "vidya",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (tṛtīyā: 'endowed with learning and humility')",
          "vigraha": "vidyayā vinayena ca saṃpannaḥ",
          "members": [
            "vidyā",
            "vinaya",
            "saṃpanna"
          ]
        },
        "parts": [
          {
            "form": "vidyā",
            "gloss": "learning, knowledge"
          },
          {
            "form": "vinaya",
            "gloss": "humility, discipline, good conduct"
          },
          {
            "form": "sam-√pad",
            "gloss": "to be accomplished; to be endowed with, to attain"
          },
          {
            "form": "-na",
            "gloss": "(kta, past passive participle: 'having been —ed', here 'endowed with')"
          }
        ],
        "note": "Śaṅkara reads vidyā as brahma-vidyā, knowledge of Brahman, and vinaya as its outward mark — humility, restraint of the senses."
      },
      {
        "i": 1,
        "deva": "ब्राह्मणे",
        "iast": "brāhmaṇe",
        "gloss": "in a brahmin",
        "stem": "brāhmaṇa",
        "root": null,
        "affix": "aṇ (taddhita) + ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "viṣaya-saptamī governed by sama-darśinaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "brahman",
            "gloss": "brahman; here, in its taddhita form, 'belonging to sacred learning'"
          },
          {
            "form": "-a",
            "gloss": "(taddhita aṇ, with vṛddhi: 'relating to, descended from —')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "गवि",
        "iast": "gavi",
        "gloss": "in a cow",
        "stem": "go",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. fem.",
        "karaka": "viṣaya-saptamī governed by sama-darśinaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "go",
            "gloss": "cow, ox; cattle"
          }
        ]
      },
      {
        "i": 3,
        "deva": "हस्तिनि",
        "iast": "hastini",
        "gloss": "in an elephant",
        "stem": "hastin",
        "root": null,
        "affix": "ini (taddhita) + ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "viṣaya-saptamī governed by sama-darśinaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "hasta",
            "gloss": "hand; trunk (of an elephant)"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'the one who has —', hence 'the trunked one, the elephant')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "शुनि",
        "iast": "śuni",
        "gloss": "in a dog",
        "stem": "śvan",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "viṣaya-saptamī governed by sama-darśinaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "śvan",
            "gloss": "dog (irregular consonant stem; weak stem śun-)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins śuni to the series)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ],
        "sandhi": "caiva ← ca + eva (a + e → ai)"
      },
      {
        "i": 6,
        "deva": "एव",
        "iast": "eva",
        "gloss": "even, indeed",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphatic, extending the equal vision to the lowest case)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, even, just, at all (emphatic)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "श्वपाके",
        "iast": "śvapāke",
        "gloss": "in an outcaste, a dog-cooker",
        "stem": "śva-pāka",
        "root": "√pac (bhvādi, 1U)",
        "rootGloss": "to cook, to bake, to ripen",
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "viṣaya-saptamī governed by sama-darśinaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (upapada: 'one who cooks dogs')",
          "vigraha": "śvānaṃ pacati iti śvapākaḥ, tasmin",
          "members": [
            "śvan",
            "pac"
          ]
        },
        "parts": [
          {
            "form": "śvan",
            "gloss": "dog"
          },
          {
            "form": "√pac",
            "gloss": "to cook, to bake"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the agent/action-noun ending)"
          }
        ],
        "note": "The traditional term for an outcaste of the lowest rank — the extreme case, set against the brāhmaṇa at the top of the social order."
      },
      {
        "i": 8,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins śvapāke as the final item of the series)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "पण्डिताः",
        "iast": "paṇḍitāḥ",
        "gloss": "the wise, the learned",
        "stem": "paṇḍita",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of the implied copula ('are')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "paṇḍita",
            "gloss": "wise, learned; a wise or learned person"
          }
        ],
        "note": "The root of paṇḍita is not securely fixed in the traditional grammar (often treated as a deśya word); none is given here rather than guessed."
      },
      {
        "i": 10,
        "deva": "समदर्शिनः",
        "iast": "sama-darśinaḥ",
        "gloss": "equal-seeing, those who see with an equal eye",
        "stem": "sama-darśin",
        "root": "√dṛś (bhvādi, 1P)",
        "rootGloss": "to see, to look at, to behold",
        "affix": "ṇini (taddhita/kṛt agentive) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "predicate of paṇḍitāḥ (implied copula); its viṣaya is the five preceding locatives",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "upapada tatpuruṣa ('seeing equally')",
          "vigraha": "samaṃ paśyanti iti sama-darśinaḥ",
          "members": [
            "sama",
            "darśin"
          ]
        },
        "parts": [
          {
            "form": "sama",
            "gloss": "equal, the same"
          },
          {
            "form": "√dṛś",
            "gloss": "to see, to look at, to behold"
          },
          {
            "form": "-in",
            "gloss": "(ṇini, taddhita/kṛt agentive: 'the one who —s')"
          }
        ],
        "note": "The verse's key term — the wise are defined by what they see: one undivided regard across the brahmin and the outcaste, the cow and the elephant."
      }
    ],
    "grammar": {
      "karakaSummary": "One nominal sentence with an implied copula. paṇḍitāḥ — kartṛ; sama-darśinaḥ — predicate nominative agreeing with it. Five locatives — brāhmaṇe (with its attribute vidyā-vinaya-saṃpanne), gavi, hastini, śuni, śvapāke — all viṣaya-saptamī, the objects of the 'equal seeing' named by sama-darśinaḥ, joined by ca … ca and intensified by eva before the lowest case.",
      "verbalModality": "No finite verb at all — a single nominal predication (paṇḍitāḥ sama-darśinaḥ, 'the wise are equal-seeing'), with the five loci of that vision listed as a bare series of locatives."
    }
  },
  {
    "locus": "5.19",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "इहैव तैर् जितः सर्गो येषां साम्ये स्थितं मनः ।\nनिर्दोषं हि समं ब्रह्म तस्माद् ब्रह्मणि ते स्थिताः ॥",
    "iast": "ihaiva tair jitaḥ sargo yeṣāṃ sāmye sthitaṃ manaḥ |\nnirdoṣaṃ hi samaṃ brahma tasmād brahmaṇi te sthitāḥ ||",
    "sense": "Even in this very life, birth is conquered by those whose manas is established in sameness; Brahman is flawless and the same everywhere, so they stand established in Brahman.",
    "english": "{0,1:Even here}, {4:birth} {3:is conquered} {2:by them} {5:whose} {8:manas} {7:is established} {6:in sameness}. {12:Brahman} {10:indeed} {9:is flawless}, {11:the same} — {13:therefore} {15:they} {16:are established} {14:in Brahman}.",
    "words": [
      {
        "i": 0,
        "deva": "इह",
        "iast": "iha",
        "gloss": "here, in this world, in this life",
        "stem": "iha",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of place",
        "karaka": "adhikaraṇa in adverbial form ('here')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "iha",
            "gloss": "here, in this place, in this world"
          }
        ],
        "sandhi": "ihaiva ← iha + eva (a + e → ai)"
      },
      {
        "i": 1,
        "deva": "एव",
        "iast": "eva",
        "gloss": "even, indeed, just, precisely",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on iha)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "even, indeed, just, only (emphatic)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "तैः",
        "iast": "taiḥ",
        "gloss": "by them",
        "stem": "tad",
        "root": null,
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. masc.",
        "karaka": "kartṛ (logical agent of the passive kta jitaḥ), expressed instrumentally as required with a kta participle",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          },
          {
            "form": "-aiḥ",
            "gloss": "(instrumental plural: 'by, with')"
          }
        ],
        "sandhi": "tair jitaḥ ← taiḥ + jitaḥ (visarga → r before a voiced consonant)"
      },
      {
        "i": 3,
        "deva": "जितः",
        "iast": "jitaḥ",
        "gloss": "conquered, won, overcome",
        "stem": "jita",
        "root": "√ji (bhvādi, 1P)",
        "rootGloss": "to conquer, to win, to overcome, to be victorious over",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "predicate of sargaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ji",
            "gloss": "to conquer, to win, to overcome"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "सर्गः",
        "iast": "sargaḥ",
        "gloss": "creation; birth, the process of coming-into-being; the created order",
        "stem": "sarga",
        "root": "√sṛj (tudādi, 6P)",
        "rootGloss": "to create, to emit, to let go, to produce",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "karman of the passive kta jitaḥ, standing in the nominative",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sṛj",
            "gloss": "to create, to emit, to produce, to let go"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the creating, what is created')"
          }
        ],
        "note": "sarga's range runs from 'creation, emanation' to, by extension, 'birth' — the coming-into-being that repeats. Rendered here as 'birth' because that is the sense the verb jitaḥ ('conquered') fits: conquering creation-as-such makes little sense as a claim, conquering the birth-cycle does."
      },
      {
        "i": 5,
        "deva": "येषाम्",
        "iast": "yeṣām",
        "gloss": "of whom, whose",
        "stem": "yad",
        "root": null,
        "affix": "ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "sambandha (possessive genitive, 'whose' — resuming taiḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          },
          {
            "form": "-eṣām",
            "gloss": "(genitive plural: 'of whom, whose')"
          }
        ]
      },
      {
        "i": 6,
        "deva": "साम्ये",
        "iast": "sāmye",
        "gloss": "in sameness, in equality, in equanimity",
        "stem": "sāmya",
        "root": null,
        "affix": "ṣyañ (taddhita, bhāva) + ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "viṣaya-adhikaraṇa (the sphere in which manas is established)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "sama",
            "gloss": "same, equal, level, equanimous"
          },
          {
            "form": "-ya",
            "gloss": "(taddhita ṣyañ, with vṛddhi: 'the state of being —')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "स्थितम्",
        "iast": "sthitam",
        "gloss": "established, fixed, standing firm",
        "stem": "sthita",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to stand firm, to abide, to be established",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; past passive part.",
        "karaka": "predicate of manaḥ (implied copula)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sthā",
            "gloss": "to stand, to stand firm, to be established"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "मनः",
        "iast": "manaḥ",
        "gloss": "manas — the faculty that intends, hesitates and turns things over",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "asun (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ of the implied copula, with sthitam as predicate",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          {
            "form": "√man",
            "gloss": "to think, to consider, to have in mind"
          },
          {
            "form": "-as",
            "gloss": "(asun, the neuter action/agent noun)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "निर्दोषम्",
        "iast": "nirdoṣam",
        "gloss": "flawless, faultless, without defect",
        "stem": "nirdoṣa",
        "root": "√duṣ (divādi, 4P)",
        "rootGloss": "to become spoiled, to be at fault, to be corrupt",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "predicate of brahma (implied copula)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with nir- as a privative prefix)",
          "vigraha": "nirgato doṣo yasmāt tat",
          "members": [
            "nir",
            "doṣa"
          ]
        },
        "parts": [
          {
            "form": "nir-",
            "gloss": "without, free from"
          },
          {
            "form": "√duṣ",
            "gloss": "to be at fault, to be spoiled or corrupt"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, with guṇa: 'the fault, the flaw')"
          }
        ]
      },
      {
        "i": 10,
        "deva": "हि",
        "iast": "hi",
        "gloss": "for, indeed, surely",
        "stem": "hi",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis / grounds the second sentence)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "hi",
            "gloss": "for, indeed, surely (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "समम्",
        "iast": "samam",
        "gloss": "equal, the same, level",
        "stem": "sama",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "predicate of brahma, in apposition to nirdoṣam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "sama",
            "gloss": "same, equal, level, uniform"
          }
        ]
      },
      {
        "i": 12,
        "deva": "ब्रह्म",
        "iast": "brahma",
        "gloss": "Brahman",
        "stem": "brahman",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ of the implied copula, with nirdoṣam and samam as predicates",
        "glossaryKey": "brahman",
        "translatable": true,
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          }
        ]
      },
      {
        "i": 13,
        "deva": "तस्मात्",
        "iast": "tasmāt",
        "gloss": "therefore, from that",
        "stem": "tad",
        "root": null,
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. neut.",
        "karaka": "hetu in the ablative ('it being so')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, it (the anaphoric demonstrative)"
          },
          {
            "form": "-smāt",
            "gloss": "(ablative singular, pronominal declension: 'from that')"
          }
        ]
      },
      {
        "i": 14,
        "deva": "ब्रह्मणि",
        "iast": "brahmaṇi",
        "gloss": "in Brahman",
        "stem": "brahman",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa of sthitāḥ ('established in Brahman')",
        "glossaryKey": "brahman",
        "translatable": true,
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          }
        ]
      },
      {
        "i": 15,
        "deva": "ते",
        "iast": "te",
        "gloss": "they",
        "stem": "tad",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of the implied copula, with sthitāḥ as predicate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          },
          {
            "form": "-e",
            "gloss": "(nominative plural, pronominal declension)"
          }
        ]
      },
      {
        "i": 16,
        "deva": "स्थिताः",
        "iast": "sthitāḥ",
        "gloss": "established, standing firm, situated",
        "stem": "sthita",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to stand firm, to abide, to be established",
        "affix": "kta (niṣṭhā) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.; past passive part.",
        "karaka": "predicate of te",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sthā",
            "gloss": "to stand, to stand firm, to be established"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "yeṣām sāmye sthitam manaḥ is a relative clause qualifying taiḥ: yeṣām — sambandha ('whose'); sāmye — viṣaya-adhikaraṇa (what the manas is fixed in); manaḥ — kartṛ of the implied copula, sthitam its predicate. In the main clause, sargaḥ is karman of the passive kta jitaḥ, standing in the nominative; taiḥ is the logical kartṛ, expressed instrumentally as required with a kta participle; iha is adhikaraṇa of place. Second sentence: brahma — kartṛ of the implied copula with two predicates, nirdoṣam and samam; tasmāt — hetu (ablative of cause); te — kartṛ of the implied copula with sthitāḥ; brahmaṇi — adhikaraṇa ('in Brahman').",
      "verbalModality": "No finite verb in either sentence: jitaḥ, sthitam and sthitāḥ are all kta (past passive) participles standing as predicates, so the verse states a settled condition — already conquered, already established — rather than an event in progress."
    }
  },
  {
    "locus": "5.20",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "न प्रहृष्येत् प्रियं प्राप्य नोद्विजेत् प्राप्य चाप्रियम् ।\nस्थिरबुद्धिर् असंमूढो ब्रह्मविद् ब्रह्मणि स्थितः ॥",
    "iast": "na prahṛṣyet priyaṃ prāpya nodvijet prāpya cāpriyam |\nsthirabuddhir asaṃmūḍho brahmavid brahmaṇi sthitaḥ ||",
    "sense": "One should not rejoice on getting what is pleasant, nor be distressed on getting what is unpleasant — steadfast in buddhi, undeluded, a knower of Brahman, established in Brahman.",
    "english": "{0:Not} {1:should he rejoice}, {3:having gotten} {2:what is pleasant}; {4,7:nor} {5:should he be distressed}, {6:having gotten} {8:what is unpleasant} — {9:steadfast in buddhi}, {10:undeluded}, {11:a knower of Brahman}, {12:in Brahman} {13:he stands}.",
    "words": [
      {
        "i": 0,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates prahṛṣyet)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not (the plain negative particle)"
          }
        ]
      },
      {
        "i": 1,
        "deva": "प्रहृष्येत्",
        "iast": "prahṛṣyet",
        "gloss": "should rejoice, should be delighted",
        "stem": null,
        "root": "√hṛṣ (divādi, 4P)",
        "rootGloss": "to bristle, to thrill, to be delighted, to rejoice",
        "affix": "śyan (present-stem, divādi) + yāt (liṅ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. optative (vidhi-liṅ) parasmaipada",
        "karaka": "the verb; kartṛ unstated ('one, a person')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, exceedingly"
          },
          {
            "form": "√hṛṣ",
            "gloss": "to bristle, to thrill, to rejoice"
          },
          {
            "form": "-ya-",
            "gloss": "(śyan, the present-stem marker of the divādi class)"
          },
          {
            "form": "-et",
            "gloss": "(3rd person singular optative, parasmaipada)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "प्रियम्",
        "iast": "priyam",
        "gloss": "the pleasant, the dear, the agreeable",
        "stem": "priya",
        "root": "√prī (divādi 4Ā / kryādi 9U)",
        "rootGloss": "to please, to delight, to gratify; to love, to be fond of",
        "affix": "ka (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of the absolutive prāpya",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√prī",
            "gloss": "to please, to delight, to gratify"
          },
          {
            "form": "-ya",
            "gloss": "(kṛt: 'that which pleases, the pleasant')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "प्राप्य",
        "iast": "prāpya",
        "gloss": "having obtained, having gotten",
        "stem": null,
        "root": "pra-√āp (svādi, 5P)",
        "rootGloss": "to obtain, to get, to reach, to attain",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same unstated kartṛ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, onward"
          },
          {
            "form": "√āp",
            "gloss": "to obtain, to get, to reach"
          },
          {
            "form": "-ya",
            "gloss": "(lyap: 'having —ed', used when the root carries a prefix)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "न",
        "iast": "na",
        "gloss": "not, nor",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates udvijet)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not (the plain negative particle)"
          }
        ],
        "sandhi": "nodvijet ← na + udvijet (a + u → o)"
      },
      {
        "i": 5,
        "deva": "उद्विजेत्",
        "iast": "udvijet",
        "gloss": "should be distressed, should be agitated, should shrink back",
        "stem": null,
        "root": "√vij (tudādi, 6)",
        "rootGloss": "to tremble, to be afraid, to shrink back, to be agitated",
        "affix": "śa (present-stem, tudādi) + yāt (liṅ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. optative (vidhi-liṅ), parasmaipada ending",
        "karaka": "the verb; kartṛ unstated ('one, a person'), same as prahṛṣyet",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ud-",
            "gloss": "up, forth (of a startled recoil)"
          },
          {
            "form": "√vij",
            "gloss": "to tremble, to be afraid, to be agitated"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-et",
            "gloss": "(3rd person singular optative, parasmaipada ending)"
          }
        ],
        "note": "√vij is properly ātmanepada in Pāṇinian grammar (vijate); the parasmaipada ending -et seen here is a recognized epic-Sanskrit interchange of the two padas, matching prahṛṣyet in the same verse rather than following the classical rule strictly."
      },
      {
        "i": 6,
        "deva": "प्राप्य",
        "iast": "prāpya",
        "gloss": "having obtained, having gotten",
        "stem": null,
        "root": "pra-√āp (svādi, 5P)",
        "rootGloss": "to obtain, to get, to reach, to attain",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same unstated kartṛ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, onward"
          },
          {
            "form": "√āp",
            "gloss": "to obtain, to get, to reach"
          },
          {
            "form": "-ya",
            "gloss": "(lyap: 'having —ed', used when the root carries a prefix)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins the two clauses)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ],
        "sandhi": "cāpriyam ← ca + apriyam (a + a → ā)"
      },
      {
        "i": 8,
        "deva": "अप्रियम्",
        "iast": "apriyam",
        "gloss": "the unpleasant, the undesired, the disagreeable",
        "stem": "apriya",
        "root": "√prī (divādi 4Ā / kryādi 9U)",
        "rootGloss": "to please, to delight, to gratify; to love, to be fond of",
        "affix": "nañ + ka (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of the absolutive prāpya",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "nañ-tatpuruṣa (negative compound)",
          "vigraha": "na priyam",
          "members": [
            "a",
            "priya"
          ]
        },
        "parts": [
          {
            "form": "a-",
            "gloss": "not (the negative prefix nañ)"
          },
          {
            "form": "priya",
            "gloss": "pleasant, dear, agreeable"
          }
        ]
      },
      {
        "i": 9,
        "deva": "स्थिरबुद्धिः",
        "iast": "sthirabuddhiḥ",
        "gloss": "one whose buddhi is steadfast, steady in buddhi",
        "stem": "sthira-buddhi",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative describing the same unstated subject (implied copula)",
        "glossaryKey": "buddhi",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "sthirā buddhir yasya saḥ",
          "members": [
            "sthira",
            "buddhi"
          ]
        },
        "parts": [
          {
            "form": "sthira",
            "gloss": "firm, steady, stable"
          },
          {
            "form": "buddhi",
            "gloss": "buddhi — the faculty that discriminates and settles a matter"
          }
        ]
      },
      {
        "i": 10,
        "deva": "असंमूढः",
        "iast": "asaṃmūḍhaḥ",
        "gloss": "undeluded, unconfused",
        "stem": "asaṃmūḍha",
        "root": "√muh (divādi, 4P)",
        "rootGloss": "to be bewildered, to lose one's bearings, to be deluded",
        "affix": "nañ + sam- + kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part., negated",
        "karaka": "predicate nominative, in apposition to sthirabuddhiḥ",
        "glossaryKey": "moha",
        "translatable": true,
        "parts": [
          {
            "form": "a-",
            "gloss": "not (the negative prefix nañ)"
          },
          {
            "form": "sam-",
            "gloss": "thoroughly, altogether"
          },
          {
            "form": "√muh",
            "gloss": "to be bewildered, to be deluded"
          },
          {
            "form": "-ḍha",
            "gloss": "(past passive participle -ta, irregular as -ḍha after this root)"
          }
        ]
      },
      {
        "i": 11,
        "deva": "ब्रह्मवित्",
        "iast": "brahmavit",
        "gloss": "the knower of Brahman",
        "stem": "brahma-vit",
        "root": "√vid (adādi, 2P)",
        "rootGloss": "to know, to understand, to perceive",
        "affix": "kvip (kṛt, upapada) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative, in apposition to sthirabuddhiḥ",
        "glossaryKey": "brahman",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (upapada: object + agent-noun)",
          "vigraha": "brahma vetti iti",
          "members": [
            "brahman",
            "vid"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          },
          {
            "form": "√vid",
            "gloss": "to know, to understand, to perceive"
          },
          {
            "form": "-",
            "gloss": "(kvip: a zero-affix agent noun, 'the one who knows —')"
          }
        ]
      },
      {
        "i": 12,
        "deva": "ब्रह्मणि",
        "iast": "brahmaṇi",
        "gloss": "in Brahman",
        "stem": "brahman",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa of sthitaḥ",
        "glossaryKey": "brahman",
        "translatable": true,
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          }
        ]
      },
      {
        "i": 13,
        "deva": "स्थितः",
        "iast": "sthitaḥ",
        "gloss": "established, standing firm, situated",
        "stem": "sthita",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to stand firm, to abide, to be established",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "final predicate nominative, with brahmaṇi as its adhikaraṇa",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sthā",
            "gloss": "to stand, to stand firm, to be established"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Two parallel optative clauses, each headed by na plus an absolutive: prahṛṣyet / udvijet — the verb (optative, 3rd sg., subject unstated, 'one'); priyam / apriyam — karman of the absolutive prāpya in each clause. Four nominatives then describe the same unstated subject in apposition: sthirabuddhiḥ, asaṃmūḍhaḥ, brahmavit — predicate adjectives; sthitaḥ — final predicate, with brahmaṇi as its adhikaraṇa.",
      "verbalModality": "Two optatives (vidhi-liṅ) state what should or should not happen — a rule of conduct, not a report. The compounds and participle that follow (sthirabuddhiḥ, asaṃmūḍhaḥ, brahmavit, sthitaḥ) shift the verse from prescription to a description of the settled state such a person is already in."
    }
  },
  {
    "locus": "5.21",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "बाह्यस्पर्शेष्व् असक्तात्मा विन्दत्य् आत्मनि यत् सुखम् ।\nस ब्रह्मयोगयुक्तात्मा सुखम् अक्षयम् अश्नुते ॥",
    "iast": "bāhyasparśeṣv asaktātmā vindaty ātmani yat sukham |\nsa brahmayogayuktātmā sukham akṣayam aśnute ||",
    "sense": "One who is unattached to external contacts finds whatever pleasure is in the self; yoked in the yoga of Brahman, such a one enjoys imperishable pleasure.",
    "english": "{1:One whose self is unattached} {0:to external contacts} {2:finds} {4:whatever} {5:pleasure} {3:is in the self}; {6:he}, {7:whose self is yoked in the yoga of Brahman}, {10:enjoys} {9:imperishable} {8:pleasure}.",
    "words": [
      {
        "i": 0,
        "deva": "बाह्यस्पर्शेषु",
        "iast": "bāhyasparśeṣu",
        "gloss": "in external contacts, among outward sense-touches",
        "stem": "bāhya-sparśa",
        "root": "√spṛś (tudādi, 6P)",
        "rootGloss": "to touch, to come into contact with",
        "affix": "su (loc. pl.) — ṣu (saptamī bahuvacana)",
        "morph": "loc. pl. masc.",
        "karaka": "adhikaraṇa of asaktātmā (the object non-attachment concerns)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "karmadhāraya",
          "vigraha": "bāhyāś ca te sparśāś ca",
          "members": [
            "bāhya",
            "sparśa"
          ]
        },
        "parts": [
          {
            "form": "bāhya",
            "gloss": "external, outward, outer"
          },
          {
            "form": "√spṛś",
            "gloss": "to touch, to come into contact with"
          },
          {
            "form": "-a",
            "gloss": "(ghañ: 'the touch, the contact')"
          }
        ],
        "sandhi": "bāhyasparśeṣv asaktātmā ← bāhyasparśeṣu + asaktātmā (u → v before a dissimilar vowel)"
      },
      {
        "i": 1,
        "deva": "असक्तात्मा",
        "iast": "asaktātmā",
        "gloss": "one whose self is unattached",
        "stem": "asakta-ātman",
        "root": "√sañj (bhvādi, 1P)",
        "rootGloss": "to cling, to adhere, to be attached",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of vindati",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (first member itself a nañ-tatpuruṣa)",
          "vigraha": "na saktaḥ ātmā yasya saḥ",
          "members": [
            "asakta",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "a-",
            "gloss": "not (the negative prefix nañ)"
          },
          {
            "form": "√sañj",
            "gloss": "to cling, to adhere, to be attached"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "the self, the inner self; oneself"
          }
        ],
        "sandhi": "asaktātmā ← asakta + ātmā (a + ā → ā)"
      },
      {
        "i": 2,
        "deva": "विन्दति",
        "iast": "vindati",
        "gloss": "finds, obtains, comes upon",
        "stem": null,
        "root": "√vid (tudādi, 6U)",
        "rootGloss": "to find, to obtain, to get, to come upon",
        "affix": "śa (present-stem, tudādi) + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ asaktātmā, karman yat sukham",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√vid",
            "gloss": "to find, to obtain, to come upon"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ],
        "sandhi": "vindaty ātmani ← vindati + ātmani (i → y before a dissimilar vowel)"
      },
      {
        "i": 3,
        "deva": "आत्मनि",
        "iast": "ātmani",
        "gloss": "in the self",
        "stem": "ātman",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "adhikaraṇa (locus of the pleasure yat sukham)",
        "glossaryKey": "atman",
        "translatable": true,
        "parts": [
          {
            "form": "ātman",
            "gloss": "the self, the inner self; oneself"
          }
        ]
      },
      {
        "i": 4,
        "deva": "यत्",
        "iast": "yat",
        "gloss": "which, whatever",
        "stem": "yad",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "viśeṣaṇa (relative adjective) of sukham, both karman of vindati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which, whatever (the relative stem)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "सुखम्",
        "iast": "sukham",
        "gloss": "pleasure, happiness, ease",
        "stem": "sukha",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of vindati",
        "glossaryKey": "sukha",
        "translatable": true,
        "parts": [
          {
            "form": "sukha",
            "gloss": "pleasure, happiness, ease, joy"
          }
        ]
      },
      {
        "i": 6,
        "deva": "सः",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of aśnute, resuming asaktātmā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "ब्रह्मयोगयुक्तात्मा",
        "iast": "brahmayogayuktātmā",
        "gloss": "one whose self is yoked in the yoga of Brahman",
        "stem": "brahma-yoga-yukta-ātman",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to unite",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative in apposition to saḥ",
        "glossaryKey": "yoga",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with a tatpuruṣa + karmadhāraya first member)",
          "vigraha": "brahmaṇi yogaḥ brahma-yogaḥ; brahma-yoge yuktaḥ brahma-yoga-yuktaḥ; brahma-yoga-yuktaḥ ātmā yasya saḥ",
          "members": [
            "brahman",
            "yoga",
            "yukta",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          },
          {
            "form": "yoga",
            "gloss": "yoga — disciplined union, the yoked state"
          },
          {
            "form": "√yuj",
            "gloss": "to yoke, to join, to unite"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "the self, the inner self; oneself"
          }
        ]
      },
      {
        "i": 8,
        "deva": "सुखम्",
        "iast": "sukham",
        "gloss": "pleasure, happiness, ease",
        "stem": "sukha",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of aśnute",
        "glossaryKey": "sukha",
        "translatable": true,
        "parts": [
          {
            "form": "sukha",
            "gloss": "pleasure, happiness, ease, joy"
          }
        ]
      },
      {
        "i": 9,
        "deva": "अक्षयम्",
        "iast": "akṣayam",
        "gloss": "imperishable, undecaying, inexhaustible",
        "stem": "akṣaya",
        "root": "√kṣi (bhvādi, 1P)",
        "rootGloss": "to decay, to wane, to come to an end, to perish",
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "attribute of sukham",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "na vidyate kṣayo yasya tat",
          "members": [
            "a",
            "kṣaya"
          ]
        },
        "parts": [
          {
            "form": "a-",
            "gloss": "not (the negative prefix nañ)"
          },
          {
            "form": "√kṣi",
            "gloss": "to decay, to wane, to perish"
          },
          {
            "form": "-a",
            "gloss": "(ghañ: 'the decay, the waning')"
          }
        ]
      },
      {
        "i": 10,
        "deva": "अश्नुते",
        "iast": "aśnute",
        "gloss": "enjoys, obtains, partakes of",
        "stem": null,
        "root": "√aś (svādi, 5Ā)",
        "rootGloss": "to obtain, to reach, to pervade; to enjoy, to partake of",
        "affix": "nu (present-stem, svādi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ saḥ, karman sukham",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√aś",
            "gloss": "to obtain, to reach; to enjoy, to partake of"
          },
          {
            "form": "-nu-",
            "gloss": "(the present-stem marker of the svādi class)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ],
        "note": "A different root from the √aś (kryādi, 9P, 'aśnāti') that means 'to eat'; this svādi √aś means 'to obtain, pervade, enjoy'."
      }
    ],
    "grammar": {
      "karakaSummary": "asaktātmā — kartṛ of vindati; bāhyasparśeṣu — adhikaraṇa (the locus of the non-attachment); yat sukham — karman of vindati, a relative clause whose own adhikaraṇa is ātmani. saḥ — kartṛ of aśnute, resumed from asaktātmā; brahmayogayuktātmā — apposition to saḥ; sukham — karman of aśnute; akṣayam — attribute of sukham.",
      "verbalModality": "Two present indicatives (vindati, aśnute) state what is generally and always so for such a person — a timeless present, not a single event."
    }
  },
  {
    "locus": "5.22",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "ये हि संस्पर्शजा भोगा दुःखयोनय एव ते ।\nआद्यन्तवन्तः कौन्तेय न तेषु रमते बुधः ॥",
    "iast": "ye hi saṃsparśajā bhogā duḥkhayonaya eva te |\nādyantavantaḥ kaunteya na teṣu ramate budhaḥ ||",
    "sense": "The enjoyments that are born of contact are indeed wombs of sorrow, Kaunteya — they have a beginning and an end; the wise do not delight in them.",
    "english": "{1:For} {3:the enjoyments} {0:that} {2:are born of contact} — {6:they} {5:indeed} {4:are sources of sorrow}, {7:having a beginning and an end}. {8:O son of Kuntī}, {12:the wise one} {9:does not} {11:delight} {10:in them}.",
    "words": [
      {
        "i": 0,
        "deva": "ये",
        "iast": "ye",
        "gloss": "which, those which",
        "stem": "yad",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "viśeṣaṇa (relative adjective) of bhogāḥ, both kartṛ of the implied copula",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ]
      },
      {
        "i": 1,
        "deva": "हि",
        "iast": "hi",
        "gloss": "for, indeed, surely",
        "stem": "hi",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (grounds the statement)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "hi",
            "gloss": "for, indeed, surely (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "संस्पर्शजाः",
        "iast": "saṃsparśajāḥ",
        "gloss": "born of contact, arising from sense-contact",
        "stem": "saṃsparśa-ja",
        "root": "√jan (divādi, 4Ā)",
        "rootGloss": "to be born, to be produced, to arise, to come into being",
        "affix": "ḍa (kṛt, upapada) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "viśeṣaṇa of bhogāḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (upapada, '-ja' = born from)",
          "vigraha": "saṃsparśāt jātāḥ",
          "members": [
            "saṃsparśa",
            "ja"
          ]
        },
        "parts": [
          {
            "form": "sam-",
            "gloss": "together, fully"
          },
          {
            "form": "√spṛś",
            "gloss": "to touch, to come into contact with"
          },
          {
            "form": "√jan",
            "gloss": "to be born, to arise, to come into being"
          },
          {
            "form": "-a",
            "gloss": "(ḍa, kṛt: 'born from —')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "भोगाः",
        "iast": "bhogāḥ",
        "gloss": "enjoyments, pleasures",
        "stem": "bhoga",
        "root": "√bhuj (rudhādi, 7U)",
        "rootGloss": "to enjoy, to partake of, to experience",
        "affix": "ghañ (kṛt) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of the implied copula, with te resuming it and duḥkhayonayaḥ as predicate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√bhuj",
            "gloss": "to enjoy, to partake of, to experience"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the enjoying, the enjoyment')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "दुःखयोनयः",
        "iast": "duḥkhayonayaḥ",
        "gloss": "sources of sorrow, wombs from which sorrow is born",
        "stem": "duḥkha-yoni",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "predicate nominative, describing bhogāḥ / te",
        "glossaryKey": "duhkha",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "duḥkhasya yonayaḥ",
          "members": [
            "duḥkha",
            "yoni"
          ]
        },
        "parts": [
          {
            "form": "duḥkha",
            "gloss": "sorrow, pain, distress"
          },
          {
            "form": "yoni",
            "gloss": "womb, source, origin"
          }
        ],
        "note": "A tatpuruṣa: duḥkhasya yonayaḥ, the wombs or causes OF sorrow — these enjoyments give rise to it. Not the reverse."
      },
      {
        "i": 5,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, verily, certainly",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on duḥkhayonayaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "even, indeed, just, only (emphatic)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "ते",
        "iast": "te",
        "gloss": "they",
        "stem": "tad",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of the implied copula, resuming ye … bhogāḥ, with duḥkhayonayaḥ as predicate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          },
          {
            "form": "-e",
            "gloss": "(nominative plural, pronominal declension)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "आद्यन्तवन्तः",
        "iast": "ādyantavantaḥ",
        "gloss": "having a beginning and an end",
        "stem": "ādi-anta-vant",
        "root": null,
        "affix": "matup (taddhita) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "predicate nominative, in apposition to te",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (dvandva first member + matup/vant suffix)",
          "vigraha": "ādiś ca antaś ca ādyantau; ādyantau vidyete yeṣāṃ te",
          "members": [
            "ādi",
            "anta",
            "vant"
          ]
        },
        "parts": [
          {
            "form": "ādi",
            "gloss": "beginning, start"
          },
          {
            "form": "anta",
            "gloss": "end, limit"
          },
          {
            "form": "-vant",
            "gloss": "(matup: 'possessed of —')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "कौन्तेय",
        "iast": "kaunteya",
        "gloss": "O son of Kuntī",
        "stem": "kaunteya",
        "root": null,
        "affix": "ḍhak (taddhita, apatya) + su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "kuntī",
            "gloss": "Kuntī, Arjuna's mother"
          },
          {
            "form": "-eya",
            "gloss": "(taddhita ḍhak: 'son of —', with vṛddhi of the first vowel)"
          }
        ]
      },
      {
        "i": 9,
        "deva": "न",
        "iast": "na",
        "gloss": "not",
        "stem": "na",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable negative particle",
        "karaka": "— (negates ramate)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "na",
            "gloss": "not (the plain negative particle)"
          }
        ]
      },
      {
        "i": 10,
        "deva": "तेषु",
        "iast": "teṣu",
        "gloss": "in them",
        "stem": "tad",
        "root": null,
        "affix": "su (saptamī bahuvacana)",
        "morph": "loc. pl. masc.",
        "karaka": "adhikaraṇa (locus of non-delight)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          },
          {
            "form": "-eṣu",
            "gloss": "(locative plural: 'in, among')"
          }
        ]
      },
      {
        "i": 11,
        "deva": "रमते",
        "iast": "ramate",
        "gloss": "delights, takes pleasure, rejoices",
        "stem": null,
        "root": "√ram (bhvādi, 1Ā)",
        "rootGloss": "to rejoice, to delight in, to be pleased with, to sport",
        "affix": "śap (present-stem, bhvādi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada, negated",
        "karaka": "the verb; kartṛ budhaḥ, adhikaraṇa teṣu",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ram",
            "gloss": "to rejoice, to delight in, to sport"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      },
      {
        "i": 12,
        "deva": "बुधः",
        "iast": "budhaḥ",
        "gloss": "the wise one, the sage, the discerning one",
        "stem": "budha",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "a (kṛt, kartari) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of ramate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√budh",
            "gloss": "to wake, to be aware of, to understand"
          },
          {
            "form": "-a",
            "gloss": "(kṛt kartari: 'the one who is awake / who understands')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "ye … saṃsparśajāḥ bhogāḥ is the antecedent, resumed by the correlative te: bhogāḥ — kartṛ of the implied copula; duḥkhayonayaḥ and ādyantavantaḥ — predicate nominatives; kaunteya — āmantraṇa; budhaḥ — kartṛ of ramate; teṣu — adhikaraṇa (the locus of non-delight).",
      "verbalModality": "One finite verb only, ramate (laṭ, present, negated) — a standing fact about the wise, not a single event. The rest of the verse is nominal predication (an implied copula) describing what such enjoyments are."
    }
  },
  {
    "locus": "5.23",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "शक्नोतीहैव यः सोढुं प्राक् शरीरविमोक्षणात् ।\nकामक्रोधोद्भवं वेगं स युक्तः स सुखी नरः ॥",
    "iast": "śaknotīhaiva yaḥ soḍhuṃ prāk śarīravimokṣaṇāt |\nkāmakrodhodbhavaṃ vegaṃ sa yuktaḥ sa sukhī naraḥ ||",
    "sense": "He who, in this very life, before the release from the body, is able to bear the onrush that arises from kāma and krodha — he is yoked, he is a happy man.",
    "english": "{3:He who}, {2:even} {1:here}, {0:is able} {4:to endure}, {5:before} {6:the release of the body}, {8:the onrush} {7:arising from kāma and krodha} — {9:he} {10:is yoked}; {11:he}, {13:the man}, {12:is happy}.",
    "words": [
      {
        "i": 0,
        "deva": "शक्नोति",
        "iast": "śaknoti",
        "gloss": "is able, can",
        "stem": null,
        "root": "√śak (svādi, 5P)",
        "rootGloss": "to be able, to be capable of",
        "affix": "śnu (present-stem, svādi, strong-grade -no-) + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ yaḥ, governing the infinitive soḍhum",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√śak",
            "gloss": "to be able, to be capable of"
          },
          {
            "form": "-no-",
            "gloss": "(śnu, the present-stem marker of the svādi class, strong grade)"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ],
        "sandhi": "śaknotīhaiva ← śaknoti + iha + eva (i + i → ī; a + e → ai)"
      },
      {
        "i": 1,
        "deva": "इह",
        "iast": "iha",
        "gloss": "here, in this life",
        "stem": "iha",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of place",
        "karaka": "adhikaraṇa in adverbial form ('here')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "iha",
            "gloss": "here, in this place, in this world"
          }
        ]
      },
      {
        "i": 2,
        "deva": "एव",
        "iast": "eva",
        "gloss": "even, indeed, just",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on iha)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "even, indeed, just, only (emphatic)"
          }
        ]
      },
      {
        "i": 3,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who, he who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of śaknoti",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ]
      },
      {
        "i": 4,
        "deva": "सोढुम्",
        "iast": "soḍhum",
        "gloss": "to endure, to bear, to withstand",
        "stem": null,
        "root": "√sah (bhvādi, 1Ā)",
        "rootGloss": "to bear, to endure, to withstand, to overpower",
        "affix": "tumun (kṛt, infinitive)",
        "morph": "indeclinable infinitive",
        "karaka": "complement of śaknoti, itself governing vegam as karman",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√sah",
            "gloss": "to bear, to endure, to withstand"
          },
          {
            "form": "-ḍhum",
            "gloss": "(tumun, the infinitive ending; h + t → ḍh, with guṇa a → o, an irregular formation of this root)"
          }
        ],
        "note": "soḍhum is the irregular infinitive of √sah: the expected sah + tum undergoes h+t → ḍh and guṇa strengthening of the root vowel."
      },
      {
        "i": 5,
        "deva": "प्राक्",
        "iast": "prāk",
        "gloss": "before, prior to",
        "stem": "prāk",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of time",
        "karaka": "governs śarīravimokṣaṇāt (ablative, 'prior to —')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "prāk",
            "gloss": "before, previously, prior to"
          }
        ]
      },
      {
        "i": 6,
        "deva": "शरीरविमोक्षणात्",
        "iast": "śarīravimokṣaṇāt",
        "gloss": "from the release of the body, from the casting off of the body",
        "stem": "śarīra-vimokṣaṇa",
        "root": "vi-√muc (tudādi, 6U)",
        "rootGloss": "to release, to let go, to set free, to loosen",
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. neut.",
        "karaka": "apādāna, governed by prāk ('prior to')",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī, 'the release of the body')",
          "vigraha": "śarīrasya vimokṣaṇam",
          "members": [
            "śarīra",
            "vimokṣaṇa"
          ]
        },
        "parts": [
          {
            "form": "śarīra",
            "gloss": "the body"
          },
          {
            "form": "vi-",
            "gloss": "apart, away"
          },
          {
            "form": "√muc",
            "gloss": "to release, to let go, to set free"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action-noun: 'the releasing')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "कामक्रोधोद्भवम्",
        "iast": "kāmakrodhodbhavam",
        "gloss": "arising from kāma and krodha",
        "stem": "kāma-krodha-udbhava",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "attribute of vegam",
        "glossaryKey": "kama",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī, with a dvandva first member)",
          "vigraha": "kāmaś ca krodhaś ca kāma-krodhau; tābhyām udbhavaḥ",
          "members": [
            "kāma",
            "krodha",
            "udbhava"
          ]
        },
        "parts": [
          {
            "form": "kāma",
            "gloss": "kāma — desire as craving, the wanting that reaches for its object"
          },
          {
            "form": "krodha",
            "gloss": "krodha — anger, the flare of wrath"
          },
          {
            "form": "sam-ud-√bhū",
            "gloss": "to arise fully up out of; to originate"
          },
          {
            "form": "-a",
            "gloss": "(the action-noun ending: 'the arising')"
          }
        ],
        "note": "Both kāma and krodha are kept in IAST here, per site policy: neither has a plain English word that carries its full philosophical load."
      },
      {
        "i": 8,
        "deva": "वेगम्",
        "iast": "vegam",
        "gloss": "onrush, impulsive force, urge",
        "stem": "vega",
        "root": "√vij (tudādi, 6)",
        "rootGloss": "to dart, to shoot forth, to move quickly; to shrink, to tremble",
        "affix": "ghañ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of soḍhum",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√vij",
            "gloss": "to dart, to shoot forth, to move quickly"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, with guṇa: 'the onrush, the speed')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "सः",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, with yuktaḥ as predicate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          }
        ]
      },
      {
        "i": 10,
        "deva": "युक्तः",
        "iast": "yuktaḥ",
        "gloss": "yoked, joined, disciplined",
        "stem": "yukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to unite",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "predicate of saḥ (implied copula)",
        "glossaryKey": "yoga",
        "translatable": true,
        "parts": [
          {
            "form": "√yuj",
            "gloss": "to yoke, to harness, to join"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 11,
        "deva": "सः",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, resumed, with sukhī as predicate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          }
        ]
      },
      {
        "i": 12,
        "deva": "सुखी",
        "iast": "sukhī",
        "gloss": "happy, possessed of pleasure",
        "stem": "sukhin",
        "root": null,
        "affix": "in (taddhita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate of saḥ (implied copula)",
        "glossaryKey": "sukha",
        "translatable": true,
        "parts": [
          {
            "form": "sukha",
            "gloss": "pleasure, happiness, ease, joy"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'possessed of —')"
          }
        ]
      },
      {
        "i": 13,
        "deva": "नरः",
        "iast": "naraḥ",
        "gloss": "the man",
        "stem": "nara",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "apposition to saḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "nara",
            "gloss": "man, person"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "yaḥ — kartṛ of śaknoti; soḍhum — infinitive complement of śaknoti, itself governing vegam as karman; kāmakrodhodbhavam — attribute of vegam; śarīravimokṣaṇāt — apādāna in the ablative, governed by prāk ('before'); iha — adhikaraṇa. The apodosis is two nominal sentences with an implied copula: saḥ — kartṛ, yuktaḥ — predicate; saḥ — kartṛ (resumed), naraḥ — apposition, sukhī — predicate.",
      "verbalModality": "One finite verb, śaknoti (laṭ, present indicative), governing the infinitive soḍhum — the ability is stated as a present capacity. The consequence (yuktaḥ, sukhī) is given as two nominal predications rather than further verbs: the reward is a state, not a further event."
    }
  },
  {
    "locus": "5.24",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "यो ऽन्तःसुखो ऽन्तरारामस् तथान्तर्ज्योतिर् एव यः ।\nस योगी ब्रह्मनिर्वाणं ब्रह्मभूतो ऽधिगच्छति ॥",
    "iast": "yo 'ntaḥsukho 'ntarārāmas tathāntarjyotir eva yaḥ |\nsa yogī brahmanirvāṇaṃ brahmabhūto 'dhigacchati ||",
    "sense": "He who has pleasure within, delight within, and indeed light within — that yogī, having become Brahman, attains extinction in Brahman.",
    "english": "{0:He who} {1:has pleasure within}, {2:has delight within}, {3:and} {5:indeed} {6:who} {4:has light within} — {7:he}, {8:yogī}, {10:having become Brahman}, {11:attains} {9:extinction in Brahman}.",
    "words": [
      {
        "i": 0,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who, he who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, resumed by saḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ],
        "sandhi": "yo 'ntaḥsukhaḥ ← yaḥ + antaḥsukhaḥ (visarga → o before a, elided as 'a)"
      },
      {
        "i": 1,
        "deva": "अन्तःसुखः",
        "iast": "antaḥsukhaḥ",
        "gloss": "having pleasure within, inwardly happy",
        "stem": "antar-sukha",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative, describing yaḥ",
        "glossaryKey": "sukha",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "antaḥ sukham yasya saḥ",
          "members": [
            "antar",
            "sukha"
          ]
        },
        "parts": [
          {
            "form": "antar",
            "gloss": "within, inside"
          },
          {
            "form": "sukha",
            "gloss": "pleasure, happiness, ease, joy"
          }
        ],
        "sandhi": "antaḥsukho 'ntarārāmaḥ ← antaḥsukhaḥ + antarārāmaḥ (visarga → o before a, elided as 'a)"
      },
      {
        "i": 2,
        "deva": "अन्तरारामः",
        "iast": "antarārāmaḥ",
        "gloss": "having delight within, inwardly at ease",
        "stem": "antar-ārāma",
        "root": "ā-√ram (bhvādi, 1Ā)",
        "rootGloss": "to delight in, to rejoice, to take pleasure",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative, describing yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "antaḥ ārāmaḥ yasya saḥ",
          "members": [
            "antar",
            "ārāma"
          ]
        },
        "parts": [
          {
            "form": "antar",
            "gloss": "within, inside"
          },
          {
            "form": "ā-",
            "gloss": "toward, at"
          },
          {
            "form": "√ram",
            "gloss": "to delight in, to rejoice"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the place/action-noun: 'the delight, the garden of delight')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "तथा",
        "iast": "tathā",
        "gloss": "and, likewise, so too",
        "stem": "tathā",
        "root": null,
        "affix": "thāl (taddhita) — avyaya",
        "morph": "indeclinable",
        "karaka": "— (joins the third attribute to the first two)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that (the correlative stem)"
          },
          {
            "form": "-thā",
            "gloss": "(taddhita thāl: 'in the manner of —')"
          }
        ]
      },
      {
        "i": 4,
        "deva": "अन्तर्ज्योतिः",
        "iast": "antarjyotiḥ",
        "gloss": "having light within, inwardly lit",
        "stem": "antar-jyotis",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate nominative, describing yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "antar jyotiḥ yasya saḥ",
          "members": [
            "antar",
            "jyotis"
          ]
        },
        "parts": [
          {
            "form": "antar",
            "gloss": "within, inside"
          },
          {
            "form": "jyotis",
            "gloss": "light, radiance, brilliance; a heavenly light"
          }
        ],
        "sandhi": "antarjyotir eva ← antarjyotiḥ + eva (visarga → r before a vowel)"
      },
      {
        "i": 5,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, precisely, just",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on antarjyotiḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "even, indeed, just, only (emphatic)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, in apposition to the first yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative stem)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "सः",
        "iast": "sa",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of adhigacchati, resuming yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "he, that (the anaphoric demonstrative)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "योगी",
        "iast": "yogī",
        "gloss": "yogī — one who has yoga, a practitioner of yoga",
        "stem": "yogin",
        "root": null,
        "affix": "in (taddhita) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "apposition to saḥ",
        "glossaryKey": "yoga",
        "translatable": false,
        "parts": [
          {
            "form": "yoga",
            "gloss": "yoga — disciplined union, the yoked state"
          },
          {
            "form": "-in",
            "gloss": "(taddhita ini: 'the one who has —')"
          }
        ]
      },
      {
        "i": 9,
        "deva": "ब्रह्मनिर्वाणम्",
        "iast": "brahmanirvāṇam",
        "gloss": "extinguished into Brahman — the flame of ego and desire gone out, merged in Brahman",
        "stem": "brahma-nirvāṇa",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of adhigacchati",
        "glossaryKey": "brahmanirvana",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (saptamī: 'nirvāṇa in brahman') / or karmadhāraya ('the nirvāṇa that is brahman')",
          "vigraha": "brahmaṇi nirvāṇam — OR — brahma eva nirvāṇam",
          "members": [
            "brahman",
            "nirvāṇa"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "brahman, the Absolute, the supreme Reality, the boundless"
          },
          {
            "form": "nirvāṇa",
            "gloss": "blown out, extinguished; final release, cessation"
          }
        ]
      },
      {
        "i": 10,
        "deva": "ब्रह्मभूतः",
        "iast": "brahmabhūtaḥ",
        "gloss": "having become Brahman, one who is Brahman",
        "stem": "brahma-bhūta",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "predicate nominative, in apposition to saḥ",
        "glossaryKey": "brahman",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (prathamā, 'become X')",
          "vigraha": "brahma bhūtaḥ (san)",
          "members": [
            "brahman",
            "bhūta"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "Brahman, the Absolute, the boundless"
          },
          {
            "form": "√bhū",
            "gloss": "to be, to become, to arise"
          },
          {
            "form": "-ta",
            "gloss": "(past passive participle: 'having become —')"
          }
        ],
        "sandhi": "brahmabhūto 'dhigacchati ← brahmabhūtaḥ + adhigacchati (visarga → o before a, elided as 'a)"
      },
      {
        "i": 11,
        "deva": "अधिगच्छति",
        "iast": "adhigacchati",
        "gloss": "attains, reaches, arrives at",
        "stem": null,
        "root": "adhi-√gam (bhvādi, 1P)",
        "rootGloss": "to go, to move; (with adhi-) to attain, to reach, to master",
        "affix": "śap (present-stem, bhvādi) + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ saḥ, karman brahmanirvāṇam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "adhi-",
            "gloss": "over, unto, toward mastery of"
          },
          {
            "form": "√gam",
            "gloss": "to go, to move"
          },
          {
            "form": "-cch-",
            "gloss": "(the irregular present stem of √gam, gam → gacch before śap)"
          },
          {
            "form": "-ati",
            "gloss": "(3rd person singular, active)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Two relative clauses (yaḥ … yaḥ) share one subject, resumed by the correlative saḥ: antaḥsukhaḥ, antarārāmaḥ, antarjyotiḥ — three predicate nominatives (bahuvrīhi compounds) describing the same understood 'he'. In the main clause: saḥ — kartṛ of adhigacchati; yogī and brahmabhūtaḥ — apposition to saḥ; brahmanirvāṇam — karman of adhigacchati.",
      "verbalModality": "One finite verb, adhigacchati (laṭ, present indicative) — arrival at brahma-nirvāṇa is stated as a present, general fact about such a person, not a future promise."
    }
  },
  {
    "locus": "5.25",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "लभन्ते ब्रह्मनिर्वाणम् ऋषयः क्षीणकल्मषाः ।\nछिन्नद्वैधा यतात्मानः सर्वभूतहिते रताः ॥",
    "iast": "labhante brahmanirvāṇam ṛṣayaḥ kṣīṇakalmaṣāḥ |\nchinnadvaidhā yatātmānaḥ sarvabhūtahite ratāḥ ||",
    "sense": "Seers who have worn away their impurities, cut off from doubt, self-controlled, and devoted to the welfare of all beings, attain the beatitude that is Brahman.",
    "english": "{2:Seers} {3:whose impurities are worn away}, {4:free of doubt}, {5:whose selves are controlled}, {7:delighting} {6:in the welfare of all beings}, {0:attain} {1:brahma-nirvāṇa}.",
    "words": [
      {
        "i": 0,
        "deva": "लभन्ते",
        "iast": "labhante",
        "gloss": "they obtain, they attain",
        "stem": null,
        "root": "√labh (bhvādi, 1Ā)",
        "rootGloss": "to take, to obtain, to get, to attain",
        "affix": "śap + jha (laṭ, prathama-puruṣa bahuvacana ātmanepada)",
        "morph": "3rd pl. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ ṛṣayaḥ, karman brahmanirvāṇam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√labh",
            "gloss": "to take, to obtain, to get, to attain"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-nte",
            "gloss": "(3rd person plural, ātmanepada)"
          }
        ]
      },
      {
        "i": 1,
        "deva": "ब्रह्मनिर्वाणम्",
        "iast": "brahma-nirvāṇam",
        "gloss": "brahma-nirvāṇa — the beatitude that is extinction in Brahman",
        "stem": "brahma-nirvāṇa",
        "root": "√vā (adādi, 2P, 'to blow')",
        "rootGloss": "to blow; (nir- + kta) blown out, extinguished",
        "affix": "kta (niṣṭhā) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of labhante",
        "glossaryKey": "brahmanirvana",
        "translatable": false,
        "compound": {
          "type": "tatpuruṣa (saptamī)",
          "vigraha": "brahmaṇi nirvāṇam",
          "members": [
            "brahman",
            "nirvāṇa"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "brahman — the absolute, the ultimate reality"
          },
          {
            "form": "nir-",
            "gloss": "out, away, completely"
          },
          {
            "form": "√vā",
            "gloss": "to blow"
          },
          {
            "form": "-ṇa",
            "gloss": "(kta, past passive participle: 'blown out' — hence 'extinction, beatitude')"
          }
        ],
        "note": "Śaṅkara reads it as brahmaṇi nirvāṇam, 'the extinguishing (of the manifest self) in Brahman' — a saptamī-tatpuruṣa; some read the alternative karmadhāraya 'brahman itself is the nirvāṇa'. Either way the compound names Brahman-beatitude, not a Buddhist technical borrowing."
      },
      {
        "i": 2,
        "deva": "ऋषयः",
        "iast": "ṛṣayaḥ",
        "gloss": "seers, sages",
        "stem": "ṛṣi",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "kartṛ of labhante",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ṛṣi",
            "gloss": "seer, sage — one who has directly seen the truth"
          }
        ],
        "note": "Grammatically ṛṣi is treated as a primary, underived stem; Nirukta popularly connects it with √dṛś 'to see', which is folk etymology rather than the formal Pāṇinian derivation."
      },
      {
        "i": 3,
        "deva": "क्षीणकल्मषाः",
        "iast": "kṣīṇa-kalmaṣāḥ",
        "gloss": "whose impurities are worn away, whose sins have waned",
        "stem": "kṣīṇa-kalmaṣa",
        "root": "√kṣi (svādi, 5U)",
        "rootGloss": "to waste away, to diminish, to perish; (transitive) to destroy",
        "affix": "kta (niṣṭhā) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "attribute of ṛṣayaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "kṣīṇaṃ kalmaṣaṃ yeṣāṃ te",
          "members": [
            "kṣīṇa",
            "kalmaṣa"
          ]
        },
        "parts": [
          {
            "form": "√kṣi",
            "gloss": "to waste away, to diminish, to perish"
          },
          {
            "form": "-ṇa",
            "gloss": "(kta, past passive participle, with guṇa: 'waned, worn away')"
          },
          {
            "form": "kalmaṣa",
            "gloss": "impurity, stain, sin"
          }
        ]
      },
      {
        "i": 4,
        "deva": "छिन्नद्वैधाः",
        "iast": "chinnadvaidhāḥ",
        "gloss": "whose doubt is cut off, free of duality",
        "stem": "chinna-dvaidha",
        "root": "√chid (rudhādi, 7U)",
        "rootGloss": "to cut, to cut off, to sever",
        "affix": "kta (niṣṭhā) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "attribute of ṛṣayaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "chinnaṃ dvaidhaṃ yeṣāṃ te",
          "members": [
            "chinna",
            "dvaidha"
          ]
        },
        "parts": [
          {
            "form": "√chid",
            "gloss": "to cut, to cut off, to sever"
          },
          {
            "form": "-na",
            "gloss": "(kta, past passive participle, the -na allomorph after a root in d: 'having been —ed')"
          },
          {
            "form": "dvaidha",
            "gloss": "duality, division, doubt, uncertainty of mind (from dvi 'two')"
          }
        ],
        "note": "Śaṅkara glosses chinnadvaidhāḥ as chinna-saṃśayāḥ, 'whose doubt is cut off'.",
        "sandhi": "chinnadvaidhā yatātmānaḥ ← chinnadvaidhāḥ + yatātmānaḥ (visarga after ā drops before a following voiced consonant)"
      },
      {
        "i": 5,
        "deva": "यतात्मानः",
        "iast": "yatātmānaḥ",
        "gloss": "whose self is controlled, self-restrained",
        "stem": "yata-ātman",
        "root": "√yam (bhvādi, 1P)",
        "rootGloss": "to hold, to hold in, to check, to restrain",
        "affix": "kta (niṣṭhā) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "attribute of ṛṣayaḥ",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "yataḥ ātmā yaiḥ te",
          "members": [
            "yata",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "√yam",
            "gloss": "to hold, to hold in, to check, to restrain"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "the self"
          }
        ],
        "sandhi": "yatātmānaḥ ← yata + ātmānaḥ (a + ā → ā)"
      },
      {
        "i": 6,
        "deva": "सर्वभूतहिते",
        "iast": "sarva-bhūta-hite",
        "gloss": "in the welfare of all beings",
        "stem": "sarva-bhūta-hita",
        "root": "√dhā (juhotyādi, 3U)",
        "rootGloss": "to place, to put, to set",
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa (locus) governed by ratāḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī), with a karmadhāraya first member",
          "vigraha": "sarvāṇi ca tāni bhūtāni ca sarva-bhūtāni; teṣāṃ hitam, tasmin",
          "members": [
            "sarva",
            "bhūta",
            "hita"
          ]
        },
        "parts": [
          {
            "form": "sarva",
            "gloss": "all, every"
          },
          {
            "form": "√bhū",
            "gloss": "to be, to become, to arise, to come into being"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past participle used as a noun: 'a being')"
          },
          {
            "form": "√dhā",
            "gloss": "to place, to put, to set"
          },
          {
            "form": "hi-",
            "gloss": "(the irregular root-substitute of √dhā before kta)"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'well-placed' — hence 'beneficial, welfare')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "रताः",
        "iast": "ratāḥ",
        "gloss": "delighting in, devoted to, taking pleasure in",
        "stem": "rata",
        "root": "√ram (bhvādi, 1Ā)",
        "rootGloss": "to delight in, to rejoice, to take pleasure, to be devoted to",
        "affix": "kta (niṣṭhā) + jas (prathamā bahuvacana)",
        "morph": "nom. pl. masc.",
        "karaka": "second predicate of ṛṣayaḥ, governing the locus sarvabhūtahite",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ram",
            "gloss": "to delight in, to rejoice, to take pleasure, to be devoted to"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past participle used adjectivally: '—ing, devoted to')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "One sentence. ṛṣayaḥ — kartṛ of labhante; brahmanirvāṇam — karman; kṣīṇakalmaṣāḥ, chinnadvaidhāḥ, yatātmānaḥ, ratāḥ — four nominatives in apposition to ṛṣayaḥ; sarvabhūtahite — adhikaraṇa governed by ratāḥ.",
      "verbalModality": "One finite verb, labhante (laṭ, present indicative ātmanepada) — attainment stated as settled fact about seers of this description. Everything else is participial/bahuvrīhi apposition."
    }
  },
  {
    "locus": "5.26",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "कामक्रोधवियुक्तानां यतीनां यतचेतसाम् ।\nअभितो ब्रह्मनिर्वाणं वर्तते विदितात्मनाम् ॥",
    "iast": "kāmakrodhaviyuktānāṃ yatīnāṃ yatacetasām |\nabhito brahmanirvāṇaṃ vartate viditātmanām ||",
    "sense": "For ascetics released from kāma and krodha, self-controlled in mind and having known the self, the beatitude that is Brahman is present on every side.",
    "english": "{1:For ascetics} {0:released from kāma and krodha}, {2:whose minds are controlled}, {6:who have known the self} — {4:brahma-nirvāṇa} {5:abides} {3:on every side}.",
    "words": [
      {
        "i": 0,
        "deva": "कामक्रोधवियुक्तानाम्",
        "iast": "kāmakrodhaviyuktānām",
        "gloss": "of those released from kāma and krodha",
        "stem": "kāma-krodha-viyukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to set to a task",
        "affix": "kta (niṣṭhā) + ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "attribute of yatīnām (agreeing genitive)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with a dvandva first member)",
          "vigraha": "kāmaś ca krodhaś ca kāma-krodhau; tābhyāṃ viyuktau yeṣāṃ te, teṣām",
          "members": [
            "kāma",
            "krodha",
            "viyukta"
          ]
        },
        "parts": [
          {
            "form": "kāma",
            "gloss": "kāma — desire as craving, the wanting that reaches for its object"
          },
          {
            "form": "krodha",
            "gloss": "krodha — anger, wrath, rage"
          },
          {
            "form": "vi-",
            "gloss": "apart, away; disjoined"
          },
          {
            "form": "√yuj",
            "gloss": "to yoke, to harness, to join, to attach; to set to a task"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "यतीनाम्",
        "iast": "yatīnām",
        "gloss": "of ascetics, of those who restrain themselves",
        "stem": "yati",
        "root": "√yam (bhvādi, 1P)",
        "rootGloss": "to hold, to hold in, to check, to restrain",
        "affix": "i (Uṇādi kṛt, with loss of the root-final nasal) + ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "sambandha — genitive of reference with vartate ('for the ascetics...')",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√yam",
            "gloss": "to hold, to hold in, to check, to restrain"
          },
          {
            "form": "-i",
            "gloss": "(Uṇādi affix forming the agent-noun 'one who restrains himself')"
          }
        ],
        "note": "yati, 'ascetic', is traditionally derived from √yam by an Uṇādi affix; some grammarians instead connect it with √yat 'to strive, to endeavor' — both converge on the ascetic's characteristic effort at self-control."
      },
      {
        "i": 2,
        "deva": "यतचेतसाम्",
        "iast": "yata-cetasām",
        "gloss": "whose minds are controlled",
        "stem": "yata-cetas",
        "root": "√yam (bhvādi, 1P)",
        "rootGloss": "to hold, to hold in, to check, to restrain",
        "affix": "kta (niṣṭhā) + ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "attribute of yatīnām",
        "glossaryKey": "citta",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "yataṃ cetaḥ yeṣāṃ te, teṣām",
          "members": [
            "yata",
            "cetas"
          ]
        },
        "parts": [
          {
            "form": "√yam",
            "gloss": "to hold, to hold in, to check, to restrain"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          },
          {
            "form": "√cit",
            "gloss": "to perceive, to be aware, to think, to know"
          },
          {
            "form": "-as",
            "gloss": "(asun, the neuter action/state noun: 'awareness, mind')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "अभितः",
        "iast": "abhitaḥ",
        "gloss": "on both sides, all around, everywhere near",
        "stem": "abhitas",
        "root": null,
        "affix": "tasil (taddhita, adverb-forming)",
        "morph": "indeclinable adverb",
        "karaka": "adverbial complement of vartate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "abhi",
            "gloss": "toward, facing, on both sides of, near"
          },
          {
            "form": "-tas",
            "gloss": "(tasil, forming an adverb of place: 'from, at, on the side of —')"
          }
        ],
        "note": "Śaṅkara reads abhitaḥ not merely spatially but as 'on both sides' of the ascetic's life — present both here (in embodied life) and hereafter (after death)."
      },
      {
        "i": 4,
        "deva": "ब्रह्मनिर्वाणम्",
        "iast": "brahmanirvāṇam",
        "gloss": "brahma-nirvāṇa — the beatitude that is extinction in Brahman",
        "stem": "brahma-nirvāṇa",
        "root": "√vā (adādi, 2P, 'to blow')",
        "rootGloss": "to blow; (nir- + kta) blown out, extinguished",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ of vartate",
        "glossaryKey": "brahmanirvana",
        "translatable": false,
        "compound": {
          "type": "tatpuruṣa (saptamī)",
          "vigraha": "brahmaṇi nirvāṇam",
          "members": [
            "brahman",
            "nirvāṇa"
          ]
        },
        "parts": [
          {
            "form": "brahman",
            "gloss": "brahman — the absolute, the ultimate reality"
          },
          {
            "form": "nir-",
            "gloss": "out, away, completely"
          },
          {
            "form": "√vā",
            "gloss": "to blow"
          },
          {
            "form": "-ṇa",
            "gloss": "(kta, past passive participle: 'blown out' — hence 'extinction, beatitude')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "वर्तते",
        "iast": "vartate",
        "gloss": "exists, abides, is present, continues",
        "stem": null,
        "root": "√vṛt (bhvādi, 1Ā)",
        "rootGloss": "to turn, to revolve; to be, to exist, to abide, to continue",
        "affix": "śap + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. ātmanepada",
        "karaka": "the verb; kartṛ brahmanirvāṇam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√vṛt",
            "gloss": "to turn, to revolve; to be, to exist, to abide, to continue"
          },
          {
            "form": "-a-",
            "gloss": "(śap, the present-stem marker of the bhvādi class)"
          },
          {
            "form": "-te",
            "gloss": "(3rd person singular, ātmanepada)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "विदितात्मनाम्",
        "iast": "vidita-ātmanām",
        "gloss": "of those by whom the self has been known",
        "stem": "vidita-ātman",
        "root": "√vid (adādi, 2P)",
        "rootGloss": "to know, to be aware of, to recognize",
        "affix": "kta (niṣṭhā) + ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. masc.",
        "karaka": "attribute of yatīnām",
        "glossaryKey": "atman",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "viditaḥ ātmā yaiḥ te, teṣām",
          "members": [
            "vidita",
            "ātman"
          ]
        },
        "parts": [
          {
            "form": "√vid",
            "gloss": "to know, to be aware of, to recognize"
          },
          {
            "form": "-ita",
            "gloss": "(kta, past passive participle, with the connecting -iṭ-: 'having been —ed')"
          },
          {
            "form": "ātman",
            "gloss": "the self"
          }
        ],
        "sandhi": "asyādhiṣṭhānam-style vṛddhi does not apply here; the pada-pāṭha form vidita-ātmanām is unsandhied ← the saṃhitā viditātmanām already shows the regular a+ā→ā internal to the compound."
      }
    ],
    "grammar": {
      "karakaSummary": "One sentence. yatīnām — head genitive, sambandha with vartate ('for the ascetics'); kāmakrodhaviyuktānām, yatacetasām, viditātmanām — three attributive genitives agreeing with yatīnām; brahmanirvāṇam — kartṛ of vartate; abhitaḥ — adverbial complement of vartate.",
      "verbalModality": "One finite verb, vartate (laṭ, present indicative ātmanepada) — brahma-nirvāṇa's presence is stated as an abiding fact, not an event, for those of this description."
    }
  },
  {
    "locus": "5.27",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "स्पर्शान् कृत्वा बहिर् बाह्यांश् चक्षुश् चैवान्तरे भ्रुवोः ।\nप्राणापानौ समौ कृत्वा नासाभ्यन्तरचारिणौ ॥",
    "iast": "sparśān kṛtvā bahir bāhyāṃś cakṣuś caivāntare bhruvoḥ |\nprāṇāpānau samau kṛtvā nāsābhyantaracāriṇau ||",
    "sense": "He shuts the external sense-contacts outside, fixes the gaze between the eyebrows, and evens out the prāṇa and apāna moving within the nostrils —",
    "english": "{1:Having put} {3:external} {0:contacts} {2:outside}, {5:and} {4:the eye} {6:indeed} {7:between} {8:the eyebrows}; {11:having made} {9:the prāṇa and the apāna}, {12:moving within the nostrils}, {10:equal} —",
    "words": [
      {
        "i": 0,
        "deva": "स्पर्शान्",
        "iast": "sparśān",
        "gloss": "sense-contacts, touches",
        "stem": "sparśa",
        "root": "√spṛś (tudādi, 6P)",
        "rootGloss": "to touch, to come into contact with",
        "affix": "ghañ (kṛt) + śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. masc.",
        "karaka": "karman of kṛtvā (i=1)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√spṛś",
            "gloss": "to touch, to come into contact with"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, forming the action/object-noun with vṛddhi: 'contact, touch')"
          }
        ],
        "note": "Śaṅkara glosses sparśān as śabdādīn viṣayān, the sense-objects generally (sound and the rest), of which touch-contact is named as the type."
      },
      {
        "i": 1,
        "deva": "कृत्वा",
        "iast": "kṛtvā",
        "gloss": "having made, having done, having put",
        "stem": null,
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to make, to do, to perform, to put",
        "affix": "ktvā (kṛt)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same unstated kartṛ (the muniḥ of 5.28)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to make, to do, to perform, to put"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "बहिः",
        "iast": "bahiḥ",
        "gloss": "outside, without",
        "stem": "bahis",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb",
        "karaka": "adverbial complement of kṛtvā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "bahis",
            "gloss": "outside, without, external to"
          }
        ],
        "sandhi": "bahir bāhyāṃś ← bahiḥ + bāhyān (visarga → r before a voiced consonant)"
      },
      {
        "i": 3,
        "deva": "बाह्यान्",
        "iast": "bāhyān",
        "gloss": "external, outer",
        "stem": "bāhya",
        "root": null,
        "affix": "yat (taddhita) + śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. masc.",
        "karaka": "attribute of sparśān",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "bahis",
            "gloss": "outside, without, external to"
          },
          {
            "form": "-ya",
            "gloss": "(taddhita yat, with vṛddhi: 'pertaining to —', forming the adjective 'external')"
          }
        ],
        "sandhi": "bāhyāṃś cakṣuś ← bāhyān + cakṣuḥ (n → ṃś before c)"
      },
      {
        "i": 4,
        "deva": "चक्षुः",
        "iast": "cakṣuḥ",
        "gloss": "the eye, the gaze",
        "stem": "cakṣus",
        "root": "√cakṣ (adādi, 2Ā)",
        "rootGloss": "to see, to appear, to shine; to tell, to declare",
        "affix": "us (Uṇādi kṛt) + am (dvitīyā ekavacana, formally identical to the nom. in a neuter)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of the carried-over kṛtvā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√cakṣ",
            "gloss": "to see, to appear, to shine; to tell, to declare"
          },
          {
            "form": "-us",
            "gloss": "(Uṇādi kṛt, the neuter noun: 'the eye, the seeing organ')"
          }
        ],
        "note": "The governing verb for cakṣuḥ is elided and carried over from kṛtvā (or supplied by commentators as dhārayet, 'let him hold'): '...and [fixing] the eye right between the eyebrows'.",
        "sandhi": "cakṣuś caivāntare ← cakṣuḥ + ca + eva + antare (visarga → ś before c; a + e → ai)"
      },
      {
        "i": 5,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins the eye-clause to the sense-contact clause)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "ca",
            "gloss": "and, also (enclitic — never first in its clause)"
          }
        ]
      },
      {
        "i": 6,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, just, exactly",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, just, exactly, only (emphatic particle)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "अन्तरे",
        "iast": "antare",
        "gloss": "between, within",
        "stem": "antara",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. neut.",
        "karaka": "adhikaraṇa (locus), governing the genitive bhruvoḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "antara",
            "gloss": "the interior, the space between; interval"
          }
        ]
      },
      {
        "i": 8,
        "deva": "भ्रुवोः",
        "iast": "bhruvoḥ",
        "gloss": "of the two eyebrows",
        "stem": "bhrū",
        "root": null,
        "affix": "os (ṣaṣṭhī dvivacana)",
        "morph": "gen. dual fem.",
        "karaka": "sambandha, complement of antare",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "bhrū",
            "gloss": "eyebrow"
          }
        ]
      },
      {
        "i": 9,
        "deva": "प्राणापानौ",
        "iast": "prāṇāpānau",
        "gloss": "the prāṇa and the apāna — the up-breath and the down-breath",
        "stem": "prāṇa-apāna",
        "root": "√an (adādi, 2P)",
        "rootGloss": "to breathe",
        "affix": "ghañ (kṛt) + au (dvitīyā dvivacana)",
        "morph": "acc. dual masc.",
        "karaka": "karman of the second kṛtvā (i=11)",
        "glossaryKey": null,
        "translatable": false,
        "compound": {
          "type": "dvandva",
          "vigraha": "prāṇaś ca apānaś ca prāṇāpānau",
          "members": [
            "prāṇa",
            "apāna"
          ]
        },
        "parts": [
          {
            "form": "pra-",
            "gloss": "forth, forward"
          },
          {
            "form": "√an",
            "gloss": "to breathe"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the outgoing, upward vital breath')"
          },
          {
            "form": "apa-",
            "gloss": "away, down"
          },
          {
            "form": "√an",
            "gloss": "to breathe"
          },
          {
            "form": "-a",
            "gloss": "(ghañ, the action-noun: 'the downward, eliminative breath')"
          }
        ],
        "note": "prāṇa and apāna are two of the five named vital breaths; no single English word carries the precise directional pair, so both stay in IAST."
      },
      {
        "i": 10,
        "deva": "समौ",
        "iast": "samau",
        "gloss": "equal, even",
        "stem": "sama",
        "root": null,
        "affix": "au (dvitīyā dvivacana)",
        "morph": "acc. dual masc.",
        "karaka": "predicate accusative complement of kṛtvā, describing prāṇāpānau",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "sama",
            "gloss": "equal, even, level, the same"
          }
        ]
      },
      {
        "i": 11,
        "deva": "कृत्वा",
        "iast": "kṛtvā",
        "gloss": "having made",
        "stem": null,
        "root": "√kṛ (tanādi, 8U)",
        "rootGloss": "to make, to do, to perform, to put",
        "affix": "ktvā (kṛt)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same unstated kartṛ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√kṛ",
            "gloss": "to make, to do, to perform, to put"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ]
      },
      {
        "i": 12,
        "deva": "नासाभ्यन्तरचारिणौ",
        "iast": "nāsā-abhyantara-cāriṇau",
        "gloss": "moving within the nostrils",
        "stem": "nāsā-abhyantara-cārin",
        "root": "√car (bhvādi, 1P)",
        "rootGloss": "to move, to roam, to walk; with an object: to engage in, to practise",
        "affix": "ṇini (kṛt, habitual agent) + au (prathamā/dvitīyā dvivacana)",
        "morph": "acc. dual masc.",
        "karaka": "attribute of prāṇāpānau",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "upapada tatpuruṣa (with a locative tatpuruṣa first member)",
          "vigraha": "nāsāyāḥ abhyantare carataḥ tau",
          "members": [
            "nāsā",
            "abhyantara",
            "cārin"
          ]
        },
        "parts": [
          {
            "form": "nāsā",
            "gloss": "nose, nostril"
          },
          {
            "form": "abhyantara",
            "gloss": "interior, inside"
          },
          {
            "form": "√car",
            "gloss": "to move, to roam, to walk"
          },
          {
            "form": "-in",
            "gloss": "(ṇini, the agent-suffix: 'the one who habitually moves')"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "No independent finite clause: two absolutives govern the whole verse. sparśān — karman of kṛtvā (i=1); bāhyān — attribute of sparśān; bahiḥ — adverbial complement of kṛtvā; cakṣuḥ — karman of the elided verb carried over from kṛtvā; antare — adhikaraṇa, taking bhruvoḥ as its genitive complement; prāṇāpānau — karman of the second kṛtvā (i=11); samau — predicate accusative of that kṛtvā; nāsābhyantaracāriṇau — attribute of prāṇāpānau.",
      "verbalModality": "No finite verb: two absolutives (kṛtvā, kṛtvā), naming actions completed prior to the finite predication that only arrives with 5.28's nominal sentence."
    }
  },
  {
    "locus": "5.28",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "यतेन्द्रियमनोबुद्धिर् मुनिर् मोक्षपरायणः ।\nविगतेच्छाभयक्रोधो यः सदा मुक्त एव सः ॥",
    "iast": "yatendriyamanobuddhir munir mokṣaparāyaṇaḥ |\nvigatecchābhayakrodho yaḥ sadā mukta eva saḥ ||",
    "sense": "He who is a sage with senses, manas and buddhi controlled, intent on liberation, free from desire, fear and krodha — such a one is forever liberated indeed.",
    "english": "{4:He who} — {0:whose indriyas, manas and buddhi are controlled}, {1:a sage}, {2:devoted to liberation}, {3:from whom desire, fear and krodha have departed} — {5:is always} {6:liberated} {7:indeed}: {8:he}.",
    "words": [
      {
        "i": 0,
        "deva": "यतेन्द्रियमनोबुद्धिः",
        "iast": "yata-indriya-mano-buddhiḥ",
        "gloss": "whose indriyas, manas and buddhi are controlled",
        "stem": "yata-indriya-manas-buddhi",
        "root": "√yam (bhvādi, 1P)",
        "rootGloss": "to hold, to hold in, to check, to restrain",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of yaḥ (nominative apposition)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with a dvandva second member)",
          "vigraha": "indriyāṇi ca manaś ca buddhiś ca indriya-mano-buddhayaḥ; yatāḥ indriya-mano-buddhayaḥ yena saḥ",
          "members": [
            "yata",
            "indriya",
            "manas",
            "buddhi"
          ]
        },
        "parts": [
          {
            "form": "√yam",
            "gloss": "to hold, to hold in, to check, to restrain"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          },
          {
            "form": "indriya",
            "gloss": "indriya — a power of sense or of action"
          },
          {
            "form": "manas",
            "gloss": "manas — the faculty that intends, hesitates and turns things over"
          },
          {
            "form": "buddhi",
            "gloss": "buddhi — the faculty that discriminates and settles a matter"
          }
        ]
      },
      {
        "i": 1,
        "deva": "मुनिः",
        "iast": "muniḥ",
        "gloss": "the sage, one given to silent reflection",
        "stem": "muni",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind",
        "affix": "i (Uṇādi kṛt)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate, in apposition to yaḥ",
        "glossaryKey": "muni",
        "translatable": true,
        "parts": [
          {
            "form": "√man",
            "gloss": "to think, to consider, to have in mind"
          },
          {
            "form": "-i",
            "gloss": "(Uṇādi kṛt, forming the agent-noun: 'the one who thinks' — the silent sage)"
          }
        ]
      },
      {
        "i": 2,
        "deva": "मोक्षपरायणः",
        "iast": "mokṣa-parāyaṇaḥ",
        "gloss": "intent on liberation, for whom liberation is the supreme goal",
        "stem": "mokṣa-parāyaṇa",
        "root": "√i (adādi, 2P)",
        "rootGloss": "to go, to move, to proceed",
        "affix": "ana (lyuṭ, kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute, in apposition to yaḥ",
        "glossaryKey": "moksa",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mokṣaḥ parāyaṇaṃ yasya saḥ",
          "members": [
            "mokṣa",
            "para",
            "ayana"
          ]
        },
        "parts": [
          {
            "form": "mokṣa",
            "gloss": "liberation, release"
          },
          {
            "form": "para",
            "gloss": "highest, ultimate, supreme"
          },
          {
            "form": "√i",
            "gloss": "to go, to move, to proceed"
          },
          {
            "form": "-ana",
            "gloss": "(lyuṭ, the action/place-noun: 'the going, the resort, the goal')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "विगतेच्छाभयक्रोधः",
        "iast": "vigatecchābhayakrodhaḥ",
        "gloss": "from whom desire, fear and krodha have departed",
        "stem": "vigata-icchā-bhaya-krodha",
        "root": "√gam (bhvādi, 1P)",
        "rootGloss": "to go, to go away, to depart",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute, in apposition to yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with a dvandva second member)",
          "vigraha": "icchā ca bhayaṃ ca krodhaś ca icchā-bhaya-krodhāḥ; vigatāḥ icchā-bhaya-krodhāḥ yasmāt saḥ",
          "members": [
            "vigata",
            "icchā",
            "bhaya",
            "krodha"
          ]
        },
        "parts": [
          {
            "form": "√gam",
            "gloss": "to go, to go away, to depart"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          },
          {
            "form": "icchā",
            "gloss": "wish, desire, longing"
          },
          {
            "form": "bhaya",
            "gloss": "fear, dread"
          },
          {
            "form": "krodha",
            "gloss": "anger, wrath, rage"
          }
        ]
      },
      {
        "i": 4,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "who, the one who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the relative clause, correlative with saḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "yad",
            "gloss": "who, which (the relative pronoun stem)"
          }
        ]
      },
      {
        "i": 5,
        "deva": "सदा",
        "iast": "sadā",
        "gloss": "always, ever, at all times",
        "stem": "sadā",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of time",
        "karaka": "adhikaraṇa (temporal), modifying muktaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "sadā",
            "gloss": "always, ever, at all times"
          }
        ]
      },
      {
        "i": 6,
        "deva": "मुक्तः",
        "iast": "muktaḥ",
        "gloss": "freed, released, liberated",
        "stem": "mukta",
        "root": "√muc (tudādi, 6U)",
        "rootGloss": "to release, to set free, to let go",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate of saḥ, under an implied copula",
        "glossaryKey": "moksa",
        "translatable": true,
        "parts": [
          {
            "form": "√muc",
            "gloss": "to release, to set free, to let go"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past passive participle: 'having been —ed')"
          }
        ]
      },
      {
        "i": 7,
        "deva": "एव",
        "iast": "eva",
        "gloss": "indeed, certainly",
        "stem": "eva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on muktaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "eva",
            "gloss": "indeed, just, exactly, only (emphatic particle)"
          }
        ]
      },
      {
        "i": 8,
        "deva": "सः",
        "iast": "saḥ",
        "gloss": "he",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the implied copula, correlative with yaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "tad",
            "gloss": "that, he, it (the anaphoric/demonstrative stem)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "One relative-correlative sentence (yaḥ ... saḥ) with an implied copula. yaḥ — kartṛ of the relative clause; yatendriyamanobuddhiḥ, muniḥ, mokṣaparāyaṇaḥ, vigatecchābhayakrodhaḥ, muktaḥ — five nominatives in apposition to yaḥ; sadā — adhikaraṇa of time; eva — emphatic particle; saḥ — the correlative demonstrative, subject of the implied copula.",
      "verbalModality": "No finite verb: the relative-correlative construction (yaḥ ... saḥ) closes the participial span begun in 5.27 with a string of nominative epithets under an implied 'is', naming a standing state rather than an event."
    }
  },
  {
    "locus": "5.29",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "भोक्तारं यज्ञतपसां सर्वलोकमहेश्वरम् ।\nसुहृदं सर्वभूतानां ज्ञात्वा मां शान्तिम् ऋच्छति ॥",
    "iast": "bhoktāraṃ yajñatapasāṃ sarvalokamaheśvaram |\nsuhṛdaṃ sarvabhūtānāṃ jñātvā māṃ śāntim ṛcchati ||",
    "sense": "One who knows me as the enjoyer of sacrifices and austerities, the great lord of all worlds, and the friend of all beings, attains peace.",
    "english": "{5:Having known} {6:me} — {0:the enjoyer} {1:of sacrifices and austerities}, {2:the great lord of all worlds}, {3:the friend} {4:of all beings} — {8:he attains} {7:peace}.",
    "words": [
      {
        "i": 0,
        "deva": "भोक्तारम्",
        "iast": "bhoktāram",
        "gloss": "the enjoyer, the one who partakes",
        "stem": "bhoktṛ",
        "root": "√bhuj (rudhādi, 7U)",
        "rootGloss": "to enjoy, to eat, to partake of, to experience",
        "affix": "tṛc (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of jñātvā, predicate accusative in apposition to mām",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√bhuj",
            "gloss": "to enjoy, to eat, to partake of, to experience"
          },
          {
            "form": "-tṛ",
            "gloss": "(tṛc, the agent-noun: 'the one who —s')"
          }
        ]
      },
      {
        "i": 1,
        "deva": "यज्ञतपसाम्",
        "iast": "yajña-tapasām",
        "gloss": "of sacrifices and austerities",
        "stem": "yajña-tapas",
        "root": "√yaj (bhvādi, 1U)",
        "rootGloss": "to sacrifice, to worship, to offer in sacrifice",
        "affix": "ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. neut.",
        "karaka": "sambandha, genitive complement of bhoktāram",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "dvandva",
          "vigraha": "yajñāś ca tapāṃsi ca yajña-tapāṃsi, teṣām",
          "members": [
            "yajña",
            "tapas"
          ]
        },
        "parts": [
          {
            "form": "√yaj",
            "gloss": "to sacrifice, to worship, to offer in sacrifice"
          },
          {
            "form": "-na",
            "gloss": "(naṅ, the kṛt action-noun: 'the sacrifice')"
          },
          {
            "form": "√tap",
            "gloss": "to heat, to burn; to practise austerity, to undergo penance"
          },
          {
            "form": "-as",
            "gloss": "(asun, the neuter action-noun: 'austerity, penance')"
          }
        ]
      },
      {
        "i": 2,
        "deva": "सर्वलोकमहेश्वरम्",
        "iast": "sarva-loka-mahā-īśvaram",
        "gloss": "the great lord of all the worlds",
        "stem": "sarva-loka-mahā-īśvara",
        "root": "√īś (adādi, 2Ā)",
        "rootGloss": "to rule, to be capable, to have power over",
        "affix": "vara (Uṇādi kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of jñātvā, predicate accusative in apposition to mām",
        "glossaryKey": "isvara",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī), with two karmadhāraya members",
          "vigraha": "sarve ca te lokāḥ ca sarva-lokāḥ; teṣāṃ mahān īśvaraḥ",
          "members": [
            "sarva",
            "loka",
            "mahat",
            "īśvara"
          ]
        },
        "parts": [
          {
            "form": "sarva",
            "gloss": "all, every"
          },
          {
            "form": "loka",
            "gloss": "world, realm"
          },
          {
            "form": "mahā-",
            "gloss": "great, vast (the compounding form of mahat)"
          },
          {
            "form": "√īś",
            "gloss": "to rule, to be capable, to have power over"
          },
          {
            "form": "-vara",
            "gloss": "(Uṇādi kṛt, the agent-noun: 'the ruler, the lord')"
          }
        ]
      },
      {
        "i": 3,
        "deva": "सुहृदम्",
        "iast": "suhṛdam",
        "gloss": "the friend, the well-wisher",
        "stem": "suhṛd",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of jñātvā, predicate accusative in apposition to mām",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "śobhanaṃ hṛdayaṃ yasya saḥ, tam",
          "members": [
            "su",
            "hṛd"
          ]
        },
        "parts": [
          {
            "form": "su-",
            "gloss": "good, well; happy, pleasant"
          },
          {
            "form": "hṛd",
            "gloss": "heart"
          }
        ]
      },
      {
        "i": 4,
        "deva": "सर्वभूतानाम्",
        "iast": "sarva-bhūtānām",
        "gloss": "of all beings",
        "stem": "sarva-bhūta",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "ām (ṣaṣṭhī bahuvacana)",
        "morph": "gen. pl. neut.",
        "karaka": "sambandha, genitive complement of suhṛdam",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "karmadhāraya",
          "vigraha": "sarvāṇi ca tāni bhūtāni ca, teṣām",
          "members": [
            "sarva",
            "bhūta"
          ]
        },
        "parts": [
          {
            "form": "sarva",
            "gloss": "all, every"
          },
          {
            "form": "√bhū",
            "gloss": "to be, to become, to arise, to come into being"
          },
          {
            "form": "-ta",
            "gloss": "(kta, past participle used as a noun: 'a being')"
          }
        ]
      },
      {
        "i": 5,
        "deva": "ज्ञात्वा",
        "iast": "jñātvā",
        "gloss": "having known, having understood",
        "stem": null,
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to understand, to recognize",
        "affix": "ktvā (kṛt)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same unstated kartṛ",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          {
            "form": "√jñā",
            "gloss": "to know, to understand, to recognize"
          },
          {
            "form": "-tvā",
            "gloss": "(ktvā, the absolutive: 'having —ed')"
          }
        ]
      },
      {
        "i": 6,
        "deva": "माम्",
        "iast": "mām",
        "gloss": "me",
        "stem": "asmad",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg.",
        "karaka": "karman of jñātvā (the primary object)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "asmad",
            "gloss": "I, me (the first-person stem)"
          }
        ]
      },
      {
        "i": 7,
        "deva": "शान्तिम्",
        "iast": "śāntim",
        "gloss": "peace, tranquility, cessation",
        "stem": "śānti",
        "root": "√śam (divādi, 4P)",
        "rootGloss": "to become calm, to be pacified, to cease, to be quieted",
        "affix": "ktin (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. fem.",
        "karaka": "karman of ṛcchati",
        "glossaryKey": "santi",
        "translatable": true,
        "parts": [
          {
            "form": "√śam",
            "gloss": "to become calm, to be pacified, to cease, to be quieted"
          },
          {
            "form": "-ti",
            "gloss": "(ktin, the feminine action-noun: 'peace, tranquility')"
          }
        ]
      },
      {
        "i": 8,
        "deva": "ऋच्छति",
        "iast": "ṛcchati",
        "gloss": "attains, reaches, arrives at, goes to",
        "stem": null,
        "root": "√ṛch (tudādi, 6P)",
        "rootGloss": "to go; to reach, to arrive at, to attain",
        "affix": "śa + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ unstated (the one who has known me thus), karman śāntim",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          {
            "form": "√ṛch",
            "gloss": "to go; to reach, to arrive at, to attain"
          },
          {
            "form": "-a-",
            "gloss": "(śa, the present-stem marker of the tudādi class)"
          },
          {
            "form": "-ti",
            "gloss": "(3rd person singular, active)"
          }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "One sentence built on the absolutive jñātvā. mām — karman of jñātvā; bhoktāram, sarvalokamaheśvaram, suhṛdam — three predicate accusatives in apposition to mām, naming what is known; yajñatapasām — sambandha with bhoktāram; sarvabhūtānām — sambandha with suhṛdam; śāntim — karman of ṛcchati.",
      "verbalModality": "One finite verb, ṛcchati (laṭ, present indicative parasmaipada) — the peace that follows is stated as present fact, contingent on the prior absolutive jñātvā ('having known')."
    }
  }
];
