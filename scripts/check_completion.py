#!/usr/bin/env python3
"""Read-only structural gate. Never authenticates agent records or changes DONE."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


class GateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(r"[<>]", value)


def digest(data):
    return hashlib.sha256(data).hexdigest()


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


def check(root, task_path, receipt_path, selected):
    task = metadata(project_file(root, task_path))
    require(task.get("status") in ("VERIFY", "DONE"), "Task must be VERIFY or DONE")
    require(nonempty(task.get("id")), "Missing task ID")
    require(task.get("blockers") == [], "Blockers must be explicitly empty")
    spec_ref = task.get("spec")
    require(isinstance(spec_ref, dict), "Missing Spec reference")
    spec_path = project_file(root, spec_ref.get("path"))
    spec_hash = digest(spec_path.read_bytes())
    require(spec_hash == spec_ref.get("sha256"), "Approved Spec bytes changed")
    spec = metadata(spec_path)
    require(spec.get("status") == "APPROVED" and nonempty(spec.get("approval_ref")), "Missing approved Spec / approval evidence reference")
    target = candidate(root, selected)
    require(task.get("candidate") == target, "Task is not for the selected final candidate")
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
        require(item.get("task_id") == task["id"] and item.get("spec_sha256") == spec_hash, "Result Task / Spec mismatch")
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
    return {"task_id": task["id"], "candidate": target}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--receipts", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
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
