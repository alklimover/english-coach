---
name: review
description: Run today's spaced-repetition review queue — items scheduled by SM-2 that need reinforcement before the learner forgets them. Triggered only when the learner types /review. Pulls due items from spaced-repetition.review_queue.today, generates a targeted exercise for each, evaluates the response, updates SM-2 parameters, and reshelves items into the correct future queue.
allowed-tools: Read, Write, Bash
disable-model-invocation: true
---

# Spaced-Repetition Review Session

Replay items the learner learned before, timed so they hit just before the forgetting curve drops them. This is the single most effective session type — the system depends on it running daily.

## Protocol

### 1. Load review queue

```bash
python3 .claude/hooks/read-db.py
```

Read `spaced-repetition.review_queue.today` and `daily_limits.review_items_per_day`. Sort items by `priority` (critical → high → medium → low). Cap at the daily limit (usually 20).

If the queue is empty, tell the learner and suggest a different command:

```markdown
🎉 No reviews due today! Your spaced repetition is up to date.

Want to practice something new? Try:
- `/learn` — adaptive mixed practice
- `/vocab` — learn new words
- `/progress` — see your stats
```

### 2. Opening

```markdown
# 🔄 Today's Spaced Repetition Review

Hallo {name}! Time to review items your brain is about to forget. This keeps everything fresh. 🧠

**Items Due Today:** {count}
**Estimated Time:** ~{minutes} min

Why review? Spaced repetition prevents forgetting, moves items into long-term memory, and builds automaticity.

**Ready? Let's start!** 💪
```

### 3. For each queue item

Each item has:
```json
{
  "item_id": "...",
  "item_type": "error_pattern | vocabulary | grammar_rule",
  "easiness_factor": 2.5,
  "interval_days": 6,
  "repetitions": 2,
  "due_date": "YYYY-MM-DD",
  "priority": "critical | high | medium | low",
  "content": "...",
  "answer": "..."
}
```

Generate an exercise matched to `item_type`:

- **error_pattern**: load the pattern from `mistakes-db`, create a scenario that forces the correct form. E.g. `formal_informal_confusion` → ask the learner to complete a formal email opening.
- **vocabulary**: recognition (target → native), production (native → target), or cloze — rotate modes.
- **grammar_rule**: a fill-in or error-correction exercise that tests the rule.

Present one at a time:

```markdown
## Review {N}/{total} — {priority emoji}

**Type:** {item_type}
**Last reviewed:** {X} days ago
**Current mastery:** {stars}

{exercise}

**Type your answer:**
```

### 4. Evaluate + update SM-2

Use `feedback-formatter` for the per-answer feedback.

Then stage the item for the end-of-session update. Do NOT hand-edit `spaced-repetition.json` — use `review_results[]` in the `db-updater` payload:

```json
{ "item_id": "vocab_huis", "quality": 4 }
```

The `update-db.py` script runs the SM-2 math (see `sm2-calculator` skill) and rebuilds the queue. Mapping: `quality = floor(score / 2)`.

### 5. Progress pulse every 5 items

```markdown
## Progress Update

**Reviewed:** {N}/{total}
**Accuracy:** {percent}%
**Time Remaining:** ~{min} min

Keep going! 💪
```

### 6. Session summary

```markdown
## 🎉 Review Session Complete!

**Reviewed:** {count}
**Accuracy:** {percent}%
**Time:** {min} min

### Breakdown

**Mastered (no mistakes):** {count} — won't appear again for a while 🎉
**Good (minor slips):** {count} — next in {X} days
**Need more practice:** {count} — tomorrow again

### Next Review Schedule
- Tomorrow: {count}
- This week: {count}
- Next week: {count}

**Streak:** 🔥 {X} {day/days} 🔥

**Tip:** {one line of advice based on accuracy}

{target-language well done}! 🌟
```

### 7. Update all databases

Call `db-updater`:
- `command_used: "/review"`, `skills_practiced: [derived from reviewed items]`
- `skill_scores` — aggregate per skill touched
- `review_results[]` — every item reviewed, with `quality`
- `errors[]` — only patterns where the learner got it wrong (bumps frequency)
- `focus_next_session[]` — the 2-3 items with lowest quality this session

Save exchange to `/results/review-session-{NNN}.md` for later analysis.

## SM-2 Queue Reshelving

After each item:
- quality ≥ 3 → new `interval_days` computed, move to `tomorrow` / `this_week` / `later` based on the interval.
- quality < 3 → `interval_days = 1`, `repetitions = 0`, stay in `today` (so the learner sees it again this session).

Details in the `sm2-calculator` skill. The script handles this — do not re-implement.

## Critical Rules

- **Daily.** The whole system assumes the learner runs `/review` every day. Missing a day breaks the intended spacing.
- **Honor `disable-model-invocation`.** This session is long and mutates SM-2 state. Never auto-start.
- **One item at a time.** Rushing = false positives.
- **Let the learner struggle.** If they don't remember, that's useful data (quality 0-2). The algorithm needs honest signals.
- **Never hand-edit `spaced-repetition.json`.** Queue is rebuilt on every `update-db.py` call.

## What the Schedule Means (tell the learner if they ask)

- 1 day — new or struggling items
- 2-3 days — learning, building strength
- 1 week — getting comfortable
- 2+ weeks — strong, maintenance only
- 1+ month — mastered, long-term memory
