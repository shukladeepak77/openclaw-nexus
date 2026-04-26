#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def analyze_file(path: str):
    lines = 0
    words = 0
    chars = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            lines += 1
            words += len(line.split())
            chars += len(line)
    return lines, words, chars


def main():
    if len(sys.argv) < 3:
        print("Usage: python batch_analyzer.py <input_dir> <output_report>", file=sys.stderr)
        sys.exit(2)
    input_dir = sys.argv[1]
    output_report = sys.argv[2]

    if not os.path.isdir(input_dir):
        print("Error: input_dir is not a directory", file=sys.stderr)
        sys.exit(3)

    files = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().endswith('.txt') and os.path.isfile(os.path.join(input_dir, f))
    ])

    total_lines = total_words = total_chars = 0
    records = []
    for fname in files:
        fullpath = os.path.join(input_dir, fname)
        l, w, c = analyze_file(fullpath)
        total_lines += l
        total_words += w
        total_chars += c
        records.append((fname, l, w, c))

    with open(output_report, 'w', encoding='utf-8') as out:
        out.write("Batch Analysis Report\n")
        out.write("Generated: " + datetime.now().isoformat() + "\n")
        out.write("Directory: " + input_dir + "\n\n")
        if not records:
            out.write("No TXT files found in the input directory.\n")
        else:
            for fname, l, w, c in records:
                out.write(f"FILE: {fname} | Lines: {l} | Words: {w} | Characters: {c}\n")
            out.write("\nTOTALS\n")
            out.write(f"Files: {len(records)} Lines: {total_lines} Words: {total_words} Characters: {total_chars}\n")

    print("Batch analysis complete.")
    if records:
        print(f"{len(records)} file(s) analyzed. Summary saved to: {output_report}")
    else:
        print("No TXT files found.")

if __name__ == "__main__":
    main()
