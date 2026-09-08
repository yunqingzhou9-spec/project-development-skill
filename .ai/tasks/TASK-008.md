# TASK-008 — Local Skill synchronization

```json
{
  "id": "TASK-008",
  "short_name": "local_skill_sync",
  "status": "DOING",
  "spec": {"path": ".ai/specs/SPEC-007.md", "sha256": "4e9f04950791572dfca380a4e722fcbd31daa3d26f87a41092fb5d0225bfcc77"},
  "owner": "manager",
  "depends_on": ["TASK-007"],
  "base": "3ff3e5b8239d92f4847dcd37625865975761480d",
  "candidate": {"kind": "git", "commit": "3ff3e5b8239d92f4847dcd37625865975761480d"},
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Developer builds and verifies the exact accepted archive, preserves the existing installation as a backup, and synchronizes the local Skill without publication."
}
```

## Scope and acceptance

Execute SPEC-007. This is a stateful local installation Task, so use the FULL workflow with separate Developer, Tester and Reviewer identities. The immutable Git candidate is the installation source; the installed manifest, file hashes and recorded backup path bind the non-Git output.

## Verification / findings

- PENDING.

## Handoff / evidence

- User authorization: “同步到本机并验证，暂不发布”.
- Accepted source: `3ff3e5b8239d92f4847dcd37625865975761480d` under DEC-021.

## History / next action

- 2026-09-09: Created under DEC-022; Spec frozen at SHA-256 `4e9f04950791572dfca380a4e722fcbd31daa3d26f87a41092fb5d0225bfcc77`; moved to DOING for Developer dispatch.
