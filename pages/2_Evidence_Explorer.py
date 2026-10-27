"""Search, annotate, and export synthetic incident records."""

import json
from datetime import datetime, time, timezone

import pandas as pd
import streamlit as st

from src.evidence_analysis import events_to_dataframe, filter_events
from src.ui_helpers import evidence_ids, render_page_header, save_analysis_notes
from src.validation import validate_events


render_page_header(
    "Evidence Explorer",
    "Separate what a record says from what you think it might mean.",
)
events = st.session_state.case_data["events"]
all_categories = sorted({event["category"] for event in events})
all_hosts = sorted({event["host_or_identity"] for event in events})
event_days = sorted({datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")).date() for event in events})

with st.sidebar:
    st.subheader("Evidence filters")
    query = st.text_input("Search records", placeholder="ID, process, document, host...")
    categories = st.multiselect("Category", all_categories, default=all_categories)
    hosts = st.multiselect("Host / identity", all_hosts, default=all_hosts)
    minimum_confidence = st.slider("Minimum source confidence", 0.0, 1.0, 0.0, 0.05)
    selected_days = st.date_input(
        "Date range (UTC)", value=(event_days[0], event_days[-1]), min_value=event_days[0], max_value=event_days[-1]
    )

if isinstance(selected_days, tuple) and len(selected_days) == 2:
    start = datetime.combine(selected_days[0], time.min, timezone.utc)
    end = datetime.combine(selected_days[1], time.max, timezone.utc)
else:
    start = end = None

filtered = filter_events(
    events,
    query=query,
    minimum_confidence=minimum_confidence,
    start=start,
    end=end,
)
filtered = [
    event for event in filtered
    if event["category"] in categories
    and any(host.casefold() in event["host_or_identity"].casefold() for host in hosts)
]
st.dataframe(events_to_dataframe(filtered), width="stretch", hide_index=True)
st.download_button(
    "Download filtered evidence CSV",
    data=events_to_dataframe(filtered).to_csv(index=False).encode("utf-8"),
    file_name="nightfall_filtered_evidence.csv",
    mime="text/csv",
    disabled=not filtered,
)

if filtered:
    selected_id = st.selectbox("Evidence detail", [event["evidence_id"] for event in filtered])
    event = next(item for item in filtered if item["evidence_id"] == selected_id)
    with st.expander("Complete source record", expanded=True):
        st.json(event)
    note = st.session_state.analysis_notes.get(
        selected_id,
        {
            "direct_observation": event["observed_behaviour"],
            "interpretation": "",
            "alternatives": "",
            "additional_evidence": "",
            "confidence": 3,
            "related_events": event["related_events"],
        },
    )
    with st.form(f"analysis_{selected_id}"):
        st.subheader("Your analysis")
        observed = st.text_area("What was directly observed?", value=note["direct_observation"])
        interpretation = st.text_area("What might it indicate?", value=note["interpretation"])
        alternatives = st.text_area("What alternative explanations exist?", value=note["alternatives"])
        additional = st.text_area("What additional evidence is needed?", value=note["additional_evidence"])
        analyst_confidence = st.slider("Your confidence in this interpretation", 1, 5, note["confidence"])
        related = st.multiselect(
            "Potentially related evidence (analyst-selected)",
            evidence_ids(),
            default=[item for item in note["related_events"] if item in evidence_ids()],
        )
        if st.form_submit_button("Save analysis"):
            save_analysis_notes(
                selected_id,
                {
                    "direct_observation": observed,
                    "interpretation": interpretation,
                    "alternatives": alternatives,
                    "additional_evidence": additional,
                    "confidence": analyst_confidence,
                    "related_events": related,
                },
            )
            st.success("Analysis saved for this browser session; it is not a verified incident conclusion.")

with st.expander("Optional: load additional synthetic evidence from CSV"):
    st.caption("CSV rows must use the incident-event field names and explicitly mark `synthetic` as true.")
    upload = st.file_uploader("Choose synthetic evidence CSV", type=["csv"], key="evidence_csv")
    if upload is not None:
        try:
            frame = pd.read_csv(upload, dtype=str).fillna("")
            imported = frame.to_dict(orient="records")
            for item in imported:
                item["confidence"] = float(item["confidence"])
                item["synthetic"] = item["synthetic"].strip().casefold() == "true"
                raw_related = item["related_events"]
                item["related_events"] = (
                    json.loads(raw_related)
                    if raw_related.lstrip().startswith("[")
                    else [value.strip() for value in raw_related.split(",") if value.strip()]
                )
            errors = validate_events(events + imported)
            if errors:
                st.error("CSV not loaded: " + "; ".join(errors))
            elif st.button("Add validated records to this session"):
                st.session_state.case_data["events"].extend(imported)
                st.session_state.case_data["events"].sort(key=lambda item: item["timestamp"])
                st.success(f"Added {len(imported)} synthetic records for this session.")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError, pd.errors.ParserError) as exc:
            st.error(f"Could not validate the uploaded CSV: {exc}")
