# TASK-011 — Sanitized release closure

```json
{
  "id": "TASK-011",
  "short_name": "sanitized_release_closure",
  "status": "DOING",
  "spec": {"path": ".ai/specs/SPEC-010-v2.md", "sha256": "cde3da8b111396d96bb497cca2069e96668baa08199bf94234cce4dc20be99d4"},
  "owner": "manager",
  "depends_on": ["TASK-010"],
  "base": "adbb53cd5020c2f1192fb6163355e2878335d26c",
  "candidate": null,
  "contributors": [],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "Dispatch a Developer to sanitize current governance records and record the released state without modifying runtime files."
}
```

## Scope and acceptance

Execute SPEC-010-v2 as a FULL governance/release-recovery workflow on an isolated branch from public `main`. Runtime product changes are prohibited.

## Verification / findings

- SPEC-010-v2 frozen at SHA-256 `cde3da8b111396d96bb497cca2069e96668baa08199bf94234cce4dc20be99d4`.

## Handoff / evidence

- Human decision: do not publish raw-path local commits; retain the working release and perform a sanitized governance closure.
- Public base: `adbb53cd5020c2f1192fb6163355e2878335d26c`.
- Accepted release candidate: `1c4f2f9a10d735cb506ebc90f143d8cec801e66c`.
- Release asset SHA-256: `cb7501603baa8053c6c58a3408fbd7f378edd2a44178796d8eb4c41f8cb17afd`.
- Private raw-path commits are retained locally and explicitly excluded from this branch.

## History / next action

- 2026-09-09: Created under DEC-026 from public `main`; the unpublished SPEC-010 draft was rejected by its own privacy scan and is excluded.
