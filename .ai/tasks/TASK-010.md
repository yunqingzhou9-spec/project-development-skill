# TASK-010 — Finalize 2.1.0 release

```json
{
  "id": "TASK-010",
  "short_name": "finalize_2_1_0_release",
  "status": "DOING",
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
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Complete the sanitized governance closure under TASK-011; the accepted 2.1.0 product release and local installation are already verified."
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
- Pre-release completion gate: `.ai/evidence/TASK-010.json` returned `STRUCTURAL / CONSISTENT`; Manager verified native creation, assignments and final results. At that checkpoint AC-6 through AC-10 were deliberately uncompleted; the later entries below record their completion.
- AC-6 complete: Human accepted exact candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c` and archive SHA-256 `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd` under DEC-025 and instructed publication.
- AC-7 complete: local installed Skill is exact `2.1.0` archive content bound to the accepted candidate; independent Tester PASS, quick validation PASS and installed verifier VERIFIED. Recoverable `2.1.0-dev.1` backup retained at `<CODEX_BACKUPS>/project-development/2.1.0-dev.1-20260909T101834+0800-task-010`; earlier 2.0.4 backup remains intact.
- AC-8 complete: refreshed remote state allowed a non-force, explicit `main` push; annotated tag `v2.1.0` was created and resolves to exact accepted candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c`. Existing `v2.0.4` remains unchanged.
- AC-9 complete: GitHub Release `v2.1.0` is live with clean asset `project-development-2.1.0.zip`; the downloaded asset is byte-identical to the accepted archive and has SHA-256 `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd`.
- AC-10 product checks complete: remote release/tag identity, installed version and artifact identity are verified. Publication governance closure continues separately under TASK-011 so rejected raw-path commits are never published.

## Handoff / evidence

- Human release authorization: “1、2、3、4确认都满意，正式发布吧”.
- Accepted functional source: `3ff3e5b8239d92f4847dcd37625865975761480d` (`2.1.0-dev.1`).
- Pre-release repository snapshot after fetch: local `main` at `23c40a910a8f35232e459c794ac27891dac8e79d`, `origin/main` at `d9ad8e4a3d878787a07703927e270fba700ebc35`, remote is an ancestor, worktree clean, and local `v2.1.0` absent.
- Existing published tag `v2.0.4` resolves to `912ec892395572447462ce7e0924ab149735f794` and must remain unchanged.
- Developer `/root/task_010_finalize_2_1_0_release_developer`: native creation/assignment/result in the current collaboration tree; delivered exact candidate and two deterministic archives without installation or publication.
- Tester `/root/task_010_finalize_2_1_0_release_tester`: native creation/assignment/result in the current collaboration tree; PASS with no edits.
- Reviewer `/root/task_010_finalize_2_1_0_release_reviewer`: native creation/assignment/result in the current collaboration tree; APPROVE with no implementation edits.
- Candidate archive paths: `<TEMP_DIR>/task-010-release/project-development-2.1.0-build-1.zip` and `<TEMP_DIR>/task-010-release/project-development-2.1.0-build-2.zip`.
- Release asset path: `<TEMP_DIR>/task-010-release/project-development-2.1.0.zip`, byte-identical to the accepted archive.

## History / next action

- 2026-09-09: Created under DEC-024 after Human confirmed the local cleanup, real-use test and release decision; Spec frozen at SHA-256 `d084aababfc04cf6a980b097a43c45fd1752fe77d45baff5e052c322650e5490`; moved to DOING.
- 2026-09-09: Developer delivered candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c` and deterministic clean archive evidence; moved to VERIFY with fresh identities required.
- 2026-09-09: Fresh Tester PASS and Reviewer APPROVE received for the exact candidate. Reviewer P2 governance-comparison wording was corrected; structural gate and Human candidate-specific acceptance remain pending.
- 2026-09-09: Pre-release structural gate returned CONSISTENT. Task moved to BLOCKED solely for Human acceptance of the exact candidate and archive before any installation or remote mutation.
- 2026-09-09: Human replied “接受该候选并发布”; DEC-025 records exact-candidate acceptance, the blocker is cleared, and TASK-010 returned to DOING for local synchronization and publication.
- 2026-09-09: Developer synchronized the accepted archive locally with a recoverable backup; independent Tester verified AC-7 PASS. Fresh remote preflight and publication remain.
- 2026-09-09: Product `2.1.0` was published and post-verified: annotated tag `v2.1.0` resolves to the accepted candidate, the Release asset hash matches the accepted archive, and the installed Skill remains verified. TASK-011 now owns the remaining sanitized governance closure.
