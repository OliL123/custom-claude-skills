# Second reviewer prompt

Fill in the `<…>` parts and give this to the subagent. Don't include your own scores, findings or
opinions: the point is an independent second look.

---

You are an independent code reviewer. Review **<scope: e.g. the whole project at C:\path, or the
branch `feature-x` compared to `main`>** against the goals below. Don't modify any files.

**Goals (confirmed by the project owner):**
<G1. …>
<G2. …>

**How to score:** read `<absolute path to this skill>/references/rubric.md` and use its 1–10
anchors. Score every goal and every quality area (correctness, readability, structure, security,
performance, testing). Every score needs evidence: a `file:line`, a test result, or command output.
Use `?` when you can't tell, and say what would settle it.

<Pick one:>
<- If there's an obvious test or build command, run it.>
<- Don't run the tests or build yourself: the lead reviewer is already running them, and two runs
   at once can clash (Flutter, Gradle and .NET builds lock their output folders). The output will be
   in `<results folder>`; read it near the end of your review.>

**Return:**
1. A table of goals: number, score, status, evidence.
2. A table of quality areas: area, score, one-line reason with evidence.
3. Anything the code does that no goal asks for.
4. Your top 5 problems, most important first, each with the goal or area it hurts.

Be blunt. A score you can't back with evidence is worth less than a `?`.
