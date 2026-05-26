"""Portfolio MCP server — core tool implementations.

All tools are read-only. Every response embeds a source URI:
  portfolio://<domain>/<file>.md@<git-sha-or-mtime>
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

PORTFOLIO_ROOT = Path("~/msp-portfolio").expanduser()

MAX_SEARCH_HITS = 10


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _sha_or_mtime(file_path: Path) -> str:
    """Return git sha for *file_path* if the portfolio is a git repo, else mtime."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(file_path)],
            cwd=file_path.parent,
            capture_output=True,
            text=True,
            timeout=5,
        )
        sha = result.stdout.strip()
        if sha:
            return sha
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    try:
        return str(int(file_path.stat().st_mtime))
    except OSError:
        return "unknown"


def _source_uri(domain: str, filename: str) -> str:
    file_path = PORTFOLIO_ROOT / domain / filename
    ref = _sha_or_mtime(file_path)
    return f"portfolio://{domain}/{filename}@{ref}"


def _find_service_file(name: str) -> tuple[Path, str] | None:
    """Return (path, domain) for a service by stem or filename, or None."""
    for domain_dir in sorted(PORTFOLIO_ROOT.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("."):
            continue
        for f in domain_dir.glob("*.md"):
            if f.stem == name or f.name == name:
                return f, domain_dir.name
    return None


# ---------------------------------------------------------------------------
# Public tool functions
# ---------------------------------------------------------------------------


def list_domains() -> list[str]:
    """Return sorted list of domain names in the portfolio."""
    return sorted(
        d.name
        for d in PORTFOLIO_ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def list_services_in_domain(domain: str) -> list[dict[str, str]]:
    """Return services in *domain* with source URIs."""
    domain_dir = PORTFOLIO_ROOT / domain
    if not domain_dir.is_dir():
        raise ValueError(f"Domain not found: {domain!r}")
    return [
        {"name": f.stem, "source": _source_uri(domain, f.name)}
        for f in sorted(domain_dir.glob("*.md"))
    ]


def read_service(name: str) -> dict[str, Any]:
    """Read a service markdown file by stem or filename. Searches all domains."""
    result = _find_service_file(name)
    if result is None:
        raise ValueError(f"Service not found: {name!r}")
    file_path, domain = result
    content = file_path.read_text(encoding="utf-8")
    return {
        "name": file_path.stem,
        "domain": domain,
        "content": content,
        "source": _source_uri(domain, file_path.name),
    }


def search_services(query: str, max_hits: int = MAX_SEARCH_HITS) -> list[dict[str, Any]]:
    """Search services by keyword in name or content. Returns at most *max_hits* results.

    Each hit includes a short snippet around the match and a source citation —
    never returns raw file dumps.
    """
    query_lower = query.lower()
    hits: list[dict[str, Any]] = []
    for domain_dir in sorted(PORTFOLIO_ROOT.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("."):
            continue
        domain = domain_dir.name
        for f in sorted(domain_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            if query_lower not in f.stem.lower() and query_lower not in content.lower():
                continue
            idx = content.lower().find(query_lower)
            if idx >= 0:
                start = max(0, idx - 60)
                end = min(len(content), idx + 120)
                raw = content[start:end].replace("\n", " ").strip()
                snippet = f"...{raw}..."
            else:
                snippet = content[:140].replace("\n", " ").strip()
            hits.append(
                {
                    "name": f.stem,
                    "domain": domain,
                    "source": _source_uri(domain, f.name),
                    "snippet": snippet,
                }
            )
            if len(hits) >= max_hits:
                return hits
    return hits


def head(name: str) -> dict[str, str]:
    """Return freshness info for a service (source URI with git sha or mtime).

    Used by decay_check to detect stale [known] claims.
    """
    result = _find_service_file(name)
    if result is None:
        raise ValueError(f"Service not found: {name!r}")
    file_path, domain = result
    return {
        "name": file_path.stem,
        "domain": domain,
        "source": _source_uri(domain, file_path.name),
    }
