# TASK-009 — Backup discovery cleanup

```json
{
  "id": "TASK-009",
  "short_name": "backup_discovery_cleanup",
  "status": "DONE",
  "spec": {"path": ".ai/specs/SPEC-008.md", "sha256": "0775b8345946b9db9e08fa9c7aebb2c4613c25cea3936451af227dd7fe514876"},
  "owner": "manager",
  "depends_on": ["TASK-008"],
  "base": "499fc99a2a79cde74bf948251838b03bad007027",
  "candidate": {"kind": "git", "commit": "4d6940c852a251db5779b259b73f9f23e5c1554d"},
  "contributors": ["/root/task_009_backup_discovery_cleanup_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PASS",
  "review": "APPROVE",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "NONE; backup discovery cleanup and state reconciliation are complete. Publication remains unauthorized."
}
```

## Scope and acceptance

Execute SPEC-008. The Developer owns only the exact backup move and preservation checks. The Manager serializes the `PROJECT_STATE.md` truth reconciliation and Git write-back. Fresh independent Tester and Reviewer verify the combined result.

## Verification / findings

- Developer self-check: moved the exact backup to the approved destination; source no longer exists, destination is readable, version remains `2.0.4`, 11 regular files and no symlinks.
- Developer hash check: all per-file SHA-256 values match before/after; deterministic sorted-list digest `6a2ab2112f7ea4bdc0ffd268347f8d3c861b7c0ec0248f98f50e3b162cf7a766`.
- Discovery check: only `/Users/duolaamengmac/.codex/skills/project-development/SKILL.md` remains under the Skill root for this name.
- Current installation check: unchanged `2.1.0-dev.1`, 13 files, source commit `3ff3e5b8239d92f4847dcd37625865975761480d`, all manifest hashes valid.
- Independent Tester `/root/task_009_backup_discovery_cleanup_tester`: PASS on corrected candidate `4d6940c852a251db5779b259b73f9f23e5c1554d`; all six acceptance criteria and 38/38 plus 20/20 regressions passed.
- Independent Reviewer `/root/task_009_backup_discovery_cleanup_reviewer`: APPROVE on the corrected candidate with no P0/P1/P2 findings; verified the state wording, backup-byte identity, single discovery entry, unchanged current installation and local no-publication evidence.
- Limits: no rollback drill was performed; remote non-change is supported by local refs rather than a live network check.
- Completion gate: `.ai/evidence/TASK-009.json` returned `STRUCTURAL / CONSISTENT`; Manager verified the native creation, assignments and corrected-candidate final results for three distinct Worker identities. TASK-009 is DONE under PROTOCOL assurance.

## Handoff / evidence

- User authorization: “先做1和2”.
- Source backup: `/Users/duolaamengmac/.codex/skills/project-development.backup-20260909T000444+0800-2.0.4-4547`.
- Destination backup: `/Users/duolaamengmac/.codex/backups/project-development/2.0.4-20260909T000444+0800-4547`.
- Developer `/root/task_009_backup_discovery_cleanup_developer`: native creation/assignment/result in the current collaboration tree; no repository edits.
- Tester `/root/task_009_backup_discovery_cleanup_tester`: native creation/assignment/result in the current collaboration tree; PASS with no edits.
- Reviewer `/root/task_009_backup_discovery_cleanup_reviewer`: native creation/assignment/result in the current collaboration tree; APPROVE with no implementation edits.

## History / next action

- 2026-09-09: Created under DEC-023; Spec frozen at SHA-256 `0775b8345946b9db9e08fa9c7aebb2c4613c25cea3936451af227dd7fe514876`; moved to DOING.
- 2026-09-09: Developer moved the backup with byte-preservation and discovery checks passing; Manager reconciled the authoritative current-state text.
- 2026-09-09: Candidate `4d6940c852a251db5779b259b73f9f23e5c1554d` frozen; moved to VERIFY with fresh Tester and Reviewer required. An initially transcribed nonexistent full hash sharing the same short prefix was invalidated before any final verdict; both workers received the corrected Git-resolved identity.
- 2026-09-09: Fresh Tester PASS and Reviewer APPROVE received for the corrected exact candidate; completion gate pending.
- 2026-09-09: Manager verified native provenance and the `STRUCTURAL / CONSISTENT` receipt, marked TASK-009 DONE and retained the no-publication boundary.
