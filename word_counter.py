#!/usr/bin/env python3
import sys

def count_words_in_file(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Simple whitespace-based word count
        words = text.split()
        return len(words)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python word_counter.py <filename>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    count = count_words_in_file(path)
    print(count)

if __name__ == "__main__":
    main()
