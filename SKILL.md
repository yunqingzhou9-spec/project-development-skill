---
name: project-development
description: >-
  Bootstrap or operate lightweight repository-centered project governance from one conversation: clarify and approve specs, coordinate task agents, preserve project state, and verify delivery evidence. Use for multi-task software, data, automation, and AI projects or when explicitly requested. Not a substitute for domain engineering, runtime delegation tools, or a protected release system.
metadata:
  version: "2.1.0-dev.1"
---

# Project Development

Use one human-facing conversation; keep durable project memory in the repository.

## 60-second start / 60 秒开始

Tell me the outcome in ordinary language, for example: `$project-development Add CSV export and verify it works.` I will inspect the repository, clarify only consequential unknowns, select `LIGHTWEIGHT` for an objectively small low-risk change or `FULL` otherwise, and show you the exact candidate for acceptance. You do not need to learn the roles or evidence vocabulary first. Implementation, installation and publication remain separate decisions.

直接描述结果即可，例如：`$project-development 添加 CSV 导出并验证可用。` 我会检查仓库，只询问会影响结果的重要问题；客观上小而低风险的改动走 `LIGHTWEIGHT`，其余走 `FULL`；最后把准确候选版本交给你验收。你不需要先学习角色或证据术语。实现、安装和发布仍是不同决定。

## Entry

Read project `AGENTS.md`, its state-file pointer, then only the assigned Task, approved Spec and relevant files. Reuse existing paths. Never load all tasks, reports or chat history by default.

Choose the mode from the user's request; do not ask them to select a role:

- **Set up / migrate:** read [Protocol: Setup](references/PROTOCOL.md#setup) and its [environment gate](references/PROTOCOL.md#environment-gate); adapt the five templates. Preserve existing files and evidence.
- **Discuss / define:** act as Chief of Staff. Record a concise Spec for `FULL`, or the approved scope inside one Task for eligible `LIGHTWEIGHT` work; discussion alone does not authorize implementation. An explicit request to implement a sufficiently defined change can be recorded as its approval without another ritual confirmation.
- **Execute / resume:** act as Manager. Read [Protocol: Execution](references/PROTOCOL.md#execution), starting with its environment gate. Prefer Codex and ChatGPT Work; verify actual tools, never infer protected acceptance from the product name. Other/unknown hosts require disclosure and the user's approval before environment adaptation. This mode requests real subagent delegation where permitted by the host.
- **Handoff / recover:** when replacing a long or unavailable main conversation, read [Main-window handoff and recovery](references/PROTOCOL.md#main-window-handoff-and-recovery). Match the user-selected project to its recorded identity, preserve state and prevent duplicate coordination. Do not copy the previous chat.
- **Assigned worker:** read only the corresponding role and evidence rules in [Protocol](references/PROTOCOL.md#roles), your Task and its Spec. Return references, not a transcript.
- **Finish / accept:** apply [Completion gate](references/GATE.md). Missing required evidence blocks completion. Report the assurance level honestly.

## Invariants

1. Execute only the approved scope and exact criteria digest (frozen Spec for `FULL`, inline scope for eligible `LIGHTWEIGHT`). Approval does not grant unrelated permissions or publishing authority.
2. One active Task per worker; the Manager may coordinate multiple Tasks. Fresh worker context across Tasks; scoped reuse within a Task.
3. Developer, required Tester and Reviewer are separate runtime identities. A contributor cannot independently review their own change, even after switching role labels.
4. Bind handoffs and results to an immutable candidate (Git commit or file snapshot hashes). New candidate means old verdicts are stale.
5. Keep Working Version, Strictly Accepted Baseline, task completion and actual release distinct. Verify combined changes before accepting an integrated baseline.
6. Write status, evidence, blockers and the next action before stopping. A new conversation must be able to resume from files.
7. Workers and Manager cannot self-issue formal acceptance. They report eligibility; formal acceptance requires the human's actual candidate-specific decision or a verified protected acceptance service. Task DONE under protocol is not formal acceptance.
8. One main Manager coordinates a project scope at a time. A replacement verifies Project ID, repository/worktree state and live workers before dispatching.

## Small default

Use `AGENTS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, `.ai/specs/` and `.ai/tasks/`. The Task is also its handoff record. Split large evidence into linked files only when needed. Runtime receipts are created only when validating a completed candidate; they are not another daily document to maintain.

Select `LIGHTWEIGHT` only by the bounded checklist in [Protocol](references/PROTOCOL.md#workflow-profiles). Any false or uncertain item selects `FULL`. `LIGHTWEIGHT` still requires a real Developer, an independent Reviewer, candidate-bound evidence and Human acceptance; it removes redundant records, not safeguards.

Keep domain rules and project commands in the project. Keep prompts short. The user handles scope, consequential tradeoffs and actions outside existing authority; the Manager handles routine dispatch, verification and bounded rework.
