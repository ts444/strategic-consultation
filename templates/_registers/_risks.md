# Risks Register Schema

> **Canonical reference.** Binds to `_claim.schema.md` §2.3. All risk blocks
> used in any phase artifact must conform to this schema.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

The risks register is the single list of identified risks across the engagement.
Risks are referenced by id (`RSK-NNN`) from gap blocks, recommendation blocks,
roadmap items, and the handover document.

---

## Entry Schema

See `_claim.schema.md` §2.3 for the full Risk block schema. The fields are
reproduced here for register-level context.

| Field | Type | Notes |
|---|---|---|
| `id` | `RSK-NNN` | Sequential, unique within engagement |
| `title` | string | |
| `description` | claim | `[inferred]` or `[assumed]`; must carry `[source:…]` and `[conf:…]` |
| `likelihood` | `low \| medium \| high` | |
| `impact` | `low \| medium \| high` | |
| `owner` | string | Named person or role |
| `mitigation` | string | Direction or action; `pending` is permitted temporarily |
| `triggered_by` | list of claim ids | Must be resolvable (enforced by validator) |
| `status` | `open \| mitigated \| accepted \| closed` | Lifecycle state |
| `phase_identified` | `00–06` | Phase when the risk was first recorded |

---

## Register-level fields (file header)

The register file carries YAML frontmatter:

```yaml
---
register: risks
phase_updated: "02"
harness_version: "0.1.0"
---
```

---

## Worked Example

```yaml
---
id: RSK-003
title: Credential compromise during PAM migration window
description: >
  Between REC-007 go-live planning and actual CyberArk deployment there is a
  period (estimated 6–10 weeks) where domain admin accounts remain under the
  current weak controls. A targeted attack in this window could achieve full
  domain compromise.
  [inferred] [source:from: GAP-004 + REC-007] [conf:M]
likelihood: medium
impact: high
owner: Customer CISO (placeholder)
mitigation: >
  Accelerate deployment timeline; add temporary break-glass monitoring via
  SIEM during migration window. See REC-011.
triggered_by:
  - GAP-004
  - REC-007
status: open
phase_identified: "03"
---
```

---

## Validator Notes

- `triggered_by` ids must resolve to in-scope claims
  (`claim_composition_resolvable.py`).
- `description` conf ≤ min(conf of `triggered_by` claims)
  (`confidence_propagation.py`).
- `status: mitigated` requires a `mitigation` field that is not `pending`.
