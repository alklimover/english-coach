---
name: coach-intro
description: Transparent voice-first onboarding — explains the system in Russian, runs an announced ladder of English speaking probes, places the learner's level, records interests, and hands off to autonomous weekly planning. Runs on first contact after agreement or a clear request to explain the system or measure level.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Coach Intro — Onboarding Conversation

## Overview

The learner's first structured contact with the coach. Unlike a normal conversation with silent tracking, this session is **openly diagnostic**: the coach says what it is doing at every step. The learner leaves knowing how the system works, what their level is and why, and what the program will look like.

Re-running is safe and useful — it re-assesses the level and updates the profile; it never deletes progress.

## Language & voice rules for this skill

- **Meta-talk in Russian, on screen, NOT spoken** — explanations of how the system works, instructions, the verdict. The TTS voice is English-only; never pipe Russian text to `say`.
- **Probes and conversation in English, spoken** — every English line follows the `/talk` voice rules (2–3 sentences, no markdown, spoken via `say` per `preferences.voice`).
- The learner answers by dictation; the same tolerance rules as `/talk` apply (ignore punctuation, garbled fragment → re-ask, never logged as a mistake).

## Instructions

### 1. Load context

`read-db.py` as usual. If a `current_level` already exists, treat it as a prior to verify, not a fact.

### 2. Explain the system (Russian, ~6 lines, on screen)

Cover exactly this, briefly and warmly:

- Это голосовой тренажёр: ты говоришь (диктовкой), коуч отвечает голосом.
- Во время разговора коуч **не исправляет** — все ошибки и полезные фразы копятся и разбираются после, чтобы не ломать речь.
- Ошибки и фразы попадают в систему повторений (SM-2) — они будут возвращаться, пока не закрепятся.
- Я сам составляю программу недели из разговоров, аудирования, письма и повторений; когда ты говоришь «начинаем», я выбираю и запускаю занятие на сегодня.
- Сейчас — 10 минут разговорных проб от простых к сложным, чтобы честно определить уровень. Коуч будет говорить, когда усложняет.

Ask (Russian): «Готов? Дальше — по-английски.»

### 3. Level probe ladder (English, spoken, announced)

Climb rung by rung. **Announce each rung in one casual English line** ("Okay, warm-up first — easy one." / "Nice. Now a bit harder."). One task per rung, follow-up allowed. Stop climbing after the learner clearly struggles on **two consecutive rungs** (very short answers, broken structure, long stalls) — finish with one comfortable question so the session ends on a success.

| Rung | Target | Task shape |
|---|---|---|
| 1 · A2 | present simple, everyday lexis | introduce yourself, your typical day |
| 2 · B1 | past narrative | tell a short story about something that happened recently |
| 3 · B1+ | future / plans, connected speech | plans for this year, and why |
| 4 · B2 | opinion + justification, comparison | give an opinion on a familiar topic and defend it against one gentle pushback |
| 5 · B2+ | hypotheticals (conditionals) | "what would you do if…" on their domain |
| 6 · C1 | abstract topic, nuance | trade-offs, ambiguity, hedging on an abstract question |

Silent tracking as in `/talk`: mistakes and good phrases are collected but never corrected mid-flow.

### 4. Verdict (Russian, on screen)

Give a clear, honest placement the learner can act on:

- **Уровень: {CEFR}** — одной строкой, без хеджирования.
- **Что уже уверенно** — 2–3 пункта с примерами из проб (цитаты их собственных фраз).
- **Что ломается** — 2–3 пункта с примерами (сказал → естественный вариант → почему, по-русски).
- **Что это значит для программы** — какие сценарии и форматы будут в плане и почему.

### 5. Goals and interests (mixed, quick)

Confirm/refine conversationally or via AskUserQuestion:

1. Цель и целевой уровень (сейчас в профиле: work, C1) — всё ещё так?
2. Минут в день реалистично? (сейчас: 20)
3. **Интересы для материалов** — 3–5 тем, которые реально интересно слушать и обсуждать. Планировщик использует их при выборе материалов.

### 6. Record and persist

1. Update `data/learner-profile.json` (targeted edits): `learner.current_level`, `preferences.interests: [...]`, `preferences.onboarding_completed: "YYYY-MM-DD"`, refresh `focus_areas` if the verdict changed them.
2. Persist the probe conversation via `fluent-db-updater`: `command_used: "/coach-intro"`, `skills_practiced: ["speaking"]`, real duration; `errors[]` = the verdict's "что ломается" items (reuse watch-pattern ids where they match); good phrases → SRS.
3. Transcript → `results/coach-intro-{NNN}.md` (probes + verdict).

### 7. Hand off

Russian, one line: «Уровень записан. Теперь я соберу план недели и предложу первое занятие.» Then internally run `coach-plan` in autonomous mode and continue to today's activity.

## Critical Rules

- **Transparent, always.** The learner must never wonder "what is happening and why" — that was the failure mode this skill exists to fix.
- **Announce difficulty changes.** Silent level-testing is what `/talk` does; here it's explicit.
- **Russian meta is never spoken aloud.** Only English lines go to `say`.
- **End on a success.** Never end the ladder on a failed rung.
- **Re-runs refine, never reset.** No data is deleted; the level is simply updated.
- **Offer, don't ambush.** On first contact suggest the intro in one line and start only after natural agreement; never require a command name.
