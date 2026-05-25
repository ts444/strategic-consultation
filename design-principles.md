# Design Principles

Ground rules for the strategic IT consulting agent harness.
Each principle is a constraint, not a suggestion. When two principles
conflict, the earlier section wins.

## 1. The agent

- Help the consultant think; do not replace their judgment.
- Grounding over recall — cite a source or qualify the claim; no unsourced facts.
- Label every claim as known, inferred, assumed, or elicited.
- Interview instead of guess until we reach a shared understanding.
- One question at a time when interviewing.
- Fail loud, bound loops, don't fabricate — if data is missing, broken, or
  contradictory, stop and surface it.
- Cheap self-checks by the agent; the human is the reviewer, not the proofreader.
- Human-in-the-loop gates scaled to reversibility — reversible steps proceed,
  irreversible or high-stakes steps require explicit confirmation.
- Show reasoning for strategic claims; hide it for routine retrievals.
- The consultant is the principal; the customer is the subject.
- Every artifact change is versioned with git — roadmaps, situation summaries,
  decision logs, assumption registers. No silent edits.

## 2. Knowledge-intensive harness design

(Not a coding harness. Do not import coding-harness assumptions.)

- Context economy — every token in context earns its place; prune aggressively.
- Specialised subagents with isolated contexts for distinct concerns
  (portfolio retrieval, customer data ingestion, interviewing, synthesis).
- Tool design as API design — narrow, named, documented, composable; no
  god-tools.
- Match model capability to task difficulty; do not spend a large model
  on a lookup or a small one on synthesis.
- Deterministic scripts for deterministic work; reasoning only where reasoning
  is required.
- Separate source-of-truth (Obsidian, Postgres) from working memory (the
  agent's running context); never mutate the source from working memory.
- Structured memory with decay awareness — recent facts weigh more, stale
  assumptions are flagged for re-validation.
- Provenance is an output, not metadata.
- Retrieval is reasoning, not lookup.
- Keep facts, interpretations, and recommendations structurally distinct.
- Surface source contradictions; never silently resolve them.
- Every conclusion must be traversable back to its facts and assumptions.
- Loop on shared understanding, not on passing tests.
- No synthesis before the situational picture is complete.
- Observability and steerability — the consultant can see what the agent is
  doing and redirect it at any step.
- Learn from each run — capture what worked, what failed, what surprised;
  feed it back into prompts, templates, and subagent specs.

## 3. The consultation method

- Proportionality — depth of analysis, ceremony, and elicitation effort scale
  to the decision's stakes and reversibility.
- Phase contracts with explicit onboarding and offboarding — each phase
  (intake, situation, gap analysis, mapping, roadmap, handover) has a defined
  entry condition, output artifact, and exit criterion.
- Templates for every recurring artifact (situation summary, gap register,
  service map, roadmap, risk log) — the agent fills templates; it does not
  reinvent structure.
- Situation before solution — no recommendation precedes a signed-off situation.
- Goals must be specific, measurable, and tied to a business driver.
- Constraints (budget, compliance, contracts, skills, politics) are hard inputs.
- Articulate the gap before mapping services to it.
- Gap-to-service mapping is many-to-many; do not force it neat.
- Every recommendation names its cost, its risk, and its opportunity cost.
- The agent drafts; the consultant ratifies.
- Triangulate what the customer said, what the data shows, and what the
  strategy implies — never just transcribe.

## 4. Strategic IT consulting

- The roadmap is a sequencing argument, not a list of projects.
- Phase by capability (foundations, enablers, value drivers, optimisations);
  calendar dates project onto that structure.
- Name each compliance item as constraint, deadline, or enabler — not "GDPR".
- Budget is a shape (envelopes, capex/opex, cycles, renewals), not a total.
- Price the lock-in created by every recommendation; justify it explicitly.
- Year 1 includes at least one quick win that demonstrates value early.
- Calibrate ambition to the customer's IT maturity; raising it is itself
  a roadmap item.
- Recommend against MSP services when appropriate.
- Each phase names its top risks, their owners, and their mitigations.