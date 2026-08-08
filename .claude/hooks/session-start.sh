#!/bin/bash
set -euo pipefail

# Installs the main-branch commit guard into .git/hooks/pre-commit directly,
# using core's default hook location (part of .git/, not the working tree),
# so protection exists no matter which branch happens to be checked out.
#
# First attempt (2026-08-07) pointed core.hooksPath at the tracked
# scripts/hooks/ directory instead. That failed silently: scripts/hooks/pre-commit
# only exists on branches where it has been committed, so checking out `main`
# (which did not yet have it) made the hook vanish on exactly the branch it
# was meant to protect, and a commit landed on main during the very test that
# was supposed to prove the guard worked. See INCIDENT_LOG.md, "Independent
# review synthesis (2026-08-07)" for the incident and the fix below.
#
# Keep this logic identical to scripts/hooks/pre-commit (the readable,
# reviewable source copy); this file is the self-contained installer.

GIT_DIR="$(git -C "$CLAUDE_PROJECT_DIR" rev-parse --absolute-git-dir)"
HOOK_PATH="$GIT_DIR/hooks/pre-commit"
mkdir -p "$(dirname "$HOOK_PATH")"

cat > "$HOOK_PATH" << 'HOOK_EOF'
#!/usr/bin/env bash
set -euo pipefail

current_branch="$(git branch --show-current)"

if [ "$current_branch" = "main" ]; then
  echo "REFUSED (pre-commit hook): current branch is 'main'." >&2
  echo "Non-trivial changes must be committed on a dedicated branch (GOVERNANCE.md §13)." >&2
  echo "Create or switch to a working branch first, e.g.:" >&2
  echo "  git checkout -B <branch-name> origin/main" >&2
  exit 1
fi

# Canonical-document environment-neutrality check. Root cause this closes:
# INCIDENT_LOG.md "environment-specific facts written into AI-agnostic
# canonical agent files (2026-08-07)". Best-effort: skips with a warning if
# python or the checker script is unavailable, rather than blocking unrelated
# commits on a missing secondary tool — only the main-branch guard above is
# unconditional.
staged_agent_files="$(git diff --cached --name-only -- 'agents/*.md' || true)"
if [ -n "$staged_agent_files" ]; then
  checker="scripts/check_canonical_environment_neutrality.py"
  py=""
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && [ "$("$candidate" -c 'print(1)' 2>/dev/null)" = "1" ]; then
      py="$candidate"
      break
    fi
  done
  if [ -z "$py" ] || [ ! -f "$checker" ]; then
    echo "WARNING (pre-commit hook): skipping canonical environment-neutrality check (python or $checker not found)." >&2
  else
    tmpdir="$(mktemp -d)"
    check_failed=0
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      out="$tmpdir/staged.md"
      git show ":$f" > "$out"
      if ! output="$("$py" "$checker" "$out" --root "$tmpdir" 2>&1)"; then
        check_failed=1
        echo "[$f]" >&2
        echo "$output" >&2
      fi
    done <<< "$staged_agent_files"
    rm -rf "$tmpdir"
    if [ "$check_failed" -eq 1 ]; then
      echo "REFUSED (pre-commit hook): canonical environment-neutrality check failed on staged agents/*.md changes." >&2
      echo "If the phrasing is intentional and environment-agnostic, rephrase it. If it is genuinely environment-specific, move it to the matching .claude/agents or .codex/agents adapter file instead." >&2
      exit 1
    fi
  fi
fi
HOOK_EOF

chmod +x "$HOOK_PATH"

# core.hooksPath may have been set to scripts/hooks by an earlier session;
# unset it so git falls back to the default .git/hooks location this script
# just wrote to. Ignore failure if it was never set.
git -C "$CLAUDE_PROJECT_DIR" config --unset core.hooksPath 2>/dev/null || true
