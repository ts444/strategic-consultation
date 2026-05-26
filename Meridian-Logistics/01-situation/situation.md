---
phase: "01-situation"
status: ratified
harness_version: "0.2.0"
template: "situation@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T09:30:00Z"
produced_by: "synthesizer"
---

# Situation Summary: Meridian-Logistics

> **Harness version:** `0.2.0`
> **Template:** `situation@1.0.0`
> **Phase:** 01-situation
> **Entry condition:** `00-intake/scope.md` frontmatter `status: ratified`

---

## §1 Current Technology Landscape

### §1.1 Infrastructure and Hosting

Meridian-Logistics operates a hybrid IT estate: SAP ERP and traditional core services are hosted on-premises; Microsoft Azure is used for new workloads and redundancy.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

The organisation operates approximately 240 endpoint devices, consistent with its 240-employee headcount; the customer portal asset registry is known to be incomplete and records only 25 devices.
[inferred] [source:from: customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z + interview:2026-05-26/consultant] [conf:H]

### §1.2 Network and Connectivity

VPN and WAN services are contracted at Healthy status, providing remote connectivity. Detailed network architecture has not been directly evidenced by retrieval; further discovery is deferred to phase 02.
[assumed] [source:from: customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z] [conf:M]

### §1.3 Security Controls

Six MSP security services are contracted and in Healthy status: EDR (Gold SLA), IAM (Gold SLA), Vulnerability Management (Gold SLA), Backup and DR (Silver SLA), Mail Security (Silver SLA, contract expiring), and Device Hardening (Silver SLA, contract expiring).
[inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

Critical detection and response capabilities — including SIEM, NDR, Business Continuity, Threat Intelligence, and a formal Incident Response service — are not contracted and have not been deployed.
[inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + interview:2026-05-26/consultant] [conf:H]

### §1.4 Identity and Access Management

IAM services (PIM, PAM, MFA enforcement, SSO, directory management) are contracted at Gold tier and in Healthy status. However, organisational resistance to MFA has been elicited; the gap between contracted capability and actual enforcement maturity must be assessed.
[inferred] [source:from: customer-portal://contracts/cs-mer-8@2026-05-25T16:50:36.223Z + interview:2026-05-26/consultant] [conf:H]

### §1.5 End-User Computing

The endpoint fleet consists of 240 Dell Latitude 5540 laptops running Windows 11, managed under the MSP's EDR (Gold) and Device Hardening (Silver) services; the Device Hardening contract expires today and its renewal is under review.
[inferred] [source:from: customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

### §1.6 Applications and Data

Core business applications are SAP ERP (on-premises) and Microsoft 365 E3 (cloud productivity, approximately 250 seats); Adobe Acrobat DC is also licenced for document management.
[inferred] [source:from: customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z + interview:2026-05-26/consultant] [conf:H]

No dedicated data loss prevention or outbound data control service is contracted; the degree of protection for sensitive automotive customer data handled in SAP and Microsoft 365 is not fully evidenced from current retrieval.
[inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + interview:2026-05-26/consultant] [conf:M]

---

## §2 Organisational Context

### §2.1 IT Team Structure and Capability

The internal IT function comprises six staff: two helpdesk, two infrastructure, one dedicated security resource, and one compliance resource. The CISO (Izayoi Nayuta) leads the security and compliance programme; the CTO is Asim Raza.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:H]

A six-person IT team serving a 240-employee regulated-sector organisation is unlikely to deliver NIS2 attestation or TISAX certification without substantial MSP support; internal specialist security capacity is limited to one person.
[inferred] [source:from: interview:2026-05-26/consultant + portfolio://Governance/IT_Risk_Management.md] [conf:M]

### §2.2 IT Governance and Decision-Making

IT governance is informal: strategic technology decisions are made in meetings attended by the CEO (Cheng Zebang), CISO (Izayoi Nayuta), and CTO (Asim Raza); no formal IT steering committee, change advisory board, or security governance body exists.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:H]

IT Change Management is in Incident status and its contract expires today; this reduces audit-trail confidence and creates risk of undocumented changes during a compliance build period.
[inferred] [source:from: customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z + customer-portal://contracts/cs-mer-15@2026-05-25T16:50:36.223Z] [conf:H]

### §2.3 Vendor and Partner Landscape

Key technology vendors are SAP (ERP, significant on-premises data holdings), Microsoft (Azure cloud platform and Microsoft 365 productivity suite), and the MSP (security programme delivery). No other significant managed service providers have been identified.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:H]

No third-party or vendor access management service is contracted; SAP and Microsoft Azure access controls are assumed to be managed through internal IT and the contracted IAM service, but no external vendor access review process has been evidenced.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:M]

### §2.4 IT Maturity Assessment

IT maturity at Meridian-Logistics is assessed as Low. Evidence converges from five directions: (1) existing IT security policies are outdated and not actively enforced; (2) a ransomware attack in 2025 resulted in full ransom payment, demonstrating inadequate incident detection and response capability at the time; (3) critical controls — SIEM, Business Continuity, NDR — are absent from the contracted estate; (4) IT Change Management is in Incident status; and (5) cultural resistance to controls such as MFA has been reported. The engaged security controls (EDR, IAM, Vulnerability Management) establish a foundation, but policy, process, and cultural maturity are low.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z] [conf:M]

---

## §3 Key Facts (Retrieved Evidence)

| SIT-id | Claim summary | Label | Source | Conf |
|--------|---------------|-------|--------|------|
| SIT-001 | SIEM service provides NIS2-mapped compliance reporting | known | portfolio://Security/SIEM.md | H |
| SIT-002 | SIEM includes incident timeline reconstruction and forensic evidence preservation | known | portfolio://Security/SIEM.md | H |
| SIT-003 | SIEM does not include 24/7 SOC/active threat hunting as standard (MDR add-on required) | known | portfolio://Security/SIEM.md | H |
| SIT-004 | Business Continuity service includes incident containment support (network isolation, credential reset, eviction procedures) | known | portfolio://Security/Business_Continuity.md | H |
| SIT-005 | Business Continuity service includes stakeholder notification communication templates for incidents | known | portfolio://Security/Business_Continuity.md | H |
| SIT-006 | Full DFIR retainer and 24/7 staffed IR retainer are excluded from Business Continuity service (separate engagement) | known | portfolio://Security/Business_Continuity.md | H |
| SIT-007 | Business Continuity service includes annual tabletop exercise facilitation | known | portfolio://Security/Business_Continuity.md | H |
| SIT-008 | Backup and DR service implements 3-2-1-1 principle with immutable/air-gap backup protection | known | portfolio://Security/Backup_and_DR.md | H |
| SIT-009 | Backup and DR service includes monthly restore testing and annual DR exercise | known | portfolio://Security/Backup_and_DR.md | H |
| SIT-010 | Vulnerability Management service provides weekly authenticated scanning with CVSS/EPSS/KEV-based prioritisation | known | portfolio://Security/Vulnerability_Management.md | H |
| SIT-011 | Vulnerability Management service produces compliance evidence trail satisfying audit requirements | known | portfolio://Security/Vulnerability_Management.md | H |
| SIT-012 | IAM service includes MFA enforcement, PIM with JIT elevation, and PAM with session recording and credential vaulting | known | portfolio://Security/Identity_Access_Management.md | H |
| SIT-013 | IAM service includes quarterly access certification campaigns | known | portfolio://Security/Identity_Access_Management.md | H |
| SIT-014 | EDR service includes automated threat containment (process termination, network isolation) with MITRE ATT&CK-aligned detection | known | portfolio://Security/Endpoint_Detection_and_Response.md | H |
| SIT-015 | EDR service includes peripheral control (USB block/allow lists, removable media restrictions) relevant to automotive data handling | known | portfolio://Security/Endpoint_Detection_and_Response.md | H |
| SIT-016 | Attack Surface Management service provides continuous external asset discovery and exposure management | known | portfolio://Security/Attack_Surface_Management.md | H |
| SIT-017 | Attack Surface Management includes leaked credential monitoring across paste sites and breach databases | known | portfolio://Security/Attack_Surface_Management.md | H |
| SIT-018 | Threat Intelligence service provides sector-specific monthly briefings and dark web monitoring | known | portfolio://Security/Threat_Intelligence.md | H |
| SIT-019 | Threat Intelligence service includes quarterly threat landscape review aligned to the customer risk register | known | portfolio://Security/Threat_Intelligence.md | H |
| SIT-020 | Device Hardening service applies CIS Benchmark baselines with compliance scanning and deviation reporting | known | portfolio://Security/Device_Hardening.md | H |
| SIT-021 | EOL Services Management service provides compensating controls and EOL exception documentation for compliance audit | known | portfolio://Security/EOL_Services.md | H |
| SIT-022 | Mail Security service provides attachment sandboxing, SPF/DKIM/DMARC management, and outbound DLP scanning | known | portfolio://Security/Mail_Security.md | H |
| SIT-023 | NDR service analyses east-west traffic for lateral movement and C2/DNS-tunnelling detection | known | portfolio://Security/Network_Detection_and_Response.md | H |
| SIT-024 | Macrosegmentation service provides NGFW policy management with explicit deny-all defaults and quarterly rule review | known | portfolio://Security/Macrosegmentation.md | H |
| SIT-025 | Microsegmentation service provides workload-to-workload east-west access controls for hybrid cloud environments | known | portfolio://Security/Microsegmentation.md | H |
| SIT-026 | NAC service enforces 802.1X with device posture assessment and rogue device quarantine | known | portfolio://Security/Network_Access_Control.md | H |
| SIT-027 | Secret Management service includes automated rotation, certificate lifecycle management, and access audit logging | known | portfolio://Security/Secret_Management.md | H |
| SIT-028 | DDoS Protection service provides always-on mitigation with annual simulation exercise | known | portfolio://Security/DDoS_Protection.md | H |
| SIT-029 | Deception Technology service provides near-zero-false-positive early warning via decoy assets | known | portfolio://Security/Deception.md | H |
| SIT-030 | IT Risk Management service maintains risk register with quarterly review aligned to ISO 27005/NIST SP 800-30 | known | portfolio://Governance/IT_Risk_Management.md | H |
| SIT-031 | IT Risk Management service excludes external certification body assessments (NIS2/TISAX assessments require separate engagement) | known | portfolio://Governance/IT_Risk_Management.md | H |
| SIT-032 | IT Asset Management service provides criticality classification as input to vulnerability and risk management | known | portfolio://Governance/IT_Asset_Management.md | H |
| SIT-033 | Patch Management service includes emergency patch deployment within defined SLA and exception documentation | known | portfolio://Infrastructure/Patch_Management.md | H |
| SIT-034 | Remote Access Management service enforces MFA and device posture for all remote sessions with ZTNA support | known | portfolio://Infrastructure/Remote_Access_Management.md | H |
| SIT-035 | Remote Access Management service includes time-limited audited vendor access controls | known | portfolio://Infrastructure/Remote_Access_Management.md | H |
| SIT-036 | Security Awareness Training service delivers monthly modules, quarterly phishing simulations, and compliance completion reports | known | portfolio://Workplace/Awareness_Training.md | H |
| SIT-037 | IT Change Management service includes emergency change fast-track with retroactive risk documentation for audit | known | portfolio://Governance/IT_Change_Management.md | M |
| SIT-101 | Customer portal records 60 assets: 25 devices, 25 users, 10 licenses (registry confirmed incomplete) | known | customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z | H |
| SIT-102 | All 25 registered devices are Dell Latitude 5540 laptops running Windows 11 | known | customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z | H |
| SIT-103 | 25 user asset records span IT, Operations, and Finance; actual headcount is 240 (registry incomplete) | known | customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z | H |
| SIT-104 | License assets: alternating Adobe Acrobat DC and Microsoft 365 E3, each 50 seats (×5 = 250 seats each) | known | customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z | H |
| SIT-105 | 15 contracted MSP services across five domains: Network (2), Infrastructure (3), Security (6), Workplace (2), Governance (2) | known | customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z | H |
| SIT-106 | IT Change Management (cs-mer-15) is in Incident status at Gold SLA; contract end-date is 2026-05-25 (today) | known | customer-portal://contracts/cs-mer-15@2026-05-25T16:50:36.223Z | H |
| SIT-107 | Configuration Management (cs-mer-9) is in Degraded status at Silver SLA; contract runs to 2026-08-25 | known | customer-portal://contracts/cs-mer-9@2026-05-25T16:50:36.223Z | H |
| SIT-108 | EDR (cs-mer-6) contracted at Gold SLA (99.9% / 30-min response), healthy, runs to 2026-08-25 | known | customer-portal://contracts/cs-mer-6@2026-05-25T16:50:36.223Z | H |
| SIT-109 | IAM (cs-mer-8) contracted at Gold SLA, covers PIM/PAM/SSO/MFA, healthy, runs to 2026-11-25 | known | customer-portal://contracts/cs-mer-8@2026-05-25T16:50:36.223Z | H |
| SIT-110 | Vulnerability Management (cs-mer-11) contracted at Gold SLA, healthy, runs to 2026-11-25 | known | customer-portal://contracts/cs-mer-11@2026-05-25T16:50:36.223Z | H |
| SIT-111 | Infrastructure Monitoring (cs-mer-4) contracted at Gold SLA, healthy, runs to 2026-08-25 | known | customer-portal://contracts/cs-mer-4@2026-05-25T16:50:36.223Z | H |
| SIT-112 | Backup and DR (cs-mer-5) contracted at Silver SLA with ransomware resilience, healthy, runs to 2026-11-25 | known | customer-portal://contracts/cs-mer-5@2026-05-25T16:50:36.223Z | H |
| SIT-113 | Device Hardening (cs-mer-10) contracted at Silver SLA, healthy, but contract end-date is 2026-05-25 (today) | known | customer-portal://contracts/cs-mer-10@2026-05-25T16:50:36.223Z | H |
| SIT-114 | Mail Security (cs-mer-7) contracted at Silver SLA, healthy, but contract end-date is 2026-05-25 (today) | known | customer-portal://contracts/cs-mer-7@2026-05-25T16:50:36.223Z | H |
| SIT-115 | No SIEM, Business Continuity, NDR, Threat Intelligence, or Incident Response service is contracted | known | customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z | H |
| SIT-116 | Compliance posture: Network (2 healthy), Infrastructure (2 healthy, 1 degraded), Security (6 healthy), Workplace (2 healthy), Governance (1 healthy, 1 incident) | known | customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z | H |
| SIT-117 | IT Change Management is the only service in Incident status across all domains | known | customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z | H |
| SIT-118 | Configuration Management is the only service in Degraded status (Infrastructure domain) | known | customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z | H |
| SIT-119 | All six Security-domain contracted services are in Healthy status | known | customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z | H |

---

## §4 Key Elicitations (Interviewer Output)

| SIT-id | Claim summary | Label | Source | Conf |
|--------|---------------|-------|--------|------|
| SIT-201 | Meridian-Logistics has 240 employees and approximately £10 million in annual revenue | elicited | interview:2026-05-26/consultant | H |
| SIT-202 | CTO is Asim Raza; no dedicated IT Manager or IT Director exists | elicited | interview:2026-05-26/consultant | H |
| SIT-203 | IT team comprises 6 staff: 2 helpdesk, 2 infrastructure, 1 security, 1 compliance | elicited | interview:2026-05-26/consultant | H |
| SIT-204 | Existing IT and information security policies are outdated and not in active use | elicited | interview:2026-05-26/consultant | H |
| SIT-205 | IT governance is informal: strategic decisions are made in meetings with CEO, CISO, and CTO; no formal steering committee exists | elicited | interview:2026-05-26/consultant | H |
| SIT-206 | Key technology vendors are SAP (ERP) and Microsoft (preferred cloud platform, Azure and Microsoft 365) | elicited | interview:2026-05-26/consultant | H |
| SIT-207 | IT estate is hybrid cloud: traditional core services on-premises, Microsoft Azure used for new services and redundancy | elicited | interview:2026-05-26/consultant | H |
| SIT-208 | Customer portal asset registry is incomplete; every employee has one device, one user account, and one license (240 of each) | elicited | interview:2026-05-26/consultant | H |
| SIT-209 | IT Change Management, Device Hardening, and Mail Security contracts are in a known grace period for renewal; this consultation will inform renewal decisions | elicited | interview:2026-05-26/consultant | H |
| SIT-210 | Configuration Management is in Degraded status due to a known issue; restoration to active status is in progress | elicited | interview:2026-05-26/consultant | H |
| SIT-211 | No NIS2 supervisory authority contact has been received; Meridian-Logistics wishes to be prepared if and when contact is made (validates ASM-001) | elicited | interview:2026-05-26/consultant | H |
| SIT-212 | TISAX assessment is confirmed at Assessment Level 2 (AL2), as assumed in ASM-003 | elicited | interview:2026-05-26/consultant | H |
| SIT-213 | Staff resistance to security controls that reduce flexibility exists, notably regarding MFA adoption; this is a cultural and political constraint | elicited | interview:2026-05-26/consultant | H |
| SIT-214 | A ransomware attack occurred in 2025: initial access via an unsecured company portal, important VMs encrypted, ransom paid in full due to inadequate incident response capability | elicited | interview:2026-05-26/consultant | H |

---

## §5 Situation Synthesis

### §5.1 Strengths

A working security foundation is in place: EDR (Gold), IAM (Gold, including PIM/PAM/MFA), Vulnerability Management (Gold), and Backup and DR (Silver) are contracted and healthy, providing detection, identity control, and resilience baselines.
[inferred] [source:from: customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

Dedicated CISO and compliance roles provide organisational accountability for the security and compliance programme.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:H]

The MSP portfolio contains services sufficient to address the technical control requirements of both CMP-001 and CMP-002; no portfolio gap has been identified from retrieval.
[inferred] [source:from: portfolio://Security/Business_Continuity.md + portfolio://Security/SIEM.md] [conf:H]

### §5.2 Weaknesses / Problem Areas

The 2025 ransomware attack exposed three critical gaps that remain unresolved: absence of centralised log aggregation and alerting (no SIEM), no documented Business Continuity plan, and no rehearsed Incident Response process; the same conditions exist today.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

IT and information security policies are outdated; both CMP-001 and CMP-002 frameworks require a documented and actively enforced information security policy baseline, which is currently absent.
[inferred] [source:from: interview:2026-05-26/consultant + portfolio://Governance/IT_Risk_Management.md] [conf:H]

Three contracted services (IT Change Management, Device Hardening, Mail Security) have reached or passed their contract end-date today; without renewal, coverage against phishing (mail), endpoint hardening, and change audit-trail will degrade.
[inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + interview:2026-05-26/consultant] [conf:H]

Reported resistance to MFA adoption creates a risk that the contracted Gold IAM service — which includes MFA enforcement — is not fully utilised; this would undermine identity controls required by both CMP-001 and CMP-002.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/cs-mer-8@2026-05-25T16:50:36.223Z] [conf:H]

The IT governance model is informal and lacks audit-trail discipline; IT Change Management in Incident status compounds this during a period when documented controls evidence will be required for both CMP-001 and CMP-002 assessments.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://compliance-posture/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

### §5.3 Strategic Implications for the Roadmap

Achieving NIS2 attestation (G-01) within the 12-month horizon requires deploying SIEM, Business Continuity, and Incident Response capabilities that are currently absent, alongside validating entity classification with the national competent authority; the existing security controls estate provides a foundation but is insufficient on its own.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

The TISAX AL2 December 2026 assessment deadline (G-02) is the primary hard constraint; all security workstreams must be sequenced to deliver assessment-ready evidence before the assessment date.
[inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]

The Incident Response programme (G-03) must be treated as an urgent workstream: it is required evidence for the TISAX assessment, addresses the 2025 attack vulnerability, and supports NIS2 incident notification obligations.
[inferred] [source:from: interview:2026-05-26/consultant + portfolio://Security/Business_Continuity.md] [conf:H]

At 240 employees and approximately £10 million annual revenue, Meridian-Logistics is likely an "important entity" under the applicable regulatory framework (CMP-001); this classification should be validated with the national competent authority, as obligations differ materially from "essential entity" requirements.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:M]

A change management programme will be required alongside technical controls to overcome reported resistance to security measures; purely technical remediation without an organisational change component risks non-adoption of deployed controls.
[inferred] [source:from: interview:2026-05-26/consultant] [conf:M]

---

## §6 Compliance Posture

| CMP-id | Framework | Current posture | Evidence | Conf |
|--------|-----------|-----------------|----------|------|
| CMP-001 | NIS2 Directive | Partially evidenced. Technical controls in place: EDR, IAM, Vulnerability Management, and Backup and DR are contracted and healthy. Significant gaps: no SIEM, no Business Continuity plan, no Incident Response process, no NDR, and outdated security policies. Entity classification as important or essential entity requires validation with the national competent authority. No supervisory authority contact received to date. | SIT-108, SIT-109, SIT-110, SIT-112, SIT-115, SIT-204, SIT-211 | M |
| CMP-002 | TISAX (AL2) | Partially evidenced. Confirmed at Assessment Level 2. Technical controls aligned to AL2: EDR, IAM, Device Hardening, Vulnerability Management, and Backup and DR are in place. Gaps: information security policy framework is outdated, no formal Incident Response process documented, Business Continuity plan absent, and staff security awareness training not evidenced. Contract expiry of Device Hardening today creates a coverage risk. | SIT-108, SIT-109, SIT-110, SIT-112, SIT-113, SIT-204, SIT-212 | M |

---

## §7 Contradictions Surfaced This Phase

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| — | No contradictions detected during phase 01-situation | n/a | n/a |

---

## §8 Risks Identified This Phase

| RSK-id | Title | Likelihood | Impact | Owner |
|--------|-------|------------|--------|-------|
| RSK-001 | TISAX AL2 assessment failure — December 2026 | H | H | Izayoi Nayuta (CISO) |
| RSK-002 | NIS2 compliance failure within 12-month horizon | H | H | Izayoi Nayuta (CISO) |
| RSK-003 | Repeat ransomware attack due to unresolved detection and response gaps | H | H | Izayoi Nayuta (CISO) |
| RSK-004 | Security regression from contract expiry (Device Hardening, Mail Security, IT Change Management) | M | H | Izayoi Nayuta (CISO) |
| RSK-005 | IAM control effectiveness undermined by organisational resistance to MFA | M | H | Izayoi Nayuta (CISO) |

---

## §9 HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | 2026-05-26T09:00:00Z | All four entry checklist items confirmed YES |
| Gate 3 — ratification | 2026-05-26T09:30:00Z | Consultant confirmed YES — situation.md ratified |
