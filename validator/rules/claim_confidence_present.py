"""Rule: every claim has a [conf:H|M|L] tag."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines

RULE: str = "claim_confidence_present"

_LABEL = re.compile(r"\[(known|inferred|elicited|assumed)\]")
_CONF = re.compile(r"\[conf:[HML]\]")


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    violations: list[Violation] = []
    for lineno, line in body_lines(text):
        if _LABEL.search(line) and not _CONF.search(line):
            violations.append(
                Violation(rule=RULE, line=lineno, message="claim missing [conf:H|M|L] tag")
            )
    return violations
