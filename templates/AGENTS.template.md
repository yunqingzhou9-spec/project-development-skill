# Project instructions

Use `$project-development`. Read `PROJECT_STATE.md`, only the active Task's approved scope and relevant links. Respect the recorded governing policy; prospective rules cannot weaken accepted requirements. Setup/discussion alone does not authorize implementation.

- Project ID / name: `<reuse authoritative existing ID; else explicit user ID; else generate a stable readable ID> / <name>`
- Repository identity / scope: `<portable identity> / <relative scope>`
- Purpose / exclusions: <fill>
- State / decisions: `PROJECT_STATE.md` / `DECISIONS.md`
- Existing architecture / commands / history: <links or UNVERIFIED>
- Governing policy: <accepted protocol version and project requirements>

Use the same Project ID in state. Checkout locations and native IDs stay private outside published records. Conflicting identity or inaccessible checkout stops dependent recovery; do not guess a replacement project.

Choose effort from risk, reversibility, coupling, uncertainty and required verification. Main Agent may implement a clear low-risk local change and self-check honestly. High-risk work requires distinct independent behavior and review; other selected checks and existing stricter policy remain required. Delegate only useful independent work with isolated write ownership. If selected capabilities are missing, report the affected blocker; do not fabricate independence.

Only one cooperative local owner coordinates shared writes and dispatch; follow the Skill coordinator and recovery rules. Its ownership assertion cannot fence arbitrary shell writers or grant remote side-effect authority. Workers return isolated outputs; only the current owner integrates them and updates shared state.

- Investigation: bounded question/experiment, default 15 minutes or two experiments, then reassess.
- Failed verification cycles: at most 3 unless project policy states otherwise.
- Formal acceptance: HUMAN unless an explicitly authorized protected service is verified.
- Installation / release: separate authority required; task completion is not publishing permission.
- Capability observations / private registry locator: <portable references only; unknown stays unknown>
