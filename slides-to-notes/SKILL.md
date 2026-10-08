---
name: slides-to-notes
description: Turn lecture slides (PDF or PPTX) into a notes page in Oliver's handwritten-notes style, with a plain-English summary of the lecture and tap-to-reveal answers to the in-class exercises. Use whenever the user shares lecture slides, a slide deck, or a "Lecture N" PDF and wants notes, a summary, to "digest", "break down", or "understand" the lecture, or asks what's worth writing down, even if they never say "notes". Also use for in-class exercise slides they want explained. Not for writing new presentations or editing a .pptx.
---

# Slides → Notes

Oliver takes handwritten notes on an iPad, one page per lecture. The slides are long and repetitive
(builds, breaks, exercises); his notes keep only what matters, in full sentences. This skill does that for him: it decides
what is worth writing, picks the clearest small example per idea, and lays it out the way he
already writes, as a page he can open next to his notes and copy from.

## Workflow

1. **Extract.** Run `python scripts/extract_slides.py <file>` (add `--json` for machine-readable).
   It prints every slide's text with flags: `FILLER` (title/break/joke, skip), `BUILD` (animation
   step of the previous slide, merge), `EXERCISE` (in-class question), `CODE`, and `VISUAL` (little
   text, so the content is in a picture). Look at `VISUAL` slides as images before deciding they're
   empty, because diagrams often carry the key idea. If the script can't run, read the slides directly.
2. **Find the spine.** Before writing anything, name the 3–6 ideas the lecture is built on and the
   one question it answers (e.g. "how does C++ pick which `talk()` to call?"). Everything on the page
   hangs off this spine; slides that don't serve it go to the skipped line.
3. **Read `references/style.md`** for how Oliver's pages look, with three transcribed examples.
4. **Build the page from `assets/notes-template.html`.** Copy it, keep the CSS and script, and replace
   the content. The template is a finished example (EECS 280 Lecture 10), so follow its structure:
   - `<title>`: `<COURSE> · <Topic>`, e.g. `EECS 280 · Polymorphism`.
   - Set the course color using the comment at the top of the `<style>` (EECS blue, CS HL green,
     Japanese red; for a new course pick one and say which).
   - **The big idea** (`.idea`): 3–5 plain sentences on the question the lecture answers and the
     answer. This is for understanding, not copying.
   - **The sheet**: one `.sec` per highlighted heading, using `.def`, `.arrows`, `.code` rows with
     `.note` labels, `.pair` for side-by-side, tables for contrasts, and the `.misc` sidebar.
   - **Check yourself**: one `.ex` per in-class exercise. Show the question with everything needed
     to attempt it (the code, the answer options, the base class's promises), because Oliver will
     use the page without the slides open. Only the answer and its `.why` go inside `<details>`.
     Work every answer out carefully (trace the code) rather than guessing.
   - **Skipped**: one line saying which slides were left out and why.
5. **Read it as a newcomer.** If you can start a subagent, have it read only the finished page as a
   student who missed the lecture and report what it couldn't follow: terms used before they're
   defined, variables that appear from nowhere, exercises it can't attempt. Fix those, then publish.
   Without subagents, do this pass yourself.
6. **Show it.** In Claude Code, publish the page as an Artifact named after the lecture. In claude.ai,
   output it as an HTML artifact. Either way, Oliver gets a link he can open on his iPad.

## What makes a good page

- **Written in full sentences, like his notes.** Each section opens with a proper 1–3 sentence
  explanation, and the `↳` points are sentences too. The page should teach the lecture to someone
  who missed it, so clarity wins over brevity. Still skip filler, repeats and anything off the spine,
  and move small facts into `MISC DETAILS`.
- **Small, self-contained examples.** Cut slide code down to the lines that show the idea, but keep
  every variable declared so the example makes sense on its own (`Chicken c("Myrtle");` before
  `Bird b = c;`). Make sure it would compile: e.g. class members need `public:`. Put the explanation
  in the `.note` label next to the line that matters.
- **Correct, not just faithful.** Keep the professor's framing, but add a short clarification where a
  slide's one-liner is technically misleading (e.g. "you can't override a non-virtual function"
  needs "redefining it just hides it").
- **Contrast beats description.** When the lecture teaches two things that differ (static vs dynamic,
  upcast vs downcast), put them side by side with the same example or in a small table.
- **Rules as decision trees.** If a slide says "when X, do Y", write it the way Oliver does:
  `question? —yes→ answer`.
- **Keep the professor's exact terms** (they're what shows up on exams), but say them in Oliver's
  short, casual sentences.
- **No markdown syntax on the page.** Emphasis is the `.term` accent color and headings are `h2`
  highlights, never literal `**` or `###`.
