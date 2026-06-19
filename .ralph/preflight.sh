#!/bin/bash
# Ralph preflight checks — run before the main AFK loop.
# Surfaces every issue that would cause a silent failure mid-run.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
FAILED=0
WARNINGS=0

pass()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
fail()   { printf "  \033[31m✗\033[0m %s\n" "$*"; FAILED=1; }
warn()   { printf "  \033[33m⚠\033[0m %s\n" "$*"; WARNINGS=1; }
header() { printf "\n%s:\n" "$*"; }

echo "==================================================="
echo "  Ralph Preflight Checks"
echo "==================================================="

# ---------------------------------------------------------------------------
# 1. Required tools (ralph.sh itself needs these)
# ---------------------------------------------------------------------------
header "Required tools"
for cmd in git jq; do
  if command -v "$cmd" &>/dev/null; then
    pass "$cmd — $($cmd --version 2>&1 | head -1)"
  else
    fail "$cmd not found — install it before running ralph"
  fi
done

# ---------------------------------------------------------------------------
# 2. prd.json
# ---------------------------------------------------------------------------
header "prd.json"
if [ ! -f "$PRD_FILE" ]; then
  fail "prd.json not found at $PRD_FILE"
else
  pass "prd.json found"

  if ! jq . "$PRD_FILE" &>/dev/null; then
    fail "prd.json is not valid JSON"
  else
    pass "valid JSON"

    for field in project branchName userStories; do
      if jq -e ".$field" "$PRD_FILE" &>/dev/null; then
        pass ".$field present"
      else
        fail ".$field missing — prd.json is incomplete"
      fi
    done

    if jq -e '.userStories' "$PRD_FILE" &>/dev/null; then
      TOTAL=$(jq '.userStories | length' "$PRD_FILE")
      INCOMPLETE=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE")
      if [ "$INCOMPLETE" -gt 0 ]; then
        pass "$INCOMPLETE / $TOTAL stories pending"
      else
        fail "no stories with passes:false — nothing for ralph to do"
      fi
    fi
  fi
fi

# ---------------------------------------------------------------------------
# 3. Git
# ---------------------------------------------------------------------------
header "Git"
if git -C "$SCRIPT_DIR" rev-parse --git-dir &>/dev/null 2>&1; then
  pass "inside a git repository"

  if [ -f "$PRD_FILE" ] && jq -e '.branchName' "$PRD_FILE" &>/dev/null; then
    BRANCH=$(jq -r '.branchName' "$PRD_FILE")
    if git -C "$SCRIPT_DIR" show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
      pass "branch '$BRANCH' exists locally"
    else
      pass "branch '$BRANCH' will be created at loop start"
    fi
  fi

  DIRTY=$(git -C "$SCRIPT_DIR" status --porcelain 2>/dev/null)
  if [ -n "$DIRTY" ]; then
    warn "uncommitted changes present — ralph will incorporate them into its first commit"
  else
    pass "working tree clean"
  fi
else
  fail "not inside a git repository — ralph needs git to commit progress"
fi

# ---------------------------------------------------------------------------
# 4. Node.js project
# ---------------------------------------------------------------------------
if [ -f "$SCRIPT_DIR/package.json" ] || [ -f "./package.json" ]; then
  PKG_DIR="$SCRIPT_DIR"
  [ -f "./package.json" ] && PKG_DIR="$(pwd)"

  header "Node.js (package.json detected)"
  for cmd in node npm npx; do
    if command -v "$cmd" &>/dev/null; then
      pass "$cmd — $($cmd --version 2>&1 | head -1)"
    else
      fail "$cmd not found — install Node.js before running ralph"
    fi
  done

  if [ -d "$PKG_DIR/node_modules" ]; then
    pass "node_modules present"
  else
    fail "node_modules missing — run 'npm install' before starting ralph"
  fi

  # TypeScript
  if jq -e '.devDependencies.typescript // .dependencies.typescript' "$PKG_DIR/package.json" &>/dev/null; then
    if [ -f "$PKG_DIR/node_modules/.bin/tsc" ]; then
      TSC_VER=$("$PKG_DIR/node_modules/.bin/tsc" --version 2>&1)
      pass "tsc — $TSC_VER"
    else
      fail "typescript in package.json but tsc missing from node_modules/.bin — run 'npm install'"
    fi
  fi

  # Warn about missing quality-check scripts ralph will try to run
  for script in typecheck lint test; do
    if jq -e ".scripts.\"$script\"" "$PKG_DIR/package.json" &>/dev/null; then
      pass "npm run $script defined"
    else
      warn "no '$script' script in package.json — ralph may fail quality checks"
    fi
  done
fi

# ---------------------------------------------------------------------------
# 5. Python project
# ---------------------------------------------------------------------------
if [ -f "$SCRIPT_DIR/pyproject.toml" ] || [ -f "$SCRIPT_DIR/requirements.txt" ] || [ -f "./pyproject.toml" ] || [ -f "./requirements.txt" ]; then
  header "Python (Python project detected)"
  if command -v python3 &>/dev/null; then
    pass "python3 — $(python3 --version 2>&1)"
  elif command -v python &>/dev/null; then
    pass "python — $(python --version 2>&1)"
  else
    fail "python / python3 not found"
  fi
  if command -v pip3 &>/dev/null || command -v pip &>/dev/null; then
    pass "pip available"
  else
    warn "pip not found"
  fi
fi

# ---------------------------------------------------------------------------
# 6. Go project
# ---------------------------------------------------------------------------
if [ -f "$SCRIPT_DIR/go.mod" ] || [ -f "./go.mod" ]; then
  header "Go (go.mod detected)"
  if command -v go &>/dev/null; then
    pass "go — $(go version 2>&1)"
  else
    fail "go not found"
  fi
fi

# ---------------------------------------------------------------------------
# 7. Rust project
# ---------------------------------------------------------------------------
if [ -f "$SCRIPT_DIR/Cargo.toml" ] || [ -f "./Cargo.toml" ]; then
  header "Rust (Cargo.toml detected)"
  if command -v cargo &>/dev/null; then
    pass "cargo — $(cargo --version 2>&1)"
  else
    fail "cargo not found"
  fi
fi

# ---------------------------------------------------------------------------
# 8. Claude Code permission settings
#
# ralph.sh already passes --dangerously-skip-permissions, which bypasses
# allow/deny rules. But if the user runs the loop another way (or the flag
# is stripped) a deny rule will silently block commands mid-run.
# ---------------------------------------------------------------------------
header "Claude Code permission settings"
SETTINGS_CHECKED=0

check_claude_settings() {
  local file="$1"
  [ -f "$file" ] || return
  SETTINGS_CHECKED=1

  # Collect denied patterns
  DENIED=$(jq -r '(.permissions.deny // []) | .[]' "$file" 2>/dev/null || true)
  if [ -z "$DENIED" ]; then
    pass "$file — no deny rules"
    return
  fi

  BLOCKED_ANY=0
  for tool in npm npx node git python cargo go; do
    if echo "$DENIED" | grep -qi "$tool"; then
      fail "$file denies '$tool' — add it to permissions.allow or remove the deny rule"
      BLOCKED_ANY=1
    fi
  done
  [ "$BLOCKED_ANY" -eq 0 ] && pass "$file — deny rules don't block required tools"
}

check_claude_settings "$HOME/.claude/settings.json"
check_claude_settings "$HOME/.claude/settings.local.json"
check_claude_settings "$SCRIPT_DIR/.claude/settings.json"
check_claude_settings ".claude/settings.json"

if [ "$SETTINGS_CHECKED" -eq 0 ]; then
  warn "no Claude settings.json found to inspect"
fi

# ralph.sh already uses --dangerously-skip-permissions for claude tool
warn "reminder: ralph.sh passes --dangerously-skip-permissions — if you run the loop another way, ensure required tools are in your allow list"

# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
echo ""
echo "==================================================="
if [ "$FAILED" -eq 1 ]; then
  printf "  \033[31mPREFLIGHT FAILED\033[0m — fix errors above before running ralph\n"
  echo "==================================================="
  exit 1
elif [ "$WARNINGS" -eq 1 ]; then
  printf "  \033[33mPREFLIGHT PASSED WITH WARNINGS\033[0m — review above before going AFK\n"
  echo "==================================================="
  exit 0
else
  printf "  \033[32mALL CHECKS PASSED\033[0m — ralph is ready to run\n"
  echo "==================================================="
  exit 0
fi
