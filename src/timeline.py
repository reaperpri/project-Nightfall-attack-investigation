"""Timeline visualisation data helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px


CATEGORY_COLORS = {
    "email": "#d9a441",
    "identity": "#5096c8",
    "endpoint": "#ba6c77",
    "cloud-audit": "#8f79c7",
    "network": "#47a58c",
    "interview": "#7f8c8d",
    "evidence-quality": "#95a5a6",
}


def create_timeline(events: list[dict[str, Any]]):
    """Create an interactive event timeline using only supplied evidence."""
    frame = pd.DataFrame(events)
    if frame.empty:
        return px.scatter(title="No evidence matches the current filters.")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["label"] = frame["evidence_id"] + " · " + frame["event_description"]
    figure = px.scatter(
        frame,
        x="timestamp",
        y="category",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        hover_name="evidence_id",
        hover_data={
            "host_or_identity": True,
            "observed_behaviour": True,
            "potential_significance": True,
            "confidence": True,
            "timestamp": True,
        },
        title="Evidence chronology (UTC; sequence does not prove causation)",
    )
    figure.update_traces(marker={"size": 14, "line": {"width": 1, "color": "#f0f3f5"}})
    figure.update_layout(
        height=360,
        xaxis_title="Timestamp (UTC)",
        yaxis_title="Evidence category",
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return figure
