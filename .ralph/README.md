# Ralph

![Ralph](ralph.webp)

Ralph is an autonomous AI agent loop that runs AI coding tools ([Amp](https://ampcode.com) or [Claude Code](https://docs.anthropic.com/en/docs/claude-code)) repeatedly until all PRD items are complete. Each iteration is a fresh instance with clean context. Memory persists via git history, `progress.txt`, and `prd.json`.

Based on [Geoffrey Huntley's Ralph pattern](https://ghuntley.com/ralph/).

---

## How It Works

```
/grill-me  →  /prd  →  /ralph  →  ralph.sh (AFK loop)
```

1. **`/grill-me`** — Deep interview that reaches genuine shared understanding before a single requirement is written
2. **`/prd`** — Converts the grilling session into a structured PRD saved to `tasks/`
3. **`/ralph`** — Converts the PRD into `prd.json` with right-sized, ordered user stories
4. **`ralph.sh`** — Autonomous loop that implements every story, commits, and stops when done

---

## Prerequisites

- One of the following AI coding tools installed and authenticated:
  - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`npm install -g @anthropic-ai/claude-code`)
  - [Amp CLI](https://ampcode.com) (default)
- `jq` installed (`brew install jq` on macOS)
- A git repository for your project

---

## Setup

### Option 1: Clone into your project

```bash
# From your project root
git clone https://github.com/ts444/ralph.git .ralph
chmod +x .ralph/ralph.sh .ralph/preflight.sh
```

Copy the agent instruction file to your project root (ralph.sh expects it there):

```bash
cp .ralph/CLAUDE.md ./CLAUDE.md       # for Claude Code
# or
cp .ralph/prompt.md ./prompt.md       # for Amp
```

### Option 2: Install skills globally

**Claude Code:**
```bash
cp -r .ralph/skills/grill-me  ~/.claude/skills/
cp -r .ralph/skills/prd       ~/.claude/skills/
cp -r .ralph/skills/ralph     ~/.claude/skills/
cp -r .ralph/skills/preflight ~/.claude/skills/
```

**Amp:**
```bash
cp -r .ralph/skills/grill-me  ~/.config/amp/skills/
cp -r .ralph/skills/prd       ~/.config/amp/skills/
cp -r .ralph/skills/ralph     ~/.config/amp/skills/
cp -r .ralph/skills/preflight ~/.config/amp/skills/
```

### Configure Amp auto-handoff (recommended)

Add to `~/.config/amp/settings.json`:

```json
{
  "amp.experimental.autoHandoff": { "context": 90 }
}
```

---

## Workflow

### Step 1 — Get grilled

Start an interactive session in Claude Code or Amp and run:

```
/grill-me I want to build [your feature idea]
```

Claude will interview you **one question at a time**, provide a recommended answer for each, and walk down every branch of the design tree until no ambiguity remains. Don't rush this — the quality of the PRD depends entirely on the depth of understanding reached here.

### Step 2 — Generate the PRD

In the **same conversation** (so the grilling context is available), run:

```
/prd
```

The skill reads the decisions from the grill-me session and writes a structured PRD to `tasks/prd-[feature-name].md`. It will only ask follow-up questions for anything the grilling session left unresolved.

### Step 3 — Convert to ralph format

```
/ralph
```

Converts `tasks/prd-[feature-name].md` into `prd.json` with user stories sized to fit one context window each, ordered by dependency.

### Step 4 — Run ralph

```bash
# Claude Code (recommended)
./.ralph/ralph.sh --tool claude 20

# Amp
./.ralph/ralph.sh --tool amp 20
```

Before the loop starts, ralph automatically runs:

1. **`preflight.sh`** — bash checks for tools, prd.json validity, git state, project dependencies, and Claude Code permission settings
2. **Claude preflight iteration** — actually executes `npm`, `git`, etc. in Claude's context to catch permission blocks before they silently stall the run

If anything fails, the run stops immediately with a clear error message. Once both pass, the loop runs unattended.

---

## Preflight Checks

Ralph checks all of these before entering the loop:

| Category | What's checked |
|---|---|
| System tools | `git`, `jq` present |
| prd.json | Valid JSON, required fields, at least one incomplete story |
| Git | Inside a repo, target branch reachable, warns on dirty tree |
| Node.js | `node`, `npm`, `npx`, `tsc`, `node_modules`, quality-check scripts |
| Python / Go / Rust | Relevant toolchain present if project files detected |
| Claude Code settings | `~/.claude/settings.json` and `.claude/settings.json` scanned for deny rules that would block required tools |
| Permission smoke test | Claude actually runs the commands — catches blocks that PATH checks miss |

Run the bash preflight manually at any time:

```bash
./.ralph/preflight.sh
```

Or run the full preflight skill interactively:

```
/preflight
```

### Fixing common preflight failures

| Error | Fix |
|---|---|
| `npm` / `npx` denied in settings | Add `"Bash(npm:*)"` / `"Bash(npx:*)"` to `permissions.allow` in `~/.claude/settings.json` |
| `node_modules` missing | Run `npm install` in your project root |
| No incomplete stories | prd.json is already complete — create a new one with `/ralph` |
| Not inside a git repo | Run `git init && git add -A && git commit -m "init"` |

---

## The Loop

Each iteration ralph:

1. Reads `prd.json` and `progress.txt`
2. Checks out (or creates) the feature branch from `prd.json.branchName`
3. Picks the highest-priority story where `passes: false`
4. Implements it
5. Runs quality checks (typecheck, lint, tests)
6. Commits all changes: `feat: [Story ID] - [Story Title]`
7. Marks the story `passes: true` in `prd.json`
8. Appends learnings to `progress.txt`
9. If all stories pass → outputs `<promise>COMPLETE</promise>` and exits

---

## Key Files

| File | Purpose |
|---|---|
| `ralph.sh` | Main loop — spawns fresh AI instances until all stories pass |
| `preflight.sh` | Bash preflight checks — runs automatically before the loop |
| `CLAUDE.md` | Per-iteration instructions for Claude Code |
| `prompt.md` | Per-iteration instructions for Amp |
| `prd.json` | User stories with `passes` status (the live task list) |
| `prd.json.example` | Example PRD format |
| `progress.txt` | Append-only learnings shared across iterations |
| `skills/grill-me/` | Deep interview skill — run before `/prd` |
| `skills/prd/` | PRD generation skill — reads grill-me context |
| `skills/ralph/` | Converts PRD markdown → `prd.json` |
| `skills/preflight/` | Claude-side preflight checks — permission smoke test |

---

## Critical Concepts

### Right-size your stories

Each story must fit in one context window. If it's too large, the agent runs out of context before finishing.

**Good:**
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic

**Too big (split these):**
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

### Memory between iterations

Each iteration is a **fresh AI instance**. The only memory is:
- Git history (commits from previous iterations)
- `progress.txt` (learnings and codebase patterns)
- `prd.json` (which stories are done)

### Feedback loops are required

Ralph only works if quality checks actually catch errors:
- Typecheck must pass before committing
- Tests must cover the implemented behavior
- CI must stay green — broken code compounds across iterations

### Browser verification for UI stories

Any story that changes the UI should include "Verify in browser using dev-browser skill" in its acceptance criteria. Ralph will navigate to the page and confirm the changes work before marking the story complete.

---

## Debugging

```bash
# See which stories are done
cat prd.json | jq '.userStories[] | {id, title, passes}'

# Check learnings from previous iterations
cat progress.txt

# Check git history
git log --oneline -10
```

---

## Archiving

When you start a new feature (different `branchName` in `prd.json`), ralph automatically archives the previous run to `archive/YYYY-MM-DD-feature-name/`.

---

## References

- [Geoffrey Huntley's Ralph article](https://ghuntley.com/ralph/)
- [Original ralph by snarktank](https://github.com/snarktank/ralph)
- [Amp documentation](https://ampcode.com/manual)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
