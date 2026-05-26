---
register: risks
harness_version: "0.2.0"
customer: "Meridian-Logistics"
---

# Risk Register

```yaml
---
id: RSK-001
title: TISAX AL2 assessment failure — December 2026
description: >
  Meridian-Logistics has an assessment booked for December 2026. The current absence of a documented information security policy framework, a formal Incident Response process, and a Business Continuity plan means the organisation is not assessment-ready. Failure would put automotive customer contracts at risk.
  [inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
likelihood: high
impact: high
owner: "Izayoi Nayuta (CISO)"
mitigation: >
  Accelerate IR process (G-03) and policy framework workstreams in phase 04-roadmap; prioritise all TISAX-gating items for delivery before October 2026 to allow a pre-assessment dry run.
triggered_by:
  - SIT-204
  - SIT-212
  - SIT-214
---
```

```yaml
---
id: RSK-002
title: NIS2 compliance failure within 12-month horizon
description: >
  The 12-month NIS2 attestation deadline (CMP-001) requires demonstrable technical controls, incident notification capability, and supply chain security oversight. Current gaps in SIEM, Business Continuity, and IR process mean the compliance posture is substantially below the required baseline.
  [inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
likelihood: medium
impact: high
owner: "Izayoi Nayuta (CISO)"
mitigation: >
  Define NIS2 control mapping in phase 02-gap; deploy SIEM, Business Continuity, and IR process as highest-priority roadmap items; validate entity classification with national competent authority.
triggered_by:
  - SIT-115
  - SIT-204
  - SIT-211
---
```

```yaml
---
id: RSK-003
title: Repeat ransomware attack due to unresolved detection and response gaps
description: >
  The same conditions that enabled the 2025 ransomware attack — inadequate detection capability and no rehearsed IR process — persist today. The absence of SIEM, NDR, and a Business Continuity plan means a repeat attack would likely result in similar or greater damage.
  [inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z] [conf:H]
likelihood: medium
impact: medium
owner: "Izayoi Nayuta (CISO)"
mitigation: >
  Deploy SIEM and Business Continuity service as first-priority items; stand up IR process (G-03) before next quarter; review and harden the company web portal that served as the 2025 initial access vector.
triggered_by:
  - SIT-115
  - SIT-214
---
```

```yaml
---
id: RSK-004
title: Security regression from contract expiry
description: >
  Device Hardening, Mail Security, and IT Change Management contracts expired or are expiring today. Without renewal, endpoint hardening baselines will degrade, phishing protection will lapse, and change audit-trail discipline will be lost — all during a compliance build period.
  [inferred] [source:from: customer-portal://contracts/org-meridian@2026-05-25T16:50:36.223Z + interview:2026-05-26/consultant] [conf:H]
likelihood: high
impact: medium
owner: "Izayoi Nayuta (CISO)"
mitigation: >
  Confirm renewal decisions for Device Hardening, Mail Security, and IT Change Management as an immediate action; if not renewed, implement compensating controls before the gaps widen.
triggered_by:
  - SIT-106
  - SIT-113
  - SIT-114
---
```

```yaml
---
id: RSK-005
title: IAM control effectiveness undermined by organisational resistance to MFA
description: >
  Contracted Gold-tier IAM service includes MFA enforcement, but elicited evidence indicates organisational resistance to MFA adoption. If MFA is not enforced across the estate, identity controls required by both CMP-001 and CMP-002 will not be demonstrable at assessment.
  [inferred] [source:from: interview:2026-05-26/consultant + customer-portal://contracts/cs-mer-8@2026-05-25T16:50:36.223Z] [conf:H]
likelihood: medium
impact: high
owner: "Izayoi Nayuta (CISO)"
mitigation: >
  Include an organisational change management workstream in phase 04-roadmap; set a firm MFA enforcement deadline; escalate to CEO (Cheng Zebang) sponsorship if CISO cannot drive adoption independently.
triggered_by:
  - SIT-109
  - SIT-213
---
```
