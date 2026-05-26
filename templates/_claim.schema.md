# Claim Atom and Composed-Block Schema

> **Canonical reference.** All templates, validator rules, and subagent prompts
> reference *this file* as the single source of truth for claim structure. Any
> conflict between this schema and a template or prompt: this file wins.
>
> Schema version: 1.0.0 — bound to harness 0.1.0.

---

## 1. The Claim Atom

Every substantive assertion in any phase artifact must be a **claim atom** or
embedded inside a composed block (§2). A claim atom is a single sentence or
structured field annotated with three mandatory inline tags.

### 1.1 Mandatory Tags

```
[label] [source:<uri>] [conf:H|M|L]
```

All three tags are required. An assertion without all three is not a valid
claim and will be rejected by the validator.

**Inline example:**

```markdown
The customer's firewall rule-set has not been reviewed in 18 months.
[known] [source:customer-portal://assets/fw-01@2026-04-10T09:00:00Z] [conf:H]
```

---

### 1.2 Label Vocabulary and Producer Binding

| Label | Meaning | Permitted producers |
|---|---|---|
| `[known]` | Fact retrieved from a read-only source-of-truth | `portfolio-retriever`, `customer-data-retriever` |
| `[elicited]` | Soft fact captured in a live interview session | `interviewer` |
| `[inferred]` | Conclusion derived by reasoning from other claims | `synthesizer` |
| `[assumed]` | Premise treated as true in the absence of evidence | `synthesizer` |

**Producer binding is enforceable.** The validator checks the `produced_by`
frontmatter field (or trace metadata) against this table. A `[known]` claim
in a synthesizer-produced block is a violation.

---

### 1.3 Source URI Shapes

| Context | Shape | Example |
|---|---|---|
| MSP portfolio Obsidian file | `portfolio://<domain>/<file>.md@<git-sha>` | `portfolio://Security/managed-soc.md@a3f8c21` |
| Customer-portal resource | `customer-portal://<resource>/<id>@<updated_at>` | `customer-portal://assets/server-12@2026-03-01T14:22:00Z` |
| Live interview capture | `interview:<YYYY-MM-DD>/consultant` | `interview:2026-05-25/consultant` |
| Composed from other claims | `from: <claim-id-A> + <claim-id-B>` | `from: GAP-003 + REC-007` |

Rules:
- `portfolio://` URIs must carry a git sha. The portfolio MCP `head()` tool
  returns the current sha; mtime is a fallback when the portfolio is not a git
  repo.
- `customer-portal://` URIs must carry an ISO-8601 `updated_at` timestamp.
- `from:` compositions must reference claim ids that are defined in the current
  artifact or in a prior ratified artifact accessible in the same engagement repo.
- Unresolvable URIs cause validator rejection (FR-9).

---

### 1.4 Confidence Levels

| Level | Meaning |
|---|---|
| `H` | High — primary source, freshly verified, no contradicting evidence |
| `M` | Medium — secondary source, some uncertainty, or source slightly stale |
| `L` | Low — weak evidence, indirect inference, or significant uncertainty |

**Confidence-propagation rule (FR-8):**

> The confidence of a composed claim is at most `min(confidence of all input
> claims)`.

```
conf(composed) ≤ min(conf(A), conf(B), …)
```

Phantom precision — assigning `H` to a claim derived from one or more `M` or
`L` inputs — is a validator error.

---

## 2. Composed Blocks

A **composed block** is a named, multi-field structure made up of claim atoms
plus block-level required fields. The block itself counts as one composed claim
and must carry top-level `[label]`, `[source]`, `[conf]` tags summarising its
overall provenance and confidence (subject to the propagation rule).

Blocks are rendered as YAML-fenced sections inside Markdown artifacts.

---

### 2.1 Gap Block

A gap is a shortfall between the customer's current state and a desired or
required state. Every gap declared in `gaps.md` must conform to this schema.

**Required fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | `GAP-NNN` | Sequential, unique within engagement |
| `title` | string | Plain language; no bare framework names in this field |
| `current_state` | claim | `[known]` or `[elicited]`, with source |
| `desired_state` | claim | `[elicited]` or `[inferred]`, with source |
| `gap_description` | claim | `[inferred]` or `[assumed]` |
| `compliance_drivers` | list of `CMP-NNN` | Required field; empty list `[]` is valid; broken CMP-ids are not |
| `severity` | `critical \| high \| medium \| low` | |
| `evidence` | list of claim ids | Supporting claims from situation phase |

**Confidence-propagation:** `conf(gap_description)` ≤ `min(conf(current_state), conf(desired_state))`.

**Worked example:**

```yaml
---
id: GAP-004
title: No privileged-access management for domain admin accounts
current_state: >
  Domain administrator accounts share a single password rotated annually.
  [known] [source:customer-portal://assets/ad-config@2026-04-15T11:00:00Z] [conf:H]
desired_state: >
  Domain administrator access uses just-in-time provisioning with MFA and
  session recording per CMP-002 (ISO27001 A.9.2.3 baseline).
  [elicited] [source:interview:2026-05-25/consultant] [conf:M]
gap_description: >
  No PAM tooling or JIT process exists; current controls fall below the
  ISO27001 A.9.2.3 baseline declared in CMP-002.
  [inferred] [source:from: GAP-004.current_state + GAP-004.desired_state] [conf:M]
compliance_drivers:
  - CMP-002
severity: high
evidence:
  - SIT-012
  - SIT-014
---
```

---

### 2.2 Recommendation Block

A recommendation maps one or more gaps to a proposed service or action.
Every recommendation in `recommendations.md` must conform to this schema.

**Required fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | `REC-NNN` | Sequential |
| `title` | string | No bare framework names |
| `addresses` | list of `GAP-NNN` | At least one |
| `proposed_service` | string or `[no-known-service]` | Portfolio service name; `[no-known-service]` when no MSP service fits (see §2.2.1) |
| `rationale` | claim | `[inferred]`, from the gap + portfolio retrieval |
| `compliance_relation` | `addresses \| partially-addresses \| irrelevant` | Required; never absent |
| `cost` | structured cost estimate | capex/opex per period; `tbc` is allowed, absence is not |
| `lock_in` | string | Explicit lock-in assessment; `none` is valid, absence is not |
| `opportunity_cost` | string | What the customer foregoes by choosing this; `none` is valid |

**Worked example:**

```yaml
---
id: REC-007
title: Deploy CyberArk Privilege Cloud for domain admin JIT access
addresses:
  - GAP-004
proposed_service: CyberArk Privilege Cloud (managed)
rationale: >
  CyberArk Privilege Cloud provides JIT provisioning with MFA and session
  recording, closing GAP-004 fully. The MSP portfolio's managed-PAM service
  wraps this at SME tier.
  [inferred] [source:from: GAP-004 + portfolio://Security/managed-pam.md@d9e2a31] [conf:M]
compliance_relation: addresses
cost:
  capex: 0
  opex_monthly: 1400
  notes: "Licence + managed service; pricing valid 2026-Q2"
lock_in: >
  CyberArk-specific vault format; migration to competitor requires credential
  re-enrollment. Medium lock-in.
opportunity_cost: >
  Budget consumed here is unavailable for endpoint-detection tooling (REC-011).
  Prioritising PAM first is defensible under NIS2 deadline CMP-002 but creates
  a 6-month window where EDR remains weak.
---
```

#### 2.2.1 No-known-service placeholder

When portfolio retrieval finds no MSP service that fits a gap, the recommendation
block must still be recorded, with `proposed_service: "[no-known-service]"` and a
`rationale` explaining why no service applies. This prevents silent gap omission
and surfaces the portfolio gap for the retro.

---

### 2.3 Risk Block

A risk is a potential adverse outcome. Risks live in `_risks.md` and may be
referenced from phase artifacts.

**Required fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | `RSK-NNN` | Sequential |
| `title` | string | |
| `description` | claim | `[inferred]` or `[assumed]` |
| `likelihood` | `low \| medium \| high` | |
| `impact` | `low \| medium \| high` | |
| `owner` | string | Named person or role |
| `mitigation` | string | At least a direction; may be `pending` |
| `triggered_by` | list of claim ids | What generates this risk |

**Confidence-propagation:** `conf(description)` ≤ `min(conf of triggered_by claims)`.

**Worked example:**

```yaml
---
id: RSK-003
title: Credential compromise during PAM migration window
description: >
  Between REC-007 go-live planning and actual CyberArk deployment there is a
  period (estimated 6–10 weeks) where domain admin accounts remain under the
  current weak controls. A targeted attack in this window could achieve full
  domain compromise.
  [inferred] [source:from: GAP-004 + REC-007] [conf:M]
likelihood: medium
impact: high
owner: Customer CISO (placeholder)
mitigation: >
  Accelerate deployment timeline; add temporary break-glass monitoring via
  SIEM during migration window. See REC-011.
triggered_by:
  - GAP-004
  - REC-007
---
```

---

### 2.4 Roadmap-Item Block

A roadmap item is a unit of planned work placed in a calendar window.
Every item in `roadmap.md` must conform to this schema.

**Required fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | `RMI-NNN` | Sequential |
| `title` | string | |
| `year` | `Y1 \| Y2 \| Y3` | |
| `quick_win` | boolean | Required; `true` on ≥1 Y1 item (FR-26) |
| `capability_phase` | `foundations \| enablers \| value-drivers \| optimisations` | |
| `addresses` | list of `REC-NNN` | At least one |
| `compliance_role` | `constraint \| deadline \| enabler \| none` | Required; never absent |
| `compliance_deadline` | ISO-8601 date | Required iff `compliance_role: deadline`; absent otherwise |
| `budget_envelope` | `BUD-NNN` | Must reference a declared entry in `_budget.md`; required |
| `depends_on` | list of `RMI-NNN` | May be empty |
| `owner` | string | |
| `risks` | list of `RSK-NNN` | May be empty |

**Confidence-propagation:** The roadmap item is a composed claim. Its effective
confidence is `min(conf of all addressed recommendations)`.

**Worked example:**

```yaml
---
id: RMI-005
title: Deploy managed PAM (CyberArk Privilege Cloud)
year: Y1
quick_win: false
capability_phase: foundations
addresses:
  - REC-007
compliance_role: deadline
compliance_deadline: "2026-12-31"
budget_envelope: BUD-002
depends_on:
  - RMI-001
owner: Customer CISO
risks:
  - RSK-003
---
```

---

## 3. Quick Reference

| Block | Mandatory structural field(s) beyond claim atom |
|---|---|
| Gap | `compliance_drivers` (list, may be empty) |
| Recommendation | `compliance_relation`, `cost`, `lock_in`, `opportunity_cost` |
| Risk | `likelihood`, `impact`, `owner`, `mitigation` |
| Roadmap-item | `compliance_role`, `compliance_deadline` (iff deadline), `budget_envelope` |

---

## 4. Validator Coverage

Rules in `validator/rules/` that enforce this schema:

| Rule file | Enforces |
|---|---|
| `claim_label_present.py` | Every substantive bullet has a `[label]` |
| `claim_source_present.py` | Every claim has a `[source:…]` |
| `claim_confidence_present.py` | Every claim has `[conf:H\|M\|L]` |
| `label_producer_binding.py` | Label matches the subagent that produced the block |
| `confidence_propagation.py` | Composed claim conf ≤ min(input confs) |
| `gap_compliance_drivers_field.py` | Gap has `compliance_drivers`; broken CMP-ids rejected |
| `recommendation_required_fields.py` | All four recommendation structural fields present |
| `roadmap_item_required_fields.py` | All roadmap structural fields present; budget_envelope resolves |
| `claim_composition_resolvable.py` | `from: A + B` ids exist in scope |
| `framework_name_in_structured_fields.py` | No bare framework names in titles or structured fields |
