---
phase: "03-mapping"
status: draft
harness_version: "0.1.0"
template: "recommendations@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. Every recommendation block is fully conformant with _claim.schema.md §2.2:
       - id: REC-NNN (sequential, unique within engagement)
       - addresses: at least one GAP-NNN (all ids must exist in gaps.md)
       - proposed_service: named portfolio service OR "[no-known-service]"
       - rationale: [inferred] claim with from: composition source
       - compliance_relation: addresses | partially-addresses | irrelevant
         (MANDATORY — absent field is a validator violation)
       - cost: structured (capex/opex or tbc); MANDATORY — absent field is a
         validator violation; "tbc" is valid; absence is not
       - lock_in: explicit assessment; MANDATORY — "none" is valid; absence is not
       - opportunity_cost: explicit assessment; MANDATORY — "none" is valid; absence is not
  2. Every gap from gaps.md is addressed by at least one recommendation OR
     has a recorded "[no-known-service]" recommendation with rationale.
  3. Confidence-propagation holds: conf(rationale) ≤ min(conf of input claims).
  4. No bare framework names (GDPR, NIS2, ISO27001, DORA, etc.) in titles or
     structured fields — reference CMP-NNN ids instead.
  5. Validator reports zero violations.
  6. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 03-mapping.
  7. Consultant has reviewed and ratified via HITL gate 3.
  8. Frontmatter `status` changed to `ratified`; `ratified_by` and
     `ratified_at` filled before committing.

FOUR MANDATORY FIELDS: compliance_relation, cost, lock_in, and opportunity_cost
are REQUIRED on every recommendation block. Using "none" or "tbc" is valid.
Omitting any of these fields is a validator error (recommendation_required_fields.py).

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Recommendations (Curated): {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `recommendations@1.0.0`
> **Phase:** 03-mapping
> **Entry condition:** `02-gap/gaps.md` frontmatter `status: ratified`
> **Companion artifact:** `03-mapping/service-map.md` (exhaustive mapping)

---

## 1. Recommendation Coverage

| REC-id | Title | Addresses (GAP-ids) | Compliance relation |
|--------|-------|---------------------|---------------------|
| REC-001 | | | |
| REC-002 | | | |

---

## 2. Recommendation Blocks

<!--
One YAML-fenced block per recommendation. These are the CURATED subset of
mappings from service-map.md — the synthesizer selects the highest-value
service per gap, discarding lower-fit candidates.

TEMPLATE USAGE:
  Copy the block below for each recommendation. Assign sequential REC-NNN ids.
  All four fields (compliance_relation, cost, lock_in, opportunity_cost) are
  MANDATORY. "none" and "tbc" are valid values; absence is not.

COMPLIANCE_RELATION VALUES:
  - addresses            — recommendation directly closes the compliance requirement
  - partially-addresses  — recommendation partially closes; residual gap remains
  - irrelevant           — gap has no compliance driver (compliance_drivers: [])
-->

```yaml
---
id: REC-001
title: ""
addresses:
  - GAP-001
proposed_service: "<Portfolio service name or [no-known-service]>"
rationale: >
  <[inferred] claim explaining why this service best addresses the gap(s).>
  [inferred] [source:from: GAP-001 + portfolio://<domain>/<file>.md@<git-sha>] [conf:M]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 0
  notes: "tbc — to be confirmed with portfolio pricing"
lock_in: >
  <Explicit lock-in assessment. "none" is a valid value; absence is not.>
opportunity_cost: >
  <What the customer foregoes by choosing this option. "none" is valid; absence is not.>
---
```

<!-- Example with no compliance driver and [no-known-service]: -->

```yaml
---
id: REC-002
title: ""
addresses:
  - GAP-002
proposed_service: "[no-known-service]"
rationale: >
  No portfolio service addresses this gap. Recommend customer seeks a
  third-party vendor. Gap flagged in retro change-request backlog.
  [inferred] [source:from: GAP-002 + portfolio://<domain>/<file>.md@<git-sha>] [conf:L]
compliance_relation: irrelevant
cost:
  capex: tbc
  opex_monthly: tbc
  notes: "Third-party pricing unknown; to be determined during vendor selection."
lock_in: >
  Unknown until vendor selected.
opportunity_cost: >
  none
---
```

---

## 3. Gap Coverage Summary

<!--
Confirms every gap from gaps.md is addressed by at least one recommendation.
-->

| GAP-id | Addressed by (REC-ids) | Coverage note |
|--------|------------------------|---------------|
| | | |

---

## 4. Contradictions Surfaced This Phase

<!--
Mirror of _contradictions.md rows relevant to this phase.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 03-mapping.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## 5. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
