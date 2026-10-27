# Project Nightfall — Threat Hunting & ATT&CK Investigation Lab

**Investigate the evidence. Map the behaviour. Defend the organisation.**

Project Nightfall is a local, synthetic-evidence workshop for hypothesis-driven threat hunting and MITRE ATT&CK Enterprise v15.1 analysis. Students examine an ambiguous fictional incident, distinguish observations from assumptions, test investigative hypotheses, annotate candidate technique mappings, develop measurable defensive recommendations, and export a MITRE ATT&CK Navigator layer and a cautious Markdown report.

> **Training simulation only.** Northstar Components, people, hosts, times, alerts, and records are fictional. Documentation-only IP ranges are used. This project does not connect to enterprise systems or execute command strings from evidence.

## Learning objectives

- Separate directly observed records, interpretations, and conclusions.
- Correlate identity, endpoint, mail, cloud-audit, and network context without assuming causation.
- Use a version-pinned ATT&CK Enterprise catalogue and explain mapping rationale.
- Identify alternative explanations, missing evidence, confidence, and safe next actions.
- Create an importable ATT&CK Navigator layer and a report that preserves uncertainty.
- Relate findings to measurable defensive activity using official D3FEND resources.

## Features

- Streamlit home dashboard, interactive Plotly evidence timeline, and filters.
- Searchable evidence explorer, annotations, and filtered CSV download.
- Offline catalogue derived from the official MITRE ATT&CK Enterprise **15.1** STIX release, including tactics and sub-technique relationships.
- Candidate mapping workflow with evidence links, required rationale for supported status, alternatives, missing evidence, confidence, and map visualisation.
- Guided hypothesis worksheet, D3FEND-inspired recommendations, and five progressive reasoning challenges.
- Validated Navigator layer format 4.5 JSON export and an evidence-first Markdown report.
- Pytest coverage for data loading, filtering, mapping, export, validation, and reports.

## Screenshots

Capture real screenshots after launching the application. Suggested captures:

1. Save a screenshot of the home dashboard as `docs/screenshots/home.png`.
2. Save the evidence timeline as `docs/screenshots/timeline.png`.
3. Save a populated mapping workspace and attack map as `docs/screenshots/mapping.png`.
4. Replace this section with Markdown image links after the screenshots are captured.

No screenshots are fabricated or bundled.

## Project structure

```text
.
├── app.py
├── data/
│   ├── attack_catalogue_metadata.json
│   ├── attack_techniques.json
│   ├── defensive_recommendations.json
│   ├── incident_events.json
│   ├── investigation_hypotheses.json
│   └── navigator_format_provenance.json
├── docs/
│   ├── ATTACK_MAPPING_GUIDE.md
│   ├── GITHUB_SETUP.md
│   ├── INVESTIGATION_PLAYBOOK.md
│   ├── NAVIGATOR_LAYER_FORMAT.md
│   └── STUDENT_CHALLENGES.md
├── outputs/
├── pages/
├── scripts/
├── src/
└── tests/
```

## Prerequisites

- Python 3.11 or newer (the project has been authored and checked with Python 3.14.7).
- Git is optional for local use and required only if publishing a repository.
- A modern browser for Streamlit.
- No paid services, API keys, cloud accounts, database, or network access at runtime.

## VS Code and local setup

Open this folder in VS Code. In the integrated terminal, create a virtual environment:

```shell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```shell
source .venv/bin/activate
```

Install the declared dependencies:

```shell
python -m pip install -r requirements.txt
```

Launch the application:

```shell
streamlit run app.py
```

Run the automated tests:

```shell
python -m pytest -q
```

The catalogue, event case, challenge material, and recommendations are stored locally. Internet access is needed only to install dependencies or open linked official resources; the investigation workflow itself is offline.

## How to investigate the case

1. Start at the dashboard and read the simulation warning and timeline caveat.
2. Open **Incident Timeline** and compare the baseline, signal, and benign/ambiguous records.
3. Open **Evidence Explorer**. Filter/search, inspect complete source records, and save your observation, interpretation, alternatives, missing evidence, confidence, and potential relationships.
4. Open **Threat Hunting** and update the guided hypotheses. Procedures are worksheets, not real SIEM queries.
5. Open **ATT&CK Mapping**. Search by behaviour or ID, inspect the pinned catalogue, link supporting records, explain the mapping, record alternatives and missing evidence, and set a student confidence/status. A supported status requires both evidence and rationale.
6. Review the visual map and its status legend. Tactic placement does not imply a confirmed sequence.
7. Open **Defensive Recommendations** and connect potential controls to telemetry, outcomes, and limitations.
8. Complete **Student Challenges** and read the feedback after each response.

Do not conclude that the email caused the later events, that the account is compromised, or that organisational data was exfiltrated unless evidence supports that conclusion.

## ATT&CK and Navigator exports

On **Export Investigation**, download the validated `.json` layer. It uses Enterprise domain `enterprise-attack`, ATT&CK version `15.1`, and Navigator layer format `4.5`. Comments retain status, evidence IDs, rationale, alternatives, missing evidence, and analyst confidence. Colours and scores are custom student annotations—not official MITRE ratings.

To open it:

1. Visit [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/).
2. Choose **Open Existing Layer** from the layer menu and select the downloaded JSON.
3. Verify ATT&CK version **15.1** in the layer/version details; do not silently substitute another ATT&CK version.
4. Save/export from Navigator if you want to reopen the layer later. Keep the downloaded JSON as a portable copy.

The official format references and field choices are documented in [docs/NAVIGATOR_LAYER_FORMAT.md](docs/NAVIGATOR_LAYER_FORMAT.md). For mapping quality, read [docs/ATTACK_MAPPING_GUIDE.md](docs/ATTACK_MAPPING_GUIDE.md).

## Investigation report

Download a Markdown report from **Export Investigation**. It includes the synthetic scope, evidence timeline, observations and limitations, candidate mappings, hypothesis status and confidence, alternatives, recommendations, next steps, and version provenance. Unverified hypotheses are not described as confirmed incidents.

## Data provenance and version notes

- The local catalogue is derived from the official MITRE ATT&CK STIX release file `enterprise-attack-15.1.json`, downloaded and checked against its STIX collection metadata (`x_mitre_version: 15.1`) on 2026-10-27.
- The catalogue includes 637 active Enterprise ATT&CK v15.1 attack-pattern objects and their v15.1 tactic/sub-technique relationships; it is not the full STIX knowledge base.
- The source URL, date, and SHA-256 are in [data/attack_catalogue_metadata.json](data/attack_catalogue_metadata.json).
- MITRE ATT&CK data and descriptions are attributed to The MITRE Corporation and are made available under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/); see the source release for applicable notices. The MITRE ATT&CK name and mark remain MITRE's.
- The Navigator exporter follows the official layer-format 4.5 specification. ATT&CK data version and Navigator layer-format version are separate.
- The D3FEND links point to the official D3FEND resource. Recommendations are locally authored educational examples and do not claim a control guarantees prevention.

To refresh the local catalogue from an exact official source file, see [docs/ATTACK_MAPPING_GUIDE.md](docs/ATTACK_MAPPING_GUIDE.md) and run `python scripts/build_attack_catalogue.py <official-file> data/attack_techniques.json`. The builder refuses a STIX bundle that does not identify version 15.1.

## Ethical and safety statement

Use this project only as an educational exercise over synthetic records. Do not use it to access real accounts/systems, send phishing messages, scan targets, run malware, download suspicious files, or execute evidence-derived strings. It is not production incident-response software and is not suitable for real investigations without independent validation, governance, and evidence-handling controls.

## Troubleshooting

- **`python` not found:** install Python 3.11+ and ensure it is available in the terminal; on Windows, the `py` launcher may be used for setup instead.
- **PowerShell activation is blocked:** follow your organisation's PowerShell policy or use a terminal that allows activation; do not weaken security policy just for this workshop.
- **`streamlit` not found:** activate `.venv` and rerun `python -m pip install -r requirements.txt`.
- **Port is already in use:** launch with `streamlit run app.py --server.port 8502`.
- **Navigator rejects a layer:** use the JSON produced by the current Export page, verify its `versions.attack` is `15.1`, and review `docs/NAVIGATOR_LAYER_FORMAT.md`.
- **No internet:** install dependencies before going offline; then all bundled evidence, catalogue search, mapping, tests, and exports work locally.
- **Test failures:** run `python -m pytest -q` from the project root and include the full traceback when asking for help.

## GitHub

GitHub repository creation and push commands are in [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md). No remote repository is created or pushed by this project. Suggested initial commit message: `Build Project Nightfall investigation lab`.

## License

MIT. See [LICENSE](LICENSE).
