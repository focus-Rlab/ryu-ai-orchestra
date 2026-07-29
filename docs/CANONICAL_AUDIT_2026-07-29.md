# Canonical Audit — 2026-07-29

Status: In review
Branch: `agent/roadmap-and-canonical-audit`
Scope: V1 roadmap restoration and cross-canonical completeness audit

## 1. Incident

After PR #9 was merged, README, ROADMAP, and PROJECT_HANDOFF were updated to say “Stage 2 complete / Stage 3 start.” The update did not include the new V1 roadmap restructuring confirmed in the same decision sequence. Completion was reported after checking only current-state labels, not semantic agreement with all confirmed decisions.

## 2. Severity and impact

This is a canonical-integrity failure, not a cosmetic omission.

- The main roadmap showed an obsolete Stage 3〜5 sequence.
- A new session following README and PROJECT_HANDOFF would start the wrong work.
- V1's general-purpose target, resource limits, cost gates, validation order, and approval channel existed mainly in STAGE2_DECISION_LOG and were not visible in the operational canon.
- The user could no longer trust that prior conversation decisions had been propagated.
- A full audit became necessary.

## 3. Root cause

1. The assistant scoped the requested sync to the last sentence (“Stage 2 complete / Stage 3 start”) instead of the full confirmed decision set.
2. The verification checked whether stale current-state words disappeared, not whether every confirmed decision was represented.
3. SPEC_TRACEABILITY rows marked items “reflected” without requiring semantic comparison.
4. Stage completion and roadmap-change propagation were treated as separate work even though the governance rules require one synchronized change.
5. The previous incident controls focused on PR/branch/current-state errors but did not enforce a conversation-decision inventory.

## 4. Confirmed V1 decisions used as audit baseline

| ID/source | Confirmed decision |
|---|---|
| V-01 | Final target is a self-improving, domain-adaptive general-purpose orchestrator. App development is an initial validation domain, not the final scope. |
| V-01 | Separate general core, domain packs, tool connectors, and domain-specific evaluation packs. |
| V-02 | 14 development hours/week, about 56 hours in month one. |
| V-02 | API cap JPY 10,000; warning 7,000; restrict high-performance models 9,000; stop and require approval at 10,000. |
| V-02 | First improve Raphael's own code/design, then build a small new app. |
| V-03 | Private branch work, tests, reviews, PRs, and completed non-public drafts can proceed without case-by-case approval. |
| V-03 | External publication/sending/submission, production/main, payment, sensitive access expansion, permission/safety/core changes require approval. |
| V-04 | ChatGPT is the sole formal approval channel at the current phase. |
| P-02 | Confirmed decisions must be integrated before continuing; Stage 2 cannot be skipped because a later V1 roadmap exists. |
| M/T/C/I/D | Stage 2 memory, trust, authority, emergency stop, important-change, proxy-decision, trial, evaluation, retirement, archive, and handoff decisions remain confirmed. |

## 5. Files audited and findings

| File | Finding before correction | Action on this branch |
|---|---|---|
| ROADMAP.md | Old Stage 3 “requirements agent” through Stage 5 sequence; V1 absent | Replaced with Week 0〜4 V1 execution roadmap |
| README.md | Reported Stage 3 start; no V1 resource/order summary | Updated current state and V1 router summary |
| PROJECT_HANDOFF.md | Directed new sessions to obsolete Stage 3 | Rewritten to V1 Week 0 and audit branch |
| MASTER_SPEC.md | Stage 2 governance present; V1 V-01〜V-04 absent | Added complete V1 section |
| SPEC_TRACEABILITY.md | Claimed PR #6 pending and evaluation weights/log storage unresolved | Corrected state; added V1 mappings and semantic gate |
| VISION.md | General orchestra vision but app-as-validation/general-purpose V1 not explicit | Added V1 final direction |
| STAGE2_DECISION_LOG.md | Correct V1 decisions existed, but branch/revision status stale | Preserved decisions; updated status |
| RAPHAEL_INITIAL_DESIGN.md | Evaluation log and weight shown unresolved though implemented | Corrected to “implemented, formal approval unresolved” |
| NEXT_SESSION_PROMPT.md | Directed work to merged Stage 2 branch | Replaced with current audit/V1 instructions |
| INCIDENT_LOG.md | Older evaluation-governance incident only | Kept unresolved; this incident recorded separately |
| AGENT_STANDARD.md | Stage 2 lifecycle rules present | No semantic change required |
| GOVERNANCE.md | General sync gate present but no decision-inventory proof | Strengthened through this audit's completeness controls |
| SECURITY.md | No V1-specific contradiction found | No change required |
| USER.md | Automatic-affirmation prohibition and critical-evaluation detail were incomplete | Added evidence, counterexample, uncertainty, and prohibited-phrase rules |
| RECONSIDER.md | Ciel and technical items remain conditional | No change required; evaluation approval remains unresolved |
| RAPHAEL_TEST_PLAN.md | Weights/log structure implemented | Kept; formal approval remains unresolved in INCIDENT_LOG |
| agents/raphael.md | Followed README but did not state the critical-evaluation rule | Added STARTUP_CONTEXT loading and evidence-based evaluation rule |

## 6. Additional omissions found

1. SPEC_TRACEABILITY still said Draft PR #6 was not merged.
2. SPEC_TRACEABILITY still called official evaluation log storage and scoring weights unresolved.
3. RAPHAEL_INITIAL_DESIGN still listed evaluation log storage and scoring weights as unresolved.
4. NEXT_SESSION_PROMPT still pointed to `stage2/agent-governance` and obsolete Stage 2 next actions.
5. STAGE2_DECISION_LOG still identified the merged Stage 2 branch as the active branch.
6. README, PROJECT_HANDOFF, MASTER_SPEC, and VISION did not expose V-01〜V-04 adequately.

## 7. Items deliberately not changed to “approved”

The eleven evaluation commits described in INCIDENT_LOG are implemented but their formal approval status remains unresolved. This audit does not ratify:

- scoring weights and mandatory thresholds;
- correction-round definition;
- preference-change exclusion;
- 90-point reproducibility auxiliary threshold;
- related official evaluation-record changes.

## 8. New completeness gate

A roadmap or Stage/Week change is complete only when:

1. A decision inventory is created from the user-confirmed conversation and decision logs.
2. Each decision has required destinations.
3. ROADMAP, README, PROJECT_HANDOFF, MASTER_SPEC, SPEC_TRACEABILITY, VISION, RECONSIDER, relevant agent specs, tests, and incidents are checked.
4. “Reflected” means purpose, scope, conditions, sequence, authority, and approval state agree—not merely shared keywords.
5. Old branch, PR, Stage, and unresolved-state statements are searched across all canonical files.
6. Unapproved items remain visibly unapproved.
7. A second pass reads from README as a fresh session would and verifies the correct next action.
8. Completion is not reported until the audit table has zero unexplained gaps.

## 9. Validation status

- Dedicated branch created from main.
- Main not modified.
- V1 roadmap and primary canonical propagation completed on this branch.
- Known stale-state findings corrected.
- Final branch-to-main diff reviewed; fresh-session reconstruction and similar-case retest passed. Compare reports the branch 0 behind main with main as merge base. The PR mergeable flag returned both true and false across successive connector reads after updates, so mergeability must be rechecked immediately before merge.


## Additional audit: mandatory startup sharing

### Gap

The repository had an entry router, but no single startup contract that classified long-term memory, decisions, prohibitions, required procedures, approval boundaries, incidents, and other information that changes downstream AI judgment. Model-specific entry files could therefore reach only part of the required context.

### Remediation

- Added `STARTUP_CONTEXT.md`.
- Routed README, AGENTS, Claude, Gemini, Copilot, and GitHub Raphael through it.
- Synchronized USER, GOVERNANCE, OPERATING_GUIDE, MASTER_SPEC, SPEC_TRACEABILITY, and PROJECT_HANDOFF.
- Added the rule that Ryunosuke's claims and instructions are evaluated critically rather than automatically affirmed.
- Corrected OPERATING_GUIDE's stale Stage 2 state to V1 Week 0 / PR #10 audit state.

### Closure gate

Do not mark the audit complete until entry reachability, stale-language search, fresh-session recovery, a similar-but-not-identical case, PR diff, and mergeability have been checked.


## Startup-context validation results

- Entry reachability: PASS for README, AGENTS, CLAUDE, GEMINI, Copilot instructions, GitHub Raphael, and NEXT_SESSION_PROMPT.
- Canonical propagation: PASS for STARTUP_CONTEXT, GOVERNANCE, OPERATING_GUIDE, USER, MASTER_SPEC, SPEC_TRACEABILITY, PROJECT_HANDOFF, and agents/raphael.
- Stale current-state string: no active statement that Stage 2 is the current operating stage.
- Similar-but-not-identical retest:
  - New AI entry with README + STARTUP_CONTEXT: PASS.
  - New AI entry with README only: correctly rejected as incomplete.
  - New AI entry relying on conversation memory only: correctly rejected as incomplete.
- Complete PR diff reviewed. Branch ancestry is clean (0 behind main), but the connector's PR mergeable flag fluctuated after updates; recheck it immediately before merge. Remaining closure conditions: Ryunosuke's review, merge decision, and post-merge verification.
