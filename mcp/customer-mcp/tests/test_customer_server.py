"""Tests for customer-mcp server tools."""

from __future__ import annotations

import os
import re
from typing import Any
from unittest.mock import patch

import customer_server as _srv
import pytest
from customer_server import compliance_posture, head, list_assets, list_contracts

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_ASSET_URI_RE = re.compile(r"^customer-portal://assets/[^@]+@.+$")
_CONTRACT_URI_RE = re.compile(r"^customer-portal://contracts/[^@]+@.+$")
_POSTURE_URI_RE = re.compile(r"^customer-portal://compliance-posture/[^@]+@.+$")

_FAKE_ASSETS_RESPONSE: dict[str, Any] = {
    "customerId": "org-test",
    "assets": [
        {"id": "asset-1", "type": "Device", "name": "Laptop-001", "metadata": {},
         "updatedAt": "2026-01-01T00:00:00.000Z"},
        {"id": "asset-2", "type": "Server", "name": "SRV-001", "metadata": {},
         "updatedAt": "2026-02-01T00:00:00.000Z"},
    ],
}

_FAKE_CONTRACTS_RESPONSE: dict[str, Any] = {
    "customerId": "org-test",
    "contracts": [
        {
            "id": "contract-1",
            "status": "active",
            "monthlyPricePerUser": 50,
            "userCount": 10,
            "startDate": "2025-01-01",
            "endDate": None,
            "updatedAt": "2026-01-15T00:00:00.000Z",
            "serviceDefinition": {
                "id": "svc-1", "name": "MDM", "domain": "Workplace", "description": "", "tags": []
            },
            "slaPolicy": {"tier": "Standard", "availabilityPct": 99.9, "responseTimeMinutes": 60},
        },
    ],
}

_FAKE_POSTURE_RESPONSE: dict[str, Any] = {
    "customerId": "org-test",
    "updated_at": "2026-02-01T00:00:00.000Z",
    "domains": {
        "Workplace": {
            "services": [{"id": "svc-1", "name": "MDM", "status": "active", "tags": []}],
            "updated_at": "2026-02-01T00:00:00.000Z",
        }
    },
}


def _patch_get(response: Any):  # type: ignore[no-untyped-def]
    """Return a context manager that patches _srv._get to return *response*."""
    return patch.object(_srv, "_get", return_value=response)


# ---------------------------------------------------------------------------
# list_assets
# ---------------------------------------------------------------------------


def test_list_assets_returns_assets() -> None:
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = list_assets("org-test")
    assert result["customerId"] == "org-test"
    assert len(result["assets"]) == 2


def test_list_assets_source_uri_shape() -> None:
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = list_assets("org-test")
    for asset in result["assets"]:
        assert "source" in asset
        assert _ASSET_URI_RE.match(asset["source"]), f"Bad URI: {asset['source']!r}"


def test_list_assets_source_uri_includes_asset_id() -> None:
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = list_assets("org-test")
    assert result["assets"][0]["source"].startswith("customer-portal://assets/asset-1@")
    assert result["assets"][1]["source"].startswith("customer-portal://assets/asset-2@")


def test_list_assets_source_uri_includes_updated_at() -> None:
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = list_assets("org-test")
    assert "2026-01-01T00:00:00.000Z" in result["assets"][0]["source"]


def test_list_assets_empty_customer() -> None:
    with _patch_get({"customerId": "org-empty", "assets": []}):
        result = list_assets("org-empty")
    assert result["assets"] == []


# ---------------------------------------------------------------------------
# list_contracts
# ---------------------------------------------------------------------------


def test_list_contracts_returns_contracts() -> None:
    with _patch_get(_FAKE_CONTRACTS_RESPONSE):
        result = list_contracts("org-test")
    assert result["customerId"] == "org-test"
    assert len(result["contracts"]) == 1


def test_list_contracts_source_uri_shape() -> None:
    with _patch_get(_FAKE_CONTRACTS_RESPONSE):
        result = list_contracts("org-test")
    for contract in result["contracts"]:
        assert "source" in contract
        assert _CONTRACT_URI_RE.match(contract["source"]), f"Bad URI: {contract['source']!r}"


def test_list_contracts_source_uri_includes_contract_id() -> None:
    with _patch_get(_FAKE_CONTRACTS_RESPONSE):
        result = list_contracts("org-test")
    assert result["contracts"][0]["source"].startswith("customer-portal://contracts/contract-1@")


def test_list_contracts_source_uri_includes_updated_at() -> None:
    with _patch_get(_FAKE_CONTRACTS_RESPONSE):
        result = list_contracts("org-test")
    assert "2026-01-15T00:00:00.000Z" in result["contracts"][0]["source"]


# ---------------------------------------------------------------------------
# compliance_posture
# ---------------------------------------------------------------------------


def test_compliance_posture_returns_domains() -> None:
    with _patch_get(_FAKE_POSTURE_RESPONSE):
        result = compliance_posture("org-test")
    assert "domains" in result
    assert "Workplace" in result["domains"]


def test_compliance_posture_source_uri_shape() -> None:
    with _patch_get(_FAKE_POSTURE_RESPONSE):
        result = compliance_posture("org-test")
    assert "source" in result
    assert _POSTURE_URI_RE.match(result["source"]), f"Bad URI: {result['source']!r}"


def test_compliance_posture_source_uri_includes_customer_id() -> None:
    with _patch_get(_FAKE_POSTURE_RESPONSE):
        result = compliance_posture("org-test")
    assert result["source"].startswith("customer-portal://compliance-posture/org-test@")


def test_compliance_posture_source_uri_includes_updated_at() -> None:
    with _patch_get(_FAKE_POSTURE_RESPONSE):
        result = compliance_posture("org-test")
    assert "2026-02-01T00:00:00.000Z" in result["source"]


# ---------------------------------------------------------------------------
# head
# ---------------------------------------------------------------------------


def test_head_assets_returns_source_uri() -> None:
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = head("assets", "org-test")
    assert result["customerId"] == "org-test"
    assert result["resourceType"] == "assets"
    assert _ASSET_URI_RE.match(result["source"]), f"Bad URI: {result['source']!r}"


def test_head_contracts_returns_source_uri() -> None:
    with _patch_get(_FAKE_CONTRACTS_RESPONSE):
        result = head("contracts", "org-test")
    assert result["resourceType"] == "contracts"
    assert _CONTRACT_URI_RE.match(result["source"])


def test_head_compliance_posture_returns_source_uri() -> None:
    with _patch_get(_FAKE_POSTURE_RESPONSE):
        result = head("compliance-posture", "org-test")
    assert result["resourceType"] == "compliance-posture"
    assert _POSTURE_URI_RE.match(result["source"])


def test_head_unknown_resource_type_raises() -> None:
    with _patch_get({}), pytest.raises(ValueError, match="Unknown resource_type"):
        head("unknown-type", "org-test")


def test_head_assets_max_updated_at() -> None:
    """head() returns the max updatedAt across assets."""
    with _patch_get(_FAKE_ASSETS_RESPONSE):
        result = head("assets", "org-test")
    # max of 2026-01-01 and 2026-02-01 is 2026-02-01
    assert "2026-02-01T00:00:00.000Z" in result["source"]


def test_head_empty_assets() -> None:
    with _patch_get({"customerId": "org-empty", "assets": []}):
        result = head("assets", "org-empty")
    assert "source" in result


# ---------------------------------------------------------------------------
# No write tools exposed
# ---------------------------------------------------------------------------


def test_no_write_tools_in_module() -> None:
    """The server module must not expose any write/mutate functions."""
    import customer_server as s
    _WRITE_WORDS = {"create", "update", "delete", "patch", "write", "insert", "upsert"}
    public_names = [n for n in dir(s) if not n.startswith("_")]
    write_names = [
        n for n in public_names
        if any(n == w or n.startswith(w + "_") or n.endswith("_" + w) for w in _WRITE_WORDS)
    ]
    assert write_names == [], f"Unexpected write tools found: {write_names}"


# ---------------------------------------------------------------------------
# Smoke test — live portal (skipped if not reachable)
# ---------------------------------------------------------------------------


def test_live_list_assets_smoke() -> None:
    """Smoke: real portal must return assets for the small seeded customer."""
    portal_url = os.environ.get("CUSTOMER_PORTAL_URL", "")
    bearer = os.environ.get("CUSTOMER_PORTAL_BEARER_TOKEN", "")
    if not portal_url or not bearer:
        pytest.skip("CUSTOMER_PORTAL_URL and CUSTOMER_PORTAL_BEARER_TOKEN not set")
    try:
        with (
            patch.object(_srv, "PORTAL_URL", portal_url),
            patch.object(_srv, "BEARER_TOKEN", bearer),
        ):
            result = list_assets("org-apex")
        assert "assets" in result
        assert isinstance(result["assets"], list)
        for asset in result["assets"]:
            assert _ASSET_URI_RE.match(asset["source"]), f"Bad URI: {asset['source']!r}"
    except ValueError as exc:
        pytest.skip(f"Portal not reachable: {exc}")
