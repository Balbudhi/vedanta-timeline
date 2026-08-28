#!/usr/bin/env python3
"""Build the verified Gītā-quotation registry for Chinmayananda's reader.

The printed scan remains the authority for what Chinmayananda quoted and how he
translated it.  The local BORI mūla is the comparison witness used to repair
OCR script and identify misprinted or recension-shifted loci.  A historical
Sūtrakṛt packet is retained only as a quarantined disagreement aid; it cannot
approve a token or enter the public payload. Public analysis is independently
derived from the BORI context and traditional grammar.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import hashlib
import json
import re
import unicodedata
import urllib.request
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
GITA_PATH = ROOT / "data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt"
ANALYSIS_PACKET_PATH = ROOT / "data/sources/sanskrit/vedanta/bhagavadgita_sutrakrit_word_analysis.json"
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/commentary-quotes.json"
SUTRAKRIT_URL = "https://gita.ekrasworks.com/api/v1/verse/{chapter}/{verse}"

ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
    "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17,
    "XVIII": 18,
}
REF_RE = re.compile(
    r"Gītā(?:\s*(?:Ch(?:apter)?\.?))?[\s,.:—–-]*"
    r"(XVIII|XVII|XVI|XIV|XIII|XII|XI|XV|VIII|VII|VI|IV|III|II|IX|X|V|I|\d{1,2})"
    r"[\s,.:—–-]*(?:St(?:anza)?\.?)?[\s,.:—–-]*(\d{1,2})",
    re.I,
)
DEVA_RE = re.compile(r"[\u0900-\u097f][\u0900-\u097f\u200c\u200d\s।॥,;:…\-–—()]+")
GITA_LINE_RE = re.compile(r"(.+?)\s+Bhg_(\d{2})\.(\d{3})([ac])\b")
ENGLISH_HINTS = {
    "a", "all", "am", "and", "are", "as", "be", "being", "but", "by", "can",
    "does", "for", "from", "has", "have", "he", "him", "his", "i", "in", "is",
    "it", "me", "my", "no", "not", "of", "one", "or", "shall", "that", "the",
    "their", "them", "there", "they", "this", "those", "to", "was", "which",
    "who", "will", "with", "you", "your",
}

# Only translations stated in this Sahasranāma commentary belong here.  The
# Gītā API's translations and the site's own literal renderings are never
# substituted for Chinmayananda's words.  Absence means that the printed entry
# gives no separable English translation for that quoted fragment.
TRANSLATION_OVERRIDES = {
    "name-129-paragraph-0-span-0": "This great Reality is Imperceptible, Unthinkable, without any modifications",
    "name-12-paragraph-1-span-0": "There where having gone, men never return. That sacred place is My seat",
    "name-12-paragraph-2-span-0": "O Son of Kunti, having reached Me, there shall be no more any re-birth",
    "name-12-paragraph-2-span-1": "That having reached no return again",
    "name-19-paragraph-1-span-0": "Those who contemplate upon Me with total dedication, their daily welfare and spiritual progress I shall bear",
    "name-28-paragraph-1-span-0": "Eternal, All — Pervading, the Pillar, Motionless (is) this Ancient One",
    "name-81-paragraph-0-span-0": "Rasopyasya Param Drishtvaa Nivartate",
    "name-95-paragraph-0-span-0": "That which is born must necessarily die",
    "name-107-paragraph-1-span-1": "I am the Seer in all the fields-of-experiences everywhere",
    "name-114-paragraph-0-span-3": "Among the Rudras, I am Śaṅkara",
    "name-118-paragraph-0-span-0": "Everywhere are His ears",
    "name-124-paragraph-0-span-0": "The Light that illumines all lights",
    "name-133-paragraph-1-span-0": "The Supreme puruṣa in this body is also called the spectator, the permitter, the supporter, the enjoyer, the great Lord, and the Supreme Self",
    "name-147-paragraph-1-span-0": "Among the Pandavas, I am Arjuna",
    "name-170-paragraph-2-span-0": "Very difficult indeed it is to cross over My māyā",
    "name-189-paragraph-0-span-0": "I am the Light in all effulgents",
    "name-193-paragraph-0-span-0": "Among the serpents I am Ananta",
    "name-200-paragraph-1-span-0": "Among the animals, I am the King of animals, Lion",
    "name-228-paragraph-1-span-0": "O Arjuna, the Lord dwells in the heart of all, and spins. through His māyā, all layers of personal ties as though the universe is a complicated machinery",
    "name-232-paragraph-1-span-0": "Please understand that I am the Light of the Sun that illumines all earth; and the light and heat in the moon and fire are all mine only",
    "name-236-paragraph-1-span-0": "With a little am I satisfied. if it is given with sincerity, and with faithful consistency",
    "name-263-paragraph-1-span-0": "They are in me; I am not in them",
    "name-275-paragraph-2-span-0-piece-0": "I am the Might in all strength",
    "name-275-paragraph-2-span-0-piece-1": "I am the Brilliancy in all that is brilliant",
    "name-279-paragraph-1-span-0": "One who chants my name Om and leaves his body at the time of death thus remembering Me, he shall go to the Supreme State",
    "name-281-paragraph-1-span-0": "As the rays of the moon (Soma) I fill the vegetable kingdom with nutrition",
    "name-285-paragraph-1-span-0": "that nourishes with essence all plant kingdom",
    "name-384-paragraph-2-span-0": "The intellect of one who is practising Yoga is single-pointed without vacillation",
    "name-384-paragraph-3-span-0": "Those who are revelling in sensuality and consequently disturbing the poise of their intellect, cannot have a steady mind and consistent pursuit of Yoga",
    "name-391-paragraph-2-span-0": "I accept even if you offer some leaf or flower, or fruit or spoon of water, happily, if it is offered in love",
    "name-418-paragraph-2-span-0": "I am the Time of counting",
    "name-436-paragraph-1-span-0": "This space between earth and the heavens and all the quarters are filled by You alone",
    "name-439-paragraph-1-span-0": "offer is Brahman, what is offered is Brahman, the fire is Brahman, the offerer is Brahman and the goal reached is also Brahman",
    "name-441-paragraph-1-span-0": "among the stars I am the moon",
    "name-475-paragraph-1-span-0": "In every cycle I shall manifest for re-establishing dharma",
    "name-479-paragraph-1-span-0": "Arjuna, I am at once immortality and mortality; I am both Existence and Non-existence",
    "name-481-paragraph-1-span-0": "all creatures together constitute the kṣara-purusha and the Changeless in all creatures is the A-kshara-purusha",
    "name-517-paragraph-1-span-0": "Of the lakes I am the ocean",
    "name-554-paragraph-1-span-0": "understand them all as coming out of my glory",
    "name-576-paragraph-1-span-0": "Of Vedas I am the sāma Veda",
    "name-585-paragraph-1-span-0": "To which having gone they return not; that is My Supreme Abode",
    "name-599-paragraph-1-span-0": "I shall govern both your 'Yoga' and 'kṣema' when you are a true devotee",
    "name-623-paragraph-1-span-0": "I am firm; my doubts are gone. I will do according to your word",
    "name-632-paragraph-1-span-0": "To them I shall be, err long, a Saviour from the Ocean of Samsar",
    "name-657-paragraph-1-span-0": "By Thee alone is filled the earth, the outer space and the inner space. It is Thee who fills all directions everywhere",
    "name-660-paragraph-1-span-0": "I am Dhananjaya, among the sons of Pandu",
    "name-673-paragraph-4-span-0": "The Supreme is the Light of all lights, beyond all darkness",
    "name-673-paragraph-5-span-0": "Understand that Light in the Sun by which the whole world is illumined, and that Light in the Moon and in the fire to be My own Light",
    "name-677-paragraph-1-span-0": "I am among the yajñas, the Japa-yajña",
    "name-678-paragraph-1-span-0": "We offer to Brahman that which is Brahman, in the fire which is Brahman, and the act of offering is also Brahman",
    "name-683-paragraph-1-span-0": "He is the one dear to Me",
    "name-695-paragraph-3-span-0": "The Lord dwells in the hearts of all beings, O Arjuna, causing all beings, by His illusive power, to revolve as if mounted on a machine",
    "name-696-paragraph-2-span-0": "I am the beginning, the middle and also the end of all beings",
    "name-698-paragraph-1-span-0": "the oblations are nothing but Brahman",
    "name-706-paragraph-1-span-0": "My devotee thus knowing (realising the Truth, the jneyam, seated in the heart of all) enters into My Being",
    "name-708-paragraph-2-span-0": "I am the Source of all Creation",
    "name-711-paragraph-1-span-0": "Of My Divine Glories there is no end",
    "name-715-paragraph-2-span-0": "Greater is their trouble whose minds are set on the Unmanifest; for the goal, the Unmanifested, is very hard for the embodied to reach",
    "name-719-paragraph-1-span-0": "If the splendour of a thousand Suns were to blaze out at once in the sky, that would be like the splendour of that Mighty Being",
    "name-724-paragraph-1-span-0": "Hands and feet everywhere, with heads and mouths everywhere, His ears everywhere, stands (The Lord), enveloping all",
    "name-731-paragraph-1-span-0": "'Om Tat Sat' this has been declared to be the triple designation of Brahman",
    "name-732-paragraph-1-span-0": "The Unequalled State of Perfection: The Supreme State of Truth",
    "name-742-paragraph-3-span-0": "None there exists who is equal to You; how can there be then another superior to You in the three worlds, O Being of unequalled power",
    "name-771-paragraph-1-span-0": "I am verily that which has to be known in all the Vedas: I am indeed the author of the Vedas and the 'knower' of the Vedas am I",
    "name-772-paragraph-1-span-0": "The whole universe is supported by one part of Myself",
    "name-780-paragraph-2-span-0": "This Yoga of equanimity, taught by Thee, O slayer of Madhu, I see not its enduring continuity, because of the restlessness (of the mind)",
    "name-780-paragraph-3-span-0": "As a lamp placed in a windless place does not flicker",
    "name-789-paragraph-1-span-0": "I am the author of all the Vedas; I alone am the knower of the Veda",
    "name-801-paragraph-1-span-0": "He attains Peace into whom all desires enter as waters enter the ocean, which filled from all sides, remains unmoved; but not the 'desirer-of-desires'",
    "name-804-paragraph-1-span-0": "My māyā (non-apprehension and the consequent misapprehension) is very difficult to cross over",
    "name-817-paragraph-1-span-0": "I am easily attainable by that ever-steadfast Yogi who constantly remembers Me daily, not thinking of anything else, O Partha",
    "name-832-paragraph-1-span-0": "Nourisher of All",
    "name-835-paragraph-1-span-0": "I am seated in the heart of all—as the core or Essence in all",
    "name-859-paragraph-1-span-0": "Among punishers I am the Sceptre",
    "name-877-paragraph-1-span-0": "The Light of all lights",
    "name-892-paragraph-1-span-0": "There is neither anything that I have not gained nor anything I have yet to gain",
    "name-898-paragraph-1-span-0": "I am Kapila among the great ones",
    "name-915-paragraph-2-span-0": "Wherever, there is any special glory in anyone. know that to be a manifestation of a part of my Splendour",
    "name-928-paragraph-1-span-0": "For the protection of the good, the destruction of the wicked and the establishment of righteousness, He takes different Incarnations",
    "name-930-paragraph-1-span-0": "Permeating the earth I support all beings by (My) energy; and having become the juicy Moon I nourish all herbs",
    "name-946-paragraph-1-span-0": "Thou art the Father of the world, movable and immovable",
    "name-948-paragraph-1-span-0": "Oh, Glorious Sir, seeing your wonderful but awesome form, the whole world is shuddering with fear",
    "name-948-paragraph-2-span-0": "Having seen Thy Immeasurable Form… the worlds are terrified, and so am I",
    "name-948-paragraph-3-span-0": "On seeing Thee touching the sky… my heart is stricken with dread and I find no courage nor peace, O Viṣṇu",
    "name-966-paragraph-1-span-0": "He is not born, nor does He ever die; after having been He again ceases not to be; unborn, eternal, changeless and ancient he is not killed when the body is killed",
    "name-972-paragraph-1-span-0": "The 'Enjoyer' and the 'Lord' in all yajñas am I",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commentary_quote_source_sha256(commentary: dict) -> str:
    """Hash only numbered Full commentary, not the separate Simplified layer."""
    rows = [
        {"number": row["number"], "commentary": row["commentary"]}
        for row in commentary.get("names", [])
    ]
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compact_key(text: str) -> str:
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", text.lower())


def english_key(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def locus_text(locus: tuple[int, int]) -> str:
    return f"Gītā {locus[0]}.{locus[1]}"


def parse_locus(match: re.Match[str]) -> tuple[int, int]:
    chapter_text = match.group(1)
    chapter = int(chapter_text) if chapter_text.isdigit() else ROMAN[chapter_text.upper()]
    return chapter, int(match.group(2))


def load_gita() -> dict[tuple[int, int], str]:
    verses: dict[tuple[int, int], list[str]] = {}
    for line in GITA_PATH.read_text(encoding="utf-8").splitlines():
        match = GITA_LINE_RE.match(line)
        if match:
            locus = int(match.group(2)), int(match.group(3))
            verses.setdefault(locus, []).append(match.group(1).strip())
    result = {locus: " ".join(lines) for locus, lines in verses.items()}
    if len(result) != 700:
        raise ValueError(f"expected 700 Gītā verses, found {len(result)}")
    return result


def similarity(left: str, right: str) -> float:
    return difflib.SequenceMatcher(None, compact_key(left), compact_key(right), autojunk=False).ratio()


def best_window(query: str, verse: str) -> tuple[float, str]:
    words = verse.split()
    query_length = max(1, len(compact_key(query)))
    best = (0.0, 0.0, "")
    for start in range(len(words)):
        for end in range(start + 1, len(words) + 1):
            candidate = " ".join(words[start:end])
            candidate_length = len(compact_key(candidate))
            length_ratio = min(query_length, candidate_length) / max(query_length, candidate_length)
            if candidate_length > query_length * 1.45:
                break
            if length_ratio < 0.60:
                continue
            raw_score = similarity(query, candidate)
            objective = raw_score * (length_ratio ** 0.5)
            best = max(best, (objective, raw_score, candidate))
    return best[1], best[2]


def choose_match(
    printed_iast: str,
    printed_loci: list[tuple[int, int]],
    gita: dict[tuple[int, int], str],
) -> tuple[float, tuple[int, int], str] | None:
    stated = max(
        ((best_window(printed_iast, gita.get(locus, ""))[0], locus,
          best_window(printed_iast, gita.get(locus, ""))[1]) for locus in printed_loci),
        default=(0.0, (0, 0), ""),
    )
    best = stated
    if stated[0] < 0.78:
        best = max((best_window(printed_iast, verse)[0], locus, best_window(printed_iast, verse)[1])
                   for locus, verse in gita.items())
    if best[0] < 0.80:
        return None
    if best[1] not in printed_loci and len(compact_key(printed_iast)) < 15:
        return None
    return best


def english_quotes(paragraph: str) -> list[tuple[int, int, str]]:
    found = []
    for match in re.finditer(r'[“"]([^”"\n]{8,500})[”"]', paragraph):
        value = match.group(1).strip()
        if re.search(r"[\u0900-\u097f]", value):
            continue
        tokens = re.findall(r"[A-Za-z]+", value.lower())
        if len(tokens) < 2:
            continue
        hint_count = sum(token in ENGLISH_HINTS for token in tokens)
        if hint_count < 1 and not re.search(r"\b(?:Lord|Self|Supreme|Truth|Light|Peace|Form|Consciousness)\b", value):
            continue
        found.append((match.start(1), match.end(1), value))
    return found


def chinmayananda_translation(paragraphs: list[str], paragraph_index: int, source_start: int, source_end: int) -> str | None:
    paragraph = paragraphs[paragraph_index]
    candidates: list[tuple[float, str]] = []
    for start, end, value in english_quotes(paragraph):
        if start >= source_end:
            score = 1000 - (start - source_end)
        elif end <= source_start:
            score = 900 - (source_start - end)
        else:
            continue
        candidates.append((score, value))
    if candidates:
        return max(candidates)[1]

    if paragraph_index > 0:
        previous = paragraphs[paragraph_index - 1]
        previous_quotes = english_quotes(previous)
        if "Gītā" in previous and previous_quotes:
            return previous_quotes[-1][2]
    if paragraph_index + 1 < len(paragraphs):
        following = paragraphs[paragraph_index + 1]
        following_quotes = english_quotes(following)
        if following_quotes and following_quotes[0][0] < 40:
            return following_quotes[0][2]
    return None


def build_quotes(commentary: dict, gita: dict[tuple[int, int], str]) -> list[dict]:
    quotes = []
    for row in commentary["names"]:
        paragraphs = row["commentary"].split("\n\n")
        for paragraph_index, paragraph in enumerate(paragraphs):
            printed_loci = [parse_locus(match) for match in REF_RE.finditer(paragraph)]
            nearby = " ".join(paragraphs[max(0, paragraph_index - 1):paragraph_index + 2])
            if not printed_loci and "Gītā" not in nearby:
                continue
            for span_index, match in enumerate(DEVA_RE.finditer(paragraph)):
                printed_devanagari = " ".join(match.group().split()).strip(" -–—(),;:")
                if len(re.sub(r"\s", "", printed_devanagari)) < 2:
                    continue
                printed_iast = transliterate(printed_devanagari, sanscript.DEVANAGARI, sanscript.IAST)
                if row["number"] == 129 and paragraph_index == 0 and span_index == 0:
                    canonical_iast = "avyakto 'yam acintyo 'yam avikāryo 'yam ucyate"
                    quote_id = "name-129-paragraph-0-span-0"
                    quotes.append({
                        "id": quote_id, "name_number": 129, "paragraph_index": 0,
                        "source_start": match.start(), "source_end": match.end(),
                        "printed_devanagari": printed_devanagari, "printed_iast": printed_iast,
                        "printed_loci": ["Gītā 2.25"], "canonical_locus": "Gītā 2.25",
                        "canonical_devanagari": transliterate(canonical_iast, sanscript.IAST, sanscript.DEVANAGARI),
                        "canonical_iast": canonical_iast, "match_score": 1.0,
                        "match_basis": "scan-and-critical-witness-repair",
                        "textual_notes": [
                            "The improved OCR duplicated the final phrase repeatedly. The displayed line is restored "
                            "from the printed locus and the local critical Gītā witness."
                        ],
                        "analysis_ref": "2.25", "analysis_status": "linked-reviewed-corpus",
                        "chinmayananda_translation": TRANSLATION_OVERRIDES[quote_id],
                    })
                    continue
                if row["number"] == 275 and paragraph_index == 2 and span_index == 0:
                    composite = (
                        ((7, 11), "balaṃ balavatāṃ cāhaṃ", "बलं बलवतामस्मि"),
                        ((10, 36), "tejas tejasvinām aham", "तेजस्तेजस्विनामहम्"),
                    )
                    for piece_index, (canonical_locus, canonical_iast, printed_piece) in enumerate(composite):
                        quote_id = f"name-275-paragraph-2-span-0-piece-{piece_index}"
                        translation = TRANSLATION_OVERRIDES.get(quote_id)
                        quotes.append({
                            "id": quote_id,
                            "name_number": 275,
                            "paragraph_index": paragraph_index,
                            "source_start": match.start(),
                            "source_end": match.end(),
                            "printed_devanagari": printed_piece,
                            "printed_iast": transliterate(printed_piece, sanscript.DEVANAGARI, sanscript.IAST),
                            "printed_loci": [locus_text(locus) for locus in printed_loci],
                            "canonical_locus": locus_text(canonical_locus),
                            "canonical_devanagari": transliterate(canonical_iast, sanscript.IAST, sanscript.DEVANAGARI),
                            "canonical_iast": canonical_iast,
                            "match_score": round(similarity(transliterate(printed_piece, sanscript.DEVANAGARI, sanscript.IAST), canonical_iast), 4),
                            "match_basis": "manual-composite-adjudication",
                            "textual_notes": [
                                "The printed footnote combines two Gītā clauses under its Gītā 10.36 label. "
                                "This clause is aligned separately so neither source is misrepresented."
                            ],
                            "analysis_ref": f"{canonical_locus[0]}.{canonical_locus[1]}",
                            "analysis_status": "linked-reviewed-corpus",
                            "chinmayananda_translation": translation,
                        })
                    continue
                selected = choose_match(printed_iast, printed_loci, gita)
                if not selected:
                    continue
                match_score, canonical_locus, canonical_iast = selected
                canonical_devanagari = transliterate(canonical_iast, sanscript.IAST, sanscript.DEVANAGARI)
                notes = []
                if canonical_locus not in printed_loci:
                    if printed_loci:
                        notes.append(
                            f"Printed as {', '.join(locus_text(locus) for locus in printed_loci)}; "
                            f"the quoted words align with the critical-edition locus {locus_text(canonical_locus)}."
                        )
                    else:
                        notes.append(
                            f"The printed entry gives no exact Gītā locus; the quoted words align with the "
                            f"critical-edition locus {locus_text(canonical_locus)}."
                        )
                if compact_key(printed_iast) != compact_key(canonical_iast):
                    notes.append(
                        "The source-script line is normalized from the printed/OCR reading against the local "
                        "critical witness; the printed form remains recorded in this quote entry."
                    )
                quote_id = f"name-{row['number']}-paragraph-{paragraph_index}-span-{span_index}"
                translation = TRANSLATION_OVERRIDES.get(quote_id)
                if translation and english_key(translation) not in english_key(row["commentary"]):
                    raise ValueError(f"{quote_id} translation does not replay Chinmayananda's commentary")
                quotes.append({
                    "id": quote_id,
                    "name_number": row["number"],
                    "paragraph_index": paragraph_index,
                    "source_start": match.start(),
                    "source_end": match.end(),
                    "printed_devanagari": printed_devanagari,
                    "printed_iast": printed_iast,
                    "printed_loci": [locus_text(locus) for locus in printed_loci],
                    "canonical_locus": locus_text(canonical_locus),
                    "canonical_devanagari": canonical_devanagari,
                    "canonical_iast": canonical_iast,
                    "match_score": round(match_score, 4),
                    "match_basis": "critical-witness-fuzzy-replay",
                    "textual_notes": notes,
                    "analysis_ref": f"{canonical_locus[0]}.{canonical_locus[1]}",
                    "analysis_status": "linked-reviewed-corpus",
                    "chinmayananda_translation": translation,
                })
    quotes.sort(key=lambda quote: (quote["name_number"], quote["paragraph_index"], quote["source_start"]))
    return quotes


def fetch_analysis(locus: tuple[int, int], expected_iast: str) -> tuple[str, dict]:
    candidates = []
    for verse in (locus[1], locus[1] + 1, locus[1] - 1):
        if verse < 1:
            continue
        url = SUTRAKRIT_URL.format(chapter=locus[0], verse=verse)
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                body = response.read()
        except Exception:
            continue
        payload = json.loads(body)
        candidates.append((similarity(payload["mūla"]["iast"], expected_iast), url, body, payload))
    if not candidates:
        raise ValueError(f"Sūtrakṛt has no reachable analysis near {locus_text(locus)}")
    witness_score, url, body, payload = max(candidates, key=lambda item: item[0])
    if witness_score < 0.90:
        raise ValueError(f"Sūtrakṛt has no mūla replay near {locus_text(locus)}; best={witness_score:.3f}")
    record = {
        "verse_id": f"{locus[0]}.{locus[1]}",
        "api_verse_id": payload["verse_id"],
        "mula": payload["mūla"],
        "word_by_word": payload.get("word_by_word", []),
        "audit": {
            "word_by_word_parser": payload.get("audit_trail", {}).get("word_by_word_parser"),
            "corpus_provenance": payload.get("audit_trail", {}).get("corpus_provenance"),
            "response_sha256": hashlib.sha256(body).hexdigest(),
            "url": url,
            "local_bori_replay_score": round(witness_score, 4),
        },
    }
    return f"{locus[0]}.{locus[1]}", record


def refresh_analysis_packet(loci: set[tuple[int, int]], gita: dict[tuple[int, int], str]) -> dict:
    records = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch_analysis, locus, gita[locus]) for locus in sorted(loci)]
        for future in concurrent.futures.as_completed(futures):
            key, record = future.result()
            records[key] = record
    return {
        "schema_version": 1,
        "source": {
            "title": "Sūtrakṛt-Gītā selected-verse word analysis",
            "base_url": "https://gita.ekrasworks.com/api/v1/verse/",
            "license": "CC-BY 4.0",
            "attribution": "Gaurav Rastogi, Sūtrakṛt-Gītā: A Substrate-Rendered Edition of the Bhagavad-Gītā (2026)",
            "retrieved": "2026-08-28",
            "use_limit": "Quarantined computational comparison only; never a source for public morphology, derivation, or gloss.",
        },
        "verses": {key: records[key] for key in sorted(records, key=lambda value: tuple(map(int, value.split("."))))},
    }


def validate(quotes: list[dict], analysis_packet: dict | None) -> dict:
    ids = [quote["id"] for quote in quotes]
    if len(ids) != len(set(ids)):
        raise ValueError("quote ids are not unique")
    if any(not 1 <= quote["name_number"] <= 1000 for quote in quotes):
        raise ValueError("quote registry contains an invalid name number")
    if any(quote["match_score"] < 0.80 and quote.get("match_basis") != "manual-composite-adjudication"
           for quote in quotes):
        raise ValueError("quote registry contains a weak critical-witness match")
    refs = {quote["analysis_ref"] for quote in quotes}
    if analysis_packet is not None and refs - set(analysis_packet.get("verses", {})):
        raise ValueError(f"word-analysis packet lacks loci: {sorted(refs - set(analysis_packet.get('verses', {})))}")
    return {
        "quotes": len(quotes),
        "names_with_quotes": len({quote["name_number"] for quote in quotes}),
        "unique_gita_loci": len(refs),
        "printed_locus_corrections": sum(bool(quote["textual_notes"] and quote["canonical_locus"] not in quote["printed_loci"])
                                               for quote in quotes),
        "pending_word_audit": sum(quote["analysis_status"] == "pending-word-audit" for quote in quotes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-analysis", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    commentary = json.loads(COMMENTARY_PATH.read_text(encoding="utf-8"))
    gita = load_gita()
    quotes = build_quotes(commentary, gita)
    loci = {tuple(map(int, quote["analysis_ref"].split("."))) for quote in quotes}

    if args.refresh_analysis:
        packet = refresh_analysis_packet(loci, gita)
        ANALYSIS_PACKET_PATH.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        packet = json.loads(ANALYSIS_PACKET_PATH.read_text(encoding="utf-8")) if ANALYSIS_PACKET_PATH.exists() else None

    payload = {
        "schema_version": 1,
        "work": "Swami Chinmayananda, Thousand Ways to the Transcendental",
        "source_commentary": {
            "path": str(COMMENTARY_PATH.relative_to(ROOT)),
            "scope": "numbered Full commentary fields only",
            "sha256": commentary_quote_source_sha256(commentary),
        },
        "critical_gita": {"path": str(GITA_PATH.relative_to(ROOT)), "sha256": sha256(GITA_PATH)},
        "quotes": quotes,
    }
    report = validate(quotes, packet)
    if not args.check:
        OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
