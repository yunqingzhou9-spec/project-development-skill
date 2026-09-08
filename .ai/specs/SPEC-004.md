# SPEC-004 — Reliable main-window handoff prompts

```json
{
  "id": "SPEC-004",
  "status": "APPROVED",
  "approval_ref": "Human request on 2026-09-08 to revise both window-switch prompts after the Project ID-only takeover prompt failed and a four-field identity block succeeded"
}
```

## Goal / scope

Revise the reusable planned-handoff and replacement-window prompts so a new Codex window can locate and verify the intended repository even when its initial workspace is unrelated.

- The outgoing-window prompt must require a fully populated, copy-ready replacement prompt rather than returning only Project ID and next action.
- The replacement prompt must visibly carry Project ID, absolute local repository path, GitHub/remote URL and current stable version before the recovery instructions.
- The governing handoff protocol must explain that the four-field identity capsule selects the intended checkout, that the supplied absolute path is inspected before the replacement reads `AGENTS.md`, and that a differing initial workspace must not be mistaken for the target repository.
- Keep repository records and native runtime evidence authoritative; the identity capsule locates and cross-checks them rather than replacing them.

## Non-goals / constraints

- Do not hard-code PDP-SKILL's personal local path or repository identity into reusable public prompt templates; use explicit placeholders.
- Do not weaken conflict handling, duplicate-worker prevention, candidate binding or the ban on copying old chat as authoritative state.
- Do not change runtime tools, the completion checker, package dependencies, installed Skill, version, tags, release state or GitHub.
- Do not promise that a path exists or is accessible on another host; missing/inaccessible/conflicting identity must stop takeover for Human resolution.

## Acceptance

- AC-1: README's outgoing prompt requires the final response to include a complete replacement-window prompt populated with Project ID, absolute local repository path, GitHub/remote URL and current stable version, plus the verified branch/candidate/dirty/agent/blocker/next-action state.
- AC-2: README's replacement prompt begins with the four explicit identity fields and tells the Manager to inspect the supplied absolute checkout before reading its governance files; it must not assume the initial workspace is the project.
- AC-3: `references/PROTOCOL.md` makes the same identity-capsule and wrong-initial-workspace behavior normative while retaining repository/native evidence authority and stop-on-conflict behavior.
- AC-4: The prompts remain reusable through placeholders and do not embed the user's PDP-SKILL absolute path.
- AC-5: Skill quick validation and the existing completion test suite pass.
- AC-6: An independent forward-test, starting from an unrelated workspace and only the revised replacement prompt plus accessible target repository, concludes that the supplied absolute checkout is inspected first, identity is cross-checked, old chat is unnecessary and active work is not redispatched before native-state verification.

This approved Spec is frozen. Changes require a new approved version.
