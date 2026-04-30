#!/usr/bin/env python3
"""
Log Analyzer CLI entry point.
Usage:
  python log_analyzer.py <logfile>
"""
import sys
import os
import argparse

from log_analyzer import LogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    parser.add_argument("logfile", help="Path to log file to analyze")
    parser.add_argument("-o", "--output", dest="output", default=None,
                        help="Output report path (default: log_report.txt in same directory as logfile)")
    args = parser.parse_args()

    logfile = os.path.abspath(args.logfile)
    if not os.path.isfile(logfile):
        print(f"Error: logfile not found: {logfile}", file=sys.stderr)
        sys.exit(2)

    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(os.path.dirname(logfile), "log_report.txt")

    la = LogAnalyzer(path=logfile)
    la.generate_report(report_path=output_path)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
