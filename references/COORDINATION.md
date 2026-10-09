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

`status` and `assert` are read-only: they do not create, migrate, chmod or update the registry. Their default output retains full legacy history; add `--summary` for owner/generation, unresolved attempts and counts during ordinary work. A missing registry remains missing after inspection. Read-only inspection supports the default rollback journal; WAL-mode registries are rejected before SQLite opens them, because even `mode=ro` can create WAL/SHM sidecars. Reconcile such a custom registry explicitly; never auto-migrate its journal or ignore a live WAL. Use full history only when investigating an actual mismatch or auditing history.

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

Stop new dispatch. Inspect native workers and preserve their progress. Resolve attempts only after confirming completion/stopping, or retain them for explicit reconnection. Use `status --summary` for the current owner/generation and unresolved attempts. When no unresolved attempts remain, `release` with current ownership options. Then the replacement `claim`s and receives a strictly newer generation. For an idle planned handoff, [handoff.py](PERFORMANCE.md#idle-window-handoff) performs the short local inspect/prepare/takeover sequence and gives the fixed prompt only after release.

If the old owner is unavailable, check actual writer state first. Uncertain active writers block conflicting work. Recovery never happens automatically due to age. After a confirmed safe boundary, run:

```sh
python3 "$COORD" recover --project "$PROJECT" --repository "$REPOSITORY" --checkout "$CHECKOUT" --owner '<OBSERVED_OLD_OWNER>' --generation '<OBSERVED_OLD_GENERATION>' --new-owner "$OWNER" --recovery-ref '<WRITERS_STOPPED_OR_RECONNECTED_EVIDENCE>'
```

This is a conditional compare-and-update, not proof the prior process stopped. Keep its original attempts as history. Explicitly resolve old-generation attempts after native reconciliation before redispatch; they cannot supply new-generation acceptance. Reconnected work needs a newly bound assignment/result under the current generation or fresh verification. Never let isolated Worker output overwrite the primary checkout: integrate serially after ownership checks, preserving dirty work.

## Stable host identity and explicit legacy migration

Version 2.4.0 uses a domain-separated SHA-256 of a platform-owned machine identifier: macOS IOPlatformUUID, Linux machine-id, or Windows MachineGuid. Network hostname is informational only. Reads obtain the same platform ID and do not create a cache or alter the registry. Missing/invalid IDs and denied local OS access block with a permissions diagnostic; grant the narrow local read needed, never fall back to hostname. OS reinstall, cloned machine IDs and privileged changes require manual reconciliation. This is cooperative locality checking, not cryptographic attestation; cloning a machine ID can defeat it.

Legacy registries contain no stable identity, so even a matching hostname cannot prove continuity. Ordinary commands refuse them without changes. After explicit Human authorization, inspect the actual old owner/Workers and current local Git binding. Confirm same-machine provenance using native/local evidence. Do not use this procedure to move a registry to another machine or override an existing stable binding. A renamed legacy host can be reconciled only with that explicit evidence; the helper cannot authenticate it.

`coordinator.py migrate-host --project ... --repository ... --checkout ... --owner ... --generation ... --expected-host ... --confirm-same-machine --backup <NEW_PRIVATE_ABSOLUTE_FILE> --evidence-ref <EXISTING_PRIVATE_JSON>` checks the selected active project, exact legacy hostname, repository, current owner/generation, existing Git common-directory binding and no unresolved attempts for that project. Evidence JSON needs nonempty `authorization_ref`, `native_check_ref` and `same_machine_basis`. Both files must be outside the checkout; keep them in trusted private directories. A transaction preserves all project/attempt/root/context data and the original hostname, creates an exclusive pre-change full database backup, then adds a stable host binding, selected project opt-in and a timestamped audit containing backup/evidence hashes. An already bound project, different stable machine identity, WAL registry or changed expectation blocks. Other projects, contexts and attempts remain unchanged; migrating one project does not authorize another. Each legacy project must explicitly opt in using its own verified owner/generation and evidence. New projects bind on initial claim. Failed migrations may leave a retained backup; inspect before retrying with a fresh path. No timeout-based takeover, automatic generation increment, worker dispatch, task replay or network access occurs.

If legacy hostname validation blocks even the ownership assertion, keep repair development isolated and dispatch stopped. The explicitly authorized migration is the bounded recovery operation: its locked owner/generation and root checks replace the unavailable assertion for that operation only. Once migrated, resume normal assertions before shared writes and dispatch. Validate the repair independently under the previously accepted protocol; migration is not self-acceptance. After migration, use the matching new coordinator; old installed versions still compare the legacy hostname and cannot interpret the new identity record.
