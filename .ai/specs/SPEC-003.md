# SPEC-003 — Reproducible Skill validation environment

```json
{
  "id": "SPEC-003",
  "status": "APPROVED",
  "approval_ref": "Human instruction on 2026-09-08: 按你的建议执行"
}
```

## Goal / scope

Make the repository's Skill Creator validation reproducible without modifying Codex-managed Python runtimes:

- ignore the repository-local `.venv/` directory;
- declare `PyYAML>=6.0` in `requirements-dev.txt`;
- update the project commands to create/use `.venv`, install development requirements and run Skill validation with that interpreter;
- create the local virtual environment, install the declared dependency and rerun Skill validation plus the existing completion test suite.

## Non-goals / constraints

- Do not modify system Python, Codex bundled/cache runtimes or the installed `project-development` Skill.
- Do not change the Skill's functional behavior or version.
- Do not publish, push, tag or promote a new accepted baseline.
- Keep environment files untracked; only the dependency declaration and instructions belong in Git.

## Acceptance

- AC-1: `.gitignore` excludes `.venv/`, and `.venv` is not tracked by Git.
- AC-2: `requirements-dev.txt` declares `PyYAML>=6.0`, and the project instructions use it to provision `.venv`.
- AC-3: `.venv/bin/python -c "import yaml; print(yaml.__version__)"` succeeds after installation.
- AC-4: Skill Creator `quick_validate.py` reports `Skill is valid!` when run with `.venv/bin/python` against this repository.
- AC-5: `scripts/test_completion.py` passes under the same virtual environment.

This approved Spec is frozen. Changes require a new approved version.
