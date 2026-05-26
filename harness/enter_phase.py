#!/usr/bin/env python3
"""CLI entry point for running a phase orchestrator against an engagement repo.

Usage:
    python -m harness.enter_phase [--phase NN] [--rerun] [engagement-repo]

Default behaviour:
  - Determines the next phase from which 0N-*/ directories have ratified
    artifacts (frontmatter status: ratified).
  - Verifies engagement CLAUDE.md harness_version matches harness CHANGELOG.md.
  - On version mismatch: surfaces choice (pin / upgrade / abort).
  - Invokes `claude` with the appropriate orchestrator prompt and correct CWD.
  - Appends invocation metadata to 0N-<name>/_trace.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from harness.charts import generate_charts

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PHASE_DIRS = [
    "00-intake",
    "01-situation",
    "02-gap",
    "03-mapping",
    "04-roadmap",
    "05-handover",
    "06-retro",
]

# Artifact that must have status: ratified for a phase to count as done
_PHASE_ARTIFACT: dict[str, str] = {
    "00-intake": "scope.md",
    "01-situation": "situation.md",
    "02-gap": "gaps.md",
    "03-mapping": "recommendations.md",
    "04-roadmap": "roadmap.md",
    "05-handover": "handover.md",
    "06-retro": "retro.md",
}

_HARNESS_DIR = Path(__file__).parent.parent
_ORCHESTRATOR_DIR = _HARNESS_DIR / "prompts" / "orchestrator"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_harness_version() -> str:
    changelog = _HARNESS_DIR / "CHANGELOG.md"
    if not changelog.exists():
        return "unknown"
    text = changelog.read_text(encoding="utf-8")
    match = re.search(r"##\s+\[(\d+\.\d+\.\d+)\]", text)
    return match.group(1) if match else "unknown"


def _is_ratified(artifact_path: Path) -> bool:
    """Return True iff the artifact exists and has 'status: ratified' frontmatter."""
    if not artifact_path.exists():
        return False
    text = artifact_path.read_text(encoding="utf-8")
    # Extract YAML frontmatter between --- delimiters
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return False
    fm = fm_match.group(1)
    return bool(re.search(r"^status\s*:\s*ratified\s*$", fm, re.MULTILINE))


def _detect_next_phase(engagement_repo: Path) -> str | None:
    """Return the next phase directory name that has not yet been ratified.

    Phases are evaluated in order; the first unratified phase is the next one.
    Returns None if all phases are complete.
    """
    for phase_dir in _PHASE_DIRS:
        artifact_name = _PHASE_ARTIFACT[phase_dir]
        artifact_path = engagement_repo / phase_dir / artifact_name
        if not _is_ratified(artifact_path):
            return phase_dir
    return None


def _read_engagement_version(engagement_repo: Path) -> str | None:
    """Extract harness_version from engagement CLAUDE.md (looks for 'harness_version: "X.Y.Z"')."""
    claude_md = engagement_repo / "CLAUDE.md"
    if not claude_md.exists():
        return None
    text = claude_md.read_text(encoding="utf-8")
    match = re.search(r'harness_version\s*:\s*["\']?(\d+\.\d+\.\d+)["\']?', text)
    return match.group(1) if match else None


def _prompt_path(phase_dir: str) -> Path:
    """Return the orchestrator prompt path for a phase directory."""
    # e.g. "00-intake" -> "prompts/orchestrator/00-intake.md"
    return _ORCHESTRATOR_DIR / f"{phase_dir}.md"


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    return h


def _append_trace(engagement_repo: Path, phase_dir: str, prompt_path: Path) -> None:
    """Append invocation metadata to 0N-<name>/_trace.jsonl."""
    trace_file = engagement_repo / phase_dir / "_trace.jsonl"
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "phase": phase_dir,
        "prompt_file": str(prompt_path),
        "prompt_hash": _file_sha256(prompt_path) if prompt_path.exists() else None,
        "harness_version": _read_harness_version(),
    }
    with trace_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def _handle_version_mismatch(
    engagement_version: str,
    harness_version: str,
    engagement_repo: Path,
    *,
    non_interactive: bool = False,
) -> bool:
    """Prompt the consultant to choose how to handle a version mismatch.

    Returns True to proceed, False to abort.
    """
    print(
        f"WARNING: Version mismatch detected.\n"
        f"  Engagement CLAUDE.md: harness_version = {engagement_version}\n"
        f"  Current harness:      version          = {harness_version}",
        file=sys.stderr,
    )

    if non_interactive:
        print(
            "error: version mismatch in non-interactive mode. "
            "Use --pin or --upgrade to resolve.",
            file=sys.stderr,
        )
        return False

    print(
        "\nChoose:\n"
        "  [p] Pin — continue with the engagement's original version (no change)\n"
        "  [u] Upgrade — update engagement CLAUDE.md to the current harness version\n"
        "  [a] Abort — stop and do nothing",
        file=sys.stderr,
    )
    while True:
        choice = input("Your choice [p/u/a]: ").strip().lower()
        if choice in ("p", "pin"):
            print("Continuing with engagement version pinned at", engagement_version)
            return True
        elif choice in ("u", "upgrade"):
            _upgrade_engagement_version(engagement_repo, engagement_version, harness_version)
            print(f"Upgraded engagement CLAUDE.md to harness_version: {harness_version}")
            return True
        elif choice in ("a", "abort"):
            print("Aborted.")
            return False
        else:
            print("Please enter p, u, or a.", file=sys.stderr)


def _upgrade_engagement_version(
    engagement_repo: Path, old_version: str, new_version: str
) -> None:
    """Update harness_version in the engagement CLAUDE.md."""
    claude_md = engagement_repo / "CLAUDE.md"
    text = claude_md.read_text(encoding="utf-8")
    updated = re.sub(
        r'(harness_version\s*:\s*["\']?)' + re.escape(old_version) + r'(["\']?)',
        r"\g<1>" + new_version + r"\g<2>",
        text,
    )
    claude_md.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# Phase detection from --phase flag
# ---------------------------------------------------------------------------


def _resolve_phase(phase_arg: str | None, engagement_repo: Path) -> str | None:
    """Return the resolved phase directory name from --phase argument or auto-detect."""
    if phase_arg is None:
        return _detect_next_phase(engagement_repo)

    # Allow either "00" or "00-intake"
    normalized = phase_arg.zfill(2)
    for p in _PHASE_DIRS:
        if p.startswith(normalized):
            return p
    # Try exact match
    if phase_arg in _PHASE_DIRS:
        return phase_arg

    return None


# ---------------------------------------------------------------------------
# Phase 05 PDF render post-step
# ---------------------------------------------------------------------------

_HANDOVER_PHASE = "05-handover"
_ASSETS_DIR = _HARNESS_DIR / "assets"


def _render_handover_pdf(engagement_repo: Path) -> Path:
    """Generate charts then render handover.pdf via pandoc + weasyprint.

    Raises RuntimeError if pandoc or weasyprint is not installed.
    Returns the absolute path to the produced PDF.
    """
    # Check external tools are available.
    for tool, install_hint in (
        ("pandoc", "Install pandoc: https://pandoc.org/installing.html"),
        (
            "weasyprint",
            "Install weasyprint: pip install weasyprint  "
            "(system deps: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)",
        ),
    ):
        result = subprocess.run(
            [tool, "--version"],
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"'{tool}' is not installed or not on PATH.\n{install_hint}"
            )

    handover_dir = engagement_repo / _HANDOVER_PHASE
    handover_md = handover_dir / "handover.md"
    handover_html = handover_dir / "handover.html"
    handover_pdf = handover_dir / "handover.pdf"
    template = _ASSETS_DIR / "handover-template.html"

    # Step 1 — generate charts.
    logger.info("Generating charts for %s …", engagement_repo)
    chart_paths = generate_charts(engagement_repo)

    # Step 2 — run pandoc to produce intermediate HTML.
    pandoc_cmd = [
        "pandoc",
        str(handover_md),
        "--template",
        str(template),
        "--standalone",
        "--output",
        str(handover_html),
    ]
    # Pass chart paths as pandoc metadata variables so the template can embed them.
    for key, path in chart_paths.items():
        pandoc_cmd += ["--metadata", f"{key}={path}"]

    logger.info("Running pandoc …")
    pandoc_result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
    if pandoc_result.returncode != 0:
        raise RuntimeError(
            f"pandoc failed (exit {pandoc_result.returncode}):\n{pandoc_result.stderr}"
        )

    # Step 3 — run weasyprint to produce PDF.
    logger.info("Running weasyprint …")
    weasy_result = subprocess.run(
        ["weasyprint", str(handover_html), str(handover_pdf)],
        capture_output=True,
        text=True,
    )
    if weasy_result.returncode != 0:
        raise RuntimeError(
            f"weasyprint failed (exit {weasy_result.returncode}):\n{weasy_result.stderr}"
        )

    # Step 4 — log the produced PDF path.
    logger.info("Handover PDF produced: %s", handover_pdf.resolve())
    print(f"Handover PDF: {handover_pdf.resolve()}")
    return handover_pdf.resolve()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enter a consulting phase orchestrator for an engagement repo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "engagement_repo",
        nargs="?",
        default=".",
        help="Path to the engagement repo (default: current directory)",
    )
    parser.add_argument(
        "--phase",
        default=None,
        help="Phase number or name to run (e.g. '00', '01-situation'); "
        "default: auto-detect next unratified phase",
    )
    parser.add_argument(
        "--rerun",
        action="store_true",
        help="Re-run the last completed phase even if its artifact is ratified",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without invoking claude or writing trace",
    )
    args = parser.parse_args(argv)

    engagement_repo = Path(args.engagement_repo).resolve()

    if not engagement_repo.is_dir():
        print(
            f"error: engagement repo not found: {engagement_repo}",
            file=sys.stderr,
        )
        return 1

    # -----------------------------------------------------------------
    # Engagement-repo validation (fail loud, §1)
    # An engagement repo must have a CLAUDE.md with harness_version.
    # If it doesn't, refuse to run — running outside an engagement repo would
    # scaffold trace files into the wrong directory and corrupt the agent's
    # working assumptions.
    # -----------------------------------------------------------------
    claude_md = engagement_repo / "CLAUDE.md"
    if not claude_md.exists():
        print(
            f"error: {engagement_repo} is not an engagement repo "
            f"(missing CLAUDE.md).\n"
            f"  Run from inside an engagement repo created with `harness init`, "
            f"or pass the engagement repo path explicitly.",
            file=sys.stderr,
        )
        return 1
    if _read_engagement_version(engagement_repo) is None:
        print(
            f"error: {engagement_repo}/CLAUDE.md has no `harness_version` field.\n"
            f"  This does not look like an engagement repo. "
            f"Create one with `harness init` or add `harness_version: X.Y.Z` "
            f"to the engagement CLAUDE.md.",
            file=sys.stderr,
        )
        return 1

    # -----------------------------------------------------------------
    # Phase detection
    # -----------------------------------------------------------------
    if args.rerun:
        # Rerun: pick the most recent completed phase
        last_done: str | None = None
        for phase_dir in _PHASE_DIRS:
            artifact = engagement_repo / phase_dir / _PHASE_ARTIFACT[phase_dir]
            if _is_ratified(artifact):
                last_done = phase_dir
        if last_done is None:
            print(
                "error: --rerun specified but no completed phase found.",
                file=sys.stderr,
            )
            return 1
        phase_dir = last_done
    else:
        resolved = _resolve_phase(args.phase, engagement_repo)
        if resolved is None and args.phase is not None:
            print(
                f"error: unknown phase '{args.phase}'. "
                f"Valid values: {', '.join(_PHASE_DIRS)}",
                file=sys.stderr,
            )
            return 1
        if resolved is None:
            print("All phases are complete. Nothing to do.", file=sys.stderr)
            return 0
        phase_dir = resolved

    # -----------------------------------------------------------------
    # Locate orchestrator prompt
    # -----------------------------------------------------------------
    prompt_path = _prompt_path(phase_dir)
    if not prompt_path.exists():
        print(
            f"error: orchestrator prompt not found: {prompt_path}",
            file=sys.stderr,
        )
        return 1

    # -----------------------------------------------------------------
    # Version check
    # -----------------------------------------------------------------
    harness_version = _read_harness_version()
    engagement_version = _read_engagement_version(engagement_repo)
    # engagement_version is guaranteed non-None by the upfront validation above.

    if engagement_version != harness_version:
        assert engagement_version is not None  # guaranteed non-None by upfront validation
        proceed = _handle_version_mismatch(
            engagement_version,
            harness_version,
            engagement_repo,
            non_interactive=args.dry_run,
        )
        if not proceed:
            return 1

    # -----------------------------------------------------------------
    # Dry-run reporting
    # -----------------------------------------------------------------
    if args.dry_run:
        print(f"Phase:         {phase_dir}")
        print(f"Prompt:        {prompt_path}")
        print(f"Engagement:    {engagement_repo}")
        print(f"Trace will be appended to: {engagement_repo / phase_dir / '_trace.jsonl'}")
        return 0

    # -----------------------------------------------------------------
    # Append trace before invocation
    # -----------------------------------------------------------------
    _append_trace(engagement_repo, phase_dir, prompt_path)

    # -----------------------------------------------------------------
    # Invoke claude
    # -----------------------------------------------------------------
    prompt_text = prompt_path.read_text(encoding="utf-8")
    # Pass the orchestrator prompt as the initial user turn, then drop into
    # interactive mode so HITL gates can collect consultant input.
    # Do NOT use --print: that returns a single response and exits, which
    # breaks every HITL gate in every orchestrator.
    cmd = ["claude", prompt_text]

    print(f"Entering phase {phase_dir} …")
    print(f"  Prompt: {prompt_path}")
    print(f"  CWD:    {engagement_repo}")

    try:
        result = subprocess.run(cmd, cwd=engagement_repo)
        rc = result.returncode

        # Post-ratification hook: render handover PDF after phase 05.
        if rc == 0 and phase_dir == _HANDOVER_PHASE:
            try:
                _render_handover_pdf(engagement_repo)
            except RuntimeError as exc:
                print(f"warning: PDF render failed — {exc}", file=sys.stderr)

        return rc
    except FileNotFoundError:
        print(
            "error: 'claude' CLI not found. "
            "Ensure Claude Code is installed and on your PATH.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
