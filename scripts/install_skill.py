#!/usr/bin/env python3
"""Install a verified clean archive into a new directory, never overwrite."""
import argparse
import io
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
import package_skill as package


def install(repo, source, archive, destination):
    # Snapshot once: source verification and writes consume identical archive bytes.
    data = Path(archive).read_bytes()
    import tempfile
    with tempfile.TemporaryDirectory(prefix="skill-verify-") as temporary:
        copy = Path(temporary) / "package.zip"
        copy.write_bytes(data)
        verified = package.verify(repo, source, copy)
    target = Path(destination).absolute()
    for parent in (target, *target.parents):
        package.require(not parent.is_symlink(), "Installation path cannot contain symlinks")
    package.require(target.parent.is_dir(), "Create the installation parent explicitly first")
    # mkdir is exclusive, including an empty existing directory or racing installer.
    target.mkdir(mode=0o700)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as source_zip:
            for relative in (*package.RUNTIME_FILES, package.MANIFEST_PATH):
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as output:
                    output.write(source_zip.read(package.ARCHIVE_ROOT + "/" + relative))
                path.chmod(0o644)
        expected = set(package.RUNTIME_FILES) | {package.MANIFEST_PATH}
        package.require({p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()} == expected, "Installed membership mismatch")
    except Exception:
        shutil.rmtree(target)
        raise
    return {"result": "INSTALLED", "destination": str(target), "source_commit": verified["source_commit"], "version": verified["version"], "sha256": package.sha256(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "source", "archive", "destination"):
        parser.add_argument("--" + name, required=True)
    try:
        print(json.dumps(install(**vars(parser.parse_args())), sort_keys=True))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print(json.dumps({"result": "REJECTED", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
