---
phase: "04-roadmap"
status: draft
harness_version: "0.1.0"
template: "roadmap@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. A '## Sequencing argument' H2 section exists and contains a written
     justification for the chosen sequencing of capability phases.
     (MANDATORY — absence is a validator violation; template_conformance.py.)
  2. At least one Y1 roadmap item carries `quick_win: true`.
     (MANDATORY — FR-26; roadmap_item_required_fields.py enforces >=1 Y1 quick-win.)
  3. Every roadmap item block is fully conformant with _claim.schema.md §2.4:
       - id: RMI-NNN (sequential, unique within engagement)
       - year: Y1 | Y2 | Y3
       - quick_win: boolean (present on every item)
       - capability_phase: foundations | enablers | value-drivers | optimisations
       - addresses: at least one REC-NNN (all ids must exist in recommendations.md)
       - compliance_role: constraint | deadline | enabler | none
         (MANDATORY — absent field is a validator violation)
       - compliance_deadline: ISO-8601 date
         (MANDATORY iff compliance_role: deadline; ABSENT otherwise)
       - budget_envelope: BUD-NNN
         (MANDATORY — must reference a declared entry in _budget.md)
       - owner: named person or role
  4. Every Y1 item is traceable (via its addresses field) back to >=1 gap.
  5. Every compliance item has a compliance_role value other than "none".
  6. The calendar projection (§3) covers Y1–Y3 with quarterly or half-year
     milestones grounded in the recommendations.
  7. Confidence-propagation holds: effective conf of each roadmap item
     ≤ min(conf of its addressed recommendations).
  8. Validator reports zero violations.
  9. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 04-roadmap.
  10. Consultant has reviewed and ratified via HITL gate 3.
  11. Frontmatter `status` changed to `ratified`; `ratified_by` and
      `ratified_at` filled before committing.

COMPLIANCE_ROLE RULE: compliance_role is MANDATORY on every roadmap item.
compliance_deadline is REQUIRED iff compliance_role is "deadline", and MUST
be absent otherwise. Absence of compliance_role is a validator error.

BUDGET_ENVELOPE RULE: budget_envelope is MANDATORY on every roadmap item.
The value must reference a BUD-NNN id declared in _budget.md. An unresolvable
reference is a validator error (roadmap_item_required_fields.py).

QUICK_WIN RULE: At least one Y1 item must carry quick_win: true (FR-26).
A roadmap with no Y1 quick-win is rejected by the validator.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Roadmap: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `roadmap@1.0.0`
> **Phase:** 04-roadmap
> **Entry condition:** `03-mapping/recommendations.md` frontmatter `status: ratified`

---

## Sequencing argument

<!--
MANDATORY H2 SECTION — must contain a written justification for the chosen
sequencing of capability phases. The validator checks for this H2 by name.
Explain: why foundations before enablers, which compliance deadlines drive
ordering, what dependencies exist between items, and the rationale for
quick-win selection.
-->

<[inferred] claim summarising the sequencing rationale.>
[inferred] [source:from: <list of REC-ids that drive sequencing>] [conf:M]

---

## 1. Roadmap Items

<!--
One YAML-fenced block per roadmap item. All items must reference recommendations
from 03-mapping/recommendations.md via the `addresses` field.

MANDATORY FIELDS ON EVERY BLOCK:
  - compliance_role (constraint | deadline | enabler | none)
  - compliance_deadline (REQUIRED iff compliance_role: deadline; ABSENT otherwise)
  - budget_envelope (must be a BUD-NNN id declared in _budget.md)
  - quick_win (boolean; at least one Y1 item must be true)

TEMPLATE USAGE:
  Copy the block below for each item. Assign sequential RMI-NNN ids.
  Replace ALL placeholder values before ratifying.
-->

```yaml
---
id: RMI-001
title: ""
year: Y1
quick_win: true
capability_phase: foundations
addresses:
  - REC-001
compliance_role: deadline
compliance_deadline: "YYYY-MM-DD"
budget_envelope: BUD-001
depends_on: []
owner: ""
risks:
  - RSK-001
---
```

<!-- Example of a non-quick-win item with compliance_role: constraint (no deadline): -->

```yaml
---
id: RMI-002
title: ""
year: Y1
quick_win: false
capability_phase: foundations
addresses:
  - REC-002
compliance_role: constraint
budget_envelope: BUD-001
depends_on:
  - RMI-001
owner: ""
risks: []
---
```

<!-- Example of an item with compliance_role: none (no compliance driver): -->

```yaml
---
id: RMI-003
title: ""
year: Y2
quick_win: false
capability_phase: enablers
addresses:
  - REC-003
compliance_role: none
budget_envelope: BUD-002
depends_on:
  - RMI-001
owner: ""
risks: []
---
```

---

## 2. Capability Phase Summary

<!--
Group items by capability_phase for a structured view of build progression.
Foundations must precede Enablers; Enablers precede Value-drivers; etc.
-->

### Foundations

| RMI-id | Title | Year | Quick win | Owner |
|--------|-------|------|-----------|-------|
| | | | | |

### Enablers

| RMI-id | Title | Year | Quick win | Owner |
|--------|-------|------|-----------|-------|
| | | | | |

### Value-drivers

| RMI-id | Title | Year | Quick win | Owner |
|--------|-------|------|-----------|-------|
| | | | | |

### Optimisations

| RMI-id | Title | Year | Quick win | Owner |
|--------|-------|------|-----------|-------|
| | | | | |

---

## 3. Calendar Projection

<!--
Quarterly or half-year milestones for Y1–Y3. Each milestone must be traceable
to at least one RMI-NNN id.
-->

| Period | Milestone | RMI-ids | Notes |
|--------|-----------|---------|-------|
| Y1-H1 | | | |
| Y1-H2 | | | |
| Y2-H1 | | | |
| Y2-H2 | | | |
| Y3-H1 | | | |
| Y3-H2 | | | |

---

## 4. Compliance Items

<!--
All items where compliance_role != "none". Summarises compliance coverage
for the handover phase. Deadline items must carry compliance_deadline.
-->

| RMI-id | Compliance role | Deadline | CMP-ids addressed |
|--------|-----------------|----------|-------------------|
| | | | |

---

## 5. Budget Overview

<!--
Cross-reference to _budget.md envelopes used in this roadmap.
Not a replacement for _budget.md — a navigation aid.
-->

| BUD-id | Envelope description | RMI-ids drawing on this envelope |
|--------|---------------------|----------------------------------|
| | | |

---

## 6. Risks and Mitigations

<!--
Risks from _risks.md referenced by roadmap items. Summary for the handover phase.
-->

| RSK-id | Title | Likelihood | Impact | Mitigation summary | Referenced by (RMI-ids) |
|--------|-------|-----------|--------|--------------------|-------------------------|
| | | | | | |

---

## 7. Contradictions Surfaced This Phase

<!--
Mirror of _contradictions.md rows relevant to this phase.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 04-roadmap.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## 8. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
