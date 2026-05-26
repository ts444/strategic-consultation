"""Shared parsing utilities for validator rules."""

from __future__ import annotations


def body_lines(text: str) -> list[tuple[int, str]]:
    """Return (1-based line number, content) for non-frontmatter, non-HTML-comment lines."""
    raw = text.splitlines()
    start = 0
    if raw and raw[0].strip() == "---":
        for i in range(1, len(raw)):
            if raw[i].strip() == "---":
                start = i + 1
                break
    result: list[tuple[int, str]] = []
    in_comment = False
    for i in range(start, len(raw)):
        line = raw[i]
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            open_idx = line.index("<!--")
            if line.find("-->", open_idx + 4) == -1:
                in_comment = True
            continue
        result.append((i + 1, line))
    return result


def frontmatter_value(text: str, key: str) -> str | None:
    """Return the value of a top-level frontmatter key, or None if absent."""
    raw = text.splitlines()
    if not raw or raw[0].strip() != "---":
        return None
    for line in raw[1:]:
        if line.strip() == "---":
            break
        if not line or line[0].isspace():
            continue
        if line.startswith(f"{key}:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            return val if val else None
    return None


def parse_yaml_blocks(text: str) -> list[dict[str, object]]:
    """
    Parse all ```yaml fenced blocks that use ---...--- YAML delimiters.

    Returns one dict per block. Each dict contains:
      '_lineno': int  — line number of the opening ---
      '_present_keys': set[str]  — all top-level keys declared in the block
      '<key>': str | list[str] | None
        - str   for scalar values  (e.g. id: GAP-001)
        - list[str] for list values  (inline [] or indented - items)
        - None  for keys with a multi-line / empty body and no list items
    """
    blocks: list[dict[str, object]] = []
    in_fence = False
    in_block = False
    current: dict[str, object] | None = None
    current_list_key: str | None = None

    for lineno, line in body_lines(text):
        stripped = line.strip()

        if stripped == "```yaml" and not in_fence:
            in_fence = True
            in_block = False
            current = None
            current_list_key = None
            continue

        if stripped == "```" and in_fence:
            if in_block and current is not None:
                blocks.append(current)
            in_fence = False
            in_block = False
            current = None
            current_list_key = None
            continue

        if not in_fence:
            continue

        if stripped == "---":
            if not in_block:
                in_block = True
                current = {"_lineno": lineno, "_present_keys": set()}
                current_list_key = None
            else:
                if current is not None:
                    blocks.append(current)
                in_block = False
                current = None
                current_list_key = None
            continue

        if not in_block or current is None:
            continue

        # Top-level key: non-indented line containing ':'
        if line and not line[0].isspace() and ":" in line and not stripped.startswith("#"):
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip() if len(parts) > 1 else ""
            present_keys = current["_present_keys"]
            assert isinstance(present_keys, set)
            present_keys.add(key)
            current_list_key = None
            if val == "[]":
                current[key] = []
            elif val == "":
                # No inline value — may be followed by list items or multi-line scalar
                current[key] = []
                current_list_key = key
            else:
                current[key] = val
            continue

        # List item under current_list_key
        if (
            current_list_key is not None
            and line
            and line[0].isspace()
            and stripped.startswith("- ")
        ):
            item = stripped[2:].strip()
            lst = current[current_list_key]
            assert isinstance(lst, list)
            lst.append(item)
            continue

        # Non-indented line that isn't a key → end of block scope; stop list collection
        if current_list_key is not None and line and not line[0].isspace():
            current_list_key = None

    return blocks


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
