---
name: handoff
description: Switch between Oliver's devices (laptop, PC, phone) without leaving work stranded. When leaving, scans his project folders for uncommitted or unpushed work, proposes one action per repo for a single yes, pushes, and updates the shared HANDOFF.md. When arriving, pulls everything that can update cleanly and shows where he left off. Use when the user says "I'm switching", "moving to my PC/laptop", "I'm on my phone now", "handoff", "where did I leave off", "sync my stuff", or is about to close a device, even if they don't say "handoff".
---

# Handoff

Oliver works on a laptop, a PC (both Windows, projects under `Source\Repos`, not all projects on
both) and sometimes his phone. Things go missing between them in three ways: work that was never
pushed, repos that only exist on one machine, and context that lives in one machine's memory.
This skill closes all three.

**HANDOFF.md** lives at the root of his skills repo (`custom-claude-skills` on GitHub, cloned
locally as `claude-skills`), so every device reads the same one through git. It holds what he's
focused on, one line per active project, and notes about how he likes to work, so a new session
on any device starts with the same context. Use `assets/HANDOFF-template.md`; keep it under ~50
lines and rewrite it rather than appending.

Run the script from this skill's folder: `python <skill>/scripts/handoff_scan.py [root]`
(`py` on Windows). The root defaults to `~/Source/Repos`.

**The project list** is the `## Projects` section of HANDOFF.md. Each line names the GitHub repo
in brackets (`- **Cadence** (OliL123/Cadence): …`); the script matches it to the local folder by
its remote, so folder names don't matter. Only listed projects get the full check. Any other repo
with unpushed work gets a one-line mention, so nothing is stranded silently; if Oliver says "add it
to my list", add a line for it. To add a new project, add a line, that's all.

## Leaving a device

1. **Scan.** Run the script with `--fetch`. For each listed project it reports uncommitted
   changes, unpushed commits, no upstream, or no remote, and flags changes made in the last 30
   minutes, which may belong to another session that's still working.
2. **Propose one list.** One line per repo with a recommended action, then ask once: "OK to do
   all of these? Or tell me which to change." Recommendations:
   - **Unpushed commits on a clean repo:** push.
   - **Finished-looking changes** (Oliver says so, or the session that made them is this one):
     commit with a clear message, then push.
   - **Mid-work changes**, or anything flagged as recent: leave it, and note it in HANDOFF.md
     ("Cadence: sync fix in progress on LAPTOP, not pushed"). If he wants to continue on the other
     device, offer a `wip/<device>` branch instead: commit there, push, and switch back.
   - **No remote:** ask whether to make a private GitHub repo. Never create one without a yes.
   - **Someone else's repo** (the scan shows a GitHub owner other than `OliL123`): leave it and
     just mention it, unless Oliver says otherwise. Pushing there publishes to another person.

   Never force-push, never commit to `main` work that isn't finished, and never commit files that
   look like secrets, build output or large archives (`.zip`, `.apk`, `.env`).
3. **Do what was approved**, then report what happened, including anything that failed (a
   rejected push, a merge needed).
4. **Update HANDOFF.md**: focus, the project lines (what's where, what's unpushed), the date and
   this device's name. Commit and push it in the skills repo. If the script listed skills that
   changed since they were last saved to the account, add a reminder to re-upload them.

## Arriving on a device

1. **Pull the skills repo first**, then read HANDOFF.md and tell Oliver where he left off in 2–4
   lines: the focus, anything left unpushed on another device, and any skills to re-upload.
2. **Run the script with `--pull`.** It fast-forwards every listed project that's behind and lists
   the ones it couldn't (local changes, diverged history). For those, say what's in the way and ask.
3. **Missing projects:** the script names listed projects this device doesn't have; offer to clone
   them into `Source\Repos`.
4. **First time on a device:** if the skills repo isn't there yet, clone
   `OliL123/custom-claude-skills` into `Source\Repos\claude-skills` first, then carry on.
5. **Open the latest devlog entry** for the project he's about to work on, if it has a `DEVLOG.md`.

## On the phone

- **Claude Code cloud session on one GitHub repo:** git and Python work, so both modes work for
  that one repo; clone the skills repo alongside it to read and update HANDOFF.md.
- **Plain Claude chat:** no git or scripts. If a GitHub connector is available, read HANDOFF.md
  through it; otherwise tell Oliver to open it in the GitHub app. Don't pretend to sync anything.

See `references/examples.md` for a full leaving list and an arrival summary.
