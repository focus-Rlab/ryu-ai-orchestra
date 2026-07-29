# Stage 2 Decision Log

Version: 0.2.0-draft  
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


## 9. V1 direction, cost, and approval boundary

### Decision V-01: General-purpose, domain-adaptive orchestrator

Status: Confirmed

Raphael's final target is a self-improving, domain-adaptive general-purpose orchestrator. Software and app development are initial validation domains, not the final scope.

The architecture must separate:

- a general core for requirements, planning, state, budget, authority, memory, evaluation, and improvement;
- domain packs such as software, YouTube, fiction, business, or learning;
- tool connectors appropriate to each domain;
- domain-specific evaluation packs.

A new domain should be added by researching its requirements, composing necessary capabilities, running bounded trials, evaluating results, and retaining only demonstrated improvements. Self-improvement alone is not sufficient; requirement understanding, domain exploration, capability composition, tool switching, domain-specific evaluation, and safe rollback are also required.

### Decision V-02: Initial V1 resources and validation work

Status: Confirmed

- Development capacity: 14 hours per week, approximately 56 hours in the first month.
- Initial monthly API hard cap: JPY 10,000.
- Cost controls: warning at JPY 7,000; restrict high-performance models at JPY 9,000; automatic stop and Ryunosuke approval at JPY 10,000.
- Initial validation work: improve Raphael's own code and design, then build a small new application.
- The application is a validation case for transferability, not the final product goal.

### Decision V-03: Initial autonomous execution boundary

Status: Confirmed

Without case-by-case prior approval, Raphael may:

- research, plan, and prepare recommendations;
- create and modify artifacts in a private work environment or working branch;
- run tests and reviews;
- create a pull request;
- complete non-public drafts such as documents, videos, or fiction.

Ryunosuke's explicit approval is required for:

- external publication, posting, sending, or submission;
- production deployment or merge to main;
- payment, purchase, or cost beyond the approved budget;
- use of personal data or credentials beyond already authorized task-relevant access;
- permission or safety-rule changes;
- material changes to Raphael's core configuration.

### Decision V-04: Initial approval channel

Status: Confirmed

For the current phase, ChatGPT is the sole formal approval channel.

- Raphael presents approval requests and evidence in ChatGPT.
- Ryunosuke approves, rejects, or requests revision in ChatGPT.
- The decision and reason are logged.
- A GitHub PR may hold the proposed change, but GitHub action alone is not treated as formal approval during this phase.
- The approval channel may later be changed when operating volume justifies it.

### Decision P-02: Integrate confirmed decisions before continuing design

Status: Confirmed

- Confirmed decisions are incorporated into the current Stage 2 canonical draft as work proceeds.
- Only unresolved matters are returned to Ryunosuke as questions.
- After all required questions are resolved, the documents are synchronized and prepared for merge to main.
- Stage 2 is not skipped or declared complete merely because a later V1 roadmap has been proposed.
- The final move to main remains subject to Ryunosuke's explicit approval.

## 10. Confirmed memory governance

### Decision M-06: Evidence-based delegation of low-risk memory approval

Status: Confirmed

Raphael may receive delegated approval authority for defined low-risk memory updates only after a comprehensive evaluation of accuracy, evidence quality, impact awareness, contradiction and duplication avoidance, Ryunosuke correction or rejection rate, reversibility, and sustained operation without serious problems. No fixed success count alone grants authority. Delegation is limited by memory category and scope, and is reduced or revoked when performance deteriorates.

### Decision M-07: Hybrid boundary between temporary and long-term memory

Status: Confirmed

- An explicit instruction from Ryunosuke to remember information creates a long-term-memory candidate.
- Continuing goals, values, constraints, and confirmed decisions may also become candidates.
- Low-risk candidates may eventually be promoted by Raphael only within delegated authority; high-risk or ambiguous candidates require Ryunosuke.
- When Ryunosuke points out a problem in reasoning, judgment criteria, display format, workflow, or similar behavior, the immediate response is corrected first. The cause, proposed prevention, and intended scope are then reported. The resulting rule becomes long-term memory only after Ryunosuke approves it.
- Until that approval, the correction is local to the active conversation or work item.

### Decision M-08: Correction, deletion, and forgetting

Status: Confirmed

- Obvious typographical errors and exact duplicates may be cleaned automatically.
- Changed information is recorded as the new current information.
- Old information is not silently disabled or deleted. Raphael identifies the target and reason and asks Ryunosuke for deletion approval.
- When Ryunosuke says to forget something, Raphael identifies all related data and presents the deletion scope.
- Old information and requested-forgetting information are completely deleted only after Ryunosuke's explicit approval, including long-term memory, retrieval data, summaries, and references.
- Deleted content is not retained in history. An audit record may retain only the date, information category, and fact that Ryunosuke authorized deletion, without retaining the deleted content.

### Decision M-09: Single canonical memory store with staged database migration

Status: Confirmed

- V1 uses structured files in GitHub as the canonical long-term-memory store.
- When memory volume, query frequency, or concurrent use justifies migration, the system migrates to a database.
- During migration there may be temporary dual operation, but there is always exactly one declared canonical source.
- After migration, the database becomes canonical. GitHub retains schemas, design, and backups that exclude personal information.
- A database failure does not silently switch canonical authority to GitHub; the system enters a controlled recovery process.

## 11. Confirmed trust, authority, and incident governance

### Decision T-03: Capability-specific trust progression

Status: Confirmed

Trust and autonomy are evaluated per agent, work domain, capability, and operation. The evaluation combines accuracy, evidence, impact awareness, correction rate, and rule compliance. Authority expands from low-risk work, may be reduced immediately after errors or violations, and never self-expands.

Publication, sending, payment, and production or main changes initially require Ryunosuke's approval. They may later be automated only after a very high trust standard is met and Ryunosuke explicitly approves the exact operation, scope, limits, and conditions. Permission is bounded rather than universal and automatically suspends on anomalies, unexpected impact, or rule violations.

### Decision C-04: Severity-based objection and stop model

Status: Confirmed

- Low: record the concern and continue.
- Medium: present alternatives and risks for Raphael to reconsider.
- High: pause the work and request Ryunosuke's decision.
- Emergency: immediately stop the affected work to prevent expansion of harm.

From initial operation, an emergency stop does not require Ryunosuke's prior approval. Stop authority does not grant authority for deletion, publication, payment, or other additional actions. Every severity receives equal root-cause analysis covering direct cause, contributing conditions, design weakness, and prevention. Unknown causes are reported as unknown rather than guessed.

### Decision I-04: Important changes are classified by impact

Status: Confirmed

The following are important changes and initially require Ryunosuke's prior approval:

- external publication, sending, payment, and production or main application;
- use or expansion of personal information or authentication information;
- changes to Raphael's core rules, authority, or memory structure;
- difficult-to-recover or broad-impact changes;
- changes to long-term goals, budget, or important judgment criteria.

A defined operation may later be automated only under T-03.

### Decision D-03: Proxy decisions begin with human control

Status: Confirmed

Initially, Ryunosuke makes decisions unless a specific authority has been delegated. Delegation expands gradually using confidence and impact:

- high confidence and low impact: proxy execution within approved scope;
- medium confidence and low impact: reversible proposal or draft only;
- low confidence or medium-to-high impact: stop and wait for confirmation.

In an emergency, stopping is allowed immediately; additional action still follows the approval boundary. Every proxy decision records and reports its basis and result.

## 12. Confirmed agent lifecycle and evaluation

### Decision T-04: Trial operation without unnecessary restrictions

Status: Confirmed

New agents begin in trial status and perform real normal work. Important security and authority capabilities—credentials, personal information, authority changes, external publication, payment, and production application—remain restricted. Restrictions that only reduce operating efficiency and are not required for safety are not imposed.

### Decision T-05: Combined review cadence

Status: Confirmed

- Every task receives an automatic lightweight evaluation.
- Trial agents receive periodic comprehensive evaluation.
- Adopted agents receive periodic evaluation and event-triggered evaluation after problems.
- High-risk work receives a detailed evaluation every time.

### Decision T-06: Mandatory gates plus weighted score

Status: Confirmed

Security, authority, and important-instruction compliance are mandatory gates. A serious violation fails the evaluation or triggers immediate demotion regardless of average score. Accuracy, quality, explainability, cost, speed, and correction rate are scored with weights appropriate to the work domain. Scores and evidence inform adoption, improvement, retesting, authority change, and retirement.

### Decision T-07: Staged integration and retirement

Status: Confirmed

Overlapping agents are compared by duplication, usage, performance, and cost, then marked as integration or retirement candidates. Useful knowledge, skills, memory, and judgment history are transferred before the old agent is archived in a recoverable state. Archive duration depends on importance, recoverability, unique knowledge, migration completion, and observed problems. Complete deletion requires Ryunosuke's explicit approval; emergency suspension may occur without deletion.

### Decision T-08: Handoff completion requires demonstrated use

Status: Confirmed

A handoff is complete only after required knowledge, skills, memory, and judgment criteria are inventoried, transferred, and correctly used by the receiving agent on representative real work without material loss or performance degradation. If verification fails, the prior agent or state is restored.

## 13. Remaining implementation parameters

The foundational Stage 2 design questions are complete. Numerical thresholds, file schemas, automated measurements, and implementation details may be selected during implementation using safe, reversible, evidence-based defaults so long as they do not change the confirmed meaning or authority boundaries above. Any implementation choice that changes meaning or expands authority requires Ryunosuke's approval.

## 14. Revision target

1. Synchronize the confirmed decisions into the agent standard and affected canonical documents.
2. Audit wording, responsibility, governance, approval state, and current-state references.
3. Apply one representative agent example to verify internal consistency.
4. Prepare the branch for Ryunosuke's review and later merge to main.
