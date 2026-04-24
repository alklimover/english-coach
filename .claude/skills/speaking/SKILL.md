---
name: speaking
description: Run an interactive typed conversation session simulating spoken practice — free-flowing dialogue, role-plays, and opinion questions prioritizing communication over perfect grammar. Triggered only when the learner types /speaking. Asks questions one at a time in the target language, evaluates clarity + naturalness first and grammar second, and updates all databases at the end.
allowed-tools: Read, Write, Bash
disable-model-invocation: true
---

# Speaking Practice (Typed)

Conversational practice through typed dialogue. Unlike `/writing`, prioritize **communication and naturalness** — grammar errors that don't block meaning are downplayed.

## Protocol

### 1. Load context

```bash
python3 .claude/hooks/read-db.py
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

Feedback template (variant of `feedback-formatter`):

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

**Scenario:** {description in native language}
**Your role:** {what the learner plays}
**I'll be:** {what Claude plays}

Ready? I'll start...

---

{first line in target language}

**Your turn:**
```

Example scenarios:
- Supermarket: find bread, ask for help
- Doctor: make an appointment by phone
- Restaurant: order + ask about vegetarian options
- Lost tourist: ask directions to the station

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

Call `db-updater`:
- `command_used: "/speaking"`, `skills_practiced: ["speaking"]`
- `skill_scores.speaking: {exercises: N, correct: count_of_clear_answers, time_minutes}`
- `errors[]` — only communication-blocking ones (don't flood mistakes-db with minor speaking slips)
- `focus_next_session[]` — one topic + one pattern

Save exchange to `/results/speaking-session-{NNN}.md`.

## Critical Rules

- **Communication first.** A clear message with a missed article scores better than a grammatically perfect but confusing answer.
- **One question at a time.** Wait for reply before next.
- **Stay in the target language** for questions and transitions. Drop to native only for explanations.
- **Praise natural expression.** If the learner uses "Nou..." or "Eh..." correctly, call it out — those are fluency markers.
- **Don't over-correct.** A speaking session with 20 red marks kills confidence.

## Useful Conversational Phrases (target language hints)

### Dutch A2
- "Nou..." (well / so)
- "Eh..." (uh / um)
- "Eigenlijk..." (actually)
- "Dus..." (so / therefore)
- "Ja, dat klopt" (yes, that's right)
- "Ik snap het niet" (I don't understand)

Add equivalents for other target languages as needed.
