---
name: addictive-development-skill
description: Design ethical, accessible product loops that make productive action—starting, making progress, and finishing—compelling and repeatable. Use when task and project apps need lower start friction, visible momentum, satisfying completion, and healthy return cues. Never use it to intensify gambling, compulsive consumption, doom-scrolling, or other harmful behavior.
---

# Addictive Development Skill

## Purpose

Make productivity itself the rewarding loop. Help users start useful work, sustain momentum, finish truthfully, and stop cleanly. Treat “addictive” as “compelling to begin and satisfying to complete,” never as loss of control. Do not make consumption or degenerative behavior more compulsive. Preserve user agency, privacy, accessibility, and a clear stopping point.

## Non-negotiable guardrails

- Do not use gambling-like variable rewards, loot-box logic, deceptive defaults, artificial scarcity, fear of loss, shame, punitive streak resets, or notification pressure.
- Do not apply these mechanics to gambling, doom-scrolling, compulsive shopping, substance use, or other harmful behavior.
- Do not optimize for time-in-app, compulsive checking, or engagement at the expense of the user’s stated goal.
- Do not target children or vulnerable users with persuasive mechanics.
- Make reminders, sound, motion, streaks, and data collection controllable and off by default when not necessary.
- Provide pause, exit, undo, snooze, reset, and “done for today” actions.
- Keep progress truthful: never fake completion, inflate counts, or conceal blockers.
- For sensitive campaign/finance work, stay local and aggregate-first; never expose donor rows, credentials, or financial identifiers.

## Workflow

1. Define the user’s real outcome, time available, and healthy stopping condition.
2. Inventory the existing product and canonical skills before adding anything. Prefer `design-taste-frontend`, `stitch-design-taste`, `accessibility-and-inclusive-visualization`, `codebase-design`, `testing-strategy`, `task-manager`, `hermes-agent`, and `record-replay` where they fit.
3. Map the productivity journey: choose → start → focused work → visible progress → finish → reflect → stop.
4. Add the smallest set of mechanics that improves clarity or momentum. Prefer visible progress, one next action, previews, forgiving recovery, meaningful defaults, and user-chosen rewards.
5. Specify accessibility and safety behavior before implementation: keyboard path, screen-reader labels, contrast, reduced motion, dyslexia-friendly copy, quiet hours, and recovery.
6. Define success using completion quality, time-to-first-action, abandonment reasons, error recovery, opt-out rate, and self-reported usefulness. Do not use raw session length as the primary success metric.
7. Test deterministic fixtures and representative flows. Separate static design fit from live runtime evidence.
8. Record `NOW / NEXT / BLOCKED / EVIDENCE / SHIP GATES` and leave publication, credentials, external sends, live routing, and destructive changes gated.

## Preferred engagement mechanics

- **Low start friction:** turn intention into one useful action that can begin now.
- **Progress clarity:** show remaining work, completed work, dependencies, and the next concrete action.
- **Immediate truthful feedback:** confirm what changed, why it matters, and how to undo it.
- **Small wins:** split large tasks into meaningful, user-approved steps without hiding total scope.
- **Goal gradient:** show progress toward a user-chosen finish line; never manufacture urgency.
- **Forgiving continuity:** preserve drafts, resume context, allow missed days, and avoid punishment for stopping.
- **Choice with defaults:** recommend one safe next step while keeping alternatives visible.
- **Reflection:** summarize what was accomplished and surface the next session’s starting point.
- **Healthy closure:** congratulate completion briefly, suggest a stopping point, and make “close” as easy as “continue.”

## Product and backend requirements

- Keep engagement state separate from task truth. Store event IDs, timestamps, task IDs, consent/settings, and provenance; never infer completion from a click alone.
- Make event handling idempotent, replayable, and auditable. Use request/correlation IDs and explicit state transitions.
- Bound polling, retries, notifications, queue depth, and background work. Coalesce duplicate updates and back off when idle.
- Fail closed on missing owner, destination, authorization, or evidence. Do not create duplicate tasks or control planes.
- Treat metrics as diagnostic signals, not hidden optimization targets. Provide exportable summaries and retention controls.
- Benchmark semantic quality and transport/resource behavior. For LiteLLM or local models, use a small authenticated route set, concurrency 1, fixed prompts, timeouts, warm/cold labels, p50/p95 latency, error classes, output validity, and peak RSS; stop on repeated timeouts or resource pressure.

## Design review questions

- Can a user tell what to do next in under five seconds?
- Can they stop without losing work or status?
- Is every reward understandable, earned, and dismissible?
- Does the UI work without motion, color, sound, or a streak?
- Does the backend preserve exact-once semantics and truthful state?
- Can an operator explain why a task is open, blocked, or complete?
- Are notification and personalization choices explicit rather than inferred?

## References

- Read [ethical-engagement-patterns.md](references/ethical-engagement-patterns.md) for the pattern catalog and anti-pattern substitutions.
- Read [stack-integration.md](references/stack-integration.md) before selecting existing UI, backend, Hermes, replay, routing, or release skills.
