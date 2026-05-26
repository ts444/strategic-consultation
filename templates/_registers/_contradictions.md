# Contradictions Register Schema

> **Canonical reference.** Contradictions block phase progression until resolved.
> This register is checked by orchestrator prompts at step 4 of the seven-step
> loop before synthesis may begin.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

A contradiction is a collision between two claims in scope that cannot both be
true simultaneously. Three collision types are tracked:

| Type | Description |
|---|---|
| `hard<->hard` | Two `[known]` or `[elicited]` facts directly contradict each other |
| `hard<->soft` | A `[known]` or `[elicited]` fact contradicts an `[inferred]` or `[assumed]` claim |
| `soft<->soft` | Two `[inferred]` or `[assumed]` claims contradict each other |

Explicit supersessions (`supersedes: <claim-id>` on a newer elicited claim)
are **not** contradictions and are excluded from detection.

---

## Entry Schema

| Field | Type | Notes |
|---|---|---|
| `id` | `CON-NNN` | Sequential, unique within engagement |
| `title` | string | Brief description of the collision |
| `claim_a` | claim id | First contradicting claim |
| `claim_b` | claim id | Second contradicting claim |
| `collision_type` | `hard<->hard \| hard<->soft \| soft<->soft` | |
| `detected_at` | ISO-8601 datetime | When `check_contradictions.py` first recorded this |
| `detected_in_phase` | `00–06` | |
| `Status` | see below | Lifecycle field; capitalised by convention |
| `Blocks` | phase id(s) | Phase(s) that cannot proceed while this contradiction is unresolved |
| `resolution_path` | `a \| b \| c \| d` or null | Which of the four paths was used |
| `resolution_ref` | id or null | The artifact that closes this (e.g. `DEC-004`, `ASM-007`) |
| `resolved_at` | ISO-8601 datetime or null | |

---

## Status Values

| Status | Meaning |
|---|---|
| `unresolved` | Active block; phase in `Blocks` cannot proceed |
| `resolved-by-a-<ref>` | Source-update placeholder applied (path a) |
| `resolved-by-b-<claim-id>` | Superseded by a newer elicited claim (path b) |
| `resolved-by-c-<ASM-NNN>` | Filed as a declared assumption (path c) |
| `resolved-by-d-<DEC-NNN>` | Resolved by a binding consultant decision (path d) |

`Blocks` must list every phase id whose synthesis depends on the contradicting
claims. Non-empty `unresolved` entries with a `Blocks` field that includes the
current phase halt the orchestrator loop at step 4.

---

## Resolution Paths

| Path | Action |
|---|---|
| **(a)** Source update | The source is outdated; a placeholder is added to refresh it at next decay check. Status: `resolved-by-a-<source-refresh-ref>`. |
| **(b)** Supersession | A new `[elicited]` claim carries `supersedes: <claim-id>` for the older contradicting claim. Status: `resolved-by-b-<new-claim-id>`. |
| **(c)** Assumption | Both claims are acknowledged and the team proceeds under a declared assumption in `_assumptions.md`. Status: `resolved-by-c-<ASM-NNN>`. |
| **(d)** Decision | The consultant makes a binding override in `_decisions.md`. Status: `resolved-by-d-<DEC-NNN>`. |

---

## Register-level fields (file header)

```yaml
---
register: contradictions
phase_updated: "02"
harness_version: "0.1.0"
---
```

---

## Worked Example

```yaml
---
id: CON-002
title: Firewall review date conflict — portal metadata vs. interview statement
claim_a: SIT-008
claim_b: SIT-015
collision_type: hard<->soft
detected_at: "2026-05-26T10:15:00Z"
detected_in_phase: "01"
Status: resolved-by-d-DEC-004
Blocks: []
resolution_path: d
resolution_ref: DEC-004
resolved_at: "2026-05-26T11:30:00Z"
---
```

---

## Validator Notes

- Any entry with `Status: unresolved` and a non-empty `Blocks` list that
  includes the current phase will halt synthesis (`check_contradictions.py`).
- `resolved-by-*` statuses must reference an existing id in the corresponding
  register (`_decisions.md`, `_assumptions.md`, or a claim in scope).
