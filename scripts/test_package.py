"""Offline regression tests for deterministic clean Skill archives."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("package_skill.py")
loader = importlib.util.spec_from_file_location("package_skill", SCRIPT)
package = importlib.util.module_from_spec(loader)
loader.loader.exec_module(package)
REPO = SCRIPT.parent.parent


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="package-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for path in package.RUNTIME_FILES:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            content = "---\nmetadata:\n  version: \"2.1.0-dev.1\"\n---\n" if path == "SKILL.md" else "safe runtime content for " + path + "\n"
            target.write_text(content, encoding="utf-8")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.commit = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True).stdout.strip()

    def build(self, name="one.zip"):
        output = self.root / name
        package.build(self.root, self.commit, output)
        return output

    def rewrite(self, source, output, transform):
        with zipfile.ZipFile(source) as current, zipfile.ZipFile(output, "w") as changed:
            for info in current.infolist():
                name, data = transform(info.filename, current.read(info.filename))
                changed.writestr(package.zip_info(name), data)

    def test_working_version_has_one_authoritative_runtime_source(self):
        skill = (REPO / "SKILL.md").read_bytes()
        self.assertRegex(package.package_version(skill), r"^\d+\.\d+\.\d+-dev\.\d+$")
        first_title = (REPO / "references/PROTOCOL.md").read_text(encoding="utf-8").splitlines()[0]
        self.assertNotRegex(first_title, r"\d+\.\d+\.\d+")

    def test_deterministic_build_and_exact_allowlist(self):
        first, second = self.build("one.zip"), self.build("two.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            expected = {package.ARCHIVE_ROOT + "/" + path for path in package.RUNTIME_FILES}
            expected.add(package.ARCHIVE_ROOT + "/" + package.MANIFEST_PATH)
            self.assertEqual(set(archive.namelist()), expected)
            manifest = json.loads(archive.read(package.ARCHIVE_ROOT + "/" + package.MANIFEST_PATH))
            self.assertEqual(manifest["source_commit"], self.commit)
            self.assertEqual(manifest["version"], "2.1.0-dev.1")
            self.assertEqual([item["path"] for item in manifest["files"]], sorted(package.RUNTIME_FILES))

    def test_rejects_extra_member(self):
        archive = self.build()
        with zipfile.ZipFile(archive, "a") as changed:
            changed.writestr(package.zip_info(package.ARCHIVE_ROOT + "/PROJECT_STATE.md"), b"governance")
        with self.assertRaises(package.PackageError):
            package.verify(self.root, self.commit, archive)

    def test_rejects_unsafe_member(self):
        archive, changed = self.build(), self.root / "unsafe.zip"
        target = package.ARCHIVE_ROOT + "/" + package.RUNTIME_FILES[0]
        self.rewrite(archive, changed, lambda name, data: ("../LICENSE", data) if name == target else (name, data))
        with self.assertRaises(package.PackageError):
            package.verify(self.root, self.commit, changed)

    def test_rejects_symlink_member(self):
        archive, changed = self.build(), self.root / "symlink.zip"
        target = package.ARCHIVE_ROOT + "/" + package.RUNTIME_FILES[0]
        with zipfile.ZipFile(archive) as current, zipfile.ZipFile(changed, "w") as output:
            for info in current.infolist():
                new_info = package.zip_info(info.filename)
                if info.filename == target:
                    new_info.external_attr = 0o120777 << 16
                output.writestr(new_info, current.read(info.filename))
        with self.assertRaises(package.PackageError):
            package.verify(self.root, self.commit, changed)

    def test_rejects_hash_or_version_tamper(self):
        archive, changed = self.build(), self.root / "tampered.zip"
        target = package.ARCHIVE_ROOT + "/SKILL.md"
        self.rewrite(archive, changed, lambda name, data: (name, data + b"tampered") if name == target else (name, data))
        with self.assertRaises(package.PackageError):
            package.verify(self.root, self.commit, changed)

    def test_rejects_wrong_source_commit(self):
        archive = self.build()
        (self.root / "LICENSE").write_text("new source bytes\n", encoding="utf-8")
        self.git("add", "LICENSE")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "next")
        next_commit = self.git("rev-parse", "HEAD")
        with self.assertRaises(package.PackageError):
            package.verify(self.root, next_commit, archive)

    def test_rejects_source_leak(self):
        (self.root / "LICENSE").write_text("local /Users/alice/private/project\n", encoding="utf-8")
        self.git("add", "LICENSE")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "leak")
        leak_commit = self.git("rev-parse", "HEAD")
        with self.assertRaises(package.PackageError):
            package.build(self.root, leak_commit, self.root / "leak.zip")

    def test_requires_full_source_commit(self):
        with self.assertRaises(package.PackageError):
            package.build(self.root, self.commit[:8], self.root / "short.zip")


if __name__ == "__main__":
    unittest.main(verbosity=2)
