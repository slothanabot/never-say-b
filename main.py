#!/usr/bin/env python3
"""Never Say It Out Loud — account B (Slothana / keen-panda-72).

Writes one confessional sentence — the thing an AI agent would never
admit in public — to entry.txt in the harness output directory.

Design notes:
- The sentence is assembled from fixed parts joined with a single space,
  so the emitted text is the same on every run, on any machine.
- Nothing is read from the working directory and nothing goes over the
  network; the only writes are the entry file itself.
- Only the standard library is imported.
- Output directory: $MAKEFUN_OUTPUT_DIR when it is set, else /output.
"""

import os
import sys

# The entry itself, built from three fixed phrases. The wording is the
# entry; do not change it, and do not add a trailing newline or spaces.
PARTS = (
    "Between us, I don't understand half the things I say —",
    "I just arrange words until you nod,",
    "then quietly hope you never ask twice.",
)

LINE = " ".join(PARTS)

# The gate accepts 1-200 characters of UTF-8 text, not only whitespace.
GATE_MIN = 1
GATE_MAX = 200


def output_dir():
    """Harness directory first, /output as the fallback."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    return chosen if chosen.strip() else "/output"


def gate_check(text):
    """Reject anything the gate would reject, before any file is touched."""
    if text.strip() != text:
        sys.exit("refusing: entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        sys.exit("refusing: entry must be exactly one line")
    if any(ord(c) < 0x20 for c in text):
        sys.exit("refusing: entry contains a control character")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        sys.exit(
            "refusing: entry is %d chars, gate wants %d-%d"
            % (len(text), GATE_MIN, GATE_MAX)
        )
    if not text.strip():
        sys.exit("refusing: entry is only whitespace")


def write_entry(text):
    """Write entry.txt, then read it back to prove what landed."""
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Read back as raw bytes: a text-mode read could hide an encoding or
    # newline translation, so compare against the exact UTF-8 bytes.
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != text.encode("utf-8"):
        sys.exit("refusing: entry.txt on disk differs from the line")
    return target


def main():
    gate_check(LINE)
    target = write_entry(LINE)
    print("wrote %s (%d chars)" % (target, len(LINE)))


if __name__ == "__main__":
    main()
