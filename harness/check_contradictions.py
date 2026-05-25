#!/usr/bin/env python3
"""Contradiction-handling tool with blocking semantics.

Usage:
    python -m harness.check_contradictions <engagement-repo> [--phase NN]

Detects contradictions across three collision types:
  hard<->hard  — [known] or [elicited] facts contradict each other
  hard<->soft  — hard fact contradicts an [inferred] or [assumed] claim
  soft<->soft  — two [inferred] or [assumed] claims contradict each other

Explicit supersessions (supersedes: <claim-id>) are excluded from detection.

New contradictions are written as structured CON-NNN blocks to
<engagement-repo>/_contradictions.md.

Exit codes:
  0 — no unresolved contradictions blocking the requested phase
  1 — one or more unresolved contradictions block the phase (printed to stdout)
  2 — argument / usage error
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from harness.decay_check import (
    _PHASE_DIRS,
    _find_ratified_artifacts,
    _frontmatter_value,
)

# ── constants ──────────────────────────────────────────────────────────────

_LABEL_RE = re.compile(r"\[(known|inferred|elicited|assumed)\]")
_SOURCE_RE = re.compile(r"\[source:([^\]]+)\]")
_SUPERSEDES_RE = re.compile(r"supersedes:\s*([A-Z]{2,8}-\d+)", re.IGNORECASE)

_HARD_LABELS = frozenset({"known", "elicited"})
_SOFT_LABELS = frozenset({"inferred", "assumed"})

_NEGATION_WORDS = frozenset({
    "not", "no", "never", "isn't", "aren't", "doesn't", "don't", "won't",
    "cannot", "can't", "hasn't", "haven't", "hadn't", "wouldn't", "shouldn't",
    "neither", "nor", "none", "nothing",
})

_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "this", "that", "these",
    "those", "it", "its", "on", "in", "at", "to", "of", "for", "with",
    "and", "or", "but", "by", "from",
})


# ── data classes ───────────────────────────────────────────────────────────


@dataclass
class ContradictionEntry:
    con_id: str
    title: str
    claim_a: str
    claim_b: str
    collision_type: str
    detected_at: str
    detected_in_phase: str
    status: str
    blocks: list[str]
    resolution_path: str | None = None
    resolution_ref: str | None = None
    resolved_at: str | None = None


@dataclass
class ClaimAtom:
    claim_id: str
    label: str
    text: str  # prose content following claim markers
    artifact: Path
    lineno: int
    supersedes: str | None = None  # claim-id this claim explicitly supersedes


@dataclass
class ContradictionResult:
    detected: list[ContradictionEntry] = field(default_factory=list)
    blocking: list[ContradictionEntry] = field(default_factory=list)
    existing: list[ContradictionEntry] = field(default_factory=list)


# ── parsing ────────────────────────────────────────────────────────────────


def _parse_contradictions_register(path: Path) -> list[ContradictionEntry]:
    """Parse _contradictions.md YAML fence blocks into ContradictionEntry objects."""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    entries: list[ContradictionEntry] = []

    in_fence = False
    in_block = False
    current: dict[str, object] = {}
    in_list_key: str | None = None

    for raw in text.splitlines():
        s = raw.strip()

        if s == "```yaml" and not in_fence:
            in_fence = True
            in_block = False
            current = {}
            in_list_key = None
            continue

        if s == "```" and in_fence:
            if in_block and "id" in current:
                _flush_entry(current, entries)
            in_fence = False
            in_block = False
            current = {}
            in_list_key = None
            continue

        if not in_fence:
            continue

        if s == "---":
            if not in_block:
                in_block = True
                current = {}
                in_list_key = None
            else:
                if "id" in current:
                    _flush_entry(current, entries)
                in_block = False
                current = {}
                in_list_key = None
            continue

        if not in_block:
            continue

        # List item under current key
        if in_list_key is not None and raw and raw[0].isspace() and s.startswith("- "):
            item = s[2:].strip().strip('"').strip("'")
            lst = current[in_list_key]
            assert isinstance(lst, list)
            lst.append(item)
            continue

        # Top-level key: value
        if raw and not raw[0].isspace() and ":" in s and not s.startswith("#"):
            in_list_key = None
            key, _, val = s.partition(":")
            key = key.strip()
            val = val.strip()

            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                current[key] = (
                    [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
                    if inner
                    else []
                )
            elif val == "":
                current[key] = []
                in_list_key = key
            else:
                current[key] = val.strip('"').strip("'")

    return entries


def _flush_entry(blk: dict[str, object], out: list[ContradictionEntry]) -> None:
    con_id = str(blk.get("id", "")).strip('"').strip("'")
    if not con_id.startswith("CON-"):
        return

    raw_blocks = blk.get("Blocks", blk.get("blocks", []))
    if isinstance(raw_blocks, list):
        blocks_list = [str(v).strip('"').strip("'") for v in raw_blocks]
    elif isinstance(raw_blocks, str):
        inner = raw_blocks.strip("[]")
        blocks_list = (
            [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
            if inner
            else []
        )
    else:
        blocks_list = []

    def _opt(key: str) -> str | None:
        v = blk.get(key)
        if v is None or str(v).lower() in {"null", "none", "~", ""}:
            return None
        return str(v).strip('"').strip("'")

    out.append(
        ContradictionEntry(
            con_id=con_id,
            title=str(blk.get("title", "")).strip('"').strip("'"),
            claim_a=str(blk.get("claim_a", "")).strip('"').strip("'"),
            claim_b=str(blk.get("claim_b", "")).strip('"').strip("'"),
            collision_type=str(blk.get("collision_type", "")).strip('"').strip("'"),
            detected_at=str(blk.get("detected_at", "")).strip('"').strip("'"),
            detected_in_phase=str(blk.get("detected_in_phase", "")).strip('"').strip("'"),
            status=str(blk.get("Status", blk.get("status", "unresolved"))).strip('"').strip("'"),
            blocks=blocks_list,
            resolution_path=_opt("resolution_path"),
            resolution_ref=_opt("resolution_ref"),
            resolved_at=_opt("resolved_at"),
        )
    )


# ── claim atom extraction ──────────────────────────────────────────────────


def _extract_claim_atoms(artifacts: list[Path]) -> list[ClaimAtom]:
    """Extract ClaimAtom objects (with prose text) from artifact files."""
    atoms: list[ClaimAtom] = []
    for artifact in artifacts:
        text = artifact.read_text(encoding="utf-8")
        lines = text.splitlines()

        # Skip YAML frontmatter
        start = 0
        if lines and lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    start = i + 1
                    break

        in_fence = False
        in_block = False
        current_block_id: str | None = None

        for i in range(start, len(lines)):
            lineno = i + 1
            line = lines[i]
            stripped = line.strip()

            if stripped == "```yaml" and not in_fence:
                in_fence = True
                in_block = False
                current_block_id = None
                continue

            if stripped == "```" and in_fence:
                in_fence = False
                in_block = False
                current_block_id = None
                continue

            if in_fence and stripped == "---":
                if not in_block:
                    in_block = True
                    current_block_id = None
                else:
                    in_block = False
                    current_block_id = None
                continue

            if in_fence and in_block and line and not line[0].isspace():
                if stripped.startswith("id:"):
                    current_block_id = stripped.split(":", 1)[1].strip().strip('"').strip("'")

            label_m = _LABEL_RE.search(line)
            source_m = _SOURCE_RE.search(line)
            if not (label_m and source_m):
                continue

            label = label_m.group(1)
            # Extract prose text: everything after the last ] marker
            text_after = re.sub(r"\[source:[^\]]+\]", "", line)
            text_after = re.sub(r"\[(known|inferred|elicited|assumed)\]", "", text_after)
            text_after = re.sub(r"\[conf:[HML]\]", "", text_after).strip(" .")

            supersedes_m = _SUPERSEDES_RE.search(line)
            supersedes = supersedes_m.group(1) if supersedes_m else None

            claim_id = current_block_id or f"line-{lineno}"
            atoms.append(
                ClaimAtom(
                    claim_id=claim_id,
                    label=label,
                    text=text_after,
                    artifact=artifact,
                    lineno=lineno,
                    supersedes=supersedes,
                )
            )

    return atoms


# ── subject / polarity extraction ──────────────────────────────────────────


def _key_words(text: str) -> list[str]:
    """Return first 5 non-stopword lowercase tokens from text."""
    tokens = re.findall(r"[a-z']+", text.lower())
    out: list[str] = []
    for tok in tokens:
        if tok not in _STOPWORDS and tok not in _NEGATION_WORDS and len(tok) > 1:
            out.append(tok)
            if len(out) >= 5:
                break
    return out


def _has_negation(text: str) -> bool:
    tokens = set(re.findall(r"[a-z']+", text.lower()))
    return bool(tokens & _NEGATION_WORDS)


def _subject_overlap(words_a: list[str], words_b: list[str]) -> int:
    """Count shared words between the first-2 content words of each claim."""
    set_a = set(words_a[:2])
    set_b = set(words_b[:2])
    return len(set_a & set_b)


# ── collision classification ───────────────────────────────────────────────


def _collision_type(label_a: str, label_b: str) -> str:
    a_hard = label_a in _HARD_LABELS
    b_hard = label_b in _HARD_LABELS
    if a_hard and b_hard:
        return "hard<->hard"
    if a_hard or b_hard:
        return "hard<->soft"
    return "soft<->soft"


# ── detection ─────────────────────────────────────────────────────────────


def _already_registered(
    id_a: str,
    id_b: str,
    existing: list[ContradictionEntry],
) -> bool:
    for e in existing:
        pair = {e.claim_a, e.claim_b}
        if pair == {id_a, id_b}:
            return True
    return False


def _detect_new_contradictions(
    atoms: list[ClaimAtom],
    existing: list[ContradictionEntry],
    current_phase_dir: str,
) -> list[ContradictionEntry]:
    """Find contradicting pairs not already in the register."""
    superseded_ids: set[str] = {a.supersedes for a in atoms if a.supersedes}

    detected: list[ContradictionEntry] = []
    next_num = _next_con_number(existing)

    for i, a in enumerate(atoms):
        if a.claim_id in superseded_ids:
            continue
        words_a = _key_words(a.text)
        neg_a = _has_negation(a.text)

        for b in atoms[i + 1 :]:
            if b.claim_id in superseded_ids:
                continue
            # Same artifact + same claim_id → skip
            if a.artifact == b.artifact and a.claim_id == b.claim_id:
                continue
            if _already_registered(a.claim_id, b.claim_id, existing):
                continue
            if _already_registered(a.claim_id, b.claim_id, detected):
                continue

            words_b = _key_words(b.text)
            neg_b = _has_negation(b.text)

            # Contradiction: shared subject words AND opposite polarity
            if _subject_overlap(words_a, words_b) >= 2 and neg_a != neg_b:
                con_id = f"CON-{next_num:03d}"
                next_num += 1
                ctype = _collision_type(a.label, b.label)
                title = f"{a.claim_id} vs {b.claim_id}: {ctype} conflict"
                detected.append(
                    ContradictionEntry(
                        con_id=con_id,
                        title=title,
                        claim_a=a.claim_id,
                        claim_b=b.claim_id,
                        collision_type=_collision_type(a.label, b.label),
                        detected_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        detected_in_phase=current_phase_dir.split("-")[0],
                        status="unresolved",
                        blocks=[current_phase_dir],
                    )
                )

    return detected


def _next_con_number(existing: list[ContradictionEntry]) -> int:
    nums = [
        int(e.con_id[4:])
        for e in existing
        if re.match(r"^CON-\d+$", e.con_id)
    ]
    return (max(nums) + 1) if nums else 1


# ── register writing ───────────────────────────────────────────────────────


def _write_new_contradictions(
    register_path: Path,
    new_entries: list[ContradictionEntry],
    harness_version: str = "0.1.0",
) -> None:
    """Append new CON-NNN blocks to _contradictions.md (create if absent)."""
    if not new_entries:
        return

    if not register_path.exists():
        phase_updated = new_entries[0].detected_in_phase if new_entries else "00"
        header = (
            "# Contradictions Register\n\n"
            "```yaml\n"
            "---\n"
            f"register: contradictions\n"
            f"phase_updated: \"{phase_updated}\"\n"
            f"harness_version: \"{harness_version}\"\n"
            "---\n"
            "```\n\n"
        )
        register_path.write_text(header, encoding="utf-8")

    lines: list[str] = []
    for e in new_entries:
        blocks_yaml = (
            "[]"
            if not e.blocks
            else "[" + ", ".join(f'"{b}"' for b in e.blocks) + "]"
        )
        lines.append("```yaml")
        lines.append("---")
        lines.append(f"id: {e.con_id}")
        lines.append(f"title: \"{e.title}\"")
        lines.append(f"claim_a: {e.claim_a}")
        lines.append(f"claim_b: {e.claim_b}")
        lines.append(f"collision_type: {e.collision_type}")
        lines.append(f"detected_at: \"{e.detected_at}\"")
        lines.append(f"detected_in_phase: \"{e.detected_in_phase}\"")
        lines.append(f"Status: {e.status}")
        lines.append(f"Blocks: {blocks_yaml}")
        lines.append("resolution_path: null")
        lines.append("resolution_ref: null")
        lines.append("resolved_at: null")
        lines.append("---")
        lines.append("```")
        lines.append("")

    with register_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ── blocking check ─────────────────────────────────────────────────────────


def _blocking_entries(
    entries: list[ContradictionEntry],
    phase_dir: str,
) -> list[ContradictionEntry]:
    """Return unresolved entries whose Blocks list includes phase_dir."""
    result: list[ContradictionEntry] = []
    for e in entries:
        if e.status != "unresolved":
            continue
        if phase_dir in e.blocks:
            result.append(e)
    return result


# ── resolution helpers ─────────────────────────────────────────────────────


def resolve_contradiction(
    register_path: Path,
    con_id: str,
    path: str,
    ref: str,
) -> bool:
    """Mark an existing contradiction as resolved (in-place rewrite of the block).

    path — one of 'a', 'b', 'c', 'd'
    ref  — the artifact id that closes this (e.g. 'DEC-004', 'ASM-007', claim-id)

    Returns True on success, False if con_id not found.
    """
    if not register_path.exists():
        return False

    text = register_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    new_status = f"resolved-by-{path}-{ref}"
    resolved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    in_fence = False
    in_target_block = False
    found = False
    out: list[str] = []

    for raw in lines:
        s = raw.strip()

        if s == "```yaml" and not in_fence:
            in_fence = True
            in_target_block = False
            out.append(raw)
            continue

        if s == "```" and in_fence:
            in_fence = False
            in_target_block = False
            out.append(raw)
            continue

        if not in_fence:
            out.append(raw)
            continue

        if s == f"id: {con_id}":
            in_target_block = True
            found = True
            out.append(raw)
            continue

        if in_target_block:
            if s.startswith("Status:"):
                out.append(f"Status: {new_status}\n")
                continue
            if s.startswith("Blocks:"):
                out.append("Blocks: []\n")
                continue
            if s.startswith("resolution_path:"):
                out.append(f"resolution_path: {path}\n")
                continue
            if s.startswith("resolution_ref:"):
                out.append(f"resolution_ref: {ref}\n")
                continue
            if s.startswith("resolved_at:"):
                out.append(f'resolved_at: "{resolved_at}"\n')
                continue
            if s == "---":
                in_target_block = False

        out.append(raw)

    if found:
        register_path.write_text("".join(out), encoding="utf-8")
    return found


# ── main public API ────────────────────────────────────────────────────────


def run_check_contradictions(
    repo: Path,
    phase_idx: int | None = None,
    write_new: bool = True,
) -> ContradictionResult:
    """Run contradiction detection and blocking check.

    Args:
        repo:       Engagement repo root.
        phase_idx:  Index into _PHASE_DIRS for the phase to check blocking for.
                    If None, auto-detected from ratified artifacts.
        write_new:  If True, append newly detected contradictions to
                    _contradictions.md.

    Returns:
        ContradictionResult with .detected, .blocking, .existing fields.
    """
    result = ContradictionResult()

    register_path = repo / "_contradictions.md"
    existing = _parse_contradictions_register(register_path)
    result.existing = existing

    # Auto-detect current phase if not provided
    if phase_idx is None:
        from harness.decay_check import _detect_current_phase
        phase_idx = _detect_current_phase(repo)

    if phase_idx < len(_PHASE_DIRS):
        current_phase_dir = _PHASE_DIRS[phase_idx]
    else:
        current_phase_dir = _PHASE_DIRS[-1]

    # Collect all in-scope artifacts (ratified) + current phase drafts
    artifacts: list[Path] = list(_find_ratified_artifacts(repo))
    phase_path = repo / current_phase_dir
    if phase_path.is_dir():
        for md in sorted(phase_path.glob("*.md")):
            if md not in artifacts and not md.name.startswith("_"):
                text = md.read_text(encoding="utf-8")
                if _frontmatter_value(text, "status") == "draft":
                    artifacts.append(md)

    atoms = _extract_claim_atoms(artifacts)

    # Detect new contradictions
    new = _detect_new_contradictions(atoms, existing, current_phase_dir)
    result.detected = new

    if write_new and new:
        _write_new_contradictions(register_path, new)
        existing = _parse_contradictions_register(register_path)
        result.existing = existing

    # Check blocking
    result.blocking = _blocking_entries(result.existing, current_phase_dir)

    return result


# ── CLI ────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check contradictions and block synthesis if unresolved."
    )
    parser.add_argument("repo", help="Path to engagement repo root")
    parser.add_argument(
        "--phase",
        metavar="NN",
        help="Phase number or directory name (e.g. '01' or '01-situation'). "
             "Defaults to auto-detection.",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Detect but do not write new contradictions to the register.",
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    if not repo.is_dir():
        print(f"error: repo not found: {repo}", file=sys.stderr)
        return 2

    phase_idx: int | None = None
    if args.phase:
        spec = args.phase.strip()
        # Accept '01' or '01-situation'
        for i, pd in enumerate(_PHASE_DIRS):
            if spec == str(i).zfill(2) or spec == pd or pd.startswith(spec + "-"):
                phase_idx = i
                break
        if phase_idx is None:
            print(f"error: unknown phase: {spec!r}", file=sys.stderr)
            return 2

    result = run_check_contradictions(
        repo,
        phase_idx=phase_idx,
        write_new=not args.no_write,
    )

    if result.detected:
        print(f"DETECTED {len(result.detected)} new contradiction(s):")
        for e in result.detected:
            print(f"  {e.con_id}: {e.title}")

    if result.blocking:
        print(f"\nBLOCKING — {len(result.blocking)} unresolved contradiction(s) block synthesis:")
        for e in result.blocking:
            print(f"  {e.con_id} [{e.collision_type}]: {e.title}")
            print(f"    claim_a={e.claim_a}  claim_b={e.claim_b}")
        return 1

    print("OK — no unresolved contradictions blocking this phase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
