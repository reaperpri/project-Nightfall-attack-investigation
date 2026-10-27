from src.data_loader import load_case
from src.validation import validate_events, validate_mapping


def test_bundled_events_have_valid_cross_references():
    events = load_case()["events"]
    assert validate_events(events) == []


def test_event_validator_rejects_bad_timestamp_confidence_and_missing_reference():
    event = {
        "evidence_id": "E-X",
        "timestamp": "not-a-time",
        "host_or_identity": "synthetic",
        "category": "test",
        "event_description": "Synthetic test record",
        "data_source": "test fixture",
        "observed_behaviour": "test",
        "potential_significance": "test",
        "confidence": 5,
        "evidence_limitations": "test",
        "related_events": ["E-NOT-FOUND"],
        "synthetic": True,
    }
    errors = validate_events([event])
    assert any("ISO-8601" in error for error in errors)
    assert any("confidence" in error for error in errors)
    assert any("unknown evidence ID" in error for error in errors)


def test_supported_mapping_without_rationale_is_invalid():
    mapping = {
        "technique_id": "T1057",
        "evidence_id": "E-04",
        "evidence_ids": ["E-04"],
        "status": "supported",
        "confidence": 3,
        "rationale": " ",
    }
    assert any(
        "requires an analyst rationale" in error
        for error in validate_mapping(mapping, {"T1057"}, {"E-04"})
    )
