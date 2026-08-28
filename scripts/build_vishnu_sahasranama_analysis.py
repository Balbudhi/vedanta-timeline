#!/usr/bin/env python3
"""Build source-backed word cards for all 1,000 Viṣṇusahasranāma names.

Generation consumes the deterministic prejoin packet (received text,
Chinmayananda, Vidyut, and Monier-Williams). The committed artifact is fully
self-validating; regeneration additionally requires the pinned source packet.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "gita/vishnu-sahasranama/_build/word-analysis-prejoin.json.gz"
DEFAULT_MW = Path("/tmp/mw-csl.txt")
DEFAULT_OUTPUT = ROOT / "gita/vishnu-sahasranama/analysis.json"
COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
PACKET_FILE_SHA256 = "16120ab456f8bf575923510b8b4ecf5706eabd43c8f0fdef9b67de70a500db18"
PACKET_PAYLOAD_SHA256 = "1d057b8c18e05141c309b94e17156cac0b9ad7bd2f5c230064fd686fc27c7429"
MW_SHA256 = "f4fff3926d053848d44807b08d3f14f0755793e92f04e7424e03bcad2ca7e4e5"
MW_INDEX: dict[str, list[dict]] = {}

# The pinned boundary aid is valuable for numbering but contains a small,
# finite set of romanization/OCR errors. These citation forms were checked
# against the received stanza and the BORI witness before morphological lookup.
# Surface sandhi remains untouched in reader.json.
CITATION_CORRECTIONS = {
    31: "saṃbhavaḥ",
    54: "sthaviraḥ dhruvaḥ",
    91: "saṃvatsaraḥ",
    95: "ajaḥ",
    100: "acyutaḥ",
    113: "vṛṣākṛtiḥ",
    125: "viṣvaksenaḥ",
    128: "vedavit",
    134: "surādhyakṣaḥ",
    141: "bhrājiṣṇuḥ",
    145: "jagadādijaḥ",
    164: "vaidyaḥ",
    173: "mahābuddhiḥ",
    182: "mahībhartā",
    184: "satāṃ gatiḥ",
    200: "siṃhaḥ",
    207: "viśrutātmā",
    213: "satyaparākramaḥ",
    228: "āvartanaḥ",
    238: "viśvadhṛk",
    239: "viśvabhuk",
    250: "śiṣṭakṛt",
    257: "vṛṣabhaḥ",
    275: "ojas-tejo-dyuti-dharaḥ",
    296: "kāntaḥ",
    305: "vyaktarūpaḥ",
    315: "krodhakṛt-kartā",
    317: "mahīdharaḥ",
    333: "bṛhadbhānuḥ",
    345: "padmanibhekṣaṇaḥ",
    349: "śarīrabhṛt",
    350: "maharddhiḥ",
    385: "vyavasthānaḥ",
    386: "saṃsthānaḥ",
    394: "rāmaḥ",
    396: "virajaḥ",
    427: "sthāvaraḥ sthāṇuḥ",
    434: "mahādhanaḥ",
    435: "anirviṇṇaḥ",
    453: "sarvajñaḥ",
    450: "satāṃ gatiḥ",
    454: "jñānam uttamam",
    475: "dharmagup",
    482: "avijñātā",
    488: "siṃhaḥ",
    507: "purusattamaḥ",
    512: "sātvatāṃ patiḥ",
    552: "saṅkarṣaṇaḥ acyutaḥ",
    555: "vṛkṣaḥ",
    568: "khaṇḍaparaśuḥ",
    571: "divaspṛk",
    581: "śamaḥ",
    582: "śāntaḥ",
    584: "śāntiḥ",
    595: "vṛṣapriyaḥ",
    604: "śrīmatāṃ varaḥ",
    613: "śrīmān",
    617: "śatānandaḥ",
    618: "nandiḥ",
    628: "bhūśayaḥ",
    660: "dhanañjayaḥ",
    697: "vasumanāḥ",
    715: "durdharaḥ",
    716: "aparājitaḥ",
    728: "kaḥ",
    729: "kim",
    734: "lokanāthaḥ",
    732: "padam anuttamam",
    744: "ghṛtāśīḥ",
    751: "trilokadhṛk",
    752: "sumedhā",
    755: "satyamedhā",
    759: "sarva-śastra-bhṛtāṃ varaḥ",
    774: "anivṛttātmā",
    797: "śṛṅgī",
    825: "cāṇūrāndhra-niṣūdanaḥ",
    832: "acintyaḥ",
    833: "bhayakṛt",
    842: "adhṛtaḥ",
    859: "daṇḍaḥ",
    871: "abhiprāyaḥ",
    875: "prītivardhanaḥ",
    894: "lokādhiṣṭhānam",
    902: "svastikṛt",
    907: "kuṇḍalī",
    937: "gabhīrātmā",
    943: "lakṣmīḥ",
    945: "rucirāṅgadaḥ",
    948: "bhīmaḥ",
    949: "bhīma-parākramaḥ",
    950: "ādhāranilayaḥ",
    961: "prāṇabhṛt",
    967: "bhūr-bhuvaḥ-svas-taruḥ",
    974: "yajñāṅgaḥ",
    984: "annādaḥ",
    993: "śaṅkhabhṛt",
    1000: "sarvapraharaṇāyudhaḥ",
}

STOPWORDS = {
    "that", "which", "whose", "with", "from", "into", "this", "one", "who",
    "the", "and", "all", "him", "himself", "called", "means", "meaning",
    "lord", "supreme", "vishnu", "sree", "narayana",
}

MEMBER_LEXICON = {
    "a": "not; without", "an": "not; without", "ati": "beyond; exceeding",
    "adhi": "over; above", "anu": "after; following", "apa": "away; forth",
    "abhi": "towards; fully", "ava": "down; away", "ā": "towards; up to",
    "ud": "up; forth", "upa": "near; towards", "ni": "down; in",
    "nir": "out; without", "nis": "out; without", "parā": "away; beyond",
    "pari": "around; completely", "pra": "forth; forward", "prati": "towards; in return",
    "sam": "together; completely", "su": "good; well", "dus": "bad; difficult",
    "dur": "bad; difficult", "mahā": "great", "sarva": "all; every",
    "viśva": "all; the universe", "loka": "world", "jagat": "world; moving universe",
    "bhūta": "being; creature", "bhavya": "future; what is to be", "bhavat": "present; existing",
    "ātman": "self", "puruṣa": "person; spirit", "deva": "deity; shining one",
    "īśa": "lord", "īśvara": "lord; sovereign", "prabhu": "lord; master",
    "pati": "lord; master", "nātha": "lord; protector", "dhara": "bearing; supporting",
    "bhṛt": "bearer; supporter", "kṛt": "maker; doer", "kartṛ": "maker; doer",
    "jña": "knowing; knower", "vid": "knowing; knower", "rūpa": "form; appearance",
    "akṣa": "eye", "īkṣaṇa": "seeing; eye", "nābhi": "navel", "garbha": "womb; interior",
    "ādi": "beginning; first", "anta": "end; limit", "ananta": "endless; infinite",
    "satya": "true; real", "dharma": "law; right order; duty", "jñāna": "knowledge",
    "buddhi": "understanding; intelligence", "medhā": "intelligence; wisdom",
    "śrī": "splendour; prosperity", "tejas": "radiance; energy", "dyuti": "splendour; lustre",
    "ojas": "vital strength; vigour", "prāṇa": "breath; vital life", "yajña": "sacrifice; worship",
    "soma": "Soma; the sacred draught", "amṛta": "immortal; nectar", "padma": "lotus",
    "puṣkara": "lotus", "kṣetra": "field", "gati": "going; destination; goal",
    "nidhi": "store; treasury; receptacle", "śastra": "weapon", "vara": "best; foremost",
    "vaṣaṭ": "the vaṣaṭ call used in sacrifice", "prabhuḥ": "lord; master",
    "puruṣeśvaraḥ": "lord of persons and spirits", "nidhir": "store; treasury; receptacle",
    "avyayaḥ": "imperishable; undecaying", "svayam": "oneself; by oneself",
    "śam": "welfare; auspiciousness", "an-ādi": "without beginning", "a-mara": "immortal",
    "vin": "possessing; endowed with", "ātma": "self", "sarvayoga": "every bond or connection",
    "viniḥsṛtaḥ": "gone out from; free from", "sthāṇuḥ": "firm; motionless",
    "bhānuḥ": "light; radiance", "srag": "garland", "vācaspatir": "lord of speech",
    "udāradhīḥ": "having noble understanding", "ṇī": "leader; guide",
    "saṃvartakaḥ": "drawing together; dissolving", "vāg": "speech", "min": "possessing",
    "bṛhad": "great; vast", "tejo": "radiance; energy", "dharaḥ": "bearing; supporting",
    "dyutiḥ": "splendour; lustre", "parākramaḥ": "heroic power; valour",
    "bhavan": "present; existing", "nāthaḥ": "lord; protector", "vy-akta": "manifest; distinct",
    "an-anta": "without end; infinite", "krodhakṛt": "maker of anger", "kartā": "maker; doer",
    "nibhekṣaṇa": "having eyes resembling the preceding member", "rddhi": "prosperity; power",
    "sam-aya": "agreement; convention; proper time", "havir": "sacrificial oblation",
    "hariḥ": "Hari; the remover", "lakṣaṇyaḥ": "indicated or characterized by marks",
    "sam-iti": "assembly; encounter; battle", "ṃ-jaya": "conquering; victorious",
    "viduttamaḥ": "best among knowers", "parame": "in the highest", "ṣṭhin": "standing; abiding",
    "yūpaḥ": "sacrificial post", "satāṃ": "of the good", "gatiḥ": "going; destination; goal",
    "jñānam": "knowledge", "mano": "mind", "sat-tva": "being; essence",
    "devabhṛd": "supporter of the gods", "guruḥ": "teacher; weighty one", "a-mṛta": "immortal; nectar",
    "sātvatāṃ": "of the Sātvatas", "patiḥ": "lord; master", "vinayitā": "guide; disciplinarian",
    "sākṣī": "witness", "a-mita": "unmeasured; measureless", "mahodadhi": "great ocean",
    "śayaḥ": "lying; resting", "rha": "worthy", "ṣeṇa": "army; host",
    "saṅkarṣaṇo": "Saṅkarṣaṇa; the one who draws together", "acyutaḥ": "unfallen; unfailing",
    "jyotir": "light", "ādityaḥ": "Āditya; the sun", "divah": "of heaven", "spṛk": "touching; reaching",
    "sarvadṛg": "all-seeing", "vyāsaḥ": "arranger; compiler", "sāmā": "Sāman chant",
    "śrīmatāṃ": "among those endowed with śrī", "gaṇeśvaraḥ": "lord of hosts",
    "sarvataḥ": "on every side", "cakṣuḥ": "eye", "sthiraḥ": "firm; stable", "rathaḥ": "chariot",
    "kālanemi": "the demon Kālanemi", "priyaḥ": "dear; beloved", "bhūtiḥ": "being; prosperity",
    "a-mūrti": "without material form", "su-varṇa": "beautifully coloured; golden", "ṣama": "even; equal",
    "labha": "obtainable; attainment", "āri-han": "slayer of enemies",
    "vāg-īśvareśvara": "lord of the lords of speech", "nyag": "downward", "ttha": "standing; abiding",
    "cāṇūrāndhra": "Cāṇūra, the wrestler", "niṣūdanaḥ": "destroyer; slayer", "sapta": "seven",
    "prāg": "forward; eastward", "dhanur": "bow", "duḥ": "bad; difficult", "kīrtanaḥ": "praise; recitation",
    "janmādiḥ": "birth and what follows", "bhīma": "terrible; formidable", "jīvanaḥ": "life-giving; enlivening",
    "jarātigaḥ": "going beyond old age", "bhuvaḥ": "the middle world; atmosphere",
    "svastaruḥ": "the beneficent tree", "svayaṃ": "oneself; by oneself", "jātaḥ": "born",
    "devakī": "Devakī",
    "varaḥ": "best; foremost", "sarvato": "on every side", "sv-asti": "well-being; auspiciousness",
    "śāsanaḥ": "command; rule; discipline",
    "vi": "apart; distinctly", "vṛṣā": "bull; emblem of dharma", "asaṃkhyeya": "innumerable",
    "asaṅkhyeya": "innumerable", "bhāvana": "causing to be; producing; fostering",
    "da": "giving; giver", "uttama": "highest; best", "praharaṇa": "weapon; implement of attack",
    "āyudha": "weapon",
    "mat": "possessing; endowed with", "catur": "four", "saṃśaya": "doubt; uncertainty",
    "tal": "abstract-state suffix: -ness; state of being", "bhūr": "earth; the terrestrial world",
    "bhūḥ": "earth; the terrestrial world", "anna": "food", "āda": "eater",
    "śaṅkha": "conch", "nandi": "delighting; joyful", "śāśvata": "eternal; constant",
    "skanda": "Skanda", "stava": "praise; hymn", "sad": "good; true; existent",
    "sat": "good; true; existent", "vapus": "form; body", "ahan": "day",
    "havis": "sacrificial oblation", "jyotis": "light; radiance", "cakṣus": "eye",
    "puruṣeśvara": "lord of persons and spirits", "viniḥsṛta": "gone out from; free from",
    "sthāṇu": "firm; motionless", "bhānu": "light; radiance", "vācaspati": "lord of speech",
    "udāra-dhī": "having noble understanding", "saṃvartaka": "drawing together; dissolving",
    "parākrama": "heroic power; valour", "nātha": "lord; protector", "dhara": "bearing; supporting",
    "dyuti": "splendour; lustre", "lakṣaṇya": "indicated or characterized by marks",
    "yūpa": "sacrificial post", "guru": "teacher; weighty one", "śaya": "lying; resting",
    "āditya": "Āditya; the sun", "vyāsa": "arranger; compiler", "gaṇeśvara": "lord of hosts",
    "sthira": "firm; stable", "ratha": "chariot", "priya": "dear; beloved",
    "bhūti": "being; prosperity", "gati": "going; destination; goal", "śāsana": "command; rule; discipline",
    "kīrtana": "praise; recitation", "janmādi": "birth and what follows", "jīvana": "life-giving; enlivening",
    "jarātiga": "going beyond old age", "jāta": "born", "niṣūdana": "destroyer; slayer",
    "vid-uttama": "best among knowers", "sarva-dṛś": "all-seeing",
    "hari": "Hari; the receiver and remover", "lakṣaṇa": "mark; characteristic",
    "bhāskara": "light-maker; sun", "vyūha": "arrangement; ordered manifestation",
    "daṃṣṭra": "tusk; fang", "bhuja": "arm", "bāhu": "arm", "mūrti": "form; embodiment",
    "vihāyasa": "sky; atmosphere", "ūrjita": "strong; powerful", "puṇya": "merit; virtue; purity",
    "śravaṇa": "hearing; that which is heard", "svapna": "dream", "nāśana": "destroying; remover",
    "jana": "person; creature", "janma": "birth", "mṛtyu": "death", "nārasiṃha": "the man-lion form",
    "bhū": "being; becoming", "bhu": "being; becoming", "svana": "sound; resonance",
    "dhā": "placing; supporting", "tri": "three", "dhāma": "abode; domain", "vat": "possessing",
    "retas": "seed; generative power", "darśana": "seeing; vision", "karman": "action; deed",
    "sadā": "always", "vīra": "hero; valiant one", "han": "slayer", "bala": "strength; power",
    "mahī": "earth", "bhartṛ": "bearer; supporter", "surāri": "enemy of the gods",
    "grāma": "group; community", "saṃkalpa": "resolve; intention", "sāgara": "ocean",
    "śana": "calm; quiet", "sahasra": "thousand", "jit": "conquering; victor", "kośa": "treasury; sheath",
    "sva": "own; oneself", "pa": "drinker", "saṃdha": "joining; union", "medinī": "earth",
    "varāha": "boar", "śānti": "peace; tranquillity", "muda": "joy; delight", "yāmuna": "of the Yamunā",
    "bhakta": "devotee", "jaya": "victory; conquest", "gama": "going", "indra": "Indra; lord",
    "kāma": "desire", "rodha": "growth; obstruction", "jihva": "tongue", "mahat": "great; mighty",
    "siddha": "accomplished; perfected", "sukha": "pleasure; ease", "vidvat": "learned; wise",
    "aśra": "corner; angle", "bhuj": "enjoying; experiencing",
}

# Exact prātipadika corrections for members that the surface/citation aid
# supplies with visarga, sandhi, or an already-inflected ending.
MEMBER_FORM_CORRECTIONS = {
    4: {"prabhuḥ": "prabhu"}, 20: {"puruṣeśvaraḥ": "puruṣeśvara"},
    21: {"vapuḥ": "vapus"}, 30: {"nidhir": "nidhi", "avyayaḥ": "avyaya"},
    103: {"viniḥsṛtaḥ": "viniḥsṛta"}, 120: {"sthāṇuḥ": "sthāṇu"},
    124: {"bhānuḥ": "bhānu"}, 177: {"vapuḥ": "vapus"},
    217: {"vācaspatir": "vācaspati", "udāradhīḥ": "udāra-dhī"},
    232: {"ahaḥ": "ahan", "saṃvartakaḥ": "saṃvartaka"},
    275: {"tejo": "tejas", "dharaḥ": "dhara"}, 282: {"dyutiḥ": "dyuti"},
    289: {"parākramaḥ": "parākrama"}, 290: {"nāthaḥ": "nātha"},
    328: {"dharaḥ": "dhara"}, 359: {"havir": "havis", "hariḥ": "hari"},
    360: {"lakṣaṇyaḥ": "lakṣaṇya"}, 404: {"viduttamaḥ": "vid-uttama"},
    438: {"yūpaḥ": "yūpa"}, 493: {"guruḥ": "guru"}, 519: {"śayaḥ": "śaya"},
    564: {"jyotir": "jyotis", "ādityaḥ": "āditya"},
    572: {"sarvadṛg": "sarva-dṛś", "vyāsaḥ": "vyāsa"},
    619: {"jyotir": "jyotis", "gaṇeśvaraḥ": "gaṇeśvara"},
    625: {"cakṣuḥ": "cakṣus"}, 627: {"sthiraḥ": "sthira"},
    639: {"rathaḥ": "ratha"}, 656: {"vapuḥ": "vapus"},
    680: {"priyaḥ": "priya"}, 702: {"bhūtiḥ": "bhūti"},
    825: {"niṣūdanaḥ": "niṣūdana"}, 876: {"gatiḥ": "gati"},
    910: {"śāsanaḥ": "śāsana"}, 922: {"kīrtanaḥ": "kīrtana"},
    947: {"janmādiḥ": "janmādi"}, 949: {"parākramaḥ": "parākrama"},
    962: {"jīvanaḥ": "jīvana"}, 966: {"jarātigaḥ": "jarātiga"},
    986: {"jātaḥ": "jāta"},
}

TRANSLATION_CARD_AUDIT = {
    2, 10, 11, 17, 23, 24, 27, 34, 45, 46, 56, 89, 91, 95, 101, 113,
    125, 134, 184, 207, 213, 250, 555, 568, 595, 751, 774, 832, 842,
    871, 875, 894, 943, 945, 950,
}

GENDER_LABEL = {"puM": "masculine", "strI": "feminine", "napuMsaka": "neuter"}
CASE_LABEL = {
    "praTamA": "nominative", "dvitIyA": "accusative", "tftIyA": "instrumental",
    "caturTI": "dative", "paYcamI": "ablative", "zazWI": "genitive",
    "saptamI": "locative", "samboDana": "vocative",
}
NUMBER_LABEL = {"eka": "singular", "dvi": "dual", "bahu": "plural"}

# Contextually reviewed head-gender exceptions and received multiword phrases.
EXPECTED_GENDER = {
    1: "napuMsaka", 12: "strI", 21: "napuMsaka", 45: "puM", 62: "napuMsaka", 63: "napuMsaka",
    86: "napuMsaka", 87: "napuMsaka", 113: "strI", 142: "napuMsaka", 177: "napuMsaka", 184: "strI", 211: "napuMsaka",
    287: "napuMsaka", 324: "napuMsaka", 378: "napuMsaka", 379: "napuMsaka",
    428: "napuMsaka", 429: "napuMsaka", 430: "puM", 431: "puM",
    448: "napuMsaka", 449: "napuMsaka", 450: "puM", 451: "napuMsaka",
    452: "puM", 453: "napuMsaka", 454: "napuMsaka", 455: "napuMsaka",
    479: "napuMsaka", 577: "napuMsaka", 578: "napuMsaka", 580: "puM",
    583: "strI", 584: "strI", 585: "napuMsaka", 606: "strI", 607: "strI",
    608: "puM", 609: "puM", 610: "puM", 611: "puM", 612: "napuMsaka",
    613: "puM", 681: "napuMsaka", 682: "strI", 683: "puM", 684: "puM",
    685: "puM", 686: "puM", 687: "puM", 688: "puM", 689: "puM",
    656: "napuMsaka", 701: "strI", 703: "napuMsaka", 704: "strI", 728: "puM", 729: "napuMsaka",
    730: "napuMsaka", 731: "napuMsaka", 732: "napuMsaka", 943: "strI",
    959: "napuMsaka", 963: "napuMsaka", 982: "napuMsaka", 983: "napuMsaka",
}

COMPOUND_OVERRIDES = {
    4: ("ṣaṣṭhī-tatpuruṣa with coordinated dependents", "bhūtasya bhavyasya bhavataś ca prabhuḥ"),
    5: ("upapada-tatpuruṣa", "bhūtāni karoti iti bhūtakṛt"),
    6: ("upapada-tatpuruṣa", "bhūtāni bibharti iti bhūtabhṛt"),
    20: ("ṣaṣṭhī-tatpuruṣa with coordinated dependents", "pradhānasya puruṣasya ca īśvaraḥ"),
    21: ("bahuvrīhi", "narasiṃhaṃ vapur yasya saḥ"),
    40: ("bahuvrīhi", "puṣkaravad akṣiṇī yasya saḥ"),
    47: ("ṣaṣṭhī-tatpuruṣa", "hṛṣīkāṇām īśaḥ"),
    48: ("bahuvrīhi", "padmaṃ nābhau yasya saḥ"),
}

ROOT_OVERRIDES = {
    5: ({"form": "√kṛ", "gana": "tanādi (8)", "pada": "ubhayapada", "gloss": "to do; make"}, "kvip (kṛt) + su (prathamā ekavacana)"),
    6: ({"form": "√bhṛ", "gana": "juhotyādi (3)", "pada": "ubhayapada", "gloss": "to bear; support; nourish"}, "kvip (kṛt) + su (prathamā ekavacana)"),
    7: ({"form": "√bhū", "gana": "bhvādi (1)", "pada": "parasmaipada", "gloss": "to be; become"}, "ghañ (kṛt) + su (prathamā ekavacana)"),
    18: ({"form": "√yuj", "gana": "rudhādi (7)", "pada": "ubhayapada", "gloss": "to join; yoke"}, "ghañ (kṛt) + su (prathamā ekavacana)"),
    33: ({"form": "√bhṛ", "gana": "juhotyādi (3)", "pada": "ubhayapada", "gloss": "to bear; support"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    43: ({"form": "√dhā", "gana": "juhotyādi (3)", "pada": "ubhayapada", "gloss": "to put; place; support"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    44: ({"form": "√dhā", "gana": "juhotyādi (3)", "pada": "ubhayapada", "gloss": "to put; arrange; establish"}, "vi- + √dhā + tṛc (kṛt) + su (prathamā ekavacana)"),
    59: ({"form": "√tṛd", "gana": "rudhādi (7)", "pada": "ubhayapada", "gloss": "to split; destroy"}, "pra- + √tṛd + lyuṭ (kṛt) + su (prathamā ekavacana)"),
    79: ({"form": "√kram", "gana": "bhvādi (1)", "pada": "parasmaipada", "gloss": "to step; stride"}, "ghañ (kṛt) + su (prathamā ekavacana)"),
    143: ({"form": "√bhuj", "gana": "rudhādi (7)", "pada": "ubhayapada", "gloss": "to enjoy; experience"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    163: ({"form": "√vid", "gana": "adādi (2)", "pada": "parasmaipada", "gloss": "to know"}, "ṇyat (kṛt) + su (prathamā ekavacana)"),
    222: ({"form": "√nī", "gana": "bhvādi (1)", "pada": "ubhayapada", "gloss": "to lead; carry"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    380: ({"form": "√kṛ", "gana": "tanādi (8)", "pada": "ubhayapada", "gloss": "to do; make"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    398: ({"form": "√nī", "gana": "bhvādi (1)", "pada": "ubhayapada", "gloss": "to lead; carry"}, "yat (kṛt) + su (prathamā ekavacana)"),
    500: ({"form": "√bhuj", "gana": "rudhādi (7)", "pada": "ubhayapada", "gloss": "to enjoy; experience"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    588: ({"form": "√sṛj", "gana": "tudādi (6)", "pada": "parasmaipada", "gloss": "to release; create"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    634: ({"form": "√arc", "gana": "bhvādi (1)", "pada": "parasmaipada", "gloss": "to praise; worship"}, "kta (kṛt) + su (prathamā ekavacana)"),
    683: ({"form": "√stu", "gana": "adādi (2)", "pada": "ubhayapada", "gloss": "to praise"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    714: ({"form": "√dṛp", "gana": "divādi (4)", "pada": "parasmaipada", "gloss": "to be proud; exult"}, "kta (kṛt) + su (prathamā ekavacana)"),
    888: ({"form": "√bhuj", "gana": "rudhādi (7)", "pada": "ubhayapada", "gloss": "to enjoy; experience"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
    929: ({"form": "√as", "gana": "adādi (2)", "pada": "parasmaipada", "gloss": "to be; exist"}, "śatṛ (kṛt, present participle) + jas (prathamā bahuvacana)"),
    973: ({"form": "√yaj", "gana": "bhvādi (1)", "pada": "ubhayapada", "gloss": "to sacrifice; worship"}, "kvanip (kṛt) + su (prathamā ekavacana)"),
    990: ({"form": "√sṛj", "gana": "tudādi (6)", "pada": "parasmaipada", "gloss": "to release; create"}, "tṛc (kṛt) + su (prathamā ekavacana)"),
}

PART_GLOSS_OVERRIDES = {
    4: {"bhūta": "past", "bhavya": "future", "bhavat": "present", "prabhu": "lord, master"},
    5: {"bhūta": "creature, being", "kṛt": "maker, creator"},
    6: {"bhūta": "creature, being", "bhṛt": "bearer, supporter, nourisher"},
    20: {"pradhāna": "primordial matter", "puruṣa": "spirit, person", "īśvara": "lord, master"},
    21: {"nara": "human", "siṃha": "lion", "vapus": "form, body"},
    40: {"puṣkara": "lotus", "akṣa": "eye"},
    47: {"hṛṣīka": "sense organ", "īśa": "lord"},
    48: {"padma": "lotus", "nābhi": "navel"},
}

PHRASE_OVERRIDES = {
    54: {
        "stem": "sthavira + dhruva",
        "parts": [
            {"form_iast": "sthavira", "gloss": "ancient, venerable", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "dhruva", "gloss": "fixed, constant, enduring", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "two nominative singular masculine epithets",
        "affix": "su (prathamā ekavacana) on both epithets",
        "root": None,
        "grammar": "Two coordinated epithets counted together in this enumeration: 'the ancient; the constant.'",
    },
    12: {
        "stem": "gati",
        "parts": [
            {"form_iast": "√muc (tudādi 6U)", "gloss": "to release, free", "kind": "root"},
            {"form_iast": "kta", "gloss": "past participle: liberated", "kind": "suffix"},
            {"form_iast": "ām", "gloss": "genitive plural: of the liberated", "kind": "ending"},
            {"form_iast": "parama", "gloss": "supreme, highest", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular feminine agreement", "kind": "ending"},
            {"form_iast": "√gam (bhvādi 1P)", "gloss": "to go", "kind": "root"},
            {"form_iast": "ktin", "gloss": "action/result noun: going, destination, goal", "kind": "suffix"},
            {"form_iast": "su", "gloss": "nominative singular feminine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular feminine adjective and head",
        "affix": "√muc + kta + ām (ṣaṣṭhī bahuvacana); parama + su; √gam + ktin + su (prathamā ekavacana)",
        "root": {"form": "√gam", "gana": "bhvādi (1)", "pada": "parasmaipada", "gloss": "to go"},
        "grammar": "A genitive phrase: 'the supreme destination of the liberated'; paramā agrees with the feminine head gatiḥ.",
    },
    19: {
        "stem": "netṛ",
        "parts": [
            {"form_iast": "yoga-vid", "gloss": "knower of yoga", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: of those who know", "kind": "ending"},
            {"form_iast": "netṛ", "gloss": "leader, guide", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)",
        "root": None,
        "grammar": "A genitive phrase: 'leader of those who know yoga.'",
    },
    63: {
        "stem": "maṅgala",
        "parts": [
            {"form_iast": "maṅgala", "gloss": "auspiciousness; blessing", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter head", "kind": "ending"},
            {"form_iast": "parama", "gloss": "supreme", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter agreement", "kind": "ending"},
        ],
        "morph": "nominative singular neuter noun with agreeing superlative adjective",
        "affix": "su (prathamā ekavacana) on both head and adjective",
        "root": None,
        "grammar": "A nominal phrase: 'the supreme auspiciousness'; param agrees with maṅgalam.",
    },
    188: {
        "stem": "pati",
        "parts": [
            {"form_iast": "go-vid", "gloss": "knower of speech/knowledge", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural", "kind": "ending"},
            {"form_iast": "pati", "gloss": "lord, master", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'lord of the knowers of go (speech/knowledge).'",
    },
    184: {
        "stem": "gati",
        "parts": [
            {"form_iast": "sat", "gloss": "good; true; existent", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: of the good", "kind": "ending"},
            {"form_iast": "gati", "gloss": "going, destination, goal", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular feminine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular feminine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'the destination of the good.'",
    },
    288: {
        "stem": "setu",
        "parts": [
            {"form_iast": "jagat", "gloss": "world, moving universe", "kind": "stem"},
            {"form_iast": "as", "gloss": "genitive singular: of the world", "kind": "ending"},
            {"form_iast": "setu", "gloss": "bridge, boundary, causeway", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive singular neuter dependent + nominative singular masculine head",
        "affix": "ṅas (ṣaṣṭhī ekavacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'the bridge or boundary of the world.'",
    },
    323: {
        "stem": "nidhi",
        "parts": [
            {"form_iast": "ap", "gloss": "water", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: of the waters", "kind": "ending"},
            {"form_iast": "nidhi", "gloss": "store, treasury, receptacle", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive plural feminine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'repository of the waters.'",
    },
    402: {
        "stem": "śreṣṭha",
        "parts": [
            {"form_iast": "śaktimat", "gloss": "possessing power", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: among/of the powerful", "kind": "ending"},
            {"form_iast": "śreṣṭha", "gloss": "best, most excellent", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A partitive genitive phrase: 'the best among those possessing power.'",
    },
    427: {
        "stem": "sthāvara + sthāṇu",
        "parts": [
            {"form_iast": "sthāvara", "gloss": "standing, fixed, immovable", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "sthāṇu", "gloss": "firm, motionless, stable", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "two nominative singular masculine epithets",
        "affix": "su (prathamā ekavacana) on both epithets",
        "root": None,
        "grammar": "Two coordinated epithets counted together in this enumeration: 'the fixed; the motionless.'",
    },
    450: {
        "stem": "gati",
        "parts": [
            {"form_iast": "sat", "gloss": "good; true; existent", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: of the good", "kind": "ending"},
            {"form_iast": "gati", "gloss": "going, destination, goal", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular feminine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular feminine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'the destination of the good.'",
    },
    454: {
        "stem": "jñāna",
        "parts": [
            {"form_iast": "jñāna", "gloss": "knowledge", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter head", "kind": "ending"},
            {"form_iast": "uttama", "gloss": "highest, best", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter agreement", "kind": "ending"},
        ],
        "morph": "nominative singular neuter noun with agreeing adjective",
        "affix": "su (prathamā ekavacana) on both head and adjective", "root": None,
        "grammar": "A nominal phrase: 'the highest knowledge'; uttamam agrees with jñānam.",
    },
    512: {
        "stem": "pati",
        "parts": [
            {"form_iast": "sātvata", "gloss": "member of the Sātvata people", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: of the Sātvatas", "kind": "ending"},
            {"form_iast": "pati", "gloss": "lord, master", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A genitive phrase: 'lord of the Sātvatas.'",
    },
    552: {
        "stem": "saṅkarṣaṇa + acyuta",
        "parts": [
            {"form_iast": "saṅkarṣaṇa", "gloss": "the one who draws together", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "a-cyuta", "gloss": "unfallen, unfailing", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "two nominative singular masculine epithets",
        "affix": "su (prathamā ekavacana) on both epithets", "root": None,
        "grammar": "Two coordinated epithets counted together in this enumeration: 'Saṅkarṣaṇa; Acyuta.'",
    },
    604: {
        "stem": "vara",
        "parts": [
            {"form_iast": "śrīmat", "gloss": "possessing splendour or prosperity", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: among those endowed with śrī", "kind": "ending"},
            {"form_iast": "vara", "gloss": "best, foremost", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine head", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A partitive genitive phrase: 'the foremost among those endowed with śrī.'",
    },
    531: {
        "stem": "kapilācārya",
        "parts": [
            {"form_iast": "mahā-ṛṣi", "gloss": "great sage", "kind": "member"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "kapila-ācārya", "gloss": "the teacher Kapila", "kind": "member"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "two nominative singular masculine expressions in apposition",
        "affix": "su (prathamā ekavacana) on both appositional expressions", "root": None,
        "grammar": "Apposition: 'the great sage, the teacher Kapila.'",
    },
    732: {
        "stem": "pada",
        "parts": [
            {"form_iast": "pada", "gloss": "state, station, goal", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter head", "kind": "ending"},
            {"form_iast": "an-uttama", "gloss": "unsurpassed; with nothing higher", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter agreement", "kind": "ending"},
        ],
        "morph": "nominative singular neuter noun with agreeing adjective",
        "affix": "su (prathamā ekavacana) on both head and adjective",
        "root": None,
        "grammar": "A nominal phrase: 'the unsurpassed state'; anuttamam agrees with the neuter head padam.",
    },
    759: {
        "stem": "vara",
        "parts": [
            {"form_iast": "sarva-śastra-bhṛt", "gloss": "bearer of every weapon", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: among weapon-bearers", "kind": "ending"},
            {"form_iast": "vara", "gloss": "best, foremost", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A partitive genitive phrase: 'foremost among all who bear weapons.'",
    },
    919: {
        "stem": "vara",
        "parts": [
            {"form_iast": "kṣamin", "gloss": "patient, forbearing", "kind": "stem"},
            {"form_iast": "ām", "gloss": "genitive plural: among the forbearing", "kind": "ending"},
            {"form_iast": "vara", "gloss": "best, foremost", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "genitive plural masculine dependent + nominative singular masculine head",
        "affix": "ām (ṣaṣṭhī bahuvacana) + su (prathamā ekavacana)", "root": None,
        "grammar": "A partitive genitive phrase: 'foremost among the patient/forbearing.'",
    },
}

WORD_OVERRIDES = {
    31: {"stem": "saṃbhava", "parts": [
        {"form_iast": "saṃbhava", "gloss": "arising together; coming into being", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    35: {"stem": "prabhu", "parts": [
        {"form_iast": "prabhu", "gloss": "lord, master, one with power", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    75: {"stem": "vikramin", "parts": [
        {"form_iast": "vi-krama", "gloss": "stride; prowess", "kind": "stem"},
        {"form_iast": "in", "gloss": "possessing", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    76: {"stem": "dhanvin", "parts": [
        {"form_iast": "dhanus", "gloss": "bow", "kind": "stem"},
        {"form_iast": "in", "gloss": "possessing", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    211: {
        "stem": "dhāman",
        "parts": [
            {"form_iast": "dhāman", "gloss": "abode, domain, destination", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular neuter", "kind": "ending"},
        ],
        "root": {"form": "√dhā", "gana": "juhotyādi (3)", "pada": "ubhayapada", "gloss": "to put, place, support"},
        "affix": "manin (kṛt) + su (prathamā ekavacana)",
        "morph": "nominative singular neuter",
        "grammar": "The neuter action/result noun dhāman is formed from √dhā with manin and is used here as a nominative singular epithet.",
    },
    247: {"stem": "asaṅkhyeya", "parts": [
        {"form_iast": "a-saṅkhyeya", "gloss": "not to be numbered; innumerable", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    380: {"stem": "kartṛ", "parts": [
        {"form_iast": "√kṛ", "gloss": "to do, make", "kind": "root"},
        {"form_iast": "tṛc", "gloss": "agent-forming suffix: doer", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    385: {"stem": "vyavasthāna", "parts": [
        {"form_iast": "vy-ava-sthāna", "gloss": "standing apart; fixed arrangement or basis", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    413: {"stem": "vyāpta", "parts": [
        {"form_iast": "vi-āpta", "gloss": "pervaded; extended throughout", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    467: {"stem": "vyāpin", "parts": [
        {"form_iast": "vi-āp", "gloss": "to pervade; extend through", "kind": "root"},
        {"form_iast": "in", "gloss": "possessing or characterized by", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    581: {"stem": "śama", "parts": [
        {"form_iast": "śama", "gloss": "calm; tranquillity", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    582: {"stem": "śānta", "parts": [
        {"form_iast": "śānta", "gloss": "peaceful; stilled", "kind": "stem"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    634: {"stem": "arcita", "parts": [
        {"form_iast": "√arc", "gloss": "to praise, worship", "kind": "root"},
        {"form_iast": "kta", "gloss": "past participle: worshipped", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    660: {"stem": "dhanañjaya", "parts": [
        {"form_iast": "dhana", "gloss": "wealth", "kind": "member"},
        {"form_iast": "jaya", "gloss": "conquest; victory", "kind": "member"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    714: {"stem": "dṛpta", "parts": [
        {"form_iast": "√dṛp", "gloss": "to be proud; exult", "kind": "root"},
        {"form_iast": "kta", "gloss": "past participle", "kind": "suffix"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ]},
    728: {
        "stem": "kim",
        "parts": [{"form_iast": "ka", "gloss": "who?; the interrogative pronoun", "kind": "stem"},
                  {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"}],
        "morph": "nominative singular masculine interrogative pronoun",
        "affix": "su (prathamā ekavacana)",
    },
    729: {
        "stem": "kim",
        "parts": [{"form_iast": "kim", "gloss": "what?; the neuter interrogative pronoun", "kind": "stem"}],
        "morph": "nominative or accusative singular neuter interrogative pronoun",
        "affix": "neuter nominative/accusative singular pronominal form",
    },
    730: {
        "stem": "yad",
        "parts": [{"form_iast": "yat", "gloss": "which; what; the neuter relative pronoun", "kind": "stem"}],
        "root": None,
        "morph": "nominative or accusative singular neuter relative pronoun",
        "affix": "neuter nominative/accusative singular pronominal form",
    },
    731: {
        "stem": "tad",
        "parts": [{"form_iast": "tat", "gloss": "that; the neuter demonstrative pronoun", "kind": "stem"}],
        "morph": "nominative or accusative singular neuter demonstrative pronoun",
        "affix": "neuter nominative/accusative singular pronominal form",
    },
    940: {
        "stem": "diś",
        "parts": [
            {"form_iast": "diś", "gloss": "direction; quarter of space", "kind": "stem"},
            {"form_iast": "jas", "gloss": "nominative plural feminine", "kind": "ending"},
        ],
        "root": None,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nominative plural feminine",
        "grammar": "The plural noun diśaḥ, 'the directions,' is used as a name.",
    },
    1000: {
        "stem": "sarva-praharaṇa-āyudha",
        "parts": [
            {"form_iast": "sarva", "gloss": "all, every", "kind": "member"},
            {"form_iast": "praharaṇa", "gloss": "weapon, implement of attack", "kind": "member"},
            {"form_iast": "āyudha", "gloss": "weapon", "kind": "member"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "sandhi": "praharaṇa + āyudha appears as praharaṇāyudha by vowel sandhi.",
    },
}


def reviewed_nominal(stem: str, members: list[tuple[str, str, str]], gender: str = "masculine") -> dict:
    return {
        "stem": stem,
        "parts": [
            {"form_iast": form, "gloss": gloss, "kind": kind}
            for form, gloss, kind in members
        ] + [{"form_iast": "su", "gloss": f"nominative singular {gender}", "kind": "ending"}],
        "morph": f"nominative singular {gender}",
        "affix": "su (prathamā ekavacana)",
    }


AUDIT_WORD_OVERRIDES = {
    2: {
        **reviewed_nominal("viṣṇu", [
            ("√viś", "to enter; pervade", "root"),
            ("ṇu", "traditional uṇādi derivative suffix", "suffix"),
        ]),
        "root": {"form": "√viś", "gana": "tudādi (6)", "pada": "parasmaipada", "gloss": "to enter; pervade"},
        "affix": "ṇu (uṇādi) + su (prathamā ekavacana)",
    },
    10: reviewed_nominal("pūtātman", [("pūta", "purified", "member"), ("ātman", "self", "member")]),
    11: reviewed_nominal("paramātman", [("parama", "highest; supreme", "member"), ("ātman", "self", "member")]),
    17: reviewed_nominal("akṣara", [("a", "not", "prefix"), ("kṣara", "perishing; mutable", "stem")]),
    23: reviewed_nominal("keśava", [("keśa", "hair", "stem"), ("va", "possessing", "suffix")]),
    24: reviewed_nominal("puruṣottama", [("puruṣa", "person; spirit", "member"), ("uttama", "highest; best", "member")]),
    27: reviewed_nominal("śiva", [("śiva", "auspicious; gracious; beneficent", "stem")]),
    34: reviewed_nominal("prabhava", [("pra", "forth; forward", "prefix"), ("bhava", "origin; source; coming into being", "stem")]),
    45: reviewed_nominal("dhāturuttama", [("dhātu", "element; constituent", "member"), ("uttama", "highest; best", "member")]),
    46: reviewed_nominal("aprameya", [("a", "not", "prefix"), ("prameya", "measurable; knowable", "stem")]),
    56: reviewed_nominal("śāśvata", [("śāśvata", "eternal; constant", "stem")]),
    89: reviewed_nominal("prajābhava", [("prajā", "creatures; offspring", "member"), ("bhava", "origin; coming into being", "member")]),
    91: reviewed_nominal("saṃvatsara", [("saṃvatsara", "year; cycle of time", "stem")]),
    95: reviewed_nominal("aja", [("a", "not", "prefix"), ("ja", "born; produced", "stem")]),
    101: reviewed_nominal("vṛṣākapi", [
        ("vṛṣa", "dharma; righteousness", "member"),
        ("kapi", "the Boar; one who raises from the waters", "member"),
    ]),
    113: reviewed_nominal("vṛṣākṛti", [("vṛṣa", "dharma; righteousness", "member"), ("ākṛti", "form; shape", "member")], "feminine"),
    125: reviewed_nominal("viṣvaksena", [("viṣvak", "throughout; on every side", "member"), ("senā", "army; host", "member")]),
    134: reviewed_nominal("surādhyakṣa", [("sura", "deity", "member"), ("adhyakṣa", "overseer; presiding authority", "member")]),
    207: reviewed_nominal("viśrutātman", [("viśruta", "widely heard; renowned", "member"), ("ātman", "self", "member")]),
    213: reviewed_nominal("satya-parākrama", [("satya", "true; unfailing", "member"), ("parākrama", "heroic power; valour", "member")]),
    250: reviewed_nominal("śiṣṭakṛt", [("śiṣṭa", "disciplined; good; governed", "member"), ("kṛt", "maker; doer", "member")]),
    275: {
        **reviewed_nominal("ojas-tejas-dyuti-dhara", [("ojas", "vital strength; vigour", "member"), ("tejas", "radiance; energy", "member"), ("dyuti", "splendour; lustre", "member"), ("dhara", "bearing; possessing", "member")]),
        "sandhi": "tejas + dyuti appears as tejo-dyuti; dhara + su appears as dharaḥ.",
    },
    296: reviewed_nominal("kānta", [("kānta", "beloved; beautiful; enchanting", "stem")]),
    30: {
        "stem": "nidhi + avyaya",
        "parts": [
            {"form_iast": "nidhi", "gloss": "store; treasure", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "avyaya", "gloss": "imperishable; undecaying", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine agreement", "kind": "ending"},
        ],
        "morph": "nominative singular masculine noun with agreeing adjective",
        "affix": "su (prathamā ekavacana) on both expressions",
        "grammar": "A nominal phrase: 'the imperishable treasure.'",
    },
    217: {
        "stem": "vācaspati + udāra-dhī",
        "parts": [
            {"form_iast": "vācaspati", "gloss": "lord of speech", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
            {"form_iast": "udāra-dhī", "gloss": "having noble understanding", "kind": "stem"},
            {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
        ],
        "morph": "two nominative singular masculine epithets",
        "affix": "su (prathamā ekavacana) on both epithets",
        "grammar": "Two coordinated epithets counted together: 'lord of speech; noble-minded.'",
    },
    352: reviewed_nominal("vṛddhātman", [("vṛddha", "ancient; mature", "member"), ("ātman", "self", "member")]),
    452: reviewed_nominal("vimuktātman", [("vi-mukta", "fully liberated", "member"), ("ātman", "self", "member")]),
    482: {
        **reviewed_nominal("avijñātṛ", [("a", "not", "prefix"), ("vi", "distinctly; fully", "prefix"), ("√jñā", "to know", "root"), ("tṛc", "agent-forming suffix: knower", "suffix")]),
        "root": {"form": "√jñā", "gana": "kryādi (9)", "pada": "ubhayapada", "gloss": "to know"},
        "affix": "a- + vi- + √jñā + tṛc (kṛt) + su (prathamā ekavacana)",
    },
    555: reviewed_nominal("vṛkṣa", [("vṛkṣa", "tree", "stem")]),
    568: reviewed_nominal("khaṇḍa-paraśu", [("khaṇḍa", "broken; notched", "member"), ("paraśu", "axe", "member")]),
    595: reviewed_nominal("vṛṣa-priya", [("vṛṣa", "dharma; righteousness", "member"), ("priya", "dear; beloved", "member")]),
    618: reviewed_nominal("nandi", [("nandi", "delighting; joyful", "stem")]),
    623: reviewed_nominal("chinna-saṃśaya", [("chinna", "cut off", "member"), ("saṃśaya", "doubt; uncertainty", "member")]),
    701: {
        "stem": "sattā",
        "parts": [
            {"form_iast": "sat", "gloss": "being; existent", "kind": "stem"},
            {"form_iast": "tal", "gloss": "abstract-state suffix: -ness; state of being", "kind": "suffix"},
            {"form_iast": "su", "gloss": "nominative singular feminine", "kind": "ending"},
        ],
        "morph": "nominative singular feminine",
        "affix": "tal (taddhita) + su (prathamā ekavacana)",
    },
    751: reviewed_nominal("tri-loka-dhṛk", [("tri", "three", "member"), ("loka", "world", "member"), ("dhṛk", "bearer; supporter", "member")]),
    774: reviewed_nominal("anivṛttātman", [("a-nivṛtta", "not turned back; not withdrawn", "member"), ("ātman", "self", "member")]),
    832: {
        **reviewed_nominal("acintya", [("a", "not", "prefix"), ("√cint", "to think; consider", "root"), ("yat", "gerundive: to be conceived", "suffix")]),
        "root": {"form": "√cint", "gana": "curādi (10)", "pada": "ubhayapada", "gloss": "to think; consider"},
        "affix": "a- + √cint + yat (kṛt) + su (prathamā ekavacana)",
    },
    842: reviewed_nominal("adhṛta", [("a", "not", "prefix"), ("dhṛta", "held; supported", "stem")]),
    871: reviewed_nominal("abhiprāya", [("abhi", "towards", "prefix"), ("prāya", "aim; intention; purpose", "stem")]),
    875: reviewed_nominal("prīti-vardhana", [("prīti", "delight; affection", "member"), ("vardhana", "increasing; fostering", "member")]),
    894: reviewed_nominal("lokādhiṣṭhāna", [("loka", "world", "member"), ("adhiṣṭhāna", "basis; substratum", "member")], "neuter"),
    937: reviewed_nominal("gabhīrātman", [("gabhīra", "deep; profound", "member"), ("ātman", "self", "member")]),
    942: {
        "stem": "bhūḥ + bhuvaḥ",
        "parts": [
            {"form_iast": "bhūḥ", "gloss": "earth; the terrestrial world", "kind": "member"},
            {"form_iast": "bhuvaḥ", "gloss": "the middle world; atmosphere", "kind": "member"},
        ],
        "morph": "two fixed Vedic vyāhṛti forms used together as a name",
        "affix": "fixed Vedic forms; no additional sup ending asserted",
    },
    943: reviewed_nominal("lakṣmī", [("lakṣmī", "splendour; prosperity; good fortune", "stem")], "feminine"),
    945: reviewed_nominal("rucirāṅgada", [("rucira", "beautiful; radiant", "member"), ("aṅgada", "armlet", "member")]),
    950: reviewed_nominal("ādhāra-nilaya", [("ādhāra", "support; foundation", "member"), ("nilaya", "abode; resting-place", "member")]),
    967: {
        **reviewed_nominal("bhūr-bhuvaḥ-svas-taru", [("bhūḥ", "earth; the terrestrial world", "member"), ("bhuvaḥ", "the middle world; atmosphere", "member"), ("svaḥ", "heaven; the celestial world", "member"), ("taru", "tree", "member")]),
        "sandhi": "The three vyāhṛtis bhūḥ, bhuvaḥ, svaḥ combine before taru in the received form bhūrbhuvaḥsvastaruḥ.",
    },
    984: reviewed_nominal("annāda", [("anna", "food", "member"), ("āda", "eater", "member")]),
    993: reviewed_nominal("śaṅkha-bhṛt", [("śaṅkha", "conch", "member"), ("bhṛt", "bearer; holder", "member")]),
}

DERIVATION_OVERRIDES = {
    2: "Veveṣṭi vyāpnoti iti viṣṇuḥ: 'that which pervades everywhere is Viṣṇu.' Chinmayananda connects the name with the root viś, 'to enter, to pervade.'",
    5: "Bhūtāni karoti iti bhūta-kṛt: 'the maker of beings'; or bhūtāni kṛntati iti bhūta-kṛt: 'the destroyer of beings.' Chinmayananda explicitly gives both dissolutions.",
    101: "Chinmayananda cites kapi in the operative sense 'the Boar' and vṛṣa as dharma. His resulting interpretation is the Boar who raises the world from adharma into dharma; the longer commentary preserves the traditional lexical dispute rather than placing it in the translation slot.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_packet(path: Path) -> dict:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(path.read_text(encoding="utf-8"))


def key(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value).lower())
    return "".join(char for char in value if char.isalpha())


def english_tokens(value: str) -> set[str]:
    tokens = set()
    for token in re.findall(r"[a-z]{4,}", value.lower()):
        if token in STOPWORDS:
            continue
        token = re.sub(r"(?:ing|ers?|ed|es|s)$", "", token)
        tokens.add(token)
    return tokens


def clean_snippet(snippet: str) -> str:
    text = snippet.split("¦", 1)[-1].strip()
    text = re.sub(r"^(?:mfn|mf\([^)]*\)n|m|f|n)\.\s*", "", text)
    text = re.sub(r"^only ifc\.\s*", "", text)
    if text.startswith("(") and ") " in text:
        text = text.split(") ", 1)[1]
    text = re.sub(r"\b(?:RV|MBh|BhP|Up|AV|TS|VS)\.[^.;]*", "", text)
    text = re.sub(r"\s+", " ", text).strip(" ;,.")
    for separator in (";", "."):
        if separator in text and len(text.split(separator, 1)[0]) >= 8:
            text = text.split(separator, 1)[0]
            break
    return text[:180].strip()


def usable_gloss(gloss: str) -> bool:
    if not gloss or len(gloss) < 3:
        return False
    blocked = (
        "N. of", "See under", "See below", "See p.", "in comp. for", "for 1.",
        "cl. ", "Dhātup.", "an affix", "the first labial", "ind. (",
    )
    if any(fragment.lower() in gloss.lower() for fragment in blocked):
        return False
    if gloss.count("˚") or gloss.count("/") > 1:
        return False
    return True


def concise_traditional_gloss(value: str) -> str:
    text = re.sub(r"^[\s—–\-'\"“”]+|[\s'\"“”]+$", "", value)
    text = re.sub(r"\s+", " ", text)
    for marker in (". ", "; ", "—", " – "):
        if marker in text and len(text.split(marker, 1)[0]) >= 8:
            text = text.split(marker, 1)[0]
            break
    return text[:160].rstrip(" .;:")


def current_derivation_sentences(commentary: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", commentary))
    return [
        sentence.strip()
        for sentence in sentences
        if re.search(r"\b(root|derived|derivation|dissolved|means?|etymolog|pāṇini|panini)\b", sentence, re.I)
    ]


def mw_records(row: dict) -> list[dict]:
    return [record for records in row.get("mw_exact", {}).values() for record in records]


def choose_mw_gloss(row: dict, fallback: str, preferred_iast: str | None = None, gender_code: str | None = None) -> tuple[str, dict | None]:
    records = mw_records(row)
    if preferred_iast:
        preferred_slp1 = transliterate(preferred_iast, sanscript.IAST, sanscript.SLP1)
        preferred = [record for record in records if record.get("k1") == preferred_slp1]
        if preferred:
            records = preferred
    expected_tag = {"puM": "m", "strI": "f", "napuMsaka": "n"}.get(gender_code or "")
    if expected_tag:
        exact_gender = [record for record in records if expected_tag in record.get("gender_tags", []) or f"{expected_tag}." in record.get("gender_tags", [])]
        if exact_gender:
            records = exact_gender
    if not records:
        return fallback, None
    target = english_tokens(row["chinmayananda"]["short_meaning"])
    ranked = []
    for record in records:
        gloss = clean_snippet(record.get("snippet", ""))
        if not usable_gloss(gloss):
            continue
        overlap = len(target & english_tokens(gloss))
        ranked.append((overlap, -len(gloss), gloss, record))
    if not ranked:
        return concise_traditional_gloss(fallback), None
    best_overlap = max(item[0] for item in ranked)
    if best_overlap == 0:
        return concise_traditional_gloss(fallback), None
    first_gloss = clean_snippet(records[0].get("snippet", ""))
    first_overlap = len(target & english_tokens(first_gloss))
    if best_overlap - first_overlap <= 1 and first_gloss:
        return first_gloss, records[0]
    _score, _length, gloss, record = max(ranked, key=lambda item: (item[0], item[1]))
    return gloss, record


def expected_gender(row: dict) -> str:
    number = row["number"]
    if number in EXPECTED_GENDER:
        return EXPECTED_GENDER[number]
    citation = row["citation_candidate_iast"]
    if citation.endswith(("am", "aṃ", "ṃ")):
        return "napuMsaka"
    return "puM"


def citation_base(citation: str) -> str:
    head = citation.split()[-1]
    if head.endswith("ḥ"):
        return head[:-1]
    if head.endswith("am"):
        return head[:-1]
    return head


def score_candidate(row: dict, candidate: dict) -> tuple[int, int, int, str]:
    score = 0
    expected = expected_gender(row)
    if candidate.get("linga") == expected:
        score += 8
    if candidate.get("vibhakti") == "praTamA":
        score += 5
    if candidate.get("vacana") == ("bahu" if row["number"] == 929 else "eka"):
        score += 4
    lemma = candidate.get("lemma_slp1", "")
    lemma_iast = candidate.get("lemma_iast", "")
    if key(lemma_iast) == key(citation_base(row["citation_candidate_iast"])):
        score += 10
    if lemma in row.get("mw_exact", {}):
        score += 4
    derivation = " ".join(row["chinmayananda"].get("derivation_sentences", []))
    if candidate.get("pratipadika_kind") == "krdanta" and candidate.get("dhatu"):
        score += 2
        if re.search(r"\b(root|derived|dissolved)\b", derivation, re.I):
            score += 3
    if candidate.get("dhatu", {}).get("artha_en"):
        score += len(english_tokens(candidate["dhatu"]["artha_en"]) & english_tokens(derivation)) * 2
    return score, int(candidate.get("pratipadika_kind") == "krdanta"), -len(lemma), lemma


def select_candidate(row: dict, candidates: list[dict] | None = None) -> tuple[dict | None, list[dict]]:
    candidates = list(candidates if candidates is not None else row.get("vidyut_candidates", []))
    if not candidates:
        return None, []
    ranked = sorted(candidates, key=lambda c: score_candidate(row, c), reverse=True)
    best_score = score_candidate(row, ranked[0])[0]
    ties = [candidate for candidate in ranked if score_candidate(row, candidate)[0] == best_score]
    return ranked[0], ties


def stem_from(row: dict, selected: dict | None) -> str:
    citation = row["citation_candidate_iast"].split()[-1]
    if selected and selected.get("pratipadika_kind") == "basic":
        return selected.get("lemma_iast") or citation
    for slp1 in row.get("mw_exact", {}):
        iast = transliterate(slp1, sanscript.SLP1, sanscript.IAST)
        if key(iast) in key(citation) or key(citation).startswith(key(iast)):
            return iast
    if citation.endswith("ḥ"):
        return citation[:-1]
    if citation.endswith("am"):
        return citation[:-1]
    return citation


def member_gloss(member: str, row: dict) -> str:
    normalized = member.strip("- ")
    if normalized in MEMBER_LEXICON:
        return MEMBER_LEXICON[normalized]
    target = key(normalized)
    records = []
    for exact_records in row.get("mw_exact", {}).values():
        records.extend(record for record in exact_records if key(transliterate(record.get("k1", ""), sanscript.SLP1, sanscript.IAST)) == target)
    slp1 = transliterate(normalized, sanscript.IAST, sanscript.SLP1)
    records.extend(MW_INDEX.get(slp1, []))
    context = english_tokens(row["chinmayananda"]["short_meaning"] + " " + " ".join(row["chinmayananda"].get("derivation_sentences", [])))
    ranked = []
    for index, record in enumerate(records):
        gloss = clean_snippet(record.get("snippet", ""))
        if not usable_gloss(gloss):
            continue
        overlap = len(context & english_tokens(gloss))
        ranked.append((overlap, -index, -len(gloss), gloss))
    if ranked:
        return max(ranked)[3][:100]
    derivation = " ".join(row["chinmayananda"].get("derivation_sentences", []))
    pattern = re.search(rf"\b{re.escape(normalized)}\b[^.;:]{{0,30}}(?:means?|=)\s*[‘'\"]?([^.;,'\"]+)", derivation, re.I)
    if pattern:
        return pattern.group(1).strip()[:100]
    return f"[unresolved lexical member: {normalized}]"


def build_mw_index(path: Path, packet: dict) -> None:
    wanted = set()
    for row in packet["rows"]:
        citation = CITATION_CORRECTIONS.get(row["number"], row["citation_candidate_iast"])
        for part in re.split(r"[-\s]+", citation):
            if part:
                wanted.add(transliterate(part, sanscript.IAST, sanscript.SLP1))
        for record in mw_records(row):
            for part in record.get("k2", "").split("—"):
                part = part.replace("/", "")
                if part:
                    wanted.add(part)
    current = None
    buffer = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("<L>"):
            match = re.search(r"<L>([^<]+).*?<k1>([^<]+)<k2>([^<]+)", line)
            current = match.groups() if match and match.group(2) in wanted else None
            buffer = [line] if current else []
        elif current:
            buffer.append(line)
            if line == "<LEND>":
                L, k1, k2 = current
                body = " ".join(buffer[1:-1])
                body = re.sub(r"<[^>]+>", "", body)
                MW_INDEX.setdefault(k1, []).append({"L": L, "k1": k1, "k2": k2, "gender_tags": [], "snippet": body})
                current = None
                buffer = []


def split_members(citation: str, row: dict, stem: str) -> list[str]:
    if " " in citation:
        return citation.split()
    for record in mw_records(row):
        k2 = record.get("k2", "")
        if "—" in k2:
            members = [transliterate(part.replace("/", ""), sanscript.SLP1, sanscript.IAST) for part in k2.split("—")]
            if len(members) > 1:
                return members
    if "-" in citation:
        return [part for part in citation.split("-") if part]
    return [stem]


def analysis_for(row: dict) -> dict:
    row = dict(row)
    row["citation_candidate_iast"] = CITATION_CORRECTIONS.get(row["number"], row["citation_candidate_iast"])
    citation = unicodedata.normalize("NFC", row["citation_candidate_iast"])
    selected, ties = select_candidate(row)
    stem = stem_from(row, selected)
    gender_code = selected.get("linga") if selected else expected_gender(row)
    gloss, mw_record = choose_mw_gloss(row, row["chinmayananda"]["short_meaning"], stem, gender_code)
    case_code = selected.get("vibhakti", "praTamA") if selected else "praTamA"
    number_code = selected.get("vacana", "eka") if selected else ("bahu" if row["number"] == 929 else "eka")
    members = split_members(citation, row, stem)
    member_corrections = MEMBER_FORM_CORRECTIONS.get(row["number"], {})
    members = [member_corrections.get(member, member) for member in members]
    parts = [
        {
            "form_iast": member,
            "gloss": member_gloss(member, row) if len(members) > 1 else MEMBER_LEXICON.get(member, gloss),
            "kind": "member" if len(members) > 1 else "stem",
        }
        for member in members
    ]
    for part in parts:
        if part["kind"] != "ending" and part["form_iast"] in PART_GLOSS_OVERRIDES.get(row["number"], {}):
            part["gloss"] = PART_GLOSS_OVERRIDES[row["number"]][part["form_iast"]]
    parts.append({"form_iast": "su" if number_code == "eka" else "jas", "gloss": f"marks nominative {NUMBER_LABEL.get(number_code, number_code)}", "kind": "ending"})

    # A lexical candidate is not by itself authority to choose one historical
    # derivation among homonymous dhātus. Formal roots are therefore supplied
    # only by the reviewed override table (and reviewed phrase analyses below).
    root = None
    affix = "su (prathamā ekavacana)" if number_code == "eka" else "jas (prathamā bahuvacana)"
    compound = None
    if row["number"] in COMPOUND_OVERRIDES:
        ctype, vigraha = COMPOUND_OVERRIDES[row["number"]]
        compound = {"type": ctype, "vigraha": vigraha, "members": members}

    derivation_sentences = [
        re.sub(r"[*†‡]+", "", sentence).strip()
        for sentence in row["chinmayananda"].get("derivation_sentences", [])
        if sentence.strip()
    ]
    derivation = DERIVATION_OVERRIDES.get(row["number"]) or (" ".join(derivation_sentences)[:700] or None)
    if derivation and key(derivation) == key(row["chinmayananda"]["short_meaning"]):
        derivation = None
    uncertainty = []
    if len(ties) > 1:
        uncertainty.append("Vidyut admits multiple equally ranked analyses; this row selects the reading that matches the stanza and Chinmayananda context.")
    if selected is None:
        uncertainty.append("Vidyut has no exact lexicalized entry for the full name; the prātipadika and members are retained from the received text and Monier-Williams evidence.")
    if len(members) > 1 and compound is None:
        uncertainty.append("Members are shown without asserting a samāsa type not secured by the consulted evidence.")
    surface = row["received"]["surface_iast"]
    sandhi = "No surface change beyond word-boundary punctuation."
    if key(surface) != key(citation):
        sandhi = f"The citation form {citation} occurs in the received stanza as {surface}; the displayed difference is external sandhi."

    evidence = {
        "vidyut": None if selected is None else {
            "query_slp1": selected.get("query_slp1"), "lemma_slp1": selected.get("lemma_slp1"),
            "kind": selected.get("pratipadika_kind"), "candidate_count_at_best_score": len(ties),
        },
        "mw": None if mw_record is None else {"L": mw_record.get("L"), "k1": mw_record.get("k1"), "k2": mw_record.get("k2")},
        "chinmayananda_scan_pages": row["chinmayananda"]["scan_pages"],
    }
    result = {
        "number": row["number"],
        "citation_iast": citation,
        "citation_devanagari": transliterate(citation, sanscript.IAST, sanscript.DEVANAGARI),
        "whole_gloss": row["chinmayananda"]["short_meaning"],
        "parts": parts,
        "stem": stem,
        "root": root,
        "affix": affix,
        "morph": f"{CASE_LABEL.get(case_code, case_code)} {NUMBER_LABEL.get(number_code, number_code)} {GENDER_LABEL.get(gender_code, gender_code)}",
        "compound": compound,
        "sandhi": sandhi,
        "derivation": derivation,
        "grammar": f"The name is used as a {CASE_LABEL.get(case_code, case_code)} {NUMBER_LABEL.get(number_code, number_code)} expression; its head is {stem}.",
        "source_basis": "Chinmayananda + Vidyut + Monier-Williams" if selected else "Chinmayananda + received text + Monier-Williams",
        "status": "source-adjudicated",
        "uncertainty": uncertainty,
        "evidence": evidence,
    }
    if row["number"] in ROOT_OVERRIDES:
        result["root"], result["affix"] = ROOT_OVERRIDES[row["number"]]
    if row["number"] in PHRASE_OVERRIDES:
        override = PHRASE_OVERRIDES[row["number"]]
        for field in ("stem", "parts", "morph", "affix", "root", "grammar"):
            result[field] = override[field]
    if row["number"] in WORD_OVERRIDES:
        result.update(WORD_OVERRIDES[row["number"]])
    if row["number"] in AUDIT_WORD_OVERRIDES:
        result.update(AUDIT_WORD_OVERRIDES[row["number"]])
    return result


def validate(data: dict) -> dict:
    rows = data.get("names", [])
    errors = []
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        errors.append("analysis population is not exactly 1–1000")
    for row in rows:
        number = row.get("number")
        for field in ("citation_iast", "citation_devanagari", "whole_gloss", "parts", "stem", "affix", "morph", "sandhi", "grammar", "source_basis", "status", "uncertainty", "evidence"):
            if field not in row or row[field] in (None, ""):
                errors.append(f"name {number} lacks {field}")
        parts = row.get("parts", [])
        if not parts or any(not all(part.get(key) for key in ("form_iast", "gloss", "kind")) for part in parts):
            errors.append(f"name {number} has incomplete parts")
        if any("[unresolved lexical member:" in part.get("gloss", "") for part in parts):
            errors.append(f"name {number} has an unresolved lexical member")
        old_member_forms = set(MEMBER_FORM_CORRECTIONS.get(number, {}))
        if old_member_forms & {part.get("form_iast") for part in parts}:
            errors.append(f"name {number} retains an inflected or sandhied member as a prātipadika")
        if len(parts) == 1 and key(parts[0].get("gloss", "")) == key(row.get("whole_gloss", "")):
            errors.append(f"name {number} card only repeats its translation")
        root = row.get("root")
        if root is not None and not all(root.get(field) for field in ("form", "gana", "pada", "gloss")):
            errors.append(f"name {number} has incomplete root evidence")
        compound = row.get("compound")
        if compound is not None and not all(compound.get(field) for field in ("type", "vigraha", "members")):
            errors.append(f"name {number} has incomplete compound evidence")
        if row.get("derivation") and key(row["derivation"]) == key(row.get("whole_gloss", "")):
            errors.append(f"name {number} derivation repeats the translation")
        if number in TRANSLATION_CARD_AUDIT:
            lexical = " ".join(part.get("gloss", "") for part in parts if part.get("kind") != "ending")
            lexical_key = key(lexical)
            whole_key = key(row.get("whole_gloss", ""))
            if lexical_key == whole_key or (len(lexical_key) > 20 and (lexical_key.startswith(whole_key) or whole_key.startswith(lexical_key))):
                errors.append(f"name {number} card still repeats its reading-line translation")
        if not re.search(r"[\u0900-\u097f]", row.get("citation_devanagari", "")):
            errors.append(f"name {number} lacks Devanāgarī")
    if errors:
        raise ValueError("\n".join(errors[:100]))
    return {
        "names": len(rows),
        "with_roots": sum(row.get("root") is not None for row in rows),
        "with_members": sum(len(row.get("parts", [])) > 2 for row in rows),
        "with_compound_type": sum(row.get("compound") is not None for row in rows),
        "with_chinmayananda_derivation": sum(row.get("derivation") is not None for row in rows),
        "with_uncertainty": sum(bool(row.get("uncertainty")) for row in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--mw", type=Path, default=DEFAULT_MW)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.check:
        print(json.dumps(validate(json.loads(args.check.read_text())), indent=2))
        return
    if sha256(args.packet) != PACKET_FILE_SHA256:
        raise ValueError("prejoin packet checksum mismatch")
    packet = load_packet(args.packet)
    if packet.get("canonical_payload_sha256") != PACKET_PAYLOAD_SHA256:
        raise ValueError("prejoin canonical payload checksum mismatch")
    if sha256(args.mw) != MW_SHA256:
        raise ValueError("Monier-Williams source checksum mismatch")
    current_commentary = json.loads(COMMENTARY_PATH.read_text(encoding="utf-8"))["names"]
    if [row.get("number") for row in current_commentary] != list(range(1, 1001)):
        raise ValueError("current Chinmayananda transcription is not exactly names 1-1000")
    for packet_row, source_row in zip(packet["rows"], current_commentary):
        packet_row["chinmayananda"]["short_meaning"] = source_row["short_meaning"]
        packet_row["chinmayananda"]["scan_pages"] = source_row["scan_pages"]
        packet_row["chinmayananda"]["derivation_sentences"] = current_derivation_sentences(source_row["commentary"])
    build_mw_index(args.mw, packet)
    sources = json.loads(json.dumps(packet["sources"]))
    sources["received_reader"] = {
        "path": "gita/vishnu-sahasranama/reader.json",
        "prejoin_snapshot_sha256": sources["received_reader"]["sha256"],
    }
    sources["bori"]["path"] = "data/sources/sanskrit/vedanta/vishnu_sahasranama_bori_critical_excerpt.txt"
    sources["monier_williams"].pop("path", None)
    sources["vidyut"].pop("data_path", None)
    sources["chinmayananda"] = {
        "path": str(COMMENTARY_PATH.relative_to(ROOT)),
        "sha256": sha256(COMMENTARY_PATH),
        "editorial_scan_corrections": [2, 5],
    }
    output = {
        "schema_version": 1,
        "sources": sources,
        "prejoin_payload_sha256": PACKET_PAYLOAD_SHA256,
        "names": [analysis_for(row) for row in packet["rows"]],
    }
    report = validate(output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
