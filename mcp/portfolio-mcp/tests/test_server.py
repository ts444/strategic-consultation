"""Tests for portfolio-mcp server tools."""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import patch

import pytest
import server as _srv
from server import (
    PORTFOLIO_ROOT,
    head,
    list_domains,
    list_services_in_domain,
    read_service,
    search_services,
)

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

_SOURCE_RE = re.compile(r"^portfolio://[^/]+/[^@]+\.md@.+$")

_REQUIRED_DOMAINS = {"Governance", "Infrastructure", "Network", "Security", "Workplace"}


def _make_portfolio(tmp_path: Path) -> Path:
    """Create a minimal synthetic portfolio directory."""
    root = tmp_path / "portfolio"
    for domain, services in [
        ("Alpha", ["ServiceA.md", "ServiceB.md"]),
        ("Beta", ["ServiceC.md"]),
    ]:
        d = root / domain
        d.mkdir(parents=True)
        for svc in services:
            stem = Path(svc).stem
            (d / svc).write_text(
                f"---\nname: {stem}\ntags: [test]\n---\n\n## Overview\n{svc} overview.\n",
                encoding="utf-8",
            )
    return root


# ---------------------------------------------------------------------------
# list_domains — live smoke test
# ---------------------------------------------------------------------------


def test_list_domains_live() -> None:
    """Smoke: live ~/msp-portfolio must contain the five expected domains."""
    if not PORTFOLIO_ROOT.is_dir():
        pytest.skip("~/msp-portfolio not present in this environment")
    domains = list_domains()
    assert _REQUIRED_DOMAINS.issubset(set(domains)), (
        f"Expected {_REQUIRED_DOMAINS!r}, got {domains!r}"
    )


def test_list_domains_synthetic(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        domains = list_domains()
    assert domains == ["Alpha", "Beta"]


# ---------------------------------------------------------------------------
# list_services_in_domain
# ---------------------------------------------------------------------------


def test_list_services_in_domain_returns_services(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        services = list_services_in_domain("Alpha")
    assert [s["name"] for s in services] == ["ServiceA", "ServiceB"]
    for svc in services:
        assert _SOURCE_RE.match(svc["source"]), f"Bad source URI: {svc['source']!r}"


def test_list_services_in_domain_source_uri_shape(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        services = list_services_in_domain("Beta")
    assert services[0]["source"].startswith("portfolio://Beta/ServiceC.md@")


def test_list_services_in_domain_unknown_domain(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root), pytest.raises(ValueError):
        list_services_in_domain("NoSuchDomain")


# ---------------------------------------------------------------------------
# read_service
# ---------------------------------------------------------------------------


def test_read_service_by_stem(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        result = read_service("ServiceA")
    assert result["name"] == "ServiceA"
    assert result["domain"] == "Alpha"
    assert "overview" in result["content"].lower()
    assert _SOURCE_RE.match(result["source"])


def test_read_service_by_filename(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        result = read_service("ServiceA.md")
    assert result["name"] == "ServiceA"


def test_read_service_not_found(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root), pytest.raises(ValueError):
        read_service("NoSuchService")


# ---------------------------------------------------------------------------
# search_services
# ---------------------------------------------------------------------------


def test_search_services_finds_match(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        hits = search_services("overview")
    assert len(hits) >= 1
    for h in hits:
        assert _SOURCE_RE.match(h["source"])
        assert "snippet" in h


def test_search_services_no_match(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        hits = search_services("xyzzy_nonexistent")
    assert hits == []


def test_search_services_max_hits(tmp_path: Path) -> None:
    """max_hits is respected."""
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        hits = search_services("overview", max_hits=1)
    assert len(hits) <= 1


def test_search_services_never_raw_grep(tmp_path: Path) -> None:
    """Every hit must have a snippet field (not a raw file dump)."""
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        hits = search_services("overview")
    for h in hits:
        assert "snippet" in h
        assert isinstance(h["snippet"], str)
        assert len(h["snippet"]) < 300, "snippet should be a short excerpt, not a full file"


# ---------------------------------------------------------------------------
# head
# ---------------------------------------------------------------------------


def test_head_returns_source_uri(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        result = head("ServiceC")
    assert result["name"] == "ServiceC"
    assert result["domain"] == "Beta"
    assert _SOURCE_RE.match(result["source"])


def test_head_mtime_when_not_git(tmp_path: Path) -> None:
    """When the portfolio is not a git repo, source URI ends with a numeric mtime."""
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        result = head("ServiceA")
    ref = result["source"].split("@")[-1]
    assert ref.isdigit(), f"Expected mtime, got: {ref!r}"


def test_head_not_found(tmp_path: Path) -> None:
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root), pytest.raises(ValueError):
        head("NoSuchService")


# ---------------------------------------------------------------------------
# source URI shape — portfolio:// with no write exposure
# ---------------------------------------------------------------------------


def test_source_uri_shape(tmp_path: Path) -> None:
    """Source URIs must match portfolio://<domain>/<file>.md@<ref>."""
    root = _make_portfolio(tmp_path)
    with patch.object(_srv, "PORTFOLIO_ROOT", root):
        for domain in list_domains():
            for svc in list_services_in_domain(domain):
                assert _SOURCE_RE.match(svc["source"]), svc["source"]
