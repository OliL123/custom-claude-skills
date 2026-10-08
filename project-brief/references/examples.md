# Examples

Both examples use an invented project, Flashdeck, so they show the shape without hinting at the
answers for any real project.

## A full brief

```markdown
# Flashdeck

A desktop flashcard app for Japanese vocabulary that schedules reviews with spaced repetition,
built because the popular apps can't import the class word lists.

Updated: 2026-03-02 at 9c1e4b7

## Goals
★ = core, scored strictly · ~ = just needs to work

- **G1 ★** Imports the class's weekly vocab CSV without manual cleanup, including furigana and example sentences.
- **G2 ★** Review sessions schedule each card with spaced repetition, so forgotten cards return sooner and known ones later.
- **G3 ~** Shows how many cards are due today and a 7-day streak.
- **G4 ~** Plays the audio for a word when the class list includes it.

## Planned
- Stroke-order animation for kanji cards.

## Out of scope
- Mobile apps: it's for studying at the desk.

## Constraints
- C# / .NET 8, Windows only. Free: no paid APIs.

Retired: none
```

## A worked update

Six weeks later. `git log --oneline 9c1e4b7..HEAD` shows 31 commits: a `Kanji/` folder with
stroke-order SVGs and a player, a rewrite of the scheduler from fixed intervals to SM-2, CSV import
fixes, a dark theme, and a crash fix in audio playback. No commits have touched the streak code
(G3) since early March.

Checking the code, not just the log: the streak counter is still shown, but the 7-day streak was
replaced by a monthly calendar heatmap in a commit *before* 9c1e4b7. The brief was already wrong.

Proposed changes shown to Oliver:

- **Promote** stroke order from Planned to **G5 ~** "Kanji cards animate their stroke order."
  Reason: `Kanji/StrokePlayer.cs` exists and works.
- **Clarify G2** to "…with SM-2 spaced repetition…". Same goal, more precise, so it keeps the number.
- **Retire G3, add G6 ~** "Shows cards due today and a monthly study heatmap." A review of
  "7-day streak" wouldn't apply to a heatmap, so it's a new goal, not a reword.
- **No entry** for the CSV fixes (they serve G1), the dark theme (polish), or the audio crash fix
  (serves G4).
- **Ask:** "Planned is empty now. Anything next?"

After Oliver says yes and "nothing planned", the brief has G1, G2 (clarified), G4, G5, G6,
`Planned: - none`, and `Retired: G3`. It's the same length as before.
