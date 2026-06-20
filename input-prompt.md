# Project kickoff: Strategic IT consulting agent harness

I'm building an agentic AI harness on top of this Claude Code project.

## What the harness does (one sentence)

It conducts strategic IT consulting for customers of a Managed Service Provider
(MSP) and produces a 3-year roadmap showing how the customer reaches its
strategic goals using the MSP's service portfolio.

## Inputs the agent will work from

- **Hard facts — MSP service portfolio:** an Obsidian notebook (path/structure
  to be decided in our session).
- **Hard facts — customer data:** a custom customer portal backed by a Postgres
  database (access pattern to be decided in our session).
- **Soft facts:** elicited from the human consultant during an interactive
  consulting interview the agent conducts.
- **Cross-cutting constraints:** compliance frameworks and budget, treated as
  first-class factors in the analysis.

## Output

A 3-year roadmap. Structure, granularity, format, and review checkpoints are
open questions.

## Design principles — read and apply before your first question

Read `~/strategic-consultation/design-principles` in full before grilling. Treat it as the
standard every question and every recommended answer is held to — not as
background reading. The document covers:

1. Rules for the agent itself.
2. Knowledge-intensive harness design (explicitly distinct from coding-harness
   design — do not import coding-harness assumptions).
3. The consultation method.
4. Specifics for strategic IT consulting.

The document has its own tiebreaker for internal conflicts (earlier sections
win). If anything in *this prompt* conflicts with the document, the document
wins — flag the conflict and ask. Don't ask me to restate things the document
already settles; cite it and move on.

## How to run the grilling

- Apply proportionality: grill irreversible and high-stakes decisions deeply;
  default low-stakes ones with a note and move on.
- For each question, the recommended answer must be consistent with the
  design principles — if no consistent answer exists, say so and ask me to
  resolve the tension.

## Priority areas

Front-load questions on:

- **Harness architecture:** subagent decomposition, isolated contexts, tool
  design, model-to-task routing, deterministic vs reasoning work.
- **Source-of-truth vs working memory:** how Obsidian and Postgres feed the
  agent without being mutated by it; how structured memory is maintained and
  decayed.
- **The consultation workflow:** phase contracts (intake → situation → gap
  analysis → mapping → roadmap → handover), entry/exit conditions, artifact
  templates.
- **Hard vs soft facts:** the boundary, and what happens when they disagree.
- **Compliance and budget:** how they flow through every stage as constraints,
  deadlines, or enablers — not as afterthoughts.
- **Human-in-the-loop gates:** where the consultant ratifies, calibrated to
  reversibility.
- **Failure modes specific to a knowledge-intensive (not coding) harness.**