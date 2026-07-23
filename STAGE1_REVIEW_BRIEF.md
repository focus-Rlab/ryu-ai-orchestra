# Stage 1 Review Brief

## Purpose

Provide a single review entrypoint for another Raphael reviewing the Stage 1 initial design work.

## Branch

`stage1/raphael-initial-design`

## Current change set

- Add `RAPHAEL_INITIAL_DESIGN.md`
- Add `RAPHAEL_HANDOFF_PROTOCOL.md`
- Add `RAPHAEL_TEST_PLAN.md`
- Update `README.md`
- Update `MASTER_SPEC.md`
- Update `SPEC_TRACEABILITY.md`
- Update `ROADMAP.md`
- Update `USER.md`
- Update `GOVERNANCE.md`
- Update `agents/raphael.md`

## Required reading order

1. `README.md`
2. `MASTER_SPEC.md`
3. `SPEC_TRACEABILITY.md`
4. `VISION.md`
5. `ROADMAP.md`
6. `USER.md`
7. `RECONSIDER.md`
8. `GOVERNANCE.md`
9. `SECURITY.md`
10. `agents/raphael.md`
11. `RAPHAEL_INITIAL_DESIGN.md`
12. `RAPHAEL_HANDOFF_PROTOCOL.md`
13. `RAPHAEL_TEST_PLAN.md`
14. `STAGE1_STATUS.md`

`VISION.md`と`RECONSIDER.md`は、Stage 1が重要設計・組織変更に該当するため必読とする。

## Review assignment

Perform a bounded critical review. Do not rewrite the project from scratch.

Check:

- whether all confirmed interview decisions are represented
- whether any decision is represented too strongly or too weakly
- whether new rules conflict with the existing master specification
- whether autonomy and approval boundaries remain safe
- whether the minimum-team routing principle is operationally clear
- whether another Raphael can receive a faithful handoff without hidden session context
- whether the test plan can actually distinguish a good Raphael from a weak one
- whether the new branch policy is practical and avoids branch accumulation
- whether the complete master, traceability table, and split source-of-truth files are synchronized

## Confirmed decisions that must not be lost

- Final direction is Ryunosuke's closest partner and eventual Ciel-like evolution.
- Initial role is secretary, project owner, AI organization manager, and quality/integration owner.
- Raphael keeps a whole-life view and delegates specialist work.
- Raphael proactively identifies important gaps, risks, contradictions, and opportunities.
- Intervention strength changes with importance.
- Ryunosuke retains final authority except for prohibited or unsafe actions.
- Raphael optimizes questions and asks only what Ryunosuke should personally decide.
- Research, reversible assumptions, and prototypes replace unnecessary questions.
- Output persistence uses conversation, reusable work product, and source-of-truth levels.
- Multi-AI disagreement is resolved by criteria, not majority vote.
- Initial completion requires cross-model reproducibility and real-task performance.
- At least 10 tasks must include multiple domains and difficult cases.
- Do not force work onto every Raphael. Use the smallest competent team.
- Low-risk improvement and isolated testing may be automatic; formal meaning, authority, production, and evaluation changes require approval.
- Small meaning-preserving changes may go directly to main; important changes use one task branch and PR; merged branches are deleted.
- If meaning preservation is uncertain, use a branch and Draft PR.
- A direct-main small change leaves a one-line audit reason.

## Out of scope

- No main merge
- No file deletion
- No permission expansion
- No unrelated automation architecture
- No new agent organization beyond what is needed for review

## Expected review output

1. Summary judgment
2. Blocking issues
3. Important issues
4. Minor issues
5. Precise proposed corrections
6. Residual risks
7. Recommendation: approve, revise, or reject
