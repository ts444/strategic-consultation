#!/usr/bin/env python3
"""Decay-check tool: surface stale claims at phase entry.

Usage:
    python -m harness.decay_check <engagement-repo> [--current-phase N]
                                  [--skip-known]

Output groups:
  HARD STALE                     — [known] claims whose source has changed
  ELICITED DUE FOR REVALIDATION  — [elicited] claims past phase-distance threshold
  ASSUMPTIONS FLAGGED            — _assumptions.md entries with requires_revalidation
  DOWNSTREAM IMPACT              — [inferred]/[assumed] claims depending on stale inputs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Phase ordering
# ---------------------------------------------------------------------------

_PHASE_DIRS = [
    "00-intake",
    "01-situation",
    "02-gap",
    "03-mapping",
    "04-roadmap",
    "05-handover",
    "06-retro",
]
_PHASE_INDEX: dict[str, int] = {p: i for i, p in enumerate(_PHASE_DIRS)}

# Elicited-decay thresholds: claim goes stale when phase_distance >= threshold
_DEFAULT_THRESHOLDS: dict[str, int] = {"H": 3, "M": 2, "L": 1}

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

_LABEL_RE = re.compile(r"\[(known|inferred|elicited|assumed)\]")
_SOURCE_RE = re.compile(r"\[source:([^\]]+)\]")
_CONF_RE = re.compile(r"\[conf:([HML])\]")
# portfolio://<domain/path.md>@<ref>  (ref has no '@')
_PORTFOLIO_URI_RE = re.compile(r"^portfolio://([^@]+)@([^@]+)$")
# customer-portal://<resource>/<id>@<updated_at>
_CUSTOMER_URI_RE = re.compile(r"^customer-portal://([^/]+)/([^@]+)@(.+)$")
_CLAIM_ID_PAT = re.compile(r"^[A-Z]{2,8}-\d+$")

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Claim:
    claim_id: str
    label: str
    source: str
    conf: str
    artifact: Path
    lineno: int
    phase_idx: int
    composed_from: list[str] = field(default_factory=list)


@dataclass
class StaleEntry:
    claim_id: str
    label: str
    artifact: Path
    lineno: int
    reason: str


@dataclass
class DecayResult:
    hard_stale: list[StaleEntry] = field(default_factory=list)
    elicited_due: list[StaleEntry] = field(default_factory=list)
    assumptions_flagged: list[StaleEntry] = field(default_factory=list)
    downstream_impact: list[StaleEntry] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _phase_idx_of(artifact: Path) -> int:
    """Return the phase index for an artifact based on its parent directory."""
    for part in artifact.parts:
        if part in _PHASE_INDEX:
            return _PHASE_INDEX[part]
    return -1


def _frontmatter_value(text: str, key: str) -> str | None:
    raw = text.splitlines()
    if not raw or raw[0].strip() != "---":
        return None
    for line in raw[1:]:
        if line.strip() == "---":
            break
        if not line or line[0].isspace():
            continue
        if line.startswith(f"{key}:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            return val if val else None
    return None


def _find_ratified_artifacts(repo: Path) -> list[Path]:
    artifacts: list[Path] = []
    for phase_dir in _PHASE_DIRS:
        phase_path = repo / phase_dir
        if not phase_path.is_dir():
            continue
        for md_file in sorted(phase_path.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            if _frontmatter_value(text, "status") == "ratified":
                artifacts.append(md_file)
    return artifacts


def _detect_current_phase(repo: Path) -> int:
    """Return the index of the next un-entered phase (highest ratified phase + 1)."""
    highest = -1
    for phase_dir in _PHASE_DIRS:
        phase_path = repo / phase_dir
        if not phase_path.is_dir():
            continue
        for md_file in phase_path.glob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            if _frontmatter_value(text, "status") == "ratified":
                highest = max(highest, _PHASE_INDEX[phase_dir])
    return highest + 1


def _append_trace(trace_path: Path | None, entry: dict[str, object]) -> None:
    if trace_path is None:
        return
    record: dict[str, object] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **entry,
    }
    with trace_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _extract_claims(artifact: Path) -> list[Claim]:
    """Scan artifact body for claim atoms and return Claim objects."""
    phase_idx = _phase_idx_of(artifact)
    text = artifact.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Skip YAML frontmatter
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break

    claims: list[Claim] = []
    in_yaml_fence = False
    in_yaml_block = False
    current_block_id: str | None = None

    for i in range(start, len(lines)):
        lineno = i + 1
        line = lines[i]
        stripped = line.strip()

        if stripped == "```yaml" and not in_yaml_fence:
            in_yaml_fence = True
            in_yaml_block = False
            current_block_id = None
            continue

        if stripped == "```" and in_yaml_fence:
            in_yaml_fence = False
            in_yaml_block = False
            current_block_id = None
            continue

        if in_yaml_fence and stripped == "---":
            if not in_yaml_block:
                in_yaml_block = True
                current_block_id = None
            else:
                in_yaml_block = False
                current_block_id = None
            continue

        # Capture id: field from top-level YAML block lines
        if in_yaml_fence and in_yaml_block and line and not line[0].isspace():
            if stripped.startswith("id:"):
                current_block_id = (
                    stripped.split(":", 1)[1].strip().strip('"').strip("'")
                )

        # Match claim atoms on any body line
        label_m = _LABEL_RE.search(line)
        source_m = _SOURCE_RE.search(line)
        if not (label_m and source_m):
            continue

        label = label_m.group(1)
        source = source_m.group(1).strip()
        conf_m = _CONF_RE.search(line)
        conf = conf_m.group(1) if conf_m else "M"
        claim_id = current_block_id or f"line-{lineno}"

        composed_from: list[str] = []
        if source.startswith("from:"):
            refs_str = source[5:].strip()
            for ref in re.split(r"\s*\+\s*", refs_str):
                ref = ref.strip()
                if _CLAIM_ID_PAT.match(ref):
                    composed_from.append(ref)

        claims.append(
            Claim(
                claim_id=claim_id,
                label=label,
                source=source,
                conf=conf,
                artifact=artifact,
                lineno=lineno,
                phase_idx=phase_idx,
                composed_from=composed_from,
            )
        )

    return claims


def _assumptions_entry_stale(
    blk: dict[str, str],
    start_lineno: int,
    current_phase: int,
    artifact: Path,
) -> StaleEntry | None:
    req_reval = blk.get("requires_revalidation", "true").strip('"').strip("'").lower()
    if req_reval != "true":
        return None
    pe_raw = blk.get("phase_expires", "never").strip('"').strip("'")
    if pe_raw == "never":
        return None
    try:
        pe_int = int(pe_raw)
    except ValueError:
        return None
    if current_phase <= pe_int:
        return None
    entry_id = blk.get("id", f"ASM-line-{start_lineno}").strip('"').strip("'")
    return StaleEntry(
        claim_id=entry_id,
        label="assumed",
        artifact=artifact,
        lineno=start_lineno,
        reason=(
            f"requires_revalidation=true, "
            f"phase_expires={pe_raw!r}, "
            f"current_phase={current_phase}"
        ),
    )


# ---------------------------------------------------------------------------
# Decay check functions
# ---------------------------------------------------------------------------


def _check_known_decay(
    claims: list[Claim],
    head_portfolio: Callable[[str], str] | None,
    head_customer: Callable[[str, str], str] | None,
    trace_path: Path | None,
) -> list[StaleEntry]:
    stale: list[StaleEntry] = []
    for claim in claims:
        if claim.label != "known":
            continue

        port_m = _PORTFOLIO_URI_RE.match(claim.source)
        cust_m = _CUSTOMER_URI_RE.match(claim.source)

        if port_m is not None and head_portfolio is not None:
            source_name = port_m.group(1)
            stored_ref = port_m.group(2)
            try:
                current_ref = head_portfolio(source_name)
            except Exception:
                current_ref = stored_ref  # can't verify; skip

            if current_ref != stored_ref:
                stale.append(
                    StaleEntry(
                        claim_id=claim.claim_id,
                        label="known",
                        artifact=claim.artifact,
                        lineno=claim.lineno,
                        reason=(
                            f"portfolio://{source_name} changed: "
                            f"was {stored_ref!r}, now {current_ref!r}"
                        ),
                    )
                )
            else:
                _append_trace(
                    trace_path,
                    {
                        "type": "known_freshness_check",
                        "claim_id": claim.claim_id,
                        "source": claim.source,
                        "status": "unchanged",
                        "ref": current_ref,
                    },
                )

        elif cust_m is not None and head_customer is not None:
            resource_type = cust_m.group(1)
            id_part = cust_m.group(2)
            stored_ref = cust_m.group(3)
            try:
                current_ref = head_customer(resource_type, id_part)
            except Exception:
                current_ref = stored_ref

            if current_ref != stored_ref:
                stale.append(
                    StaleEntry(
                        claim_id=claim.claim_id,
                        label="known",
                        artifact=claim.artifact,
                        lineno=claim.lineno,
                        reason=(
                            f"customer-portal://{resource_type}/{id_part} changed: "
                            f"was {stored_ref!r}, now {current_ref!r}"
                        ),
                    )
                )
            else:
                _append_trace(
                    trace_path,
                    {
                        "type": "known_freshness_check",
                        "claim_id": claim.claim_id,
                        "source": claim.source,
                        "status": "unchanged",
                        "ref": current_ref,
                    },
                )

    return stale


def _check_elicited_decay(
    claims: list[Claim],
    current_phase: int,
    thresholds: dict[str, int],
) -> list[StaleEntry]:
    due: list[StaleEntry] = []
    for claim in claims:
        if claim.label != "elicited":
            continue
        if claim.phase_idx < 0:
            continue
        distance = current_phase - claim.phase_idx
        threshold = thresholds.get(claim.conf, 1)
        if distance >= threshold:
            due.append(
                StaleEntry(
                    claim_id=claim.claim_id,
                    label="elicited",
                    artifact=claim.artifact,
                    lineno=claim.lineno,
                    reason=(
                        f"conf={claim.conf} threshold={threshold} "
                        f"phase_distance={distance}"
                    ),
                )
            )
    return due


def _check_assumptions(repo: Path, current_phase: int) -> list[StaleEntry]:
    flagged: list[StaleEntry] = []
    assumptions_file = repo / "_assumptions.md"
    if not assumptions_file.exists():
        return flagged

    text = assumptions_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_fence = False
    in_block = False
    current: dict[str, str] = {}
    block_start_lineno = 0

    for i, raw_line in enumerate(lines):
        stripped = raw_line.strip()

        if stripped == "```yaml" and not in_fence:
            in_fence = True
            in_block = False
            current = {}
            continue

        if stripped == "```" and in_fence:
            if in_block:
                entry = _assumptions_entry_stale(
                    current, block_start_lineno, current_phase, assumptions_file
                )
                if entry is not None:
                    flagged.append(entry)
            in_fence = False
            in_block = False
            current = {}
            continue

        if not in_fence:
            continue

        if stripped == "---":
            if not in_block:
                in_block = True
                current = {}
                block_start_lineno = i + 1
            else:
                entry = _assumptions_entry_stale(
                    current, block_start_lineno, current_phase, assumptions_file
                )
                if entry is not None:
                    flagged.append(entry)
                in_block = False
                current = {}
            continue

        if in_block and ":" in stripped and not stripped.startswith("#"):
            if not raw_line[0:1].isspace():
                k, _, v = stripped.partition(":")
                current[k.strip()] = v.strip()

    return flagged


def _check_downstream(
    claims: list[Claim],
    stale_ids: set[str],
) -> list[StaleEntry]:
    downstream: list[StaleEntry] = []
    for claim in claims:
        if claim.label not in ("inferred", "assumed"):
            continue
        if not claim.composed_from:
            continue
        impacted = [ref for ref in claim.composed_from if ref in stale_ids]
        if impacted:
            downstream.append(
                StaleEntry(
                    claim_id=claim.claim_id,
                    label=claim.label,
                    artifact=claim.artifact,
                    lineno=claim.lineno,
                    reason=f"depends on stale input(s): {', '.join(impacted)}",
                )
            )
    return downstream


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_decay_check(
    engagement_repo: Path,
    current_phase: int | None = None,
    elicited_thresholds: dict[str, int] | None = None,
    head_portfolio: Callable[[str], str] | None = None,
    head_customer: Callable[[str, str], str] | None = None,
    trace_path: Path | None = None,
) -> DecayResult:
    """Run all decay checks against an engagement repo.

    Args:
        engagement_repo: Root of the engagement repo.
        current_phase: Phase index we are about to enter (0–6).
                       Auto-detected from ratified artifacts if None.
        elicited_thresholds: Override default {H:3, M:2, L:1} stale thresholds.
        head_portfolio: Callable(source_name) → current_ref for portfolio sources.
                        If None, [known] portfolio checks are skipped.
        head_customer: Callable(resource_type, id) → current_ref for customer sources.
                       If None, [known] customer checks are skipped.
        trace_path: Path to _trace.jsonl for freshness-bump logging.
                    Auto-resolved to current phase dir/_trace.jsonl if None.
    """
    if elicited_thresholds is None:
        elicited_thresholds = dict(_DEFAULT_THRESHOLDS)

    if current_phase is None:
        current_phase = _detect_current_phase(engagement_repo)

    if trace_path is None and 0 <= current_phase < len(_PHASE_DIRS):
        phase_dir = engagement_repo / _PHASE_DIRS[current_phase]
        if phase_dir.is_dir():
            trace_path = phase_dir / "_trace.jsonl"

    artifacts = _find_ratified_artifacts(engagement_repo)
    all_claims: list[Claim] = []
    for artifact in artifacts:
        all_claims.extend(_extract_claims(artifact))

    hard_stale = _check_known_decay(
        all_claims, head_portfolio, head_customer, trace_path
    )
    elicited_due = _check_elicited_decay(all_claims, current_phase, elicited_thresholds)
    assumptions_flagged = _check_assumptions(engagement_repo, current_phase)

    stale_ids = {e.claim_id for e in hard_stale} | {e.claim_id for e in elicited_due}
    downstream_impact = _check_downstream(all_claims, stale_ids)

    return DecayResult(
        hard_stale=hard_stale,
        elicited_due=elicited_due,
        assumptions_flagged=assumptions_flagged,
        downstream_impact=downstream_impact,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_result(result: DecayResult) -> None:
    sections = [
        ("HARD STALE", result.hard_stale),
        ("ELICITED DUE FOR REVALIDATION", result.elicited_due),
        ("ASSUMPTIONS FLAGGED", result.assumptions_flagged),
        ("DOWNSTREAM IMPACT", result.downstream_impact),
    ]
    if not any(entries for _, entries in sections):
        print("All claims fresh.")
        return
    for section_name, entries in sections:
        if not entries:
            continue
        print(f"\n{section_name}")
        for e in entries:
            rel = e.artifact.name
            print(f"  {e.claim_id} [{e.label}] — {e.reason}")
            print(f"    at {rel}:{e.lineno}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Surface stale claims in an engagement repo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("engagement_repo", help="Path to the engagement repo root")
    parser.add_argument(
        "--current-phase",
        type=int,
        default=None,
        metavar="N",
        help="Phase index we are about to enter (0–6; default: auto-detect)",
    )
    parser.add_argument(
        "--skip-known",
        action="store_true",
        help="Skip [known] MCP freshness checks",
    )
    args = parser.parse_args(argv)

    repo = Path(args.engagement_repo)
    if not repo.is_dir():
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 1

    result = run_decay_check(
        engagement_repo=repo,
        current_phase=args.current_phase,
    )
    _print_result(result)

    total = (
        len(result.hard_stale)
        + len(result.elicited_due)
        + len(result.assumptions_flagged)
        + len(result.downstream_impact)
    )
    return 1 if total > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
