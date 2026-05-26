"""Tests for harness/charts.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from harness.charts import (
    _gantt,
    _gap_coverage,
    _risk_donut,
    _spend_bar,
    generate_charts,
)

_MERIDIAN = Path(__file__).parent.parent.parent / "Meridian-Logistics"


def _skip_if_no_meridian() -> None:
    if not _MERIDIAN.exists():
        pytest.skip("Meridian-Logistics fixture not found")


# ---------------------------------------------------------------------------
# Individual chart functions — write to tmp_path
# ---------------------------------------------------------------------------


def test_spend_bar_produces_nonempty_png(tmp_path: Path) -> None:
    _skip_if_no_meridian()
    out = _spend_bar(_MERIDIAN, tmp_path)
    assert out is not None
    assert out.name == "spend_bar.png"
    assert out.stat().st_size > 0


def test_gantt_produces_nonempty_png(tmp_path: Path) -> None:
    _skip_if_no_meridian()
    out = _gantt(_MERIDIAN, tmp_path)
    assert out is not None
    assert out.name == "gantt.png"
    assert out.stat().st_size > 0


def test_risk_donut_produces_nonempty_png(tmp_path: Path) -> None:
    _skip_if_no_meridian()
    out = _risk_donut(_MERIDIAN, tmp_path)
    assert out is not None
    assert out.name == "risk_donut.png"
    assert out.stat().st_size > 0


def test_gap_coverage_produces_nonempty_png(tmp_path: Path) -> None:
    _skip_if_no_meridian()
    out = _gap_coverage(_MERIDIAN, tmp_path)
    assert out is not None
    assert out.name == "gap_coverage.png"
    assert out.stat().st_size > 0


# ---------------------------------------------------------------------------
# Missing source register — chart is skipped, returns None
# ---------------------------------------------------------------------------


def test_missing_risks_returns_none(tmp_path: Path) -> None:
    empty = tmp_path / "empty-eng"
    empty.mkdir()
    out = _risk_donut(empty, tmp_path)
    assert out is None


def test_missing_roadmap_skips_spend_bar(tmp_path: Path) -> None:
    empty = tmp_path / "empty-eng"
    empty.mkdir()
    out = _spend_bar(empty, tmp_path)
    assert out is None


def test_missing_roadmap_skips_gantt(tmp_path: Path) -> None:
    empty = tmp_path / "empty-eng"
    empty.mkdir()
    out = _gantt(empty, tmp_path)
    assert out is None


def test_missing_gaps_skips_gap_coverage(tmp_path: Path) -> None:
    empty = tmp_path / "empty-eng"
    empty.mkdir()
    out = _gap_coverage(empty, tmp_path)
    assert out is None


# ---------------------------------------------------------------------------
# generate_charts integration — writes to engagement 05-handover/charts/
# ---------------------------------------------------------------------------


def test_generate_charts_returns_four_charts() -> None:
    _skip_if_no_meridian()
    charts = generate_charts(_MERIDIAN)
    assert isinstance(charts, dict)
    assert len(charts) == 4
    for name in ("spend_bar", "gantt", "risk_donut", "gap_coverage"):
        assert name in charts, f"Chart '{name}' missing from results"
        assert charts[name].stat().st_size > 0, f"Chart '{name}' is empty"
