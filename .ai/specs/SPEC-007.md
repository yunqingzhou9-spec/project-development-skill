# SPEC-007 — Local Skill synchronization

```json
{
  "id": "SPEC-007",
  "status": "APPROVED",
  "approval_ref": "DEC-022"
}
```

## Goal / scope

Synchronize the local installed `project-development` Skill from the formally accepted, immutable TASK-007 candidate `3ff3e5b8239d92f4847dcd37625865975761480d`, then independently verify the installed bytes and behavior.

Included work:

- build and verify the deterministic exact-allowlist archive from the accepted commit;
- preserve the current installed version `2.0.4` as a recoverable backup;
- replace the installed Skill directory with the verified archive contents;
- verify exact archive membership, manifest/source/version binding, installed byte equality, Skill validation and repository regression tests;
- record the installed identity and backup path in project governance.

## Non-goals / constraints

- Do not push, tag, publish a package, create a GitHub Release or otherwise modify remote state.
- Do not alter the accepted candidate, historical tags or published version `2.0.4`.
- Install only files present in the verified archive built from the exact accepted commit; do not copy repository governance, tests, caches or Git data.
- Preserve a recoverable backup before replacement. Do not delete that backup in this Task.
- Developer, Tester and Reviewer must be separate native identities. Tester and Reviewer do not edit the installed Skill or product files.

## Acceptance

- AC-1: The archive verifies against source commit `3ff3e5b8239d92f4847dcd37625865975761480d`, reports version `2.1.0-dev.1`, has SHA-256 `74920397033b299f77d16a20aa9f649c6fb0b11045bb826ee4a416d282a51c69`, and contains exactly the 12 allowlisted runtime files plus `MANIFEST.json`.
- AC-2: The previous installed `2.0.4` directory is retained at a recorded, readable backup path.
- AC-3: The installed directory contains exactly the verified archive members beneath `project-development/`; every installed runtime file and `MANIFEST.json` is byte-identical to the archive, with no stale `scripts/test_completion.py` or repository governance records.
- AC-4: Installed `SKILL.md` and manifest identify working/unreleased version `2.1.0-dev.1` and the exact accepted source commit; they do not claim that version is published.
- AC-5: Installed Skill quick validation passes, the installed archive verifier passes against the accepted source, and repository completion/package regressions pass.
- AC-6: An independent Tester reports PASS and an independent Reviewer reports APPROVE on the installed state and recorded evidence.
- AC-7: GitHub/remote state, tags and releases remain untouched.
