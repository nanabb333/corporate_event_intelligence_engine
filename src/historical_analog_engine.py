#!/usr/bin/env python3
"""Deterministic historical analog engine for CEO departure cases."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "corporate_events_seed.csv"
RESULTS_PATH = ROOT / "outputs" / "sample_retrieval_results.json"
ANSWER_PATH = ROOT / "outputs" / "sample_ceo_departure_answer.md"

QUERY = "What usually happens after an abrupt CEO departure?"

QUERY_PROFILE = {
    "event_type": "CEO departure",
    "departure_type": "abrupt resignation",
    "sector": "",
    "context": (
        "abrupt resignation CEO departure investor pressure board pressure "
        "governance culture controversy crisis founder scrutiny"
    ),
    "observed_pathway": "governance repair",
}

STOPWORDS = {
    "a",
    "after",
    "an",
    "and",
    "as",
    "at",
    "by",
    "ceo",
    "company",
    "during",
    "for",
    "from",
    "in",
    "is",
    "of",
    "or",
    "the",
    "to",
    "under",
    "was",
    "what",
    "with",
}

TOKEN_ALIASES = {
    "abrupt": {"abrupt", "unexpected", "rapid", "immediate"},
    "pressure": {"pressure", "pressured", "investor", "activist", "board", "scrutiny"},
    "governance": {"governance", "board", "controls", "disclosure"},
    "crisis": {"crisis", "scandal", "controversy", "controversies", "regulatory", "safety"},
    "founder": {"founder", "founder-led"},
    "conduct": {"conduct", "misconduct", "policy", "investigation"},
    "performance": {"performance", "execution", "operating", "competitive", "strategic"},
}

PATHWAY_FAMILIES = {
    "governance enforcement": "accountability_repair",
    "governance repair": "accountability_repair",
    "reputational repair": "accountability_repair",
    "conduct accountability": "accountability_repair",
    "crisis accountability": "accountability_repair",
    "board-led reset": "leadership_reset",
    "operational reset": "leadership_reset",
    "strategic reset": "leadership_reset",
    "strategic acceleration": "leadership_reset",
    "portfolio reset": "leadership_reset",
    "continuity succession": "planned_continuity",
    "founder transition": "founder_transition",
    "interim founder return": "founder_transition",
}

TAG_LABELS = {
    "abrupt_pressure": "abrupt or pressure-driven exit",
    "founder": "founder leadership",
    "planned": "planned succession",
    "crisis": "crisis-linked departure",
    "conduct": "conduct-related departure",
    "performance": "performance-driven change",
    "board_action": "board action",
}


def normalize_label(value: str) -> str:
    return value.strip().lower().replace("_", " ")


def tokens(value: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z][a-zA-Z-]+", value.lower())
    normalized = set()
    for item in raw:
        if item in STOPWORDS:
            continue
        normalized.add(item)
        for alias, terms in TOKEN_ALIASES.items():
            if item in terms:
                normalized.add(alias)
    return normalized


def departure_tags(value: str) -> set[str]:
    text = normalize_label(value)
    tags = set()
    if any(term in text for term in ("abrupt", "resignation", "investor pressure", "board pressure")):
        tags.add("abrupt_pressure")
    if "founder" in text:
        tags.add("founder")
    if "planned" in text or "succession" in text:
        tags.add("planned")
    if "crisis" in text:
        tags.add("crisis")
    if "conduct" in text:
        tags.add("conduct")
    if "performance" in text:
        tags.add("performance")
    if "termination" in text or "replacement" in text:
        tags.add("board_action")
    return tags


def pathway_family(value: str) -> str:
    return PATHWAY_FAMILIES.get(normalize_label(value), "other")


def load_cases() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="") as handle:
        return list(csv.DictReader(handle))


def score_case(case: dict[str, str], profile: dict[str, str]) -> dict:
    case_departure = normalize_label(case["departure_type"])
    target_departure = normalize_label(profile["departure_type"])
    case_departure_tags = departure_tags(case_departure)
    target_departure_tags = departure_tags(target_departure)

    if case_departure == target_departure or case_departure.startswith(target_departure):
        departure_score = 35.0
    else:
        overlap = case_departure_tags & target_departure_tags
        departure_score = min(28.0, len(overlap) * 14.0)

    target_sector = normalize_label(profile.get("sector", ""))
    if target_sector:
        sector_score = 15.0 if normalize_label(case["sector"]) == target_sector else 0.0
    else:
        sector_score = 0.0

    context_terms = tokens(case["context"] + " " + case["departure_type"] + " " + case["analyst_note"])
    query_terms = tokens(profile["context"])
    overlap_terms = sorted(context_terms & query_terms)
    context_score = min(25.0, len(overlap_terms) * 3.5)

    target_pathway = normalize_label(profile["observed_pathway"])
    case_pathway = normalize_label(case["observed_pathway"])
    if case_pathway == target_pathway:
        pathway_score = 25.0
    elif pathway_family(case_pathway) == pathway_family(target_pathway):
        pathway_score = 16.0
    else:
        pathway_score = 0.0

    score = departure_score + sector_score + context_score + pathway_score
    selection_reasons = []
    if departure_score:
        overlap = sorted(case_departure_tags & target_departure_tags)
        if case_departure == target_departure or case_departure.startswith(target_departure):
            selection_reasons.append("departure type directly matches abrupt resignation")
        elif overlap:
            labels = [TAG_LABELS[tag] for tag in overlap]
            selection_reasons.append("departure type shares " + ", ".join(labels))
    if sector_score:
        selection_reasons.append("sector matches the query profile")
    if context_score:
        selection_reasons.append("context overlaps on " + ", ".join(overlap_terms[:6]))
    if pathway_score == 25.0:
        selection_reasons.append("observed pathway exactly matches governance repair")
    elif pathway_score:
        selection_reasons.append("observed pathway belongs to the same accountability or repair family")

    return {
        "event_id": case["event_id"],
        "company": case["company"],
        "ticker": case["ticker"],
        "sector": case["sector"],
        "event_date": case["event_date"],
        "departure_type": case["departure_type"],
        "observed_pathway": case["observed_pathway"],
        "source_url": case["source_url"],
        "analyst_note": case["analyst_note"],
        "score": round(score, 2),
        "score_components": {
            "departure_type": round(departure_score, 2),
            "sector": round(sector_score, 2),
            "context": round(context_score, 2),
            "observed_pathway": round(pathway_score, 2),
        },
        "selection_reasons": selection_reasons,
    }


def retrieve(top_n: int = 7) -> list[dict]:
    scored = [score_case(case, QUERY_PROFILE) for case in load_cases()]
    scored.sort(key=lambda item: (-item["score"], item["event_date"], item["event_id"]))
    return scored[:top_n]


def aggregate_pathways(results: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in results:
        groups[item["observed_pathway"]].append(item)

    output = []
    for pathway, cases in groups.items():
        output.append(
            {
                "pathway": pathway,
                "case_count": len(cases),
                "cases": [case["event_id"] for case in cases],
                "companies": [case["company"] for case in cases],
                "interpretation": pathway_interpretation(pathway),
            }
        )
    output.sort(key=lambda item: (-item["case_count"], item["pathway"]))
    return output


def pathway_interpretation(pathway: str) -> str:
    notes = {
        "governance repair": "Leadership change is part of repairing governance, culture, controls, or investor confidence.",
        "reputational repair": "The company uses leadership transition as one part of restoring public, customer, or stakeholder trust.",
        "crisis accountability": "CEO removal or resignation signals accountability during a major operational, safety, or regulatory crisis.",
        "board-led reset": "The board installs new leadership to reset credibility, direction, or execution discipline.",
        "conduct accountability": "The departure centers on policy enforcement and leadership standards.",
        "founder transition": "Founder leadership gives way to a successor while governance continuity remains a central issue.",
        "governance enforcement": "The board emphasizes investigation, process, and governance standards after conduct concerns.",
    }
    return notes.get(pathway, "The pathway describes an observed historical response pattern.")


def build_answer(results: list[dict], pathways: list[dict]) -> str:
    analog_lines = []
    why_lines = []
    evidence_lines = []
    analyst_lines = []

    for item in results:
        analog_lines.append(
            f"- {item['company']} ({item['ticker']}), {item['event_date']}: "
            f"{item['departure_type']}; pathway: {item['observed_pathway']}."
        )
        why_lines.append(
            f"- {item['company']}: score {item['score']} "
            f"({', '.join(item['selection_reasons'])})."
        )
        evidence_lines.append(f"- {item['company']}: {item['source_url']}")
        analyst_lines.append(f"- {item['company']}: {item['analyst_note']}")

    pathway_lines = [
        f"- {item['pathway']} ({item['case_count']} case"
        f"{'' if item['case_count'] == 1 else 's'}): {item['interpretation']}"
        for item in pathways
    ]

    return "\n".join(
        [
            "# Sample CEO Departure Analyst Brief",
            "",
            "## Question",
            "",
            QUERY,
            "",
            "## Historical Analogs",
            "",
            *analog_lines,
            "",
            "## Why These Cases Were Selected",
            "",
            *why_lines,
            "",
            "## Observed Pathways",
            "",
            *pathway_lines,
            "",
            "## Evidence Base",
            "",
            *evidence_lines,
            "",
            "## Analyst Notes",
            "",
            *analyst_lines,
            "",
            "## Limitations",
            "",
            "- This brief describes historical CEO departure cases and observed corporate pathways.",
            "- It does not forecast future company performance.",
            "- It does not provide investment recommendations, stock predictions, ratings, or price targets.",
            "- The retrieval result is deterministic and depends on the current Sprint 1 case library.",
            "",
        ]
    )


def main() -> None:
    results = retrieve()
    pathways = aggregate_pathways(results)
    payload = {
        "question": QUERY,
        "query_profile": QUERY_PROFILE,
        "scoring_framework": {
            "departure_type": "0-35 points for exact or related departure-type signals",
            "sector": "0-15 points when a sector is specified and matches",
            "context": "0-25 points from deterministic keyword overlap",
            "observed_pathway": "0-25 points for exact or pathway-family match",
        },
        "retrieved_cases": results,
        "observed_pathways": pathways,
        "limitations": [
            "descriptive historical retrieval only",
            "no forecasting",
            "no investment recommendations",
            "no stock prediction",
            "no price targets",
        ],
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    ANSWER_PATH.write_text(build_answer(results, pathways))


if __name__ == "__main__":
    main()
