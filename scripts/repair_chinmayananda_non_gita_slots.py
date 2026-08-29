#!/usr/bin/env python3
"""Apply reviewed literal-English wording and exact slot replay repairs."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATHS = tuple(sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-*.json")))
SLOT_RE = re.compile(r"\{[\d,\s]+:([^}]*)\}")

REPAIRS = {
    "name-11-paragraph-5-span-0": (
        "And the supreme Self, the support of all, the supreme Lord, Viṣṇu by name, is sung in all the Vedas and in the Vedāntas",
        "{1:And} {0:the supreme Self}, {2:the support of all}, {3:the supreme Lord}, {4:Viṣṇu by name}, {8:is sung} {5:in all the Vedas} {7:and} {6:in the Vedāntas}",
    ),
    "name-23-paragraph-2-span-0": (
        "because by you alone the evil-souled Keśī was slain, O Janārdana, therefore by the name Keśava you will be known in the world",
        "{0:because} {1:by you alone} {2:the evil-souled} {4:Keśī} {3:was slain}, {5:O Janārdana}, {6:therefore} {8:by the name} {7:Keśava} {9,11,12:you will be known} {10:in the world}",
    ),
    "name-55-paragraph-3-span-0": (
        "that which by the eye is not seen, by which the eyes see, know that alone to be Brahman, not this which they worship here as this",
        "{0:that which by the eye} {1,2:is not seen}, {3:by which} {4:the eyes} {5:see}, {8,9:know} {6:that alone} {7:to be Brahman}, {10:not this} {11:which they worship here as this}",
    ),
    "name-57-paragraph-2-span-0": (
        "the word kṛṣi, denotative of being, and ṇa, denotative of nirvṛti; the unity of those two, the supreme Brahman, is called “Kṛṣṇa”",
        "{1:the word} {0:kṛṣi, denotative of being}, {2:and ṇa}, {3:denotative of nirvṛti}; {4:the unity of those two}, {5:the supreme} {6:Brahman}, {7,8:is called “Kṛṣṇa”}",
    ),
    "name-57-paragraph-3-span-0": (
        "I plough the earth, having become a plough of iron for ploughing",
        "{0:I plough} {1:the earth}, {2:having become} {4,5:a plough of iron} {3:for ploughing}",
    ),
    "name-63-paragraph-1-span-0": (
        "They know that Brahman, which for men, by mere remembrance, removes inauspicious things and extends the auspicious succession, as that auspiciousness.",
        "{8:They know} {6:that Brahman}, {5:which for men}, {4:by mere remembrance}, {1:removes} {0:inauspicious things} {2:and extends} {3:the auspicious succession}, {7:as that auspiciousness.}",
    ),
    "name-72-paragraph-2-span-0": (
        "Because of understanding the Madhu-vidyā, or because of always being Śrī's husband, because of silence, and because of meditation, and because of yoga, know Mādhava, O Bhārata.",
        "{0:Because of understanding the Madhu-vidyā}, {1,2:or because of always being Śrī's husband}, {3:because of silence}, {4:and because of meditation}, {5:and because of yoga}, {6:know} {8:Mādhava}, {7:O Bhārata.}",
    ),
    "name-141-paragraph-2-span-0": (
        "There the sun does not shine, nor the moon-and-stars; these lightnings do not shine; how much less this fire. All shines after that one alone, shining; by its light all this shines.",
        "{1:There} {2:the sun} {0:does not} {3:shine}, {4:nor} {5:the moon-and-stars}; {7:these} {8:lightnings} {6:do not} {9:shine}; {10:how much less} {11:this} {12:fire}. {18:All} {16,17:shines after} {13,14:that one alone}, {15:shining}; {19:by its} {20:light} {21,22:all this} {23:shines}.",
    ),
    "name-187-paragraph-2-span-0": (
        "That which is not brought forth by speech, by which speech is brought forth: that alone know as Brahman, not this which here they worship.",
        "{0:That which} {2:is not brought forth} {1:by speech}, {3:by which} {4:speech} {5:is brought forth}: {6,7:that alone} {9,10:know} {8:as Brahman}, {11,12:not this} {13:which} {14:here} {15:they worship}.",
    ),
    "name-192-paragraph-1-span-0": (
        "two fair-winged companions, joined together, cling to the same tree; of the two, one eats the sweet pippala fruit, the other, not eating, looks on",
        "{0:two} {1:fair-winged} {3:companions}, {2:joined together}, {6:cling} {4:to the same} {5:tree}; {7:of the two, one} {9:eats the sweet} {8:pippala fruit}, {9:the other, not eating}, {10:looks on}",
    ),
    "name-245-paragraph-5-span-0": (
        "The principles born from Nara, the wise know as nārāṇi; those indeed are his resting-place, therefore he is remembered as Nārāyaṇa",
        "{0,1:The principles born from Nara}, {3:the wise know} {2:as nārāṇi}; {4:those indeed} {5:are his resting-place}, {7:therefore} {9:he is remembered} {6,8:as Nārāyaṇa}",
    ),
    "name-245-paragraph-6-span-0": (
        "I remember in mind the child Mukunda, lying in the hollow of a banyan leaf, placing his lotus foot into his lotus mouth with his lotus hand",
        "{11:I remember} {10:in mind} {8:the child} {9:Mukunda}, {7:lying} {6:in the hollow} {4,5:of a banyan leaf}, {3:placing} {1:his lotus foot} {2:into his lotus mouth} {0:with his lotus hand}",
    ),
    "name-899-paragraph-1-span-0": (
        "He drinks water (kam); therefore he is Kapi.",
        "{0,1,2:He drinks water (kam)}; {3:therefore} {4:he is Kapi.}",
    ),
}


def main() -> None:
    found = set()
    for path in PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for quote_id, row in data.get("quotes", {}).items():
            if quote_id not in REPAIRS:
                continue
            english, slots = REPAIRS[quote_id]
            if SLOT_RE.sub(lambda match: match.group(1), slots) != english:
                raise ValueError(f"repair does not replay: {quote_id}")
            row["english"] = english
            row["english_slots"] = slots
            found.add(quote_id)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if found != set(REPAIRS):
        raise ValueError(f"repair population differs: missing={sorted(set(REPAIRS)-found)}")
    print(json.dumps({"repaired": len(found)}, indent=2))


if __name__ == "__main__":
    main()
