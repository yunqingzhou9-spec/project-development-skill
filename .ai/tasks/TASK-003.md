# TASK-003 — Provision reproducible Skill validation environment

```json
{
  "id": "TASK-003",
  "status": "READY",
  "spec": {"path": ".ai/specs/SPEC-003.md", "sha256": "1fc359f0227c1f44d49c24a13513168aaf0d7e36757838602616ec5c98245fbd"},
  "owner": "manager",
  "depends_on": [],
  "base": "602cf7b26c0e9c210757b6c9c60e520a034fbad3",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Assign a fresh Developer after committing the approved Spec and Task"
}
```

## Scope and acceptance

Implement approved `.ai/specs/SPEC-003.md` exactly. The deliverable is limited to a repository-local, ignored virtual environment; a tracked development dependency declaration; and accurate project commands. Acceptance is AC-1 through AC-5.

Verification profile: Static, Integration and Scenario are required. Unit is covered by the existing completion suite. Acceptance requires an independent Tester PASS and an independent Reviewer APPROVE for the exact candidate.

## Verification / findings

PENDING.

## Handoff / evidence

Manager created TASK-003 from the Human's explicit implementation instruction. Native Developer, Tester and Reviewer receipts will be recorded here.

## History / next action

- 2026-09-08T14:06:18+08:00 — Manager recorded SPEC-003 as APPROVED from the Human's “按你的建议执行” instruction and created this Task at READY.
- Next: commit the approved governance records, then assign a fresh Developer.
