# TASK-001 — <concise outcome, e.g. Layout adjustment>

```json
{
  "id": "TASK-001",
  "short_name": "<matching lower-snake-case slug, e.g. layout_adjustment>",
  "profile": "FULL",
  "status": "READY",
  "spec": {"path": ".ai/specs/SPEC-001.md", "sha256": "<approved file digest>"},
  "owner": "manager",
  "depends_on": [],
  "base": "<commit or snapshot reference>",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Assign task_001_<short_name>_developer after checking approval and runtime capability"
}
```

## Scope and acceptance

<This Task's outcome, exclusions, AC references and verification profile selected before implementation. Dependencies if any must be accepted before dispatch.>

## Verification / findings

<Static, unit, integration, scenario, acceptance: commands, observed results, N/A reasons; classify failures. Reviewer checks criteria and assumptions independently.>

## Handoff / evidence

<Developer/Test/Review report links, native creation/assignment/result references and candidate identity. The title and slug above are dynamically chosen from this Task's outcome; `Layout adjustment` / `layout_adjustment` is only an example. Where the host supports caller-selected names, reuse the same slug in names such as `task_001_layout_adjustment_developer`, `task_001_layout_adjustment_tester` and `task_001_layout_adjustment_reviewer`; native returned identities remain authoritative. Small reports live here. Large reports and completion receipts are linked only when needed.>

## History / next action

<Meaningful transitions, rework, remaining blockers and exact next action. Manager owns state updates; preserve old evidence when a candidate changes.>

`FULL` is the default. Use `TASK-LIGHTWEIGHT.template.md` only after every objective eligibility condition passes; any false or uncertain condition stays `FULL`.
