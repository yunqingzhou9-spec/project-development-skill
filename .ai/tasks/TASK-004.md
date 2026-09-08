# TASK-004 — Make main-window handoff prompts self-locating

```json
{
  "id": "TASK-004",
  "status": "DONE",
  "spec": {"path": ".ai/specs/SPEC-004.md", "sha256": "b7365083d284ce1ec1cc63f3094215e00cfc4c6ed9eaa28ca2cf23e7b7fb9ee6"},
  "owner": "manager",
  "depends_on": [],
  "base": "a32f23fa8c1014924b95779d5c98640bd6c043ca",
  "candidate": {"kind": "git", "commit": "8bdb522332aa176ab371aa147f7e28949ae03768"},
  "contributors": ["/root/task_004_developer"],
  "test_required": true,
  "test_na_reason": null,
  "test": "PASS",
  "review": "APPROVE",
  "blockers": [],
  "rework_cycles": 0,
  "next_action": "NONE; Task complete under PROTOCOL assurance; formal Human acceptance remains separate"
}
```

## Scope and acceptance

Implement frozen `.ai/specs/SPEC-004.md` exactly. Update only the reusable handoff guidance needed to satisfy AC-1 through AC-4; keep the prompt compact but complete. AC-5 requires regression checks. AC-6 requires independent scenario evaluation from an unrelated initial workspace.

Verification profile: Static, Unit, Scenario and Acceptance are required. Integration is N/A because no runtime integration or executable behavior changes. Independent Tester PASS and independent Reviewer APPROVE are required for the exact candidate.

## Verification / findings

Developer self-checks for candidate `8bdb522332aa176ab371aa147f7e28949ae03768`:

- Skill Creator quick validation reported `Skill is valid!`.
- Existing completion suite passed 28/28 tests.
- `git diff --check` passed, and the deliverable changed only `README.md` and `references/PROTOCOL.md`.
- Reusable prompt diff contains no hard-coded PDP-SKILL personal path.
- Developer reasoned the unrelated-initial-workspace scenario: the replacement first inspects the supplied absolute checkout, then reads and cross-checks its authoritative records and native worker state, without old chat or redispatch.
- Independent Tester/forward evaluator `/root/task_004_tester`: PASS for AC-1 through AC-6. Began in unrelated empty workspace `/private/tmp/task004-forward-unrelated.jiaOaQ`, inspected the populated absolute checkout first, then read and cross-checked target governance/native state. Confirmed no old-chat dependency, no redispatch while verification was active, and stop behavior for conflicting remote or nonexistent path. Also confirmed 28/28 tests, Skill validation, unchanged deliverable blobs and no edits.
- Independent Reviewer `/root/task_004_reviewer`: APPROVE with no findings. Confirmed four-field completeness, copy-ready outgoing prompt, wrong-workspace handling, authority and conflict boundaries, reusable placeholders, exact two-file scope, candidate-bound regression checks and no edits.
- Completion gate: installed version 2.0.4 checker returned `STRUCTURAL / CONSISTENT` for exact candidate `8bdb522332aa176ab371aa147f7e28949ae03768`. The checker reports `runtime_authenticated:false` and `enforced:false`; Manager separately inspected native creation, assignment and result records and marks Task completion at `PROTOCOL` assurance.

## Handoff / evidence

Manager created TASK-004 from the Human's explicit implementation request. Developer creation/assignment/result native reference: `/root/task_004_developer`. The Developer was interrupted once by new Human input, left only the two scoped deliverable edits, then resumed under the same Task identity and returned candidate `8bdb522332aa176ab371aa147f7e28949ae03768`. Independent verification results: Tester/forward evaluator `/root/task_004_tester` PASS; Reviewer `/root/task_004_reviewer` APPROVE with no-edit attestation. Gate receipt: `.ai/evidence/TASK-004.json`.

## History / next action

- 2026-09-08T14:32:00+08:00 — Manager recorded SPEC-004 as APPROVED and created TASK-004 at READY.
- 2026-09-08T14:32:47+08:00 — Manager assigned fresh Developer `/root/task_004_developer`; Task moved READY → DOING.
- Developer was interrupted by new Human input; Manager inspected the two scoped uncommitted edits, confirmed no other writer, and resumed the same Task identity rather than duplicating the assignment.
- 2026-09-08T14:37:51+08:00 — Developer delivered immutable candidate `8bdb522332aa176ab371aa147f7e28949ae03768`; Manager confirmed the commit, clean worktree and frozen Spec digest, then moved Task DOING → VERIFY.
- 2026-09-08T14:38:56+08:00 — Manager assigned fresh independent Tester/forward evaluator `/root/task_004_tester` and Reviewer `/root/task_004_reviewer` to the exact candidate.
- Independent Tester/forward evaluator returned PASS and independent Reviewer returned APPROVE with no findings for exact candidate `8bdb522332aa176ab371aa147f7e28949ae03768`.
- 2026-09-08T14:42:50+08:00 — Structural gate returned CONSISTENT; Manager verified native provenance, exact candidate scope and implementation authority, then moved Task VERIFY → DONE under PROTOCOL assurance.
- Next: NONE. Formal Human acceptance, installed-Skill synchronization and publication remain separate decisions.
