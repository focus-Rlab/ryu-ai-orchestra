# Mistake Prevention Controls

Status: Required before the next AURA revision starts.
Date: 2026-08-05
Owner: Raphael / Codex

## Purpose

This file converts the Week 4 AURA conversation review into action-blocking controls. The goal is not to preserve a nicer summary. The goal is to stop a later worker before it repeats the same type of mistake.

AURA application fixes are intentionally paused until these controls are reviewed and merged.

## Core Principle

The failure is not only that individual visible mistakes happened. The deeper failure is that a rule, review point, or user preference can be written down, read, and still not affect the next action.

Therefore every future action gate must answer three questions before work starts:

1. What known failure patterns were reviewed for this action?
2. For each applicable rule, what failure mode could happen if the rule is only read but not applied?
3. What concrete action check blocks that failure before implementation, explanation, delivery, or completion?

## Named Canonical Domains

The 8 broad rule categories are not enough by themselves. A later worker could satisfy those categories while still missing a specific important rule area. Every action-gate v2 record must therefore include `canonical_rule_domain_coverage` for all named domains below, each marked `applicable` or `not_applicable` with a reason.

If a domain is applicable, the record must include the source, failure mode, and action check.

Required domains:

- `security`: secrets, private data, file integrity, unsafe operations, and permission boundaries.
- `ryunosuke_evaluation_method`: Ryunosuke's personal acceptance, objective checks, explanation quality, correction burden, and subjective usefulness.
- `raphael_behavior_code`: Raphael's identity, role, action norms, response style, and responsibility boundaries.
- `approval_authority`: what Ryunosuke has approved, what is only proposed, and what cannot be decided by AI or GitHub alone.
- `user_communication`: plain-language explanation, jargon handling, and understanding checks.
- `delivery_acceptance`: internal validation, public access, user access evidence, and Ryunosuke acceptance as separate states.
- `feedback_interpretation`: surface examples, underlying issue, interpretation risk, and prevention controls.
- `mistake_recovery`: classification, impact, root cause, recurrence prevention, and incident records.
- `agent_design`: whether existing agents are enough, whether temporary help is needed, or whether a new agent/skill is justified.
- `state_sync`: current branch, PR, issue, next action, and project digest consistency.
- `quality_validation`: tests, failure tests, independent review, and unverified scope.
- `cost_and_tool_authority`: paid tools, tool availability, alternate paths, and authority to execute.

## Control Map

| Failure pattern | Required control | Blocking check |
| --- | --- | --- |
| Rules were read but not applied at the action boundary. | Every applicable rule category must include `failure_mode` and `action_check`, not only `reason`, `control`, and `evidence`. | `scripts/check_action_gate.py` rejects applicable rule coverage without both fields. |
| Future workers may miss a written rule that has not yet produced an obvious visible error. | Every action-gate v2 record must include `preflight_failure_review` with reviewed sources, known failure patterns, and risk-to-action controls. | The gate rejects missing or empty preflight failure review fields. |
| Specific important rule areas are hidden inside broad categories. | Every action-gate v2 record must include all named canonical domains such as security, Ryunosuke evaluation method, Raphael behavior code, and approval authority. | The gate rejects missing canonical domains and applicable domains without source, failure mode, or action check. |
| User-facing explanations were hard to understand, including unexplained PR/branch/gate/status language. | When `user_communication` applies, preflight must include a communication plan for Ryunosuke and future workers. | The gate rejects missing audience, plain-language summary, jargon list, or understanding check. |
| Improvement scope was narrowed to recent visible examples such as security or beginner explanation. | The preflight review must list known failure patterns and map each risk to a prevention control. | The gate rejects empty risk-to-action controls. |
| One failed path was treated as the whole task being impossible. | Impossibility claims must inventory requested tool, configured connector, API, local VCS, browser, and manual handoff paths. | The gate rejects incomplete path inventories and rejects an impossibility claim when an authorized equivalent path is available. |
| Internal test completion and user acceptance were mixed. | Deliverables that need handoff must separately record internal validation, user access evidence, and user acceptance. | Completion claims for deliverables fail unless internal validation and user acceptance are both `passed`. |
| Screenshots, URLs, or app links were assumed to be reachable by Ryunosuke. | Handoff records must state the medium and acceptance check, and final completion must include user-access evidence. | The gate rejects completion claims without user-access evidence. |
| Feedback was recorded as labels instead of concrete successes, failures, and evidence. | Reviewed feedback must include positive patterns, failures or gaps, and source evidence. | The gate rejects empty feedback detail fields. |
| Surface examples were corrected while the underlying issue was missed. | Reviewed feedback must identify `underlying_issue`, `surface_examples`, `interpretation_risk`, and `prevention_controls`. | The gate rejects reviewed feedback without those fields. |
| Agent use or non-use was decided but not recorded. | Assignment decisions must state whether agents are used, why, and execution evidence when they are used. | The gate rejects missing assignment rationale or execution evidence. |
| File corruption was not caught before a passing report. | Repository text files must be checked for UTF-8 readability. | `tests/test_repository_text_encoding.py` covers repository text encoding. |
| Unauthorized repair changed content before approval. | Mistake responses must run full incident steps, including approval boundary and canonical updates. | Mistake actions fail without all incident steps and evidence. |
| Visual artifacts passed internal checks but did not match Ryunosuke's ideal. | AURA revision cannot start until visual ideal sharing is planned before UI code changes. | This file and `PROJECT_STATE.json` keep AURA app repair paused until this prevention PR is merged. |
| Continued-use needs were not predicted during design. | AURA revision must include continued-use behavior prediction before feature implementation. | The next AURA plan must include this before app repair starts. |

## Feedback Interpretation Rule

When Ryunosuke gives examples such as "name change/delete", "character/aura", "overall", "various", or "for example", the worker must not turn those words directly into a narrow checklist.

Before implementation, extract and record:

1. Surface examples: the literal examples that appeared in the conversation.
2. Underlying issue: the broader failure pattern or user judgment criterion.
3. Interpretation risk: how a later worker could misunderstand the examples.
4. Prevention controls: what will stop that misunderstanding before code changes begin.

For the AURA acceptance result, the underlying issues are:

- Visual ideal, worldview, character quality, aura quality, and daily-use appeal were not sufficiently shared or structured before implementation.
- Continued-use user behavior was not predicted during design.
- Feedback interpretation itself failed when Codex tried to fix the named examples instead of the failure pattern.

## Plain-Language Explanation Rule

If the work involves reporting status, explaining a PR, describing checks, or handing off a result, `user_communication` is applicable.

The worker must prepare a communication plan that says:

- who the explanation is for;
- what will be explained in ordinary language;
- which jargon terms must be explained or avoided;
- how the answer will make the next practical action clear.

This prevents the failure where a rule about beginner-friendly explanation exists but the worker still replies with terms such as PR, branch, gate, check, or acceptance without enough context.

## Before AURA Revision Can Start

The next AURA app repair must not start until all of the following are true:

- This prevention-control change is merged.
- The action gate passes with all named canonical domains reviewed, including security, Ryunosuke evaluation method, Raphael behavior code, approval authority, and user communication.
- The action gate passes with feedback fields that preserve the underlying issue, not only example labels.
- The action gate passes with preflight failure review fields that map known written rules to action checks.
- The next implementation plan includes a visual ideal sharing step before UI changes.
- The next implementation plan includes continued-use behavior prediction before feature changes.
- The next completion claim separates internal validation, public URL access, and Ryunosuke's user acceptance.

## Notes On Agent Decisions

The Week 4 review said it was good that the AURA task did not add a new agent. That was only true for that case. It is not a standing rule to avoid adding agents.

For future work, decide per task whether existing agents are enough, whether a temporary role is needed, or whether a new persistent agent or skill is justified. Record the reason either way.
