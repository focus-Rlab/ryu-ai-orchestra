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
HOOK_EOF

chmod +x "$HOOK_PATH"

# core.hooksPath may have been set to scripts/hooks by an earlier session;
# unset it so git falls back to the default .git/hooks location this script
# just wrote to. Ignore failure if it was never set.
git -C "$CLAUDE_PROJECT_DIR" config --unset core.hooksPath 2>/dev/null || true
