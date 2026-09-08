#!/usr/bin/env python3
"""Build and verify a deterministic, source-bound Skill ZIP using only stdlib."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath


SKILL_NAME = "project-development"
MANIFEST_PATH = "MANIFEST.json"
ARCHIVE_ROOT = SKILL_NAME
RUNTIME_FILES = (
    "LICENSE",
    "SKILL.md",
    "agents/openai.yaml",
    "references/GATE.md",
    "references/PROTOCOL.md",
    "scripts/check_completion.py",
    "scripts/package_skill.py",
    "templates/AGENTS.template.md",
    "templates/DECISIONS.template.md",
    "templates/PROJECT_STATE.template.md",
    "templates/SPEC.template.md",
    "templates/TASK-LIGHTWEIGHT.template.md",
    "templates/TASK.template.md",
)
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
VERSION_RE = re.compile(r'^\s*version:\s*["\']([^"\']+)["\']\s*$', re.M)
FULL_COMMIT_RE = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
CONCRETE_LEAKS = (
    ("absolute home path", re.compile(rb"/(?:Users|home)/[^/\s]+/")),
    ("Windows user path", re.compile(rb"[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\")),
    ("native runtime UUID", re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I)),
    ("private key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


class PackageError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PackageError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run_git(repo, *args, binary=False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=False,
        text=not binary, timeout=30,
    )
    stderr = result.stderr.decode(errors="replace") if binary else result.stderr
    require(result.returncode == 0, "Git command failed: " + stderr.strip())
    return result.stdout


def explicit_commit(repo, source):
    require(FULL_COMMIT_RE.fullmatch(source or "") is not None, "--source must be a full lowercase Git commit ID")
    resolved = run_git(repo, "rev-parse", "--verify", source + "^{commit}").strip()
    require(source == resolved, "--source must identify the exact resolved commit")
    return resolved


def source_file(repo, commit, path):
    record = run_git(repo, "ls-tree", commit, "--", path).strip().split()
    require(len(record) >= 4 and record[1] == "blob", "Missing runtime source file: " + path)
    require(record[0] in ("100644", "100755"), "Runtime source must be a regular file: " + path)
    return run_git(repo, "show", commit + ":" + path, binary=True)


def package_version(skill_bytes):
    match = VERSION_RE.search(skill_bytes.decode("utf-8"))
    require(match is not None, "SKILL.md must contain quoted metadata.version")
    return match.group(1)


def reject_leaks(path, data):
    for label, pattern in CONCRETE_LEAKS:
        require(pattern.search(data) is None, "Rejected %s in %s" % (label, path))


def source_payload(repo, commit):
    payload = {}
    for path in RUNTIME_FILES:
        data = source_file(repo, commit, path)
        reject_leaks(path, data)
        payload[path] = data
    return payload


def canonical_manifest(version, commit, payload):
    manifest = {
        "files": [{"path": path, "sha256": sha256(payload[path])} for path in sorted(payload)],
        "format": "project-development-skill-archive-v1",
        "skill": SKILL_NAME,
        "source_commit": commit,
        "version": version,
    }
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def zip_info(name):
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits = 0x800
    return info


def build(repo, source, output):
    repo = Path(repo).resolve(strict=True)
    commit = explicit_commit(repo, source)
    payload = source_payload(repo, commit)
    version = package_version(payload["SKILL.md"])
    manifest = canonical_manifest(version, commit, payload)
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(zip_info(ARCHIVE_ROOT + "/" + MANIFEST_PATH), manifest, compresslevel=9)
        for path in sorted(payload):
            archive.writestr(zip_info(ARCHIVE_ROOT + "/" + path), payload[path], compresslevel=9)
    verify(repo, source, output)
    return {"archive": str(output), "sha256": sha256(output.read_bytes()), "source_commit": commit, "version": version}


def safe_member(name):
    path = PurePosixPath(name)
    require(name == path.as_posix() and not path.is_absolute(), "Unsafe archive member: " + name)
    require(".." not in path.parts and "" not in path.parts, "Unsafe archive member: " + name)
    require("\\" not in name and not name.endswith("/"), "Unsafe archive member: " + name)


def verify(repo, source, archive_path):
    repo = Path(repo).resolve(strict=True)
    commit = explicit_commit(repo, source)
    expected_payload = source_payload(repo, commit)
    expected_version = package_version(expected_payload["SKILL.md"])
    expected_names = {ARCHIVE_ROOT + "/" + path for path in RUNTIME_FILES}
    expected_names.add(ARCHIVE_ROOT + "/" + MANIFEST_PATH)
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        require(len(names) == len(set(names)), "Duplicate archive member")
        for item in infos:
            safe_member(item.filename)
            mode = (item.external_attr >> 16) & 0o170000
            require(mode in (0, 0o100000), "Archive contains a non-regular member: " + item.filename)
            require(item.date_time == ZIP_TIME and item.compress_type == zipfile.ZIP_DEFLATED, "Archive member encoding is not canonical: " + item.filename)
            require(item.flag_bits & 1 == 0, "Encrypted archive members are not allowed: " + item.filename)
            require(item.file_size <= 2_000_000, "Archive member is unexpectedly large: " + item.filename)
        require(set(names) == expected_names, "Archive members do not match the exact runtime allowlist")
        manifest_bytes = archive.read(ARCHIVE_ROOT + "/" + MANIFEST_PATH)
        reject_leaks(MANIFEST_PATH, manifest_bytes)
        manifest = json.loads(manifest_bytes)
        require(manifest_bytes == canonical_manifest(expected_version, commit, expected_payload), "Manifest is not canonical or source-bound")
        require(manifest.get("skill") == SKILL_NAME, "Manifest skill mismatch")
        require(manifest.get("version") == expected_version, "Manifest version mismatch")
        require(manifest.get("source_commit") == commit, "Manifest source commit mismatch")
        for path in RUNTIME_FILES:
            data = archive.read(ARCHIVE_ROOT + "/" + path)
            reject_leaks(path, data)
            require(data == expected_payload[path], "Archive file differs from source commit: " + path)
    return {"archive": str(Path(archive_path).resolve()), "sha256": sha256(Path(archive_path).read_bytes()), "source_commit": commit, "version": expected_version}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--repo", default=".")
    build_parser.add_argument("--source", required=True)
    build_parser.add_argument("--output", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--repo", default=".")
    verify_parser.add_argument("--source", required=True)
    verify_parser.add_argument("--archive", required=True)
    args = parser.parse_args(argv)
    try:
        result = build(args.repo, args.source, args.output) if args.command == "build" else verify(args.repo, args.source, args.archive)
        result["result"] = "VERIFIED"
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, PackageError, RuntimeError, subprocess.SubprocessError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "REJECTED", "reason": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
