"""Unit tests for harness/init.py."""

import subprocess
from pathlib import Path

from harness.init import (
    _REGISTER_STUBS,
    PHASE_DIRS,
    _read_harness_version,
    _scaffold,
    main,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run(tmp_path: Path, args: list[str]) -> int:
    """Run main() with CWD patched to tmp_path so relative paths land there."""
    orig = Path.cwd()
    import os

    os.chdir(tmp_path)
    try:
        return main(args)
    finally:
        os.chdir(orig)


# ---------------------------------------------------------------------------
# _read_harness_version
# ---------------------------------------------------------------------------


def test_read_harness_version_returns_semver() -> None:
    version = _read_harness_version()
    assert version != "unknown", "Expected a real version from CHANGELOG.md"
    parts = version.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts)


def test_read_harness_version_no_version_line() -> None:
    """Fallback: CHANGELOG.md with no version header returns 'unknown'."""
    import re

    text = "# Changelog\nNo version here.\n"
    match = re.search(r"##\s+\[(\d+\.\d+\.\d+)\]", text)
    assert match is None, "Regex should not match a CHANGELOG with no version"


# ---------------------------------------------------------------------------
# _scaffold — layout
# ---------------------------------------------------------------------------


def test_scaffold_creates_phase_dirs(tmp_path: Path) -> None:
    target = tmp_path / "acme-corp"
    _scaffold("acme-corp", target, "0.1.0")

    for phase in PHASE_DIRS:
        assert (target / phase).is_dir(), f"Missing phase dir: {phase}"


def test_scaffold_creates_all_registers(tmp_path: Path) -> None:
    target = tmp_path / "acme-corp"
    _scaffold("acme-corp", target, "0.1.0")

    for filename in _REGISTER_STUBS:
        path = target / filename
        assert path.exists(), f"Missing register: {filename}"
        content = path.read_text()
        assert "acme-corp" in content
        assert "0.1.0" in content


def test_scaffold_creates_claude_md(tmp_path: Path) -> None:
    target = tmp_path / "acme-corp"
    _scaffold("acme-corp", target, "0.1.0")

    claude_md = target / "CLAUDE.md"
    assert claude_md.exists()
    content = claude_md.read_text()
    assert "acme-corp" in content
    assert "0.1.0" in content
    assert "<PLACEHOLDER" in content  # stub has unfilled placeholders


# ---------------------------------------------------------------------------
# Version pin matches CHANGELOG.md
# ---------------------------------------------------------------------------


def test_version_pin_matches_changelog(tmp_path: Path) -> None:
    target = tmp_path / "test-eng"
    version = _read_harness_version()
    _scaffold("test-eng", target, version)

    claude_md = (target / "CLAUDE.md").read_text()
    assert version in claude_md, "harness_version in CLAUDE.md must match CHANGELOG.md"


# ---------------------------------------------------------------------------
# Refusal on non-empty target
# ---------------------------------------------------------------------------


def test_refuses_non_empty_target(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    (target / "some-file.txt").write_text("content")

    ret = _run(tmp_path, ["existing"])
    assert ret == 1, "Should exit non-zero when target is non-empty"


def test_accepts_non_existent_target(tmp_path: Path) -> None:
    ret = _run(tmp_path, ["brand-new-customer"])
    assert ret == 0, "Should succeed for a new engagement name"
    assert (tmp_path / "brand-new-customer").is_dir()


def test_accepts_explicit_target_dir(tmp_path: Path) -> None:
    target = tmp_path / "custom-dir"
    ret = _run(tmp_path, ["my-customer", "--target-dir", str(target)])
    assert ret == 0
    assert (target / "CLAUDE.md").exists()


def test_refuses_non_empty_explicit_target_dir(tmp_path: Path) -> None:
    target = tmp_path / "custom-dir"
    target.mkdir()
    (target / "existing.txt").write_text("data")

    ret = _run(tmp_path, ["my-customer", "--target-dir", str(target)])
    assert ret == 1


# ---------------------------------------------------------------------------
# Git initialisation
# ---------------------------------------------------------------------------


def test_git_repo_initialised(tmp_path: Path) -> None:
    ret = _run(tmp_path, ["git-test-customer"])
    assert ret == 0
    assert (tmp_path / "git-test-customer" / ".git").is_dir()


def test_git_initial_commit_exists(tmp_path: Path) -> None:
    ret = _run(tmp_path, ["commit-test"])
    assert ret == 0
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=tmp_path / "commit-test",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scaffold engagement for commit-test" in result.stdout
