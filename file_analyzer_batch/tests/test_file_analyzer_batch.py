import unittest
import subprocess
import sys
from pathlib import Path

# Build paths relative to this test file (works both locally and in CI)
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "batch_analyzer.py"

class TestBatchAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use ROOT as the base for all test data
        cls.base = ROOT
        cls.input_dir = cls.base / "test_data" / "input"
        cls.output_dir = cls.base / "test_data" / "output"
        cls.input_empty = cls.base / "test_data" / "input_empty"
        cls.input_dir.mkdir(parents=True, exist_ok=True)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.input_empty.mkdir(parents=True, exist_ok=True)

        cls.SCRIPT = SCRIPT

    def run_batch(self, input_dir, output_report):
        # Ensure both input and output directories exist before running
        Path(input_dir).mkdir(parents=True, exist_ok=True)
        Path(output_report).parent.mkdir(parents=True, exist_ok=True)
        return subprocess.run([sys.executable, str(self.SCRIPT), str(input_dir), str(output_report)], capture_output=True, text=True)

    def test_two_txt_files_counts(self):
        f1 = self.input_dir / "file1.txt"
        f2 = self.input_dir / "file2.txt"
        content1 = "Hello batch\nThis is a batch file.\n"
        content2 = "Another sample text file for analysis.\n"
        f1.write_text(content1, encoding="utf-8")
        f2.write_text(content2, encoding="utf-8")
        output_report = self.output_dir / "summary.txt"
        res = self.run_batch(self.input_dir, output_report)
        self.assertEqual(res.returncode, 0)
        with open(output_report, "r", encoding="utf-8") as f:
            summary = f.read()
        lines1 = len(content1.splitlines())
        words1 = len(content1.split())
        chars1 = len(content1)
        lines2 = len(content2.splitlines())
        words2 = len(content2.split())
        chars2 = len(content2)
        total_lines = lines1 + lines2
        total_words = words1 + words2
        total_chars = chars1 + chars2
        self.assertIn(f"FILE: file1.txt | Lines: {lines1} | Words: {words1} | Characters: {chars1}", summary)
        self.assertIn(f"FILE: file2.txt | Lines: {lines2} | Words: {words2} | Characters: {chars2}", summary)
        self.assertIn("TOTALS", summary)
        self.assertIn(f"Files: 2 Lines: {total_lines} Words: {total_words} Characters: {total_chars}", summary)

    def test_no_txt_files(self):
        output_report = self.output_dir / "empty_summary.txt"
        res = self.run_batch(self.input_empty, output_report)
        self.assertIn(res.returncode, (0,))
        with open(output_report, "r", encoding="utf-8") as f:
            summary = f.read()
        self.assertIn("No TXT files found in the input directory.", summary)

if __name__ == "__main__":
    unittest.main()
