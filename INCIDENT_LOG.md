# Incident Log

Version: 0.1.0-draft  
Status: Open — corrective policy decisions pending Ryunosuke approval  
Owner and final approver: Ryunosuke Matsumoto  
Recorded by: ChatGPT Raphael  
Independent audit source: Claude Raphael  
Incident date: 2026-07-26  
Record branch: `agent/record-governance-incident`

## 1. Incident title

Governance-bypassing direct commits to `main` for Raphael evaluation criteria

## 2. Executive statement

After pull request #6 was merged into `main` at commit `fa5c0cb52ad68d4afd4089af85e9fc78dc6609a2`, eleven consecutive commits were written directly to `main` on 2026-07-26 without a pull request or a decision-log entry.

The commits changed material evaluation criteria and their official recording structure, including scoring weights, mandatory pass thresholds, correction-round counting, treatment of preference changes, and cross-environment reproducibility criteria. These are not typo, link, formatting, or whitespace corrections.

This conflicts with:

- `GOVERNANCE.md` §3, which requires prior approval for changes to important evaluation criteria and canonical meaning;
- `GOVERNANCE.md` §13, which permits direct commits only for meaning-preserving minor changes and requires a one-line reason when that exception is used;
- the repository's established branch + Draft PR review model for material changes.

This record documents the incident. It does **not** ratify the eleven commits, resolve the semantic conflicts, merge branches, or decide the open governance questions.

## 3. Scope

### In scope

- the eleven direct commits;
- the affected files and criteria;
- the three read-only audits performed by Claude Raphael;
- process causes supported by the audit and available records;
- impact and unresolved decisions;
- the branch and Draft PR used to record the incident.

### Out of scope

- reverting or amending `main`;
- approving or rejecting the evaluation criteria;
- synchronizing `MASTER_SPEC.md` or `SPEC_TRACEABILITY.md`;
- merging `stage2/agent-governance`;
- resolving the authority-model conflict;
- deleting branches or files;
- merging this record into `main`.

## 4. Timeline

1. **2026-07-24:** PR #6 was merged into `main` at `fa5c0cb52ad68d4afd4089af85e9fc78dc6609a2`.
2. **2026-07-26 14:28:57–14:48:43 UTC:** eleven commits were added directly to `main`.
3. **Audit 1:** stale current-state documents and the initial count of four post-PR #6 direct commits were detected.
4. **Audit 2:** the direct-commit count was corrected from four to eleven; all eleven were classified as material evaluation-specification changes with no PR, approval record, or direct-commit exception reason.
5. **Audit 3:** `main` and `stage2/agent-governance` were compared. No file-level conflict was found, but two material semantic conflicts remained.
6. **2026-07-29:** this incident record was prepared on a dedicated branch for Draft PR review. `main` was not changed by this recording action.

## 5. Affected commits

| # | Commit | Change | File(s) | Governance significance |
|---:|---|---|---|---|
| 1 | `93afa5616a7b3e8e4636657d159e0a12a79b1dca` | Defined eight-axis scoring weights and mandatory pass thresholds | `RAPHAEL_TEST_PLAN.md` | Changes important evaluation criteria |
| 2 | `cc17213996cb72f0bac5ec1fca93142dc18d1b17` | Defined two-layer official evaluation-log storage | `RAPHAEL_TEST_PLAN.md` | Changes official evaluation procedure and records |
| 3 | `07faf0bd6f7611f513ef965c236d783ef13ccd26` | Created the official ten-task summary log | `RAPHAEL_TEST_LOG.md` | Creates an official evaluation record |
| 4 | `c314d1e7d7fe8ae132930f5feca25d6ef4bf069c` | Created the task-level evaluation template | `evaluations/raphael/TEMPLATE.md` | Creates the official detailed evaluation format |
| 5 | `4de651a878143a57b5121f044adb8409d77255a6` | Renamed and clarified the revision-round metric in the summary log | `RAPHAEL_TEST_LOG.md` | Synchronizes a newly defined evaluation metric |
| 6 | `5c18f67f94ea32f7557b0e1bd95e1a2af0a6f6b3` | Added revision-round fields to the task template | `evaluations/raphael/TEMPLATE.md` | Synchronizes a newly defined evaluation metric |
| 7 | `02e6330d831321cc269ce92905a1b18c2bb0d1c3` | Defined how correction rounds are counted and the two-round average condition | `RAPHAEL_TEST_PLAN.md` | Changes a formal pass/fail metric |
| 8 | `d79e80dfd1de67f970e492d0685e78b6a422b832` | Added fields for preference-change and ideal-image correction judgments | `evaluations/raphael/TEMPLATE.md` | Adds official evidence fields for correction scoring |
| 9 | `f86f49afb79b16e858a51dcc4523ff4ef5ea9a07` | Defined when ideal-image mismatch counts and when later preference changes are excluded | `RAPHAEL_TEST_PLAN.md` | Changes correction classification and scoring |
| 10 | `09dec7b726a894e518c02763a7162985c542da5e` | Defined cross-environment substantive agreement and the 90-point auxiliary threshold | `RAPHAEL_TEST_PLAN.md` | Changes a formal reproducibility pass criterion |
| 11 | `d2b142784573409060dbaba454ef6d1206e288bf` | Added cross-environment comparison fields to the task template | `evaluations/raphael/TEMPLATE.md` | Synchronizes the newly defined reproducibility criterion |

The displayed ordering above groups paired plan/template changes by subject. In repository history the commits form one direct sequence after PR #6.

## 6. Audit findings

### Audit 1 — Stage 2 initial cross-document audit

Findings:

- `README.md`, main's `PROJECT_HANDOFF.md`, and `ROADMAP.md` still described PR #6 as awaiting approval or being worked on, although PR #6 had already been merged.
- The verified PR #6 merge commit is `fa5c0cb52ad68d4afd4089af85e9fc78dc6609a2`.
- At the initial audit point, four direct commits after the merge were identified.
- `SPEC_TRACEABILITY.md` still stated that official evaluation-log storage and scoring weights were unresolved, conflicting with the evaluation plan already changed on `main`.
- Main's current-state documents did not expose the existence or work state of `stage2/agent-governance`, so a reader following the prescribed entry path could not reconstruct the actual Stage 2 work.

### Audit 2 — direct-commit re-audit

Findings:

- The direct-commit count was eleven, not four.
- The eleven commits materially changed `RAPHAEL_TEST_PLAN.md`, `RAPHAEL_TEST_LOG.md`, and `evaluations/raphael/TEMPLATE.md`.
- None of the eleven changes was limited to a typo, link, formatting, or whitespace correction.
- No pull request was used.
- No decision-log entry or other approval record was found for these commits.
- No one-line reason was recorded to invoke the minor direct-commit exception.
- Approval basis for every commit is therefore recorded as **unknown**, not assumed.

### Audit 3 — `main` × `stage2/agent-governance` comparison

Findings:

- No file-level conflict was found between the two lines of work.
- The branches nevertheless diverged semantically and operationally: evaluation criteria advanced on `main`, while agent-governance design advanced on `stage2/agent-governance`.
- **D-1:** `GOVERNANCE.md` §3 requires approval for important evaluation-criteria changes, but the eleven material changes were committed directly to `main` without a recorded approval gate.
- **D-2:** `agents/raphael.md` uses a binary practical authority boundary, while the draft `AGENT_STANDARD.md` defines an L0–L4 model. Their intended relationship is unresolved.

Neither D-1 nor D-2 is resolved by this incident record.

## 7. Cause analysis

### Confirmed process causes

The available records support the following process failures:

1. The target branch was not explicitly verified and reported before each write.
2. Content approval in conversation was treated as if it also authorized direct write to `main`; those are separate approvals.
3. The agreed unit of change—one task branch plus Draft PR—was not enforced before repository writes.
4. Post-write verification did not check current branch, PR association, divergence from `main`, or cross-canonical synchronization.
5. Current-state synchronization failed after PR #6 merged, allowing stale entry documents to conceal the actual repository state.
6. Parallel Stage 2 work was not surfaced from main's entry documents, allowing two work lines to progress without a single reviewable integration path.
7. Important decisions were written to one evaluation source without synchronizing the complete specification and traceability layer or stopping on the detected inconsistency.

### Attribution limitation

GitHub metadata identifies the author and committer account as `focus-Rlab`. That does not establish whether the actual initiating actor was Ryunosuke, ChatGPT Raphael, another AI, or another tool operating through the account.

The identity of the initiating actor remains an open item and must not be inferred from account metadata alone.

## 8. Impact

### Canonical integrity

- Material pass/fail criteria appear in the evaluation plan as if formally settled.
- `SPEC_TRACEABILITY.md` and `MASTER_SPEC.md` were not fully synchronized to those criteria.
- Readers cannot determine from main alone whether the criteria are approved, provisional, or unauthorized.

### Approval authority

- Ryunosuke's right to review important changes before they become main-state was bypassed at the repository-control level.
- Conversation-level selection and repository-level approval were conflated.

### Evaluation validity

- Future Raphael evaluation could apply weights, thresholds, correction rules, or reproducibility criteria whose approval status is unclear.
- Evaluation records created under the current state could inherit that uncertainty.

### Branch and Stage 2 integration

- `main` contains the eleven evaluation commits.
- `stage2/agent-governance` contains separate governance-design commits.
- The timing and method for reconciling these histories is unresolved.
- The unresolved authority-model difference may affect future agent-governance implementation.

### Recurrence risk

Without an approved corrective policy and enforcement mechanism, another AI session or tool could repeat the same pattern: interpret a content decision as write authorization, update `main`, and leave cross-document or branch state unsynchronized.

## 9. Open items — explicitly unresolved

The following require Ryunosuke's answer. This record does not choose for him.

1. **Actual initiating actor**  
   Were the eleven direct commits initiated by Ryunosuke personally, or through another AI/tool?

2. **Status of the evaluation criteria**  
   Should the weights, mandatory lines, correction-round definition, preference-change exclusion rule, and 90-point reproducibility criterion be formally approved as-is, or remain open for review?

3. **Future repository procedure**  
   Should all material changes use a dedicated branch + Draft PR, with direct commits limited to the existing meaning-preserving exception?

4. **Reconciliation timing**  
   When should `stage2/agent-governance` be brought up to date with the current `main` history?

5. **Authority-model relationship**  
   Should the binary authority model in `agents/raphael.md` and the L0–L4 draft in `AGENT_STANDARD.md` be unified, or retained for different purposes with an explicit mapping?

## 10. Corrective options awaiting approval

These are proposals, not decisions.

1. Correct stale PR #6 state in `README.md`, main's `PROJECT_HANDOFF.md`, and `ROADMAP.md`.
2. Add a visible reference from main's entry documents to the active or pending `stage2/agent-governance` work.
3. Decide whether to ratify, revise, or supersede the eleven commits' evaluation criteria.
4. After that decision, synchronize `MASTER_SPEC.md`, `SPEC_TRACEABILITY.md`, the evaluation documents, and current-state documents in one reviewable change.
5. Decide when and how to reconcile `stage2/agent-governance` with current `main`.
6. Add an enforceable pre-write check that records target branch, approval basis, PR association, affected canonical files, and post-write verification.

## 11. Containment and current status

- This incident is being recorded on `agent/record-governance-incident`.
- The record is submitted through a Draft PR targeting `main`.
- No direct commit to `main` is used for this record.
- No merge, revert, deletion, authority change, evaluation ratification, or semantic-conflict resolution is included.
- The incident remains open until Ryunosuke decides the open items and approves any corrective implementation.

## 12. Closure criteria

This incident may be marked closed only after:

1. Ryunosuke answers or explicitly defers every open item;
2. the status of the eleven evaluation changes is unambiguous;
3. stale current-state documents are corrected through an approved PR;
4. branch reconciliation timing and ownership are recorded;
5. the authority-model relationship is resolved or explicitly deferred with a documented boundary;
6. corrective controls are implemented and tested;
7. Ryunosuke approves the closure record.


---

# Incident: paid-service approval gate omitted from initial Week 1 core

Incident date: 2026-07-29  
Record branch: `agent/v1-week1-general-core`

## Summary

The initial Week 1 implementation treated the 7,000/9,000/10,000 JPY monthly budget thresholds as the primary cost control. It did not separately enforce Ryunosuke's higher-priority rule that any paid, billable, or cost-uncertain service requires prior explicit approval even below the monthly thresholds.

## Root cause

The implementation conflated two different decisions: permission to use a paid service and permission to exceed or approach a monthly budget limit. Cost amount was modeled, but billing-risk classification and a separate `paid_service` approval scope were absent.

## Impact and similar-case audit

Without correction, a request estimated at 1 JPY could execute without prior approval. A zero-estimate service with automatic billing risk or unknown pricing could also pass. README, ROADMAP, NEXT_SESSION_PROMPT, SECURITY, GOVERNANCE, MASTER_SPEC, PROJECT_HANDOFF, and SPEC_TRACEABILITY were audited because stale wording could reproduce the same mistake in another AI session.

## Correction and prevention

- Added `CostKind` with local-free, guaranteed-free, paid-or-billable, and unknown classifications.
- Added a fail-closed pre-execution `paid_service` approval gate.
- Kept `budget_override` separate so monthly-limit approval cannot authorize the underlying paid service.
- Added startup, governance, security, roadmap, handoff, traceability, and session-entry rules.
- Added success, failure, and similar-case tests for 1 JPY, zero-estimate billable, unknown pricing, budget-only approval, five accepted AI windows, invalid approvers, end-to-end flow, verification failure, and side-effect rollback.

## Verification

`python -m unittest discover -s tests -v`: 12 tests passed.  
`python -m compileall -q v1_core tests`: passed.

Status: corrective implementation complete in Draft PR #12; main merge remains Ryunosuke's decision.
