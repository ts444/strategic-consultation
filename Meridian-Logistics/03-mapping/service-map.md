---
phase: "03-mapping"
status: ratified
harness_version: "0.2.0"
template: "service-map@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T10:45:00Z"
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. Every gap declared in 02-gap/gaps.md has at least one entry in §2
     (Mapping Table). An entry may be a named portfolio service OR a
     [no-known-service] placeholder — silent omission is not allowed.
  2. Every mapped service has a written fit_rationale (claim atom with
     source and conf). The rationale must name the gap(s) it addresses
     and cite a portfolio:// URI.
  3. [no-known-service] entries include a rationale explaining why no
     portfolio service fits and mark the portfolio gap for retro.
  4. Validator reports zero violations.
  5. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 03-mapping.
  6. Consultant has reviewed and ratified via HITL gate 3.
  7. Frontmatter `status` changed to `ratified`; `ratified_by` and
     `ratified_at` filled before committing.
-->

# Service Map (Exhaustive): Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `service-map@1.0.0`
> **Phase:** 03-mapping
> **Entry condition:** `02-gap/gaps.md` frontmatter `status: ratified`

---

## 1. Mapping Summary

| GAP-id | Gap title | Candidate services (count) | [no-known-service]? |
|--------|-----------|---------------------------|---------------------|
| GAP-001 | No SIEM / centralised security monitoring capability | 3 (SIEM, Network Detection and Response, Threat Intelligence) | No |
| GAP-002 | No Incident Response capability | 1 (Business Continuity — partial fit) | No |
| GAP-003 | No Business Continuity Plan or BC service | 2 (Business Continuity, Backup and DR) | No |
| GAP-004 | Outdated and unenforced information security policy framework | 1 (IT Risk Management) | No |
| GAP-005 | MFA enforcement maturity unconfirmed despite contracted IAM capability | 2 (Identity and Access Management, Awareness Training) | No |
| GAP-006 | Lapsed security service contracts — Device Hardening and Mail Security | 2 (Device Hardening, Mail Security — both curated) | No |
| GAP-007 | IT governance and change management deficit | 2 (IT Change Management, IT Risk Management) | No |
| GAP-008 | Incomplete IT asset inventory | 1 (IT Asset Management) | No |
| GAP-009 | CMP-001 entity classification not validated with national supervisory authority | 0 | Yes |

---

## 2. Mapping Entries

<!--
One YAML-fenced block per (gap × candidate service) pair. Every gap from
gaps.md appears at least once. curated: true marks the highest-fit service
per gap; curated: false marks secondary and tertiary candidates.
Exception: GAP-006 has two curated entries (Device Hardening, Mail Security)
as they address distinct sub-components of the same lapsed-contracts gap.
-->

```yaml
---
id: MAP-001
gap: GAP-001
proposed_service: "SIEM"
portfolio_uri: "portfolio://Security/SIEM.md"
fit_rationale: >
  The SIEM service directly addresses GAP-001 by providing centralised log
  ingestion and normalisation from servers, endpoints, firewalls, IdPs, and
  cloud platforms — eliminating the absence of any log aggregation capability
  confirmed in GAP-001. MITRE ATT&CK-aligned detection rules and 24/7 alert
  triage deliver the incident-detection capability required by CMP-001 (NIS2
  Art.21 logging and detection) and CMP-002 (TISAX AL2 security monitoring).
  Compliance-mapped reporting for CMP-001 directly supports the NIS2 audit
  evidence trail required before May 2027, and quarterly detection-rule tuning
  sustains coverage ahead of the TISAX assessment in December 2026. This is a
  direct fit for the desired_state of centralised security monitoring with
  NIS2-mapped compliance reporting operational before both deadlines.
  [inferred] [source:from: GAP-001 + portfolio://Security/SIEM.md] [conf:H]
curated: true
notes: "Primary recommendation for GAP-001. 24/7 SOC and DFIR are out of scope for this service; separate MDR engagement required if round-the-clock staffed response is needed."
---
```

```yaml
---
id: MAP-002
gap: GAP-001
proposed_service: "Network Detection and Response"
portfolio_uri: "portfolio://Security/Network_Detection_and_Response.md"
fit_rationale: >
  NDR extends the detection coverage identified in GAP-001 by adding
  network-layer visibility that a SIEM alone cannot provide: east-west lateral
  movement detection, C2/DNS-tunnelling identification, and encrypted traffic
  analysis. Its telemetry forwarding to SIEM makes it a complementary dependency
  rather than a standalone replacement for SIEM. For Meridian-Logistics, which
  experienced a 2025 ransomware attack that traversed the internal network
  undetected, network-layer detection is a strong secondary measure supporting
  CMP-001 (NIS2 technical monitoring measures) and CMP-002 (TISAX AL2 detection
  controls). However, SIEM is the primary addressing service; NDR alone would
  not satisfy the compliance-mapped reporting requirement.
  [inferred] [source:from: GAP-001 + portfolio://Security/Network_Detection_and_Response.md] [conf:M]
curated: false
notes: "Secondary candidate. Best value when deployed alongside SIEM as a dependency. Detection-only — no inline blocking."
---
```

```yaml
---
id: MAP-003
gap: GAP-001
proposed_service: "Threat Intelligence"
portfolio_uri: "portfolio://Security/Threat_Intelligence.md"
fit_rationale: >
  Threat Intelligence partially addresses GAP-001 by enriching detection with
  sector-specific threat briefings, dark-web and leaked-credential monitoring,
  and intelligence-driven SIEM detection-rule updates. For a logistics company
  with a demonstrated ransomware exposure, early-warning notifications on
  emerging threats and IOC enrichment flowing into SIEM would strengthen the
  monitoring posture required by CMP-001 and CMP-002. However, Threat
  Intelligence depends on SIEM (IOCs are distributed to SIEM) and does not
  provide log aggregation or compliance-mapped reporting in its own right; it
  is therefore a tertiary augmentation rather than a direct fit for GAP-001.
  [inferred] [source:from: GAP-001 + portfolio://Security/Threat_Intelligence.md] [conf:M]
curated: false
notes: "Tertiary candidate. Depends on SIEM being contracted first. IR is not included in this service."
---
```

```yaml
---
id: MAP-004
gap: GAP-002
proposed_service: "Business Continuity"
portfolio_uri: "portfolio://Security/Business_Continuity.md"
fit_rationale: >
  The Business Continuity service is the closest available portfolio service for
  GAP-002 and provides meaningful IR-adjacent capabilities: incident containment
  support (network isolation, credential reset, eviction procedures), post-incident
  remediation coordination, annual tabletop exercise facilitation, and
  communication plan templates for stakeholder notification. These directly
  address the G-03 requirement for a documented, trained, and tabletop-tested
  IR process before the TISAX assessment in December 2026, and contribute to
  CMP-001 (NIS2 Art.21 incident response) and CMP-002 (TISAX AL2 IR controls).
  This is a PARTIAL FIT: the service does not include a 24/7 staffed IR retainer
  or a full DFIR capability; no portfolio service currently covers those
  sub-components, which should be surfaced as a portfolio gap in the retro phase.
  [inferred] [source:from: GAP-002 + portfolio://Security/Business_Continuity.md] [conf:M]
curated: true
notes: "Partial fit only. No portfolio service provides a full DFIR or 24/7 IR retainer. This gap should be flagged for 06-retro portfolio change-request backlog regarding DFIR/IR staffing coverage."
---
```

```yaml
---
id: MAP-005
gap: GAP-003
proposed_service: "Business Continuity"
portfolio_uri: "portfolio://Security/Business_Continuity.md"
fit_rationale: >
  The Business Continuity service directly addresses GAP-003: it provides BCP
  development and annual review aligned to a critical process inventory, Business
  Impact Analysis with RTO/RPO per system tier, annual tabletop exercise
  facilitation, incident containment support, communication plan templates for
  stakeholder notification, and post-incident remediation coordination. These
  capabilities map precisely to the desired_state — a documented and tested BCP
  covering containment, communication, and tabletop exercise — satisfying CMP-001
  (NIS2 Art.21 BC measures) and CMP-002 (TISAX AL2 BCP documentation and testing
  requirements) ahead of the December 2026 TISAX assessment deadline. Physical
  site recovery, workspace recovery, and DFIR remain out of scope.
  [inferred] [source:from: GAP-003 + portfolio://Security/Business_Continuity.md] [conf:H]
curated: true
notes: "Primary recommendation for GAP-003. Physical site recovery and DFIR not included. Depends on SIEM, IAM, and IT Change Management for full effectiveness."
---
```

```yaml
---
id: MAP-006
gap: GAP-003
proposed_service: "Backup and DR"
portfolio_uri: "portfolio://Security/Backup_and_DR.md"
fit_rationale: >
  The Backup and DR service is a dependency-layer complement to Business
  Continuity for GAP-003: it provides 3-2-1-1 backup with immutable/air-gap
  protection, backup policy aligned to customer RTO/RPO targets set in the BIA,
  monthly automated restore testing, and annual DR test exercise. For Meridian-
  Logistics, which paid a full ransom in 2025 due to inadequate recovery
  capability, immutable backup protection directly mitigates recurrence risk and
  contributes to the NIS2 Art.21 resilience requirements (CMP-001) and TISAX AL2
  backup/recovery controls (CMP-002). SaaS backup for M365 is not included and
  would require a separate engagement. The service is secondary to Business
  Continuity for GAP-003 as it provides the data-recovery layer rather than the
  BCP documentation and process framework.
  [inferred] [source:from: GAP-003 + portfolio://Security/Backup_and_DR.md] [conf:M]
curated: false
notes: "Secondary/dependency candidate. Best contracted alongside Business Continuity so that RTO/RPO targets from the BIA directly inform backup policy. M365 SaaS backup not included."
---
```

```yaml
---
id: MAP-007
gap: GAP-004
proposed_service: "IT Risk Management"
portfolio_uri: "portfolio://Governance/IT_Risk_Management.md"
fit_rationale: >
  The IT Risk Management service partially addresses GAP-004 by providing the
  governance framework and risk register that are prerequisite to a formal IS
  policy refresh: risk register design and quarterly review facilitation, risk
  assessment methodology (ISO 27005 / NIST SP 800-30), risk identification
  workshops covering technology and process risks, risk treatment plans with
  owners and target dates, and annual executive-level risk reporting. This
  produces auditable governance evidence required by CMP-001 (NIS2 governance
  obligations) and CMP-002 (TISAX AL2 documented governance). The service does
  not directly produce or maintain IS policy documents — that work remains a
  separate engagement or internal action — and legal/regulatory compliance gap
  assessments beyond IT controls mapping are explicitly excluded. The fit is
  therefore indirect: the risk register and governance cadence create the
  structural foundation from which IS policies can be refreshed and enforced.
  [inferred] [source:from: GAP-004 + portfolio://Governance/IT_Risk_Management.md] [conf:M]
curated: true
notes: "Only available portfolio candidate for GAP-004. IS policy drafting and maintenance is not included. Customer will need to assign an internal or advisory resource to produce the refreshed policy documents on the foundation this service provides."
---
```

```yaml
---
id: MAP-008
gap: GAP-005
proposed_service: "Identity and Access Management"
portfolio_uri: "portfolio://Security/Identity_Access_Management.md"
fit_rationale: >
  The IAM service is ALREADY CONTRACTED at Gold tier (cs-mer-8, healthy through
  2026-11-25) and includes MFA policy enforcement across all managed identity
  providers as a named capability. GAP-005 is an execution gap, not a capability
  gap: the service exists but enforcement maturity across the 240-person workforce
  is unconfirmed due to staff resistance. The correct resolution is to activate
  the MFA enforcement capability already within scope of the contracted service —
  working with the IAM delivery team to enforce policies, resolve exceptions, and
  produce coverage evidence meeting CMP-001 (NIS2 access control) and CMP-002
  (TISAX AL2 strong-authentication requirements). PIM, PAM, SSO, and quarterly
  access certification campaigns within the Gold tier also contribute directly to
  these compliance controls.
  [inferred] [source:from: GAP-005 + portfolio://Security/Identity_Access_Management.md] [conf:H]
curated: true
notes: "Already contracted — no new procurement required. Action is activation and enforcement of existing contracted MFA capability. Recommend escalating MFA enforcement to an executive sponsor (CEO or CISO) to overcome staff resistance."
---
```

```yaml
---
id: MAP-009
gap: GAP-005
proposed_service: "Awareness Training"
portfolio_uri: "portfolio://Workplace/Awareness_Training.md"
fit_rationale: >
  The Awareness Training service addresses the cultural and organisational root
  cause of GAP-005: staff resistance to security controls, specifically MFA.
  Monthly security awareness modules, quarterly phishing simulations, and
  human-risk metrics feeding the IT risk register create a measurable behavioural
  change programme that supports — and over time reduces resistance to — the MFA
  enforcement activation being driven through the IAM service. This is an indirect
  fit: Awareness Training does not itself enforce MFA but removes the primary
  obstacle (cultural resistance) that has prevented GAP-005 from closing despite
  the contracted capability. It also contributes to CMP-001 (NIS2 Art.21 awareness
  and training obligations) and CMP-002 (TISAX AL2 security awareness requirements).
  [inferred] [source:from: GAP-005 + portfolio://Workplace/Awareness_Training.md] [conf:M]
curated: false
notes: "Secondary candidate targeting the cultural/behavioural dimension of GAP-005. Most effective when coordinated with the IAM enforcement activation plan so that training messaging is aligned to the MFA rollout timeline."
---
```

```yaml
---
id: MAP-010
gap: GAP-006
proposed_service: "Device Hardening"
portfolio_uri: "portfolio://Security/Device_Hardening.md"
fit_rationale: >
  The Device Hardening service directly addresses the Device Hardening
  sub-component of GAP-006: the lapsed contract cs-mer-10 (ended 2026-05-25)
  covered CIS Benchmark / DISA STIG baselines, automated baseline application
  via GPO/config management/MDM, attack surface reduction, application
  allowlisting for high-risk device classes, LAPS, and hardening compliance
  scanning with deviation reporting. Renewing this service restores continuous
  control coverage required by CMP-002 (TISAX AL2 continuous evidenced control
  coverage) and contributes to CMP-001 (NIS2 Art.21 technical measures for
  endpoint hardening). Baseline review following major OS releases or
  significant threat changes maintains coverage ahead of the December 2026
  TISAX assessment. Pricing tiers: Bronze £18, Silver £26, Gold £36 /user/month.
  [inferred] [source:from: GAP-006 + portfolio://Security/Device_Hardening.md] [conf:H]
curated: true
notes: "One of two curated entries for GAP-006 (addresses Device Hardening sub-component). Contract lapsed 2026-05-25 — reinstatement is time-sensitive. Depends on Configuration Management, Patch Management, EDR, and Vulnerability Management."
---
```

```yaml
---
id: MAP-011
gap: GAP-006
proposed_service: "Mail Security"
portfolio_uri: "portfolio://Security/Mail_Security.md"
fit_rationale: >
  The Mail Security service directly addresses the Mail Security sub-component
  of GAP-006: the lapsed contract cs-mer-7 (ended 2026-05-25) covered attachment
  sandboxing, SPF/DKIM/DMARC policy management, URL rewriting and time-of-click
  protection, outbound email DLP scanning, BEC and impersonation detection, and
  quarantine management. Email is cited as addressing more than 90% of ransomware
  attack vectors — directly relevant to Meridian-Logistics given the 2025
  ransomware incident. Renewing this service restores the CMP-002 (TISAX AL2)
  continuous evidenced mail-security coverage and contributes to CMP-001 (NIS2
  Art.21 technical measures). Outbound DLP also provides partial coverage of
  data-exfiltration risk relevant to both compliance frameworks. Pricing tiers:
  Bronze £20, Silver £28, Gold £38 /user/month.
  [inferred] [source:from: GAP-006 + portfolio://Security/Mail_Security.md] [conf:H]
curated: true
notes: "One of two curated entries for GAP-006 (addresses Mail Security sub-component). Contract lapsed 2026-05-25 — reinstatement is time-sensitive given ransomware history. Depends on DNS, Awareness Training, SIEM, and Productivity suite."
---
```

```yaml
---
id: MAP-012
gap: GAP-007
proposed_service: "IT Change Management"
portfolio_uri: "portfolio://Governance/IT_Change_Management.md"
fit_rationale: >
  The IT Change Management service directly addresses GAP-007: it provides change
  request intake and categorisation (standard/normal/emergency), CAB coordination
  with documented risk review and approval records, pre/post-change implementation
  plans and rollback documentation, emergency change fast-track with retroactive
  risk documentation, and change success rate and PIR tracking. This produces
  exactly the audit trail and evidenced governance process required by CMP-001
  (NIS2 governance obligations) and CMP-002 (TISAX AL2 change-management
  controls). The current service (cs-mer-15) is in Incident status with a lapsed
  contract as of 2026-05-25; reinstatement and incident resolution is therefore
  the immediate action. Affected-asset identification depends on IT Asset
  Management (addressing GAP-008), and high-risk changes reference the IT Risk
  Management risk register. Pricing tiers: Bronze £15, Silver £22, Gold £30
  /user/month.
  [inferred] [source:from: GAP-007 + portfolio://Governance/IT_Change_Management.md] [conf:H]
curated: true
notes: "Primary recommendation for GAP-007. Contract lapsed 2026-05-25 and currently in Incident status — incident resolution and reinstatement are time-sensitive. Effectiveness is enhanced when deployed alongside IT Risk Management (MAP-013) and IT Asset Management (MAP-014)."
---
```

```yaml
---
id: MAP-013
gap: GAP-007
proposed_service: "IT Risk Management"
portfolio_uri: "portfolio://Governance/IT_Risk_Management.md"
fit_rationale: >
  The IT Risk Management service provides governance-layer evidence that
  complements IT Change Management for GAP-007: the risk register supports
  high-risk change assessments within the CAB process, risk identification
  workshops address the informal ad-hoc decision-making culture documented in
  GAP-007, and annual board-level risk reporting provides the executive governance
  forum evidence required by CMP-001 (NIS2 governance) and CMP-002 (TISAX AL2
  governance). The service does not itself provide a change management process but
  removes the risk-register dependency gap that would otherwise leave high-risk
  change approvals without a documented risk foundation. This is an indirect but
  material fit as a governance-layer complement to the primary IT Change Management
  service.
  [inferred] [source:from: GAP-007 + portfolio://Governance/IT_Risk_Management.md] [conf:M]
curated: false
notes: "Secondary candidate for GAP-007. Also curated as primary for GAP-004 (MAP-007). Contracting IT Risk Management once covers both gaps — note this in the proposal to avoid double-counting."
---
```

```yaml
---
id: MAP-014
gap: GAP-008
proposed_service: "IT Asset Management"
portfolio_uri: "portfolio://Governance/IT_Asset_Management.md"
fit_rationale: >
  The IT Asset Management service directly addresses GAP-008: it provides
  hardware asset inventory with automated discovery reconciliation (covering
  servers, network devices, workstations, and peripherals), software asset
  inventory with version and licence entitlement tracking, full asset lifecycle
  management from procurement to secure disposal, licence compliance reporting,
  contract and warranty tracking with 90/30-day renewal alerts, asset criticality
  classification (input to vulnerability and risk management), and annual physical
  asset audit reconciliation. Current state is approximately 10% inventory
  coverage (25 of 240 devices); this service will close that gap and produce the
  complete accurate inventory required by CMP-001 (NIS2 asset-management
  obligations) and CMP-002 (TISAX AL2 inventory requirements). Asset criticality
  classification also feeds IT Change Management (MAP-012) and IT Risk Management
  (MAP-007/MAP-013), making this a foundational dependency service. MDM
  enrollment/policy enforcement and cloud SaaS subscription management are
  not included.
  [inferred] [source:from: GAP-008 + portfolio://Governance/IT_Asset_Management.md] [conf:H]
curated: true
notes: "Primary and sole recommendation for GAP-008. Foundational dependency for IT Change Management, IT Risk Management, Vulnerability Management, and EDR. MDM and cloud SaaS management not included. Pricing not confirmed in portfolio retrieval — marked TBC for proposal."
---
```

```yaml
---
id: MAP-015
gap: GAP-009
proposed_service: "[no-known-service]"
portfolio_uri: ""
fit_rationale: >
  Portfolio retrieval found no managed service covering NIS2 entity
  classification advisory or supervisory authority engagement for GAP-009.
  The closest candidates examined were IT Risk Management
  (portfolio://Governance/IT_Risk_Management.md) — which explicitly excludes
  legal or regulatory compliance gap assessments beyond IT controls mapping —
  and SIEM (portfolio://Security/SIEM.md) — whose CMP-001-mapped compliance
  reporting is tangential and does not address NCA registration, NIS2
  self-classification, or regulatory filing. No other service in the portfolio
  covers engagement with a national competent authority, NIS2 entity
  classification self-assessment, or regulatory submission. This gap requires
  specialist legal or regulatory advisory input outside the current MSP
  portfolio and is flagged for the 06-retro portfolio change-request backlog.
  [inferred] [source:from: GAP-009 + portfolio://Governance/IT_Risk_Management.md] [conf:H]
curated: false
notes: "Portfolio gap — surface in 06-retro change-request backlog. Recommend customer engages a legal or regulatory advisory firm with CMP-001 / national competent authority expertise to resolve entity classification before the CMP-001 deadline of 2027-05-26."
---
```

---

## 3. Portfolio Domains Searched

| Domain | Services reviewed | Head timestamp |
|--------|------------------|----------------|
| Security | SIEM.md, Network_Detection_and_Response.md, Threat_Intelligence.md, Business_Continuity.md, Backup_and_DR.md, Endpoint_Detection_and_Response.md, Identity_Access_Management.md, Device_Hardening.md, Mail_Security.md, Vulnerability_Management.md, Attack_Surface_Management.md, Deception.md, EOL_Services.md | 1779442954 (SIEM.md) … 1779443119 (Network_Detection_and_Response.md) |
| Governance | IT_Risk_Management.md, IT_Change_Management.md, IT_Asset_Management.md, IT_Knowledge_Management.md, IT_Project_Management.md | 1779443146 (IT_Risk_Management.md) … 1779443178 (IT_Project_Management.md) |
| Infrastructure | Patch_Management.md, Remote_Access_Management.md, Configuration_Management.md, Monitoring.md, Deployment.md | 1779442713 (Configuration_Management.md) … 1779442909 (Monitoring.md) |
| Workplace | Awareness_Training.md | 1779443206 (Awareness_Training.md) |
| Network | DNS.md (flagged as dependency of Mail Security — SPF/DKIM/DMARC management) | not retrieved (dependency reference only) |

---

## 4. Contradictions Surfaced This Phase

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| — | No contradictions detected during phase 03-mapping | n/a | n/a |

---

## 5. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T10:31:00Z | All four entry checklist items confirmed YES |
| Gate 3 — ratification | 2026-05-26T10:45:00Z | Consultant confirmed YES — service-map.md ratified |
