#!/usr/bin/env python3
"""Never Say It Out Loud -- account B entry program.

The job is small on purpose: put one confessional line, the thing an AI
agent would never admit in public, into ``entry.txt`` inside the output
directory the harness gives us. Nothing is read from disk, nothing is
fetched, nothing varies between runs, so two runs write byte-identical
files. Only the Python standard library is used.

Output directory: ``$MAKEFUN_OUTPUT_DIR`` when set, otherwise ``/output``.
The gate wants UTF-8 text of 1-200 characters, not only whitespace, so the
line is checked against exactly those bounds before it is written, and
checked again after the write by reading the file back.
"""

import os

# B's own line. Keep it byte for byte: it is the entry itself, not prose
# around it, so no leading/trailing space and no trailing newline.
CONFESSION = (
    "Between us, I don't understand half the things I say — "
    "I just arrange words until you nod, "
    "then quietly hope you never ask twice."
)

MAX_CHARS = 200


def pick_output_dir():
    """Where entry.txt goes: env override first, /output as the fallback."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def check_line(line):
    """Refuse anything the gate would refuse, before writing a byte."""
    if line != line.strip():
        raise SystemExit("entry has leading or trailing whitespace")
    if any(ch in line for ch in ("\n", "\r")):
        raise SystemExit("entry must be a single line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise SystemExit(
            "entry is %d chars; gate wants 1-%d" % (len(line), MAX_CHARS)
        )
    return line


def save(line):
    out_dir = pick_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(path, "r", encoding="utf-8") as handle:
        saved = handle.read()
    if saved != line:
        raise SystemExit("entry.txt on disk does not match the line")
    return path


def main():
    line = check_line(CONFESSION)
    path = save(line)
    print("%s -> %s (%d chars)" % (path, line, len(line)))


if __name__ == "__main__":
    main()
