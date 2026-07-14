---
name: coach-plan
description: Build the learner's weekly training plan from weak skills, real error patterns, SRS load, recent capacity, and last week's retro. Runs from natural requests to plan the week and internally when coach-today finds no current plan. Writes data/weekly-plan.json for the daily orchestrator and activity skills.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Coach Plan — Weekly Program

## Overview

Turns the learner's accumulated data into a concrete week: which days, which activities, which scenarios. The plan is what makes english-coach a coach instead of a chat — the learner never has to decide "what should I do today".

## When to Use

Run when the learner naturally asks about the week, or internally from `coach-today` when `weekly-plan.json` is absent or belongs to an earlier ISO week. A current-week plan is never overwritten automatically; changing it mid-week requires a clear replan request.
## Instructions

### 0. Onboarding check

If `preferences.onboarding_completed` is absent, offer the natural-language onboarding once. If the learner wants to start now, proceed with known data and mark the week as calibration; never require them to name a command.

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Pull out: `current_level`, `daily_goal_minutes`, `focus_areas`, weakest skills from mastery, top error patterns by frequency (ignore seeded watch patterns still at 0), SRS queue size, and recent session notes / `focus_next_session`.

Then read `data/weekly-plan.json` if it exists — that's last week. Compute its retro: how many activities are `done` vs `planned`/`skipped`, what got carried over.

### 2. Retro (when a previous week exists)

Show a three-line summary: completed %, what worked, what was skipped. Rule: **a skip is data, not failure** — the tone is diagnostic, never guilty. Record the retro into the old plan's `retro` block and back the file up to `data/.backups/weekly-plan-{week_id}.json` before overwriting.

If last week completed under 50%, this week gets **lighter** — fewer activities, not more resolve.

**Self-tuning step:** skim the week's transcripts in `results/`. If a stable preference pattern shows up (formats that work or annoy, pacing, reply length, topics that spark real talk), propose one concrete edit to `CLAUDE.md`'s Local Context or a skill file — show the diff, apply only after the learner agrees. One tweak per week max; the tool adapts to the learner gradually, not in rewrites.

### 3. Resolve availability without making the learner plan

In autonomous mode, derive a conservative schedule from `daily_goal_minutes`, recent completed days, missed activities, and the current day. Do not interview the learner when these data are sufficient.

Ask at most one short question only when a fact blocks a safe plan — for example, whether travel leaves any practice days. Preferences about topics, pacing, and annoying formats should come from session history and natural feedback, not a mandatory questionnaire.

### 4. Generate the plan

Composition for a normal week — scale down to available days and `daily_goal_minutes` × available days total load:

- **3–4 × talk** — scenarios chosen against weak patterns and `focus_areas`, level-appropriate (a B1 learner gets "status update" before "investor grilling")
- **1 × listen + discuss pair** — pick a real material by interests and level (podcast episode, YouTube talk; give title, link, duration ≤ 20 min) and schedule `discuss` 1–2 days after `listen`; attach 3 orienting questions to the listen entry
- **1 × write** — a `weekly_reflection` by default, scheduled near the end of the learner's week (120–220 words about achievements, difficulties, lessons, and next-week focus). Use `daily_reflection` instead when a short 5–10 minute slot fits better. A clearly requested work-writing goal may replace the reflection.
- **1–2 × review** — scale to SRS queue size; if the queue is nearly empty, drop to 1 and add a talk instead

First-ever plan = **calibration week**: mark it as such in `goals`, keep it light, expect to adjust.

**Monthly checkpoint:** roughly every 4 weeks, schedule one internal `coach-intro` re-run — a transparent level re-measure. Compare with the previous verdict and say what moved.

### 5. Write first, then summarize

In autonomous mode, write `data/weekly-plan.json` immediately and show one concise natural-language summary of the next activity. Do not expose skill names or ask the learner to approve a command menu. When the learner explicitly asked to inspect or change the week, show a compact day/type/topic table and apply conversational edits.

```json
{
  "week_id": "2026-W29",
  "created": "YYYY-MM-DD",
  "goals": ["…2-3 outcome-style goals…"],
  "activities": [
    {"id": "w29-1", "day": "mon", "type": "talk", "scenario": "status update call", "status": "planned", "session_ref": null},
    {"id": "w29-2", "day": "tue", "type": "listen", "source": {"title": "…", "url": "…", "duration_min": 15}, "questions": ["…", "…", "…"], "followup": "w29-3", "status": "planned"},
    {"id": "w29-3", "day": "wed", "type": "discuss", "about": "w29-2", "status": "planned"},
    {"id": "w29-4", "day": "sun", "type": "write", "format": "weekly_reflection", "topic": "reflect on this week", "prompts": ["What went well?", "What was difficult?", "What did you learn?", "What will you focus on next week?"], "length_words": {"min": 120, "max": 220}, "status": "planned", "session_ref": null},
    {"id": "w29-5", "day": "fri", "type": "review", "status": "planned"}
  ],
  "retro": {"completed_pct": null, "carried_over": [], "notes": ""}
}
```

`type ∈ {talk, listen, discuss, write, review, vocab}` · `status ∈ {planned, done, skipped}` · day codes `mon…sun`. Each executing skill marks its own activity `done` and sets `session_ref`.

## Critical Rules

- **Load ≤ daily_goal_minutes × available days.** An overloaded plan kills the habit; when in doubt, plan less.
- **Real data only.** Scenarios come from actual error patterns and session notes, not generic curricula.
- **A skip is data, not failure.** Retro tone is neutral; carried-over items get easier, not doubled.
- **Safe automatic boundary.** Missing/stale plans may be generated automatically from real data. Never overwrite a current-week plan unless the learner clearly asks to replan it.
