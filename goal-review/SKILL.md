---
name: goal-review
description: Step back and review a codebase, branch or PR against the goals it's supposed to achieve. Finds the project's goals and confirms them with the user, gets an independent second reviewer, scores each goal and each quality area 1-10 with evidence, and ends with a prioritized fix list. Use whenever the user asks to review their project or code "properly", asks "does this do what it's supposed to", "how close is this to done", "score my project", "step back and look at this", or wants a review before submitting or shipping, even if they don't mention goals. Not for a quick line-by-line bug hunt on a small diff (that's the built-in /code-review).
---

# Goal Review

A normal code review asks "is this code good?". This one asks "does this code do what it was
meant to do, and how well?". Oliver wants the review to step back from the details, check the
work against the original goals, and get a second opinion, so the scores aren't one reviewer's
blind spots.

## Workflow

### 1. Pin down the scope
Decide what's being reviewed: the whole project, the current branch versus its base, one folder,
or a PR. If the user didn't say, pick the obvious one (a branch with changes → the branch;
otherwise the whole project) and say which you picked.

Run `python scripts/repo_snapshot.py <project-path>` (`py` on Windows) for a map of the project:
languages, biggest files, tests, TODOs, and recent git activity. It skips installed packages,
virtual environments and build output, which can otherwise drown the real code.

### 2. Find the goals, then confirm them
Look for goals in this order: `BRIEF.md` (written by the project-brief skill, goals numbered G1, G2…),
then `README`, `CLAUDE.md`, `docs/`, spec or plan files, assignment specs, and the PR description.

Turn what you find into a numbered list of **testable** goals ("Users can log a workout offline
and it syncs later", not "good UX"). Show the list to the user with where each one came from, and
ask them to confirm, edit or add before you review anything. Goals are the yardstick for the whole
review, so a wrong list makes every score wrong. If you found nothing, ask 2–3 short questions
about what the project is supposed to do.

In the same message, ask which goals are **core** and which **just need to work**. Most of
Oliver's projects are personal tools, and plenty of features only need to do their job reliably;
they don't need polish, full test coverage or every edge case. The bar changes how each goal is
scored (see the rubric) and how much effort the fix list asks for. Also ask whether there are
**planned goals** (things he wants to add next). Those aren't scored; they go in the
"Future potential" section of the report.

### 3. Review it yourself
Read the code that matters for each goal. Run the tests or build if there's an obvious command;
a passing or failing run is strong evidence. Score each goal and each quality area using
`references/rubric.md`. Every score needs evidence: a `file:line`, a test result, or a command's
output. If you can't tell, score it `?` and say what would settle it.

Write your scores down before step 4, so the second reviewer can't sway them.

### 4. Get a second reviewer
If you can start a subagent, give it the prompt in `references/reviewer-prompt.md`, filled in
with the scope and confirmed goals but **none of your scores or opinions**. It reviews
independently and returns its own scores with evidence.

If you can't start a subagent, do a deliberate second pass yourself: re-read the goals, then
look at the code from the angle you skipped the first time (e.g. if you started from the entry
point, now start from the tests and the error handling).

### 5. Confer
Put both sets of scores side by side. Where they differ by 2 or more, look at both reviewers'
evidence and settle on a score. Keep the disagreement in the report, because the gaps between
reviewers are often where the real problems are.

Check every problem the second reviewer found that you didn't before it goes in the report
(open the file, run the command). In the first test run it caught four real issues the lead
missed, and an unchecked finding is just as likely to be wrong as one of yours.

### 6. Report, then offer fixes
Use the format in `references/example-report.md`. End with the prioritized fix list and ask
which ones to make. Don't change any code until the user picks.

## Things to watch for

- **Drift.** Code that does things no goal asks for is either scope creep or a sign the goals are
  out of date. List it separately, and if the goals look stale, suggest updating `BRIEF.md`.
- **Scores must be earned.** A 9 means you'd defend it with evidence. Don't inflate scores to be
  nice, and don't nitpick a goal down for style issues; style belongs in the quality areas.
- **Fixes trace back to scores.** Each fix names the goal or area it improves, so the user can see
  why it's worth doing. Order them by how much they move the project toward its goals, not by how
  easy they are.
- **Match the size of the project.** A personal app doesn't need enterprise security, a
  production test suite or a refactor for the sake of it. For a "just needs to work" goal, only
  suggest a fix when something is actually broken or likely to break; leave polish ideas out.
  Keep the quality areas proportionate the same way: name the risk that matters at this scale.
- **Future potential stays short.** 2–5 bullets: the planned goals the user mentioned, each with a
  concrete first step that fits the existing code, plus at most a couple of opportunities you
  noticed. It's a pointer for later, not a second fix list.
