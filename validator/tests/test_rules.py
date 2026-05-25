"""Tests for validator rules."""

from pathlib import Path

from validator.rules import (
    claim_confidence_present,
    claim_label_present,
    claim_source_present,
    frontmatter_required_fields,
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
