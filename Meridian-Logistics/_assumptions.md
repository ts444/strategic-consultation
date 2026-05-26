---
register: assumptions
harness_version: "0.2.0"
customer: "Meridian-Logistics"
---

# Assumptions Register

## ASM-001: NIS2 National Enforcement Deadline

[elicited] [source:interview:2026-05-26/consultant] [conf:M]

Assumes no earlier national supervisory authority audit or enforcement action has been
scheduled that would require NIS2 attestation before the 12-month engagement horizon.
If a supervisory authority contact date exists, this assumption must be revalidated
in phase 01-situation.

Requires revalidation: **Yes** — confirm with Izayoi Nayuta in phase 01.

**Validation status (phase 01):** Validated — no supervisory authority contact received (SIT-211). Assumption holds. Revalidation no longer required.

## ASM-002: MSP Delivery Capacity

[elicited] [source:interview:2026-05-26/consultant] [conf:M]

Assumes the new MSP is resourced and contracted to deliver security controls beyond
the capability of the small internal IT team. The exact split of responsibilities
between MSP and internal team is not yet defined and is deferred to phase 03-mapping.

Requires revalidation: **Yes** — resolve in phase 03-mapping.

**Resolution (phase 03-mapping):** Deferred — MSP delivery capacity accepted as a working assumption
for the mapping and roadmap phases. The formal MSP contract and responsibility matrix have not been
finalised; however, the engagement scope presupposes MSP ownership of controls flagged in
recommendations.md. Formal SLA and RACI documentation is captured as a Year 1 roadmap action.

```yaml
---
id: ASM-002
requires_revalidation: true
target_phase: 03-mapping
resolution_status: deferred
resolved_in_phase: 03-mapping
resolution_note: MSP delivery capacity not formally validated but accepted given engagement scope; MSP responsibilities and split with internal IT team to be documented in SLA/RACI before Phase 04 implementation begins
---
```

## ASM-003: TISAX Assessment Level

[elicited] [source:interview:2026-05-26/consultant] [conf:M]

Assumes the December 2026 TISAX assessment is at Assessment Level 2 (AL2), which is
standard for automotive logistics partners handling sensitive vehicle information.
If the customer contracts require AL3, the scope and effort of the engagement will
increase materially.

Requires revalidation: **Yes** — confirm with Izayoi Nayuta in phase 01.

**Validation status (phase 01):** Confirmed — TISAX assessment is at AL2 (SIT-212). Assumption confirmed. No further revalidation required.
