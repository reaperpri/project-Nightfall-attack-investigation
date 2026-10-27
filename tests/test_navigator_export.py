import json

import pytest

from src.data_loader import load_technique_catalogue
from src.navigator_export import (
    build_navigator_layer,
    navigator_layer_json,
    validate_navigator_layer,
)


def make_mapping(technique_id="T1057", status="supported"):
    catalogue = load_technique_catalogue()
    technique = next(item for item in catalogue["techniques"] if item["technique_id"] == technique_id)
    return {
        "evidence_id": "E-04",
        "evidence_ids": ["E-04", "E-03"],
        "technique_id": technique_id,
        "technique_name": technique["name"],
        "tactics": technique["tactics"],
        "rationale": "Observed process inventory queries may align with process discovery.",
        "alternative_explanations": "An approved inventory utility may explain the query.",
        "missing_evidence": "Process lineage and script telemetry.",
        "confidence": 3,
        "status": status,
        "include_in_export": True,
    }


def test_navigator_layer_has_version_domain_and_annotations():
    catalogue = load_technique_catalogue()
    layer = build_navigator_layer([make_mapping()], catalogue)
    assert layer["domain"] == "enterprise-attack"
    assert layer["versions"] == {"attack": "15.1", "navigator": "5.1.1", "layer": "4.5"}
    technique = layer["techniques"][0]
    assert technique["techniqueID"] == "T1057"
    assert "Status: supported" in technique["comment"]
    assert "E-04, E-03" in technique["comment"]
    assert "student-defined" in technique["comment"]
    assert validate_navigator_layer(layer, {item["technique_id"]: item for item in catalogue["techniques"]}) == []


def test_export_json_round_trip_and_empty_investigation():
    catalogue = load_technique_catalogue()
    exported = navigator_layer_json([make_mapping()], catalogue)
    assert json.loads(exported)["techniques"][0]["comment"]
    empty = build_navigator_layer([], catalogue)
    assert empty["techniques"] == []
    assert validate_navigator_layer(empty) == []


def test_export_rejects_unknown_technique():
    mapping = make_mapping()
    mapping["technique_id"] = "T9999"
    with pytest.raises(ValueError, match="Unsupported ATT&CK v15.1 technique ID"):
        build_navigator_layer([mapping], load_technique_catalogue())


def test_export_omits_mappings_marked_out_of_scope():
    mapping = make_mapping()
    mapping["include_in_export"] = False
    assert build_navigator_layer([mapping], load_technique_catalogue())["techniques"] == []


def test_navigator_validation_rejects_wrong_attack_version():
    layer = build_navigator_layer([], load_technique_catalogue())
    layer["versions"]["attack"] = "latest"
    assert any("versions.attack must be 15.1" in error for error in validate_navigator_layer(layer))
