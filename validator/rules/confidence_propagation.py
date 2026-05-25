"""Rule: composed claim conf ≤ min(input claim confs)."""

import re
from pathlib import Path

from validator import Violation
from validator._util import body_lines

RULE: str = "confidence_propagation"

_CONF_RE = re.compile(r"\[conf:([HML])\]")
_FROM_RE = re.compile(r"\[source:from:\s*([^\]]+)\]")

CONF_RANK: dict[str, int] = {"H": 2, "M": 1, "L": 0}
_RANK_TO_CONF: dict[int, str] = {v: k for k, v in CONF_RANK.items()}


def _build_conf_map(text: str) -> dict[str, str]:
    """Return {block_id.field_name → conf} from YAML blocks inside ```yaml fences."""
    conf_map: dict[str, str] = {}
    in_fence = False
    in_block = False
    block_id: str | None = None
    current_field: str | None = None

    for _, raw_line in body_lines(text):
        stripped = raw_line.strip()

        if stripped == "```yaml" and not in_fence:
            in_fence = True
            in_block = False
            block_id = None
            current_field = None
            continue

        if stripped == "```" and in_fence:
            in_fence = False
            in_block = False
            continue

        if not in_fence:
            continue

        if stripped == "---":
            if not in_block:
                in_block = True
                block_id = None
                current_field = None
            else:
                in_block = False
            continue

        if not in_block:
            continue

        # Parse block id
        if stripped.startswith("id:") and not raw_line[0:1].isspace():
            block_id = stripped[3:].strip()
            current_field = "id"
            continue

        # Track current top-level field name (unindented lines with a colon)
        if raw_line and not raw_line[0].isspace() and ":" in raw_line:
            current_field = raw_line.split(":", 1)[0].strip()

        # Capture conf value for this field
        conf_m = _CONF_RE.search(raw_line)
        if conf_m and block_id and current_field and current_field != "id":
            conf_val = conf_m.group(1)
            field_key = f"{block_id}.{current_field}"
            if field_key not in conf_map:
                conf_map[field_key] = conf_val
            # Also record block-level key with the first conf seen in the block
            if block_id not in conf_map:
                conf_map[block_id] = conf_val

    return conf_map


def check(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8")
    conf_map = _build_conf_map(text)
    violations: list[Violation] = []

    for lineno, line in body_lines(text):
        from_m = _FROM_RE.search(line)
        if not from_m:
            continue

        # Find the conf tag that follows the [source:from:...] tag
        after_from = line[from_m.end() :]
        conf_m = _CONF_RE.search(after_from) or _CONF_RE.search(line)
        if not conf_m:
            continue

        composed_conf = conf_m.group(1)
        raw_from = from_m.group(1)
        refs = [r.strip() for r in raw_from.split("+")]

        input_confs: list[str] = []
        for ref in refs:
            if ref in conf_map:
                input_confs.append(conf_map[ref])

        if not input_confs:
            continue  # Can't verify without known input confs — skip

        min_rank = min(CONF_RANK[c] for c in input_confs)
        composed_rank = CONF_RANK[composed_conf]

        if composed_rank > min_rank:
            min_label = _RANK_TO_CONF[min_rank]
            violations.append(
                Violation(
                    rule=RULE,
                    line=lineno,
                    message=(
                        f"composed claim conf:{composed_conf} exceeds min input conf:{min_label}"
                        f" (refs: {', '.join(refs)})"
                    ),
                )
            )

    return violations
