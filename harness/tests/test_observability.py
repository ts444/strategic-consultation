"""Tests for harness/observability.py."""

from __future__ import annotations

import json
from pathlib import Path

from harness.observability import append_source_event, append_trace_event

# ---------------------------------------------------------------------------
# append_trace_event
# ---------------------------------------------------------------------------


def test_trace_creates_file(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    append_trace_event(
        phase_dir,
        subagent="synthesizer",
        model="claude-sonnet-4-6",
        prompt_hash="abc123",
        input_hash="def456",
        output_hash="ghi789",
        duration_ms=1234,
    )
    assert (phase_dir / "_trace.jsonl").exists()


def test_trace_line_is_valid_json(tmp_path: Path) -> None:
    phase_dir = tmp_path / "00-intake"
    phase_dir.mkdir()
    append_trace_event(
        phase_dir,
        subagent="interviewer",
        model="claude-opus-4-7",
        prompt_hash="p1",
        input_hash="i1",
        output_hash="o1",
        duration_ms=500,
    )
    lines = (phase_dir / "_trace.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["subagent"] == "interviewer"
    assert record["model"] == "claude-opus-4-7"
    assert record["prompt_hash"] == "p1"
    assert record["input_hash"] == "i1"
    assert record["output_hash"] == "o1"
    assert record["duration_ms"] == 500
    assert "timestamp" in record


def test_trace_required_fields_present(tmp_path: Path) -> None:
    phase_dir = tmp_path / "01-situation"
    phase_dir.mkdir()
    append_trace_event(
        phase_dir,
        subagent="synthesizer",
        model="claude-sonnet-4-6",
        prompt_hash="ph",
        input_hash="ih",
        output_hash="oh",
        duration_ms=0,
    )
    record = json.loads((phase_dir / "_trace.jsonl").read_text())
    expected_keys = (
        "timestamp", "subagent", "model", "prompt_hash",
        "input_hash", "output_hash", "duration_ms",
    )
    for key in expected_keys:
        assert key in record, f"missing key: {key}"


def test_trace_is_append_only(tmp_path: Path) -> None:
    phase_dir = tmp_path / "02-gap"
    phase_dir.mkdir()
    for i in range(3):
        append_trace_event(
            phase_dir,
            subagent=f"agent-{i}",
            model="claude-sonnet-4-6",
            prompt_hash=f"ph{i}",
            input_hash=f"ih{i}",
            output_hash=f"oh{i}",
            duration_ms=i * 100,
        )
    lines = (phase_dir / "_trace.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    for i, line in enumerate(lines):
        record = json.loads(line)
        assert record["subagent"] == f"agent-{i}"


def test_trace_never_truncates_existing(tmp_path: Path) -> None:
    phase_dir = tmp_path / "03-mapping"
    phase_dir.mkdir()
    trace = phase_dir / "_trace.jsonl"
    trace.write_text('{"existing": true}\n', encoding="utf-8")
    append_trace_event(
        phase_dir,
        subagent="synthesizer",
        model="claude-sonnet-4-6",
        prompt_hash="p",
        input_hash="i",
        output_hash="o",
        duration_ms=1,
    )
    lines = trace.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == {"existing": True}


def test_trace_creates_parent_dir(tmp_path: Path) -> None:
    phase_dir = tmp_path / "deep" / "00-intake"
    # Do NOT pre-create the dir
    append_trace_event(
        phase_dir,
        subagent="interviewer",
        model="claude-opus-4-7",
        prompt_hash="p",
        input_hash="i",
        output_hash="o",
        duration_ms=10,
    )
    assert (phase_dir / "_trace.jsonl").exists()


# ---------------------------------------------------------------------------
# append_source_event
# ---------------------------------------------------------------------------


def test_source_creates_file(tmp_path: Path) -> None:
    phase_dir = tmp_path / "01-situation"
    phase_dir.mkdir()
    append_source_event(
        phase_dir,
        tool="portfolio-retriever",
        source_uri="portfolio://security/firewall.md@abc123",
    )
    assert (phase_dir / "_sources.jsonl").exists()


def test_source_line_is_valid_json(tmp_path: Path) -> None:
    phase_dir = tmp_path / "01-situation"
    phase_dir.mkdir()
    append_source_event(
        phase_dir,
        tool="customer-data-retriever",
        source_uri="customer-portal://assets/42@2026-05-25T10:00:00Z",
    )
    lines = (phase_dir / "_sources.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["tool"] == "customer-data-retriever"
    assert record["source_uri"] == "customer-portal://assets/42@2026-05-25T10:00:00Z"
    assert "timestamp" in record


def test_source_required_fields_present(tmp_path: Path) -> None:
    phase_dir = tmp_path / "02-gap"
    phase_dir.mkdir()
    append_source_event(
        phase_dir,
        tool="portfolio-retriever",
        source_uri="portfolio://infra/network.md@deadbeef",
    )
    record = json.loads((phase_dir / "_sources.jsonl").read_text())
    for key in ("timestamp", "tool", "source_uri"):
        assert key in record, f"missing key: {key}"


def test_source_is_append_only(tmp_path: Path) -> None:
    phase_dir = tmp_path / "01-situation"
    phase_dir.mkdir()
    uris = [
        "portfolio://security/ids.md@sha1",
        "portfolio://network/vpn.md@sha2",
        "customer-portal://contracts/7@2026-01-01",
    ]
    for uri in uris:
        append_source_event(phase_dir, tool="portfolio-retriever", source_uri=uri)
    lines = (phase_dir / "_sources.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    for i, line in enumerate(lines):
        assert json.loads(line)["source_uri"] == uris[i]


def test_source_parseable_as_jsonl(tmp_path: Path) -> None:
    phase_dir = tmp_path / "03-mapping"
    phase_dir.mkdir()
    for i in range(5):
        append_source_event(
            phase_dir,
            tool="portfolio-retriever",
            source_uri=f"portfolio://domain/file{i}.md@ref{i}",
        )
    raw = (phase_dir / "_sources.jsonl").read_text(encoding="utf-8")
    records = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
    assert len(records) == 5
