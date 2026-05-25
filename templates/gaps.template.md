---
phase: "02-gap"
status: draft
harness_version: "0.1.0"
template: "gaps@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. Every goal declared in 00-intake/scope.md is either:
       (a) addressed by at least one gap block in this document, OR
       (b) explicitly marked "no gap" with a written reasoning entry in §3.
  2. Every gap block is fully conformant with _claim.schema.md §2.1:
       - id: GAP-NNN (sequential, unique within engagement)
       - compliance_drivers: <list of CMP-NNN ids> (empty list [] is valid;
         field must always be present — absence is a validator violation)
       - current_state: [known] or [elicited] claim with source
       - desired_state: [elicited] or [inferred] claim with source
       - gap_description: [inferred] or [assumed] claim with from: composition
       - severity: critical | high | medium | low
       - evidence: list of SIT-ids from situation phase
  3. Validator reports zero violations (claim atoms, labels, sources, confidence,
     compliance_drivers field on every gap, no broken CMP-id pointers).
  4. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 02-gap.
  5. Consultant has ratified via HITL gate 3.
  6. Frontmatter `status` is changed to `ratified` and `ratified_by` /
     `ratified_at` are filled before committing.

COMPLIANCE_DRIVERS RULE: The `compliance_drivers` field is MANDATORY on every
gap block. An empty list `[]` is valid (means the gap has no compliance driver).
A missing field is a validator error. Broken CMP-NNN pointers (ids not in
_compliance.md) are a validator error.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Gap Analysis: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `gaps@1.0.0`
> **Phase:** 02-gap
> **Entry condition:** `01-situation/situation.md` frontmatter `status: ratified`

---

## 1. Goal Coverage Map

<!--
Every goal from scope.md must appear in this table.
Column "addressed by" lists GAP-ids or "no gap" with a reason reference.
This table is the validator's check for the "every goal mapped" exit criterion.
-->

| Goal # | Goal summary | Addressed by (GAP-ids) | No-gap reason (§3 ref) |
|--------|--------------|------------------------|------------------------|
| G-01 | | | |
| G-02 | | | |
| G-03 | | | |

---

## 2. Gap Blocks

<!--
One YAML-fenced block per gap. The synthesizer fills these from situation-phase
claim ids. The validator checks every field.

TEMPLATE USAGE:
  Copy the block below for each gap. Do not leave placeholder ids (GAP-NNN)
  in committed artifacts — assign sequential ids starting from GAP-001.

COMPLIANCE_DRIVERS: MANDATORY on every block. Use [] if no compliance driver.
Do not omit the field. Broken CMP-ids (not declared in _compliance.md) are
rejected by gap_compliance_drivers_field.py.
-->

```yaml
---
id: GAP-001
title: ""
current_state: >
  <[known] or [elicited] claim describing actual current state.>
  [known] [source:customer-portal://<resource>/<id>@<updated_at>] [conf:H]
desired_state: >
  <[elicited] or [inferred] claim describing the target state.>
  [elicited] [source:interview:<YYYY-MM-DD>/consultant] [conf:M]
gap_description: >
  <[inferred] or [assumed] claim naming the shortfall.
   conf must be <= min(conf(current_state), conf(desired_state)).>
  [inferred] [source:from: GAP-001.current_state + GAP-001.desired_state] [conf:M]
compliance_drivers:
  - CMP-001
severity: high
evidence:
  - SIT-001
---
```

<!-- Repeat block for each gap. Example of a gap with no compliance driver: -->

```yaml
---
id: GAP-002
title: ""
current_state: >
  [known] [source:customer-portal://<resource>/<id>@<updated_at>] [conf:H]
desired_state: >
  [elicited] [source:interview:<YYYY-MM-DD>/consultant] [conf:M]
gap_description: >
  [inferred] [source:from: GAP-002.current_state + GAP-002.desired_state] [conf:M]
compliance_drivers: []
severity: medium
evidence:
  - SIT-002
---
```

---

## 3. Goals With No Gap

<!--
Goals that exist in scope.md but require no corrective action. Each entry
must give a written reason why no gap exists. The goal-coverage-map (§1)
references this section's row numbers.
-->

| Goal # | Reason no gap exists | Evidence (SIT-ids) |
|--------|---------------------|---------------------|
| | | |

---

## 4. Compliance Coverage Summary

<!--
For each CMP-NNN item in _compliance.md, which gaps address it?
This is a cross-reference for the mapping phase, not an additional validator check.
Empty means the compliance item is not yet addressed by any gap — which may
itself be a gap to add.
-->

| CMP-id | Compliance item | Addressed by (GAP-ids) | Notes |
|--------|----------------|------------------------|-------|
| | | | |

---

## 5. Contradictions Surfaced This Phase

<!--
Mirror of _contradictions.md rows relevant to this phase.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 02-gap.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## 6. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
