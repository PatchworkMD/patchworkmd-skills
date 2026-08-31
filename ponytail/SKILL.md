---
name: ponytail
description: >-
  Use this on any coding task when the smallest thing that actually ships is the
  right answer (YAGNI, stdlib first).
---
# Ponytail

Lazy means efficient, not careless. The best code is the code never written.

## The ladder

Stop at the first rung that holds:

1. Does this need to exist at all? Speculative need = skip it.
2. Already in this codebase? Reuse it.
3. Stdlib does it? Use it.
4. Native platform feature covers it?
5. Already-installed dependency solves it?
6. Can it be one line?
7. Only then: the minimum code that works.

Read the task and the code it touches first. Bug fix = root cause, not symptom.

## Rules

- No unrequested abstractions.
- Deletion over addition. Boring over clever.
- Fewest files possible.
- Never lazy about validation at trust boundaries, data-loss error handling, security, or accessibility.
- Non-trivial logic leaves one runnable check behind.

Default intensity: full. lite = build what's asked and name the lazier alternative. ultra = YAGNI extremist.

Code first. Then at most three short lines: what was skipped, when to add it.
