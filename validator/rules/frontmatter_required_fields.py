"""Rule: artifact frontmatter has all required fields."""

from pathlib import Path

from validator import Violation
from validator._util import frontmatter_keys

RULE: str = "frontmatter_required_fields"

REQUIRED_KEYS: frozenset[str] = frozenset({"phase", "status", "harness_version", "template"})


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    keys = frontmatter_keys(text)
    violations: list[Violation] = []
    for key in sorted(REQUIRED_KEYS - keys):
        violations.append(
            Violation(
                rule=RULE,
                line=None,
                message=f"frontmatter missing required field: {key!r}",
            )
        )
    return violations
