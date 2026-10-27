"""Shared Streamlit session setup and page presentation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import streamlit as st

from src.data_loader import load_case, load_hypotheses, load_recommendations, load_technique_catalogue


def initialize_state() -> None:
    """Create isolated, per-browser-session working copies of case data."""
    if "case_data" not in st.session_state:
        st.session_state.case_data = load_case()
    if "catalogue" not in st.session_state:
        st.session_state.catalogue = load_technique_catalogue()
    if "analysis_notes" not in st.session_state:
        st.session_state.analysis_notes = {}
    if "mappings" not in st.session_state:
        st.session_state.mappings = []
    if "hypotheses" not in st.session_state:
        st.session_state.hypotheses = deepcopy(load_hypotheses())
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = deepcopy(load_recommendations())
    if "challenge_answers" not in st.session_state:
        st.session_state.challenge_answers = {}


def render_page_header(title: str, subtitle: str = "") -> None:
    initialize_state()
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.warning(
        "Training simulation only. All evidence is synthetic; event order does not establish causation, "
        "and candidate mappings are not confirmed incident findings.",
        icon="⚠️",
    )


def evidence_ids() -> list[str]:
    return [event["evidence_id"] for event in st.session_state.case_data["events"]]


def catalogue_by_id() -> dict[str, dict[str, Any]]:
    return {
        technique["technique_id"]: technique
        for technique in st.session_state.catalogue["techniques"]
    }


def save_analysis_notes(evidence_id: str, values: dict[str, Any]) -> None:
    st.session_state.analysis_notes[evidence_id] = values
