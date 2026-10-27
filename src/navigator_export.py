"""Build and validate ATT&CK Navigator v4.5 layer files."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


STATUS_COLORS = {
    "supported": "#3A8D67",
    "proposed": "#E5A93D",
    "requires further investigation": "#4787B8",
    "rejected": "#9A6673",
}


def build_navigator_layer(
    mappings: list[dict[str, Any]],
    catalogue: dict[str, Any],
    *,
    name: str = "Project Nightfall — Student Investigation",
) -> dict[str, Any]:
    """Build a Navigator v4.5 layer using the pinned ATT&CK 15.1 catalogue."""
    techniques_by_id = {technique["technique_id"]: technique for technique in catalogue["techniques"]}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for mapping in mappings:
        if not mapping.get("include_in_export", True):
            continue
        technique_id = mapping.get("technique_id")
        if technique_id not in techniques_by_id:
            raise ValueError(f"Unsupported ATT&CK v15.1 technique ID: {technique_id}")
        if mapping.get("status") not in STATUS_COLORS:
            raise ValueError(f"Unsupported mapping status: {mapping.get('status')}")
        if not isinstance(mapping.get("evidence_ids"), list) or not mapping["evidence_ids"]:
            raise ValueError(f"Mapping for {technique_id} must retain at least one evidence reference.")
        if mapping.get("status") == "supported" and not str(mapping.get("rationale", "")).strip():
            raise ValueError(f"Supported mapping for {technique_id} requires an analyst rationale.")
        if isinstance(mapping.get("confidence"), bool) or not isinstance(mapping.get("confidence"), int):
            raise ValueError(f"Mapping confidence for {technique_id} must be an integer from 1 to 5.")
        if not 1 <= mapping["confidence"] <= 5:
            raise ValueError(f"Mapping confidence for {technique_id} must be an integer from 1 to 5.")
        grouped[technique_id].append(mapping)

    layer_techniques = []
    for technique_id in sorted(grouped):
        entries = grouped[technique_id]
        comments = []
        for entry in entries:
            comments.append(
                "\n".join(
                    (
                        f"Status: {entry['status']}",
                        f"Analyst confidence: {entry['confidence']}/5 (student-defined; not MITRE metadata)",
                        f"Evidence: {', '.join(entry.get('evidence_ids', []))}",
                        f"Rationale: {entry.get('rationale') or 'Not provided'}",
                        f"Alternative explanations: {entry.get('alternative_explanations') or 'Not recorded'}",
                        f"Missing evidence: {entry.get('missing_evidence') or 'Not recorded'}",
                    )
                )
            )
        strongest = max(entries, key=lambda item: (item["confidence"], item["status"] == "supported"))
        layer_techniques.append(
            {
                "techniqueID": technique_id,
                "score": round(strongest["confidence"] * 20),
                "color": STATUS_COLORS[strongest["status"]],
                "comment": "\n\n---\n\n".join(comments),
            }
        )

    layer = {
        "name": name,
        "versions": {"attack": "15.1", "navigator": "5.1.1", "layer": "4.5"},
        "domain": "enterprise-attack",
        "description": "Synthetic Project Nightfall investigation. Colours represent analyst mapping status; scores are student-defined confidence, not MITRE ratings. Adjacency does not assert sequence or causation.",
        "filters": {"platforms": ["Windows", "Office 365", "Network"]},
        "sorting": 0,
        "layout": {"layout": "side"},
        "hideDisabled": False,
        "techniques": layer_techniques,
        "gradient": {
            "colors": ["#D8E9E1", "#3A8D67"],
            "minValue": 0,
            "maxValue": 100,
        },
        "legendItems": [
            {"label": status.title(), "color": color}
            for status, color in STATUS_COLORS.items()
        ],
        "metadata": [
            {"name": "Case", "value": "NIGHTFALL-SIM-001 (synthetic)"},
            {"name": "ATT&CK catalogue", "value": "Enterprise ATT&CK 15.1"},
            {"name": "Layer format", "value": "Navigator 4.5"},
        ],
    }
    errors = validate_navigator_layer(layer, techniques_by_id)
    if errors:
        raise ValueError("Invalid Navigator layer: " + "; ".join(errors))
    return layer


def validate_navigator_layer(
    layer: dict[str, Any], techniques_by_id: dict[str, dict[str, Any]] | None = None
) -> list[str]:
    """Check the format/version/domain and technique references before export."""
    errors: list[str] = []
    if not isinstance(layer, dict):
        return ["layer must be an object"]
    versions = layer.get("versions", {})
    if not isinstance(versions, dict):
        errors.append("versions must be an object")
        versions = {}
    if versions.get("attack") != "15.1":
        errors.append("versions.attack must be 15.1")
    if versions.get("layer") != "4.5":
        errors.append("versions.layer must be 4.5")
    if not isinstance(versions.get("navigator"), str) or not versions["navigator"]:
        errors.append("versions.navigator must be a non-empty string")
    if layer.get("domain") != "enterprise-attack":
        errors.append("domain must be enterprise-attack")
    if not isinstance(layer.get("name"), str) or not layer["name"].strip():
        errors.append("name must be a non-empty string")
    if not isinstance(layer.get("techniques"), list):
        errors.append("techniques must be a list")
        return errors
    seen: set[str] = set()
    for index, technique in enumerate(layer["techniques"]):
        if not isinstance(technique, dict):
            errors.append(f"techniques[{index}] must be an object")
            continue
        technique_id = technique.get("techniqueID")
        if not isinstance(technique_id, str) or not technique_id:
            errors.append(f"techniques[{index}].techniqueID must be a string")
            continue
        if technique_id in seen:
            errors.append(f"duplicate Navigator technique ID: {technique_id}")
        seen.add(technique_id)
        if techniques_by_id is not None and technique_id not in techniques_by_id:
            errors.append(f"unsupported ATT&CK v15.1 technique ID: {technique_id}")
        if not isinstance(technique.get("comment", ""), str):
            errors.append(f"techniques[{index}].comment must be a string")
        score = technique.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
            errors.append(f"techniques[{index}].score must be between 0 and 100")
    return errors


def navigator_layer_json(mappings: list[dict[str, Any]], catalogue: dict[str, Any]) -> str:
    """Serialize a validated Navigator layer as UTF-8-ready JSON text."""
    return json.dumps(build_navigator_layer(mappings, catalogue), indent=2, ensure_ascii=False) + "\n"
