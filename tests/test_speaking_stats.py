#!/usr/bin/env python3
"""
Focused tests for read-db.py speaking_stats robustness.

Covers current-week bounds, future-date exclusion, null/malformed dates,
fractional/malformed/negative durations, same-day multi-session sums with
streak deduplication, and today/yesterday streak anchoring.

Usage:
    python3 tests/test_speaking_stats.py
"""
import importlib.util
import unittest
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / ".claude" / "hooks" / "read-db.py"

spec = importlib.util.spec_from_file_location("read_db", str(SCRIPT))
read_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(read_db)


class SpeakingStatsTest(unittest.TestCase):
    """Deterministic unit tests for speaking_stats edge cases."""

    def _session(self, date, duration_minutes, skills=("speaking",)):
        return {
            "date": date,
            "duration_minutes": duration_minutes,
            "skills_practiced": list(skills),
        }

    def test_current_week_bounds(self):
        # 2024-01-10 is Wednesday; week is Mon 2024-01-08 through today.
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-08", 10),   # Monday — included
            self._session("2024-01-09", 15),   # Tuesday — included
            self._session("2024-01-10", 20),   # today — included
            self._session("2024-01-07", 30),   # Sunday before week — excluded
            self._session("2024-01-01", 5),    # prior Monday — excluded
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 45)
        self.assertEqual(streak, 4)  # Sun, Mon, Tue, Wed (week bounds only affect minutes)

    def test_future_date_exclusion(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-11", 100),  # tomorrow — excluded
            self._session("2024-01-10", 10),   # today — included
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 10)
        self.assertEqual(streak, 1)

    def test_null_and_malformed_dates(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session(None, 10),
            self._session("not-a-date", 10),
            self._session("20240110", 10),     # wrong format
            {"duration_minutes": 10, "skills_practiced": ["speaking"]},  # missing date
            self._session("2024-01-10", 10),   # valid anchor
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 10)
        self.assertEqual(streak, 1)

    def test_non_string_date_types_do_not_crash(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session(20240110, 10),
            self._session(["2024-01-10"], 10),
            self._session({"date": "2024-01-10"}, 10),
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 0)
        self.assertEqual(streak, 0)

    def test_fractional_malformed_negative_durations(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-10", 10.5),   # fractional -> 10
            self._session("2024-01-10", "abc"),  # malformed -> 0
            self._session("2024-01-10", -5),     # negative -> 0 (must not reduce)
            self._session("2024-01-10", "-10"),  # negative string -> 0
            self._session("2024-01-10", None),   # null -> 0
            self._session("2024-01-10", 15),     # normal -> 15
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 25)
        self.assertEqual(streak, 1)

    def test_non_numeric_duration_types_do_not_crash(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-10", [15]),
            self._session("2024-01-10", {"minutes": 15}),
            self._session("2024-01-10", ""),
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 0)
        self.assertEqual(streak, 1)

    def test_multi_session_same_day_sum_and_streak_dedup(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        yesterday = "2024-01-09"
        today = "2024-01-10"
        sessions = [
            self._session(today, 10),
            self._session(today, 15),
            self._session(yesterday, 20),
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 45)
        self.assertEqual(streak, 2)  # today + yesterday, counted once each

    def test_today_anchors_streak(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-10", 5),
            self._session("2024-01-09", 5),
            self._session("2024-01-08", 5),
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(streak, 3)

    def test_yesterday_anchors_streak_when_no_session_today(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-09", 5),
            self._session("2024-01-08", 5),
            self._session("2024-01-07", 5),  # Sunday before week, still streak-relevant
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(streak, 3)

    def test_streak_zero_when_neither_today_nor_yesterday(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-08", 5),  # two days ago only
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(streak, 0)

    def test_only_non_speaking_sessions_contribute_nothing(self):
        now = datetime(2024, 1, 10, 12, 0, 0)
        sessions = [
            self._session("2024-01-10", 30, skills=("vocabulary",)),
        ]
        minutes, streak = read_db.speaking_stats(sessions, now)
        self.assertEqual(minutes, 0)
        self.assertEqual(streak, 0)


if __name__ == "__main__":
    unittest.main()
