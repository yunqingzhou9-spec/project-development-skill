# SPEC-005-v2 — Future Manager naming for Tasks and Worker Agents

```json
{
  "id": "SPEC-005-v2",
  "status": "APPROVED",
  "approval_ref": "Human clarification on 2026-09-08 that the reusable project-development Skill must make future Managers assign the same concise purpose name when decomposing Tasks and creating their Worker Agents in any future project; current and historical Task/Agent names are not to be renamed"
}
```

## Goal / scope

Change the reusable `project-development` Skill so that, in future projects using the updated Skill, the Manager assigns every newly decomposed Task both a stable numbered ID and a concise purpose name, then carries that same purpose into every Worker Agent name for the Task.

- At Task decomposition time, the Manager chooses a short human-readable purpose such as `Layout adjustment` and displays the Task as `TASK-001 — Layout adjustment`.
- The Manager records a matching lower-snake-case slug such as `layout_adjustment` for host-compatible runtime names.
- When creating Workers, the Manager reuses the same Task number and purpose slug, then appends the role: `task_001_layout_adjustment_developer`, `task_001_layout_adjustment_tester`, `task_001_layout_adjustment_reviewer`, or another accurate role suffix.
- Make this prospective behavior normative in the installed Skill's execution protocol and reusable templates, and explain it briefly in the README.

## Non-goals / constraints

- Do not rename, rewrite or reorganize any current or historical Task, Task file, Agent identity, receipt or evidence record, including this repository's TASK-001 through TASK-005 runtime identities.
- Do not treat renaming the current conversation's Agents as implementation or acceptance evidence.
- Keep the stable machine-facing Task ID and Task filename numbered; the descriptive purpose supplements the ID rather than replacing it.
- The purpose name is a usability label, not authentication or formal identity evidence; the native runtime identity returned by the host remains authoritative.
- If a host requires restricted characters, derive a lower-snake-case runtime slug from the human-readable Task name. If the host assigns names or rejects caller-selected names, preserve its native identity and record the closest supported readable label instead of fabricating one.
- Keep names concise and specific: normally one to four meaningful words; avoid generic labels such as `work`, `task` or `update` when a clearer outcome is known.
- Do not change the completion checker's evidence semantics, installed Skill, version, tags, release state or GitHub publication in this Task.

## Acceptance

- AC-1: `references/PROTOCOL.md` requires a future Manager to choose the descriptive Task name during decomposition, display it with the numbered Task ID, and reuse its semantic slug for all Worker roles created for that Task.
- AC-2: `templates/TASK.template.md` visibly pairs a human-readable Task title with a matching `short_name` slug and shows the derived Worker naming pattern.
- AC-3: `templates/PROJECT_STATE.template.md` shows the numbered Task and human-readable short name together in the active-work index, with a matching Worker example.
- AC-4: `README.md` explains that this behavior applies to future projects using the updated Skill and includes a consistent `Layout adjustment` / `layout_adjustment` example.
- AC-5: The rules preserve stable Task IDs and native runtime identities, define restricted-host fallback behavior, and explicitly prohibit retrospective renaming.
- AC-6: A reasoned future-project scenario confirms that a Manager decomposing a game project into a layout-adjustment Task would create `TASK-001 — Layout adjustment` and role-specific Workers derived from `task_001_layout_adjustment_*`, without relying on changes to current Agent names.
- AC-7: Existing historical Tasks and evidence remain byte-for-byte unchanged from base `6741a431a43252d77c7b7f5c997620c90fec36f4`.
- AC-8: Skill quick validation and all existing completion-checker tests pass.

This approved Spec supersedes SPEC-005 under DEC-016 and is frozen. Changes require a new approved version.
