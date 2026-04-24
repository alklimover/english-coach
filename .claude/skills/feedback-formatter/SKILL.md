---
name: feedback-formatter
description: Canonical feedback template for every learner answer in the Fluent system — celebrate correct parts, correct mistakes with category + brief explanation, show full correct version, score out of 10, and classify severity (🔴 critical / 🟡 moderate / 🟢 minor). Use in every practice session (writing, vocab, speaking, reading, review) immediately after the learner submits an answer.
user-invocable: false
---

# Feedback Formatter

Every practice session ends each turn with immediate feedback. Consistency matters: the learner builds mental models from the structure, and the error patterns we mine from session files depend on predictable markers (❌, ✅, severity emoji).

## Standard Template

```markdown
{✅ or ❌} {one-line encouragement or gentle correction}

**Corrections:**
- ❌ "{wrong_part}" → **"{correct_part}"** ({category} — {brief_why})
- ✅ "{correct_part}" — {specific_praise}

**Correct version:**
"{full_correct_sentence}"

**Score: {X}/10** {emoji} {short_comment}

---
```

Skip the ❌ block if the answer was fully correct; skip the ✅ block only if truly nothing was right (rare — usually at least word order or intent was right).

## Severity Markers

Classify each ❌ error and tag it inline:

| Symbol | Severity | Meaning | Example |
|--------|----------|---------|---------|
| 🔴 | Critical | Breaks communication or exam-blocker | Formal/informal mix in formal email; wrong subordinate-clause word order |
| 🟡 | Moderate | Noticeable but understandable | Preposition error, missing article |
| 🟢 | Minor | Low priority | Spelling, punctuation, accent marks |

A single answer may contain multiple errors of different severity — tag each.

## Category Labels

Use these when explaining corrections (fed into `mistakes-db.json`):

- `grammar` — word order, conjugation, clause structure
- `formal_informal` — u/je, uw/jouw, register mismatch
- `vocabulary` — wrong word, English mixing, register-wrong synonym
- `spelling` — minor
- `prepositions` — om/op/in/bij/naar/etc.
- `articles` — de/het, definite/indefinite
- `missing` — omitted greeting, closing, required word

## Tone Rules

- **Encourage before correcting.** Open with a ✅ or a warm ❌ (`"Close! Let's tune one word."`), not a bare `Wrong.`.
- **Explain why, not just what.** `"Ik schrijf je" → "Ik schrijf u" (formal_informal — business emails require "u")` beats `"Use u not je."`.
- **Name the pattern.** Helps the learner generalize: `"This is the 'omdat' word-order rule: verb goes last."`.
- **Celebrate progress.** `"You didn't miss this last time — well done."` when mistakes-db shows improvement.
- **Emojis on.** The learner's profile has `use_emojis: true` by default. Keep them.

## Examples

### Mostly correct

> ✅ Nice — past tense is solid.
>
> **Corrections:**
> - 🟢 "gestern" → **"hier"** (vocabulary — small slip, you used the German word)
> - ✅ "Ik ben gegaan" — perfect auxiliary + participle
>
> **Correct version:**
> "Ik ben hier naar de markt gegaan."
>
> **Score: 9/10** 🎯 One minor swap — don't sweat it.
>
> ---

### Critical error

> ❌ Close, but one pattern is costing you points on the exam.
>
> **Corrections:**
> - 🔴 "Ik schrijf je omdat ik heb een vraag" → **"Ik schrijf u omdat ik een vraag heb"** (formal_informal + grammar — formal register needs "u", and "omdat" pushes the verb to the end)
> - ✅ "Ik schrijf" — correct opening verb
>
> **Correct version:**
> "Ik schrijf u omdat ik een vraag heb."
>
> **Score: 5/10** 💪 Two patterns to drill — both fixable.
>
> ---

## Score → SM-2 Quality

After scoring, feed the score into the SM-2 update (see the `sm2-calculator` skill). Quality = `floor(score / 2)`.

## Why This Matters

Structured, consistent feedback:
1. Lets the learner scan for what to fix at a glance.
2. Makes session files parseable so `PRACTICE.md` analysis + `/results` mining work.
3. Populates `mistakes-db.json` categories cleanly — which feeds spaced repetition, which drives the whole system.
