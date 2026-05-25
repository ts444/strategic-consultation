"""MCP JSON-RPC 2.0 stdio server entry point.

Environment: set CUSTOMER_PORTAL_URL and CUSTOMER_PORTAL_BEARER_TOKEN before running.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from customer_server import (
    compliance_posture,
    head,
    list_assets,
    list_contracts,
)

_SERVER_INFO = {"name": "customer-mcp", "version": "1.0.0"}
_PROTOCOL_VERSION = "2024-11-05"

_TOOLS: list[dict[str, Any]] = [
    {
        "name": "list_assets",
        "description": (
            "List all IT assets for a customer. "
            "Each asset includes a customer-portal:// source URI."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Customer organisation id"}
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "list_contracts",
        "description": (
            "List all contracted services for a customer. "
            "Each contract includes a customer-portal:// source URI."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Customer organisation id"}
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "compliance_posture",
        "description": (
            "Return the compliance posture (domain-grouped services) for a customer. "
            "Includes a customer-portal:// source URI."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Customer organisation id"}
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "head",
        "description": (
            "Return freshness info (source URI with updated_at) for a customer's resource "
            "collection. Used for decay checking of [known] claims."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource_type": {
                    "type": "string",
                    "description": "Resource type: 'assets', 'contracts', or 'compliance-posture'",
                    "enum": ["assets", "contracts", "compliance-posture"],
                },
                "customer_id": {"type": "string", "description": "Customer organisation id"},
            },
            "required": ["resource_type", "customer_id"],
        },
    },
]


def _ok(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _err(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def _call_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "list_assets":
        return list_assets(args["customer_id"])
    if name == "list_contracts":
        return list_contracts(args["customer_id"])
    if name == "compliance_posture":
        return compliance_posture(args["customer_id"])
    if name == "head":
        return head(args["resource_type"], args["customer_id"])
    raise ValueError(f"Unknown tool: {name!r}")


def _dispatch(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method", "")
    req_id = msg.get("id")

    # Notifications (no id) — fire-and-forget
    if req_id is None:
        return None

    if method == "initialize":
        return _ok(
            req_id,
            {
                "protocolVersion": _PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": _SERVER_INFO,
            },
        )

    if method == "tools/list":
        return _ok(req_id, {"tools": _TOOLS})

    if method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name", "")
        tool_args: dict[str, Any] = params.get("arguments", {})
        try:
            result = _call_tool(tool_name, tool_args)
        except ValueError as exc:
            return _err(req_id, -32602, str(exc))
        except Exception as exc:  # noqa: BLE001
            return _err(req_id, -32603, f"Internal error: {exc}")
        return _ok(req_id, {"content": [{"type": "text", "text": json.dumps(result)}]})

    return _err(req_id, -32601, f"Method not found: {method!r}")


def main() -> None:
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            msg = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            resp = _err(None, -32700, f"Parse error: {exc}")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            continue
        resp2 = _dispatch(msg)
        if resp2 is not None:
            sys.stdout.write(json.dumps(resp2) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
