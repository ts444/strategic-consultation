"""Customer-data MCP server — wraps the customer-portal HTTP API.

All tools are read-only. Every response embeds a source URI:
  customer-portal://<resource>/<id>@<updated_at>

Environment variables:
  CUSTOMER_PORTAL_URL           Base URL (default: http://localhost:3000)
  CUSTOMER_PORTAL_BEARER_TOKEN  Bearer token for API auth
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

PORTAL_URL = os.environ.get("CUSTOMER_PORTAL_URL", "http://localhost:3000").rstrip("/")
BEARER_TOKEN = os.environ.get("CUSTOMER_PORTAL_BEARER_TOKEN", "")

_VALID_RESOURCE_TYPES = {"assets", "contracts", "compliance-posture"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get(path: str) -> Any:
    """GET from the customer portal API; raises ValueError on HTTP errors."""
    url = f"{PORTAL_URL}{path}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise ValueError("Unauthorized: check CUSTOMER_PORTAL_BEARER_TOKEN") from exc
        if exc.code == 404:
            raise ValueError(f"Customer not found: {path!r}") from exc
        raise ValueError(f"HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"Network error reaching customer portal: {exc.reason}") from exc


def _asset_uri(asset_id: str, updated_at: str) -> str:
    return f"customer-portal://assets/{asset_id}@{updated_at}"


def _contract_uri(contract_id: str, updated_at: str) -> str:
    return f"customer-portal://contracts/{contract_id}@{updated_at}"


def _posture_uri(customer_id: str, updated_at: str) -> str:
    return f"customer-portal://compliance-posture/{customer_id}@{updated_at}"


# ---------------------------------------------------------------------------
# Public tool functions
# ---------------------------------------------------------------------------


def list_assets(customer_id: str) -> dict[str, Any]:
    """List all assets for a customer. Each asset includes a source URI."""
    data = _get(f"/api/customers/{customer_id}/assets")
    assets: list[dict[str, Any]] = []
    for a in data.get("assets", []):
        updated = str(a.get("updatedAt", ""))
        assets.append({**a, "source": _asset_uri(a["id"], updated)})
    return {"customerId": data["customerId"], "assets": assets}


def list_contracts(customer_id: str) -> dict[str, Any]:
    """List all contracted services for a customer. Each contract includes a source URI."""
    data = _get(f"/api/customers/{customer_id}/contracts")
    contracts: list[dict[str, Any]] = []
    for c in data.get("contracts", []):
        updated = str(c.get("updatedAt", ""))
        contracts.append({**c, "source": _contract_uri(c["id"], updated)})
    return {"customerId": data["customerId"], "contracts": contracts}


def compliance_posture(customer_id: str) -> dict[str, Any]:
    """Return the compliance posture (domain-grouped services) for a customer."""
    data = _get(f"/api/customers/{customer_id}/compliance-posture")
    updated_at = str(data.get("updated_at", ""))
    return {**data, "source": _posture_uri(customer_id, updated_at)}


def head(resource_type: str, customer_id: str) -> dict[str, str]:
    """Return freshness info for a customer's resource collection.

    resource_type: 'assets' | 'contracts' | 'compliance-posture'
    customer_id:   the customer whose resource to check

    Returns a source URI with the most-recent updated_at for the collection.
    Used by decay_check to detect stale [known] claims.
    """
    if resource_type not in _VALID_RESOURCE_TYPES:
        raise ValueError(
            f"Unknown resource_type: {resource_type!r}. "
            f"Must be one of: {sorted(_VALID_RESOURCE_TYPES)}"
        )

    if resource_type == "assets":
        data = _get(f"/api/customers/{customer_id}/assets")
        assets = data.get("assets", [])
        updated_at = (
            max((str(a.get("updatedAt", "")) for a in assets), default="")
            if assets
            else ""
        )
        return {
            "customerId": customer_id,
            "resourceType": resource_type,
            "source": _asset_uri(customer_id, updated_at),
        }

    if resource_type == "contracts":
        data = _get(f"/api/customers/{customer_id}/contracts")
        contracts = data.get("contracts", [])
        updated_at = (
            max((str(c.get("updatedAt", "")) for c in contracts), default="")
            if contracts
            else ""
        )
        return {
            "customerId": customer_id,
            "resourceType": resource_type,
            "source": _contract_uri(customer_id, updated_at),
        }

    # compliance-posture
    data = _get(f"/api/customers/{customer_id}/compliance-posture")
    updated_at = str(data.get("updated_at", ""))
    return {
        "customerId": customer_id,
        "resourceType": resource_type,
        "source": _posture_uri(customer_id, updated_at),
    }
