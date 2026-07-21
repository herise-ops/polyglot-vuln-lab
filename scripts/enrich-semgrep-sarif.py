#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from typing import Any


# Azure/GitHub Advanced Security uses numeric security-severity scores.
SEVERITY_CONFIG = {
    "CRITICAL": {
        "score": "9.5",
        "level": "error",
        "name": "critical",
        "rank": 4,
    },
    "HIGH": {
        "score": "8.0",
        "level": "error",
        "name": "high",
        "rank": 3,
    },
    "ERROR": {  # Older Semgrep equivalent of HIGH
        "score": "8.0",
        "level": "error",
        "name": "high",
        "rank": 3,
    },
    "MEDIUM": {
        "score": "5.0",
        "level": "warning",
        "name": "medium",
        "rank": 2,
    },
    "WARNING": {  # Older Semgrep equivalent of MEDIUM
        "score": "5.0",
        "level": "warning",
        "name": "medium",
        "rank": 2,
    },
    "LOW": {
        "score": "2.0",
        "level": "note",
        "name": "low",
        "rank": 1,
    },
    "INFO": {  # Older Semgrep equivalent of LOW
        "score": "2.0",
        "level": "note",
        "name": "low",
        "rank": 1,
    },
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def get_severity(finding: dict[str, Any]) -> str | None:
    extra = finding.get("extra", {})

    severity = extra.get("severity")
    if severity:
        return str(severity).upper()

    metadata = extra.get("metadata", {})
    severity = metadata.get("severity")
    if severity:
        return str(severity).upper()

    return None


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: enrich-semgrep-sarif.py "
            "<semgrep.json> <semgrep.sarif>"
        )

    semgrep_json_path = Path(sys.argv[1])
    sarif_path = Path(sys.argv[2])

    semgrep_data = load_json(semgrep_json_path)
    sarif_data = load_json(sarif_path)

    severity_by_rule: dict[str, str] = {}

    # Read Semgrep's original severity for every rule that produced a finding.
    for finding in semgrep_data.get("results", []):
        rule_id = finding.get("check_id")
        severity = get_severity(finding)

        if not rule_id or severity not in SEVERITY_CONFIG:
            continue

        existing = severity_by_rule.get(rule_id)

        # Keep the highest severity if a rule somehow appears with
        # more than one severity.
        if existing is None:
            severity_by_rule[rule_id] = severity
        elif (
            SEVERITY_CONFIG[severity]["rank"]
            > SEVERITY_CONFIG[existing]["rank"]
        ):
            severity_by_rule[rule_id] = severity

    enriched_rules = 0
    enriched_results = 0

    for run in sarif_data.get("runs", []):
        driver = run.get("tool", {}).get("driver", {})
        rules = driver.get("rules", [])

        for rule in rules:
            rule_id = rule.get("id")
            severity = severity_by_rule.get(rule_id)

            if not severity:
                continue

            config = SEVERITY_CONFIG[severity]

            properties = rule.setdefault("properties", {})
            tags = properties.setdefault("tags", [])

            if "security" not in tags:
                tags.append("security")

            # This field produces Critical/High/Medium/Low in
            # Advanced Security.
            properties["security-severity"] = config["score"]

            # Preserve the original Semgrep meaning for inspection.
            properties["semgrep-severity"] = config["name"]

            # Also align SARIF's standard Error/Warning/Note level.
            default_configuration = rule.setdefault(
                "defaultConfiguration", {}
            )
            default_configuration["level"] = config["level"]

            enriched_rules += 1

        # Result-level severity overrides the rule default in SARIF.
        for result in run.get("results", []):
            rule_id = result.get("ruleId")
            severity = severity_by_rule.get(rule_id)

            if not severity:
                continue

            config = SEVERITY_CONFIG[severity]
            result["level"] = config["level"]

            result_properties = result.setdefault("properties", {})
            result_properties["semgrep-severity"] = config["name"]

            enriched_results += 1

    sarif_path.write_text(
        json.dumps(sarif_data, indent=2),
        encoding="utf-8",
    )

    print(f"Enriched SARIF rules: {enriched_rules}")
    print(f"Enriched SARIF results: {enriched_results}")

    for rule_id, severity in sorted(severity_by_rule.items()):
        config = SEVERITY_CONFIG[severity]
        print(
            f"{config['name'].upper():8} "
            f"score={config['score']} "
            f"rule={rule_id}"
        )


if __name__ == "__main__":
    main()