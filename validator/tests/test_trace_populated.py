"""Tests for validator/rules/trace_populated.py."""

from __future__ import annotations

from pathlib import Path

from validator.rules import trace_populated

_FULL_FM = (
    "---\n"
    "phase: 00-intake\n"
    "status: ratified\n"
    "harness_version: 0.1.0\n"
    "template: scope@1.0.0\n"
    "---\n"
)


def _artifact(phase_dir: Path, body: str = "# Heading\n") -> Path:
    path = phase_dir / "scope.md"
    path.write_text(_FULL_FM + body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Passing cases (no warning)
# ---------------------------------------------------------------------------


def test_trace_populated_pass(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    (phase_dir / "_trace.jsonl").write_text(
        '{"timestamp":"2026-05-25T10:00:00+00:00","subagent":"synthesizer","model":"claude-sonnet-4-6","prompt_hash":"p","input_hash":"i","output_hash":"o","duration_ms":100}\n',
        encoding="utf-8",
    )
    art = _artifact(phase_dir)
    assert trace_populated.check(art) == []


def test_trace_populated_pass_multiple_lines(tmp_path: Path) -> None:
    phase_dir = tmp_path / "01-situation"
    phase_dir.mkdir()
    lines = (
        '{"timestamp":"t","subagent":"interviewer","model":"m","prompt_hash":"p","input_hash":"i","output_hash":"o","duration_ms":1}\n'
        '{"timestamp":"t","subagent":"synthesizer","model":"m","prompt_hash":"p","input_hash":"i","output_hash":"o","duration_ms":2}\n'
    )
    (phase_dir / "_trace.jsonl").write_text(lines, encoding="utf-8")
    art = _artifact(phase_dir)
    assert trace_populated.check(art) == []


# ---------------------------------------------------------------------------
# Warning cases
# ---------------------------------------------------------------------------


def test_trace_missing_emits_warning(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    art = _artifact(phase_dir)
    warnings = trace_populated.check(art)
    assert len(warnings) == 1
    assert warnings[0].rule == "trace_populated"
    assert "not found" in warnings[0].message


def test_trace_empty_emits_warning(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    (phase_dir / "_trace.jsonl").write_text("", encoding="utf-8")
    art = _artifact(phase_dir)
    warnings = trace_populated.check(art)
    assert len(warnings) == 1
    assert warnings[0].rule == "trace_populated"
    assert "empty" in warnings[0].message


def test_trace_whitespace_only_emits_warning(tmp_path: Path) -> None:
    phase_dir = tmp_path / "02-gap"
    phase_dir.mkdir()
    (phase_dir / "_trace.jsonl").write_text("   \n  \n", encoding="utf-8")
    art = _artifact(phase_dir)
    warnings = trace_populated.check(art)
    assert len(warnings) == 1


# ---------------------------------------------------------------------------
# Warning is non-blocking (returns Warning, not Violation)
# ---------------------------------------------------------------------------


def test_trace_warning_is_warning_type(tmp_path: Path) -> None:
    from validator import Warning

    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    art = _artifact(phase_dir)
    warnings = trace_populated.check(art)
    assert len(warnings) == 1
    assert isinstance(warnings[0], Warning)
