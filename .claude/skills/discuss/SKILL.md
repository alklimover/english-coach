---
name: discuss
description: Voice discussion of a listening material from the weekly plan — retell, give opinions, argue with the author, all by the /talk conversation mechanics (TTS output, dictated input, zero mid-conversation corrections, review afterwards). New vocabulary from the material goes to the SRS queue. Fires on /discuss or when the learner says they've listened/watched the planned material and wants to talk about it ("я послушал подкаст", "давай обсудим видео").
allowed-tools: Read, Write, Edit, Bash
---

# Discuss — Talk About What You Listened To

## Overview

Turns passive listening into active speech. The learner watched/listened to a planned material; now they retell it, react to it, and defend a position — a real conversation about real content, not comprehension quiz questions.

## Instructions

### 1. Find the material

Read `data/weekly-plan.json` → today's (or the referenced) `discuss` activity → its `about` listen activity → `source` and `questions`.

- **Material not listened yet:** offer to reschedule the discussion and, if the learner wants, start a free conversation instead. Rescheduling is one edit, no drama.
- **No plan / ad-hoc discuss:** ask what they listened to and proceed the same way.

### 2. The conversation — /talk mechanics apply in full

Load the `talk` skill's rules and follow them exactly: context from `read-db.py`, TTS per `preferences.voice` after every reply, replies 2–3 spoken-ready sentences, **zero corrections mid-flow**, dictated-input tolerance, level matching, one simple question per turn, English only.

Discussion arc (adapt to the learner's level — retell first, argue later):

1. **Retell:** "So, what was it about? Give me the short version."
2. **React:** what surprised, what they agreed/disagreed with — use the 3 orienting questions from the plan as anchors, not as a quiz.
3. **Argue:** pick one of the author's claims and take the other side, gently — make the learner defend a position.

Duration ~10–15 minutes or a stop phrase, as in `/talk`.

### 3. Review and persist

Identical to the `/talk` review (four blocks, mistake explanations in Russian) plus one addition: **useful vocabulary from the material itself** — words/phrases the learner reached for or the material featured — goes to SRS as `item_type: "phrase"` with `category` = the material's topic.

Persist via `fluent-db-updater`: `command_used: "/discuss"`, `skills_practiced: ["speaking", "listening"]`. Transcript → `results/discuss-session-{NNN}.md`. Mark **both** the `listen` and the `discuss` activities `done` with `session_ref`.

## Critical Rules

- Everything in `/talk`'s Critical Rules applies here unchanged.
- **Not a comprehension quiz.** The orienting questions are conversation anchors; if the learner takes the discussion elsewhere, follow them.
- **Mark both activities** (`listen` + `discuss`) done — the pair is one unit of the plan.
- **Clear intent only.** `/discuss` or "I listened to it, let's talk" — ambiguous prompt → one clarifying question.
