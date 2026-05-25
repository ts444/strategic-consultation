# Decisions Register Schema

> **Canonical reference.** Binds to `_claim.schema.md` §1. Records consultant
> decisions that resolve contradictions, override claims, or establish binding
> direction for the engagement.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

The decisions register makes explicit choices visible and auditable. It is the
destination for contradiction resolution path **(d)**: when the consultant
decides which of two contradicting claims to treat as authoritative, a decision
entry records the override and its rationale.

---

## Entry Schema

| Field | Type | Notes |
|---|---|---|
| `id` | `DEC-NNN` | Sequential, unique within engagement |
| `title` | string | Short description of the decision |
| `decision` | string | The actual choice made, stated plainly |
| `rationale` | string | Why this option was chosen |
| `overrides` | list of claim ids | Claim ids that are superseded by this decision; used by `claim_composition_resolvable.py` to clear dependency violations |
| `alternatives_considered` | list of strings | Other options that were evaluated and rejected |
| `made_by` | string | Named consultant or role |
| `made_at` | ISO-8601 date | |
| `phase` | `00–06` | Phase in which the decision was made |
| `resolves_contradiction` | `CON-NNN` or null | ID of the contradiction this decision closes (see `_contradictions.md`) |

---

## Resolution-path (d) usage

When contradiction resolution path **(d)** is chosen (consultant makes an
explicit binding decision), the entry in `_decisions.md` must:

1. Set `overrides` to the list of claim ids being superseded.
2. Set `resolves_contradiction` to the `CON-NNN` id in `_contradictions.md`.
3. Set the corresponding contradiction's `Status` field to
   `resolved-by-d-DEC-NNN`.

The `overrides` field is the machine-readable binding: the validator's
`claim_composition_resolvable.py` uses it to suppress false-positive
resolution failures for superseded claims.

---

## Worked Example

```yaml
---
id: DEC-004
title: Treat customer's self-reported firewall review date as authoritative
decision: >
  Accept the customer's stated "reviewed 2025-Q3" date from the interview over
  the portal-recorded last-modified date of 2024-11-01. The portal timestamp
  reflects document upload, not the review itself.
rationale: >
  The IT manager confirmed verbally in Phase 01 that the firewall was reviewed
  in August 2025 but the documentation upload was delayed. Accepting the
  interview date removes a hard<->soft contradiction and avoids inflating gap
  severity based on stale portal metadata.
overrides:
  - SIT-008
alternatives_considered:
  - Treat portal date as authoritative and flag higher severity (rejected: over-conservative)
  - Flag as unresolvable and escalate to customer (rejected: consultant has direct confirmation)
made_by: Lead Consultant
made_at: "2026-05-26"
phase: "01"
resolves_contradiction: CON-002
---
```

---

## Validator Notes

- `overrides` ids must exist in scope; the validator confirms this in
  `claim_composition_resolvable.py`.
- `resolves_contradiction` must match a `CON-NNN` id in `_contradictions.md`
  whose `Status` is `resolved-by-d-DEC-NNN`.
