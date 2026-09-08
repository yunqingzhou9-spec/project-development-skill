# Project Development Skill

一个轻量、通用、以仓库为项目记忆的 Codex Skill。它帮助你在一个主对话中完成需求澄清、Spec 审批、任务拆解、子 Agent 协作、独立测试与审查，以及可恢复的项目交接。

适用于软件、数据、自动化和 AI 项目，不包含任何特定业务领域规则。

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

先让旧窗口把状态写回仓库并标记可接管。然后在 Codex 中打开或选择同一个仓库，在新窗口明确指定项目的 `Project ID`：

```text
$project-development 接管项目 <PROJECT_ID>。请从 AGENTS.md 和 PROJECT_STATE.md 恢复，核对仓库、工作区和活动任务后继续；不要依赖或复制旧聊天。
```

同时进行多个项目时，应分别打开对应的仓库或工作区，并使用各自稳定的 `Project ID`。如果项目身份与当前仓库不匹配，Skill 应停止并请你确认，不能猜测。

## 验证

在仓库根目录运行：

```sh
python3 scripts/test_completion.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

第二个命令使用 Codex 自带的 Skill 校验器。如果当前 Python 环境缺少 PyYAML，应说明 `quick_validate` 尚未完成，并在隔离环境中安装或提供 PyYAML 后再运行；不要为此自动修改项目依赖。

## 许可

[MIT License](LICENSE)
