"""Document measurable defensive recommendations."""

import streamlit as st

from src.ui_helpers import render_page_header


render_page_header(
    "Defensive Recommendations",
    "Connect controls to a finding, measurable telemetry, expected outcomes, and limitations.",
)
st.info(
    "ATT&CK describes adversary behaviour. MITRE D3FEND organises defensive countermeasure knowledge. "
    "The references below point to the official D3FEND resource; no D3FEND identifiers are invented.",
    icon="🛡️",
)

for index, recommendation in enumerate(st.session_state.recommendations):
    with st.expander(f"{recommendation['purpose']} · {recommendation['finding']}", expanded=index == 0):
        st.markdown(f"**Proposed defensive action:** {recommendation['action']}")
        st.markdown(f"**Telemetry needed:** {recommendation['telemetry']}")
        st.markdown(f"**Expected outcome:** {recommendation['expected_outcome']}")
        st.markdown(f"**Limitations and assumptions:** {recommendation['limitations']}")
        st.markdown(f"**Authoritative starting point:** [{recommendation['reference']}]({recommendation['reference']})")
        with st.form(f"recommendation_{index}"):
            action = st.text_area("Edit proposed action", recommendation["action"], key=f"action_{index}")
            purpose = st.selectbox(
                "Purpose",
                ["Preventive", "Detective", "Response", "Preventive and detective", "Detective and response"],
                index=[
                    "Preventive",
                    "Detective",
                    "Response",
                    "Preventive and detective",
                    "Detective and response",
                ].index(recommendation["purpose"]),
                key=f"purpose_{index}",
            )
            telemetry = st.text_area("Telemetry to evaluate effectiveness", recommendation["telemetry"], key=f"telemetry_{index}")
            outcome = st.text_area("Expected outcome", recommendation["expected_outcome"], key=f"outcome_{index}")
            limitations = st.text_area("Limitations and assumptions", recommendation["limitations"], key=f"limits_{index}")
            if st.form_submit_button("Save recommendation"):
                recommendation.update(
                    {
                        "action": action,
                        "purpose": purpose,
                        "telemetry": telemetry,
                        "expected_outcome": outcome,
                        "limitations": limitations,
                    }
                )
                st.success("Recommendation saved for this session.")

st.markdown("[Open MITRE D3FEND](https://d3fend.mitre.org/)")
st.caption(
    "Recommendations are educational starting points, not guarantees that an attack will be prevented or detected."
)
