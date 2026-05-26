"""Rule: bare framework names must not appear in titles or structured YAML fields."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines, parse_yaml_blocks

RULE: str = "framework_name_in_structured_fields"

# Default set of framework names to guard against bare use in structured fields
FRAMEWORK_NAMES: list[str] = [
    "GDPR",
    "NIS2",
    "ISO27001",
    "ISO 27001",
    "DORA",
    "PCI-DSS",
    "PCIDSS",
    "HIPAA",
    "SOC2",
    "SOC 2",
    "NIST",
    "CIS",
    "ENISA",
    "NIS",
    "CCPA",
    "LGPD",
]

# Regex matching any framework name as a whole word (case-sensitive)
_FW_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(fw) for fw in FRAMEWORK_NAMES) + r")\b"
)

# Markdown heading pattern (# ... ## ... ### ...)
_HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$")


def _is_prose_paragraph(line: str) -> bool:
    """Return True if the line looks like narrative prose (not a heading, list, or code)."""
    s = line.strip()
    if not s:
        return False
    if s.startswith("#"):
        return False
    if s.startswith("-") or s.startswith("*") or s.startswith(">"):
        return False
    if s.startswith("```") or s.startswith("|"):
        return False
    # Lines that look like YAML key: value pairs are structured
    if re.match(r"^\w[\w\s-]*:", s):
        return False
    return True


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    violations: list[Violation] = []

    # Check 1: headings — framework names in headings are always a violation
    for lineno, line in body_lines(text):
        m = _HEADING_RE.match(line.strip())
        if m:
            heading_text = m.group(1)
            fw_match = _FW_PATTERN.search(heading_text)
            if fw_match:
                violations.append(
                    Violation(
                        rule=RULE,
                        line=lineno,
                        message=(
                            f"bare framework name '{fw_match.group(0)}' in heading — "
                            "use a CMP-NNN reference instead"
                        ),
                    )
                )

    # Check 2: YAML structured fields inside ```yaml blocks
    blocks = parse_yaml_blocks(text)
    for block in blocks:
        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)
        lineno = lineno_raw
        present_keys = block["_present_keys"]
        assert isinstance(present_keys, set)

        for key in present_keys:
            val = block.get(key)
            values_to_check: list[str] = []
            if isinstance(val, str):
                values_to_check = [val]
            elif isinstance(val, list):
                values_to_check = [v for v in val if isinstance(v, str)]

            for v in values_to_check:
                fw_match = _FW_PATTERN.search(v)
                if fw_match:
                    violations.append(
                        Violation(
                            rule=RULE,
                            line=lineno,
                            message=(
                                f"bare framework name '{fw_match.group(0)}' in structured "
                                f"field '{key}' — use a CMP-NNN reference instead"
                            ),
                        )
                    )

    return violations
