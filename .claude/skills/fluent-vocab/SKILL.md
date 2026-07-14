---
name: fluent-vocab
description: Run an interactive vocabulary drill with active-recall prompts, spaced repetition, and per-answer feedback. Invoked by a confirmed vocabulary activity in the weekly plan or clear natural intent such as "потренируем слова" / "practice vocabulary"; updates the learning databases at the end.
allowed-tools: Read, Write, Bash
---

# Vocabulary Drill Session

## Overview

Flashcard-style vocabulary practice using spaced repetition. One word at a time, immediate feedback, DB update at the end. Interleaves three modes (recognition, production, cloze) to force active recall rather than passive re-reading.

## When to Use

Run only from a confirmed vocabulary activity selected by `coach-today` or an unambiguous natural request to practise words. An incidental mention of vocabulary is not authorization to start a drill.

If there are no due or queued words, naturally offer today's next planned activity without naming internal skills.

## Instructions

### 1. Load vocabulary data

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

If the helper is unavailable, resolve `<data_dir>` via `fluent_paths.data_dir()` then read:

- `<data_dir>/spaced-repetition.json`
- `<data_dir>/mistakes-db.json`
- `<data_dir>/mastery-db.json`
- `<data_dir>/learner-profile.json` (for target_language, name, level)

If any are missing, direct the learner to `/fluent-setup` and stop.

### 2. Select words

Priority order:

1. Items in `spaced-repetition.review_queue.today` with `item_type == "vocabulary"`.
2. Words from `mistakes-db.json` where `category == "vocabulary"` and `mastery_level <= 2`.
3. New high-frequency words matching `learner-profile.focus_areas`.

Limit: `spaced-repetition.daily_limits.review_items_per_day` (default 20).

### 3. Present one word at a time

Rotate the three modes so the session is not monotonous.

**Recognition** (target_language → native):

```markdown
## Word {N}/{total}

**{target_language}:** {word}

**Context:** {example_sentence}

**What does it mean in {native_language}?**

**Type your answer:**
```

**Production** (native → target_language):

```markdown
## Word {N}/{total}

**{native_language}:** {word}

**Use it in a sentence (optional).**

**How do you say this in {target_language}?**

**Type your answer:**
```

**Cloze** (fill in the blank):

```markdown
## Word {N}/{total}

**Complete the sentence:**

{target_language sentence with _____ where the word goes}

**Type the missing word:**
```

### 4. Feedback after each answer

Use the `fluent-feedback-formatter` skill's template. Score out of 10, tag severity.

Track the answer for the end-of-session DB update:

- Add to `review_results[]` with `quality = floor(score / 2)` (see `fluent-sm2-calculator` skill).
- If the learner met a new word, stage it for `new_vocabulary[]`.
- If the learner made an error, stage it for `errors[]`.

Do **not** call `update-db.py` after every word — batch at session end.

### 5. Session summary

```markdown
## 📚 Vocabulary Session Complete!

**Words Reviewed:** {N}
**Accuracy:** {X}%
**New Words Learned:** {Y}
**Words Mastered (→ level 5):** {Z}

**Strong:** {list words with mastery 4-5}
**Need more practice:** {list words with mastery 0-2}

**Next review:**
- Tomorrow: {count} words
- This week: {count} words

{target-language "well done"}! 🌟
```

### 6. Update all databases

Call the `fluent-db-updater` skill's workflow — one `update-db.py` invocation with:

- `session_id`, `date`, `duration_minutes`
- `command_used: "/fluent-vocab"`
- `skills_practiced: ["vocabulary"]`
- `skill_scores.vocabulary`: `{exercises, correct, time_minutes}`
- `errors[]`, `new_vocabulary[]`, `review_results[]` collected during the session
- `focus_next_session[]` — top 2-3 weak words

## Examples

### Example 1 — recognition drill

> ## Word 1/15
>
> **English:** to hire
>
> **Context:** "We're hiring two engineers this quarter."
>
> **What does it mean in Russian?**
>
> Type your answer:

Learner: "нанимать"

> ✅ Exactly.
>
> **Answer:** нанимать (брать на работу)
> **Meaning:** To employ someone for a job.
> **Example:** "We're hiring two engineers this quarter." (Мы нанимаем двух инженеров в этом квартале.)
>
> **Score: 10/10** 🎯
>
> ---

### Example 2 — production with error

> ## Word 7/15
>
> **Russian:** обсудить

> **How do you say this in English?**

Learner: "to discuss about"

> ⚠️ Almost — "discuss" takes **no preposition**: *discuss the plan*, not ~~discuss about the plan~~.
>
> Now: use it in a short sentence about tomorrow's meeting.

### Example 3 — session end summary

> ## 📚 Vocabulary Session Complete!
>
> **Words Reviewed:** 15
> **Accuracy:** 80% (12/15)
> **New Words Learned:** 3
> **Words Mastered:** 1
>
> **Need more practice:** de sleutel, het raam, gisteren
>
> **Next review:** Tomorrow 4 words, this week 8 words.
>
> Goed gedaan! 🌟

## Critical Rules

- **One word at a time.** Wait for the learner's answer before showing the next.
- **Immediate feedback** after each — use `fluent-feedback-formatter`.
- **Mix modes.** Don't drill 20 recognition prompts in a row — interleave for discrimination.
- **Use target language** for greetings + transitions when the learner is B1+; for A1-A2 mix target + native.
- **Never** update the DBs mid-session — batch at end.
- **Authorization boundary.** Start only from a confirmed vocabulary activity or clear request to practise words.

## Tips for the Learner (append if they seem tired or unsure)

- Review daily for best retention — spaced repetition depends on it.
- Focus time on weak words (mastery 0-2), not already-strong ones.
- Use words in sentences to build contextual memory.
- Say words out loud even though you're typing.
