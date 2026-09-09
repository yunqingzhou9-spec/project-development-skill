# Same-host cooperative coordination

Python 3.9+ and Git are required; SQLite is included in Python. No daemon or network service is used. This protocol supports cooperative Agents on one host and OS account, sharing the default registry. It does not coordinate multiple hosts, authenticate native Agent identities or fence arbitrary shell writes. Do not place the database on a shared/network filesystem. Custom `--registry` is for controlled tests or an explicitly shared local configuration: using different registries defeats exclusivity and must not be claimed as safe coordination.

The registry defaults under the current user's `.local/state/project-development` directory, outside the checkout. It contains private native references and recovery context. Keep its directory private; never package or publish it. Same Project ID and exact repository identity unify clones; linked Git worktrees also share a common-directory binding. Reusing a Project ID with another repository, or a repository/common directory with another Project ID fails closed. Origin URL is cross-checked exactly; URL aliases require explicit reconciliation, not silent normalization. For an origin-less repository choose a stable identity and use it consistently for every clone. The registry cannot discover deliberately mislabelled origin-less clones.

Set these shell variables from the verified project and native session; placeholders are not runnable values:

```sh
CHECKOUT='<ACCESSIBLE_CHECKOUT>'
REPOSITORY='<EXACT_ORIGIN_OR_STABLE_LOCAL_IDENTITY>'
PROJECT='<PROJECT_ID>'
OWNER='<CURRENT_NATIVE_SESSION_REFERENCE>'
COORD='<SKILL_DIR>/scripts/coordinator.py'
python3 "$COORD" claim --project "$PROJECT" --repository "$REPOSITORY" --checkout "$CHECKOUT" --owner "$OWNER"
```

Read `generation` from the response, then save it as `GENERATION`. All mutating operations after claim require the current owner and generation. Before each cooperative shared write, dispatch or integration:

```sh
python3 "$COORD" assert --project "$PROJECT" --repository "$REPOSITORY" --checkout "$CHECKOUT" --owner "$OWNER" --generation "$GENERATION"
```

A failed assertion stops the action. The assertion is an advisory prerequisite to later shell actions, not an atomic wrapper or operating-system fence. `update` takes `--context '{"next_action":"verify candidate"}'` for private context. Portable project state remains a short index with links.

## Dispatch and results

Prepare before the native create call. Each logical assignment has a stable `work-key` (for example implement, behavior or review) within its Task; Test and Review can coexist. `attempt` identifies one actual creation attempt; never reuse it for a retry. `inputs` binds the exact criteria/candidate/assignment (normally a digest).

```sh
python3 "$COORD" begin --project "$PROJECT" --repository "$REPOSITORY" --checkout "$CHECKOUT" --owner "$OWNER" --generation "$GENERATION" --task TASK-001 --work-key review --attempt review-1 --inputs '<ASSIGNMENT_DIGEST>'
```

Call the native tool once. On success, `dispatch` with the same ownership options plus `--attempt review-1 --native '<RETURNED_NATIVE_ID>'`. On an uncertain response, `uncertain` with the same ownership options and attempt. PREPARED is also unresolved after a crash. Neither may be blindly retried: query actual native state, then bind a found identity with `dispatch`, or explicitly `resolve --attempt review-1 --resolution-ref '<NATIVE_NO_CREATION_OR_STOPPED_EVIDENCE>'` before preparing a new attempt. Do not infer non-creation from a timeout.

On completion, use `result` with ownership options plus:

```sh
--attempt review-1 --native '<RETURNED_NATIVE_ID>' --inputs '<ASSIGNMENT_DIGEST>' --result-ref '<NATIVE_RESULT_REFERENCE>' --payload '{"verdict":"APPROVE","report_ref":"<REPORT_REFERENCE>"}'
```

The ledger only records the payload; the completion gate still evaluates it. Exact duplicate result replay is idempotent; conflicting duplicates, reused result references and old-generation results are rejected. A local attempt key is not a native identity.

## Stop and recover

Stop new dispatch. Inspect native workers and preserve their progress. Resolve attempts only after confirming completion/stopping, or retain them for explicit reconnection. Use `status` (project/repository/checkout options only) to read current owner/generation and attempts. When no unresolved attempts remain, `release` with current ownership options. Then the replacement `claim`s and receives a strictly newer generation.

If the old owner is unavailable, check actual writer state first. Uncertain active writers block conflicting work. Recovery never happens automatically due to age. After a confirmed safe boundary, run:

```sh
python3 "$COORD" recover --project "$PROJECT" --repository "$REPOSITORY" --checkout "$CHECKOUT" --owner '<OBSERVED_OLD_OWNER>' --generation '<OBSERVED_OLD_GENERATION>' --new-owner "$OWNER" --recovery-ref '<WRITERS_STOPPED_OR_RECONNECTED_EVIDENCE>'
```

This is a conditional compare-and-update, not proof the prior process stopped. Keep its original attempts as history. Explicitly resolve old-generation attempts after native reconciliation before redispatch; they cannot supply new-generation acceptance. Reconnected work needs a newly bound assignment/result under the current generation or fresh verification. Never let isolated Worker output overwrite the primary checkout: integrate serially after ownership checks, preserving dirty work.
