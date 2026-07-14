---
name: coach-today
description: Daily entry point — reads the weekly plan and today's date, proposes the day's activity in one line, and launches the right skill (/talk, /discuss, /fluent-writing, /fluent-review) with parameters from the plan. Handles missed days without guilt. Fires on /coach-today or whenever the learner signals "let's practice" without naming an activity — "давай заниматься", "что у нас сегодня?", "начнём", "let's go".
allowed-tools: Read, Write, Edit, Bash
---

# Coach Today — Daily Entry Point

## Overview

Removes the "what should I do today" decision. One line, one confirmation, straight into the activity. The SessionStart hook already prints today's plan; this skill acts on it.

## Instructions

### 1. Read the plan

Read `data/weekly-plan.json`. Determine today's day code (`mon…sun`).

- **No plan file:** offer two options — build a week with `/coach-plan`, or do a free `/talk` right now. Don't lecture.
- **Plan exists, nothing planned today:** offer the nearest not-yet-done activity or a free talk: "Nothing on the plan today — want a free talk, or pull Thursday's session forward?"

### 2. Propose today's activity

One conversational line: "Today's plan is a talk — status update call, about 15 minutes. Ready?" On agreement, launch the mapped skill **with the plan's parameters**:

| `type` | Launch | Parameters passed |
|---|---|---|
| `talk` | `/talk` flow | `scenario` |
| `discuss` | `/discuss` flow | `about` (the listen activity it refers to) |
| `listen` | no skill — hand over the material | `source` (title, url, duration) + the 3 orienting `questions`; mark `done` when the learner confirms they've listened |
| `write` | `/fluent-writing` flow | `topic` |
| `review` | `/fluent-review` flow | — |
| `vocab` | `/fluent-vocab` flow | — |

The executing skill marks the activity `done` and sets `session_ref`. For `listen`, this skill marks it `done` itself on the learner's confirmation.

### 3. Missed days — no guilt, ever

- **Yesterday's activity still `planned`:** mention it once, neutrally: "Yesterday's review didn't happen — want to fold it in today, or skip it?" Skipping sets `status: skipped`. Never moralize; a skip is data.
- **2+ days missed:** don't stack a backlog. Offer to rebuild the rest of the week: "Let's just replan the remaining days" → run the `/coach-plan` regeneration for the remaining days, lighter.

### 4. If the learner wants something else

They can always override: "хочу просто поговорить" → free `/talk`, and today's planned activity stays `planned` (they may still do it later). The plan serves the learner, not the reverse.

## Critical Rules

- **One line, one confirmation, go.** No tables, no stats dump — SessionStart already showed the summary.
- **Pass the plan's parameters** to the launched skill — the scenario/topic/material is the whole point of planning.
- **Skips are data.** Neutral tone, `skipped` status, move on.
- **This is the default entry point.** Any "давай заниматься"-shaped intent routes here; the learner never needs to know the command.
