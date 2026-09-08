# Project instructions

## Start here

Use `$project-development`. Read `PROJECT_STATE.md`, then only your Task, its approved Spec and relevant links. This project authorizes task-scoped subagent delegation for approved execution, subject to host permissions. Discussion/setup alone does not authorize implementation.

If the skill is unavailable, report it; do not invent its rules or claim independent acceptance. A project-local copy may be linked here when the host cannot discover installed skills.

## Project

- Project ID / name: `<reuse authoritative existing ID; else explicit user ID; else Skill-generated readable unique ID> / <human-facing name>`
- Repository identity / scope: `<remote or NONE> / <relative scope path>`
- Current local checkout: `<host-specific path; may change>`
- Purpose / scope / exclusions: <fill>
- Domain rules / architecture: <links or explicit unknown>
- State: `PROJECT_STATE.md`
- Decisions: `DECISIONS.md`
- Specs / Tasks: `.ai/specs/` / `.ai/tasks/`
- Existing issues / roadmap / invalid history: <reuse links, or state sections>

## Team

Chief of Staff clarifies; Human approves; Manager dispatches and updates shared state. Developer implements; independent Tester verifies behavior; independent Reviewer checks correctness. Read only your role in the skill protocol. Fresh workers across Tasks; one active Task per worker. Never treat roleplay or self-authored identities as independent evidence.

Only one main Manager coordinates the same project scope. For replacement or recovery, follow the skill's main-window handoff protocol and verify the Project ID before dispatching.

Record the same Project ID here and in `PROJECT_STATE.md`. Keep it stable across checkout moves and main-window handoffs. If authoritative records, a user-provided ID or the selected project conflict, stop and ask the user to resolve the conflict; do not guess or regenerate it.

## Project settings

- Verification: functional work = test + review; pure docs = review + reasoned test N/A; high risk = both + integration acceptance.
- Rework: at most 3 failed verification cycles per Task.
- Runtime / receipt access / assurance: <observed tools; unknown until checked>
- Preferred hosts: Codex / ChatGPT Work; run the skill's environment gate. Other/unknown host adaptation requires an explicit scoped user decision.
- Formal acceptance authority: HUMAN; Manager reports eligibility, not approval. PROTECTED_SERVICE requires verified protected controls and a recorded authority decision.
- Shared-write isolation: <serial ownership or supported worktrees>
- Release authority and applicable checks: <existing policy or human decision required>

## Commands

- Setup: <command or UNVERIFIED>
- Static / unit / integration / scenario: <commands or reasoned N/A>
- Completion gate: Python 3 + installed skill `scripts/check_completion.py`; see its `references/GATE.md` only at completion.
