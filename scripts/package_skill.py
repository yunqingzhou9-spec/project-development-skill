#!/usr/bin/env python3
"""Build and verify a deterministic, source-bound Skill ZIP using only stdlib."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
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
    "templates/TASK.template.md",
)
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
FULL_COMMIT_RE = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
CONCRETE_LEAKS = (
    ("native runtime UUID", re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)),
    ("private key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
PLACEHOLDER_TOKEN_RE = re.compile(r"\S*<[^>\r\n]+>\S*")
GENERIC_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.:/-])/path/to/project(?=$|[\s'\"`)},;])")
POSIX_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.:<>/-])/[A-Za-z0-9._~-]+(?:/[A-Za-z0-9._~() -]+)*")
WINDOWS_DRIVE_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])[A-Za-z]:[\\/][A-Za-z0-9._~$ -]+")
WINDOWS_UNC_PATH_RE = re.compile(r"(?<!\\)\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9._$ -]+")


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
    text = skill_bytes.decode("utf-8")
    lines = text.splitlines()
    require(lines and lines[0] == "---", "SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise PackageError("SKILL.md frontmatter is not closed")
    stack = []
    version_values = []
    metadata_count = 0
    block_scalar_indent = None
    key_pattern = re.compile(r"^( *)([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$")
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        leading = len(line) - len(line.lstrip(" "))
        if block_scalar_indent is not None:
            if leading > block_scalar_indent:
                continue
            block_scalar_indent = None
        require("\t" not in line, "Tabs are not allowed in SKILL.md frontmatter")
        match = key_pattern.match(line)
        require(match is not None, "Unsupported YAML in SKILL.md frontmatter")
        indent, key, scalar = len(match.group(1)), match.group(2), match.group(3)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = [item[1] for item in stack] + [key]
        if path == ["metadata"]:
            metadata_count += 1
        if key == "version":
            require(path == ["metadata", "version"], "version must be metadata.version in SKILL.md frontmatter")
            version_values.append(scalar)
        if not scalar or scalar.startswith("#"):
            stack.append((indent, key))
        elif scalar in ("|", "|-", "|+", ">", ">-", ">+"):
            block_scalar_indent = indent
    require(metadata_count == 1, "SKILL.md must contain exactly one metadata mapping")
    require(len(version_values) == 1, "SKILL.md must contain exactly one metadata.version")
    scalar = version_values[0]
    quoted = re.fullmatch(r'(["\'])([^"\']+)\1(?:\s+#.*)?', scalar)
    if quoted:
        version = quoted.group(2)
    else:
        require("#" not in scalar and not re.search(r"\s", scalar), "metadata.version must be one scalar")
        version = scalar
    match = SEMVER_RE.fullmatch(version)
    require(match is not None, "metadata.version must be valid SemVer")
    prerelease = match.group(4)
    if prerelease:
        require(all(not (part.isdigit() and len(part) > 1 and part.startswith("0")) for part in prerelease.split(".")), "SemVer numeric prerelease identifiers cannot have leading zeroes")
    return version


def reject_leaks(path, data):
    for label, pattern in CONCRETE_LEAKS:
        require(pattern.search(data) is None, "Rejected %s in %s" % (label, path))
    text = data.decode("utf-8")
    for line in text.splitlines():
        if line.startswith("#!/usr/bin/env"):
            line = line[len("#!/usr/bin/env"):]
        line = PLACEHOLDER_TOKEN_RE.sub("", line)
        line = GENERIC_PATH_RE.sub("", line)
        require(POSIX_PATH_RE.search(line) is None, "Rejected absolute POSIX path in " + path)
        require(WINDOWS_DRIVE_PATH_RE.search(line) is None, "Rejected absolute Windows drive path in " + path)
        require(WINDOWS_UNC_PATH_RE.search(line) is None, "Rejected absolute Windows UNC path in " + path)


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
    temporary = tempfile.NamedTemporaryFile(prefix="." + output.name + ".", suffix=".tmp", dir=output.parent, delete=False)
    temporary_path = Path(temporary.name)
    temporary.close()
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            archive.writestr(zip_info(ARCHIVE_ROOT + "/" + MANIFEST_PATH), manifest, compresslevel=9)
            for path in sorted(payload):
                archive.writestr(zip_info(ARCHIVE_ROOT + "/" + path), payload[path], compresslevel=9)
        verify(repo, source, temporary_path)
        temporary_path.chmod(0o644)
        os.replace(temporary_path, output)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
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
