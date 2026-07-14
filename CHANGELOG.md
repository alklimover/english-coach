# Changelog

All notable changes are documented in this file. Entries tagged `-ec` are
specific to the **english-coach** fork; upstream *fluent* releases are kept
below them for reference.

## [0.3.0-ec.3] — 2026-07-14

### Added

- **Zero-command learner interface:** natural Russian or English intent now starts
  planning, conversation, writing, reading, vocabulary, review, progress, and
  onboarding flows without requiring learner-facing slash commands.
- `coach-today` autonomously creates a missing or stale weekly plan, treats
  «начинаем» as confirmation, and launches the selected activity with its plan
  parameters.
- Daily reflections (60–120 words), weekly reflections (120–220 words), and
  direct journal checking are first-class writing modes. Weekly planning
  schedules a reflection by default.
- Focused SessionStart tests cover command-free first contact, due-review
  messaging, and plan launch through the natural «начинаем» intent.

### Changed

- Learner-facing startup, onboarding, empty-queue, progress, and README copy no
  longer exposes internal skill names.
- Automatic invocation is allowed only for a confirmed plan activity or clear
  natural intent. Ambiguous text still requires one short clarification;
  profile creation and reset retain explicit confirmation safeguards.

## [0.3.0-ec.2] — 2026-07-13

### Added

- **Speaking north-star metrics:** `read-db.py` now computes speaking minutes
  for the current Monday–Sunday week and a speaking-specific day streak.
  SessionStart and `/fluent-progress` surface these values ahead of general
  study statistics.

### Fixed

- Speaking statistics tolerate malformed dates and durations, exclude
  future-dated sessions from the current week, and are covered by focused
  deterministic tests.
- The voice-first rules now take explicit precedence over conflicting upstream
  typed-tutor rules (delayed feedback, natural conversation flow, and no
  spoken markdown/emojis).
- Removed learner-specific identity and biographical examples from tracked
  public files. Runtime learner records and transcripts remain ignored.
- The fork README now documents the actual project-folder installation path,
  local voice setup and fallback behavior instead of directing users to
  install the upstream plugin.
- Release metadata now reports `0.3.0-ec.2`; the unsupported upstream
  marketplace manifest was removed so the repository exposes one honest
  installation path: clone and run from the project folder.

### Privacy

- Learner records, transcripts, and Kokoro/`say` speech synthesis remain
  local; no voice API credentials are needed.


## [0.3.0-ec.1] — 2026-07-07

First english-coach release: a single-learner, voice-first English deployment
on top of *fluent* v0.3.0. Runs as a project folder (session started from
`english-coach/`), not a plugin install.

### Fixed

- `update-db.py` now accepts the session payload via `argv[1]` as well as
  stdin (`3e61588`). Previously an argv call silently read nothing and left
  the databases untouched. Regression-covered in `tests/test_update_db.py`.

### Added — voice layer

- **`/talk`** — live voice conversation skill, the fork's core (`b5a8e48`).
  Delayed feedback (zero corrections mid-conversation; review after wrap-up),
  level-matched i+1 difficulty, garbled-dictation handling, and recovery of an
  interrupted session into `results/talk-session-{NNN}-partial.md`. Difficulty
  now adapts to the learner's level with reduced latency and no language slips
  (`b33e39c`).
- **Neural TTS via Kokoro** with automatic fallback to macOS `say`
  (`bin/tts.sh`, `000fe0b`, Phase 4.1). Voice and rate read from
  `learner-profile.preferences.voice`.

### Added — coach layer

- **`/coach-plan`**, **`/coach-today`**, **`/discuss`**, and a plan-of-day line
  in the SessionStart greeting (`51ea3de`). Weekly program stored in
  `data/weekly-plan.json`.
- **`/coach-intro`** — transparent voice onboarding with an announced level
  ladder; system explained in Russian on screen, verdict in Russian, hand-off
  to `/coach-plan` (`1912e6a`).
- `/coach-plan` self-tunes weekly from session transcripts (`7603203`) and runs
  a monthly level checkpoint by re-running `/coach-intro` (`6314d20`).
- **Natural-language intent routing** (`7d9d9e7`) — Russian or English phrasing
  maps to the right skill; the learner never needs to memorize commands.

### Changed

- Fork identity: `plugin.json` name `english-coach`, version `0.3.0-ec.1`,
  homepage/repository pointing at the fork (`98300af`).
- Personalized for an English-learning Russian speaker: profile, seeded
  RU-speaker watch patterns in `mistakes-db.json`, English examples in skills,
  Local Context in `CLAUDE.md` (`7e70556`).
- Sessions in this folder default to Sonnet (`4631613`).
- Runtime learner records and transcripts under `data/` and `results/` are
  gitignored by default, keeping those private artifacts out of the public fork
  (`5cb69b1`).

### Docs

- PRD, user stories, and implementation plan for english-coach v1 (`0b42adf`).

## [0.3.0] — 2026-06-15

### Added

- Milestones support in the `update-db.py` session payload. The new
  `milestones[]` field accepts either a bare string or an object
  `{ "milestone": <required non-empty string>, "date": <optional YYYY-MM-DD,
  defaults to the session date> }`. Each milestone is recorded in both
  `session-log.milestones[]` and `learner-profile.achievements[]`. Validation
  rejects malformed entries (exit `1`, no files written); an unparseable
  `date` falls back to the session date.

## [0.2.1] — 2026-06-11

### Fixed

- Hooks no longer fail on Windows with `No such file or directory` (#5).
  Plugin hook commands in `hooks.json` used the bash default-value syntax
  `${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}`, which Claude Code's own
  variable substitution does not understand on Windows — it replaced the
  variable names but left the `:-` separators literal, producing a single
  garbage path. Hook commands now use plain `${CLAUDE_PLUGIN_ROOT}` (always
  set for plugin hooks) and invoke scripts via an explicit `python3`/`bash`
  interpreter so they don't depend on shebang handling under Git Bash.

## [0.2.0] — 2026-05-14

### Breaking changes

All 12 skills renamed with a `fluent-` prefix to prevent collisions with other
plugins and Claude Code built-ins. Update any muscle memory or external
references.

| Old | New |
|-----|-----|
| `/setup` | `/fluent-setup` |
| `/learn` | `/fluent-learn` |
| `/review` | `/fluent-review` |
| `/vocab` | `/fluent-vocab` |
| `/writing` | `/fluent-writing` |
| `/speaking` | `/fluent-speaking` |
| `/reading` | `/fluent-reading` |
| `/progress` | `/fluent-progress` |
| `sm2-calculator` | `fluent-sm2-calculator` |
| `db-updater` | `fluent-db-updater` |
| `feedback-formatter` | `fluent-feedback-formatter` |
| `session-analyzer` | `fluent-session-analyzer` |

New session result files use `/results/fluent-{skill}-session-{NNN}.md`.
Existing files using the older `{skill}-session-{NNN}.md` naming are still
read by `fluent-session-analyzer` — no migration required.

### Fixed

- Plugin install no longer fails on first DB read. Skills now invoke helper
  scripts via `${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/...`
  so the path resolves regardless of CWD.
- Added missing `.claude/hooks/ensure_data_dir.py` referenced by
  `fluent-setup`.

### Migration

```bash
claude plugin update fluent@m98
```

Then use the new slash commands. Your data (`~/.claude/fluent-data/` or
`./data/`) is unchanged.

## [0.1.0] — 2026-03-15

Initial release.
