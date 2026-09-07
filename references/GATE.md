# Completion gate

Read at VERIFY/completion, or when configuring runtime verification. This package provides a standard-library Python structural checker, not a host-specific agent launcher or a protected CI service.

## Required procedure

1. Manager obtains the actual runtime creation, assignment and result records through the host tools. Check task ownership, independent identities, candidate, Spec digest and actual report conclusions. A tool name, a printed UUID or a worker's claim is not evidence. Receipts below are a compact index of those records, not their authentication.
2. Capture all implementation contributors, including anyone who repaired the candidate. Required Tester and Reviewer must not be contributors or the Manager, and must differ from each other. Confirm Reviewer did not modify the implementation. For file outputs include the complete deliverable set; for Git ensure deliverable changes are committed.
3. Manager sets current Test/Review summaries from returned results, resolves blockers and saves runtime receipts. Missing/ambiguous evidence leaves the Task in VERIFY or BLOCKED. Never substitute main-agent roleplay.
4. Run the checker on the explicit final candidate. It reads files only, does not change state or execute project tests. On success, Manager may mark DONE under a **PROTOCOL** assurance policy only after step 1's native-record check. DONE means this Task is complete, not human approval or formal acceptance. Report **STRUCTURAL** as the checker result, never as proof of runtime authenticity. At the configured overall/milestone acceptance point, obtain the actual candidate-specific human decision (default authority), or the verified protected service receipt; Manager/worker declarations cannot substitute for either.
5. For **ENFORCED** assurance, a protected host/CI must authenticate native records, verify complete candidate scope and contributor provenance, supply the actual final candidate, protect validator/policy/approval inputs and control authoritative acceptance/release. This package does not install that service. If ENFORCED is required but unavailable, block acceptance. A mutable Task's DONE label alone never establishes protected acceptance.

Assurance vocabulary: PROTOCOL = Manager followed rules and checked native records; STRUCTURAL = this script checked supplied data consistency; ENFORCED = a verified protected integration controls acceptance. Record the actual level plus evidence; never infer a stronger one from a successful script exit.

Apply the protocol's [environment gate](PROTOCOL.md#environment-gate) for all hosts. Codex/ChatGPT Work names alone do not establish ENFORCED capability. On other/unknown hosts disclose the unvalidated support condition and obtain approval before adapting the environment. Human-controlled formal acceptance can be used under PROTOCOL without claiming protected automation. This structural script does not implement environment discovery, adaptation approval or formal-acceptance authentication; those are Manager/native-host checks.

## Invocation

Resolve `<skill>` to the installed skill directory; no runtime package installation is needed beyond Python 3.

```sh
python3 <skill>/scripts/check_completion.py --repo <project> \
  --task .ai/tasks/TASK-001.md --receipts .ai/evidence/TASK-001.json \
  --candidate git:<full-commit-id>
```

For outputs without Git use `--candidate files:.ai/evidence/candidate.json`. That file contains the candidate object below. Task and receipt targets must equal it, and each actual file is rehashed. Paths are project-relative, regular files inside the project; symlink escapes are rejected. Preserve accepted file bytes under versioned snapshot paths; a hash cannot recover overwritten content. The manifest must list all deliverables. The checker cannot detect omitted deliverables or unrecorded contributors.

```json
{"kind":"files","files":[{"path":"outputs/result.txt","sha256":"<64 hex characters>"}]}
```

Git Task/receipt target example: `{"kind":"git","commit":"<full commit ID>"}`. The checker verifies commit existence in this repo and matches it against the candidate explicitly selected on the command line. It does not assert the working tree/HEAD, merged code or deployed artifact equals that commit; the Manager/protected runner must select and verify the actual final deliverable. If integration changes its content, reverify the new candidate.

Task and Spec use their first and only `json` fenced metadata block from the templates. Freeze Spec by hashing the entire approved file after approval is recorded. `approval_ref` points to durable approval evidence, which must be checked for actual authorization; a nonempty reference alone does not prove consent.

## Runtime receipt format

Store only at gate time, typically `.ai/evidence/TASK-001.json`; large native logs remain in their original system and are referenced. If retention is short, preserve supported exports before losing access; an unverifiable excerpt does not become authenticated by copying it. Never fabricate records to make the checker pass.

```json
{
  "manager_id": "<native parent ID>",
  "agents": [
    {"id":"<developer ID>","role":"developer","task_id":"TASK-001","create_ref":"<native creation>","assignment_ref":"<native assignment>"},
    {"id":"<tester ID>","role":"tester","task_id":"TASK-001","create_ref":"<native creation>","assignment_ref":"<native assignment>"},
    {"id":"<reviewer ID>","role":"reviewer","task_id":"TASK-001","create_ref":"<native creation>","assignment_ref":"<native assignment>"}
  ],
  "results": [
    {"agent_id":"<developer ID>","task_id":"TASK-001","spec_sha256":"<approved digest>","target":{"kind":"git","commit":"<commit>"},"verdict":"DELIVERED","result_ref":"<native result>","report_ref":"<report>"},
    {"agent_id":"<tester ID>","task_id":"TASK-001","spec_sha256":"<approved digest>","target":{"kind":"git","commit":"<commit>"},"verdict":"PASS","result_ref":"<native result>","report_ref":"<report>"},
    {"agent_id":"<reviewer ID>","task_id":"TASK-001","spec_sha256":"<approved digest>","target":{"kind":"git","commit":"<commit>"},"verdict":"APPROVE","result_ref":"<native result>","report_ref":"<report>","no_implementation_edits":true}
  ]
}
```

Task `contributors` lists every implementation runtime ID. Multiple Developers are permitted; each needs creation/assignment provenance. At least one Developer DELIVERED result must bind the final candidate. Include only current-candidate results in this receipt; link previous receipts from Task history. For preselected test N/A, omit Tester/results, use Task `test_required:false`, `test:"N/A"`, and a concrete `test_na_reason`. Reviewer is always required. The checker rejects an optional failing test result as well.

Exit codes: 0 = structurally consistent supplied evidence; 1 = gate blocked by missing/invalid/inconsistent evidence; 2 = command-line usage error. Gate-result JSON states `runtime_authenticated:false` and `enforced:false`; usage errors return ordinary CLI diagnostics instead. Host integrations may consume gate results but must establish authentication and enforcement separately. Ordinary projects do not need an SDK or background service to follow the protocol with native tools.
