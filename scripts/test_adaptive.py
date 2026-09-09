"""Synthetic offline scenarios: no live identities, installation or acceptance."""
import copy
import json
import itertools
import multiprocessing
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import check_completion as gate
import coordinator as coordination
import install_skill
import package_skill as package
import test_package


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit(root, message="fixture"):
    git(root, "add", ".")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", message)
    return git(root, "rev-parse", "HEAD")


class WorkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.outer = Path(self.temp.name).resolve()
        self.root = self.outer / "project"
        self.root.mkdir()
        git(self.root, "init", "-q")
        (self.root / "text.txt").write_text("old text\n")
        self.base = commit(self.root)
        (self.root / "text.txt").write_text("Clear wording\n")
        self.candidate = commit(self.root, "clear wording")
        self.scope = {"outcome": "Make text clearer", "acceptance": ["Text says Clear wording"], "assessment": {"risk": "low", "reversibility": "Git rollback", "coupling": "one standalone text", "uncertainty": "none after reading", "verification_reason": "read exact text"}, "base": self.base, "deliverables": ["text.txt"], "checks": [{"id": "targeted", "capability": "behavior", "independent": False}]}
        self.task = {"format": "work-v1", "id": "TASK-1", "status": "VERIFY", "approval_ref": "fixture:user-request", "scope": self.scope, "candidate": {"kind": "git", "commit": self.candidate}, "contributors": ["main"], "depends_on": [], "dependencies_satisfied": [], "blockers": []}
        self.evidence = {"format": "evidence-v1", "formal_acceptance": False, "identities": [{"id": "main", "contributed": True, "provenance_ref": "fixture:session"}], "checks": []}
        self.refreeze()

    def refreeze(self):
        self.task["scope_sha256"] = gate.canonical_digest(self.scope)
        self.evidence["checks"] = [{"id": check["id"], "actor": "main", "task_id": "TASK-1", "scope_sha256": self.task["scope_sha256"], "target": self.task["candidate"], "status": "PASS", "command": "read text.txt", "environment": "fixture:stdlib", "report_ref": "fixture:report", "result_ref": "fixture:" + check["id"], "no_implementation_edits": True} for check in self.scope["checks"]]

    def check(self):
        (self.root / "task.md").write_text("```json\n" + json.dumps(self.task) + "\n```\n")
        evidence = self.outer / "private-evidence.json"
        evidence.write_text(json.dumps(self.evidence))
        return gate.check(self.root, "task.md", str(evidence), "git:" + self.candidate)

    def blocked(self):
        with self.assertRaises(gate.GateError):
            self.check()

    def test_direct_main_with_private_evidence(self):
        self.assertEqual(self.check()["format"], "work-v1")
        self.assertFalse(self.check()["formal_acceptance"])

    def test_selected_independent_self_check_rejected(self):
        self.scope["checks"][0]["independent"] = True
        self.refreeze()
        self.blocked()

    def test_missing_and_failed_evidence_rejected(self):
        original = copy.deepcopy(self.evidence["checks"])
        self.evidence["checks"] = []
        self.blocked()
        self.evidence["checks"] = original
        self.evidence["checks"][0]["status"] = "FAIL"
        self.blocked()

    def test_scope_missing_deliverables_rejected(self):
        del self.scope["deliverables"]
        self.refreeze()
        self.blocked()

    def test_undeclared_change_rejected(self):
        (self.root / "other.txt").write_text("extra")
        self.candidate = commit(self.root, "extra")
        self.task["candidate"]["commit"] = self.candidate
        self.blocked()

    def test_invalid_ancestry_rejected(self):
        git(self.root, "checkout", "--orphan", "unrelated")
        (self.root / "text.txt").write_text("other")
        other = commit(self.root)
        self.scope["base"] = other
        self.refreeze()
        self.blocked()

    def test_scope_mutation_stale_evidence_rejected(self):
        self.scope["outcome"] = "different"
        self.blocked()

    def test_dependencies_not_silently_ignored(self):
        self.task["depends_on"] = ["TASK-0"]
        self.blocked()

    def test_formal_acceptance_claim_rejected(self):
        self.evidence["formal_acceptance"] = True
        self.blocked()

    def test_one_independent_verifier_can_supply_multiple_checks(self):
        self.scope["checks"] = [{"id": x, "capability": x, "independent": True} for x in ("behavior", "review")]
        self.refreeze()
        self.evidence["identities"].append({"id": "verifier", "contributed": False, "provenance_ref": "fixture:verifier"})
        for item in self.evidence["checks"]:
            item["actor"] = "verifier"
        self.check()

    def test_high_risk_requires_distinct_capabilities_and_people(self):
        self.scope["assessment"]["risk"] = "high"
        self.refreeze()
        self.blocked()
        self.scope["checks"] = [{"id": x, "capability": x, "independent": True} for x in ("behavior", "review")]
        self.refreeze()
        self.evidence["identities"].extend({"id": x, "contributed": False, "provenance_ref": "fixture:" + x} for x in ("tester", "reviewer"))
        for item in self.evidence["checks"]:
            item["actor"] = "tester"
        self.blocked()
        self.evidence["checks"][1]["actor"] = "reviewer"
        self.check()

    def test_high_risk_extra_checks_and_repeated_capability_order_independent(self):
        self.scope["assessment"]["risk"] = "high"
        self.scope["checks"] = [
            {"id": cid, "capability": capability, "independent": True}
            for cid, capability in (("behavior", "behavior"), ("review", "review"),
                                    ("extra", "static"), ("repeat", "behavior"))
        ]
        self.refreeze()
        self.evidence["identities"].extend(
            {"id": actor, "contributed": False, "provenance_ref": "fixture:" + actor}
            for actor in ("tester", "reviewer")
        )
        records = self.evidence["checks"]
        for item in records:
            item["actor"] = "reviewer" if item["id"] == "review" else "tester"
        for extra_actor in ("tester", "reviewer"):
            records[2]["actor"] = extra_actor
            for order in itertools.permutations(records):
                with self.subTest(extra_actor=extra_actor, order=[x["id"] for x in order]):
                    self.evidence["checks"] = list(order)
                    self.check()
        # An extra capability between behavior and review must not erase the
        # behavior actor and thereby permit independent self-review.
        records[1]["actor"] = "tester"
        records[2]["actor"] = "tester"
        self.evidence["checks"] = [records[0], records[2], records[1], records[3]]
        self.blocked()
        # Additional static evidence still requires a non-contributor.
        records[1]["actor"] = "reviewer"
        records[2]["actor"] = "main"
        self.blocked()

    def test_hidden_contributor_rejected(self):
        self.evidence["identities"].append({"id": "repairer", "contributed": True, "provenance_ref": "fixture:repairer"})
        self.blocked()

    def test_spec_original_blob_and_unsafe_objects(self):
        original = b'```json\n{"status":"APPROVED","approval_ref":"fixture:approval"}\n```\n'
        (self.root / "spec.md").write_bytes(original)
        source = commit(self.root)
        (self.root / "spec.md").write_text("sanitized projection")
        self.assertEqual(gate.spec_bytes(self.root, {"path": source + ":spec.md"}), original)
        (self.root / "link.md").symlink_to("spec.md")
        linked = commit(self.root)
        for ref in (source + ":../spec.md", source[:8] + ":spec.md", linked + ":link.md", source + ":.", source + ":missing"):
            with self.subTest(ref=ref), self.assertRaises(gate.GateError):
                gate.spec_bytes(self.root, {"path": ref})

    def test_full_declared_scope_rejects_extra_files(self):
        with self.assertRaises(gate.GateError):
            gate.git_scope(self.root, self.base, self.task["candidate"], ["wrong.txt"])


def race_claim(registry, root, ready, go, results, owner):
    ready.put(True)
    go.wait(10)
    store = None
    try:
        store = coordination.Coordinator(registry)
        store.operate("claim", "fixture-project", "fixture-repository", root, owner)
        results.put("claimed")
    except Exception:
        results.put("blocked")
    finally:
        if store:
            store.close()


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.outer = Path(self.temp.name).resolve()
        self.root = self.outer / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        (self.root / "file").write_text("fixture")
        commit(self.root)
        self.path = self.outer / "private" / "ledger.sqlite3"
        self.store = coordination.Coordinator(self.path)
        self.addCleanup(self.store.close)

    def op(self, command, **data):
        return self.store.operate(command, "fixture-project", "fixture-repository", self.root, "owner-one", 1, **data)

    def prepare(self):
        self.op("claim")
        self.op("begin", attempt="a1", task="TASK-1", work_key="review", inputs="scope-candidate-digest")

    def test_multiprocess_claim_exactly_one_winner(self):
        context = multiprocessing.get_context("spawn")
        ready, go, results = context.Queue(), context.Event(), context.Queue()
        processes = [context.Process(target=race_claim, args=(str(self.path), str(self.root), ready, go, results, "owner-" + str(x))) for x in range(2)]
        for process in processes:
            process.start()
        for _ in processes:
            ready.get(timeout=15)
        go.set()
        outcomes = [results.get(timeout=15) for _ in processes]
        for process in processes:
            process.join(timeout=15)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual(sorted(outcomes), ["blocked", "claimed"])

    def test_uncertain_retry_blocks_but_other_check_can_run(self):
        self.prepare()
        self.op("uncertain", attempt="a1")
        with self.assertRaises(coordination.CoordinationError):
            self.op("begin", attempt="a2", task="TASK-1", work_key="review", inputs="same")
        self.op("begin", attempt="test1", task="TASK-1", work_key="behavior", inputs="same")
        self.op("resolve", attempt="a1", resolution_ref="fixture:native-no-creation")
        self.op("begin", attempt="a2", task="TASK-1", work_key="review", inputs="same")

    def test_result_dedup_and_conflicting_duplicate(self):
        self.prepare()
        self.op("dispatch", attempt="a1", native="fixture-worker")
        result = dict(attempt="a1", native="fixture-worker", inputs="scope-candidate-digest", result_ref="fixture:result", payload={"verdict": "PASS"})
        self.op("result", **result)
        self.op("result", **result)
        result["payload"] = {"verdict": "FAIL"}
        with self.assertRaises(coordination.CoordinationError):
            self.op("result", **result)

    def test_generation_guards_old_writes_and_late_results(self):
        self.prepare()
        self.op("dispatch", attempt="a1", native="fixture-worker")
        row = self.op("recover", new_owner="owner-two", recovery_ref="fixture:confirmed-stopped")
        self.assertEqual(row["generation"], 2)
        with self.assertRaises(coordination.CoordinationError):
            self.op("update", context={"bad": True})
        with self.assertRaises(coordination.CoordinationError):
            self.store.operate("result", "fixture-project", "fixture-repository", self.root, "owner-two", 2, attempt="a1", native="fixture-worker", inputs="scope-candidate-digest", result_ref="fixture:late", payload={})

    def test_no_timeout_steal_and_release_requires_resolution(self):
        self.prepare()
        with self.assertRaises(coordination.CoordinationError):
            self.op("claim")
        with self.assertRaises(coordination.CoordinationError):
            self.op("release")
        with self.assertRaises(coordination.CoordinationError):
            self.op("recover", new_owner="owner-two")
        self.op("resolve", attempt="a1", resolution_ref="fixture:stopped")
        self.op("release")
        self.assertEqual(self.op("claim")["generation"], 2)

    def test_linked_worktree_and_clone_share_project_claim(self):
        self.op("claim")
        linked = self.outer / "linked"
        git(self.root, "worktree", "add", "-qb", "worker", str(linked))
        with self.assertRaises(coordination.CoordinationError):
            self.store.operate("claim", "fixture-project", "fixture-repository", linked, "other")
        with self.assertRaises(coordination.CoordinationError):
            self.store.operate("claim", "different-project", "different-repository", linked, "other")
        cloned = self.outer / "clone"
        subprocess.run(["git", "clone", "-q", str(self.root), str(cloned)], check=True)
        git(cloned, "remote", "set-url", "origin", "fixture-repository")
        with self.assertRaises(coordination.CoordinationError):
            self.store.operate("claim", "fixture-project", "fixture-repository", cloned, "other")

    def test_identity_conflict_and_registry_in_checkout_rejected(self):
        self.op("claim")
        with self.assertRaises(coordination.CoordinationError):
            self.store.operate("status", "fixture-project", "different", self.root)
        sub = self.root / "nested"
        sub.mkdir()
        bad = coordination.Coordinator(self.root / "private.sqlite3")
        try:
            with self.assertRaises(coordination.CoordinationError):
                bad.operate("claim", "fixture-project", "fixture-repository", sub, "owner")
        finally:
            bad.close()

    def test_persistent_attempt_cannot_be_reused(self):
        self.prepare()
        self.op("resolve", attempt="a1", resolution_ref="fixture:no-creation")
        second = coordination.Coordinator(self.path)
        try:
            with self.assertRaises(Exception):
                second.operate("begin", "fixture-project", "fixture-repository", self.root, "owner-one", 1, attempt="a1", task="TASK-1", work_key="review", inputs="scope-candidate-digest")
        finally:
            second.close()


class InstallTests(unittest.TestCase):
    setUp = test_package.PackageTests.setUp
    git = test_package.PackageTests.git
    build = test_package.PackageTests.build

    def test_exact_clean_install_and_refuse_overwrite(self):
        archive = self.build()
        target = self.root / "installed"
        install_skill.install(self.root, self.commit, archive, target)
        members = {x.relative_to(target).as_posix() for x in target.rglob("*") if x.is_file()}
        self.assertEqual(members, set(package.RUNTIME_FILES) | {package.MANIFEST_PATH})
        before = (target / "SKILL.md").read_bytes()
        with self.assertRaises(FileExistsError):
            install_skill.install(self.root, self.commit, archive, target)
        self.assertEqual((target / "SKILL.md").read_bytes(), before)

    def test_unsafe_archive_never_creates_target(self):
        archive = self.build()
        with zipfile.ZipFile(archive, "a") as out:
            out.writestr(package.zip_info("../escape"), "bad")
        target = self.root / "installed"
        with self.assertRaises(package.PackageError):
            install_skill.install(self.root, self.commit, archive, target)
        self.assertFalse(target.exists())

    def test_symlink_parent_rejected(self):
        archive = self.build()
        (self.root / "alias").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(package.PackageError):
            install_skill.install(self.root, self.commit, archive, self.root / "alias" / "installed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
