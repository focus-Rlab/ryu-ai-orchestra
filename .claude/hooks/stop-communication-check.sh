#!/usr/bin/env bash
# Wrapper so the Stop hook works whether the interpreter is named python3 or
# python, and skips silently (never blocks) if neither actually runs --
# same PATH-robustness fix as scripts/hooks/pre-commit needed on this
# project's own Windows test machine, where a non-functional "python3" App
# Execution Alias stub can shadow a real install on PATH.
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

py=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && [ "$("$candidate" -c 'print(1)' 2>/dev/null)" = "1" ]; then
    py="$candidate"
    break
  fi
done

if [ -z "$py" ]; then
  exit 0
fi

"$py" "$script_dir/stop-communication-check.py"
exit 0
