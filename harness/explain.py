#!/usr/bin/env python3
"""Explain claim traversal tool.

Usage:
    python -m harness.explain <engagement-repo> <claim-id>

Walks a claim back through its 'from: A + B' composition graph to leaf
facts ([known] and [elicited]), printing a tree with source URIs.  Also
surfaces any decisions in _decisions.md whose 'overrides:' field hits any
claim in the chain.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from harness.decay_check import (
    _PHASE_DIRS,
    Claim,
    _extract_claims,
)

# ---------------------------------------------------------------------------
# Decisions parsing
# ---------------------------------------------------------------------------


@dataclass
class Decision:
    dec_id: str
    title: str
    overrides: list[str]
    artifact: Path
    lineno: int


def _parse_decisions_text(text: str, artifact: Path) -> list[Decision]:
    """Parse decisions register content and return Decision objects."""
    lines = text.splitlines()
    out: list[Decision] = []
    in_fence = False
    in_block = False
    current: dict[str, object] = {}
    block_start = 0
    in_overrides = False

    for i, raw in enumerate(lines):
        s = raw.strip()
        if s == "```yaml" and not in_fence:
            in_fence, in_block, current, in_overrides = True, False, {}, False
            continue
        if s == "```" and in_fence:
            if in_block:
                _flush_decision(current, block_start, artifact, out)
            in_fence, in_block, current, in_overrides = False, False, {}, False
            continue
        if not in_fence:
            continue
        if s == "---":
            if not in_block:
                in_block, current, block_start, in_overrides = True, {}, i + 1, False
            else:
                _flush_decision(current, block_start, artifact, out)
                in_block, current, in_overrides = False, {}, False
            continue
        if not in_block:
            continue
        if not raw[:1].isspace():
            in_overrides = False
            if ":" in s and not s.startswith("#"):
                k, _, v = s.partition(":")
                k, v = k.strip(), v.strip()
                if k == "overrides":
                    current["overrides"] = [v] if v else []
                    in_overrides = not bool(v)
                else:
                    current[k] = v
        elif in_overrides and s.startswith("-"):
            item = s[1:].strip().strip('"').strip("'")
            if item:
                ov = current.setdefault("overrides", [])
                assert isinstance(ov, list)
                ov.append(item)

    return out


def _flush_decision(
    blk: dict[str, object], lineno: int, artifact: Path, out: list[Decision]
) -> None:
    dec_id = str(blk.get("id", "")).strip('"').strip("'")
    if not dec_id:
        return
    title = str(blk.get("title", "")).strip('"').strip("'")
    raw_ov = blk.get("overrides", [])
    if isinstance(raw_ov, list):
        overrides = [str(x).strip('"').strip("'") for x in raw_ov]
    else:
        overrides = [str(raw_ov).strip('"').strip("'")]
    out.append(
        Decision(dec_id=dec_id, title=title, overrides=overrides, artifact=artifact, lineno=lineno)
    )


def _load_decisions(repo: Path) -> list[Decision]:
    f = repo / "_decisions.md"
    if not f.exists():
        return []
    return _parse_decisions_text(f.read_text(encoding="utf-8"), f)


# ---------------------------------------------------------------------------
# Claim collection
# ---------------------------------------------------------------------------


def _collect_claims(repo: Path) -> list[Claim]:
    """Collect claims from all phase artifact .md files (skips _register files)."""
    claims: list[Claim] = []
    for phase_dir in _PHASE_DIRS:
        phase_path = repo / phase_dir
        if not phase_path.is_dir():
            continue
        for md in sorted(phase_path.glob("*.md")):
            if md.name.startswith("_"):
                continue
            claims.extend(_extract_claims(md))
    return claims


def _build_index(claims: list[Claim]) -> dict[str, Claim]:
    """Map claim_id to its first-seen Claim (earlier phases win)."""
    index: dict[str, Claim] = {}
    for c in claims:
        if c.claim_id not in index:
            index[c.claim_id] = c
    return index


# ---------------------------------------------------------------------------
# Tree datatype + traversal
# ---------------------------------------------------------------------------


@dataclass
class ExplainNode:
    claim: Claim
    children: list[ExplainNode] = field(default_factory=list)
    missing: bool = False
    is_cycle: bool = False


def _build_tree(
    claim_id: str,
    index: dict[str, Claim],
    visited: frozenset[str] = frozenset(),
) -> ExplainNode:
    """Recursively build an explain tree rooted at claim_id."""
    if claim_id in visited:
        stub = Claim(
            claim_id=claim_id,
            label="(cycle)",
            source="(circular reference)",
            conf="?",
            artifact=Path("(cycle)"),
            lineno=0,
            phase_idx=-1,
        )
        return ExplainNode(claim=stub, is_cycle=True)

    claim = index.get(claim_id)
    if claim is None:
        stub = Claim(
            claim_id=claim_id,
            label="(not found)",
            source="(claim not found in any artifact)",
            conf="?",
            artifact=Path("(unknown)"),
            lineno=0,
            phase_idx=-1,
        )
        return ExplainNode(claim=stub, missing=True)

    node = ExplainNode(claim=claim)
    new_visited = visited | {claim_id}
    for child_id in claim.composed_from:
        node.children.append(_build_tree(child_id, index, new_visited))
    return node


def _all_ids(node: ExplainNode, ids: set[str] | None = None) -> set[str]:
    """Collect all claim ids reachable in the tree."""
    if ids is None:
        ids = set()
    ids.add(node.claim.claim_id)
    for child in node.children:
        _all_ids(child, ids)
    return ids


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _rel(p: Path) -> str:
    parts = p.parts
    return str(Path(parts[-2]) / parts[-1]) if len(parts) >= 2 else str(p)


def _render(node: ExplainNode, depth: int = 0) -> list[str]:
    """Render an ExplainNode as indented text lines."""
    pad = "  " * depth
    c = node.claim
    conf_part = f" conf:{c.conf}" if c.conf != "?" else ""
    lines = [f"{pad}{c.claim_id} [{c.label}]{conf_part}"]
    detail = pad + "  "
    lines.append(f"{detail}source: {c.source}")
    if not node.missing and not node.is_cycle:
        lines.append(f"{detail}at: {_rel(c.artifact)}:{c.lineno}")
    for child in node.children:
        lines.extend(_render(child, depth + 1))
    return lines


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@dataclass
class ExplainResult:
    root: ExplainNode
    decisions: list[Decision]
    chain_ids: set[str]


def explain_claim(repo: Path, claim_id: str) -> ExplainResult | None:
    """Walk claim_id through its composition graph.

    Returns None if the claim id is not found in any artifact.
    """
    claims = _collect_claims(repo)
    index = _build_index(claims)
    if claim_id not in index:
        return None

    root = _build_tree(claim_id, index)
    chain_ids = _all_ids(root)
    relevant = [d for d in _load_decisions(repo) if any(ov in chain_ids for ov in d.overrides)]
    return ExplainResult(root=root, decisions=relevant, chain_ids=chain_ids)


def format_result(result: ExplainResult) -> str:
    """Return the explain output as a string."""
    lines = _render(result.root)
    if result.decisions:
        lines.append("")
        lines.append("Decisions overriding claims in this chain:")
        for dec in result.decisions:
            title_part = f" — {dec.title}" if dec.title else ""
            lines.append(f"  {dec.dec_id}{title_part}")
            lines.append(f"    overrides: {', '.join(dec.overrides)}")
            lines.append(f"    at: {_rel(dec.artifact)}:{dec.lineno}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Walk a claim back to its leaf facts.")
    p.add_argument("engagement_repo", help="Path to the engagement repo root")
    p.add_argument("claim_id", help="Claim id to explain (e.g. GAP-001)")
    args = p.parse_args(argv)

    repo = Path(args.engagement_repo)
    if not repo.is_dir():
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 1

    result = explain_claim(repo, args.claim_id)
    if result is None:
        print(f"error: claim '{args.claim_id}' not found", file=sys.stderr)
        return 1

    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
