# ATT&CK Mapping Guide

## What the mapping means

MITRE ATT&CK describes adversary behaviour. A technique mapping is an analyst interpretation of evidence; it does not prove malicious intent, attribution, compromise, or a complete attack sequence. ATT&CK tactics group techniques by adversary goal and are not a timeline.

This lab pins its Enterprise catalogue to **ATT&CK 15.1**, the official MITRE STIX release `enterprise-attack-15.1.json`. The bundled local catalogue contains active technique objects, names, descriptions, platforms, tactics, and sub-technique relationships. Provenance and the downloaded source hash are recorded in `data/attack_catalogue_metadata.json`.

Official source: [MITRE ATT&CK STIX data, Enterprise 15.1](https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-15.1.json).

## A defensible mapping workflow

1. Select the evidence record whose behaviour you are assessing.
2. Search the local catalogue by ID or behaviour; filter by tactic as a narrowing aid.
3. Read the technique description and inspect available sub-techniques.
4. Link one or more evidence IDs and state exactly which observed behaviour supports the candidate.
5. Record plausible alternatives and the missing evidence that could distinguish them.
6. Use **Supported** only after entering a rationale and linked evidence. Confidence is analyst-defined (1–5), not official MITRE metadata.
7. Revisit and revise mappings as new evidence changes the assessment. Rejection is a valid analytical result.

Receiving an email does not prove phishing succeeded; an unfamiliar sign-in does not prove account compromise; an unusual flow does not prove data exfiltration. Match the behaviour actually observed and avoid mapping intent that the evidence cannot establish.

## Exercise seed ideas

- E-01: T1566 (Phishing) is a question to investigate, not an automatic match: no click or payload evidence is supplied.
- E-03: T1059 (Command and Scripting Interpreter) may describe the observed office-app child process; the command and actions remain unknown.
- E-04: T1057 (Process Discovery) is relevant to the process query; context and script telemetry are still needed.
- E-04: T1082 (System Information Discovery) must not be used unless the observed query actually supports system-information discovery.
- E-06: Do not force an exfiltration mapping based only on flow volume. T1041 is specific to exfiltration over a C2 channel and requires evidence for that behaviour.

## Reproducibly refresh the local catalogue

The application does not need network access. To rebuild the catalogue, obtain the exact official v15.1 file from the source URL above, then run:

```shell
python scripts/build_attack_catalogue.py enterprise-attack-15.1.json data/attack_techniques.json
```

The utility rejects files whose STIX collection does not identify version 15.1. Review the generated hash and active technique count before replacing bundled data.
