#!/usr/bin/env python3
"""
Dashboard Auto-Sync
===================
Scans platform/ for .prompt.md files that are NOT yet referenced in
docs/dashboard/workflows.js and inserts them into the appropriate
workflow's agents array.

  Safe  — existing entries are never modified or removed.
  Smart — derives step label and display name from filename / frontmatter.

Workflow mapping (path fragment → workflow id):
  vm-bs/hsw        → hsw
  vm-bs/isw/dcom   → dcom
  vm-bs/isw/dsm    → dsm

Files in unmapped paths are reported and skipped.
"""

import sys
import os
import re
import glob

ROOT         = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKFLOWS_JS = os.path.join(ROOT, "docs", "dashboard", "workflows.js")
PLATFORM     = os.path.join(ROOT, "platform")

# path-fragment (using forward-slashes) → workflow id
FRAGMENT_TO_WF: dict[str, str] = {
    "vm-bs/hsw":      "hsw",
    "vm-bs/isw/dcom": "dcom",
    "vm-bs/isw/dsm":  "dsm",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def current_refs(js: str) -> set[str]:
    """Return the set of filenames currently listed as file: values."""
    return set(re.findall(r'\bfile\s*:\s*["\']([^"\']+)["\']', js))


def detect_workflow(filepath: str) -> str | None:
    norm = filepath.replace(os.sep, "/")
    for fragment, wf_id in FRAGMENT_TO_WF.items():
        if fragment in norm:
            return wf_id
    return None


def extract_step(filename: str) -> str | None:
    """
    Derive a step label from the filename's numeric prefix.

    Examples:
      00-build-software.prompt.md        → "00"
      3-ut-0-create-workspace.prompt.md  → "3-0"
      5-create-componenttest.prompt.md   → "5"
      c-code-review-misra.prompt.md      → "★"
      hsw-memory-orchestrator.prompt.md  → "★"
    """
    name = filename.replace(".prompt.md", "")

    # Sub-numbered: "3-ut-0-…" or "4-ut-3-…"
    m = re.match(r"^(\d+)-[a-z]+-(\d+)-", name)
    if m:
        return f"{m.group(1)}-{m.group(2)}"

    # Plain number prefix: "5-create-…" or "00-build-…"
    m = re.match(r"^(\d+)-", name)
    if m:
        return m.group(1)

    # Special non-numbered artifacts
    if any(k in name.lower() for k in ("memory", "orchestrat", "misra", "review-result")):
        return "\u2605"

    return None  # caller assigns sequential index


def extract_name(filepath: str) -> str:
    """
    Return a short display name for the agent.
    Prefers the 'description' field from YAML frontmatter; falls back to
    a title-cased, human-readable derivation of the filename.
    """
    # Try frontmatter description
    try:
        with open(filepath, encoding="utf-8", errors="replace") as fh:
            head = fh.read(2000)
        if head.lstrip().startswith("---"):
            end = head.find("\n---", 3)
            if end != -1:
                fm = head[3:end]
                m = re.search(r"description:\s*['\"](.+?)['\"]", fm)
                if not m:
                    m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
                if m:
                    desc = m.group(1).strip().strip("'\"")
                    # First clause only, max 60 chars
                    desc = re.split(r"[.,;(]", desc)[0].strip()
                    if 5 < len(desc) <= 60:
                        return desc
    except Exception:
        pass

    # Derive from filename
    name = os.path.basename(filepath).replace(".prompt.md", "")
    # Strip leading "3-ut-0-" style prefix
    name = re.sub(r"^\d+-(?:[a-z]+-)*\d+-", "", name)
    # Strip plain leading "5-" prefix
    name = re.sub(r"^\d+-", "", name)
    # Strip domain prefix like "hsw-" or "c-"
    name = re.sub(r"^[a-z]{1,5}-", "", name)
    name = name.replace("-", " ").replace("_", " ")

    # Expand known abbreviations to uppercase
    for abbr, full in [
        ("dsd", "DSD"), ("ut", "UT"), ("swcs", "SWCS"), ("dcom", "DCOM"),
        ("dsm", "DSM"), ("ct", "CT"), ("bat", "BAT"), ("tpa", "TPA"),
        ("hsw", "HSW"), ("asw", "ASW"),
    ]:
        name = re.sub(rf"\b{abbr}\b", full, name, flags=re.IGNORECASE)

    return name.title()


def js_agent_line(filepath: str, step: str) -> str:
    name     = extract_name(filepath)
    filename = os.path.basename(filepath)
    step_s   = step.replace('"', '\\"')
    name_s   = name.replace('"', '\\"')
    return f'      {{ step:"{step_s}", name:"{name_s}", file:"{filename}" }}'


def insert_into_workflow(js: str, wf_id: str, new_lines: list[str]) -> str:
    """
    Append new_lines into the agents:[…] array of workflow wf_id,
    just before the closing ] of that array.
    """
    wf_match = re.search(rf'id\s*:\s*["\']?{re.escape(wf_id)}["\']?', js)
    if not wf_match:
        print(f"  WARNING: workflow id='{wf_id}' not found in workflows.js — skipping.")
        return js

    block_start  = wf_match.start()
    agents_match = re.search(r"agents\s*:\s*\[", js[block_start:])
    if not agents_match:
        print(f"  WARNING: agents array for id='{wf_id}' not found — skipping.")
        return js

    pos   = block_start + agents_match.end()
    depth = 1
    while pos < len(js) and depth:
        if js[pos] == "[":
            depth += 1
        elif js[pos] == "]":
            depth -= 1
        pos += 1
    close_bracket = pos - 1   # index of the closing ]

    insertion = "\n" + ",\n".join(new_lines) + ","
    return js[:close_bracket] + insertion + "\n    " + js[close_bracket:]


# ── Main ──────────────────────────────────────────────────────────────────────

with open(WORKFLOWS_JS, encoding="utf-8") as fh:
    original_js = fh.read()

known = current_refs(original_js)
print(f"workflows.js currently references {len(known)} file(s).\n")

all_prompts = sorted(
    glob.glob(os.path.join(PLATFORM, "**", "*.prompt.md"), recursive=True)
)

# Group new (unknown) files by workflow
new_by_wf: dict[str, list[tuple[str, str]]] = {}   # wf_id → [(filepath, step)]
wf_seq_idx: dict[str, int] = {}                     # for sequential fallback step

for fp in all_prompts:
    fn = os.path.basename(fp)
    if fn in known:
        continue

    wf_id = detect_workflow(fp)
    if wf_id is None:
        print(f"  SKIP (no mapping): {os.path.relpath(fp, ROOT)}")
        continue

    step = extract_step(fn)
    if step is None:
        idx  = wf_seq_idx.get(wf_id, 0) + 1
        step = str(idx)
        wf_seq_idx[wf_id] = idx

    new_by_wf.setdefault(wf_id, []).append((fp, step))
    print(f"  NEW  [{wf_id}]  step={step:>4}  {fn}")

total_new = sum(len(v) for v in new_by_wf.values())

if total_new == 0:
    print("\n✅ workflows.js is already up to date — no new prompt files found.")
    sys.exit(0)

# Apply insertions
updated_js = original_js
for wf_id, entries in new_by_wf.items():
    lines = [js_agent_line(fp, step) for fp, step in entries]
    updated_js = insert_into_workflow(updated_js, wf_id, lines)

with open(WORKFLOWS_JS, "w", encoding="utf-8") as fh:
    fh.write(updated_js)

print(f"\n✅ Added {total_new} new agent(s) to workflows.js.")
