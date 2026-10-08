"""Print a quick map of a project for a goal review.

Usage: python repo_snapshot.py [project-path] [--base main]

Shows languages, biggest source files, test files, TODO/FIXME counts, likely goal documents,
and git activity. Skips installed packages, virtual environments and build output, and warns
when those are checked into git (they bloat the repo and hide the real code).
"""
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "site-packages", "bin", "obj", "build",
    "dist", ".dart_tool", ".gradle", ".idea", ".vs", "Pods", "Library", "Temp", "Logs",
    ".pytest_cache", ".mypy_cache", "target",
}
# Checked into git, these are almost always a mistake
JUNK_DIRS = {"node_modules", "venv", ".venv", "__pycache__", "site-packages", "bin", "obj", ".dart_tool"}
GENERATED = (".dart.js", ".min.js", ".g.dart", ".freezed.dart", ".designer.cs", ".g.cs")
GENERATED_LINES = 20000
LANGS = {
    ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".hpp": "C++", ".h": "C/C++ header", ".c": "C",
    ".py": "Python", ".dart": "Dart", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".java": "Java", ".kt": "Kotlin", ".swift": "Swift", ".go": "Go", ".rs": "Rust", ".sql": "SQL",
    ".shader": "Shader", ".hlsl": "Shader", ".lua": "Lua",
}
GOAL_DOCS = ("brief", "readme", "claude.md", "spec", "plan", "requirements", "design", "assignment", "goals")


def git(root, *args):
    try:
        r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def find_git_root(root):
    """The project folder itself, or the first git repo up to two levels inside it."""
    if git(root, "rev-parse", "--is-inside-work-tree") == "true":
        return root
    for depth in ("*/.git", "*/*/.git"):
        found = sorted(root.glob(depth))
        if found:
            return found[0].parent
    return None


def is_test(path):
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    return bool(parts & {"test", "tests", "__tests__", "spec"}) or name.startswith("test_") \
        or name.endswith(("_test.py", "_test.dart", "tests.cs", "test.cs", "_test.cpp", ".test.ts", ".spec.ts"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0] if args else ".").resolve()
    base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None

    langs, lines_by_lang, sizes, tests, docs, generated = Counter(), Counter(), [], [], [], []
    todo = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
                       and not (Path(dirpath) / d / "pyvenv.cfg").exists()]  # any-named virtualenv
        for f in filenames:
            p = Path(dirpath) / f
            rel = p.relative_to(root)
            if any(k in f.lower() for k in GOAL_DOCS) and p.suffix.lower() in (".md", ".txt", ".pdf", ""):
                docs.append(str(rel))
            lang = LANGS.get(p.suffix.lower())
            if not lang:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            n = text.count("\n") + 1
            if f.lower().endswith(GENERATED) or n > GENERATED_LINES:
                generated.append(f"{rel} ({n:,} lines)")
                continue
            langs[lang] += 1
            lines_by_lang[lang] += n
            sizes.append((n, str(rel)))
            todo += text.count("TODO") + text.count("FIXME")
            if is_test(rel):
                tests.append(str(rel))

    print(f"# Snapshot of {root}\n")
    print("## Languages (files / lines)")
    for lang, count in langs.most_common():
        print(f"- {lang}: {count} files / {lines_by_lang[lang]:,} lines")
    if not langs:
        print("- no source files found")

    print("\n## Biggest source files")
    for n, rel in sorted(sizes, reverse=True)[:10]:
        print(f"- {rel} ({n:,} lines)")

    if generated:
        print("\n## Generated or compiled files (not counted above)")
        for g in generated[:10]:
            print(f"- {g}")

    print(f"\n## Tests: {len(tests)} file(s)")
    for t in tests[:15]:
        print(f"- {t}")

    print(f"\n## TODO/FIXME markers: {todo}")

    print("\n## Possible goal documents")
    for d in docs[:20] or ["none found; ask the user what the project should do"]:
        print(f"- {d}")

    repo = find_git_root(root)
    if repo is None:
        print("\n## Git\n- not a git repository")
    else:
        print("\n## Git")
        if repo != root:
            print(f"- repo is in a subfolder: {repo.relative_to(root)}")
        root = repo
        print(f"- branch: {git(root, 'branch', '--show-current') or '(detached)'}")
        print("- recent commits:")
        for line in git(root, "log", "--oneline", "-8").splitlines():
            print(f"    {line}")
        status = git(root, "status", "--short")
        print(f"- uncommitted changes: {len(status.splitlines()) if status else 0} file(s)")
        if base:
            print(f"- changes vs {base}:")
            print("    " + (git(root, "diff", "--stat", f"{base}...HEAD") or "none").replace("\n", "\n    "))
        tracked = git(root, "ls-files").splitlines()
        junk = Counter()
        for t in tracked:
            parts = t.split("/")
            hit = next((d for d in parts[:-1] if d in JUNK_DIRS), None)
            if hit:
                junk[hit] += 1
            elif t.endswith((".pyc", ".dll", ".exe", ".pdb")):
                junk["compiled files"] += 1
        if junk:
            total = sum(junk.values())
            print(f"- WARNING: {total:,} of {len(tracked):,} tracked files look like installed packages or "
                  f"build output: " + ", ".join(f"{k} ({v:,})" for k, v in junk.most_common(5)))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
