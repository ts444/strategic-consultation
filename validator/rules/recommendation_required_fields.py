"""Rule: every REC block must declare compliance_relation, cost, lock_in, opportunity_cost."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import parse_yaml_blocks

RULE: str = "recommendation_required_fields"

_REC_ID_RE = re.compile(r"^REC-\d+$")

_REQUIRED: tuple[str, ...] = (
    "compliance_relation",
    "cost",
    "lock_in",
    "opportunity_cost",
)


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    violations: list[Violation] = []

    for block in blocks:
        raw_id = block.get("id")
        if not isinstance(raw_id, str) or not _REC_ID_RE.match(raw_id.strip()):
            continue

        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)
        lineno = lineno_raw
        present_keys = block["_present_keys"]
        assert isinstance(present_keys, set)

        for field in _REQUIRED:
            if field not in present_keys:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno,
                        message=(
                            f"{raw_id}: missing required field '{field}'"
                            " ('none'/'tbc' valid; absence is not)"
                        ),
                    )
                )

    return violations
