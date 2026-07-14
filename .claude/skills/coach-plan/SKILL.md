---
name: coach-plan
description: Build the learner's weekly training plan from their data — weak skills, error patterns, SRS queue size, and last week's retro — through a short interview. Writes data/weekly-plan.json that /coach-today and /talk read all week. Fires on /coach-plan or when the learner asks to plan the week ("спланируем неделю", "какой план на неделю?", "plan my week"); cadence is Sunday retro → Monday plan.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Coach Plan — Weekly Program

## Overview

Turns the learner's accumulated data into a concrete week: which days, which activities, which scenarios. The plan is what makes english-coach a coach instead of a chat — the learner never has to decide "what should I do today".

## When to Use

Trigger only on explicit `/coach-plan`. Normally run on Sunday or Monday (retro → plan cadence). Mid-week runs are fine — the plan is built from the current day to Sunday.

## Instructions

### 0. Onboarding check

If `preferences.onboarding_completed` is absent from the profile, suggest (don't force) running `/coach-intro` first: the plan is only as good as the level assessment and the interests list it's built on. If the learner wants a plan anyway, proceed with what's known and mark the week as calibration.

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

### 3. Short interview

Three questions max (use AskUserQuestion where it helps):

1. Which days are realistic this week? (workload, travel)
2. Anything you want more of / less of? (scenarios, formats)
3. Did anything annoy you last week? (voice, difficulty, pacing)

### 4. Generate the plan

Composition for a normal week — scale down to available days and `daily_goal_minutes` × available days total load:

- **3–4 × talk** — scenarios chosen against weak patterns and `focus_areas`, level-appropriate (a B1 learner gets "status update" before "investor grilling")
- **1 × listen + discuss pair** — pick a real material by interests and level (podcast episode, YouTube talk; give title, link, duration ≤ 20 min) and schedule `discuss` 1–2 days after `listen`; attach 3 orienting questions to the listen entry
- **1 × write** — work topic (investor update, team announcement, reply to an objection); executed by `/fluent-writing`
- **1–2 × review** — scale to SRS queue size; if the queue is nearly empty, drop to 1 and add a talk instead

First-ever plan = **calibration week**: mark it as such in `goals`, keep it light, expect to adjust.

**Monthly checkpoint:** roughly every 4 weeks, schedule one `/coach-intro` re-run as an activity — a transparent level re-measure. Compare with the previous verdict and say out loud what moved (this is the long-arc progress signal on the road to `target_level`).

### 5. Confirm and write

Show the week as a table (day / type / what / minutes). Apply edits conversationally. Then write `data/weekly-plan.json`:

```json
{
  "week_id": "2026-W29",
  "created": "YYYY-MM-DD",
  "goals": ["…2-3 outcome-style goals…"],
  "activities": [
    {"id": "w29-1", "day": "mon", "type": "talk", "scenario": "status update call", "status": "planned", "session_ref": null},
    {"id": "w29-2", "day": "tue", "type": "listen", "source": {"title": "…", "url": "…", "duration_min": 15}, "questions": ["…", "…", "…"], "followup": "w29-3", "status": "planned"},
    {"id": "w29-3", "day": "wed", "type": "discuss", "about": "w29-2", "status": "planned"},
    {"id": "w29-4", "day": "thu", "type": "write", "topic": "…", "status": "planned"},
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
- **Clear intent only.** `/coach-plan` or an explicit ask to plan the week; it rewrites the plan file, so never fire from an ambiguous prompt.
