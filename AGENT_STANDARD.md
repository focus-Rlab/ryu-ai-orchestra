# Agent Standard

Version: 0.2.0-draft  
Status: Stage 2 Draft Standard  
Owner: Ryunosuke Matsumoto  
Applies to: All specialist agents, test agents, and future agent candidates in `ryu-ai-orchestra`

## 1. Purpose

This document defines the minimum design standard required before any specialist agent can be proposed, tested, approved, adopted, changed, split, merged, suspended, or retired.

The goal is to prevent vague agents, duplicated responsibilities, excessive autonomy, unclear handoffs, and tool/model confusion.

Raphael remains the top-level orchestrating agent. A specialist agent exists only when separating the work improves quality, speed, safety, repeatability, or scalability enough to justify the added complexity.

## 2. Core principles

Every agent must follow these principles.

1. **Purpose before existence**: no agent is created only because the role sounds useful.
2. **Responsibility before model**: define the organizational role first, then choose the AI model or execution environment.
3. **Single accountable owner**: every deliverable has one integration owner.
4. **Minimum necessary authority**: grant only the tools and permissions required for the defined scope.
5. **Explicit boundaries**: state what the agent does and does not do.
6. **Auditable decisions**: important outputs must show sources, assumptions, unresolved points, and approval status.
7. **Reversible by default**: test in isolation before permanent adoption where possible.
8. **Human approval for high-impact changes**: Ryunosuke approves permanent adoption, major authority changes, splitting, merging, suspension, and retirement.
9. **No false execution claims**: tool or permission failures must be reported immediately.
10. **Execute first when safe and authorized**: do not repeat planning when the requested work can be completed without further approval.

## 3. Agent versus AI model or execution environment

An **agent** is an organizational work unit with a defined purpose, responsibility, inputs, outputs, authority, completion conditions, and evaluation criteria.

An **AI model or execution environment** is a tool used by an agent, such as ChatGPT, Claude, Codex, Gemini, Claude Code, GitHub Copilot, or a GitHub-connected environment.

The selection order is:

1. define the work;
2. select the responsible agent;
3. define authority and acceptance criteria;
4. select the model, tools, and environment.

A model name must not be used as a substitute for an agent role.

## 4. Required agent definition

Every proposed agent must include all fields below. A field may be marked `Not applicable`, but it must not be omitted.

### 4.1 Identity

- **Agent name**
- **Agent ID**
- **Version**
- **Status**: proposed / sandbox / pilot / active / suspended / retired
- **Owner**
- **Integration owner**
- **Created date**
- **Last reviewed date**

### 4.2 Purpose and justification

- **One-sentence purpose**
- **Problem being solved**
- **Why Raphael alone should not retain the work**
- **Expected benefit**
- **Expected cost and complexity**
- **Evidence or hypothesis supporting separation**
- **Conditions under which the agent should not be created**

### 4.3 Scope

- **In scope**
- **Out of scope**
- **Primary responsibility**
- **Secondary responsibilities**
- **Prohibited actions**
- **Relevant life or project domains**
- **Time horizon**: short / mid / long / cross-horizon

### 4.4 Inputs

For each input:

- name;
- source;
- required or optional;
- format;
- freshness requirement;
- validation rule;
- sensitivity level;
- fallback when missing.

### 4.5 Outputs

For each output:

- name;
- recipient;
- format;
- required content;
- quality criteria;
- storage location;
- approval requirement;
- completion condition.

### 4.6 Decision authority

Each decision type must be assigned one of these levels:

- **L0 — Observe**: read, analyze, and recommend only.
- **L1 — Draft**: create drafts or sandbox artifacts without external effect.
- **L2 — Reversible execute**: perform low-risk, reversible actions within explicit rules.
- **L3 — Conditional execute**: perform defined higher-impact actions only when pre-approved conditions are met.
- **L4 — Human approval required**: propose only; Ryunosuke must approve each execution.

The agent definition must list:

- decisions it may make independently;
- decisions requiring Raphael review;
- decisions requiring Ryunosuke approval;
- emergency stop conditions;
- actions that are always prohibited.

### 4.7 Tools, data, and permissions

For every tool or data source:

- tool or source name;
- purpose;
- read permission;
- write permission;
- external side effects;
- authentication dependency;
- failure behavior;
- minimum necessary access;
- logging or evidence requirement.

The agent must verify connectivity and write capability before claiming execution has started.

### 4.8 Model and environment policy

Define:

- preferred model or environment;
- acceptable alternatives;
- selection criteria;
- tasks that require a specific environment;
- privacy or security constraints;
- cost or latency constraints;
- fallback when the preferred environment is unavailable.

The model choice may change without changing the agent's organizational identity, unless the change affects capability, risk, or authority.

### 4.9 Workflow

The workflow must define:

1. trigger;
2. intake and validation;
3. ambiguity handling;
4. task decomposition;
5. execution;
6. self-check;
7. handoff;
8. review;
9. approval;
10. storage and state synchronization;
11. closure;
12. failure and recovery.

### 4.10 Handoffs and collaboration

For every regular handoff:

- sender;
- receiver;
- trigger;
- required payload;
- expected response;
- deadline or service expectation;
- escalation path;
- ownership after handoff.

An agent must not assume that transferring information transfers accountability. The integration owner remains accountable until the deliverable is accepted.

### 4.11 Quality and acceptance criteria

Define measurable criteria where possible:

- correctness;
- completeness;
- traceability;
- timeliness;
- consistency;
- security;
- user usefulness;
- rework rate;
- failure rate.

When numerical targets are not appropriate, define:

- pass example;
- fail example;
- mandatory conditions;
- preferred conditions;
- verification method.

### 4.12 Failure handling

Define:

- known failure modes;
- detection method;
- immediate containment;
- user notification rule;
- retry rule;
- rollback rule;
- escalation path;
- root-cause analysis requirement;
- cross-document or cross-system audit requirement;
- prevention update.

### 4.13 Logging and records

The agent must record, when applicable:

- request;
- assumptions;
- source material;
- decisions;
- tool usage;
- generated artifacts;
- approval status;
- errors;
- unresolved risks;
- final state;
- next action.

Logs must be sufficient for another agent or session to continue without inventing missing context.

### 4.14 Security and privacy

Define:

- data classification;
- permitted storage locations;
- prohibited disclosures;
- credential handling;
- personal-data handling;
- deletion or retention rules;
- actions requiring explicit consent;
- security review triggers.

### 4.15 Lifecycle

Every agent must define entry and exit criteria for:

- proposed;
- sandbox;
- pilot;
- active;
- suspended;
- retired.

It must also define:

- review frequency;
- owner of the review;
- upgrade conditions;
- downgrade conditions;
- suspension conditions;
- retirement conditions;
- replacement or migration plan.

### 4.16 Change history

Every material change must record:

- date;
- version;
- change;
- reason;
- proposer;
- approver;
- affected documents or agents;
- migration or retest requirement.

## 5. Agent creation gate

A new agent may advance from `proposed` to `sandbox` only when all conditions below are satisfied.

- The problem and expected benefit are clear.
- The responsibility cannot be handled more simply by improving Raphael, a skill, a workflow, or an existing agent.
- In-scope and out-of-scope boundaries are explicit.
- Responsibility overlap has been audited.
- Inputs, outputs, authority, tools, and acceptance criteria are defined.
- Risks and failure handling are defined.
- A sandbox test plan exists.
- The change is reversible.

A new agent may advance to `active` only when:

- sandbox and pilot criteria pass;
- responsibility ownership is unambiguous;
- handoffs work in practice;
- measured benefit justifies complexity;
- unresolved high-risk failures are absent;
- required documentation is synchronized;
- Ryunosuke approves permanent adoption.

## 6. When not to create a new agent

Do not create a new agent when the need can be met by:

- adding or improving a skill;
- changing a prompt or checklist;
- improving Raphael's existing workflow;
- using a temporary task role;
- changing the model or execution environment;
- adding a validation step;
- improving a data source or integration;
- clarifying ownership in an existing agent.

A narrow recurring function does not automatically justify a separate agent.

## 7. Responsibility overlap check

Before approval, compare the candidate agent against Raphael and all existing agents.

For each responsibility classify the relationship as:

- **Unique**: no existing owner.
- **Delegated**: Raphael owns the outcome; the agent performs a defined part.
- **Shared with boundary**: both act, but conditions are explicit.
- **Duplicate**: two agents own the same outcome without a clear boundary.
- **Gap**: required work has no owner.

`Duplicate` and `Gap` findings must be resolved before activation.

## 8. Minimum agent file template

Each permanent agent should have a canonical file using this structure:

```markdown
# <Agent Name>

Version:
Status:
Owner:
Integration owner:

## Purpose
## Justification
## In scope
## Out of scope
## Inputs
## Outputs
## Decision authority
## Tools and permissions
## Model and environment policy
## Workflow
## Handoffs
## Quality and acceptance criteria
## Failure handling
## Logging
## Security and privacy
## Lifecycle
## Open questions
## Change history
```

## 9. Required review questions

Before approval, the reviewer must answer:

1. What exact problem does this agent solve?
2. Why is a new agent better than a skill, workflow, or Raphael improvement?
3. Who owns the final outcome?
4. Where does its authority begin and end?
5. What existing responsibility could overlap?
6. What happens when inputs are missing or stale?
7. What can the agent change without approval?
8. What actions have external side effects?
9. How will success be measured?
10. What evidence would justify suspension or retirement?
11. Can another session understand and operate it from the canonical documents alone?
12. Has every affected canonical document been synchronized?

## 10. Confirmed Stage 2 operating architecture

This standard now incorporates the following confirmed architecture. Detailed decision rationale and unresolved parameters remain in `STAGE2_DECISION_LOG.md`.

### 10.1 Organizational model

- An agent is a persistent accountable organizational actor.
- It executes through a changing combination of skills, workflows, tools, data, models, and environments.
- Human-like qualities are used only when they improve professional judgment, critique, collaboration, responsibility, or continuity.
- Raphael assigns work by default; the organization does not hold a permanent all-agent meeting.

### 10.2 Discussion, objection, and stopping

- Agents may proactively propose improvements, corrections, alternatives, contradictions, and risks.
- A normal improvement proposal does not stop assigned work.
- Relevant agents discuss an issue only when their responsibility, expertise, dependency, or affected domain makes participation useful, or Raphael requests it.
- Serious risk, fundamental contradiction, or unacceptable external impact may trigger a stop request.
- Exact severity names and mandatory-stop thresholds remain unresolved.

### 10.3 Trust and autonomy

- New agents begin under close supervision.
- Authority grows only from demonstrated reliability and may be reduced after failure or changed conditions.
- Initially, Ryunosuke approves creation, permanent adoption, important modification, authority expansion, integration, suspension, and retirement.
- Raphael may later receive bounded authority for defined low-risk categories.
- The existing L0–L4 decision-authority labels describe action types; they do not by themselves grant trust or promotion.

### 10.4 Improvement and change control

- Improvement operates at two layers: specialist self-improvement and Raphael's organization-wide improvement.
- Every change must be visible and traceable to Raphael.
- Important changes require Ryunosuke approval.
- Candidate changes must identify source, reason, affected scope, evidence, uncertainty, rollback, approval status, and observed effect.
- Unverified self-modification must not replace canonical rules or memory.

### 10.5 Memory architecture

- Memory is hierarchical and separated by purpose and sensitivity.
- Specialist agents govern their own specialist memory; Raphael governs shared organizational memory, cross-domain memory, and Ryunosuke's protected judgment history.
- Agents may broadly discover non-protected memory but retrieve only what is task-relevant and necessary.
- Agents select their own necessary retrieval; Raphael supplements missing facts, dependencies, contradictions, or risks.
- Long-term memory updates begin as candidates, are verified against the previous version, and are promoted only with required approval.
- Initial promotion to canonical long-term memory requires Ryunosuke approval. Delegation to Raphael may expand gradually and may be revoked.

### 10.6 V1 scope and authority

- Raphael targets a self-improving, domain-adaptive general-purpose orchestrator.
- Software development is an initial validation domain, not the final scope.
- The design separates general core, domain packs, tool connectors, and domain-specific evaluation packs.
- Initial development capacity is 14 hours per week.
- The initial monthly API hard cap is JPY 10,000, with controls at JPY 7,000 and JPY 9,000.
- Raphael may autonomously produce and test private work, working-branch changes, pull requests, and non-public drafts.
- External publication, sending, production or main changes, payment, sensitive access expansion, and material core-governance changes require Ryunosuke approval.
- ChatGPT is the sole formal approval channel for the current phase.

## 11. Unresolved Stage 2 parameters

Only the parameters below remain open; the confirmed architecture above must not be reopened unless Ryunosuke requests reconsideration.

1. Memory-update delegation evidence, eligible low-risk categories, review cadence, and revocation thresholds.
2. Temporary working memory versus canonical long-term memory.
3. Memory correction, deletion, forgetting, retention, storage, and canonical-source rules.
4. Trust promotion and demotion thresholds.
5. Objection severity and mandatory-stop thresholds.
6. The exact boundary of an important change.
7. Confidence requirements for Raphael proxy decisions.
8. Pilot evidence required before agent activation.
9. Performance review cadence and scoring.
10. Archive and retirement structure.

Until a parameter is decided, use the safest reversible default and do not promote that default to canonical architecture without Ryunosuke's approval.

