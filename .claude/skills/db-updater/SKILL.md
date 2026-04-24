---
name: db-updater
description: Atomically update all 6 Fluent learner databases (learner-profile, progress, mistakes, mastery, spaced-repetition, session-log) at session end by calling .claude/hooks/update-db.py with a single JSON payload. Use at the end of every practice session — writing, vocab, speaking, reading, review, learn — to persist the session's errors, review results, new vocabulary, and session metadata.
user-invocable: false
---

# Database Updater

Every practice skill ends with a DB update. Instead of hand-editing 6 JSON files (error-prone, racy, easy to desync), pipe one JSON report to `update-db.py`. The script runs pre-write backups, validates, applies all changes atomically via `.tmp + fsync + rename`, and rebuilds the spaced-repetition queue.

## When to Call

- At the end of every session, **after** the last feedback is shown and **before** the session summary.
- Never mid-session. The script rebuilds the review queue each run — partial updates risk inconsistency.

## Command

```bash
python3 .claude/hooks/update-db.py <<'EOF'
{ ...payload... }
EOF
```

Run from the repo root. Exit codes: `0` success, `1` validation error, `2` I/O error.

## Payload Schema

### Required

- `session_id` — string, convention `session-NNN`. Use `computed.next_session_id` from `read-db.py`.
- `date` — YYYY-MM-DD.

### Optional (omit to skip)

```json
{
  "session_id": "session-005",
  "date": "2026-04-24",
  "duration_minutes": 20,
  "command_used": "/learn",
  "skills_practiced": ["vocabulary", "writing"],
  "skill_scores": {
    "vocabulary": { "exercises": 5, "correct": 4, "time_minutes": 10 },
    "writing":    { "exercises": 3, "correct": 3, "time_minutes": 10 }
  },
  "errors": [
    {
      "pattern_id": "verb_conjugation_3rd_person",
      "category": "grammar",
      "subcategory": "verb_conjugation",
      "your_answer": "Hij spreek",
      "correct_answer": "Hij spreekt",
      "context": "3rd person singular",
      "difficulty_score": 0.7,
      "severity": "critical",
      "notes": "optional"
    }
  ],
  "new_vocabulary": [
    {
      "item_id": "het_huis",
      "item_type": "vocabulary",
      "content": "het huis",
      "answer": "the house",
      "category": "essential_nouns",
      "difficulty": "A1",
      "initial_quality": 4,
      "priority": "medium"
    }
  ],
  "review_results": [
    { "item_id": "vocab_dag", "quality": 4 }
  ],
  "topics_covered": ["articles", "house_vocabulary"],
  "breakthroughs": ["First correct use of 'het' vs 'de'"],
  "focus_next_session": ["Drill de/het article gender"],
  "session_notes": "Strong session.",
  "achievements_earned": [],
  "milestones": []
}
```

## Field Notes

- `errors[]` — one entry per distinct mistake made this session. Collapse duplicates (same pattern_id) before sending; `frequency` is bumped by the script.
- `new_vocabulary[]` — items the learner met for the first time. Fill every field; incomplete entries yield incomplete spaced-repetition records.
- `review_results[]` — items already in the queue that were reviewed this session. The script runs SM-2 on each. See the `sm2-calculator` skill.
- `skill_scores[].correct` counts correct exercises, not a percentage. Accuracy is derived.
- `confidence` in `learner-profile.skills` is 0–100 integer; `accuracy` in `progress-db` is 0.0–1.0 float. The script handles the conversion.

## Data Model Quick Reference

- Session IDs: `session-NNN` (zero-padded to 3 digits).
- `spaced-repetition.review_queue` is **regenerated from scratch** every run — any manual edits there get wiped. Only update queue items via `review_results` / `new_vocabulary`.
- Backups land in `.backups/pre-update-<session_id>/` before any write.

## Reading Before Writing

Always call `read-db.py` at session start to get current state + `next_session_id`. Don't read each JSON file separately:

```bash
python3 .claude/hooks/read-db.py
```

Returns all 6 databases plus computed fields (`due_reviews_count`, `next_session_id`, `streak_active`, `days_since_last_session`).

## Failure Handling

- Exit `1` (validation): fix the payload — usually a missing required field or malformed JSON. No files were touched.
- Exit `2` (I/O): stderr has a full traceback. No files were touched. Check disk space, permissions.
- After a success, `session-log.json` has a new entry with `session_id`. If the same `session_id` is sent twice, the second call replaces the first.

## Why This Matters

Six interdependent JSON files must agree: a new `session-log` entry, a bumped `total_sessions`, updated SM-2 params, new mistake patterns, recalculated accuracy, refreshed streak. Hand-editing causes silent desync — streak says 7 days but session-log has 6 entries, mastery says 4 stars but accuracy says 45%. The script is the single source of truth.
