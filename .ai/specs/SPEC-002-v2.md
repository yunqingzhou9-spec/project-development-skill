# SPEC-002 v2 — Add revised bilingual Skill introduction

```json
{
  "id": "SPEC-002-v2",
  "status": "APPROVED",
  "approval_ref": "User explicitly designated this revised bilingual text as authoritative in the current Codex task on 2026-09-08; recorded as DEC-008"
}
```

## Goal / scope

- Put the exact approved Chinese and English introduction below at the beginning of `README.md`, directly below the existing document title.
- Remove the older short opening paragraphs that would duplicate the new introduction; retain the existing detailed feature list and capability-boundary section.
- Release the documentation update as patch version `2.0.4`, updating `SKILL.md`, the protocol version heading and `CHANGELOG.md` without changing protocol semantics.
- After candidate-specific Human acceptance, synchronize the installed Skill and publish `main` plus annotated tag `v2.0.4` to GitHub under the user's explicit sync-and-publish request.

## Exact approved README introduction

# 中文

> **让 AI 不只是会写代码，而是能像一支受管理的软件团队一样完成项目。**

使用 AI 开发时，真正困难的往往不是“生成代码”，而是：**需求没想清楚、任务不会拆、多个 Agent 难协调、实现缺乏独立验证、返工过程混乱，以及到底什么时候才算真正完成。**

`project-development` 就是为了解决这些问题。

它在一个主窗口中保留常驻的 **Chief of Staff + Manager**：前者帮助 Human 澄清目标、范围和验收标准，后者把批准后的 Spec 拆成 Tasks，并按需创建独立的 Developer、Tester、Reviewer 等 Worker Agents，自动组织实现、测试、审查和返工。

```sql
Idea
→ Clarify the goal
→ Approve the Spec
→ Break it into Tasks
→ Create the right Worker Agents
→ Implement
→ Independently test & review
→ Rework when needed
→ Complete
→ Human acceptance
```

**Human 负责方向和最终决策，AI 团队负责把事情可靠地做完。**

---

# English

> **Make AI not just write code, but complete software work like a managed engineering team.**

The hard part of AI-assisted development is often no longer code generation. It is **clarifying what should be built, breaking it into executable work, coordinating multiple agents, independently verifying implementation, managing rework, and knowing when the work is actually done.**

`project-development` is designed to solve that problem.

It keeps a persistent **Chief of Staff + Manager** in one primary session: the Chief of Staff helps the Human clarify goals, scope, trade-offs, and acceptance criteria; the Manager turns the approved Spec into Tasks and dynamically creates independent Developer, Tester, Reviewer, and other Worker Agents to execute, verify, review, and rework the project.

```sql
Idea
→ Clarify the goal
→ Approve the Spec
→ Break it into Tasks
→ Create the right Worker Agents
→ Implement
→ Independently test & review
→ Rework when needed
→ Complete
→ Human acceptance
```

**The Human owns direction and final decisions. The AI team handles the work of getting there reliably.**

## Non-goals / constraints

- Do not alter the approved introduction wording other than normal Markdown placement below the existing document title.
- Do not change agent roles, state transitions, delegation requirements, evidence rules, acceptance authority or safety boundaries.
- Do not add new scripts, dependencies or a separate GitHub Release page.
- Version 2.0.3 governs this task; version 2.0.4 cannot approve or verify itself.
- Publication authority does not replace candidate-specific Human acceptance.

## Acceptance

- AC-1: README begins with the complete approved Chinese introduction, workflow and tagline.
- AC-2: README then includes the complete approved English introduction, workflow and tagline.
- AC-3: Existing duplicate opening prose is removed while the detailed feature list and capability-boundary explanation remain.
- AC-4: `SKILL.md`, `references/PROTOCOL.md` and `CHANGELOG.md` consistently identify version 2.0.4; protocol behavior is otherwise unchanged.
- AC-5: Existing completion-checker tests and Skill quick validation pass as non-regression checks.
- AC-6: An independent Reviewer approves the exact immutable candidate and confirms accuracy, bilingual completeness, non-duplication, boundary preservation and version consistency.
- AC-7: Local installation and GitHub publication occur only after Human acceptance of the exact candidate; tag `v2.0.4` binds that accepted candidate.

