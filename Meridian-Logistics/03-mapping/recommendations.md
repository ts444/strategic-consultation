---
phase: "03-mapping"
status: ratified
harness_version: "0.2.0"
template: "recommendations@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T10:45:00Z"
produced_by: "synthesizer"
---

# Recommendations (Curated): Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `recommendations@1.0.0`
> **Phase:** 03-mapping
> **Entry condition:** `02-gap/gaps.md` frontmatter `status: ratified`
> **Companion artifact:** `03-mapping/service-map.md` (exhaustive mapping)

---

## 1. Recommendation Coverage

| REC-id | Title | Addresses (GAP-ids) | Compliance relation |
|--------|-------|---------------------|---------------------|
| REC-001 | Deploy SIEM for centralised security monitoring | GAP-001 | addresses |
| REC-002 | Deploy Business Continuity service for IR capability and BCP | GAP-002, GAP-003 | partially-addresses |
| REC-003 | Deploy IT Risk Management for governance framework | GAP-004 | addresses |
| REC-004 | Enforce MFA and activate contracted IAM controls | GAP-005 | addresses |
| REC-005 | Reinstate Device Hardening contract | GAP-006 | addresses |
| REC-006 | Reinstate Mail Security contract | GAP-006 | addresses |
| REC-007 | Reinstate and resolve IT Change Management | GAP-007 | addresses |
| REC-008 | Deploy IT Asset Management | GAP-008 | addresses |
| REC-009 | Engage legal/regulatory advisory for CMP-001 entity classification | GAP-009 | partially-addresses |

---

## 2. Recommendation Blocks

```yaml
---
id: REC-001
title: "Deploy SIEM for centralised security monitoring"
addresses:
  - GAP-001
proposed_service: "SIEM"
portfolio_uri: "portfolio://Security/SIEM.md"
rationale: >
  Meridian-Logistics has no contracted SIEM, NDR, or threat intelligence
  capability, leaving no centralised log aggregation or detection function.
  The SIEM service at Silver tier provides centralised log ingestion,
  MITRE ATT&CK-aligned detection, CMP-001-mapped compliance reporting,
  alert triage, and incident timeline reconstruction — directly satisfying
  the logging and detection controls required by CMP-001 (NIS2 Art.21)
  and the security monitoring controls required by CMP-002 (TISAX AL2).
  Note: 24/7 SOC coverage and DFIR are not included in this service;
  the SOC and DFIR gap is partially addressed by REC-002 and flagged for
  06-retro portfolio change-request review.
  [inferred] [source:from: GAP-001 + portfolio://Security/SIEM.md] [conf:H]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 8640
  notes: >
    Silver tier, 240 users at £36/user/month = £8,640/month (£103,680/yr).
    Annual opex exceeds the BUD-001 opex envelope of £20,000/yr on its own;
    the total programme cost must be reviewed against BUD-001 hard limit of
    £200,000 total. SIEM is the highest-priority new service and should be
    prioritised if budget trade-offs are required.
lock_in: >
  Moderate. Switching SIEM providers requires migrating log ingestion
  configuration, porting MITRE ATT&CK detection rules, and rebuilding the
  CMP-001/CMP-002 compliance reporting baseline tuned to this engagement.
  No proprietary data formats trap raw log data; however, the institutional
  knowledge embedded in detection rules and compliance reports represents a
  meaningful switching cost.
opportunity_cost: >
  Foregoing SIEM means the customer cannot evidence security monitoring for
  CMP-001 (NIS2 Art.21 logging and detection) or CMP-002 (TISAX AL2
  monitoring control). Building equivalent in-house log management is not
  feasible for a 6-person IT team. Failure to evidence monitoring capability
  ahead of the December 2026 TISAX assessment creates a high risk of
  assessment failure.
---
```

```yaml
---
id: REC-002
title: "Deploy Business Continuity service for IR capability and BCP"
addresses:
  - GAP-002
  - GAP-003
proposed_service: "Business Continuity"
portfolio_uri: "portfolio://Security/Business_Continuity.md"
rationale: >
  Meridian-Logistics has no contracted incident response, business
  continuity, or DFIR retainer — a demonstrated capability failure
  evidenced by the 2025 ransomware incident (full ransom paid). The
  Business Continuity service addresses GAP-003 directly (BCP development
  and annual review, BIA with RTO/RPO definition, annual tabletop
  facilitation, communication plan templates, post-incident remediation
  coordination) and partially addresses GAP-002 (incident containment
  support including network isolation, credential reset, and eviction is
  included; however, 24/7 IR retainer and full DFIR are NOT included in
  the portfolio). The combined service closes both the NIS2 Art.21
  business continuity obligation and the TISAX AL2 BCP documentation and
  testing requirement. Residual gap on 24/7 IR and DFIR is flagged for
  06-retro portfolio change-request backlog.
  [inferred] [source:from: GAP-002 + GAP-003 + portfolio://Security/Business_Continuity.md] [conf:M]
compliance_relation: partially-addresses
cost:
  capex: 0
  opex_monthly: 7920
  notes: >
    Silver tier, 240 users at £33/user/month = £7,920/month (£95,040/yr).
    Combined with REC-001, programme opex significantly exceeds BUD-001
    annual opex envelope of £20,000/yr; full programme cost must be assessed
    against BUD-001 hard limit of £200,000 total. This service is critical
    for the December 2026 TISAX assessment and should not be deferred.
lock_in: >
  Moderate. Replacing the Business Continuity service requires re-running
  BCP development and the tabletop exercise with a new provider, and
  re-building the evidence trail for TISAX assessment. No proprietary data
  formats. Switching cost is primarily in re-running facilitated exercises
  and re-documenting plans acceptable to TISAX assessors.
opportunity_cost: >
  Foregoing this service means no documented BCP, no tabletop exercise, and
  no IR coordination capability — all of which are required evidence items
  for the December 2026 TISAX assessment. High risk of TISAX assessment
  failure. It also leaves the customer with no structured IR support in the
  event of a repeat ransomware incident, which has already occurred once
  at full ransom cost.
---
```

```yaml
---
id: REC-003
title: "Deploy IT Risk Management for governance framework"
addresses:
  - GAP-004
proposed_service: "IT Risk Management"
portfolio_uri: "portfolio://Governance/IT_Risk_Management.md"
rationale: >
  Customer's IS policies are outdated and unenforced, and governance is
  entirely informal with no steering committee or board-level risk
  reporting. The IT Risk Management service provides an IT risk register,
  quarterly review facilitation using ISO 27005/NIST SP 800-30 methodology,
  risk treatment plans, an annual board-level risk report, and cyber
  insurance renewal support — establishing the governance foundation
  required by CMP-001 NIS2 governance obligations and CMP-002 TISAX AL2
  IS policy and risk management controls. Note: IS policy document drafting
  itself is not included in this service and remains a separate internal or
  advisory action to be planned alongside this recommendation.
  [inferred] [source:from: GAP-004 + portfolio://Governance/IT_Risk_Management.md] [conf:M]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 6240
  notes: >
    Silver tier, 240 users at £26/user/month = £6,240/month (£74,880/yr).
    Must be assessed against BUD-001 hard limit of £200,000 total across
    all programme spend. Deferral carries risk of CMP-001 and CMP-002
    non-compliance on governance evidence.
lock_in: >
  Moderate. Switching IT Risk Management providers requires migrating the
  risk register, re-establishing the ISO 27005/NIST methodology baseline,
  and rebuilding the board-level reporting cadence. No proprietary data
  formats; lock-in is primarily procedural and relational.
opportunity_cost: >
  Foregoing IT Risk Management means the IS policy framework refresh has
  no governance foundation, the risk register and board reporting remain
  absent, and cyber insurance renewal support is unavailable. Both CMP-001
  and CMP-002 require evidence of a functioning risk management process;
  absence creates a compliance evidence gap at both the NIS2 and TISAX
  assessment stages.
---
```

```yaml
---
id: REC-004
title: "Enforce MFA and activate contracted IAM controls"
addresses:
  - GAP-005
proposed_service: "Identity and Access Management"
portfolio_uri: "portfolio://Security/Identity_Access_Management.md"
rationale: >
  Gold-tier IAM is already contracted (cs-mer-8, healthy through
  2026-11-25) and includes MFA enforcement, PIM, PAM, SSO, and quarterly
  access certification. GAP-005 is an execution gap — cultural resistance
  among staff has prevented confirmed MFA enforcement — not a capability
  gap. The recommended action is to escalate MFA enforcement through
  executive sponsorship (CEO/CISO) and pair the rollout with the
  contracted Awareness Training capability to resolve staff resistance.
  No new procurement is required. This closes the CMP-001 NIS2 access
  control obligation and CMP-002 TISAX AL2 strong-authentication
  requirement using already-contracted tooling.
  [inferred] [source:from: GAP-005 + portfolio://Security/Identity_Access_Management.md] [conf:H]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 0
  notes: >
    No additional cost — activation of existing contracted capability.
    IAM Gold is contracted at cs-mer-8 (£40/user/month, healthy through
    2026-11-25). Renewal cost at contract expiry should be tracked against
    BUD-001 ongoing opex. Current contract cost is already within existing
    opex commitments.
lock_in: >
  No new lock-in created. Existing contract commitment runs through
  2026-11-25. Renewal terms should be reviewed before expiry given the
  programme's dependency on MFA enforcement evidence for TISAX and CMP-001.
opportunity_cost: >
  Not proceeding with MFA enforcement means both CMP-001 and CMP-002
  strong-authentication evidence remains absent. As a zero-cost activation
  of already-contracted capability, the opportunity cost of inaction is
  asymmetric: compliance risk at no additional spend. Staff resistance
  unresolved will also undermine the effectiveness of other security
  controls across the programme.
---
```

```yaml
---
id: REC-005
title: "Reinstate Device Hardening contract"
addresses:
  - GAP-006
proposed_service: "Device Hardening"
portfolio_uri: "portfolio://Security/Device_Hardening.md"
rationale: >
  The Device Hardening contract (cs-mer-10) lapsed on 2026-05-25 — the
  same day as phase ratification — ending continuous CIS Benchmark
  baseline application, attack surface reduction, LAPS, and hardening
  compliance scanning with deviation reporting. TISAX AL2 requires
  continuous, evidenced control coverage; any gap in Device Hardening
  coverage during the evidence collection window ahead of the December
  2026 assessment creates an assessable finding. Contract reinstatement
  is time-sensitive and should be initiated immediately.
  [inferred] [source:from: GAP-006 + portfolio://Security/Device_Hardening.md] [conf:H]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 6240
  notes: >
    Silver tier, 240 users at £26/user/month = £6,240/month (£74,880/yr).
    This is a contract reinstatement (previously contracted at Silver tier);
    costs should be considered against BUD-001 hard limit. Time-sensitive:
    contract lapsed 2026-05-25; delay increases the evidence gap window
    before the December 2026 TISAX assessment.
lock_in: >
  Moderate. Device Hardening switching cost includes re-baselining CIS
  benchmarks, re-running deviation scans to rebuild the evidence trail,
  and re-onboarding device inventory. No proprietary data formats.
opportunity_cost: >
  Foregoing Device Hardening reinstatement means TISAX AL2 continuous
  control coverage for endpoint hardening remains absent. The longer the
  lapse, the larger the evidence gap ahead of the December 2026 assessment.
  There is also a direct security risk during the lapse: without CIS
  baseline enforcement, endpoint attack surface regression is undetected
  and unremediated.
---
```

```yaml
---
id: REC-006
title: "Reinstate Mail Security contract"
addresses:
  - GAP-006
proposed_service: "Mail Security"
portfolio_uri: "portfolio://Security/Mail_Security.md"
rationale: >
  The Mail Security contract (cs-mer-7) lapsed on 2026-05-25 — the same
  day as phase ratification — ending attachment sandboxing, SPF/DKIM/DMARC
  enforcement, URL rewriting, outbound DLP, and BEC detection. Given the
  customer's 2025 ransomware incident (attributed to phishing vector,
  full ransom paid), the absence of mail security controls represents an
  active and material ransomware re-exposure risk, not merely a compliance
  gap. Contract reinstatement is time-sensitive and should be treated as
  an immediate remediation action. This service also contributes to CMP-001
  NIS2 Art.21 technical measures and CMP-002 TISAX AL2 continuous control
  coverage.
  [inferred] [source:from: GAP-006 + portfolio://Security/Mail_Security.md] [conf:H]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 6720
  notes: >
    Silver tier, 240 users at £28/user/month = £6,720/month (£80,640/yr).
    This is a contract reinstatement (previously contracted at Silver tier);
    costs should be considered against BUD-001 hard limit. Time-sensitive:
    contract lapsed 2026-05-25; each day of delay maintains active
    ransomware exposure via unscanned email attachments.
lock_in: >
  Moderate. Switching Mail Security providers requires re-configuring
  SPF/DKIM/DMARC DNS records, re-tuning sandbox policies, and re-establishing
  outbound DLP rules. No proprietary data formats. Switching cost is
  primarily operational reconfiguration.
opportunity_cost: >
  Foregoing Mail Security reinstatement maintains active ransomware exposure
  via unscreened email — a risk that has already materialised for this
  customer (2025 incident, full ransom paid). It also leaves TISAX AL2
  continuous-control evidence for mail security absent. The combination of
  historical incident and active lapse makes this the highest immediate
  security risk in the programme.
---
```

```yaml
---
id: REC-007
title: "Reinstate and resolve IT Change Management"
addresses:
  - GAP-007
proposed_service: "IT Change Management"
portfolio_uri: "portfolio://Governance/IT_Change_Management.md"
rationale: >
  IT Change Management (cs-mer-15) is simultaneously in Incident status
  and has a lapsed contract (ended 2026-05-25); governance is informal
  with no steering committee and strategic decisions are made ad hoc.
  The IT Change Management service provides change request intake and
  categorisation, CAB coordination with approval records, emergency change
  fast-track with retroactive documentation, and PIR tracking — the audit
  trail required by CMP-001 NIS2 governance obligations and CMP-002 TISAX
  AL2 change management controls. Reinstatement requires concurrent
  incident resolution (cs-mer-15) to restore service continuity.
  [inferred] [source:from: GAP-007 + portfolio://Governance/IT_Change_Management.md] [conf:H]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 5280
  notes: >
    Silver tier, 240 users at £22/user/month = £5,280/month (£63,360/yr).
    Contract reinstatement; cs-mer-15 incident resolution may carry
    one-time remediation cost (tbc with MSP delivery team). Costs should
    be assessed against BUD-001 hard limit.
lock_in: >
  Moderate. Switching IT Change Management providers requires migrating
  CAB records and change history, re-establishing emergency change
  protocols, and rebuilding audit trail documentation acceptable to TISAX
  assessors. No proprietary data formats.
opportunity_cost: >
  Foregoing IT Change Management reinstatement means the audit trail of
  changes remains absent. Both CMP-001 and CMP-002 require evidenced
  change governance; absence at the December 2026 TISAX assessment creates
  an assessable finding. Continued informal change governance also
  increases operational risk from undocumented changes to in-scope systems.
---
```

```yaml
---
id: REC-008
title: "Deploy IT Asset Management"
addresses:
  - GAP-008
proposed_service: "IT Asset Management"
portfolio_uri: "portfolio://Governance/IT_Asset_Management.md"
rationale: >
  The customer's asset registry records only 25 devices, 25 users, and
  10 licences against an actual headcount of 240 — approximately 10%
  coverage. The IT Asset Management service provides hardware and software
  asset inventory with automated discovery, full lifecycle management,
  asset criticality classification, and an annual physical audit. An
  accurate asset inventory is a prerequisite for effective vulnerability
  management, risk management, and access control — meaning this gap
  creates a cascading risk that degrades the effectiveness of all other
  programme services. Both CMP-001 NIS2 asset management obligations and
  CMP-002 TISAX AL2 inventory requirements are addressed.
  [inferred] [source:from: GAP-008 + portfolio://Governance/IT_Asset_Management.md] [conf:H]
compliance_relation: addresses
cost:
  capex: tbc
  opex_monthly: tbc
  notes: >
    Pricing was not retrieved from portfolio — marked tbc. Silver-tier
    pricing should be confirmed before programme budget sign-off. All
    spend must be assessed against BUD-001 hard limit of £200,000 total.
lock_in: >
  Moderate. Switching IT Asset Management providers requires exporting
  the asset inventory, re-running automated discovery with a new tool,
  and re-establishing criticality classifications. No proprietary data
  formats; the asset data itself is portable.
opportunity_cost: >
  Foregoing IT Asset Management means vulnerability management and risk
  management operate without accurate asset scope — cascading risk across
  all other programme services. An incomplete asset inventory at the
  December 2026 TISAX assessment is an assessable finding that may block
  the label outcome. CMP-001 NIS2 asset management obligations also
  remain unmet.
---
```

```yaml
---
id: REC-009
title: "Engage legal/regulatory advisory for CMP-001 entity classification"
addresses:
  - GAP-009
proposed_service: "[no-known-service]"
rationale: >
  No portfolio service addresses NIS2 entity classification advisory or
  supervisory authority engagement. The customer's NIS2 entity
  classification (essential vs important entity) has not been confirmed
  with the national competent authority, meaning the precise scope of
  NIS2 obligations cannot be fixed. The recommended action is to engage
  a specialist legal and regulatory advisory firm with CMP-001 expertise
  and national competent authority knowledge to conduct the classification
  review and initiate supervisory authority contact. This partially
  addresses the gap — the underlying legal obligation to self-classify
  and register remains the customer's responsibility; the advisory action
  supports execution of that obligation. Gap flagged for 06-retro portfolio
  change-request backlog.
  [inferred] [source:from: GAP-009 + portfolio://Governance/IT_Risk_Management.md] [conf:H]
compliance_relation: partially-addresses
cost:
  capex: tbc
  opex_monthly: tbc
  notes: >
    Third-party legal/regulatory advisory fee — pricing unknown until
    advisory firm is selected and scope of work is agreed. Should be
    assessed against BUD-001 hard limit. Typically a one-time engagement
    cost with possible annual retainer for ongoing regulatory monitoring.
lock_in: >
  None. Legal/regulatory advisory is a time-bounded engagement;
  no long-term service dependency is created. Advisory deliverables
  (classification opinion, authority correspondence) are owned by
  the customer.
opportunity_cost: >
  Foregoing this advisory means entity classification under CMP-001 remains
  unconfirmed with the supervisory authority. The scope of NIS2 obligations
  — and therefore the design of the entire compliance programme — cannot
  be fixed with certainty. If the customer is later assessed as an
  "essential entity" rather than "important entity," significantly higher
  obligations apply and the programme scope would need to be redesigned
  at cost.
---
```

---

## 3. Gap Coverage Summary

| GAP-id | Addressed by (REC-ids) | Coverage note |
|--------|------------------------|---------------|
| GAP-001 | REC-001 | Fully addressed by SIEM service; 24/7 SOC and DFIR residual gap flagged for retro |
| GAP-002 | REC-002 | Partially addressed — Business Continuity covers containment support and tabletop; 24/7 IR retainer and DFIR not in portfolio; flagged for retro |
| GAP-003 | REC-002 | Fully addressed — Business Continuity delivers BCP, BIA, tabletop, communication templates |
| GAP-004 | REC-003 | Addressed by IT Risk Management; IS policy document drafting is a separate action not covered by the service |
| GAP-005 | REC-004 | Addressed — execution gap resolved by activating already-contracted IAM Gold capability; no new procurement required |
| GAP-006 | REC-005, REC-006 | Both sub-components addressed: Device Hardening (REC-005) and Mail Security (REC-006) contract reinstatements |
| GAP-007 | REC-007 | Addressed by IT Change Management reinstatement and cs-mer-15 incident resolution |
| GAP-008 | REC-008 | Addressed by IT Asset Management new service deployment; pricing tbc |
| GAP-009 | REC-009 | Partially addressed — no portfolio service available; legal/regulatory advisory engagement recommended; flagged for retro |

---

## 4. Contradictions Surfaced This Phase

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| — | No contradictions detected during phase 03-mapping | n/a | n/a |

---

## 5. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T10:31:00Z | Entry condition confirmed: gaps.md status ratified |
| Gate 3 — ratification | 2026-05-26T10:45:00Z | Consultant confirmed YES — recommendations.md ratified |
