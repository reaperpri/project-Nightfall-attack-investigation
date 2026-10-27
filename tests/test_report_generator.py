from src.data_loader import load_case, load_hypotheses, load_recommendations
from src.report_generator import generate_report


def test_report_includes_synthetic_scope_and_cautious_findings():
    case = load_case()
    report = generate_report(
        case,
        case["events"],
        [],
        load_hypotheses(),
        load_recommendations(),
        {"E-03": {"interpretation": "Needs process telemetry", "confidence": 2}},
    )
    assert "SIMULATED TRAINING CASE" in report
    assert "does not establish" in report
    assert "Enterprise 15.1" in report
    assert "Evidence timeline" in report
    assert "Suggested next investigative steps" in report
    assert "Student evidence analysis" in report
    assert "Needs process telemetry" in report


def test_report_handles_empty_investigation():
    case = load_case()
    report = generate_report(case, [], [], [], [])
    assert "Review covers 0 synthetic evidence records" in report
    assert "No candidate mappings have been recorded." in report
