#!/usr/bin/env python3
"""Local Kokoro TTS CLI for Hermes command-provider integration.
Reads text from {input_path}, writes speech WAV to {output_path}.
Uses sherpa-onnx Kokoro (proven on M1/M4, ~0 network, ~1s first audio).

Usage: kokoro_tts.py <input_text_file> <output_wav>
Env:  KOKORO_MODEL_DIR (required: local Kokoro ONNX model directory)
      KOKORO_VOICE_ID (default 0 = af_heart)
"""
import os, sys, wave
import numpy as np

def main():
    if len(sys.argv) < 3:
        print("usage: kokoro_tts.py <input.txt> <output.wav>", file=sys.stderr)
        sys.exit(2)
    text_path, out_path = sys.argv[1], sys.argv[2]
    text = open(text_path, encoding='utf-8').read().strip()
    if not text:
        # silent empty output — Hermes treats missing/empty as failure-safe
        sys.exit(0)

    import sherpa_onnx
    md = os.environ.get('KOKORO_MODEL_DIR')
    if not md:
        print("KOKORO_MODEL_DIR must point to a local Kokoro ONNX model dir", file=sys.stderr)
        sys.exit(2)
    sid = int(os.environ.get('KOKORO_VOICE_ID', '0'))
    speed = float(os.environ.get('KOKORO_SPEED', '1.0'))

    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                model=md+'model.int8.onnx', voices=md+'voices.bin',
                tokens=md+'tokens.txt', lexicon=md+'lexicon-us-en.txt',
                data_dir=md, dict_dir=md+'dict'),
            num_threads=2),
        rule_fsts=md+'number-zh.fst', rule_fars=md+'date-zh.fst')
    tts = sherpa_onnx.OfflineTts(cfg)
    gen = tts.generate(text, sid=sid, speed=speed)  # GeneratedAudio, NOT tuple

    s = np.asarray(gen.samples)
    # CRITICAL: float64 in [-1,1]; naive astype(int16) = silent. Scale first.
    if s.dtype in (np.float32, np.float64):
        s16 = (np.clip(s, -1.0, 1.0) * 32767).astype(np.int16)
    else:
        s16 = s.astype(np.int16)

    with wave.open(out_path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(gen.sample_rate)
        w.writeframes(s16.tobytes())
    print(f"Kokoro TTS OK: {len(s16)/gen.sample_rate:.2f}s -> {out_path}")

if __name__ == '__main__':
    main()
