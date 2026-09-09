---
name: project-development
description: >-
  Bootstrap or operate lightweight repository-centered project governance from one conversation: clarify and approve specs, coordinate task agents, preserve project state, and verify delivery evidence. Use for multi-task software, data, automation, and AI projects or when explicitly requested. Not a substitute for domain engineering, runtime delegation tools, or a protected release system.
metadata:
  version: "2.2.0"
---

# Project Development

Help the user finish a goal, with effort proportional to its consequences. Keep durable facts in the project and private runtime details outside published files.

## Entry

Read the selected project's AGENTS, its state pointer, then only the active work's approved scope and relevant files. Respect existing project policy and its accepted governing version; these prospective rules never weaken historical acceptance requirements.

- Starting: inspect existing instructions and reuse the five templates only where needed. Follow [Setup](references/PROTOCOL.md#setup).
- Asking for a change: an explicit, sufficiently clear implementation request authorizes that scope. Record it; do not ask for ritual approval. Discussion alone remains discussion.
- Working: assess risk, reversibility, coupling, uncertainty and useful verification. A clear low-risk local change can be implemented by the main Agent with honest targeted self-checks. Select independent capabilities where they add needed assurance; high-risk work requires separate independent behavior verification and review. No fixed file/line cutoff or mandatory worker count for new ordinary work.
- Investigating: unknowns trigger a bounded investigation, not automatic escalation. Resolve uncertainty with a small experiment, then reassess. Read [Effort and resources](references/PROTOCOL.md#effort-and-resources).
- Continuing or switching windows: use bound project context, or Project ID plus an accessible checkout locator. Read [Recovery](references/PROTOCOL.md#main-window-handoff-and-recovery); reconstruct HEAD and active workers, never copy a full transcript.
- Completing: apply [Gate](references/GATE.md). Use [work-v1](references/WORK_FORMAT.md) for new work unless project policy selects legacy FULL/LIGHTWEIGHT. Missing required checks block completion.
- Installing: use the [verified clean archive installer](references/INSTALL.md), never copy the repository root.

## Invariants

One cooperative local owner guards shared writes, dispatch and integration using the [coordinator](references/COORDINATION.md). Check generation before each such action. Isolated workers return their candidate; they do not overwrite the primary checkout. The coordinator cannot fence arbitrary shell writers, authenticate Agent identities, coordinate other hosts or authorize external side effects.

Freeze scope before implementation and bind all results to the exact candidate and inputs. Contributors may self-check but cannot claim independent review. Required failing evidence cannot be omitted, relabelled N/A or waived just to finish. If selected native delegation is unavailable, block that check; do not roleplay independence.

Keep working version, accepted baseline, source commit, published release and installed copy distinct. This package version is 2.2.0; verify publication and installation independently. A structural check does not issue formal Human acceptance, establish protected enforcement or grant installation/publication authority.

Persist the active outcome, blockers, candidate and next action before stopping. Link history, do not embed it into current state. Native IDs and local locators belong in a private runtime registry, never published templates or product files.

The exact runtime allowlist read from an immutable source commit plus canonical manifest hashes is the structural cleanliness boundary. Maintained privacy scans are defense in depth, not exhaustive secret detection. See [Identity vocabulary](references/PROTOCOL.md#identity-vocabulary).
