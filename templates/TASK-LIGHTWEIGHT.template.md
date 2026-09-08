# TASK-001 — <concise low-risk outcome>

```json
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
    "verification": "<known targeted command>",
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
  "test_na_reason": "Eligible LIGHTWEIGHT change; targeted Developer verification plus independent Review selected",
  "test": "N/A",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Assign task_001_<short_name>_developer"
}
```

## Verification / findings

<Developer command/result and independent Reviewer report, both bound to the scope digest and exact candidate. Add a separate independent Tester whenever useful; if risk or uncertainty grows, escalate to FULL before continuing.>

## Handoff / history

<Candidate, native worker/result references, meaningful checkpoint, blockers and next action. Do not create a commit for every transient status.>
