---
name: project-brief
description: Create or update a project's BRIEF.md, a short living file of what the project is for, its numbered goals (G1, G2…), what's planned, and what's out of scope. Always asks the user clarifying questions, and on updates checks the brief against the current code to drop finished or abandoned goals instead of letting the file grow. Use when the user starts a project, says "write down the goals", "what is this project for", "update the brief", "the plan changed", "we're adding X", or when a devlog or goal review notices the goals look stale. Other skills (goal-review, devlog) read BRIEF.md, so use this whenever a project's goals need to be set or refreshed.
---

# Project Brief

`BRIEF.md` sits at the root of a project and answers one question: what is this project trying
to do *right now*? Reviews score against its goals and devlogs check work against it, so it has
to stay accurate and short. A brief that only ever grows becomes a history of old ideas, and
then nobody trusts it.

Run the checker as `python scripts/check_brief.py BRIEF.md` (on Windows, `py` instead of `python`).

## The file

Use `assets/BRIEF-template.md`. Its rules, and why:

- **One screen.** At most ~60 lines and 10 goals. If an update would push it past that, merge
  or remove something first. A brief you can read in a minute gets read.
- **Short, testable goals.** One sentence, about 25 words at most, describing the outcome
  ("Tasks sync between devices without losing edits"), not a feature list. Details live in the
  code. Each goal is marked **★ core** (scored strictly) or **~ just needs to work** (scored on
  whether it reliably does its job). goal-review uses these marks.
- **Goal numbers never change and are never reused.** G4 always means the same goal in old
  reviews, devlogs and commits. When a goal is removed, its number goes on the `Retired:` line.
- **Planned is separate.** Things Oliver wants to add next go under Planned, not Goals, so
  reviews don't score unfinished ideas. A planned item becomes a goal when work on it starts.
- **Out of scope only for ideas that would come back.** Something Oliver was asked about,
  seriously considered, or tried and dropped on purpose. Not every revert or small decision.
- **Empty sections:** Planned and Out of scope say `- none`. Delete Open questions when there
  are none.
- **No changelog.** Each update rewrites the brief to describe the present; git keeps the history.

## Creating a brief

1. Read what exists: README, CLAUDE.md, docs, and the git log (`git log --oneline -40`).
   Draft the purpose, goals and constraints from what you find, with the source of each.
2. Ask Oliver to confirm or correct the draft, and always ask these, even when the answer seems
   obvious, because guesses here distort everything downstream:
   - Which goals are core and which just need to work?
   - Is anything planned next?
   - Is there anything it should deliberately *not* do?
   - Any constraints (free to run, platforms, deadline, course rules)?
   Ask anything else that's genuinely unclear, but keep it to one round of a few questions.
3. Write `BRIEF.md` from the template, run the checker, fix anything it flags, and show Oliver
   the result.

## Updating a brief

Updates are where briefs usually go wrong, by piling on. The job is to make the brief true
again, which usually means removing as much as adding.

1. **Read the brief and what changed.** Its `Updated:` line names a commit, so run
   `git log --oneline <commit>..HEAD` to see recent work. But also check **every** goal, planned
   item and open question against the *current code*, because some may already have been wrong
   when the brief was written. Back each claim with the code, not just a commit message.
2. **Sort every goal**, with evidence:
   - **Still right**: leave it alone.
   - **Done**: it works now. Keep it if it must *stay* working (most features); remove it if it
     was a one-off ("migrate to Supabase").
   - **Clarify**: same goal, better wording (e.g. it now names the case that was fixed). Keep the
     number.
   - **Changed meaning**: if a review of the old goal wouldn't apply to the new wording, it's a
     different goal. Retire the old number and give it a new one.
   - **Abandoned or contradicted**: the code went another way, or nothing has touched it in about
     a month while the rest of the project was active. Always ask; never decide this alone.
3. **Look for work no goal covers.** Most of it needs no entry: bug fixes, polish and small
   features belong under the goal they serve. Only a genuinely new area of the project becomes a
   new goal, or a planned item that has started gets promoted.
4. **Propose, then ask.** Show Oliver a short list (keep / clarify / add / promote / retire, each
   with a one-line reason and evidence) plus your questions. Nothing is removed without a yes.
5. **Rewrite** the brief, update the `Updated:` line, run the checker, and show the new version.

See `references/examples.md` for a full brief and a worked update.
