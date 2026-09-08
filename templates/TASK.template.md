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

`FULL` is the default. Its ordinary functional work keeps `test_required:true` and requires independent Tester + Reviewer. Only after every objective eligibility condition passes may the Manager replace the metadata block above with this `LIGHTWEIGHT` variant (use a `json` fence in the instantiated Task); any false or uncertain condition stays or escalates to `FULL`:

```jsonc
{
  "id": "TASK-001",
  "short_name": "<matching lower_snake_case slug>",
  "profile": "LIGHTWEIGHT",
  "status": "READY",
  "approval_ref": "<durable reference to the Human's approved request>",
  "scope": {
    "outcome": "<one bounded outcome>",
    "acceptance": ["<observable criterion>"],
    "deliverables": ["<project-relative file>"],
    "verification": "<known targeted Developer command>",
    "eligibility": {
      "single_outcome": true,
      "no_dependencies_or_integration": true,
      "ordinary_git_rollback": true,
      "targeted_verification_known": true,
      "independent_implementer_and_reviewer": true,
      "risk_categories_absent": true,
      "no_conflict_or_unresolved_choice": true
    }
  },
  "scope_sha256": "<canonical scope digest from check_completion.py --scope-digest>",
  "owner": "manager",
  "depends_on": [],
  "base": "<full Git commit ID>",
  "candidate": null,
  "contributors": [],
  "test_required": false,
  "test_na_reason": "Eligible LIGHTWEIGHT change; Developer targeted verification plus fresh independent Review selected",
  "test": "N/A",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Assign task_001_<short_name>_developer"
}
```

For `FULL`, read the frozen approved Spec. For `LIGHTWEIGHT`, workers read the inline approved scope and its digest; no separate Spec exists. A LIGHTWEIGHT Developer must run the recorded targeted verification, and a fresh independent Reviewer is always required. Add a separate independent Tester when useful or escalate to `FULL` if eligibility changes.
