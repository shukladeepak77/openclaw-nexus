import os
import sys
import unittest
from pathlib import Path
import subprocess

class TestLogAnalyzerCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Repo root is two levels up from this tests dir
        cls.root = Path(__file__).resolve().parents[2]
        cls.script = cls.root / "log_analyzer.py"
        cls.sample_log = cls.root / "log_analyzer" / "sample_log.log"
        cls.report_path = cls.root / "log_analyzer" / "log_report_cli.txt"

    def test_cli_runs_and_generates_report(self):
        # Explicitly specify output path to avoid ambiguity
        result = subprocess.run([sys.executable, str(self.script), str(self.sample_log), "-o", str(self.report_path)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0, msg=f"CLI exited with code {result.returncode}, stderr: {result.stderr}")
        self.assertTrue(self.report_path.exists())
        with open(self.report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Counts by level", content)
