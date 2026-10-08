"""Gather what a devlog entry needs: work since the last entry, plus the brief.

Usage: python devlog_context.py [project-path] [--devlog PATH] [--brief PATH]

Finds the last logged commit in DEVLOG.md (a "## date · a..b" or "## month (summary) · a..b"
heading), then prints commits since, changed files, uncommitted changes, the brief's goals and
planned items, and whether a roll-up of old entries is due.
"""
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROLLUP_DAYS = 30
MAX_LINES = 150
NOISE = re.compile(r"^(Deploy |Rebuild |Bump |Merge branch|Update build|chore)", re.I)
META = (".claude/", "BRIEF.md", "DEVLOG.md")  # files the skills themselves write
HEADING = re.compile(r"^## (\d{4}-\d{2}(?:-\d{2})?)(?: \(summary\))? · ([0-9a-f]+)\.\.([0-9a-f]+)", re.M)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout.rstrip() if r.returncode == 0 else ""  # rstrip: status lines start with a space


def commit_exists(root, ref):
    return subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{ref}^{{commit}}"],
                          capture_output=True).returncode == 0


def opt(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def area(path):
    """Files near the top keep their name (lib/sync.dart); deeper ones group by folder."""
    parts = path.split("/")
    return "/".join(parts[:2]) + "/" if len(parts) > 2 else path


def subject(line):
    parts = line.split(" ", 2)
    return parts[2] if len(parts) == 3 else line


def main():
    args = [a for i, a in enumerate(sys.argv[1:], 1)
            if not a.startswith("--") and sys.argv[i - 1] not in ("--devlog", "--brief")]
    root = Path(args[0] if args else ".").resolve()
    if git(root, "rev-parse", "--is-inside-work-tree") != "true":
        sys.exit(f"{root} is not a git repository")
    devlog = Path(opt("--devlog") or root / "DEVLOG.md")
    brief = Path(opt("--brief") or root / "BRIEF.md")
    today = date.today()

    # ---- last entry ----
    heads, lines = [], 0
    if devlog.exists():
        text = devlog.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        heads = HEADING.findall(text)
    dated = [h for h in heads if len(h[0]) == 10]
    last = heads[0] if heads else None

    print(f"# Devlog context for {root.name}\n")
    if last and not commit_exists(root, last[2]):
        print(f"WARNING: last logged commit {last[2]} isn't in this repo (rebased?). Falling back to the last day.\n")
        last = None

    if last:
        rng = f"{last[2]}..HEAD"
        print(f"Last entry: {last[0]}, ended at {last[2]}")
        if last[0] == today.isoformat():
            print(f"The top entry is today's: extend it (new range {last[1]}..HEAD) instead of adding one.")
    else:
        # First entry: only the most recent day that has commits.
        newest_day = git(root, "log", "-1", "--format=%ad", "--date=short")
        first_of_day = git(root, "log", f"--since={newest_day} 00:00", "--reverse", "--format=%h").splitlines()
        base = git(root, "rev-parse", "--short", f"{first_of_day[0]}^") if first_of_day else ""
        if base:
            rng = f"{base}..HEAD"
        else:
            # The day starts at the repo's very first commit, which has no parent: log from it.
            root_commit = git(root, "rev-list", "--max-parents=0", "--abbrev-commit", "HEAD").splitlines()[0]
            rng = f"{root_commit}^!" if root_commit == git(root, "rev-parse", "--short", "HEAD") else f"{root_commit}..HEAD"
        print(f"No previous entry: covering the most recent day of work ({newest_day}).")

    head = git(root, "rev-parse", "--short", "HEAD")
    start = rng.split("..")[0] if ".." in rng else rng.removesuffix("^!")
    print(f"Range for the new entry: {start}..{head}")

    commits = git(root, "log", "--reverse", "--format=%h %ad %s", "--date=short", rng).splitlines()
    real = [c for c in commits if not NOISE.match(subject(c))]
    print(f"\n## Commits ({len(commits)}, of which {len(commits) - len(real)} deploy/rebuild noise)")
    for c in real:
        print(f"- {c}")

    if real:
        files = git(root, "diff", "--name-only", rng) if start else git(root, "show", "--name-only", "--format=", "HEAD")
        areas = Counter(area(f) for f in files.splitlines() if f and not f.startswith("docs/"))
        print("\n## Changed files and folders (files changed)")
        for a, n in sorted(areas.items(), key=lambda kv: (-kv[1], kv[0]))[:15]:
            print(f"- {a} ({n})")

    status = [l for l in git(root, "status", "--short").splitlines()
              if l and not l[3:].strip('"').startswith(META)]
    print(f"\n## Uncommitted changes: {len(status)}")
    for line in status[:10]:
        print(f"  {line}")
    if not real and not status:
        print("\nNOTHING NEW since the last entry: say so and stop.")

    # ---- brief ----
    print("\n## Brief")
    if not brief.exists():
        print("- no BRIEF.md (skip the brief check)")
    else:
        b = brief.read_text(encoding="utf-8")
        upd = re.search(r"^Updated: (\d{4}-\d{2}-\d{2}) at ([0-9a-f]+)", b, re.M)
        if upd:
            n = git(root, "rev-list", "--count", f"{upd.group(2)}..HEAD")
            age = (today - datetime.strptime(upd.group(1), "%Y-%m-%d").date()).days
            stale = (n.isdigit() and int(n) > 30) or age > 30
            print(f"- updated {upd.group(1)} at {upd.group(2)}: {n or '?'} commits and {age} days ago"
                  + ("  <- likely stale" if stale else ""))
        for g in re.findall(r"^- \*\*(G\d+ [★~])\*\* (.*)$", b, re.M):
            print(f"- {g[0]} {g[1]}")
        planned = re.search(r"^## Planned\n(.*?)(?=^## |\Z)", b, re.M | re.S)
        if planned:
            for p in [l for l in planned.group(1).splitlines() if l.startswith("- ") and l != "- none"]:
                print(f"- Planned: {p[2:]}")
        questions = re.search(r"^## Open questions\n(.*?)(?=^## |^Retired:|\Z)", b, re.M | re.S)
        if questions:
            for q in [l for l in questions.group(1).splitlines() if l.startswith("- ")]:
                print(f"- Open question: {q[2:]}")

    # ---- roll-up ----
    old = [h for h in dated if (today - datetime.strptime(h[0], "%Y-%m-%d").date()).days > ROLLUP_DAYS]
    if old or lines > MAX_LINES:
        print(f"\n## Roll-up due: {len(old)} entries older than {ROLLUP_DAYS} days; "
              f"log is {lines} lines (budget {MAX_LINES})")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
