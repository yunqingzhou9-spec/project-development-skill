# SPEC-008 — Backup discovery cleanup

```json
{
  "id": "SPEC-008",
  "status": "APPROVED",
  "approval_ref": "DEC-023"
}
```

## Goal / scope

Prevent the retained `2.0.4` backup from being discovered as a second installed Skill, and reconcile the two stale installed-version statements in `PROJECT_STATE.md` with the verified TASK-008 state.

Included work:

- move `/Users/duolaamengmac/.codex/skills/project-development.backup-20260909T000444+0800-2.0.4-4547` to `/Users/duolaamengmac/.codex/backups/project-development/2.0.4-20260909T000444+0800-4547` without changing its bytes;
- update only the stale Strictly Accepted Baseline and Formal acceptance statements in `PROJECT_STATE.md` so installation is recorded as completed under DEC-022/TASK-008 while publication remains unauthorized;
- independently verify the backup, Skill discovery boundary, current installation and repository state.

## Non-goals / constraints

- Do not alter the current installed Skill, accepted source candidate, backup contents, version, tag, remote branch or release state.
- Do not delete the backup. Move it only after confirming the exact source and destination.
- Do not push, fetch, tag, publish or create a GitHub Release.
- Use separate Developer, Tester and Reviewer identities because the filesystem move is outside the Git checkout and LIGHTWEIGHT excludes install-adjacent/external-side-effect work.

## Acceptance

- AC-1: The old backup path under `~/.codex/skills` no longer exists, and the exact destination under `~/.codex/backups/project-development` exists and is readable.
- AC-2: The moved backup remains version `2.0.4`, contains the same 11 files, has no symlinks, and every relative-path hash matches the pre-move TASK-008 backup evidence.
- AC-3: Skill discovery under `~/.codex/skills` finds only the current `project-development/SKILL.md`, not the backup.
- AC-4: The current installed Skill remains version `2.1.0-dev.1`, contains 13 files, and remains source-bound to accepted commit `3ff3e5b8239d92f4847dcd37625865975761480d`.
- AC-5: `PROJECT_STATE.md` contains no current-state claim that the installed Skill remains `2.0.4` or that installation is not included; it records local synchronization under DEC-022/TASK-008 and keeps publication unauthorized.
- AC-6: Independent Tester reports PASS and independent Reviewer reports APPROVE; repository worktree is clean after the verification write-back.
