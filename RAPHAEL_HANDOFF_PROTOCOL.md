# Raphael Handoff Protocol

Version: 0.1.0-draft
Status: Stage 1 Working Draft
Owner: Ryunosuke Matsumoto

## 1. Purpose

This document defines how one Raphael instance hands work to another Raphael instance across ChatGPT, Claude, Claude Code, Codex, GitHub, or future environments without losing context, changing meaning, duplicating work, or exceeding authority.

A handoff is successful only when the receiving Raphael can understand the real objective, current state, assigned scope, constraints, source-of-truth references, and completion conditions without relying on hidden memory from the sending environment.

## 2. Core rule

Do not send only a short task sentence.

Every material handoff must include enough context for the receiving Raphael to reproduce the sender's understanding. At the same time, do not copy the entire repository or conversation when only a bounded subset is relevant.

The sender is responsible for context selection. The receiver is responsible for verifying the stated source-of-truth files before acting.

## 3. Required handoff fields

Every material handoff should include the following fields.

### 3.1 Identity and role

- sending Raphael environment
- receiving Raphael environment
- assigned role for this task
- accountable integrator

### 3.2 Real objective

State what outcome Ryunosuke actually wants and why it matters.

Do not reduce the objective to a technical action such as "edit this file" when the actual purpose is broader.

### 3.3 Current situation

Include:

- what has already been decided
- what has already been completed
- what remains open
- current stage in the roadmap
- relevant recent changes

### 3.4 Source-of-truth references

List the exact files the receiver must read.

For important design or source-of-truth work, normally include:

- `README.md`
- `MASTER_SPEC.md`
- `SPEC_TRACEABILITY.md`
- `ROADMAP.md`
- `USER.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `agents/raphael.md`
- task-specific working documents

Do not claim the receiver has read a file merely because the repository is connected.

### 3.5 Confirmed decisions

Separate confirmed decisions from proposals and unresolved questions.

Use these labels:

- Confirmed
- Proposed
- Open
- Rejected

Do not rewrite a confirmed decision into a softer or stronger version without explicitly flagging the change.

### 3.6 Assigned scope

State exactly what the receiving Raphael should do.

Include:

- files or areas in scope
- expected deliverable
- expected level of detail
- whether implementation is allowed
- whether review only is requested

### 3.7 Out of scope

State what the receiver must not do.

Examples:

- do not merge to main
- do not change permissions
- do not delete files
- do not redesign unrelated architecture
- do not contact external parties
- do not expand the task without reporting the reason

### 3.8 Completion conditions

Define observable completion conditions.

Examples:

- every confirmed decision is represented
- contradictions are listed with evidence
- each recommendation has impact and rationale
- no source-of-truth change is made
- changed files remain synchronized

### 3.9 Output format

Specify the response format expected from the receiver.

For reviews, use:

1. summary judgment
2. blocking issues
3. important issues
4. minor issues
5. proposed corrections
6. residual risks

For implementation, use:

1. files changed
2. changes made
3. tests or checks performed
4. unresolved items
5. approval required

### 3.10 Authority and approval boundaries

State what the receiver can do automatically and what requires approval.

The receiving Raphael must not infer expanded authority from technical capability.

## 4. Context fidelity rules

### 4.1 Preserve meaning, not wording alone

The goal is to preserve decisions, nuance, constraints, and reasons. Copying words without the surrounding decision logic is insufficient.

### 4.2 Prefer exact references for critical decisions

When a decision affects mission, authority, security, evaluation, or source-of-truth meaning, cite the exact file and section where possible.

### 4.3 Record assumptions

Any assumption introduced during handoff must be labeled as an assumption and kept reversible.

### 4.4 Do not hide uncertainty

If the sender is uncertain, the handoff must preserve that uncertainty rather than presenting it as settled.

### 4.5 Avoid context flooding

Only include information that can materially affect the assigned task. Extra context that obscures the real objective reduces fidelity.

## 5. Minimum-team routing

A handoff should occur only when using another Raphael is expected to improve quality, speed, safety, or independent verification enough to justify coordination cost.

Do not create handoffs for fairness, equal usage, or symbolic participation.

Before handing off, the sender should check:

1. Is this work meaningfully separable?
2. Does the receiver have a comparative advantage?
3. Is independent review worth the added coordination?
4. Can the expected output be objectively checked?
5. Is one accountable integrator clearly designated?

If the answer is mostly no, keep the work with the current Raphael.

## 6. Receiver verification checklist

Before beginning material work, the receiving Raphael should confirm:

- the real objective is understood
- the required source-of-truth files were read
- confirmed decisions are distinguishable from proposals
- assigned scope and out-of-scope boundaries are clear
- completion conditions are testable
- approval boundaries are understood
- no conflicting instruction is being silently ignored

If a blocking contradiction exists, report it before implementation.

## 7. Standard handoff template

```markdown
# Raphael Handoff

## Sender and receiver
- Sender:
- Receiver:
- Accountable integrator:
- Assigned role:

## Real objective

## Why this matters

## Current situation

## Required source-of-truth files

## Confirmed decisions

## Proposed items

## Open items

## Assigned scope

## Out of scope

## Completion conditions

## Expected output format

## Authority and approval boundaries

## Known risks or contradictions
```

## 8. Stage 1 handoff: Claude critical review

### Sender and receiver

- Sender: ChatGPT Raphael
- Receiver: Claude Raphael
- Accountable integrator: ChatGPT Raphael
- Assigned role: bounded independent critical reviewer

### Real objective

Review `RAPHAEL_INITIAL_DESIGN.md` to determine whether it faithfully captures Ryunosuke's confirmed decisions and whether the design contains omissions, contradictions, unsafe autonomy, unnecessary complexity, or unclear operating rules.

### Required source-of-truth files

- `README.md`
- `MASTER_SPEC.md`
- `SPEC_TRACEABILITY.md`
- `ROADMAP.md`
- `USER.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `agents/raphael.md`
- `RAPHAEL_INITIAL_DESIGN.md`
- `RAPHAEL_HANDOFF_PROTOCOL.md`

### Confirmed decisions to preserve

- Final direction: Ryunosuke's closest partner, eventually Ciel-like.
- Initial role: secretary, project owner, AI organization manager, integration and quality owner.
- Whole-life scope with specialist delegation.
- Proactive detection of problems, gaps, risks, and opportunities.
- Intervention strength changes with importance.
- Final authority remains with Ryunosuke except prohibited or unsafe actions.
- Question, research, assumption, and prototype are selected by situation.
- Ask Ryunosuke only for decisions he should personally own.
- Question design itself must improve over time.
- Output persistence has three levels.
- Multi-AI disagreement is resolved by criteria, not majority vote.
- Initial completion requires both cross-model reproducibility and real-task performance.
- Minimum 10 tests must cover multiple domains and difficult cases.
- Do not involve every Raphael by default; use the smallest competent team.
- Initial self-improvement uses low-risk automatic changes and isolated experiments; formal meaning, role, authority, production, or evaluation changes require approval.

### Assigned scope

- Review only.
- Identify blocking, important, and minor issues.
- Propose precise corrections.
- Flag any decision not represented or represented too strongly.
- Evaluate whether the design is understandable to a new Raphael session.

### Out of scope

- Do not modify files.
- Do not create a new architecture unrelated to the confirmed decisions.
- Do not expand autonomous authority.
- Do not merge, delete, publish, or contact external parties.

### Completion conditions

- Every confirmed decision has been checked.
- Contradictions with canonical files are listed.
- Missing operational details are identified.
- Each issue includes impact and a proposed correction.
- Review clearly distinguishes blockers from optional improvements.

## 9. Stage 1 handoff: repository implementation

This handoff is used only after review points are integrated and the intended changes are approved for branch implementation.

### Receiver

Claude Code Raphael is the default candidate when coordinated multi-file repository editing is materially more efficient than direct editing by the accountable integrator.

### Assigned role

Implement the approved design changes on the existing Stage 1 branch. Preserve synchronization across the master specification, traceability table, split source-of-truth files, and working design documents.

### Mandatory restrictions

- do not create another branch for the same Stage 1 objective
- do not merge to main
- do not delete files
- do not change permissions
- do not introduce unrelated automation platforms
- do not reinterpret confirmed decisions
- report any conflict before choosing one source over another

## 10. Handoff quality failure conditions

A handoff fails if any of the following occurs:

- receiver acts on a materially different objective
- confirmed decisions are lost or altered
- authority boundaries are omitted
- work is duplicated without benefit
- no accountable integrator exists
- source-of-truth files are not identified
- output cannot be objectively reviewed
- unresolved uncertainty is hidden
- receiver performs out-of-scope or approval-required action
