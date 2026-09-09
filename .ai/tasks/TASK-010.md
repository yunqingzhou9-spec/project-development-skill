# TASK-010 — Finalize 2.1.0 release

```json
{
  "id": "TASK-010",
  "short_name": "finalize_2_1_0_release",
  "status": "DOING",
  "spec": {"path": ".ai/specs/SPEC-009.md", "sha256": "d084aababfc04cf6a980b097a43c45fd1752fe77d45baff5e052c322650e5490"},
  "owner": "manager",
  "depends_on": ["TASK-007", "TASK-008", "TASK-009"],
  "base": "23c40a910a8f35232e459c794ac27891dac8e79d",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Developer creates the bounded 2.1.0 release candidate and deterministic archive without installation or publication."
}
```

## Scope and acceptance

Execute SPEC-009 as a FULL release workflow. Candidate creation and verification precede the candidate-specific Human acceptance gate. No remote publication or final installed-Skill replacement occurs before that gate.

## Verification / findings

- PENDING.

## Handoff / evidence

- Human release authorization: “1、2、3、4确认都满意，正式发布吧”.
- Accepted functional source: `3ff3e5b8239d92f4847dcd37625865975761480d` (`2.1.0-dev.1`).
- Pre-release repository snapshot after fetch: local `main` at `23c40a910a8f35232e459c794ac27891dac8e79d`, `origin/main` at `d9ad8e4a3d878787a07703927e270fba700ebc35`, remote is an ancestor, worktree clean, and local `v2.1.0` absent.
- Existing published tag `v2.0.4` resolves to `912ec892395572447462ce7e0924ab149735f794` and must remain unchanged.

## History / next action

- 2026-09-09: Created under DEC-024 after Human confirmed the local cleanup, real-use test and release decision; Spec frozen at SHA-256 `d084aababfc04cf6a980b097a43c45fd1752fe77d45baff5e052c322650e5490`; moved to DOING.
