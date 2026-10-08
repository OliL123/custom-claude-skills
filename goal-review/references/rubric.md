# Scoring rubric

Use whole numbers 1–10, or `?` when the evidence isn't there. The anchors below keep scores
consistent between reviews and between the two reviewers.

## Goals: how fully does the code achieve this goal?

| Score | Meaning |
|---|---|
| 1–2 | Not started, or the code works against the goal. |
| 3–4 | A skeleton exists, but the main path is missing or broken. |
| 5–6 | The main path works. Important cases are missing, or nothing proves it works. |
| 7–8 | Works, including the main edge cases. Small gaps, or thin testing. |
| 9–10 | Fully met and verified (tests, or you ran it). Nothing important left to add. |

Status for each goal: **Met** (8+), **Partly met** (5–7), **Not met** (≤4), **Unclear** (`?`).

**Goals that "just need to work".** Score these against a lower bar: if the feature reliably
does its job in normal use, it's an 8, even without tests, polish or rare edge cases. Only score
below that when it's actually broken, unreliable, or likely to lose data. Core goals use the
full scale above.

**Example.** Goal G2: "An NPC answers using only facts from its own lore file."
Score 5, Partly met. `retriever.py:41` filters documents by `npc_id`, so the main path works.
But `prompt_builder.py:88` appends the shared world lore to every prompt, so NPCs can quote facts
they shouldn't know, and no test checks this.

## Quality areas

Score each area across the code in scope. Skip an area only if it truly doesn't apply, and say so.

**Correctness.** Does it do the right thing, including on bad input and edge cases?
3: crashes or wrong results on normal use. 6: normal use is fine, edge cases break.
9: handles edge cases and errors deliberately.

**Readability.** Could a classmate follow it?
3: unclear names, long tangled functions, misleading comments. 6: mostly clear with a few hard spots.
9: names and structure explain the code; comments only where the why isn't obvious.

**Structure.** Are responsibilities split sensibly?
3: one giant file or class does everything, lots of copy-paste. 6: reasonable split with some
leaky boundaries. 9: clear modules, little duplication, easy to change one part alone.

**Security.** Secrets, input handling, permissions.
3: committed secrets or keys, unvalidated input reaching a database or shell. 6: no obvious holes,
but some trust in input. 9: secrets in config or env, input validated at the edges.

**Performance.** Only what matters at this project's scale.
3: something clearly too slow or wasteful for real use. 6: fine for now, with a known bottleneck.
9: no issues at the expected scale. Don't penalize missing optimizations nobody needs.

**Testing.** Would a broken change be caught?
3: no tests, or tests that don't run. 6: the main paths are tested. 9: main paths and the
important edge cases are tested, and the tests pass.

## Language notes

- **C#:** `async void` outside event handlers, missing `using`/`Dispose`, nullable warnings ignored,
  `catch (Exception)` that swallows errors.
- **C++:** ownership (raw `new` without a clear owner, missing virtual destructor in a base class),
  out-of-bounds access, copies of large objects where a `const&` would do.
- **Python:** a checked-in virtual environment, bare `except:`, mutable default arguments,
  no pinned dependencies.
- **Dart/Flutter:** `setState` after `dispose`, business logic inside widgets, Supabase keys or
  service-role keys in client code.
