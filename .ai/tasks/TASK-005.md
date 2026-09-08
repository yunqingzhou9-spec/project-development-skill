# TASK-005 — Add descriptive Worker Agent names

```json
{
  "id": "TASK-005",
  "short_name": "agent_names",
  "status": "READY",
  "spec": {"path": ".ai/specs/SPEC-005.md", "sha256": "9c670d37e7a462a586c9d4e34b5abeb33b8d90344ef92f375fc13fd4cb3c518d"},
  "owner": "manager",
  "depends_on": [],
  "base": "6741a431a43252d77c7b7f5c997620c90fec36f4",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Assign fresh Developer task_005_agent_names_developer"
}
```

## Scope and acceptance

Implement frozen `.ai/specs/SPEC-005.md` exactly. Update only `references/PROTOCOL.md`, `templates/TASK.template.md`, `templates/PROJECT_STATE.template.md` and `README.md` unless a directly necessary regression test is identified. Preserve all historical Task, receipt and runtime identity bytes.

Verification profile: Static, Unit, Scenario and Acceptance are required. Integration is represented by a native naming forward check because the behavior is exercised through the host's Agent creation API. Independent Tester PASS and independent Reviewer APPROVE are required for the exact candidate.

## Verification / findings

PENDING.

## Handoff / evidence

Manager created TASK-005 from the Human's explicit optimization request. Runtime references will be recorded after dispatch.

## History / next action

- 2026-09-08T15:20:21+08:00 — Human requested descriptive Task/Agent naming beyond the numeric sequence; Manager recorded SPEC-005 as APPROVED and created TASK-005 at READY under DEC-015.
- Next: assign fresh Developer `task_005_agent_names_developer` against the frozen Spec and base.
