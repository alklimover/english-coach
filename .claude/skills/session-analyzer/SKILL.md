---
name: session-analyzer
description: Parse Fluent `/results/*.md` session files to extract error patterns, strengths, accuracy trends, and focus areas for the next session. Use when the tutor needs to analyze the learner's recent performance — planning the next lesson, recommending focus areas, or answering "what should I practice next?".
user-invocable: false
---

# Session Analyzer

Every practice session writes a markdown report to `/results/{skill}-session-{ID}.md` (e.g. `writing-session-012.md`). This skill describes how to read those files to plan adaptive follow-up practice.

## When to Use

- Before `/learn`, `/writing`, etc. — to decide today's focus.
- When the learner asks "what's my weakest area" or "what should I work on".
- When generating the next session plan.

## Where to Look

```
/results/{skill}-session-{ID}.md
```

File naming: `{skill}-session-{NNN}.md` keeps files grouped by skill + chronological by ID. Read the most recent 3-5 files of the relevant skill; don't re-read the entire history.

## What to Extract

### 1. Error patterns

Scan for `❌` markers. Each correction has:

- The wrong form ("Your answer")
- The correct form
- A category (grammar, formal_informal, vocabulary, prepositions, articles, spelling, missing)
- A severity (🔴 critical, 🟡 moderate, 🟢 minor)

Count frequency per pattern across the recent files:

- **1 occurrence** — possibly a typo, ignore
- **2-3** — emerging pattern, worth drilling
- **4+** — critical weakness, highest priority

### 2. Strengths

Scan for `✅` markers and scores ≥ 7/10. Note consistent correct usage — these are reinforcement targets, not drill targets.

### 3. Trajectory

Across sessions, track:

- Overall accuracy per session
- Critical vs moderate vs minor error counts
- Writing speed (words per minute, if tracked)

## Output Format

When reporting to the learner or using for planning, structure as:

```markdown
## Error Pattern Summary

| Category | Pattern | Session Count | Total Count | Severity | Example |
|----------|---------|---------------|-------------|----------|---------|
| formal_informal | Using "je" in formal context | 2 | 5 | 🔴 | "Ik schrijf je" → "Ik schrijf u" |
| grammar | Wrong "omdat" clause order | 1 | 3 | 🟡 | "omdat ik kan niet" → "omdat ik niet kan" |

## Strengths
| Skill | Evidence | Confidence |
|-------|----------|------------|
| Vocabulary recall | Correctly used "afspraak", "dokter" | ⭐⭐⭐⭐☆ |

## Trajectory
| Session | Date | Accuracy | Critical | Moderate | Minor |
|---------|------|----------|----------|----------|-------|
| 003 | 2026-04-22 | 65% | 3 | 4 | 2 |
| 004 | 2026-04-23 | 72% | 2 | 3 | 3 |
```

## Planning the Next Session

Based on the analysis:

1. **Top 3 critical weaknesses** (highest frequency + severity) → 50% of session time.
2. **Top 2 moderate patterns** → 30% of session time.
3. **One full integration scenario** → 20% of session time.

Template:

```markdown
## Session {N} Plan ({X} min)

**Top 3 Weaknesses:**
1. {pattern} — {count} occurrences, severity {emoji}
2. ...

**Strengths to Reinforce:**
- {skill}

**Drill Sequence:**
1. Warm-up ({x} min) — quick wins on known patterns
2. Targeted drill 1 ({y} min) — focus on weakness #1
3. Targeted drill 2 ({y} min) — focus on weakness #2
4. Mixed integration ({z} min) — combine all patterns
5. Full scenario ({w} min) — exam-style task
```

## Adaptive Difficulty

Use recent session accuracy to tune today's difficulty:

- **<50%** → simplify, add scaffolding, smaller chunks
- **50-70%** → correct zone, keep going
- **>70%** → raise difficulty, introduce new patterns

## Interaction with the Databases

This skill reads `/results/` **markdown** files — the narrative record. The JSON databases (`mistakes-db.json` etc.) already aggregate the same data; prefer reading the DB via `.claude/hooks/read-db.py` when you need counts + metadata. Use the markdown files when you need **context** — the actual sentence the learner wrote, the scenario, the exact feedback given.

## Why This Matters

Pattern analysis turns raw session records into an adaptive curriculum. Without it, every session looks the same regardless of progress. With it, tomorrow's drills target yesterday's weakest spots — that's the whole point of the system.
