---
name: whiteboard
description: Use when creating a whiteboard-style explainer video from a scene list, local narration, and deterministic ffmpeg rendering.
---

# Whiteboard Explainer Skill

Deterministic whiteboard explainer pipeline: PIL-rendered scene PNGs (no AI
video gen), local Kokoro narration, PIL caption burn (ffmpeg on macOS
Homebrew lacks libass/subtitles/drawtext — always use `burn_captions.py`,
never the ffmpeg `subtitles` filter).

## Prerequisites (user-provided)

- `ffmpeg` / `ffprobe` on PATH.
- System Python with Pillow for caption burn (use `/usr/bin/python3` and
  `env -u PYTHONPATH` if your project venv has a broken `_imaging`).
- Kokoro narration: `sherpa-onnx` Python package and a local Kokoro ONNX
  model directory, exposed as `KOKORO_MODEL_DIR` (see `scripts/kokoro_tts.py`).

## Verified pipeline

1. Generate hand-drawn scenes (`image_generate`): black+blue marker, explicit
   labels, landscape.
2. Typo gate: run `vision_analyze` on every scene, list all visible words,
   flag garbles. After 2 failed generations, ship the diagram and let
   captions carry the correct terms.
3. Narration: `python3 scripts/kokoro_tts.py script.txt narration.wav`
   (Kokoro via sherpa-onnx, float→int16 conversion).
4. Captions: `python3 scripts/make_srt.py script.txt narration.wav captions.srt`
5. Burn: `python3 scripts/burn_captions.py manifest.json captions.srt captioned_manifest.json`
6. Render: `python3 scripts/render.py captioned_manifest.json out.mp4`
   (scene clips → concat → mux narration).
7. Verify: `ffprobe` streams, `volumedetect`, duration matches narration.

Use `SKILL_DIR` (path to the installed skill) or run from the skill directory
so the `scripts/` and `templates/` references resolve.

## Required content gate

Before rendering, write a scene list. For a technical system explainer,
cover: the user-facing front door, the core loop, routing and profiles,
orchestration and approval flow, memory/secrets/communication, and a clear
implemented / partial / pending status. Do not claim the system is complete
while any part is unresolved. A 30–45 second single-image status card is a
teaser, not an explainer; use a 2–4 minute multi-scene format for a real
overview.

## Pitfalls

- Image models garble short labels reliably; plan for 2 attempts per scene.
- Keep on-screen labels SHORT (2–4 words); captions carry full sentences.
- Kokoro phoneme warnings (skip unknown phonemes) are harmless.
- Scene durations must sum ≈ narration duration + small head/tail; measure
  narration first with `ffprobe`.
- Always archive MP4 + script + SRT; temp dirs vanish on reboot.
- Float64 Kokoro samples need scaling before int16 conversion
  (`np.clip(s, -1.0, 1.0) * 32767`).
- `data_dir` is required by the Kokoro config constructor.
- `GeneratedAudio` must be read through `.samples` and `.sample_rate`.
- **Zoompan is pathologically slow on multi-minute video.** Use plain
  scale+pad with `-preset veryfast`; do not reintroduce zoompan for long
  scenes.
- Never expose personal paths, credentials, donor data, or local identifiers
  in a public package.
