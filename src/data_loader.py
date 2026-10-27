"""Load and validate the bundled synthetic case and ATT&CK catalogue."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.validation import validate_events


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load valid JSON from {path}: {exc}") from exc


def load_case(path: Path | None = None) -> dict[str, Any]:
    """Load case metadata and chronologically sorted synthetic evidence."""
    case = _read_json(path or DATA_DIR / "incident_events.json")
    if not isinstance(case, dict) or case.get("synthetic") is not True:
        raise ValueError("The case file must be a synthetic case object.")
    events = case.get("events")
    if not isinstance(events, list):
        raise ValueError("The case file must contain an events list.")
    errors = validate_events(events)
    if errors:
        raise ValueError("Invalid incident data: " + "; ".join(errors))
    case["events"] = sorted(events, key=lambda event: event["timestamp"])
    return case


def load_technique_catalogue(path: Path | None = None) -> dict[str, Any]:
    """Load the version-pinned Enterprise ATT&CK technique catalogue."""
    catalogue = _read_json(path or DATA_DIR / "attack_techniques.json")
    if (
        not isinstance(catalogue, dict)
        or catalogue.get("metadata", {}).get("domain") != "enterprise-attack"
        or catalogue.get("metadata", {}).get("catalogue_version") != "15.1"
        or not isinstance(catalogue.get("techniques"), list)
    ):
        raise ValueError("ATT&CK catalogue must be an Enterprise v15.1 catalogue.")
    ids = [technique.get("technique_id") for technique in catalogue["techniques"]]
    if any(not isinstance(technique_id, str) for technique_id in ids) or len(ids) != len(set(ids)):
        raise ValueError("ATT&CK catalogue contains missing or duplicate technique IDs.")
    return catalogue


def load_hypotheses(path: Path | None = None) -> list[dict[str, Any]]:
    """Load guided investigation hypotheses."""
    hypotheses = _read_json(path or DATA_DIR / "investigation_hypotheses.json")
    if not isinstance(hypotheses, list) or any(not isinstance(item, dict) for item in hypotheses):
        raise ValueError("Hypotheses data must be a list of objects.")
    return hypotheses


def load_recommendations(path: Path | None = None) -> list[dict[str, Any]]:
    """Load the locally maintained defensive recommendation examples."""
    recommendations = _read_json(path or DATA_DIR / "defensive_recommendations.json")
    if not isinstance(recommendations, list) or any(not isinstance(item, dict) for item in recommendations):
        raise ValueError("Defensive recommendations must be a list of objects.")
    return recommendations
