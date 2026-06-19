# Strategic Consulting Harness

A knowledge-intensive Claude Code harness for conducting strategic IT consulting engagements. Produces a 3-year roadmap per customer engagement across seven phases.

## Structure

```
strategic-consultation/
├── design-principles.md        # Binding design contract — see below
├── CHANGELOG.md
├── templates/                  # Artifact templates and schemas
│   ├── _claim.schema.md        # Atomic claim and composed-block definitions
│   ├── _registers/             # Root register schemas
│   └── *.template.md           # Phase artifact templates
├── prompts/
│   ├── orchestrator/           # Per-phase orchestrator prompts (00–06)
│   └── subagents/              # Retriever, interviewer, synthesizer prompts
├── validator/
│   ├── cli.py                  # Deterministic validator CLI
│   └── rules/                  # One file per validation rule
├── mcp/
│   ├── portfolio-mcp/          # Read-only MCP server wrapping ~/msp-portfolio
│   └── customer-mcp/           # Read-only MCP server wrapping customer-portal HTTP API
├── harness/                    # CLI tools: init, enter_phase, decay_check, explain, check_contradictions
├── backlog/
│   └── change-requests/        # CR-YYYY-NNN.md retro change requests
└── .ralph/                     # Ralph autonomous-agent harness (vendored in-repo; upstream ts444/ralph)
    ├── prd.json                # Active PRD driving the Ralph build loop
    ├── progress.txt            # Ralph iteration progress log
    └── ralph.sh                # Ralph AFK run loop
```

## Binding design contract

`design-principles.md` at repo root defines the ground rules for this harness. Every template, prompt, validator rule, and tool must respect those principles. When a design decision conflicts with a principle, the principle wins.

## Phases

| Phase | Artifact | Entry condition |
|-------|----------|----------------|
| 00 Intake | scope.md | — |
| 01 Situation | situation.md | scope.md ratified |
| 02 Gap analysis | gaps.md | situation.md ratified |
| 03 Mapping | service-map.md, recommendations.md | gaps.md ratified |
| 04 Roadmap | roadmap.md | recommendations.md ratified |
| 05 Handover | handover.md | roadmap.md ratified |
| 06 Retro | retro.md + change requests | handover.md ratified |

## Getting started

```bash
python harness/init.py <customer-name> [--target-dir <path>]
cd <target-dir>
python <harness-repo>/harness/enter_phase.py
```

## Versioning

See CHANGELOG.md. Engagement repos pin `harness_version` in their `CLAUDE.md`. The `enter_phase` CLI enforces version matching.
