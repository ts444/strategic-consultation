#!/usr/bin/env python3
"""Shared observability utilities for append-only trace and source logging.

Append functions:
  append_trace_event  — records a subagent invocation into _trace.jsonl
  append_source_event — records a retriever tool call into _sources.jsonl

Both files are strictly append-only (opened with mode="a").
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path


def append_trace_event(
    phase_dir: Path,
    *,
    subagent: str,
    model: str,
    prompt_hash: str,
    input_hash: str,
    output_hash: str,
    duration_ms: int,
) -> None:
    """Append one invocation record to <phase_dir>/_trace.jsonl."""
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "subagent": subagent,
        "model": model,
        "prompt_hash": prompt_hash,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "duration_ms": duration_ms,
    }
    _append_jsonl(phase_dir / "_trace.jsonl", record)


def append_source_event(
    phase_dir: Path,
    *,
    tool: str,
    source_uri: str,
) -> None:
    """Append one retrieval record to <phase_dir>/_sources.jsonl."""
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "tool": tool,
        "source_uri": source_uri,
    }
    _append_jsonl(phase_dir / "_sources.jsonl", record)


def _append_jsonl(path: Path, record: Mapping[str, object]) -> None:
    """Append a JSON line to path; creates file if absent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
