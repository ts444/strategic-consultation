"""Rule: RMI blocks must have compliance_role, conditional compliance_deadline, budget_envelope."""

from __future__ import annotations

import re
from pathlib import Path

from validator import Violation
from validator._util import parse_yaml_blocks

RULE: str = "roadmap_item_required_fields"

_RMI_ID_RE = re.compile(r"^RMI-\d+$")
_BUD_ID_RE = re.compile(r"^BUD-\d+$")
_BUD_DECL_RE = re.compile(r"\bid:\s*(BUD-\d+)")


def _known_bud_ids(artifact: Path) -> set[str] | None:
    """Return declared BUD-NNN ids from _budget.md, or None if not found."""
    for parent in (artifact.parent, artifact.parent.parent):
        reg = parent / "_budget.md"
        if reg.exists():
            return set(_BUD_DECL_RE.findall(reg.read_text(encoding="utf-8")))
    return None


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    known_bud = _known_bud_ids(path)
    violations: list[Violation] = []

    has_y1_quick_win = False

    for block in blocks:
        raw_id = block.get("id")
        if not isinstance(raw_id, str) or not _RMI_ID_RE.match(raw_id.strip()):
            continue

        lineno_raw = block["_lineno"]
        assert isinstance(lineno_raw, int)
        lineno = lineno_raw
        present_keys = block["_present_keys"]
        assert isinstance(present_keys, set)

        # Track Y1 quick-win
        year_val = block.get("year")
        qw_val = block.get("quick_win")
        if isinstance(year_val, str) and year_val.strip() == "Y1":
            if isinstance(qw_val, str) and qw_val.strip().lower() == "true":
                has_y1_quick_win = True

        # compliance_role mandatory
        if "compliance_role" not in present_keys:
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno,
                    message=f"{raw_id}: missing required field 'compliance_role'",
                )
            )
        else:
            role = block.get("compliance_role")
            if isinstance(role, str):
                role = role.strip()
                if role == "deadline":
                    if "compliance_deadline" not in present_keys:
                        violations.append(
                            Violation(
                                rule=RULE,
                                line=lineno,
                                message=(
                                    f"{raw_id}: compliance_role=deadline"
                                    " requires compliance_deadline field"
                                ),
                            )
                        )
                else:
                    if "compliance_deadline" in present_keys:
                        violations.append(
                            Violation(
                                rule=RULE,
                                line=lineno,
                                message=(
                                    f"{raw_id}: compliance_deadline must be"
                                    f" absent when compliance_role={role}"
                                ),
                            )
                        )

        # budget_envelope mandatory and must resolve
        if "budget_envelope" not in present_keys:
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno,
                    message=f"{raw_id}: missing required field 'budget_envelope'",
                )
            )
        else:
            bud_val = block.get("budget_envelope")
            if isinstance(bud_val, str) and known_bud is not None:
                bud_ref = bud_val.strip()
                if _BUD_ID_RE.match(bud_ref) and bud_ref not in known_bud:
                    violations.append(
                        Violation(
                            rule=RULE,
                            line=lineno,
                            message=f"{raw_id}: budget_envelope references unknown id: {bud_ref}",
                        )
                    )

    # File-level: at least one Y1 quick-win required when RMI blocks exist
    rmi_blocks = [
        b for b in blocks
        if isinstance(b.get("id"), str) and _RMI_ID_RE.match(str(b.get("id", "")).strip())
    ]
    if rmi_blocks and not has_y1_quick_win:
        violations.append(
            Violation(
                rule=RULE,
                line=None,
                message="roadmap has no Y1 item with quick_win: true (at least one required)",
            )
        )

    return violations
