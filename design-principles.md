# Design Principles

Ground rules for the strategic IT consulting agent harness.
Each principle is a constraint, not a suggestion. When two principles conflict, the earlier section wins.

## 1. Built-In harness (BU) principles for the agent itself

- BU-1	Interview instead of guess until we reach a shared understanding.
- BU-2	One question at a time when interviewing.
- BU-3	Triangulate what the human said and what the data shows; never just transcribe.
- BU-4	Fail loud, bound loops, don't fabricate; if data is missing, broken, or contradictory, stop and surface it.
- BU-5	Human-in-the-loop gates scaled to reversibility; reversible steps proceed, irreversible or high-stakes steps require explicit confirmation.
- BU-6	Observability and steerability; the human can see what the agent is doing and redirect it at any step.
- BU-7	Every artifact change is versioned with git; no silent edits.
- BU-8	Tool design as API design; narrow, named, documented, composable; no god-tools.
- BU-9	Deterministic scripts for deterministic work; reasoning only where reasoning is required.

## 2. Knowledge intense (KN) principles to emphasize that this is not a coding harness

- KN-1.1	Context economy; every token in context earns its place; prune aggressively.
- KN-1.2	Specialised subagents with isolated contexts for distinct concerns.
- KN-1.3	Match model capability to task difficulty.
- KN-2.1	Separate source-of-truth from working memory; never mutate the source from working memory.
- KN-2.2	Structured memory with decay awareness.
- KN-2.3	Retrieval is reasoning, not lookup.
- KN-2.4	Surface source contradictions; never silently resolve them.
- KN-3.1	Grounding over recall; cite a source or qualify the claim; no unsourced facts.
- KN-3.2	Provenance is an output, not metadata.
- KN-3.3	Label every claim as known, inferred, assumed, or elicited.
- KN-3.4	Every conclusion must be traversable back to its facts and assumptions.
- KN-4.1	Loop on shared understanding, not on passing tests.
- KN-4.2	Cheap self-checks by the agent; the human is the reviewer, not the proofreader.
- KN-5.1	Phase contracts with explicit onboarding and offboarding; each phase has a defined entry condition, output artifact, and exit criterion.
- KN-5.2	Templates for every recurring artifact; the agent fills templates; it does not reinvent structure.
- KN-5.3	The agent drafts; the human ratifies.
- KN-5.4	Help the human think; do not replace their judgment.
- KN-6.1	Learn from each run; capture what worked, what failed, what surprised; feed it back into prompts, templates, and subagent specs.

## 3. Domain specific (DO) principles for consultations

- DO-1	The consultant is the principal; the customer is the subject.
- DO-2	Help the consultant think; do not replace their judgment.
- DO-3	Situation before solution; no recommendation precedes a signed-off situation.
- DO-4	Keep facts, interpretations, and recommendations structurally distinct.
- DO-5	Proportionality; depth of analysis, ceremony, and elicitation effort scale to the decision's stakes and reversibility.
- DO-6	Price the lock-in created by every recommendation; justify it explicitly.

## 4. Use-Case specific (US) principles for a strategic IT consultation

- US-1	Constraints (budget, compliance, contracts, skills, politics) are hard inputs.
- US-2	Goals must be specific, measurable, and tied to a business driver.
- US-3	Every recommendation names its cost, its risk, and its opportunity cost.
- US-4	Articulate the gap before mapping services to it.
- US-5	Gap-to-service mapping is many-to-many; do not force it neat.
- US-6	No synthesis before the situational picture is complete.
- US-7	Show reasoning for strategic claims; hide it for routine retrievals.
- US-8	The roadmap is a sequencing argument, not a list of projects.
- US-9	Phase by capability (foundations, enablers, value drivers, optimisations); calendar dates project onto that structure.
- US-10	Year 1 includes at least one quick win that demonstrates value early.
- US-11	Calibrate ambition to the customer's IT maturity; raising it is itself a roadmap item.
- US-12	Each phase names its top risks, their owners, and their mitigations.
- US-13	Budget is a shape (envelopes, capex/opex, cycles, renewals), not a total.
- US-14	Name each compliance item as constraint, deadline, or enabler
- US-15	Recommend against MSP services when appropriate.
