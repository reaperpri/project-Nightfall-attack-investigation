# Navigator Layer Format and Provenance

The exporter follows the official MITRE ATT&CK Navigator **layer format v4.5**. Before implementation, the project checked the official format document and sample layer:

- Specification: https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md
- Example: https://github.com/mitre-attack/attack-navigator/blob/master/layers/samples/Bear_APT.json
- Local provenance record: `data/navigator_format_provenance.json`

The generated JSON uses the documented `versions` object (`attack`, `navigator`, `layer`), Enterprise domain `enterprise-attack`, `techniqueID`, `score`, `color`, and `comment` fields, and layer metadata. Confidence/status/rationale/evidence references use technique comments because they are analyst annotations rather than ATT&CK catalog metadata.

The format version is 4.5; the ATT&CK data version is 15.1. These are different version values and should not be conflated. The `navigator` version identifies the compatible Navigator client format baseline.
