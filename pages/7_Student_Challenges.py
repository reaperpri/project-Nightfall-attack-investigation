"""Progressive reasoning challenges for the synthetic case."""

import streamlit as st

from src.ui_helpers import render_page_header


render_page_header(
    "Student Challenges",
    "Make a choice first; feedback and reasoning appear only after submission.",
)

challenges = [
    {
        "id": "challenge_1",
        "title": "Challenge 1 — Evidence or assumption?",
        "prompt": "The unfamiliar sign-in proves that an attacker compromised the employee account.",
        "choices": ["Observed evidence", "Hypothesis", "Unsupported conclusion"],
        "answer": "Unsupported conclusion",
        "feedback": "E-02 records a successful sign-in from an unfamiliar address and an MFA approval. That observation merits investigation, but the available fields do not establish who authenticated or whether access was unauthorised.",
    },
    {
        "id": "challenge_2",
        "title": "Challenge 2 — Find the ATT&CK mapping",
        "prompt": "E-04 reports running-process and installed-security-software queries. Which mapping is best supported by that observation alone?",
        "choices": ["T1057 — Process Discovery", "T1566 — Phishing", "T1041 — Exfiltration Over C2 Channel"],
        "answer": "T1057 — Process Discovery",
        "feedback": "T1057 is a plausible candidate for the process-enumeration behaviour, but the installed-security-product query also needs context. A rationale and alternative explanations are still required; no single event confirms an adversary.",
    },
    {
        "id": "challenge_3",
        "title": "Challenge 3 — Identify the missing evidence",
        "prompt": "What would best test whether the 24 MiB outbound flow contained organisational data?",
        "choices": [
            "Process-to-network attribution plus relevant file/document and transfer context",
            "A second unrelated sign-in record",
            "The alert volume threshold alone",
        ],
        "answer": "Process-to-network attribution plus relevant file/document and transfer context",
        "feedback": "Flow size is not payload content. Attribution, destination context, document/download events, and appropriate content evidence would strengthen or contradict the hypothesis.",
    },
    {
        "id": "challenge_4",
        "title": "Challenge 4 — Build the investigation map",
        "prompt": "Which mapping is ready to mark Supported?",
        "choices": [
            "Any mapping with a high numeric confidence score",
            "A mapping with an explicit analyst rationale and linked evidence, while alternatives are recorded",
            "Every technique displayed in an adjacent ATT&CK tactic",
        ],
        "answer": "A mapping with an explicit analyst rationale and linked evidence, while alternatives are recorded",
        "feedback": "The mapping workflow requires a rationale and evidence before a mapping can be marked supported. Confidence is student-defined and cannot replace evidence.",
    },
    {
        "id": "challenge_5",
        "title": "Challenge 5 — Defend your conclusion",
        "prompt": "Which statement best communicates a defensible current conclusion?",
        "choices": [
            "The email caused exfiltration.",
            "Several observations merit correlation; the supplied records do not establish compromise or data exfiltration.",
            "The 24 MiB flow proves sensitive documents left the organisation.",
        ],
        "answer": "Several observations merit correlation; the supplied records do not establish compromise or data exfiltration.",
        "feedback": "A good conclusion states what is known, what remains a hypothesis, what is not established, and the next evidence needed to discriminate between explanations.",
    },
]

for challenge in challenges:
    with st.expander(challenge["title"], expanded=challenge["id"] not in st.session_state.challenge_answers):
        with st.form(challenge["id"]):
            selection = st.radio(challenge["prompt"], challenge["choices"], key=f"{challenge['id']}_selection")
            submitted = st.form_submit_button("Check my reasoning")
        if submitted:
            st.session_state.challenge_answers[challenge["id"]] = selection
        if challenge["id"] in st.session_state.challenge_answers:
            selected = st.session_state.challenge_answers[challenge["id"]]
            if selected == challenge["answer"]:
                st.success("Good reasoning.")
            else:
                st.info(f"Review this distinction. Your choice: **{selected}**")
            st.markdown(f"**Best answer:** {challenge['answer']}")
            st.write(challenge["feedback"])
