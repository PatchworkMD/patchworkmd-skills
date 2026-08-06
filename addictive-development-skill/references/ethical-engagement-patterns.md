# Ethical engagement pattern cards

Use this file as a design-review reference. Each card should name the user benefit, the safe implementation, the failure mode, and the stopping control.

| Goal | Prefer | Avoid | Verify |
|---|---|---|---|
| Start work | One obvious next action, preview, undo | Forced onboarding, fake urgency | First-action success and cancellation |
| Sustain momentum | Real milestones, visible dependencies, saved context | Random rewards, infinite feeds, streak punishment | Completion quality and pause/resume |
| Recover | Drafts, retry with explanation, graceful backoff | Lost work, shame copy, escalating prompts | Error and offline fixtures |
| Finish | Summary, export, done-for-now, quiet close | Confetti loops, autoplay, “one more” pressure | User can stop in one action |
| Personalize | Explicit preferences and reversible defaults | Hidden profiling or sensitive inference | Settings audit and data minimization |

For any proposed mechanic, answer:

1. What user goal does it serve?
2. What happens when the user says “not now”?
3. Can the user understand and disable it?
4. Does it work with keyboard, screen reader, high contrast, reduced motion, and dyslexia-friendly copy?
5. What durable evidence proves the task state?
