"""Search and filter synthetic incident evidence."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd


def filter_events(
    events: list[dict[str, Any]],
    query: str = "",
    category: str | None = None,
    host_or_identity: str | None = None,
    minimum_confidence: float = 0,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[dict[str, Any]]:
    """Apply case-insensitive text, category, host, confidence, and time filters."""
    needle = query.casefold().strip()
    filtered: list[dict[str, Any]] = []
    for event in events:
        timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        searchable = " ".join(
            str(event.get(field, ""))
            for field in ("evidence_id", "event_description", "observed_behaviour", "data_source", "host_or_identity")
        ).casefold()
        if needle and needle not in searchable:
            continue
        if category and event.get("category") != category:
            continue
        if host_or_identity and host_or_identity.casefold() not in event.get("host_or_identity", "").casefold():
            continue
        if float(event.get("confidence", 0)) < minimum_confidence:
            continue
        if start and timestamp < start:
            continue
        if end and timestamp > end:
            continue
        filtered.append(event)
    return filtered


def events_to_dataframe(events: list[dict[str, Any]]) -> pd.DataFrame:
    """Return a student-friendly table while preserving reference lists."""
    return pd.DataFrame(
        [
            {
                "Evidence ID": event["evidence_id"],
                "Timestamp (UTC)": event["timestamp"],
                "Host / identity": event["host_or_identity"],
                "Category": event["category"],
                "Description": event["event_description"],
                "Source": event["data_source"],
                "Confidence": event["confidence"],
                "Related events": ", ".join(event["related_events"]),
                "Synthetic": event["synthetic"],
            }
            for event in events
        ]
    )
