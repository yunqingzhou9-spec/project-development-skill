# Project Development Skill

## 60 秒开始 / 60-second quick start

你只需说明想要的结果，不必先学习角色、状态或证据术语：

```text
$project-development 给这个项目添加 CSV 导出，并验证它可用。
```

Skill 会检查仓库、只澄清重要分歧，并自动选择流程：客观上小而低风险的单项改动使用 `LIGHTWEIGHT`；任何不满足或不确定的情况使用 `FULL`。它会安排真实 Developer 和独立 Reviewer，运行合适验证，再把准确候选版本交给你决定是否接受。安装和发布始终是另外的 Human 决定。

Just describe the outcome; you do not need to learn the roles, states, or evidence terms first:

```text
$project-development Add CSV export to this project and verify it works.
```

The Skill inspects the repository, asks only about consequential ambiguity, and selects the workflow: an objectively small, low-risk single change may use `LIGHTWEIGHT`; anything ineligible or uncertain uses `FULL`. It assigns a real Developer and independent Reviewer, runs suitable checks, and presents the exact candidate for your acceptance. Installation and publication always remain separate Human decisions.

`LIGHTWEIGHT` is limited to one independent outcome with no dependencies or integration, at most five enumerated files and 200 changed text lines, ordinary Git rollback, known targeted verification, independent implementation/review, no consequential unknowns, and no security, privacy, permissions, production, external-effect, billing/legal, compatibility, dependency, migration, destructive, release/install/publish, protected-acceptance, or conflict risk. Crossing any boundary escalates to `FULL`; it never relaxes candidate binding, independent Review, or Human authority.

# 中文

> **让 AI 不只是会写代码，而是能像一支受管理的软件团队一样完成项目。**

使用 AI 开发时，真正困难的往往不是“生成代码”，而是：**需求没想清楚、任务不会拆、多个 Agent 难协调、实现缺乏独立验证、返工过程混乱，以及到底什么时候才算真正完成。**

`project-development` 就是为了解决这些问题。

它在一个主窗口中保留常驻的 **Chief of Staff + Manager**：前者帮助 Human 澄清目标、范围和验收标准，后者将 `FULL` 的批准 Spec 或 `LIGHTWEIGHT` Task 内批准范围组织成工作，并按流程创建独立 Worker Agents，自动组织实现、验证、审查和返工。

```sql
Idea
→ Clarify the goal
→ Approve the criteria
→ Select FULL or LIGHTWEIGHT
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

It keeps a persistent **Chief of Staff + Manager** in one primary session: the Chief of Staff helps the Human clarify goals, scope, trade-offs, and acceptance criteria; the Manager coordinates a frozen approved Spec for `FULL` or inline approved Task scope for `LIGHTWEIGHT`, then creates the independent workers required to execute, verify, review, and rework it.

```sql
Idea
→ Clarify the goal
→ Approve the criteria
→ Select FULL or LIGHTWEIGHT
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
- Chief of Staff 将讨论整理成可审批的 `FULL` Spec 或 `LIGHTWEIGHT` Task 内范围。
- Manager 按 `FULL` 的 Approved Spec 或 `LIGHTWEIGHT` 的 Task 内批准范围协调任务。
- Developer 和 Reviewer 使用独立运行身份；`FULL` 功能工作还需要独立 Tester。
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

## 版本与发行身份

`SKILL.md` frontmatter 中的 `metadata.version` 是唯一权威的软件包版本。本仓库当前可使用开发版号；开发版号不表示已经发布。Working version、Human 已接受的 immutable baseline、source commit、历史 Git tag/GitHub Release、生成的安装包，以及本机 installed copy 是六个不同身份，必须分别核对，不能因数字相同而互相推断。

`SKILL.md` frontmatter `metadata.version` is the only authoritative package version. A development version is not a release claim. The working version, Human-accepted immutable baseline, source commit, historical Git tag/release, generated archive, and installed copy are six separate identities and must be verified independently.

## 构建干净安装包 / Build a clean installable archive

构建与校验都必须指定完整 source commit。命令只读取该 commit 的精确 runtime allowlist，加入 canonical manifest，并拒绝治理文件、额外/危险成员、符号链接、哈希或版本/commit 不一致，以及维护策略覆盖的已知本机路径、runtime UUID 和私钥标记。输出在 `dist/`，不会加入 Git。

结构清洁边界是：从 immutable source commit 读取的精确 allowlist，以及对照该 source 校验的 canonical manifest 哈希。针对已知项目 checkout、用户目录、本机系统路径、原生 runtime ID 和私钥标记的文本扫描只是 defense in depth；它不是对所有绝对路径语法或语义秘密的穷尽证明。

Both commands require the full source commit. The builder reads only the exact runtime allowlist from that commit, adds a canonical manifest, and rejects governance files, extra/unsafe members, symlinks, hash/version/commit mismatches, and maintained patterns for known local paths, runtime UUIDs, and private-key markers. `dist/` is ignored by Git.

The exact allowlist read from the immutable source commit plus canonical manifest hashes verified against that source is the structural cleanliness boundary. Maintained text scanning for known project checkout, user-home and local-system paths, native runtime IDs, and private-key markers is defense in depth. It is not exhaustive absolute-path recognition or semantic-secret proof.

```sh
python3 scripts/package_skill.py build --repo . \
  --source <FULL_SOURCE_COMMIT> --output dist/project-development.zip
python3 scripts/package_skill.py verify --repo . \
  --source <FULL_SOURCE_COMMIT> --archive dist/project-development.zip
```

The archive itself records the Skill name, package version, full source commit, and sorted SHA-256 for every runtime file in `project-development/MANIFEST.json`. GitHub-generated source archives are repository snapshots, not these clean installable artifacts.

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

目标已经明确并希望按 `FULL` 开始执行：

```text
$project-development 按已经批准的 Spec 开始执行，使用真实子 Agent，并把状态和证据写回仓库。
```

日常使用只需要一个主对话。Manager 在后台协调每个 Task 所需的 Developer、Tester 和 Reviewer；你不需要在多个窗口之间复制结果。

在未来使用更新后 Skill 的项目中，Manager 会在拆分每个新 Task 时根据实际内容或结果动态选择简短名称，并与稳定编号一起显示，例如 `TASK-001 — Layout adjustment`，同时记录匹配的 `layout_adjustment`。这只是示例，不是固定名称；其他 Task 可按实际结果命名为 `Player movement` / `player_movement` 或 `Collision detection` / `collision_detection`。平台支持自定义名称时，同一 Task 的所有 Worker 都复用其编号和用途 slug，再附加角色，例如 `task_001_layout_adjustment_developer`、`task_001_layout_adjustment_tester` 和 `task_001_layout_adjustment_reviewer`。用途名只是可读标签，平台返回的原生运行身份仍是权威记录；不会回头重命名当前或历史 Task、Agent 或证据。

In future projects using the updated Skill, the Manager dynamically chooses a concise name from each new Task's actual content or outcome during decomposition and displays it with the stable number, for example `TASK-001 — Layout adjustment`, while recording the matching `layout_adjustment` slug. That is an example, not a prescribed name: other outcomes might be `Player movement` / `player_movement` or `Collision detection` / `collision_detection`. When the host supports caller-selected names, every Worker for that Task reuses its number and purpose slug before the role, such as `task_001_layout_adjustment_developer`, `task_001_layout_adjustment_tester` and `task_001_layout_adjustment_reviewer`. The readable name is only a label; the native runtime identity returned by the host remains authoritative. Current and historical Tasks, Agents and evidence are never retrospectively renamed.

## 更换主窗口

提示词只是方便操作的入口，不是交接的权威记录。仓库中的 `AGENTS.md`、`PROJECT_STATE.md`、Task 和 Spec，以及平台可核验的原生运行状态，才是恢复和核对的依据；不要复制旧聊天来代替这些记录。

计划更换窗口时，可以把下面这段直接发给旧窗口：

```text
$project-development 准备交接当前项目。停止派发新任务。检查活动 Agent。核对 Project ID、本地仓库绝对路径、GitHub/远程 URL、稳定版本、分支、候选 commit、未提交变更、活动 Agent、阻塞项和下一步。把它们写回状态和 Task 记录。一致后将 coordination 标记为 READY_FOR_TAKEOVER。最后只返回一段已填好、可直接复制到新窗口的完整接管提示词。提示词必须包含上述全部信息。回复后停止协调。
```

旧窗口确认可接管后，把它返回的已填全提示词发给新窗口。下面的占位符模板展示完整格式：

```text
项目 ID：<PROJECT_ID>
本地仓库绝对路径：<ABSOLUTE_LOCAL_REPOSITORY_PATH>
GitHub/远程 URL：<GITHUB_OR_REMOTE_URL>
稳定版本：<CURRENT_STABLE_VERSION>
分支：<BRANCH>
候选 commit：<CANDIDATE_COMMIT>
未提交变更：<DIRTY_OR_UNTRACKED_CHANGES>
活动 Agent：<ACTIVE_AGENTS>
阻塞项：<BLOCKERS>
下一步：<NEXT_ACTION>

$project-development 接管上述项目。不要假定当前工作区是目标仓库。先检查上述绝对路径指向的 checkout。路径不存在或无法访问时，停止并请 Human 处理。再从该 checkout 读取 AGENTS.md、PROJECT_STATE.md、活动 Task，以及 `FULL` Task 的 frozen Approved Spec 或 `LIGHTWEIGHT` Task 的 inline approved scope。用上述信息核对仓库身份、范围和现场状态。以仓库记录和可核验的原生运行状态为准。信息缺失或冲突时，停止并请 Human 处理。先核实活动 Agent，再继续派发。不要复制或依赖旧聊天。不要重复派发可能仍在运行的任务。按已核对的下一步继续项目。
```

首次设置时，Project ID 按固定顺序确定：先复用项目已有的权威 ID；若没有，则使用用户明确提供的 ID；两者都没有时，Skill 生成一个易读且唯一的 ID。它必须同时记录在 `AGENTS.md` 和 `PROJECT_STATE.md`，在目录移动和主窗口交接后保持不变。如果两处记录、用户指定值或当前项目之间出现冲突，Skill 应停止并请你确认，不能猜测或重新生成。

同时进行多个项目时，应分别打开对应的仓库或工作区，并使用各自稳定的 `Project ID`。

## 验证

在仓库根目录运行：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/test_completion.py
.venv/bin/python scripts/test_package.py
.venv/bin/python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

后两个命令使用同一个仓库本地虚拟环境；`requirements-dev.txt` 提供 Skill 校验器需要的 PyYAML。

## 许可

[MIT License](LICENSE)
