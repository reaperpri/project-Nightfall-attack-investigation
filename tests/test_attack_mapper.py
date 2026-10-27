from src.attack_mapper import create_mapping, search_techniques
from src.data_loader import load_case, load_technique_catalogue
from src.validation import validate_mapping, validate_mapping_transition


def test_search_by_id_name_and_tactic():
    catalogue = load_technique_catalogue()
    techniques = catalogue["techniques"]
    assert [item["technique_id"] for item in search_techniques(techniques, "T1057")] == ["T1057"]
    assert any(item["name"] == "Process Discovery" for item in search_techniques(techniques, "process discovery"))
    assert all("discovery" in item["tactics"] for item in search_techniques(techniques, tactic="discovery"))


def test_supported_mapping_requires_rationale_and_evidence():
    assert validate_mapping_transition(None, "supported", "", ["E-03"])
    assert validate_mapping_transition(None, "supported", "Process query observed", [])
    assert validate_mapping_transition(None, "supported", "Process query observed", ["E-04"]) == []


def test_mapping_validates_catalogue_and_evidence_references():
    case = load_case()
    catalogue = load_technique_catalogue()
    technique = next(item for item in catalogue["techniques"] if item["technique_id"] == "T1057")
    mapping = create_mapping(
        evidence_id="E-04",
        technique=technique,
        evidence_ids=["E-04"],
        rationale="Process and security-software inventory queries were observed.",
        alternatives="Approved inventory activity is possible.",
        missing_evidence="Need process lineage and script telemetry.",
        confidence=3,
        status="supported",
    )
    assert validate_mapping(
        mapping,
        {item["technique_id"] for item in catalogue["techniques"]},
        {event["evidence_id"] for event in case["events"]},
    ) == []
    mapping["technique_id"] = "T9999"
    assert any("unsupported technique ID" in error for error in validate_mapping(
        mapping,
        {item["technique_id"] for item in catalogue["techniques"]},
        {event["evidence_id"] for event in case["events"]},
    ))


def test_unsupported_supported_transition_is_rejected():
    try:
        create_mapping(
            evidence_id="E-03",
            technique={"technique_id": "T1059", "name": "Command and Scripting Interpreter", "tactics": []},
            evidence_ids=[],
            rationale="",
            alternatives="",
            missing_evidence="",
            confidence=2,
            status="supported",
        )
    except ValueError as exc:
        assert "requires" in str(exc)
    else:
        raise AssertionError("A supported mapping without rationale or evidence was accepted.")
