#!/usr/bin/env python3
"""Repair reviewed Gītā quote rows where source-token coverage exposed omissions."""

import copy
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json"
QUOTE_ID = "name-200-paragraph-1-span-0"


def sample_word(data: dict, iast: str) -> dict:
    return copy.deepcopy(next(
        word
        for candidate in data["quotes"].values()
        for word in candidate["words"]
        if word["iast"] == iast
    ))


def shift_slots(slots: str, position: int) -> str:
    def replace(match: re.Match[str]) -> str:
        values = [int(value.strip()) for value in match.group(1).split(",")]
        shifted = [value + 1 if value >= position else value for value in values]
        return "{" + ",".join(str(value) for value in shifted) + ":"
    return re.sub(r"\{([\d,\s]+):", replace, slots)


def insert_word(row: dict, position: int, word: dict, expected_count: int = 1) -> None:
    if sum(existing["iast"] == word["iast"] for existing in row["words"]) >= expected_count:
        return
    row["english_slots"] = shift_slots(row["english_slots"], position)
    row["words"].insert(position, word)
    for index, item in enumerate(row["words"]):
        item["i"] = index


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    row = data["quotes"][QUOTE_ID]
    if not any(word["iast"] == "aham" for word in row["words"]):
        word = sample_word(data, "aham")
        word["i"] = len(row["words"])
        row["words"].append(word)
    row["english_slots"] = "{0:Among the animals}, {1,3:I am} {2:the King of animals, Lion}"
    for quote_id in ("name-554-paragraph-1-span-0", "name-915-paragraph-2-span-0"):
        target = data["quotes"][quote_id]
        insert_word(target, 0, sample_word(data, "yat"), expected_count=2)
    data["quotes"]["name-554-paragraph-1-span-0"]["english_slots"] = (
        "{11,12:understand} {0,1,2,3,4,5,6,7,8,9,10:them all} "
        "{16:as coming out} {13,14,15:of my glory}"
    )
    data["quotes"]["name-915-paragraph-2-span-0"]["english_slots"] = (
        "{0,1,2,3,4,5,6,7:Wherever, there is any special glory in anyone}. "
        "{11,12:know} {8,9,10:that} {16:to be a manifestation} "
        "{13,14,15:of a part of my Splendour}"
    )
    target = data["quotes"]["name-742-paragraph-3-span-0"]
    insert_word(target, len(target["words"]), sample_word(data, "anyaḥ"))
    target["english_slots"] = (
        "{0,1,2,3:None there exists who is equal to You}; "
        "{4,5,6:how can there be then another superior to You} "
        "{0,1,2,3,4,5,6:in the three worlds, O Being of unequalled power}"
    )
    target = data["quotes"]["name-780-paragraph-2-span-0"]
    insert_word(target, 0, sample_word(data, "yaḥ"))
    target["english_slots"] = (
        "{0,1,2,5:This Yoga of equanimity}, {3,4:taught by Thee}, "
        "{6:O slayer of Madhu}, {8,9,10:I see not} {7,13,14:its enduring continuity}, "
        "{11,12:because of the restlessness} {11,12:(of the mind)}"
    )
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"quote_id": QUOTE_ID, "words": len(row["words"])}))


if __name__ == "__main__":
    main()
