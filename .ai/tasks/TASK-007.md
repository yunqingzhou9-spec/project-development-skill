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
  "candidate": {"kind": "git", "commit": "4fabd192ceb17ea38f5b9311e07d879b8ec0f020"},
  "contributors": ["/root/task_007_clear_lightweight_skill_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "FAIL",
  "review": "REJECT",
  "blockers": [],
  "rework_cycles": 2,
  "next_action": "Route rework-cycle-1 findings to the same Developer, unify LIGHTWEIGHT instructions, complete path rejection and remove the extra template."
}
```

## Scope and acceptance

Implement SPEC-006 AC-2 through AC-7 using the minimal remediation design accepted from TASK-006. Preserve full-mode safeguards and all historical records. Verification profile requires an independent Tester and Reviewer.

## Verification / findings

- Developer self-checks: completion regressions 33/33 PASS; package regressions 9/9 PASS; Skill Creator validation PASS; Python compilation and `git diff --check` PASS.
- Developer deterministic-build check: two archives built from the candidate were byte-identical with SHA-256 `f3b3e1eccba5deac9b97b6f4a60b09fdf142c250aecef763fc6a2b55a06c26a9`; 14 members equal manifest plus 13 allowlisted files.
- Independent Test: FAIL for candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; the LIGHTWEIGHT checker ignores undeclared candidate files, and package leak scanning misses UUIDv7 runtime IDs and several concrete absolute-path forms.
- Independent Review: REJECT for the same two P1 issues plus a P2 issue: package version parsing is not uniquely bound to frontmatter `metadata.version`.
- Rework cycle 1 Developer self-checks for candidate `4fabd192ceb17ea38f5b9311e07d879b8ec0f020`: completion tests 38/38 PASS; package tests 15/15 PASS; quick validation, compilation and diff check PASS; deterministic archive SHA-256 `56ecea924c9891165fa0a5c64578a87187402b53cc02d74a0242fb6246efb3e0`.
- Fresh independent Test and Review: PENDING; old candidate verdicts are stale.
- Rework-cycle-1 Test: FAIL because a normal Windows user path remained accepted by package leak scanning.
- Rework-cycle-1 Review: REJECT because additional `/var/folders`, `/Volumes` and exact Windows paths remained accepted; FULL/LIGHTWEIGHT Tester and Spec-reading instructions contradicted each other; setup still claimed five templates while packaging a sixth.

## Handoff / evidence

- Developer `/root/task_007_clear_lightweight_skill_developer`: native creation/assignment/result in current collaboration tree; DELIVERED candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; no installation, push, tag or release.

## History / next action

- 2026-09-08: Created from DEC-018; waiting on TASK-006.
- 2026-09-08: TASK-006 completed with Review APPROVE and structural receipt; dependency cleared.
- 2026-09-08: Developer delivered candidate `02d381e2c03a0c3df2e59c77e812afb19442c363`; moved to VERIFY.
- 2026-09-08: Fresh Tester FAIL and Reviewer REJECT on the exact candidate. Rework cycle 1 opened; old verdicts remain historical and cannot cover a new candidate.
- 2026-09-08: Same Developer delivered rework candidate `4fabd192ceb17ea38f5b9311e07d879b8ec0f020`, fixing all three findings and adding adversarial regressions; moved to VERIFY with fresh identities required.
- 2026-09-08: Fresh rework Tester FAIL and Reviewer REJECT. Rework cycle 2 opened; candidate `4fabd192ceb17ea38f5b9311e07d879b8ec0f020` and its verdicts are stale for any later candidate.
