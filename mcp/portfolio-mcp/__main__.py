"""MCP JSON-RPC 2.0 stdio server entry point.

Run with:  python -m portfolio_mcp
"""

from __future__ import annotations

import json
import sys
from typing import Any

from server import (
    head,
    list_domains,
    list_services_in_domain,
    read_service,
    search_services,
)

_SERVER_INFO = {"name": "portfolio-mcp", "version": "1.0.0"}
_PROTOCOL_VERSION = "2024-11-05"

_TOOLS: list[dict[str, Any]] = [
    {
        "name": "list_domains",
        "description": "Return the list of service domains in the MSP portfolio.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "list_services_in_domain",
        "description": "List all services within a specific domain with source URIs.",
        "inputSchema": {
            "type": "object",
            "properties": {"domain": {"type": "string", "description": "Domain name"}},
            "required": ["domain"],
        },
    },
    {
        "name": "read_service",
        "description": "Read the full markdown content of a service by name.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Service stem or filename"}},
            "required": ["name"],
        },
    },
    {
        "name": "search_services",
        "description": (
            "Search services by keyword. Returns up to 10 hits with snippets "
            "and portfolio:// source citations."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword"},
                "max_hits": {
                    "type": "integer",
                    "description": "Maximum results (default 10)",
                    "default": 10,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "head",
        "description": (
            "Return the source URI (with git sha or mtime) for a service. "
            "Used for freshness / decay checking."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Service stem or filename"}},
            "required": ["name"],
        },
    },
]


def _ok(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _err(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def _call_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "list_domains":
        return list_domains()
    if name == "list_services_in_domain":
        return list_services_in_domain(args["domain"])
    if name == "read_service":
        return read_service(args["name"])
    if name == "search_services":
        return search_services(args["query"], args.get("max_hits", 10))
    if name == "head":
        return head(args["name"])
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
