# Project state

- Project ID / name: `<stable ID> / <name>`
- Portable repository identity / scope: `<repository identity> / <relative scope>`
- Purpose / boundaries: <brief>
- Working version / candidate: <version and immutable candidate or NONE>
- Strictly Accepted Baseline: <authority-bound immutable candidate or UNESTABLISHED>
- Published release / installed copy: <separately verified identities or UNKNOWN>
- Governing policy: <accepted protocol and project-specific requirements>
- Active work: <Task links, concise outcome/status/blockers/next action>
- Relevant decisions / history / invalid records: <links only>
- Commands: <verified commands or UNVERIFIED>
- Next action: <concrete>

Keep this current and portable. Private checkout locators, native session/Worker IDs, ownership generations and attempt state live in the outside-checkout coordinator registry and private evidence; do not paste them here. Reconstruct changing HEAD, dirty work and native state during recovery. Bound project context or Project ID plus accessible locator normally suffices to resume. Check wrong-project/inaccessible-path conflicts and active writers before claiming ownership. Do not embed completed history or handoff transcripts.
