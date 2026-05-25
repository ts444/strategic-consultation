"""Rule: every claim has a [source:…] tag."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines

RULE: str = "claim_source_present"

_LABEL = re.compile(r"\[(known|inferred|elicited|assumed)\]")
_SOURCE = re.compile(r"\[source:")


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    violations: list[Violation] = []
    for lineno, line in body_lines(text):
        if _LABEL.search(line) and not _SOURCE.search(line):
            violations.append(
                Violation(rule=RULE, line=lineno, message="claim missing [source:…] tag")
            )
    return violations
