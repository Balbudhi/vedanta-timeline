#!/usr/bin/env python3

import json
import re
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINKERS_DIR = ROOT / "data" / "thinkers"
REGISTRY_PATH = ROOT / "data" / "registries" / "primitive_graph.json"
APP_JS_PATH = ROOT / "assets" / "app.js"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_primitive_graph_phase2 import DEPENDENCIES, PRIMITIVES  # noqa: E402


ARTICLE_BY_THINKER = {
    "adorno": "data/articles/source/adorno.md",
    "anirban": "data/articles/source/samkhya-anirban.md",
    "aurobindo": "data/articles/source/aurobindo.md",
    "bergson": "data/articles/source/bergson.md",
    "caitanya": "data/articles/source/caitanya.md",
    "chaudhuri": "data/articles/source/chaudhuri-banerji.md",
    "deleuze": "data/articles/source/deleuze.md",
    "derrida": "data/articles/source/derrida.md",
    "foucault": "data/articles/source/foucault.md",
    "gebser": "data/articles/source/gebser.md",
    "hegel": "data/articles/source/hegel.md",
    "heidegger": "data/articles/source/heidegger.md",
    "husserl": "data/articles/source/husserl.md",
    "kc-bhattacharyya": "data/articles/source/kc-bhattacharyya.md",
    "leibniz": "data/articles/source/leibniz.md",
    "levinas": "data/articles/source/levinas.md",
    "madhva": "data/articles/source/madhva.md",
    "mcgilchrist": "data/articles/source/mcgilchrist.md",
    "medhananda": "data/articles/source/medhananda.md",
    "nietzsche": "data/articles/source/nietzsche.md",
    "prigogine": "data/articles/source/prigogine.md",
    "ramakrishna": "data/articles/source/vivekananda-ramakrishna.md",
    "ramanuja": "data/articles/source/ramanuja.md",
    "sankara": "data/articles/source/shankara.md",
    "spinoza": "data/articles/source/spinoza.md",
    "vivekananda": "data/articles/source/vivekananda-ramakrishna.md",
    "whitehead": "data/articles/source/whitehead.md",
}


ARTICLE_BACKED_THINKERS = {
    "adorno",
    "aurobindo",
    "bergson",
    "caitanya",
    "derrida",
    "foucault",
    "gebser",
    "hegel",
    "heidegger",
    "husserl",
    "kc-bhattacharyya",
    "levinas",
    "madhva",
    "mcgilchrist",
    "medhananda",
    "nietzsche",
    "prigogine",
    "ramanuja",
    "sankara",
    "spinoza",
    "vivekananda",
    "whitehead",
}


MANUAL_CITATION_LOCI = {
    "bergson": {
        "substrate_structure": "Creative Evolution, chs. 1-3",
        "selfhood_structure": "Time and Free Will, ch. 2",
        "temporal_mode": "Creative Evolution, Introduction",
        "register_of_evolution": "Creative Evolution, chs. 1-3",
        "method_of_critique": "Creative Evolution, Introduction",
    },
    "deleuze": {
        "individuation_status": "Difference and Repetition, ch. 1",
        "determination_operator": "Difference and Repetition, ch. 1",
        "method_of_critique": "Difference and Repetition, Preface",
    },
    "derrida": {
        "epistemic_authority": "Of Grammatology, Part I",
        "determination_operator": "Différance",
        "method_of_critique": "Of Grammatology, Part I",
        "semantic_mediation": "Différance",
        "modal_structure_of_truth": "Speech and Phenomena, chs. 6-7",
    },
    "foucault": {
        "manifestation_status": "Discipline and Punish, Part III",
        "selfhood_structure": "History of Sexuality, vol. 1, Part II",
        "finite_cognition_model": "Discipline and Punish, Part III",
        "epistemic_authority": "Nietzsche, Genealogy, History",
        "determination_operator": "Nietzsche, Genealogy, History",
        "method_of_critique": "Nietzsche, Genealogy, History",
        "normative_order_source": "Discipline and Punish, Part III",
        "social_formation_model": "Discipline and Punish, Parts III-IV",
        "practice_path": "What Is Critique?",
    },
    "gebser": {
        "temporal_mode": "The Ever-Present Origin, Part II",
        "register_of_evolution": "The Ever-Present Origin, Part II",
        "social_formation_model": "The Ever-Present Origin, Conclusion",
    },
    "levinas": {
        "selfhood_structure": "Totality and Infinity, Section I",
        "normative_order_source": "Totality and Infinity, Preface",
        "social_formation_model": "Otherwise than Being, ch. 5",
        "affective_motive_force": "Totality and Infinity, Section I",
        "soteric_end": "Otherwise than Being, ch. 5",
    },
    "leibniz": {
        "substrate_structure": "Monadology §§1-19",
        "manifestation_status": "Monadology §§47-60",
        "causation_model": "Monadology §§78-81",
        "temporal_mode": "Monadology §§47-52",
    },
    "mcgilchrist": {
        "social_formation_model": "The Master and His Emissary, Part Two",
        "temporal_mode": "The Matter with Things, vol. II, chs. 20-28",
        "individuation_status": "The Matter with Things, vol. II, ch. 27",
    },
    "medhananda": {
        "epistemic_authority": "Swami Vivekananda's Vedantic Cosmopolitanism, Introduction",
        "method_of_critique": "Swami Vivekananda's Vedantic Cosmopolitanism, ch. 1",
        "modal_structure_of_truth": "Swami Vivekananda's Vedantic Cosmopolitanism, chs. 4-5",
        "relation_to_perspectivism": "Swami Vivekananda's Vedantic Cosmopolitanism, chs. 4-5",
    },
    "prigogine": {
        "substrate_structure": "Order out of Chaos, chs. 5-6",
        "causation_model": "Order out of Chaos, chs. 5-6",
        "temporal_mode": "The End of Certainty, Introduction",
        "register_of_evolution": "Order out of Chaos, ch. 6",
    },
}


MANUAL_CROSS_ENGAGEMENTS = {
    "mcgilchrist": [
        {
            "counter_thinker": "aurobindo",
            "primitive": "temporal_mode",
            "agreement_type": "shared-axis",
            "register": "metaphysical",
            "brief": "Aurobindo also insists that a timeless poise and a dynamic unfolding must be held together rather than collapsed into a flat process-metaphysics.",
            "citations": ["cite://aurobindo/the-life-divine/II.27"],
            "source_article": "data/articles/source/mcgilchrist.md",
        }
    ]
}


CITE_RE = re.compile(r"cite://[^)\s>]+")
SECTION_RE = re.compile(r"^(##+)\s+(.*)$")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def article_sections(article_path):
    path = ROOT / article_path
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(line)
        if m:
            out.append(m.group(2).strip())
    return out


def first_article_section(article_path):
    sections = article_sections(article_path)
    return sections[0] if sections else None


def first_primary_citation(thinker_id, thinker):
    for item in thinker.get("primitive_commitments", []):
        for ev in item.get("evidence", []):
            if ev.get("kind") == "primary" and ev.get("refs"):
                return ev["refs"][0]
    for work in thinker.get("engaged_works", []):
        title = work.get("title_iast") or work.get("title")
        if title:
            return title
    article_path = ARTICLE_BY_THINKER.get(thinker_id)
    if article_path:
        cites = CITE_RE.findall((ROOT / article_path).read_text(encoding="utf-8"))
        if cites:
            return cites[0]
        section = first_article_section(article_path)
        if section:
            return f"{Path(article_path).name} § {section}"
    return f"{thinker_id}.json core_thesis"


def commitment_citation_locus(thinker_id, thinker, item):
    if item.get("citation_locus"):
        return item["citation_locus"]
    manual = MANUAL_CITATION_LOCI.get(thinker_id, {})
    if item["primitive"] in manual:
        return manual[item["primitive"]]
    for ev in item.get("evidence", []):
        if ev.get("kind") == "primary" and ev.get("refs"):
            return ev["refs"][0]
    for work in thinker.get("engaged_works", []):
        title = work.get("title_iast") or work.get("title")
        if title:
            return title
    article_path = ARTICLE_BY_THINKER.get(thinker_id)
    if article_path:
        cites = CITE_RE.findall((ROOT / article_path).read_text(encoding="utf-8"))
        if cites:
            return cites[0]
        section = first_article_section(article_path)
        if section:
            return f"{Path(article_path).name} § {section}"
    return first_primary_citation(thinker_id, thinker)


def normalize_commitments(thinker_id, thinker):
    normalized = []
    for item in thinker.get("primitive_commitments", []):
        out = {
            "primitive": item["primitive"],
            "value": item["value"],
            "register": item["register"],
            "citation_locus": commitment_citation_locus(thinker_id, thinker, item),
        }
        if item.get("confidence"):
            out["confidence"] = item["confidence"]
        if item.get("notes"):
            out["notes"] = item["notes"]
        normalized.append(out)
    return sorted(
        normalized,
        key=lambda x: (x["primitive"], x["register"], x["value"]),
    )


def line_number_for_passage(article_path, passage):
    full = ROOT / article_path
    if not full.exists():
        return None
    target = passage.strip()
    for idx, line in enumerate(full.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip() == target:
            return idx
    return None


def normalize_brief(passage):
    text = passage.strip()
    text = re.sub(r"^Cross-engagement:\s*", "", text)
    text = re.sub(r"\s*in \[primary text\]\([^)]+\)\.", ".", text)
    text = text.replace(
        " The disagreement is structural, not verbal. Both texts are answering the same pressure-point; they are not locating the pressure in the same way.",
        "",
    )
    text = text.replace(
        " The convergence is narrow rather than total: the shared primitive is real, but the wider doctrine still travels under a different architecture.",
        "",
    )
    text = text.replace(
        " The point of contact is genuine, but the comparison only holds once the register-shift is kept visible.",
        "",
    )
    return text.strip()


def normalize_agreement_type(relation):
    mapping = {
        "agrees": "shared-presupposition",
        "disagrees": "genuine-disagreement",
        "subsumes": "subsumption",
        "sharpens": "shared-axis",
        "transposes-register": "register-shift",
        "shares-axis-different-end": "shared-axis",
    }
    return mapping.get(relation, "genuine-disagreement")


def normalize_cross_engagements(thinker_id, thinker):
    normalized = []
    seen = set()
    for item in thinker.get("cross_engagements", []):
        citations = []
        if item.get("other_primary_citation"):
            citations.append(item["other_primary_citation"])
        elif item.get("citations"):
            citations.extend(item["citations"])
        if not citations:
            continue
        brief = normalize_brief(item.get("passage", item.get("brief", "")))
        out = {
            "counter_thinker": item.get("other_thinker_id") or item.get("counter_thinker"),
            "primitive": item["primitive"],
            "agreement_type": normalize_agreement_type(item.get("relation")),
            "register": item["register"],
            "brief": brief,
            "citations": citations,
        }
        article_path = item.get("article")
        if article_path:
            out["source_article"] = article_path
            if item.get("passage"):
                line = line_number_for_passage(article_path, item["passage"])
                if line:
                    out["source_locus"] = f"{Path(article_path).name}:{line}"
        sig = (
            out["counter_thinker"],
            out["primitive"],
            out["agreement_type"],
            out["register"],
            tuple(out["citations"]),
            out["brief"],
        )
        if sig in seen:
            continue
        seen.add(sig)
        normalized.append(out)
    for item in MANUAL_CROSS_ENGAGEMENTS.get(thinker_id, []):
        sig = (
            item["counter_thinker"],
            item["primitive"],
            item["agreement_type"],
            item["register"],
            tuple(item["citations"]),
            item["brief"],
        )
        if sig in seen:
            continue
        seen.add(sig)
        normalized.append(deepcopy(item))
    return normalized


def build_registry(thinkers):
    observed_registers = defaultdict(set)
    commitment_edges = []
    cross_edges = []
    subsumption_critique = []

    for thinker_id, thinker in thinkers.items():
        for item in thinker.get("primitive_commitments", []):
            observed_registers[item["primitive"]].add(item["register"])
            commitment_edges.append({
                "thinker": thinker_id,
                "primitive": item["primitive"],
                "value": item["value"],
                "register": item["register"],
                "citation_locus": item["citation_locus"],
                "confidence": item.get("confidence", "medium"),
            })
        for item in thinker.get("cross_engagements", []):
            edge = {
                "thinker": thinker_id,
                "counter_thinker": item["counter_thinker"],
                "primitive": item["primitive"],
                "agreement_type": item["agreement_type"],
                "register": item["register"],
                "brief": item["brief"],
                "citations": item["citations"],
            }
            if item.get("source_article"):
                edge["source_article"] = item["source_article"]
            if item.get("source_locus"):
                edge["source_locus"] = item["source_locus"]
            cross_edges.append(edge)
            if item["agreement_type"] in {"subsumption", "register-shift"}:
                subsumption_critique.append({
                    "from": thinker_id,
                    "to": item["counter_thinker"],
                    "register": item["register"],
                    "brief": item["brief"],
                })

    primitives = []
    for primitive_id, meta in PRIMITIVES.items():
        primitives.append({
            "id": primitive_id,
            "label": meta["label"],
            "definition": meta["description"],
            "values": meta["values"],
            "registers": sorted(observed_registers.get(primitive_id, {meta["category"]})),
        })

    return {
        "version": "v2-phase125",
        "description": "Master registry for the primitives_v2 graph and per-thinker commitment portal scaffolding.",
        "primitives": primitives,
        "edges": {
            "dependency": [[item["from"], item["to"]] for item in DEPENDENCIES],
            "commitment_thinker_to_primitive": commitment_edges,
            "cross_engagement": cross_edges,
            "subsumption_critique": subsumption_critique,
        },
    }


def main():
    thinkers = {}
    for path in sorted(THINKERS_DIR.glob("*.json")):
        thinker = load_json(path)
        thinker["primitive_commitments"] = normalize_commitments(path.stem, thinker)
        thinker["cross_engagements"] = normalize_cross_engagements(path.stem, thinker)
        thinkers[path.stem] = thinker
        save_json(path, thinker)

    # Coverage floor for article-backed thinkers.
    for thinker_id in sorted(ARTICLE_BACKED_THINKERS):
        thinker = thinkers[thinker_id]
        if len(thinker["primitive_commitments"]) < 3:
            raise SystemExit(f"{thinker_id} has only {len(thinker['primitive_commitments'])} primitive commitments")
        if len(thinker["cross_engagements"]) < 3:
            raise SystemExit(f"{thinker_id} has only {len(thinker['cross_engagements'])} cross engagements")

    save_json(REGISTRY_PATH, build_registry(thinkers))


if __name__ == "__main__":
    main()
