# Budget Register Schema

> **Canonical reference.** Defines the budget envelope shape for the engagement.
> Roadmap items reference `BUD-NNN` ids; the validator rejects roadmap items
> whose `budget_envelope` pointer does not resolve to an entry here.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## Purpose

The budget register captures the customer's financial constraints and
preferences in a structured form. It is **never** a single `total:` field —
budget is always expressed as envelope components so individual roadmap items
can be allocated to the correct pool.

A single `total:` field is forbidden by schema. The validator rejects any
`_budget.md` entry that uses `total` as the only expenditure field.

---

## Entry Schema

Each entry defines one named budget envelope that roadmap items can reference.

| Field | Type | Notes |
|---|---|---|
| `id` | `BUD-NNN` | Sequential, unique within engagement |
| `label` | string | Human-readable name for this envelope (e.g. `Security Uplift Y1`, `Infrastructure Refresh`) |
| `period` | string | Calendar period this envelope covers (e.g. `2026-FY`, `2026-Q3/Q4`, `Y1`) |
| `capex` | number or `tbc` | Capital expenditure ceiling for this envelope; `tbc` is allowed, absence is not |
| `opex_annual` | number or `tbc` | Recurring annual operational expenditure ceiling; absence forbidden |
| `renewals` | list of renewal objects | Existing contract renewals within this envelope (may be empty list `[]`) |
| `hard_limit` | number or null | Absolute ceiling the customer will not exceed under any circumstances |
| `soft_preference` | string or null | Qualitative guidance (e.g. "prefer opex over capex", "avoid multi-year commitments") |
| `currency` | string | ISO 4217 code (e.g. `EUR`, `GBP`); defaults to `EUR` if omitted |
| `notes` | string or null | Free-text context |

---

## Renewal Object Schema

| Field | Type | Notes |
|---|---|---|
| `description` | string | What is being renewed |
| `annual_cost` | number or `tbc` | |
| `renewal_date` | ISO-8601 date | |
| `negotiable` | boolean | Whether the customer is open to renegotiating or replacing this renewal |

---

## Register-level fields (file header)

```yaml
---
register: budget
phase_updated: "00"
harness_version: "0.1.0"
---
```

---

## Worked Example

```yaml
---
id: BUD-001
label: Security Uplift — Year 1
period: "2026-FY"
capex: 40000
opex_annual: 24000
renewals:
  - description: "Existing endpoint AV subscription (Sophos)"
    annual_cost: 3200
    renewal_date: "2026-11-30"
    negotiable: true
hard_limit: 75000
soft_preference: >
  Customer prefers opex-heavy solutions to avoid large upfront capital
  approval cycles. Multi-year vendor lock-in should be flagged explicitly.
currency: EUR
notes: >
  Envelope confirmed by CFO in intake interview 2026-05-25. Hard limit
  includes renewals. Does not cover business-continuity or DR spend (see BUD-002).
---
```

```yaml
---
id: BUD-002
label: Business Continuity and DR — Year 1
period: "2026-FY"
capex: tbc
opex_annual: 8000
renewals: []
hard_limit: null
soft_preference: "Preference for cloud-native DR over on-premises tape."
currency: EUR
notes: null
---
```

---

## Validator Notes

- A `_budget.md` entry using only a bare `total:` field (and no `capex`/
  `opex_annual` breakdown) is rejected.
- Roadmap item `budget_envelope` values must resolve to a `BUD-NNN` id
  declared in this file (`roadmap_item_required_fields.py`).
- `tbc` is a valid value for `capex` and `opex_annual`; a missing field is not.
