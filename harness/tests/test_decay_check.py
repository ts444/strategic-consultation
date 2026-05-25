"""Tests for harness/decay_check.py."""

from __future__ import annotations

import json
from pathlib import Path

from harness.decay_check import (
    DecayResult,
    _detect_current_phase,
    _extract_claims,
    run_decay_check,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONTMATTER = """\
---
phase: "{phase}"
status: ratified
harness_version: "0.1.0"
template: "scope@1.0.0"
produced_by: portfolio-retriever
---
"""


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "engagement"
    repo.mkdir()
    for d in ["00-intake", "01-situation", "02-gap", "03-mapping"]:
        (repo / d).mkdir()
    return repo


def _make_artifact(phase_dir: Path, name: str, body: str, phase_key: str = "") -> Path:
    if not phase_key:
        # derive from dir name
        phase_key = phase_dir.name
    frontmatter = _FRONTMATTER.format(phase=phase_key)
    path = phase_dir / name
    path.write_text(frontmatter + "\n" + body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# _detect_current_phase
# ---------------------------------------------------------------------------


def test_detect_current_phase_no_ratified(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    # No ratified artifacts → current phase = 0
    assert _detect_current_phase(repo) == 0


def test_detect_current_phase_one_ratified(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(repo / "00-intake", "scope.md", "body")
    # Phase 0 ratified → current = 1
    assert _detect_current_phase(repo) == 1


def test_detect_current_phase_two_ratified(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(repo / "00-intake", "scope.md", "body")
    _make_artifact(repo / "01-situation", "situation.md", "body", "01-situation")
    # Phase 1 ratified → current = 2
    assert _detect_current_phase(repo) == 2


# ---------------------------------------------------------------------------
# _extract_claims
# ---------------------------------------------------------------------------


def test_extract_claim_from_prose(tmp_path: Path) -> None:
    artifact = tmp_path / "scope.md"
    artifact.write_text(
        _FRONTMATTER.format(phase="00-intake")
        + "\n[known] [source:portfolio://Governance/fw.md@abc123] [conf:H] text.\n",
        encoding="utf-8",
    )
    claims = _extract_claims(artifact)
    assert len(claims) == 1
    c = claims[0]
    assert c.label == "known"
    assert c.source == "portfolio://Governance/fw.md@abc123"
    assert c.conf == "H"


def test_extract_claim_id_from_yaml_block(tmp_path: Path) -> None:
    body = """\
```yaml
---
id: GAP-001
evidence: "[known] [source:portfolio://Gov/fw.md@sha1] [conf:M] finding."
---
```
"""
    artifact = tmp_path / "gaps.md"
    artifact.write_text(
        _FRONTMATTER.format(phase="02-gap") + "\n" + body, encoding="utf-8"
    )
    claims = _extract_claims(artifact)
    assert len(claims) == 1
    assert claims[0].claim_id == "GAP-001"


def test_extract_composed_claim(tmp_path: Path) -> None:
    artifact = tmp_path / "gaps.md"
    artifact.write_text(
        _FRONTMATTER.format(phase="02-gap")
        + "\n[inferred] [source:from: SIT-001 + GAP-001] [conf:M] derived.\n",
        encoding="utf-8",
    )
    claims = _extract_claims(artifact)
    assert len(claims) == 1
    assert claims[0].composed_from == ["SIT-001", "GAP-001"]


def test_extract_elicited_claim(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    artifact = phase_dir / "scope.md"
    artifact.write_text(
        _FRONTMATTER.format(phase="00-intake")
        + "\n[elicited] [source:interview:2026-05-25/consultant] [conf:L] elicited fact.\n",
        encoding="utf-8",
    )
    claims = _extract_claims(artifact)
    assert len(claims) == 1
    assert claims[0].label == "elicited"
    assert claims[0].conf == "L"
    assert claims[0].phase_idx == 0


# ---------------------------------------------------------------------------
# [known] decay — HARD STALE
# ---------------------------------------------------------------------------


def test_known_stale_portfolio(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Governance/fw.md@old-ref] [conf:H] text.\n",
    )
    result = run_decay_check(
        repo,
        current_phase=1,
        head_portfolio=lambda _name: "new-ref",
    )
    assert len(result.hard_stale) == 1
    assert "old-ref" in result.hard_stale[0].reason
    assert "new-ref" in result.hard_stale[0].reason


def test_known_stale_customer(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:customer-portal://assets/org-apex@2024-01-01] [conf:H] text.\n",
    )
    result = run_decay_check(
        repo,
        current_phase=1,
        head_customer=lambda _rtype, _id: "2024-06-01",
    )
    assert len(result.hard_stale) == 1
    assert "2024-01-01" in result.hard_stale[0].reason


def test_known_fresh_portfolio_no_stale(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Governance/fw.md@abc123] [conf:H] text.\n",
    )
    result = run_decay_check(
        repo,
        current_phase=1,
        head_portfolio=lambda _name: "abc123",
    )
    assert result.hard_stale == []


def test_known_fresh_writes_trace(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Governance/fw.md@abc123] [conf:H] text.\n",
    )
    trace_path = tmp_path / "trace.jsonl"
    run_decay_check(
        repo,
        current_phase=1,
        head_portfolio=lambda _name: "abc123",
        trace_path=trace_path,
    )
    assert trace_path.exists()
    lines = [json.loads(ln) for ln in trace_path.read_text().splitlines() if ln.strip()]
    assert any(ln["status"] == "unchanged" for ln in lines)


def test_known_no_head_fn_skips_check(tmp_path: Path) -> None:
    """Without a head function, [known] claims are not flagged (MCP unavailable)."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Governance/fw.md@abc123] [conf:H] text.\n",
    )
    result = run_decay_check(repo, current_phase=1)
    assert result.hard_stale == []


# ---------------------------------------------------------------------------
# [elicited] decay
# ---------------------------------------------------------------------------


def test_elicited_stale_low_conf(tmp_path: Path) -> None:
    """L conf: stale after distance >= 1."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:L] fact.\n",
    )
    result = run_decay_check(repo, current_phase=1)  # distance = 1, threshold = 1
    assert len(result.elicited_due) == 1
    assert "threshold=1" in result.elicited_due[0].reason


def test_elicited_not_stale_same_phase(tmp_path: Path) -> None:
    """Claim in phase 0, current_phase=0: distance=0 < threshold=1 → not stale."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:L] fact.\n",
    )
    result = run_decay_check(repo, current_phase=0)
    assert result.elicited_due == []


def test_elicited_stale_medium_conf(tmp_path: Path) -> None:
    """M conf: stale after distance >= 2."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:M] fact.\n",
    )
    result = run_decay_check(repo, current_phase=2)  # distance=2, threshold=2
    assert len(result.elicited_due) == 1


def test_elicited_not_stale_high_conf(tmp_path: Path) -> None:
    """H conf: threshold=3; distance=2 is still fresh."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:H] fact.\n",
    )
    result = run_decay_check(repo, current_phase=2)  # distance=2, threshold=3
    assert result.elicited_due == []


def test_custom_elicited_thresholds(tmp_path: Path) -> None:
    """Custom thresholds override defaults."""
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:H] fact.\n",
    )
    # Override H threshold to 1: distance=1 should now flag it
    result = run_decay_check(
        repo,
        current_phase=1,
        elicited_thresholds={"H": 1, "M": 2, "L": 1},
    )
    assert len(result.elicited_due) == 1


# ---------------------------------------------------------------------------
# [assumed] decay — ASSUMPTIONS FLAGGED
# ---------------------------------------------------------------------------

_ASM_BLOCK = """\
```yaml
---
id: ASM-001
statement: "Customer has no supplier register"
requires_revalidation: true
phase_expires: "01"
---
```
"""


def test_assumptions_flagged_past_phase_expires(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    assumptions_file = repo / "_assumptions.md"
    assumptions_file.write_text(
        "---\nregister: assumptions\nharness_version: 0.1.0\ncustomer: test\n---\n\n"
        + _ASM_BLOCK,
        encoding="utf-8",
    )
    # current_phase=2 > phase_expires=1 → flagged
    result = run_decay_check(repo, current_phase=2)
    assert len(result.assumptions_flagged) == 1
    assert result.assumptions_flagged[0].claim_id == "ASM-001"


def test_assumptions_not_flagged_before_expires(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    assumptions_file = repo / "_assumptions.md"
    assumptions_file.write_text(
        "---\nregister: assumptions\nharness_version: 0.1.0\ncustomer: test\n---\n\n"
        + _ASM_BLOCK,
        encoding="utf-8",
    )
    # current_phase=1 == phase_expires=1 → NOT flagged (must be strictly greater)
    result = run_decay_check(repo, current_phase=1)
    assert result.assumptions_flagged == []


def test_assumptions_flagged_never_phase_expires(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    asm_never = """\
```yaml
---
id: ASM-002
requires_revalidation: true
phase_expires: "never"
---
```
"""
    (repo / "_assumptions.md").write_text(
        "---\nregister: assumptions\n---\n\n" + asm_never, encoding="utf-8"
    )
    result = run_decay_check(repo, current_phase=5)
    assert result.assumptions_flagged == []


def test_assumptions_flagged_requires_revalidation_false(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    asm_no_reval = """\
```yaml
---
id: ASM-003
requires_revalidation: false
phase_expires: "01"
---
```
"""
    (repo / "_assumptions.md").write_text(
        "---\nregister: assumptions\n---\n\n" + asm_no_reval, encoding="utf-8"
    )
    result = run_decay_check(repo, current_phase=5)
    assert result.assumptions_flagged == []


def test_assumptions_no_file_returns_empty(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    result = run_decay_check(repo, current_phase=2)
    assert result.assumptions_flagged == []


# ---------------------------------------------------------------------------
# DOWNSTREAM IMPACT
# ---------------------------------------------------------------------------


def test_downstream_impact_inferred_from_stale_known(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)

    # Phase-0 artifact with a [known] claim under block id SIT-001 that is stale
    body_scope = """\
```yaml
---
id: SIT-001
evidence: "[known] [source:portfolio://Governance/fw.md@old-ref] [conf:H] text"
---
```
"""
    _make_artifact(repo / "00-intake", "scope.md", body_scope)

    # Phase-2 artifact with an [inferred] claim composed from SIT-001
    body_gaps = "[inferred] [source:from: SIT-001] [conf:M] derived finding.\n"
    _make_artifact(repo / "02-gap", "gaps.md", body_gaps, "02-gap")

    result = run_decay_check(
        repo,
        current_phase=3,
        head_portfolio=lambda _name: "new-ref",
    )
    assert len(result.hard_stale) == 1
    assert result.hard_stale[0].claim_id == "SIT-001"
    assert len(result.downstream_impact) == 1
    assert "SIT-001" in result.downstream_impact[0].reason


def test_downstream_impact_not_triggered_when_source_fresh(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    body_scope = """\
```yaml
---
id: SIT-001
evidence: "[known] [source:portfolio://Governance/fw.md@same-ref] [conf:H] text"
---
```
"""
    _make_artifact(repo / "00-intake", "scope.md", body_scope)
    body_gaps = "[inferred] [source:from: SIT-001] [conf:M] derived finding.\n"
    _make_artifact(repo / "02-gap", "gaps.md", body_gaps, "02-gap")

    result = run_decay_check(
        repo,
        current_phase=3,
        head_portfolio=lambda _name: "same-ref",
    )
    assert result.hard_stale == []
    assert result.downstream_impact == []


def test_downstream_impact_multiple_inputs_one_stale(tmp_path: Path) -> None:
    """Downstream fires even if only one of the composed inputs is stale."""
    repo = _make_repo(tmp_path)

    # SIT-001: known, stale; SIT-002: elicited (not directly stale in this check)
    body_scope = (
        "```yaml\n---\nid: SIT-001\n"
        'evidence: "[known] [source:portfolio://G/fw.md@old] [conf:H] text"\n---\n```\n'
    )
    _make_artifact(repo / "00-intake", "scope.md", body_scope)

    body_gaps = "[inferred] [source:from: SIT-001 + SIT-002] [conf:L] derived.\n"
    _make_artifact(repo / "02-gap", "gaps.md", body_gaps, "02-gap")

    result = run_decay_check(
        repo,
        current_phase=3,
        head_portfolio=lambda _name: "new",
    )
    assert len(result.downstream_impact) == 1
    assert "SIT-001" in result.downstream_impact[0].reason


# ---------------------------------------------------------------------------
# Integration: all fresh
# ---------------------------------------------------------------------------


def test_all_fresh_returns_clean(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Governance/fw.md@same] [conf:H] text.\n",
    )
    result = run_decay_check(
        repo,
        current_phase=1,
        head_portfolio=lambda _name: "same",
    )
    assert result == DecayResult()


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------


def test_main_returns_zero_on_clean(tmp_path: Path) -> None:
    from harness.decay_check import main

    repo = _make_repo(tmp_path)
    _make_artifact(repo / "00-intake", "scope.md", "No claims here.\n")
    ret = main([str(repo), "--current-phase", "1"])
    assert ret == 0


def test_main_returns_nonzero_on_stale(tmp_path: Path) -> None:
    """CLI exits non-zero when there are stale claims."""
    from harness.decay_check import main

    repo = _make_repo(tmp_path)
    _make_artifact(
        repo / "00-intake",
        "scope.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:L] fact.\n",
    )
    # distance=2 >= threshold=1 for L → stale
    ret = main([str(repo), "--current-phase", "2"])
    assert ret == 1


def test_main_missing_dir_returns_one(tmp_path: Path) -> None:
    from harness.decay_check import main

    ret = main([str(tmp_path / "nonexistent"), "--current-phase", "1"])
    assert ret == 1
