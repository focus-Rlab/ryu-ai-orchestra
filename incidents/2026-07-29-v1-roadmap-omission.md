# Canonical Incident — Omitted V1 Roadmap Propagation

Date: 2026-07-29
Status: Corrective branch prepared; closure requires Ryunosuke review and main merge
Branch: `agent/roadmap-and-canonical-audit`

## Incident

The assistant reported that main had been synchronized after PR #9, but only updated the “Stage 2 complete / Stage 3 start” status. The user-approved V1 roadmap restructuring was not added to ROADMAP or propagated across the canonical document system.

## Why this is serious

The canonical repository is designed to replace fragile conversation memory. If a confirmed decision remains only in conversation or a decision log while README/ROADMAP/HANDOFF direct future work elsewhere, the repository cannot reproduce the intended project. The omission therefore invalidated the claim that canonical synchronization was complete and forced a full audit.

## Root cause

- Narrow interpretation of the last instruction instead of the full decision sequence.
- Verification of labels rather than semantic traceability.
- No explicit inventory of confirmed decisions before declaring synchronization complete.
- No fresh-session reconstruction test after the change.

## Impact

- Wrong next stage and work order on main.
- V1 target, budget, time, validation order, and approval channel hidden from the primary route.
- Increased user audit burden and reduced trust in all previous synchronization claims.
- Similar stale statements remained in traceability, initial design, and next-session instructions.

## Correction

- Created a dedicated audit branch.
- Restored the V1 Week 0〜4 roadmap.
- Propagated V1 decisions to operational and complete canon.
- Corrected stale PR/branch/evaluation-state statements.
- Added an audit report and a decision-inventory completeness gate.
- Kept unresolved evaluation approvals unresolved.

## Closure criteria

1. All findings in `docs/CANONICAL_AUDIT_2026-07-29.md` are verified against actual files.
2. Fresh-session reading of README → PROJECT_HANDOFF → ROADMAP leads to V1 Week 0/1, not obsolete Stage 3.
3. No stale active reference to merged branches/PRs remains.
4. Every V1 decision has traceable canonical destinations.
5. The user reviews the Draft PR and performs the main merge.
