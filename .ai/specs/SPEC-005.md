# SPEC-005 — Descriptive Task and Worker Agent names

```json
{
  "id": "SPEC-005",
  "status": "APPROVED",
  "approval_ref": "Human request on 2026-09-08 to begin the next optimization by adding a short descriptive name beyond the Task sequence so Worker Agent names reveal both the Task purpose and the Agent role"
}
```

## Goal / scope

Make newly created Task and Worker Agent names understandable in native runtime lists without opening the Task file.

- Keep the stable numbered Task ID, and add a concise descriptive `short_name` written as lower snake case.
- When the host permits caller-selected names, name new Worker Agents with the pattern `task_<sequence>_<short_name>_<role>`, for example `task_005_agent_names_developer`, `task_005_agent_names_tester` and `task_005_agent_names_reviewer`.
- Show the Task's descriptive name alongside its numbered ID in the active-work index and human-facing guidance.
- Make the naming rule normative in the execution protocol and reusable project templates.

## Non-goals / constraints

- Do not rename or rewrite historical Task IDs, files, native Agent identities, receipts or evidence.
- Do not change the stable machine-facing Task ID or require descriptive text inside receipt `task_id` fields.
- A descriptive name is a usability label, not authentication or formal identity evidence; native returned runtime identity remains authoritative.
- If a host assigns names or rejects the preferred form, preserve its native identity and record the closest supported readable label instead of fabricating one.
- Keep names concise: `short_name` uses one to four meaningful lower-case ASCII words separated by underscores; avoid generic labels such as `work`, `task` or `update` when a clearer outcome is known.
- Do not change the completion checker's evidence semantics, installed Skill, version, tags, release state or GitHub publication.

## Acceptance

- AC-1: `references/PROTOCOL.md` requires each new Task to have a concise descriptive short name and requires the preferred `task_<sequence>_<short_name>_<role>` Worker Agent naming pattern where supported.
- AC-2: The protocol preserves stable Task IDs and native runtime identities, explicitly treats the descriptive name as non-authoritative, and defines safe host fallback behavior.
- AC-3: `templates/TASK.template.md` contains a `short_name` metadata field and a concrete naming example consistent with the protocol.
- AC-4: `templates/PROJECT_STATE.template.md` makes the Task short name visible in the active-work index.
- AC-5: `README.md` briefly explains the readable naming behavior with an example that shows both Task purpose and Worker role.
- AC-6: Existing historical Tasks and evidence remain byte-for-byte unchanged, and no historical identity is renamed.
- AC-7: Skill quick validation and all existing completion-checker tests pass.
- AC-8: A native forward check for TASK-005 confirms that Developer, Tester and Reviewer identities using the new pattern are distinguishable by Task purpose and role in the available Agent inventory or returned runtime references.

This approved Spec is frozen. Changes require a new approved version.
