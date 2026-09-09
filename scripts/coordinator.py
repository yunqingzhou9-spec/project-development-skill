#!/usr/bin/env python3
"""Cooperative same-host ownership and durable dispatch ledger; no shell fencing."""
import argparse
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
    def __init__(self, registry=None):
        self.path = Path(registry) if registry is not None else default_registry()
        require(not self.path.is_symlink(), "Registry cannot be a symlink")
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        os.chmod(self.path, 0o600)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS host (name TEXT PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS projects (
          project TEXT PRIMARY KEY, repository TEXT NOT NULL UNIQUE,
          owner TEXT NOT NULL, generation INTEGER NOT NULL, state TEXT NOT NULL,
          context TEXT NOT NULL DEFAULT '{}');
        CREATE TABLE IF NOT EXISTS roots (common TEXT PRIMARY KEY, project TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS attempts (
          project TEXT NOT NULL, attempt TEXT NOT NULL, task TEXT NOT NULL,
          work_key TEXT NOT NULL, inputs TEXT NOT NULL, generation INTEGER NOT NULL, state TEXT NOT NULL,
          native TEXT, result TEXT, payload TEXT, resolution TEXT,
          PRIMARY KEY(project, attempt));
        ''')
        self.db.execute("BEGIN IMMEDIATE")
        try:
            host = self.db.execute("SELECT name FROM host").fetchone()
            require(host is None or host[0] == socket.gethostname(), "Cross-host registry unsupported")
            if host is None:
                self.db.execute("INSERT INTO host VALUES (?)", (socket.gethostname(),))
            self.db.commit()
        except Exception:
            self.db.rollback()
            self.db.close()
            raise

    def close(self):
        self.db.close()

    def operate(self, command, project, repository, checkout, owner=None, generation=None, **data):
        require(all(isinstance(x, str) and x.strip() for x in (project, repository)), "Project and repository identity required")
        root, common = repository_identity(checkout, repository)
        require(root not in self.path.resolve().parents and Path(common) not in self.path.resolve().parents, "Private registry must be outside checkout")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM projects WHERE project=?", (project,)).fetchone()
            other = self.db.execute("SELECT project FROM projects WHERE repository=?", (repository,)).fetchone()
            linked = self.db.execute("SELECT project FROM roots WHERE common=?", (common,)).fetchone()
            require(other is None or other[0] == project, "Repository already bound to another Project ID")
            require(linked is None or linked[0] == project, "Linked checkout has conflicting Project ID")
            require(row is None or row["repository"] == repository, "Project has conflicting repository identity")
            if command == "claim":
                require(owner, "Owner reference required")
                require(row is None or row["state"] == "RELEASED", "Project already owned; inspect and explicitly release/recover")
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
            self.db.execute("INSERT OR IGNORE INTO roots VALUES (?,?)", (common, project))
            result = dict(self.db.execute("SELECT * FROM projects WHERE project=?", (project,)).fetchone())
            result["attempts"] = [dict(x) for x in self.db.execute("SELECT * FROM attempts WHERE project=? ORDER BY attempt", (project,))]
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["claim", "status", "assert", "update", "release", "recover", "begin", "uncertain", "dispatch", "result", "resolve"])
    parser.add_argument("--registry")
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
        coordinator = Coordinator(args.pop("registry"))
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
