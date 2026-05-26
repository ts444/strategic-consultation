---
phase: "00-intake"
status: ratified
harness_version: "0.2.0"
template: "scope@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T00:00:00Z"
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

# Scope: Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `scope@1.0.0`
> **Phase:** 00-intake

---

## 1. Customer Overview

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

**Customer name:** Meridian-Logistics

**Industry / sector:** Logistics and freight; specialist automotive logistics partner to OEM and tier-1 automotive customers.

**Size (headcount, revenue band):** Not confirmed at intake — open question for phase 01.

**Primary IT model:** Hybrid — small internal IT team handling operational basics; new MSP engaged to lead the security and compliance programme. MSP working areas to be defined in phase 03-mapping.

**Engagement motivation (why now):** Dual pressure: (1) TISAX label required by existing automotive customer contracts, with a December 2026 assessment already booked — failure to achieve the label puts those contracts at risk; (2) NIS2 Directive regulatory obligation as a logistics operator, with a 12-month compliance horizon.

---

## 2. Engagement Goals

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

| # | Goal | Business driver | Success measure |
|---|------|-----------------|-----------------|
| G-01 | Achieve attestation under the NIS2 Directive within 12 months | Regulatory obligation — Meridian-Logistics is in scope as a logistics operator | NIS2 attestation / supervisory authority confirmation obtained by 2027-05-26 |
| G-02 | Achieve TISAX label by December 2026 | Contractual requirement — existing automotive customer contracts require TISAX certification; contract retention at risk if label is not achieved | TISAX label awarded at the December 2026 assessment (see CMP-002) |
| G-03 | Build and operationalise a working Incident Response process | Operational resilience — customer requirement is not merely paper compliance but a demonstrably functional IR capability | IR process documented, staff trained, and at least one tabletop exercise completed before TISAX assessment |

---

## 3. Constraints

### 3.1 Budget Envelope

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

| Envelope | Capex yr 1 | Opex/yr | Hard limit | Notes |
|----------|-----------|---------|------------|-------|
| BUD-001 | £50,000 | £20,000 | £200,000 | Shape declared at engagement open; binding across all phases |

### 3.2 Compliance Frameworks

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

| # | Framework | Role | Deadline | CMP-id |
|---|-----------|------|----------|--------|
| 1 | NIS2 Directive | Regulatory constraint | 2027-05-26 (12-month horizon; national supervisory authority date TBC — see ASM-001) | CMP-001 |
| 2 | TISAX | Contractual constraint | December 2026 (assessment booked) | CMP-002 |

### 3.3 Contractual and Operational Constraints

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

Meridian-Logistics holds active contracts with automotive OEM and/or tier-1 customers that
require a valid TISAX label as a condition of contract. The December 2026 assessment
window is fixed; slippage would trigger contract breach risk. This makes G-02 (see CMP-002)
the highest-priority time-bound goal.

### 3.4 Skills and Capacity Constraints

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

Internal security capability is limited to the CISO (Izayoi Nayuta) and a small IT team
responsible for operational basics. The engagement is therefore MSP-led. The MSP must
supply the specialist security capability required to meet G-01, G-02, and G-03.
Exact MSP working areas are deferred to phase 03-mapping (see OQ-01 and ASM-002).

### 3.5 Political / Organisational Constraints

<!-- No political or organisational constraints elicited at intake. To be probed in phase 01-situation. -->

---

## 4. Stakeholders

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

| Name | Role | Involvement | Primary contact? |
|------|------|-------------|-----------------|
| Cheng Zebang | CEO | Executive sponsor; accountable for contract obligations and strategic direction | No |
| Izayoi Nayuta | CISO | Day-to-day engagement owner; approves deliverables, coordinates system and staff access, owns compliance programme | **Yes** |

---

## 5. Out of Scope

[elicited] [source:interview:2026-05-26/consultant] [conf:H]

| Item | Reason out of scope |
|------|---------------------|
| OOS-01: Physical security | Explicitly excluded by customer; managed separately outside this engagement |
| OOS-02: Active security testing (penetration testing) | Explicitly excluded by customer; not part of this engagement's mandate |
| OOS-03: Secure development / SDLC | Explicitly excluded by customer; deferred or handled internally |

---

## 6. Assumptions at Intake

| ASM-id | Assumption | Source | Requires revalidation? |
|--------|-----------|--------|------------------------|
| ASM-001 | No earlier NIS2 supervisory authority enforcement date exists that would require attestation before the 12-month horizon | [elicited] [source:interview:2026-05-26/consultant] [conf:M] | Yes — confirm with Izayoi Nayuta in phase 01 |
| ASM-002 | MSP is contracted and resourced to deliver security controls beyond internal IT team basics; exact responsibility split TBD in phase 03 | [elicited] [source:interview:2026-05-26/consultant] [conf:M] | Yes — resolve in phase 03-mapping |
| ASM-003 | TISAX assessment is at Assessment Level 2 (AL2); if AL3 is required, scope and effort increase materially | [elicited] [source:interview:2026-05-26/consultant] [conf:M] | Yes — confirm with Izayoi Nayuta in phase 01 |

---

## 7. Open Questions

| # | Question | Owner | Target phase |
|---|----------|-------|--------------|
| OQ-01 | Which security controls, workstreams, and domains will the MSP own versus the internal IT team? | Izayoi Nayuta + MSP | 03-mapping |
| OQ-02 | What is Meridian-Logistics's headcount and revenue band? (Relevant for NIS2 entity classification — essential vs important) | Izayoi Nayuta | 01-situation |
| OQ-03 | Has a national supervisory authority contact or audit date been communicated by the relevant NIS2 competent authority? | Izayoi Nayuta | 01-situation |
| OQ-04 | What TISAX assessment level (AL2 or AL3) do the automotive customer contracts require? | Izayoi Nayuta | 01-situation |

---

## 8. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T00:00:00Z | All four entry checklist items confirmed YES |
| Gate 3 — ratification | 2026-05-26T00:00:00Z | Consultant confirmed YES — scope.md ratified |
