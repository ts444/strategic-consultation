"""Rule: phase _trace.jsonl is non-empty (soft warning, non-blocking)."""

from pathlib import Path

from validator import Warning

RULE: str = "trace_populated"


def check(path: Path) -> list[Warning]:
    """Return a warning if the phase directory has no _trace.jsonl entries.

    The artifact path is expected to live inside a phase directory
    (e.g. 00-intake/scope.md).  The rule looks for _trace.jsonl as a sibling.
    """
    phase_dir = path.parent
    trace_path = phase_dir / "_trace.jsonl"

    if not trace_path.exists():
        return [
            Warning(
                rule=RULE,
                message=(
                    f"_trace.jsonl not found in {phase_dir.name}/"
                    " — phase was not run via enter_phase"
                ),
            )
        ]

    content = trace_path.read_text(encoding="utf-8").strip()
    if not content:
        return [
            Warning(
                rule=RULE,
                message=(
                    f"_trace.jsonl in {phase_dir.name}/ is empty"
                    " — no subagent invocations recorded"
                ),
            )
        ]

    return []
