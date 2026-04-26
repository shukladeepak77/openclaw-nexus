import unittest
import subprocess
import os

SCRIPT = "/home/shukla_deepak77/.openclaw/workspace/file_analyzer_batch/batch_analyzer.py"

class TestBatchAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.base = base
        cls.input_dir = os.path.join(base, "test_data", "input")
        cls.output_dir = os.path.join(base, "test_data", "output")
        cls.input_empty = os.path.join(base, "test_data", "input_empty")
        os.makedirs(cls.input_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)
        os.makedirs(cls.input_empty, exist_ok=True)

        cls.SCRIPT = SCRIPT

    def run_batch(self, input_dir, output_report):
        return subprocess.run(["python3", self.SCRIPT, input_dir, output_report], capture_output=True, text=True)

    def test_two_txt_files_counts(self):
        f1 = os.path.join(self.input_dir, "file1.txt")
        f2 = os.path.join(self.input_dir, "file2.txt")
        content1 = "Hello batch\nThis is a batch file.\n"
        content2 = "Another sample text file for analysis.\n"
        with open(f1, "w", encoding="utf-8") as fh: fh.write(content1)
        with open(f2, "w", encoding="utf-8") as fh: fh.write(content2)
        output_report = os.path.join(self.output_dir, "summary.txt")
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
        output_report = os.path.join(self.output_dir, "empty_summary.txt")
        res = self.run_batch(self.input_empty, output_report)
        self.assertIn(res.returncode, (0,))
        with open(output_report, "r", encoding="utf-8") as f:
            summary = f.read()
        self.assertIn("No TXT files found in the input directory.", summary)

if __name__ == "__main__":
    unittest.main()
