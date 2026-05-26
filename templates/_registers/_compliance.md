# Compliance Register Schema

> **Canonical reference.** Every compliance obligation, framework requirement,
> or regulatory constraint in scope must be registered here. Gaps, recommendations,
> and roadmap items reference `CMP-NNN` ids.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

The compliance register gives structured ids to every regulatory or contractual
requirement in scope. This prevents bare framework names from appearing in
structured fields of gaps and roadmap items (enforced by
`framework_name_in_structured_fields.py`).

---

## Entry Schema

| Field | Type | Notes |
|---|---|---|
| `id` | `CMP-NNN` | Sequential, unique within engagement |
| `framework` | string | Name of the framework or regulation (e.g. `NIS2`, `ISO27001`) |
| `clause` | string | Specific clause, control, or article (e.g. `A.9.2.3`, `Art.21(2)(e)`) |
| `description` | string | Plain-language summary of the obligation |
| `role` | `constraint \| deadline \| enabler` | How this compliance item shapes the engagement |
| `deadline` | ISO-8601 date | **Required iff `role: deadline`**; must be omitted when `role` is `constraint` or `enabler` |
| `source` | source URI | Where this obligation was established (e.g. customer-portal compliance posture) |
| `in_scope` | boolean | `true` if active for this engagement; `false` to mark as out-of-scope without deleting |

---

## Role Semantics

| Role | Meaning |
|---|---|
| `constraint` | The engagement must respect this requirement as a hard boundary (e.g. data residency, contractual prohibition) |
| `deadline` | There is a binding date by which a control must be in place; `deadline` field is mandatory |
| `enabler` | Achieving this compliance item unlocks a commercial opportunity or removes a future blocker |

---

## Register-level fields (file header)

```yaml
---
register: compliance
phase_updated: "00"
harness_version: "0.1.0"
---
```

---

## Worked Example

```yaml
---
id: CMP-002
framework: ISO27001
clause: "A.9.2.3"
description: >
  Management of privileged access rights: formal process for authorisation,
  review, and revocation of privileged accounts.
role: deadline
deadline: "2026-12-31"
source: "customer-portal://compliance-posture/cmp-iso27001@2026-05-01T08:00:00Z"
in_scope: true
---
```

```yaml
---
id: CMP-005
framework: NIS2
clause: "Art.21(2)(e)"
description: >
  Entities must have processes to acquire, develop and maintain secure systems
  including vulnerability handling and disclosure.
role: constraint
source: "customer-portal://compliance-posture/cmp-nis2@2026-05-01T08:00:00Z"
in_scope: true
---
```

---

## Validator Notes

- `deadline` is **required** when `role: deadline` and **must be absent** when
  `role` is `constraint` or `enabler`.
- Gaps must reference valid `CMP-NNN` ids from this register in their
  `compliance_drivers` field (`gap_compliance_drivers_field.py`).
- Bare framework names (e.g. `NIS2`, `ISO27001`) may appear only in
  narrative prose, not in structured fields. Use `CMP-NNN` references in
  structured fields.
