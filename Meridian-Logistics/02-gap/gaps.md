---
phase: "02-gap"
status: ratified
harness_version: "0.2.0"
template: "gaps@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T10:15:00Z"
produced_by: "synthesizer"
---

# Gap Analysis: Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `gaps@1.0.0`
> **Phase:** 02-gap
> **Entry condition:** `01-situation/situation.md` frontmatter `status: ratified`

## 1. Goal Coverage Map

| Goal | Description | Addressed by (GAP-ids) |
|------|-------------|------------------------|
| G-01 | Achieve attestation under the NIS2 Directive within 12 months | GAP-001, GAP-002, GAP-003, GAP-004, GAP-005, GAP-006, GAP-007, GAP-008, GAP-009 |
| G-02 | Achieve TISAX label by December 2026 | GAP-001, GAP-002, GAP-003, GAP-004, GAP-005, GAP-006, GAP-007, GAP-008 |
| G-03 | Build and operationalise a working Incident Response process | GAP-002 |

## §2 Gap Blocks

```yaml
---
id: GAP-001
title: "No SIEM / centralised security monitoring capability"
current_state: >
  No SIEM, NDR, or Threat Intelligence service is contracted; the customer
  has no centralised log aggregation or security event detection capability.
  [inferred] [source:customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
desired_state: >
  Centralised security monitoring with log aggregation, incident detection,
  and NIS2-mapped compliance reporting is operational and evidenced for
  audit before TISAX assessment (Dec 2026) and NIS2 deadline (May 2027).
  [inferred] [source:from: CMP-001 NIS2 Art.21 logging/detection + CMP-002 TISAX AL2 monitoring control] [conf:H]
gap_description: >
  Customer lacks any contracted SIEM/monitoring capability required by both
  NIS2 (log aggregation, incident detection) and TISAX AL2 (security
  monitoring), creating a critical compliance and detection shortfall.
  [inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + CMP-001/CMP-002 monitoring requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: critical
evidence:
  - SIT-115
  - SIT-001
  - SIT-002
---
```

```yaml
---
id: GAP-002
title: "No Incident Response capability"
current_state: >
  No Incident Response, Business Continuity, or DFIR retainer service is
  contracted; a 2025 ransomware attack was paid in full because internal
  incident response capability was inadequate.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
desired_state: >
  A documented Incident Response process is operational, staff are trained,
  and a tabletop exercise has been completed before the TISAX assessment
  in December 2026.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
gap_description: >
  Customer has no contracted or internal IR capability and a demonstrated
  prior failure (2025 ransomware, full ransom paid); G-03 mandates a
  documented, trained, and tabletop-tested IR process before TISAX.
  [inferred] [source:from: interview:2026-05-26/consultant + interview:2026-05-26/consultant] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: critical
evidence:
  - SIT-115
  - SIT-214
  - SIT-006
---
```

```yaml
---
id: GAP-003
title: "No Business Continuity Plan or BC service"
current_state: >
  No Business Continuity service is contracted; no BCP documentation,
  stakeholder notification templates, or tabletop facilitation exists
  from MSP coverage.
  [inferred] [source:customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
desired_state: >
  A documented and tested business continuity plan exists covering
  containment, communication, and tabletop exercise — satisfying NIS2
  Article 21 BC measures and TISAX AL2 BCP documentation/testing.
  [inferred] [source:from: CMP-001 NIS2 Art.21 BC measures + CMP-002 TISAX AL2 BCP requirements] [conf:H]
gap_description: >
  Customer has no contracted or in-house BC capability; NIS2 Art.21 and
  TISAX AL2 both require documented and tested BC measures, leaving a
  critical compliance shortfall ahead of both deadlines.
  [inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + CMP-001/CMP-002 BC requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: critical
evidence:
  - SIT-115
  - SIT-004
  - SIT-005
  - SIT-007
---
```

```yaml
---
id: GAP-004
title: "Outdated and unenforced information security policy framework"
current_state: >
  Existing IT and information security policies are described as outdated
  and not in active use; governance is informal with no formal steering
  committee.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
desired_state: >
  Current, approved, and actively-enforced IS policy framework is in place
  with documented governance, satisfying NIS2 governance/policy obligations
  and TISAX AL2 documented-and-enforced IS policy requirements.
  [inferred] [source:from: CMP-001 NIS2 governance requirements + CMP-002 TISAX AL2 IS policy controls] [conf:H]
gap_description: >
  Customer's IS policies are outdated and unused, and governance is
  informal; both NIS2 and TISAX AL2 require documented and enforced IS
  policies plus governance evidence, creating a high-severity shortfall.
  [inferred] [source:from: interview:2026-05-26/consultant + CMP-001/CMP-002 policy requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: high
evidence:
  - SIT-204
  - SIT-205
---
```

```yaml
---
id: GAP-005
title: "MFA enforcement maturity unconfirmed despite contracted IAM capability"
current_state: >
  Gold-SLA IAM is contracted (covers PIM/PAM/SSO/MFA) and healthy, but
  staff resistance to flexibility-reducing controls — notably MFA — means
  effective enforcement maturity across the 240-person workforce is
  unconfirmed.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
desired_state: >
  MFA is enforced for all users across all in-scope systems with measurable
  coverage and exception handling, meeting NIS2 access-control obligations
  and TISAX AL2 strong-authentication requirements.
  [inferred] [source:from: CMP-001 NIS2 access control + CMP-002 TISAX AL2 authentication controls] [conf:H]
gap_description: >
  Contracted IAM capability exists but cultural resistance has prevented
  confirmed MFA enforcement; both NIS2 and TISAX AL2 require effective MFA
  enforcement, leaving a high-severity execution gap rather than a
  capability gap.
  [inferred] [source:from: interview:2026-05-26/consultant + CMP-001/CMP-002 authentication requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: high
evidence:
  - SIT-109
  - SIT-012
  - SIT-213
---
```

```yaml
---
id: GAP-006
title: "Lapsed security service contracts — Device Hardening and Mail Security"
current_state: >
  Device Hardening (cs-mer-10) and Mail Security (cs-mer-7) contracts both
  ended 2026-05-25 (today) and are in renewal grace period; continuity of
  endpoint hardening and mail/DLP coverage is therefore not guaranteed.
  [inferred] [source:customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
desired_state: >
  Endpoint hardening (CIS baselines, deviation reporting) and mail security
  (sandboxing, SPF/DKIM/DMARC, outbound DLP) are continuously contracted
  and evidenced as part of the TISAX AL2 assessment evidence trail.
  [inferred] [source:from: CMP-002 TISAX AL2 continuous control coverage + CMP-001 NIS2 technical measures] [conf:H]
gap_description: >
  Two TISAX-relevant security controls have lapsed contractual coverage
  on the same day as ratification; TISAX AL2 assessment requires
  continuous, evidenced control coverage, creating a high-severity gap.
  [inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + CMP-001/CMP-002 continuous-control requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: high
evidence:
  - SIT-113
  - SIT-114
  - SIT-209
  - SIT-020
  - SIT-022
---
```

```yaml
---
id: GAP-007
title: "IT governance and change management deficit"
current_state: >
  IT Change Management (cs-mer-15) is in Incident status and its contract
  ended 2026-05-25; IT governance is informal (no steering committee) and
  strategic decisions are made ad hoc between CEO, CISO, and CTO.
  [inferred] [source:customer-portal://contracts/cs-mer-15@2026-05-25T16:50:36.223Z] [conf:H]
desired_state: >
  Documented and operational IT change management process with audit
  trail, and formal governance forum producing evidence required by NIS2
  governance obligations and TISAX AL2 change-management controls.
  [inferred] [source:from: CMP-001 NIS2 governance + CMP-002 TISAX AL2 change management] [conf:H]
gap_description: >
  Customer's primary change-management service is in Incident status with
  a lapsed contract, and governance is informal with no audit discipline;
  NIS2 and TISAX AL2 both require evidenced change and governance
  processes.
  [inferred] [source:from: customer-portal://contracts/cs-mer-15@2026-05-25T16:50:36.223Z + CMP-001/CMP-002 governance requirements] [conf:H]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: high
evidence:
  - SIT-106
  - SIT-117
  - SIT-205
  - SIT-209
  - SIT-037
---
```

```yaml
---
id: GAP-008
title: "Incomplete IT asset inventory"
current_state: >
  Customer portal asset registry records only 25 devices, 25 users, and
  10 licences against an actual headcount of 240; the registry is
  confirmed incomplete by the customer.
  [inferred] [source:customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z] [conf:H]
desired_state: >
  A complete, accurate, and maintained IT asset inventory (devices, users,
  licences) underpinning vulnerability, access, and risk management,
  satisfying NIS2 asset-management obligations and TISAX AL2 inventory
  requirements.
  [inferred] [source:from: CMP-001 NIS2 asset management + CMP-002 TISAX AL2 inventory controls] [conf:H]
gap_description: >
  Asset inventory captures roughly 10% of the workforce/device estate;
  NIS2 and TISAX AL2 require a complete and accurate inventory as the
  foundation of risk and access control, creating a medium-severity gap.
  [inferred] [source:from: customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z + CMP-001/CMP-002 inventory requirements] [conf:M]
compliance_drivers:
  - CMP-001
  - CMP-002
severity: medium
evidence:
  - SIT-101
  - SIT-103
  - SIT-208
---
```

```yaml
---
id: GAP-009
title: "CMP-001 entity classification not validated with national supervisory authority"
current_state: >
  No NIS2 supervisory authority contact has been received; the customer's
  entity classification (essential vs important) under NIS2 has not been
  confirmed with the national competent authority despite the 240-employee
  / ~£10M revenue profile suggesting "important entity" scope.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
desired_state: >
  NIS2 entity classification is formally confirmed with the national
  competent authority, so that the scope of NIS2 obligations and
  attestation requirements is known and planned for ahead of the
  2027-05-26 deadline.
  [inferred] [source:interview:2026-05-26/consultant] [conf:H]
gap_description: >
  Customer's NIS2 classification is unconfirmed with the supervisory
  authority, so the precise scope of NIS2 obligations cannot be fixed;
  this is a medium-severity prerequisite gap to the NIS2 attestation goal.
  [inferred] [source:from: interview:2026-05-26/consultant + interview:2026-05-26/consultant] [conf:H]
compliance_drivers:
  - CMP-001
severity: medium
evidence:
  - SIT-201
  - SIT-211
---
```

## §3 Goals With No Gap

All goals addressed by gap blocks in §2.

## §4 Compliance Coverage Summary

| CMP-id | Compliance item | Addressed by (GAP-ids) | Notes |
|--------|-----------------|------------------------|-------|
| CMP-001 | NIS2 Directive (attestation by 2027-05-26) | GAP-001, GAP-002, GAP-003, GAP-004, GAP-005, GAP-006, GAP-007, GAP-008, GAP-009 | Entity classification (GAP-009) is a prerequisite for scoping the remaining NIS2 obligations. |
| CMP-002 | TISAX AL2 (assessment December 2026) | GAP-001, GAP-002, GAP-003, GAP-004, GAP-005, GAP-006, GAP-007, GAP-008 | All TISAX-mapped gaps must close ahead of the December 2026 assessment. |

## §5 Contradictions Surfaced This Phase

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| — | No contradictions detected during phase 02-gap | n/a | n/a |

## §6 HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T10:00:00Z | All four entry checklist items confirmed YES |
| Gate 3 — ratification | 2026-05-26T10:15:00Z | Consultant confirmed YES — gaps.md ratified |
