# TASK-007 — Clear and lightweight Skill

```json
{
  "id": "TASK-007",
  "short_name": "clear_lightweight_skill",
  "status": "DOING",
  "spec": {"path": ".ai/specs/SPEC-006.md", "sha256": "d57d15463f71f23aec19bfa600345afd24c7145af5026a80cd067ce18a1f6c1f"},
  "owner": "manager",
  "depends_on": ["TASK-006"],
  "base": "1daff6e007d419e553529b1fd6112e8c7a4459c8",
  "candidate": {"kind": "git", "commit": "02d381e2c03a0c3df2e59c77e812afb19442c363"},
  "contributors": ["/root/task_007_clear_lightweight_skill_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "FAIL",
  "review": "REJECT",
  "blockers": [],
  "rework_cycles": 1,
  "next_action": "Route the three candidate-bound verification findings to the same Developer for focused rework and produce a new candidate."
}
```

## Scope and acceptance

Implement SPEC-006 AC-2 through AC-7 using the minimal remediation design accepted from TASK-006. Preserve full-mode safeguards and all historical records. Verification profile requires an independent Tester and Reviewer.

## Verification / findings

- Developer self-checks: completion regressions 33/33 PASS; package regressions 9/9 PASS; Skill Creator validation PASS; Python compilation and `git diff --check` PASS.
- Developer deterministic-build check: two archives built from the candidate were byte-identical with SHA-256 `f3b3e1eccba5deac9b97b6f4a60b09fdf142c250aecef763fc6a2b55a06c26a9`; 14 members equal manifest plus 13 allowlisted files.
- Independent Test: FAIL for candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; the LIGHTWEIGHT checker ignores undeclared candidate files, and package leak scanning misses UUIDv7 runtime IDs and several concrete absolute-path forms.
- Independent Review: REJECT for the same two P1 issues plus a P2 issue: package version parsing is not uniquely bound to frontmatter `metadata.version`.

## Handoff / evidence

- Developer `/root/task_007_clear_lightweight_skill_developer`: native creation/assignment/result in current collaboration tree; DELIVERED candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; no installation, push, tag or release.

## History / next action

- 2026-09-08: Created from DEC-018; waiting on TASK-006.
- 2026-09-08: TASK-006 completed with Review APPROVE and structural receipt; dependency cleared.
- 2026-09-08: Developer delivered candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; moved to VERIFY.
- 2026-09-08: Fresh Tester FAIL and Reviewer REJECT on the exact candidate. Rework cycle 1 opened; old verdicts remain historical and cannot cover a new candidate.
