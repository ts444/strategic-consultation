---
phase: "00-intake"
status: draft
harness_version: "0.1.0"
template: "scope@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "interviewer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. All engagement goals are specific, measurable, and tied to a named business driver.
  2. All declared constraints (budget envelope shape, compliance frameworks, contracts,
     skills, political) are listed.
  3. Stakeholder list is complete with at least one named primary contact.
  4. Out-of-scope items are explicit (prevents silent omission at later phases).
  5. Consultant has confirmed entry via HITL gate 1 and ratified this artifact
     via HITL gate 3.
  6. Validator reports zero violations.
  7. Frontmatter `status` is changed to `ratified` and `ratified_by` / `ratified_at`
     are filled before committing.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Scope: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `scope@1.0.0`
> **Phase:** 00-intake

---

## 1. Customer Overview

<!-- [elicited] claims only in this section — sourced to interview:<date>/consultant -->

**Customer name:** {{CUSTOMER_NAME}}

**Industry / sector:**

**Size (headcount, revenue band):**

**Primary IT model** (in-house / fully managed / hybrid):

**Engagement motivation** (why now):

---

## 2. Engagement Goals

<!--
Each goal must be specific, measurable, and tied to a named business driver
(design-principles §3: "Goals must be specific, measurable, and tied to a business driver").
Format: claim atom — [elicited] [source:interview:<date>/consultant] [conf:H|M|L]
-->

| # | Goal | Business driver | Success measure |
|---|------|-----------------|-----------------|
| G-01 | | | |
| G-02 | | | |
| G-03 | | | |

<!-- Add rows as needed. Every goal must appear in gap analysis or be explicitly marked 'no gap'. -->

---

## 3. Constraints

<!--
Hard inputs; the agent must not route around them (design-principles §3).
Include: budget envelope shape, compliance deadlines, contractual obligations,
skills availability, political/organisational constraints.
Each constraint is a [elicited] claim.
-->

### 3.1 Budget Envelope

<!--
State *shape*, not a single total (design-principles §4: "Budget is a shape").
Populate _budget.md with BUD-NNN envelopes; reference them here by id.
-->

| Envelope | Capex | Opex/yr | Hard limit | Notes |
|----------|-------|---------|------------|-------|
| BUD-001 | | | | |

### 3.2 Compliance Frameworks

<!--
List every declared framework. Populate _compliance.md with CMP-NNN items;
reference them here. Bare framework names in this table are acceptable
(they are labels, not structured fields — see design-principles §4).
-->

| # | Framework | Role (constraint / deadline / enabler) | Deadline (if any) | CMP-id |
|---|-----------|----------------------------------------|--------------------|--------|
| | | | | |

### 3.3 Contractual and Operational Constraints

<!-- SLAs, existing vendor lock-in, end-of-support cliffs, etc. -->

### 3.4 Skills and Capacity Constraints

### 3.5 Political / Organisational Constraints

---

## 4. Stakeholders

<!--
At least one named primary contact is required before ratification.
Format: [elicited] [source:interview:<date>/consultant] [conf:H]
-->

| Name | Role | Involvement | Primary contact? |
|------|------|-------------|-----------------|
| | | | |

---

## 5. Out of Scope

<!--
Explicit exclusions prevent silent omission later and surface disagreements early.
Each item should note *why* it is out of scope.
-->

| Item | Reason out of scope |
|------|---------------------|
| | |

---

## 6. Assumptions at Intake

<!--
Record any assumptions the interviewer or consultant is making at this stage.
These are provisional; each must be entered in _assumptions.md as ASM-NNN entries.
-->

| ASM-id | Assumption | Source | Requires revalidation? |
|--------|-----------|--------|------------------------|
| | | | |

---

## 7. Open Questions

<!--
Questions that emerged during intake but could not be resolved in this session.
Each becomes a potential [elicited] claim in phase 01 if pursued.
-->

| # | Question | Owner | Target phase |
|---|----------|-------|--------------|
| | | | |

---

## 8. HITL Confirmation Record

<!--
Filled by the orchestrator at each gate. Do not edit manually.
-->

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
