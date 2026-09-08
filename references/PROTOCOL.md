# Project development protocol — 2.0.3

Read the relevant section, not the entire file on every action. These are workflow rules, not a permission grant or a claim that any host supports delegation.

## Setup

1. Inspect the project's existing instructions, Git state and governance. Reuse existing sources instead of creating a competing hierarchy. Do not modify business code during governance-only setup.
2. Default to the five templates: AGENTS, PROJECT_STATE, DECISIONS, SPEC and TASK. Instantiate only needed documents; directories may be created with their first file. Replace template placeholders. Unknown facts stay `UNVERIFIED`; do not invent commands, approvals, accepted revisions or agent identities.
   Assign one stable Project ID during first setup. Reuse an authoritative existing project key first; otherwise use an ID explicitly supplied by the user; if neither exists, the Skill generates a readable unique value such as `SNAKE-GAME-7F3A2C`. Record the same ID in AGENTS and project state, and record the human-facing name, repository identity, project scope path and current local checkout separately. It identifies the project; it is not a credential. Project ID remains stable when the repository moves, is renamed or changes main conversation; checkout paths may change. Conflicting recorded IDs block setup or takeover until the user resolves the identity; do not regenerate or silently replace an ID.
3. AGENTS routes to the state, decisions and this skill's role/protocol rules. State indexes active Tasks and current blockers. Each Task owns its detailed state and handoff. Manager is the sole coordinator updating these shared records; workers return evidence and avoid concurrent edits to shared governance.
4. Preserve v1 `DECISION_LOG.md`, `KNOWN_ISSUES.md`, `ROADMAP.md`, `milestones/`, `audits/`, `archive/` and handoffs if present. Map them from AGENTS; do not rename or delete history for cosmetic consistency. Make the old `CURRENT_TASK.md` an optional compatibility pointer to the active-task index, not a second authoritative status record.
5. Separate truth by kind: human authorization and active decisions define intent; source/runtime evidence establishes implemented behavior; Task records establish workflow; state is a summary. When they conflict, record `CONFLICT` and investigate. Neither a stale summary nor unapproved code changes intent or proves acceptance.
6. Retain `ACTIVE`, `PROVISIONAL`, `UNVERIFIED`, `CONFLICT`, `SUPERSEDED`, `INVALID/DEPRECATED` when needed. Preserve invalid history with provenance and prevent its active use. Historical documented acceptance is not automatically an accepted baseline.
7. Cold-start check: from AGENTS alone, follow links to purpose, boundaries, working candidate, accepted baseline (or `UNESTABLISHED`), active Tasks, P0/P1 blockers, decisions, invalid knowledge, commands and next action. Unknowns may be explicit, but no answer may depend on chat memory. Verify paths and commands only within setup authority.

## Roles

| Role | Responsibility | Boundary |
|---|---|---|
| Human | Goals, scope approval, consequential tradeoffs and authority | Does not relay worker messages |
| Chief of Staff | Clarify goal, alternatives, scope and acceptance; record approval evidence | Discussion does not start implementation |
| Manager | Decompose approved work, dispatch, track dependencies, gate results and summarize | Cannot invent approval, overrule a required rejection or impersonate workers |
| Developer | Investigate, implement minimal scoped changes, self-test and identify candidate | Cannot grant task acceptance |
| Tester | Independently verify behavior against criteria; PASS/FAIL/BLOCKED | No product-code repairs; test additions are identified separately |
| Reviewer | Independently inspect intent, assumptions, logic, architecture, evidence and risk; APPROVE/REJECT/BLOCKED | No implementation edits while claiming independence |

The main agent may act as Chief of Staff and later Manager after approval. Never count its self-review or a worker's renamed role as independent verification. Tester/Reviewer must differ from all implementers and each other. If they repair deliverables, record them as contributors and obtain fresh independent verification.

Developer self-tests remain useful but are not the independent Test verdict. Reviewer can reject passing tests, including incorrect expected values or unreliable provenance. Domain-specific checks belong to the Spec/project (not hard-coded finance rules here).

## Specs and task sizing

- A Spec contains a goal, scope, non-goals, observable acceptance and approval reference. Freeze the approved version by SHA-256 of its file bytes; Tasks reference path + digest. Append a new version for scope/acceptance changes; do not silently edit an approved file. Record supersession in decisions/state, preserving the previous approved artifact.
- If the current user already clearly authorized implementation and its scope is sufficiently defined, record that actual request as approval. Ask only about unresolved consequential choices. Do not require a magic phrase or repeat permission already granted.
- Discussion, review-only or a draft with unanswered scope choices stays DRAFT. Preparing a draft or reading project evidence does not authorize business-code changes.
- Split by independently verifiable outcome, dependency or ownership boundary, not by each command or role. A Task moves through roles; ordinary rework stays in it. Record dependencies only when present.
- Verification profile is set before implementation: ordinary functional work requires Tester and Reviewer; pure documentation can omit runtime testing with a concrete reason; high-risk behavior requires both and integrated acceptance. Reviewer remains independent even for lightweight work. Do not relax required checks after failure without an authorized policy/scope decision.

## Execution

### Environment gate

- At setup and execution/resume, identify the host from trusted session metadata and exposed native tool provenance: `CODEX`, `CHATGPT_WORK`, `OTHER` or `UNKNOWN`. A GPT model name, a user-agent string, a repository label or an ordinary ChatGPT conversation does not establish ChatGPT Work. If evidence is ambiguous, use UNKNOWN rather than guess.
- Record a compact environment entry in project state: host + evidence reference, delegation/result access `VERIFIED/MISSING/UNKNOWN`, protected acceptance `VERIFIED/MISSING/UNKNOWN`, and formal acceptance authority `HUMAN` (default) or `PROTECTED_SERVICE`. Record current tool observations; a previous session's capability claim is not current proof. Reuse unchanged observations within a session instead of probing on every worker action. The first actual dispatch/result completes delegation verification; do not mark an untested capability VERIFIED.
- Codex and ChatGPT Work are preferred hosts for the native-tool workflow. Check their actual creation, assignment, result and state/artifact access. A supported product name or read-only Reviewer does not prove that logs, approvals or acceptance controls are protected. Missing native capability blocks the affected execution/verification stage; missing protected controls prevents ENFORCED claims but does not automatically prohibit authorized PROTOCOL work.
- For OTHER/UNKNOWN, notify once per environment change: this host has no validated support profile for this skill, state what is actually verified/missing/unknown, and ask whether the user wants the specific capability adaptation. Do not claim an inherently incapable platform if evidence only shows it is unverified. Safe read-only diagnosis and Spec preparation may continue. Pause dependent team execution until the user decides whether to authorize adaptation or explicitly use an already demonstrated, adequate native workflow at its stated assurance level.
- Adaptation needs a contemporaneous approval scoped to proposed installs, configuration, credentials, external services and cost where relevant. This skill's installation or the original project's implementation approval is not that approval. Honor an existing decision for the same host and scope without repeated questions. Do not install packages, alter permission/CI settings or provision services automatically on any host. No reply/declined adaptation leaves affected work blocked; it never authorizes roleplay or silent assurance downgrade.
- After approved adaptation, recheck actual tools and persist evidence before resuming. Native platform permissions remain controlling. Formal acceptance is issued only by the human for the exact candidate, or by a verified protected service with immutable candidate-bound receipt; workers/Manager can propose eligibility, not approve on the human's behalf. Human approval is a workflow boundary, not programmatic tamper resistance. Routine Task DONE can remain PROTOCOL; overall accepted-baseline promotion/release needs the configured formal authority. Ask for the human decision at the intended project/milestone acceptance point, not on every subtask. If PROTECTED_SERVICE/ENFORCED was selected and unavailable, block formal acceptance and ask before any authority change.

### Capability and dispatch

- Inspect the host's actual create/assign/status/result APIs. The first real dispatch must return a runtime identity; assignments and returned results must be attributable to it. Record the native creation/assignment/result references in the Task's receipts. Do not use invented UUIDs, role names, or shell-generated text as identities.
- Missing required delegation capability makes execution `BLOCKED`; missing result/provenance capability blocks verification/completion. Continue safe read-only diagnosis or Spec preparation, but do not replace required workers with main-agent roleplay. Report what is missing and what remains possible.
- Use task-scoped subagents, not user-visible top-level conversations, unless the user explicitly requests new conversations. Fresh context means no full-chat fork by default. Send only role, Task path, frozen Spec reference, candidate/base and necessary project paths. Reviewer receives original criteria and evidence, not instructions to agree with Developer conclusions.
- Respect observed concurrency/cumulative limits. Do not hard-code a slot count or assume idle agents release capacity. Use native termination/release when available; interruption is not assumed to delete an agent. Queue when slots are busy; if the host cannot free capacity for a required fresh identity, record a capacity blocker rather than reusing a contaminated agent.
- Start fresh identities for new Tasks. Reuse a Developer within the same Task for focused rework; restart from file references after confusion or repeated unproductive attempts. A task spanning several contributors records all of them.
- Run dependent tasks sequentially. Parallelize only separable work with safe write ownership or isolated worktrees/checkouts when supported. Shared repository does not mean all agents should edit one checkout. Manager serializes integration; any resulting new candidate gets fresh verification.

### State and rework

| Transition | Condition / responsible party |
|---|---|
| READY → DOING | Manager verifies approval, dependencies, capacity and assignment |
| DOING → VERIFY | Developer supplies frozen candidate, self-checks and evidence; Manager records handoff |
| VERIFY → DOING | Required test FAIL or review REJECT; Manager routes concrete findings back |
| VERIFY → DONE | Manager applies the completion gate to the exact final candidate |
| Active → BLOCKED | Missing authority, capability, evidence, external input or exhausted rework budget |
| BLOCKED → previous stage | Manager verifies blocker is resolved and rechecks stale inputs |
| DONE → VERIFY/DOING | Candidate/criteria changed or acceptance invalidated; preserve old evidence, clear current verdicts |

Store Test `PENDING/PASS/FAIL/BLOCKED/N/A` and Review `PENDING/APPROVE/REJECT/BLOCKED` separately from Task state. An N/A needs its previously selected profile and reason. Worker messages are evidence; only Manager updates authoritative state. DONE is not a release status.

Default rework budget: 3 failed verification cycles per Task; an explicit project limit overrides it. Ordinary failures within approved scope are handled without asking the user. At the limit, stop dispatching repeated repair attempts, summarize root cause and options, and request the necessary decision. New scope, risk acceptance, authority or unresolved authoritative conflicts also require escalation. Capacity queues and unchanged progress need no repetitive user notifications.

### Evidence and recovery

- Evaluate Static, Unit, Integration, Scenario and Acceptance as applicable; N/A needs a reason. Classify failures as introduced, pre-existing, environment-limited or unverified. Existing failures only cease blocking when the approved criteria/policy supports that conclusion, not because they are old.
- Handoff is Task ID + Spec digest + base/candidate + report references + next action. Reports include commands, observed results, environment limits and unresolved issues. Keep small reports inside the Task; link large outputs. No repeated transcript copying.
- For Git, use a full commit ID that includes all deliverable changes; do not describe dirty work as covered by that commit. Report-only/governance commits may follow it, but no later deliverable change inherits approval. For non-Git outputs, use explicit file paths and SHA-256 hashes, including all deliverables; retain accepted bytes in versioned snapshot paths so old baselines remain reproducible. Review context must include relevant base/diff and inputs, not merely a hash list.
- Persist state before ending. On resume, inspect actual run status, working files and candidate before launching replacement work; do not blindly replay an assignment. Reconnect to live workers where supported; otherwise record interrupted work and create a fresh worker only after avoiding duplicate writers.
- Main context contains active index, decisions and short references. Archive/index completed detail without deleting evidence. A replacement main conversation uses AGENTS and state; no permanent-window or uninterrupted-background guarantee is implied.

### Main-window handoff and recovery

Changing the main conversation does not create a new Spec or Task. The user selects the intended project/workspace when opening the replacement conversation and, when several projects exist, names its Project ID. The Manager must match that ID to project state and verify repository identity and scope before changing anything. A name or folder label alone is insufficient. On mismatch, stop and ask the user to open or identify the intended project; do not search unrelated projects or guess.

When the user asks how to perform a planned handoff, provide a copy-ready request that tells the current Manager to stop new dispatch, inspect active workers, write the required state, mark `READY_FOR_TAKEOVER`, cease coordination and report the Project ID plus readiness. Exact prompt wording is not an authority or receipt: repository records and verifiable native runtime state determine whether takeover is safe. Do not substitute copied chat for those records.

#### Planned handoff

The current Manager:

1. Stops new dispatch and marks coordination `HANDOFF_PREPARING`.
2. Checks active workers. Prefer waiting for normally progressing work to reach a reportable point. A worker may continue only if the replacement Manager can inspect or reconnect through a native reference.
3. Stops a worker only when it is stalled, blocked, conflicting, or the user requires immediate handoff. First record its runtime ID, observable progress, changed files and unfinished work. Do not assume interruption deletes an agent or releases capacity.
4. Writes Project ID, repository/worktree, branch, candidate commit, dirty/untracked changes, active workers, blockers and exact next action to state and Task records. Commit only coherent scoped work appropriate to commit; describe other partial work accurately.
5. Marks coordination `READY_FOR_TAKEOVER` and ceases coordination for that project scope.

The replacement Manager:

1. Reads AGENTS, state, active Tasks and their approved Specs from the user-selected project.
2. Confirms requested Project ID, repository identity, scope path, actual worktree/checkout, branch, commit, uncommitted changes and native worker state. A different worktree may not contain uncommitted or ignored files.
3. Reconnects to observable workers where supported. It does not duplicate an assignment that may still be running or allow two Managers to dispatch within the same scope.
4. Reconciles differences between recorded and actual state, marks coordination `ACTIVE` with its current Manager/session reference, then resumes the recorded next action.

#### Unplanned recovery

If the prior window is unavailable, the replacement Manager marks coordination `RECOVERY` and treats recorded runtime state as potentially stale. It verifies Project ID and actual repository/runtime state before dispatch. If an existing writer cannot be ruled out, keep that Task BLOCKED until the worker completes, is reconnected, or is confirmed stopped; unrelated safe Tasks may continue. Record lost or unverifiable work, reconcile state, mark the new Manager ACTIVE and continue. Do not reconstruct authoritative state from copied chat when repository/native evidence exists.

## Completion and release

Read [GATE.md](GATE.md) only when collecting receipts, checking completion or integrating runtime enforcement.

Task DONE means the exact candidate satisfied its required checks and write-back. Keep the working candidate separate from the last independently accepted immutable baseline. Multiple accepted Tasks do not prove their merged behavior: create an integration Task for the final combined candidate. Every release/milestone retains independent integration acceptance proportional to its criteria, including high-risk failure/migration/rollback checks where relevant.

State records release `NOT_RELEASED/READY/RELEASED/ROLLED_BACK` only when applicable, with candidate, integration evidence, actual authorization, deployed artifact/environment and post-release result. Release only within explicit or pre-existing authority; candidate approval is not publishing permission. Baseline promotion requires independent verification plus the configured formal authority's acceptance of that exact state, not just a report, task completion or a successful upload. Preserve prior baseline and rollback references as appropriate.
