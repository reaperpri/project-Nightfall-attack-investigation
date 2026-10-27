# Project Nightfall Investigation Playbook

## Ground rules

- This case and every record are synthetic; Northstar Components is fictional.
- Documentation-only IP ranges are used. Do not treat them as real attribution.
- An event is an observation, an interpretation is a hypothesis, and a conclusion needs corroborating evidence.
- The records are intentionally incomplete. E-10 notes an approximate endpoint clock offset of 45 seconds.
- Never execute strings copied from evidence or attempt to access real accounts, hosts, or services.

## Suggested investigation sequence

### 1. Scope and timeline

Review the baseline sign-in E-00, the email E-01, identity event E-02, endpoint events E-03/E-04, access event E-05, network alert E-06, and context records E-07 through E-11. Use the category, host, confidence, and time filters. Note the collector offset before making fine-grained ordering claims.

### 2. Separate evidence and inference

For each selected record, write:

- Directly observed fields and source.
- What the behaviour could indicate.
- At least one alternative explanation.
- What evidence would test those explanations.
- A confidence rating and related records.

Do not treat the sequence of records as proof that the email caused later events.

### 3. Test hypotheses

Use the guided worksheet to assess the unfamiliar sign-in, office-app child process, discovery-like queries, document access, and outbound transfer. Identify both supporting and contradictory observations. State a next action that is specific and safe.

### 4. Map behaviour carefully

Search the offline Enterprise ATT&CK 15.1 catalogue. Link the evidence, rationale, alternatives, and missing evidence to each candidate. Require a rationale before using **Supported**. Preserve rejected and unresolved mappings as analytical outcomes.

### 5. Recommend and report

Tie preventive, detective, or response recommendations to a specific finding and telemetry. The D3FEND link is an authoritative starting point, not a claim that a control guarantees prevention. Export the report and Navigator layer; inspect the comments before sharing.

## Guided questions

1. Was the unfamiliar sign-in consistent with legitimate employee activity?
2. Did the office application's child process execute an interpreter, and what telemetry can establish its actions?
3. Which process or system details were enumerated?
4. Was sensitive information accessed, downloaded, or shared?
5. What evidence would establish whether the outbound transfer contained organisational data?

## Safety and scope

This project is not a SIEM, a live threat-intelligence service, or a production incident-response platform. No real systems are queried. Procedures are investigation worksheets only. Follow your organisation's authority, evidence-preservation requirements, and privacy policies in any real incident.
