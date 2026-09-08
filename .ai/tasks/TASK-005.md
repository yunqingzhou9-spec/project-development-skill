# TASK-005 — Add descriptive Worker Agent names

```json
{
  "id": "TASK-005",
  "short_name": "agent_names",
  "status": "DONE",
  "spec": {"path": ".ai/specs/SPEC-005-v2.md", "sha256": "9d90803a4900e56a21c5e6fe281644491e79d217126a5e08595e31f586438395"},
  "owner": "manager",
  "depends_on": [],
  "base": "6741a431a43252d77c7b7f5c997620c90fec36f4",
  "candidate": {"kind": "git", "commit": "bc70cb75dfa1076765678017cca3a76325f417b6"},
  "contributors": ["/root/task_005_agent_names_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PASS",
  "review": "APPROVE",
  "blockers": [],
  "rework_cycles": 1,
  "next_action": "Refresh origin, verify fast-forward safety, then publish GitHub main only under DEC-017"
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
- Independent Tester `/root/task_005_tester`: PASS for AC-1 through AC-8 on exact candidate `bc70cb75dfa1076765678017cca3a76325f417b6`. Confirmed dynamic per-Task naming with distinct layout, movement and collision mappings; future-project-only scope; stable IDs and native identity authority; exact four-file scope; unchanged historical Task/evidence blobs; 28/28 tests; Skill validation; and no repository edits.
- Independent Reviewer `/root/task_005_reviewer`: APPROVE with no P0/P1/P2 findings on the exact candidate and Spec digest. Confirmed the Task name is chosen dynamically during decomposition, the same semantic slug flows across Worker roles, examples are not fixed values, compatibility and fallback are preserved, and current/historical identities are not renamed. Reviewer made no edits.
- Completion gate: installed version 2.0.4 checker returned `STRUCTURAL / CONSISTENT` for exact candidate `bc70cb75dfa1076765678017cca3a76325f417b6`. The checker reports `runtime_authenticated:false` and `enforced:false`; Manager separately inspected native creation, assignment and result records and marks Task completion at `PROTOCOL` assurance.

## Handoff / evidence

Manager created TASK-005 from the Human's explicit optimization request. Candidate-bound runtime receipt: `.ai/evidence/TASK-005.json`. Native creation, assignment and result records were inspected through the current Codex collaboration tools; the receipt is a compact index and does not claim protected authentication.

## History / next action

- 2026-09-08T15:20:21+08:00 — Human requested descriptive Task/Agent naming beyond the numeric sequence; Manager recorded SPEC-005 as APPROVED and created TASK-005 at READY under DEC-015.
- 2026-09-08T15:22:23+08:00 — Manager created and assigned fresh Developer `/root/task_005_agent_names_developer`; native creation returned the same descriptive identity and Task moved READY → DOING.
- Developer returned candidate `97ab2887bbaa292531239cb4ba83866d7ca1160f` for SPEC-005 with 28/28 tests and Skill validation passing; no independent verification was dispatched.
- 2026-09-08T15:33:21+08:00 — Human clarified that the change must govern Manager naming in future projects using the Skill and must not target current-conversation Task/Agent names. Manager froze SPEC-005-v2, superseded SPEC-005, marked the old candidate result stale and opened rework cycle 1.
- 2026-09-08T15:36:27+08:00 — Same Developer delivered SPEC-005-v2 candidate `bc70cb75dfa1076765678017cca3a76325f417b6`; Manager confirmed exact four-file scope, clean worktree and frozen Spec digest, then moved Task DOING → VERIFY.
- 2026-09-08T15:37:16+08:00 — Manager assigned fresh independent Tester `/root/task_005_tester` and Reviewer `/root/task_005_reviewer` to the exact candidate and frozen v2 Spec. Their current-project Agent names are deliberately not acceptance evidence for the future-facing behavior.
- Tester returned PASS and Reviewer returned APPROVE with no findings; both remained independent and made no edits.
- 2026-09-08T15:40:07+08:00 — Structural gate returned CONSISTENT; Manager verified native provenance, exact candidate scope and implementation authority, then moved Task VERIFY → DONE under PROTOCOL assurance.
- 2026-09-08T15:42:56+08:00 — Human formally accepted exact candidate `bc70cb75dfa1076765678017cca3a76325f417b6` and authorized local installed-Skill synchronization plus GitHub publication under DEC-017. Version `2.0.4` and existing tag `v2.0.4` remain unchanged; no GitHub Release is authorized.
- 2026-09-08T15:45:28+08:00 — Manager synchronized the three accepted runtime-facing files present in the installed Skill. Repository/installed SHA-256 pairs match: `references/PROTOCOL.md` `28630c3ef368161f6d01efe0cd8ceb42794f9ce3e6e2a642c238b85eefe6f322`, `templates/TASK.template.md` `26b460042e92c62e6414c26fdcc7aba4feb4508afee5369d286c8227abe39fca`, and `templates/PROJECT_STATE.template.md` `10ee4c47df3946ac8d1af3b74da9ec9099d459b7b6ecd8ff1df00e8bae0374e4`. Installed Skill validation passed and repository tests passed 28/28. Repository `README.md` is not part of the installed bundle.
- Next: refresh origin, verify fast-forward safety, then push current HEAD to GitHub `main` only.
