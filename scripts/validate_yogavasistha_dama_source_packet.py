#!/usr/bin/env python3
"""Fail-closed validation for the Dāma story source population."""

from __future__ import annotations

import json
import re
from pathlib import Path

from indic_transliteration.sanscript import DEVANAGARI, IAST, transliterate


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/sources/sanskrit/vedanta/laghuyogavasistha_dama_story.json"


def fold_iast(value: str) -> str:
    value = value.normalize("NFC") if hasattr(value, "normalize") else value
    value = value.replace("ṁ", "ṃ").replace("’", "'").lower()
    return re.sub(r"[^a-zāīūṛṝḷeoṃḥkgṅcjñṭḍṇtdnpbmyrlvśṣsh']", "", value)


def main() -> None:
    data = json.loads(PACKET.read_text(encoding="utf-8"))
    expected = [f"lyv-4-2-{verse:02d}" for verse in range(31, 87)]
    observed = [unit["id"] for unit in data["units"]]
    errors: list[str] = []
    if observed != expected:
        errors.append("unit population differs from the frozen 31-86 sequence")
    if len(observed) != len(set(observed)):
        errors.append("duplicate unit IDs")
    if data["population"]["expected_units"] != 56 or data["population"]["observed_units"] != 56:
        errors.append("population accounting is not 56/56")

    for unit in data["units"]:
        if unit["verse"] != int(unit["id"].rsplit("-", 1)[1]):
            errors.append(f"{unit['id']}: verse number disagrees with ID")
        generated = transliterate(unit["deva"], DEVANAGARI, IAST)
        if fold_iast(generated) != fold_iast(unit["iast"]):
            errors.append(f"{unit['id']}: Devanāgarī/IAST replay mismatch")

    apparatus = {entry["id"]: entry for entry in data["apparatus"]}
    robot = apparatus.get("robot-reading", {})
    if "yantrapuruṣāś" not in robot.get("critical_iast", ""):
        errors.append("critical yantrapuruṣa reading is absent")
    if "ऽत्यज्ञपुरुषाः" not in robot.get("vulgate_devanagari", ""):
        errors.append("vulgate atyajñapuruṣa reading is absent")
    construction = apparatus.get("construction-cluster", {})
    if len(construction.get("critical_iast", [])) != 6:
        errors.append("critical construction cluster is not 6/6")
    if len(construction.get("vulgate_devanagari", [])) != 7:
        errors.append("vulgate construction cluster is not 7/7")

    notes = {entry["unit_id"]: entry for entry in data.get("textual_notes", [])}
    if "mīmabhāsa" not in notes.get("lyv-4-2-33", {}).get("printed_and_transcribed", ""):
        errors.append("printed mīmabhāsa reading is not preserved in the apparatus")

    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    print("Yoga-Vāsiṣṭha Dāma source packet: 56/56 units, paired-script replay and apparatus OK")


if __name__ == "__main__":
    main()
