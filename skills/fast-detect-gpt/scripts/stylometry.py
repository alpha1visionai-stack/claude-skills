#!/usr/bin/env python3
"""
Fast-DetectGPT Stylometric & Structural Analysis Module
Provides rule-based and statistical heuristics (Burstiness, AI-Slop, Structure Analysis)
to complement Fast-DetectGPT's probability curvature.
"""

import re
import numpy as np
from typing import List, Dict, Any

# Common German & English AI-Slop patterns
AI_INTRO_PATTERNS_DE = [
    r"\bIn der heutigen (?:dynamischen|schnelllebigen|digitalen|modernen) Welt\b",
    r"\bIn einer (?:Zeit|Ära|Welt), in der\b",
    r"\bIn Zeiten von\b",
    r"\bEs ist wichtig zu (?:beachten|betonen|verstehen|erwähnen)\b",
    r"\bDie Frage,? ob .+?, ist von zentraler Bedeutung\b",
    r"\bIm Zuge der zunehmenden (?:Digitalisierung|Globalisierung|Entwicklung)\b",
]

AI_INTRO_PATTERNS_EN = [
    r"\bIn today'?s (?:fast-paced|dynamic|digital|rapidly changing) world\b",
    r"\bIn an era (?:where|of)\b",
    r"\bIt is (?:crucial|essential|important) to (?:note|understand|highlight)\b",
    r"\bIn the ever-evolving landscape of\b",
]

AI_CONNECTORS_DE = [
    r"\bdarüber hinaus\b",
    r"\bdes Weiteren\b",
    r"\bnichtsdestotrotz\b",
    r"\bnichtsdestoweniger\b",
    r"\bzusammenfassend lässt sich sagen\b",
    r"\bschliesslich und letztlich\b",
    r"\bein weiterer wichtiger Aspekt ist\b",
    r"\bhinzu kommt,? dass\b",
    r"\bzusätzlich zu\b",
    r"\bes lässt sich festhalten,? dass\b",
]

AI_CONNECTORS_EN = [
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bnonetheless\b",
    r"\bnevertheless\b",
    r"\bin summary\b",
    r"\bto sum up\b",
    r"\bit is worth noting that\b",
    r"\banother key aspect is\b",
    r"\bin conclusion\b",
]

AI_BUZZWORDS_DE = [
    r"\bbahnbrechend(?:e[rnms]?)?\b",
    r"\brevolutionär(?:e[rnms]?)?\b",
    r"\btiefgreifend(?:e[rnms]?)?\b",
    r"\bMeilenstein(?:e[ns]?)?\b",
    r"\bParadigmenwechsel(?:s)?\b",
    r"\bmaßgeblich(?:e[rnms]?)?\b",
    r"\bganzheitlich(?:e[rnms]?)?\b",
    r"\bwegweisend(?:e[rnms]?)?\b",
    r"\bunabdingbar(?:e[rnms]?)?\b",
    r"\bLeuchtturmprojekt(?:e[ns]?)?\b",
    r"\bSynergieeffekt(?:e[ns]?)?\b",
    r"\bFacettenreichtum\b",
    r"\bTransformationsprozess(?:e[ns]?)?\b",
]

AI_BUZZWORDS_EN = [
    r"\bgroundbreaking\b",
    r"\brevolutionary\b",
    r"\bpivotal\b",
    r"\bmilestone\b",
    r"\bparadigm shift\b",
    r"\bholistic\b",
    r"\bseamless(?:ly)?\b",
    r"\bgame-changer\b",
    r"\btestament to\b",
    r"\bdelve into\b",
    r"\btapestry of\b",
    r"\bbeacon of\b",
]

AI_CONCLUSION_PATTERNS_DE = [
    r"\bSchlussendlich (?:bleibt|zeigt sich|lässt sich)\b",
    r"\bZusammenfassend lässt sich (?:konstatieren|festhalten|sagen)\b",
    r"\bFazit:?\b",
    r"\bAlles in allem zeigt sich\b",
    r"\bAbschließend lässt sich festhalten\b",
]

def split_into_sentences(text: str) -> List[str]:
    """Splits text into sentences while respecting common German/English abbreviations."""
    # Temporarily protect common abbreviations
    protected = text
    abbrevs = [
        "z.B.", "z. B.", "bzw.", "d.h.", "d. h.", "u.a.", "u. a.", "ca.", "Dr.", "Prof.",
        "e.g.", "i.e.", "etc.", "vs.", "al.", "Nr.", "Abb.", "Tab.", "S."
    ]
    replacements = {}
    for i, abbr in enumerate(abbrevs):
        placeholder = f"__ABBR_{i}__"
        replacements[placeholder] = abbr
        protected = protected.replace(abbr, placeholder)

    # Split on sentence terminators followed by whitespace or quote
    raw_sentences = re.split(r'(?<=[.!?])\s+', protected)
    
    sentences = []
    for s in raw_sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        # Restore abbreviations
        for placeholder, abbr in replacements.items():
            s_clean = s_clean.replace(placeholder, abbr)
        # Skip pure headers or bullet marks
        words = [w for w in re.findall(r'\b\w+\b', s_clean) if not w.isdigit()]
        if len(words) >= 3:
            sentences.append(s_clean)
            
    return sentences

def analyze_burstiness(text: str) -> Dict[str, Any]:
    """
    Computes sentence length metrics and Burstiness (variance in rhythm and sentence length).
    High CV (Coefficient of Variation >= 0.55): Typically human (lively mix of short and long sentences).
    Low CV (CV < 0.35): Typical AI pattern (monotone sentences around 15-22 words).
    """
    sentences = split_into_sentences(text)
    if not sentences or len(sentences) < 2:
        return {
            "sentence_count": len(sentences),
            "mean_length": 0.0,
            "median_length": 0.0,
            "std_length": 0.0,
            "cv": 0.0,
            "min_length": 0,
            "max_length": 0,
            "verdict": "Zu kurz für Burstiness-Berechnung",
            "score_penalty": 0.0
        }

    lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    mean_l = float(np.mean(lengths))
    median_l = float(np.median(lengths))
    std_l = float(np.std(lengths))
    cv = float(std_l / mean_l) if mean_l > 0 else 0.0

    # Verdict based on empirical stylometric thresholds
    if cv >= 0.55:
        verdict = "🟢 Hohe Varianz (Sehr lebendiger, menschlicher Satzrhythmus)"
        penalty = -0.15  # Lowers AI probability
    elif cv >= 0.38:
        verdict = "🟡 Moderate Varianz (Ausgewogene Satzlängen)"
        penalty = 0.0
    else:
        verdict = "🔴 Geringe Varianz / Monoton (Starre, maschinenartige Taktung)"
        penalty = +0.20  # Increases AI probability

    return {
        "sentence_count": len(sentences),
        "mean_length": mean_l,
        "median_length": median_l,
        "std_length": std_l,
        "cv": cv,
        "min_length": int(np.min(lengths)),
        "max_length": int(np.max(lengths)),
        "verdict": verdict,
        "score_penalty": penalty
    }

def analyze_slop_and_phrases(text: str) -> Dict[str, Any]:
    """Scans for AI-Slop phrases, recurring fillers, buzzwords, and stereotypical connectors."""
    findings = []
    
    categories = [
        ("Einleitungsfloskel (DE)", AI_INTRO_PATTERNS_DE, 1.5),
        ("Einleitungsfloskel (EN)", AI_INTRO_PATTERNS_EN, 1.5),
        ("Stereotyper Konnektor (DE)", AI_CONNECTORS_DE, 0.8),
        ("Stereotyper Konnektor (EN)", AI_CONNECTORS_EN, 0.8),
        ("KI-Schlagwort / Buzzword (DE)", AI_BUZZWORDS_DE, 0.6),
        ("KI-Schlagwort / Buzzword (EN)", AI_BUZZWORDS_EN, 0.6),
        ("Formelhaftes Fazit (DE)", AI_CONCLUSION_PATTERNS_DE, 1.2),
    ]

    total_slop_weight = 0.0
    lines = text.split("\n")

    for cat_name, pattern_list, weight in categories:
        for pat in pattern_list:
            regex = re.compile(pat, re.IGNORECASE)
            for line_idx, line in enumerate(lines, start=1):
                for match in regex.finditer(line):
                    matched_text = match.group(0)
                    total_slop_weight += weight
                    # Extract small context snippet
                    start = max(0, match.start() - 30)
                    end = min(len(line), match.end() + 30)
                    snippet = line[start:end].strip()
                    findings.append({
                        "category": cat_name,
                        "phrase": matched_text,
                        "line": line_idx,
                        "context": snippet,
                        "weight": weight
                    })

    words_total = len(re.findall(r'\b\w+\b', text))
    density_per_1000 = (len(findings) / words_total * 1000.0) if words_total > 0 else 0.0

    if density_per_1000 >= 6.0:
        verdict = "🔴 Hohe Häufung von KI-Signalwörtern & Slop"
    elif density_per_1000 >= 2.0:
        verdict = "🟡 Vereinzelte typische KI-Floskeln"
    else:
        verdict = "🟢 Kaum / keine auffälligen KI-Floskeln"

    return {
        "findings": findings,
        "total_hits": len(findings),
        "total_slop_weight": total_slop_weight,
        "density_per_1000_words": density_per_1000,
        "verdict": verdict
    }

def analyze_structure(text: str) -> Dict[str, Any]:
    """Analyzes layout formatting, bullet-point density, and template architecture."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return {
            "bullet_ratio": 0.0,
            "bullet_count": 0,
            "total_lines": 0,
            "verdict": "Kein Text"
        }

    bullet_patterns = re.compile(r"^([\*\-\+•]|(?:\d+[\.\)]))\s+")
    bullet_lines = sum(1 for l in lines if bullet_patterns.match(l))
    bullet_ratio = (bullet_lines / len(lines)) * 100.0

    # Symmetry of paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    p_lengths = [len(p.split()) for p in paragraphs if len(p.split()) > 10]
    p_std = float(np.std(p_lengths)) if len(p_lengths) > 2 else 0.0

    if bullet_ratio >= 35.0:
        verdict = "🔴 Hohe Listen-Dichte (Ausgeprägter KI-Formatierungsdrang)"
    elif bullet_ratio >= 15.0:
        verdict = "🟡 Moderate Listen-Nutzung"
    else:
        verdict = "🟢 Natürlich strukturierter Fließtext"

    return {
        "total_lines": len(lines),
        "bullet_count": bullet_lines,
        "bullet_ratio_pct": bullet_ratio,
        "paragraph_count": len(paragraphs),
        "paragraph_length_std": p_std,
        "verdict": verdict
    }

def compute_hybrid_assessment(fast_detect_prob: float, burstiness_res: Dict[str, Any], slop_res: Dict[str, Any], structure_res: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combines Fast-DetectGPT mathematical curvature with stylometric and structural dimensions.
    Weights: Fast-DetectGPT (60%), Slop & Lexicon (25%), Burstiness & Structure (15%).
    """
    # 1. Base Probability from Fast-DetectGPT (0.0 to 1.0)
    prob_base = fast_detect_prob

    # 2. Slop Factor (0.0 to 1.0)
    # Density of 8+ per 1000 words scales to ~0.9
    slop_density = slop_res.get("density_per_1000_words", 0.0)
    slop_prob = min(1.0, max(0.0, (slop_density / 8.0)))

    # 3. Burstiness / Structure Factor (0.0 to 1.0)
    cv = burstiness_res.get("cv", 0.45)
    bullet_ratio = structure_res.get("bullet_ratio_pct", 0.0)

    # Low CV and high bullet ratio indicate AI
    struct_ai_signal = 0.5
    if cv > 0.0:
        # High CV (0.6+) -> signal ~ 0.1; Low CV (<0.3) -> signal ~ 0.85
        struct_ai_signal = max(0.05, min(0.95, 1.0 - (cv / 0.7)))
    if bullet_ratio > 30.0:
        struct_ai_signal = min(1.0, struct_ai_signal + 0.15)

    # Weighted composite score
    hybrid_prob = (0.60 * prob_base) + (0.25 * slop_prob) + (0.15 * struct_ai_signal)
    hybrid_pct = hybrid_prob * 100.0

    if hybrid_pct >= 75.0:
        verdict = "🔴 SEHR WAHRSCHEINLICH KI-GENERIERT"
    elif hybrid_pct >= 40.0:
        verdict = "🟡 GEMISCHT / TEILWEISE KI-UNTERSTÜTZT (HYBRID)"
    else:
        verdict = "🟢 SEHR WAHRSCHEINLICH MENSCHLICH VERFASST"

    return {
        "hybrid_probability_pct": hybrid_pct,
        "fast_detect_probability_pct": fast_detect_prob * 100.0,
        "slop_probability_pct": slop_prob * 100.0,
        "structure_probability_pct": struct_ai_signal * 100.0,
        "overall_verdict": verdict
    }
