# Whiteboard — Patchwork release candidate

Status: **PORTABLE — CLEARED FOR PUBLICATION** (2026-08-06)

## Purpose
Lightweight, local-first, low-cost whiteboard-style explainer video skill.
Diagram (image), local Kokoro narration, deterministic ffmpeg render. No cloud
video generation.

## Package contents
- `SKILL.md` — canonical skill (portability-rewritten 2026-08-06)
- `agents/openai.yaml` — agent wiring metadata
- `scripts/kokoro_tts.py` — local Kokoro narration (requires `KOKORO_MODEL_DIR`)
- `scripts/make_srt.py` — deterministic caption timing from narration script
- `scripts/burn_captions.py` — PIL caption burn (never ffmpeg subtitles filter)
- `scripts/render.py` — deterministic multi-scene renderer (manifest-driven)
- `scripts/smoke_test.sh` — install/compile/schema gate (skill-relative)
- `templates/example-explainer.json` — generic example manifest

## Portability (2026-08-06 rewrite)
- No absolute user paths. Scripts resolve skill-relative via
  `dirname "${BASH_SOURCE[0]}"`.
- Kokoro model directory is required via `KOKORO_MODEL_DIR`, no personal
  default.
- Content gate genericized to any technical explainer; the personal example
  was removed.

## Provenance
- Author: PatchworkMD (first-party).
- Pipeline verified on macOS: Kokoro sherpa-onnx 1.13.4, ffmpeg 8.1,
  PIL-rendered scenes. Dependencies: ffmpeg, sherpa-onnx, numpy, a local
  Kokoro ONNX model dir. All local.

## Privacy scan
- No credentials, tokens, API keys, donor rows, or machine identifiers in
  packaged files.
- No personal absolute paths, credentials, tokens, donor rows, or machine
  identifiers remain in packaged files.

## Tests
- `scripts/smoke_test.sh` — expected ALL PASS on a host with ffmpeg + system
  PIL (renderer, srt gen, burner, kokoro helper, template schema, compiles).
- Live render of the full technical explainer passed the audio gate
  (mean -27 dB) and produced a 2.5-minute MP4 with AAC audio (2026-08-06).

## License
MIT — see `LICENSE`. Cleared by the repository maintainer on 2026-08-06.
