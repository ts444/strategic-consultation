# PRD: Strategic IT Consulting Agent Harness

## 1. Introduction / Overview

This PRD specifies a knowledge-intensive (not coding) agent harness that conducts strategic IT consulting for customers of a Managed Service Provider (MSP) and produces a 3-year roadmap mapping customer goals onto the MSP's service portfolio.

The harness operates as a sequence of phase-bounded Claude Code invocations driven by a human consultant (the principal). Each phase reads ratified artifacts from prior phases, retrieves from read-only sources (Obsidian portfolio + customer-portal HTTP API), elicits soft facts from the consultant via a long-lived interviewer subagent, synthesises typed claims into the phase's output artifact, validates it deterministically, and surfaces it for ratification. Every artifact is git-versioned; every claim carries label, source, and confidence; every conclusion is traversable to its facts and assumptions.

The architecture is fully specified in the kickoff grilling session decisions Q1–Q11 (see `~/.claude/projects/-home-tim-strategic-consultation/memory/decisions_kickoff.md`) and bound by `design-principles.md`. This PRD turns those decisions into a buildable backlog.

## 2. Goals

- Build the harness repo structure (templates, prompts, validator, MCP servers, CLI glue, retro backlog) inside `/home/tim/strategic-consultation`.
- Make every artifact, claim, and decision in an engagement git-versioned, typed, and traceable end-to-end (claim → facts → assumptions).
- Enforce design principles structurally (not aspirationally) via validator rules and read-only source boundaries.
- Run a complete tracer-bullet engagement (a real customer-shaped repo, all seven phases, ratified handover) using the v0.1.0 harness.
- Establish the structural learning loop: retro phase produces typed change requests that flow into the harness backlog and version into the next release.

## 3. User Stories

Stories are ordered to deliver a tracer-bullet (end-to-end thin slice) first, then deepen. Each is sized for one focused implementation session.

### US-001: Harness repo skeleton + versioning
**Description:** As a developer, I want the harness repo directory structure in place so all subsequent work has a canonical home.

**Acceptance Criteria:**
- [ ] Directories created: `templates/`, `prompts/orchestrator/`, `prompts/subagents/`, `validator/rules/`, `mcp/portfolio-mcp/`, `mcp/customer-mcp/`, `harness/`, `backlog/change-requests/`.
- [ ] `CHANGELOG.md` initialised at `0.1.0`.
- [ ] `design-principles.md` confirmed at repo root as canonical (existing file).
- [ ] `README.md` describes the structure in one screen.
- [ ] Git initialised (if not already), `0.1.0` tag created on first commit.

### US-002: Claim atom schema + worked example
**Description:** As a developer, I want a single schema doc that defines the atomic claim and the composed blocks (gap, recommendation, risk, roadmap item) so every template and validator rule references one source of truth.

**Acceptance Criteria:**
- [ ] `templates/_claim.schema.md` defines: claim atom (mandatory `[label]` `[source]` `[conf:H|M|L]`), four labels (known | inferred | elicited | assumed), source URI shapes (`portfolio://...`, `customer-portal://...`, `interview:<date>/consultant`, `from: A + B`), composed-block schemas with mandatory fields (gap → `compliance_drivers`; recommendation → `compliance_relation` + `cost` + `lock_in` + `opportunity_cost`; roadmap item → `compliance_role` + optional `compliance_deadline` + `budget_envelope`).
- [ ] Worked example for every block type included inline.
- [ ] Schema explicitly states label-producer binding (which subagent emits which label).
- [ ] Schema explicitly states confidence-propagation rule (composed claim conf ≤ min(input confs)).

### US-003: Register schemas for root cross-cutting registers
**Description:** As a developer, I want schemas for the six root registers so engagement repos have a uniform shape.

**Acceptance Criteria:**
- [ ] `templates/_registers/` contains one schema doc per register: `_assumptions.md`, `_decisions.md`, `_risks.md`, `_contradictions.md`, `_compliance.md`, `_budget.md`.
- [ ] Each schema defines the entry shape, required fields, and lifecycle (e.g., `_contradictions.md` entries carry `Status: unresolved | resolved-by-{a|b|c|d}-...` and `Blocks: <phase>`).
- [ ] `_compliance.md` schema enforces `role: constraint | deadline | enabler` and `id: CMP-NNN`.
- [ ] `_budget.md` schema enforces envelope-shape (capex/opex × period, renewals, hard limits, soft preferences), never a total.

### US-004: Phase artifact templates (all seven phases)
**Description:** As a developer, I want one template per phase artifact so the synthesizer fills templates rather than reinventing structure.

**Acceptance Criteria:**
- [ ] `templates/` contains `scope.template.md`, `situation.template.md`, `gaps.template.md`, `service-map.template.md`, `recommendations.template.md`, `roadmap.template.md`, `handover.template.md`, `retro.template.md`.
- [ ] Each template has YAML frontmatter: `phase`, `status: draft|ratified`, `harness_version`, `template_version`, `ratified_by`, `ratified_at`, `template: <name>@<version>`.
- [ ] Each template embeds the exit criteria for that phase as a comment block.
- [ ] `roadmap.template.md` mandates a "Sequencing argument" section (per §4 "the roadmap is a sequencing argument, not a list of projects").
- [ ] `roadmap.template.md` mandates ≥1 Y1 quick-win marker.
- [ ] `handover.template.md` explicitly excludes meta-findings about portal hygiene.
- [ ] `retro.template.md` includes a "Change requests" section with template-id references.

### US-005: Engagement repo scaffold script (`harness init`)
**Description:** As a consultant, I want a single command to create a new engagement repo with the correct layout and version pin.

**Acceptance Criteria:**
- [ ] `harness/init.py` (or equivalent) accepts `<customer-name>` and an optional target dir.
- [ ] Creates phase directories `00-intake/ ... 06-retro/`.
- [ ] Creates empty root registers from schemas.
- [ ] Creates engagement `CLAUDE.md` stub with placeholders for: customer name, compliance frameworks, budget envelope, stakeholders, `harness_version` pinned to current `CHANGELOG.md` version.
- [ ] Initialises git and commits the scaffold.
- [ ] Refuses to overwrite an existing non-empty directory.

### US-006: Validator core CLI + structural rules
**Description:** As a developer, I want a deterministic validator that rejects malformed artifacts so structural enforcement is not a vibe.

**Acceptance Criteria:**
- [ ] `validator/cli.py validate <artifact-path>` exits non-zero with specific error messages on violation.
- [ ] Rules implemented as separate files in `validator/rules/`:
  - `claim_label_present.py` (every substantive bullet has a `[label]`)
  - `claim_source_present.py` (every claim has a `[source]`)
  - `claim_confidence_present.py` (every claim has `[conf:H|M|L]`)
  - `label_producer_binding.py` (e.g., `[known]` only from retriever-produced blocks)
  - `confidence_propagation.py` (composed claim ≤ min(input confs))
  - `frontmatter_required_fields.py` (phase, status, template, harness_version)
  - `template_conformance.py` (artifact has the H2 sections its template requires)
- [ ] Each rule has a unit test with at least one passing and one failing fixture.

### US-007: Validator compliance + budget + composition rules
**Description:** As a developer, I want validator rules that enforce the compliance/budget structural fields and the claim composition graph so §3/§4 are enforced, not asked.

**Acceptance Criteria:**
- [ ] Rules added:
  - `gap_compliance_drivers_field.py` (gaps have `compliance_drivers:` field, list may be empty, broken `CMP-id` rejected)
  - `recommendation_required_fields.py` (`compliance_relation`, `cost`, `lock_in`, `opportunity_cost` — `lock_in: none` is valid; absence is not)
  - `roadmap_item_required_fields.py` (`compliance_role`; `compliance_deadline` iff role=deadline; `budget_envelope` matches a `_budget.md` entry)
  - `framework_name_in_structured_fields.py` (bare framework names in titles/structured fields rejected; narrative prose tolerated)
  - `claim_composition_resolvable.py` (`from: A + B` requires A and B to be valid claim ids in scope)
- [ ] Each rule has unit tests.
- [ ] Validator output groups errors by rule for skimmability.

### US-008: Portfolio MCP server (read-only, service-shaped)
**Description:** As a developer, I want a read-only MCP server wrapping `~/msp-portfolio` so the agent has narrow named tools instead of grep.

**Acceptance Criteria:**
- [ ] `mcp/portfolio-mcp/` implements: `list_domains()`, `list_services_in_domain(domain)`, `read_service(name)`, `search_services(query)`, `head(name)` (returns git sha or mtime for freshness checks).
- [ ] No write tools. Source filesystem mounted read-only at the server boundary.
- [ ] Every response embeds the source URI (`portfolio://<domain>/<file>.md@<sha-or-mtime>`).
- [ ] `search_services` returns at most N hits with citation; never returns raw greps.
- [ ] Smoke test: starts and answers `list_domains()` against the live `~/msp-portfolio`.

### US-009: Customer-portal read-only HTTP API
**Description:** As a developer, I want the existing customer-portal to expose a read-only HTTP API so customer data has a single authoritative shape.

**Acceptance Criteria:**
- [ ] New route group in `~/customer-portal/app/api/` exposes endpoints aligned to Prisma entities (e.g., `/api/customers/:id/assets`, `/api/customers/:id/contracts`, `/api/customers/:id/compliance-posture`).
- [ ] API uses a read-only Postgres role (separate DB user with `SELECT` only).
- [ ] All responses include an `updated_at` for freshness.
- [ ] Auth: a single shared bearer token configured via env var (single-consultant assumption).
- [ ] Smoke test: a curl against each endpoint returns expected shape on seeded data.

### US-010: Customer-data MCP server (wraps the HTTP API)
**Description:** As a developer, I want a thin MCP server wrapping the customer-portal HTTP API so the agent's tool surface is uniform.

**Acceptance Criteria:**
- [ ] `mcp/customer-mcp/` exposes narrow typed tools matching the API endpoints: `list_assets(customer_id)`, `list_contracts(customer_id)`, `compliance_posture(customer_id)`, etc.
- [ ] Every response embeds `customer-portal://<resource>/<id>@<updated_at>`.
- [ ] No write tools.
- [ ] Smoke test: lists assets for a seeded customer.

### US-011: `decay_check` deterministic tool
**Description:** As a consultant, I want a single command to surface stale claims at phase entry so revalidation is structured.

**Acceptance Criteria:**
- [ ] `harness/decay_check.py <engagement-repo>` reads all root registers and prior ratified artifacts.
- [ ] Implements three policies: `[known]` source-mutation check (re-resolves URIs against MCPs); `[elicited]` phase-distance × confidence (H=3, M=2, L=1, configurable); `[inferred]`/`[assumed]` input-change cascade + `requires_revalidation` flag.
- [ ] Output grouped: HARD STALE, ELICITED DUE FOR REVALIDATION, ASSUMPTIONS FLAGGED, DOWNSTREAM IMPACT.
- [ ] For unchanged hard claims, freshness-bumps timestamp and logs to `_trace.jsonl` (silent no-op per Q10c).
- [ ] Tests: synthetic engagement repo with seeded stale claims of each type.

### US-012: `harness explain <claim-id>` traversal tool
**Description:** As a consultant, I want to walk any claim back to its facts and assumptions so traceability is operational.

**Acceptance Criteria:**
- [ ] `harness/explain.py <engagement-repo> <claim-id>` walks the claim graph via `from: A + B` composition.
- [ ] Output is a tree: claim → inputs → ... → leaf facts (`[known]`, `[elicited]`) with sources and timestamps.
- [ ] Surfaces decisions in `_decisions.md` that override any claim in the chain.
- [ ] Tests: seeded artifact set, known traversal expected output.

### US-013: Phase orchestrator prompt (00 intake)
**Description:** As a developer, I want the intake phase orchestrator prompt so the first phase can be driven end-to-end.

**Acceptance Criteria:**
- [ ] `prompts/orchestrator/00-intake.md` encodes: read engagement `CLAUDE.md`; announce plan; invoke interviewer; produce `scope.md`; run validator; surface for ratification.
- [ ] Lists allowed subagents for this phase (interviewer only; no retrievers in intake).
- [ ] Specifies the three HITL gates (entry confirm, elicitation continuous, ratification).
- [ ] References template by version pin.

### US-014: Subagent prompts (retrievers, interviewer, synthesizer)
**Description:** As a developer, I want system prompts for the four specialist subagents so the orchestrator can delegate.

**Acceptance Criteria:**
- [ ] `prompts/subagents/portfolio-retriever.md`: only portfolio MCP, stamps `[known]`, stateless, returns cited markdown.
- [ ] `prompts/subagents/customer-data-retriever.md`: only customer MCP, stamps `[known]`, stateless, returns cited markdown.
- [ ] `prompts/subagents/interviewer.md`: no tools, stamps `[elicited]`, long-lived intra-phase, periodic in-scope self-check, soft-bounded turn count with threshold warnings.
- [ ] `prompts/subagents/synthesizer.md`: no tools, stamps `[inferred]` or `[assumed]`, forbidden from emitting `[known]`, enforces confidence-propagation rule in its output.
- [ ] Each prompt names its model (Sonnet or Opus per Q4; never Haiku) and forbids tool access outside its scope.

### US-015: Phase orchestrator prompts (01 situation through 06 retro)
**Description:** As a developer, I want orchestrator prompts for the remaining six phases so every phase can be driven.

**Acceptance Criteria:**
- [ ] One file per phase under `prompts/orchestrator/`: `01-situation.md`, `02-gap.md`, `03-mapping.md`, `04-roadmap.md`, `05-handover.md`, `06-retro.md`.
- [ ] Each names its entry condition, the subagents it may invoke, the produced artifact(s) (mapping produces two: `service-map.md` + `recommendations.md`), and exit criteria.
- [ ] Retro orchestrator emits change-request files into `<harness-repo>/backlog/change-requests/` with anonymised engagement reference.
- [ ] Each prompt encodes the seven-step orchestrator loop and bounded-retry policy from Q9.

### US-016: `harness enter_phase` CLI entry point
**Description:** As a consultant, I want a single command that figures out the current phase from repo state and invokes Claude Code with the right context.

**Acceptance Criteria:**
- [ ] `harness/enter_phase.py [--phase NN] [--rerun]` run from inside an engagement repo.
- [ ] Default: determines next phase from which `0N-*/` directories have ratified artifacts.
- [ ] Verifies `harness_version` in engagement `CLAUDE.md` matches current; on mismatch, surfaces choice (pin / upgrade / abort) per Q11.
- [ ] Invokes Claude Code with the appropriate orchestrator prompt and the right CWD.
- [ ] Logs invocation metadata to `0N-<name>/_trace.jsonl`.

### US-017: Contradiction-handling tool + blocking semantics
**Description:** As a consultant, I want contradictions to block synthesis and present the four resolution paths.

**Acceptance Criteria:**
- [ ] `harness/check_contradictions.py <engagement-repo>` detects three collision types (hard↔hard, hard↔soft, soft↔soft) by subject+predicate matching.
- [ ] New contradictions written as structured blocks in `_contradictions.md` with `Status: unresolved` and `Blocks: <phase>`.
- [ ] Orchestrator prompts call this tool before invoking synthesizer (Q9 step 4); non-empty unresolved-blocking list halts the phase.
- [ ] Resolution paths recorded explicitly: (a) source-update placeholder, (b) re-elicit supersession marker, (c) explicit assumption added to `_assumptions.md`, (d) `_decisions.md` entry with `overrides: <claim-id>` pointer.
- [ ] Tests: seeded contradicting claim pair, verifies block + halt.

### US-018: Trace + observability logging
**Description:** As a consultant, I want to watch what the agent is doing in real time and audit afterwards.

**Acceptance Criteria:**
- [ ] Every subagent invocation logs to `0N-<name>/_trace.jsonl`: timestamp, subagent, model, prompt hash, input hash, output hash, duration.
- [ ] Every retriever call appends source URIs to `0N-<name>/_sources.jsonl`.
- [ ] Consultant can `tail -f` either file during a phase.
- [ ] Validator surfaces missing trace entries as a soft warning (not blocking) on phase ratification.

### US-019: Tracer-bullet engagement (end-to-end dry run)
**Description:** As the harness author, I want to run a complete fake engagement through all seven phases so the design is proven end-to-end before claiming v1.0.

**Acceptance Criteria:**
- [ ] Synthetic customer "Acme Test Corp" engagement repo created via `harness init`.
- [ ] All seven phases run, each producing a ratified artifact validator-green.
- [ ] At least one contradiction triggered and resolved via path (d).
- [ ] At least one stale claim caught by `decay_check`.
- [ ] At least one `[no-known-service]` placeholder emitted in mapping (proving §4 "recommend against MSP services").
- [ ] Retro phase produces ≥1 change-request file in `backlog/change-requests/`.
- [ ] `harness explain` walks a roadmap-item claim back to its facts.

### US-020: First retro feedback applied → v0.2.0
**Description:** As the harness author, I want to ship one structural improvement based on the tracer-bullet's retro so the learning loop is proven, not just designed.

**Acceptance Criteria:**
- [ ] At least one change request from US-019's retro is implemented.
- [ ] `CHANGELOG.md` bumped to `0.2.0` with explicit reference to the originating change-request id.
- [ ] Git tag `0.2.0` created.
- [ ] The change request's status in `backlog/change-requests/` is updated to `shipped` with the version.

## 4. Functional Requirements

- **FR-1:** The harness operates as phase-bounded Claude Code invocations; never as a single continuous session across phases.
- **FR-2:** Engagement state lives in one git repo per engagement; the harness never mutates source-of-truth systems (Obsidian portfolio, customer-portal Postgres).
- **FR-3:** Source-of-truth access is exclusively via read-only MCP servers (portfolio MCP wrapping Obsidian; customer MCP wrapping a read-only HTTP API exposed by customer-portal).
- **FR-4:** Within a phase invocation, the top-level orchestrator delegates to four specialist subagents with isolated contexts (portfolio-retriever, customer-data-retriever, interviewer, synthesizer) plus a deterministic validator script.
- **FR-5:** No task is routed to a Haiku model. Model floor is Sonnet; Opus is used for interviewer and synthesizer.
- **FR-6:** Every claim in every artifact carries mandatory `[label]` `[source]` `[conf:H|M|L]` fields. Validator rejects artifacts where any claim lacks any of the three.
- **FR-7:** Claim labels are producer-bound: retrievers stamp `[known]`, interviewer stamps `[elicited]`, synthesizer stamps `[inferred]` or `[assumed]`. The validator enforces this binding.
- **FR-8:** Composed claims (`from: A + B`) carry confidence ≤ `min(input confidences)`. Validator enforces phantom-precision check.
- **FR-9:** The validator resolves every source URI against the MCPs as part of structural validation. Unresolvable URIs cause rejection.
- **FR-10:** Hard-vs-soft contradictions trigger warn + ask: consultant decides authoritatively via one of four resolution paths (fix source, re-elicit, explicit assumption, decision-with-override). Synthesis is blocked while unresolved blocking contradictions exist.
- **FR-11:** Each engagement repo has six root registers: `_assumptions.md`, `_decisions.md`, `_risks.md`, `_contradictions.md`, `_compliance.md`, `_budget.md`.
- **FR-12:** Compliance items are typed (`role: constraint | deadline | enabler`) and referenced by id (`CMP-NNN`). Bare framework names like "GDPR" or "NIS2" are rejected by the validator in structured fields (titles, names, IDs); tolerated in narrative prose.
- **FR-13:** Budget is declared as envelope-shapes (capex/opex per period, renewals, hard limits, soft preferences), not totals. Roadmap items reference budget envelopes; validator rejects references to undeclared envelopes.
- **FR-14:** Every gap carries `compliance_drivers`; every recommendation carries `compliance_relation`, `cost`, `lock_in`, `opportunity_cost`; every roadmap item carries `compliance_role`, `compliance_deadline` (iff `role=deadline`), and `budget_envelope`. Validator rejects artifacts missing these fields.
- **FR-15:** The orchestrator loop per phase: bootstrap → retrieval pass → elicitation pass (if required) → contradiction check → synthesis → validator → consultant review. Three intra-phase HITL gates: entry confirm, elicitation continuous, ratification.
- **FR-16:** Loop bounds: retrieval retry 1, synthesizer-on-validator retry 2, human-driven loops (revisions, contradiction resolution, interviewer turns) unbounded (interviewer soft-bounded with threshold warnings).
- **FR-17:** `decay_check` runs at phase entry. `[known]` claims decay on source mutation (auto re-retrieve when changed; silent freshness-bump when unchanged, logged to `_trace.jsonl`). `[elicited]` claims decay by phase distance × confidence. `[inferred]`/`[assumed]` claims decay on input change and explicit `requires_revalidation` flag.
- **FR-18:** No cross-engagement memory. Learning flows structurally via retro change requests into the harness repo backlog, never via stored facts.
- **FR-19:** Engagement `CLAUDE.md` pins `harness_version` at intake. Version mismatches on later invocation surface a choice (pin to original / upgrade / abort) — never silent.
- **FR-20:** Templates are referenced by version (`template: <name>@<version>`), not copied into engagement repos.
- **FR-21:** Retro change requests are structured with origin phase, originating customer/engagement reference, proposed change target, evidence link, and status. No anonymisation applied.
- **FR-22:** `harness explain <claim-id>` walks any claim back to its leaf facts and assumptions, surfacing any decisions in `_decisions.md` that override claims in the chain.
- **FR-23:** Every subagent invocation, retriever call, and validator run is logged to per-phase `_trace.jsonl` / `_sources.jsonl`.
- **FR-24:** The seven phases are: 00 intake → 01 situation → 02 gap → 03 mapping → 04 roadmap → 05 handover → 06 retro. Phase 03 produces two artifacts: `service-map.md` (exhaustive) and `recommendations.md` (curated).
- **FR-25:** Phase 05 handover excludes meta-findings about MSP portal hygiene; those flow into phase 06 retro.
- **FR-26:** Phase 04 roadmap exit requires: every Y1 item traceable to ≥1 gap; ≥1 quick-win Y1 item present; every compliance item categorised as constraint/deadline/enabler.

## 5. Non-Goals (Out of Scope)

- **No multi-consultant or multi-tenant operation.** Single-consultant assumption; single bearer token for customer-portal API. Revisit later.
- **No customer-facing agent interaction.** The consultant is the principal; the agent never interviews the customer directly. The customer is the subject.
- **No agent-driven mutation of any source-of-truth.** The agent will never edit Obsidian portfolio files or customer-portal data. Out-of-band consultant edits are the only path.
- **No cross-engagement memory of customer specifics.** No "this customer is similar to that customer" inference inside the harness.
- **No browser/UI for the harness.** It runs in Claude Code (terminal). Customer-portal already has a UI for separate purposes; harness does not add one.
- **No automatic ramp/upgrade of `harness_version`.** Mismatches are explicit consultant decisions.
- **No skip-phase mode.** Every engagement runs every phase; depth within a phase scales with stakes (proportionality lives in content, not in skipping).
- **No customer-approval workflow.** Customer ratification happens after handover, outside the harness.
- **No live "watch the conversation" UI for the consultant during interviewer turns** beyond `tail -f _trace.jsonl`.
- **No backwards-compatibility hacks** for templates or claim schemas — engagements pin a version and stay on it; new versions are clean breaks.

## 6. Design Considerations

- **Markdown + YAML frontmatter** is the artifact format throughout — diff-reviewable, Obsidian-native, validator-friendly. JSON would be hostile to the consultant; pure prose would lose §2's structural distinction between facts/interpretations/recommendations.
- **Confidence is three-bucket (H/M/L)**, not numeric. Honest about resolution: the agent does not have calibrated probabilities.
- **Inline citations**: `[label] [source] [conf:X]` after every claim. Provenance is an output, not metadata (§2).
- **Templates as referenced (versioned) artifacts**, not copied — reproducibility depends on it.
- **`design-principles.md` is the binding spec.** Any conflict between this PRD and that doc: the doc wins, flag the conflict.

## 7. Technical Considerations

- **MCP server runtime** unspecified; pick whatever is fastest to build and well-supported by the Claude Code MCP client. Python is the likely default.
- **Validator language**: Python is the natural choice given the rest of the toolchain. Pure functions, one rule per file, unit-tested.
- **Customer-portal HTTP API** must use a separate read-only Postgres role to enforce the read-only boundary structurally (not via convention).
- **Source URIs must carry a freshness handle**: git sha for the Obsidian portfolio (`portfolio://...@<sha>`), `updated_at` for customer-portal (`customer-portal://...@<timestamp>`). The MCP `head()` verb returns this without fetching the body.
- **Trace files** (`_trace.jsonl`, `_sources.jsonl`) are append-only; never rewritten.
- **No automated tests are required for the *content* of templates and prompts** — those iterate via retros. Tests are required for validator rules, decay logic, contradiction detection, and the `explain` traversal.

## 8. Success Metrics

- **Tracer-bullet completes**: synthetic engagement runs all seven phases, every artifact validator-green, end-to-end (US-019).
- **Learning loop closes once**: at least one retro change request is implemented and shipped in v0.2.0 (US-020).
- **Structural enforcement holds**: zero artifacts in the tracer-bullet engagement have an unlabelled claim, a missing source URI, a missing confidence, or a missing compliance/budget field — all proven by validator-green status.
- **Traceability is total**: every claim in the tracer-bullet's `roadmap.md` is reachable by `harness explain` back to a `[known]` or `[elicited]` leaf.
- **Source-mutation decay works silently when nothing changed**: re-running phase 02 on an engagement where sources are untouched produces a clean `decay_check` output with HARD STALE = 0.
- **At least one `[no-known-service]` placeholder emerges in the tracer-bullet's mapping**: proves the harness can recommend against the MSP's portfolio (§4).

## 9. Open Questions

All open questions from the kickoff have been resolved:

- **MCP runtime/language: Python.** All MCP servers, validator, decay/explain tools, and CLI are Python.
- **Tracer-bullet customer data:** the customer-portal Postgres already has three seeded customers (small/medium/large). The tracer-bullet uses one of these directly — no new seed needed.
- **`harness_version` semantics:** strict semver (`0.1.0` → `0.2.0` → ...).
- **Phase-distance decay defaults** (H=3, M=2, L=1) shipped as-is; tune via retro after the first real engagement.
- **Interviewer threshold-warning levels** shipped with conservative defaults; tune via retro.
- **Anonymisation of retro change requests: not required.** Originating customer is named in the change request directly. No customer-name → id mapping needed.
