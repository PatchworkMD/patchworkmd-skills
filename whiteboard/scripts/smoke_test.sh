#!/usr/bin/env bash
# Smoke test for the whiteboard skill: renderer exists, template valid, ffmpeg present.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== whiteboard smoke test ==="
test -f "$SKILL_DIR/scripts/render.py" && echo "PASS renderer exists" || { echo "FAIL renderer missing"; exit 1; }
test -f "$SKILL_DIR/scripts/make_srt.py" && echo "PASS srt generator exists" || { echo "FAIL srt gen missing"; exit 1; }
test -f "$SKILL_DIR/scripts/burn_captions.py" && echo "PASS caption burner exists" || { echo "FAIL burner missing"; exit 1; }
test -f "$SKILL_DIR/scripts/kokoro_tts.py" && echo "PASS kokoro helper exists" || { echo "FAIL kokoro helper missing"; exit 1; }
test -f "$SKILL_DIR/templates/example-explainer.json" && echo "PASS template exists" || { echo "FAIL template missing"; exit 1; }
command -v ffmpeg >/dev/null && echo "PASS ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')" || { echo "FAIL ffmpeg missing"; exit 1; }
python3 -m py_compile "$SKILL_DIR/scripts/render.py" && echo "PASS render.py compiles"
python3 -m py_compile "$SKILL_DIR/scripts/kokoro_tts.py" && echo "PASS kokoro_tts.py compiles"
env -u PYTHONPATH /usr/bin/python3 -c "import PIL; assert PIL.__version__" 2>/dev/null && echo "PASS system PIL available" || { echo "FAIL system PIL (captions will fail)"; exit 1; }
python3 - <<PY
import json
m = json.load(open('$SKILL_DIR/templates/example-explainer.json'))
assert m['scenes'] and all(s.get('image') and s.get('duration') for s in m['scenes'])
print('PASS template schema valid')
PY
echo "ALL PASS"
