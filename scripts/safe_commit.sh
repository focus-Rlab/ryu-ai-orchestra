#!/usr/bin/env bash
# Mechanical pre-commit branch guard.
#
# Root cause this closes: INCIDENT_LOG.md incident #1 (2026-07-26) and its
# 2026-08-07 recurrence (INCIDENT_LOG.md "Incident #1 §13") both trace to the
# same failure — a write to `main` proceeded because content approval was
# treated as write-location approval, without checking the current branch
# first. Documentation alone did not prevent the second occurrence, so this
# script makes the check mechanical: it refuses to run `git commit` at all
# while the current branch is `main`.
#
# Usage: scripts/safe_commit.sh -m "message"   (forwards all args to git commit)
set -euo pipefail

current_branch="$(git branch --show-current)"

if [ "$current_branch" = "main" ]; then
  echo "REFUSED: current branch is 'main'." >&2
  echo "Non-trivial changes must be committed on a dedicated branch (GOVERNANCE.md §13)." >&2
  echo "Create or switch to a working branch first, e.g.:" >&2
  echo "  git checkout -B <branch-name> origin/main" >&2
  exit 1
fi

exec git commit "$@"
