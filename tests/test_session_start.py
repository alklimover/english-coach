#!/usr/bin/env python3
"""Behavioral tests for the zero-command SessionStart interface."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK = REPO_ROOT / ".claude" / "hooks" / "session-start.py"


class SessionStartZeroCommandTest(unittest.TestCase):
    def _run_hook(self, data_dir: Path) -> str:
        env = os.environ.copy()
        env["FLUENT_DATA_DIR"] = str(data_dir)
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input="{}",
            text=True,
            capture_output=True,
            env=env,
            cwd=REPO_ROOT,
            timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    @staticmethod
    def _write_json(path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_first_contact_offers_natural_setup_without_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = self._run_hook(Path(tmp))

        self.assertIn("давайте настроим репетитора", output)
        self.assertNotIn("/fluent-", output)
        self.assertNotIn("/coach-", output)

    def test_current_plan_and_due_reviews_need_only_start_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            self._write_json(
                data / "learner-profile.json",
                {
                    "learner": {
                        "name": "Learner",
                        "target_language": "English",
                        "current_level": "B1",
                        "target_level": "B2",
                    }
                },
            )
            self._write_json(
                data / "spaced-repetition.json",
                {"items": {"due": {"due_date": "2000-01-01"}}},
            )
            self._write_json(data / "session-log.json", {"sessions": []})
            self._write_json(
                data / "weekly-plan.json",
                {
                    "activities": [
                        {
                            "day": datetime.now().strftime("%a").lower()[:3],
                            "type": "write",
                            "format": "weekly_reflection",
                            "topic": "reflect on the week",
                            "status": "planned",
                        }
                    ]
                },
            )

            output = self._run_hook(data)

        self.assertIn("they will be included automatically", output)
        self.assertIn('say "начинаем" to start', output)
        self.assertIn("reflect on the week", output)
        self.assertNotIn("/fluent-", output)
        self.assertNotIn("/coach-", output)


if __name__ == "__main__":
    unittest.main()
