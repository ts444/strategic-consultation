#!/usr/bin/env python3
"""Deterministic validator CLI for phase artifacts."""

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

from validator import Violation, Warning
from validator.rules import (
    assumption_resolution_required,
    claim_composition_resolvable,
    claim_confidence_present,
    claim_label_present,
    claim_source_present,
    confidence_propagation,
    framework_name_in_structured_fields,
    frontmatter_required_fields,
    gap_compliance_drivers_field,
    label_producer_binding,
    recommendation_required_fields,
    roadmap_item_required_fields,
    rsk_likelihood_impact,
    template_conformance,
    trace_populated,
)

_WARN_CHECKERS: list[tuple[str, Callable[[Path], list[Warning]]]] = [
    (trace_populated.RULE, trace_populated.check),
]

_CHECKERS: list[tuple[str, Callable[[Path], list[Violation]]]] = [
    (assumption_resolution_required.RULE, assumption_resolution_required.check),
    (claim_label_present.RULE, claim_label_present.check),
    (claim_source_present.RULE, claim_source_present.check),
    (claim_confidence_present.RULE, claim_confidence_present.check),
    (frontmatter_required_fields.RULE, frontmatter_required_fields.check),
    (label_producer_binding.RULE, label_producer_binding.check),
    (confidence_propagation.RULE, confidence_propagation.check),
    (template_conformance.RULE, template_conformance.check),
    (gap_compliance_drivers_field.RULE, gap_compliance_drivers_field.check),
    (recommendation_required_fields.RULE, recommendation_required_fields.check),
    (roadmap_item_required_fields.RULE, roadmap_item_required_fields.check),
    (framework_name_in_structured_fields.RULE, framework_name_in_structured_fields.check),
    (claim_composition_resolvable.RULE, claim_composition_resolvable.check),
    (rsk_likelihood_impact.RULE, rsk_likelihood_impact.check),
]


def _run_rules(path: Path) -> dict[str, list[Violation]]:
    results: dict[str, list[Violation]] = {}
    for rule_name, check_fn in _CHECKERS:
        violations = check_fn(path)
        if violations:
            results[rule_name] = violations
    return results


def _run_warn_rules(path: Path) -> dict[str, list[Warning]]:
    results: dict[str, list[Warning]] = {}
    for rule_name, check_fn in _WARN_CHECKERS:
        warnings = check_fn(path)
        if warnings:
            results[rule_name] = warnings
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a phase artifact.")
    parser.add_argument("artifact", type=Path, help="Path to the artifact file")
    args = parser.parse_args(argv)

    path: Path = args.artifact
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    warn_results = _run_warn_rules(path)
    for rule_name, warnings in sorted(warn_results.items()):
        print(f"\n[WARN:{rule_name}]")
        for w in warnings:
            print(f"  warning: {w.message}")

    results = _run_rules(path)
    if not results:
        print(f"OK: {path}")
        return 0

    for rule_name, violations in sorted(results.items()):
        print(f"\n[{rule_name}]")
        for v in violations:
            loc = f"line {v.line}" if v.line is not None else "file"
            print(f"  {loc}: {v.message}")

    total = sum(len(vs) for vs in results.values())
    print(f"\n{total} violation(s) in {len(results)} rule(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
