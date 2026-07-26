# Stage 2 Decision Log

Version: 0.1.4-draft  
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

## 8. Memory architecture

### Decision M-01: Hierarchical reference model with selected automatic sharing

Status: Confirmed

The memory architecture uses a hierarchical reference model with selected automatic sharing.

- Memory is separated by purpose and sensitivity rather than exposed as one unrestricted shared store.
- Each specialist agent maintains specialist memory for its own responsibility.
- Raphael governs shared organizational memory and the organization-wide change history.
- Ryunosuke's judgment history is maintained as a separate protected memory domain.
- Agents receive or reference only the memory needed for their role and current work.
- A limited set of frequently needed organizational information is shared automatically to support normal coordination.

The automatically shared set should include categories such as:

- organizational goals;
- current priorities;
- common rules;
- relevant project status;
- urgent organization-wide risks.

Specialist memory and Ryunosuke's protected judgment history are not automatically shared in full.

This decision establishes the baseline structure only. Exact read, proposal, write, update, approval, correction, deletion, forgetting, retention, storage, and canonical-source rules remain unresolved.

Reason:

This model preserves specialist responsibility and protects sensitive judgment history while avoiding unnecessary dependence on Raphael for routine information distribution.

### Decision M-02: Broad discoverability with task-necessary retrieval

Status: Confirmed

Agents may broadly discover that organizational memory exists, except for protected or restricted domains. However, an agent should retrieve and load only information that is necessary and relevant to its assigned role and current task.

- Broad read eligibility does not mean loading all accessible memory into every task context.
- Retrieval should be purpose-bound and limited to the minimum useful scope.
- Specialist agents should not collect unrelated information merely because it is technically accessible.
- Updates remain more restricted than reads and are governed separately.
- Protected memories, including sensitive information and Ryunosuke's protected judgment history, are outside this broad-access default unless separately authorized.
- Raphael must be able to trace material cross-domain retrieval when governance or risk requires it.

The exact definition of "necessary information," enforcement method, protected-memory categories, and retrieval logging thresholds remain unresolved.

Reason:

This preserves fast cross-agent coordination while reducing irrelevant context, privacy exposure, contamination of specialist judgment, and unnecessary processing cost.

### Decision M-03: Agent-selected retrieval with Raphael supplementation

Status: Confirmed

Each agent primarily determines what information is necessary for its assigned work and retrieves that information itself. Raphael supplements the agent's context when Raphael identifies an important related fact, premise, dependency, contradiction, or risk that the agent has missed.

- The default does not require Raphael to select or approve every retrieval.
- Agents may retrieve task-relevant information using their own professional judgment, subject to the purpose limitation and protected-domain restrictions established in M-02.
- Raphael may proactively provide missing information when doing so improves correctness, safety, coordination, or alignment with organizational priorities.
- Raphael's supplementation is a safety and coordination backstop, not a requirement to mediate all routine retrieval.
- Role-based fixed retrieval scopes are not the primary control model, though role, responsibility, sensitivity, and current assignment may still inform necessity and access decisions.
- This decision does not grant unrestricted access to protected memory and does not settle write or update authority.

The exact mechanism for necessity checks, excessive-retrieval detection, Raphael supplementation, and retrieval logging remains unresolved.

Reason:

This preserves agent initiative and speed while allowing Raphael to reduce important omissions across agents and domains.

### Decision M-04: Domain-based write authority with staged validation

Status: Confirmed

Long-term memory write authority is divided by memory domain, while all updates use a staged validation process.

Write responsibility:

- Each specialist agent may propose and perform updates to its own specialist memory within its assigned responsibility.
- Raphael updates and governs shared organizational memory, Ryunosuke's judgment history, and other important or cross-domain memory.
- All memory changes must be visible to Raphael under Decision I-02.
- A specialist agent may not directly rewrite protected, organization-wide, or another agent's specialist memory merely because it can read or discover it.

Update process:

1. Register the proposed update as a candidate rather than immediately treating it as canonical truth.
2. Record the source, reason, proposer, affected scope, confidence or uncertainty, and rollback path.
3. Test or otherwise verify the candidate using criteria appropriate to the memory and its intended use.
4. Compare the candidate against the prior version to determine whether it actually improves correctness, usefulness, reliability, efficiency, safety, or another declared objective.
5. Promote it to canonical memory only when the evidence supports improvement and the required approval has been obtained.
6. Reject, revise, or roll back the candidate when it does not outperform the prior version, creates unacceptable trade-offs, or lacks sufficient evidence.
7. Record the observed post-change effect so later reviews can confirm that the improvement persisted in real operation.

Important, protected, organization-wide, high-risk, or value-defining updates require Raphael review and, where applicable under existing governance, Ryunosuke's approval.

This decision extends the already confirmed change-control principles in I-02 and I-03: changes must disclose whether they were tested, whether rollback is possible, and what effect was observed. It also aligns with the earlier operating principle that procedures improve from recorded failures, confusion, and rework rather than from unverified assumptions.

Exact test types, evaluation metrics, evidence thresholds, review periods, and low-risk automatic-promotion conditions remain unresolved.

Reason:

This structure preserves specialist speed and ownership without allowing untested changes to silently replace long-term canonical memory. Comparing the candidate with the prior version makes “improvement” an evidence-based judgment rather than an assumption.


### Decision M-05: Ryunosuke approval first, gradual delegation to Raphael

Status: Confirmed

Candidate long-term memory updates require Ryunosuke's approval at the beginning of operation. Approval authority may later be delegated gradually to Raphael as evidence of reliable judgment accumulates.

- The initial default is that Ryunosuke approves promotion of candidate memory into canonical long-term memory.
- Passing validation or outperforming the prior version does not by itself grant automatic promotion during the initial stage.
- Raphael should prepare the evidence, comparison results, risks, affected scope, and recommendation so Ryunosuke can decide efficiently.
- As Raphael demonstrates reliable memory-governance judgment, Ryunosuke may delegate approval for defined low-risk categories or bounded scopes.
- Delegation is not permanent by default: it may be narrowed, suspended, or revoked after failures, changed conditions, insufficient confidence, or boundary violations.
- Important, protected, organization-wide, high-impact, irreversible, privacy-sensitive, security-sensitive, value-defining, or novel updates remain subject to Ryunosuke approval unless he explicitly delegates them.
- All promotions, whether approved by Ryunosuke or delegated to Raphael, remain visible and traceable under I-02 and must follow the staged validation process in M-04.

This decision applies the gradual-autonomy principle in T-01 and D-01 specifically to canonical memory promotion. Exact evidence requirements, delegation levels, eligible low-risk categories, review cadence, and revocation thresholds remain unresolved.

Reason:

Early human approval allows Raphael to learn Ryunosuke's standards for evidence, trade-offs, and acceptable risk before receiving bounded proxy authority. Gradual delegation preserves the intended path toward autonomy without granting broad memory-control authority prematurely.


## 9. Current unresolved topics

The following matters have not yet been decided and must not be assumed:

1. Detailed memory governance
   - exact evidence requirements, delegation levels, eligible low-risk categories, review cadence, and revocation thresholds for memory-update approval;
   - temporary working memory vs long-term canonical memory;
   - correction, deletion, forgetting, and retention;
   - storage location and canonical source;
   - exact scope and delivery rules for automatically shared organizational memory;\n   - definition and enforcement of task-necessary retrieval;\n   - protected-memory categories and cross-domain retrieval logging thresholds.
2. Exact trust/autonomy levels and promotion/demotion thresholds.
3. Exact objection severity levels and mandatory stop conditions.
4. Exact definition of an important change.
5. Exact confidence threshold for Raphael proxy decisions.
6. Pilot duration and evidence required for agent activation.
7. Review frequency and performance scoring.
8. Archive and retirement structure.
9. Full synchronization targets after `AGENT_STANDARD.md` revision.

## 10. Next design question

The next discussion continues with detailed memory governance, beginning with the conditions and evidence required before Raphael receives delegated approval authority for candidate long-term memory updates.

The next session must explain the main access models and trade-offs, then ask Ryunosuke to choose from multiple options. It must not assume unresolved read, write, approval, correction, deletion, forgetting, retention, storage, or canonical-source rules.

## 11. Revision target

After enough foundational decisions are complete:

1. Rewrite `AGENT_STANDARD.md` to match this decision log.
2. Audit every section against every confirmed decision.
3. Mark remaining proposals explicitly.
4. Synchronize affected canonical documents.
5. Add tests and acceptance criteria.
6. Create a PR only after Ryunosuke reviews the consolidated design.
