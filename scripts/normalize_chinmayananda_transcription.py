#!/usr/bin/env python3
"""Normalize the scan-backed Chinmayananda transcription for publication.

The printed scan is the authority.  This pass deliberately does not import
text from either OCR witness merely because it looks plausible: it applies
only canonical name headings, reviewed Sanskrit spellings, scan-confirmed OCR
repairs, and page-locus corrections.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTION = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
ANALYSIS = ROOT / "gita/vishnu-sahasranama/analysis.json"

SCAN_PAGE_OVERRIDES = {
    48: [33], 75: [41], 129: [53, 54], 199: [71],
    430: [126, 127], 531: [146, 147], 673: [175, 176], 679: [177, 178],
    770: [198, 199], 793: [206, 207],
}

# Exact scan-confirmed repairs for characters introduced by OCR script
# confusion.  These strings were checked on the named scan pages.
ENTRY_REPAIRS = {
    14: {
        "पुरि शेते इति पुरुष:": "पुरि शेते इति पुरुषः",
        "प्रा आसीत् इति प्रव:": "पुरा आसीत् इति पुरुषः",
        "परयति इति पुरुष:": "पूरयति इति पुरुषः",
    },
    27: {"स ब्रह्म स: शिव:": "स ब्रह्म सः शिवः"},
    36: {"ईष्टे इति ईश्वर:": "ईष्टे इति ईश्वरः"},
    59: {"तर्द हिसायां": "तर्द हिंसायाम्"},
    62: {"(पनि)": "(पवि)"},
    100: {"यस्मान्न च्यतपूर्वोऽहं अच्यतस्तेन कर्मणा": "यस्मान्न च्युतपूर्वोऽहमच्युतस्तेन कर्मणा"},
    106: {"सत्स साथ: सत्य:": "सत्सु साधुः सत्यम्"},
    107: {"एको वशी सर्वभूतान्तरात्मा एक बहुधा यः करोति तमात्मस्थं यऽनुपत्रयन्ति धीरास्तेषां सूखं…": "एको वशी सर्वभूतान्तरात्मा एकं रूपं बहुधा यः करोति । तमात्मस्थं येऽनुपश्यन्ति धीरास्तेषां सुखं शाश्वतं नेतरेषाम् ॥"},
    117: {"विश्वस्य योनि: विश्वयोनि:": "विश्वस्य योनिः विश्वयोनिः"},
    127: {"सर्वे वेदा: सर्वेविद्या: संशास्त्राः सर्वयज्ञाः सर्वज्ञञ्च कृष्णः": "सर्वे वेदाः सर्वविद्याः सर्वशास्त्राः सर्वयज्ञाः सर्वज्ञश्च कृष्णः"},
    130: {"वेदाः सर्वाङ्गानि…": "वेदाः सर्वाङ्गानि"},
    132: {"कविर्मनीषी परिभः स्वयंभूः": "कविर्मनीषी परिभूः स्वयंभूः"},
    148: {"सत्यमेव जयते नानतं": "सत्यमेव जयते नानृतम्"},
    150: {"वसति इति वस:": "वसति इति वसुः"},
    175: {"(शिक्त)": "(शक्ति)", "(किया-काम-ज्ञान)": "(क्रिया-काम-ज्ञान)"},
    177: {"(वव्)": "(वपुः)"},
    181: {"(शार्ड)": "(शार्ङ्ग)"},
    182: {"(बराह)": "(वराह)"},
    186: {"आनन्दं ब्रह्मोति व्यजानात्": "आनन्दं ब्रह्मेति व्यजानात्"},
    195: {"स तपः तप्तवा इदमेतदस्जत्": "स तपोऽतप्यत । स तपस्तप्त्वा इदं सर्वमसृजत"},
    213: {"सत्यमेव जयते न अनुतं": "सत्यमेव जयते नानृतम्"},
    215: {"इन्ट: दन्टे: अविपरिलोपात पश्यन्नेव भवति": "द्रष्टुर्दृष्टेरविपरिलोपात् पश्यन्नेव भवति"},
    227: {"सहस्रशीर्षा पृरुष: सहस्राक्ष: सहस्रपात्": "सहस्रशीर्षा पुरुषः सहस्राक्षः सहस्रपात्"},
    241: {"सतकरोति इति सत्कर्ता": "सत्करोति इति सत्कर्ता"},
    243: {"साधयति इति साध:": "साधयति इति साधुः"},
    258: {"क्रमणात चाप्यहं पार्थ विष्णरित्यभिसंज्ञित:।": "क्रमणाच्चाप्यहं पार्थ विष्णुरित्यभिसंज्ञितः।", "इदं विष्ण: विचक्रमे": "इदं विष्णुर्विचक्रमे"},
    270: {"यस्त् सर्वाणि भृतानि आत्मन्येवानुपश्यति । सर्वभृतेषु चात्मानं ततो न विज्गुप्सते ।।": "यस्तु सर्वाणि भूतान्यात्मन्येवानुपश्यति । सर्वभूतेषु चात्मानं ततो न विजुगुप्सते ॥"},
    271: {"जलं विष्णु: स्थलं विष्णु: विष्णुराकाशमुच्यते । स्थावरं जंगमं विष्णुः सर्वं विष्णुमयं जगत्।।": "जलं विष्णुः स्थलं विष्णुर्विष्णुराकाशमुच्यते । स्थावरं जङ्गमं विष्णुः सर्वं विष्णुमयं जगत् ॥"},
    280: {"मननात त्रायते इति मंत्र:": "मननात् त्रायते इति मन्त्रः"},
    312: {"(ईव्वर:)": "(ईश्वरः)"},
    386: {"(प्रलय:)": "(प्रलयः)"},
    455: {"अभयं सर्वभूतेभ्यो ददाम्येतत् व्रतं मम": "अभयं सर्वभूतेभ्यो ददाम्येतद् व्रतं मम"},
    464: {"(भदार:)": "(भूदारः)"},
    547: {"(स्रष्टा)": "(स्रष्टा)", "(प्रजापति:)": "(प्रजापतिः)"},
    539: {"गोभिरेव यतो वेद्यो गोविन्द: समुदाहृत: ।": "गोभिरेव यतो वेद्यो गोविन्दः समुदाहृतः ।"},
    627: {"(स्थिर:)": "(स्थिरः)", "(शाइवत:)": "(शाश्वतः)"},
    831: {"(अघ:)": "(अघः)"},
    846: {"( वर्ष )": "( वर्ध् )"},
    900: {"(अव्यय:)": "(अव्ययः)"},
    311: {" গিৰত্ত ": " शिखण्ड "},
    313: {"Ishtalı": "Iṣṭaḥ"},
    389: {"† † Ŋ:": "††"},
    702: {"(পুরি)": "(भूति)", "(ऐश्वयं)": "(ऐश्वर्यं)"},
    796: {"( লক্ষম: चक्ष:)": "(चक्षुषश्चक्षुः)"},
    827: {"হৰ:=tomorrow; হৰ্থ=remaining tomorrow also;": "श्वः = tomorrow; श्वत्थ = remaining tomorrow also;"},
    845: {"(পুৰাণ पुरुष:)": "(पुराणपुरुषः)"},
}

# The printed opening sentence is not always a definition.  These reviewed
# concise meanings replace extraction preambles, cross-references, lexical
# discussion, and overlong exposition in the Simple reader only.  The source
# wording remains untouched in short_meaning/commentary and therefore remains
# visible in Full mode.
SIMPLE_MEANING_OVERRIDES = {
    2: "The all-pervading one",
    3: "The sacred vaṣaṭ call through which offerings are made",
    6: "The sustainer and nourisher of all beings",
    7: "Existence becoming all moving and unmoving beings",
    9: "The creator and nourisher of all beings",
    10: "The supremely pure Self",
    11: "The supreme self beyond all material limitations",
    13: "The changeless and imperishable one",
    17: "Indestructible",
    24: "The supreme person, beyond the perishable and imperishable",
    26: "The auspicious one who bestows auspiciousness",
    28: "The firm and immovable one",
    36: "The independent lord whose power needs no aid",
    39: "The golden person shining within the sun",
    41: "The one whose commanding voice is thunderous",
    45: "The supreme essence underlying every existent thing",
    46: "The one beyond definition and comparison",
    47: "The lord of the senses",
    50: "The maker of the universe and all experience",
    51: "The reflective thinker who contemplates the highest",
    53: "The supremely gross—the whole universe as Viṣṇu's form",
    55: "The ungraspable subject, never an object of perception",
    57: "The dark-hued one",
    59: "The supreme destroyer",
    60: "The ever-full and abundant one",
    66: "The life-breath that sustains all",
    68: "The most excellent and glorious one",
    76: "The wielder of the divine bow Śārṅga",
    78: "The one of mighty stride who measured the universe",
    82: "The knower of all deeds",
    85: "The lord of the gods",
    88: "The seed from which the universe arises",
    91: "The Lord of Time, from whom the concept of time arises",
    94: "The all-seeing one",
    99: "The beginning of all",
    100: "The unfallen and ever-pure one",
    101: "The Boar who raises the world from adharma to dharma",
    103: "The one free from every bond and attachment",
    105: "The one whose mind is supremely pure",
    108: "The acceptable one",
    110: "The unfailing one whose acts are never futile",
    111: "The one realized in the lotus of the heart",
    112: "The one whose actions are dharma",
    123: "The all-pervading one who has gone everywhere",
    125: "The one before whom hostile armies scatter",
    126: "The one who brings sorrow to the vicious and joy to the good",
    127: "The Veda; knowledge itself",
    131: "The knower and contemplator of the Veda",
    132: "The seer",
    134: "The lord of the gods",
    136: "The one who is both cause and manifested effect",
    137: "The fourfold self",
    139: "The four-tusked one",
    142: "Food; all that is experienced",
    145: "The one born at the very beginning of the world",
    146: "The sinless and faultless one",
    149: "The source of the universe, or he whose source is the universe",
    152: "The small-bodied Vāmana incarnation",
    153: "The tall one whose body fills the sky",
    161: "The appointing authority who orders the laws of nature",
    165: "The one always united in yoga",
    167: "The lord of Lakṣmī",
    168: "The one sweet as honey to his devotees",
    169: "The one beyond the senses and their functions",
    173: "The one of great intelligence",
    178: "The possessor of glory",
    181: "The wielder of the great bow Śārṅga",
    187: "The supporter of all and protector of the cows",
    189: "The ray of light in all that shines",
    191: "The Self realized as 'I am He'",
    192: "The beautiful-winged one",
    193: "The greatest serpent, Ananta",
    207: "The self celebrated throughout the Vedas",
    208: "The destroyer of the enemies of the gods",
    209: "The teacher",
    210: "The greatest teacher",
    214: "The one whose eyes close in inward contemplation",
    216: "The wearer of an unfading garland",
    217: "The lord of speech, endowed with generous intelligence",
    220: "The radiant possessor of splendor",
    221: "Justice and the reasoning that leads to scriptural truth",
    226: "The thousand-eyed cosmic form",
    234: "Air; the beginningless, all-pervading enjoyer",
    242: "The one honored and worshiped by the good",
    245: "The resting place of all beings",
    247: "The one beyond all counting",
    248: "The one whose self cannot be measured by any proof",
    253: "The one whose resolve is always fulfilled",
    256: "The controller of actions and dispenser of their results",
    257: "The embodiment of dharma who showers desired fruits",
    259: "The ladder whose steps are dharma",
    260: "The one whose depths contain the source of creation",
    263: "The solitary and distinct one",
    269: "The giver of wealth",
    270: "The one manifest as wealth, the veil, and the nourishing sun",
    271: "The one of infinite forms",
    283: "The source of the nectar-rayed moon",
    285: "The moon marked like a hare",
    286: "The lord of the shining gods",
    288: "The bridge by which one crosses egocentric imperfection to Infinite Perfection",
    292: "The one who gives air its life-sustaining and purifying power",
    293: "The sacred fire",
    279: "The one whose imperishable syllable is clear",
    300: "The creator of the ages",
    301: "The one who turns the wheel of the ages",
    303: "The consumer into whom perceptions, emotions, and thoughts are swallowed in samādhi",
    304: "The one unseen by senses, mind, or intellect",
    308: "The beloved one",
    311: "The wearer of the peacock plume",
    312: "The one who binds beings through māyā",
    313: "The embodiment of dharma",
    323: "The ocean, treasury of the waters",
    325: "The unerring one who is never careless",
    320: "The life manifest in every living being",
    327: "The Lord whose glory is expressed through Skanda, commander of the righteous host",
    333: "The vast light whose rays illumine sun and moon",
    334: "The first of the gods",
    338: "The savior from the fear of rebirth",
    340: "Kṛṣṇa, descendant of Śūrasena",
    343: "The one of innumerable manifestations",
    350: "The one of magnificent prosperity and power",
    353: "The great-eyed one",
    357: "The formidable and awe-inspiring one",
    358: "The knower of every philosophy and the right time for every act",
    360: "The one indicated by every valid mark and method of knowledge",
    363: "The imperishable one",
    364: "The Fish incarnation",
    367: "The one known through self-control and a purified mind",
    383: "The one hidden in the cave of the heart",
    391: "The ever-contented one",
    395: "The abode of perfect rest",
    403: "Dharma itself, the law that upholds",
    408: "The giver and withdrawer of life-breath",
    411: "The golden womb, the cosmic creator",
    416: "Time as the ordered cycle of seasons",
    417: "The one whose auspicious vision is readily gained through devotion",
    477: "The upholder in whom dharma rests",
    479: "The conditioned one",
    508: "The one of supreme humility",
    511: "Kṛṣṇa of the Dāśārha lineage",
    517: "The ocean",
    548: "The beautiful one whose limbs are perfectly proportioned",
    539: "The one known through the declarations of the Veda",
    552: "The one who draws all into himself yet never falls",
    553: "The evening sun at the western horizon",
    554: "The son of Varuṇa",
    558: "The possessor of wealth, power, dharma, fame, character, knowledge, and detachment",
    563: "The son of Aditi",
    567: "The bearer of the splendid bow Śārṅga",
    568: "The bearer of the battle-axe",
    572: "The all-seeing Vyāsa who arranged the Vedas",
    578: "The medicine for worldly suffering",
    580: "The institutor of renunciation",
    593: "The protector who also veils himself",
    628: "Rāma resting upon the earth beside the ocean",
    648: "The long-haired Kṛṣṇa",
    649: "The slayer of the demon Keśī",
    644: "Kṛṣṇa of the Śūrasena clan",
    650: "The destroyer who removes sorrow and sin",
    662: "The one who brings forth and lives in sacred knowledge",
    667: "The knower of Brahman who sees unity beneath plurality",
    691: "The ancient teacher of all vidyās and tantras",
    694: "The giver of liberation",
    707: "The one attended by the righteous people of the Yamunā",
    713: "The one who gives the righteous a pride that protects their virtue",
    715: "The one difficult to hold in contemplation",
    718: "The great cosmic form supporting creation",
    721: "The one of many forms and incarnations",
    723: "The one of myriad forms",
    737: "The golden-coloured one",
    758: "The bearer of radiance",
    763: "The many-horned one",
    809: "The one lovely as the kunda flower",
    813: "The one whose aspiration is immortality",
    824: "The tree of life",
    817: "The one readily attained through true devotion",
    849: "The supreme yogī, realized through yoga",
    858: "The revealer of archery and the unfailing technique of Oṃ-meditation",
    864: "The supreme controller, controlled by none",
    875: "The one who increases love and joy",
    876: "The one whose path is the sky",
    878: "The one of beautiful radiance and auspicious will",
    883: "The sun that nurtures and nourishes all living creatures",
    902: "The maker and remover of auspicious conditions",
    907: "The wearer of makara earrings",
    908: "The bearer of the discus Sudarśana",
    913: "The cool season that relieves burning heat",
    914: "The maker of night and darkness",
    912: "The one who permits invocation through sacred sound",
    917: "The prompt and capable one",
    924: "The destroyer of evil deeds",
    929: "The one present as the good and saintly",
    945: "The wearer of resplendent shoulder-caps",
    954: "The exalted one",
    951: "The unsurpassed supreme controller",
    964: "The knower of reality as it truly is",
    965: "The one Self",
    987: "The Boar who dug through the earth to destroy Hiraṇyākṣa",
    976: "The ruler of yajñas",
    985: "Self-born",
    986: "Self-born",
    994: "The bearer of the sword Nandaka",
    995: "The bearer of the discus Sudarśana",
    996: "The wielder of the bow Śārṅga",
    997: "The mace-bearer",
    998: "The one whose hand holds the chariot wheel",
}

SIMPLE_META = re.compile(
    r"\b(?:term|word|root|means?|meaning|interpreted|interpretation|dissolved|degree|"
    r"familiar|etymolog|commented|used|stands for|indicates?|connotes?|reference|"
    r"controvers|earlier|above|below|here we|we read|we find|can be|is called|name of|"
    r"called|describ|declar|previous|already|\bwe\b|sanskrit|prefix|suffix|superlative|"
    r"comparative|appellation|purāṇ|puran|iti)\b|=",
    re.I,
)

# The former Simple layer used concise editorial paraphrases for these names.
# They were faithful in intent, but the UI called them "direct" even when the
# exact wording was not Chinmayananda's.  These excerpts select his own words
# when the automatic sentence matcher would otherwise choose a nearby example,
# citation, or secondary interpretation.  Punctuation may be regularized by
# ``normalize_simple_excerpt``; the lexical wording must replay the commentary.
SIMPLE_EXCERPT_OVERRIDES = {
    13: "The Indestructible, and therefore, changeless",
    24: "This Transcendental Truth is indicated by the term the Supreme puruṣa (Purushottama).",
    39: "The Truth (puruṣa) that glows with a golden splendour in the solar orb is called ādityaḥ.",
    45: "Of the endless varieties of dhātus available in existence, the subtlest dhātu. without which no existence, is ever possible, is the Chit dhātu, and this is dhātu-ruttamah.",
    46: "He, who cannot be defined and explained in terms of any logical terms of reference with other things, should necessarily be inexpressible.",
    53: "It is the superlative degree of gross (sthoola) and thus 'the Supremely gross' is the subtlest Reality.",
    55: "That which cannot be perceived through the play of the sense-organs",
    59: "One who does this total destruction (pratardanaḥ) is the Lord in the form of Rudra at the time of the great dissolution (Pralaya).",
    78: "Vikrama is an appellation that had come to Viṣṇu as a result of His Supernatural Act of measuring the universe with three steps.",
    88: "He who is the very cause for the entire play of experience in the world of pluralistic objects (Sarva — Prapancha — Kaaranabhootah) is called viśvaretāḥ.",
    94: "It is indeed the One Seer in all 'seeing', by everyone, everywhere.",
    100: "One who has never fallen",
    108: "The term Sammatam means 'acceptable'.",
    110: "Amogha is the opposite of it: 'Ever Useful', 'Ever the Ful-filler' of all the wishes and demands of His devotees.",
    123: "'He who has gone everywhere', meaning 'One who pervades everything'.",
    127: "Since Veda gives knowledge, the Lord is termed as vedaḥ",
    131: "‘One who contemplates upon the Veda is vedavit’: (Vedam Vichaarayati = vedavit).",
    134: "The President of the Heavens to whom the Devas run for protection when they are threatened by their constant enemies - the Daityas and the Asuras.",
    136: "The former (kṛtam) indicates all the \"effects\" manifested out of the Creator's activities, and the latter (Akritam) is the \"cause\" from which no manifestation has yet emerged — it is still unmanifest.",
    139: "He whose glory is the four-tusked Airaavata is Maha — Viṣṇu.",
    149: "It can be interpreted in two ways as (a) He who is the Cause of the universe or (b) He who has the world as His Cause.",
    146: "Agham means sin (pāpa), impurities (mala); and therefore, anaghaḥ means One who has no imperfections",
    152: "Of the ten great incarnations, the fifth one is Vāmana; and the very name indicates 'One who has a small body'.",
    161: "The Appointing Authority",
    163: "That which is to be known",
    165: "The Goal, the Self, therefore, in the language of the seeker must be Sadaayoga-ever in yoga.",
    169: "One who is beyond the sense-organs",
    214: "The condition of \"the eyelids closed\" is called nimiṣaḥ",
    217: "vācaspati is a term given to One who is eloquent in championing the Supreme law of life; and dhī means the power of intelligence; and udāradhīḥ one who has a \"Large-hearted intelligence\", One who is not puritanical in his viewpoints.",
    234: "'Air' (Vaayu)",
    242: "One who is adored by all good people",
    245: "The Shelter (Ayanam) for man (Nara) is Naaraayana.",
    256: "Therefore, vṛṣāhī means \"One who is a controller of all actions and the dispenser of all results\", in all individual, conscious, intelligent creatures.",
    260: "He is called as vṛṣodaraḥ, 'the Showering Belly.'",
    270: "The term Vasu has got three meanings: Wealth (Dhana), Veil (Aacchaadana) and Sun (Āditya)",
    279: "One who is clearly indicated by the Supreme Sound (Akshara), the famous Sound — Symbol of the Eternal Lord Om.",
    283: "Since Viṣṇu is described as ever reposing upon His Ananta-bed in Ksheerasaagara, the Lord is Himself termed here as the Begetter of the Moon.",
    285: "that which has a \"beauty-spot\" (Bindu) in the shape of a rabbit (Sasa) is called Sasabindu — the moon.",
    286: "Sura means Deva and so the term indicates 'the God of all gods'.",
    292: "Here, the present term \"pāvanaḥ\" means the One who gives this life-sustaining power to the atmospheric air.",
    293: "The term itself means Fire.",
    301: "He is also the Power behind the wheel of time that goes on changing and repeating itself",
    304: "He is the Subjective Core, the Eternal Essence, wherein, the perceived and the instruments of perceptions are all totally absent.",
    308: "One who is loved by all.",
    311: "One who wears 'śikhaṇḍa' ( शिखण्ड ) meaning 'the peacock feather'.",
    327: "Therefore, Skanda means \"the Lord, whose glory is expressed, through Subrahmanya\".",
    333: "Possessed of endless rays, meaning \"One who illumines the world with the rays of the Sun and the Moon.\"",
    338: "One who saves is called tāraḥ.",
    343: "Thus the term 'śatāvartaḥ' means 'One who takes infinite varieties of forms'.",
    353: "He is the \"Great Eye\" seeing all, at all times, as He is the Consciousness that illumines everything at all times, in all bosoms.",
    367: "He is One who is known through a mind which is purified (Udara) by means of self-control (dama) and such other qualities.",
    408: "This can mean 'One who gives prāṇa' or as 'One who takes away prāṇa', because, the root 'da' has both the meanings, 'to give' and 'to break.'",
    417: "One who is easy to be perceived if the seeker has sufficient devotion, or He whose meeting is auspicious inasmuch as it removes the seeker's worldly worries.",
    438: "The Lord is the very Post to which all dharmas (righteousness) are tied.",
    477: "The Supporter of dharma; meaning the very Seat of all dharma.",
    479: "The Conditioned; Limited; the One who appears at this moment as the limited, conditioned, and therefore confined only to the world of plurality.",
    508: "In direct meaning, of course, it means 'He who shows the supreme humility.' But the term also means 'One who humiliates those who are unrighteous.'",
    558: "One who has all the Six Great Glories—Wealth, Power, dharma, Fame, Character, Knowledge and Dispassion—is called 'bhagavān'.",
    552: "The Lord Nārāyaṇa who absorbs the whole world into Himself at the time of the deluge. and He who never falls away from His own Real Nature.",
    555: "In the Upaniṣads the world emerging out of the Supreme Brahman is described metaphorically as a 'Tree'.",
    572: "One who is Omniscient and Vyasa.",
    593: "Thus 'goptā' can imply 'One who protects the universe' or 'One who, by His māyā, veils the glory of the Divine Self within.'",
    628: "One Who rested on the shores of the ocean, on His Way to Lanka—referring to Śrī Ramachandraji.",
    644: "Born in the Soorasena-clan, in Jagannaath—which, in the Purāṇas, is called the Utkala country.",
    667: "One who has realised that the pluralistic world is a mere superimposition upon the Brahman caused by an error of judgement, and who experiences the Supreme Consciousness of the One Reality is a brāhmaṇaḥ.",
    715: "The object of contemplation which is indeed very difficult to attain",
    718: "The Great — Form- Divine of the Lord as He reclines upon the Sesha couch as the very support for the Creator to bring into existence the Universe",
    721: "One Who Himself has become the world of varieties of Forms",
    723: "Of Myriad — Forms",
    809: "In this context the term means \"One who is as comely and attractive as the kunda flowers\".",
    817: "One Who is readily available",
    824: "That which will not remain the same tomorrow.",
    878: "The suffix ‘Su’ indicates Auspiciousness (sobhana): the term ‘Ruchi’ is Glory or Desire.",
    883: "The term etymologically means the One Source from which all things have been born or out of which they have been delivered.",
    902: "One Who brings Auspiciousness or One who robs all Auspiciousness",
    908: "He Who wears ever His Discus called Su — Darsana (Auspicious Vision).",
    913: "Therefore, by suggestion, this name indicates that the Lord is the 'cool arbour' for those who are tortured by the heat of Samsar.",
    945: "One Who wears resplendent shoulder-caps",
    957: "Therefore, Śrī Nārāyaṇa is called 'praṇavaḥ': meaning He is of the 'nature of oṃkāra.'",
    986: "One Who, as the Lord of the Universe, has no other ‘Instrumental Cause’ (nimitta-kāraṇa) in projecting Himself.",
    997: "One who holds His divine Club (Mace) celebrated as Kaumodakī-which generates and spreads beauty and joy.",
}

# Chinmayananda's entry for this name introduces scriptural evidence but does
# not itself state a standalone one-line meaning. The fact belongs to the Full
# source record; Simplified may still give a clearly site-authored summary.
FULL_NO_STANDALONE_MEANING = {
    226: "The entry supplies Gītā evidence but no standalone one-line meaning.",
}

# Page-bottom apparatus on printed pp. 41–43 was swept into adjacent entries
# by OCR. These five entries are reconstructed in printed reading order from
# the page images so Full mode can preserve complete prose without raw sigils
# or misassigned quotations.
COMMENTARY_STRUCTURE_OVERRIDES = {
    93: (
        "One whose very nature is Knowledge. That the Supreme is Knowledge Absolute is very well known. "
        "It is in the light of Consciousness that all 'knowledges' are possible. 'Knowledge of a thing' is "
        "the Awareness of its nature. Awareness is Knowledge. Since the Supreme is the One Awareness everywhere, "
        "all 'Knowledges' spring from the Self. Hence, He is called \"the Pure Knowledge\". \"Consciousness is "
        "Brahman\" is one of the mahāvākyas.\n\n"
        "\"Prajñānam brahma.\" — Aitareya Upaniṣad 3.3."
    ),
    94: (
        "This term, \"All-seeing\", is very appropriate inasmuch as the Supreme Consciousness has been defined "
        "and indicated in the Kenopaniṣad as, \"That which the eyes cannot see, but because of which the eyes see.\" "
        "It is the Seer in the eyes, the Hearer in the ears, the Speaker, the Feeler and the Thinker. And since this "
        "Principle of Consciousness is One everywhere, as expressed through the equipments, It is indeed the One "
        "Seer in all 'seeing', by everyone, everywhere. The Upaniṣad says, \"विश्वतश्चक्षुर्विश्वाक्षः\", and the Gītā "
        "indicates Him as \"One who has eyes and heads everywhere\"—\"सर्वतोऽक्षिशिरोमुखम्\".\n\n"
        "Sarvadarśanaḥ: omnispective."
    ),
    95: (
        "Unborn. Birth implies a modification; birth cannot be without the death of its previous condition. Since "
        "the Eternal and the Infinite is ever Changeless, there can be in It neither birth nor death. That which is "
        "born must necessarily die (जातस्य हि ध्रुवो मृत्युः — Gītā 2.27), and so that which is unborn should be "
        "deathless (amṛta).\n\n"
        "Ṛg Veda 1.81.5: \"He was neither born nor is He going to be born.\"\n\n"
        "न जायते म्रियते वा कदाचिन्नायं भूत्वा भविता वा न भूयः ।\n"
        "अजो नित्यः शाश्वतोऽयं पुराणो न हन्यते हन्यमाने शरीरे ॥ — Gītā 2.20.\n\n"
        "In the Mahābhārata (Śānti Parva 343) we read, \"I am not born, nor am I to be born, nor have I any "
        "possibility of future birth; I am the Kṣetrajña in all beings; hence I am called 'Unborn'.\""
    ),
    98: (
        "He who is available for recognition (Siddha) everywhere at all points in His nature as Pure Consciousness. "
        "Again, Siddhi also means the 'fruit of action', and in the context here this would mean, \"He who gives the "
        "Infinite fruit of Kaivalya, mokṣa.\" All other karmas can acquire for us only relative joys of the heavens, "
        "but in realizing the Self the seeker gains an 'Infinite State from which there is no return', so describes "
        "the Gītā.\n\n"
        "यद्गत्वा न निवर्तन्ते तद्धाम परमं मम । — Gītā 15.6."
    ),
    101: (
        "There is a lot of controversy among pundits upon the exact meaning of this term. But all controversies "
        "become meaningless when we read Bhagavān's own words, \"Since Kapi has a meaning the 'boar', and since "
        "vṛṣa has the meaning of 'dharma', the great Kaśyapa Prajāpati says I am vṛṣākapiḥ.\"\n\n"
        "कपिर्वराहः श्रेष्ठश्च धर्मश्च वृष उच्यते ।\n"
        "तस्माद् वृषाकपिं प्राह कश्यपो मां प्रजापतिः ॥\n\n"
        "In Sanskrit the term Kapi has a meaning: 'that which saves one from drowning'. Lord in the form of the Great "
        "Boar (Varāha), in that incarnation, had lifted the world from the waters at the end of the deluge; the term "
        "vṛṣa means 'dharma'. One who thus lifts the world drowned in Adharma to the sunny fields of dharma is "
        "vṛṣākapiḥ."
    ),
}

APPARATUS_PACKET_PATHS = (
    ROOT / "gita/vishnu-sahasranama/apparatus/early.json",
    ROOT / "gita/vishnu-sahasranama/apparatus/middle.json",
    ROOT / "gita/vishnu-sahasranama/apparatus/late.json",
)

APPARATUS_RESIDUE = re.compile(
    r"[*†‡]|\bnewpage\b|GLORIES OF THE LORD|VISHNU SAHASRANAAMA",
)


def load_apparatus_packets() -> dict[int, dict]:
    missing = [str(path.relative_to(ROOT)) for path in APPARATUS_PACKET_PATHS if not path.exists()]
    if missing:
        raise ValueError(f"scan-apparatus correction packets are missing: {missing}")
    merged: dict[int, dict] = {}
    for path in APPARATUS_PACKET_PATHS:
        packet = json.loads(path.read_text(encoding="utf-8"))
        if packet.get("schema_version") != 1 or not isinstance(packet.get("entries"), list):
            raise ValueError(f"invalid apparatus packet schema: {path}")
        page_range = packet.get("range", {}).get("scan_pages", packet.get("range", {}).get("pdf_pages", []))
        if not (isinstance(page_range, list) and len(page_range) == 2):
            raise ValueError(f"apparatus packet lacks a scan/PDF page range: {path}")
        first_page, last_page = page_range
        name_range = packet.get("range", {}).get("names", [])
        if not (isinstance(name_range, list) and len(name_range) == 2):
            raise ValueError(f"apparatus packet lacks a name range: {path}")
        low, high = name_range
        for entry in packet["entries"]:
            number = entry.get("number")
            commentary = entry.get("commentary", "")
            if not isinstance(number, int) or not low <= number <= high:
                raise ValueError(f"apparatus packet entry outside declared range: {path} name {number}")
            if number in merged:
                raise ValueError(f"duplicate apparatus correction for name {number}")
            scan_pages = entry.get("scan_pages")
            if not (
                isinstance(scan_pages, list)
                and scan_pages
                and all(isinstance(page, int) and first_page <= page <= last_page for page in scan_pages)
            ):
                raise ValueError(f"apparatus correction for name {number} lacks an in-range scan locus")
            if not commentary.strip() or APPARATUS_RESIDUE.search(commentary):
                raise ValueError(f"apparatus correction for name {number} retains raw apparatus/page residue")
            if entry.get("basis") != "scan-checked apparatus reconstruction":
                raise ValueError(f"apparatus correction for name {number} lacks the scan-checked basis")
            normalized_entry = dict(entry)
            normalized_entry["commentary"] = normalize_packet_commentary(commentary)
            for old, new in ENTRY_REPAIRS.get(number, {}).items():
                normalized_entry["commentary"] = normalized_entry["commentary"].replace(old, new)
            merged[number] = normalized_entry
    return merged

# Reviewed source-romanization -> IAST vocabulary.  Longest forms are applied
# first and only at token boundaries.  English wording is otherwise untouched.
ROMAN_REPLACEMENTS = {
    "Sa eva Sarva-Bhootaatmaa Visvaroopo Yato-Avyayah": "sa eva sarva-bhūtātmā viśvarūpo yato 'vyayaḥ",
    "Veveshti Vyaapnoti iti Vishnuh": "veveṣṭi vyāpnoti iti viṣṇuḥ",
    "Eesaavaasyam Idam Sarvam": "īśāvāsyam idaṃ sarvam",
    "AUM Ityekaaksharam Brahma": "oṃ ity ekākṣaraṃ brahma",
    "Omkaara Evedam Sarvam": "oṃkāra evedam sarvam",
    "Sat-Chit-Aananda": "sat-cit-ānanda", "Sat-chit-aananda": "sat-cit-ānanda",
    "Nimitta-Kaarana": "nimitta-kāraṇa", "Sree Maha Vishnu": "Śrī Mahāviṣṇu",
    "Mahaabhaarata": "Mahābhārata", "Mahabharata": "Mahābhārata",
    "Brihadaranyaka": "Bṛhadāraṇyaka", "Mundakopanishad": "Muṇḍakopaniṣad",
    "Kathopanishad": "Kaṭhopaniṣad", "Kenopanishad": "Kenopaniṣad",
    "Isavasyopanishad": "Īśāvāsyopaniṣad", "Taittireeya": "Taittirīya",
    "Chhandogya": "Chāndogya", "Chandogya": "Chāndogya",
    "Harivamsa": "Harivaṃśa", "Upanishads": "Upaniṣads", "Upanishad": "Upaniṣad",
    "Puranas": "Purāṇas", "Purana": "Purāṇa", "Sahasranaama": "Sahasranāma",
    "Vishnu": "Viṣṇu", "Krishna": "Kṛṣṇa", "Narayana": "Nārāyaṇa",
    "Naravana": "Nārāyaṇa", "Lakshmi": "Lakṣmī", "Sankara": "Śaṅkara",
    "Bhagavan": "Bhagavān", "Geeta": "Gītā", "Sree": "Śrī", "Sri": "Śrī",
    "Maayaa": "māyā", "maayaa": "māyā", "Moksha": "mokṣa", "Dharma": "dharma",
    "Dharmas": "dharmas", "Yajnas": "yajñas", "Yajna": "yajña",
    "Vaasanaas": "vāsanās", "vaasanaas": "vāsanās", "Vaasanaa": "vāsanā",
    "Aatmaanam": "ātmānam", "Paramaatman": "paramātman", "Paramaatmaa": "paramātmā",
    "Aatmans": "ātmans", "Aatman": "ātman", "Aatmaa": "ātmā", "Aatma": "ātma",
    "Eesvarah": "Īśvaraḥ", "Eesvara": "Īśvara", "Isvarah": "Īśvaraḥ", "Isvara": "Īśvara",
    "Jeevaatmaa": "jīvātmā", "Jeevas": "jīvas", "Jeeva": "jīva", "jeevah": "jīvaḥ",
    "Praanas": "prāṇas", "Praana": "prāṇa", "praana": "prāṇa",
    "Gunas": "guṇas", "gunas": "guṇas", "Guna": "guṇa",
    "Sastras": "śāstras", "Sastra": "śāstra", "Sakti": "śakti", "saktees": "śaktis",
    "Raakshasas": "rākṣasas", "Raakshasa": "rākṣasa", "Vaamana": "Vāmana",
    "Vaasudeva": "Vāsudeva", "Maadhava": "Mādhava", "Devakee": "Devakī",
    "Saarnga": "Śārṅga", "Saama": "Sāma", "Saaman": "Sāman",
    "Kaama": "kāma", "Kaarana": "kāraṇa", "Aadi": "ādi", "Paraa": "parā",
    "Bhootaanaam": "bhūtānām", "Bhootaani": "bhūtāni", "Bhootaatmaa": "bhūtātmā",
    "Bhoota": "bhūta", "Pootaatmaa": "pūtātmā", "Pootam": "pūtam",
    "Rishis": "ṛṣis", "Rishi": "ṛṣi", "Yogins": "yogins", "Yogees": "yogīs", "Yogee": "yogī",
    "Vidyaas": "vidyās", "Vidyaa": "vidyā", "Vyoohas": "vyūhas", "Vyooha": "vyūha",
    "Viraat-Purusha": "virāṭ-puruṣa", "Viraatpurusha": "virāṭpuruṣa", "Viraat": "virāṭ",
    "Purushah": "puruṣaḥ", "Purusha": "puruṣa", "Kshetrajnah": "kṣetrajñaḥ",
    "Pradhaana": "pradhāna", "Sreemaan": "śrīmān", "Kesa": "keśa",
    "Bhaavah": "bhāvaḥ", "Avyayah": "avyayaḥ", "Aksharah": "akṣaraḥ",
    "Saakshee": "sākṣī", "Vashatkaara": "vaṣaṭkāra", "vashat": "vaṣaṭ",
    "Bhaagavata": "Bhāgavata", "Brahmaaji": "Brahmājī", "Sthaanuh": "sthāṇuḥ",
    "Vrisha": "vṛṣa", "Teertham": "tīrtham", "Sankalpa": "saṅkalpa",
    "Samnyaasa": "saṃnyāsa", "Anga-Nyaasa": "aṅga-nyāsa", "Kara-Nyaasa": "kara-nyāsa",
    "Mahaavaakya": "mahāvākya", "Aham Brahmaasmi": "ahaṃ brahmāsmi",
    "Pooja": "pūjā", "Saadhaka": "sādhaka", "Saadhana": "sādhana",
    "Vedanta": "Vedānta", "Bhagavat": "Bhāgavata", "Vibhooti": "vibhūti", "vibhooti": "vibhūti",
    "Riddhi": "ṛddhi", "Jihvaa": "jihvā", "Sikhanda": "śikhaṇḍa", "Praagvamsah": "prāgvaṃśaḥ",
    "Aadityaanaam": "ādityānām", "Aadityas": "Ādityas", "Aaditya": "Āditya",
    "Bhaavana": "bhāvanā", "Dadaati": "dadāti", "Bhooh": "bhūḥ",
    "Mahaalakshmee": "Mahālakṣmī", "Aakriti": "ākṛti", "Aaroha": "āroha",
    "Saasvatah": "śāśvataḥ", "Bhaanuh": "bhānuḥ", "Aananda": "ānanda",
    "Raakshasic": "rākṣasic", "Bhaaga": "bhāga", "Yoopah": "yūpaḥ",
    "kshaama": "kṣāma", "Dakshinaa": "dakṣiṇā", "Saatvat": "Sātvata",
    "Yaadava": "Yādava", "Vaijavantee": "Vaijayantī", "Saamas": "Sāmans",
    "Raaga": "rāga", "Dvesha": "dveṣa", "Aagamas": "Āgamas",
    "Braahmanas": "brāhmaṇas", "Jayee": "jayī", "Chaanoora": "Cāṇūra",
    "Saamkhya": "Sāṅkhya", "Om-kaara": "oṃkāra", "Pranava": "praṇava",
    "Yogis": "yogīs", "Yaagas": "yāgas", "Yaaga": "yāga", "yaaga": "yāga",
    "Kritam": "kṛtam", "Krita": "kṛta", "Krit": "kṛt", "Kartaa": "kartā",
    "Karoti": "karoti", "Krindati": "kṛntati", "Rajoguna": "rajoguṇa",
    "Sattvaguna": "sattvaguṇa", "Tamoguna": "tamoguṇa", "Desa": "deśa", "Kaala": "kāla",
    "Dhaatus": "dhātus", "Dhaatu": "dhātu", "Preeti": "prīti", "Hiranya": "hiraṇya",
    "Sanaatanah": "sanātanaḥ", "Sanaatana": "sanātana", "sanaatanah": "sanātanaḥ",
    "Prajaah": "prajāḥ", "Prajaa": "prajā", "Paapa": "pāpa", "Lakshana": "lakṣaṇa",
    "Kshetra": "kṣetra", "Ksharah": "kṣaraḥ", "Kshara": "kṣara", "Jnaanam": "jñānam",
    "Jnaana": "jñāna", "Graama": "grāma", "Damshtraa": "daṃṣṭrā", "Vihaayasa": "vihāyasa",
    "Vaachaspati": "vācaspati", "Udaaradheeh": "udāradhīḥ", "Sattaa": "sattā",
    "Maharshi": "maharṣi", "Kaalanemi": "kālanemi", "Dheeh": "dhī", "Dharanee": "dharaṇī",
    "Dhaama": "dhāma", "Bhoktaa": "bhoktā", "Bhartaa": "bhartā", "sthaana": "sthāna",
    "sreeh": "śrīḥ", "sadaa": "sadā", "saagarah": "sāgaraḥ", "paramaatmaa": "paramātmā",
    "paada": "pāda", "mayaa": "māyayā", "gadaa": "gadā", "Veerya": "vīrya",
    "Srashtaa": "sraṣṭā", "Sishtah": "śiṣṭaḥ", "Sishta": "śiṣṭa", "Samaatmaa": "samātmā",
    "Saatvata": "sātvata", "Raajaa": "rājā", "Mahee": "mahī", "Kshema": "kṣema",
    "Chakree": "cakrī", "Bhagavaan": "bhagavān", "Aksharam": "akṣaram",
    "Veveshti": "veveṣṭi", "Vyaapnoti": "vyāpnoti", "Visvaroopo": "viśvarūpo",
    "Vishnuh": "Viṣṇuḥ", "Vishnusahasranaama": "Viṣṇusahasranāma", "Vis": "√viś",
    "Omkaara": "oṃkāra", "Poota": "pūta", "Samsaara": "saṃsāra", "Samsaar": "saṃsāra",
    "Saattvic": "sāttvika", "Pramaana": "pramāṇa", "Vaasu": "Vāsu",
    "OM Ityekaaksharam Brahma": "oṃ ity ekākṣaraṃ brahma", "Yato-avyayaḥ": "yato 'vyayaḥ",
    "Mandukya": "Māṇḍūkya", "yajna": "yajña", "Yajno": "yajño",
    "Paanchajanya": "Pāñcajanya", "Paancha-janya": "pāñca-janya", "Ahamkaara": "ahaṅkāra",
    "Sudarsana": "Sudarśana", "Kaumodakee": "Kaumodakī", "Paarthasaarathi": "Pārthasārathi",
    "Samsaara-Vriksha": "saṃsāra-vṛkṣa", "Samaadhi": "samādhi", "Pramaada": "pramāda",
    "Bheema": "Bhīma", "Prahlaada": "Prahlāda", "Hiranyakasipu": "Hiraṇyakaśipu",
    "Hiranyaaksha": "Hiraṇyākṣa", "Hiranyaksha": "Hiraṇyākṣa",
    "Sa eva": "sa eva", "Sarva-bhūtātmā": "sarva-bhūtātmā", "Vastu": "vastu", "Isa": "Īśa",
}

FOREIGN_SCRIPT = re.compile(r"[\u0980-\u09ff\u0b80-\u0bffıŊķ]")


def replace_token(text: str, source: str, target: str) -> str:
    return re.sub(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", target, text)


def normalize_prose(text: str, *, concise: bool = False) -> str:
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"\b(can also mean|it can also mean|meaning)\.\s+(?=[A-Z])", r"\1: ", text, flags=re.I)
    text = re.sub(r"(?<=[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ])-(?=[A-Z])", " — ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    if concise:
        text = re.sub(r"[.;:]\s*$", "", text.strip())
    return text


SIMPLE_STOPWORDS = {
    "a", "all", "an", "and", "as", "called", "for", "from", "he", "him",
    "himself", "his", "in", "is", "it", "meaning", "means", "of", "one",
    "or", "that", "the", "this", "to", "which", "who", "with",
}


def source_key(text: str) -> str:
    """Comparison key for proving that a concise line replays source words."""
    import unicodedata

    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def simple_tokens(text: str) -> set[str]:
    import unicodedata

    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return {token for token in re.findall(r"[a-z]+", ascii_text) if token not in SIMPLE_STOPWORDS}


def simple_excerpt_candidates(commentary: str) -> list[str]:
    candidates: list[str] = []
    for paragraph in commentary.split("\n\n"):
        sentences = re.split(
            r'(?<=[.!?।॥])(?:["”’)]*)\s+(?=["“‘A-ZĀĪŪṚŚṢṄÑ])',
            paragraph,
        )
        for sentence in sentences:
            sentence = sentence.strip(" \n\t-*†‡")
            pieces = [sentence]
            pieces.extend(re.split(r';\s+|:\s+(?=[A-Z“"\'])', sentence))
            pieces.extend(match.group(1) for match in re.finditer(r'[“"]([^”"]{15,220})[”"]', sentence))
            for piece in pieces:
                piece = piece.strip(" \n\t-*†‡;:")
                if 18 <= len(piece) <= 220 and piece not in candidates:
                    candidates.append(piece)
    return candidates


def clean_simple_text(value: str) -> str:
    value = re.sub(r"\s*\([^)]*[\u0900-\u0dff][^)]*\)", "", value)
    value = re.sub(r"[\u0900-\u0dff]+", "", value)
    value = normalize_prose(value, concise=True).strip()
    quote_pairs = {'"': '"', "'": "'", "“": "”", "‘": "’"}
    if len(value) >= 2 and value[0] in quote_pairs and value[-1] == quote_pairs[value[0]]:
        value = value[1:-1].strip()
    if value and value[0].islower():
        value = value[0].upper() + value[1:]
    return value


def select_simple_excerpt(commentary: str, guide: str, number: int) -> str:
    override = SIMPLE_EXCERPT_OVERRIDES.get(number)
    if override:
        return clean_simple_text(override)
    if source_key(guide) and source_key(guide) in source_key(commentary):
        return clean_simple_text(guide)

    target = simple_tokens(guide)
    ranked: list[tuple[float, str]] = []
    for candidate in simple_excerpt_candidates(commentary):
        candidate_tokens = simple_tokens(candidate)
        score = len(target & candidate_tokens) * 8
        score -= max(0, len(candidate_tokens) - len(target)) * 0.15
        if re.match(r"^(?:One|He|That|The (?:term|Lord|Self|Supreme)|It can|Lord|Śrī|Nārāyaṇa)", candidate):
            score += 3
        if re.search(r"\b(?:is|means|called|indicates|signifies|denotes)\b", candidate, re.I):
            score += 2
        if re.search(r"\b(?:Gītā|Upaniṣad|Purāṇa|Mahābhārata|says|declares|read|earlier|previous)\b", candidate, re.I):
            score -= 4
        if re.search(r"[\u0900-\u097f]", candidate):
            score -= 2
        if len(candidate_tokens) < 3:
            score -= 8
        ranked.append((score, candidate))
    if not ranked:
        raise ValueError(f"name {number} has no source-excerpt candidate for its Simple meaning")
    return clean_simple_text(max(ranked)[1])


def simple_source_record(commentary: str, excerpt: str) -> dict:
    """Describe where the excerpt occurs without pretending it is a definition."""
    offset = source_key(commentary).find(source_key(excerpt))
    if offset < 0:
        raise ValueError("simple excerpt cannot be located in its commentary")
    return {
        "field": "commentary",
        "scope": "opening" if offset <= 300 else "later-explicit-explanation",
        "normalized_character_offset": offset,
    }


def normalize_packet_commentary(text: str) -> str:
    """Apply the public Sanskrit romanization standard to scan-checked prose."""
    replacements = sorted(ROMAN_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True)
    for old, new in replacements:
        text = replace_token(text, old, new)
    return normalize_prose(text)


def normalize(data: dict, analysis: dict) -> dict:
    rows = data["names"]
    analyses = analysis["names"]
    apparatus_overrides = load_apparatus_packets()
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        raise ValueError("transcription is not exactly names 1-1000")

    data["work"]["transcription_standard"] = "scan-backed English; canonical heading Devanagari and IAST; reviewed Sanskrit romanization"
    data["work"]["secondary_ocr_witness"] = {
        "filename": "chinmayananda_vishnu_sahasranama_secondary_ocr_2026-08-27.txt",
        "sha256": "8e87779ac1ac0555c9b12b62e895c2338bc8e6c5cf2e0cc82b9f9d69557f36a4",
        "status": "quarantined-comparison-only",
        "note": "Same 2011 edition; incomplete numbering, malformed scripts, and at least one scan-unsupported insertion. Never authoritative without page confirmation.",
    }
    data["work"]["apparatus_corrections"] = {
        "status": "scan-checked",
        "packets": [str(path.relative_to(ROOT)) for path in APPARATUS_PACKET_PATHS],
        "corrected_entries": len(apparatus_overrides),
    }

    replacements = sorted(ROMAN_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True)
    for row, parsed in zip(rows, analyses):
        if "source_heading_roman" not in row:
            row["source_heading_roman"] = row.pop("heading_roman")
        if "source_heading_devanagari_ocr" not in row:
            row["source_heading_devanagari_ocr"] = row["heading_devanagari"]
        row["heading_iast"] = parsed["citation_iast"]
        row["heading_devanagari"] = parsed["citation_devanagari"]

        for field in ("short_meaning", "commentary"):
            value = row[field]
            for old, new in ENTRY_REPAIRS.get(row["number"], {}).items():
                value = value.replace(old, new)
            # The entry's own printed roman heading is the strongest lexical
            # normalization available for its name.
            value = replace_token(value, row["source_heading_roman"], row["heading_iast"])
            for old, new in replacements:
                value = replace_token(value, old, new)
            row[field] = normalize_prose(value, concise=field == "short_meaning")

        if row["number"] in COMMENTARY_STRUCTURE_OVERRIDES:
            row["commentary"] = COMMENTARY_STRUCTURE_OVERRIDES[row["number"]]
        if row["number"] in apparatus_overrides:
            apparatus_entry = apparatus_overrides[row["number"]]
            row["commentary"] = apparatus_entry["commentary"]
            if apparatus_entry.get("scan_pages"):
                row["scan_pages"] = apparatus_entry["scan_pages"]
            row["apparatus_status"] = "scan-checked"

        # Apparatus packets replay the scan before entry-level Sanskrit
        # correction. Reapply the narrow, reviewed fixes after packet replay so
        # a corrected quotation is not replaced by its older OCR spelling.
        for field in ("short_meaning", "commentary"):
            for old, new in ENTRY_REPAIRS.get(row["number"], {}).items():
                row[field] = row[field].replace(old, new)

        simple_guide = SIMPLE_MEANING_OVERRIDES.get(row["number"], row["short_meaning"])
        if row["number"] in FULL_NO_STANDALONE_MEANING:
            basis_excerpt = None
            basis_source = {
                "field": "commentary",
                "scope": "entry-reviewed",
                "note": FULL_NO_STANDALONE_MEANING[row["number"]],
            }
        else:
            basis_excerpt = select_simple_excerpt(row["commentary"], simple_guide, row["number"])
            basis_source = simple_source_record(row["commentary"], basis_excerpt)
        row["simple_basis_excerpt"] = basis_excerpt
        row["simple_basis_source"] = basis_source
        row["simple_meaning"] = clean_simple_text(simple_guide if row["number"] in SIMPLE_MEANING_OVERRIDES else basis_excerpt)
        row["simple_meaning_status"] = "site-generated-summary-derived-from-chinmayananda"
        row["simple_meaning_source"] = {
            "basis": "chinmayananda-full-commentary",
            "editorial_operation": (
                "site-authored concise summary" if row["number"] in SIMPLE_MEANING_OVERRIDES
                else "site-selected concise source wording"
            ),
            "attribution": "site-generated Simplified layer; not credited as Chinmayananda's translation or quotation",
        }

        if row["number"] in SCAN_PAGE_OVERRIDES:
            old_pages = row["scan_pages"]
            target_pages = SCAN_PAGE_OVERRIDES[row["number"]]
            redundant = f"Scan locus corrected from {target_pages} to {target_pages} by complete-text replay against the PDF page OCR."
            row["ocr_notes"] = [note for note in row.setdefault("ocr_notes", []) if note != redundant]
            row["scan_pages"] = target_pages
            if old_pages != target_pages:
                note = f"Scan locus corrected from {old_pages} to {target_pages} by complete-text replay against the PDF page OCR."
                if note not in row["ocr_notes"]:
                    row["ocr_notes"].append(note)
    return data


def validate(data: dict, analysis: dict) -> dict:
    errors = []
    rows = data.get("names", [])
    analyses = analysis["names"]
    apparatus_overrides = load_apparatus_packets()
    expected_overrides = {
        row.get("number")
        for row in rows
        if SIMPLE_META.search(row.get("short_meaning", "")) or len(row.get("short_meaning", "")) > 160
    }
    missing_overrides = sorted(expected_overrides - set(SIMPLE_MEANING_OVERRIDES))
    if missing_overrides:
        errors.append(f"simple meaning override population is incomplete; missing={missing_overrides}")
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        errors.append("population is not exactly 1-1000")
    for row, parsed in zip(rows, analyses):
        n = row.get("number")
        if row.get("heading_iast") != parsed["citation_iast"]:
            errors.append(f"name {n} IAST heading differs from canonical analysis")
        if row.get("heading_devanagari") != parsed["citation_devanagari"]:
            errors.append(f"name {n} Devanagari heading differs from canonical analysis")
        for field in ("short_meaning", "commentary"):
            public_text = row.get(field, "")
            if FOREIGN_SCRIPT.search(public_text):
                errors.append(f"name {n} {field} retains a foreign-script OCR substitution")
            for source in ROMAN_REPLACEMENTS:
                if re.search(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", public_text):
                    errors.append(f"name {n} {field} retains unnormalized Sanskrit romanization: {source}")
            if "we are stuck in dwaita" in public_text.lower():
                errors.append(f"name {n} imports scan-unsupported text from the secondary OCR")
            if re.search(r"[ \t]+[,.;:!?]|\.{3,}|\b(?:can also mean|it can also mean|meaning)\.\s+(?=[A-Z])", public_text, re.I):
                errors.append(f"name {n} {field} retains mechanical punctuation/OCR spacing")
            if field == "short_meaning" and re.search(r"[.;:]\s*$", public_text):
                errors.append(f"name {n} concise definition retains terminal separator punctuation")
            if field == "commentary" and APPARATUS_RESIDUE.search(public_text):
                errors.append(f"name {n} commentary retains raw apparatus/page residue")
        simple = row.get("simple_meaning")
        if not isinstance(simple, str) or not 3 <= len(simple) <= 260 or "\n" in simple:
            errors.append(f"name {n} simplified summary has invalid length/shape")
            simple = simple or ""
        if re.search(r"[*†‡\u0900-\u0dff]", simple):
            errors.append(f"name {n} simplified summary contains a footnote marker or source script")
        expected_summary = clean_simple_text(
            SIMPLE_MEANING_OVERRIDES[n] if n in SIMPLE_MEANING_OVERRIDES else row.get("simple_basis_excerpt", "")
        )
        if simple != expected_summary:
            errors.append(f"name {n} simplified summary differs from its reviewed editorial layer")
        basis_excerpt = row.get("simple_basis_excerpt")
        if n in FULL_NO_STANDALONE_MEANING:
            if basis_excerpt is not None:
                errors.append(f"name {n} falsely records a standalone Chinmayananda excerpt")
        elif not basis_excerpt or source_key(basis_excerpt) not in source_key(row.get("commentary", "")):
            errors.append(f"name {n} lacks replayable source evidence for its Simplified review")
        expected_status = "site-generated-summary-derived-from-chinmayananda"
        if row.get("simple_meaning_status") != expected_status:
            errors.append(f"name {n} simple meaning status is not {expected_status}")
        source = row.get("simple_meaning_source")
        if not isinstance(source, dict) or source.get("basis") != "chinmayananda-full-commentary":
            errors.append(f"name {n} simplified summary lacks its commentary basis")
        if n in COMMENTARY_STRUCTURE_OVERRIDES and row.get("commentary") != COMMENTARY_STRUCTURE_OVERRIDES[n]:
            errors.append(f"name {n} commentary does not replay its scan-checked apparatus reconstruction")
        if n in apparatus_overrides:
            if row.get("commentary") != apparatus_overrides[n]["commentary"]:
                errors.append(f"name {n} commentary does not replay its range apparatus packet")
            if row.get("apparatus_status") != "scan-checked":
                errors.append(f"name {n} lacks scan-checked apparatus status")
        if n in SCAN_PAGE_OVERRIDES and row.get("scan_pages") != SCAN_PAGE_OVERRIDES[n]:
            errors.append(f"name {n} retains the wrong scan locus")
    if errors:
        raise ValueError("\n".join(errors[:100]))
    return {
        "names": len(rows),
        "canonical_iast_headings": sum(row.get("heading_iast") == parsed["citation_iast"] for row, parsed in zip(rows, analyses)),
        "canonical_devanagari_headings": sum(row.get("heading_devanagari") == parsed["citation_devanagari"] for row, parsed in zip(rows, analyses)),
        "scan_locus_corrections": len(SCAN_PAGE_OVERRIDES),
        "foreign_script_substitutions": 0,
        "simplified_site_summaries": len(rows),
        "simple_basis_excerpts": len(rows) - len(FULL_NO_STANDALONE_MEANING),
        "full_entries_without_standalone_meaning": len(FULL_NO_STANDALONE_MEANING),
        "reviewed_simple_overrides": len(SIMPLE_MEANING_OVERRIDES),
        "scan_checked_commentary_structures": len(COMMENTARY_STRUCTURE_OVERRIDES),
        "apparatus_packet_entries": len(apparatus_overrides),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(TRANSCRIPTION.read_text(encoding="utf-8"))
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    if args.write:
        data = normalize(data, analysis)
        TRANSCRIPTION.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = validate(data, analysis)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
