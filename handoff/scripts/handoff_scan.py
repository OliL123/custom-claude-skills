"""Find work that would be stranded when switching devices, or pull everything on arrival.

Usage:
  python handoff_scan.py [root] [--fetch]   check the listed projects for uncommitted/unpushed work
  python handoff_scan.py [root] --pull      fast-forward every listed project that's behind

The root defaults to ~/Source/Repos; repos up to three folders deep are found (e.g.
NPCRAGSystem/NPCRAGSystem). The project list is the "## Projects" section of HANDOFF.md in the
skills repo: each line names a GitHub repo in brackets, e.g. "- **Cadence** (OliL123/Cadence): ...".
Listed projects get the full check; any other repo only gets a one-line mention if it has work
that isn't pushed. Without a HANDOFF.md, every repo is checked.
"""
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

IGNORE = (".claude/",)          # tool folders, never work
RISKY = re.compile(r"(\.env$|\.zip$|\.apk$|\.exe$|\.pem$|\.key$|secret|credential)", re.I)
RECENT_SECONDS = 30 * 60
SLUG = re.compile(r"github\.com[/:]([^/]+/[^/]+?)(?:\.git)?/?$", re.I)


def git(repo, *args, timeout=60):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, r.stdout.rstrip(), r.stderr.strip()  # rstrip: status lines start with a space
    except subprocess.TimeoutExpired:
        return 1, "", "timed out"


def find_repos(root, depth=3):
    repos = []
    for dirpath, dirnames, _ in os.walk(root):
        level = Path(dirpath).relative_to(root).parts
        if ".git" in dirnames:
            repos.append(Path(dirpath))
            dirnames[:] = []           # don't look inside a repo for more repos
            continue
        if len(level) >= depth:
            dirnames[:] = []
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("node_modules", "bin", "obj", "build")]
    return sorted(repos)


def slug_of(repo):
    _, url, _ = git(repo, "remote", "get-url", "origin")
    m = SLUG.search(url)
    return m.group(1) if m else None


def listed_projects(handoff):
    """(name, owner/repo) pairs from the ## Projects section of HANDOFF.md."""
    text = handoff.read_text(encoding="utf-8")
    section = re.search(r"^## Projects\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        return []
    return re.findall(r"^- \*\*([^*]+)\*\* \(([\w.-]+/[\w.-]+)", section.group(1), re.M)


def status(repo, fetch):
    if fetch:
        git(repo, "fetch", "--quiet", timeout=90)
    _, branch, _ = git(repo, "branch", "--show-current")
    _, remotes, _ = git(repo, "remote")
    slug = slug_of(repo)
    code, upstream, _ = git(repo, "rev-parse", "--abbrev-ref", "@{u}")
    ahead = behind = 0
    if code == 0:
        _, counts, _ = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}")
        if counts:
            ahead, behind = (int(x) for x in counts.split())
    _, st, _ = git(repo, "status", "--porcelain")
    changes = [l for l in st.splitlines() if l and not l[3:].strip('"').startswith(IGNORE)]
    now = time.time()
    recent = []
    for l in changes:
        p = repo / l[3:].strip('"')
        try:
            if p.is_file() and now - p.stat().st_mtime < RECENT_SECONDS:
                recent.append(l[3:])
        except OSError:
            pass
    risky = [l[3:] for l in changes if RISKY.search(l[3:])]
    return {
        "branch": branch or "(detached)", "remote": bool(remotes), "owner": slug.split("/")[0] if slug else None,
        "upstream": upstream if code == 0 else None,
        "ahead": ahead, "behind": behind, "changes": changes, "recent": recent, "risky": risky,
    }


def report(name, s):
    """Print the full check for one repo; return False if it's clean and pushed."""
    issues = []
    if not s["remote"]:
        issues.append("NO REMOTE (only exists on this device)")
    elif not s["upstream"]:
        issues.append(f"branch {s['branch']} has no upstream (never pushed)")
    if s["ahead"]:
        issues.append(f"{s['ahead']} commit(s) not pushed")
    if s["behind"]:
        issues.append(f"{s['behind']} commit(s) behind GitHub")
    if s["changes"]:
        issues.append(f"{len(s['changes'])} uncommitted change(s)")
    if not issues:
        return False
    owner = f", GitHub: {s['owner']}" if s["owner"] else ""
    print(f"## {name} (on {s['branch']}{owner})")
    for i in issues:
        print(f"- {i}")
    for c in s["changes"][:8]:
        print(f"    {c}")
    if len(s["changes"]) > 8:
        print(f"    ... and {len(s['changes']) - 8} more")
    if s["recent"]:
        print(f"- CHANGED IN THE LAST 30 MIN ({len(s['recent'])} files): may be another session's work in progress")
    if s["risky"]:
        print(f"- DON'T COMMIT without asking: {', '.join(s['risky'][:5])}")
    print()
    return True


def pull(name, s):
    if not s["upstream"]:
        print(f"- {name}: no upstream, nothing to pull")
    elif s["behind"] == 0:
        print(f"- {name}: up to date")
    elif s["changes"]:
        print(f"- {name}: {s['behind']} new commit(s) on GitHub, NOT pulled: {len(s['changes'])} local change(s) in the way")
    elif s["ahead"]:
        print(f"- {name}: diverged ({s['ahead']} local, {s['behind']} remote), NOT pulled: needs a merge or rebase")
    else:
        code, _, err = git(REPOS[name], "pull", "--ff-only", "--quiet", timeout=120)
        print(f"- {name}: pulled {s['behind']} commit(s)" if code == 0 else f"- {name}: pull failed: {err[:120]}")


def skills_to_reupload(repo):
    m = re.search(r"^Skills saved to account at: ([0-9a-f]{6,})", (repo / "HANDOFF.md").read_text(encoding="utf-8"), re.M)
    if not m:
        return None
    _, out, _ = git(repo, "diff", "--name-only", f"{m.group(1)}..HEAD")
    _, dirty, _ = git(repo, "status", "--porcelain")
    paths = out.splitlines() + [l[3:] for l in dirty.splitlines()]
    return sorted({p.split("/")[0] for p in paths if "/" in p and (repo / p.split("/")[0] / "SKILL.md").exists()})


REPOS = {}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]).expanduser() if args else Path.home() / "Source" / "Repos"
    if not root.exists():
        root = Path.cwd()
    fetch, do_pull = "--fetch" in sys.argv, "--pull" in sys.argv
    device = os.environ.get("COMPUTERNAME") or socket.gethostname()
    found = find_repos(root)
    skills_repo = next((r for r in found if (r / "HANDOFF.md").exists()), None)

    by_slug = {(slug_of(r) or "").lower(): r for r in found}
    listed, missing = [], []
    if skills_repo:
        for name, slug in listed_projects(skills_repo / "HANDOFF.md"):
            repo = by_slug.get(slug.lower())
            if repo:
                listed.append((name, repo))
            else:
                missing.append((name, slug))
        if skills_repo not in [r for _, r in listed]:
            listed.insert(0, (skills_repo.name, skills_repo))
        print(f"# Handoff on {device}: {len(listed)} listed projects here (from {skills_repo.name}/HANDOFF.md)\n")
    else:
        listed = [(str(r.relative_to(root)), r) for r in found]
        print(f"# Handoff on {device}: no HANDOFF.md found, checking all {len(found)} repos under {root}\n")
    for name, repo in listed:
        REPOS[name] = repo

    if do_pull:
        for name, repo in listed:
            pull(name, status(repo, fetch=True))
    else:
        clean = [name for name, repo in listed if not report(name, status(repo, fetch))]
        if clean:
            print("## Clean and pushed")
            print("- " + ", ".join(clean))

    # Safety net: anything off the list with work that only exists here.
    listed_paths = {r for _, r in listed}
    others = []
    for repo in found:
        if repo in listed_paths:
            continue
        s = status(repo, fetch=False)
        if s["changes"] or s["ahead"] or not s["remote"]:
            owner = f", owned by {s['owner']}" if s["owner"] else ""
            others.append(f"{repo.relative_to(root)}{owner}")
    if others:
        print(f"\nAlso not pushed, not on your list: {'; '.join(others)}")
    if missing:
        print("\nOn your list but not on this device: " + "; ".join(f"{n} ({s})" for n, s in missing))

    if skills_repo:
        changed = skills_to_reupload(skills_repo)
        if changed is None:
            print(f"\n{skills_repo.name}/HANDOFF.md has no 'Skills saved to account at' line.")
        elif changed:
            print(f"\nSkills changed since last saved to the account: {', '.join(changed)}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
