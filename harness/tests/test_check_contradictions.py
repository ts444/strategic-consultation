"""Tests for harness/check_contradictions.py."""

from __future__ import annotations

from pathlib import Path

from harness.check_contradictions import (
    ClaimAtom,
    ContradictionEntry,
    _blocking_entries,
    _collision_type,
    _detect_new_contradictions,
    _extract_claim_atoms,
    _has_negation,
    _key_words,
    _next_con_number,
    _parse_contradictions_register,
    _subject_overlap,
    _write_new_contradictions,
    resolve_contradiction,
    run_check_contradictions,
)

# ── helpers ────────────────────────────────────────────────────────────────

_FM = """\
---
phase: "{phase}"
status: ratified
harness_version: "0.1.0"
template: "scope@1.0.0"
produced_by: portfolio-retriever
---
"""

_FM_DRAFT = """\
---
phase: "{phase}"
status: draft
harness_version: "0.1.0"
template: "scope@1.0.0"
produced_by: synthesizer
---
"""


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "engagement"
    repo.mkdir()
    for d in ["00-intake", "01-situation", "02-gap"]:
        (repo / d).mkdir()
    return repo


def _artifact(phase_dir: Path, name: str, body: str, draft: bool = False) -> Path:
    phase_key = phase_dir.name
    fm = (_FM_DRAFT if draft else _FM).format(phase=phase_key)
    p = phase_dir / name
    p.write_text(fm + "\n" + body, encoding="utf-8")
    return p


def _con_entry(
    con_id: str = "CON-001",
    status: str = "unresolved",
    blocks: list[str] | None = None,
    claim_a: str = "SIT-001",
    claim_b: str = "SIT-002",
    collision_type: str = "hard<->hard",
) -> ContradictionEntry:
    return ContradictionEntry(
        con_id=con_id,
        title="test conflict",
        claim_a=claim_a,
        claim_b=claim_b,
        collision_type=collision_type,
        detected_at="2026-05-25T10:00:00Z",
        detected_in_phase="01",
        status=status,
        blocks=blocks if blocks is not None else ["01-situation"],
    )


# ── _key_words ─────────────────────────────────────────────────────────────


def test_key_words_basic() -> None:
    assert _key_words("The firewall version is current.") == ["firewall", "version", "current"]


def test_key_words_skips_stopwords() -> None:
    words = _key_words("It is on the network.")
    assert "it" not in words
    assert "is" not in words
    assert "the" not in words
    assert "network" in words


def test_key_words_skips_negation_words() -> None:
    words = _key_words("Firewall is not patched.")
    assert "not" not in words
    assert "firewall" in words


# ── _has_negation ──────────────────────────────────────────────────────────


def test_has_negation_with_not() -> None:
    assert _has_negation("The firewall is not patched.")


def test_has_negation_with_no() -> None:
    assert _has_negation("No backup policy exists.")


def test_has_negation_false() -> None:
    assert not _has_negation("The firewall is patched and current.")


# ── _subject_overlap ───────────────────────────────────────────────────────


def test_subject_overlap_two_shared() -> None:
    a = ["firewall", "version", "current"]
    b = ["firewall", "version", "outdated"]
    assert _subject_overlap(a, b) == 2


def test_subject_overlap_none() -> None:
    assert _subject_overlap(["network", "switch"], ["firewall", "version"]) == 0


def test_subject_overlap_one() -> None:
    assert _subject_overlap(["firewall", "policy"], ["firewall", "version"]) == 1


# ── _collision_type ────────────────────────────────────────────────────────


def test_collision_hard_hard() -> None:
    assert _collision_type("known", "elicited") == "hard<->hard"
    assert _collision_type("known", "known") == "hard<->hard"
    assert _collision_type("elicited", "elicited") == "hard<->hard"


def test_collision_hard_soft() -> None:
    assert _collision_type("known", "inferred") == "hard<->soft"
    assert _collision_type("elicited", "assumed") == "hard<->soft"
    assert _collision_type("inferred", "known") == "hard<->soft"


def test_collision_soft_soft() -> None:
    assert _collision_type("inferred", "assumed") == "soft<->soft"
    assert _collision_type("assumed", "assumed") == "soft<->soft"


# ── _parse_contradictions_register ────────────────────────────────────────


def test_parse_empty_register(tmp_path: Path) -> None:
    path = tmp_path / "_contradictions.md"
    assert _parse_contradictions_register(path) == []


def test_parse_single_unresolved_entry(tmp_path: Path) -> None:
    path = tmp_path / "_contradictions.md"
    path.write_text(
        "# Contradictions Register\n\n"
        "```yaml\n"
        "---\n"
        "id: CON-001\n"
        'title: "Firewall version conflict"\n'
        "claim_a: SIT-008\n"
        "claim_b: SIT-015\n"
        "collision_type: hard<->soft\n"
        'detected_at: "2026-05-26T10:00:00Z"\n'
        'detected_in_phase: "01"\n'
        "Status: unresolved\n"
        'Blocks: ["01-situation"]\n'
        "resolution_path: null\n"
        "resolution_ref: null\n"
        "resolved_at: null\n"
        "---\n"
        "```\n",
        encoding="utf-8",
    )
    entries = _parse_contradictions_register(path)
    assert len(entries) == 1
    e = entries[0]
    assert e.con_id == "CON-001"
    assert e.status == "unresolved"
    assert e.blocks == ["01-situation"]
    assert e.claim_a == "SIT-008"
    assert e.claim_b == "SIT-015"
    assert e.collision_type == "hard<->soft"
    assert e.resolution_path is None


def test_parse_resolved_entry(tmp_path: Path) -> None:
    path = tmp_path / "_contradictions.md"
    path.write_text(
        "```yaml\n"
        "---\n"
        "id: CON-002\n"
        'title: "Conflict resolved by decision"\n'
        "claim_a: SIT-001\n"
        "claim_b: SIT-002\n"
        "collision_type: hard<->hard\n"
        'detected_at: "2026-05-26T10:00:00Z"\n'
        'detected_in_phase: "01"\n'
        "Status: resolved-by-d-DEC-004\n"
        "Blocks: []\n"
        "resolution_path: d\n"
        "resolution_ref: DEC-004\n"
        'resolved_at: "2026-05-26T11:00:00Z"\n'
        "---\n"
        "```\n",
        encoding="utf-8",
    )
    entries = _parse_contradictions_register(path)
    assert len(entries) == 1
    e = entries[0]
    assert e.status == "resolved-by-d-DEC-004"
    assert e.blocks == []
    assert e.resolution_path == "d"
    assert e.resolution_ref == "DEC-004"


def test_parse_multiple_entries(tmp_path: Path) -> None:
    path = tmp_path / "_contradictions.md"
    path.write_text(
        "```yaml\n"
        "---\n"
        "id: CON-001\n"
        'title: "First"\n'
        "claim_a: A\nclaim_b: B\ncollision_type: hard<->hard\n"
        'detected_at: "2026-01-01T00:00:00Z"\n'
        'detected_in_phase: "01"\n'
        "Status: unresolved\nBlocks: [\"01-situation\"]\n"
        "resolution_path: null\nresolution_ref: null\nresolved_at: null\n"
        "---\n"
        "---\n"
        "id: CON-002\n"
        'title: "Second"\n'
        "claim_a: C\nclaim_b: D\ncollision_type: soft<->soft\n"
        'detected_at: "2026-01-02T00:00:00Z"\n'
        'detected_in_phase: "02"\n'
        "Status: unresolved\nBlocks: [\"02-gap\"]\n"
        "resolution_path: null\nresolution_ref: null\nresolved_at: null\n"
        "---\n"
        "```\n",
        encoding="utf-8",
    )
    entries = _parse_contradictions_register(path)
    assert len(entries) == 2
    assert entries[0].con_id == "CON-001"
    assert entries[1].con_id == "CON-002"


# ── _blocking_entries ──────────────────────────────────────────────────────


def test_blocking_entries_match() -> None:
    entries = [_con_entry("CON-001", "unresolved", ["01-situation"])]
    assert len(_blocking_entries(entries, "01-situation")) == 1


def test_blocking_entries_different_phase() -> None:
    entries = [_con_entry("CON-001", "unresolved", ["02-gap"])]
    assert _blocking_entries(entries, "01-situation") == []


def test_blocking_entries_resolved() -> None:
    entries = [_con_entry("CON-001", "resolved-by-d-DEC-001", ["01-situation"])]
    assert _blocking_entries(entries, "01-situation") == []


def test_blocking_entries_empty_blocks() -> None:
    entries = [_con_entry("CON-001", "unresolved", [])]
    assert _blocking_entries(entries, "01-situation") == []


# ── _next_con_number ───────────────────────────────────────────────────────


def test_next_con_number_empty() -> None:
    assert _next_con_number([]) == 1


def test_next_con_number_existing() -> None:
    entries = [_con_entry("CON-003"), _con_entry("CON-001")]
    assert _next_con_number(entries) == 4


# ── _extract_claim_atoms ───────────────────────────────────────────────────


def test_extract_claim_atom_basic(tmp_path: Path) -> None:
    art = tmp_path / "sit.md"
    body = (
        "[known] [source:portfolio://Gov/fw.md@abc] [conf:H]"
        " The firewall firmware is version 2.5.\n"
    )
    art.write_text(_FM.format(phase="01-situation") + "\n" + body, encoding="utf-8")
    atoms = _extract_claim_atoms([art])
    assert len(atoms) == 1
    assert atoms[0].label == "known"
    assert "firewall firmware" in atoms[0].text.lower()
    assert atoms[0].supersedes is None


def test_extract_claim_atom_with_supersedes(tmp_path: Path) -> None:
    art = tmp_path / "sit.md"
    art.write_text(
        _FM.format(phase="01-situation")
        + "\n[elicited] [source:interview:2026-05-25/consultant] [conf:M] "
        "Firewall firmware is not version 2.5. supersedes: SIT-008\n",
        encoding="utf-8",
    )
    atoms = _extract_claim_atoms([art])
    assert len(atoms) == 1
    assert atoms[0].supersedes == "SIT-008"


def test_extract_skips_superseded_pairs(tmp_path: Path) -> None:
    art = tmp_path / "sit.md"
    art.write_text(
        _FM.format(phase="01-situation")
        + "\n[known] [source:portfolio://Gov/fw.md@abc] [conf:H] "
        "The firewall firmware is version 2.5.\n"
        "[elicited] [source:interview:2026-05-25/consultant] [conf:M] "
        "The firewall firmware is not version 2.5. supersedes: line-6\n",
        encoding="utf-8",
    )
    atoms = _extract_claim_atoms([art])
    assert len(atoms) == 2
    # second atom supersedes the first
    superseded_ids = {a.supersedes for a in atoms if a.supersedes}
    assert "line-6" in superseded_ids


# ── _detect_new_contradictions ─────────────────────────────────────────────


def _make_atom(
    claim_id: str,
    label: str,
    text: str,
    artifact: Path | None = None,
    supersedes: str | None = None,
) -> ClaimAtom:
    return ClaimAtom(
        claim_id=claim_id,
        label=label,
        text=text,
        artifact=artifact or Path("/fake/sit.md"),
        lineno=1,
        supersedes=supersedes,
    )


def test_detect_hard_hard_contradiction() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom("SIT-002", "elicited", "Firewall firmware is not version 2.5"),
    ]
    detected = _detect_new_contradictions(atoms, [], "01-situation")
    assert len(detected) == 1
    e = detected[0]
    assert e.con_id == "CON-001"
    assert e.collision_type == "hard<->hard"
    assert e.claim_a == "SIT-001"
    assert e.claim_b == "SIT-002"
    assert e.status == "unresolved"
    assert "01-situation" in e.blocks


def test_detect_hard_soft_contradiction() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Backup policy covers all servers"),
        _make_atom("REC-001", "inferred", "Backup policy does not cover all servers"),
    ]
    detected = _detect_new_contradictions(atoms, [], "02-gap")
    assert len(detected) == 1
    assert detected[0].collision_type == "hard<->soft"


def test_detect_soft_soft_contradiction() -> None:
    atoms = [
        _make_atom("REC-001", "inferred", "Network segmentation is sufficient"),
        _make_atom("REC-002", "assumed", "Network segmentation is not sufficient"),
    ]
    detected = _detect_new_contradictions(atoms, [], "03-mapping")
    assert len(detected) == 1
    assert detected[0].collision_type == "soft<->soft"


def test_detect_no_contradiction_same_polarity() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom("SIT-002", "known", "Firewall firmware is current"),
    ]
    detected = _detect_new_contradictions(atoms, [], "01-situation")
    assert detected == []


def test_detect_no_contradiction_different_subject() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom("SIT-002", "elicited", "Backup system is not configured"),
    ]
    detected = _detect_new_contradictions(atoms, [], "01-situation")
    assert detected == []


def test_detect_skips_already_registered() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom("SIT-002", "elicited", "Firewall firmware is not version 2.5"),
    ]
    existing = [_con_entry("CON-001", claim_a="SIT-001", claim_b="SIT-002")]
    detected = _detect_new_contradictions(atoms, existing, "01-situation")
    assert detected == []


def test_detect_skips_superseded_claims() -> None:
    atoms = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom(
            "SIT-002", "elicited", "Firewall firmware is not version 2.5", supersedes="SIT-001"
        ),
    ]
    detected = _detect_new_contradictions(atoms, [], "01-situation")
    # SIT-001 is superseded → excluded → no contradiction
    assert detected == []


def test_detect_increments_con_id() -> None:
    atoms_1 = [
        _make_atom("SIT-001", "known", "Firewall firmware is version 2.5"),
        _make_atom("SIT-002", "elicited", "Firewall firmware is not version 2.5"),
    ]
    atoms_2 = [
        _make_atom("SIT-003", "known", "Backup policy covers all servers"),
        _make_atom("SIT-004", "elicited", "Backup policy does not cover all servers"),
    ]
    existing = _detect_new_contradictions(atoms_1, [], "01-situation")
    assert existing[0].con_id == "CON-001"
    next_batch = _detect_new_contradictions(atoms_2, existing, "01-situation")
    assert next_batch[0].con_id == "CON-002"


# ── _write_new_contradictions ──────────────────────────────────────────────


def test_write_creates_register(tmp_path: Path) -> None:
    reg = tmp_path / "_contradictions.md"
    entries = [
        ContradictionEntry(
            con_id="CON-001",
            title="Test conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )
    ]
    _write_new_contradictions(reg, entries)
    assert reg.exists()
    text = reg.read_text()
    assert "CON-001" in text
    assert "SIT-001" in text
    assert "Status: unresolved" in text


def test_write_appends_to_existing(tmp_path: Path) -> None:
    reg = tmp_path / "_contradictions.md"
    reg.write_text("# Contradictions Register\n\n", encoding="utf-8")
    entries = [
        ContradictionEntry(
            con_id="CON-002",
            title="Another conflict",
            claim_a="SIT-003",
            claim_b="SIT-004",
            collision_type="hard<->soft",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )
    ]
    _write_new_contradictions(reg, entries)
    text = reg.read_text()
    assert "# Contradictions Register" in text
    assert "CON-002" in text


def test_write_noop_if_no_entries(tmp_path: Path) -> None:
    reg = tmp_path / "_contradictions.md"
    _write_new_contradictions(reg, [])
    assert not reg.exists()


def test_written_entry_is_parseable(tmp_path: Path) -> None:
    reg = tmp_path / "_contradictions.md"
    entries = [
        ContradictionEntry(
            con_id="CON-001",
            title="Test conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )
    ]
    _write_new_contradictions(reg, entries)
    parsed = _parse_contradictions_register(reg)
    assert len(parsed) == 1
    assert parsed[0].con_id == "CON-001"
    assert parsed[0].status == "unresolved"
    assert parsed[0].blocks == ["01-situation"]


# ── resolve_contradiction ──────────────────────────────────────────────────


def _register_with_unresolved(tmp_path: Path, con_id: str = "CON-001") -> Path:
    reg = tmp_path / "_contradictions.md"
    entries = [
        ContradictionEntry(
            con_id=con_id,
            title="Conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )
    ]
    _write_new_contradictions(reg, entries)
    return reg


def test_resolve_path_d(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    ok = resolve_contradiction(reg, "CON-001", "d", "DEC-001")
    assert ok
    entries = _parse_contradictions_register(reg)
    assert entries[0].status == "resolved-by-d-DEC-001"
    assert entries[0].blocks == []
    assert entries[0].resolution_path == "d"
    assert entries[0].resolution_ref == "DEC-001"


def test_resolve_path_c(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    ok = resolve_contradiction(reg, "CON-001", "c", "ASM-003")
    assert ok
    entries = _parse_contradictions_register(reg)
    assert entries[0].status == "resolved-by-c-ASM-003"
    assert entries[0].resolution_path == "c"


def test_resolve_path_b(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    ok = resolve_contradiction(reg, "CON-001", "b", "SIT-010")
    assert ok
    entries = _parse_contradictions_register(reg)
    assert entries[0].status == "resolved-by-b-SIT-010"


def test_resolve_path_a(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    ok = resolve_contradiction(reg, "CON-001", "a", "source-refresh-001")
    assert ok
    entries = _parse_contradictions_register(reg)
    assert "resolved-by-a" in entries[0].status


def test_resolve_not_found(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    ok = resolve_contradiction(reg, "CON-999", "d", "DEC-001")
    assert not ok
    # Original entry unchanged
    entries = _parse_contradictions_register(reg)
    assert entries[0].status == "unresolved"


def test_resolve_clears_blocking(tmp_path: Path) -> None:
    reg = _register_with_unresolved(tmp_path)
    resolve_contradiction(reg, "CON-001", "d", "DEC-001")
    entries = _parse_contradictions_register(reg)
    blocking = _blocking_entries(entries, "01-situation")
    assert blocking == []


# ── run_check_contradictions ───────────────────────────────────────────────


def test_run_no_contradictions(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _artifact(repo / "00-intake", "scope.md", "No claim atoms here.\n")
    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result.detected == []
    assert result.blocking == []


def test_run_detects_and_writes_contradiction(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Gov/fw.md@abc] [conf:H] "
        "Firewall firmware is version 2.5.\n",
    )
    _artifact(
        repo / "01-situation",
        "situation.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:M] "
        "Firewall firmware is not version 2.5.\n",
    )
    result = run_check_contradictions(repo, phase_idx=1, write_new=True)
    assert len(result.detected) == 1
    reg = repo / "_contradictions.md"
    assert reg.exists()
    parsed = _parse_contradictions_register(reg)
    assert len(parsed) == 1
    assert parsed[0].status == "unresolved"


def test_run_blocks_phase_on_unresolved(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    # Write pre-existing unresolved entry
    reg = repo / "_contradictions.md"
    entries = [
        ContradictionEntry(
            con_id="CON-001",
            title="Pre-existing conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )
    ]
    _write_new_contradictions(reg, entries)

    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert len(result.blocking) == 1
    assert result.blocking[0].con_id == "CON-001"


def test_run_not_blocking_resolved_entry(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    reg = repo / "_contradictions.md"
    entries = [
        ContradictionEntry(
            con_id="CON-001",
            title="Resolved conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="resolved-by-d-DEC-001",
            blocks=[],
            resolution_path="d",
            resolution_ref="DEC-001",
        )
    ]
    _write_new_contradictions(reg, entries)

    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result.blocking == []


def test_run_resolution_path_d_clears_block(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _artifact(
        repo / "00-intake",
        "scope.md",
        "[known] [source:portfolio://Gov/fw.md@abc] [conf:H] "
        "Firewall firmware is version 2.5.\n",
    )
    _artifact(
        repo / "01-situation",
        "situation.md",
        "[elicited] [source:interview:2026-05-25/consultant] [conf:M] "
        "Firewall firmware is not version 2.5.\n",
    )
    # Detect and write
    run_check_contradictions(repo, phase_idx=1, write_new=True)
    # Resolve via path d
    reg = repo / "_contradictions.md"
    entries = _parse_contradictions_register(reg)
    assert len(entries) == 1
    resolve_contradiction(reg, entries[0].con_id, "d", "DEC-001")
    # Re-run: no longer blocking
    result2 = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result2.blocking == []


def test_run_resolution_path_b_clears_block(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    reg = repo / "_contradictions.md"
    _write_new_contradictions(
        reg,
        [ContradictionEntry(
            con_id="CON-001",
            title="Conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )],
    )
    resolve_contradiction(reg, "CON-001", "b", "SIT-010")
    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result.blocking == []


def test_run_resolution_path_c_clears_block(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    reg = repo / "_contradictions.md"
    _write_new_contradictions(
        reg,
        [ContradictionEntry(
            con_id="CON-001",
            title="Conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )],
    )
    resolve_contradiction(reg, "CON-001", "c", "ASM-002")
    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result.blocking == []


def test_run_resolution_path_a_clears_block(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    reg = repo / "_contradictions.md"
    _write_new_contradictions(
        reg,
        [ContradictionEntry(
            con_id="CON-001",
            title="Conflict",
            claim_a="SIT-001",
            claim_b="SIT-002",
            collision_type="hard<->hard",
            detected_at="2026-05-25T10:00:00Z",
            detected_in_phase="01",
            status="unresolved",
            blocks=["01-situation"],
        )],
    )
    resolve_contradiction(reg, "CON-001", "a", "source-refresh-sit001")
    result = run_check_contradictions(repo, phase_idx=1, write_new=False)
    assert result.blocking == []
