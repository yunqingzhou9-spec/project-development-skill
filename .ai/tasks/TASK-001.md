# TASK-001 — Clarify handoff prompts and Project ID lifecycle

```json
{
  "id": "TASK-001",
  "status": "READY",
  "spec": {"path": ".ai/specs/SPEC-001.md", "sha256": "9650653205f6e1141c5774b6819aaa7e3a7cc2c3673ed5c937659aa98867e590"},
  "owner": "manager",
  "depends_on": [],
  "base": "4228450dda18b9726a4c559efc61d73844a4487d",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Manager implements the approved documentation and metadata changes, then freezes a candidate for independent verification"
}
```

## Scope and acceptance

Implement SPEC-001 AC-1 through AC-7. The work is protocol-sensitive, so the verification profile requires an independent Tester and an independent Reviewer. The governing rules remain version 2.0.2. Publishing and installed-Skill synchronization are excluded.

## Verification / findings

PENDING. Required checks include the existing completion-checker tests, Skill quick validation, acceptance-criteria inspection, and independent review of role independence, state transitions, completion gates, and safety/publishing boundaries.

## Handoff / evidence

Base: Git commit `4228450dda18b9726a4c559efc61d73844a4487d`. Candidate and native agent receipts will be recorded after implementation is frozen.

## History / next action

- 2026-09-08: Created from approved SPEC-001 under the version 2.0.2 protocol.
- Next: implement the bounded change and identify the exact candidate.
