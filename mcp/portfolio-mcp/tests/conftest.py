"""Add mcp/portfolio-mcp to sys.path so tests import server directly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
