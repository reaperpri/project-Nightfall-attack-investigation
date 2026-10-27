"""Generate a cautious, evidence-first Markdown case report."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def generate_report(
    case: dict[str, Any],
    events: list[dict[str, Any]],
    mappings: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
    analysis_notes: dict[str, dict[str, Any]] | None = None,
) -> str:
    """Return a downloadable report that distinguishes observations from analysis."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Project Nightfall — Investigation Report",
        "",
        "> **SIMULATED TRAINING CASE.** All identities, hosts, timestamps, addresses, alerts, and records are synthetic.",
        "",
        f"- Case: {case.get('case_id', 'NIGHTFALL-SIM-001')}",
        f"- Organisation: {case.get('organisation', 'Fictional organisation')}",
        f"- Report generated: {now}",
        "- ATT&CK: Enterprise 15.1 (pinned local catalogue)",
        "- Catalogue provenance: official MITRE ATT&CK STIX release `enterprise-attack-15.1.json`; see `data/attack_catalogue_metadata.json`.",
        "",
        "## 1. Executive summary",
        "",
        "This exercise contains signals that merit validation, including an unfamiliar sign-in, an office-application child process, discovery-like queries, unusual document access, and an outbound-flow alert. The supplied records do not establish that the email caused later activity, that the account or endpoint was compromised, or that organisational data was exfiltrated.",
        "",
        "## 2. Incident scope",
        "",
        f"Review covers {len(events)} synthetic evidence records for {case.get('incident_date', 'the simulated incident date')}. The records are limited to the bundled case data and student analysis entered in this browser session.",
        "",
        "## 3. Evidence timeline",
        "",
        "| ID | Timestamp (UTC) | Category | Description |",
        "|---|---|---|---|",
    ]
    for event in sorted(events, key=lambda item: item["timestamp"]):
        description = str(event["event_description"]).replace("|", "\\|")
        lines.append(
            f"| {event['evidence_id']} | {event['timestamp']} | {event['category']} | {description} |"
        )
    lines.extend(["", "## 4. Key observations", ""])
    for event in events:
        lines.extend(
            [
                f"### {event['evidence_id']} — {event['event_description']}",
                f"- **Observed:** {event['observed_behaviour']}",
                f"- **Potential significance (not a conclusion):** {event['potential_significance']}",
                f"- **Source and confidence:** {event['data_source']}; source confidence {event['confidence']:.0%}.",
                f"- **Limitations:** {event['evidence_limitations']}",
                "",
            ]
        )
    lines.extend(["## 5. Candidate ATT&CK mappings", ""])
    if not mappings:
        lines.append("No candidate mappings have been recorded.")
    for mapping in mappings:
        lines.extend(
            [
                f"### {mapping['technique_id']} — {mapping.get('technique_name', 'Technique')}",
                f"- **Status:** {mapping['status']}",
                f"- **Analyst-defined confidence:** {mapping['confidence']}/5",
                f"- **Evidence:** {', '.join(mapping.get('evidence_ids', []))}",
                f"- **Rationale:** {mapping.get('rationale') or 'Not recorded'}",
                f"- **Alternative explanations:** {mapping.get('alternative_explanations') or 'Not recorded'}",
                f"- **Missing evidence:** {mapping.get('missing_evidence') or 'Not recorded'}",
                "",
            ]
        )
    lines.extend(["## 6. Student evidence analysis", ""])
    notes_by_id = analysis_notes or {}
    saved_notes = [(event_id, note) for event_id, note in notes_by_id.items() if event_id in {e["evidence_id"] for e in events}]
    if not saved_notes:
        lines.append("No student evidence annotations have been recorded.")
    for event_id, note in saved_notes:
        lines.extend(
            [
                f"### {event_id}",
                f"- **Direct observation:** {note.get('direct_observation') or 'Not recorded'}",
                f"- **Interpretation:** {note.get('interpretation') or 'Not recorded'}",
                f"- **Alternatives:** {note.get('alternatives') or 'Not recorded'}",
                f"- **Additional evidence:** {note.get('additional_evidence') or 'Not recorded'}",
                f"- **Analyst confidence:** {note.get('confidence', 'Not recorded')}/5",
                f"- **Related evidence selected by analyst:** {', '.join(note.get('related_events', [])) or 'None'}",
                "",
            ]
        )
    lines.extend(["## 7. Hypotheses, confidence, and unresolved questions", ""])
    if not hypotheses:
        lines.append("No investigation hypotheses have been recorded.")
    for hypothesis in hypotheses:
        lines.extend(
            [
                f"### {hypothesis['hypothesis_id']} — {hypothesis['question']}",
                f"- **Conclusion:** {hypothesis.get('conclusion', 'unresolved')} (student analysis; not independently verified)",
                f"- **Confidence:** {hypothesis.get('confidence', 0):.0%}",
                f"- **Findings:** {hypothesis.get('findings') or 'Not recorded'}",
                f"- **Next action:** {hypothesis.get('next_action') or 'Not recorded'}",
                "",
            ]
        )
    lines.extend(["## 8. Alternative explanations", ""])
    alternatives = list(dict.fromkeys(
        mapping.get("alternative_explanations", "").strip()
        for mapping in mappings
        if mapping.get("alternative_explanations", "").strip()
    ))
    lines.extend([f"- {item}" for item in alternatives] or ["- No analyst alternatives have been recorded; normal business activity, approved tooling, VPN/shared egress, and backup activity remain examples to test against evidence."])
    lines.extend(["", "## 9. Defensive recommendations", ""])
    for recommendation in recommendations:
        lines.extend(
            [
                f"- **{recommendation['purpose']}:** {recommendation['action']}",
                f"  - Related finding: {recommendation['finding']}",
                f"  - Telemetry/outcome: {recommendation['telemetry']} {recommendation['expected_outcome']}",
                f"  - Limitations: {recommendation['limitations']}",
                f"  - Reference: {recommendation['reference']}",
            ]
        )
    lines.extend(
        [
            "",
            "## 10. Limitations",
            "",
            "All evidence is synthetic and intentionally incomplete. Documentation-range addresses are reserved examples. No real identity provider, endpoint, mail system, SIEM, or network was queried. Event ordering is approximate where the endpoint collector clock may be offset. ATT&CK describes observed adversary behaviour; a mapping is an analyst interpretation, not proof of attribution or intent. D3FEND references are starting points, not guarantees of prevention.",
            "",
            "## 11. Suggested next investigative steps",
            "",
            "- Validate the unfamiliar sign-in using full session, device, MFA, and employee-confirmation context.",
            "- Reconstruct process lineage and review collected script telemetry without executing recovered strings.",
            "- Establish the business context and sensitivity of the accessed documents.",
            "- Attribute the outbound flow to a process and destination; use appropriate content evidence before claiming data exfiltration.",
            "- Reconcile timestamps with the documented collector offset and preserve original evidence context.",
            "",
            "## 12. Version and provenance",
            "",
            "- MITRE ATT&CK Enterprise v15.1, official pinned STIX release file `enterprise-attack-15.1.json`.",
            "- Navigator layer format v4.5, checked against the official Navigator specification.",
            "- Source URL: https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-15.1.json",
            "- D3FEND: https://d3fend.mitre.org/",
            "",
        ]
    )
    return "\n".join(lines)
