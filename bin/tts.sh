#!/usr/bin/env bash
# english-coach TTS: speaks the given English text aloud.
# Usage: bin/tts.sh "text to speak"
# Engine comes from learner-profile preferences.voice.engine ("kokoro" | "say").
# Any Kokoro failure falls back to `say`; speech must never block a session.
set -u

TEXT="${1:-}"
[ -z "$TEXT" ] && exit 0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="$ROOT/data/learner-profile.json"

read_pref() {
  /usr/bin/python3 - "$PROFILE" "$1" "$2" 2>/dev/null <<'PY'
import json, sys
try:
    voice = json.load(open(sys.argv[1])).get("preferences", {}).get("voice", {})
    print(voice.get(sys.argv[2], sys.argv[3]))
except Exception:
    print(sys.argv[3])
PY
}

ENGINE="$(read_pref engine say)"
SAY_VOICE="$(read_pref tts_voice Samantha)"
SAY_RATE="$(read_pref tts_rate 175)"


if [ "$ENGINE" = "kokoro" ] && [ -x "$ROOT/.tts-venv/bin/python" ]; then
  KOKORO_VOICE="$(read_pref kokoro_voice af_heart)"
  OUT_DIR="$(mktemp -d)"
  trap 'rm -rf "$OUT_DIR"' EXIT
  if "$ROOT/.tts-venv/bin/python" -m mlx_audio.tts.generate \
      --model mlx-community/Kokoro-82M-bf16 \
      --voice "$KOKORO_VOICE" \
      --text "$TEXT" \
      --output_path "$OUT_DIR" --file_prefix reply --audio_format wav \
      >/dev/null 2>&1; then
    for WAV in "$OUT_DIR"/reply*.wav; do
      [ -f "$WAV" ] && afplay "$WAV" && exit 0
    done
  fi
fi

exec say -v "$SAY_VOICE" -r "$SAY_RATE" -- "$TEXT"
