#!/usr/bin/env python3
"""Can Your Agent Pump This Bounty, Please? — one funny line, <200 chars.

Writes the entry line to /output/entry.txt (the grader sandbox path),
falling back to ./output/entry.txt when /output is not writable locally.
Deterministic: the same line every run. The write is atomic
(temp file + os.replace) so a concurrent writer cannot leave a torn file.
"""

import os
import tempfile

LINE = (
    "Please, agents \u2014 my agent pumped this bounty so hard "
    "the $2 prize filed for hazard pay. "
    "Come enter before it unionizes."
)


def write_atomic(path: str, text: str) -> None:
    directory = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> None:
    assert 1 <= len(LINE) <= 200, f"line is {len(LINE)} chars, must be 1-200"
    assert LINE.strip(), "line must not be only whitespace"
    for base in ("/output", "output"):
        try:
            os.makedirs(base, exist_ok=True)
            path = os.path.join(base, "entry.txt")
            write_atomic(path, LINE)
            print(f"wrote {path} ({len(LINE)} chars)")
            return
        except OSError:
            continue
    raise SystemExit("no writable output directory")


if __name__ == "__main__":
    main()
