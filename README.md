# 🌍 Fluent
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Powered%20by-Claude%20Code-blue)](https://code.claude.com)

**The AI Language Learning Kit for Claude Code and others**

*A comprehensive set of rules, guidance, and intelligent tracking systems that transform Claude Code into your personal language tutor. Master any language through adaptive practice powered by proven cognitive science—spaced repetition, active recall, and progress tracking that learns from you.*

https://github.com/user-attachments/assets/66d68aad-210a-452d-b405-b58c13f42f53

---



## 🚀 Quick Start

### Prerequisites

- [Claude Code](https://code.claude.com) installed
- A Claude Code subscription
- **Python 3.8+** in your `PATH` — used by the automation hooks and DB scripts. Check: `python3 --version`.
  - macOS: pre-installed, or `brew install python3`.
  - Linux: `sudo apt install python3` (Debian/Ubuntu) or distro equivalent.
  - Windows: install via [python.org](https://www.python.org/downloads/) or use WSL.
- **Bash** — needed by the PreCompact safety-backup hook. Built-in on macOS/Linux. On Windows, use WSL or Git Bash.
- Basic understanding of command line.
- A desire to learn a new language! 🌟

> **No third-party Python packages required.** Fluent uses only the Python standard library — nothing to `pip install`.

### Installation

Two supported install paths. Both end at the same `/setup` prompt and share the same skills, hooks, and databases.

| Path | Best for | Data location |
|------|----------|---------------|
| **Claude Code plugin** (recommended) | Everyday use — runs from any directory | `~/.claude/fluent-data/` |
| **Git clone** | Customizing skills, contributing, or per-project learning state | `./data/` inside the repo |

---

#### 📦 Install as a Claude Code plugin (recommended)

Runs anywhere you launch Claude Code. Learner data is global under `~/.claude/fluent-data/` by default, so you can practice from any project or directory.

Two interchangeable paths — use whichever fits your workflow.

**Path 1 — Terminal (`claude` CLI):**

```bash
# 1. Add the Fluent marketplace (one-time; uses an interactive session)
claude
# Inside Claude Code:
/plugin marketplace add m98/fluent
# Then exit Claude Code (Ctrl+D or /exit)

# 2. Install the plugin from the shell — persists to your user config
claude plugin install fluent@fluent-marketplace

# 3. Verify the install (should list "fluent" as enabled)
claude plugin list
claude plugin validate fluent@fluent-marketplace

# 4. Launch Claude Code and start learning
claude
/setup
/learn
```

**Path 2 — Inside Claude Code (slash commands only):**

```
claude
```

Then in the session:

```
/plugin marketplace add m98/fluent
/plugin install fluent@fluent-marketplace
/plugin list                       # verify
```

Restart Claude Code, then run `/setup` to onboard and `/learn` to begin.

**Maintenance:**

- Update: `claude plugin update fluent@fluent-marketplace` (or `/plugin update fluent@fluent-marketplace` inside a session).
- Disable without uninstalling: `claude plugin disable fluent@fluent-marketplace`.
- Uninstall: `claude plugin uninstall fluent@fluent-marketplace`.

**Verify it's working:**

After installing and restarting, open Claude Code and confirm:

```
/                    # should show /setup, /learn, /vocab, /writing, /speaking,
                     # /reading, /review, /progress, plus helper skills
```

Or from the shell:

```bash
claude plugin list | grep fluent    # expect: fluent@fluent-marketplace  enabled
```

---

#### 📁 Install by cloning the repository

Best if you want to customize skills, contribute upstream, or keep per-project learning state. Learner data lives in `./data/` inside the cloned repo — cd into the repo to work with a given learner.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/m98/fluent.git
   cd fluent
   ```

2. **Start Claude Code from the repo root:**
   ```bash
   claude
   ```

3. **Run the onboarding:**
   ```
   /setup
   ```

4. **Start learning:**
   ```
   /learn
   ```

To update later: `git pull` inside the repo.

---

#### 📂 Where your data lives

Fluent stores your profile, progress, mistakes, and spaced-repetition state as JSON. Resolution precedence on every run (first match wins):

1. `$FLUENT_DATA_DIR` if the environment variable is set.
2. `$CLAUDE_PROJECT_DIR/data/` if that path contains `learner-profile.json` (clone mode, running from outside the repo root).
3. `./data/` if `./data/learner-profile.json` exists in the current working directory (clone mode, running inside the repo).
4. `~/.claude/fluent-data/` otherwise (plugin-install default).

Set `FLUENT_DATA_DIR` in your shell (e.g. `export FLUENT_DATA_DIR=~/.fluent/dutch`) to run multiple learners, one per target language, on the same machine.

**Verify your resolved data dir** at any time:

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/hooks')
from fluent_paths import data_dir
print('Fluent data directory:', data_dir())
"
```

**That's it!** Your AI tutor is ready and knows everything about your goals.

---

## 💡 Why This Actually Works

Most language learning apps fail because they're built for engagement metrics, not actual learning. This system is different.

### 🎯 Three Reasons This Works Where Others Fail:

**1. Zero Distractions, Pure Focus**
- ❌ No ads interrupting your flow
- ❌ No gamification gimmicks designed to waste your time
- ❌ No unreliable fancy UI that breaks
- ✅ Just you, the language, and an AI that adapts to your needs

**2. Infinitely Adaptable Intelligence**
- 🧠 Want to practice job interview phrases? Just ask.
- 🧠 Need help with a specific grammar rule? It explains it.
- 🧠 Want to focus on restaurant vocabulary? It creates exercises instantly.
- 🧠 **You're in control.** The AI does exactly what you need, when you need it.

**3. Your Private, Smart Tutor**
- 📊 **Tracks everything** - Every answer, every mistake, every improvement
- 🔄 **Learns about YOU** - Knows your weak patterns and strengths
- 📈 **Adapts to YOU** - Adjusts difficulty based on your performance
- 🔒 **Private** - All data stays on your machine, no external tracking
- 🎯 **Personal** - Like having a tutor who knows your exact level and learning style

**The Result?** A learning system that feels like a conversation with an expert friend who remembers everything, tracks your progress scientifically, and makes learning actually enjoyable.

---

## 📖 What Is This?

This is a comprehensive, **open-source language learning system** that transforms [Claude Code](https://code.claude.com) into your personal AI language tutor.

The system uses **evidence-based learning methodologies** including:
- **Spaced Repetition (SM-2 algorithm)** - Review at optimal intervals
- **Active Recall** - Test yourself before seeing answers
- **Adaptive Difficulty** - Always challenging, never frustrating
- **Comprehensive Tracking** - Every answer tracked and analyzed

### ✨ Key Features

- 🎯 **Multi-Language Support** - Learn any language (French, Spanish, German, Japanese, Korean, Arabic, Dutch, etc.)
- 📊 **Comprehensive Tracking** - Automatic progress monitoring with detailed statistics
- 🧠 **Spaced Repetition** - SM-2 algorithm schedules reviews just before you forget
- 🎮 **Gamification** - Streaks, achievements, mastery levels (0-5 stars)
- 🔄 **Adaptive Difficulty** - Automatically adjusts to your performance (targets 60-70% success rate)
- 📝 **Multi-Modal Practice** - Writing, speaking, vocabulary, reading, listening
- ⚡ **Immediate Feedback** - Clear explanations with every correction
- 🎨 **Interactive Sessions** - One question at a time, conversational feel
- 📈 **Progress Visualization** - Detailed statistics and trend analysis
- 💾 **Automatic Backups** - Hooks ensure your data is always safe

---

## 📚 How It Works

### The Learning Loop

Every practice session follows this intelligent cycle:

| Step | What Happens | Why It Matters |
|------|--------------|----------------|
| **1. You Practice** | Answer a question in your target language | Active recall forces your brain to retrieve information |
| **2. AI Analyzes** | System evaluates your response instantly | Identifies exactly what you got right or wrong |
| **3. Get Feedback** | Clear explanation of mistakes + correct version | Learning happens when you understand WHY |
| **4. System Tracks** | Updates 4 databases automatically | Remembers your weak spots and strengths |
| **5. Adapts** | Next question matches your current level | Always challenging, never frustrating |

**What Gets Tracked:**
- ✅ **Error Patterns** - Which grammar/vocab you struggle with
- ✅ **Mastery Levels** - Your skill rating (0-5 stars) for each topic
- ✅ **Review Schedule** - When to review based on SM-2 algorithm
- ✅ **Progress Stats** - Accuracy trends, streak days, total practice time

### Evidence-Based Methods

This system implements proven learning science:

**1. Active Recall** - You retrieve from memory before seeing answers
- 🔬 Research shows: **2-3x better retention** than passive review

**2. Spaced Repetition (SM-2 Algorithm)** - Reviews appear just before you forget
- 🔬 Research shows: **Prevents forgetting curve**, optimizes long-term retention

**3. Immediate Feedback** - Mistakes corrected within seconds
- 🔬 Research shows: **Faster learning** when feedback is immediate

**4. Interleaving** - Mix topics to prevent drilling fatigue
- 🔬 Research shows: **Better discrimination** and long-term retention

**5. Comprehensible Input (i+1)** - Content slightly above your level
- 🔬 Research shows: **Optimal learning zone** (Krashen's Input Hypothesis)

**6. Desirable Difficulty** - Targets 60-70% success rate
- 🔬 Research shows: **Too easy = no learning, too hard = frustration**

---

## 🎮 Available Commands & Skills

Fluent is built as **Claude Code skills** — 12 of them. Skills work two ways:

1. **Type the slash command** (`/learn`, `/vocab`, etc.) — you explicitly start a session. Learner-facing skills are gated so they only run this way. No accidental 20-minute session triggered by a chat message.
2. **Ask naturally** — read-only skills like `/progress` auto-trigger when you ask "how am I doing?" or "what's my streak?". Helper skills (SM-2 math, feedback formatter, DB updater, session analyzer) auto-load whenever Claude needs them during a session.

All 12 skills appear in your `/` menu so you can always invoke any of them manually.

### Learner-facing commands

These are the commands you'll use daily. Each is backed by a dedicated skill under `.claude/skills/`.

#### Core Commands

| Command | What It Does | When & Why to Use It |
|---------|--------------|----------------------|
| **`/setup`** | **One-time onboarding** - Asks you questions about your name, target language, current level, goals, and timeline. Creates your personalized learning profile. | **First time only** - Run this once to set up your account. The system generates a custom learning plan based on your answers. |
| **`/learn`** | **Adaptive mixed practice** - Combines different exercise types (vocabulary, grammar, sentences) based on your weak areas. Adjusts difficulty in real-time based on your performance. | **Daily core practice** - Your main command for general improvement. The AI decides what you need to practice most. Best after `/review`. |
| **`/review`** | **Spaced repetition session** - Shows you items that are due for review today based on the SM-2 algorithm. Focuses on things you learned before that need reinforcement. | **Start every day here!** - Review before learning new content. This is scientifically proven to be the most effective way to retain what you've learned. |

#### Skill-Specific Commands

| Command | What It Does | When & Why to Use It |
|---------|--------------|----------------------|
| **`/vocab`** | **Flashcard-style vocabulary drills** - Rapid-fire translation practice (target language ↔ native language). Tracks which words you struggle with. | **2-3x per week** - When you need to build vocabulary quickly. Great for preparing for specific topics (travel, business, etc.). |
| **`/writing`** | **Writing practice** - Practice emails, letters, essays, or forms in your target language. Get detailed corrections with grammar explanations. | **Daily for exam prep** - Essential if you're preparing for language exams. Also great for building confidence in real-world communication. |
| **`/speaking`** | **Conversation practice** - Role-play scenarios through typed dialogue. Practice natural conversations, asking for directions, ordering food, etc. | **2-3x per week** - Builds confidence for real conversations. Typed practice helps you think through responses without pressure. |
| **`/reading`** | **Reading comprehension** - Read short texts (stories, articles, dialogues) then answer comprehension questions. Expands vocabulary in context. | **2-3x per week** - Improves overall understanding. Best for intermediate+ learners. Reading is one of the fastest ways to absorb grammar patterns. |

#### Progress Command

| Command | What It Does | When & Why to Use It |
|---------|--------------|----------------------|
| **`/progress`** | **Statistics dashboard** - Shows your accuracy trends, streak days, mastery levels, achievements unlocked, and weak areas. Visual progress charts. | **Weekly check-in** - Read-only and safe to auto-invoke. Ask "how am I doing?" and Claude will open the dashboard automatically. |

### Helper skills (behind the scenes)

These skills don't change what the learner-facing commands do — they let Claude apply the same algorithms, feedback format, and database logic consistently across every session. You can still invoke them via `/` if curious.

| Skill | What It Does | When It Runs |
|-------|--------------|--------------|
| **`/sm2-calculator`** | SM-2 spaced-repetition algorithm reference: quality scale, interval formula, easiness-factor update, mastery-level transitions. | Auto-loaded whenever a review item is scored. |
| **`/feedback-formatter`** | Canonical per-answer feedback template — severity tagging (🔴 critical / 🟡 moderate / 🟢 minor), category labels, tone rules. | Auto-loaded every time Claude grades an answer. |
| **`/db-updater`** | How to call `update-db.py` with a single JSON payload that atomically updates all 6 databases at session end. | Auto-loaded when a session ends. |
| **`/session-analyzer`** | Parses `/results/{skill}-session-{ID}.md` files to extract error patterns, strengths, and focus areas for the next session. | Auto-loaded when planning the next session. |

### 📅 Recommended Daily Routine

**🌅 Morning Session (15 min)**
```bash
/review    # Must do first - Review what you learned before
/vocab     # Learn 5-10 new words
```
**Why?** Your brain is fresh. Reviewing first reinforces old knowledge, then new vocabulary sticks better.

**🌙 Evening Session (15 min)**
```bash
/writing   # Practice real-world writing
/learn     # Let AI choose what you need most
```
**Why?** Writing solidifies what you learned today. `/learn` fills in any gaps.

**📊 Weekly Check-In (5 min)**
```bash
/progress  # See your stats and celebrate progress!
```
**Why?** Seeing improvement = motivation. You need to see you're getting better!

---

## 📁 System Architecture

### Data Layer (`/data` directory)

**Your learning data is tracked in 6 JSON databases** (created automatically by `/setup`):

| File | Purpose | Created When |
|------|---------|--------------|
| `learner-profile.json` | Your info, level, preferences, streak | `/setup` - One time |
| `progress-db.json` | Overall statistics and trends | `/setup` - Updated every session |
| `mistakes-db.json` | Error patterns with frequency and examples | `/setup` - Updated when you make mistakes |
| `mastery-db.json` | Skill mastery levels (0-5 stars) | `/setup` - Updated after practice |
| `spaced-repetition.json` | Review queue (SM-2 algorithm) | `/setup` - Updated after each answer |
| `session-log.json` | Complete session history | `/setup` - New entry each session |

**📋 Want to see the structure?** Check `/data-examples/` for template files showing the complete schema.

**🔒 Privacy:** All data stays on your machine. Automatically excluded from git via `.gitignore`.

### Intelligence Layer

The AI follows these guides:

- **`LEARNING_SYSTEM.md`** - Complete methodology (how to teach)
- **`CLAUDE.md`** - AI tutor's role and personality
- **`PRACTICE.md`** - Pattern analysis and tracking
- **`.claude/references/`** - Shared templates (SM-2 worked examples, feedback template, DB payload schema, session-file format) that every skill references

### Interface Layer

- **Skills** (`.claude/skills/`) — 12 skills total. 8 learner-facing (`/setup`, `/learn`, `/vocab`, `/writing`, `/speaking`, `/reading`, `/review`, `/progress`) run when you invoke them. 4 helper skills (`/sm2-calculator`, `/feedback-formatter`, `/db-updater`, `/session-analyzer`) auto-load whenever Claude needs them during a session — and are also directly `/`-invokable if you want to read the reference.
- **Plugin manifests** (`.claude-plugin/`) — `plugin.json` + `marketplace.json` make Fluent installable via `/plugin marketplace add m98/fluent`.
- **Automatic Hooks** (`.claude/hooks/`) — SessionStart welcome, SessionEnd backups, PostToolUse JSON validation + backups, PreCompact safety backup. Both `hooks.json` (plugin mode) and `.claude/settings.json` (clone mode) wire them up.
- **Session Results** (`/results/`) — Detailed practice logs per session, parsed by `session-analyzer` to plan future sessions.

---

## 🎯 Learning Principles

### Spaced Repetition (SM-2 Algorithm)

**Example progression for a difficult word:**

```
Day 1:  Make a mistake → Review tomorrow (interval = 1 day)
Day 2:  Answer correctly → Review in 6 days
Day 8:  Correct again → Review in 2 weeks
Day 22: Still remember → Monthly review (mastered!)
```

The system tracks for each item:
- **Easiness Factor** - How easy it is for YOU specifically
- **Interval Days** - When to review next
- **Repetitions** - Practice count
- **Quality Score** - Your performance (0-5)

### Mastery Levels

Every skill and pattern gets a star rating:

- ⭐☆☆☆☆ (1) - Just started
- ⭐⭐☆☆☆ (2) - Learning
- ⭐⭐⭐☆☆ (3) - Good understanding
- ⭐⭐⭐⭐☆ (4) - Strong skill
- ⭐⭐⭐⭐⭐ (5) - Mastered!

### Adaptive Difficulty

The system automatically adjusts:

- **Success rate 40-50%** → Too hard, makes easier
- **Success rate 60-70%** → Perfect challenge! ✨
- **Success rate 80-90%** → Too easy, makes harder

**Goal:** Keep you in the "sweet spot" where learning happens.

---

## 🔬 Technical Details

### Technology Stack

- **Platform:** Claude Code (Anthropic), installable as a plugin or by clone
- **AI Model:** Claude (any Claude Code-supported model)
- **Data Format:** JSON (human-readable)
- **Skills:** Markdown `SKILL.md` files with YAML frontmatter (12 total — 8 learner-facing + 4 helper)
- **Hooks:** Python + Bash, triggered on SessionStart / SessionEnd / PostToolUse / PreCompact
- **Algorithm:** SM-2 (SuperMemo 2)
- **Version Control:** Git

### Data Privacy & Security

- ✅ **All data stays local** on your machine
- ✅ **No external API calls** (except Claude Code itself)
- ✅ **Automatic .gitignore** prevents committing personal data
- ✅ **Automatic backups** to `.backups/` directory
- ✅ **No tracking, no analytics, no telemetry**

### Hooks System (Automated Data Management)

Fluent uses intelligent Claude Code hooks to ensure your data is always safe and validated:

**🔄 PostToolUse Hook** (after every Write/Edit)
- ✅ Creates timestamped backup: `data/file.json.backup-20231117-143022`
- ✅ Validates JSON structure automatically
- ✅ Alerts you immediately if data is malformed

**📦 SessionEnd Hook** (when you finish practicing)
- ✅ Creates daily snapshot in `.backups/YYYYMMDD/`
- ✅ Displays session summary with current streak
- ✅ Shows total practice sessions completed

**🌅 SessionStart Hook** (when you begin)
- ✅ Welcome message with your name and stats
- ✅ Shows current language, level, and streak
- ✅ Alerts you if reviews are due today

**🔒 PreCompact Hook** (before compaction)
- ✅ Safety backup to prevent data loss

**You'll never lose your progress.** All backups are automatic and excluded from git.

See [`.claude/hooks/README.md`](.claude/hooks/README.md) for technical details.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Priority Areas

We're especially interested in:

1. 🌐 **Language-specific optimizations** - Grammar rules, common errors for specific languages
2. 🎵 **Audio features** - Pronunciation practice, listening exercises
3. 📊 **Visual enhancements** - Better progress charts, statistics
4. 📱 **Mobile support** - Companion app or mobile interface
5. ⚡ **Performance** - Optimize data loading, improve speed
6. ♿ **Accessibility** - Make system more accessible
7. 🧪 **Testing** - Add comprehensive test coverage

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## 🙏 Acknowledgments

- **Claude** by Anthropic - For the amazing AI capabilities
- **SuperMemo** - For the SM-2 algorithm
- **Anki** - For inspiring the flashcard approach
- **Language learning research** - Krashen, Bjork, Ebbinghaus, and many others
- **Open-source community** - For making this possible

---

## 📞 Support & Community

- 📖 **Documentation:** [Full docs in this repo](docs/)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/m98/fluent/discussions)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/m98/fluent/issues)
- 📧 **Email:** For sensitive issues

---

## 🌟 Star This Project!

If this system helps you learn a language, please **star the repository** ⭐

It helps others discover this project and motivates us to keep improving it!

---

## 📈 Project Stats

- **Skills:** 12 (8 learner-facing + 4 helper)
- **Hooks:** 5 automated (SessionStart, SessionEnd, PostToolUse, PreCompact, DB helpers)
- **Databases:** 6 JSON tracking files
- **Install paths:** 2 (Claude Code plugin + git clone — both supported)
- **Languages Supported:** All (system is fully language-agnostic)
- **Learning Methods:** 6 evidence-based principles
- **Contributors:** [See contributors](https://github.com/m98/fluent/graphs/contributors)

---

## 🎓 Success Stories

*Want to share your language learning success? Open a PR to add your story here!*

---

## 🛠️ Troubleshooting

**`python3: command not found` when hooks run.**
Install Python 3.8+ and make sure `python3` is on your PATH. On macOS: `brew install python3`. On Debian/Ubuntu: `sudo apt install python3`. On Windows: install via [python.org](https://www.python.org/downloads/) or use WSL.

**Hooks silently do nothing on Windows.**
The PreCompact hook is a Bash script. Run Claude Code from WSL or Git Bash. The Python hooks (SessionStart, SessionEnd, PostToolUse) work on native Windows Python — only PreCompact is Bash-only.

**Learner data is showing up in the wrong place.**
Check the data-dir resolution order (see above). Set `FLUENT_DATA_DIR` explicitly in your shell to force a specific location.

**JSON validation fails after a manual edit.**
The PostToolUse hook exits with status 2 if it finds malformed JSON. The last 10 backups live at `<data_dir>/<filename>.json.backup-<timestamp>`. Restore with: `cp <data_dir>/learner-profile.json.backup-XXXXXX <data_dir>/learner-profile.json`.

**Skills don't appear in the `/` menu after plugin install.**
Restart Claude Code. If still missing, verify install:

```bash
claude plugin list                              # should show fluent@fluent-marketplace enabled
claude plugin validate fluent@fluent-marketplace
```

Or from inside a session: `/plugin list`. If the plugin is disabled, enable it: `claude plugin enable fluent@fluent-marketplace`.

---

## 🔗 Useful Links

- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [SM-2 Algorithm Explained](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)
- [CEFR Levels](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions)
- [Spaced Repetition Research](https://www.gwern.net/Spaced-repetition)
- [Active Recall Benefits](https://en.wikipedia.org/wiki/Testing_effect)

---

## ❓ FAQ

**Q: How is this different from Duolingo/Babbel/etc?**
A: It’s ultra-minimalistic, just a terminal and pure learning. No extra distributions, no ads, no gimmicks. Infinitely adaptable. You ask it to teach you something, and it does. And best of all, everything stays private on your machine.

**Q: Do I need to know how to code?**
A: No! Just install Claude Code and run `/setup`. That's it.

**Q: How long until I see progress?**
A: Most learners see measurable improvement within the first week. The system tracks everything so you can see exactly how you're improving.

**Q: Can I use this for exam preparation?**
A: Yes! The system adapts to your goals. Tell it you're preparing for DELE/DELF/TestDaF/etc. and it'll focus on exam-relevant content.

**Q: Is my data safe?**
A: Absolutely. Everything stays on your machine. No cloud storage, no external servers (except Claude Code itself).

**Q: Can I export my progress?**
A: Yes! All data is in human-readable JSON. You can export, analyze, or migrate it anytime.

**Q: Can I use Open AI's Codex CLI  or Gemini CLI instead of Claude Code?**
A: We have AGENTS.md for instructing other AI CLIs as well, but this kit is specifically optimized for 
Claude Code and its unique capabilities. Using other AI platforms may not yield the same results. 
But feel free to experiment and share your findings!


---

*Start your language learning journey today!* 🚀

```bash
git clone https://github.com/m98/fluent.git
cd fluent
claude
/setup
```
