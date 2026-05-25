"""Rule: every claim annotation has a [label] tag."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines

RULE: str = "claim_label_present"

_LABEL = re.compile(r"\[(known|inferred|elicited|assumed)\]")
_SOURCE = re.compile(r"\[source:")
_CONF = re.compile(r"\[conf:[HML]\]")


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    violations: list[Violation] = []
    for lineno, line in body_lines(text):
        has_source = bool(_SOURCE.search(line))
        has_conf = bool(_CONF.search(line))
        has_label = bool(_LABEL.search(line))
        if (has_source or has_conf) and not has_label:
            violations.append(
                Violation(rule=RULE, line=lineno, message="claim annotation missing [label] tag")
            )
    return violations
