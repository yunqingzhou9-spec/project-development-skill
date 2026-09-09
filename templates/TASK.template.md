# TASK-001 — <meaningful purpose>

```json
{
  "format": "work-v1",
  "id": "TASK-001",
  "short_name": "<purpose_slug>",
  "status": "READY",
  "approval_ref": "<actual authorization reference>",
  "scope": {
    "outcome": "<authorized outcome>",
    "acceptance": ["<observable criterion>"],
    "assessment": {
      "risk": "low",
      "reversibility": "<rollback and consequences>",
      "coupling": "<dependencies and integration needs>",
      "uncertainty": "<known facts or bounded investigation conclusion>",
      "verification_reason": "<why these checks are sufficient>"
    },
    "base": "<full Git base commit>",
    "deliverables": ["<exact changed file>"],
    "checks": [{"id": "targeted", "capability": "behavior", "independent": false}]
  },
  "scope_sha256": "<canonical scope digest frozen before implementation>",
  "candidate": null,
  "contributors": [],
  "depends_on": [],
  "dependencies_satisfied": [],
  "blockers": [],
  "next_action": "<next concrete action>"
}
```

Use a portable contributor alias (including main if it implements); actual native IDs and mappings belong in private evidence. Fill candidate only after freezing all scoped bytes. Read `references/WORK_FORMAT.md` in the installed Skill directory (resolve that directory at setup). Existing projects may retain FULL/LIGHTWEIGHT; do not rewrite old Tasks. Existing stricter policy controls. High risk needs separate independent behavior and review; ordinary low-risk work may use honest main-Agent self-checks. No new-work file/line or worker-count threshold.

## Investigation and budget

<Question, bounded experiment and stop condition if uncertain; default up to 15 minutes or two experiments, then reassess. Three failed verification cycles by default; no repeated blind retries.>

## Result / next action

<Commands, observations, candidate, private evidence locator alias, remaining limits, next action. Record measured elapsed work/wait and attempts where available; Token/cost UNAVAILABLE unless measured. Link history instead of copying it. Task completion is not Human acceptance.>
