import json

import pytest

from src.data_loader import load_case, load_technique_catalogue


def test_case_loads_synthetic_events_in_chronological_order():
    case = load_case()
    timestamps = [event["timestamp"] for event in case["events"]]
    assert case["synthetic"] is True
    assert timestamps == sorted(timestamps)
    assert len(case["events"]) >= 6


def test_case_loader_rejects_malformed_records(tmp_path):
    path = tmp_path / "bad-case.json"
    path.write_text(json.dumps({"synthetic": True, "events": [{"evidence_id": "E-1"}]}), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid incident data"):
        load_case(path)


def test_case_loader_reports_invalid_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="Unable to load valid JSON"):
        load_case(path)


def test_catalogue_is_pinned_to_enterprise_v15_1():
    catalogue = load_technique_catalogue()
    assert catalogue["metadata"]["catalogue_version"] == "15.1"
    assert catalogue["metadata"]["domain"] == "enterprise-attack"
    assert len(catalogue["techniques"]) == 637
