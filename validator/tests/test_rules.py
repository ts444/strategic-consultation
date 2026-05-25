"""Tests for validator rules."""

from pathlib import Path

from validator.rules import (
    claim_confidence_present,
    claim_label_present,
    claim_source_present,
    confidence_propagation,
    frontmatter_required_fields,
    label_producer_binding,
    template_conformance,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FULL_FM = (
    "---\n"
    "phase: 00-intake\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: scope@1.0.0\n"
    "---\n"
)


def _artifact(tmp_path: Path, body: str, frontmatter: str = _FULL_FM) -> Path:
    f = tmp_path / "art.md"
    f.write_text(frontmatter + body, encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# claim_label_present
# ---------------------------------------------------------------------------


def test_label_present_pass(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "[known] [source:interview:2026-05-25/consultant] [conf:H]\n")
    assert claim_label_present.check(f) == []


def test_label_present_fail_source_no_label(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "[source:interview:2026-05-25/consultant] [conf:H]\n")
    violations = claim_label_present.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "claim_label_present"


def test_label_present_fail_conf_no_label(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "Some text [source:foo] [conf:M]\n")
    violations = claim_label_present.check(f)
    assert len(violations) == 1


def test_label_present_ignores_frontmatter_lines(tmp_path: Path) -> None:
    # Frontmatter lines have colons but not [source:]/[conf:] — no false positives
    f = _artifact(tmp_path, "# Plain heading, no claim tags\n")
    assert claim_label_present.check(f) == []


def test_label_present_multiple_violations(tmp_path: Path) -> None:
    body = (
        "[source:foo] [conf:H]\n"
        "[source:bar] [conf:L]\n"
    )
    f = _artifact(tmp_path, body)
    assert len(claim_label_present.check(f)) == 2


# ---------------------------------------------------------------------------
# claim_source_present
# ---------------------------------------------------------------------------


def test_source_present_pass(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[known] [source:customer-portal://assets/x@2026-01-01T00:00:00Z] [conf:H]\n",
    )
    assert claim_source_present.check(f) == []


def test_source_present_fail(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "[known] [conf:H]\n")
    violations = claim_source_present.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "claim_source_present"
    assert violations[0].line == 7  # 6 frontmatter lines + 1


def test_source_present_all_labels(tmp_path: Path) -> None:
    body = (
        "[inferred] [source:from: GAP-001 + REC-002] [conf:M]\n"
        "[elicited] [source:interview:2026-05-25/consultant] [conf:L]\n"
        "[assumed] [source:interview:2026-05-25/consultant] [conf:L]\n"
    )
    f = _artifact(tmp_path, body)
    assert claim_source_present.check(f) == []


def test_source_present_fail_multiple(tmp_path: Path) -> None:
    body = "[inferred] [conf:M]\n[elicited] [conf:L]\n"
    f = _artifact(tmp_path, body)
    assert len(claim_source_present.check(f)) == 2


# ---------------------------------------------------------------------------
# claim_confidence_present
# ---------------------------------------------------------------------------


def test_conf_present_pass_all_levels(tmp_path: Path) -> None:
    body = (
        "[known] [source:foo] [conf:H]\n"
        "[inferred] [source:bar] [conf:M]\n"
        "[assumed] [source:baz] [conf:L]\n"
    )
    f = _artifact(tmp_path, body)
    assert claim_confidence_present.check(f) == []


def test_conf_present_fail_missing(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "[assumed] [source:interview:2026-05-25/consultant]\n")
    violations = claim_confidence_present.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "claim_confidence_present"


def test_conf_present_fail_invalid_level(tmp_path: Path) -> None:
    # [conf:X] is not a valid level — regex requires H, M, or L
    f = _artifact(tmp_path, "[known] [source:foo] [conf:X]\n")
    violations = claim_confidence_present.check(f)
    assert len(violations) == 1


def test_conf_present_no_claims_no_violations(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "# No claims here\nJust plain text.\n")
    assert claim_confidence_present.check(f) == []


# ---------------------------------------------------------------------------
# frontmatter_required_fields
# ---------------------------------------------------------------------------


def test_frontmatter_pass(tmp_path: Path) -> None:
    f = tmp_path / "art.md"
    f.write_text(
        "---\n"
        "phase: 00-intake\n"
        "status: draft\n"
        "harness_version: 0.1.0\n"
        "template: scope@1.0.0\n"
        "---\n"
        "# Content\n",
        encoding="utf-8",
    )
    assert frontmatter_required_fields.check(f) == []


def test_frontmatter_fail_missing_phase(tmp_path: Path) -> None:
    f = tmp_path / "art.md"
    f.write_text(
        "---\nstatus: draft\nharness_version: 0.1.0\ntemplate: scope@1.0.0\n---\n",
        encoding="utf-8",
    )
    violations = frontmatter_required_fields.check(f)
    assert len(violations) == 1
    assert "phase" in violations[0].message


def test_frontmatter_fail_multiple_missing(tmp_path: Path) -> None:
    f = tmp_path / "art.md"
    f.write_text("---\nstatus: draft\n---\n", encoding="utf-8")
    violations = frontmatter_required_fields.check(f)
    messages = {v.message for v in violations}
    assert len(violations) == 3
    assert any("phase" in m for m in messages)
    assert any("harness_version" in m for m in messages)
    assert any("template" in m for m in messages)


def test_frontmatter_no_frontmatter_at_all(tmp_path: Path) -> None:
    f = tmp_path / "art.md"
    f.write_text("# Just markdown\nNo frontmatter.\n", encoding="utf-8")
    violations = frontmatter_required_fields.check(f)
    assert len(violations) == 4  # all four required fields missing


def test_frontmatter_nested_keys_not_counted(tmp_path: Path) -> None:
    # Indented YAML values should not be mistaken for top-level keys
    f = tmp_path / "art.md"
    f.write_text(
        "---\n"
        "phase: 00-intake\n"
        "status: draft\n"
        "harness_version: 0.1.0\n"
        "template: scope@1.0.0\n"
        "extra:\n"
        "  nested_key: value\n"
        "---\n",
        encoding="utf-8",
    )
    assert frontmatter_required_fields.check(f) == []


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


def test_cli_valid_artifact(tmp_path: Path) -> None:
    from validator.cli import main

    f = tmp_path / "valid.md"
    f.write_text(
        "---\n"
        "phase: 00-intake\n"
        "status: draft\n"
        "harness_version: 0.1.0\n"
        "template: scope@1.0.0\n"
        "---\n"
        "# Content\n"
        "[known] [source:customer-portal://x@2026-01-01T00:00:00Z] [conf:H]\n",
        encoding="utf-8",
    )
    assert main([str(f)]) == 0


def test_cli_invalid_artifact_exits_nonzero(tmp_path: Path) -> None:
    from validator.cli import main

    f = tmp_path / "bad.md"
    # Missing frontmatter fields and a claim with no source
    f.write_text("# no frontmatter\n[known] [conf:H]\n", encoding="utf-8")
    assert main([str(f)]) == 1


def test_cli_missing_file_exits_nonzero(tmp_path: Path) -> None:
    from validator.cli import main

    assert main([str(tmp_path / "nonexistent.md")]) == 1


def test_cli_groups_errors_by_rule(tmp_path: Path, capsys: object) -> None:
    from validator.cli import main

    f = tmp_path / "multi.md"
    # Two lines each missing label, so claim_label_present fires twice
    f.write_text(
        "---\nphase: 01\nstatus: draft\nharness_version: 0.1.0\ntemplate: t@1\n---\n"
        "[source:foo] [conf:H]\n"
        "[source:bar] [conf:M]\n",
        encoding="utf-8",
    )
    ret = main([str(f)])
    assert ret == 1
    captured = getattr(capsys, "readouterr", None)
    if captured:
        out = captured().out
        assert "[claim_label_present]" in out


# ---------------------------------------------------------------------------
# label_producer_binding
# ---------------------------------------------------------------------------

_SYNTH_FM = (
    "---\n"
    "phase: 02-gap\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: gaps@1.0.0\n"
    "produced_by: synthesizer\n"
    "---\n"
)

_RETRIEVER_FM = (
    "---\n"
    "phase: 01-situation\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: situation@1.0.0\n"
    "produced_by: portfolio-retriever\n"
    "---\n"
)


def test_producer_binding_pass_synthesizer(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[inferred] [source:from: GAP-001 + SIT-002] [conf:M]\n",
        frontmatter=_SYNTH_FM,
    )
    assert label_producer_binding.check(f) == []


def test_producer_binding_pass_assumed_synthesizer(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[assumed] [source:interview:2026-01-01/consultant] [conf:L]\n",
        frontmatter=_SYNTH_FM,
    )
    assert label_producer_binding.check(f) == []


def test_producer_binding_fail_known_in_synthesizer(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[known] [source:portfolio://Security/soc.md@abc1234] [conf:H]\n",
        frontmatter=_SYNTH_FM,
    )
    violations = label_producer_binding.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "label_producer_binding"
    assert "[known]" in violations[0].message


def test_producer_binding_fail_elicited_in_synthesizer(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[elicited] [source:interview:2026-01-01/consultant] [conf:M]\n",
        frontmatter=_SYNTH_FM,
    )
    violations = label_producer_binding.check(f)
    assert len(violations) == 1


def test_producer_binding_pass_known_in_retriever(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[known] [source:portfolio://Security/soc.md@abc1234] [conf:H]\n",
        frontmatter=_RETRIEVER_FM,
    )
    assert label_producer_binding.check(f) == []


def test_producer_binding_fail_inferred_in_retriever(tmp_path: Path) -> None:
    f = _artifact(
        tmp_path,
        "[inferred] [source:portfolio://Security/soc.md@abc1234] [conf:M]\n",
        frontmatter=_RETRIEVER_FM,
    )
    violations = label_producer_binding.check(f)
    assert len(violations) == 1


def test_producer_binding_skips_unknown_producer(tmp_path: Path) -> None:
    fm = (
        "---\n"
        "phase: 01\n"
        "status: draft\n"
        "harness_version: 0.1.0\n"
        "template: t@1\n"
        "produced_by: unknown-agent\n"
        "---\n"
    )
    f = _artifact(tmp_path, "[known] [source:uri@t] [conf:H]\n", frontmatter=fm)
    # Unknown producer → rule skips without violation
    assert label_producer_binding.check(f) == []


def test_producer_binding_skips_no_produced_by(tmp_path: Path) -> None:
    f = _artifact(tmp_path, "[known] [source:uri@t] [conf:H]\n")
    assert label_producer_binding.check(f) == []


# ---------------------------------------------------------------------------
# confidence_propagation
# ---------------------------------------------------------------------------

_GAP_FM = (
    "---\n"
    "phase: 02-gap\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: gaps@1.0.0\n"
    "produced_by: synthesizer\n"
    "---\n"
)

_YAML_BLOCK_PASS = (
    "```yaml\n"
    "---\n"
    "id: GAP-001\n"
    "title: Test gap\n"
    "current_state: >\n"
    "  Current state facts.\n"
    "  [known] [source:customer-portal://assets/x@2026-01-01T00:00:00Z] [conf:H]\n"
    "desired_state: >\n"
    "  Desired state.\n"
    "  [elicited] [source:interview:2026-01-01/consultant] [conf:M]\n"
    "gap_description: >\n"
    "  Gap. [inferred] [source:from: GAP-001.current_state + GAP-001.desired_state] [conf:M]\n"
    "compliance_drivers: []\n"
    "severity: high\n"
    "evidence: []\n"
    "---\n"
    "```\n"
)

_YAML_BLOCK_FAIL = (
    "```yaml\n"
    "---\n"
    "id: GAP-002\n"
    "title: Test violation\n"
    "current_state: >\n"
    "  [known] [source:customer-portal://assets/x@2026-01-01T00:00:00Z] [conf:M]\n"
    "desired_state: >\n"
    "  [elicited] [source:interview:2026-01-01/consultant] [conf:L]\n"
    "gap_description: >\n"
    "  Gap. [inferred] [source:from: GAP-002.current_state + GAP-002.desired_state] [conf:H]\n"
    "compliance_drivers: []\n"
    "severity: high\n"
    "evidence: []\n"
    "---\n"
    "```\n"
)


def test_conf_propagation_pass(tmp_path: Path) -> None:
    f = _artifact(tmp_path, _YAML_BLOCK_PASS, frontmatter=_GAP_FM)
    assert confidence_propagation.check(f) == []


def test_conf_propagation_fail(tmp_path: Path) -> None:
    f = _artifact(tmp_path, _YAML_BLOCK_FAIL, frontmatter=_GAP_FM)
    violations = confidence_propagation.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "confidence_propagation"
    assert "conf:H" in violations[0].message
    assert "conf:L" in violations[0].message


def test_conf_propagation_equal_is_ok(tmp_path: Path) -> None:
    # Composed conf == min(inputs) is valid (≤ not strict <)
    body = (
        "```yaml\n"
        "---\n"
        "id: REC-001\n"
        "current_state: >\n"
        "  [known] [source:uri@t] [conf:M]\n"
        "desired_state: >\n"
        "  [elicited] [source:interview:2026-01-01/consultant] [conf:M]\n"
        "gap_description: >\n"
        "  [inferred] [source:from: REC-001.current_state + REC-001.desired_state] [conf:M]\n"
        "---\n"
        "```\n"
    )
    f = _artifact(tmp_path, body, frontmatter=_GAP_FM)
    assert confidence_propagation.check(f) == []


def test_conf_propagation_no_from_no_violation(tmp_path: Path) -> None:
    # Plain claims without 'from:' are not composed claims
    body = "[known] [source:portfolio://Security/soc.md@abc] [conf:H]\n"
    f = _artifact(tmp_path, body, frontmatter=_GAP_FM)
    assert confidence_propagation.check(f) == []


def test_conf_propagation_skips_unresolvable_refs(tmp_path: Path) -> None:
    # If input refs aren't found in the document, rule skips (no false positive)
    body = (
        "```yaml\n"
        "---\n"
        "id: GAP-003\n"
        "gap_description: >\n"
        "  [inferred] [source:from: EXTERNAL-001 + EXTERNAL-002] [conf:H]\n"
        "---\n"
        "```\n"
    )
    f = _artifact(tmp_path, body, frontmatter=_GAP_FM)
    assert confidence_propagation.check(f) == []


# ---------------------------------------------------------------------------
# template_conformance
# ---------------------------------------------------------------------------

_ROADMAP_FM = (
    "---\n"
    "phase: 04-roadmap\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: roadmap@1.0.0\n"
    "produced_by: synthesizer\n"
    "---\n"
)

_GAPS_FM = (
    "---\n"
    "phase: 02-gap\n"
    "status: draft\n"
    "harness_version: 0.1.0\n"
    "template: gaps@1.0.0\n"
    "produced_by: synthesizer\n"
    "---\n"
)


def test_template_conformance_pass_roadmap(tmp_path: Path) -> None:
    body = "## Sequencing argument\n\nSome reasoning here.\n"
    f = _artifact(tmp_path, body, frontmatter=_ROADMAP_FM)
    assert template_conformance.check(f) == []


def test_template_conformance_fail_roadmap_missing_h2(tmp_path: Path) -> None:
    body = "## Introduction\n\nSome content.\n"
    f = _artifact(tmp_path, body, frontmatter=_ROADMAP_FM)
    violations = template_conformance.check(f)
    assert len(violations) == 1
    assert violations[0].rule == "template_conformance"
    assert "Sequencing argument" in violations[0].message


def test_template_conformance_pass_gaps(tmp_path: Path) -> None:
    body = "## 1. Goal Coverage Map\n\n| col |\n"
    f = _artifact(tmp_path, body, frontmatter=_GAPS_FM)
    assert template_conformance.check(f) == []


def test_template_conformance_fail_gaps_missing_h2(tmp_path: Path) -> None:
    body = "## 2. Gap Blocks\n\nSome content.\n"
    f = _artifact(tmp_path, body, frontmatter=_GAPS_FM)
    violations = template_conformance.check(f)
    assert len(violations) == 1
    assert "Goal Coverage Map" in violations[0].message


def test_template_conformance_skips_unknown_template(tmp_path: Path) -> None:
    # Template without required H2 rules → no violations
    fm = (
        "---\n"
        "phase: 01\n"
        "status: draft\n"
        "harness_version: 0.1.0\n"
        "template: unknown@1.0.0\n"
        "---\n"
    )
    f = _artifact(tmp_path, "# Content\n", frontmatter=fm)
    assert template_conformance.check(f) == []
