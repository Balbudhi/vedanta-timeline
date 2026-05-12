"""Inventory Sanskrit terms across the corpus and queue terms needing entries.

The site's runtime renderer (assets/app.js) already auto-wraps any term whose
key OR alias appears in data/glossary/*.json (see buildGlossaryRegex). So the
authorial markdown does not need to embed link wrappers — coverage is purely a
function of (a) presence of a glossary file, and (b) the alias list inside it.

This script:
  1. Builds the alias lookup matching what the JS regex would match.
  2. Scans articles/thinkers/perspectives/glossary for italicized Sanskrit
     terms (the `*term*` markdown signal) and known-Sanskrit plain tokens.
  3. Reports:
       - existing glossary coverage (terms linked, surfaces touched).
       - missing terms (italicized Sanskrit not in any alias list) → queue.
"""

import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GLOSSARY_DIR = os.path.join(ROOT, "data", "glossary")
ARTICLES_DIR = os.path.join(ROOT, "data", "articles", "source")
THINKERS_DIR = os.path.join(ROOT, "data", "thinkers")
PERSPECTIVES_DIR = os.path.join(ROOT, "data", "perspectives", "source")

AUDIT_DIR = os.path.join(ROOT, "audit")
os.makedirs(AUDIT_DIR, exist_ok=True)

# IAST diacritic letters that mark a word as Sanskrit.
IAST_DIACRITICS = set("āīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ")

# Letters that count as part of an IAST word (matches app.js IAST_LETTER_CLASS).
IAST_LETTER = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    "āīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ"
)


def has_diacritic(s: str) -> bool:
    return any(c in IAST_DIACRITICS for c in s)


# A loose list of common Sanskrit terms that appear without diacritics in
# the corpus and should still be flagged. We are conservative — only flag
# terms that almost certainly carry technical Sanskrit weight when italicized.
KNOWN_SANSKRIT_PLAIN = {
    "atman", "brahman", "karma", "dharma", "moksha", "moksa", "samsara",
    "advaita", "dvaita", "bhakti", "jnana", "jiva", "guru", "vedanta",
    "upanishad", "yoga", "samadhi", "guna", "prakrti", "purusa", "purusha",
    "maya", "avidya", "isvara", "ishvara", "antahkarana", "ahankara",
    "buddhi", "manas", "citta", "sat", "cit", "ananda", "sakti", "shakti",
    "siva", "shiva", "visnu", "vishnu", "nyaya", "vaisesika", "samkhya",
    "sankhya", "mimamsa", "yogacara", "madhyamaka", "sruti", "smrti",
    "smriti", "sastra", "shastra", "tarka", "pramana", "sabda", "shabda",
    "pratyaksa", "anumana", "upamana", "arthapatti", "anupalabdhi",
    "tattva", "padartha", "vyakti", "jati", "kala", "akasa", "akasha",
    "prana", "vac", "vak", "lila", "rasa", "vrtti", "vritti", "vasana",
    "samskara", "rta", "rita", "satya", "tapas", "vairagya", "viveka",
    "moha", "raga", "dvesa", "klesha", "klesa", "nirvana", "sunyata",
    "shunyata", "tathagata", "bodhisattva", "anatta", "anatman", "skandha",
    "samadhi", "samapatti", "dhyana", "japa", "mantra", "yantra", "tantra",
    "sadhana", "siddhi", "bhasya", "varttika", "tika", "sutra", "karika",
    "asrama", "ashrama", "varna", "purana", "agama", "nigama", "rsi",
    "rishi", "muni", "deva", "asura", "bhuta", "indriya", "tanmatra",
    "mahabhuta", "ksetra", "kshetra", "ksetrajna", "kshetrajna",
    "paramatman", "antaryamin", "saksin", "sakshin", "turiya", "jagrat",
    "svapna", "susupti", "sushupti", "pratibimba", "abhasa", "upadhi",
    "adhyasa", "abheda", "bheda", "anyonyabhava", "atyantabhava",
    "samavaya", "samyoga", "vibhaga", "parinama", "vivartta", "vivarta",
    "abhava", "ekayana", "ekajiva", "drsti", "drishti", "srsti", "srishti",
    "pralaya", "kalpa", "yuga", "loka", "naraka", "svarga", "moksha-marga",
    "prarabdha", "sancita", "sanchita", "agami", "kriyamana",
    "phalapeksa", "phalapeksha", "niskama", "nishkama", "karta", "kartrtva",
    "bhokrtva", "anugraha", "saranagati", "prapatti", "namo", "nyasa",
    "abhinanda", "abhinaya", "abhinivesha", "abhinivesa",
}


def load_glossary():
    """Return (alias_set, alias_to_key, all_entries).

    alias_set: every string that the JS regex would match (term_key + aliases).
    alias_to_key: alias → term_key.
    all_entries: term_key → entry-dict.
    """
    manifest = json.load(open(os.path.join(GLOSSARY_DIR, "manifest.json")))
    alias_set = set()
    alias_to_key = {}
    all_entries = {}
    for fname in manifest["terms"]:
        with open(os.path.join(GLOSSARY_DIR, fname), encoding="utf-8") as f:
            entry = json.load(f)
        key = entry["term_key"]
        all_entries[key] = entry
        alias_set.add(key)
        alias_to_key[key] = key
        for a in entry.get("aliases", []):
            alias_set.add(a)
            alias_to_key[a] = key
    return alias_set, alias_to_key, all_entries


def build_alias_regex(alias_set):
    """Mirror buildGlossaryRegex in app.js so we match the same surface."""
    keys = sorted(alias_set, key=lambda s: -len(s))
    escaped = [re.escape(k) for k in keys]
    letter_class = "".join(sorted(IAST_LETTER))
    # Use lookarounds matching the JS character class.
    pattern = (
        r"(?<![" + letter_class + r"])(" + "|".join(escaped)
        + r")(?![" + letter_class + r"])"
    )
    return re.compile(pattern)


# Detect a candidate Sanskrit token inside italics or a bare diacritic word.
ITALIC_TOKEN_RE = re.compile(r"\*([^*\n]+?)\*")
# Split italic content into individual word tokens.
WORD_RE = re.compile(r"[A-Za-z" + "".join(IAST_DIACRITICS) + r"]+(?:[-’'][A-Za-z" + "".join(IAST_DIACRITICS) + r"]+)*")

# Strip codeblocks before scanning markdown.
CODEBLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINECODE_RE = re.compile(r"`[^`\n]+`")
HTMLLINK_RE = re.compile(r"\]\([^)]*\)")  # markdown link target — skip


def strip_non_prose(src: str) -> str:
    src = CODEBLOCK_RE.sub("", src)
    src = INLINECODE_RE.sub("", src)
    return src


def iter_files():
    """Yield (surface_kind, file_path, content) tuples."""
    # Articles (markdown).
    for fn in sorted(os.listdir(ARTICLES_DIR)):
        if fn.endswith(".md"):
            p = os.path.join(ARTICLES_DIR, fn)
            yield ("article", p, open(p, encoding="utf-8").read())
    # Perspectives (markdown).
    if os.path.isdir(PERSPECTIVES_DIR):
        for fn in sorted(os.listdir(PERSPECTIVES_DIR)):
            if fn.endswith(".md"):
                p = os.path.join(PERSPECTIVES_DIR, fn)
                yield ("perspective", p, open(p, encoding="utf-8").read())
    # Thinkers (JSON — pull text out of relevant fields).
    for fn in sorted(os.listdir(THINKERS_DIR)):
        if fn.endswith(".json"):
            p = os.path.join(THINKERS_DIR, fn)
            data = json.load(open(p, encoding="utf-8"))
            # Concatenate prose fields.
            parts = []
            for k in ("core_thesis", "key_moves", "engaged_works", "notes"):
                v = data.get(k)
                if isinstance(v, str):
                    parts.append(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            parts.append(item)
                        elif isinstance(item, dict):
                            for sv in item.values():
                                if isinstance(sv, str):
                                    parts.append(sv)
            yield ("thinker", p, "\n\n".join(parts))
    # Glossary cross-links (term definitions reference each other).
    for fn in sorted(os.listdir(GLOSSARY_DIR)):
        if fn.endswith(".json") and fn != "manifest.json":
            p = os.path.join(GLOSSARY_DIR, fn)
            data = json.load(open(p, encoding="utf-8"))
            parts = [data.get("invariant_definition", "") or "",
                     data.get("translator_note", "") or "",
                     data.get("literal", "") or ""]
            for s in data.get("per_school", []) or []:
                if isinstance(s, dict):
                    parts.append(s.get("definition", "") or "")
            yield ("glossary", p, "\n\n".join(parts))


def is_probable_sanskrit(token: str) -> bool:
    """Heuristic: a token is Sanskrit if it carries a diacritic, OR is a
    known plain-romanized Sanskrit term, OR is hyphenated and has diacritics
    in any segment.
    """
    if has_diacritic(token):
        return True
    low = token.lower().strip("-")
    if low in KNOWN_SANSKRIT_PLAIN:
        return True
    # Hyphen compound where any segment is known.
    if "-" in low:
        segs = [s for s in low.split("-") if s]
        if any(seg in KNOWN_SANSKRIT_PLAIN for seg in segs):
            return True
    return False


# Normalize IAST → ASCII for stem-matching.
_IAST_FOLD = str.maketrans({
    "ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṝ": "r", "ḷ": "l", "ḹ": "l",
    "ṅ": "n", "ñ": "n", "ṭ": "t", "ḍ": "d", "ṇ": "n",
    "ś": "s", "ṣ": "s", "ṃ": "m", "ḥ": "h",
    "Ā": "a", "Ī": "i", "Ū": "u", "Ṛ": "r", "Ṝ": "r", "Ḷ": "l", "Ḹ": "l",
    "Ṅ": "n", "Ñ": "n", "Ṭ": "t", "Ḍ": "d", "Ṇ": "n",
    "Ś": "s", "Ṣ": "s", "Ṃ": "m", "Ḥ": "h",
})


def fold_iast(s: str) -> str:
    return s.lower().translate(_IAST_FOLD)


# Suffix patterns characteristic of Sanskrit work / commentary titles. A
# candidate ending in one of these is treated as a proper work-name unless
# its lemma is a known stand-alone technical term.
WORK_TITLE_SUFFIXES = (
    "-bhāṣya", "-bhasya", "-sūtra", "-sutra", "-kārikā", "-karika",
    "-vārttika", "-varttika", "-ṭīkā", "-tika", "-upaniṣad", "-upanisad",
    "-saṃhitā", "-samhita", "-saṅgraha", "-sangraha", "-prakaraṇa",
    "-prakarana", "-dīpikā", "-dipika", "-pradīpa", "-pradipa",
    "-kaustubha", "-ratnāvalī", "-ratnavali", "-mañjarī", "-manjari",
    "-muktāvalī", "-muktavali", "-nirṇaya", "-nirnaya", "-mīmāṃsā",
    "-mimamsa", "-gītā", "-gita", "-purāṇa", "-purana", "-darśana",
    "-darsana", "-saurabha",
)

# Tokens that look Sanskrit but are actually proper-name-only (or stand-alone
# work titles). Manually curated from a first-pass scan; expand cautiously.
WORK_NAME_TOKENS = {
    "brahma-sūtra", "brahma-sūtra-bhāṣya", "brahma-sutra", "brahma-sutra-bhasya",
    "śrī-bhāṣya", "sri-bhasya", "anuvyākhyāna", "anuvyakhyana",
    "advaita-siddhi", "nyāyāmṛta", "nyayamrta", "naiṣkarmya-siddhi",
    "bhāgavata", "bhagavata", "gītā", "gita", "bhāmatī", "bhamati",
    "vivaraṇa", "vivarana", "pañcadaśī", "pancadasi",
    "māṇḍūkya", "mandukya", "bṛhadāraṇyaka", "brhadaranyaka",
    "chāndogya", "chandogya", "taittirīya", "taittiriya",
    "kena", "katha", "praśna", "prasna", "muṇḍaka", "mundaka",
    "īśa", "isa", "aitareya", "kauṣītaki", "kausitaki",
    "śvetāśvatara", "svetasvatara",
}


def load_thinker_keys():
    keys = set()
    for fn in os.listdir(THINKERS_DIR):
        if fn.endswith(".json"):
            try:
                d = json.load(open(os.path.join(THINKERS_DIR, fn), encoding="utf-8"))
            except Exception:
                continue
            for k in ("key", "id", "thinker_key"):
                if isinstance(d.get(k), str):
                    keys.add(d[k].lower())
            # Also fold the IAST name into a key form.
            for k in ("name", "name_iast"):
                v = d.get(k)
                if isinstance(v, str):
                    keys.add(fold_iast(v.strip().split()[0]))
            keys.add(fn[:-5].lower())  # filename stem
    return keys


# English-adjective-ish suffix forms of Sanskrit terms — should not be queued
# as new glossary entries.
ENGLISH_ADJ_SUFFIXES = ("ic", "ical", "ist", "istic", "ian", "ist's", "ic's")


def main():
    alias_set, alias_to_key, all_entries = load_glossary()
    alias_regex = build_alias_regex(alias_set)
    thinker_keys = load_thinker_keys()

    # Normalized-stem index: for inflection detection.
    folded_keys = {fold_iast(k): k for k in all_entries}
    for a, k in alias_to_key.items():
        folded_keys.setdefault(fold_iast(a), k)

    # For each surface, count alias matches (existing glossary coverage)
    # and italicized Sanskrit candidates that don't match any alias.
    surface_matches = defaultdict(Counter)  # surface_path → Counter of matched keys
    missing_terms = Counter()  # candidate Sanskrit term → count
    missing_contexts = defaultdict(list)  # candidate term → list of (path, snippet)
    surfaces_touched = set()  # surfaces that contain at least one matched term
    files_scanned = Counter()  # surface_kind → file count
    # Capitalization gaps: token IS an existing alias when lowercased, but
    # the capitalized form is not in the alias list. Runtime regex is
    # case-sensitive, so the capitalized form silently fails to auto-link.
    case_gaps = Counter()  # (capitalized_token, target_key) → count

    for kind, path, content in iter_files():
        files_scanned[kind] += 1
        text = strip_non_prose(content)

        # 1. Count matches against the existing alias regex.
        for m in alias_regex.finditer(text):
            matched = m.group(1)
            key = alias_to_key[matched]
            surface_matches[path][key] += 1
            surfaces_touched.add(path)

        # 2. Find italicized Sanskrit candidates not covered by any alias.
        # The italic span itself (whole content) is treated as the lemma —
        # we do not pull sub-tokens out of compounds, because doing so
        # generates false positives (e.g. extracting `maya` from
        # `*acintya-śakti-maya*` even though `maya` is already a glossary alias
        # that matches via the runtime regex's lookarounds).
        for m in ITALIC_TOKEN_RE.finditer(text):
            inner = m.group(1).strip()
            # Reject if inner is multi-word English-style prose.
            if " " in inner:
                continue
            # Reject very long spans (likely multi-clause).
            if len(inner) > 60:
                continue
            # Drop trailing punctuation.
            token = inner.rstrip(".,;:!?)’'")
            token = token.lstrip("(‘'")
            if len(token) < 3:
                continue
            # Skip pure-English: no diacritic AND not in known plain set AND
            # not a hyphen-compound with a known segment.
            if not is_probable_sanskrit(token):
                continue
            # Skip if already covered by alias regex (case-sensitive, mirrors
            # the runtime regex in app.js).
            if alias_regex.fullmatch(token) is not None:
                continue
            # ALSO skip if the lowercased token would match — these are
            # sentence-start capitalizations of glossary terms. They will not
            # auto-link at runtime (the renderer regex is case-sensitive), but
            # they are not a "new term" candidate either; they're a coverage
            # gap to fix by adding the Capitalized form to the entry's aliases.
            lc = token[0].lower() + token[1:]
            if alias_regex.fullmatch(lc) is not None:
                tgt = alias_to_key.get(lc)
                if tgt:
                    case_gaps[(token, tgt)] += 1
                continue
            # For hyphen compounds, also skip if every diacritic-bearing
            # segment fold-matches an existing entry. (e.g. `acintya-śakti-maya`
            # would all-fold-match; surface it as a compound proposal instead.)
            if "-" in token:
                segs = [s for s in token.split("-") if s]
                if segs and all(
                    fold_iast(s) in folded_keys or s in alias_set
                    for s in segs
                ):
                    # All segments are known; the compound itself is unknown
                    # but its parts are. Treat as a compound proposal: queue
                    # under the full token so reviewer can decide whether to
                    # add an entry or rely on segment-level linking.
                    pass
            key_cand = token.lower()
            missing_terms[key_cand] += 1
            if len(missing_contexts[key_cand]) < 3:
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                snippet = text[start:end].replace("\n", " ").strip()
                rel = os.path.relpath(path, ROOT)
                missing_contexts[key_cand].append({
                    "file": rel,
                    "snippet": snippet,
                })

    # Aggregate totals.
    total_links = sum(sum(c.values()) for c in surface_matches.values())
    unique_keys_used = set()
    for c in surface_matches.values():
        unique_keys_used.update(c.keys())

    # Bucket missing candidates into:
    #   - inflected_or_variant: stem matches an existing glossary entry → fix by
    #     augmenting that entry's aliases (we list these as alias-augment proposals).
    #   - work_title: matches WORK_NAME_TOKENS or has a work-title suffix → not a
    #     glossary candidate; lives in the citation/source index instead.
    #   - genuinely_new: candidate needs a new glossary entry, queued for Agent G.
    inflected_or_variant = []  # (candidate, count, target_key)
    work_title_skipped = []    # (candidate, count)
    proper_name_skipped = []   # thinker / proper-noun overlap
    english_adj_skipped = []   # English-adj derivatives
    genuinely_new = []         # full candidate dict (≥2 occurrences)
    low_priority = []          # singletons; deferred bucket

    for term, count in sorted(missing_terms.items(), key=lambda kv: (-kv[1], kv[0])):
        # Singletons without diacritics: drop entirely (too noisy).
        if count < 2 and not has_diacritic(term):
            continue

        folded_lc = fold_iast(term)

        # English-adjective form ("vedāntic", "advaitan", "śaivist") — drop.
        if any(folded_lc.endswith(suf) for suf in ENGLISH_ADJ_SUFFIXES):
            english_adj_skipped.append({"term": term, "occurrences": count})
            continue

        # Single-token thinker name — drop (those have their own page).
        if folded_lc in thinker_keys:
            proper_name_skipped.append({"term": term, "occurrences": count, "thinker_key": folded_lc})
            continue

        # Inflection check: strip terminal -s, -m, -n, -ḥ, -ḥa, -aḥ before lookup.
        target_key = None
        candidates_stems = [
            folded_lc,
            folded_lc.rstrip("s"),
            folded_lc.rstrip("m"),
            folded_lc.rstrip("n"),
            folded_lc[:-2] if folded_lc.endswith("ah") else folded_lc,
            folded_lc[:-2] if folded_lc.endswith("am") else folded_lc,
        ]
        for stem in candidates_stems:
            if stem in folded_keys:
                target_key = folded_keys[stem]
                break
        if target_key:
            inflected_or_variant.append({
                "variant": term,
                "occurrences": count,
                "existing_key": target_key,
                "existing_aliases": list(all_entries[target_key].get("aliases", [])),
            })
            continue

        # Work-title check.
        is_work = term in WORK_NAME_TOKENS
        if not is_work:
            for suf in WORK_TITLE_SUFFIXES:
                if term.endswith(suf):
                    is_work = True
                    break
        if is_work:
            work_title_skipped.append({"term": term, "occurrences": count})
            continue

        bucket = {
            "candidate_term": term,
            "occurrences": count,
            "sample_contexts": missing_contexts[term],
            "note": (
                "Italicized Sanskrit token not matched by any current glossary "
                "alias and not a known work-title or inflected variant. Verify "
                "it is a real Sanskrit technical term and pick a canonical IAST "
                "spelling before authoring an entry. Do not invent a gloss."
            ),
        }
        if count >= 2:
            genuinely_new.append(bucket)
        else:
            low_priority.append(bucket)

    queue = genuinely_new

    out_queue = {
        "generated_by": "tools/glossary_autolink_inventory.py",
        "schema_note": (
            "Each candidate must be verified before a glossary entry is authored. "
            "Do not auto-create. Anti-fabrication: only author from primary sources."
        ),
        "total_candidates": len(queue),
        "candidates": queue,
        "alias_augmentation_proposals": inflected_or_variant,
        "alias_augmentation_note": (
            "Italicized tokens whose IAST-folded stem matches an existing "
            "glossary entry. These are already glossed; the canonical fix is to "
            "extend the entry's `aliases` list so the runtime regex catches the "
            "inflected form. No new glossary entry is needed."
        ),
        "skipped_work_titles": work_title_skipped,
        "skipped_work_titles_note": (
            "Italicized tokens that look like work / commentary titles "
            "(by suffix or curated denylist). These belong to the citation / "
            "source manifest, not the glossary."
        ),
        "skipped_proper_names": proper_name_skipped,
        "skipped_proper_names_note": (
            "Tokens that collide with a thinker key. These already have a "
            "thinker page; not a glossary candidate."
        ),
        "skipped_english_adjectives": english_adj_skipped,
        "skipped_english_adjectives_note": (
            "Tokens with English adjective / agent suffixes (e.g. -ic, -ical, "
            "-ist, -ian). Drop — they are English derivatives, not Sanskrit lemmas."
        ),
        "low_priority_singletons": low_priority,
        "low_priority_note": (
            "Diacritic-bearing italicized tokens that appear only once across "
            "the entire corpus. Likely real Sanskrit, but isolated — author entries "
            "only if the term is doctrinally load-bearing in the cited surface. "
            "Defer until the ≥2-occurrence queue is drained."
        ),
        "capitalization_gaps": [
            {"capitalized_token": tok, "existing_key": tgt, "occurrences": cnt}
            for (tok, tgt), cnt in sorted(case_gaps.items(), key=lambda kv: -kv[1])
        ],
        "capitalization_gaps_note": (
            "Italicized terms appearing in capitalized form (typically at "
            "sentence-start) whose lowercase form matches an existing alias. "
            "The runtime regex is case-sensitive (mirrors app.js), so these "
            "fail to auto-link silently. Fix by adding the capitalized form to "
            "the entry's `aliases` list."
        ),
    }
    with open(os.path.join(AUDIT_DIR, "glossary_terms_to_create.json"), "w", encoding="utf-8") as f:
        json.dump(out_queue, f, indent=2, ensure_ascii=False)

    # Report.
    by_kind = Counter()
    for path in surface_matches:
        if "/articles/" in path:
            by_kind["articles"] += 1
        elif "/thinkers/" in path:
            by_kind["thinkers"] += 1
        elif "/glossary/" in path:
            by_kind["glossary"] += 1
        elif "/perspectives/" in path:
            by_kind["perspectives"] += 1

    report_lines = [
        "# Glossary Autolink Inventory",
        "",
        "**Mechanism note:** the runtime renderer (`assets/app.js`,",
        "`buildGlossaryRegex` at line 2352 and the two `state.glossaryRegex` ",
        "calls in `md()` / `renderMarkdownFull()`) auto-wraps every occurrence",
        "of a glossary key or alias in `<span class=\"term\" data-term=...>`.",
        "Authors therefore do *not* embed link wrappers in source markdown;",
        "coverage is determined entirely by the alias lists in",
        "`data/glossary/*.json`.",
        "",
        "## Coverage",
        "",
        f"- Files scanned: " + ", ".join(f"{k}={v}" for k, v in files_scanned.items()),
        f"- Surfaces with at least one auto-link: **{len(surfaces_touched)}**",
        f"- Distinct glossary keys hit: **{len(unique_keys_used)} / {len(all_entries)}**",
        f"- Total auto-link occurrences (will render as popovers): **{total_links}**",
        "",
        "### Per-kind surface counts",
        "",
    ]
    for k, v in sorted(by_kind.items()):
        report_lines.append(f"- {k}: {v} files contain at least one auto-link")

    # Top 15 most-linked terms.
    top_used = Counter()
    for c in surface_matches.values():
        for k, v in c.items():
            top_used[k] += v
    report_lines.append("")
    report_lines.append("### Top 15 most-used glossary entries")
    report_lines.append("")
    for key, count in top_used.most_common(15):
        entry = all_entries[key]
        iast = entry.get("term_iast", key)
        report_lines.append(f"- `{key}` ({iast}): {count} occurrences")

    # Unused glossary entries.
    unused = sorted(set(all_entries) - unique_keys_used)
    report_lines.append("")
    report_lines.append(f"### Unused glossary entries ({len(unused)})")
    report_lines.append("")
    if unused:
        report_lines.append(
            "These have a JSON file but no alias matches in the scanned corpus. "
            "May indicate spelling drift in either the entry's aliases or the "
            "prose; review and add aliases as needed."
        )
        report_lines.append("")
        for k in unused:
            iast = all_entries[k].get("term_iast", k)
            report_lines.append(f"- `{k}` ({iast})")

    # Queue summary.
    report_lines.extend([
        "",
        "## New-entry queue",
        "",
        f"- Genuinely new candidates (≥2 occurrences) queued in `audit/glossary_terms_to_create.json`: **{len(queue)}**",
        f"- Low-priority diacritic singletons (deferred bucket): **{len(low_priority)}**",
        f"- Alias-augmentation proposals (inflected forms of existing entries): **{len(inflected_or_variant)}**",
        f"- Capitalization gaps (sentence-start capitalized forms missing from alias lists): **{len(case_gaps)}**",
        f"- Work-title tokens skipped (belong to citation index, not glossary): **{len(work_title_skipped)}**",
        f"- Proper-name tokens skipped (already a thinker page): **{len(proper_name_skipped)}**",
        f"- English-adjective tokens skipped: **{len(english_adj_skipped)}**",
        "",
        "Filters applied:",
        "",
        "- Italicized Sanskrit token (`*term*`) is the primary precision signal.",
        "- ≥2 occurrences OR a diacritic-bearing token.",
        "- Stem-fold (IAST → ASCII, with terminal -s/-m/-n/-aḥ stripped) routes",
        "  inflected forms into the alias-augmentation bucket instead of the queue.",
        "- Work-title denylist + suffix list routes commentary names away.",
        "- *No glosses are invented*: Agent G picks these up and authors entries",
        "  from primary sources.",
        "",
        "### Top 30 genuinely-new candidates",
        "",
    ])
    for c in queue[:30]:
        report_lines.append(f"- `{c['candidate_term']}` ({c['occurrences']} occurrences)")

    report_lines.extend([
        "",
        "### Top 20 alias-augmentation proposals",
        "",
        "These are inflected forms of existing glossary entries. Folding their",
        "stem into the entry's `aliases` list will make the runtime regex catch",
        "them on next page load — no new entry needed.",
        "",
    ])
    for prop in inflected_or_variant[:20]:
        report_lines.append(
            f"- `{prop['variant']}` → existing entry `{prop['existing_key']}` "
            f"({prop['occurrences']} occurrences)"
        )

    report_lines.extend([
        "",
        "## Known limitations",
        "",
        "- The italics signal (`*term*`) is the primary precision filter. Bare",
        "  romanized tokens (e.g. plain \"karma\" in casual prose) are intentionally",
        "  not flagged; the renderer's regex still picks them up if a glossary alias",
        "  exists, but we do not surface them as new-entry candidates.",
        "- A token in a markdown link's display text *could* be flagged spuriously;",
        "  inline-code and fenced-code blocks are stripped before scanning.",
        "- Whole italicized spans are treated as the candidate lemma. Multi-word",
        "  italic phrases (containing a space) are dropped to avoid noise; this",
        "  may miss legitimate two-word Sanskrit titles, which surface in the",
        "  citation index instead.",
        "- The work-title denylist is curated, not exhaustive. Compounds ending in",
        "  `-bhāṣya`, `-sūtra`, `-kārikā`, etc. are filtered by suffix; novel work",
        "  names without those suffixes may slip through.",
        "- Codex/Opus authoring step (Agent G) must confirm each candidate is a",
        "  real Sanskrit technical term, not (e.g.) an italicized English phrase",
        "  or a proper name already covered by the thinkers index.",
    ])

    with open(os.path.join(AUDIT_DIR, "autolink_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"Wrote audit/glossary_terms_to_create.json ({len(queue)} candidates)")
    print(f"Wrote audit/autolink_report.md")
    print(f"Coverage: {total_links} auto-link occurrences across {len(surfaces_touched)} surfaces")
    print(f"Distinct glossary keys used: {len(unique_keys_used)}/{len(all_entries)}")


if __name__ == "__main__":
    main()
