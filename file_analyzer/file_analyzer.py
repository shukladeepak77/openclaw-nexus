#!/usr/bin/env python3
import sys

def analyze_file(path: str):
    lines = 0
    words = 0
    chars = 0
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                lines += 1
                words += len(line.split())
                chars += len(line)
        return lines, words, chars
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python file_analyzer.py <filename>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    lines, words, chars = analyze_file(path)
    print(f"File: {path}")
    print(f"Lines: {lines}")
    print(f"Words: {words}")
    print(f"Characters: {chars}")

if __name__ == "__main__":
    main()
