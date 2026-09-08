# TASK-009 — Backup discovery cleanup

```json
{
  "id": "TASK-009",
  "short_name": "backup_discovery_cleanup",
  "status": "DOING",
  "spec": {"path": ".ai/specs/SPEC-008.md", "sha256": "0775b8345946b9db9e08fa9c7aebb2c4613c25cea3936451af227dd7fe514876"},
  "owner": "manager",
  "depends_on": ["TASK-008"],
  "base": "499fc99a2a79cde74bf948251838b03bad007027",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Developer moves the exact backup while preserving its bytes and verifies the discovery boundary."
}
```

## Scope and acceptance

Execute SPEC-008. The Developer owns only the exact backup move and preservation checks. The Manager serializes the `PROJECT_STATE.md` truth reconciliation and Git write-back. Fresh independent Tester and Reviewer verify the combined result.

## Verification / findings

- PENDING.

## Handoff / evidence

- User authorization: “先做1和2”.
- Source backup: `/Users/duolaamengmac/.codex/skills/project-development.backup-20260909T000444+0800-2.0.4-4547`.
- Destination backup: `/Users/duolaamengmac/.codex/backups/project-development/2.0.4-20260909T000444+0800-4547`.

## History / next action

- 2026-09-09: Created under DEC-023; Spec frozen at SHA-256 `0775b8345946b9db9e08fa9c7aebb2c4613c25cea3936451af227dd7fe514876`; moved to DOING.
