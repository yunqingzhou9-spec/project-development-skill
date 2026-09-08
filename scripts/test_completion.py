"""Offline regression tests; all identities are synthetic, never live acceptance receipts."""

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_completion.py")
loader = importlib.util.spec_from_file_location("completion_gate", SCRIPT)
gate = importlib.util.module_from_spec(loader)
loader.loader.exec_module(gate)


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="completion-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "result.txt").write_text("verified output\n", encoding="utf-8")
        self.spec = {"id": "SPEC-1", "status": "APPROVED", "approval_ref": "fixture-only:user-request-1"}
        self.write_meta("spec.md", self.spec)
        spec_hash = gate.digest((self.root / "spec.md").read_bytes())
        self.target = {"kind": "files", "files": [{"path": "result.txt", "sha256": gate.digest((self.root / "result.txt").read_bytes())}]}
        self.task = {"id": "TASK-1", "status": "VERIFY", "spec": {"path": "spec.md", "sha256": spec_hash}, "candidate": self.target, "contributors": ["fixture-dev"], "test_required": True, "test": "PASS", "review": "APPROVE", "blockers": []}
        self.receipts = {"manager_id": "fixture-manager", "agents": [], "results": []}
        for role, short, verdict in [("developer", "dev", "DELIVERED"), ("tester", "test", "PASS"), ("reviewer", "review", "APPROVE")]:
            agent_id = "fixture-" + short
            self.receipts["agents"].append({"id": agent_id, "role": role, "task_id": "TASK-1", "create_ref": "fixture:create:" + short, "assignment_ref": "fixture:assign:" + short})
            self.receipts["results"].append({"agent_id": agent_id, "task_id": "TASK-1", "spec_sha256": spec_hash, "target": copy.deepcopy(self.target), "verdict": verdict, "result_ref": "fixture:result:" + short, "report_ref": "fixture:report:" + short, "no_implementation_edits": True})

    def write_meta(self, name, data):
        (self.root / name).write_text("# Fixture\n\n```json\n" + json.dumps(data) + "\n```\n", encoding="utf-8")

    def persist(self):
        self.write_meta("task.md", self.task)
        (self.root / "receipts.json").write_text(json.dumps(self.receipts), encoding="utf-8")
        (self.root / "candidate.json").write_text(json.dumps(self.target), encoding="utf-8")

    def run_gate(self, selected="files:candidate.json"):
        self.persist()
        return gate.check(self.root, "task.md", "receipts.json", selected)

    def blocked(self):
        with self.assertRaises(gate.GateError):
            self.run_gate()

    def test_valid_file_candidate(self):
        result = self.run_gate()
        self.assertEqual(result["candidate"], self.target)
        self.assertEqual(result["profile"], "FULL")

    def test_missing_test_role(self):
        self.receipts["results"].pop(1)
        self.blocked()

    def test_same_worker_multiple_roles(self):
        self.receipts["agents"][2]["id"] = "fixture-dev"
        self.blocked()

    def test_manager_impersonates_worker(self):
        self.receipts["manager_id"] = "fixture-review"
        self.blocked()

    def test_reviewer_repaired_code(self):
        self.task["contributors"].append("fixture-review")
        self.blocked()

    def test_reviewer_missing_no_edit_attestation(self):
        self.receipts["results"][2].pop("no_implementation_edits")
        self.blocked()

    def test_spec_edited_after_approval(self):
        (self.root / "spec.md").write_text((self.root / "spec.md").read_text() + "Changed scope\n")
        self.blocked()

    def test_draft_spec(self):
        self.spec["status"] = "DRAFT"
        self.write_meta("spec.md", self.spec)
        self.task["spec"]["sha256"] = gate.digest((self.root / "spec.md").read_bytes())
        self.blocked()

    def test_missing_approval_ref(self):
        self.spec["approval_ref"] = None
        self.write_meta("spec.md", self.spec)
        self.task["spec"]["sha256"] = gate.digest((self.root / "spec.md").read_bytes())
        self.blocked()

    def test_stale_review(self):
        self.receipts["results"][2]["target"]["files"][0]["sha256"] = "0" * 64
        self.blocked()

    def test_stale_spec_result(self):
        self.receipts["results"][2]["spec_sha256"] = "0" * 64
        self.blocked()

    def test_artifact_changed(self):
        (self.root / "result.txt").write_text("new output")
        self.blocked()

    def test_unresolved_blocker(self):
        self.task["blockers"] = ["Acceptance failure"]
        self.blocked()

    def test_failure_cannot_be_hidden_by_task_summary(self):
        self.receipts["results"][1]["verdict"] = "FAIL"
        self.blocked()

    def test_other_task_result(self):
        self.receipts["results"][1]["task_id"] = "TASK-2"
        self.blocked()

    def test_missing_native_reference(self):
        self.receipts["agents"][2]["create_ref"] = ""
        self.blocked()

    def test_receipt_reused(self):
        self.receipts["results"][2]["result_ref"] = self.receipts["results"][1]["result_ref"]
        self.blocked()

    def test_test_na_with_reason(self):
        self.task.update(test_required=False, test="N/A", test_na_reason="Approved docs-only profile; no executable behavior")
        self.receipts["agents"].pop(1)
        self.receipts["results"].pop(1)
        self.assertEqual(self.run_gate()["task_id"], "TASK-1")

    def test_na_without_reason(self):
        self.task.update(test_required=False, test="N/A")
        self.blocked()

    def test_profile_must_be_boolean(self):
        self.task["test_required"] = "false"
        self.blocked()

    def test_unrecorded_contributor(self):
        self.task["contributors"].append("fixture-other")
        self.blocked()

    def test_path_escape(self):
        self.target["files"][0]["path"] = "../outside.txt"
        self.blocked()

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="outside-test-") as outside:
            path = Path(outside) / "outside.txt"
            path.write_text("outside")
            (self.root / "link.txt").symlink_to(path)
            self.target["files"][0]["path"] = "link.txt"
            self.blocked()

    def test_duplicate_snapshot_path(self):
        self.target["files"].append(copy.deepcopy(self.target["files"][0]))
        self.blocked()

    def test_nonexistent_git_commit(self):
        self.persist()
        with self.assertRaises(gate.GateError):
            gate.check(self.root, "task.md", "receipts.json", "git:" + "a" * 40)

    def test_git_candidate(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("add", "result.txt")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        commit = git("rev-parse", "HEAD")
        self.target = {"kind": "git", "commit": commit}
        self.task["candidate"] = self.target
        for item in self.receipts["results"]:
            item["target"] = self.target
        self.assertEqual(self.run_gate("git:" + commit)["candidate"], self.target)

    def make_lightweight(self, lines="small change\n"):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("add", "result.txt")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "base")
        base = git("rev-parse", "HEAD")
        (self.root / "result.txt").write_text(lines, encoding="utf-8")
        git("add", "result.txt")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "candidate")
        commit = git("rev-parse", "HEAD")
        scope = {
            "outcome": "Change one fixture output",
            "acceptance": ["result.txt contains the requested output"],
            "deliverables": ["result.txt"],
            "verification": "check result.txt",
            "eligibility": {
                "single_outcome": True,
                "no_dependencies_or_integration": True,
                "ordinary_git_rollback": True,
                "targeted_verification_known": True,
                "independent_implementer_and_reviewer": True,
                "risk_categories_absent": True,
                "no_conflict_or_unresolved_choice": True,
            },
        }
        self.target = {"kind": "git", "commit": commit}
        self.task = {
            "id": "TASK-1", "profile": "LIGHTWEIGHT", "status": "VERIFY",
            "approval_ref": "fixture-only:user-request-1", "scope": scope,
            "scope_sha256": gate.canonical_digest(scope), "depends_on": [], "base": base,
            "candidate": self.target, "contributors": ["fixture-dev"],
            "test_required": False, "test_na_reason": "Eligible low-risk targeted check", "test": "N/A",
            "review": "APPROVE", "blockers": [],
        }
        self.receipts["agents"].pop(1)
        self.receipts["results"].pop(1)
        for item in self.receipts["results"]:
            item.pop("spec_sha256", None)
            item["scope_sha256"] = self.task["scope_sha256"]
            item["target"] = copy.deepcopy(self.target)
        return commit

    def test_lightweight_valid_without_spec_or_tester(self):
        commit = self.make_lightweight()
        result = self.run_gate("git:" + commit)
        self.assertEqual(result["profile"], "LIGHTWEIGHT")

    def test_lightweight_scope_digest_change_blocks(self):
        commit = self.make_lightweight()
        self.task["scope"]["outcome"] = "Widened outcome"
        with self.assertRaises(gate.GateError):
            self.run_gate("git:" + commit)

    def test_lightweight_false_eligibility_blocks(self):
        commit = self.make_lightweight()
        self.task["scope"]["eligibility"]["risk_categories_absent"] = False
        self.task["scope_sha256"] = gate.canonical_digest(self.task["scope"])
        for item in self.receipts["results"]:
            item["scope_sha256"] = self.task["scope_sha256"]
        with self.assertRaises(gate.GateError):
            self.run_gate("git:" + commit)

    def test_lightweight_over_200_lines_blocks(self):
        commit = self.make_lightweight("".join("line %d\n" % number for number in range(201)))
        with self.assertRaises(gate.GateError):
            self.run_gate("git:" + commit)

    def test_scope_digest_cli(self):
        self.make_lightweight()
        self.persist()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.root), "--scope-digest", "task.md"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.task["scope_sha256"])

    def test_cli_never_claims_authenticity_and_does_not_write(self):
        self.persist()
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.iterdir() if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root), "--task", "task.md", "--receipts", "receipts.json", "--candidate", "files:candidate.json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertFalse(output["runtime_authenticated"])
        self.assertFalse(output["enforced"])
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.iterdir() if p.is_file()}
        self.assertEqual(before, after)

    def test_cli_malformed_json_blocks_cleanly(self):
        self.persist()
        (self.root / "receipts.json").write_text("{")
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root), "--task", "task.md", "--receipts", "receipts.json", "--candidate", "files:candidate.json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["result"], "BLOCKED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
