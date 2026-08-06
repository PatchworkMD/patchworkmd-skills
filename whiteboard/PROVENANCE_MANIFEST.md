# Provenance manifest — whiteboard

- `package_name`: whiteboard
- `brand`: PatchworkMD
- `canonical_source`: local the operator skill hub (personal-branded) → portability-rewritten 2026-08-06 for public export
- `included_paths`: SKILL.md, agents/openai.yaml, scripts/{kokoro_tts,make_srt,burn_captions,render}.py, scripts/smoke_test.sh, templates/example-explainer.json, LICENSE, LICENSE_DECISION.md, README.md, PROVENANCE_MANIFEST.md, RELEASE_NOTES.md
- `source_revision_or_hash`: see tree digest in verification receipt (recomputed at ship)
- `skill_validator_result`: pending at write time; run `smoke_test.sh` before push
- `test_result`: smoke_test.sh + live render evidence (2026-08-06)
- `toolchain`: macOS, sherpa-onnx 1.13.4, ffmpeg 8.1, system PIL 11.3, /usr/bin/python3
- `license_decision`: MIT (cleared by the operator 2026-08-06)
- `private_material_scan`: clean — no user paths, tokens, donor rows, machine IDs
- `third_party_provenance`: none copied; standard library + system frameworks only
- `publication_status`: cleared for publication 2026-08-06 → `PatchworkMD/patchworkmd-skills`
- `human_gates`: license (MIT, approved), wording/branding (approved), destination (approved), publication action (approved)
