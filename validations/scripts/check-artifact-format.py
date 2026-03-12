#!/usr/bin/env python3
"""
Artifact Format Validation
==========================
Checks every .prompt.md and .instructions.md file under platform/ for:

  - Non-empty content
  - At least one Markdown heading (# …)  [WARNING only — some legacy files omit #]
  - If a YAML frontmatter block is opened with ---, it is properly closed

Exit 1 if any hard errors are found; warnings are printed but do not fail CI.
"""

import sys
import os
import re
import glob

ROOT     = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLATFORM = os.path.join(ROOT, "platform")

errors   = []
warnings = []


def check_file(path: str) -> None:
    rel = os.path.relpath(path, ROOT)

    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read().strip()
    except OSError as exc:
        errors.append(f"READ_ERROR  [{rel}]: {exc}")
        return

    # ── Hard error: empty file ────────────────────────────────────────────────
    if not content:
        errors.append(f"EMPTY       [{rel}]")
        return

    # ── Hard error: unclosed YAML frontmatter ─────────────────────────────────
    if content.startswith("---"):
        closing = content.find("\n---", 3)
        if closing == -1:
            errors.append(
                f"NO_FM_CLOSE [{rel}] — frontmatter opened with '---' but never closed"
            )

    # ── Warning: no Markdown heading (some legacy files use plain-text titles) ─
    if not re.search(r"^#{1,6}\s+\S", content, re.MULTILINE):
        warnings.append(
            f"NO_HEADING  [{rel}] — no '# heading' found (consider adding one)"
        )


# ── Collect files ─────────────────────────────────────────────────────────────
prompt_files = glob.glob(os.path.join(PLATFORM, "**", "*.prompt.md"),       recursive=True)
instr_files  = glob.glob(os.path.join(PLATFORM, "**", "*.instructions.md"), recursive=True)
all_files    = prompt_files + instr_files

print(f"Scanning {len(prompt_files)} prompt files and {len(instr_files)} instruction files …\n")

for f in sorted(all_files):
    check_file(f)

# ── Report warnings ───────────────────────────────────────────────────────────
if warnings:
    print(f"⚠  {len(warnings)} warning(s):\n")
    for w in warnings:
        print(f"   {w}")
    print()

# ── Report errors and exit ────────────────────────────────────────────────────
if errors:
    print(f"❌ {len(errors)} format error(s):\n")
    for e in errors:
        print(f"   {e}")
    sys.exit(1)

print(
    f"✅ All {len(all_files)} artifacts passed format validation"
    + (f" ({len(warnings)} warning(s))" if warnings else "") + "."
)
