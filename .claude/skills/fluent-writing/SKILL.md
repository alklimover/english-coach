---
name: fluent-writing
description: Run writing practice or check a supplied text with systematic feedback and database updates. Invoked by a confirmed writing activity in the weekly plan or clear natural intent, including "подведём итоги дня/недели", "проверим дневник", "daily/weekly reflection", emails, and other short texts.
allowed-tools: Read, Write, Bash
---

# Writing Practice Session

## Overview

Full-text writing practice with systematic correction. One scenario per session, detailed feedback broken down by severity and category, DB update at end. Mastery-driven scenario selection keeps the task at the right level — challenging, not frustrating.

## When to Use

Run from a confirmed writing activity selected by `coach-today`, an unambiguous natural request to write, or a clear request to check a supplied journal/text. Do not auto-start merely because the learner pasted unrelated text; ask one short question if correction intent is unclear.

For journal-check mode, the supplied text is the answer: skip task generation and proceed directly to full-text analysis. For a planned activity, use its `format`, `topic`, `prompts`, and `length_words` instead of selecting a generic scenario.

## Instructions

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Need: `learner-profile` (level, target language, focus areas), `mistakes-db` (weak writing patterns), `mastery-db` (writing sub-skills).

### 2. Resolve the writing format

Use this precedence:

1. **Supplied journal/text to check:** preserve it verbatim as the original answer; infer `daily_reflection` or `weekly_reflection` only when clear, otherwise label it `personal_text`.
2. **Plan parameters:** obey `format`, `topic`, `prompts`, and `length_words`.
3. **Clear reflection intent:**
   - `daily_reflection` — 60–120 words: what happened, what went well or was difficult, what the learner felt or learned, and tomorrow's intention.
   - `weekly_reflection` — 120–220 words: achievements, difficult moments, lessons, recurring communication problems, and next-week focus.
4. **Other writing practice:** select by `mastery-db.skills_mastery`: formal email, informal email, form filling, personal text, then mixed scenarios as mastery rises.

Match every format to the learner's CEFR level. Reflections are personal records, not formal correspondence: never require greetings or closings, and prioritize clear chronology and natural expression.

### 3. Present the task only when no text was supplied

If the learner already supplied the journal/text to check, skip steps 3–4 and go directly to step 5 with that exact original text.

```markdown
## ✍️ Writing Exercise

**Scenario:** {clear description in native language}

**Task:** Write a {type} in {target_language}.

**Requirements:**
- Length: {X-Y} words
- Include: {must-include elements}
- Register: {formal / informal}
- Level: {CEFR}

{Optional: example structure for harder tasks}

**Write your {text_type} below:**
```

### 4. Collect the full text when needed

For a newly assigned task, wait for the complete text and don't correct mid-composition. Let the learner finish.

### 5. Systematic error analysis

Check every sentence for these categories:

1. **Grammar** — word order, conjugation, clause structure, articles
2. **Formal/informal** — register consistency
3. **Vocabulary** — wrong word, English mixing, register-wrong synonyms
4. **Missing elements** — only elements required by this scenario; greetings and closings apply to correspondence, never to reflections
5. **Spelling** — minor at A2, weightier at B2+
6. **Structure** — organization, flow, paragraphing

Tag each finding with a severity: 🔴 critical, 🟡 moderate, 🟢 minor.

### 6. Detailed feedback

Diverges slightly from the standard `fluent-feedback-formatter` template because writing answers are multi-sentence. Use this variant:

```markdown
## Feedback

### ✅ What You Did Well
- {strength 1}
- {strength 2}

### ❌ Areas to Improve

**Critical:** 🔴
- {issue}: "{wrong}" → **"{correct}"** — {why}

**Moderate:** 🟡
- {issue}: {explanation}

**Minor:** 🟢
- {spelling / punctuation}

### 📝 Corrected Version

```
{fully corrected text}
```

**Score: {X}/10**

**Breakdown:**
- Grammar: {Y}/10
- Vocabulary: {Z}/10
- Structure: {W}/10
- Communication: {V}/10

---
```

### 7. Optional rewrite

If score < 7, naturally offer to rewrite the text using the corrections. Do not require a keyword or command; understand an ordinary yes/no response.

### 8. Session summary

```markdown
## 📊 Writing Session Summary

**Text Type:** {type}
**Score:** {X}/10
**Key Takeaways:**
- {learning 1}
- {learning 2}
- {learning 3}

**Next Time:**
- Focus on: {weak pattern}
- Review: {relevant flashcards}

{target-language "well done"}! ✍️
```

### 9. Update all databases

Use the `fluent-db-updater` skill:

- `command_used: "/fluent-writing"`, `skills_practiced: ["writing"]`
- `skill_scores.writing: {exercises: 1, correct: 1_if_score_≥_7_else_0, time_minutes}`
- `errors[]` — one per distinct pattern found (dedupe; the script bumps frequency)
- `focus_next_session[]` — top 2 patterns to drill

Also save the exchange as `/results/fluent-writing-session-{NNN}.md` with the full task, the learner's original text, the corrected version, and the error table. The `fluent-session-analyzer` skill depends on this format.

## Examples

### Example 1 — formal email task (Dutch A2)

> ## ✍️ Writing Exercise
>
> **Scenario:** You need to cancel a doctor's appointment you have on Thursday.
>
> **Task:** Write a formal email to the doctor's office in Dutch.
>
> **Requirements:**
> - Length: 40-60 words
> - Include: greeting, reason, request for new appointment, closing
> - Register: formal
> - Level: A2
>
> **Write your email below:**

Learner: "Hallo, Ik schrijf je omdat ik kan niet komen op donderdag. Ik ben ziek. Kunnen we een andere dag afspreken? Bedankt, Mohammad"

> ## Feedback
>
> ### ✅ What You Did Well
> - Clear reason for cancellation.
> - Correct request structure.
>
> ### ❌ Areas to Improve
>
> **Critical:** 🔴
> - `formal_informal`: "Hallo" + "je" — formal email needs "Beste meneer/mevrouw" + "u". Mixed registers cost exam points.
> - `grammar`: "ik kan niet komen" is OK standalone, but after "omdat" Dutch word order flips: **"omdat ik niet kan komen"**.
>
> **Moderate:** 🟡
> - `missing`: no formal closing. Use "Met vriendelijke groet,".
>
> **Minor:** 🟢
> - Capitalize "Donderdag"? Actually no — Dutch doesn't capitalize weekdays. You were right.
>
> ### 📝 Corrected Version
>
> ```
> Beste meneer/mevrouw,
>
> Ik schrijf u omdat ik niet kan komen op donderdag. Ik ben ziek.
> Kunnen we een andere dag afspreken?
>
> Met vriendelijke groet,
> Mohammad
> ```
>
> **Score: 6/10**
> - Grammar: 6/10 — omdat word order tripped you up.
> - Vocabulary: 8/10 — solid word choice.
> - Structure: 5/10 — missing proper opening + closing.
> - Communication: 7/10 — message was clear despite issues.

## Critical Rules

- **One scenario per session.** Don't chain multiple writing tasks — depth over breadth.
- **Wait for the full answer** before correcting.
- **Severity tagging is mandatory.** Fed into `mistakes-db` and drives spaced repetition priority.
- **Always save the session file** in `/results/` for later analysis by `fluent-session-analyzer`.
- **Invoke only with authorization.** A confirmed plan activity, clear writing/reflection request, or explicit request to check supplied text is sufficient. Ask one short question when intent is ambiguous.

## Language Reference

### Dutch A2 patterns

**Formal emails:** always "u" (not "je"); open `Beste meneer/mevrouw {NAME},`; closing `Met vriendelijke groet,` + name.

**Informal emails:** "je" not "u"; open `Hallo {NAME},`; closing `Groetjes,` or `Tot snel,`.

**Common mistakes:** mixing formal/informal in one text; word order in `omdat` clauses (verb last); time expressions (`om 10:00 uur`, `op dinsdag`).

Add similar sections for other target languages as the learner needs them.
