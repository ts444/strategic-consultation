---
phase: "06-retro"
status: draft
harness_version: "0.1.0"
template: "retro@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. '## What Worked' H2 section exists with at least one entry.
  2. '## What Failed' H2 section exists (may be empty — but section must exist).
  3. '## What Surprised' H2 section exists (may be empty — but section must exist).
  4. '## Data-Quality Meta-Findings' H2 section exists and records:
       - Contradiction count for the engagement (total raised, by type)
       - Resolution-path (c) count (assumptions logged to resolve contradictions)
       - Any MSP portal hygiene findings (stale sources, missing domains,
         search quality issues) — these belong HERE and not in handover.md
  5. '## Change Requests' H2 section exists. Every change request listed
     here has been written as a file in:
       <harness-repo>/backlog/change-requests/CR-YYYY-NNN.md
     Each file must name the originating customer/engagement directly
     (no anonymisation). The section must include the file path for each CR.
  6. Validator reports zero violations.
  7. Consultant has reviewed and ratified via HITL gate 3.
  8. Frontmatter `status` changed to `ratified`; `ratified_by` and
     `ratified_at` filled before committing.

CHANGE-REQUEST DESTINATION: Change requests emitted by this phase are written
into the HARNESS REPO at:
  backlog/change-requests/CR-YYYY-NNN.md
NOT in the engagement repo. The orchestrator must write those files and commit
them in the harness repo as a separate commit from the engagement ratification.

DATA-QUALITY META-FINDINGS: This is the designated home for observations about
MSP portfolio data quality, customer-portal freshness, and harness tooling
issues encountered during the engagement. These must NOT appear in handover.md.

Claim atom rules: every substantive assertion in this document must carry
[label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Engagement Retro: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `retro@1.0.0`
> **Phase:** 06-retro
> **Entry condition:** `05-handover/handover.md` frontmatter `status: ratified`
> **Engagement dates:** {{ENGAGEMENT_START}} — {{ENGAGEMENT_END}}

---

## What Worked

<!--
What went well during this engagement? Focus on:
  - Harness phases / tooling that performed as designed
  - Subagent interactions that produced high-quality outputs
  - Claims that were well-supported and held up under validation
  - HITL gates that caught real issues before they propagated

Each bullet should be specific enough to produce an actionable change request
or positive confirmation. Vague entries ("everything was fine") are not useful.
-->

- 

---

## What Failed

<!--
What broke, stalled, or produced poor outputs? Focus on:
  - Validator rules that fired incorrectly (false positives)
  - Validator rules that missed real violations (false negatives)
  - Subagent prompts that produced off-schema outputs requiring reruns
  - Phase entry/exit conditions that were unclear or incomplete
  - Orchestrator loops that stalled or exceeded retry budgets
  - Any claim that was later found to be unsupported

Each failure should map to a specific change request (§5) if the fix is
actionable in the harness.
-->

- 

---

## What Surprised

<!--
Observations that were unexpected but not clearly a success or failure:
  - Customer context that differed significantly from what was assumed
  - Portfolio gaps that weren't anticipated (drives [no-known-service] rate)
  - Compliance requirements that added unforeseen complexity
  - Claim confidence levels that were unexpectedly low or high

These drive future prompt or template calibration, even if no immediate fix
is required.
-->

- 

---

## Data-Quality Meta-Findings

<!--
DESIGNATED SECTION for MSP tooling and data-quality observations.
These findings inform harness change requests but are NOT customer-facing.

Required subsections:
  §4.1 Contradiction statistics (mandatory)
  §4.2 MSP portfolio observations (include if any issues encountered)
  §4.3 Customer-portal observations (include if any issues encountered)
-->

### §4.1 Contradiction Statistics

| Metric | Count |
|--------|-------|
| Contradictions raised (total) | |
| Resolved via path (a) — source update | |
| Resolved via path (b) — supersedes marker | |
| Resolved via path (c) — assumption logged | |
| Resolved via path (d) — decision logged | |
| Unresolved at engagement close | |

### §4.2 MSP Portfolio Observations

<!--
Observations about portfolio data quality encountered during portfolio-retriever
invocations. Examples:
  - Services with no updated_at / stale content
  - Domains with insufficient coverage for the customer's needs
  - search_services quality issues (false positives / misses)
  - head() returning mtime fallbacks (portfolio not a git repo)
Include portfolio:// URIs for any specific problem sources.
-->

- 

### §4.3 Customer-Portal Observations

<!--
Observations about customer-portal API data quality. Examples:
  - Resources missing updated_at fields
  - Endpoints returning incomplete or stale data
  - Compliance posture data that was absent or unstructured
Include customer-portal:// URIs for any specific problem sources.
-->

- 

---

## Change Requests

<!--
Every change request raised in this retro must be written as a file in the
harness repo at:
  backlog/change-requests/CR-YYYY-NNN.md

Format for this section: one sub-section per change request, with the file
path so the orchestrator knows exactly where to write it.

CHANGE REQUEST RULES:
  - File naming: CR-YYYY-NNN.md (e.g., CR-2026-001.md)
  - The file must name this engagement's customer directly (no anonymisation)
  - Each file must include frontmatter with:
      status: open
      origin_phase: <phase where the issue was observed>
      originating_customer: <customer name>
      proposed_change_target: <template | validator | prompt | tool | schema>
  - Files are committed in the HARNESS REPO, not the engagement repo

DESTINATION: <harness-repo>/backlog/change-requests/

List each CR below with its path and a one-line summary.
-->

| CR file | Target | Summary |
|---------|--------|---------|
| `backlog/change-requests/CR-YYYY-001.md` | | |

### CR-YYYY-001: {{ONE_LINE_TITLE}}

> File: `backlog/change-requests/CR-YYYY-001.md`
> Target: `template | validator | prompt | tool | schema`
> Origin phase: `<phase where the issue was observed>`

<Description of the change request. What problem was observed, what change is
proposed, and what the expected improvement would be.>

---

## HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
