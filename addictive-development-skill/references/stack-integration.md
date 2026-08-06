# Existing stack integration map

Reuse these canonical skills instead of downloading or bulk-installing overlapping repositories.

| Need | Existing skill | Role |
|---|---|---|
| Anti-slop UI | `design-taste-frontend`, `stitch-design-taste` | Visual direction, hierarchy, non-template review |
| Inclusive UI | `accessibility-and-inclusive-visualization` | Contrast, keyboard, reduced motion, text alternatives |
| Architecture/backend | `codebase-design`, `testing-strategy`, `error-handling-patterns` | Seams, tests, failure recovery |
| Task truth | `task-manager`, `kanban-task-execution` | Durable task state and Hermes queue diagnosis |
| Hermes | `hermes-agent`, `hermes-architecture-scaffolding` | Profiles, gateway, extension boundaries |
| Record/replay | `record-replay`, `record-and-replay` | Existing canonical replay behavior; check overlap before packaging |
| Routing | `PatchworkMD-smart-model-router`, `PatchworkMD-sol-operating-guide` | Local route selection and approval boundaries |
| Release | `github-repo-management`, `packaging-notarization`, `skill-creator` | Candidate package and validation |

Integration rule: load only the smallest relevant set, preserve `approveHere`, keep approval and activation separate, and do not alter live routing or publish as a side effect of packaging.
