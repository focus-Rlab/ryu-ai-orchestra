# Mistake Prevention Controls

Status: Required before the next AURA revision starts.
Date: 2026-08-05
Owner: Raphael / Codex

## Purpose

This file converts the Week 4 AURA conversation review into action-blocking controls. The goal is not to preserve a nicer summary. The goal is to stop a later worker before it repeats the same type of mistake.

AURA application fixes are intentionally paused until these controls are reviewed and merged.

## Control Map

| Failure pattern | Required control | Blocking check |
| --- | --- | --- |
| Rules were read but not applied at the action boundary. | Every action-gate v2 record must cover all 8 rule categories: security, authority, quality, user communication, state sync, delivery, recovery, and agent design. | `scripts/check_action_gate.py` rejects missing categories. |
| One failed path was treated as the whole task being impossible. | Impossibility claims must inventory requested tool, configured connector, API, local VCS, browser, and manual handoff paths. | The gate rejects incomplete path inventories and rejects an impossibility claim when an authorized equivalent path is available. |
| Internal test completion and user acceptance were mixed. | Deliverables that need handoff must separately record internal validation, user access evidence, and user acceptance. | Completion claims for deliverables fail unless internal validation and user acceptance are both `passed`. |
| User-facing explanations were hard to understand. | Required deliverable handoff must include a plain-language summary. | The gate rejects required handoff without `plain_language_summary`. |
| Screenshots, URLs, or app links were assumed to be reachable by Ryunosuke. | Handoff records must state the medium and acceptance check, and final completion must include user-access evidence. | The gate rejects completion claims without user-access evidence. |
| Feedback was recorded as labels instead of concrete successes, failures, and evidence. | Reviewed feedback must include positive patterns, failures or gaps, and source evidence. | The gate rejects empty feedback detail fields. |
| Surface examples were corrected while the underlying issue was missed. | Reviewed feedback must identify `underlying_issue`, `surface_examples`, `interpretation_risk`, and `prevention_controls`. | The gate rejects reviewed feedback without those fields. |
| Agent use or non-use was decided but not recorded. | Assignment decisions must state whether agents are used, why, and execution evidence when they are used. | The gate rejects missing assignment rationale or execution evidence. |
| File corruption was not caught before a passing report. | Repository text files must be checked for UTF-8 readability. | `tests/test_repository_text_encoding.py` covers repository text encoding. |
| Unauthorized repair changed content before approval. | Mistake responses must run full incident steps, including approval boundary and canonical updates. | Mistake actions fail without all incident steps and evidence. |

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

## Before AURA Revision Can Start

The next AURA app repair must not start until all of the following are true:

- This prevention-control change is merged.
- The action gate passes with feedback fields that preserve the underlying issue, not only example labels.
- The next implementation plan includes a visual ideal sharing step before UI changes.
- The next implementation plan includes continued-use behavior prediction before feature changes.
- The next completion claim separates internal validation, public URL access, and Ryunosuke's user acceptance.

## Notes On Agent Decisions

The Week 4 review said it was good that the AURA task did not add a new agent. That was only true for that case. It is not a standing rule to avoid adding agents.

For future work, decide per task whether existing agents are enough, whether a temporary role is needed, or whether a new persistent agent or skill is justified. Record the reason either way.
