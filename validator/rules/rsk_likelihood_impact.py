"""Rule: every RSK block must declare likelihood and impact (low | medium | high)."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import parse_yaml_blocks

RULE: str = "rsk_likelihood_impact"

_RSK_ID_RE = re.compile(r"^RSK-\d+$")
_VALID_VALUES: frozenset[str] = frozenset({"low", "medium", "high"})
_REQUIRED_FIELDS: tuple[str, ...] = ("likelihood", "impact")


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    violations: list[Violation] = []

    for block in blocks:
        raw_id = block.get("id")
        if not isinstance(raw_id, str) or not _RSK_ID_RE.match(raw_id.strip()):
            continue

        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)
        present_keys = block["_present_keys"]
        assert isinstance(present_keys, set)

        for field in _REQUIRED_FIELDS:
            if field not in present_keys:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno_raw,
                        message=(
                            f"{raw_id}: missing required field '{field}'"
                            " (must be low | medium | high)"
                        ),
                    )
                )
            else:
                value = block.get(field)
                if not isinstance(value, str) or value.strip() not in _VALID_VALUES:
                    violations.append(
                        Violation(
                            rule=RULE,
                            line=lineno_raw,
                            message=(
                                f"{raw_id}: field '{field}' has invalid value {value!r};"
                                " must be one of: low, medium, high"
                            ),
                        )
                    )

    return violations
