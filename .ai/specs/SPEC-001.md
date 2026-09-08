# SPEC-001 — Clarify main-window handoff and Project ID creation

```json
{
  "id": "SPEC-001",
  "status": "APPROVED",
  "approval_ref": "User confirmation in the current Codex task on 2026-09-08; recorded as DEC-001"
}
```

## Goal / scope

Remove user-facing ambiguity around planned main-window handoff and initial Project ID assignment.

- Add copy-ready old-window and replacement-window prompts to `README.md`.
- State that repository records, not exact prompt wording or copied chat, are the handoff authority.
- Clarify the Project ID precedence and lifecycle: reuse an authoritative existing ID; otherwise use an explicit user-provided ID; otherwise the Skill generates a readable unique ID during first setup. Record it in both `AGENTS.md` and `PROJECT_STATE.md`, keep it stable across moves and handoffs, and stop on conflicts.
- Update relevant templates so setup placeholders reflect the same rule.
- Release the clarification as version `2.0.3` and document it in `CHANGELOG.md`.

## Non-goals / constraints

- Do not add an ID generator script or prescribe a host-specific randomness implementation.
- Do not rotate existing Project IDs; this project remains `PDP-SKILL`.
- Do not weaken role independence, candidate binding, state transitions, completion gates, formal acceptance, or publishing boundaries from version 2.0.2.
- Do not copy old chat as authoritative handoff state.
- Do not sync the installed Skill or push GitHub without separate user direction.
- Version 2.0.2 remains the governing and acceptance protocol for this work.

## Acceptance

- AC-1: `README.md` includes a copy-ready old-window prompt covering dispatch stop, active-agent inspection, repository write-back, `READY_FOR_TAKEOVER`, cessation of coordination, and a concise readiness response.
- AC-2: `README.md` includes a copy-ready replacement-window prompt containing the Project ID and repository-first recovery instructions.
- AC-3: Documentation says prompt wording is not authoritative; repository and native runtime evidence are.
- AC-4: Protocol and templates consistently express Project ID precedence, Skill generation when absent, dual recording, stability, and conflict handling; `PDP-SKILL` is not regenerated.
- AC-5: `SKILL.md` and the protocol identify version `2.0.3`, and `CHANGELOG.md` describes the change.
- AC-6: Existing completion-checker tests and the Skill quick validator pass.
- AC-7: An independent Tester and an independent Reviewer evaluate the exact final candidate; Reviewer explicitly checks role independence, state machine, acceptance gates, and safety/publishing boundaries.

