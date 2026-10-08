---
name: devlog
description: Add a short entry to a project's DEVLOG.md at the end of a work session (what got done and which goals it served, why, what's next, what's blocking), built from git rather than memory, and keep the log short by condensing old entries. Also checks the work against BRIEF.md and suggests a brief update when they've drifted apart. Use when the user says "log this", "update the devlog", "wrap up", "end of session", "write down what we did", "where was I?", or is about to stop working on a project, even if they don't say "devlog".
---

# Devlog

`DEVLOG.md` is how Oliver picks a project back up after a break: open it, read the top entry,
know where things stand. That only works if entries are short, accurate and current, so they're
built from what git shows actually happened, and old entries get condensed instead of piling up.

## Workflow

1. **Gather the facts.** Run `scripts/devlog_context.py` from this skill's folder, passing the
   project's path: `python <skill>/scripts/devlog_context.py <project-path>` (`py` on Windows).
   It prints the range to log, the commits and changed files in it, uncommitted changes, the
   brief's goals, planned items and open questions, and whether a roll-up is due. Use the
   conversation too if this session did the work: it knows the *why*, which git doesn't.
   - **First entry ever:** the script covers only the most recent day of work. Don't backfill;
     git has the history. Gaps between entries are normal too; never fill them in.
   - **Nothing new:** if the script says so, tell Oliver and stop.
   - **Top entry is today's:** extend that entry and its range instead of adding a second one.
   - **Several unlogged days:** one entry, dated today, covering the whole range.
2. **Write the entry** at the top of the log (create `DEVLOG.md` with a `# Devlog` heading if
   there isn't one). Shape, at most about 8 lines:

   ```markdown
   ## 2026-04-14 · 3f9a2c1..b81d07e
   - **Did:** Scheduler switched from fixed intervals to SM-2, with tests for lapsed cards (G2).
     CSV import keeps furigana when a row has an empty example sentence (G1).
   - **Why:** Fixed intervals kept showing known words daily; SM-2 spaces them out per card.
   - **Next:** Migrate existing review history to SM-2 ease factors (G2).
   - **Stuck on:** Nothing.
   ```

   - **Did:** the 2–4 outcomes that matter most, one line each, tagged with the goal they served.
     Fixes and hardening go under the goal of the area they touch (a sign-out fix serves the sync
     goal). Work on something that isn't a goal yet is tagged `(Planned)` if it's in the brief's
     Planned list, otherwise `(new)`. Leave out deploys, rebuilds and anything minor; the commit
     messages hold the details.
   - **Why:** only when it isn't obvious from Did. Decisions and their reasons are the most
     valuable part of a devlog, because they're what nobody remembers later.
   - **Next** and **Stuck on:** take them from the conversation. If you don't know, write the entry
     without those lines, show it, and ask Oliver one short question ("What's next, and is anything
     blocking you?"). Add his answer when he replies. Never invent a next step.
3. **Check against the brief.** If `BRIEF.md` exists, compare the work to it:
   - a Planned item has started,
   - a goal now looks done, changed, or contradicted, or an open question was answered,
   - a whole new area of work that no goal covers (not fixes or polish, which belong to a goal),
   - the script marks the brief "likely stale".

   If any apply, end with one line naming them and suggesting a project-brief update, e.g.
   "Brief may be stale: the email digester (Planned) has started. Update it with project-brief?"
   Don't edit the brief yourself; that's project-brief's job, and it asks Oliver first.
4. **Roll up old entries** when the script says one is due. Entries older than 30 days become one
   `## 2026-09 (summary) · <first>..<last>` section per month with at most 5 bullets: what got
   finished, decisions and their reasons, and anything still unresolved. Check each old "Stuck on"
   or "Next" against git before keeping it; most were resolved later. The file should stay under
   about 150 lines.
5. **Show Oliver the new entry** (and the brief note, if any). Don't commit unless he asks.

See `references/examples.md` for a full log and a worked roll-up.
