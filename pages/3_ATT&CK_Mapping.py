"""Create and inspect evidence-linked ATT&CK mapping hypotheses."""

import plotly.express as px
import pandas as pd
import streamlit as st

from src.attack_mapper import create_mapping, search_techniques
from src.ui_helpers import catalogue_by_id, evidence_ids, render_page_header
from src.validation import validate_mapping


render_page_header(
    "ATT&CK Mapping",
    "Use the pinned Enterprise ATT&CK 15.1 catalogue. A mapping is an analyst hypothesis, not proof.",
)
catalogue = st.session_state.catalogue
techniques = catalogue["techniques"]
events = st.session_state.case_data["events"]
ids = evidence_ids()
techniques_by_id = catalogue_by_id()
tactics = sorted({tactic for technique in techniques for tactic in technique["tactics"]})

mapping_tab, map_tab = st.tabs(["Mapping workspace", "Visual attack map"])
with mapping_tab:
    event_id = st.selectbox("Select an evidence record", ids)
    query = st.text_input("Search ATT&CK v15.1 techniques", placeholder="Technique name or ID, e.g. T1057")
    tactic = st.selectbox("Filter by tactic", ["All tactics", *tactics])
    matches = search_techniques(
        techniques,
        query=query,
        tactic=None if tactic == "All tactics" else tactic,
    )
    if not matches:
        st.info("No techniques match. Try a broader name or choose another tactic.")
    else:
        options = [item["technique_id"] for item in matches]
        selected_technique_id = st.selectbox(
            "Technique",
            options,
            format_func=lambda value: f"{value} — {techniques_by_id[value]['name']}",
        )
        selected_technique = techniques_by_id[selected_technique_id]
        st.markdown(f"**Tactics:** {', '.join(selected_technique['tactics']) or 'Not tagged'}")
        st.caption(selected_technique["description"][:1200])
        child_ids = selected_technique.get("subtechnique_ids", [])
        if child_ids:
            with st.expander(f"Available sub-techniques ({len(child_ids)})"):
                for child_id in child_ids:
                    child = techniques_by_id.get(child_id)
                    if child:
                        st.markdown(f"- **{child_id} — {child['name']}**")

        same_technique = [
            (index, mapping)
            for index, mapping in enumerate(st.session_state.mappings)
            if mapping["technique_id"] == selected_technique_id
        ]
        edit_choice = st.selectbox(
            "Mapping to edit (or create a new mapping)",
            ["New mapping", *[f"{i + 1}. {m['evidence_id']} · {m['status']}" for i, m in same_technique]],
        )
        editing_index = None
        if edit_choice != "New mapping":
            choice = same_technique[["New mapping", *[f"{i + 1}. {m['evidence_id']} · {m['status']}" for i, m in same_technique]].index(edit_choice) - 1]
            editing_index = same_technique[choice][0]
        existing = st.session_state.mappings[editing_index] if editing_index is not None else {}

        with st.form("mapping_form"):
            selected_evidence_id = st.selectbox(
                "Primary evidence record",
                ids,
                index=ids.index(existing.get("evidence_id", event_id)),
            )
            supporting_ids = st.multiselect(
                "Supporting evidence records",
                ids,
                default=[
                    value for value in existing.get("evidence_ids", [selected_evidence_id])
                    if value in ids
                ],
            )
            rationale = st.text_area(
                "Analyst rationale (required for Supported)",
                value=existing.get("rationale", ""),
            )
            alternatives = st.text_area(
                "Alternative explanations",
                value=existing.get("alternative_explanations", ""),
            )
            missing = st.text_area("Missing evidence", value=existing.get("missing_evidence", ""))
            confidence = st.slider(
                "Analyst-defined confidence (not MITRE metadata)",
                1,
                5,
                int(existing.get("confidence", 2)),
            )
            statuses = ["proposed", "supported", "requires further investigation", "rejected"]
            status = st.selectbox(
                "Mapping status",
                statuses,
                index=statuses.index(existing.get("status", "proposed")),
            )
            include = st.checkbox(
                "Include in Navigator export",
                value=existing.get("include_in_export", status != "rejected"),
            )
            submitted = st.form_submit_button("Save mapping")
        if submitted:
            try:
                new_mapping = create_mapping(
                    evidence_id=selected_evidence_id,
                    technique=selected_technique,
                    evidence_ids=supporting_ids,
                    rationale=rationale,
                    alternatives=alternatives,
                    missing_evidence=missing,
                    confidence=confidence,
                    status=status,
                    current_status=existing.get("status"),
                    include_in_export=include,
                )
                errors = validate_mapping(new_mapping, set(techniques_by_id), set(ids))
                if errors:
                    st.error("; ".join(errors))
                elif editing_index is None:
                    st.session_state.mappings.append(new_mapping)
                    st.success("Candidate mapping added.")
                else:
                    st.session_state.mappings[editing_index] = new_mapping
                    st.success("Candidate mapping updated.")
            except ValueError as exc:
                st.error(str(exc))

    st.subheader("Mappings for selected evidence")
    related_mappings = [
        (index, mapping)
        for index, mapping in enumerate(st.session_state.mappings)
        if event_id in mapping["evidence_ids"]
    ]
    if not related_mappings:
        st.info("No mappings are linked to this evidence yet.")
    for index, mapping in related_mappings:
        with st.expander(f"{mapping['technique_id']} · {mapping['technique_name']} · {mapping['status']}"):
            st.write(mapping)
            if st.button("Remove mapping", key=f"remove_{index}"):
                st.session_state.mappings.pop(index)
                st.rerun()

    starter_candidates = {
        "E-01": (
            "T1566",
            "An unexpected external document-review email is observed, but no click or payload evidence is supplied.",
            "Routine external business mail is possible; receiving the email alone does not establish successful phishing.",
            "Message content, authentication results, URL destination at delivery, and recipient interaction telemetry.",
        ),
        "E-03": (
            "T1059",
            "An office application started a scripting interpreter; the recorded command and resulting actions are unavailable.",
            "An approved add-in or administrative workflow may explain the process relationship.",
            "Full process lineage, script telemetry, file metadata, and application/add-in context.",
        ),
        "E-04": (
            "T1057",
            "Running processes were enumerated; this is a candidate behaviour, not proof of adversary activity.",
            "Approved inventory or endpoint-management tooling may explain process enumeration.",
            "Initiating process, user context, query details, and approved-tool baseline.",
        ),
    }
    if event_id in starter_candidates:
        technique_id, rationale_seed, alternatives_seed, missing_seed = starter_candidates[event_id]
        technique = techniques_by_id[technique_id]
        st.caption(
            f"Exercise starting point: {technique_id} — {technique['name']}. This is a proposed candidate only; "
            "review the description and alternatives before adding it."
        )
        if event_id == "E-04":
            st.info(
                "T1082 (System Information Discovery) is in the catalogue, but the supplied E-04 description "
                "does not establish that system information was queried. Do not map it without supporting telemetry."
            )
        already_suggested = any(
            item["evidence_id"] == event_id and item["technique_id"] == technique_id
            for item in st.session_state.mappings
        )
        if not already_suggested and st.button(f"Add proposed candidate {technique_id}"):
            st.session_state.mappings.append(
                create_mapping(
                    evidence_id=event_id,
                    technique=technique,
                    evidence_ids=[event_id],
                    rationale=rationale_seed,
                    alternatives=alternatives_seed,
                    missing_evidence=missing_seed,
                    confidence=2,
                    status="proposed",
                    include_in_export=True,
                )
            )
            st.success("Proposed candidate added; it is not a confirmed finding.")
            st.rerun()
    elif event_id == "E-06":
        st.info(
            "No specific exfiltration technique is preselected for E-06. Flow volume alone does not establish "
            "payload content, a command-and-control channel, or exfiltration."
        )

with map_tab:
    selected_mappings = st.session_state.mappings
    if not selected_mappings:
        st.info("Add candidate mappings to populate the visual map.")
    else:
        technique_rows = []
        for mapping in selected_mappings:
            tech = techniques_by_id[mapping["technique_id"]]
            for tactic_name in tech["tactics"] or ["Unspecified tactic"]:
                technique_rows.append(
                    {
                        "Tactic": tactic_name,
                        "Technique": f"{mapping['technique_id']} — {mapping['technique_name']}",
                        "Status": mapping["status"],
                        "Evidence": ", ".join(mapping["evidence_ids"]),
                        "Confidence": f"{mapping['confidence']}/5",
                        "Rationale": mapping["rationale"] or "No rationale recorded",
                        "Missing evidence": mapping["missing_evidence"] or "Not recorded",
                    }
                )
        frame = pd.DataFrame(technique_rows)
        fig = px.scatter(
            frame,
            x="Tactic",
            y="Technique",
            color="Status",
            hover_data=["Evidence", "Confidence", "Rationale", "Missing evidence"],
            color_discrete_map={
                "supported": "#3A8D67",
                "proposed": "#E5A93D",
                "requires further investigation": "#4787B8",
                "rejected": "#9A6673",
            },
            title="Candidate techniques grouped by tactic (not a confirmed attack sequence)",
        )
        fig.update_traces(marker={"size": 18})
        fig.update_layout(height=max(420, 42 * len(set(row["Technique"] for row in technique_rows))))
        st.plotly_chart(fig, width="stretch")
        st.markdown(
            "**Legend:** green = supported by the student's stated rationale; amber = proposed; "
            "blue = needs further investigation; muted red = rejected. Tactic placement is not a timeline."
        )
        st.caption(
            "ATT&CK describes adversary behaviour; this training map records analyst assessments and unresolved questions."
        )
