from datetime import datetime, timezone

from src.data_loader import load_case
from src.evidence_analysis import events_to_dataframe, filter_events


def test_search_category_host_confidence_and_time_filters():
    events = load_case()["events"]
    result = filter_events(
        events,
        query="powershell",
        category="endpoint",
        host_or_identity="NS-LT-042",
        minimum_confidence=0.7,
        start=datetime(2025, 3, 12, 10, 0, tzinfo=timezone.utc),
        end=datetime(2025, 3, 12, 10, 30, tzinfo=timezone.utc),
    )
    assert [event["evidence_id"] for event in result] == ["E-03"]


def test_dataframe_handles_empty_results_and_export_columns():
    events = load_case()["events"]
    assert events_to_dataframe([]).empty
    table = events_to_dataframe(events)
    assert "Evidence ID" in table.columns
    assert "Related events" in table.columns
    assert len(table) == len(events)
