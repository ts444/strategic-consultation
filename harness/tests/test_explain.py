"""Tests for harness/explain.py."""

from __future__ import annotations

from pathlib import Path

from harness.explain import (
    _all_ids,
    _build_index,
    _build_tree,
    _collect_claims,
    _load_decisions,
    _parse_decisions_text,
    explain_claim,
    format_result,
    main,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FM = """\
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


def _make_artifact(phase_dir: Path, name: str, body: str) -> Path:
    fm = _FM.format(phase=phase_dir.name)
    path = phase_dir / name
    path.write_text(fm + "\n" + body, encoding="utf-8")
    return path


def _claim_block(claim_id: str, label: str, source: str, conf: str = "M") -> str:
    """Return a ```yaml block containing a single claim atom."""
    return (
        "```yaml\n"
        "---\n"
        f"id: {claim_id}\n"
        f'claim_line: "[{label}] [source:{source}] [conf:{conf}]"\n'
        "---\n"
        "```\n"
    )


def _make_standard_repo(tmp_path: Path) -> Path:
    """
    Repo structure used by most tests:
      01-situation/situation.md
        SIT-001 [known] portfolio://infra/server.md@abc123 conf:H
        SIT-002 [elicited] interview:2026-03-15/consultant conf:L
      02-gap/gaps.md
        GAP-001 [inferred] from: SIT-001 + SIT-002 conf:M
      03-mapping/recommendations.md
        REC-001 [inferred] from: GAP-001 + SIT-001 conf:M
    """
    repo = _make_repo(tmp_path)

    sit_body = (
        _claim_block("SIT-001", "known", "portfolio://infra/server.md@abc123", "H")
        + _claim_block("SIT-002", "elicited", "interview:2026-03-15/consultant", "L")
    )
    _make_artifact(repo / "01-situation", "situation.md", sit_body)

    gap_body = _claim_block("GAP-001", "inferred", "from: SIT-001 + SIT-002", "M")
    _make_artifact(repo / "02-gap", "gaps.md", gap_body)

    rec_body = _claim_block("REC-001", "inferred", "from: GAP-001 + SIT-001", "M")
    _make_artifact(repo / "03-mapping", "recommendations.md", rec_body)

    return repo


# ---------------------------------------------------------------------------
# _collect_claims + _build_index
# ---------------------------------------------------------------------------


def test_collect_claims_finds_all(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    ids = {c.claim_id for c in claims}
    assert {"SIT-001", "SIT-002", "GAP-001", "REC-001"}.issubset(ids)


def test_collect_claims_skips_register_files(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    register = repo / "01-situation" / "_trace.md"
    register.write_text(
        _FM.format(phase="01-situation")
        + "\n"
        + _claim_block("REG-001", "known", "portfolio://x.md@abc"),
        encoding="utf-8",
    )
    claims = _collect_claims(repo)
    assert not any(c.claim_id == "REG-001" for c in claims)


def test_build_index_first_wins(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    assert "SIT-001" in index
    assert index["SIT-001"].label == "known"


# ---------------------------------------------------------------------------
# _build_tree leaf nodes
# ---------------------------------------------------------------------------


def test_leaf_known_claim(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("SIT-001", index)
    assert node.claim.claim_id == "SIT-001"
    assert node.claim.label == "known"
    assert node.children == []
    assert not node.missing
    assert not node.is_cycle


def test_leaf_elicited_claim(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("SIT-002", index)
    assert node.claim.label == "elicited"
    assert node.children == []


def test_missing_claim_returns_missing_node(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("MISS-999", index)
    assert node.missing
    assert node.claim.claim_id == "MISS-999"
    assert node.children == []


# ---------------------------------------------------------------------------
# _build_tree composed nodes
# ---------------------------------------------------------------------------


def test_composed_one_level(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("GAP-001", index)
    assert node.claim.claim_id == "GAP-001"
    child_ids = {c.claim.claim_id for c in node.children}
    assert child_ids == {"SIT-001", "SIT-002"}


def test_composed_two_levels(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("REC-001", index)
    assert node.claim.claim_id == "REC-001"
    child_ids = {c.claim.claim_id for c in node.children}
    assert child_ids == {"GAP-001", "SIT-001"}
    gap_node = next(c for c in node.children if c.claim.claim_id == "GAP-001")
    grandchild_ids = {gc.claim.claim_id for gc in gap_node.children}
    assert grandchild_ids == {"SIT-001", "SIT-002"}


def test_diamond_dag_no_cycle(tmp_path: Path) -> None:
    # SIT-001 appears under both GAP-001 and directly under REC-001 — this is
    # a DAG diamond, not a cycle.  Both occurrences should be leaf nodes.
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    root = _build_tree("REC-001", index)
    # Both SIT-001 occurrences must be leaves (not cycle nodes)
    sit_nodes = [c for c in root.children if c.claim.claim_id == "SIT-001"]
    assert len(sit_nodes) == 1
    assert not sit_nodes[0].is_cycle
    # Also check the one under GAP-001
    gap_node = next(c for c in root.children if c.claim.claim_id == "GAP-001")
    sit_under_gap = [c for c in gap_node.children if c.claim.claim_id == "SIT-001"]
    assert len(sit_under_gap) == 1
    assert not sit_under_gap[0].is_cycle


def test_cycle_detection(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    circ_body = (
        _claim_block("CIRC-001", "inferred", "from: CIRC-002", "M")
        + _claim_block("CIRC-002", "inferred", "from: CIRC-001", "M")
    )
    _make_artifact(repo / "02-gap", "circ.md", circ_body)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    root = _build_tree("CIRC-001", index)
    assert root.claim.claim_id == "CIRC-001"
    assert len(root.children) == 1
    child = root.children[0]
    assert child.claim.claim_id == "CIRC-002"
    assert len(child.children) == 1
    cycle_node = child.children[0]
    assert cycle_node.is_cycle
    assert cycle_node.claim.claim_id == "CIRC-001"


# ---------------------------------------------------------------------------
# _all_ids
# ---------------------------------------------------------------------------


def test_all_ids_leaf(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("SIT-001", index)
    assert _all_ids(node) == {"SIT-001"}


def test_all_ids_composed(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    claims = _collect_claims(repo)
    index = _build_index(claims)
    node = _build_tree("REC-001", index)
    ids = _all_ids(node)
    assert {"REC-001", "GAP-001", "SIT-001", "SIT-002"}.issubset(ids)


# ---------------------------------------------------------------------------
# explain_claim (public API)
# ---------------------------------------------------------------------------


def test_explain_claim_returns_none_for_unknown(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    assert explain_claim(repo, "MISS-999") is None


def test_explain_claim_leaf(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    result = explain_claim(repo, "SIT-001")
    assert result is not None
    assert result.root.claim.claim_id == "SIT-001"
    assert result.root.children == []
    assert result.chain_ids == {"SIT-001"}


def test_explain_claim_composed(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    result = explain_claim(repo, "GAP-001")
    assert result is not None
    assert result.root.claim.claim_id == "GAP-001"
    assert {"GAP-001", "SIT-001", "SIT-002"} == result.chain_ids


# ---------------------------------------------------------------------------
# Decisions parsing
# ---------------------------------------------------------------------------


def test_parse_decisions_empty() -> None:
    decs = _parse_decisions_text("", Path("_decisions.md"))
    assert decs == []


def test_parse_decisions_single_override() -> None:
    text = (
        "```yaml\n"
        "---\n"
        "id: DEC-001\n"
        "title: Use interview date\n"
        "overrides: SIT-001\n"
        "---\n"
        "```\n"
    )
    decs = _parse_decisions_text(text, Path("_decisions.md"))
    assert len(decs) == 1
    assert decs[0].dec_id == "DEC-001"
    assert decs[0].title == "Use interview date"
    assert decs[0].overrides == ["SIT-001"]


def test_parse_decisions_list_overrides() -> None:
    text = (
        "```yaml\n"
        "---\n"
        "id: DEC-002\n"
        "title: Consolidate sources\n"
        "overrides:\n"
        "  - SIT-001\n"
        "  - SIT-002\n"
        "---\n"
        "```\n"
    )
    decs = _parse_decisions_text(text, Path("_decisions.md"))
    assert len(decs) == 1
    assert set(decs[0].overrides) == {"SIT-001", "SIT-002"}


def test_decisions_surfaced_in_chain(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    dec_text = (
        "```yaml\n"
        "---\n"
        "id: DEC-001\n"
        "title: Accept interview date\n"
        "overrides: SIT-001\n"
        "---\n"
        "```\n"
    )
    (repo / "_decisions.md").write_text(dec_text, encoding="utf-8")
    result = explain_claim(repo, "REC-001")
    assert result is not None
    assert len(result.decisions) == 1
    assert result.decisions[0].dec_id == "DEC-001"


def test_decisions_not_in_chain_excluded(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    dec_text = (
        "```yaml\n"
        "---\n"
        "id: DEC-099\n"
        "title: Unrelated\n"
        "overrides: UNRELATED-999\n"
        "---\n"
        "```\n"
    )
    (repo / "_decisions.md").write_text(dec_text, encoding="utf-8")
    result = explain_claim(repo, "REC-001")
    assert result is not None
    assert result.decisions == []


def test_load_decisions_no_file(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    assert _load_decisions(repo) == []


# ---------------------------------------------------------------------------
# format_result rendering
# ---------------------------------------------------------------------------


def test_format_result_leaf(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    result = explain_claim(repo, "SIT-001")
    assert result is not None
    out = format_result(result)
    assert "SIT-001" in out
    assert "[known]" in out
    assert "conf:H" in out
    assert "portfolio://infra/server.md@abc123" in out


def test_format_result_composed_shows_children(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    result = explain_claim(repo, "GAP-001")
    assert result is not None
    out = format_result(result)
    assert "GAP-001" in out
    assert "SIT-001" in out
    assert "SIT-002" in out
    # Children should be indented relative to parent
    lines = out.splitlines()
    gap_line = next(ln for ln in lines if "GAP-001" in ln)
    sit_line = next(ln for ln in lines if "SIT-001" in ln)
    assert len(sit_line) - len(sit_line.lstrip()) > len(gap_line) - len(gap_line.lstrip())


def test_format_result_includes_decisions(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    dec_text = (
        "```yaml\n"
        "---\n"
        "id: DEC-001\n"
        "title: Accept interview date\n"
        "overrides: SIT-001\n"
        "---\n"
        "```\n"
    )
    (repo / "_decisions.md").write_text(dec_text, encoding="utf-8")
    result = explain_claim(repo, "SIT-001")
    assert result is not None
    out = format_result(result)
    assert "Decisions overriding claims in this chain:" in out
    assert "DEC-001" in out
    assert "SIT-001" in out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_bad_repo(tmp_path: Path) -> None:
    rc = main([str(tmp_path / "nonexistent"), "GAP-001"])
    assert rc == 1


def test_cli_missing_claim(tmp_path: Path) -> None:
    repo = _make_standard_repo(tmp_path)
    rc = main([str(repo), "MISS-999"])
    assert rc == 1


def test_cli_success(tmp_path: Path, capsys: object) -> None:
    repo = _make_standard_repo(tmp_path)
    rc = main([str(repo), "GAP-001"])
    assert rc == 0
