"""Rule: every 'from: A + B' must reference claim ids in scope."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines, parse_yaml_blocks

RULE: str = "claim_composition_resolvable"

_FROM_RE = re.compile(r"\[source:from:\s*([^\]]+)\]")
_CLAIM_ID_RE = re.compile(r"\b([A-Z]{2,8}-\d+)\b")

# Phase directories in engagement order
_PHASE_ORDER = [
    "00-intake",
    "01-situation",
    "02-gap",
    "03-mapping",
    "04-roadmap",
    "05-handover",
    "06-retro",
]


def _collect_ids_from_text(text: str) -> set[str]:
    """Collect all claim block ids declared in ```yaml blocks in text."""
    ids: set[str] = set()
    blocks = parse_yaml_blocks(text)
    for block in blocks:
        raw_id = block.get("id")
        if isinstance(raw_id, str):
            ids.add(raw_id.strip())
    return ids


def _in_scope_ids(artifact: Path) -> set[str]:
    """
    Return the set of claim ids in scope for this artifact.

    Scope = ids in the current artifact + ids in all ratified artifacts
    from prior phases found in an engagement repo layout.

    Falls back to just the current artifact's ids when the artifact is
    not inside a recognisable engagement repo directory structure.
    """
    text = artifact.read_text(encoding="utf-8")
    ids = _collect_ids_from_text(text)

    # Try to locate a parent phase directory
    artifact_phase_dir: Path | None = None
    artifact_phase_name: str | None = None
    for part in reversed(artifact.parts):
        if part in _PHASE_ORDER:
            artifact_phase_name = part
            # Rebuild path up to that directory
            idx = artifact.parts.index(part)
            artifact_phase_dir = Path(*artifact.parts[: idx + 1])
            break

    if artifact_phase_dir is None or artifact_phase_name is None:
        return ids

    engagement_root = artifact_phase_dir.parent
    artifact_phase_index = _PHASE_ORDER.index(artifact_phase_name)

    for prior_phase in _PHASE_ORDER[:artifact_phase_index]:
        phase_dir = engagement_root / prior_phase
        if not phase_dir.is_dir():
            continue
        for md_file in phase_dir.glob("*.md"):
            try:
                prior_text = md_file.read_text(encoding="utf-8")
            except OSError:
                continue
            # Only include ratified artifacts
            status_match = re.search(r"^status:\s*(\S+)", prior_text, re.MULTILINE)
            if status_match and status_match.group(1) == "ratified":
                ids.update(_collect_ids_from_text(prior_text))
            elif not status_match:
                # No status field — include anyway (permissive for bare test fixtures)
                ids.update(_collect_ids_from_text(prior_text))

    return ids


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    in_scope = _in_scope_ids(path)
    violations: list[Violation] = []

    for lineno, line in body_lines(text):
        m = _FROM_RE.search(line)
        if not m:
            continue

        raw_refs = m.group(1)
        parts = [r.strip() for r in raw_refs.split("+")]

        for ref in parts:
            ref = ref.strip()
            # Only validate refs that look like structured claim ids (e.g. GAP-001)
            if not _CLAIM_ID_RE.fullmatch(ref):
                continue
            if ref not in in_scope:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno,
                        message=f"composed claim references unknown id '{ref}' (not in scope)",
                    )
                )

    return violations
