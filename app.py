"""Project Nightfall — Threat Hunting & ATT&CK Investigation Lab."""

import streamlit as st

from src.timeline import create_timeline
from src.ui_helpers import initialize_state


st.set_page_config(
    page_title="Project Nightfall — Threat Hunting Lab",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_state()
case = st.session_state.case_data
events = case["events"]
mappings = st.session_state.mappings
open_questions = [
    hypothesis
    for hypothesis in st.session_state.hypotheses
    if hypothesis.get("conclusion", "unresolved") == "unresolved"
]

st.markdown(
    """
    <style>
    .nightfall-hero { padding: 1.5rem 1.8rem; border-radius: 16px;
      background: linear-gradient(115deg, #10243a, #1a3b4e 65%, #315c62);
      color: #f3f6f7; margin-bottom: 1rem; }
    .nightfall-hero h1 { margin: 0 0 .4rem; color: #ffffff; }
    .nightfall-hero p { margin: 0; color: #d3e2e4; font-size: 1.05rem; }
    </style>
    <section class="nightfall-hero">
      <h1>Project Nightfall</h1>
      <p>Investigate the evidence. Map the behaviour. Defend the organisation.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.subheader("Incident overview")
st.markdown(
    "A fictional employee account, endpoint, and network generate a cluster of signals. "
    "Your job is to separate observation from inference, test alternative explanations, "
    "and document what the supplied evidence does—and does not—support."
)
st.info(
    "SIMULATED EVIDENCE — Northstar Components is fictional. Reserved documentation IP ranges are used. "
    "This lab does not connect to enterprise systems or execute commands found in records.",
    icon="🧪",
)

metric_columns = st.columns(4)
metric_columns[0].metric("Evidence records", len(events))
metric_columns[1].metric(
    "Candidate ATT&CK mappings",
    len(st.session_state.mappings),
)
metric_columns[2].metric("Unresolved questions", len(open_questions))
metric_columns[3].metric(
    "Investigation status",
    "In progress" if open_questions or not mappings else "Ready to review",
)

st.subheader("Investigation timeline")
st.plotly_chart(create_timeline(events), width="stretch")
st.caption(
    "Timeline positions show recorded timestamps only. The endpoint collector may be offset by approximately 45 seconds."
)

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Evidence to validate")
    st.dataframe(
        [
            {
                "ID": event["evidence_id"],
                "Time (UTC)": event["timestamp"][11:16],
                "Category": event["category"],
                "Record": event["event_description"],
            }
            for event in events
        ],
        width="stretch",
        hide_index=True,
    )
with right:
    st.subheader("Start here")
    st.markdown(
        """
        1. **Incident Timeline** — filter and compare the synthetic records.
        2. **Evidence Explorer** — record observations, alternatives, and missing evidence.
        3. **ATT&CK Mapping** — create justified candidate mappings from the local v15.1 catalogue.
        4. **Threat Hunting** — test guided hypotheses against the evidence.
        5. **Defensive Recommendations** — connect findings to measurable controls.
        6. **Export Investigation** — download a Navigator layer and cautious report.
        7. **Student Challenges** — check your evidence reasoning.
        """
    )
    st.caption(
        f"ATT&CK catalogue: Enterprise 15.1 · {len(st.session_state.catalogue['techniques'])} active techniques · "
        "offline after setup."
    )
