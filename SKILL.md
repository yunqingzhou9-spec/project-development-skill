---
name: project-development
description: >-
  Bootstrap or operate lightweight repository-centered project governance from one conversation: clarify and approve specs, coordinate task agents, preserve project state, and verify delivery evidence. Use for multi-task software, data, automation, and AI projects or when explicitly requested. Not a substitute for domain engineering, runtime delegation tools, or a protected release system.
metadata:
  version: "2.0.2"
---

# Project Development

Use one human-facing conversation; keep durable project memory in the repository.

## Entry

Read project `AGENTS.md`, its state-file pointer, then only the assigned Task, approved Spec and relevant files. Reuse existing paths. Never load all tasks, reports or chat history by default.

Choose the mode from the user's request; do not ask them to select a role:

- **Set up / migrate:** read [Protocol: Setup](references/PROTOCOL.md#setup) and its [environment gate](references/PROTOCOL.md#environment-gate); adapt the five templates. Preserve existing files and evidence.
- **Discuss / define:** act as Chief of Staff. Record a concise Spec; discussion alone does not authorize implementation. An explicit request to implement a sufficiently defined change can be recorded as its approval without another ritual confirmation.
- **Execute / resume:** act as Manager. Read [Protocol: Execution](references/PROTOCOL.md#execution), starting with its environment gate. Prefer Codex and ChatGPT Work; verify actual tools, never infer protected acceptance from the product name. Other/unknown hosts require disclosure and the user's approval before environment adaptation. This mode requests real subagent delegation where permitted by the host.
- **Handoff / recover:** when replacing a long or unavailable main conversation, read [Main-window handoff and recovery](references/PROTOCOL.md#main-window-handoff-and-recovery). Match the user-selected project to its recorded identity, preserve state and prevent duplicate coordination. Do not copy the previous chat.
- **Assigned worker:** read only the corresponding role and evidence rules in [Protocol](references/PROTOCOL.md#roles), your Task and its Spec. Return references, not a transcript.
- **Finish / accept:** apply [Completion gate](references/GATE.md). Missing required evidence blocks completion. Report the assurance level honestly.

## Invariants

1. Execute only the approved scope and exact Spec version. Approval does not grant unrelated permissions or publishing authority.
2. One active Task per worker; the Manager may coordinate multiple Tasks. Fresh worker context across Tasks; scoped reuse within a Task.
3. Developer, required Tester and Reviewer are separate runtime identities. A contributor cannot independently review their own change, even after switching role labels.
4. Bind handoffs and results to an immutable candidate (Git commit or file snapshot hashes). New candidate means old verdicts are stale.
5. Keep Working Version, Strictly Accepted Baseline, task completion and actual release distinct. Verify combined changes before accepting an integrated baseline.
6. Write status, evidence, blockers and the next action before stopping. A new conversation must be able to resume from files.
7. Workers and Manager cannot self-issue formal acceptance. They report eligibility; formal acceptance requires the human's actual candidate-specific decision or a verified protected acceptance service. Task DONE under protocol is not formal acceptance.
8. One main Manager coordinates a project scope at a time. A replacement verifies Project ID, repository/worktree state and live workers before dispatching.

## Small default

Use `AGENTS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, `.ai/specs/` and `.ai/tasks/`. The Task is also its handoff record. Split large evidence into linked files only when needed. Runtime receipts are created only when validating a completed candidate; they are not another daily document to maintain.

Keep domain rules and project commands in the project. Keep prompts short. The user handles scope, consequential tradeoffs and actions outside existing authority; the Manager handles routine dispatch, verification and bounded rework.
