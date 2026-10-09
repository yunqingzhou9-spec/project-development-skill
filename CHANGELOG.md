# Changelog

## [2.4.0] - 2026-10-09

- 按风险、可逆性、耦合和不确定性选择工作量；低风险改动允许主智能体实施并做针对性自检，高风险工作保留分别独立的行为验证与审查。
- 新增精简的同机空闲交接流程：定向核实写入者，固定辅助程序一次完成安全检查、协调权转换及结果复核，保留所有未提交内容。
- 使用稳定机器标识，避免网络主机名变化阻断同机协调；旧登记仅在明确授权和核验后迁移，并保留备份及审计。
- 核对 Git 可见的未提交文件原始字节和模式，拒绝不适用的 WAL 只读登记；未解决尝试、身份不确定和交接指纹不一致仍阻止接管。
- 增加本地阶段计时和可选私有回执，区分本地耗时、权限/模型等待与端到端耗时。10 秒是优化目标，超过 1 分钟排查原因，时间本身不会触发中断或削弱检查。
- 更新中文 README、交接提示词及安装说明；发布包沿用精确运行文件列表和绑定不可变源码提交的清单，不包含当前项目状态及私人运行记录。

## [2.3.0] - 2026-09-23

- 新增目标澄清与确认门：先判断请求是否合理、清晰、可执行，帮助用户明确目标、边界和完成标准，待用户确认当前方案后再实施。
- 在确定实现方向前按需检查 GitHub 与现有生态，比较直接复用、适配和自行实现，且确认前仅进行只读研究。
- 将用户界面名称改为“许愿机（测试版）”，保留内部 Skill 名称和调用方式 `project-development`。

## [2.2.0] - 2026-09-09

- 按任务需要选择流程和子智能体，减少简单改动的操作与等待。
- 增加简洁工作记录、同机窗口协调与可核对来源的安装工具。
- 保留历史工作记录的检查能力，明确检查、验收、安装与发布的区别。
- 重写中文 README：许愿机（测试版）、通用安装提示词、明确分工、窗口交接与免责声明。

## [2.1.0] - 2026-09-09

- Clarify package, source, accepted-baseline, tag, artifact and installed-copy identities; the working package version is sourced only from `SKILL.md` metadata.
- Add a deterministic allowlisted archive builder/verifier with a canonical source-bound manifest and leak/safety checks.
- Add a bilingual beginner quick start and an objectively bounded LIGHTWEIGHT workflow while preserving FULL safeguards and Human authority.
- Extend completion checks, templates and regression coverage for inline scope digests and lightweight eligibility.

## [2.0.4] - 2026-09-08

- 在 README 开头增加完整的中英双语 Skill 介绍、协作流程和标语。
- 保留现有的详细功能列表和能力边界说明，不改变协作协议语义。

## [2.0.3] - 2026-09-08

- 增加可直接复制的旧窗口交接准备提示词和新窗口接管提示词。
- 明确提示词与复制的聊天不是权威交接状态，应以仓库记录和可核验的原生运行证据为准。
- 明确 Project ID 的来源优先级、首次缺省生成、双处记录、跨移动与交接稳定性，以及冲突时停止处理的规则。

## [2.0.2] - 2026-09-07

首次公开候选版本。

- 提供面向通用项目的轻量仓库治理流程。
- 支持 Approved Spec、Task 状态机和项目状态恢复。
- 规定 Developer、Tester、Reviewer 的独立身份与交接证据。
- 支持以 Git commit 或文件哈希绑定候选版本。
- 提供结构化完成检查器、测试和最小项目模板。
- 区分 Task 完成、正式验收和实际发布。
