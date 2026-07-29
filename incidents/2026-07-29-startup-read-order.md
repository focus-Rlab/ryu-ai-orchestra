# Startup read-order process incident

Date: 2026-07-29

## Summary

During the Week 2 Codex session, repository structure and V1 source files were
inspected before `STARTUP_CONTEXT.md` was read and acknowledged. No repository
file had been changed at the time the violation was detected.

## Root cause

The repository was cloned and immediately inspected using a generic repository
orientation routine. The routine did not make the repository-owned
`STARTUP_CONTEXT.md` gate its first post-clone read.

## Impact

- No code, document, GitHub branch, issue, or PR was changed before detection.
- No paid service or external execution was used.
- The analysis order violated `AGENTS.md` and `STARTUP_CONTEXT.md`, even though
  later decisions were revalidated against the required sources.

## Containment

Implementation stopped. `STARTUP_CONTEXT.md`, the README router, current-state
sources, governance, security, Raphael, roadmap, master specification, and
traceability sources were read before implementation resumed.

## Prevention

For this repository, the first post-clone content read must be:

1. `STARTUP_CONTEXT.md`;
2. `README.md`;
3. the README-routed required sources.

Repository-wide listing or source inspection must wait until the startup read is
acknowledged. The rule is tested by recording this incident and including it in
the Week 2 review scope; no new authority or evaluation criterion is created.
