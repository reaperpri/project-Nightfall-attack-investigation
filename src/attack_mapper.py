"""ATT&CK catalogue search and candidate mapping helpers."""

from __future__ import annotations

from typing import Any

from src.validation import MAPPING_STATUSES, validate_mapping_transition


def search_techniques(
    techniques: list[dict[str, Any]], query: str = "", tactic: str | None = None
) -> list[dict[str, Any]]:
    """Search the local v15.1 catalogue by ID, name, or description."""
    needle = query.casefold().strip()
    exact_id = next(
        (technique for technique in techniques if technique["technique_id"].casefold() == needle),
        None,
    )
    if exact_id and (not tactic or tactic in exact_id.get("tactics", [])):
        return [exact_id]
    matches = [
        technique
        for technique in techniques
        if (not needle or needle in " ".join(
            (technique["technique_id"], technique["name"], technique.get("description", ""))
        ).casefold())
        and (not tactic or tactic in technique.get("tactics", []))
    ]
    return sorted(matches, key=lambda item: (item["name"].casefold(), item["technique_id"]))


def create_mapping(
    *,
    evidence_id: str,
    technique: dict[str, Any],
    evidence_ids: list[str],
    rationale: str,
    alternatives: str,
    missing_evidence: str,
    confidence: int,
    status: str,
    current_status: str | None = None,
    include_in_export: bool = True,
) -> dict[str, Any]:
    """Build a mapping after enforcing the supported-status evidence gate."""
    linked_evidence_ids = list(dict.fromkeys([evidence_id, *evidence_ids]))
    errors = validate_mapping_transition(current_status, status, rationale, linked_evidence_ids)
    if errors:
        raise ValueError("; ".join(errors))
    if not linked_evidence_ids:
        raise ValueError("At least one supporting evidence ID is required.")
    if status not in MAPPING_STATUSES:
        raise ValueError(f"Unsupported mapping status: {status}")
    if isinstance(confidence, bool) or not isinstance(confidence, int) or not 1 <= confidence <= 5:
        raise ValueError("Analyst confidence must be from 1 to 5.")
    return {
        "evidence_id": evidence_id,
        "evidence_ids": linked_evidence_ids,
        "technique_id": technique["technique_id"],
        "technique_name": technique["name"],
        "tactics": list(technique.get("tactics", [])),
        "rationale": rationale.strip(),
        "alternative_explanations": alternatives.strip(),
        "missing_evidence": missing_evidence.strip(),
        "confidence": confidence,
        "status": status,
        "include_in_export": bool(include_in_export),
    }
