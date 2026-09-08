# TASK-004 — Make main-window handoff prompts self-locating

```json
{
  "id": "TASK-004",
  "status": "READY",
  "spec": {"path": ".ai/specs/SPEC-004.md", "sha256": "b7365083d284ce1ec1cc63f3094215e00cfc4c6ed9eaa28ca2cf23e7b7fb9ee6"},
  "owner": "manager",
  "depends_on": [],
  "base": "a32f23fa8c1014924b95779d5c98640bd6c043ca",
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

Implement frozen `.ai/specs/SPEC-004.md` exactly. Update only the reusable handoff guidance needed to satisfy AC-1 through AC-4; keep the prompt compact but complete. AC-5 requires regression checks. AC-6 requires independent scenario evaluation from an unrelated initial workspace.

Verification profile: Static, Unit, Scenario and Acceptance are required. Integration is N/A because no runtime integration or executable behavior changes. Independent Tester PASS and independent Reviewer APPROVE are required for the exact candidate.

## Verification / findings

PENDING.

## Handoff / evidence

Manager created TASK-004 from the Human's explicit implementation request. Native Developer, Tester and Reviewer receipts will be recorded here.

## History / next action

- 2026-09-08T14:32:00+08:00 — Manager recorded SPEC-004 as APPROVED and created TASK-004 at READY.
- Next: commit governance records, then assign a fresh Developer.
