# Project state

- Updated: <ISO time with timezone>
- Project ID / name: <same stable ID recorded in AGENTS.md: reuse authoritative existing ID; else explicit user ID; else Skill-generated readable unique ID> / <human-facing name>
- Repository identity / scope path: <remote or NONE> / <relative path such as . or apps/snake>
- Local checkout: <current host path; not the stable identity>
- Coordination: <ACTIVE / HANDOFF_PREPARING / READY_FOR_TAKEOVER / RECOVERY; Manager/session reference; updated time>
- Purpose / boundaries: <short summary>
- Working candidate: <commit/snapshot; disclose dirty or incomplete work>
- Strictly Accepted Baseline: UNESTABLISHED
- Historical documented acceptance: <reference or NONE>
- Active approved Specs: <path + digest>
- Runtime capabilities / assurance: <observed result references; PROTOCOL / STRUCTURAL / ENFORCED, or UNKNOWN>
- Environment: <CODEX / CHATGPT_WORK / OTHER / UNKNOWN; trusted host evidence; delegation/result access and protected acceptance VERIFIED / MISSING / UNKNOWN; scoped adaptation decision or NONE>
- Formal acceptance: <authority HUMAN by default; PENDING or actual candidate-specific human/service evidence; distinct from Task DONE>
- Next action: <one concrete next coordination action>

Keep Project ID stable across checkout moves and main-window handoffs. If this value conflicts with AGENTS, a user-provided ID or the selected project, record `CONFLICT`, stop and request resolution; do not guess or regenerate it.

## Active work (index; Task files own detailed state)

| Task / short name | State | Owner / runtime ID | Run status / native reference | Depends on | Next action |
|---|---|---|---|---|---|
| `.ai/tasks/TASK-001.md` — `snake_game` | READY | Manager / NONE | Not dispatched | NONE | Assign `task_001_snake_game_developer` |

## Blockers and decisions needed

List P0/P1 issues, unresolved conflicts, required human decisions and links; use NONE when established empty. Distinguish PROVISIONAL, UNVERIFIED and INVALID/DEPRECATED facts.

## Accepted / completed work

Link completed Tasks and immutable evidence. Do not reload their full reports during routine coordination.

## Release (when relevant)

NOT_RELEASED. Before changing: identify combined candidate, independent integration evidence, authorization, deployed artifact/environment, post-release checks and applicable rollback reference.
