"""Rule: artifact has the H2 sections required by its template."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines, frontmatter_value

RULE: str = "template_conformance"

# Maps template base-name → list of required H2 heading strings (exact match)
REQUIRED_H2: dict[str, list[str]] = {
    "roadmap": ["## Sequencing argument"],
    "gaps": ["## 1. Goal Coverage Map"],
}

_TEMPLATE_BASE_RE = re.compile(r"^([\w-]+)")


def _template_base(text: str) -> str | None:
    """Extract the template base name from the frontmatter template field.

    E.g. 'roadmap@1.0.0' → 'roadmap'.
    """
    raw = frontmatter_value(text, "template")
    if not raw:
        return None
    m = _TEMPLATE_BASE_RE.match(raw)
    return m.group(1) if m else None


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    name = _template_base(text)
    if name is None or name not in REQUIRED_H2:
        return []

    required_headings = REQUIRED_H2[name]
    violations: list[Violation] = []

    h2_present: set[str] = set()
    for _, line in body_lines(text):
        stripped = line.strip()
        if stripped.startswith("## "):
            h2_present.add(stripped)

    for heading in required_headings:
        if heading not in h2_present:
            violations.append(
                Violation(
                    rule=RULE,
                    line=None,
                    message=f"template '{name}' requires H2 section: {heading!r}",
                )
            )

    return violations
