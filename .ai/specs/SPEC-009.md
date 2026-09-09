# SPEC-009 — Finalize 2.1.0 release

```json
{
  "id": "SPEC-009",
  "status": "APPROVED",
  "approval_ref": "DEC-024"
}
```

## Goal / scope

Finalize the Human-accepted `2.1.0-dev.1` functionality as formal version `2.1.0`, independently verify the exact release candidate and clean distribution artifact, then—after candidate-specific Human acceptance—publish that exact state to the existing GitHub repository.

Included work:

- change the authoritative `SKILL.md` `metadata.version` from `2.1.0-dev.1` to `2.1.0`;
- move the current Unreleased changelog entries into a dated `2.1.0` section and leave a clear Unreleased section;
- update only version-dependent tests/documentation needed for the final SemVer identity;
- build and verify a deterministic exact-allowlist archive from the final release candidate;
- independently verify regression, package, identity, archive, installation and release-readiness evidence;
- present the exact immutable release candidate and artifact hash for Human acceptance;
- after that candidate-specific acceptance, synchronize the local installed Skill, fast-forward GitHub `main`, create annotated tag `v2.1.0` at the exact accepted release commit, and create a GitHub Release with the verified clean archive asset and concise release notes;
- verify local installation and published refs/release/artifact after publication.

## Non-goals / constraints

- Do not change the accepted product behavior beyond release-identity finalization.
- Do not rewrite, delete or move historical tags, releases, Tasks, Specs, decisions or commits.
- Do not publish GitHub-generated source archives as the clean Skill artifact; attach the exact verified allowlisted ZIP.
- Do not push any ref other than `main` and new `v2.1.0`; do not force-push.
- Do not publish the new candidate until the Human accepts its exact full commit ID after independent verification. The current instruction authorizes the release operation but cannot pre-bind formal acceptance to a commit that does not yet exist.
- Abort publication if refreshed `origin/main` is no longer an ancestor of the candidate, if `v2.1.0` already exists, if tests/review fail, or if the clean archive cannot be reproduced exactly.

## Acceptance

- AC-1: `SKILL.md` is the sole authoritative package-version source and reports exactly `2.1.0`; documentation and changelog call it released only after successful publication.
- AC-2: The release candidate differs from the accepted `2.1.0-dev.1` functionality only in bounded final-version, changelog, version-dependent test/documentation and release-governance changes.
- AC-3: Completion tests, package tests, Skill quick validation, Python compilation and diff checks pass on the exact candidate.
- AC-4: Two builds from the exact candidate are byte-identical; both verify successfully; the archive contains exactly 12 allowlisted runtime files plus canonical `MANIFEST.json`, bound to version `2.1.0`, the full candidate commit and matching hashes.
- AC-5: Independent Tester reports PASS and independent Reviewer reports APPROVE on the exact candidate, archive and release plan; the completion gate reports `STRUCTURAL / CONSISTENT`.
- AC-6: Human formally accepts the exact candidate before any publication mutation.
- AC-7: The local installed Skill is synchronized to the accepted `2.1.0` archive with a recoverable prior backup and passes post-install validation.
- AC-8: A fresh pre-push fetch shows `origin/main` is an ancestor of the accepted candidate and `v2.1.0` is absent; explicit main-only and tag-only pushes succeed without force.
- AC-9: GitHub Release `v2.1.0` exists, targets the exact accepted commit/tag, includes the verified clean ZIP asset, and the downloaded asset hash matches the accepted archive.
- AC-10: Post-release verification confirms remote `main`, tag, GitHub Release, installed version and artifact identity; repository state records `RELEASED`. Existing `v2.0.4` remains unchanged.
