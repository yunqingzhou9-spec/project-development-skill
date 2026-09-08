#!/usr/bin/env python3
"""Read-only structural gate. Never authenticates agent records or changes DONE."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


LIGHTWEIGHT_SCOPE_KEYS = {"outcome", "acceptance", "deliverables", "verification", "eligibility"}
LIGHTWEIGHT_ELIGIBILITY_KEYS = {
    "single_outcome",
    "no_dependencies_or_integration",
    "ordinary_git_rollback",
    "targeted_verification_known",
    "independent_implementer_and_reviewer",
    "risk_categories_absent",
    "no_conflict_or_unresolved_choice",
}


class GateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(r"[<>]", value)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def project_file(root, name):
    require(nonempty(name) and not Path(name).is_absolute(), "Expected project-relative file path")
    target = (root / name).resolve()
    require(root in target.parents and target.is_file(), "Missing file or path outside project: " + name)
    return target


def metadata(path):
    blocks = re.findall(r"^```json\s*\n(.*?)^```\s*$", path.read_text(encoding="utf-8"), re.M | re.S)
    require(len(blocks) == 1, "Expected exactly one JSON metadata block: " + str(path))
    result = json.loads(blocks[0])
    require(isinstance(result, dict), "Metadata must be an object")
    return result


def candidate(root, selected):
    kind, _, identity = selected.partition(":")
    if kind == "git":
        require(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", identity) is not None, "Use full Git commit ID")
        result = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-t", identity],
            capture_output=True, text=True, check=False, timeout=15,
        )
        require(result.returncode == 0 and result.stdout.strip() == "commit", "Candidate is not an existing commit")
        return {"kind": "git", "commit": identity}
    require(kind == "files", "Candidate must be git:<full-ID> or files:<manifest-path>")
    result = json.loads(project_file(root, identity).read_text(encoding="utf-8"))
    require(isinstance(result, dict) and set(result) == {"kind", "files"} and result["kind"] == "files", "Invalid snapshot")
    require(isinstance(result["files"], list) and result["files"], "Empty snapshot")
    seen = set()
    for item in result["files"]:
        require(isinstance(item, dict) and set(item) == {"path", "sha256"}, "Invalid file entry")
        path = project_file(root, item["path"])
        require(path not in seen, "Duplicate snapshot file")
        seen.add(path)
        require(digest(path.read_bytes()) == item["sha256"], "Snapshot file changed: " + item["path"])
    return result


def git_commit(root, value, label):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is not None, label + " must be a full Git commit ID")
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-t", value],
        capture_output=True, text=True, check=False, timeout=15,
    )
    require(result.returncode == 0 and result.stdout.strip() == "commit", label + " is not an existing commit")
    return value


def lightweight_criteria(root, task, target, task_path):
    require(task.get("profile") == "LIGHTWEIGHT", "Invalid workflow profile")
    require(nonempty(task.get("approval_ref")), "LIGHTWEIGHT requires approval evidence reference")
    require(task.get("depends_on") == [], "LIGHTWEIGHT cannot have dependencies")
    scope = task.get("scope")
    require(isinstance(scope, dict) and set(scope) == LIGHTWEIGHT_SCOPE_KEYS, "Invalid LIGHTWEIGHT scope")
    require(nonempty(scope.get("outcome")), "LIGHTWEIGHT requires one outcome")
    acceptance = scope.get("acceptance")
    require(isinstance(acceptance, list) and acceptance and all(nonempty(item) for item in acceptance), "LIGHTWEIGHT requires observable acceptance")
    deliverables = scope.get("deliverables")
    require(isinstance(deliverables, list) and 0 < len(deliverables) <= 5, "LIGHTWEIGHT requires one to five deliverable files")
    require(len(deliverables) == len(set(deliverables)), "Duplicate LIGHTWEIGHT deliverable")
    for path in deliverables:
        require(nonempty(path) and not Path(path).is_absolute() and ".." not in Path(path).parts, "Invalid LIGHTWEIGHT deliverable path")
    require(nonempty(scope.get("verification")), "LIGHTWEIGHT requires targeted verification")
    eligibility = scope.get("eligibility")
    require(isinstance(eligibility, dict) and set(eligibility) == LIGHTWEIGHT_ELIGIBILITY_KEYS, "Invalid LIGHTWEIGHT eligibility assertions")
    require(all(value is True for value in eligibility.values()), "Every LIGHTWEIGHT eligibility assertion must be true")
    scope_hash = canonical_digest(scope)
    require(task.get("scope_sha256") == scope_hash, "LIGHTWEIGHT scope digest mismatch")
    require(target.get("kind") == "git", "LIGHTWEIGHT requires a Git candidate for bounded rollback/diff checks")
    base = git_commit(root, task.get("base"), "LIGHTWEIGHT base")
    ancestry = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", base, target["commit"]],
        capture_output=True, check=False, timeout=15,
    )
    require(ancestry.returncode == 0, "LIGHTWEIGHT base must be an ancestor of the candidate")
    changed = subprocess.run(
        ["git", "-C", str(root), "diff", "--no-renames", "--numstat", "-z", base, target["commit"]],
        capture_output=True, check=False, timeout=15,
    )
    require(changed.returncode == 0, "Cannot inspect LIGHTWEIGHT candidate diff")
    seen, line_count = set(), 0
    allowed_paths = set(deliverables) | {task_path}
    for record in changed.stdout.split(b"\0"):
        if not record:
            continue
        fields = record.split(b"\t", 2)
        require(len(fields) == 3, "Cannot parse LIGHTWEIGHT candidate diff")
        added, deleted = fields[0].decode("ascii", errors="strict"), fields[1].decode("ascii", errors="strict")
        path = fields[2].decode("utf-8", errors="surrogateescape")
        require(added.isdigit() and deleted.isdigit(), "Generated/binary deliverables require FULL")
        require(path in allowed_paths, "LIGHTWEIGHT candidate contains undeclared file: " + path)
        seen.add(path)
        if path in deliverables:
            line_count += int(added) + int(deleted)
    require(seen - {task_path} == set(deliverables), "LIGHTWEIGHT deliverables must exactly match changed scoped files")
    require(line_count <= 200, "LIGHTWEIGHT deliverables exceed 200 changed lines")
    return scope_hash


def check(root, task_path, receipt_path, selected):
    task_file = project_file(root, task_path)
    task = metadata(task_file)
    require(task.get("status") in ("VERIFY", "DONE"), "Task must be VERIFY or DONE")
    require(nonempty(task.get("id")), "Missing task ID")
    require(task.get("blockers") == [], "Blockers must be explicitly empty")
    target = candidate(root, selected)
    require(task.get("candidate") == target, "Task is not for the selected final candidate")
    profile = task.get("profile", "FULL")
    require(profile in ("FULL", "LIGHTWEIGHT"), "Invalid workflow profile")
    if profile == "LIGHTWEIGHT":
        relative_task_path = task_file.relative_to(root).as_posix()
        criteria_key, criteria_hash = "scope_sha256", lightweight_criteria(root, task, target, relative_task_path)
    else:
        spec_ref = task.get("spec")
        require(isinstance(spec_ref, dict), "Missing Spec reference")
        spec_path = project_file(root, spec_ref.get("path"))
        criteria_hash = digest(spec_path.read_bytes())
        require(criteria_hash == spec_ref.get("sha256"), "Approved Spec bytes changed")
        spec = metadata(spec_path)
        require(spec.get("status") == "APPROVED" and nonempty(spec.get("approval_ref")), "Missing approved Spec / approval evidence reference")
        criteria_key = "spec_sha256"
    require(type(task.get("test_required")) is bool, "Explicit test profile required")
    if task["test_required"]:
        require(task.get("test") == "PASS", "Required testing has not passed")
    else:
        require(task.get("test") == "N/A" and nonempty(task.get("test_na_reason")), "Test N/A requires selected profile and reason")
    require(task.get("review") == "APPROVE", "Independent review has not approved")

    receipts = json.loads(project_file(root, receipt_path).read_text(encoding="utf-8"))
    require(isinstance(receipts, dict) and nonempty(receipts.get("manager_id")), "Missing runtime Manager identity")
    require(isinstance(receipts.get("agents"), list), "Missing runtime agent receipts")
    agents = {}
    for item in receipts["agents"]:
        require(isinstance(item, dict), "Invalid agent receipt")
        agent_id = item.get("id")
        require(nonempty(agent_id) and agent_id not in agents and agent_id != receipts["manager_id"], "Duplicate, missing or Manager worker identity")
        require(item.get("role") in ("developer", "tester", "reviewer"), "Invalid worker role")
        require(item.get("task_id") == task["id"], "Agent assigned to another Task")
        require(nonempty(item.get("create_ref")) and nonempty(item.get("assignment_ref")), "Missing native creation / assignment reference")
        agents[agent_id] = item
    contributors = task.get("contributors")
    require(isinstance(contributors, list) and contributors and all(nonempty(x) for x in contributors), "Missing contributor identities")
    require(len(contributors) == len(set(contributors)), "Duplicate contributor")
    require(all(x in agents and agents[x]["role"] == "developer" for x in contributors), "Contributor missing provenance or acting as verifier")
    require(all(x in contributors for x, record in agents.items() if record["role"] == "developer"), "Developer omitted from contributors")

    results = receipts.get("results")
    require(isinstance(results, list) and results, "Missing native results")
    roles_seen, result_refs = set(), set()
    for item in results:
        require(isinstance(item, dict), "Invalid result receipt")
        agent_id = item.get("agent_id")
        require(nonempty(agent_id) and agent_id in agents, "Result has no matching created agent")
        role = agents[agent_id]["role"]
        require(item.get("task_id") == task["id"] and item.get(criteria_key) == criteria_hash, "Result Task / criteria mismatch")
        require(item.get("target") == target, "Stale result: different candidate")
        require(nonempty(item.get("result_ref")) and nonempty(item.get("report_ref")), "Missing native result / report reference")
        require(item["result_ref"] not in result_refs, "Native result reused across records")
        result_refs.add(item["result_ref"])
        require(item.get("verdict") == {"developer": "DELIVERED", "tester": "PASS", "reviewer": "APPROVE"}[role], "Failed, pending or invalid worker verdict")
        if role in ("tester", "reviewer"):
            require(agent_id not in contributors, "Contributor cannot independently verify")
        if role == "reviewer":
            require(item.get("no_implementation_edits") is True, "Missing Reviewer no-edit attestation")
        roles_seen.add(role)
    needed = {"developer", "reviewer"} | ({"tester"} if task["test_required"] else set())
    require(needed <= roles_seen, "Missing required role result")
    return {"task_id": task["id"], "profile": profile, "criteria_sha256": criteria_hash, "candidate": target}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task")
    parser.add_argument("--receipts")
    parser.add_argument("--candidate")
    parser.add_argument("--scope-digest", metavar="TASK")
    args = parser.parse_args()
    if args.scope_digest:
        try:
            root = Path(args.repo).resolve(strict=True)
            scope = metadata(project_file(root, args.scope_digest)).get("scope")
            require(isinstance(scope, dict), "Task has no inline scope")
            print(canonical_digest(scope))
            return 0
        except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as exc:
            print(json.dumps({"result": "BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
            return 1
    if not (args.task and args.receipts and args.candidate):
        parser.error("--task, --receipts and --candidate are required unless --scope-digest is used")
    output = {"assurance": "STRUCTURAL", "runtime_authenticated": False, "enforced": False}
    try:
        root = Path(args.repo).resolve(strict=True)
        require(root.is_dir(), "Project root must be a directory")
        output.update(check(root, args.task, args.receipts, args.candidate))
        output["result"] = "CONSISTENT"
        output["next"] = "Verify native provenance, actual authorization and complete candidate scope before acceptance."
        code = 0
    except (ValueError, OSError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        output.update(result="BLOCKED", reason=str(exc))
        code = 1
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
