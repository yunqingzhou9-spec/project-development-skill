# TASK-011 — Sanitized release closure

```json
{
  "id": "TASK-011",
  "short_name": "sanitized_release_closure",
  "status": "VERIFY",
  "spec": {"path": ".ai/specs/SPEC-010-v2.md", "sha256": "cde3da8b111396d96bb497cca2069e96668baa08199bf94234cce4dc20be99d4"},
  "owner": "manager",
  "depends_on": ["TASK-010"],
  "base": "adbb53cd5020c2f1192fb6163355e2878335d26c",
  "candidate": {"kind": "git", "commit": "a1d42876769612d00c4951dd7e1dbc06566348ce"},
  "contributors": ["/root/task_011_sanitized_release_closure_v2_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PASS",
  "review": "APPROVE",
  "blockers": [],
  "rework_cycles": 1,
  "next_action": "Perform a fresh remote fast-forward preflight and publish only the sanitized main line, then verify remote state and reconcile the primary checkout."
}
```

## Scope and acceptance

Execute SPEC-010-v2 as a FULL governance/release-recovery workflow on an isolated branch from public `main`. Runtime product changes are prohibited.

## Verification / findings

- SPEC-010-v2 frozen at SHA-256 `cde3da8b111396d96bb497cca2069e96668baa08199bf94234cce4dc20be99d4`.
- Developer candidate `80838770c45fbd6dd7ff4c22f19112a93a3fbe38`: sanitized seven tracked governance Markdown files, preserved release facts, and left all runtime files byte-identical to the accepted product candidate.
- Developer verification: completion 38/38 PASS; package 20/20 PASS; Skill quick validation PASS; Python compilation PASS; diff and strict tracked-Markdown privacy scans PASS; excluded local-only commits are not ancestors.
- Independent Tester PASS on `80838770c45fbd6dd7ff4c22f19112a93a3fbe38` for AC-1 through AC-5 and the Tester portion of AC-6.
- Independent Reviewer CHANGES_REQUESTED on `80838770c45fbd6dd7ff4c22f19112a93a3fbe38`: sanitizing frozen `.ai/specs/SPEC-008.md` changed its current digest while TASK-009 still paired that path with the original approved digest. Rework must preserve the original source-commit-qualified binding and explicitly label the current file as a sanitized projection.
- Rework candidate `a1d42876769612d00c4951dd7e1dbc06566348ce`: TASK-009 now binds the approved Spec to immutable blob `cf04ea8b76fa7403cc14a3ddd8d148048ee8290c:.ai/specs/SPEC-008.md` at its original digest and separately records the DEC-026-authorized current sanitized projection and digest. Fresh independent verification is required.
- Fresh independent Tester PASS and Reviewer APPROVE on exact rework candidate `a1d42876769612d00c4951dd7e1dbc06566348ce`; no findings remain. Candidate-bound receipt: `.ai/evidence/TASK-011.json`.
- Structural gate result: `STRUCTURAL / CONSISTENT` for TASK-011, frozen Spec digest and exact candidate `a1d42876769612d00c4951dd7e1dbc06566348ce`; native provenance was separately inspected by the Manager. The gate is not protected acceptance.

## Handoff / evidence

- Human decision: do not publish raw-path local commits; retain the working release and perform a sanitized governance closure.
- Public base: `adbb53cd5020c2f1192fb6163355e2878335d26c`.
- Accepted release candidate: `1c4f2f9a10d735cb506ebc90f143d8cec801e66c`.
- Release asset SHA-256: `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd`.
- Private raw-path commits are retained locally and explicitly excluded from this branch.

## History / next action

- 2026-09-09: Created under DEC-026 from public `main`; the unpublished SPEC-010 draft was rejected by its own privacy scan and is excluded.
- 2026-09-09: Developer delivered exact candidate `80838770c45fbd6dd7ff4c22f19112a93a3fbe38`; independent verification pending.
- 2026-09-09: Tester PASS; Reviewer requested one bounded provenance-integrity rework cycle. Candidate `80838770c45fbd6dd7ff4c22f19112a93a3fbe38` is not publishable.
- 2026-09-09: Developer delivered rework candidate `a1d42876769612d00c4951dd7e1dbc06566348ce`; prior verdicts do not carry forward.
- 2026-09-09: Fresh rework Tester PASS and Reviewer APPROVE received; structural gate and remote operations pending.
- 2026-09-09: Candidate-bound structural gate returned CONSISTENT; fresh remote preflight and authorized sanitized publication remain.
