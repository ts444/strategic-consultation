---
name: preflight
description: "Check all preconditions before a ralph AFK run. Verifies that required commands can actually execute (catches Claude Code permission blocks), dependencies are installed, prd.json is valid, and git is ready. Run this manually before starting ralph, or ralph.sh runs it automatically."
user-invocable: true
---

# Ralph Preflight Check

Before starting the ralph loop, verify every precondition that could silently break a multi-hour AFK run. A blocked `npm` command or missing `node_modules` discovered at hour three is far worse than catching it now.

Work through each section below. Print a clear pass/fail line for each item. At the end, print either `<preflight-passed>` or `<preflight-failed>` so the caller can detect the result.

---

## 1. Command Execution — Permission Check

**Actually run** each command (don't just check PATH). A command that exists on disk but is blocked by Claude Code permissions will fail here, not silently later.

Run and report the output of:
- `git --version`
- `node --version` *(if package.json exists)*
- `npm --version` *(if package.json exists)*
- `npx --version` *(if package.json exists)*

If any command is **blocked by a permission error** (distinct from "not found"):
- Report: `BLOCKED: <command> — add it to permissions.allow in your Claude Code settings, or run ralph with --dangerously-skip-permissions`
- Mark as a critical failure

---

## 2. prd.json Validity

Read `prd.json` and verify:
- File exists and is valid JSON
- Has `project`, `branchName`, and `userStories` fields
- At least one story has `passes: false` (otherwise there is nothing to do)
- All story IDs are unique

---

## 3. Git State

- Confirm we are inside a git repository
- Check whether the branch in `prd.json.branchName` exists locally; if not, confirm it can be created from the current branch
- List any uncommitted changes (not a failure, but worth noting — ralph will commit them)

---

## 4. Project Dependencies

**Node.js** — if `package.json` exists:
- Confirm `node_modules/` is present; if missing, run `npm install` now and re-check
- If `typescript` is in dependencies: run `npx tsc --version` to confirm tsc is usable
- List which quality-check scripts exist in `package.json` (`typecheck`, `lint`, `test`) — warn for any that are missing, since ralph will try to run them

**Python** — if `pyproject.toml` or `requirements.txt` exists:
- Confirm `python3` (or `python`) is available

**Go** — if `go.mod` exists: confirm `go` is available

**Rust** — if `Cargo.toml` exists: confirm `cargo` is available

---

## 5. Progress File

- If `progress.txt` exists: confirm it is readable
- If it does not exist: note that ralph will create it — no action needed

---

## Output

Print a summary of every check. Then end with exactly one of:

```
<preflight-passed>
```
```
<preflight-failed>
1. <first issue>
2. <second issue>
...
```
