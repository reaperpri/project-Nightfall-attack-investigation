"""Hypothesis-driven investigation worksheet."""

import streamlit as st

from src.ui_helpers import render_page_header


render_page_header(
    "Threat Hunting",
    "Formulate a testable question, name what could disprove it, and record a bounded next step.",
)
hypotheses = st.session_state.hypotheses
labels = [f"{item['hypothesis_id']} — {item['question']}" for item in hypotheses]
selected_label = st.selectbox("Guided investigation question", labels)
index = labels.index(selected_label)
hypothesis = hypotheses[index]

st.markdown(f"### {hypothesis['question']}")
with st.form(f"hypothesis_{hypothesis['hypothesis_id']}"):
    supporting = st.text_area(
        "Supporting observations (evidence IDs)",
        value=", ".join(hypothesis["supporting_observations"]),
    )
    contradictions = st.text_area(
        "Evidence that would contradict this hypothesis",
        value="\n".join(hypothesis["contradicting_evidence"]),
    )
    sources = st.text_area(
        "Data sources to inspect",
        value="\n".join(hypothesis["data_sources"]),
    )
    procedure = st.text_area("Search / analysis procedure", value=hypothesis["procedure"])
    findings = st.text_area("Findings (separate observations from interpretation)", value=hypothesis["findings"])
    conclusion = st.selectbox(
        "Current assessment",
        ["unresolved", "evidence supports", "evidence contradicts", "inconclusive"],
        index=["unresolved", "evidence supports", "evidence contradicts", "inconclusive"].index(
            hypothesis.get("conclusion", "unresolved")
        ),
    )
    confidence = st.slider("Analyst confidence", 0.0, 1.0, float(hypothesis["confidence"]), 0.05)
    next_action = st.text_area("Next investigative action", value=hypothesis["next_action"])
    if st.form_submit_button("Save hypothesis worksheet"):
        hypothesis.update(
            {
                "supporting_observations": [item.strip() for item in supporting.split(",") if item.strip()],
                "contradicting_evidence": [item.strip() for item in contradictions.splitlines() if item.strip()],
                "data_sources": [item.strip() for item in sources.splitlines() if item.strip()],
                "procedure": procedure,
                "findings": findings,
                "conclusion": conclusion,
                "confidence": confidence,
                "next_action": next_action,
            }
        )
        st.success("Worksheet saved to this browser session.")

with st.expander("Guided examples and investigation safety"):
    st.markdown(
        """
        - Was the unfamiliar sign-in consistent with legitimate employee activity?
        - Did the office application's child process execute an interpreter?
        - Which process or system details were enumerated?
        - Was sensitive information accessed?
        - What evidence would establish whether an outbound transfer contained organisational data?

        Procedures are classroom exercises over the supplied synthetic records. They do not query a real SIEM,
        identity provider, endpoint, or network. Never execute strings copied from evidence.
        """
    )
