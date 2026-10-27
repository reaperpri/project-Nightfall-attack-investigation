"""Input and mapping validation for the synthetic investigation."""

from __future__ import annotations

from datetime import datetime
from typing import Any


EVENT_FIELDS = {
    "evidence_id",
    "timestamp",
    "host_or_identity",
    "category",
    "event_description",
    "data_source",
    "observed_behaviour",
    "potential_significance",
    "confidence",
    "evidence_limitations",
    "related_events",
}
MAPPING_STATUSES = {"proposed", "supported", "rejected", "requires further investigation"}


def validate_events(events: list[dict[str, Any]]) -> list[str]:
    """Return all schema and cross-reference errors in an event list."""
    errors: list[str] = []
    identifiers: set[str] = set()
    for index, event in enumerate(events):
        prefix = f"events[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = EVENT_FIELDS - event.keys()
        if missing:
            errors.append(f"{prefix} is missing: {', '.join(sorted(missing))}")
            continue
        evidence_id = event.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            errors.append(f"{prefix}.evidence_id must be a non-empty string")
        elif evidence_id in identifiers:
            errors.append(f"duplicate evidence_id: {evidence_id}")
        else:
            identifiers.add(evidence_id)
        try:
            parsed = datetime.fromisoformat(str(event.get("timestamp", "")).replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                errors.append(f"{prefix}.timestamp must include a timezone")
        except ValueError:
            errors.append(f"{prefix}.timestamp must be an ISO-8601 datetime")
        confidence = event.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be a number from 0 to 1")
        if not isinstance(event.get("related_events"), list) or not all(
            isinstance(item, str) for item in event.get("related_events", [])
        ):
            errors.append(f"{prefix}.related_events must be a list of evidence IDs")
        if event.get("synthetic") is not True:
            errors.append(f"{prefix}.synthetic must be true")

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        for related_id in event.get("related_events", []):
            if related_id not in identifiers:
                errors.append(f"events[{index}] references unknown evidence ID {related_id}")
    return errors


def validate_mapping(
    mapping: dict[str, Any], technique_ids: set[str], evidence_ids: set[str]
) -> list[str]:
    """Validate a student mapping and its local evidence/catalogue references."""
    errors: list[str] = []
    if mapping.get("technique_id") not in technique_ids:
        errors.append(f"unsupported technique ID: {mapping.get('technique_id')}")
    if mapping.get("evidence_id") not in evidence_ids:
        errors.append(f"unknown evidence ID: {mapping.get('evidence_id')}")
    if mapping.get("status") not in MAPPING_STATUSES:
        errors.append(f"unsupported mapping status: {mapping.get('status')}")
    if not isinstance(mapping.get("evidence_ids"), list) or not mapping.get("evidence_ids"):
        errors.append("at least one supporting evidence ID is required")
    elif any(item not in evidence_ids for item in mapping["evidence_ids"]):
        errors.append("mapping contains an unknown supporting evidence ID")
    elif mapping.get("evidence_id") not in mapping["evidence_ids"]:
        errors.append("primary evidence ID must be included in supporting evidence")
    if not isinstance(mapping.get("confidence"), int) or isinstance(mapping.get("confidence"), bool):
        errors.append("analyst confidence must be an integer from 1 to 5")
    elif not 1 <= mapping["confidence"] <= 5:
        errors.append("analyst confidence must be an integer from 1 to 5")
    if not isinstance(mapping.get("rationale"), str):
        errors.append("mapping rationale must be text")
    elif mapping.get("status") == "supported" and not mapping["rationale"].strip():
        errors.append("a supported mapping requires an analyst rationale")
    return errors


def validate_mapping_transition(
    current_status: str | None, new_status: str, rationale: str, evidence_ids: list[str]
) -> list[str]:
    """Require evidence and an explicit rationale before a mapping is supported."""
    errors: list[str] = []
    if new_status not in MAPPING_STATUSES:
        errors.append(f"unsupported mapping status: {new_status}")
    if current_status is not None and current_status not in MAPPING_STATUSES:
        errors.append(f"unsupported current mapping status: {current_status}")
    if new_status == "supported":
        if not rationale.strip():
            errors.append("a supported mapping requires an analyst rationale")
        if not evidence_ids:
            errors.append("a supported mapping requires supporting evidence")
    return errors
