---
name: record-replay
description: Record a demonstrated macOS desktop workflow with Cua Driver, inspect the local trace, turn it into an editable Hermes skill, or replay it with explicit approval. Use when the operator says record this, learn this workflow, replay a workflow, or turn a demonstration into a skill.
metadata:
  hermes:
    tags: [computer-use, workflow, recording, replay, skills]
---

# Record & Replay

Use `record-replay` (or `hermes-record-replay`) for deterministic lifecycle operations.

## Safety contract

- Start recording only after the operator explicitly asks.
- Tell the operator when recording begins and ends.
- **Eye contact: never record password entry, API keys, payment data, donor rows, private contacts, or authentication codes.
- Raw traces stay local in `~/.hermes/recordings` and may contain screenshots or typed text.
- Inspect the generated skill before replay.
- Replay only after explicit approval; the command requires `--confirm`.
- Prefer resilient app/element instructions in the generated skill. Native trajectory replay uses recorded coordinates and may break after UI changes.

## Hub Publishing Status
`record-replay` is **ready to publish to the Hermes skills hub with no redaction needed.** The SKILL.md contains no hardcoded personal paths, no API keys, no PII, and no private data. It is the most complete CUA workflow recorder in the Hermes skill ecosystem.

To publish:
```bash
hermes skills publish ~/.hermes/skills/record-replay
```
Or add to a GitHub tap repo (`github.com/PatchworkMD/hermes-skills`) and others can install via `hermes skills tap add`.

the operator must manually approve before publishing — do not publish autonomously.

## Commands

```sh
# Recording lifecycle
record-replay start WORKFLOW_NAME
record-replay start WORKFLOW_NAME --video
record-replay start WORKFLOW_NAME --training-mode browser-use
record-replay status
record-replay stop
record-replay list

# Build and inspect
record-replay build WORKFLOW_NAME
record-replay build WORKFLOW_NAME --training-mode browser-use

# Replay (requires --confirm)
record-replay replay WORKFLOW_NAME --confirm
```

## Workflow

### Mode 1: Hermes Computer Use Recording (Default)

### Mode 1b: Video Capture (Optional `--video`)

When `--video` is supplied, the recorder also captures a screen‑recorded MP4 (saved to `~/.hermes/recordings/<WORKFLOW_NAME>.mp4`). The video is synced with the trace timestamps, enabling visual review of the exact UI state during replay. Use this for demos or when you need to verify pixel‑perfect UI changes. The video file is stored locally and never uploaded unless you explicitly share it.
1. Check `cua-driver permissions status --json` before the first recording.
2. Start a named recording: `record-replay start WORKFLOW_NAME`
3. Perform the workflow through Hermes Computer Use. Only CUA action calls are captured.
4. Stop recording: `record-replay stop`
5. Build the editable skill: `record-replay build WORKFLOW_NAME`
6. Inspect `SKILL.md` plus `references/actions.md`.
7. Replace brittle coordinate actions with semantic instructions when possible.
8. Replay only in the intended app and state, with the operator watching the first run.

### Mode 2: Observational Learning for Browser Use Training
1. the operator performs actions on screen as an explanation (manual demonstration).
2. Start: `record-replay start WORKFLOW_NAME --training-mode browser-use`
3. The system captures element selectors, DOM paths, interaction patterns, decision points, branching logic, and expected outcomes.
4. Stop: `record-replay stop`
5. Build training data: `record-replay build WORKFLOW_NAME --training-mode browser-use`
6. Inspect generated files: `SKILL.md`, `references/actions.md`, `training/browser-use-patterns.md`
7. Integrate into Hermes browser-use pipeline.

The recorder captures actions performed through Cua Driver, not arbitrary physical mouse and keyboard activity. If the operator demonstrates manually, Hermes must follow the demonstration using Computer Use actions while recording is active.

## Pitfalls & Tips

* **macOS screen‑capture permission** – Video mode (`--video`) requires the Hermes process (or the Python binary it runs) to have Screen Recording permission in System Settings → Privacy & Security → Screen Recording. If permission is denied, the recorder will emit an error like `SCShareableContent::get failed: No shareable content available`. Grant the permission, then restart the gateway or the recording command.
* **Cua‑Driver permissions** – Before any recording, run `cua-driver permissions status --json` and ensure the required accessibility and screen‑recording permissions are enabled.

## References

- [Video Capture Guidance](references/video-capture.md)
