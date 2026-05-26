---
phase: "06-retro"
status: ratified
harness_version: "0.2.0"
template: "retro@1.0.0"
ratified_by: "Tim S"
ratified_at: "2026-05-26T12:50:00Z"
produced_by: "synthesizer"
---

# Phase 06 — Retrospective

**Customer:** Meridian-Logistics
**Engagement dates:** 2026-05-26 — 2026-05-26
**Phases completed:** 6 (00-intake, 01-situation, 02-gap, 03-mapping, 04-roadmap, 05-handover)
**Total ratified claim atoms:** 117 (70 SIT + 9 GAP + 15 MAP + 9 REC + 14 RMI)

## What Worked

1. The claim-atom discipline (label + source + conf on every assertion) held across all 117 ratified atoms with no validator violations relating to missing annotations in the final ratified artifacts after the harness template comment-block fix was applied [inferred] [source:from: CR-2026-001] [conf:H].

2. HITL gates performed as designed: all 12 gates (2 per phase × 6 phases) were confirmed YES without loopback, indicating the pre-flight checklists correctly scoped each phase before synthesis [inferred] [source:engagement-record:Meridian-Logistics] [conf:H].

3. The phased structure produced coherent traceability: each GAP traces to at least one SIT claim, each MAP to a GAP, each REC to a MAP, and each RMI to a REC. No orphaned claims were detected across the 117-atom corpus [inferred] [source:engagement-record:Meridian-Logistics] [conf:H].

4. Quick-win identification was effective: 4 of 14 roadmap items (RMI-001 Mail Security reinstatement, RMI-002 Device Hardening reinstatement, RMI-003 IT Change Management reinstatement, RMI-005 MFA enforcement) are zero-integration-overhead quick wins delivering immediate risk reduction on day one of the engagement. RMI-005 is notably zero-cost, activating an already-contracted capability [inferred] [source:from: 04-roadmap/roadmap.md] [conf:H].

5. The service-map exhaustive + curated two-layer approach (service-map.md + recommendations.md) cleanly separated the full evidence record from the curated actions, preventing information overload in the handover while preserving traceability [inferred] [source:from: 03-mapping/service-map.md] [conf:H].

6. The [no-known-service] mechanism worked correctly for GAP-009: the mapping phase did not silently omit the gap or force a poor-fit service recommendation; instead it surfaced the portfolio capability gap cleanly for the retro backlog [inferred] [source:from: 03-mapping/service-map.md] [conf:H].

## What Failed

1. The budget envelope declared at intake (BUD-001: capex_y1 £50k, opex_annual £20k, hard limit £200k total) was grossly misaligned with the programme cost. Known Silver-tier opex across recommended new services totals at least £492,480/yr — roughly 25× the declared £20k/yr opex envelope and exceeding the £200k total hard limit in a single year [inferred] [source:from: 04-roadmap/roadmap.md] [conf:H]. The misalignment was surfaced explicitly in §5 Budget Overview of the roadmap but could not be resolved within the engagement because resolution requires a stakeholder conversation with the CEO outside the MSP's direct control [inferred] [source:from: 05-handover/handover.md] [conf:H]. The intake template did not prompt for a sanity-check against typical MSP programme costs before the envelope was fixed [inferred] [source:from: 00-intake/scope.md] [conf:M]. This warrants a template change request (see CR-2026-005).

2. ASM-002 (MSP delivery capacity) was logged at intake as "requires revalidation in phase 03-mapping" but was not explicitly resolved during mapping [inferred] [source:from: 00-intake/_assumptions.md] [conf:H]. The service-map and recommendations phases mapped all required services to portfolio entries and implicitly assumed MSP delivery, but never produced a formal resolution entry in _assumptions.md [inferred] [source:from: 03-mapping/service-map.md] [conf:H]. At engagement close, ASM-002 remains technically open. This is a process gap in the 03-mapping HITL Gate 1 checklist (see CR-2026-006).

## What Surprised

1. Zero contradictions across all six phases was unexpected. The engagement drew on three independent data sources (consultant interview, customer-portal API, MSP portfolio) across 117 claim atoms; a non-zero contradiction rate would typically be expected when interview-elicited data meets portal-retrieved data [inferred] [source:engagement-record:Meridian-Logistics] [conf:M]. The most plausible explanation is that the customer portal data accurately reflected known-incomplete state (the asset-registry incompleteness was openly acknowledged at SIT-208), preventing source-vs-interview contradictions from arising [inferred] [source:from: 01-situation/situation.md] [conf:M]. The result is a positive signal for data source coherence but also raises the question of whether the contradiction-detection mechanism was calibrated conservatively.

2. The budget escalation magnitude (≈25×) is not a rounding difference. It suggests either the declared envelope was a placeholder rather than a genuine constraint, or that the customer has not yet been presented with realistic programme cost expectations [inferred] [source:from: 04-roadmap/roadmap.md] [conf:M]. Either way, the handover flag for this item (OQ-P04-001) is the most consequential open item from the engagement [inferred] [source:from: 05-handover/handover.md] [conf:H].

3. Two critical portfolio service gaps emerged simultaneously: no DFIR / 24/7 IR retainer, and no NIS2 regulatory advisory [inferred] [source:from: 03-mapping/service-map.md] [conf:H]. Both are high-value adjacent services for a compliance-led MSP engagement. The DFIR gap is particularly notable because the customer's 2025 ransomware incident (GAP-002) is the dominant driver for the engagement, yet the MSP cannot offer a full incident response retainer and must refer to a third party [inferred] [source:from: 03-mapping/recommendations.md] [conf:H].

## Data-Quality Meta-Findings

### 4.1 Contradiction statistics

| Metric | Count |
|--------|-------|
| Contradictions raised (total) | 0 |
| Resolved via path (a) — source update | 0 |
| Resolved via path (b) — supersedes marker | 0 |
| Resolved via path (c) — assumption logged | 0 |
| Resolved via path (d) — decision logged | 0 |
| Unresolved at engagement close | 0 |

The `_contradictions.md` register is empty — no contradictions were surfaced or raised at any phase [inferred] [source:from: _contradictions.md] [conf:H]. The `_decisions.md` register is likewise empty, consistent with the zero-contradiction outcome [inferred] [source:from: _decisions.md] [conf:H].

### 4.2 MSP portfolio observations

1. **No DFIR / 24/7 staffed IR retainer service in portfolio.** GAP-002 (No Incident Response capability) could only be mapped to Business Continuity as a partial fit (MAP-004). The Business Continuity service includes incident containment support, tabletop exercise facilitation, and communication templates, but explicitly excludes a 24/7 staffed IR retainer and full DFIR capability [inferred] [source:from: 03-mapping/service-map.md] [conf:H]. No other portfolio service fills this gap. This is a confirmed portfolio capability gap raised as CR-2026-003. Reference: `portfolio://Security/Business_Continuity.md`.

2. **No NIS2 entity classification / regulatory advisory service in portfolio.** GAP-009 produced the engagement's single [no-known-service] result (MAP-015). IT Risk Management explicitly excludes legal/regulatory compliance gap assessments beyond IT controls mapping [inferred] [source:from: 03-mapping/service-map.md] [conf:H]. No portfolio service covers NIS2 self-classification, supervisory authority engagement, or regulatory filing. Raised as CR-2026-004. Reference: `portfolio://Governance/IT_Risk_Management.md`.

### 4.3 Customer-portal observations

1. **Asset registry grossly incomplete.** The customer-portal asset registry (`customer-portal://assets/org-meridian@2026-05-25T16:50:36.209Z`) recorded only 25 devices, 25 users, and 10 licences against a confirmed actual headcount of 240 employees with one device and one user account each — approximately 10% coverage [inferred] [source:from: 01-situation/situation.md] [conf:H]. This was confirmed as a known incompleteness by the customer (SIT-208). The low coverage did not block situation analysis but required the synthesizer to reason from the interview-elicited headcount figure rather than the portal's asset count, reducing overall confidence in asset-scope claims.

2. **No customer-portal data freshness issue.** All retrieved customer-portal resources carried timestamps (e.g., `2026-05-25T16:50:36.223Z` for contracts, `2026-05-25T16:50:36.209Z` for assets) [inferred] [source:from: 01-situation/situation.md] [conf:H]. Data freshness was not a concern; all resources appeared to reflect current state at engagement open.

## Change Requests

| CR ID | Title | Target | Origin phase |
|-------|-------|--------|--------------|
| CR-2026-003 | Portfolio gap — no DFIR / 24/7 staffed IR retainer service | tool (portfolio) | 03-mapping |
| CR-2026-004 | Portfolio gap — no NIS2 entity classification / regulatory advisory service | tool (portfolio) | 03-mapping |
| CR-2026-005 | Intake template — add budget-validation prompt before envelope is fixed | template | 00-intake |
| CR-2026-006 | Mapping phase — require explicit resolution of open assumptions before ratification | template | 03-mapping |

### CR-2026-003 — Portfolio gap: no DFIR / 24/7 staffed IR retainer service

- **File:** `backlog/change-requests/CR-2026-003.md`
- **Target:** tool (portfolio)
- **Origin phase:** 03-mapping
- **Summary:** Add a DFIR / IR Retainer service to the MSP portfolio (or extend Business Continuity to include a 24/7-staffed IR retainer tier). GAP-002 — the customer's most critical gap, stemming from a 2025 paid-ransom ransomware incident — could only be mapped to Business Continuity as a partial fit. The proposed service would cover 24/7 staffed IR retainer with defined SLA, full DFIR capability, SIEM integration, and ransomware-specific playbooks [inferred] [source:from: 03-mapping/service-map.md] [conf:H].

### CR-2026-004 — Portfolio gap: no CMP-001 entity classification / regulatory advisory service

- **File:** `backlog/change-requests/CR-2026-004.md`
- **Target:** tool (portfolio)
- **Origin phase:** 03-mapping
- **Summary:** Add a NIS2 Regulatory Advisory service (or a Compliance Advisory service) covering entity classification self-assessment, supervisory authority notification and registration, NIS2 obligation scoping, and ongoing regulatory monitoring. Addresses the engagement's single [no-known-service] result (MAP-015 / GAP-009) and removes the third-party dependency for a prerequisite to the customer's NIS2 attestation goal [inferred] [source:from: 03-mapping/service-map.md] [conf:H].

### CR-2026-005 — Intake template: add budget-validation prompt before envelope is fixed

- **File:** `backlog/change-requests/CR-2026-005.md`
- **Target:** template
- **Origin phase:** 00-intake
- **Summary:** Update `templates/scope.template.md` §3.1 to prompt the consultant to estimate the likely number of new services required, provide a worked Silver-tier per-user-per-month cost example for NIS2/TISAX programmes, and flag a likely under-scoped envelope before ratification. Surfaces the budget mismatch at phase 00 rather than phase 04, where the 25× gap (£200k declared vs ≥£492k/yr identified) became a blocking handover risk [inferred] [source:from: 04-roadmap/roadmap.md] [conf:H].

### CR-2026-006 — Mapping phase: require explicit resolution of open assumptions before ratification

- **File:** `backlog/change-requests/CR-2026-006.md`
- **Target:** template
- **Origin phase:** 03-mapping
- **Summary:** Add a 03-mapping HITL Gate 1 checklist item requiring confirmation that all `requires_revalidation` assumptions targeting this phase are resolved (or explicitly deferred) in `_assumptions.md`, and update `templates/service-map.template.md` with an "Open Assumptions Resolution" section. Closes the process gap that left ASM-002 (MSP delivery capacity) technically open at engagement close [inferred] [source:from: 00-intake/_assumptions.md] [conf:H].

## HITL Confirmation Record

All gates confirmed YES with no loopbacks:

| Phase | Gate 1 | Gate 3 |
|-------|--------|--------|
| 00-intake | 2026-05-26T00:00:00Z | 2026-05-26T00:00:00Z |
| 01-situation | 2026-05-26T09:00:00Z | 2026-05-26T09:30:00Z |
| 02-gap | 2026-05-26T10:00:00Z | 2026-05-26T10:15:00Z |
| 03-mapping | 2026-05-26T10:31:00Z | 2026-05-26T10:45:00Z |
| 04-roadmap | 2026-05-26T11:00:00Z | 2026-05-26T11:30:00Z |
| 05-handover | 2026-05-26T12:00:00Z | 2026-05-26T12:30:00Z |
| 06-retro | 2026-05-26T12:46:00Z | 2026-05-26T12:50:00Z |

**Total gates:** 14 (2 per phase × 7 phases). **Loopbacks:** 0. **Failed gates:** 0.
