# SPEC-002 — Add bilingual Skill introduction

```json
{
  "id": "SPEC-002",
  "status": "APPROVED",
  "approval_ref": "User request in the current Codex task on 2026-09-08; recorded as DEC-007"
}
```

## Goal / scope

- Put the user-supplied Chinese and English Skill introduction at the beginning of `README.md`, directly below the title.
- Preserve the supplied wording, workflow line and tagline in both languages.
- Remove the older short opening paragraphs that would duplicate the new introduction; retain the existing capability-boundary section so the introduction is not read as an unconditional platform guarantee.
- Release the documentation update as patch version `2.0.4`, updating `SKILL.md`, the protocol version heading and `CHANGELOG.md` without changing protocol semantics.
- After candidate-specific Human acceptance, synchronize the installed Skill and publish `main` plus annotated tag `v2.0.4` to GitHub under the user's explicit sync-and-publish request.

## Non-goals / constraints

- Do not change agent roles, state transitions, delegation requirements, evidence rules, acceptance authority or safety boundaries.
- Do not add new scripts, dependencies or a separate GitHub Release page.
- Version 2.0.3 governs this task; version 2.0.4 cannot approve or verify itself.
- Publication authority does not replace candidate-specific Human acceptance.

## Acceptance

- AC-1: README begins with the complete supplied Chinese introduction, workflow and tagline.
- AC-2: README then includes the complete supplied English introduction, workflow and tagline.
- AC-3: Existing duplicate opening prose is removed while the detailed feature list and capability-boundary explanation remain.
- AC-4: `SKILL.md`, `references/PROTOCOL.md` and `CHANGELOG.md` consistently identify version 2.0.4; protocol behavior is otherwise unchanged.
- AC-5: Existing completion-checker tests and Skill quick validation pass as non-regression checks.
- AC-6: An independent Reviewer approves the exact immutable candidate and confirms accuracy, bilingual completeness, non-duplication, boundary preservation and version consistency.
- AC-7: Local installation and GitHub publication occur only after Human acceptance of the exact candidate; tag `v2.0.4` binds that accepted candidate.

