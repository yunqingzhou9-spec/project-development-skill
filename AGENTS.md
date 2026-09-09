# Project instructions

## Start here

Use `$project-development`. Read `PROJECT_STATE.md`, then only your assigned Task, its approved Spec and relevant links. This project authorizes task-scoped subagent delegation for approved execution, subject to host permissions. Discussion or setup alone does not authorize implementation.

If the skill is unavailable, report it; do not invent its rules or claim independent acceptance.

## Project

- Project ID / name: `PDP-SKILL / Project Development Protocol Skill`
- Repository identity / scope: `https://github.com/yunqingzhou9-spec/project-development-skill.git / .`
- Current local checkout: `<LOCAL_CHECKOUT>`
- Purpose / scope / exclusions: Maintain the repository-centered project governance Skill; it does not supply domain implementation capability or publishing authority.
- Domain rules / architecture: `SKILL.md`, `references/PROTOCOL.md`, `references/GATE.md`
- State: `PROJECT_STATE.md`
- Decisions: `DECISIONS.md`
- Specs / Tasks: `.ai/specs/` / `.ai/tasks/`
- Existing issues / roadmap / invalid history: `PROJECT_STATE.md`; none established at initialization.

## Team

Chief of Staff clarifies; Human approves; Manager dispatches and updates shared state. Developer implements; independent Tester verifies behavior when required; independent Reviewer checks correctness. Read only your role in the governing protocol version recorded by the active Task and Spec. Fresh workers across Tasks; one active Task per worker. Never treat roleplay or self-authored identities as independent evidence.

Only one main Manager coordinates the same project scope. For replacement or recovery, follow the Skill's main-window handoff protocol and verify `PDP-SKILL` before dispatching.

## Project settings

- Governing protocol: use the Strictly Accepted Baseline recorded in `PROJECT_STATE.md`; proposed rules in a working candidate do not govern their own acceptance.
- Verification: functional work requires independent Tester and Reviewer; pure documentation may use reasoned Test N/A but still requires independent Reviewer; high-risk work requires both.
- Rework: at most 3 failed verification cycles per Task.
- Runtime / receipt access / assurance: Codex task-agent tools are exposed; creation and result provenance remain `UNKNOWN` until first actual dispatch. Protected acceptance is `MISSING`. Maximum claim is `PROTOCOL` plus separately reported `STRUCTURAL` checks.
- Preferred host: Codex; apply the environment gate from the Strictly Accepted Baseline recorded in `PROJECT_STATE.md`.
- Formal acceptance authority: `HUMAN`; Manager reports eligibility, not approval.
- Shared-write isolation: Manager stages and integrates serialized changes; verification agents do not edit implementation.
- Release authority: explicit human authorization required. Never push GitHub or sync the installed Skill from implementation approval alone.

## Commands

- Create the local environment: `python3 -m venv .venv`
- Install development requirements: `.venv/bin/python -m pip install -r requirements-dev.txt`
- Tests: `.venv/bin/python scripts/test_completion.py`
- Skill validation: `.venv/bin/python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .`
- Completion gate: Python 3 plus the installed governing Skill `scripts/check_completion.py`; see its `references/GATE.md` at completion.
