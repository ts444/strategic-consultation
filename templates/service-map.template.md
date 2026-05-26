---
phase: "03-mapping"
status: draft
harness_version: "0.1.0"
template: "service-map@1.0.0"
ratified_by: ""
ratified_at: ""
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

NO-KNOWN-SERVICE RULE: When portfolio retrieval finds no MSP service that
fits a gap, record a mapping entry with proposed_service: "[no-known-service]"
and a rationale. Never leave a gap unmapped. This surfaces portfolio gaps for
the retro phase and honours design-principles §4.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Service Map (Exhaustive): {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `service-map@1.0.0`
> **Phase:** 03-mapping
> **Entry condition:** `02-gap/gaps.md` frontmatter `status: ratified`

---

## 1. Mapping Summary

| GAP-id | Gap title | Candidate services (count) | [no-known-service]? |
|--------|-----------|---------------------------|---------------------|
| GAP-001 | | | |
| GAP-002 | | | |
| GAP-003 | | | |

---

## 2. Mapping Entries

<!--
One YAML-fenced block per (gap × candidate service) pair. Every gap from
gaps.md must appear at least once. Use [no-known-service] when no portfolio
service fits. The portfolio-retriever subagent populates proposed_service
and portfolio_uri; the synthesizer populates fit_rationale.

TEMPLATE USAGE:
  Copy the block below for each mapping. Assign sequential MAP-NNN ids.
  Do not leave placeholder gaps in committed artifacts.
-->

```yaml
---
id: MAP-001
gap: GAP-001
proposed_service: "<Portfolio service name from portfolio MCP>"
portfolio_uri: "portfolio://<domain>/<file>.md@<git-sha>"
fit_rationale: >
  <[inferred] claim explaining why this service addresses the gap.>
  [inferred] [source:from: GAP-001 + portfolio://<domain>/<file>.md@<git-sha>] [conf:M]
curated: true
notes: ""
---
```

<!-- Example of a [no-known-service] entry — use when no MSP service fits the gap: -->

```yaml
---
id: MAP-002
gap: GAP-002
proposed_service: "[no-known-service]"
portfolio_uri: ""
fit_rationale: >
  Portfolio retrieval found no managed service covering <describe gap area>.
  Nearest candidates (<service A>, <service B>) do not address <specific shortfall>.
  This gap is flagged for the retro change-request backlog.
  [inferred] [source:from: GAP-002 + portfolio://<domain>/<file>.md@<git-sha>] [conf:M]
curated: false
notes: "Portfolio gap — surface in 06-retro change request."
---
```

---

## 3. Portfolio Domains Searched

<!--
List the portfolio domains queried by the portfolio-retriever during this phase.
Each domain searched must have a head() timestamp to support decay checking.
-->

| Domain | Services reviewed | Head timestamp |
|--------|------------------|----------------|
| | | |

---

## 4. Contradictions Surfaced This Phase

<!--
Mirror of _contradictions.md rows relevant to this phase.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 03-mapping.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## 5. Open Assumptions Resolution

<!--
List every assumption in _assumptions.md with requires_revalidation:true and
target_phase:03-mapping. For each, the synthesizer must either mark it resolved
or explicitly defer it with a written justification. Ratification is blocked until
every entry in this table has a non-empty resolution_status.

Required fields: resolution_status (resolved | deferred), resolved_in_phase, resolution_note.
-->

| ASM-id | Statement summary | resolution_status | resolution_note |
|--------|-------------------|-------------------|-----------------|
| | | | |

---

## 6. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
