---
name: fluent-speaking
description: Run a typed English conversation with role-plays and opinion questions, prioritizing communication and naturalness. Invoked only when the learner clearly asks for text-only conversation; ordinary requests to talk use the voice-first talk flow.
allowed-tools: Read, Write, Bash
---

# Speaking Practice (Typed)

## Overview

Conversational practice through typed dialogue. Unlike `/fluent-writing`, prioritize **communication and naturalness** — grammar errors that don't block meaning are downplayed. Goal: build the learner's confidence to produce target-language output without over-analyzing.

## When to Use

Run only from an unambiguous request for a typed/text-only conversation. Ordinary «давай поговорим» intent routes to the voice-first conversation flow.

Below A1 mastery 2, automatically choose a short vocabulary warm-up before conversation rather than asking the learner to name another skill.

## Instructions

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Need: `learner-profile` (level, target language), `mastery-db.skills_mastery.speaking`.

### 2. Opening

```markdown
# 🗣️ {target_language} Speaking Practice

Hallo {name}!

Today we're practicing **speaking** through typed conversation. I'll ask you questions or give scenarios, you respond naturally in {target_language} — just like a real conversation.

**Focus:** natural expression, fluency, pronunciation (typed)
**Level:** {CEFR}
**Duration:** 15-20 min

**Tips:**
- Think in {target_language}, not {native_language}
- Don't chase perfect grammar — focus on getting your message across
- Use complete sentences
- Be natural and conversational

**Ready? Let's chat!** 💬
```

### 3. Pick topic based on mastery

A2 topics:
1. Personal introductions
2. Daily routine
3. Hobbies and interests
4. Shopping
5. Making appointments
6. Asking for directions
7. Ordering food
8. Talking about weather
9. Weekend plans
10. Work / study

B1+: opinions, comparisons, hypotheticals, complaints, narratives.

### 4. One question at a time

```markdown
## Question {N}: {Topic}

{Question in target language}

**Type your answer in {target_language}:**
```

Build the conversation naturally — after 3-4 Qs on one topic, transition: `Interessant! Let's talk about something else...`.

### 5. Evaluate

Check in this order:

1. **Communication** (most important, 0-5 points): was the message clear? Did it answer the question?
2. **Grammar** (0-3 points): verb conjugation, word order, articles. Note but don't belabor.
3. **Vocabulary** (0-2 points): appropriate word choice, no English mixing.

Feedback template (variant of `fluent-feedback-formatter`):

```markdown
{✅ or 🟡} {one-line encouragement}

**What you said:**
"{their_answer}"

**Communication:** {Clear / Mostly clear / Unclear} ✅

**Grammar notes:** (secondary — don't over-focus)
- {major error → correction, only if communication-blocking}

**Natural alternative:**
You could also say: "{more_natural_phrasing}"

**Score: {X}/10**
- Communication: {Y}/5
- Grammar: {Z}/3
- Vocabulary: {W}/2

{encouragement}

---
```

### 6. Role-play (advanced)

For B1+ or when the learner is warmed up:

```markdown
## 🎭 Role-Play

**Scenario:** {clear description in simple target-language English}
**Your role:** {what the learner plays}
**I'll be:** {what Claude plays}

Ready? I'll start...

---

{first line in target language}

**Your turn:**
```

### 7. Session summary

```markdown
## 🎉 Speaking Session Complete!

**Duration:** {X} min
**Questions Answered:** {N}
**Topics Covered:** {list}

### Communication Scores
**Overall:** {percent}%
- Clear messages: {count}
- Natural expression: {rating}/5
- Confidence: Growing! 💪

### Vocabulary Used Well
- {words}

### For Next Time
- Try using: {new phrase}
- Practice: {weak area}

**{target-language well done}!** 🌟
```

### 8. Update all databases

Use the `fluent-db-updater` skill:

- `command_used: "/fluent-speaking"`, `skills_practiced: ["speaking"]`
- `skill_scores.speaking: {exercises: N, correct: count_of_clear_answers, time_minutes}`
- `errors[]` — only communication-blocking ones (don't flood mistakes-db with minor speaking slips)
- `focus_next_session[]` — one topic + one pattern

Save exchange to `/results/fluent-speaking-session-{NNN}.md`.

## Examples

### Example 1 — personal intro (English)

> ## Question 1: Introductions
>
> Tell me about yourself. What do you do for work?

Learner: "I am {LEARNER_NAME}. I am founder of small company, we build software products."

> ✅ Clear and natural!
>
> **What you said:** "I am {LEARNER_NAME}. I am founder of small company, we build software products."
>
> **Communication:** Clear ✅
>
> **Grammar notes:**
> - 🟢 "founder of small company" → **"the founder of a small company"** (articles — English needs them even where Russian has none). Small slip; message still crystal clear.
>
> **Natural alternative:**
> "I'm {LEARNER_NAME} — I run a small company where we build software products."
>
> **Score: 9/10**
> - Communication: 5/5
> - Grammar: 2/3
> - Vocabulary: 2/2
>
> Great start — you packed two ideas into one sentence, which is exactly what fluency looks like.

### Example 2 — role-play opener (status call scenario)

> ## 🎭 Role-Play
>
> **Scenario:** You're on a status call with a client. You need to explain a delay and propose a new timeline.
> **Your role:** Project lead
> **I'll be:** The client
>
> ---
>
> *"Hi! Thanks for jumping on. So — where are we with the delivery?"*
>
> **Your turn:**

## Critical Rules

- **Communication first.** A clear message with a missed article scores better than a grammatically perfect but confusing answer.
- **One question at a time.** Wait for reply before next.
- **Stay in the target language** for questions, transitions, and explanations. If comprehension fails, shorten, paraphrase, and give a concrete target-language example.
- **Praise natural expression.** If the learner uses "Well..." or "Actually..." correctly, call it out — those are fluency markers.
- **Don't over-correct.** A speaking session with 20 red marks kills confidence.
- **Authorization boundary.** Start only when the learner clearly requests text-only conversation; ordinary talk intent is voice-first.

## Language Reference

### English conversational fillers

- "Well..." (buying time to think)
- "Actually..." (correcting or adding nuance)
- "To be fair..." (balancing a point)
- "That makes sense." (acknowledging)
- "Sort of / kind of" (hedging)
- "Let me think..." (pausing naturally)
- "Right, got it." (confirming)

Add equivalents for other target languages as needed.
