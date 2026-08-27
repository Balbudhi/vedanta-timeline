#!/usr/bin/env python3
"""Extract Chinmayananda's name-by-name Vishnu Sahasranama commentary.

The cleaned Markdown is the transcription scaffold.  The page-preserving OCR
is used only to attach scan-page loci.  A short set of scan-checked layout
repairs handles numbers that OCR moved away from their headings.  This script
does not normalize or replace the Sanskrit witness; those fields are retained
only as an aid until the reader joins an independently verified Sanskrit text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path


DEFAULT_SCAN = Path.home() / "Downloads/Vishnu Sahasranama.pdf"
DEFAULT_MARKDOWN = Path.home() / "Downloads/Vishnu_Sahasranama_cleaned_for_google_docs.md"
DEFAULT_PAGE_OCR = Path.home() / "Downloads/Vishnu_Sahasranama_ocr_eng_san.txt"
DEFAULT_OUTPUT = Path("gita/vishnu-sahasranama/chinmayananda.json")

# These exact layout repairs were inspected in the image witness.  OCR either
# omitted a number or placed it after the heading/commentary.  Each
# substitution is deliberately narrow so a changed input fails rather than
# being guessed at.
UNICODE_REPAIRS = (
    ("Yogah ( योग: )—", "(18) Yogah ( योग: )—"),
    ("Yoga-vidaam netaa (योगविदां नेता) -", "(19) Yoga-vidaam netaa (योगविदां नेता) -"),
    ("(धन्वी)—Lord Vishnu's Divine Bow is", "(76) Dhanvee (धन्वी)—Lord Vishnu's Divine Bow is"),
    ("Samvatsarah (संवत्सर:)—One who is of the nature of", "(91) Samvatsarah (संवत्सर:)—One who is of the nature of"),
    ("Siddhih (सिद्धि:)—He who is available for recognition", "(98) Siddhih (सिद्धि:)—He who is available for recognition"),
    ("Vijayah (विजय:)—\"The Victorious\".", "(147) Vijayah (विजय:)—\"The Victorious\"."),
    ("Vaamanah (वामन:)—Of the ten great incarnations", "(152) Vaamanah (वामन:)—Of the ten great incarnations"),
    ("Vaidyah (वैद्य:)—The One Supreme Doctor", "(164) Vaidyah (वैद्य:)—The One Supreme Doctor"),
    ("worship.\"** (56) Saasvatah (", "worship.\"**\n\n(56) Saasvatah ("),
    ("(56) Saasvatah (\n\nthe same is the Permanent", "(56) Saasvatah (शाश्वतः)—That which remains at all times the same is the Permanent"),
    ("Sishtakrit (গিড্রেন্)—One who governs; One who 250. is", "250. Sishtakrit (গিড্রেন্)—One who governs; One who is"),
    ("(विशिष्ट:) -- One who is the noblest and\n\nVisishtah 309.\n\nthe most sacred.",
     "309. Visishtah (विशिष्ट:)—One who is the noblest and the most sacred."),
    ("** 388. Dhruvah ( ঘ্ৰ:)—", "**\n\n388. Dhruvah ( घ্ৰ:)—"),
    ("devotees \" 421. Ugrah (ব্য:)—", "devotees \"\n\n421. Ugrah (ব্য:)—"),
    ("the realm of the Self.* 545. Guptah (গুল:)—", "the realm of the Self.*\n\n545. Guptah (গুল:)—"),
    ("678: Mahaa-havih", "678. Mahaa-havih"),
    ("\"The 732. Padam Anuttamam Unequalled State of Perfection: The Supreme State of Truth.\"",
     "732. Padam Anuttamam (पदमनत्तमम)—\"The Unequalled State of Perfection: The Supreme State of Truth.\""),
    ("· 747. Amaanee", "747. Amaanee"),
    ("Kundalee (কুণ্ডলী)—“One Who wears the famous 907. ear-ring", "907. Kundalee (কুণ্ডলী)—“One Who wears the famous ear-ring"),
    ("(अविज्ञाता)—The Non-knower. Here we\n\n482.\n\nAvijnaataa must carefully understand",
     "482. Avijnaataa (अविज्ञाता)—The Non-knower. Here we must carefully understand"),
    ("( अ न्नं )—“One Who has Himself become\n\n983. Annam the 'food'",
     "983. Annam ( अ न्नं )—“One Who has Himself become the 'food'"),
)

SCAN_CHECKED_DEVANAGARI = {
    5: "भूतकृत्",
    18: "योगः",
    19: "योगविदां नेता",
    34: "प्रभवः",
    35: "प्रभुः",
    38: "शम्भुः",
    43: "धाता",
    56: "शाश्वतः",
    60: "प्रभूतः",
    61: "त्रिककुब्धाम",
    65: "प्राणदः",
    66: "प्राणः",
    68: "श्रेष्ठः",
    76: "धन्वी",
    82: "कृतज्ञः",
    91: "संवत्सरः",
    98: "सिद्धिः",
    101: "वृषाकपिः",
    114: "रुद्रः",
    116: "बभ्रुः",
    118: "शुचिश्रवाः",
    136: "कृताकृतः",
    147: "विजयः",
    152: "वामनः",
    155: "शुचिः",
    156: "ऊर्जितः",
    164: "वैद्यः",
    207: "विश्रुतात्मा",
    208: "सुरारिहा",
    249: "विशिष्टः",
    250: "शिष्टकृत्",
    309: "विशिष्टः",
    351: "ऋद्धः",
    356: "शरभः",
    388: "ध्रुवः",
    409: "प्रणवः",
    418: "कालः",
    421: "उग्रः",
    435: "अनिर्विण्णः",
    485: "कृतलक्षणः",
    536: "महाशृङ्गः",
    545: "गुप्तः",
    550: "कृष्णः",
    555: "वृक्षः",
    579: "भिषक्",
    586: "शुभाङ्गः",
    595: "वृषप्रियः",
    678: "महाहविः",
    728: "कः",
    729: "किम्",
    732: "पदमनुत्तमम्",
    744: "घृताशीः",
    747: "अमानी",
    751: "त्रिलोकधृक्",
    767: "चतुर्व्यूहः",
    780: "दुरावासः",
    782: "शुभाङ्गः",
    797: "शृङ्गी",
    820: "शत्रुजित्",
    837: "कृशः",
    838: "स्थूलः",
    845: "प्राग्वंशः",
    907: "कुण्डली",
    914: "शर्वरीकरः",
    917: "दक्षः",
    943: "लक्ष्मीः",
    993: "शङ्खभृत्",
    995: "चक्री",
}

SCAN_CHECKED_NUMBERS = set(SCAN_CHECKED_DEVANAGARI)

SCAN_CHECKED_ROMAN = {
    435: "Anirvinnah",
    767: "Chatur-vyoohah",
    780: "Dur-aavaasah",
}

FORBIDDEN_ARTIFACTS = (
    "newpage",
    "### ",
    "Vishnii Sahasranaama",
    "Vishnij Sahasranaama",
    "1190/011",
    "Kenseseris",
    "Glorifs Of The Lord",
    "Glories Of The Lord",
    "GLORIES OF THE LORD",
    "VISHNU SAHASRANAAMA",
    "\ufffd",
    "\f",
)

# These are genuine compounds whose printed hyphens were mistaken for
# end-of-line word-wrap hyphens.  Every pair below was checked against the
# image witness.  Keeping them record-scoped prevents a broad normalization
# from changing Chinmayananda's punctuation elsewhere.
COMMENTARY_REPAIRS: dict[int, tuple[tuple[str, str], ...]] = {
    1: (
        ("SarvaBhootaatmaa", "Sarva-Bhootaatmaa"),
        ("The Sanskrit term Visyam", "The Sanskrit term Visvam"),
        ("OM Itvekaaksharam Brahma", "OM Ityekaaksharam Brahma"),
    ),
    5: (("BhootaKrit", "Bhoota-Krit"),),
    12: (("ununderstanding", "un-understanding"),),
    13: (("Sat-chitaananda", "Sat-chit-aananda"),),
    16: (("Knower-of-thefield", "Knower-of-the-field"),),
    47: (("the \"senseorgans\"", "the \"sense-organs\""),),
    57: (("ExistenceBliss", "Existence-Bliss"),),
    62: (("selfcancellation", "self-cancellation"),),
    72: (("Madhutechnique", "Madhu-technique"),),
    78: (("whiteeagle", "white-eagle"),),
    88: (("SarvaPrapancha-Kaaranabhootah", "Sarva-Prapancha-Kaaranabhootah"),),
    111: (("AllPervading Reality", "All-Pervading Reality"),),
    143: (("Lordof-Lakshmi", "Lord-of-Lakshmi"),),
    145: (("Wombof-all-objects", "Womb-of-all-objects"),),
    168: (("MarchApril", "March-April"),),
    192: (("whitewinged", "white-winged"),),
    239: (("deepsleep", "deep-sleep"),),
    274: (("knower-ofthe-field", "knower-of-the-field"),),
    283: (("foodvalue", "food-value"),),
    316: (("in-asmuch", "in-as-much"),),
    336: (("mind-intellectequipment", "mind-intellect-equipment"),),
    361: (("worldof-matter", "world-of-matter"),),
    360: (("throughdualistic", "through dualistic"),),
    371: (("Allpervading", "All-pervading"),),
    392: (("Everfull", "Ever-full"),),
    400: (("Allpervading", "All-pervading"),),
    427: (("as oneword", "as one-word"),),
    471: (("LoveIncarnate", "Love-Incarnate"),),
    474: (("in the universeall objects", "in the universe—all objects"),),
    513: (("limitedego", "limited-ego"),),
    519: (("Vishnupurana", "Vishnu Purana"),),
    548: (("efficientcause", "efficient-cause"),),
    550: (("Alllife", "All-Life"),),
    553: (("SooryaNarayana", "Soorya-Narayana"),),
    554: (("Whereever", "Where-ever"),),
    559: (("Totalmind", "Total-mind"),),
    564: (("great-grandgiver", "great-grand-giver"),),
    568: (("axeweapon", "axe-weapon"),),
    585: (("nivartanteTat-dhaama", "nivartante Tat-dhaama"),),
    608: (("treasurehouse", "treasure-house"),),
    632: (("egosense", "ego-sense"),),
    646: (("waker-dreamersleeper", "waker-dreamer-sleeper"),),
    663: (("Creativepower", "Creative-power"),),
    669: (("the wakingthe \"dreamer\"", "the waking—the \"dreamer\""),),
    672: (("MahaPurushas", "Maha-Purushas"),),
    677: (
        ("the JapaYajna", "the Japa-Yajna"),
        ("greatest Yajnatherefore", "greatest Yajna—therefore"),
    ),
    715: (("singlepointed", "single-pointed"),),
    722: (("the senseorgans", "the sense-organs"),),
    737: (
        ("MundakaUpanishad", "Mundaka Upanishad"),
        ("Goldenhue", "Golden-hue"),
    ),
    738: (("pure-goldenform", "pure-golden-form"),),
    765: (("Deepsleeper", "Deep-sleeper"),),
    773: (("wheel-of-lifeand-death", "wheel-of-life-and-death"),),
    777: (("NarayanaConsciousness", "Narayana-Consciousness"),),
    782: (("Peace-AuspiciousnessBeauty", "Peace-Auspiciousness-Beauty"),),
    791: (("fills the observerand this", "fills the observer—and this"),),
    828: (("Seven tonguesof-flame", "Seven tongues-of-flame"),),
    849: (("thoughtflow", "thought-flow"),),
    862: (("the great weaponand fixed", "the great weapon—and fixed"),),
    888: (("bodymind-intellect", "body-mind-intellect"),),
    895: (("innerequipments", "inner-equipments"),),
    900: (("Totalmind", "Total-mind"),),
    901: (
        ("BlissExperience", "Bliss-Experience"),
        ("Giver-ofAuspiciousness", "Giver-of-Auspiciousness"),
    ),
    907: (("thousandtongued", "thousand-tongued"),),
    914: (("men of realisa tion", "men of realisation"),),
    918: (("everready", "ever-ready"),),
    923: (("bodymind-intellect", "body-mind-intellect"),),
    925: (("sensehunting", "sense-hunting"),),
    932: (
        ("dream-plane-ofConsciousness", "dream-plane-of-Consciousness"),
        ("objects-emotions-andthoughts", "objects-emotions-and-thoughts"),
    ),
    933: (("Actionpower", "Action-power"),),
    953: (("Eternal-DivineNature", "Eternal-Divine-Nature"),),
    962: (("lifegiving", "life-giving"),),
    966: (("Ever-theSame", "Ever-the-Same"),),
    977: (("Goddedication", "God-dedication"),),
    992: (
        ("vausanaas", "vaasanaas"),
        ("vaasanaus", "vaasanaas"),
    ),
    994: (("KnowledgeSpiritual", "Knowledge-Spiritual"),),
}

# Page-bottom footnotes were interleaved by OCR into these entries.  The text
# below is transcribed in printed reading order from the named scan pages; it
# excludes footnotes belonging to an earlier name on the same page.
SCAN_CHECKED_COMMENTARY = {
    214: (
        'The condition of "the eyelids closed" is called Nimishah; the unwinking is called Animishah. '
        "When the eyes are open, the mind is extrovert; the condition of mental introvertedness is expressed "
        "in an unconscious closing of the eyes. When a man is deeply thinking, remembering, contemplating, we "
        "find him naturally closing his eyes.\n\n"
        "In a state of intense contemplation, when the intellect is turned away from the objects-of-experiences, "
        'the bosom experiences the One Divine "Subject" both within and without. The Lord is described here as '
        '"with eyes closed", only to indicate that He is ever rooted in Himself; from Him viewed, there exists '
        "nothing other than Himself to constitute the world-of-objects."
    ),
    251: (
        "One who is Pure. The immaculate Reality which is never contaminated by the Maayaa and its by-products "
        "is Maha Vishnu. When dirt (Mala) exists upon anything, it becomes unclean. In the Absolute Oneness "
        "there can be nothing other than itself and therefore the Fourth-plane-of-Consciousness (Tureeyam) is "
        "indicated in our Scriptures as the Transcendental Ever-Pure Self, Sri Hari."
    ),
    338: (
        '"One who saves is called Taarah.*** One who saves from the fear of re-birth and also One who is a '
        "constant protector of the devotees and, therefore, the devotees themselves call Him as the Saviour "
        "(Taarah).\n\n"
        "These three terms indicate how Vishnu is the Absolute Protector of His devotees. He saves us from the "
        "afflictions (Asoka) of the body and so Subjective-sorrows (Adhyaatma). He enables us to cross the ocean "
        "of Samsaara (Taaranah) and, therefore, He saves us from all Cosmic pains (Adhibhootah).\n\n"
        "He saves us from the elements (Taarah), and so, He is the Saviour from all sorrows of birth and death; "
        "this indicates all trans-Cosmic tragedies (Aadhidaivika), meaning that Narayana can save us from all "
        "sorrows contributed by the hand-of-God.\n\n"
        '*** "तारयति इति तारः।"'
    ),
    585: (
        "The Supreme Goal is Narayana. After reaching Him there is no return.*** In short. the term indicates "
        "that Narayana is the way to the Supreme Liberation (Moksha).\n\n"
        '*** "यद्गत्वा न निवर्तन्ते तद्धाम परमं मम।" (Yadgatvaa na nivartante Tat-dhaama paramam mama.) '
        '"To which having gone they return not; that is My Supreme Abode." —Geeta XV-6.'
    ),
    934: (
        '“One Who has conquered anger" (manyuh). It cannot be repeated too often, thus the significance is again '
        'given in this term, that anger is one of the most overpowering enemies within us—"One Who has conquered '
        'anger" is One Who is established in His own Purity.\n\n'
        "Earlier, the technique of anger was explained that when a desire is unfulfilled, anger rises in a man's "
        "heart towards the obstacle between him and his desire. The Self is All-full (Paripoorna); It cannot feel "
        "any need, want or desire. The Self, then, Sree Narayana, is ever without the low and ruinous passion "
        "called 'anger.'"
    ),
    966: (
        '“One Who knows no change or modifications in Himself." Every finite object in the world undergoes '
        "constant 'change' and each of them is extremely painful. They are birth, growth, decay, disease and "
        "death. One who has none of these is the Infinite and the Eternal, the Changeless Self, Sree Narayana, "
        "Ever-the-Same Supreme. Geeta thunders the nature of the Self to be “ever-birthless and never-dying,” "
        "and once It has existed, Self never becomes non-existent.*\n\n"
        '* “न जायते म्रियते वा कदाचित् नायं भूत्वा भविता वा न भूयः। अजो नित्यः शाश्वतोऽयं पुराणो न हन्यते '
        'हन्यमाने शरीरे।” (Na jaayate mriyate vaa kadaachit naayam bhootvaa bhavitaa vaa na bhooyah; ajo nityah '
        'saasvato-ayam puraano na hanyate hanyamaane sareere.) “He is not born, nor does He ever die; after having '
        'been He again ceases not to be; unborn, eternal, changeless and ancient he is not killed when the body is '
        'killed.” —Geeta II-20.'
    ),
}

# Opening definitions that fail one or more short-line gates are transcribed
# from the recorded scan page.  They retain Chinmayananda's own wording while
# omitting source-script parentheticals, footnote calls, and displaced footnote
# text.  All other records use their unchanged first clean sentence.
SHORT_MEANING_OVERRIDES = {
    14: "One who dwells in the Fort-city.",
    23: "He who has beautiful and graceful locks of hair.",
    36: "One who has the ability to do anything without the help of other beings or things is called Eesvarah.",
    56: "That which remains at all times the same is the Permanent.",
    59: 'The root Tarda means "destruction" and with the prefix Pra the root (Pra-tarda) means "supreme destruction".',
    60: "The term means 'born full' or 'ever-full'.",
    66: "That which sustains is Praana, and that which has got Praana functioning in it is called a Praanee.",
    94: 'This term, "All-seeing", is very appropriate.',
    114: "One who makes all people weep.",
    117: "One who is the Total Cause from which alone the entire world of experiences has emerged out.",
    118: "One who has beautiful and efficient ears.",
    126: "The term Ardayati is a verb meaning both 'giving sorrow' or 'giving joy'.",
    150: "One who comes to live again and again in various equipments of living organisms is Punarvasuh.",
    158: "One who holds the entire world of beings-and-things together in an indissoluble embrace unto Himself.",
    177: "One whose form is indefinable, indescribable, inexplicable.",
    181: "One who wears or wields the Great Bow called Saarnga.",
    216: "A garland is called Srak and, therefore, the term means One who is constantly wearing a garland of undecaying flowers.",
    227: "The One Infinite Consciousness expresses everywhere, in all forms, at all times.",
    229: "The pure Self, which has retreated totally from all Its identifications with matter.",
    243: "One, who functions strictly according to the righteous code of living is a Saadhuh.",
    246: "The Guide.",
    310: "To all spiritually minded good people and therefore sincere seekers, the Lord is the greatest beloved.",
    311: 'One who wears Sikhanda, meaning "the peacock feather".',
    312: 'The term Nahanam means bondage; therefore, the term stands for "One who is familiar with bondages."',
    314: "One who destroys anger in all sincere seekers.",
    315: "One who generates in a sincere and serious seeker anger against the lower tendencies when they manifest.",
    317: "One who is the Substratum and support for the Earth.",
    318: "One who has not got any modifications—such as birth, growth, decay, disease, death etc.",
    325: "One who has no Pramaada, meaning, One who never commits a mistake in judgement.",
    332: "One who is at once both Vaasu and Deva.",
    338: "One who saves is called Taarah.",
    340: "Soorasena is the father of Vasudeva, and we have already found that Vasudeva's son is Vaasudeva.",
    354: "One who has the eagle (Garuda) as his insignia on his flag.",
    361: "The consort of Lakshmi.",
    375: "One who revels is Deva.",
    394: "That which revels in every form or that in which all Yogins in their meditation revel.",
    407: "One who in the form of 'Praana' exists in the body, propels all sense-organs to act in their appointed fields.",
    415: "One who is not available for the powers of the sense organs to perceive.",
    435: "One who has no nirveda.",
    517: 'The direct meaning of the word is "ocean".',
    530: "One who has taken the three steps.",
    535: "The Lord of the three steps—the three steps are waking, dream and deep-sleep.",
    558: "One who has all the Six Great Glories—Wealth, Power, Dharma, Fame, Character, Knowledge and Dispassion—is called Bhagavaan.",
    555: "The Samsaara-Vriksha—the Tree of Life.",
    593: "The root Gup has two meanings: to protect; to veil.",
    611: "One Who confers Sree upon His devotees.",
    615: 'Brilliantly "Beautiful-Eyed" is Vishnu.',
    629: 'One Who adorns the world: physically with the infinite beauties of His Creation.',
    630: 'One Who is the Pure “BE”-ness or Existence.',
    639: "One Who is never challenged by any enemies and Who has no enemies to even threaten Him.",
    655: "The author of the Scriptures (Aagamas).",
    679: "One Who is the object of all praise.",
    701: "The Lord is the One without a second.",
    707: "One Who is attended by the righteous Yaamunas—meaning Gopas who live on the Yamuna banks.",
    709: "One Who envelops the world with His Maayaa-powers of veiling and agitations.",
    725: "The One.",
    734: "One Who is the Lord of the World.",
    767: "One Who expresses Himself as the dynamic centre in the four Vyoohas.",
    769: "The clear-minded.",
    808: "The one who tore the earth in His Incarnation as the Boar in order to destroy the mighty tyrant, Hiranyaaksha.",
    818: "He Who has taken the most auspicious Forms—to destroy the evil and to protect the good.",
    825: "The slayer of Chaanoora, the great wrestler.",
    831: "One who is sinless or sorrowless.",
    888: "The One Who enjoys the world of objects-emotions-thoughts.",
    889: "One Who gives the experience of Eternal Bliss to the devotees at their final spiritual destination-Moksha.",
    894: "The one sole substratum for the entire Universe of things and beings.",
    899: "One Who drinks water.",
    922: "One Whose Glory when heard and sung causes merits to grow in the bosom of that devotee.",
    936: "One Who deals squarely with all.",
    973: "The One Who performs Yajna according to the strict prescriptions laid down in the Vedas.",
    979: "One receiver of all that is offered.",
    993: "One Who has the divine conch named Paanchajanya.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def apply_exact(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected one occurrence of scan repair {old!r}; found {count}")
    return text.replace(old, new, 1)


def prepare_markdown(text: str) -> str:
    for old, new in UNICODE_REPAIRS:
        text = apply_exact(text, old, new)

    text = apply_exact(
        text,
        "Lord Vishnu's Divine Bow is\n\nDhanvee called",
        "Lord Vishnu's Divine Bow is called",
    )

    # Repair page-break tokens while preserving the word split around them.
    text = text.replace("newpage", "")

    # OCR sometimes emitted a heading and then placed its number alone on the
    # next line.  Move only marker-only lines whose immediately preceding block
    # visibly contains the entry's heading dash.
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.fullmatch(r"\s*(\d{1,4})\.\s*", line)
        if not match:
            continue
        number = int(match.group(1))
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j < 0:
            continue
        previous = lines[j].strip()
        k_next = i + 1
        while k_next < len(lines) and not lines[k_next].strip():
            k_next += 1
        following = lines[k_next].strip() if k_next < len(lines) else ""
        following_is_heading = bool(
            re.search(r"^[A-Za-z][A-Za-z -]{1,100}\s*\([^\n)]{1,60}\)\s*(?:—|--|-)", following)
        )
        if not following_is_heading and re.search(r"\([^\n)]{1,60}\)\s*(?:—|--|-)", previous):
            # If the script is on its own line, include the Roman heading line.
            start = j
            if not re.match(r"^[A-Za-z]", previous):
                k = j - 1
                while k >= 0 and not lines[k].strip():
                    k -= 1
                if k >= 0 and re.fullmatch(r"[A-Za-z][A-Za-z -]{1,80}", lines[k].strip()):
                    start = k
            lines[start] = f"{number}. {lines[start].lstrip()}"
            lines[i] = ""
    return "\n".join(lines)


def markers(text: str) -> dict[int, re.Match[str]]:
    start = text.index("### Stanza 1")
    body = text[start:]
    pattern = re.compile(r"(?m)^\s*(?:\((\d{1,4})\)|(\d{1,4})\.)\s*")
    result: dict[int, re.Match[str]] = {}
    for match in pattern.finditer(body):
        number = int(match.group(1) or match.group(2))
        if 1 <= number <= 1000 and number not in result:
            result[number] = match
    missing = [number for number in range(1, 1001) if number not in result]
    if missing:
        raise ValueError(f"missing numbered entry markers: {missing}")
    return result


def clean_heading(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip(" .:;-\n")
    return value


def clean_commentary(value: str) -> str:
    value = re.split(r"(?m)^\s*### Stanza \d+\s*$", value, maxsplit=1)[0]
    value = re.sub(r"(?m)^\s*### [^\n]+$", "", value)
    value = re.sub(r"(?m)^\s*\d{2,4}/\d{2,4}\s*$", "", value)
    value = re.sub(r"(?m)^\s*\d{1,3}\s+(?:VISHNU SAHASRANAAMA|GLORIES OF THE LORD)\s*$", "", value)
    # Join words split mechanically at a line/page edge.
    value = re.sub(r"([A-Za-z])-\s*\n\s*\n?\s*([a-z])", r"\1\2", value)
    # The cleaned OCR inserts blank lines for physical line wraps.  Preserve
    # explicit source paragraph breaks where possible, while avoiding a screen
    # full of one-line pseudo-paragraphs.
    chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n", value) if chunk.strip()]
    paragraphs: list[str] = []
    current = ""
    for chunk in chunks:
        chunk = re.sub(r"\s+", " ", chunk)
        if not current:
            current = chunk
        elif current.endswith((".", "?", "!", "।", "।।", '.”', '."', ".*", ".**", ".***")) and len(current) >= 180:
            paragraphs.append(current)
            current = chunk
        else:
            current += " " + chunk
    if current:
        paragraphs.append(current)
    value = "\n\n".join(paragraphs)
    value = value.replace("25 37,2", "")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value).strip()
    return value


def opening_sentence(commentary: str) -> str:
    """Return the first printed English sentence without rewriting it."""
    paragraph = commentary.split("\n\n", 1)[0].replace("\n", " ").strip()
    terminator = re.compile(
        r"[.!?](?:[\"”’']{0,2})(?=(?:[\*†‡]+)?(?:\s|$))"
    )
    for match in terminator.finditer(paragraph):
        candidate = paragraph[:match.end()].strip()
        if len(candidate) >= 5:
            return candidate
    return paragraph


def short_meaning_errors(value: object) -> list[str]:
    if not isinstance(value, str):
        return ["must be a string"]
    errors: list[str] = []
    if not 5 <= len(value) <= 240:
        errors.append("must contain 5–240 characters")
    if "\n" in value or "\r" in value:
        errors.append("must be a single line")
    if re.search(r"[\*†‡]", value):
        errors.append("must not contain footnote markers")
    if re.search(r"[\u0900-\u0d7f]", value):
        errors.append("must not contain embedded Indic script")
    if any(
        residue in value
        for residue in (
            "newpage",
            "###",
            "VISHNU SAHASRANAAMA",
            "GLORIES OF THE LORD",
            "Glories Of The Lord",
        )
    ):
        errors.append("must not contain page or heading residue")
    if re.search(r"[-‐‑–—]\s*$", value):
        errors.append("must not end in a broken hyphen")
    if re.search(r"(?<![A-Z])[a-z][A-Z][a-z]", value):
        errors.append("contains a suspicious lower-to-upper joined token")
    if re.search(
        r"(?i)(?:\b[a-z]\s*[.?]\s*){1,}\b[a-z]+\s+\d(?:\s*[-.?/]\s*\d)+",
        value,
    ):
        errors.append("contains OCR digit/punctuation junk")
    if sum(value.count(mark) for mark in '\"“”') % 2:
        errors.append("contains an unmatched quotation mark")
    if re.search(
        r"\b(?:says|declares|declared|thunders)\b[^.!?]{0,100}[\"“]",
        value,
        re.I,
    ):
        errors.append("must not embed a scriptural quotation")
    return errors


def parse_entry(span: str, number: int) -> tuple[str, str, str, list[str]]:
    span = re.sub(r"^\s*(?:\(\d{1,4}\)|\d{1,4}\.)\s*", "", span, count=1)
    header = re.match(
        r"(?s)^\s*[\'\"“”]?(?P<roman>[^(\n]{1,110}?)\s*"
        r"\((?P<script>[^)]{1,100})\)\s*(?:—|--|-)\s*(?P<commentary>.*)$",
        span,
    )
    if not header:
        raise ValueError(f"could not parse heading for name {number}: {span[:180]!r}")
    roman = clean_heading(header.group("roman"))
    script = re.sub(r"\s+", " ", header.group("script")).strip()
    notes: list[str] = []
    if not re.search(r"[\u0900-\u097f]", script):
        notes.append("Printed heading script was not legible in OCR; Sanskrit will be supplied from the verified text witness.")
        devanagari = ""
    elif re.search(r"[\u0980-\u09ff\u0a00-\u0a7f]", script):
        notes.append("Printed heading contains mixed-script OCR; Sanskrit will be supplied from the verified text witness.")
        devanagari = ""
    else:
        devanagari = script
    commentary = clean_commentary(header.group("commentary"))
    for old, new in COMMENTARY_REPAIRS.get(number, ()):
        count = commentary.count(old)
        if count != 1:
            raise ValueError(
                f"name {number}: expected one occurrence of commentary repair {old!r}; found {count}"
            )
        commentary = commentary.replace(old, new, 1)
    commentary = SCAN_CHECKED_COMMENTARY.get(number, commentary)
    if number == 545:
        commentary = (
            "The Well-concealed. He is not easily revealed by words. Nor can the sense organs ever recognise Him. "
            "All the Upanishads repeatedly declare that the Self being the very \"subject,\" the instruments of the "
            "body, mind and intellect can never apprehend Him. He can only be apprehended by a steady mind that has "
            "been purified by continuous meditation.* \"Being the hidden nature of all beings he is not manifested.\"**\n\n"
            "* \"When the understanding becomes calm and refined, then in meditation one realises Him, the Absolute.\" "
            "—Mundaka, Ch. III-1-8.\n\n"
            "** \"This Atman is hidden in all beings and does not shine forth.\" —Katha, Ch. I-iii-12."
        )
    if number == 1000:
        commentary = commentary.split("श्री सर्वप्रहरणाययः", 1)[0].strip()
    if number in SCAN_CHECKED_DEVANAGARI:
        devanagari = SCAN_CHECKED_DEVANAGARI[number]
        notes = []
    roman = SCAN_CHECKED_ROMAN.get(number, roman)
    if not roman or not commentary:
        raise ValueError(f"empty heading/commentary for name {number}")
    return roman, devanagari, commentary, notes


def page_anchors(page_ocr: str) -> dict[int, int]:
    pages = page_ocr.split("\f")
    anchors: dict[int, list[int]] = {}
    pattern = re.compile(r"(?m)^\s*(?:\((\d{1,4})\)|(\d{1,4})[.:])\s*[A-Za-z]")
    for page_number, page in enumerate(pages, 1):
        if not 20 <= page_number <= 251:
            continue
        for match in pattern.finditer(page):
            number = int(match.group(1) or match.group(2))
            if 1 <= number <= 1000:
                anchors.setdefault(number, []).append(page_number)

    # Prefer the monotonic candidate closest to a linearly projected page.
    chosen: dict[int, int] = {}
    for number, candidates in anchors.items():
        projected = 20 + (number - 1) * 231 / 999
        chosen[number] = min(candidates, key=lambda page: abs(page - projected))
    # Explicit image-witness pages for displaced/malformed numeric markers.
    chosen.update({
        1: 20, 18: 26, 19: 26, 56: 35, 76: 41, 91: 44, 98: 46,
        147: 59, 152: 60, 164: 63, 250: 84, 252: 85, 309: 100, 388: 118,
        421: 125, 545: 149, 678: 177, 732: 188, 747: 192, 907: 231,
        1000: 251,
    })
    return chosen


def interpolate_pages(anchors: dict[int, int]) -> dict[int, int]:
    reliable = sorted(anchors.items())
    result: dict[int, int] = {}
    for number in range(1, 1001):
        if number in anchors:
            result[number] = anchors[number]
            continue
        before = max((item for item in reliable if item[0] < number), default=(1, 20))
        after = min((item for item in reliable if item[0] > number), default=(1000, 251))
        if before[0] == after[0]:
            result[number] = before[1]
        else:
            fraction = (number - before[0]) / (after[0] - before[0])
            result[number] = round(before[1] + fraction * (after[1] - before[1]))
    # Enforce the physical ordering of entry starts.
    last = 20
    for number in range(1, 1001):
        result[number] = max(last, min(251, result[number]))
        last = result[number]
    return result


def extract(markdown_path: Path, page_ocr_path: Path, scan_path: Path) -> dict:
    text = prepare_markdown(markdown_path.read_text(encoding="utf-8"))
    found = markers(text)
    body_start = text.index("### Stanza 1")
    body = text[body_start:]
    starts = {number: match.start() for number, match in found.items()}
    start_pages = interpolate_pages(page_anchors(page_ocr_path.read_text(encoding="utf-8")))

    names = []
    for number in range(1, 1001):
        end = starts[number + 1] if number < 1000 else len(body)
        roman, devanagari, commentary, notes = parse_entry(body[starts[number]:end], number)
        raw_short_meaning = opening_sentence(commentary)
        if number in SHORT_MEANING_OVERRIDES:
            short_meaning = SHORT_MEANING_OVERRIDES[number]
            short_meaning_status = "scan-checked"
        else:
            short_meaning = raw_short_meaning
            short_meaning_status = "ocr-clean"
        meaning_errors = short_meaning_errors(short_meaning)
        if meaning_errors:
            raise ValueError(
                f"name {number}: invalid short meaning: {', '.join(meaning_errors)}"
            )
        last_page = start_pages[number + 1] if number < 1000 else start_pages[number]
        scan_pages = list(range(start_pages[number], last_page + 1))
        names.append({
            "number": number,
            "heading_roman": roman,
            "heading_devanagari": devanagari,
            "short_meaning": short_meaning,
            "short_meaning_status": short_meaning_status,
            "commentary": commentary,
            "scan_pages": scan_pages,
            "verification_status": "scan-checked" if number in SCAN_CHECKED_NUMBERS else "ocr-structured",
            "ocr_notes": notes,
        })

    return {
        "schema_version": 1,
        "work": {
            "title": "Vishnu Sahasranama: Thousand Ways to the Transcendental",
            "author": "Swami Chinmayananda",
            "edition": "Central Chinmaya Mission Trust, reprint February 2011",
            "isbn": "978-81-7597-245-2",
            "image_witness_sha256": sha256(scan_path),
            "permission_basis": "Owner states publication permission from Chinmaya Mission",
        },
        "names": names,
    }


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    work = data.get("work")
    required_work = {"title", "author", "edition", "isbn", "image_witness_sha256", "permission_basis"}
    if not isinstance(work, dict) or not required_work.issubset(work):
        errors.append("work metadata is incomplete")
    names = data.get("names")
    if not isinstance(names, list) or len(names) != 1000:
        errors.append(f"names must contain exactly 1000 records (found {len(names) if isinstance(names, list) else 'non-list'})")
        return errors
    numbers = [entry.get("number") for entry in names]
    if numbers != list(range(1, 1001)):
        errors.append("name numbers must be unique, contiguous, and ordered 1..1000")
    for entry in names:
        number = entry.get("number", "?")
        if not isinstance(entry.get("heading_roman"), str) or not entry["heading_roman"].strip():
            errors.append(f"name {number}: empty Roman heading")
        if not isinstance(entry.get("commentary"), str) or not entry["commentary"].strip():
            errors.append(f"name {number}: empty commentary")
        if not isinstance(entry.get("heading_devanagari"), str):
            errors.append(f"name {number}: heading_devanagari must be a string")
        meaning_errors = short_meaning_errors(entry.get("short_meaning"))
        for error in meaning_errors:
            errors.append(f"name {number}: short_meaning {error}")
        meaning_status = entry.get("short_meaning_status")
        if meaning_status not in {"ocr-clean", "scan-checked"}:
            errors.append(f"name {number}: invalid short_meaning_status")
        if number in SHORT_MEANING_OVERRIDES:
            if entry.get("short_meaning") != SHORT_MEANING_OVERRIDES[number]:
                errors.append(f"name {number}: short_meaning differs from scan-checked override")
            if meaning_status != "scan-checked":
                errors.append(f"name {number}: overridden short_meaning must be scan-checked")
        else:
            expected = opening_sentence(entry.get("commentary", ""))
            if entry.get("short_meaning") != expected:
                errors.append(f"name {number}: ocr-clean short_meaning differs from opening sentence")
            if meaning_status != "ocr-clean":
                errors.append(f"name {number}: unchanged short_meaning must be ocr-clean")
        pages = entry.get("scan_pages")
        if not isinstance(pages, list) or not pages or any(not isinstance(page, int) or not 1 <= page <= 272 for page in pages):
            errors.append(f"name {number}: invalid scan_pages")
        if entry.get("verification_status") not in {"scan-checked", "ocr-structured"}:
            errors.append(f"name {number}: invalid verification_status")
        if not isinstance(entry.get("ocr_notes"), list):
            errors.append(f"name {number}: ocr_notes must be a list")
        haystack = f"{entry.get('heading_roman', '')}\n{entry.get('commentary', '')}"
        for artifact in FORBIDDEN_ARTIFACTS:
            if artifact in haystack:
                errors.append(f"name {number}: forbidden OCR artifact {artifact!r}")
        if re.search(r"(?<![A-Z])[a-z][A-Z][a-z]", entry.get("commentary", "")):
            errors.append(f"name {number}: suspicious lower-to-upper joined token")
    expected_headings = {831: "Anaghah", 832: "Achintyah"}
    for number, heading in expected_headings.items():
        if names[number - 1].get("heading_roman") != heading:
            errors.append(f"name {number}: expected heading {heading!r}")
    for number, repairs in COMMENTARY_REPAIRS.items():
        commentary = names[number - 1].get("commentary", "")
        for old, _new in repairs:
            if old in commentary:
                errors.append(f"name {number}: unrepaired OCR/layout fragment {old!r}")
    junk_patterns = (
        "bosom exNarayanopanishad",
        "I a. ? condo 0 1 - 0 2) 10",
        "The Self.\n\n* At the physical level",
        "XI---16 be nothing",
    )
    for entry in names:
        for junk in junk_patterns:
            if junk in entry.get("commentary", ""):
                errors.append(f"name {entry.get('number')}: forbidden OCR/layout junk {junk!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--page-ocr", type=Path, default=DEFAULT_PAGE_OCR)
    parser.add_argument("--scan", type=Path, default=DEFAULT_SCAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path, help="validate an existing JSON instead of extracting")
    args = parser.parse_args()
    started = time.monotonic()

    if args.check:
        data = json.loads(args.check.read_text(encoding="utf-8"))
    else:
        data = extract(args.markdown, args.page_ocr, args.scan)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    statuses = {status: 0 for status in ("scan-checked", "ocr-structured")}
    meaning_statuses = {status: 0 for status in ("scan-checked", "ocr-clean")}
    for entry in data["names"]:
        statuses[entry["verification_status"]] += 1
        meaning_statuses[entry["short_meaning_status"]] += 1
    notes = sum(len(entry["ocr_notes"]) for entry in data["names"])
    print(
        f"OK names=1000 scan-checked={statuses['scan-checked']} "
        f"ocr-structured={statuses['ocr-structured']} unresolved-notes={notes} "
        f"short-scan-checked={meaning_statuses['scan-checked']} "
        f"short-ocr-clean={meaning_statuses['ocr-clean']} "
        f"wall-seconds={time.monotonic() - started:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
