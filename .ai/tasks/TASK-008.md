# TASK-008 — Local Skill synchronization

```json
{
  "id": "TASK-008",
  "short_name": "local_skill_sync",
  "status": "VERIFY",
  "spec": {"path": ".ai/specs/SPEC-007.md", "sha256": "4e9f04950791572dfca380a4e722fcbd31daa3d26f87a41092fb5d0225bfcc77"},
  "owner": "manager",
  "depends_on": ["TASK-007"],
  "base": "3ff3e5b8239d92f4847dcd37625865975761480d",
  "candidate": {"kind": "git", "commit": "3ff3e5b8239d92f4847dcd37625865975761480d"},
  "contributors": ["/root/task_008_local_skill_sync_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Fresh independent Tester and Reviewer verify the installed state, exact source binding, backup and no-publication boundary."
}
```

## Scope and acceptance

Execute SPEC-007. This is a stateful local installation Task, so use the FULL workflow with separate Developer, Tester and Reviewer identities. The immutable Git candidate is the installation source; the installed manifest, file hashes and recorded backup path bind the non-Git output.

## Verification / findings

- Developer self-check: two exact-source archives were byte-identical with SHA-256 `74920397033b299f77d16a20aa9f649c6fb0b11045bb826ee4a416d282a51c69`; archive verification PASS.
- Installed state: version `2.1.0-dev.1`, 13 exact archive members, archive-to-installed byte equality PASS, manifest source commit matches `3ff3e5b8239d92f4847dcd37625865975761480d`, no stale test or repository governance files.
- Developer checks: installed verifier PASS; Skill Creator quick validation PASS; completion tests 38/38 PASS; package tests 20/20 PASS.
- Independent Test and Review: PENDING.

## Handoff / evidence

- User authorization: “同步到本机并验证，暂不发布”.
- Accepted source: `3ff3e5b8239d92f4847dcd37625865975761480d` under DEC-021.
- Developer `/root/task_008_local_skill_sync_developer`: native creation/assignment/result in the current collaboration tree.
- Built archive: `/private/tmp/task-008-local-skill-sync.xXwwn2/project-development.zip`.
- Retained backup: `/Users/duolaamengmac/.codex/skills/project-development.backup-20260909T000444+0800-2.0.4-4547`.

## History / next action

- 2026-09-09: Created under DEC-022; Spec frozen at SHA-256 `4e9f04950791572dfca380a4e722fcbd31daa3d26f87a41092fb5d0225bfcc77`; moved to DOING for Developer dispatch.
- 2026-09-09: Developer installed the verified accepted archive after preserving the 2.0.4 backup and delivered passing self-checks; moved to VERIFY with fresh Tester and Reviewer required.
