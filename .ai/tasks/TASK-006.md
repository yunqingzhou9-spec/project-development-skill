# TASK-006 — Distribution audit

```json
{
  "id": "TASK-006",
  "short_name": "distribution_audit",
  "status": "VERIFY",
  "spec": {"path": ".ai/specs/SPEC-006.md", "sha256": "d57d15463f71f23aec19bfa600345afd24c7145af5026a80cd067ce18a1f6c1f"},
  "owner": "manager",
  "depends_on": [],
  "base": "247e5c5cf8076cccb653eae52582de35c92d1e17",
  "candidate": null,
  "contributors": [
    "/root/task_006_distribution_audit_version_analyst",
    "/root/task_006_distribution_audit_package_analyst",
    "/root/task_006_distribution_audit_workflow_analyst"
  ],
  "test_required": false,
  "test_na_reason": "Read-only repository and workflow audit; findings are independently reviewed and implementation tests belong to TASK-007.",
  "test": "N/A",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Obtain an independent Reviewer verdict on this audit candidate before TASK-007 implementation."
}
```

## Scope and acceptance

Audit SPEC-006 AC-1 across version/release identity, repository versus installable-package boundaries, beginner usability and low-risk change overhead. Produce evidence-backed findings and a minimal remediation design. Do not edit runtime deliverables in this Task.

## Verification / findings

### Verdict

All four reported concerns exist, with one boundary correction: the installed Skill directory is currently clean; project-local data leaks through GitHub/source archives because no separate installable release artifact exists.

### Evidence

- **Version/release identity — confirmed.** `SKILL.md` metadata, the protocol title and changelog all say `2.0.4`, while annotated tag `v2.0.4` resolves to `912ec892395572447462ce7e0924ab149735f794`, the accepted baseline is `bc70cb75dfa1076765678017cca3a76325f417b6`, published `origin/main` is `d9ad8e4a3d878787a07703927e270fba700ebc35`, and the pre-audit source HEAD is `247e5c5cf8076cccb653eae52582de35c92d1e17`. `git describe` reports `v2.0.4-47-g247e5c5`; four runtime/documentation files changed after the tag without a package-version change. Existing tests do not check these identities.
- **Package cleanliness — confirmed for source archives, not the installed bundle.** HEAD tracks 21 project governance files under `AGENTS.md`, `PROJECT_STATE.md`, `DECISIONS.md` and `.ai/`; they contain the current checkout path and native runtime IDs. A GitHub tag/source ZIP therefore exposes project development records. The installed Skill has 11 files, all byte-identical to their repository counterparts, and a scan found no concrete local paths or runtime IDs. No deterministic allowlisted builder, source-bound manifest or archive verifier exists.
- **Beginner complexity — confirmed.** `SKILL.md` presents six modes and eight invariants before its simplifying guidance. README presents the full role lifecycle before actionable prompts, uses unexplained terms in those prompts and lacks an English operational quick start. The templates expose the full governance schema immediately.
- **Small-change overhead — confirmed.** The protocol calls itself lightweight but defines no eligibility, compact record, escalation rule or commit policy. TASK-005's small final runtime change used nine approval-through-acceptance commits, seven governance-only, plus synchronization/publication commits. The protocol permits these commits but does not require a commit for each transient transition, so this is a practice and guidance problem rather than a safety invariant.

### Accepted remediation design for TASK-007

1. Treat `SKILL.md` frontmatter `metadata.version` as the sole package-version source. Remove the protocol's duplicate numeric title, label the next version as working/unreleased, preserve `v2.0.4`, and document package version, accepted baseline, source commit, Git tag, generated artifact and installed-copy identity as distinct concepts.
2. Build a deterministic archive from an explicit Git commit using an exact runtime-file allowlist rather than recursive inclusion. Include a canonical manifest with skill name, package version, full source commit and sorted file hashes. Verify the archive without extraction and reject missing/extra/unsafe members, symlinks, hash mismatches, version/commit mismatches and concrete local/runtime identifiers.
3. Put a bilingual 60-second quick start before architecture. Let the user describe an outcome normally while the Skill selects the workflow; keep advanced concepts available later.
4. Add a `LIGHTWEIGHT` profile only when every objective low-risk condition passes: one scope/outcome/Task, no dependency or integration need, at most five deliverable files and 200 non-generated changed lines, ordinary Git rollback, known targeted verification, enumerable deliverables, independent implementer and Reviewer, and no security/privacy/secrets, permissions, production infrastructure, external side effects, billing/legal/compliance, public API/schema compatibility, dependency/toolchain, migration, destructive action, release/install/publish, protected acceptance, conflict or consequential unresolved choice. Any false or uncertain condition selects `FULL`.
5. For `LIGHTWEIGHT`, embed the approved scope and its canonical digest in the Task; do not require a separate Spec or DECISIONS entry for routine low-risk approval. Keep candidate-bound Developer evidence and a fresh independent Reviewer; a separate Tester is optional only while eligibility stays true. Human acceptance/install/publish authority remains unchanged.
6. Coalesce records into meaningful checkpoints: normally one candidate commit containing deliverables plus the combined Task, then one verification/state commit. Commit intermediate state only for handoff, interruption, blocker, conflict, scope revision or writer coordination. Deliverable changes always create a new candidate and stale prior verdicts.
7. Add regression tests for version consistency, deterministic package/manifest safety, lightweight eligibility and scope-digest integrity while retaining all existing full-flow completion tests.

## Handoff / evidence

- Audit contributor `/root/task_006_distribution_audit_version_analyst`: native creation/assignment/result in current collaboration tree; final result delivered, no edits.
- Audit contributor `/root/task_006_distribution_audit_package_analyst`: native creation/assignment/result in current collaboration tree; final result delivered, no edits.
- Audit contributor `/root/task_006_distribution_audit_workflow_analyst`: native creation/assignment/result in current collaboration tree; final result delivered, no edits.
- Independent Reviewer: PENDING.

## History / next action

- 2026-09-08: Created from DEC-018 and moved to DOING for read-only audit.
- 2026-09-08: Three independent read-only analyses reconciled; moved to VERIFY with Test N/A and Reviewer pending.
