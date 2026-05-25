"""Shared parsing utilities for validator rules."""


def body_lines(text: str) -> list[tuple[int, str]]:
    """Return (1-based line number, content) for all non-frontmatter lines."""
    raw = text.splitlines()
    start = 0
    if raw and raw[0].strip() == "---":
        for i in range(1, len(raw)):
            if raw[i].strip() == "---":
                start = i + 1
                break
    return [(i + 1, raw[i]) for i in range(start, len(raw))]


def frontmatter_keys(text: str) -> set[str]:
    """Return the set of top-level keys declared in YAML frontmatter."""
    raw = text.splitlines()
    if not raw or raw[0].strip() != "---":
        return set()
    keys: set[str] = set()
    for line in raw[1:]:
        if line.strip() == "---":
            break
        if line and not line[0].isspace() and ":" in line and not line.startswith("#"):
            key = line.split(":", 1)[0].strip()
            if key:
                keys.add(key)
    return keys
