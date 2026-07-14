#!/usr/bin/env python3
"""
Fluent Session Start Hook
Displays welcome message with learner stats and due reviews
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fluent_paths import data_dir, force_utf8_io  # noqa: E402

force_utf8_io()


def main():
    # Read hook input from stdin (optional for SessionStart)
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    data = data_dir()
    profile_path = data / "learner-profile.json"

    if not profile_path.exists():
        print("[Fluent] 🌍 Welcome to Fluent - The AI Language Learning Kit!")
        print('[Fluent] 📝 Say "давайте настроим репетитора" to create your learning profile')
        sys.exit(0)

    try:
        with open(profile_path, 'r') as f:
            profile = json.load(f)

        learner = profile.get("learner", {})
        name = learner.get("name", "Learner")
        target_lang = learner.get("target_language", "your target language")
        current_level = learner.get("current_level", "...")
        target_level = learner.get("target_level", "...")
        streak = profile.get("current_streak_days", 0)

        print(f"[Fluent] 🌍 Welcome back, {name}!")
        print(f"[Fluent] 📚 Learning: {target_lang}")
        print(f"[Fluent] 🎯 Level: {current_level} → {target_level}")
        print(f"[Fluent] 🔥 Streak: {streak} days")

        sr_path = data / "spaced-repetition.json"
        if sr_path.exists():
            try:
                with open(sr_path, 'r') as f:
                    sr_data = json.load(f)

                today = datetime.now().strftime("%Y-%m-%d")
                due_count = 0

                items = sr_data.get("items", {})
                iterable = items.values() if isinstance(items, dict) else items
                for item in iterable:
                    due = item.get("due_date") or item.get("next_review_date", "")
                    if due and due <= today:
                        due_count += 1

                if due_count > 0:
                    print(f"[Fluent] 📅 {due_count} items are due today — they will be included automatically")

            except Exception:
                pass

    except Exception as e:
        print(f"[Fluent] Error loading profile: {e}", file=sys.stderr)

    # english-coach north-star metric: speaking minutes this week + speaking streak.
    # Reuses the single source of truth from read-db.py (hyphenated → importlib).
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "fluent_read_db", Path(__file__).resolve().parent / "read-db.py")
        rdb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rdb)
        log_path = data / "session-log.json"
        if log_path.exists():
            with open(log_path, "r") as f:
                sessions = json.load(f).get("sessions", [])
            mins, sstreak = rdb.speaking_stats(sessions, datetime.now())
            unit = "day" if sstreak == 1 else "days"
            print(f"[Coach] 🗣️  Speaking this week: {mins} min · speaking streak: {sstreak} {unit}")
    except Exception:
        pass

    # english-coach coach layer: show today's planned activity (additive)
    try:
        plan_path = data / "weekly-plan.json"
        if plan_path.exists():
            with open(plan_path, "r") as f:
                plan = json.load(f)
            day = datetime.now().strftime("%a").lower()[:3]
            for a in plan.get("activities", []):
                if a.get("day") == day and a.get("status") == "planned":
                    label = (a.get("scenario") or a.get("topic")
                             or (a.get("source") or {}).get("title")
                             or a.get("about") or "")
                    extra = f" — {label}" if label else ""
                    print(f"[Coach] 📅 Today's plan: {a.get('type')}{extra} — say \"начинаем\" to start")
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
