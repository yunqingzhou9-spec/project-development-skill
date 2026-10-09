#!/usr/bin/env python3
"""Offline handoff helper. Native writer evidence is supplied, not authenticated here."""
import argparse
import hashlib
import json
import os
import stat
import sqlite3
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from coordinator import Coordinator, CoordinationError, default_registry, require


def git(checkout, *args):
    return subprocess.run(["git", "-C", str(checkout), *args], check=True, capture_output=True, timeout=10, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}).stdout


def snapshot(checkout):
    root = Path(git(checkout, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    # Submodules have separate worktrees; a top-level fingerprint cannot cover them.
    require(not any(line.startswith(b"160000 ") for line in git(root, "ls-files", "--stage", "-z").split(b"\0")), "Submodules require explicit manual reconciliation")
    head = git(root, "rev-parse", "HEAD").decode().strip()
    branch = git(root, "symbolic-ref", "--quiet", "--short", "HEAD").decode().strip() if subprocess.run(["git", "-C", str(root), "symbolic-ref", "--quiet", "HEAD"], capture_output=True, timeout=10, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}).returncode == 0 else "DETACHED"
    status = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    digest = hashlib.sha256()
    for blob in (status, git(root, "diff", "--binary", "--no-ext-diff", "--no-textconv"), git(root, "diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv")):
        digest.update(len(blob).to_bytes(8, "big")); digest.update(blob)
    untracked = [x for x in git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if x]
    dirty_tracked = set(git(root, "diff", "--name-only", "-z", "--no-ext-diff", "--no-textconv").split(b"\0")) | set(git(root, "diff", "--cached", "--name-only", "-z", "--no-ext-diff", "--no-textconv").split(b"\0"))
    # Git diffs can normalize CRLF or clean-filter bytes. Bind raw bytes/modes of
    # every Git-visible dirty tracked file as well as untracked entries.
    for raw in sorted((set(untracked) | dirty_tracked) - {b""}):
        file = root / os.fsdecode(raw)
        digest.update(len(raw).to_bytes(8, "big")); digest.update(raw)
        try:
            mode = file.lstat().st_mode
        except FileNotFoundError:
            digest.update(b"MISSING")
            continue
        content = hashlib.sha256()
        if stat.S_ISLNK(mode):
            content.update(os.fsencode(os.readlink(file)))
        else:
            require(stat.S_ISREG(mode), "Special untracked file requires manual reconciliation")
            with file.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    content.update(block)
        digest.update(str(stat.S_IFMT(mode)).encode()); digest.update(str(stat.S_IMODE(mode)).encode()); digest.update(content.digest())
    return {"checkout": str(root), "head": head, "branch": branch, "dirty": bool(status), "dirty_sha256": digest.hexdigest(), "untracked_count": len(untracked)}


def state_index(root, relative):
    require(isinstance(relative, str) and relative.strip(), "State path must be a nonempty string")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, "State path must be project-relative")
    target = root / path
    require(target.is_file() and not target.is_symlink() and root in target.resolve().parents, "State index must be an in-project regular file")
    return {"path": path.as_posix(), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def observe(registry, project, repository, checkout, owner=None, generation=None):
    store = Coordinator(registry, read_only=True)
    try:
        command = "assert" if owner is not None else "status"
        view = store.operate(command, project, repository, checkout, owner, generation, summary=True)
        # Context is intentionally fetched only by the handoff helper, not ordinary status.
        view["context"] = json.loads(store.db.execute("SELECT context FROM projects WHERE project=?", (project,)).fetchone()[0])
        require(isinstance(view["context"], dict), "Saved context must be an object; reconcile manually")
        return view
    finally:
        store.close()


def run(command, project, repository, checkout, registry=None, owner=None, generation=None,
        expected_generation=None, native_check_ref=None, state_path="PROJECT_STATE.md", context=None):
    started = time.perf_counter()
    phases = {}
    checkpoint = started
    def mark(name):
        nonlocal checkpoint
        now = time.perf_counter()
        phases[name] = round((now - checkpoint) * 1000, 3)
        checkpoint = now

    def finish(result):
        result['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 3)
        result['timing'] = {'scope': 'helper_only', 'phases_ms': phases,
                            'end_to_end_ms': None, 'permission_wait_ms': None,
                            'model_ms': None, 'host_roundtrip_ms': None}
        return result

    registry = Path(registry) if registry else default_registry()
    current = observe(registry, project, repository, checkout, owner if command == "prepare" else None, generation)
    mark('registry_read')
    local = snapshot(checkout)
    mark('snapshot')
    root = Path(local["checkout"])
    if command == "inspect":
        private = current.pop("context")
        saved = private.get('handoff')
        saved = saved if isinstance(saved, dict) else {}
        index = saved.get('state_index')
        index = index if isinstance(index, dict) else {}
        return finish({'coordination': current, 'local': local, 'native_writers': 'UNVERIFIED',
                       'saved_handoff': {'generation': saved.get('generation'),
                                         'state_path': index.get('path')},
                       'active_task': private.get('active_task')})
    require(command in ("prepare", "takeover"), "Unknown handoff command")
    require(isinstance(owner, str) and owner.strip(), "Native owner reference required")
    require(isinstance(native_check_ref, str) and native_check_ref.strip(), "Fresh native writer reconciliation reference required (not authenticated by this helper)")
    require(not current["unresolved_attempts"], "Resolve or reconnect outstanding attempts before handoff")
    private = current["context"]
    if command == "prepare":
        require(generation is not None, "Current generation required")
        require(isinstance(context, dict) and all(isinstance(context.get(k), str) and context[k].strip() for k in ("active_task", "next_action")), "Context requires active_task and next_action")
        require(isinstance(context.get("blockers", []), list), "Blockers must be a list")
        index = state_index(root, state_path)
        private.update(context)
        private["handoff"] = {"format": "handoff-v1", "project": project, "repository": repository, "owner": owner, "generation": generation, "local": local, "state_index": index, "native_check_ref": native_check_ref}
        private["status"] = "READY_FOR_TAKEOVER"
        # Local observations and native references are advisory, not OS fencing.
        require(snapshot(checkout) == local and state_index(root, state_path) == index, "Files changed while preparing handoff")
        mark('validation')
        store = Coordinator(registry)
        try:
            store.operate("assert", project, repository, checkout, owner, generation, summary=True)
            result = store.operate("release", project, repository, checkout, owner, generation, context=private, summary=True)
        finally:
            store.close()
        mark('mutation')
        verification = verify_after(registry, project, repository, checkout, result, local, index)
        mark('postcheck')
        prompt = ("用 $project-development 的空闲交接短流程接管。项目 " + json.dumps(project, ensure_ascii=False)
                  + "；仓库 " + json.dumps(repository, ensure_ascii=False)
                  + "；目录 " + json.dumps(str(root), ensure_ascii=False)
                  + "；本机私有登记 (--registry) " + json.dumps(str(registry.resolve()), ensure_ascii=False)
                  + "；状态指针 " + json.dumps(state_path, ensure_ascii=False)
                  + "；前任原生 owner " + json.dumps(owner, ensure_ascii=False)
                  + "；预期已释放 generation " + str(generation)
                  + "。现场核实前任及相关写入者、未解决尝试和交接指纹，取得更新 generation 后按已批准范围继续；无活动任务则等待指令。"
                  + "保留未提交内容；不重放任务、不默认联网、清理、重置或推送。使用辅助程序自带计时和 --record，不临时写计时脚本。"
                  + "目标10秒内，超过1分钟排查原因但不因耗时中断，也不省略安全检查。")
        output = {'coordination': result, 'local': local, 'verification': verification}
        # Only a verified release is suitable to advertise as ready for takeover.
        if verification['status'] == 'VERIFIED':
            output['prompt'] = prompt
        return finish(output)
    require(expected_generation is not None and current["generation"] == expected_generation and current["state"] == "RELEASED", "Expected released generation required; never steal an active owner")
    handoff = private.get("handoff", {})
    require(isinstance(handoff, dict), "Malformed saved handoff; reconcile manually")
    require(handoff.get("format") == "handoff-v1" and handoff.get("generation") == expected_generation and handoff.get("owner") == current["owner"] and handoff.get("project") == project and handoff.get("repository") == repository, "No matching compact handoff; use documented manual reconciliation")
    require(handoff.get("local") == local, "Checkout/HEAD/dirty files changed; reconcile before claim")
    index = handoff.get("state_index", {})
    require(isinstance(index, dict), "Malformed saved state index; reconcile manually")
    require(state_index(root, index.get("path", "")) == index, "State index changed; reconcile before claim")
    private.update(status="ACTIVE", takeover_native_check_ref=native_check_ref)
    mark('validation')
    store = Coordinator(registry)
    try:
        result = store.operate("claim", project, repository, checkout, owner, expected_generation=expected_generation, context=private, summary=True)
    finally:
        store.close()
    mark('mutation')
    verification = verify_after(registry, project, repository, checkout, result, local, index)
    mark('postcheck')
    return finish({'coordination': result, 'local': local, 'verification': verification,
                   'next_action': private.get('next_action'), 'active_task': private.get('active_task')})


def verify_after(registry, project, repository, checkout, expected, local, index):
    """Do not turn a committed mutation into a misleading 'not acquired' error."""
    try:
        unchanged = snapshot(checkout) == local and state_index(Path(local['checkout']), index['path']) == index
        observed = observe(registry, project, repository, checkout)
        same_owner = all(observed[key] == expected[key] for key in ('owner', 'generation', 'state'))
        clear = not observed['unresolved_attempts']
        return {'status': 'VERIFIED' if unchanged and same_owner and clear else 'RECONCILE_REQUIRED',
                'local_unchanged': unchanged, 'ownership_matches': same_owner, 'attempts_clear': clear}
    except (ValueError, OSError, subprocess.SubprocessError, sqlite3.Error) as exc:
        return {'status': 'RECONCILE_REQUIRED', 'reason': str(exc)}


def record_result(result, registry, checkout, command):
    """Best-effort private receipt; never fail or retry ownership for telemetry."""
    try:
        root = Path(git(checkout, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
        directory = (Path(registry) if registry else default_registry()).resolve().parent / 'handoff-runs'
        require(directory.resolve() != root and root not in directory.resolve().parents,
                'Timing records must be outside the checkout')
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        path = directory / (command + '-' + uuid.uuid4().hex + '.json')
        receipt = {**result, 'command': command, 'recorded_at': datetime.now(timezone.utc).isoformat()}
        # Exclusive creation prevents overwriting another run; native references stay private.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(receipt, stream, ensure_ascii=False, sort_keys=True)
            stream.write('\n')
        return {'path': str(path), 'status': 'SAVED'}
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return {'status': 'UNAVAILABLE', 'reason': str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "prepare", "takeover"))
    for name in ("project", "repository", "checkout"):
        parser.add_argument("--" + name, required=True)
    for name in ("registry", "owner", "native-check-ref"):
        parser.add_argument("--" + name)
    parser.add_argument("--generation", type=int)
    parser.add_argument("--expected-generation", type=int)
    parser.add_argument("--state-path", default="PROJECT_STATE.md")
    parser.add_argument("--context", type=json.loads)
    parser.add_argument('--record', action='store_true', help='Save a private receipt for prepare/takeover; never changes ownership on recording failure')
    args = vars(parser.parse_args())
    record = args.pop('record')
    if record and args['command'] == 'inspect':
        parser.error('--record is only available for prepare/takeover; inspect stays read-only')
    started = time.perf_counter()
    try:
        result = run(**args)
        code = 0 if result.get('verification', {}).get('status', 'VERIFIED') == 'VERIFIED' else 1
    except (ValueError, OSError, subprocess.SubprocessError, sqlite3.Error) as exc:
        result = {'result': 'BLOCKED', 'reason': str(exc), 'elapsed_ms': round((time.perf_counter()-started)*1000, 3),
                  'timing': {'scope': 'helper_only', 'end_to_end_ms': None, 'permission_wait_ms': None,
                             'model_ms': None, 'host_roundtrip_ms': None}}
        code = 1
    if record:
        result['record'] = record_result(result, args.get('registry'), args['checkout'], args['command'])
    result['cli_elapsed_ms'] = round((time.perf_counter() - started) * 1000, 3)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
