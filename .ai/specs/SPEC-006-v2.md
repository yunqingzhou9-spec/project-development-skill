# SPEC-006-v2 — Clear identity and lighter workflow

```json
{
  "id": "SPEC-006-v2",
  "status": "APPROVED",
  "approval_ref": "DEC-020"
}
```

## Goal / scope

Audit and improve the reusable `project-development` Skill so that its version and release identity are unambiguous, its installable distribution excludes repository-local governance and runtime data, beginners have a short safe entry path, and low-risk small changes require materially less process overhead while preserving candidate-bound evidence and human release authority.

Included work:

- distinguish source repository, installed Skill bundle, working candidate, accepted baseline, release tag and generated distribution artifact;
- define one authoritative package-version source and machine-check identity consistency;
- provide a reproducible clean-package builder and verifier whose output contains only an exact allowlist of distributable Skill files and a source-bound manifest;
- add beginner-first guidance and a bounded lightweight workflow for small, low-risk changes;
- reduce unnecessary standalone governance records and commits for the lightweight path without weakening conflict, candidate, independence or publishing safeguards;
- update tests and documentation for the new behavior.

## Non-goals / constraints

- Do not rewrite or delete historical Tasks, Specs, decisions, commits or tags.
- Do not push, tag, create a GitHub Release, publish a package or synchronize the installed Skill without a later explicit Human decision.
- A generated installable package must exclude repository-local `AGENTS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, `.ai/`, Git metadata, virtual environments, test suites and caches through an exact allowlist read from an immutable source commit.
- Package scanning must reject known project-specific checkout paths, concrete user/home and local-system paths, native runtime IDs and private-key markers represented by its maintained detection policy. It must test important POSIX, Windows, WSL, UNC, URL and placeholder boundaries without claiming exhaustive recognition of every possible absolute-path syntax or arbitrary semantic secret.
- Preserve the full workflow for multi-task, high-risk, release, migration, security-sensitive or otherwise non-trivial work.
- The lightweight path must remain repository-centered, scope-bounded and candidate-verifiable; it cannot grant acceptance or publishing authority.
- Existing `v2.0.4` remains historical and unchanged. Any next-version choice must clearly distinguish working/unreleased status from an actually published release.

## Acceptance

- AC-1: A written audit identifies whether each reported concern exists, with file/commit evidence and a clear distinction between repository contents and installed/package contents.
- AC-2: Documentation and machine checks establish a single authoritative package version and explicitly distinguish working version, accepted baseline, Git tag/release and source commit.
- AC-3: A deterministic repository command builds and verifies an installable archive whose members exactly equal the distributable allowlist plus a canonical manifest bound to version, source commit and file hashes. The verifier rejects missing, extra, unsafe, non-regular or altered members and the maintained targeted patterns for project-local paths, runtime IDs and private keys. Documentation states that the allowlist and source hashes are the structural cleanliness boundary and that text-pattern scanning is defense in depth, not exhaustive semantic proof.
- AC-4: A beginner can follow a concise quick start without first understanding every role, state or evidence term; advanced details remain available.
- AC-5: A bounded lightweight path defines objective eligibility and escalation conditions, permits combining approval/Spec/Task evidence where safe, and recommends coalescing transient governance write-backs instead of producing a commit per status change.
- AC-6: The full workflow remains the default whenever lightweight eligibility is uncertain or false, and formal acceptance, installation and publication remain Human-controlled.
- AC-7: Automated tests cover version consistency, exact package membership and source binding, maintained sensitive-pattern rejection boundaries, non-exhaustive-scanner documentation and lightweight-path invariants; existing completion checks continue to pass.

This Spec supersedes SPEC-006 only for package-cleanliness AC-3/AC-7 and the matching constraint. The Human approved the revised structural boundary on 2026-09-08 after the Manager explained that exhaustive absolute-path detection is not a finite or reliable guarantee. Repository-local implementation and verification remain authorized; installation and publication remain unauthorized.

