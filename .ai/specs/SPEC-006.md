# SPEC-006 — Clear identity and lighter workflow

```json
{
  "id": "SPEC-006",
  "status": "APPROVED",
  "approval_ref": "DEC-018"
}
```

## Goal / scope

Audit and improve the reusable `project-development` Skill so that its version and release identity are unambiguous, its installable distribution excludes repository-local governance and runtime data, beginners have a short safe entry path, and low-risk small changes require materially less process overhead while preserving candidate-bound evidence and human release authority.

Included work:

- distinguish source repository, installed Skill bundle, working candidate, accepted baseline, release tag and generated distribution artifact;
- define one authoritative package-version source and machine-check identity consistency;
- provide a reproducible clean-package builder and verifier whose output contains only runtime Skill files and a source-bound manifest;
- add beginner-first guidance and a bounded lightweight workflow for small, low-risk changes;
- reduce unnecessary standalone governance records and commits for the lightweight path without weakening conflict, candidate, independence or publishing safeguards;
- update tests and documentation for the new behavior.

## Non-goals / constraints

- Do not rewrite or delete historical Tasks, Specs, decisions, commits or tags.
- Do not push, tag, create a GitHub Release, publish a package or synchronize the installed Skill without a later explicit Human decision.
- Do not put project-local `AGENTS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, `.ai/`, absolute paths, native runtime IDs, Git metadata, virtual environments or test caches into a generated installable package.
- Preserve the full workflow for multi-task, high-risk, release, migration, security-sensitive or otherwise non-trivial work.
- The lightweight path must remain repository-centered, scope-bounded and candidate-verifiable; it cannot grant acceptance or publishing authority.
- Existing `v2.0.4` remains historical and unchanged. Any next-version choice must clearly distinguish working/unreleased status from an actually published release.

## Acceptance

- AC-1: A written audit identifies whether each reported concern exists, with file/commit evidence and a clear distinction between repository contents and installed/package contents.
- AC-2: Documentation and machine checks establish a single authoritative package version and explicitly distinguish working version, accepted baseline, Git tag/release and source commit.
- AC-3: A deterministic repository command builds and verifies an installable archive containing only the runtime Skill allowlist plus a manifest bound to version, source commit and file hashes; prohibited local/governance/runtime data is rejected.
- AC-4: A beginner can follow a concise quick start without first understanding every role, state or evidence term; advanced details remain available.
- AC-5: A bounded lightweight path defines objective eligibility and escalation conditions, permits combining approval/Spec/Task evidence where safe, and recommends coalescing transient governance write-backs instead of producing a commit per status change.
- AC-6: The full workflow remains the default whenever lightweight eligibility is uncertain or false, and formal acceptance, installation and publication remain Human-controlled.
- AC-7: Automated tests cover version consistency, package allowlist/denylist behavior and lightweight-path invariants; existing completion checks continue to pass.

This Spec is approved by the Human's request on 2026-09-08 to first audit and then optimize the Skill's version identity, release-package cleanliness, beginner complexity and small-change overhead. The request authorizes repository-local implementation and verification only, not installation or publication.
