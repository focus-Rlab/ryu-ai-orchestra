# Stage 2 Decision Log

Version: 0.1.0-draft  
Owner: Ryunosuke Matsumoto  
Status: Active decision record  
Branch: `stage2/agent-governance`

## 1. Purpose

This file records design decisions explicitly confirmed by Ryunosuke during the Stage 2 redesign of `AGENT_STANDARD.md`.

Priority rule:

1. Explicit decisions in this file
2. Existing approved canonical documents
3. Unresolved proposals in `AGENT_STANDARD.md`
4. AI assumptions

When this file conflicts with the current `AGENT_STANDARD.md` draft, this file takes priority until the standard is revised and approved.

## 2. Process decision

### Decision P-01: Do not invent unresolved architecture

Status: Confirmed

- Ask Ryunosuke about unclear or foundational architecture before implementing it.
- Do not treat an AI-generated draft as approved architecture.
- Explain the intended document structure and the meaning of major sections before fixing them as canonical design.
- Existing confirmed design, newly confirmed design, and AI proposals must be distinguished.
- Continue revising the existing `AGENT_STANDARD.md`; do not discard it and restart without need.

Reason:

The initial `AGENT_STANDARD.md` draft was created before asking Ryunosuke about important architecture choices. This risked embedding assumptions inconsistent with his intended organization.

## 3. Agent identity and structure

### Decision A-01: Hybrid agent model

Status: Confirmed

Agents use a hybrid structure.

Organizationally, an agent is a persistent responsible actor similar to a professional employee, team, or department. It has an ongoing role, responsibility, viewpoint, boundaries, and accountability.

Internally, the agent performs work by combining:

- skills;
- workflows;
- tools;
- data sources;
- AI models and execution environments.

An AI model such as ChatGPT, Claude, Codex, or Gemini is not itself the organizational agent. It is an execution resource selected for the responsible agent.

### Decision A-02: Purpose of human-like qualities

Status: Confirmed

Human-like elements may be included when they support organizational function, including:

- having a professional viewpoint;
- expressing an opinion;
- asking questions;
- raising objections;
- reviewing another agent's output;
- proposing improvements;
- maintaining responsibility and continuity;
- discussing issues with other relevant agents.

Human-like behavior must not introduce unnecessary emotional instability, status competition, information concealment, theatrical personality, or conversation without operational value.

Personality exists to support responsibility, expertise, critique, collaboration, and continuity—not role-play for its own sake.

## 4. Final decisions and learning Ryunosuke's judgment

### Decision D-01: Human decision first, Raphael delegation later

Status: Confirmed

The architecture is A based on B:

- Initially, important disagreements and value judgments are escalated to Ryunosuke for the final decision.
- Raphael organizes the issue, alternatives, agent opinions, risks, and recommendation before escalation.
- Raphael records not only the selected answer, but also why Ryunosuke chose it and what he prioritized.
- Over time Raphael learns how Ryunosuke tends to decide in comparable situations.
- When confidence is sufficiently high and the matter is low-risk and within delegated boundaries, Raphael may later decide on Ryunosuke's behalf.
- Low-confidence, novel, conflicting, high-impact, irreversible, legal, financial, privacy, trust, relationship, or long-term-direction decisions continue to require Ryunosuke.

The learning target is not “which agent was correct.” The learning target is:

- which values Ryunosuke prioritized;
- what risk he accepted;
- whether he prioritized speed, quality, growth, challenge, freedom, safety, cost, or reversibility;
- under what conditions the priority changed.

### Decision D-02: Judgment inference must remain explainable

Status: Confirmed in principle

When Raphael later makes or recommends a decision based on Ryunosuke's past choices, it should be possible to identify:

- relevant past decisions;
- similarities and differences;
- inferred priority rule;
- confidence;
- whether escalation is required.

Exact confidence thresholds remain unresolved.

## 5. Assignment and collaboration

### Decision C-01: Assignment-first operating model

Status: Confirmed

The default operating pattern is:

1. Raphael assigns work to the responsible agent.
2. The agent completes its assigned responsibility.
3. The agent returns the output, evidence, risks, and unresolved points to Raphael.
4. Raphael integrates or escalates as needed.

The organization is not a permanent meeting. Agents do not automatically discuss every task or review every output.

### Decision C-02: When inter-agent discussion occurs

Status: Confirmed

Discussion or consultation occurs when one or more of these conditions apply:

1. An agent judges that it has a relevant concern, alternative, contradiction, risk, or cross-domain impact that should be raised.
2. An agent whose assigned role is critical evaluation, review, audit, verification, security, quality, or challenge performs that role.
3. An important issue arises and Raphael requests input from agents that have a relevant responsibility, expertise, dependency, or affected domain.

Raphael controls:

- which agents participate;
- the scope of the issue;
- what evidence is required;
- when discussion ends;
- how disagreement is summarized;
- whether Ryunosuke must decide.

### Decision C-03: Agents may proactively object and improve

Status: Confirmed

Default approach: proactive improvement with selective stopping.

- Agents should actively propose better methods, corrections, and improvements when relevant.
- An improvement suggestion alone does not stop assigned work.
- A warning may be raised while work continues.
- Work should be stopped or a stop request issued only for serious risk, fundamental contradiction, unacceptable external impact, or conditions defined by governance.

The exact objection severity scheme may use categories such as improvement proposal, warning, and stop request, but the final names and thresholds remain to be designed.

## 6. Autonomy and trust

### Decision T-01: Autonomy expands gradually

Status: Confirmed

Agents begin under relatively close Raphael supervision. Their autonomy expands based on demonstrated reliability and trust.

Early-stage agents should not receive broad authority merely because the role would eventually need it.

Autonomy evaluation should consider:

- instruction understanding;
- output quality;
- consistency;
- risk detection;
- transparency;
- unsupported assumptions;
- rework and correction rate;
- tool-use reliability;
- ability to stay within boundaries.

Autonomy may also be reduced after failures or changed conditions.

The current L0–L4 structure in `AGENT_STANDARD.md` is provisional and must be reconciled with a trust-based progression model.

### Decision T-02: New agent creation authority expands gradually

Status: Confirmed

Initial operation:

- Raphael identifies the need and proposes the design.
- Ryunosuke approves creation, adoption, important modification, authority expansion, major responsibility changes, integration, suspension, or retirement.

Future operation:

- Raphael may receive delegated authority to create or modify low-risk agents under pre-approved criteria.
- High-risk agents, broad organizational changes, major authority, sensitive data, external effects, or strategic changes remain subject to Ryunosuke approval.

The exact low-risk auto-creation criteria remain to be finalized.

## 7. Improvement and change control

### Decision I-01: Two-layer improvement

Status: Confirmed

Improvement occurs at two layers.

Agent layer:

- improves its specialist knowledge;
- improves its own workflow;
- improves relevant skills and checks;
- improves output quality within its responsibility.

Raphael layer:

- aggregates successes and failures across agents;
- improves role assignment;
- improves common rules;
- improves handoffs and coordination;
- improves organization-wide judgment and governance;
- learns Ryunosuke's decision patterns.

### Decision I-02: Raphael knows every change

Status: Confirmed

All changes, regardless of size, must be known to Raphael.

This does not mean every minor change requires Ryunosuke's prior approval. It means there must be no hidden self-modification by an agent outside Raphael's awareness.

Raphael should be able to know:

- what changed;
- who proposed or performed it;
- why it changed;
- affected agents, skills, rules, workflows, data, or tools;
- whether it was tested;
- whether rollback is possible;
- whether approval was required and obtained;
- observed effect after change.

### Decision I-03: Important changes require Ryunosuke approval

Status: Confirmed

Important changes require Ryunosuke's approval.

Likely important categories include:

- purpose or responsibility changes;
- authority expansion;
- organization-wide rules;
- creation, integration, suspension, or retirement of agents;
- sensitive data or tool access;
- external or irreversible effects;
- major cost, security, privacy, legal, trust, or strategic impact;
- changes to the interpretation of Ryunosuke's values or judgment model.

The precise boundary between minor and important changes remains unresolved and must be designed later.

## 8. Current unresolved topics

The following matters have not yet been decided and must not be assumed:

1. Memory architecture
   - specialist agent memory;
   - Raphael shared organizational memory;
   - Ryunosuke judgment history;
   - read/write/update/approval rights;
   - temporary vs long-term memory;
   - correction, deletion, and forgetting;
   - storage location and canonical source.
2. Exact trust/autonomy levels and promotion/demotion thresholds.
3. Exact objection severity levels and mandatory stop conditions.
4. Exact definition of an important change.
5. Exact confidence threshold for Raphael proxy decisions.
6. Pilot duration and evidence required for agent activation.
7. Review frequency and performance scoring.
8. Archive and retirement structure.
9. Full synchronization targets after `AGENT_STANDARD.md` revision.

## 9. Next design question

The next discussion starts with memory architecture.

The next session must first explain the main memory categories and design trade-offs, then ask Ryunosuke for a decision. It must not write a final memory architecture into GitHub before that confirmation.

## 10. Revision target

After enough foundational decisions are complete:

1. Rewrite `AGENT_STANDARD.md` to match this decision log.
2. Audit every section against every confirmed decision.
3. Mark remaining proposals explicitly.
4. Synchronize affected canonical documents.
5. Add tests and acceptance criteria.
6. Create a PR only after Ryunosuke reviews the consolidated design.
