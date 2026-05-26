"""Root conftest: add MCP server directories to sys.path for test imports.

portfolio-mcp tests import `server` (server.py)
customer-mcp tests import `customer_server` (customer_server.py)

Both dirs are added so each can find its own module without collision.
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent

for _mcp_dir in [
    _REPO_ROOT / "mcp" / "portfolio-mcp",
    _REPO_ROOT / "mcp" / "customer-mcp",
]:
    _p = str(_mcp_dir)
    if _p not in sys.path:
        sys.path.insert(0, _p)
