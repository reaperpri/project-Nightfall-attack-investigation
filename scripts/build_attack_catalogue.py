"""Extract a compact Enterprise ATT&CK catalogue from MITRE's pinned STIX file."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


EXPECTED_VERSION = "15.1"
SOURCE_URL = (
    "https://github.com/mitre-attack/attack-stix-data/blob/master/"
    "enterprise-attack/enterprise-attack-15.1.json"
)


def build_catalogue(source_path: Path, output_path: Path) -> dict[str, Any]:
    raw_bytes = source_path.read_bytes()
    bundle = json.loads(raw_bytes)
    collection = next(
        (obj for obj in bundle.get("objects", []) if obj.get("type") == "x-mitre-collection"),
        None,
    )
    if collection is None or collection.get("x_mitre_version") != EXPECTED_VERSION:
        actual = collection.get("x_mitre_version") if collection else "missing"
        raise ValueError(f"Expected MITRE ATT&CK {EXPECTED_VERSION}; source reports {actual}.")

    active = [
        obj
        for obj in bundle["objects"]
        if obj.get("type") == "attack-pattern"
        and not obj.get("revoked")
        and not obj.get("x_mitre_deprecated")
    ]
    patterns_by_stix_id = {obj["id"]: obj for obj in active}
    external_ids: dict[str, str] = {}
    for obj in active:
        ext_id = next(
            (
                ref.get("external_id")
                for ref in obj.get("external_references", [])
                if ref.get("source_name") == "mitre-attack"
            ),
            None,
        )
        if ext_id:
            external_ids[obj["id"]] = ext_id

    children: dict[str, list[str]] = {}
    for relationship in bundle["objects"]:
        if relationship.get("type") != "relationship" or relationship.get("relationship_type") != "subtechnique-of":
            continue
        child = external_ids.get(relationship.get("source_ref", ""))
        parent = external_ids.get(relationship.get("target_ref", ""))
        if child and parent:
            children.setdefault(parent, []).append(child)

    techniques = []
    for stix_id, technique_id in external_ids.items():
        pattern = patterns_by_stix_id[stix_id]
        parent_id = next(
            (
                external_ids.get(relationship.get("target_ref", ""))
                for relationship in bundle["objects"]
                if relationship.get("type") == "relationship"
                and relationship.get("relationship_type") == "subtechnique-of"
                and relationship.get("source_ref") == stix_id
            ),
            None,
        )
        techniques.append(
            {
                "technique_id": technique_id,
                "name": pattern["name"],
                "description": pattern.get("description", ""),
                "tactics": sorted(
                    {
                        phase["phase_name"]
                        for phase in pattern.get("kill_chain_phases", [])
                        if phase.get("kill_chain_name") == "mitre-attack"
                    }
                ),
                "platforms": sorted(pattern.get("x_mitre_platforms", [])),
                "is_subtechnique": bool(pattern.get("x_mitre_is_subtechnique", False)),
                "parent_technique_id": parent_id,
                "subtechnique_ids": sorted(children.get(technique_id, [])),
            }
        )
    techniques.sort(key=lambda item: item["technique_id"])
    catalogue = {
        "metadata": {
            "catalogue_version": EXPECTED_VERSION,
            "domain": "enterprise-attack",
            "source_url": SOURCE_URL,
            "retrieved_date": date.today().isoformat(),
            "source_type": "Official MITRE ATT&CK STIX 2.1 release, version-pinned file",
            "source_bundle_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "active_technique_count": len(techniques),
            "notes": "Active Enterprise attack-pattern objects and subtechnique-of relationships extracted from the pinned STIX bundle.",
        },
        "techniques": techniques,
    }
    output_path.write_text(json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return catalogue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Local MITRE enterprise-attack-15.1.json file")
    parser.add_argument("output", type=Path, help="Destination catalogue JSON path")
    args = parser.parse_args()
    catalogue = build_catalogue(args.source, args.output)
    print(f"Wrote {len(catalogue['techniques'])} Enterprise ATT&CK {EXPECTED_VERSION} techniques to {args.output}")


if __name__ == "__main__":
    main()
