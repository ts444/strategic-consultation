# Assumptions Register Schema

> **Canonical reference.** Binds to `_claim.schema.md` §1. All `[assumed]`
> claims that cannot be supported by evidence must be registered here.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

The assumptions register captures premises the synthesizer has treated as true
in the absence of supporting evidence. Each entry makes the assumption visible
so it can be tracked, challenged, and eventually confirmed or invalidated.

---

## Entry Schema

| Field | Type | Notes |
|---|---|---|
| `id` | `ASM-NNN` | Sequential, unique within engagement |
| `statement` | string | The premise treated as true |
| `basis` | string | Why the team made this assumption (evidence gap, time constraint, prior engagement, etc.) |
| `label` | `[assumed]` | Always `[assumed]` — validated by `label_producer_binding.py` |
| `source` | claim source | Must be `interview:<date>/consultant` or `from: <claim-id-A> + <claim-id-B>` |
| `conf` | `H \| M \| L` | Typically `L` or `M`; `H` requires justification |
| `requires_revalidation` | boolean | Default `true`; set `false` only if assumption is structural and unverifiable by design |
| `phase_introduced` | `00–06` | Phase in which the assumption was first recorded |
| `phase_expires` | `00–06` or `never` | Phase after which the assumption is expected to be confirmed or superseded |
| `target_phase` | phase id (optional) | Phase whose HITL gate must resolve this assumption; used by `assumption_resolution_required` validator rule |
| `invalidates_if_wrong` | list of claim ids | Claims that depend on this assumption and must be revisited if it is invalidated |
| `resolution_status` | `pending \| resolved \| deferred` (optional) | Set when the assumption is formally addressed in `target_phase`; required when `target_phase` is set and `requires_revalidation:true` |
| `resolved_in_phase` | phase id (optional) | Phase in which `resolution_status` was last updated |
| `resolution_note` | string (optional) | Required when `resolution_status:deferred`; explains why resolution was deferred and what conditions would require reopening the assumption |

---

## Worked Example

```yaml
---
id: ASM-003
statement: >
  The customer has no existing third-party vendor management policy or
  documented supplier-risk register.
basis: >
  No supplier register was visible in the customer portal at intake.
  Assumption made pending confirmation from the IT manager in Phase 01.
label: "[assumed]"
source: "interview:2026-05-25/consultant"
conf: M
requires_revalidation: true
phase_introduced: "00"
phase_expires: "01"
target_phase: "01-situation"
invalidates_if_wrong:
  - GAP-009
  - REC-012
resolution_status: resolved
resolved_in_phase: "01-situation"
resolution_note: "Confirmed — no vendor register found in customer portal (SIT-215). Assumption holds."
---
```

---

## Validator Notes

- `requires_revalidation: true` entries surface in `decay_check.py` output
  under **ASSUMPTIONS FLAGGED** once the entry has aged past `phase_expires`.
- `invalidates_if_wrong` pointers must reference valid claim ids in scope
  (enforced by `claim_composition_resolvable.py`).
- YAML blocks with `requires_revalidation: true` AND a non-empty `target_phase` are
  checked by `assumption_resolution_required.py`: `resolution_status` must be set to
  `pending`, `resolved`, or `deferred`. A `deferred` status requires a non-empty
  `resolution_note`. Blocks without `target_phase` are not checked by this rule.
