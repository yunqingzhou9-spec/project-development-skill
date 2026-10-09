#!/usr/bin/env python3
"""Cooperative same-host ownership and durable dispatch ledger; no shell fencing."""
import argparse
import hashlib
import platform
import plistlib
import uuid
from datetime import datetime, timezone
import json
import os
import socket
import sqlite3
import subprocess
from pathlib import Path


class CoordinationError(ValueError):
    pass


def require(value, message):
    if not value:
        raise CoordinationError(message)


def default_registry():
    return Path.home() / ".local" / "state" / "project-development" / "coordination.sqlite3"


def machine_identity():
    """Hash a platform-owned stable ID; never use network hostname as identity.

    This is cooperative locality checking, not attestation. Cloned OS images or
    privileged ID changes need manual reconciliation. Never print the raw ID.
    """
    system = platform.system()
    try:
        if system == "Darwin":
            tool = str(Path(os.sep) / "usr" / "sbin" / "ioreg")
            result = subprocess.run([tool, "-rd1", "-c", "IOPlatformExpertDevice", "-a"],
                                    capture_output=True, timeout=5, check=True)
            value = plistlib.loads(result.stdout)[0]["IOPlatformUUID"]
        elif system == "Linux":
            value = (Path(os.sep) / "etc" / "machine-id").read_text().strip()
        elif system == "Windows":
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Cryptography", 0,
                                winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
                value = winreg.QueryValueEx(key, "MachineGuid")[0]
        else:
            raise ValueError("unsupported platform")
        normalized = uuid.UUID(value).hex
        require(int(normalized, 16) != 0, "Empty machine identity")
    except (OSError, ValueError, TypeError, KeyError, IndexError, subprocess.SubprocessError) as exc:
        raise CoordinationError("Stable machine identity unavailable; check local OS permissions; no hostname fallback") from exc
    return hashlib.sha256(("project-development:host-v1:" + system + ":" + normalized).encode()).hexdigest()


def rollback_registry(path):
    # mode=ro can create WAL/SHM files. Reject before connecting, including migration.
    require(not path.is_symlink(), "Registry cannot be a symlink")
    with path.open("rb") as source:
        header = source.read(20)
    require(not (len(header) == 20 and (header[18] == 2 or header[19] == 2)),
            "WAL registry requires explicit manual reconciliation; no automatic journal migration")


def check_host(db, identity):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='host'").fetchone():
        raise sqlite3.DatabaseError("Uninitialized registry: missing host table")
    exists = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='machine'").fetchone()
    require(exists, "Legacy hostname registry requires explicit migrate-host with backup and same-machine evidence")
    rows = db.execute("SELECT identity FROM machine").fetchall()
    require(len(rows) == 1 and rows[0][0] == identity, "Cross-host or uninitialized registry unsupported")


def migrate_host(registry, project, repository, checkout, owner, generation,
                 expected_host, backup, evidence_ref, confirm_same_machine=False):
    """Explicit project-scoped legacy reconciliation; cannot prove old machine identity."""
    require(confirm_same_machine, "Explicit same-machine confirmation required")
    path = Path(registry) if registry else default_registry()
    rollback_registry(path)
    identity = machine_identity()
    root, common = repository_identity(checkout, repository)
    require(root not in path.resolve().parents and Path(common) not in path.resolve().parents,
            "Private registry must be outside checkout")
    require(backup and evidence_ref and expected_host, "Backup, evidence and expected legacy hostname required")
    dest, evidence = Path(backup), Path(evidence_ref)
    for item in (dest, evidence):
        require(item.is_absolute() and not item.is_symlink() and
                root not in item.resolve().parents and Path(common) not in item.resolve().parents,
                "Backup and evidence must be private absolute paths outside checkout")
    require(evidence.is_file(), "Existing same-machine evidence file required")
    evidence_bytes = evidence.read_bytes()
    proof = json.loads(evidence_bytes)
    require(isinstance(proof, dict) and all(isinstance(proof.get(k), str) and proof[k].strip()
            for k in ("authorization_ref", "native_check_ref", "same_machine_basis")),
            "Evidence needs authorization, native writer observation and same-machine basis")
    require(not dest.exists(), "Backup must be a new exclusive file")
    db = sqlite3.connect(path.resolve().as_uri() + "?mode=rw", uri=True, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    try:
        db.execute("BEGIN IMMEDIATE")
        stable = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='machine'").fetchone()
        if stable:
            check_host(db, identity)
            require(not db.execute("SELECT 1 FROM host_projects WHERE project=?", (project,)).fetchone(),
                    "Already bound: project cannot repeat legacy migration")
        hosts = db.execute("SELECT name FROM host").fetchall()
        require(len(hosts) == 1 and hosts[0][0] == expected_host, "Legacy host changed; inspect again")
        row = db.execute("SELECT * FROM projects WHERE project=?", (project,)).fetchone()
        require(row is not None and row["repository"] == repository and
                row["owner"] == owner and row["generation"] == generation and row["state"] == "ACTIVE",
                "Migration project/repository/active owner/generation mismatch")
        linked = db.execute("SELECT project FROM roots WHERE common=?", (common,)).fetchone()
        require(linked is not None and linked[0] == project, "Migration requires existing Git common-directory binding")
        require(not db.execute("SELECT 1 FROM attempts WHERE project=? AND state IN ('PREPARED','UNCERTAIN','DISPATCHED')", (project,)).fetchone(),
                "Resolve native attempts before legacy migration")
        # BEGIN IMMEDIATE holds off cooperating writers; rollback format contains
        # the committed snapshot. No DB mutation has occurred before this backup.
        before = path.read_bytes()
        with os.fdopen(os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as out:
            out.write(before)
            out.flush()
            os.fsync(out.fileno())
        audit = {"format": "host-migration-v1", "at": datetime.now(timezone.utc).isoformat(),
                 "legacy_hostname": expected_host, "observed_hostname": socket.gethostname(),
                 "machine_identity": identity, "project": project, "repository": repository,
                 "owner": owner, "generation": generation, "common": common,
                 "backup": str(dest), "backup_sha256": hashlib.sha256(before).hexdigest(),
                 "evidence_ref": str(evidence), "evidence_sha256": hashlib.sha256(evidence_bytes).hexdigest()}
        if not stable:
            db.execute("CREATE TABLE machine (identity TEXT PRIMARY KEY, hostname TEXT NOT NULL)")
            db.execute("INSERT INTO machine VALUES (?,?)", (identity, socket.gethostname()))
            db.execute("CREATE TABLE host_projects (project TEXT PRIMARY KEY)")
            db.execute("CREATE TABLE host_migrations (audit TEXT NOT NULL)")
        db.execute("INSERT INTO host_projects VALUES (?)", (project,))
        db.execute("INSERT INTO host_migrations VALUES (?)", (json.dumps(audit, sort_keys=True),))
        db.commit()
        return {"result": "MIGRATED", "project": project, "generation": generation,
                "state": row["state"], "backup": str(dest), "backup_sha256": audit["backup_sha256"]}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def repository_identity(checkout, declared):
    root = Path(checkout).resolve(strict=True)
    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=15)
    common = git("rev-parse", "--git-common-dir")
    require(common.returncode == 0, "Accessible Git checkout required")
    common_path = (root / common.stdout.strip()).resolve()
    top = git("rev-parse", "--show-toplevel")
    require(top.returncode == 0, "Working checkout required")
    root = Path(top.stdout.strip()).resolve()
    remote = git("remote", "get-url", "origin")
    require(declared and (remote.returncode != 0 or declared == remote.stdout.strip()), "Repository identity conflicts with origin")
    return root, str(common_path)


class Coordinator:
    def __init__(self, registry=None, read_only=False):
        self.path = Path(registry) if registry is not None else default_registry()
        require(not self.path.is_symlink(), "Registry cannot be a symlink")
        self.read_only = read_only
        identity = machine_identity()
        existing = self.path.exists()
        if read_only or existing:
            rollback_registry(self.path)
        if not read_only and not existing:
            self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        mode = "ro" if read_only else ("rw" if existing else "rwc")
        self.db = sqlite3.connect(self.path.resolve().as_uri() + "?mode=" + mode,
                                 timeout=10, isolation_level=None, uri=True)
        self.db.row_factory = sqlite3.Row
        try:
            if read_only:
                self.db.execute("PRAGMA query_only=ON")
                check_host(self.db, identity)
                return
            self.db.execute("BEGIN IMMEDIATE")
            # Recheck tables under the lock: another initializer may have won.
            initialized = self.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='host'").fetchone()
            if initialized:
                check_host(self.db, identity)
            else:
                require(not existing, "Existing registry has no recognized host binding")
                self.db.execute("CREATE TABLE host (name TEXT PRIMARY KEY)")
                self.db.execute("INSERT INTO host VALUES (?)", (socket.gethostname(),))
                self.db.execute("CREATE TABLE machine (identity TEXT PRIMARY KEY, hostname TEXT NOT NULL)")
                self.db.execute("INSERT INTO machine VALUES (?,?)", (identity, socket.gethostname()))
                self.db.execute("CREATE TABLE host_projects (project TEXT PRIMARY KEY)")
                self.db.execute("CREATE TABLE host_migrations (audit TEXT NOT NULL)")
                self.db.execute("CREATE TABLE projects (project TEXT PRIMARY KEY, repository TEXT NOT NULL UNIQUE, owner TEXT NOT NULL, generation INTEGER NOT NULL, state TEXT NOT NULL, context TEXT NOT NULL DEFAULT '{}')")
                self.db.execute("CREATE TABLE roots (common TEXT PRIMARY KEY, project TEXT NOT NULL)")
                self.db.execute("CREATE TABLE attempts (project TEXT NOT NULL, attempt TEXT NOT NULL, task TEXT NOT NULL, work_key TEXT NOT NULL, inputs TEXT NOT NULL, generation INTEGER NOT NULL, state TEXT NOT NULL, native TEXT, result TEXT, payload TEXT, resolution TEXT, PRIMARY KEY(project, attempt))")
            self.db.commit()
            if not existing:
                os.chmod(self.path, 0o600)
        except Exception:
            self.db.rollback()
            self.db.close()
            raise

    def close(self):
        self.db.close()

    def view(self, project, summary=False):
        result = dict(self.db.execute("SELECT * FROM projects WHERE project=?", (project,)).fetchone())
        if summary:
            counts = {r["state"]: r["n"] for r in self.db.execute("SELECT state,COUNT(*) AS n FROM attempts WHERE project=? GROUP BY state", (project,))}
            result.pop("context")
            result["attempt_counts"] = counts
            result["unresolved_attempts"] = [dict(r) for r in self.db.execute("SELECT attempt,task,work_key,generation,state,native FROM attempts WHERE project=? AND state IN ('PREPARED','UNCERTAIN','DISPATCHED') ORDER BY attempt", (project,))]
        else:
            result["attempts"] = [dict(x) for x in self.db.execute("SELECT * FROM attempts WHERE project=? ORDER BY attempt", (project,))]
        return result

    def operate(self, command, project, repository, checkout, owner=None, generation=None, **data):
        require(all(isinstance(x, str) and x.strip() for x in (project, repository)), "Project and repository identity required")
        root, common = repository_identity(checkout, repository)
        require(root not in self.path.resolve().parents and Path(common) not in self.path.resolve().parents, "Private registry must be outside checkout")
        observing = command in ("status", "assert")
        require(observing or not self.read_only, "Read-only registry cannot mutate coordination")
        self.db.execute("BEGIN" if observing else "BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM projects WHERE project=?", (project,)).fetchone()
            if row is not None:
                require(self.db.execute("SELECT 1 FROM host_projects WHERE project=?", (project,)).fetchone(),
                        "Legacy project requires explicit migrate-host; another project's migration grants no authority")
            other = self.db.execute("SELECT project FROM projects WHERE repository=?", (repository,)).fetchone()
            linked = self.db.execute("SELECT project FROM roots WHERE common=?", (common,)).fetchone()
            require(other is None or other[0] == project, "Repository already bound to another Project ID")
            require(linked is None or linked[0] == project, "Linked checkout has conflicting Project ID")
            require(row is None or row["repository"] == repository, "Project has conflicting repository identity")
            if command == "claim":
                require(owner, "Owner reference required")
                require(row is None or row["state"] == "RELEASED", "Project already owned; inspect and explicitly release/recover")
                expected = data.get("expected_generation")
                require(expected is None or (row is not None and row["generation"] == expected), "Released generation changed; inspect again")
                require(not self.db.execute("SELECT 1 FROM attempts WHERE project=? AND state IN ('PREPARED','UNCERTAIN','DISPATCHED')", (project,)).fetchone(), "Unresolved attempts block claim")
                next_gen = 1 if row is None else row["generation"] + 1
                self.db.execute("INSERT INTO projects VALUES (?,?,?,?,?,'{}') ON CONFLICT(project) DO UPDATE SET owner=excluded.owner,generation=excluded.generation,state=excluded.state", (project, repository, owner, next_gen, "ACTIVE"))
            elif command == "status":
                require(row is not None, "Project not registered")
            else:
                require(row is not None and row["state"] == "ACTIVE" and row["owner"] == owner and row["generation"] == generation, "Stale or missing ownership generation")
                if command == "recover":
                    require(data.get("new_owner") and data.get("recovery_ref"), "Recovery requires observed old owner/generation and explicit writer-stopped/reconnected evidence")
                    self.db.execute("UPDATE projects SET owner=?,generation=generation+1,context=? WHERE project=?", (data["new_owner"], json.dumps({"recovery_ref": data["recovery_ref"]}), project))
                elif command == "release":
                    require(not self.db.execute("SELECT 1 FROM attempts WHERE project=? AND state IN ('PREPARED','UNCERTAIN','DISPATCHED')", (project,)).fetchone(), "Resolve/reconnect active attempts before release")
                    self.db.execute("UPDATE projects SET state='RELEASED' WHERE project=?", (project,))
                elif command == "assert":
                    pass
                elif command == "update":
                    require(isinstance(data.get("context"), dict), "Context must be an object")
                    self.db.execute("UPDATE projects SET context=? WHERE project=?", (json.dumps(data["context"], sort_keys=True), project))
                elif command == "begin":
                    require(all(data.get(x) for x in ("attempt", "task", "work_key", "inputs")), "Attempt, task, logical work key and bound inputs required")
                    require(not self.db.execute("SELECT 1 FROM attempts WHERE project=? AND task=? AND work_key=? AND state IN ('PREPARED','UNCERTAIN','DISPATCHED')", (project, data["task"], data["work_key"])).fetchone(), "Outstanding/uncertain creation: reconcile before retry")
                    self.db.execute("INSERT INTO attempts(project,attempt,task,work_key,inputs,generation,state) VALUES(?,?,?,?,?,?,'PREPARED')", (project, data["attempt"], data["task"], data["work_key"], data["inputs"], generation))
                else:
                    attempt = self.db.execute("SELECT * FROM attempts WHERE project=? AND attempt=?", (project, data.get("attempt"))).fetchone()
                    require(attempt is not None, "Unknown attempt")
                    if command == "resolve":
                        require(attempt["state"] in ("PREPARED", "UNCERTAIN", "DISPATCHED") and data.get("resolution_ref"), "Resolve needs native reconciliation evidence")
                        # An explicit resolution can retire an old-generation attempt; never accepts its result.
                        self.db.execute("UPDATE attempts SET state='RESOLVED',resolution=? WHERE project=? AND attempt=?", (data["resolution_ref"], project, data["attempt"]))
                    else:
                        require(attempt["generation"] == generation, "Late old-generation attempt")
                        if command == "uncertain":
                            require(attempt["state"] == "PREPARED", "Only prepared creation may become uncertain")
                            self.db.execute("UPDATE attempts SET state='UNCERTAIN' WHERE project=? AND attempt=?", (project, data["attempt"]))
                        elif command == "dispatch":
                            require(attempt["state"] in ("PREPARED", "UNCERTAIN") and data.get("native"), "Dispatch needs reconciled native identity")
                            self.db.execute("UPDATE attempts SET state='DISPATCHED',native=? WHERE project=? AND attempt=?", (data["native"], project, data["attempt"]))
                        elif command == "result":
                            require(data.get("native") == attempt["native"] and data.get("inputs") == attempt["inputs"] and data.get("result_ref") and isinstance(data.get("payload"), dict), "Result identity/inputs mismatch")
                            payload = json.dumps(data["payload"], sort_keys=True, separators=(",", ":"))
                            require(attempt["state"] == "DISPATCHED" or (attempt["state"] == "COMPLETE" and attempt["result"] == data["result_ref"] and attempt["payload"] == payload), "Duplicate or conflicting result")
                            reused = self.db.execute("SELECT attempt FROM attempts WHERE project=? AND result=? AND attempt<>?", (project, data["result_ref"], data["attempt"])).fetchone()
                            require(reused is None, "Result already belongs to another attempt")
                            self.db.execute("UPDATE attempts SET state='COMPLETE',result=?,payload=? WHERE project=? AND attempt=?", (data["result_ref"], payload, project, data["attempt"]))
                        else:
                            raise CoordinationError("Unknown operation")
            if not observing:
                if command == "claim":
                    self.db.execute("INSERT OR IGNORE INTO host_projects VALUES (?)", (project,))
                self.db.execute("INSERT OR IGNORE INTO roots VALUES (?,?)", (common, project))
                if command in ("claim", "release") and data.get("context") is not None:
                    require(isinstance(data["context"], dict), "Context must be an object")
                    self.db.execute("UPDATE projects SET context=? WHERE project=?", (json.dumps(data["context"], sort_keys=True), project))
            result = self.view(project, summary=data.get("summary", False))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["migrate-host", "claim", "status", "assert", "update", "release", "recover", "begin", "uncertain", "dispatch", "result", "resolve"])
    parser.add_argument("--registry")
    parser.add_argument("--confirm-same-machine", action="store_true")
    parser.add_argument("--expected-host")
    parser.add_argument("--backup")
    parser.add_argument("--evidence-ref")
    parser.add_argument("--summary", action="store_true", help="Compact state, counts and unresolved attempts; omit historical payloads")
    parser.add_argument("--expected-generation", type=int, help="Compare released generation before claim")
    for name in ("project", "repository", "checkout"):
        parser.add_argument("--" + name, required=True)
    for name in ("owner", "new-owner", "recovery-ref", "attempt", "task", "work-key", "inputs", "native", "result-ref", "resolution-ref"):
        parser.add_argument("--" + name)
    parser.add_argument("--generation", type=int)
    parser.add_argument("--context", type=json.loads)
    parser.add_argument("--payload", type=json.loads)
    args = vars(parser.parse_args())
    coordinator = None
    try:
        if args["command"] == "migrate-host":
            fields = ("registry", "project", "repository", "checkout", "owner", "generation",
                      "expected_host", "backup", "evidence_ref", "confirm_same_machine")
            print(json.dumps(migrate_host(**{key: args[key] for key in fields}), sort_keys=True))
            return 0
        coordinator = Coordinator(args.pop("registry"), read_only=args["command"] in ("status", "assert"))
        print(json.dumps(coordinator.operate(**args), sort_keys=True))
        return 0
    except (ValueError, OSError, sqlite3.Error, subprocess.SubprocessError) as exc:
        print(json.dumps({"result": "BLOCKED", "reason": str(exc)}))
        return 1
    finally:
        if coordinator:
            coordinator.close()


if __name__ == "__main__":
    raise SystemExit(main())
