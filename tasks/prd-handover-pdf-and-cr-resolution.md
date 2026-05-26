# PRD: Handover PDF Deliverable + Open CR Resolution

## Introduction

The current phase 05 handover produces `handover.md` — a well-structured markdown document oriented toward the consulting team. This PRD upgrades the deliverable to a visually polished PDF (`handover.pdf`) suitable for customer stakeholders, rendered automatically at the end of phase 05 via pandoc + weasyprint. In parallel, all four open change requests (CR-2026-003 through CR-2026-006) are resolved: two new MSP portfolio services are added, `[no-known-service]` gaps get a formal build/buy/partner decision gate, the intake budget validation is hardened, and assumption revalidation is generalised across all phases.

## Goals

- Phase 05 produces `handover.pdf` alongside `handover.md` with no manual post-processing
- PDF contains cover page, styled roadmap table (Y1/Y2/Y3 colour-coded), four embedded charts, and all existing handover sections
- RSK blocks gain `likelihood` and `impact` fields enabling the risk heat map chart
- MSP portfolio gains an Incident Response service and a full Compliance domain (5 services)
- `[no-known-service]` mapping gaps trigger a documented build/buy/partner HITL decision before phase ratifies
- Budget envelope mismatches are caught at intake with a hard gate, not discovered at roadmap phase
- All phase HITL gates enforce resolution of open `requires_revalidation` assumptions before ratification
- All four open CRs are marked `status: shipped`

## User Stories

### US-036: Add weasyprint dependency and preflight check
**Description:** As a developer, I need weasyprint installed as a project dependency so the PDF render step works out of the box.

**Acceptance Criteria:**
- [ ] `weasyprint` added to `[project].dependencies` in `pyproject.toml`
- [ ] `pip install -e .` installs weasyprint successfully
- [ ] `python3 -c "import weasyprint"` exits 0 after install
- [ ] Existing tests (`pytest`) still pass
- [ ] `ruff` and `mypy` pass

---

### US-037: Extend RSK schema with likelihood and impact fields
**Description:** As a consultant, I want risk blocks to record likelihood and impact so the handover PDF can render a risk heat map.

**Acceptance Criteria:**
- [ ] RSK block schema (defined in the relevant orchestrator prompt and/or schema doc) gains two new required fields: `likelihood: low | medium | high` and `impact: low | medium | high`
- [ ] Validator (`validator/`) updated to enforce these fields on all RSK blocks; any RSK block missing either field produces a validation error
- [ ] `Meridian-Logistics/_risks.md` backfilled: RSK-001 through RSK-005 each assigned plausible `likelihood` and `impact` values consistent with their descriptions
- [ ] Validator runs green on the updated Meridian-Logistics engagement
- [ ] `pytest`, `ruff`, `mypy` pass

---

### US-038: Python chart generator (four charts from engagement registers)
**Description:** As the harness, I need a deterministic Python module that reads an engagement's markdown registers and produces four chart PNG files for embedding in the PDF.

**Charts required:**
1. **Spend stacked bar** — Y1/Y2/Y3 columns, stacked capex/opex segments; data sourced from RMI blocks in `04-roadmap/roadmap.md` (capex/opex fields) grouped by year
2. **Gantt swim-lane** — One row per RMI item, grouped by phase (foundations / enablers / value-drivers / optimisations), shaded by year bucket (Y1/Y2/Y3); data from `04-roadmap/roadmap.md`
3. **Risk status donut** — Segments: open / mitigated / accepted / closed; data from `_risks.md` RSK blocks
4. **Gap coverage bar** — Horizontal bar per GAP block; each bar coloured by mapping outcome (fully mapped / partially mapped / no-known-service); data joined from `02-gap/gaps.md` GAP blocks and `03-mapping/service-map.md` MAP blocks

**Acceptance Criteria:**
- [ ] Module lives at `harness/charts.py`; callable as `generate_charts(engagement_path: Path) -> dict[str, Path]` returning a map of chart name → PNG path written to `<engagement_path>/05-handover/charts/`
- [ ] All four charts are generated for the Meridian-Logistics engagement without error
- [ ] Chart PNGs are non-empty (file size > 0) and visually correct when opened (manual check)
- [ ] Module handles missing registers gracefully: if a source file is absent, that chart is skipped and a warning is logged; the other charts still render
- [ ] `pytest` includes at least one test per chart that verifies the PNG is produced and non-empty given the Meridian-Logistics fixtures
- [ ] `ruff`, `mypy` pass

---

### US-039: HTML/CSS template and MSP logo placeholder
**Description:** As the harness, I need an HTML/CSS template that pandoc uses to produce a visually polished PDF with a cover page, MSP branding, and styled content sections.

**Acceptance Criteria:**
- [ ] Template file at `assets/handover-template.html` — a pandoc HTML5 template with embedded CSS
- [ ] MSP logo placeholder at `assets/msp-logo.png` — a simple professional placeholder (or a 1×1 transparent PNG with a comment indicating where to replace it)
- [ ] CSS provides: Inter or system-sans font stack; cover page block with MSP logo, customer name (from frontmatter), engagement date, and title; colour-coded roadmap table (Y1 = one accent colour, Y2 = second, Y3 = third); quick-win badge styling; section headings with colour accent; chart images sized to fit page width
- [ ] Running `pandoc --template assets/handover-template.html` on `Meridian-Logistics/05-handover/handover.md` produces an HTML file with all styled sections present
- [ ] `ruff`, `mypy` pass (no Python changes required; story is template/asset only)

---

### US-040: PDF render post-step in phase 05 harness
**Description:** As a consultant, I want phase 05 to automatically produce `handover.pdf` after the markdown is ratified, so I have a ready-to-send customer deliverable without any manual steps.

**Acceptance Criteria:**
- [ ] `harness/enter_phase.py` (or equivalent phase runner) gains a post-ratification hook for phase `05-handover` that:
  1. Calls `generate_charts(engagement_path)` (from US-038)
  2. Runs `pandoc <handover.md> --template assets/handover-template.html -o <handover.html>` with chart image paths injected
  3. Runs `weasyprint <handover.html> <handover.pdf>`
  4. Logs the output path of the produced PDF
- [ ] `05-handover/handover.pdf` is present in the Meridian-Logistics engagement after the hook runs
- [ ] If weasyprint or pandoc is not installed, the hook raises a clear `RuntimeError` with installation instructions rather than a silent failure
- [ ] PDF is non-empty (file size > 1 KB)
- [ ] `pytest`, `ruff`, `mypy` pass

---

### US-041: Add Incident Response service to MSP portfolio
**Description:** As the mapping phase, I need an Incident Response service in the portfolio so that DFIR-related gaps (like Meridian-Logistics GAP-002) map to a real service instead of `[no-known-service]`.

**Acceptance Criteria:**
- [ ] New file at `~/msp-portfolio/Security/Incident_Response.md` following the established service file format (YAML frontmatter with name, domain, tags, pricing tiers, SLA tiers; markdown body with Overview, What's Included, What's Not Included, Dependencies sections)
- [ ] Service covers: 24/7 on-call IR retainer, initial triage and containment, forensic evidence preservation, post-incident report, coordination with law enforcement if required
- [ ] Tags include: `incident-response`, `dfir`, `forensics`, `retainer`, `containment`
- [ ] Portfolio MCP `search_services("incident response")` returns this service
- [ ] Portfolio MCP `search_services("DFIR")` returns this service
- [ ] `~/msp-portfolio/` is a git repository — commit the new file with message `feat: add Incident Response service`
- [ ] `backlog/change-requests/CR-2026-003.md` status updated to `shipped`
- [ ] Existing portfolio MCP tests pass; `ruff`, `mypy` pass

---

### US-042: Add Compliance domain and five compliance services to MSP portfolio
**Description:** As the mapping phase, I need a Compliance service domain so that regulatory and framework-related gaps map to real services instead of `[no-known-service]`.

**Services to create (all in domain `Compliance`):**
1. `NIS2_Entity_Classification.md` — scoping whether the customer is Essential or Important entity; regulatory deadline tracking
2. `TISAX_Readiness.md` — TISAX label scoping, gap assessment, readiness roadmap for automotive suppliers
3. `ISMS_Programme.md` — ISO 27001 / ISMS establishment: scope definition, risk treatment, control implementation, certification readiness
4. `GDPR_Gap_Assessment.md` — data mapping, lawful basis review, DPIA support, breach notification readiness
5. `Regulatory_Deadline_Tracking.md` — ongoing monitoring of applicable regulatory deadlines with proactive advisory alerts

**Acceptance Criteria:**
- [ ] `~/msp-portfolio/Compliance/` directory created with all five `.md` service files in the established format
- [ ] Each file has appropriate tags enabling keyword search (e.g., `nis2`, `tisax`, `iso27001`, `gdpr`, `compliance`)
- [ ] Portfolio MCP `search_services("NIS2")` returns `NIS2_Entity_Classification`
- [ ] Portfolio MCP `search_services("TISAX")` returns `TISAX_Readiness`
- [ ] Portfolio MCP `search_services("ISO 27001")` returns `ISMS_Programme`
- [ ] Portfolio MCP `list_services_in_domain("Compliance")` returns all five services
- [ ] All five files committed to `~/msp-portfolio/` with message `feat: add Compliance domain with 5 services`
- [ ] `backlog/change-requests/CR-2026-004.md` status updated to `shipped`
- [ ] Existing portfolio MCP tests pass; `ruff`, `mypy` pass

---

### US-043: Build/buy/partner HITL decision gate for [no-known-service] gaps
**Description:** As a consultant, I want to be forced to make a documented build/buy/partner decision for any gap that maps to `[no-known-service]`, so the roadmap always has a resolution path and the decision is recorded as a DEC-NNN entry.

**Acceptance Criteria:**
- [ ] `prompts/orchestrator/03-mapping.md` updated: when the synthesizer produces a MAP entry with `[no-known-service]`, it must also emit a `DECISION_REQUIRED` block listing the gap ID, the gap description, and the three options (build in-house / buy third-party product / partner with specialist firm)
- [ ] HITL Gate 1 checklist in `03-mapping.md` gains item: "All `[no-known-service]` MAP entries have a corresponding DEC-NNN decision in `_decisions.md` selecting build / buy / partner, with a rationale"
- [ ] Phase 03 may not ratify until all `[no-known-service]` entries have a resolution decision recorded
- [ ] The synthesizer prompt instructs that the roadmap must include a sourcing/procurement RMI item for each `[no-known-service]` gap whose decision is `buy` or `partner`
- [ ] `ruff`, `mypy`, `pytest` pass

---

### US-044: Budget validation hard gate at intake (CR-2026-005)
**Description:** As a consultant, I want intake to flag and require explicit sign-off when the customer's stated budget envelope is likely undersized for their stated goals, so budget gaps are surfaced and documented before scope is fixed.

**Acceptance Criteria:**
- [ ] `prompts/orchestrator/00-intake.md` updated with a budget-complexity estimate step: after goals and scope are captured, the synthesizer produces a rough order-of-magnitude cost range based on goal count, complexity indicators (number of compliance frameworks, number of infrastructure domains, greenfield vs. brownfield), and typical MSP engagement costs
- [ ] If the estimated range exceeds the stated envelope by more than 25%, the synthesizer emits a `BUDGET_GAP_WARNING` block with: stated envelope, estimated range, gap percentage, and a prompt for the consultant to either (a) revise the envelope, (b) reduce scope, or (c) proceed with a documented risk acceptance
- [ ] HITL Gate in `00-intake.md` gains mandatory checklist item: "If a BUDGET_GAP_WARNING was raised, a DEC-NNN decision recording the consultant's resolution choice is present in `_decisions.md`"
- [ ] Phase 00 may not ratify `scope.md` until the budget gate is cleared (no warning raised, or warning raised and DEC-NNN recorded)
- [ ] `backlog/change-requests/CR-2026-005.md` status updated to `shipped`
- [ ] `ruff`, `mypy`, `pytest` pass

---

### US-045: Generalise assumption revalidation gate to all phases (CR-2026-006)
**Description:** As a consultant, I want every phase HITL gate to enforce that all assumptions flagged `requires_revalidation: true` targeting that phase are formally resolved before ratification, so `_assumptions.md` is always accurate at engagement close.

**Acceptance Criteria:**
- [ ] `templates/assumption.template.md` (or the assumptions schema doc) gains an optional `resolved_in_phase` field and a `resolution_status: pending | resolved | deferred` field with a `resolution_note` free-text field
- [ ] Each of the six orchestrator prompts (`00-intake` through `05-handover`) has its HITL gate checklist updated to include: "All assumptions in `_assumptions.md` with `requires_revalidation: true` and a `target_phase` matching this phase have `resolution_status: resolved` or `resolution_status: deferred` (with `resolution_note` explaining why deferral is acceptable)"
- [ ] `03-mapping.md` specifically updated per the CR-2026-006 proposal (HITL Gate 1 and service-map template "Open Assumptions Resolution" section)
- [ ] `Meridian-Logistics/_assumptions.md` backfilled: ASM-002 given `resolution_status: deferred`, `resolved_in_phase: 03-mapping`, and `resolution_note` explaining the deferral (MSP delivery capacity not formally validated but accepted given engagement scope)
- [ ] Validator updated to check that any assumption with `requires_revalidation: true` and a `target_phase` set has a non-empty `resolution_status` field (either at the target phase or explicitly deferred)
- [ ] `backlog/change-requests/CR-2026-006.md` status updated to `shipped`
- [ ] `ruff`, `mypy`, `pytest` pass

---

## Functional Requirements

- FR-1: `weasyprint` is a declared project dependency in `pyproject.toml`
- FR-2: RSK blocks require `likelihood: low | medium | high` and `impact: low | medium | high`; validator enforces this
- FR-3: `harness/charts.py::generate_charts(engagement_path)` produces four chart PNGs in `<engagement>/05-handover/charts/`
- FR-4: `assets/handover-template.html` is a pandoc HTML5 template with cover page, colour-coded roadmap table, and chart image embedding
- FR-5: Phase 05 post-ratification hook renders `handover.pdf` via pandoc → weasyprint; fails loudly if toolchain missing
- FR-6: `~/msp-portfolio/Security/Incident_Response.md` exists and is searchable by keyword
- FR-7: `~/msp-portfolio/Compliance/` exists with five service files; `list_services_in_domain("Compliance")` returns all five
- FR-8: Phase 03 HITL gate blocks ratification if any `[no-known-service]` gap lacks a DEC-NNN build/buy/partner decision
- FR-9: Phase 00 HITL gate blocks ratification if a `BUDGET_GAP_WARNING` was raised and no DEC-NNN resolution is recorded
- FR-10: All phase HITL gates (00–05) enforce `requires_revalidation` assumption resolution before ratification
- FR-11: `_assumptions.md` schema gains `resolution_status`, `resolved_in_phase`, and `resolution_note` fields
- FR-12: All four open CRs (`CR-2026-003` through `CR-2026-006`) have `status: shipped` after relevant stories complete

## Non-Goals

- Likelihood × impact scoring is ordinal (low/medium/high) only; no numeric probability values in this iteration
- Customer logo injection at intake (deferred — requires intake template changes beyond CR-2026-005 scope)
- Automated chart generation for phases other than 05-handover
- Interactive or web-based PDF (static print PDF only)
- NIS2 entity classification as a standalone workflow separate from the Compliance service portfolio
- Regenerating the full Meridian-Logistics engagement end-to-end (backfill only where needed for schema compliance)

## Technical Considerations

- Portfolio MCP reads from `~/msp-portfolio/` — new service files go there, not inside the harness repo
- `~/msp-portfolio/` must be a git repo; commit new services there separately from harness commits
- Pandoc version on this system is 2.9.2.1 — use `pandoc --template` with HTML5 output, not newer features
- Chart generation uses `matplotlib`; add to `pyproject.toml` if not already present
- The engagement path passed to `generate_charts` is the root of an engagement directory (e.g., `Meridian-Logistics/`); all register paths are relative to it
- RSK block backfill for Meridian-Logistics: RSK-001 (NIS2 deadline miss) → likelihood: high, impact: high; RSK-002 (patch gap exploitation) → likelihood: medium, impact: high; RSK-003 (WAN capacity crisis) → likelihood: medium, impact: medium; RSK-004 (budget overrun) → likelihood: high, impact: medium; RSK-005 (TISAX timeline) → likelihood: medium, impact: high

## Success Metrics

- `python -c "from harness.charts import generate_charts; generate_charts(Path('Meridian-Logistics'))"` completes without error and produces four non-empty PNGs
- Phase 05 post-step produces `Meridian-Logistics/05-handover/handover.pdf` > 1 KB
- `pytest` passes across all modules (validator, harness, portfolio MCP)
- All four open CRs show `status: shipped`
- `ruff` and `mypy --strict` pass across the harness package

## Open Questions

- None. All design decisions resolved in the grill-me session (2026-05-26).
