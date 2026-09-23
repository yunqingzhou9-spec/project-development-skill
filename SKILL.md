---
name: project-development
description: >-
  Bootstrap or operate lightweight repository-centered project governance from one conversation: clarify and approve specs, coordinate task agents, preserve project state, and verify delivery evidence. Use for multi-task software, data, automation, and AI projects or when explicitly requested. Not a substitute for domain engineering, runtime delegation tools, or a protected release system.
metadata:
  version: "2.3.0"
---

# Project Development

Help the user finish a goal, with effort proportional to its consequences. Keep durable facts in the project and private runtime details outside published files.

## Entry

Read the selected project's AGENTS, its state pointer, then only the active work's approved scope and relevant files. Respect existing project policy and its accepted governing version; these prospective rules never weaken historical acceptance requirements.

- Starting: inspect existing instructions and reuse the five templates only where needed. Follow [Setup](references/PROTOCOL.md#setup).
- Asking for a change: assess the request and help the user form a concrete goal before acting. Present a concise confirmation draft and wait for explicit confirmation before implementation, worker dispatch or external side effects. Follow [Goal intake and confirmation](references/PROTOCOL.md#goal-intake-and-confirmation).
- Working: assess risk, reversibility, coupling, uncertainty and useful verification. A clear low-risk local change can be implemented by the main Agent with honest targeted self-checks. Select independent capabilities where they add needed assurance; high-risk work requires separate independent behavior verification and review. No fixed file/line cutoff or mandatory worker count for new ordinary work.
- Investigating: unknowns trigger a bounded investigation, not automatic escalation. Resolve uncertainty with a small experiment, then reassess. Read [Effort and resources](references/PROTOCOL.md#effort-and-resources).
- Continuing or switching windows: use bound project context, or Project ID plus an accessible checkout locator. Read [Recovery](references/PROTOCOL.md#main-window-handoff-and-recovery); reconstruct HEAD and active workers, never copy a full transcript.
- Completing: apply [Gate](references/GATE.md). Use [work-v1](references/WORK_FORMAT.md) for new work unless project policy selects legacy FULL/LIGHTWEIGHT. Missing required checks block completion.
- Installing: use the [verified clean archive installer](references/INSTALL.md), never copy the repository root.

## Goal confirmation

For each new or materially changed goal, proportionately assess whether the request is reasonable, clear and executable. Consider the intended outcome, internal consistency, feasibility in the available environment, material constraints and risks, and observable completion criteria. Explain consequential problems, alternatives or missing information instead of mechanically accepting the request.

Help the user refine only what could materially change the result: outcome, scope, non-goals, constraints, completion criteria and solution direction. Read-only inspection, bounded investigation and discussion may continue while doing this. Do not implement, dispatch workers or cause external side effects yet.

Then present a concise confirmation draft covering the goal, relevant boundaries, completion criteria and proposed solution direction, and ask the user to confirm it. The instruction that started the discussion does not also confirm a draft produced afterward; confirmation must be an explicit response to the current draft. Silence is not confirmation.

After confirmation, record the authorized scope and proceed without repeatedly asking about routine implementation choices. If the goal or solution direction changes materially, summarize the delta and confirm it before dependent work continues. Discussion-only requests remain discussion, and continuation inside an already confirmed scope does not require a new confirmation.

## Reuse before implementation

When the solution may need reusable components, frameworks, automation, common algorithms or established integrations, ask before recommending a direction: can a suitable GitHub or ecosystem tool be reused or adapted instead of rebuilt? Perform a proportionate read-only check once the goal is clear enough. A small project-specific edit or an already constrained implementation may skip discovery with a concise reason.

Use available native web search as the baseline for public discovery. An available GitHub plugin or authenticated CLI may improve coverage, but it is optional and must not become a Skill dependency. If no suitable discovery capability is available, say the check is incomplete; do not claim that no reusable option exists.

Compare a useful shortlist by functional fit, maintenance activity, documentation and examples, license compatibility, security and dependency risk, project compatibility, and integration and ownership cost. Popularity alone is not a selection rule. Present direct reuse, adaptation and custom implementation when applicable, with a recommendation and material tradeoffs, in the solution-direction confirmation draft.

Discovery before confirmation remains read-only. Do not download dependencies, run untrusted code, modify the project or connect an external service until the user confirms the goal and solution direction and any separately required authority is present.

## Invariants

One cooperative local owner guards shared writes, dispatch and integration using the [coordinator](references/COORDINATION.md). Check generation before each such action. Isolated workers return their candidate; they do not overwrite the primary checkout. The coordinator cannot fence arbitrary shell writers, authenticate Agent identities, coordinate other hosts or authorize external side effects.

Freeze scope before implementation and bind all results to the exact candidate and inputs. Contributors may self-check but cannot claim independent review. Required failing evidence cannot be omitted, relabelled N/A or waived just to finish. If selected native delegation is unavailable, block that check; do not roleplay independence.

Keep working version, accepted baseline, source commit, published release and installed copy distinct. This package version is 2.3.0; verify publication and installation independently. A structural check does not issue formal Human acceptance, establish protected enforcement or grant installation/publication authority.

Persist the active outcome, blockers, candidate and next action before stopping. Link history, do not embed it into current state. Native IDs and local locators belong in a private runtime registry, never published templates or product files.

The exact runtime allowlist read from an immutable source commit plus canonical manifest hashes is the structural cleanliness boundary. Maintained privacy scans are defense in depth, not exhaustive secret detection. See [Identity vocabulary](references/PROTOCOL.md#identity-vocabulary).
