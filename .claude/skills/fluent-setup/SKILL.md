---
name: fluent-setup
description: Create or update the learner profile through natural conversation. Invoked after explicit agreement to first-time setup or a clear request to change/reset profile data. Every write is confirmed; resetting progress requires double confirmation and a backup.
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# Language Learning Setup

## Overview

One-time onboarding that seeds all 6 databases in the Fluent data directory. After setup, every other skill reads from those files — this is the bootstrap. Also handles profile updates and progress resets for returning users.

The data directory is resolved at runtime (not hardcoded to `./data/`):

1. `$FLUENT_DATA_DIR` if set
2. `$CLAUDE_PROJECT_DIR/data/` if that path contains `learner-profile.json` (clone mode)
3. `./data/` if `./data/learner-profile.json` exists (clone mode, cwd inside repo)
4. `~/.claude/fluent-data/` otherwise (plugin-install default)

Always resolve it via the helper rather than writing literal `data/` paths:

```bash
FLUENT_DATA="$(python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/ensure_data_dir.py")"
```

or from Python:

```python
import sys
sys.path.insert(0, f"{PLUGIN_ROOT}/.claude/hooks")
from fluent_paths import ensure_data_dir
DATA = ensure_data_dir()
```

## When to Use

For a new learner, run only after they agree to a natural prompt such as «давайте настроим репетитора». Before creating files, summarize what will be stored and ask for confirmation.

With an existing profile, invoke only from a clear request to update or reset it. If the learner merely wants to practise or see progress, route naturally to today's activity or the progress view instead.

## Instructions

### 1. Check for existing profile

Resolve the data directory first, then probe for `learner-profile.json`:

```bash
DATA_DIR="$(python3 -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks')
from fluent_paths import data_dir
print(data_dir())
")"
test -f "$DATA_DIR/learner-profile.json" && echo "exists" || echo "new"
```

If it exists, jump to **Profile updates** below. Otherwise continue.

### 2. Welcome

```markdown
# 🌍 Welcome to Your Personal Language Learning System!

This AI-powered system will help you learn any language through:
- 📊 Systematic progress tracking
- 🧠 Spaced repetition (scientifically proven)
- 🎮 Gamification (streaks, achievements)
- 📈 Adaptive difficulty
- 🎯 Personalized to YOUR goals

**Let's get you set up!** (~5 minutes)
```

### 3. Collect info

Use the `AskUserQuestion` tool to gather questions in batches when possible. Required fields:

1. **Name** — personalizes greetings.
2. **Target language** — the language being learned (e.g. Spanish, French, German, Japanese, Korean, Arabic, Dutch).
3. **Native language** — for translations and explanations.
4. **Other languages spoken** — optional, used to offer cross-language connections.
5. **Current level** — A1 / A2 / B1 / B2 / C1 / C2 / "not sure".
6. **Target level** — where they want to get to.
7. **Timeline** — 3 months / 6 months / 12 months / 2+ years / custom.
8. **Daily study minutes** — 10 / 15 / 30 / 60 / custom.
9. **Learning goal** — travel / work / exam (specify) / living in country / academic / family / interest.
10. **Learning style** — conversational / academic / immersive / balanced (default).
11. **Gamification on/off** — default on.

If the learner picks "not sure", do not substitute the old written five-question quiz. Store `learner.current_level: null` and add `"speaking placement"` to `preferences.pending_setup`. After the six files exist, offer the voice `coach-intro` placement described in Step 6.

### 4. Generate the learning plan

Compute expected months to target level:

```
A1 → A2: ~100 hours
A2 → B1: ~150 hours
B1 → B2: ~200 hours
B2 → C1: ~300 hours
C1 → C2: ~400 hours

months = hours_needed / (daily_minutes / 60) / 30
```

Adjust:

- `-10%` time if learner's native language is typologically close to the target (e.g. Dutch ↔ English, Spanish ↔ Italian).
- `-10%` per additional language already known (cap at 30% total).

Present:

```markdown
## 🎉 Setup Complete!

**Your Learning Profile:**
- 👤 Name: {name}
- 🌍 Learning: {target_language}
- 📚 Native: {native_language}
- 📊 Level: {current} → {target}
- 📅 Timeline: {timeline}
- ⏱️ Daily time: {minutes} min
- 💡 Goal: {goal}

## 📋 Personalized Plan

**Estimated time:** {months} months
**Total study hours:** ~{hours} hours

### Weekly Schedule

The coach builds each week automatically from the learner's level, available time, due reviews, recent mistakes, and completed sessions. It mixes conversation, listening and discussion, writing or reflection, vocabulary, and review without asking the learner to choose tools.

The only learner-facing action is to say «начинаем» or describe what they want naturally. Progress is summarized automatically at session start and available whenever they ask how things are going.

### Milestones
- Month 1: {reasonable short-term}
- Month 3: {quarter-way}
- Month 6: {half-way}
- Target date: {target_level}!

### Next Steps
The profile is ready. Offer the voice placement conversation first. After it succeeds—or immediately if the learner defers it—build the current week autonomously and offer the next activity in one sentence. The learner should not have to remember a schedule or command.

**Your journey to {target_language} fluency starts now!** 🚀
```

### 5. Write databases

Start from the templates in `data-examples/`. Resolve the target directory via `fluent_paths.ensure_data_dir()` (it creates the directory if missing), then create these 6 files inside it:

- `learner-profile.json` — fill all fields from the interview.
- `progress-db.json` — empty stats.
- `mistakes-db.json` — empty `error_patterns`.
- `mastery-db.json` — `skills_mastery` entries with `mastery_level: 0` for each skill.
- `spaced-repetition.json` — empty queues, `daily_limits.review_items_per_day: 20`.
- `session-log.json` — empty `sessions` array, `total_sessions: 0`.

Use the Write tool for each. Do not call `update-db.py` — that script is for session updates, not bootstrapping.

### 6. Voice placement handoff

After all six databases exist, offer one natural next step:

> «Профиль готов. Проведём короткую голосовую диагностику, чтобы проверить уровень и точнее собрать план?»

On natural agreement, internally run `coach-intro`. It explains the process, performs the announced speaking ladder, persists the CEFR verdict and interests through `fluent-db-updater`, then builds the week. Do not run `fluent-learn` first and do not require the learner to know a skill or command name.

If the learner defers, preserve any self-reported level, leave `onboarding_completed` absent, and build a conservative week. Offer the placement again on a later first contact.

## Profile Updates (existing profile)

If a profile exists, do only the action the learner requested. If the request is underspecified, ask one short natural question: whether they want to change goals/preferences, inspect the current plan, or reset progress. Never present a numbered command menu.

- **Update:** ask which field, update only that field, preserve the rest.
- **View plan:** render the plan read-only.
- **Reset:** state exactly how much history will be removed, confirm twice, then back up every JSON file before deletion:

  ```bash
  DATA_DIR="$(python3 -c "
  import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks')
  from fluent_paths import data_dir
  print(data_dir())
  ")"
  TS="$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$DATA_DIR/.backups/pre-reset-$TS"
  cp "$DATA_DIR"/*.json "$DATA_DIR/.backups/pre-reset-$TS/"
  ```

  Then restart setup from Step 2.

## Examples

### Example 1 — first-time setup flow

The learner says «давайте настроим репетитора», agrees to create the local profile, and answers the bootstrap questions. Create all six databases, then offer the voice placement naturally. On agreement, hand off to `coach-intro`; after its verdict, build the weekly plan.

### Example 2 — returning-user profile reset

Learner: "reset my progress, I want to start over"

> You're about to delete:
> - 42 sessions
> - 6-day streak
> - 287 vocabulary items
> - 12 mastered patterns
>
> This is irreversible. Type `RESET` (all caps) to confirm, or anything else to cancel.

## Critical Rules

- **Natural intent plus confirmation.** First-time creation requires explicit agreement; updates require a clear requested field; reset requires double confirmation.
- **Confirm twice before reset.** State the exact sessions, streak, and mastered items that will be erased, then require an explicit final confirmation.
- **Always seed all 6 files** — every other skill assumes they exist.
- **Back up before reset.** Hooks may not fire here; back up manually to `.backups/pre-reset-<timestamp>/`.
- **Don't invent data.** Start every file empty — progress, mistakes, mastery all start at zero. The system builds up from real sessions.
