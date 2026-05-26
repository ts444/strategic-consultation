"""Rule: claim label matches the producing subagent declared in frontmatter."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines, frontmatter_value

RULE: str = "label_producer_binding"

_LABEL_RE = re.compile(r"\[(known|inferred|elicited|assumed)\]")

# Maps produced_by value → allowed claim labels (from _claim.schema.md §1.2)
PRODUCER_ALLOWED_LABELS: dict[str, frozenset[str]] = {
    "portfolio-retriever": frozenset({"known"}),
    "customer-data-retriever": frozenset({"known"}),
    "interviewer": frozenset({"elicited"}),
    "synthesizer": frozenset({"inferred", "assumed"}),
}


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    producer = frontmatter_value(text, "produced_by")
    if not producer or producer not in PRODUCER_ALLOWED_LABELS:
        return []

    allowed = PRODUCER_ALLOWED_LABELS[producer]
    violations: list[Violation] = []

    for lineno, line in body_lines(text):
        for label_m in _LABEL_RE.finditer(line):
            label = label_m.group(1)
            if label not in allowed:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno,
                        message=(
                            f"label [{label}] not permitted for producer '{producer}'"
                            f" (allowed: {sorted(allowed)})"
                        ),
                    )
                )

    return violations
