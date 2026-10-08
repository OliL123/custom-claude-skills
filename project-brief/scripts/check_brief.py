"""Check a BRIEF.md against the project-brief rules.

Usage: python check_brief.py [path/to/BRIEF.md]

Checks: required sections, the Updated line, the size budget (60 lines, 10 goals, ~25-word goals), goal markers,
duplicate goal numbers, and that no retired number is back in use. Prints problems and exits 1
if there are any.
"""
import re
import sys
from pathlib import Path

MAX_LINES = 60
MAX_GOALS = 10
SECTIONS = ["## Goals", "## Planned", "## Out of scope", "## Constraints"]


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "BRIEF.md")
    if not path.exists():
        sys.exit(f"{path} not found")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems = []

    for s in SECTIONS:
        if s not in text:
            problems.append(f"missing section '{s}'")
    if not re.search(r"^Updated: \d{4}-\d{2}-\d{2} at [0-9a-f]{6,}", text, re.M):
        problems.append("missing or malformed 'Updated: YYYY-MM-DD at <commit>' line")
    if "<" in text and ">" in text and re.search(r"<[A-Z][^>]*>", text):
        problems.append("template placeholders like <...> are still in the file")

    content_lines = [l for l in lines if l.strip()]
    if len(content_lines) > MAX_LINES:
        problems.append(f"{len(content_lines)} non-empty lines; the budget is {MAX_LINES}. Merge or remove something.")

    goals = re.findall(r"^- \*\*G(\d+) ([★~])\*\*", text, re.M)
    goal_lines = re.findall(r"^- \*\*G\d+", text, re.M)
    if len(goal_lines) != len(goals):
        problems.append("some goals are missing a ★ (core) or ~ (just needs to work) marker")
    if len(goals) > MAX_GOALS:
        problems.append(f"{len(goals)} goals; the budget is {MAX_GOALS}")
    for line in re.findall(r"^- \*\*G\d+ [★~]\*\*.*$", text, re.M):
        words = len(re.sub(r"^- \*\*G\d+ [★~]\*\*", "", line).split())
        if words > 30:
            gid = re.match(r"- \*\*(G\d+)", line).group(1)  # outside the f-string: Python <3.12 forbids backslashes there
            problems.append(f"{gid} is {words} words; keep goals to one sentence (~25 words)")
    nums = [int(n) for n, _ in goals]
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if dupes:
        problems.append("duplicate goal numbers: " + ", ".join(f"G{n}" for n in dupes))

    retired_line = re.search(r"^Retired:(.*)$", text, re.M)
    if not retired_line:
        problems.append("missing 'Retired:' line (use 'Retired: none')")
    else:
        retired = {int(n) for n in re.findall(r"G(\d+)", retired_line.group(1))}
        reused = sorted(retired & set(nums))
        if reused:
            problems.append("retired numbers are back in use: " + ", ".join(f"G{n}" for n in reused)
                            + ". Give new goals a fresh number.")
        used = set(nums) | retired
        if used:
            gaps = sorted(set(range(1, max(used) + 1)) - used)
            if gaps:
                problems.append("numbers neither in use nor retired: " + ", ".join(f"G{n}" for n in gaps)
                                + ". Add them to Retired.")

    if problems:
        print(f"{path}: {len(problems)} problem(s)")
        for p in problems:
            print(f"- {p}")
        sys.exit(1)
    print(f"{path}: OK ({len(goals)} goals, {len(content_lines)} lines)")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
