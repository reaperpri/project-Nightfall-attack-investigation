"""Export an annotated ATT&CK Navigator layer and investigation report."""

import json

import streamlit as st

from src.navigator_export import build_navigator_layer, validate_navigator_layer
from src.report_generator import generate_report
from src.ui_helpers import catalogue_by_id, render_page_header


render_page_header(
    "Export Investigation",
    "Download a Navigator v4.5 layer and a report that preserves uncertainty and evidence references.",
)
catalogue = st.session_state.catalogue
mappings = st.session_state.mappings
if not mappings:
    st.info("No candidate mappings have been recorded. The report remains available; add mappings before creating a non-empty layer.")

try:
    layer = build_navigator_layer(mappings, catalogue)
    layer_text = json.dumps(layer, indent=2, ensure_ascii=False) + "\n"
    layer_errors = validate_navigator_layer(layer, catalogue_by_id())
except (KeyError, TypeError, ValueError) as exc:
    layer = None
    layer_text = ""
    layer_errors = [str(exc)]

if layer_errors:
    st.error("Layer validation failed: " + "; ".join(layer_errors))
else:
    st.success(
        f"Valid Navigator layer · Enterprise ATT&CK {layer['versions']['attack']} · "
        f"layer format {layer['versions']['layer']} · {len(layer['techniques'])} techniques"
    )
    st.download_button(
        "Download ATT&CK Navigator JSON",
        data=layer_text.encode("utf-8"),
        file_name="project_nightfall_navigator_layer.json",
        mime="application/json",
        disabled=not layer["techniques"],
    )
    with st.expander("Preview Navigator JSON"):
        st.code(layer_text, language="json")

report = generate_report(
    st.session_state.case_data,
    st.session_state.case_data["events"],
    mappings,
    st.session_state.hypotheses,
    st.session_state.recommendations,
    st.session_state.analysis_notes,
)
st.download_button(
    "Download investigation report (Markdown)",
    data=report.encode("utf-8"),
    file_name="project_nightfall_investigation_report.md",
    mime="text/markdown",
)
with st.expander("Preview report"):
    st.markdown(report)

st.subheader("Import and validate a Navigator JSON layer")
upload = st.file_uploader("Choose a Navigator layer JSON", type=["json"])
if upload is not None:
    try:
        imported = json.loads(upload.getvalue())
        errors = validate_navigator_layer(imported, catalogue_by_id())
        if errors:
            st.error("Layer not accepted: " + "; ".join(errors))
        else:
            st.success(
                f"Valid Navigator layer: {imported['name']} · ATT&CK {imported['versions']['attack']} · "
                f"{len(imported['techniques'])} technique annotations."
            )
            st.caption("Imported layer is validated for this exercise and is not merged into your working mappings.")
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, KeyError) as exc:
        st.error(f"Could not read a valid Navigator JSON layer: {exc}")

with st.expander("Import the layer into ATT&CK Navigator"):
    st.markdown(
        """
        1. Download the layer above.
        2. Open [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/).
        3. In the Navigator layer menu, choose **Open Existing Layer** and select the downloaded JSON file.
        4. Confirm the layer's ATT&CK version is **15.1** in the layer/version details; do not silently switch to another matrix version.
        5. Save or export the layer from Navigator to reopen it later. Keep the original JSON as a portable copy.

        The layer uses the official Navigator v4.5 format. Comments preserve status, evidence, rationale,
        alternatives, missing evidence, and analyst-defined confidence. Scores/colours are classroom annotations,
        not MITRE ratings. Adjacent tactics do not imply chronology or causation.
        """
    )
