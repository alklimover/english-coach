#!/usr/bin/env bash
# Fluent PreCompact Hook
# Creates safety backup before conversation compaction.
# Respects FLUENT_DATA_DIR env var; falls back to ./data then ~/.claude/fluent-data.
set -euo pipefail

if [[ -n "${FLUENT_DATA_DIR:-}" ]]; then
  DATA_DIR="${FLUENT_DATA_DIR/#\~/$HOME}"
elif [[ -f "data/learner-profile.json" ]]; then
  DATA_DIR="data"
else
  DATA_DIR="$HOME/.claude/fluent-data"
fi

BACKUP_DIR="$(dirname "$DATA_DIR")/.backups/precompact"
mkdir -p "$BACKUP_DIR"

if ls "$DATA_DIR"/*.json >/dev/null 2>&1; then
  cp "$DATA_DIR"/*.json "$BACKUP_DIR/"
  echo "[Fluent] 🔒 Pre-compact backup saved to $BACKUP_DIR"
fi
