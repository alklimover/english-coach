"""
Fluent path resolution — supports dual-mode (clone vs plugin install).

Data directory resolution precedence:
  1. $FLUENT_DATA_DIR if set
  2. ./data/ if learner-profile.json exists under cwd (clone-mode)
  3. ~/.claude/fluent-data/ (plugin-mode fallback)

Plugin-root resolution precedence:
  1. $CLAUDE_PLUGIN_ROOT if set (plugin install)
  2. $CLAUDE_PROJECT_DIR if set (clone run in project)
  3. parent of this file's .claude/ dir (dev-run fallback)
"""
from __future__ import annotations

import os
from pathlib import Path


def data_dir() -> Path:
    """Resolve the runtime data directory. Creates it if it falls back to global."""
    env = os.environ.get("FLUENT_DATA_DIR")
    if env:
        p = Path(env).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p

    cwd_data = Path("data")
    if (cwd_data / "learner-profile.json").exists():
        return cwd_data

    global_data = Path.home() / ".claude" / "fluent-data"
    global_data.mkdir(parents=True, exist_ok=True)
    return global_data


def plugin_root() -> Path:
    """Resolve the plugin/repo root directory."""
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return Path(env)
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    # Fallback: this file lives at <root>/.claude/hooks/fluent_paths.py
    return Path(__file__).resolve().parents[2]


def backups_dir() -> Path:
    """Resolve the backups directory. Mirrors data_dir location (.backups/ sibling to data/)."""
    d = data_dir()
    return d.parent / ".backups"
