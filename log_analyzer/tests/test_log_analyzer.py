import os
import unittest
from log_analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Determine repository root and paths
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.sample_log = os.path.join(base_dir, "sample_log.log")
        if not os.path.exists(cls.sample_log):
            os.makedirs(os.path.dirname(cls.sample_log), exist_ok=True)
            with open(cls.sample_log, "w", encoding="utf-8") as f:
                f.write("2026-04-29 20:00:01 INFO - User login successful\n")
                f.write("2026-04-29 20:00:02 WARNING - Disk space low on /dev/sda1\n")
                f.write("2026-04-29 20:00:03 ERROR - Failed to connect to database\n")
                f.write("2026-04-29 20:00:04 INFO - Data export started\n")
                f.write("2026-04-29 20:00:05 INFO - Data export completed\n")
                f.write("2026-04-29 20:00:06 WARNING - Disk space low on /dev/sda1\n")
                f.write("2026-04-29 20:00:07 ERROR - Failed to connect to database\n")
                f.write("2026-04-29 20:00:08 INFO - User login successful\n")
                f.write("2026-04-29 20:00:09 INFO - User login successful\n")
        cls.report_path = os.path.join(base_dir, "log_report.txt")

    def test_counts(self):
        la = LogAnalyzer(self.sample_log)
        counts = la.counts
        self.assertEqual(counts.get("INFO"), 5)
        self.assertEqual(counts.get("WARNING"), 2)
        self.assertEqual(counts.get("ERROR"), 2)

    def test_top_messages(self):
        la = LogAnalyzer(self.sample_log)
        top = la.top_messages(3)
        expected = [
            ("User login successful", 3),
            ("Disk space low on /dev/sda1", 2),
            ("Failed to connect to database", 2),
        ]
        self.assertEqual(top, expected)

    def test_report_generation(self):
        la = LogAnalyzer(self.sample_log)
        la.generate_report(self.report_path)
        self.assertTrue(os.path.exists(self.report_path))
        with open(self.report_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Counts by level", content)
