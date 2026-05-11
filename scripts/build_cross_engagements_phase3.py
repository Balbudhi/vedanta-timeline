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


def make_paragraph(entry):
    target = entry["target"]
    axis = PRIMITIVE_LABELS.get(entry["primitive"], entry["primitive"])
    rel = relation(entry)
    cite = f"[primary text]({target['primary']})"
    if rel == "agrees":
        return (
            f"Cross-engagement: {target['name']} works the same {axis} axis in the {entry['register']} register. "
            f"Here the operative value is `{entry['source_value']}`; {target['name']} lands on that same value in "
            f"{cite}. The convergence is narrow rather than total: the shared primitive is real, but the wider doctrine still travels under a different architecture."
        )
    if rel == "transposes-register":
        return (
            f"Cross-engagement: {target['name']} touches the same {axis} axis, but not in the same register. "
            f"This section works it as `{entry['source_value']}` in the {entry['register']} register; "
            f"{target['name']} approaches it through the {target['register']} register in {cite}. "
            f"The point of contact is genuine, but the comparison only holds once the register-shift is kept visible."
        )
    return (
        f"Cross-engagement: {target['name']} presses the same {axis} axis in the {entry['register']} register, "
        f"but with the value `{target['value']}` rather than `{entry['source_value']}` in {cite}. "
        f"The disagreement is structural, not verbal. Both texts are answering the same pressure-point; they are not locating the pressure in the same way."
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
