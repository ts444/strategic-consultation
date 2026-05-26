"""Rule: every GAP block must declare compliance_drivers; CMP-NNN refs must resolve."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import parse_yaml_blocks

RULE: str = "gap_compliance_drivers_field"

_GAP_ID_RE = re.compile(r"^GAP-\d+$")
_CMP_ID_RE = re.compile(r"^CMP-\d+$")
_CMP_DECL_RE = re.compile(r"\bid:\s*(CMP-\d+)")


def _known_cmp_ids(artifact: Path) -> set[str] | None:
    """Return declared CMP-NNN ids from _compliance.md, or None if not found."""
    for parent in (artifact.parent, artifact.parent.parent):
        reg = parent / "_compliance.md"
        if reg.exists():
            return set(_CMP_DECL_RE.findall(reg.read_text(encoding="utf-8")))
    return None


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    known_cmp = _known_cmp_ids(path)
    violations: list[Violation] = []

    for block in blocks:
        raw_id = block.get("id")
        if not isinstance(raw_id, str) or not _GAP_ID_RE.match(raw_id.strip()):
            continue

        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)
        lineno = lineno_raw
        present_keys = block["_present_keys"]
        assert isinstance(present_keys, set)

        if "compliance_drivers" not in present_keys:
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno,
                    message=f"{raw_id}: missing compliance_drivers field",
                )
            )
            continue

        # Check CMP-id references when the register is available
        if known_cmp is None:
            continue

        drivers = block.get("compliance_drivers")
        if not isinstance(drivers, list):
            continue

        for ref in drivers:
            ref = ref.strip()
            if _CMP_ID_RE.match(ref) and ref not in known_cmp:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno,
                        message=f"{raw_id}: compliance_drivers references unknown id: {ref}",
                    )
                )

    return violations
