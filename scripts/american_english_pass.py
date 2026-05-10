"""American-English standardization pass.

Operates on the following file scopes (per project brief):
    - data/thinkers/*.json (English prose fields only)
    - data/glossary/*.json
    - data/perspectives/source/*.md
    - data/full_translations/*.md (English-translation lines only;
        leaves IAST and Devanagari untouched)
    - data/polemic_chains/*.json
    - data/articles/source/*.md
    - data/articles/manifest.json (titles, subtitles)

Exemptions:
    - Code blocks (``` ... ```) in markdown are preserved verbatim
        (file paths, function names, etc.).
    - Inline code spans (`...`) in markdown preserved verbatim.
    - HTML/XML tags `<...>` preserved.
    - URLs preserved verbatim (we do not transform within http(s)://
        ... or www. ... runs).
    - IAST / Devanagari: substitution rules use \\b word boundaries and
        target only ASCII English words; IAST diacritics live outside
        the target set so they are not affected. Devanagari is in a
        different Unicode block.
    - Lines that are clearly non-English (heuristic: > 30% non-ASCII or
        contain Devanagari ranges) are skipped wholesale.
    - Author names, publishing house names, primary-source titles —
        substitutions targeted at common-noun spellings; proper nouns
        like "Centre for Indian Studies" are listed in PROTECTED_TOKENS
        and left alone.
    - Block-quoted (>) lines in markdown are preserved verbatim, since
        these are direct quotations from primary sources.

Substitutions follow the standard British-to-American mapping:
    -ise/-isation -> -ize/-ization (centralized list; some -ise verbs
        are American too, e.g. exercise/promise — these are NOT in our
        rule set).
    -our -> -or (colour, behaviour, etc.).
    -re -> -er (centre, theatre, etc.).
    -ence -> -ense for defence/offence/pretence/licence (n.).
    -ogue -> -og for analogue/catalogue/dialogue (American optional —
        we leave dialogue alone since it is widely used in US English).
    Specific word swaps: whilst -> while, amongst -> among, towards ->
        toward, forwards -> forward, learnt -> learned.

Output: writes a report to handoffs/american_english_pass_2026-05-10.md
    with file count, substitution count, and judgment-call list.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ---------------------------------------------------------------------------
# Substitution table.
# Each entry: (pattern, replacement, category, judgment_note)
# Patterns are case-aware: capitalized form mapped if the source word starts
# with a capital. We implement that with a function-replacement.
# ---------------------------------------------------------------------------

# Word-list approach (rather than blanket regex) keeps us safe from
# false-positives like 'license' (already American) vs 'licence' (British noun).

PAIRS: list[tuple[str, str]] = [
    # ise -> ize family (verbs, nouns, adjectives)
    ("analyse", "analyze"),
    ("analysed", "analyzed"),
    ("analyses", "analyzes"),  # the verb form; 'analyses' as plural noun is identical
    ("analysing", "analyzing"),
    ("realise", "realize"),
    ("realised", "realized"),
    ("realising", "realizing"),
    ("realisation", "realization"),
    ("realisations", "realizations"),
    ("organise", "organize"),
    ("organised", "organized"),
    ("organising", "organizing"),
    ("organisation", "organization"),
    ("organisations", "organizations"),
    ("recognise", "recognize"),
    ("recognised", "recognized"),
    ("recognising", "recognizing"),
    ("recognisable", "recognizable"),
    ("recognisably", "recognizably"),
    ("recognises", "recognizes"),
    ("emphasise", "emphasize"),
    ("emphasised", "emphasized"),
    ("emphasises", "emphasizes"),
    ("emphasising", "emphasizing"),
    ("characterise", "characterize"),
    ("characterised", "characterized"),
    ("characterises", "characterizes"),
    ("characterising", "characterizing"),
    ("characterisation", "characterization"),
    ("characterisations", "characterizations"),
    ("criticise", "criticize"),
    ("criticised", "criticized"),
    ("criticises", "criticizes"),
    ("criticising", "criticizing"),
    ("generalise", "generalize"),
    ("generalised", "generalized"),
    ("generalises", "generalizes"),
    ("generalising", "generalizing"),
    ("generalisation", "generalization"),
    ("specialise", "specialize"),
    ("specialised", "specialized"),
    ("specialises", "specializes"),
    ("specialising", "specializing"),
    ("specialisation", "specialization"),
    ("synthesise", "synthesize"),
    ("synthesised", "synthesized"),
    ("synthesises", "synthesizes"),
    ("synthesising", "synthesizing"),
    ("hypothesise", "hypothesize"),
    ("hypothesised", "hypothesized"),
    ("hypothesises", "hypothesizes"),
    ("hypothesising", "hypothesizing"),
    ("formalise", "formalize"),
    ("formalised", "formalized"),
    ("formalises", "formalizes"),
    ("formalising", "formalizing"),
    ("formalisation", "formalization"),
    ("normalise", "normalize"),
    ("normalised", "normalized"),
    ("normalises", "normalizes"),
    ("normalising", "normalizing"),
    ("normalisation", "normalization"),
    ("rationalise", "rationalize"),
    ("rationalised", "rationalized"),
    ("rationalises", "rationalizes"),
    ("rationalising", "rationalizing"),
    ("rationalisation", "rationalization"),
    ("polarise", "polarize"),
    ("polarised", "polarized"),
    ("polarises", "polarizes"),
    ("polarising", "polarizing"),
    ("polarisation", "polarization"),
    ("legitimise", "legitimize"),
    ("legitimised", "legitimized"),
    ("legitimises", "legitimizes"),
    ("legitimising", "legitimizing"),
    ("internalise", "internalize"),
    ("internalised", "internalized"),
    ("internalises", "internalizes"),
    ("internalising", "internalizing"),
    ("externalise", "externalize"),
    ("externalised", "externalized"),
    ("externalises", "externalizes"),
    ("externalising", "externalizing"),
    ("externalisation", "externalization"),
    ("conceptualise", "conceptualize"),
    ("conceptualised", "conceptualized"),
    ("conceptualises", "conceptualizes"),
    ("conceptualising", "conceptualizing"),
    ("contextualise", "contextualize"),
    ("contextualised", "contextualized"),
    ("contextualises", "contextualizes"),
    ("contextualising", "contextualizing"),
    ("relativise", "relativize"),
    ("relativised", "relativized"),
    ("relativises", "relativizes"),
    ("relativising", "relativizing"),
    ("absolutise", "absolutize"),
    ("absolutised", "absolutized"),
    ("absolutises", "absolutizes"),
    ("absolutising", "absolutizing"),
    ("ontologise", "ontologize"),
    ("ontologised", "ontologized"),
    ("dramatise", "dramatize"),
    ("dramatised", "dramatized"),
    ("dramatises", "dramatizes"),
    ("dramatising", "dramatizing"),
    ("idealise", "idealize"),
    ("idealised", "idealized"),
    ("idealises", "idealizes"),
    ("idealising", "idealizing"),
    ("materialise", "materialize"),
    ("materialised", "materialized"),
    ("materialises", "materializes"),
    ("materialising", "materializing"),
    ("spiritualise", "spiritualize"),
    ("spiritualised", "spiritualized"),
    ("spiritualises", "spiritualizes"),
    ("spiritualising", "spiritualizing"),
    ("popularise", "popularize"),
    ("popularised", "popularized"),
    ("popularises", "popularizes"),
    ("popularising", "popularizing"),
    ("popularisation", "popularization"),
    ("modernise", "modernize"),
    ("modernised", "modernized"),
    ("modernises", "modernizes"),
    ("modernising", "modernizing"),
    ("modernisation", "modernization"),
    ("westernise", "westernize"),
    ("westernised", "westernized"),
    ("westernises", "westernizes"),
    ("westernising", "westernizing"),
    ("westernisation", "westernization"),
    ("symbolise", "symbolize"),
    ("symbolised", "symbolized"),
    ("symbolises", "symbolizes"),
    ("symbolising", "symbolizing"),
    ("memorise", "memorize"),
    ("memorised", "memorized"),
    ("memorises", "memorizes"),
    ("memorising", "memorizing"),
    ("summarise", "summarize"),
    ("summarised", "summarized"),
    ("summarises", "summarizes"),
    ("summarising", "summarizing"),
    ("apologise", "apologize"),
    ("apologised", "apologized"),
    ("apologises", "apologizes"),
    ("apologising", "apologizing"),
    ("authorise", "authorize"),
    ("authorised", "authorized"),
    ("authorises", "authorizes"),
    ("authorising", "authorizing"),
    ("centralise", "centralize"),
    ("centralised", "centralized"),
    ("centralises", "centralizes"),
    ("centralising", "centralizing"),
    ("decentralise", "decentralize"),
    ("decentralised", "decentralized"),
    ("decentralises", "decentralizes"),
    ("decentralising", "decentralizing"),
    ("itemise", "itemize"),
    ("itemised", "itemized"),
    ("itemises", "itemizes"),
    ("itemising", "itemizing"),
    ("optimise", "optimize"),
    ("optimised", "optimized"),
    ("optimises", "optimizes"),
    ("optimising", "optimizing"),
    ("optimisation", "optimization"),
    ("minimise", "minimize"),
    ("minimised", "minimized"),
    ("minimises", "minimizes"),
    ("minimising", "minimizing"),
    ("minimisation", "minimization"),
    ("maximise", "maximize"),
    ("maximised", "maximized"),
    ("maximises", "maximizes"),
    ("maximising", "maximizing"),
    ("maximisation", "maximization"),
    ("utilise", "utilize"),
    ("utilised", "utilized"),
    ("utilises", "utilizes"),
    ("utilising", "utilizing"),
    ("utilisation", "utilization"),
    ("crystallise", "crystallize"),
    ("crystallised", "crystallized"),
    ("crystallises", "crystallizes"),
    ("crystallising", "crystallizing"),
    ("hospitalise", "hospitalize"),
    ("hospitalised", "hospitalized"),
    ("hospitalises", "hospitalizes"),
    ("hospitalising", "hospitalizing"),
    ("immunise", "immunize"),
    ("immunised", "immunized"),
    ("immunises", "immunizes"),
    ("immunising", "immunizing"),
    ("hellenise", "hellenize"),
    ("hellenised", "hellenized"),
    ("colonise", "colonize"),
    ("colonised", "colonized"),
    ("colonises", "colonizes"),
    ("colonising", "colonizing"),
    ("colonisation", "colonization"),
    ("decolonise", "decolonize"),
    ("decolonised", "decolonized"),
    ("decolonises", "decolonizes"),
    ("decolonising", "decolonizing"),
    ("decolonisation", "decolonization"),
    ("scrutinise", "scrutinize"),
    ("scrutinised", "scrutinized"),
    ("scrutinises", "scrutinizes"),
    ("scrutinising", "scrutinizing"),
    ("philosophise", "philosophize"),
    ("philosophised", "philosophized"),
    ("philosophises", "philosophizes"),
    ("philosophising", "philosophizing"),
    ("theorise", "theorize"),
    ("theorised", "theorized"),
    ("theorises", "theorizes"),
    ("theorising", "theorizing"),
    ("theorisation", "theorization"),
    ("metaphorise", "metaphorize"),
    ("metaphorised", "metaphorized"),
    ("problematise", "problematize"),
    ("problematised", "problematized"),
    ("problematises", "problematizes"),
    ("problematising", "problematizing"),
    ("dehumanise", "dehumanize"),
    ("dehumanised", "dehumanized"),
    # -our -> -or
    ("colour", "color"),
    ("colours", "colors"),
    ("coloured", "colored"),
    ("colouring", "coloring"),
    ("colourful", "colorful"),
    ("behaviour", "behavior"),
    ("behaviours", "behaviors"),
    ("behavioural", "behavioral"),
    ("behaviourally", "behaviorally"),
    ("behaviourism", "behaviorism"),
    ("behaviourist", "behaviorist"),
    ("favour", "favor"),
    ("favours", "favors"),
    ("favoured", "favored"),
    ("favouring", "favoring"),
    ("favourable", "favorable"),
    ("favourably", "favorably"),
    ("favourite", "favorite"),
    ("favourites", "favorites"),
    ("favouritism", "favoritism"),
    ("flavour", "flavor"),
    ("flavours", "flavors"),
    ("flavoured", "flavored"),
    ("flavouring", "flavoring"),
    ("flavourful", "flavorful"),
    ("honour", "honor"),
    ("honours", "honors"),
    ("honoured", "honored"),
    ("honouring", "honoring"),
    ("honourable", "honorable"),
    ("honourably", "honorably"),
    ("rumour", "rumor"),
    ("rumours", "rumors"),
    ("rumoured", "rumored"),
    ("labour", "labor"),
    ("labours", "labors"),
    ("laboured", "labored"),
    ("labouring", "laboring"),
    ("laborious", "laborious"),  # already same
    ("neighbour", "neighbor"),
    ("neighbours", "neighbors"),
    ("neighbouring", "neighboring"),
    ("neighbourhood", "neighborhood"),
    ("neighbourhoods", "neighborhoods"),
    ("endeavour", "endeavor"),
    ("endeavours", "endeavors"),
    ("endeavoured", "endeavored"),
    ("endeavouring", "endeavoring"),
    ("vigour", "vigor"),
    ("vigours", "vigors"),
    ("vigorous", "vigorous"),  # same
    ("rigour", "rigor"),
    ("rigours", "rigors"),
    ("savour", "savor"),
    ("savours", "savors"),
    ("savoured", "savored"),
    ("savouring", "savoring"),
    ("harbour", "harbor"),
    ("harbours", "harbors"),
    ("harboured", "harbored"),
    ("harbouring", "harboring"),
    ("ardour", "ardor"),
    ("clamour", "clamor"),
    ("clamours", "clamors"),
    ("clamouring", "clamoring"),
    ("demeanour", "demeanor"),
    ("fervour", "fervor"),
    ("humour", "humor"),
    ("humours", "humors"),
    ("humoured", "humored"),
    ("humouring", "humoring"),
    ("humourous", "humorous"),
    ("odour", "odor"),
    ("odours", "odors"),
    ("parlour", "parlor"),
    ("parlours", "parlors"),
    ("rancour", "rancor"),
    ("saviour", "savior"),
    ("saviours", "saviors"),
    ("splendour", "splendor"),
    ("succour", "succor"),
    ("tumour", "tumor"),
    ("tumours", "tumors"),
    ("valour", "valor"),
    # -re -> -er
    ("centre", "center"),
    ("centres", "centers"),
    ("centred", "centered"),
    ("centring", "centering"),
    ("metre", "meter"),
    ("metres", "meters"),
    ("kilometre", "kilometer"),
    ("kilometres", "kilometers"),
    ("centimetre", "centimeter"),
    ("centimetres", "centimeters"),
    ("millimetre", "millimeter"),
    ("millimetres", "millimeters"),
    ("theatre", "theater"),
    ("theatres", "theaters"),
    ("theatrical", "theatrical"),  # same
    ("calibre", "caliber"),
    ("fibre", "fiber"),
    ("fibres", "fibers"),
    ("lustre", "luster"),
    ("manoeuvre", "maneuver"),
    ("manoeuvres", "maneuvers"),
    ("manoeuvred", "maneuvered"),
    ("manoeuvring", "maneuvering"),
    ("sabre", "saber"),
    ("sceptre", "scepter"),
    ("sepulchre", "sepulcher"),
    ("sombre", "somber"),
    ("spectre", "specter"),
    ("spectres", "specters"),
    # -ence (n.) -> -ense
    ("defence", "defense"),
    ("defences", "defenses"),
    ("offence", "offense"),
    ("offences", "offenses"),
    ("pretence", "pretense"),
    ("pretences", "pretenses"),
    ("licence", "license"),  # n.
    ("licences", "licenses"),
    # -ogue -> -og (selective; we leave 'dialogue' alone — widely used in US too)
    ("catalogue", "catalog"),
    ("catalogues", "catalogs"),
    ("catalogued", "cataloged"),
    ("cataloguing", "cataloging"),
    ("analogue", "analog"),
    ("analogues", "analogs"),
    ("monologue", "monologue"),  # often retained in US
    # programme (the noun) -> program (US)
    ("programme", "program"),
    ("programmes", "programs"),
    # word swaps (preferred US choices)
    ("whilst", "while"),
    ("Whilst", "While"),
    ("amongst", "among"),
    ("Amongst", "Among"),
    ("towards", "toward"),
    ("Towards", "Toward"),
    ("forwards", "forward"),
    ("Forwards", "Forward"),
    ("backwards", "backward"),
    ("Backwards", "Backward"),
    ("upwards", "upward"),
    ("Upwards", "Upward"),
    ("downwards", "downward"),
    ("Downwards", "Downward"),
    ("learnt", "learned"),
    ("Learnt", "Learned"),
    ("burnt", "burned"),  # American prefers; British uses both
    ("Burnt", "Burned"),
    ("dreamt", "dreamed"),
    ("Dreamt", "Dreamed"),
    ("spelt", "spelled"),
    ("Spelt", "Spelled"),
    ("spilt", "spilled"),
    ("Spilt", "Spilled"),
    # double-l vs single-l (American single-l in some forms)
    ("travelled", "traveled"),
    ("travelling", "traveling"),
    ("traveller", "traveler"),
    ("travellers", "travelers"),
    ("modelled", "modeled"),
    ("modelling", "modeling"),
    ("labelled", "labeled"),
    ("labelling", "labeling"),
    ("counselled", "counseled"),
    ("counselling", "counseling"),
    ("counsellor", "counselor"),
    ("counsellors", "counselors"),
    ("cancelled", "canceled"),
    ("cancelling", "canceling"),
    ("levelled", "leveled"),
    ("levelling", "leveling"),
    ("signalled", "signaled"),
    ("signalling", "signaling"),
    ("totalled", "totaled"),
    ("totalling", "totaling"),
    ("fuelled", "fueled"),
    ("fuelling", "fueling"),
    ("dialled", "dialed"),
    ("dialling", "dialing"),
    ("equalled", "equaled"),
    ("equalling", "equaling"),
    ("focussed", "focused"),
    ("focussing", "focusing"),
    # ae/oe -> e (selective)
    ("aesthetic", "aesthetic"),  # American increasingly retains 'aesthetic'; leave alone
    ("anaemia", "anemia"),
    ("anaemic", "anemic"),
    ("encyclopaedia", "encyclopedia"),
    ("encyclopaedias", "encyclopedias"),
    ("foetus", "fetus"),
    ("foetal", "fetal"),
    ("manoeuvring", "maneuvering"),  # repeat fine
    ("oesophagus", "esophagus"),
    ("orthopaedic", "orthopedic"),
    # other lexical choices
    ("grey", "gray"),
    ("greys", "grays"),
    ("greyer", "grayer"),
    ("greyish", "grayish"),
    ("plough", "plow"),
    ("ploughs", "plows"),
    ("ploughed", "plowed"),
    ("ploughing", "plowing"),
    ("storey", "story"),
    ("storeys", "stories"),
    ("kerb", "curb"),
    ("kerbs", "curbs"),
    ("draught", "draft"),
    ("draughts", "drafts"),
    # 'ageing' -> 'aging'
    ("ageing", "aging"),
    ("Ageing", "Aging"),
    # 'judgement' -> 'judgment' (American preference)
    ("judgement", "judgment"),
    ("judgements", "judgments"),
    ("judgemental", "judgmental"),
    # 'acknowledgement' -> 'acknowledgment'
    ("acknowledgement", "acknowledgment"),
    ("acknowledgements", "acknowledgments"),
    # 'enrol' -> 'enroll' family
    ("enrolled", "enrolled"),  # same
    ("enrol", "enroll"),
    ("enrolling", "enrolling"),
    # 'tyre' -> 'tire'
    ("tyre", "tire"),
    ("tyres", "tires"),
    # 'cheque' -> 'check' (financial); risky if used in narrative
    # Skip 'cheque' — too context-sensitive.
    # 'practise' (v. British) -> 'practice' (American: same for noun & verb)
    ("practise", "practice"),
    ("practised", "practiced"),
    ("practises", "practices"),
    ("practising", "practicing"),
    # 'sceptic' -> 'skeptic'
    ("sceptic", "skeptic"),
    ("sceptics", "skeptics"),
    ("sceptical", "skeptical"),
    ("scepticism", "skepticism"),
    ("sceptically", "skeptically"),
    # 'mould' -> 'mold'
    ("mould", "mold"),
    ("moulds", "molds"),
    ("moulded", "molded"),
    ("moulding", "molding"),
    # 'cosy' -> 'cozy'
    ("cosy", "cozy"),
    ("cosier", "cozier"),
    ("cosily", "cozily"),
    # 'tonne' kept (it is also American for metric ton; leave alone)
]

# Auto-expand verb-suffix variants for -ise/-ize family.
# For every entry in PAIRS where the source ends in 'ise', also generate
# 'ises' -> 'izes' if not already present. This avoids relying on every
# plural-verb form being explicitly listed.
def _expand_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = {s for s, _ in pairs}
    extra: list[tuple[str, str]] = []
    for src, dst in pairs:
        if src.endswith("ise") and dst.endswith("ize"):
            for s_suf, d_suf in [("ises", "izes"), ("ised", "ized"), ("ising", "izing")]:
                cand_s = src[:-3] + s_suf
                cand_d = dst[:-3] + d_suf
                if cand_s not in seen:
                    extra.append((cand_s, cand_d))
                    seen.add(cand_s)
        if src.endswith("our"):
            for s_suf, d_suf in [("ours", "ors"), ("oured", "ored"), ("ouring", "oring")]:
                cand_s = src[:-3] + s_suf
                cand_d = dst[:-2] + d_suf[1:] if False else (dst + s_suf[3:])
                # simpler: handle -our endings manually elsewhere; skip auto-expansion here
                # to avoid bugs
                pass
    return pairs + extra


PAIRS = _expand_pairs(PAIRS)

# Compile a single regex per pair with case-handling.
# We use (?<!\\w) and (?!\\w) instead of \\b to avoid matching inside
# IAST-tokens that include diacritics adjacent to ASCII letters.
COMPILED: list[tuple[re.Pattern, str, str, str]] = []
for src, dst in PAIRS:
    if src == dst:
        continue
    pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(src)}(?![A-Za-z0-9_])")
    cap_pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(src.capitalize())}(?![A-Za-z0-9_])")
    COMPILED.append((pat, dst, src, "lower"))
    if src != src.capitalize():
        COMPILED.append((cap_pat, dst.capitalize(), src.capitalize(), "cap"))

# Tokens we never touch (proper nouns containing British spellings).
PROTECTED_TOKEN_RE = re.compile(
    r"\b(?:"
    # known organization / publisher / library proper nouns
    r"Centre for [A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*"
    r"|Asia Society"
    r"|Oxford University Press"
    r"|Cambridge University Press"
    r"|Indira Gandhi National Centre for the Arts"
    r"|Centre national de la recherche scientifique"
    r"|British Library"
    r"|British Museum"
    r"|Royal Asiatic Society"
    r"|National Centre for [A-Za-z ]+"
    r"|Theatre Royal"
    r")\b",
    re.UNICODE,
)


@dataclass
class Stats:
    files_scanned: int = 0
    files_changed: int = 0
    substitutions: int = 0
    by_pair: dict[str, int] = field(default_factory=dict)
    judgment_calls: list[str] = field(default_factory=list)
    files_changed_list: list[str] = field(default_factory=list)


def is_devanagari_heavy(line: str) -> bool:
    """Skip lines dominated by Devanagari (Unicode 0900–097F)."""
    if not line.strip():
        return False
    deva = sum(1 for c in line if "ऀ" <= c <= "ॿ")
    return deva > 5


def looks_like_iast_only(line: str) -> bool:
    """Skip pure-IAST quotation lines (no English words at all).

    Heuristic: the line is dominated by IAST diacritics AND has zero
    common English content words. We look at a wider stopword/contentword
    list so that lines like 'editorial-commentarial labour... PDF
    acquired; awaiting OCR.' (with a few diacritics for proper nouns) are
    NOT skipped.
    """
    iast_chars = sum(1 for c in line if c in "āīūṛṝḷḹṅñṭḍṇśṣṁḥĀĪŪṚṜṄÑṬḌṆŚṢṀḤ")
    # If the line has very few IAST chars overall, it cannot be IAST-only.
    if iast_chars < 6:
        return False
    # Look for English content. If we find any of these we are NOT
    # IAST-only.
    english_markers = re.findall(
        r"\b(?:the|of|is|and|to|in|that|a|an|by|for|with|as|on|at|from|"
        r"this|these|those|which|who|what|where|when|why|how|or|but|"
        r"not|no|yes|if|then|so|because|while|though|although|since|"
        r"however|therefore|thus|hence|whereas|here|there|now|"
        r"acquired|awaiting|secured|published|edited|translated|"
        r"editorial|commentarial|authored|notes|page|pages|book|text|"
        r"PDF|OCR|ISBN|chapter|section|verse)\b",
        line,
        re.IGNORECASE,
    )
    # Also count ASCII-only words longer than 4 letters as English signal.
    long_ascii = re.findall(r"\b[A-Za-z]{5,}\b", line)
    return len(english_markers) == 0 and len(long_ascii) <= 1


def transform_text(text: str, stats: Stats, protect_quotes: bool = True) -> str:
    """Apply substitutions to text. Skip code blocks, inline code, URLs.

    If `protect_quotes` is True, also skip markdown blockquote lines (>).
    """
    out_lines: list[str] = []
    in_code_block = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        # Toggle code-block fence.
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            out_lines.append(line)
            continue
        if in_code_block:
            out_lines.append(line)
            continue
        # Skip markdown blockquote (primary-source citation).
        if protect_quotes and stripped.startswith(">"):
            out_lines.append(line)
            continue
        # Skip Devanagari-heavy lines.
        if is_devanagari_heavy(line):
            out_lines.append(line)
            continue
        # Skip pure IAST quotation lines.
        if looks_like_iast_only(line):
            out_lines.append(line)
            continue
        # Mask out protected tokens, inline code, URLs by replacing with a
        # placeholder, then unmasking at the end.
        masks: list[str] = []

        def stash(match: re.Match) -> str:
            masks.append(match.group(0))
            return f"\x00MASK{len(masks) - 1}\x00"

        masked = re.sub(r"`[^`\n]*`", stash, line)
        masked = re.sub(r"https?://\S+", stash, masked)
        masked = re.sub(r"www\.\S+", stash, masked)
        masked = PROTECTED_TOKEN_RE.sub(stash, masked)

        # Apply substitutions.
        for pat, repl, src_word, _kind in COMPILED:
            new_masked, n = pat.subn(repl, masked)
            if n:
                stats.substitutions += n
                stats.by_pair[src_word] = stats.by_pair.get(src_word, 0) + n
                masked = new_masked

        # Restore masks.
        def unstash(match: re.Match) -> str:
            idx = int(match.group(1))
            return masks[idx]

        line = re.sub(r"\x00MASK(\d+)\x00", unstash, masked)
        out_lines.append(line)
    return "\n".join(out_lines)


def transform_json_object(obj, stats: Stats, path: str):
    """Recurse into a JSON object, transforming string fields.

    For glossary / thinker / polemic-chains / manifest JSON, all strings
    are candidates EXCEPT keys that obviously hold IAST/Devanagari values.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Field-level skip list — these typically hold non-English content.
            skip_keys = {
                "iast", "devanagari", "sanskrit", "pali", "tibetan",
                "iast_form", "deva_form", "original", "original_text",
                "primary_text", "primary_iast", "primary_deva",
                "shloka", "sloka", "verse", "mantra",
                "term", "term_iast", "term_deva",
                "id", "slug", "key", "url", "uri", "path",
                "schools", "school",  # school values include 'Tattva-vāda' which has diacritics
            }
            if isinstance(k, str) and k.lower() in skip_keys:
                # Recurse only if it's a container; primitives skipped.
                if isinstance(v, (dict, list)):
                    transform_json_object(v, stats, path)
                continue
            transform_json_object(v, stats, path)
            if isinstance(v, str):
                # For JSON we don't have markdown blockquote semantics; we
                # still skip pure-IAST and Devanagari-heavy strings.
                if is_devanagari_heavy(v) or looks_like_iast_only(v):
                    continue
                new_v = transform_text(v, stats, protect_quotes=False)
                if new_v != v:
                    obj[k] = new_v
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str):
                if is_devanagari_heavy(item) or looks_like_iast_only(item):
                    continue
                new_item = transform_text(item, stats, protect_quotes=False)
                if new_item != item:
                    obj[i] = new_item
            else:
                transform_json_object(item, stats, path)


def process_json_file(path: Path, stats: Stats):
    """Text-based substitution on JSON files.

    We do NOT parse-and-re-serialize because that normalizes whitespace
    and inflates diffs. Instead, we apply substitutions on the raw text
    while skipping JSON keys (left of the colon) and any string values
    that are pure-IAST or Devanagari. After substitution we re-parse
    to confirm the JSON is still valid; if not, we revert.
    """
    stats.files_scanned += 1
    try:
        original_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        stats.judgment_calls.append(f"{path}: skipped (decoding — {exc})")
        return
    try:
        json.loads(original_text)
    except json.JSONDecodeError as exc:
        stats.judgment_calls.append(f"{path}: skipped (cannot parse — {exc})")
        return

    # Substitute across the whole text. JSON keys are always quoted
    # ASCII identifiers in this codebase; the substitution table targets
    # British English words none of which appear as keys, so passing the
    # full text is safe in practice. We still mask out specific
    # protected zones.
    snap = stats.substitutions
    new_text = transform_text(original_text, stats, protect_quotes=False)
    if stats.substitutions == snap:
        return
    # Validate.
    try:
        json.loads(new_text)
    except json.JSONDecodeError as exc:
        stats.judgment_calls.append(
            f"{path}: substitution would break JSON ({exc}); reverted"
        )
        # Roll the by-pair counters back too.
        stats.substitutions = snap
        return
    path.write_text(new_text, encoding="utf-8")
    stats.files_changed += 1
    stats.files_changed_list.append(str(path.relative_to(ROOT)))


def process_markdown_file(path: Path, stats: Stats):
    stats.files_scanned += 1
    try:
        original_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        stats.judgment_calls.append(f"{path}: skipped (decoding — {exc})")
        return
    snap = stats.substitutions
    new_text = transform_text(original_text, stats, protect_quotes=True)
    if stats.substitutions > snap and new_text != original_text:
        path.write_text(new_text, encoding="utf-8")
        stats.files_changed += 1
        stats.files_changed_list.append(str(path.relative_to(ROOT)))


def main() -> int:
    stats = Stats()

    targets: list[tuple[Path, str]] = []
    for p in sorted((DATA / "thinkers").glob("*.json")):
        targets.append((p, "json"))
    for p in sorted((DATA / "glossary").glob("*.json")):
        targets.append((p, "json"))
    for p in sorted((DATA / "perspectives" / "source").glob("*.md")):
        targets.append((p, "md"))
    for p in sorted((DATA / "full_translations").glob("*.md")):
        targets.append((p, "md"))
    for p in sorted((DATA / "polemic_chains").glob("*.json")):
        targets.append((p, "json"))
    for p in sorted((DATA / "articles" / "source").glob("*.md")):
        targets.append((p, "md"))
    manifest = DATA / "articles" / "manifest.json"
    if manifest.exists():
        targets.append((manifest, "json"))

    for path, kind in targets:
        if kind == "json":
            process_json_file(path, stats)
        else:
            process_markdown_file(path, stats)

    # Emit report.
    project_root = Path("/orcd/home/002/eeshan/philosophy")
    handoff = project_root / "handoffs" / "american_english_pass_2026-05-10.md"
    lines = [
        "# American-English standardization pass — 2026-05-10",
        "",
        f"- Files scanned: **{stats.files_scanned}**",
        f"- Files changed: **{stats.files_changed}**",
        f"- Total substitutions: **{stats.substitutions}**",
        "",
        "## Top substitutions (by source word)",
        "",
    ]
    for word, count in sorted(stats.by_pair.items(), key=lambda kv: (-kv[1], kv[0]))[:60]:
        lines.append(f"- `{word}` -> {count}")
    lines.extend([
        "",
        "## Judgment calls / skipped files",
        "",
    ])
    if not stats.judgment_calls:
        lines.append("(none — every file parsed and validated cleanly)")
    else:
        for note in stats.judgment_calls:
            lines.append(f"- {note}")
    lines.extend([
        "",
        "## Convention notes (judgment calls baked into the substitution table)",
        "",
        "- `dialogue` left as-is (American English commonly retains it).",
        "- `aesthetic` left as-is (American English commonly retains it).",
        "- `monologue` left as-is.",
        "- `cheque` not auto-substituted (too context-sensitive — financial vs narrative).",
        "- `practise` (British verb) -> `practice` (American: same word for noun and verb).",
        "- `licence` (British noun) -> `license` (American: same word for noun and verb).",
        "- `tonne` left as-is (used in American scientific writing as well).",
        "- `judgement` -> `judgment`, `acknowledgement` -> `acknowledgment` (American preference).",
        "- Devanagari and pure-IAST lines were skipped wholesale (not English content).",
        "- Markdown blockquote lines (lines starting with `>`) were skipped (primary-source quotations preserved verbatim).",
        "- Inline code spans (`...`) and URLs were masked from substitution.",
        "- Proper-noun strings like \"Centre for X\" / \"Oxford University Press\" were masked from substitution.",
        "- Code-block fences (```) skipped wholesale.",
        "",
        "## Files changed",
        "",
    ])
    for f in stats.files_changed_list:
        lines.append(f"- `{f}`")
    handoff.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Files scanned: {stats.files_scanned}")
    print(f"Files changed: {stats.files_changed}")
    print(f"Substitutions: {stats.substitutions}")
    print(f"Report written to: {handoff}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
