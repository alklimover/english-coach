---
name: sm2-calculator
description: SM-2 spaced-repetition algorithm reference for the Fluent language learning system. Use whenever the tutor needs to schedule the next review of a vocabulary item, grammar rule, or error pattern — i.e. after every answered review question. Defines the quality scale, interval formula, easiness-factor update, and mastery-level transitions that keep the spaced-repetition database correct.
user-invocable: false
---

# SM-2 Algorithm Calculator

The Fluent system uses SM-2 (SuperMemo 2) to decide when the learner next sees an item. Every practice skill updates `data/spaced-repetition.json` through this algorithm after each answered question.

## Quality Scale

Map the learner's 0-10 score to an SM-2 quality (0-5):

| Score | Quality | Meaning |
|-------|---------|---------|
| 10/10 | 5 | Perfect, instant recall |
| 8-9   | 4 | Correct after hesitation |
| 6-7   | 3 | Correct with difficulty |
| 4-5   | 2 | Incorrect but remembered when shown |
| 2-3   | 1 | Incorrect, familiar |
| 0-1   | 0 | Complete blackout |

Rule of thumb: `quality = floor(score / 2)`.

## Interval Formula

```
if quality >= 3:   # correct
    if repetitions == 0:
        interval = 1
    elif repetitions == 1:
        interval = 6
    else:
        interval = round(previous_interval * easiness_factor)
    repetitions += 1
else:              # incorrect
    interval = 1
    repetitions = 0
```

## Easiness Factor Update

Apply after every answer (correct or incorrect):

```
EF_new = EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
EF_new = max(1.3, EF_new)    # floor at 1.3
```

## Mastery Level Transitions

Separate from EF. Track `consecutive_correct` and `consecutive_incorrect` per item:

```
if consecutive_correct >= 5:
    mastery_level = min(5, mastery_level + 1)
    consecutive_correct = 0
elif consecutive_incorrect >= 3:
    mastery_level = max(0, mastery_level - 1)
    consecutive_incorrect = 0
```

## Per-Item Fields to Update

After each answer, the item in `spaced-repetition.json` must have:

- `easiness_factor` — updated via formula above
- `interval_days` — new interval
- `repetitions` — incremented or reset
- `consecutive_correct` / `consecutive_incorrect` — one incremented, the other reset
- `total_reviews` — incremented
- `mastery_level` — possibly changed per transition rules
- `due_date` — `today + interval_days` (YYYY-MM-DD)
- `last_reviewed` — today

## Queue Placement

After updating, route the item:
- `interval_days == 1` → `review_queue.tomorrow`
- `interval_days <= 7` → `review_queue.this_week`
- `interval_days > 7` → `review_queue.later`

If the learner got it wrong (quality < 3), keep it in `review_queue.today` so it reappears in the same session.

## Preferred Implementation

Do not hand-edit `spaced-repetition.json`. Call `.claude/hooks/update-db.py` with a `review_results` array; the script runs SM-2 atomically and rebuilds the queue. Only do manual math when the script is unavailable.

```bash
python3 .claude/hooks/update-db.py <<'EOF'
{
  "session_id": "session-NNN",
  "date": "YYYY-MM-DD",
  "review_results": [
    { "item_id": "vocab_huis", "quality": 4 }
  ]
}
EOF
```

## Worked Example

Learner answers "het huis" review: 9/10 → quality = 4.

Before: `interval_days=6, repetitions=2, easiness_factor=2.5, consecutive_correct=1`.

After:
- `repetitions = 3`
- `interval_days = round(6 * 2.5) = 15`
- `EF = 2.5 + (0.1 - 1*(0.08 + 1*0.02)) = 2.5 + 0 = 2.5`
- `consecutive_correct = 2` — no mastery change yet
- `due_date = today + 15 days`
- Queue: `later`

## Why This Matters

SM-2 reviews items **just before the learner forgets them**, maximizing long-term retention per minute of practice. Wrong scheduling = wasted reviews (too early) or forgotten items (too late).
