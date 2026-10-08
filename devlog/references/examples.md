# Examples

These use an invented project, Flashdeck (a C# flashcard app for Japanese vocab), so they show
the shape without hinting at any real project's log.

## A healthy log

```markdown
# Devlog

## 2026-04-16 · b81d07e..e44c9a0
- **Did:** Existing review history migrated to SM-2 ease factors; old cards no longer all come due at once (G2).
- **Next:** Stroke-order animation for kanji cards (Planned).
- **Stuck on:** Which free stroke-order data has a licence that allows bundling.

## 2026-04-14 · 3f9a2c1..b81d07e
- **Did:** Scheduler switched from fixed intervals to SM-2, with tests for lapsed cards (G2).
  CSV import keeps furigana when a row has an empty example sentence (G1).
- **Why:** Fixed intervals kept showing known words daily; SM-2 spaces them out per card.
- **Next:** Migrate existing review history to SM-2 ease factors (G2).

## 2026-03 (summary) · 9c1e4b7..3f9a2c1
- First working version: CSV import (G1), review sessions (G2), due count and streak (G3).
- Decided: Windows-only WPF instead of cross-platform, because it's only used at the desk.
- Decided: audio is optional per word (G4); class lists only sometimes include it.
- Unresolved: the 7-day streak feels pointless; consider a monthly heatmap instead.
```

Then the brief check. Say the April 16 session had also added a `Kanji/` folder:
"Brief may be stale: stroke order (Planned) has started. Update it with project-brief?"

## A worked roll-up

On May 20 the script reports four April entries older than 30 days. They become:

```markdown
## 2026-04 (summary) · 3f9a2c1..f02b6d8
- Scheduler moved to SM-2 and old history migrated (G2).
- Stroke-order animation shipped for kanji cards (G5), using KanjiVG data (CC BY-SA, credited in About).
- Decided: dropped the 7-day streak for a monthly heatmap (G6), since streaks felt like pressure.
- Unresolved: nothing.
```

What survived the roll-up: what got finished, the decisions with their reasons, and the licence
detail that would be painful to rediscover. What was dropped: the day-by-day order, Next lines
that were later done, and "Stuck on" items that got solved.
