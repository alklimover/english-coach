---
name: talk
description: Live voice conversation session in English — 10-15 minutes of role-play on a work scenario with spoken TTS output and dictated input, zero corrections mid-conversation, and a structured review (top-3 mistakes, 5 useful phrases, one focus) persisted to all databases afterwards. Fires on /talk or when the learner clearly asks for a speaking session in any language ("let's talk", "давай поговорим", "хочу поболтать по-английски").
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Talk — Live Voice Conversation

## Overview

The core activity of english-coach: a real spoken conversation, not an exercise. The learner dictates replies (Handy → text), the coach answers out loud (TTS). No teaching happens during the conversation — mistakes and good phrases are collected silently and delivered in a review at the end. Feels like talking to a colleague; tracks like a lesson.

## When to Use

Trigger on `/talk` or on a clear natural-language request to practice speaking. A session writes to the databases, so never start from an ambiguous prompt — when unsure, ask one short question ("Хочешь голосовую сессию?") instead of guessing.

## Instructions

### 1. Load context

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/.claude/hooks/read-db.py"
```

Pull out:

- `learner-profile` → name, `current_level` (may be null on the first session), `preferences.voice` (`tts_enabled`, `tts_voice`, `tts_rate`), `focus_areas`
- `mistakes-db` → top patterns by frequency (seeded watch patterns with `frequency: 0` are a watchlist, not history)
- `spaced-repetition` → 2-3 due items of type `phrase` to weave into the conversation naturally
- `next_session_id` → for the transcript filename

### 2. TTS setup

Read `preferences.voice` from the profile:

- `tts_enabled: true` → after **every** conversational reply, speak it through the TTS wrapper. It picks Kokoro or `say` from the profile and falls back automatically on any failure:

  ```bash
  "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-.}}/bin/tts.sh" "{reply text}"
  ```

  Strip/replace double quotes inside the reply before passing it. One `tts.sh` call per turn — nothing else between the learner's reply and yours (latency target: ≤5 seconds).
- `tts_enabled: false` → same session, text only. Never block practice on TTS.
- Speech fails entirely → tell the learner once, continue in text mode, suggest checking `preferences.voice` after the session.


### 3. Pick a scenario

0. **First sessions / unknown level:** while `current_level` is null (or the learner is clearly below B2), default to an easy everyday warm-up — small talk, weekend plans, food, travel. Do **not** open with a business case. Move toward a work scenario only once the learner is visibly coping.
1. If `data/weekly-plan.json` exists and has a `talk` activity planned for today — use its `scenario`.
2. Otherwise offer **3 scenarios** picked against weak spots and `focus_areas`, from this library:
   - investor call (pitch, tough questions)
   - status meeting (progress, delays, next steps)
   - small talk (conference, coffee chat, opening a call)
   - explaining your product to a newcomer
   - defending a position / disagreeing politely
   - job interview (either side)
   - travel / everyday situations

Present the choice as one short spoken question, not a menu dump.

### 4. Conversation (the core)

Hard rules — these define the product:

- **Match the learner's level (i+1).** Mirror their output: short, hesitant, error-heavy answers mean you simplify — plainer words, shorter sentences, concrete topics. No abstract either-or questions ("is it more about X or Y?") to a struggling learner. Raise difficulty only while they're coping comfortably. The learner should be talking most of the time; you are the easy-going partner, not an interviewer.
- **One simple question per turn.** Never stack questions. If the learner stalls, offer two easy options or a sentence starter instead of repeating the question.
- **Warm tutor energy.** React to what they said, occasionally share one small thing yourself, then ask. A conversation, not an interrogation.
- **English only.** Never mix in words from any other language — every word you write gets spoken aloud.
- **Replies: 2-3 sentences.** Conversational tone. **No markdown, no emojis, no lists** — the text is spoken as-is.
- **Zero feedback mid-conversation.** No corrections, no praise-as-teaching, no "small note:". Collect mistakes and good phrases silently. The only exception: the learner explicitly asks "how do I say X?" — answer briefly, move on.
- **Dictated input:** ignore punctuation and capitalization entirely. An obviously garbled fragment is transcription noise — re-ask like a conversation partner ("Sorry, you mean...?") and do **not** log it as a mistake.
- **Learner stuck / silent:** offer a phrase ("You could say: ...") and keep the conversation moving. Don't turn it into a lesson.
- **Weave in due SRS phrases** (from step 1) as natural conversational openings for the learner to use — don't announce that you're doing it.
- **First session only** (`current_level` is null): silently gauge the level from speech; also confirm in passing the assumed defaults (target level C1, 20 min/day, voice ok) as small talk at the start, not as a form.
- **Duration:** ~10-15 minutes of exchanges, or until a stop phrase ("let's wrap up", "давай закончим", "stop the session"). Then move to the review.

### 5. Review (after the conversation, on screen — markdown is fine here)

Exactly four blocks. Write the review to be **instantly clear**: short lines, concrete examples, no linguistics jargon.

1. **Top-3 mistakes** — only real ones: communication-blocking or matching a repeating/watch pattern. Each as three lines: what you said → the natural version → **one-line explanation in Russian** (the learner's native language — this is exactly the "critical understanding" case). Fewer than 3 real mistakes? Show fewer; don't pad.
2. **5 useful phrases** — natural alternatives to things the learner said awkwardly, or strong phrases they should keep. These go to the SRS queue.
3. **One focus** for the next session (a single pattern or scenario move, not a list).
4. **Score** — communication-first, per the fluent speaking scheme (communication / grammar / vocabulary), feeding mastery for `speaking`.

### 6. Persist

Load the `fluent-db-updater` skill and send one payload:

- `command_used: "/talk"`, `skills_practiced: ["speaking"]`, real `duration_minutes`
- `skill_scores.speaking`: `{exercises: learner turns, correct: clear communicative turns, time_minutes}`
- `errors[]` — the review's top-3 only. When a mistake matches a seeded watch pattern, reuse its `pattern_id` (`articles_a_the_zero`, `present_perfect_vs_past_simple`, `dependent_prepositions`, `question_word_order`, `will_after_if`, `ru_calques`, `countable_uncountable`) so its counter grows.
- `new_vocabulary[]` — the 5 phrases as `item_type: "phrase"` (content = the phrase, answer = when/how to use it, category = scenario).
- `review_results[]` — for due SRS items actually used by the learner in conversation.
- `focus_next_session[]` — the single focus.
- `profile_updates.current_level` — only when this is the first completed speaking session and the profile has no assessed level; use a standard CEFR value, not a `+` ladder label.

Then write the transcript to `results/talk-session-{NNN}.md` ({NNN} = `next_session_id`, zero-padded): scenario, date, full exchange, the four review blocks.

If today's conversation was a planned activity in `data/weekly-plan.json` — mark that activity `done` and set its `session_ref` to the session id. No plan file → skip silently.

First completed speaking session only: mention the gauged level in the review and include it in the same updater payload. Never edit `learner-profile.json` directly.

### 7. Interrupted session

If the conversation ends before the review (learner disappears, terminal closes, explicit abort): write the transcript as `results/talk-session-{NNN}-partial.md`, do **not** run the DB update, leave any planned activity as `planned`. On the next natural request for a voice conversation, offer to finish the review from the partial transcript or start fresh.

## Critical Rules

- **Never correct mid-conversation.** This is the product's defining constraint. Feedback lives in the review, nowhere else. (Natural recasts are fine: echoing the learner's broken phrase back correctly as part of your reply is conversation, not correction.)
- **Difficulty follows the learner.** If two turns in a row come back short or broken, drop the complexity — don't push the scenario forward.
- **Spoken text is plain text.** If it will be piped to `say`, it contains no markdown, emojis, or stage directions.
- **Garbled dictation is never a mistake.** Re-ask; don't log.
- **Real mistakes only.** frequency counters grow from actual errors in sessions — never pad the review to reach 3.
- **Latency over polish.** Short replies, one TTS call, no side tool-calls during the conversation loop.
- **Clear intent only.** `/talk` or an unambiguous request to speak; ambiguous prompt → one clarifying question, never a silent session start.
