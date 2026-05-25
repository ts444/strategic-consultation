---
phase: "05-handover"
status: draft
harness_version: "0.1.0"
template: "handover@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. '## Executive Narrative' H2 section exists and contains a customer-facing
     summary of the engagement findings and recommended path forward.
  2. '## Roadmap Summary' H2 section exists and reproduces or references the
     ratified roadmap from 04-roadmap/roadmap.md.
  3. '## Decision Log' H2 section exists and reproduces all entries from
     _decisions.md, including overrides: pointers.
  4. '## Assumption Register' H2 section exists and reproduces all active
     entries from _assumptions.md.
  5. '## Risk Log' H2 section exists and reproduces all open entries from
     _risks.md.
  6. This document MUST NOT contain meta-findings about MSP portal hygiene
     (data quality, freshness issues, tooling gaps in the MSP portfolio).
     Those findings belong exclusively in 06-retro/retro.md.
     (See: MSP PORTAL HYGIENE EXCLUSION comment below.)
  7. Validator reports zero violations.
  8. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 05-handover.
  9. Consultant has reviewed and ratified via HITL gate 3.
  10. Frontmatter `status` changed to `ratified`; `ratified_by` and
      `ratified_at` filled before committing.

MSP PORTAL HYGIENE EXCLUSION: Any observations about the quality, freshness,
or completeness of MSP portfolio data (e.g., "service X had no updated_at
timestamp", "the portfolio lacked detail on domain Y", "search_services
returned stale results for Z") are FORBIDDEN in this document. Such findings
are a meta-concern about the harness/MSP tooling, not a deliverable for the
customer. Record them in 06-retro/retro.md §5 (Data-Quality Meta-Findings)
and emit a change request if warranted.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Handover Report: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `handover@1.0.0`
> **Phase:** 05-handover
> **Entry condition:** `04-roadmap/roadmap.md` frontmatter `status: ratified`

---

## Executive Narrative

<!--
Customer-facing, jargon-light summary of:
  - What the engagement set out to do (2–3 sentences)
  - Key findings from the situation and gap phases (bullet list grounded in
    ratified claims; every bullet should be traceable to a GAP-NNN or SIT-NNN)
  - Recommended direction and why (refer to sequencing argument from roadmap)
  - What success looks like at the end of Y3

Tone: written for a non-technical executive audience.
Do NOT mention MSP tooling, harness internals, or claim confidence levels here.
Do NOT include meta-findings about portal data quality (see exit criteria).
-->

<[inferred] summary of engagement purpose and direction>
[inferred] [source:from: <scope-goal-ids>] [conf:M]

### Key Findings

| Finding | Supporting evidence | Gap addressed |
|---------|---------------------|---------------|
| | | |

### Recommended Direction

<written narrative; 1–3 paragraphs referencing the sequencing argument>

---

## Roadmap Summary

<!--
Reproduce the ratified roadmap items in a customer-readable table.
Reference 04-roadmap/roadmap.md for the authoritative source.
Group by year (Y1 / Y2 / Y3). Flag quick wins with ✓.
Compliance items should note their role (constraint / deadline / enabler).
-->

| Year | RMI-id | Initiative | Owner | Compliance role | Quick win |
|------|--------|-----------|-------|-----------------|-----------|
| Y1 | | | | | |
| Y1 | | | | | |
| Y2 | | | | | |
| Y3 | | | | | |

---

## Decision Log

<!--
Reproduce all entries from _decisions.md.
Every entry must include the overrides: claim pointer if one was recorded
(machine-readable hook for claim_composition_resolvable.py).
Do not paraphrase DEC-NNN ids — copy them verbatim.
-->

| DEC-id | Decision | Rationale | Overrides | Date |
|--------|----------|-----------|-----------|------|
| | | | | |

---

## Assumption Register

<!--
Reproduce all active entries from _assumptions.md.
Flag any entries with requires_revalidation: true and note the phase at
which revalidation is due.
Stale or invalidated assumptions should be marked as such.
-->

| ASM-id | Assumption | Confidence | Requires revalidation | Invalidates if wrong |
|--------|-----------|------------|-----------------------|----------------------|
| | | | | |

---

## Risk Log

<!--
Reproduce all open entries from _risks.md.
Include status (open | mitigated | accepted | closed) and mitigation summary.
Closed risks may be omitted if the count of closed risks is noted in a
footnote.
-->

| RSK-id | Risk | Likelihood | Impact | Status | Mitigation |
|--------|------|-----------|--------|--------|-----------|
| | | | | | |

---

## Contradictions Surfaced This Phase

<!--
Mirror of _contradictions.md rows relevant to this phase.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 05-handover.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
