"""Unit tests for harness/enter_phase.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness.enter_phase import (
    _PHASE_DIRS,
    _append_trace,
    _detect_next_phase,
    _handle_version_mismatch,
    _is_ratified,
    _read_engagement_version,
    _read_harness_version,
    _render_handover_pdf,
    _resolve_phase,
    _upgrade_engagement_version,
    main,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_RATIFIED_FRONTMATTER = """\
---
phase: "{phase}"
status: ratified
harness_version: "0.1.0"
template: "scope@1.0.0"
---

# Content
"""

_DRAFT_FRONTMATTER = """\
---
phase: "{phase}"
status: draft
harness_version: "0.1.0"
template: "scope@1.0.0"
---

# Content
"""


def _make_engagement(tmp_path: Path) -> Path:
    repo = tmp_path / "engagement"
    repo.mkdir()
    for d in _PHASE_DIRS:
        (repo / d).mkdir()
    return repo


def _write_artifact(repo: Path, phase_dir: str, filename: str, *, ratified: bool) -> Path:
    frontmatter = _RATIFIED_FRONTMATTER if ratified else _DRAFT_FRONTMATTER
    artifact = repo / phase_dir / filename
    artifact.write_text(frontmatter.format(phase=phase_dir), encoding="utf-8")
    return artifact


def _write_claude_md(repo: Path, version: str) -> Path:
    claude = repo / "CLAUDE.md"
    claude.write_text(
        f'# Engagement\nharness_version: "{version}"\n', encoding="utf-8"
    )
    return claude


# ---------------------------------------------------------------------------
# _is_ratified
# ---------------------------------------------------------------------------


def test_is_ratified_missing_file(tmp_path: Path) -> None:
    assert not _is_ratified(tmp_path / "nonexistent.md")


def test_is_ratified_draft(tmp_path: Path) -> None:
    f = tmp_path / "artifact.md"
    f.write_text(_DRAFT_FRONTMATTER.format(phase="00-intake"), encoding="utf-8")
    assert not _is_ratified(f)


def test_is_ratified_ratified(tmp_path: Path) -> None:
    f = tmp_path / "artifact.md"
    f.write_text(_RATIFIED_FRONTMATTER.format(phase="00-intake"), encoding="utf-8")
    assert _is_ratified(f)


def test_is_ratified_no_frontmatter(tmp_path: Path) -> None:
    f = tmp_path / "artifact.md"
    f.write_text("# Just a heading\nstatus: ratified\n", encoding="utf-8")
    assert not _is_ratified(f)


# ---------------------------------------------------------------------------
# _detect_next_phase
# ---------------------------------------------------------------------------


def test_detect_next_phase_all_unratified(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _detect_next_phase(repo) == "00-intake"


def test_detect_next_phase_intake_done(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_artifact(repo, "00-intake", "scope.md", ratified=True)
    assert _detect_next_phase(repo) == "01-situation"


def test_detect_next_phase_first_three_done(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_artifact(repo, "00-intake", "scope.md", ratified=True)
    _write_artifact(repo, "01-situation", "situation.md", ratified=True)
    _write_artifact(repo, "02-gap", "gaps.md", ratified=True)
    assert _detect_next_phase(repo) == "03-mapping"


def test_detect_next_phase_all_done(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    artifact_map = {
        "00-intake": "scope.md",
        "01-situation": "situation.md",
        "02-gap": "gaps.md",
        "03-mapping": "recommendations.md",
        "04-roadmap": "roadmap.md",
        "05-handover": "handover.md",
        "06-retro": "retro.md",
    }
    for phase_dir, filename in artifact_map.items():
        _write_artifact(repo, phase_dir, filename, ratified=True)
    assert _detect_next_phase(repo) is None


def test_detect_next_phase_draft_not_ratified(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_artifact(repo, "00-intake", "scope.md", ratified=False)
    assert _detect_next_phase(repo) == "00-intake"


# ---------------------------------------------------------------------------
# _read_engagement_version
# ---------------------------------------------------------------------------


def test_read_engagement_version_present(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, "1.2.3")
    assert _read_engagement_version(repo) == "1.2.3"


def test_read_engagement_version_missing_file(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _read_engagement_version(repo) is None


def test_read_engagement_version_no_version_field(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    (repo / "CLAUDE.md").write_text("# Engagement\nNo version here.\n", encoding="utf-8")
    assert _read_engagement_version(repo) is None


# ---------------------------------------------------------------------------
# _read_harness_version
# ---------------------------------------------------------------------------


def test_read_harness_version_returns_semver() -> None:
    version = _read_harness_version()
    assert version != "unknown"
    parts = version.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts)


# ---------------------------------------------------------------------------
# _resolve_phase
# ---------------------------------------------------------------------------


def test_resolve_phase_none_auto_detects(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _resolve_phase(None, repo) == "00-intake"


def test_resolve_phase_numeric(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _resolve_phase("02", repo) == "02-gap"


def test_resolve_phase_full_name(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _resolve_phase("03-mapping", repo) == "03-mapping"


def test_resolve_phase_unknown(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    assert _resolve_phase("99", repo) is None


# ---------------------------------------------------------------------------
# _upgrade_engagement_version
# ---------------------------------------------------------------------------


def test_upgrade_engagement_version(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, "0.1.0")
    _upgrade_engagement_version(repo, "0.1.0", "0.2.0")
    assert _read_engagement_version(repo) == "0.2.0"


# ---------------------------------------------------------------------------
# _handle_version_mismatch — non-interactive mode
# ---------------------------------------------------------------------------


def test_handle_version_mismatch_non_interactive_returns_false(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    result = _handle_version_mismatch("0.1.0", "0.2.0", repo, non_interactive=True)
    assert result is False


def test_handle_version_mismatch_pin(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    with patch("builtins.input", return_value="p"):
        result = _handle_version_mismatch("0.1.0", "0.2.0", repo)
    assert result is True
    # Version should NOT change on pin
    assert _read_engagement_version(repo) is None  # no CLAUDE.md in bare repo


def test_handle_version_mismatch_upgrade(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, "0.1.0")
    with patch("builtins.input", return_value="u"):
        result = _handle_version_mismatch("0.1.0", "0.2.0", repo)
    assert result is True
    assert _read_engagement_version(repo) == "0.2.0"


def test_handle_version_mismatch_abort(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    with patch("builtins.input", return_value="a"):
        result = _handle_version_mismatch("0.1.0", "0.2.0", repo)
    assert result is False


# ---------------------------------------------------------------------------
# _append_trace
# ---------------------------------------------------------------------------


def test_append_trace_creates_file(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    prompt = tmp_path / "00-intake.md"
    prompt.write_text("# Prompt", encoding="utf-8")
    _append_trace(repo, "00-intake", prompt)
    trace = repo / "00-intake" / "_trace.jsonl"
    assert trace.exists()
    entry = json.loads(trace.read_text(encoding="utf-8"))
    assert entry["phase"] == "00-intake"
    assert "timestamp" in entry
    assert "prompt_hash" in entry
    assert "harness_version" in entry


def test_append_trace_is_append_only(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    prompt = tmp_path / "00-intake.md"
    prompt.write_text("# Prompt", encoding="utf-8")
    _append_trace(repo, "00-intake", prompt)
    _append_trace(repo, "00-intake", prompt)
    trace = repo / "00-intake" / "_trace.jsonl"
    lines = [ln for ln in trace.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 2
    for line in lines:
        json.loads(line)  # each line must be valid JSON


def test_append_trace_missing_prompt(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    missing = tmp_path / "nonexistent.md"
    _append_trace(repo, "00-intake", missing)
    trace = repo / "00-intake" / "_trace.jsonl"
    entry = json.loads(trace.read_text(encoding="utf-8"))
    assert entry["prompt_hash"] is None


# ---------------------------------------------------------------------------
# main() — integration (dry-run, no claude invocation)
# ---------------------------------------------------------------------------


def _make_harness_prompt(phase_dir: str) -> None:
    """Write a stub orchestrator prompt so main() can find it."""
    from harness.enter_phase import _ORCHESTRATOR_DIR

    _ORCHESTRATOR_DIR.mkdir(parents=True, exist_ok=True)
    stub = _ORCHESTRATOR_DIR / f"{phase_dir}.md"
    if not stub.exists():
        stub.write_text(f"# Orchestrator: {phase_dir}\n", encoding="utf-8")


def test_main_dry_run_detects_intake(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, _read_harness_version())
    _make_harness_prompt("00-intake")
    rc = main(["--dry-run", str(repo)])
    assert rc == 0


def test_main_dry_run_specific_phase(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, _read_harness_version())
    _make_harness_prompt("01-situation")
    rc = main(["--dry-run", "--phase", "01", str(repo)])
    assert rc == 0


def test_main_all_done_exits_zero(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    artifact_map = {
        "00-intake": "scope.md",
        "01-situation": "situation.md",
        "02-gap": "gaps.md",
        "03-mapping": "recommendations.md",
        "04-roadmap": "roadmap.md",
        "05-handover": "handover.md",
        "06-retro": "retro.md",
    }
    for phase_dir, filename in artifact_map.items():
        _write_artifact(repo, phase_dir, filename, ratified=True)
    _write_claude_md(repo, _read_harness_version())
    rc = main(["--dry-run", str(repo)])
    assert rc == 0


def test_main_version_mismatch_dry_run_aborts(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, "0.0.0")  # deliberately wrong
    _make_harness_prompt("00-intake")
    rc = main(["--dry-run", str(repo)])
    assert rc == 1


def test_main_missing_repo_exits_nonzero(tmp_path: Path) -> None:
    rc = main(["--dry-run", str(tmp_path / "no-such-dir")])
    assert rc == 1


def test_main_unknown_phase_exits_nonzero(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, _read_harness_version())
    rc = main(["--dry-run", "--phase", "99", str(repo)])
    assert rc == 1


def test_main_rerun_no_completed_phase_exits_nonzero(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, _read_harness_version())
    rc = main(["--dry-run", "--rerun", str(repo)])
    assert rc == 1


# ---------------------------------------------------------------------------
# _render_handover_pdf
# ---------------------------------------------------------------------------


def _stub_subprocess_version_ok(cmd: list[str], **_: object) -> MagicMock:
    """Return a successful CompletedProcess for --version checks; fail otherwise."""
    if "--version" in cmd:
        m = MagicMock()
        m.returncode = 0
        return m
    m = MagicMock()
    m.returncode = 0
    m.stderr = ""
    return m


def _make_handover_engagement(tmp_path: Path) -> Path:
    """Create a minimal engagement repo with a 05-handover/handover.md."""
    repo = _make_engagement(tmp_path)
    _write_claude_md(repo, _read_harness_version())
    (repo / "05-handover").mkdir(exist_ok=True)
    handover = repo / "05-handover" / "handover.md"
    handover.write_text(
        '---\nphase: "05-handover"\nstatus: ratified\nharness_version: "0.1.0"\n'
        'template: "handover@1.0.0"\n---\n\n# Handover\n',
        encoding="utf-8",
    )
    return repo


def test_render_handover_pdf_raises_if_pandoc_missing(tmp_path: Path) -> None:
    repo = _make_handover_engagement(tmp_path)

    def _no_pandoc(cmd: list[str], **_: object) -> MagicMock:
        m = MagicMock()
        m.returncode = 1 if cmd[0] == "pandoc" else 0
        return m

    with patch("harness.enter_phase.subprocess.run", side_effect=_no_pandoc):
        with pytest.raises(RuntimeError, match="pandoc"):
            _render_handover_pdf(repo)


def test_render_handover_pdf_raises_if_weasyprint_missing(tmp_path: Path) -> None:
    repo = _make_handover_engagement(tmp_path)

    def _no_weasy(cmd: list[str], **_: object) -> MagicMock:
        m = MagicMock()
        m.returncode = 1 if cmd[0] == "weasyprint" else 0
        return m

    with patch("harness.enter_phase.subprocess.run", side_effect=_no_weasy):
        with pytest.raises(RuntimeError, match="weasyprint"):
            _render_handover_pdf(repo)


def test_render_handover_pdf_raises_on_pandoc_failure(tmp_path: Path) -> None:
    repo = _make_handover_engagement(tmp_path)

    call_count: list[int] = [0]

    def _pandoc_fails(cmd: list[str], **_: object) -> MagicMock:
        m = MagicMock()
        m.stderr = "pandoc error"
        # First two calls are --version checks (pandoc, weasyprint); third is actual pandoc run.
        call_count[0] += 1
        m.returncode = 1 if call_count[0] == 3 else 0
        return m

    with patch("harness.enter_phase.subprocess.run", side_effect=_pandoc_fails):
        with patch("harness.enter_phase.generate_charts", return_value={}):
            with pytest.raises(RuntimeError, match="pandoc failed"):
                _render_handover_pdf(repo)


def test_render_handover_pdf_raises_on_weasyprint_failure(tmp_path: Path) -> None:
    repo = _make_handover_engagement(tmp_path)

    call_count: list[int] = [0]

    def _weasy_fails(cmd: list[str], **_: object) -> MagicMock:
        m = MagicMock()
        m.stderr = "weasyprint error"
        call_count[0] += 1
        # Calls: pandoc --version, weasyprint --version, pandoc run, weasyprint run
        m.returncode = 1 if call_count[0] == 4 else 0
        return m

    with patch("harness.enter_phase.subprocess.run", side_effect=_weasy_fails):
        with patch("harness.enter_phase.generate_charts", return_value={}):
            # Need a stub HTML output for weasyprint to consume
            (repo / "05-handover" / "handover.html").write_text("<html/>", encoding="utf-8")
            with pytest.raises(RuntimeError, match="weasyprint failed"):
                _render_handover_pdf(repo)


def test_render_handover_pdf_success_returns_pdf_path(tmp_path: Path) -> None:
    repo = _make_handover_engagement(tmp_path)
    pdf_stub = repo / "05-handover" / "handover.pdf"

    def _all_ok(cmd: list[str], **_: object) -> MagicMock:
        m = MagicMock()
        m.returncode = 0
        m.stderr = ""
        # Simulate weasyprint writing the PDF
        if cmd[0] == "weasyprint":
            pdf_stub.write_bytes(b"%PDF-1.4 stub" + b"\x00" * 1024)
        return m

    with patch("harness.enter_phase.subprocess.run", side_effect=_all_ok):
        with patch("harness.enter_phase.generate_charts", return_value={}):
            result = _render_handover_pdf(repo)

    assert result == pdf_stub.resolve()


def test_render_handover_pdf_with_meridian_logistics() -> None:
    """Integration test: render PDF for the real Meridian-Logistics fixture."""
    import shutil

    if not shutil.which("pandoc") or not shutil.which("weasyprint"):
        pytest.skip("pandoc or weasyprint not installed")

    engagement = Path("Meridian-Logistics")
    if not engagement.is_dir():
        pytest.skip("Meridian-Logistics fixture not present")

    pdf_path = _render_handover_pdf(engagement)
    assert pdf_path.exists(), "PDF file was not created"
    assert pdf_path.stat().st_size > 1024, "PDF is smaller than 1 KB"


def test_main_rerun_reruns_last_done(tmp_path: Path) -> None:
    repo = _make_engagement(tmp_path)
    _write_artifact(repo, "00-intake", "scope.md", ratified=True)
    _write_claude_md(repo, _read_harness_version())
    _make_harness_prompt("00-intake")
    rc = main(["--dry-run", "--rerun", str(repo)])
    assert rc == 0
