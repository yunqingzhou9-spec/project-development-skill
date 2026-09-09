# SPEC-010-v2 — Sanitized release closure

```json
{
  "id": "SPEC-010-v2",
  "status": "APPROVED",
  "approval_ref": "DEC-026"
}
```

## Goal / scope

Close the already successful 2.1.0 release without publishing local-only governance commits that contain raw machine paths. Produce a new fast-forward governance line from current public `main`, replace current tracked governance-file occurrences of operator-specific checkout/install/backup/temp paths with stable placeholders, and record the verified release state accurately.

Included work:

- preserve the rejected local-only commits on an unpushed local recovery branch;
- replace operator-specific paths in current tracked Markdown governance files with `<LOCAL_CHECKOUT>`, `<CODEX_SKILLS>`, `<CODEX_BACKUPS>` or `<TEMP_DIR>` forms while preserving meaning;
- leave synthetic path-security fixtures in executable tests unchanged;
- update TASK-010 and PROJECT_STATE to accurately record accepted candidate, installed version, tag, Release and clean-asset identity without raw local paths;
- independently verify the sanitized current tree, unchanged runtime product, published release identity and fast-forward safety;
- push only the sanitized fast-forward governance commits to `main`; do not change tags, Release assets or product files.

## Non-goals / constraints

- Do not push, cherry-pick or merge local-only commits `2ffb24a`, `15177c8` or `0a7db12`, or their private-history descendants.
- Do not force-push, rewrite already-public history, delete local recovery history, or claim that earlier public commits have been erased.
- Do not edit runtime Skill files, version `2.1.0`, annotated tag `v2.1.0`, Release notes or the published ZIP.
- Do not remove historical governance content; sanitize path values in the current tree without changing recorded outcomes.
- Do not treat generic or synthetic security-test paths as private operator data.

## Acceptance

- AC-1: The sanitized candidate is a descendant of current public `main` and does not contain the rejected local-only commits in its ancestry.
- AC-2: Current tracked Markdown governance files contain no operator-specific absolute path and no task-specific temporary path; environment-specific locations use clear placeholders or relative references.
- AC-3: Historical meaning, candidate IDs, artifact hashes, verdicts and release results are preserved; public-history commits remain intact and no force operation occurs.
- AC-4: TASK-010 and PROJECT_STATE state that product `2.1.0` is RELEASED and verified, with tag `v2.1.0` bound to `1c4f2f9a10d735cb506ebc90f143d8cec801e66c` and clean ZIP SHA-256 `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd`.
- AC-5: Runtime files at the sanitized candidate are byte-identical to accepted candidate `1c4f2f9a10d735cb506ebc90f143d8cec801e66c`; completion/package tests and Skill quick validation pass.
- AC-6: Independent Tester reports PASS and Reviewer reports APPROVE; structural gate is CONSISTENT.
- AC-7: A fresh pre-push fetch confirms fast-forward safety; sanitized `main` push succeeds; remote post-check confirms the sanitized tip, unchanged tags/Release/asset and accurate current-state files.
- AC-8: The primary local checkout is reconciled to sanitized public `main`, while rejected raw-path commits remain only on a clearly named unpushed local recovery branch.

This version supersedes an unpublished local SPEC-010 draft that failed its own privacy scan. No content from that draft is authorized for publication.
