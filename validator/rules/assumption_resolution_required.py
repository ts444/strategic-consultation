"""Rule: assumptions requiring revalidation at a target phase must have resolution_status."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import parse_yaml_blocks

RULE: str = "assumption_resolution_required"

_ASM_ID_RE = re.compile(r"^ASM-\d+$")
_VALID_STATUSES: frozenset[str] = frozenset({"pending", "resolved", "deferred"})


def _is_empty(val: object) -> bool:
    if val is None:
        return True
    if isinstance(val, list):
        return len(val) == 0
    return not str(val).strip()


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    violations: list[Violation] = []

    for block in blocks:
        raw_id = block.get("id")
        if not isinstance(raw_id, str) or not _ASM_ID_RE.match(raw_id.strip()):
            continue

        requires_revalidation = block.get("requires_revalidation")
        target_phase = block.get("target_phase")

        if _is_empty(requires_revalidation):
            continue
        if str(requires_revalidation).strip().lower() not in ("true", "yes"):
            continue
        if _is_empty(target_phase):
            continue

        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)

        resolution_status = block.get("resolution_status")
        if _is_empty(resolution_status):
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno_raw,
                    message=(
                        f"{raw_id}: requires_revalidation:true with target_phase:{target_phase}"
                        " but missing resolution_status (must be: pending | resolved | deferred)"
                    ),
                )
            )
            continue

        status_val = str(resolution_status).strip()
        if status_val not in _VALID_STATUSES:
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno_raw,
                    message=(
                        f"{raw_id}: resolution_status has invalid value {resolution_status!r};"
                        " must be one of: pending, resolved, deferred"
                    ),
                )
            )
            continue

        if status_val == "deferred":
            resolution_note = block.get("resolution_note")
            if _is_empty(resolution_note):
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno_raw,
                        message=(
                            f"{raw_id}: resolution_status:deferred requires a non-empty"
                            " resolution_note field"
                        ),
                    )
                )

    return violations
