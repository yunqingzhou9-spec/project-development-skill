# TASK-010 — Finalize 2.1.0 release

```json
{
  "id": "TASK-010",
  "short_name": "finalize_2_1_0_release",
  "status": "BLOCKED",
  "spec": {"path": ".ai/specs/SPEC-009.md", "sha256": "d084aababfc04cf6a980b097a43c45fd1752fe77d45baff5e052c322650e5490"},
  "owner": "manager",
  "depends_on": ["TASK-007", "TASK-008", "TASK-009"],
  "base": "23c40a910a8f35232e459c794ac27891dac8e79d",
  "candidate": {"kind": "git", "commit": "1c4f2f9a10d735cb506ebc90f143d8cec801e66c"},
  "contributors": ["/root/task_010_finalize_2_1_0_release_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PASS",
  "review": "APPROVE",
  "blockers": ["Human candidate-specific acceptance required for release candidate 1c4f2f9a10d735cb506ebc90f143d8cec801e66c and archive SHA-256 cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd before installation or publication."],
  "rework_cycles": 0,
  "next_action": "Human accepts or rejects the exact candidate and archive; on acceptance, Manager refreshes remote state, synchronizes the installed Skill, publishes only main/v2.1.0/GitHub Release, and post-verifies."
}
```

## Scope and acceptance

Execute SPEC-009 as a FULL release workflow. Candidate creation and verification precede the candidate-specific Human acceptance gate. No remote publication or final installed-Skill replacement occurs before that gate.

## Verification / findings

- Candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c` changes only `SKILL.md`, `CHANGELOG.md`, `README.md` and version-dependent `scripts/test_package.py` from its release-preparation parent `164511e224b19b58d8d7dfcdac0891c21dfa09b2`; TASK base `23c40a910a8f35232e459c794ac27891dac8e79d` to candidate additionally contains the four authorized release-governance files.
- Developer self-check: completion tests 38/38 PASS; package tests 20/20 PASS; Skill quick validation, Python compilation and diff checks PASS.
- Developer deterministic builds: two 34,297-byte archives are byte-identical with SHA-256 `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd`; both verify as version `2.1.0`, source commit `1c4f2f9a10d735cb506ebc90f143d8cec801e66c`, 12 allowlisted runtime files plus canonical manifest.
- Independent Tester `/root/task_010_finalize_2_1_0_release_tester`: PASS for pre-release AC-1 through AC-5 and release-readiness boundaries; independently rebuilt the identical archive and preserved AC-6/7/9/10 as uncompleted.
- Independent Reviewer `/root/task_010_finalize_2_1_0_release_reviewer`: APPROVE with no P0/P1 findings. Its P2 comparison-wording finding was corrected above without changing the product candidate; it independently reproduced the same archive and confirmed no early installation or publication.
- Pre-release completion gate: `.ai/evidence/TASK-010.json` returned `STRUCTURAL / CONSISTENT`; Manager verified native creation, assignments and final results. AC-6 through AC-10 remain deliberately uncompleted.

## Handoff / evidence

- Human release authorization: “1、2、3、4确认都满意，正式发布吧”.
- Accepted functional source: `3ff3e5b8239d92f4847dcd37625865975761480d` (`2.1.0-dev.1`).
- Pre-release repository snapshot after fetch: local `main` at `23c40a910a8f35232e459c794ac27891dac8e79d`, `origin/main` at `d9ad8e4a3d878787a07703927e270fba700ebc35`, remote is an ancestor, worktree clean, and local `v2.1.0` absent.
- Existing published tag `v2.0.4` resolves to `912ec892395572447462ce7e0924ab149735f794` and must remain unchanged.
- Developer `/root/task_010_finalize_2_1_0_release_developer`: native creation/assignment/result in the current collaboration tree; delivered exact candidate and two deterministic archives without installation or publication.
- Tester `/root/task_010_finalize_2_1_0_release_tester`: native creation/assignment/result in the current collaboration tree; PASS with no edits.
- Reviewer `/root/task_010_finalize_2_1_0_release_reviewer`: native creation/assignment/result in the current collaboration tree; APPROVE with no implementation edits.
- Candidate archive paths: `/private/tmp/task-010-release/project-development-2.1.0-build-1.zip` and `/private/tmp/task-010-release/project-development-2.1.0-build-2.zip`.

## History / next action

- 2026-09-09: Created under DEC-024 after Human confirmed the local cleanup, real-use test and release decision; Spec frozen at SHA-256 `d084aababfc04cf6a980b097a43c45fd1752fe77d45baff5e052c322650e5490`; moved to DOING.
- 2026-09-09: Developer delivered candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c` and deterministic clean archive evidence; moved to VERIFY with fresh identities required.
- 2026-09-09: Fresh Tester PASS and Reviewer APPROVE received for the exact candidate. Reviewer P2 governance-comparison wording was corrected; structural gate and Human candidate-specific acceptance remain pending.
- 2026-09-09: Pre-release structural gate returned CONSISTENT. Task moved to BLOCKED solely for Human acceptance of the exact candidate and archive before any installation or remote mutation.
