# Project development protocol

Prospective rules; existing project policy and frozen historical requirements remain controlling. Read only the section needed.

## Identity vocabulary

`SKILL.md` frontmatter `metadata.version` is the sole authoritative package version. A development/prerelease identifier is a working/unreleased package version, not a release claim. Keep these identities separate:

- **Working version:** package version in the current source candidate.
- **Strictly Accepted Baseline:** immutable candidate most recently accepted by the configured formal authority.
- **Source commit:** full Git commit from which files or a distribution artifact were read.
- **Git tag / release:** historical publication pointers; a matching number does not make later commits released.
- **Distribution artifact:** generated allowlisted archive whose manifest binds package version, source commit and file hashes.
- **Installed copy:** separate filesystem state; compare its manifest/files before claiming it matches any source or artifact.

Never infer one identity from another. Preserve historical tags and releases; publication, installation and accepted-baseline promotion each require their own authority and evidence.

The exact runtime allowlist read from the explicit immutable source commit plus canonical manifest hashes verified against that source is the structural cleanliness boundary. Maintained text-pattern scanning is defense in depth for known project-specific checkout, user-home and local-system paths, native runtime IDs and private-key markers. It is not exhaustive recognition of all path syntax, placeholder combinations or semantic secrets; do not report it as such.

## Setup

Inspect the user-selected checkout, AGENTS and current state first. Reuse existing instructions, commands and history. Setup alone does not authorize business-code edits. Instantiate only useful parts of the five templates; a small change can use one compact Task and the existing state index.

Reuse the authoritative Project ID; otherwise use the user's explicit ID, otherwise generate a readable stable ID at initial setup. Match AGENTS and state. Record portable repository identity and scope separately from the private checkout locator. Conflicts stop dependent work for resolution; do not silently select a different project or regenerate its ID.

Preserve existing Spec/Task/decision history, invalid records and accepted baseline. Link these rather than copying their contents into current state. Unknown facts remain UNVERIFIED. User authorization defines intent; source/runtime evidence shows behavior; Task records track workflow; state is a current index. Conflicts need investigation, not convenient reinterpretation.

## Roles

The main Agent clarifies, coordinates and may implement authorized ordinary work directly. It records itself as a contributor and labels its own checks as self-checks. Human owns consequential choices and formal acceptance. A coordinator cannot issue that acceptance.

Independent capabilities are selected by need, not mandatory job titles. A verifier can perform multiple appropriate checks if project policy permits. No contributor, renamed role or self-authored identity is independent. High-risk behavior verification and review require distinct verifiers, both separate from contributors. Legacy FULL/LIGHTWEIGHT retain their original role rules below.

When delegated, a Developer investigates, implements only scoped deliverables, self-tests and freezes the candidate. A Tester independently checks observable criteria; a Reviewer independently examines intent, logic, risk and evidence. Verifiers do not repair implementation while claiming independence. A repair makes them contributors and requires replacement independent evidence. Main coordination alone updates shared governance; workers return isolated output and reports.

## Scope and effort selection

Before implementation, record outcome, acceptance, declared deliverables/input boundary, actual authorization and required checks. Select effort based on risk, reversibility, coupling, uncertainty and verification needs; record a short rationale for each. Never use fixed file/line counts as a new-work classifier.

Clear low-risk local work with ordinary rollback and known checks can stay with the main Agent. Broader ordinary work can add independent capability checks where useful. Security/privacy/permissions, production infrastructure, money, destructive operations, migrations, public compatibility, external side effects and release/install actions deserve explicit risk assessment; high-risk behavior requires independent behavior and review plus integrated checks. Existing stricter project requirements still apply.

Unknowns receive a bounded investigation: state the question, relevant files/experiment, stopping condition and time/attempt budget. Default one focused investigation up to 15 minutes or two experiments, then report what was learned and replan. If evidence shows consequential unresolved risk, pause the affected action for a decision; uncertainty alone does not create workers or redundant records.

Use work-v1 for new ordinary work: [schema and examples](WORK_FORMAT.md). Freeze the complete canonical scope digest before implementation. Changes to criteria, selected checks or scope require recorded authorization when consequential and a new digest; old verdicts become stale. Never remove a failing required check as a workaround. A separate frozen Spec is useful for a substantial design, but need not duplicate a compact approved scope. Legacy Spec paths may bind explicit immutable Git blobs.

Split work by independently verifiable outcome or ownership boundary. Dependencies must be completed with matching candidate evidence before dependent work proceeds. Parallelize only work independently valuable alongside the main task, with isolated write ownership and available capacity. No mandatory extra roles for simple tasks.

## Execution

### Environment gate

Identify the host from trusted session metadata and actual tools: CODEX, CHATGPT_WORK, OTHER or UNKNOWN. A model or product name proves neither delegation nor protected acceptance. Record only observations needed by selected checks. Do not probe delegation for a task needing no delegation.

Codex and ChatGPT Work are preferred. For unvalidated hosts disclose verified/missing/unknown capabilities once per change. Safe diagnosis and directly authorized local work may proceed using demonstrated capabilities; ask before specific environment adaptation involving installation, credentials, services or cost. Missing a selected independent capability blocks that stage; never silently lower assurance. Existing adaptation approval carries forward within its scope.

Formal acceptance defaults to HUMAN. PROTECTED_SERVICE requires actually verified protected controls and an authority decision. Structural consistency is not authentication; PROTOCOL is not ENFORCED. Report honest limits without unnecessary permission rituals.

### Ownership and dispatch

Use the same-host private [coordinator](COORDINATION.md) to claim or resume the project before shared writes, dispatch or integration. Its transactional owner/generation check is mandatory immediately before each cooperative action. It cannot stop an arbitrary direct writer or eliminate the interval between checking and a shell side effect. Same host/user participants must share the registry. Other hosts/users or isolated registries need external serialization; do not claim exclusivity across them.

Prepare a durable attempt before calling native creation. Save returned native identity, or mark UNCERTAIN if the response is lost. Reconcile actual native state before retry; timeouts and expired leases never justify blind duplicate creation. Bind assignment and result to Task, frozen criteria, input/candidate and attempt. Late old-generation results cannot be accepted. Native creation/result records remain the authentication source, not ledger-generated labels.

Use fresh task-scoped workers where required, with short context: task number/purpose, accurate role, scope reference/digest, base/candidate and needed files. Prefer names such as task_<sequence>_<purpose>_<role> if supported; names are not native identity. One active Task per worker; reuse within the same Task for focused rework. Respect actual capacity; interruption does not prove termination or released capacity. Use native event waits when available instead of repeated polling.

### Effort and resources

Record meaningful task-level observations: elapsed active work/wait time when measured, attempts and failed cycles, commands/check outcomes and broad investigation effort. Token/cost is UNAVAILABLE unless the host actually measures it; never estimate savings as measured facts. Do not create per-message ledgers.

Default at most 3 failed verification cycles per Task (project overrides apply). Budget exhaustion prompts a root-cause summary and replan, not repeated identical retries or dropped checks. Keep ordinary repairs within authorization. Scope/risk/authority decisions go to the Human only when needed.

Reuse objective facts and successful checks only if relevant input hashes, command, environment/dependency identity and scope match, with original references retained. Changed candidate deliverables invalidate verdicts; never reuse stale final acceptance. Avoid rebuilding unchanged verification solely to produce more logs. A check cache is not a native identity or Human approval cache.

### State and evidence

READY → DOING after scope/ownership/dependencies are ready; DOING → VERIFY after frozen candidate and self-checks; VERIFY → DONE only when all selected requirements pass. Failure returns to DOING, blockers stay explicit, changes invalidate old verdicts. DONE is task completion, not formal acceptance or release.

Use a full immutable Git commit containing all declared deliverables, or an explicit retained hashed file snapshot. Candidate changes require fresh relevant checks. Full/new Git scope checks reject undeclared changes and non-ancestor bases; historical records without a deliverable list have an explicit structural scope limitation. Native result references must be verified outside the structural checker.

## Main-window handoff and recovery

Normally the user needs only bound project context, or Project ID plus an accessible checkout locator. Do not require them to transcribe changing version, HEAD, branch or Worker state. If the locator is inaccessible or identity conflicts, stop dependent takeover and ask for the correct context; never search unrelated projects.

Planned handoff: stop new dispatch; persist a compact active index and next action; record native worker references privately. Wait for progressing work or reconnect it, and confirm any stopped writer through actual native evidence. Resolve active attempts before release; the old coordinator releases ownership and ceases action. The replacement reads AGENTS/state, checks real Git/native state, claims the next generation and resumes. A different checkout may lack uncommitted output.

Unplanned recovery: inspect the old owner/generation and native inventory. If a writer cannot be ruled out, keep conflicting work blocked. Explicit recovery requires evidence of stopped/reconnected writers, the observed old owner/generation and a new owner; it never auto-steals due to elapsed time. Old attempts remain visible and must be resolved/reconciled before new dispatch; old-generation results are rejected. See executable recovery examples in [COORDINATION.md](COORDINATION.md).

## Completion and release

Apply [GATE.md](GATE.md) to the exact candidate. Include checks, measured observations, limitations and next action in a concise report. Main Agent self-checks are valuable evidence but not independent verdicts. Missing/failing selected checks block DONE.

Separate working version, accepted baseline, source commit, released artifact and installed copy. Baseline promotion is the configured authority's exact-candidate decision, not a successful gate. Verify integrated behavior when combining tasks. Installation/publication need their own authorization; follow [clean installation](INSTALL.md), never copy repository governance into runtime discovery.

## Legacy compatibility

Existing FULL/LIGHTWEIGHT records retain their selected requirements. Do not rewrite historical records to adopt work-v1 or apply the prospective rules to their own acceptance. FULL functional work needs independent Developer, Tester and Reviewer (Reviewer and Tester distinct from each other and all contributors). Documentation-only Test N/A requires its preselected reason. LIGHTWEIGHT retains its original bounded checklist and independent Reviewer. The following is the legacy selection contract, not the default for new work.

### Workflow profiles

`FULL` is the default and preserves the Spec, Task, verification and integration process in this document. Select `LIGHTWEIGHT` only when every condition below is known true before implementation and remains true through completion:

1. One approved outcome, one scope and one Task; no dependency, cross-Task integration or concurrent-writer need.
2. At most five enumerated deliverable files and at most 200 added/deleted non-generated lines against one full Git base commit.
3. Ordinary Git rollback is sufficient, and a known targeted verification command exists.
4. A real implementer and a fresh independent Reviewer are available.
5. There is no security, privacy, secret, permission, production-infrastructure, external-side-effect, billing, legal/compliance, public API/schema compatibility, dependency/toolchain, migration, destructive-action, release/install/publish, protected-acceptance or conflict risk.
6. No consequential product or technical choice remains unresolved.

Any false, exceeded or uncertain condition selects or immediately escalates to `FULL`. Also escalate on scope revision, unexpected coupling, failed assumptions, non-ordinary rollback, verifier independence loss or a need for release/install/publish. Preserve the old lightweight record, create and approve a frozen Spec, update the Task to `FULL`, and invalidate prior candidate verdicts as needed; never silently widen scope.

For eligible `LIGHTWEIGHT`, one Task may contain `approval_ref`, the complete approved `scope` object and its canonical SHA-256 digest instead of a separate Spec or DECISIONS entry. Canonical scope bytes are UTF-8 JSON with sorted keys and separators `,` and `:`; use `scripts/check_completion.py --scope-digest <task>` to calculate the digest before freezing it. The scope enumerates outcome, acceptance, deliverables, targeted verification and the fixed eligibility assertions from the Task template. A separate Tester is optional while eligibility remains true; record `test_required:false`, `test:"N/A"` and a concrete reason when omitted. A fresh independent Reviewer is always required. The existing preselected documentation-only Test N/A rule for `FULL` remains unchanged.

Use two meaningful checkpoints rather than a commit for every status change:

1. **Candidate checkpoint:** normally one commit containing only the exact declared deliverables and, optionally, the current combined Task handoff. It freezes the candidate reviewed by independent workers. For legacy LIGHTWEIGHT, the completion gate rejects every other changed path in the complete base-to-candidate diff, requires ancestry and excludes only that current Task path from the legacy five-file/200-line limits. FULL exact scope requires an explicit deliverables list; omitted historical lists remain a disclosed structural limitation.
2. **Verification checkpoint:** normally one later governance commit containing final verdicts, receipt/state summary and next action.

Commit an intermediate governance state only for handoff, interruption, blocker, conflict, scope revision or writer coordination. Every deliverable change creates a new candidate and makes prior Test/Review verdicts stale. Human authority over formal acceptance, installation and publication is identical in both profiles.
