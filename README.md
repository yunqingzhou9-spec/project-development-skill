# Project Development Skill

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

## 它解决什么

- Human 决定目标、范围和关键取舍。
- Chief of Staff 将讨论整理成可审批的 Spec。
- Manager 按 Approved Spec 拆分和协调任务。
- Developer、Tester、Reviewer 使用独立运行身份工作。
- 项目状态、候选版本和证据保存在仓库中，而不是依赖聊天记忆。
- 完成检查绑定 Git commit 或文件哈希，避免旧测试或旧审查被用于新候选版本。

## 能力边界

本 Skill 规定协作协议，但不提供业务实现能力，也不自行创建平台缺少的子 Agent、权限、CI 或发布系统。只有运行环境实际提供创建、派工和结果追踪能力时，才能进行真实的多 Agent 协作；否则会明确报告缺失并暂停相关阶段。

`scripts/check_completion.py` 只检查所提供证据的结构一致性，不认证运行记录，也不等同于受保护的自动验收。正式验收默认仍由人类对指定候选版本作出，发布或外部操作需要单独授权。

## 目录

```text
project-development-skill/
├── SKILL.md                  # Skill 入口与核心约束
├── agents/openai.yaml        # Codex 展示信息
├── references/PROTOCOL.md    # 角色、状态、交接与执行协议
├── references/GATE.md        # 完成条件与证据格式
├── scripts/                  # 结构检查器及其测试
└── templates/                # 最小项目治理模板
```

## 安装

在 Codex 中调用 `$skill-installer`，并提供仓库地址：

```text
$skill-installer 请从 https://github.com/yunqingzhou9-spec/project-development-skill 安装仓库根目录，并将 Skill 命名为 project-development。
```

安装完成后，在下一次对话中即可使用。若本机已经存在同名 Skill，请先自行决定是保留还是替换；安装器不会直接覆盖现有目录。

## 基本使用

首次进入一个项目：

```text
$project-development 请和我澄清目标，形成 Spec；在我批准前不要实现。
```

目标已经明确并希望开始执行：

```text
$project-development 按已经批准的 Spec 开始执行，使用真实子 Agent，并把状态和证据写回仓库。
```

日常使用只需要一个主对话。Manager 在后台协调不同 Task 的 Developer、Tester 和 Reviewer；你不需要在多个窗口之间复制结果。

## 更换主窗口

提示词只是方便操作的入口，不是交接的权威记录。仓库中的 `AGENTS.md`、`PROJECT_STATE.md`、Task 和 Spec，以及平台可核验的原生运行状态，才是恢复和核对的依据；不要复制旧聊天来代替这些记录。

计划更换窗口时，可以把下面这段直接发给旧窗口：

```text
$project-development 准备把当前项目交接到新的主窗口。请停止派发新任务，检查所有活动 Agent，把 Project ID、仓库/工作区、分支、候选 commit、未提交变更、活动 Agent、阻塞项和准确的下一步写回仓库中的状态与 Task 记录；确认信息一致后将 coordination 标记为 READY_FOR_TAKEOVER，并停止继续协调。最后只需简洁回复是否已可接管，以及 Project ID 和下一步。
```

旧窗口确认可接管后，在 Codex 中打开或选择同一个仓库，把下面这段发给新窗口，并把 `<PROJECT_ID>` 替换成仓库已记录的稳定 ID：

```text
$project-development 接管项目 <PROJECT_ID>。请以仓库记录为先，从 AGENTS.md、PROJECT_STATE.md、活动 Task 及其 Approved Spec 恢复；核对 Project ID、仓库身份与范围、实际工作区、分支、commit、未提交变更和原生活动 Agent 状态，解决记录与现场差异后再继续。不要依赖或复制旧聊天，也不要重复派发仍可能运行的任务。
```

首次设置时，Project ID 按固定顺序确定：先复用项目已有的权威 ID；若没有，则使用用户明确提供的 ID；两者都没有时，Skill 生成一个易读且唯一的 ID。它必须同时记录在 `AGENTS.md` 和 `PROJECT_STATE.md`，在目录移动和主窗口交接后保持不变。如果两处记录、用户指定值或当前项目之间出现冲突，Skill 应停止并请你确认，不能猜测或重新生成。

同时进行多个项目时，应分别打开对应的仓库或工作区，并使用各自稳定的 `Project ID`。

## 验证

在仓库根目录运行：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/test_completion.py
.venv/bin/python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

后两个命令使用同一个仓库本地虚拟环境；`requirements-dev.txt` 提供 Skill 校验器需要的 PyYAML。

## 许可

[MIT License](LICENSE)
