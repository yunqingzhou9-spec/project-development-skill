# Work and evidence v1

`work-v1` is a prospective compact format, not an upgrade of historical records. The gate accepts legacy FULL/LIGHTWEIGHT as before. Select all required checks before implementation; each selected check is required, so there is no optional flag to silently disable it. Risk assessment and checks are inside the frozen scope digest. Existing project policy may require more than this minimum. The checker cannot determine whether a risk label or a claim of complete evidence is truthful; the main Agent and required independent verification must examine that.

Use exactly one JSON block in the Task; see the [Task template](../templates/TASK.template.md). `scope` includes outcome, acceptance, assessment, deliverables, base (for Git), and checks. Canonical SHA-256 uses UTF-8 JSON, sorted keys and separators `,` and `:`. Calculate with:

```sh
python3 <SKILL_DIR>/scripts/check_completion.py --repo <CHECKOUT> --scope-digest .ai/tasks/TASK-001.md
```

Then freeze the scope before work. A meaningful scope change needs a new digest and invalidates prior evidence. `depends_on` is an explicit list; `dependencies_satisfied` must list those same dependencies in the same order. These are structural declarations: inspect their actual completion and matching inputs before dispatch. Each contributor must have a matching evidence identity with `contributed:true`; include the main Agent if it implements. Use actual native provenance where available; local self-check provenance must be labelled honestly. Use portable contributor aliases in the Task; map them to actual native provenance only in the private evidence file. Pass an absolute private file via `--receipts` for work-v1 (legacy formats keep project-relative receipt handling). Never put actual native IDs into tracked Task records.

Example companion evidence (substitute real values; placeholders intentionally do not pass):

```json
{
  "format": "evidence-v1",
  "formal_acceptance": false,
  "identities": [
    {"id": "<MAIN_ID>", "provenance_ref": "<SESSION_REFERENCE>", "contributed": true}
  ],
  "checks": [
    {
      "id": "targeted",
      "actor": "<MAIN_ID>",
      "task_id": "TASK-001",
      "scope_sha256": "<FROZEN_SCOPE_HASH>",
      "target": {"kind": "git", "commit": "<FULL_CANDIDATE_COMMIT>"},
      "status": "PASS",
      "command": "<EXACT_CHECK_COMMAND>",
      "environment": "<RELEVANT_ENVIRONMENT_IDENTITY>",
      "report_ref": "<OBSERVATIONS_REFERENCE>",
      "result_ref": "<DISTINCT_RESULT_REFERENCE>"
    }
  ]
}
```

A check has a unique id, a capability (for example behavior, review or static), and an explicit independence boolean. A single non-contributor can supply several checks; high risk requires independent behavior and review from separate identities. Independent results need `no_implementation_edits:true`. Every result must match Task, scope hash and exact target; missing, duplicate, stale, failed or undeclared results block completion. Do not hide failures by omitting checks from evidence. Preserve failed attempts separately and bind their superseding repaired candidate explicitly.

Git deliverables must exactly equal the complete base-to-candidate changed-path set; base must be a real ancestor. Include only intended deliverables; if the current Task changes in the candidate, declare it too. No implicit governance-file exception applies to work-v1. Non-Git work uses the existing `files:<project-relative-manifest>` snapshot, whose membership must match deliverables. Keep accepted snapshot bytes immutable. The work-v1 checker accepts an explicitly supplied absolute private receipt path outside the checkout; it never follows an embedded remote URL or executes evidence. The cross-checkout coordination ledger is also required outside the checkout.

## Historical Spec replay

Legacy Spec references accept either a project-relative path or `<FULL_COMMIT>:<PROJECT_RELATIVE_SPEC_PATH>` in the existing `spec.path` field, with the original SHA-256 in `spec.sha256`. Git revision must be a full immutable commit and target a regular blob; directories, symlinks, abbreviated IDs, escaping paths and unsafe object types are rejected. No old record needs to be rewritten when it already contains that explicit reference.

FULL validates ancestry when its record supplies a base; exact scope when it also supplies `deliverables`. Historical FULL records without a declared file set have no machine-verifiable complete scope boundary. Report that limit instead of inventing history. Legacy LIGHTWEIGHT keeps its original exact diff and eligibility rules. None of these checks authenticates runtime evidence or issues Human acceptance.
