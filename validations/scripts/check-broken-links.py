#!/usr/bin/env python3
"""
Broken Link Checker
===================
Reads docs/dashboard/workflows.js, extracts every file: reference,
and verifies that a matching .prompt.md file exists under platform/.

Matching is done by basename only — the dashboard only stores filenames,
not full paths, so a file named "hsw-dsd-generator.prompt.md" anywhere
under platform/ satisfies a reference to "hsw-dsd-generator.prompt.md".

Exit 1 if any reference cannot be resolved.
"""

import sys
import os
import re
import glob

ROOT         = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKFLOWS_JS = os.path.join(ROOT, "docs", "dashboard", "workflows.js")
PLATFORM     = os.path.join(ROOT, "platform")

# ── Read workflows.js ─────────────────────────────────────────────────────────
with open(WORKFLOWS_JS, encoding="utf-8") as fh:
    js = fh.read()

file_refs: list[str] = re.findall(r'\bfile\s*:\s*["\']([^"\']+)["\']', js)

print(f"Found {len(file_refs)} file reference(s) in workflows.js\n")

# ── Index all prompt files under platform/ ────────────────────────────────────
# basename → list of relative paths (there could theoretically be duplicates)
platform_index: dict[str, list[str]] = {}
for p in glob.glob(os.path.join(PLATFORM, "**", "*.prompt.md"), recursive=True):
    bn = os.path.basename(p)
    platform_index.setdefault(bn, []).append(os.path.relpath(p, ROOT))

# ── Check each reference ──────────────────────────────────────────────────────
ok      = []
missing = []

for ref in file_refs:
    bn = os.path.basename(ref)     # handles both bare filenames and paths
    if bn in platform_index:
        resolved = platform_index[bn][0]
        ok.append((ref, resolved))
        print(f"  ✓  {ref:<55}  →  {resolved}")
    else:
        missing.append(ref)
        print(f"  ✗  {ref}  (not found under platform/)")

# ── Summary ───────────────────────────────────────────────────────────────────
print()

if missing:
    print(f"❌ {len(missing)} broken reference(s) in workflows.js:\n")
    for m in missing:
        print(f"   {m}")
    print(
        "\nFix: either add the missing .prompt.md file to the correct "
        "platform/ sub-directory, or remove the stale entry from workflows.js."
    )
    sys.exit(1)

print(f"✅ All {len(ok)} file references resolved successfully.")
