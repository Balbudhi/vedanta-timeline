#!/usr/bin/env python3

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "data" / "articles" / "source"
THINKERS_DIR = ROOT / "data" / "thinkers"


ARTICLE_TO_PRIMARY = {
    "adorno": "adorno",
    "aurobindo": "aurobindo",
    "bergson": "bergson",
    "caitanya": "caitanya",
    "chaudhuri-banerji": "chaudhuri",
    "comparative-claims-framework": "hegel",
    "deleuze": "deleuze",
    "derrida": "derrida",
    "engagement-madhusudana__bhakti-rasayana": "madhusudana",
    "engagement-madhva__bhagavata-tatparya-nirnaya": "madhva",
    "engagement-madhva__brahma-sutra-bhasya": "madhva",
    "engagement-madhva__mayavada-khandana": "madhva",
    "engagement-nimbarka_srinivasa__vedanta-parijata-saurabha-kaustubha": "nimbarka",
    "engagement-raghavendra__nyaya-sudha-parimala": "raghavendra",
    "engagement-raghavendra__tantra-dipika": "raghavendra",
    "engagement-ramanuja__sri-bhasya": "ramanuja",
    "engagement-vallabha__anu-bhasya": "vallabha",
    "engagement-vedanta-desika__pancaratra-raksha": "vedanta-desika",
    "engagement-vidyaranya__vivarana-prameya-sangraha": "vidyaranya",
    "engagement-vijnanabhiksu__vijnanamrta-bhasya": "vijnanabhiksu",
    "engagement-vijnanabhiksu__yoga-varttika": "vijnanabhiksu",
    "engagement-yamuna__agama-pramanya": "yamuna",
    "foucault": "foucault",
    "gebser": "gebser",
    "hegel": "hegel",
    "hegel-preface": "hegel",
    "heidegger": "heidegger",
    "husserl": "husserl",
    "kala-cakra-clock-structures": "prigogine",
    "kc-bhattacharyya": "kc-bhattacharyya",
    "kcb-kantian-perspectivism": "kc-bhattacharyya",
    "leibniz": "leibniz",
    "levinas": "levinas",
    "madhva": "madhva",
    "mcgilchrist": "mcgilchrist",
    "medhananda": "medhananda",
    "mimamsa-aurobindo-v1": "aurobindo",
    "mimamsa-aurobindo-v2": "aurobindo",
    "mimamsa-aurobindo-v3": "aurobindo",
    "mimamsa-aurobindo-v4": "aurobindo",
    "nietzsche": "nietzsche",
    "prigogine": "prigogine",
    "primitive-graph": "madhva",
    "primitive-model": "sankara",
    "ramanuja": "ramanuja",
    "samkhya-anirban": "anirban",
    "shankara": "sankara",
    "spinoza": "spinoza",
    "vedanta-realist-history": "madhva",
    "vivekananda-ramakrishna": "vivekananda",
    "whitehead": "whitehead",
}


PRIMITIVE_LABELS = {
    "substrate_structure": "substrate structure",
    "manifestation_status": "manifestation status",
    "identity_relation": "identity relation",
    "individuation_status": "individuation status",
    "causation_model": "causation model",
    "selfhood_structure": "selfhood structure",
    "finite_cognition_model": "finite cognition",
    "epistemic_authority": "epistemic authority",
    "determination_operator": "determination",
    "method_of_critique": "method",
    "semantic_mediation": "semantic mediation",
    "temporal_mode": "temporal mode",
    "register_of_evolution": "evolution register",
    "modal_structure_of_truth": "truth-structure",
    "relation_to_perspectivism": "perspectivism",
    "normative_order_source": "normativity",
    "social_formation_model": "social formation",
    "affective_motive_force": "motive force",
    "practice_path": "practice-path",
    "soteric_end": "soteric end",
}


PREFERRED_SEQUENCE = [
    "substrate_structure",
    "manifestation_status",
    "identity_relation",
    "selfhood_structure",
    "finite_cognition_model",
    "epistemic_authority",
    "determination_operator",
    "method_of_critique",
    "semantic_mediation",
    "temporal_mode",
    "register_of_evolution",
    "modal_structure_of_truth",
    "relation_to_perspectivism",
    "normative_order_source",
    "social_formation_model",
    "affective_motive_force",
    "practice_path",
    "soteric_end",
]


def load_thinkers():
    out = {}
    for path in THINKERS_DIR.glob("*.json"):
        out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return out


def commitment_index(thinkers):
    by_primitive = defaultdict(list)
    for thinker_id, thinker in thinkers.items():
        for item in thinker.get("primitive_commitments", []):
            primary = None
            for ev in item.get("evidence", []):
                if ev.get("kind") == "primary":
                    refs = ev.get("refs", [])
                    if refs:
                        primary = refs[0]
                        break
            if not primary:
                continue
            by_primitive[item["primitive"]].append({
                "thinker_id": thinker_id,
                "name": thinker.get("name", thinker_id),
                "school": thinker.get("school", ""),
                "value": item["value"],
                "register": item["register"],
                "primary": primary,
            })
    return by_primitive


def pick_candidates(primary_thinker, commitments, by_primitive, max_items):
    chosen = []
    used_targets = set()
    ordered = sorted(
        commitments,
        key=lambda x: (PREFERRED_SEQUENCE.index(x["primitive"]) if x["primitive"] in PREFERRED_SEQUENCE else 999, x["primitive"])
    )
    for item in ordered:
        pool = [p for p in by_primitive.get(item["primitive"], []) if p["thinker_id"] != primary_thinker["id"]]
        if not pool:
            continue
        pool.sort(
            key=lambda x: (
                0 if x["register"] == item["register"] and x["value"] != item["value"] else
                1 if x["register"] == item["register"] else
                2 if x["value"] != item["value"] else
                3,
                x["name"],
            )
        )
        target = None
        for cand in pool:
            if cand["thinker_id"] not in used_targets:
                target = cand
                break
        if not target:
            continue
        used_targets.add(target["thinker_id"])
        chosen.append({
            "primitive": item["primitive"],
            "register": item["register"],
            "source_value": item["value"],
            "target": target,
        })
        if len(chosen) >= max_items:
            break
    return chosen


def relation(entry):
    target = entry["target"]
    if target["register"] != entry["register"]:
        return "transposes-register"
    if target["value"] == entry["source_value"]:
        return "agrees"
    return "disagrees"


import hashlib as _hashlib

# Rotated cross-engagement templates. Five variants per relation type, picked
# deterministically by hashing the data slots. The variants share the same
# data fields and the same load-bearing claim; they vary only the sentence
# shape and discourse vocabulary, to keep the surrounding prose from reading
# as a 30-token boilerplate the way the prior single-template form did.

_AGREES_VARIANTS = [
    "Cross-engagement: {name} settles on `{value}` for the {axis} axis at {cite}.",
    "Cross-engagement: on the {axis} axis the agreement with {name} is precise. {name} fixes `{value}` at {cite}.",
    "Cross-engagement: a narrow point of contact with {name} — `{value}` shared on the {axis} axis at {cite}.",
    "Cross-engagement: {name} reads the {axis} axis as `{value}` in the {register} register; see {cite}.",
    "Cross-engagement: on this one axis ({axis}) {name} arrives at `{value}` ({cite}).",
    "Cross-engagement: at the {axis} axis the two texts coincide; {name} treats it as `{value}` at {cite}.",
    "Cross-engagement: same value at the {axis} axis — {name} arrives at `{value}` from a different direction in {cite}, with the {register}-register reading lining up at the joint.",
    "Cross-engagement: this section and {name} land at the same point on the {axis} axis ({cite}, `{value}`).",
    "Cross-engagement: {name}'s {register}-register treatment of the {axis} axis settles on `{value}` at {cite}, the same value taken up here.",
    "Cross-engagement: both texts read the {axis} axis as `{value}` ({cite}, {name}).",
    "Cross-engagement: agreement with {name} restricted to the {axis} axis: `{value}` in the {register} register at {cite}.",
    "Cross-engagement: shared commitment at the {axis} axis. {name} commits to `{value}` in {cite}.",
    "Cross-engagement: {name} ({cite}) takes the {axis} axis the same way: `{value}`, {register} register.",
    "Cross-engagement: across architectures, one shared joint. {name} and the present section both treat the {axis} axis as `{value}` ({cite}).",
    "Cross-engagement: on the {axis} axis the present section meets {name}'s reading at {cite}, with `{value}` as the operative commitment.",
]

_DISAGREES_VARIANTS = [
    "Cross-engagement: {name} works the {axis} axis in the {register} register too, but the value is `{target_value}`, not `{source_value}` ({cite}).",
    "Cross-engagement: on the {axis} axis, {name} commits to `{target_value}` where this section commits to `{source_value}` ({cite}).",
    "Cross-engagement: {name} ({cite}) treats the {axis} axis in the {register} register with the value `{target_value}`. The present section reads it as `{source_value}`.",
    "Cross-engagement: a substantive disagreement with {name} on the {axis} axis — `{target_value}` ({cite}) against the present `{source_value}`.",
    "Cross-engagement: {name} lands on `{target_value}` for the {axis} axis ({cite}); this section lands on `{source_value}`.",
    "Cross-engagement: the disagreement with {name} is at the {axis} axis itself: `{source_value}` here, `{target_value}` in {cite}.",
    "Cross-engagement: on the {axis} axis {name} reads `{target_value}` ({cite}); the present section reads `{source_value}`.",
    "Cross-engagement: {name} takes the {axis} axis to a different commitment — `{target_value}` at {cite} against `{source_value}` here.",
    "Cross-engagement: a real divergence with {name} on the {axis} axis. The {register} register is shared; the values are not — `{source_value}` here, `{target_value}` at {cite}.",
    "Cross-engagement: at the {axis} axis the two texts choose differently. {name} ({cite}) commits to `{target_value}`; this section commits to `{source_value}`.",
    "Cross-engagement: {name} ({cite}) and this section take opposite turns on the {axis} axis — `{target_value}` against `{source_value}`.",
    "Cross-engagement: same {register} register, different commitments at the {axis} axis. {name}: `{target_value}`, {cite}. Here: `{source_value}`.",
    "Cross-engagement: against {name}: `{source_value}` rather than `{target_value}` for the {axis} axis ({cite}).",
    "Cross-engagement: {name}'s reading at {cite} fills the {axis} axis with `{target_value}`. The present section fills it with `{source_value}`.",
    "Cross-engagement: divergence at the {axis} axis. The present commitment is `{source_value}`; {name}'s is `{target_value}` ({cite}).",
]

_TRANSPOSES_VARIANTS = [
    "Cross-engagement: {name} works the same {axis} axis but in a different register. Here: `{source_value}` in the {source_register} register; {name}: {target_register} register at {cite}.",
    "Cross-engagement: the {axis} axis appears in both texts in different registers. This section: `{source_value}`, {source_register} register. {name}: {target_register} register, {cite}.",
    "Cross-engagement: {name} treats the {axis} axis from the {target_register} register ({cite}); the present section is in the {source_register} register with `{source_value}`.",
    "Cross-engagement: same axis ({axis}), different registers — `{source_value}` in the {source_register} register here, {target_register} register in {cite}.",
    "Cross-engagement: this section places the {axis} axis in the {source_register} register with `{source_value}`; {name} places it in the {target_register} register at {cite}.",
    "Cross-engagement: register-shifted contact with {name}. The {axis} axis is shared; the {source_register} reading (`{source_value}`) here and the {target_register} reading in {cite} are not interchangeable.",
    "Cross-engagement: {name} works the {axis} axis from the {target_register} side ({cite}); this section from the {source_register} side with `{source_value}`.",
    "Cross-engagement: the {axis} axis bridges two registers — {source_register} (`{source_value}`) here, {target_register} in {cite} ({name}).",
    "Cross-engagement: register-shift across the {axis} axis. Here: {source_register}, `{source_value}`. There: {name}, {target_register}, {cite}.",
    "Cross-engagement: {name} touches the {axis} axis from the {target_register} register at {cite}; the present section from the {source_register} register with `{source_value}`.",
    "Cross-engagement: {name}'s {target_register}-register treatment ({cite}) cuts the {axis} axis differently from this section's {source_register}-register `{source_value}`.",
    "Cross-engagement: a cross-register comparison with {name}. {axis} axis, {source_register} register, `{source_value}` here; {target_register} register at {cite}.",
    "Cross-engagement: {name} ({cite}) and this section meet on the {axis} axis from different sides — {target_register} register against {source_register} register, with `{source_value}` as this section's commitment.",
    "Cross-engagement: the {axis} axis surfaces here in the {source_register} register as `{source_value}`; {name} works it from the {target_register} register at {cite}.",
    "Cross-engagement: register-asymmetric agreement on the {axis} axis. {name} approaches it through the {target_register} register ({cite}); this section through the {source_register} register with `{source_value}`.",
]


def _variant_index(key: str, n: int) -> int:
    return _hashlib.sha1(key.encode("utf-8")).digest()[0] % n


def make_paragraph(entry):
    target = entry["target"]
    axis = PRIMITIVE_LABELS.get(entry["primitive"], entry["primitive"])
    rel = relation(entry)
    cite = f"[primary text]({target['primary']})"
    if rel == "agrees":
        key = f"agrees|{target['name']}|{axis}|{entry['register']}|{entry['source_value']}|{cite}"
        tpl = _AGREES_VARIANTS[_variant_index(key, len(_AGREES_VARIANTS))]
        return tpl.format(
            name=target["name"], axis=axis,
            register=entry["register"], value=entry["source_value"], cite=cite,
        )
    if rel == "transposes-register":
        key = (
            f"transposes|{target['name']}|{axis}|{entry['source_value']}|"
            f"{entry['register']}|{target['register']}|{cite}"
        )
        tpl = _TRANSPOSES_VARIANTS[_variant_index(key, len(_TRANSPOSES_VARIANTS))]
        return tpl.format(
            name=target["name"], axis=axis,
            source_value=entry["source_value"],
            source_register=entry["register"],
            target_register=target["register"],
            cite=cite,
        )
    key = (
        f"disagrees|{target['name']}|{axis}|{entry['register']}|"
        f"{target['value']}|{entry['source_value']}|{cite}"
    )
    tpl = _DISAGREES_VARIANTS[_variant_index(key, len(_DISAGREES_VARIANTS))]
    return tpl.format(
        name=target["name"], axis=axis,
        register=entry["register"],
        target_value=target["value"],
        source_value=entry["source_value"],
        cite=cite,
    )


def insertion_points(lines):
    headings = []
    for idx, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("### "):
            headings.append(idx)
    return headings


def insert_after_first_paragraph(lines, heading_idx, paragraph):
    i = heading_idx + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    while i < len(lines) and lines[i].strip() != "":
        i += 1
    insert_at = i
    block = ["", paragraph, ""]
    return lines[:insert_at] + block + lines[insert_at:]


def inject_article(path, paragraphs):
    text = path.read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines():
        if line.startswith("Cross-engagement: "):
            continue
        lines.append(line)
    headings = insertion_points(lines)
    if not headings:
        return
    count = min(len(paragraphs), len(headings))
    offset = 0
    for idx in range(count):
        lines = insert_after_first_paragraph(lines, headings[idx] + offset, paragraphs[idx])
        offset += 3
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def attach_json_records(thinkers, thinker_id, article_slug, entries):
    thinker = thinkers[thinker_id]
    thinker["cross_engagements"] = thinker.get("cross_engagements", [])
    for entry in entries:
        thinker["cross_engagements"].append({
            "article": f"data/articles/source/{article_slug}.md",
            "primitive": entry["primitive"],
            "register": entry["register"],
            "relation": relation(entry),
            "other_thinker_id": entry["target"]["thinker_id"],
            "other_primary_citation": entry["target"]["primary"],
            "passage": make_paragraph(entry),
        })


def write_thinkers(thinkers):
    for thinker_id, payload in thinkers.items():
        path = THINKERS_DIR / f"{thinker_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    thinkers = load_thinkers()
    for thinker in thinkers.values():
        thinker["cross_engagements"] = []
    by_primitive = commitment_index(thinkers)
    for article_path in sorted(ARTICLES_DIR.glob("*.md")):
        slug = article_path.stem
        primary_id = ARTICLE_TO_PRIMARY.get(slug)
        if not primary_id or primary_id not in thinkers:
            continue
        commitments = thinkers[primary_id].get("primitive_commitments", [])
        if not commitments:
            continue
        headings = insertion_points(article_path.read_text(encoding="utf-8").splitlines())
        target_count = min(len(headings), 12 if len(headings) >= 12 else len(headings))
        if target_count == 0:
            continue
        chosen = pick_candidates(thinkers[primary_id], commitments, by_primitive, target_count)
        paragraphs = [make_paragraph(entry) for entry in chosen]
        inject_article(article_path, paragraphs)
        attach_json_records(thinkers, primary_id, slug, chosen)
    write_thinkers(thinkers)


if __name__ == "__main__":
    main()
