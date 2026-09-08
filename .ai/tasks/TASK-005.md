# TASK-005 — Add descriptive Worker Agent names

```json
{
  "id": "TASK-005",
  "short_name": "agent_names",
  "status": "VERIFY",
  "spec": {"path": ".ai/specs/SPEC-005-v2.md", "sha256": "9d90803a4900e56a21c5e6fe281644491e79d217126a5e08595e31f586438395"},
  "owner": "manager",
  "depends_on": [],
  "base": "6741a431a43252d77c7b7f5c997620c90fec36f4",
  "candidate": {"kind": "git", "commit": "bc70cb75dfa1076765678017cca3a76325f417b6"},
  "contributors": ["/root/task_005_agent_names_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PENDING",
  "review": "PENDING",
  "blockers": [],
  "rework_cycles": 1,
  "next_action": "Assign fresh independent Tester and Reviewer to exact candidate bc70cb75dfa1076765678017cca3a76325f417b6"
}
```

## Scope and acceptance

Implement frozen `.ai/specs/SPEC-005-v2.md` exactly. Update only `references/PROTOCOL.md`, `templates/TASK.template.md`, `templates/PROJECT_STATE.template.md` and `README.md` unless a directly necessary regression test is identified. Preserve all current and historical Task, receipt and runtime identity bytes.

Verification profile: Static, Unit, Scenario and Acceptance are required. Integration is represented by a native naming forward check because the behavior is exercised through the host's Agent creation API. Independent Tester PASS and independent Reviewer APPROVE are required for the exact candidate.

## Verification / findings

Candidate `97ab2887bbaa292531239cb4ba83866d7ca1160f` satisfied the original SPEC-005 direction and passed Developer self-checks, but the Human clarified before independent verification that current-conversation Agent naming is not the target or acceptance evidence. Its old-Spec result is historical and stale; SPEC-005-v2 requires future-facing Manager behavior and a reasoned future-project scenario.

Developer self-checks for SPEC-005-v2 candidate `bc70cb75dfa1076765678017cca3a76325f417b6`:

- Changed exactly `README.md`, `references/PROTOCOL.md`, `templates/PROJECT_STATE.template.md` and `templates/TASK.template.md`.
- Made per-Task dynamic naming explicit and used multiple examples so `Layout adjustment` cannot be read as a fixed name.
- Reasoned future-project scenario PASS for a game Manager decomposing distinct layout, movement and collision Tasks and deriving role-specific Worker names from each Task's own slug.
- Historical TASK-001 through TASK-004 and `.ai/evidence/` are unchanged from the approved base.
- Completion tests passed 28/28; Skill quick validation and static scope checks passed.
- Current Agent names were not used as implementation or acceptance evidence.

## Handoff / evidence

Manager created TASK-005 from the Human's explicit optimization request. Runtime references will be recorded after dispatch.

## History / next action

- 2026-09-08T15:20:21+08:00 — Human requested descriptive Task/Agent naming beyond the numeric sequence; Manager recorded SPEC-005 as APPROVED and created TASK-005 at READY under DEC-015.
- 2026-09-08T15:22:23+08:00 — Manager created and assigned fresh Developer `/root/task_005_agent_names_developer`; native creation returned the same descriptive identity and Task moved READY → DOING.
- Developer returned candidate `97ab2887bbaa292531239cb4ba83866d7ca1160f` for SPEC-005 with 28/28 tests and Skill validation passing; no independent verification was dispatched.
- 2026-09-08T15:33:21+08:00 — Human clarified that the change must govern Manager naming in future projects using the Skill and must not target current-conversation Task/Agent names. Manager froze SPEC-005-v2, superseded SPEC-005, marked the old candidate result stale and opened rework cycle 1.
- 2026-09-08T15:36:27+08:00 — Same Developer delivered SPEC-005-v2 candidate `bc70cb75dfa1076765678017cca3a76325f417b6`; Manager confirmed exact four-file scope, clean worktree and frozen Spec digest, then moved Task DOING → VERIFY.
- Next: assign fresh independent Tester and Reviewer to the exact candidate. Their current-project Agent names are not acceptance evidence for the future-facing behavior.
