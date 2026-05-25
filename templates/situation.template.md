---
phase: "01-situation"
status: draft
harness_version: "0.1.0"
template: "situation@1.0.0"
ratified_by: ""
ratified_at: ""
produced_by: "synthesizer"
---

<!--
EXIT CRITERIA (from design-principles §3, Q7 phase contracts)

This artifact is ratified when ALL of the following are true:
  1. Every engagement goal declared in scope.md has at least one situation-phase
     claim providing current-state evidence.
  2. Portfolio and customer-data retrievers have been invoked; portfolio://
     and customer-portal:// URIs appear in _sources.jsonl.
  3. At least the elicitation threshold of [elicited] claims has been captured
     by the interviewer subagent.
  4. Validator reports zero violations (claim atoms, labels, sources, confidence,
     producer bindings all conformant).
  5. Zero entries in _contradictions.md with Status: unresolved AND
     Blocks: 01-situation.
  6. No synthesis occurred before the situational picture was complete
     (design-principles §2: "No synthesis before the situational picture is complete").
  7. Consultant has ratified via HITL gate 3.
  8. Frontmatter `status` is changed to `ratified` and `ratified_by` /
     `ratified_at` are filled before committing.

Claim atom rules: every substantive assertion must carry [label] [source:<uri>] [conf:H|M|L].
See templates/_claim.schema.md for the full schema. This file wins over any conflict.
-->

# Situation Summary: {{CUSTOMER_NAME}}

> **Harness version:** `{{HARNESS_VERSION}}`
> **Template:** `situation@1.0.0`
> **Phase:** 01-situation
> **Entry condition:** `00-intake/scope.md` frontmatter `status: ratified`

---

## 1. Current Technology Landscape

<!--
Synthesiser-produced section. All claims must be [inferred] or [assumed],
sourced via `from: <claim-id-A> + <claim-id-B>` referencing [known] and [elicited]
inputs. Retrievers' [known] blocks and interviewer's [elicited] blocks are inputs
to this synthesis; they are NOT reproduced verbatim here but referenced by id.
-->

### 1.1 Infrastructure and Hosting

### 1.2 Network and Connectivity

### 1.3 Security Controls

### 1.4 Identity and Access Management

### 1.5 End-User Computing

### 1.6 Applications and Data

---

## 2. Organisational Context

<!--
Captures people, process, and governance findings from the interviewer.
[elicited] and [inferred] claims only; [known] retrieval outputs referenced by id.
-->

### 2.1 IT Team Structure and Capability

### 2.2 IT Governance and Decision-Making

### 2.3 Vendor and Partner Landscape

### 2.4 IT Maturity Assessment

<!--
Self-assessed or inferred IT maturity level (design-principles §4:
"Calibrate ambition to the customer's IT maturity").
[inferred] [source:from: <sit-claim-ids>] [conf:H|M|L]
-->

---

## 3. Key Facts (Retrieved Evidence)

<!--
Flat list of [known] claim blocks produced by portfolio-retriever and
customer-data-retriever. Each entry has SIT-NNN id for referencing.
Format inline per _claim.schema.md §1.
-->

| SIT-id | Claim summary | Label | Source | Conf |
|--------|---------------|-------|--------|------|
| SIT-001 | | [known] | | |

---

## 4. Key Elicitations (Interviewer Output)

<!--
Flat list of [elicited] claim blocks produced by the interviewer subagent.
Each entry has SIT-NNN id continuing from §3 above.
-->

| SIT-id | Claim summary | Label | Source | Conf |
|--------|---------------|-------|--------|------|
| | | [elicited] | interview:<date>/consultant | |

---

## 5. Situation Synthesis

<!--
Synthesiser triangulates retrieved facts (§3), elicitations (§4), and
strategic implications (design-principles §3: "Triangulate what the customer
said, what the data shows, and what the strategy implies").
All claims here are [inferred] or [assumed] with from: composition sources.
-->

### 5.1 Strengths

### 5.2 Weaknesses / Problem Areas

### 5.3 Strategic Implications for the Roadmap

---

## 6. Compliance Posture

<!--
Map each CMP-NNN item declared in scope.md to current-state evidence.
Validator enforces CMP-id references; _compliance.md is authoritative.
-->

| CMP-id | Framework item | Current posture | Evidence (SIT-ids) | Conf |
|--------|---------------|-----------------|---------------------|------|
| | | | | |

---

## 7. Contradictions Surfaced This Phase

<!--
Mirror of relevant rows from _contradictions.md. Do not edit here;
edit _contradictions.md directly. This section is for human readability.
Synthesis is blocked while any row shows Status: unresolved AND Blocks: 01-situation.
-->

| CON-id | Description | Status | Resolution path |
|--------|-------------|--------|-----------------|
| | | | |

---

## 8. Risks Identified This Phase

<!--
Risks surfaced during situation phase. Each is entered in _risks.md as RSK-NNN
and referenced here. Do not duplicate the full block; reference by id and title.
-->

| RSK-id | Title | Likelihood | Impact | Owner |
|--------|-------|------------|--------|-------|
| | | | | |

---

## 9. HITL Confirmation Record

| Gate | Timestamp | Consultant confirmation |
|------|-----------|------------------------|
| Gate 1 — entry confirm | | |
| Gate 3 — ratification | | |
