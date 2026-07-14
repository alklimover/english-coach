---
name: coach-today
description: Zero-command daily orchestrator — reacts to natural start intent, reads or autonomously creates the current weekly plan, and launches today's activity with its parameters. Handles missed days without guilt. Fires whenever the learner says "начинаем", "давай заниматься", "что у нас сегодня?", "let's practice", or equivalent.
allowed-tools: Read, Write, Edit, Bash
---

# Coach Today — Daily Entry Point

## Overview

Removes the "what should I do today" decision. The learner expresses readiness once; this flow chooses and starts the right activity without exposing skill names.

## Instructions

### 1. Resolve the current plan

Run `.claude/hooks/read-db.py`, then read `data/weekly-plan.json`. Determine the current ISO week, today's day code (`mon…sun`), `daily_goal_minutes`, and `computed.due_reviews_count`.

- **Incomplete onboarding + uncertain start:** if `preferences.onboarding_completed` is absent and the learner says they do not know where to start (or equivalent) without requesting a specific activity, do not inspect or offer the daily plan yet. Say in simple English: “Let’s start with a short speaking assessment so I can learn your level and goals. Ready?” On agreement, hand off to `coach-intro`.
- **Explicit reassessment:** a request to determine the level again or start over diagnostically belongs to `coach-intro`, even if onboarding was completed. Never reset or delete history.

- **No plan or a plan from an earlier week:** internally invoke `coach-plan` in autonomous mode, then continue here with the generated plan. Do not ask the learner to choose a command or construct the week.
- **Nothing planned today:** choose the nearest not-yet-done activity that fits the remaining time. If none exists, start a short free conversation.
- **Reviews are due:** if today's selected activity is not `review`, prepend a compact review when it and the activity fit `daily_goal_minutes`. Otherwise make review today's activity and leave the original activity `planned` for the nearest free slot. Never claim due items are included unless the review flow will actually run.

### 2. Start today's activity

If the learner already said a readiness phrase such as «начинаем» or "let's go", that is the confirmation: launch immediately. Otherwise describe the selected activity in one conversational line and ask whether to begin. Never mention its slash command or internal skill name.

Launch the mapped flow **with the plan's parameters**:

| `type` | Internal flow | Parameters passed |
|---|---|---|
| `talk` | `talk` | `scenario` |
| `discuss` | `discuss` | `about` (the listen activity it refers to) |
| `listen` | hand over the material | `source` (title, url, duration) + the 3 orienting `questions`; mark `done` when the learner confirms they've listened |
| `write` | `fluent-writing` | `format`, `topic`, `prompts`, `length_words`; reflection formats take precedence over generic scenario selection |
| `review` | `fluent-review` | — |
| `vocab` | `fluent-vocab` | — |

The confirmed plan activity authorizes the mapped skill invocation. The executing skill marks the activity `done` and sets `session_ref`. For `listen`, this flow marks it `done` itself on the learner's confirmation.

### 3. Missed days — no guilt, ever

- **Yesterday's activity still `planned`:** mention it once, neutrally: "Yesterday's review didn't happen — want to fold it in today, or skip it?" Skipping sets `status: skipped`. Never moralize; a skip is data.
- **2+ days missed:** don't stack a backlog. Internally regenerate the remaining days with `coach-plan` in lighter mode; tell the learner only the resulting next activity.

### 4. If the learner wants something else

They can always override naturally: "хочу просто поговорить" starts a free conversation, while today's planned activity stays `planned` for later. The plan serves the learner, not the reverse.

## Critical Rules

- **One intent, straight into practice.** If readiness was already expressed, don't ask for a second confirmation. No command menus, tables, or stats dumps.
- **Pass the plan's parameters** to the launched skill — the scenario/topic/material is the whole point of planning.
- **Skips are data.** Neutral tone, `skipped` status, move on.
- **This is the default entry point.** Never require the learner to know which skill implements the activity.
