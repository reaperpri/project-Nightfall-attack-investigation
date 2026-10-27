"""Interactive chronological view of the synthetic case."""

import streamlit as st

from src.evidence_analysis import filter_events
from src.timeline import create_timeline
from src.ui_helpers import render_page_header


render_page_header(
    "Incident Timeline",
    "Use chronology to develop questions—not to assume causation.",
)
events = st.session_state.case_data["events"]
categories = sorted({event["category"] for event in events})
hosts = sorted({event["host_or_identity"] for event in events})

with st.sidebar:
    st.subheader("Timeline filters")
    selected_categories = st.multiselect("Evidence categories", categories, default=categories)
    selected_hosts = st.multiselect("Host / identity", hosts, default=hosts)
    minimum_confidence = st.slider("Source confidence at least", 0.0, 1.0, 0.0, 0.05)

selected = [
    event for event in events
    if event["category"] in selected_categories and event["host_or_identity"] in selected_hosts
]
selected = filter_events(selected, minimum_confidence=minimum_confidence)

if not selected:
    st.info("No evidence matches the current filters.")
else:
    st.plotly_chart(create_timeline(selected), width="stretch")
    st.subheader("Evidence records")
    for event in selected:
        with st.expander(f"{event['timestamp'][11:16]} UTC · {event['evidence_id']} · {event['event_description']}"):
            st.markdown(f"**Observed behaviour:** {event['observed_behaviour']}")
            st.markdown(f"**Potential significance:** {event['potential_significance']}")
            st.markdown(f"**Evidence limitations:** {event['evidence_limitations']}")
            st.caption(
                f"Source: {event['data_source']} · source confidence {event['confidence']:.0%} · "
                f"related records: {', '.join(event['related_events']) or 'none'}"
            )
st.caption("Times are UTC. Endpoint records may be approximately 45 seconds ahead of identity/cloud records.")
