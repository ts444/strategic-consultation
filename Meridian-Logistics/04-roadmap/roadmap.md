---
phase: "04-roadmap"
status: ratified
harness_version: "0.2.0"
template: "roadmap@1.0.0"
produced_by: "synthesizer"
ratified_by: "Tim S"
ratified_at: "2026-05-26T11:30:00Z"
---

# Roadmap: Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `roadmap@1.0.0`
> **Phase:** 04-roadmap

---

## Sequencing argument

[inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-004 + REC-005 + REC-006 + REC-007 + REC-008 + REC-009] [conf:M]
The roadmap is sequenced against three forcing functions: (1) the TISAX AL2 assessment booked for December 2026 (CMP-002), which is a contractual hard deadline with direct contract-loss consequences; (2) the NIS2 attestation horizon of May 2027 (CMP-001); and (3) the post-ransomware operational reality that detection, response and business-continuity gaps (GAP-001, GAP-002, GAP-003) remain open and that two preventative service contracts (Device Hardening and Mail Security, per GAP-006) lapsed on 2026-05-25. Because TISAX AL2 lands first and is the tightest, Y1 is sized to deliver every TISAX-gating capability before October 2026 to leave a quarter for pre-assessment remediation.

Capability phasing follows foundations → enablers → value-drivers → optimisations. **Foundations** (Q1 Y1) restore baseline infrastructure integrity and governance: immediate reinstatement of Mail Security (REC-006) and Device Hardening (REC-005) (both lapsed, immediate ransomware re-exposure), reinstatement and incident resolution of IT Change Management (REC-007) (currently in Incident status), and deployment of IT Asset Management (REC-008) (prerequisite for risk register, SIEM scoping, and change management completeness). **Enablers** (Q2–Q3 Y1) layer detection and resilience on top of foundations: SIEM (REC-001) requires an authoritative asset inventory and hardened endpoints to be meaningful; Business Continuity (REC-002) requires governance and MFA to underpin its IR runbooks; IT Risk Management (REC-003) requires the asset and change baseline; and MFA enforcement (REC-004) activates already-contracted IAM capability at zero new opex. **Value-drivers** (Q3–Q4 Y1 and H1 Y2) convert capability into evidence: BCP documentation, tabletop exercise (G-03), policy framework refresh, and pre-assessment audit readiness. **Optimisations** (Y2) close the longer-horizon NIS2 entity-classification question (REC-009) via specialist legal advisory.

Severity prioritisation aligns: the three critical gaps (GAP-001 SIEM, GAP-002 IR, GAP-003 BCP) are all sequenced inside Y1 and all delivered before the TISAX assessment window. Quick wins are explicitly used to buy schedule and risk-reduction at low effort: MFA enforcement (REC-004) is zero-cost and activates existing IAM; Mail Security and Device Hardening reinstatements (REC-006 and REC-005) are pure contract renewals that immediately reduce ransomware re-exposure and restore TISAX-relevant controls.

Dependency chains drive the in-year ordering. IT Asset Management (GAP-008) is a hard prerequisite for both Risk Management (REC-003) and Change Management completeness (REC-007), and is also a prerequisite for SIEM scoping (REC-001), so it is pulled into Q1/Q2 Y1 ahead of the enablers. IT Risk Management (REC-003) underpins the governance evidence for Business Continuity (REC-002) and SIEM (REC-001) operating procedures. Mail Security and Device Hardening reinstatements are independent and can be executed in parallel as immediate actions.

**Budget tension (explicit).** The declared BUD-001 envelope is capex_y1 £50k, opex p.a. £20k, hard limit £200k total. The Silver-tier opex for just the new services already specified — SIEM £103,680/yr (REC-001), Business Continuity £95,040/yr (REC-002), IT Risk Management £74,880/yr (REC-003), Device Hardening £74,880/yr (REC-005), Mail Security £80,640/yr (REC-006), IT Change Management £63,360/yr (REC-007), plus TBC for REC-008 and REC-009 — totals **at least £492,480/yr** in opex alone, which exceeds the entire £200k programme hard limit in a single year and is roughly 25× the declared £20k opex envelope. The programme as currently scoped at Silver tier **cannot be delivered within BUD-001**. Because CMP-001 (NIS2) and CMP-002 (TISAX AL2) are non-negotiable and the critical-severity gaps (GAP-001/002/003) are direct ransomware-recurrence and contract-loss risks, the recommendation is **not** to descope to fit the envelope but to escalate the budget conversation with the customer immediately. The consultant must surface the gap to Cheng Zebang (CEO) before any procurement commitment; see OQ-P04-001.

---

## §1 Roadmap Items

```yaml
---
id: RMI-001
title: "Reinstate Mail Security contract"
year: Y1
capability_phase: foundations
addresses:
  - REC-006
  - GAP-006
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-003
  - RSK-004
compliance_role: constraint
budget_envelope: BUD-001
quick_win: true
rationale: >
  [inferred] [source:from: REC-006 + GAP-006] [conf:H]
  Contract lapsed 2026-05-25, creating immediate ransomware re-exposure on the
  primary attack vector. A pure renewal with no new integration work; should be
  signed inside Q1 Y1. Required control for CMP-002 (TISAX AL2) and CMP-001 (NIS2)
  perimeter expectations.
---
```

```yaml
---
id: RMI-002
title: "Reinstate Device Hardening contract"
year: Y1
capability_phase: foundations
addresses:
  - REC-005
  - GAP-006
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-003
  - RSK-004
compliance_role: constraint
budget_envelope: BUD-001
quick_win: true
rationale: >
  [inferred] [source:from: REC-005 + GAP-006] [conf:H]
  Contract lapsed 2026-05-25. Renewal restores endpoint baseline hardening with
  zero integration overhead and supports TISAX AL2 endpoint-control evidence.
  Parallel to RMI-001; both should land in Q1 Y1.
---
```

```yaml
---
id: RMI-003
title: "Reinstate and resolve IT Change Management"
year: Y1
capability_phase: foundations
addresses:
  - REC-007
  - GAP-007
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-004
compliance_role: constraint
budget_envelope: BUD-001
quick_win: true
rationale: >
  [inferred] [source:from: REC-007 + GAP-007] [conf:H]
  Service is lapsed and currently in Incident status; reinstatement is a
  governance prerequisite for Risk Management (RMI-007) and for auditable
  change evidence required by both CMP-001 and CMP-002. Treated as foundations
  because risk and continuity workstreams cannot produce credible audit evidence
  without a working change baseline.
---
```

```yaml
---
id: RMI-004
title: "Deploy IT Asset Management"
year: Y1
capability_phase: foundations
addresses:
  - REC-008
  - GAP-008
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-002
  - RSK-003
compliance_role: constraint
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-008 + GAP-008] [conf:H]
  Authoritative asset inventory is a hard prerequisite for SIEM scoping (RMI-005),
  risk register baseline (RMI-007), and change management completeness (RMI-003).
  Deployed in Q2 Y1 to feed downstream enablers. Cost is currently TBC
  (see OQ-P04-002).
---
```

```yaml
---
id: RMI-005
title: "Enforce MFA via contracted IAM capability"
year: Y1
capability_phase: enablers
addresses:
  - REC-004
  - GAP-005
owner: "Izayoi Nayuta (CISO), sponsored by Cheng Zebang (CEO)"
risks:
  - RSK-005
compliance_role: constraint
budget_envelope: BUD-001
quick_win: true
rationale: >
  [inferred] [source:from: REC-004 + GAP-005] [conf:H]
  IAM Gold is already contracted (cs-mer-8); enforcement is a configuration and
  change-management activity with zero new opex. Organisational resistance is the
  binding constraint, so CEO sponsorship and a firm enforcement deadline are
  required to mitigate RSK-005. Schedule Q1 Y1 launch with full enforcement by
  end of Q2 Y1.
---
```

```yaml
---
id: RMI-006
title: "Deploy SIEM for centralised security monitoring"
year: Y1
capability_phase: enablers
addresses:
  - REC-001
  - GAP-001
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-002
  - RSK-003
compliance_role: deadline
compliance_deadline: 2026-12-01
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-001 + GAP-001] [conf:H]
  SIEM closes the critical detection gap (GAP-001) and is required to evidence
  monitoring controls for the CMP-002 (TISAX AL2) December 2026 assessment.
  Deployment depends on RMI-004 (asset inventory) and RMI-002 (hardened
  endpoints) being in flight. Target operational by end of Q2 Y1 to allow two
  quarters of tuned operational evidence before assessment.
---
```

```yaml
---
id: RMI-007
title: "Deploy IT Risk Management for governance framework"
year: Y1
capability_phase: enablers
addresses:
  - REC-003
  - GAP-004
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-002
compliance_role: constraint
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-003 + GAP-004] [conf:M]
  Provides the governance spine for the refreshed policy framework and the risk
  register that underpins both CMP-001 and CMP-002 evidence. Confidence is M
  because effective uptake depends on organisational adoption and on the asset
  inventory (RMI-004) being in place. Deploy Q3 Y1 once foundations are landed.
---
```

```yaml
---
id: RMI-008
title: "Deploy Business Continuity service (IR capability and BCP)"
year: Y1
capability_phase: enablers
addresses:
  - REC-002
  - GAP-002
  - GAP-003
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-001
  - RSK-002
  - RSK-003
compliance_role: deadline
compliance_deadline: 2026-12-01
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-002 + GAP-002 + GAP-003] [conf:M]
  Stands up the IR process (G-03) and BCP required by CMP-002. Confidence is M
  because REC-002 only partially-addresses GAP-002/003 — supplementary playbook
  and BIA work is required. Deploy Q2 Y1 so that BIA, runbooks, and the
  tabletop exercise (G-03) can complete by end of Q3 Y1, leaving Q4 Y1 for
  pre-assessment remediation.
---
```

```yaml
---
id: RMI-009
title: "BCP documentation and IR tabletop exercise"
year: Y1
capability_phase: value-drivers
addresses:
  - REC-002
  - GAP-002
  - GAP-003
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-001
  - RSK-003
compliance_role: deadline
compliance_deadline: 2026-12-01
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-002 + GAP-002 + GAP-003] [conf:M]
  Operationalises G-03: documented BCP, trained staff, and a completed tabletop
  exercise — the explicit success measure for G-03 and a TISAX AL2 evidence
  requirement. Sequenced Q3 Y1 to allow Q4 Y1 dry-run before the December 2026
  assessment.
---
```

```yaml
---
id: RMI-010
title: "Pre-assessment audit readiness review (CMP-002)"
year: Y1
capability_phase: value-drivers
addresses:
  - REC-001
  - REC-002
  - REC-003
  - REC-004
  - REC-005
  - REC-006
  - REC-007
  - GAP-001
  - GAP-002
  - GAP-003
  - GAP-004
  - GAP-005
  - GAP-006
  - GAP-007
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-001
compliance_role: deadline
compliance_deadline: 2026-12-01
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-004 + REC-005 + REC-006 + REC-007] [conf:M]
  Consolidated dry-run of evidence across all Y1 capabilities ahead of the
  December 2026 TISAX AL2 assessment (CMP-002). Confidence is bounded by the
  weakest contributing claim (REC-002/003 at M). Output is a gap list driving
  Q4 Y1 remediation.
---
```

```yaml
---
id: RMI-011
title: "Engage legal/regulatory advisory for entity classification (CMP-001)"
year: Y2
capability_phase: optimisations
addresses:
  - REC-009
  - GAP-009
owner: "Izayoi Nayuta (CISO), escalation to Cheng Zebang (CEO)"
risks:
  - RSK-002
compliance_role: deadline
compliance_deadline: 2027-05-26
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-009 + GAP-009] [conf:H]
  Specialist legal advisory engagement to validate entity classification with the
  national supervisory authority — a prerequisite to fixing the CMP-001 scope of
  obligation. Sized as a Y2 H1 activity so the outcome lands in time for the
  May 2027 attestation deadline. Cost TBC (see OQ-P04-003).
---
```

```yaml
---
id: RMI-012
title: "Information security policy framework refresh"
year: Y2
capability_phase: value-drivers
addresses:
  - REC-003
  - GAP-004
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-002
compliance_role: deadline
compliance_deadline: 2027-05-26
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-003 + GAP-004] [conf:M]
  Full policy refresh built on the Risk Management foundation deployed in
  RMI-007. Sequenced H1 Y2 to produce the policy evidence pack required for
  CMP-001 attestation by 2027-05-26.
---
```

```yaml
---
id: RMI-013
title: "Compliance attestation programme (CMP-001)"
year: Y2
capability_phase: value-drivers
addresses:
  - REC-001
  - REC-002
  - REC-003
  - REC-004
  - REC-009
  - GAP-001
  - GAP-002
  - GAP-003
  - GAP-004
  - GAP-005
  - GAP-009
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-002
compliance_role: deadline
compliance_deadline: 2027-05-26
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-004 + REC-009] [conf:M]
  Consolidated attestation programme for CMP-001 (NIS2), drawing evidence from
  all Y1 capabilities plus the policy refresh (RMI-012) and entity classification
  outcome (RMI-011). Targets attestation by 2027-05-26. Confidence bounded by
  weakest contributing claim.
---
```

```yaml
---
id: RMI-014
title: "Sustained operations and annual control review"
year: Y3
capability_phase: optimisations
addresses:
  - REC-001
  - REC-002
  - REC-003
  - REC-005
  - REC-006
  - REC-007
  - REC-008
owner: "Izayoi Nayuta (CISO)"
risks:
  - RSK-003
  - RSK-004
compliance_role: enabler
budget_envelope: BUD-001
quick_win: false
rationale: >
  [inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-005 + REC-006 + REC-007 + REC-008] [conf:M]
  Steady-state opex programme: annual control reviews, TISAX surveillance
  preparation, NIS2 ongoing reporting, and lessons-learned retros. Confidence
  bounded by weakest contributing REC (REC-002/003 at M).
---
```

---

## §2 Recommendation Coverage

| REC-id | Title | Addressed by RMI-id(s) |
|--------|-------|------------------------|
| REC-001 | Deploy SIEM | RMI-006, RMI-010, RMI-013, RMI-014 |
| REC-002 | Deploy Business Continuity service | RMI-008, RMI-009, RMI-010, RMI-013, RMI-014 |
| REC-003 | Deploy IT Risk Management | RMI-007, RMI-010, RMI-012, RMI-013, RMI-014 |
| REC-004 | Enforce MFA / activate IAM controls | RMI-005, RMI-010, RMI-013 |
| REC-005 | Reinstate Device Hardening | RMI-002, RMI-010, RMI-014 |
| REC-006 | Reinstate Mail Security | RMI-001, RMI-010, RMI-014 |
| REC-007 | Reinstate IT Change Management | RMI-003, RMI-010, RMI-014 |
| REC-008 | Deploy IT Asset Management | RMI-004, RMI-014 |
| REC-009 | Legal/regulatory advisory for entity classification | RMI-011, RMI-013 |

All nine REC items are addressed by at least one RMI. [inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-004 + REC-005 + REC-006 + REC-007 + REC-008 + REC-009] [conf:H]

---

## §3 Calendar Projection

| Period | Milestone | RMI-NNN | Compliance driver |
|--------|-----------|---------|-------------------|
| Immediate (Q1 Y1) | Mail Security contract reinstated | RMI-001 | CMP-002 |
| Immediate (Q1 Y1) | Device Hardening contract reinstated | RMI-002 | CMP-002 |
| Q1 Y1 | IT Change Management reinstated and Incident resolved | RMI-003 | CMP-001, CMP-002 |
| Q1 Y1 | MFA enforcement programme launched (CEO-sponsored) | RMI-005 | CMP-001, CMP-002 |
| Q2 Y1 | IT Asset Management deployed; discovery in progress | RMI-004 | CMP-001, CMP-002 |
| Q2 Y1 | SIEM deployed and operational | RMI-006 | CMP-002 |
| Q2 Y1 | Business Continuity service deployed; BIA initiated | RMI-008 | CMP-002 |
| Q2 Y1 | MFA fully enforced across workforce | RMI-005 | CMP-001, CMP-002 |
| Q3 Y1 | IT Risk Management deployed; risk register baseline established | RMI-007 | CMP-001, CMP-002 |
| Q3 Y1 | BCP documented; IR tabletop exercise completed (G-03) | RMI-009 | CMP-002 |
| Q4 Y1 | Pre-assessment audit readiness review (CMP-002 gate) | RMI-010 | CMP-002 |
| Q4 Y1 (Dec 2026) | TISAX AL2 assessment — label awarded (G-02) | RMI-010 | CMP-002 |
| H1 Y2 | Legal advisory engagement: NIS2 entity classification confirmed | RMI-011 | CMP-001 |
| H1 Y2 | Information security policy framework refresh completed | RMI-012 | CMP-001 |
| H2 Y2 (by 2027-05-26) | NIS2 attestation achieved (G-01) | RMI-013 | CMP-001 |
| H1 Y3 | First annual control review; TISAX surveillance prep | RMI-014 | CMP-002 |
| H2 Y3 | NIS2 ongoing reporting cycle; retros and optimisation | RMI-014 | CMP-001 |

---

## §4 Compliance Items

| RMI-id | Title | compliance_role | compliance_deadline | CMP-id(s) |
|--------|-------|-----------------|---------------------|-----------|
| RMI-001 | Reinstate Mail Security contract | constraint | — | CMP-001, CMP-002 |
| RMI-002 | Reinstate Device Hardening contract | constraint | — | CMP-001, CMP-002 |
| RMI-003 | Reinstate and resolve IT Change Management | constraint | — | CMP-001, CMP-002 |
| RMI-004 | Deploy IT Asset Management | constraint | — | CMP-001, CMP-002 |
| RMI-005 | Enforce MFA via contracted IAM capability | constraint | — | CMP-001, CMP-002 |
| RMI-006 | Deploy SIEM for centralised security monitoring | deadline | 2026-12-01 | CMP-002 |
| RMI-007 | Deploy IT Risk Management for governance framework | constraint | — | CMP-001, CMP-002 |
| RMI-008 | Deploy Business Continuity service (IR + BCP) | deadline | 2026-12-01 | CMP-002 |
| RMI-009 | BCP documentation and IR tabletop exercise | deadline | 2026-12-01 | CMP-002 |
| RMI-010 | Pre-assessment audit readiness review | deadline | 2026-12-01 | CMP-002 |
| RMI-011 | Legal/regulatory advisory for entity classification | deadline | 2027-05-26 | CMP-001 |
| RMI-012 | Information security policy framework refresh | deadline | 2027-05-26 | CMP-001 |
| RMI-013 | Compliance attestation programme | deadline | 2027-05-26 | CMP-001 |
| RMI-014 | Sustained operations and annual control review | enabler | — | CMP-001, CMP-002 |

---

## §5 Budget Overview

| RMI-id | Service / action | budget_envelope | Annual opex (est.) | Notes |
|--------|------------------|-----------------|--------------------|-------|
| RMI-001 | Mail Security (REC-006, Silver) | BUD-001 | £80,640 | Reinstatement; lapsed 2026-05-25 |
| RMI-002 | Device Hardening (REC-005, Silver) | BUD-001 | £74,880 | Reinstatement; lapsed 2026-05-25 |
| RMI-003 | IT Change Management (REC-007, Silver) | BUD-001 | £63,360 | Reinstatement; in Incident |
| RMI-004 | IT Asset Management (REC-008, Silver) | BUD-001 | TBC | Pricing not retrieved (OQ-P04-002) |
| RMI-005 | MFA enforcement on contracted IAM (REC-004) | BUD-001 | £0 | Activates existing IAM Gold (cs-mer-8) |
| RMI-006 | SIEM (REC-001, Silver) | BUD-001 | £103,680 | Critical detection capability |
| RMI-007 | IT Risk Management (REC-003, Silver) | BUD-001 | £74,880 | Governance spine |
| RMI-008 | Business Continuity (REC-002, Silver) | BUD-001 | £95,040 | IR + BCP |
| RMI-009 | BCP docs and tabletop (delivery within REC-002) | BUD-001 | included in RMI-008 | Internal effort + service-included workshops |
| RMI-010 | Pre-assessment readiness review | BUD-001 | internal effort + advisory TBC | Internal CISO time |
| RMI-011 | Legal/regulatory advisory (REC-009) | BUD-001 | TBC | One-off + possible retainer (OQ-P04-003) |
| RMI-012 | Policy framework refresh (delivery within REC-003) | BUD-001 | included in RMI-007 | Service-led deliverable |
| RMI-013 | CMP-001 attestation programme | BUD-001 | internal + advisory TBC | Audit fees TBC |
| RMI-014 | Sustained operations | BUD-001 | sum of recurring above | Ongoing |
| **TOTAL (recurring opex, known lines only)** | — | BUD-001 | **≥ £492,480 / yr** | **EXCEEDS BUD-001 (£200k total hard limit) in single year** |

[inferred] [source:from: REC-001 + REC-002 + REC-003 + REC-005 + REC-006 + REC-007] [conf:H]
**Budget flag.** The sum of known Silver-tier annual opex lines is at least £492,480/yr, which exceeds the BUD-001 hard limit of £200,000 (total programme) and is roughly 25× the declared £20,000/yr opex envelope. Two further lines (RMI-004, RMI-011) are TBC and will push the figure higher. The consultant must raise a revised budget conversation with Cheng Zebang (CEO) before any procurement commitment; CMP-001 and CMP-002 are non-negotiable and the critical gaps cannot be descoped without accepting contract loss and regulatory non-compliance. See OQ-P04-001.

---

## §6 Risks and Mitigations

| RSK-id | Risk title | RMI-id(s) that mitigate | Mitigation summary |
|--------|------------|--------------------------|-------------------|
| RSK-001 | TISAX AL2 assessment failure (Dec 2026) | RMI-008, RMI-009, RMI-010 | Stand up IR/BCP, complete tabletop before Q4 Y1, then dry-run readiness review |
| RSK-002 | NIS2 compliance failure within 12 months | RMI-004, RMI-006, RMI-007, RMI-008, RMI-011, RMI-012, RMI-013 | Deploy SIEM/BC/Risk Management Y1; validate entity classification H1 Y2; attestation programme H2 Y2 |
| RSK-003 | Repeat ransomware attack (detection/response gaps) | RMI-001, RMI-002, RMI-004, RMI-006, RMI-008, RMI-009, RMI-014 | Reinstate Mail Security + Device Hardening immediately; SIEM by end Q2 Y1; IR process and tabletop by Q3 Y1 |
| RSK-004 | Regression from contract expiry (Device Hardening, Mail Security, IT Change Mgmt) | RMI-001, RMI-002, RMI-003, RMI-014 | Renewal decisions confirmed Q1 Y1; annual review prevents recurrence |
| RSK-005 | MFA undermined by organisational resistance | RMI-005 | CEO sponsorship, firm enforcement deadline (end Q2 Y1), change-management workstream |

---

## §7 Open Questions

- **OQ-P04-001:** Budget envelope — the declared BUD-001 hard limit of £200k total is insufficient to fund the full programme at Silver tier pricing (known opex ≥ £492,480/yr). Consultant must raise a revised budget conversation with Cheng Zebang (CEO) before programme commitments are made. CMP-001 and CMP-002 obligations are non-negotiable; descope is not viable for critical gaps GAP-001/002/003 or for the lapsed contracts in GAP-006.
- **OQ-P04-002:** IT Asset Management pricing — REC-008 cost is TBC; Silver tier pricing should be confirmed before programme sign-off and folded into the revised BUD-001 conversation.
- **OQ-P04-003:** Legal/regulatory advisory pricing — REC-009 cost is TBC; advisory firm selection and scope of work required, including one-off fee vs. retainer model.
- **OQ-P04-004:** NIS2 entity classification — classification must be confirmed with the national supervisory authority before NIS2 compliance scope can be fixed; currently assumed "important entity" based on headcount (240) and revenue (~£10M) profile. RMI-011 owns the resolution.
- **OQ-P04-005:** TISAX AL2 assessor and pre-assessment timing — assessor booking confirmed for December 2026 but specific date and pre-assessment slot for Q4 Y1 dry-run not yet captured; required for RMI-010 sequencing.

---

## §8 HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T11:00:00Z | All six entry checklist items confirmed YES |
| Gate 3 — ratification | 2026-05-26T11:30:00Z | Consultant confirmed YES — roadmap.md ratified |
