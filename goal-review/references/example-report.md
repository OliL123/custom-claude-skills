# Report format

Follow this shape. The example is invented, to show the level of detail; it is not a real review.

---

# Goal review: NPCRAGSystem (whole project)

**Verdict:** The core loop works (an NPC can answer from retrieved lore), but NPCs leak each
other's knowledge and nothing is tested, so 2 of 4 goals are only partly met.

## Goals

| # | Goal | Score | Status | Evidence |
|---|---|---|---|---|
| G1 | Each NPC has its own lore file that's loaded at startup | 8 | Met | `loader.py:12-40` loads `lore/*.md` per NPC; tested by hand, no unit test |
| G2 | An NPC answers using only facts from its own lore | 5 | Partly met | `retriever.py:41` filters by `npc_id`, but `prompt_builder.py:88` adds shared world lore to every prompt |
| G3 | Replies stay in character | ? | Unclear | No evaluation set; needs 10–20 sample questions to judge |
| G4 | A reply takes under 2 seconds | 4 | Not met | Re-embeds all lore on every query (`retriever.py:22`); measured ~6 s |

## Quality

| Area | Score | Why |
|---|---|---|
| Correctness | 6 | Normal questions work; an empty lore file crashes `loader.py:31` |
| Readability | 7 | Clear names; `prompt_builder.py` is one 140-line function |
| Structure | 5 | Retrieval and prompt-building both reach into global config |
| Security | 3 | API key committed in `config.py:4` |
| Performance | 4 | See G4 |
| Testing | 2 | No tests |

## Where the reviewers disagreed

- **G1 (8 vs 6):** the second reviewer docked it for no unit test. Settled on 8, since the rubric
  allows "thin testing" at 7–8 and both reviewers ran it successfully.

## Drift

- A half-built voice output module (`tts/`) that no goal mentions. Either add it as a goal or park it.

## Fix list

1. **Remove the committed API key and rotate it** (`config.py:4`). Raises Security. Effort: S.
2. **Cache embeddings at startup instead of per query** (`retriever.py:22`). Raises G4 and Performance. Effort: S.
3. **Only add world lore the NPC should know** (`prompt_builder.py:88`). Raises G2. Effort: M.
4. **Add a small test set of questions per NPC.** Makes G3 measurable and raises Testing. Effort: M.

## Future potential

- **Planned: NPCs remember the player between sessions.** First step: `NpcMemoryManager` already
  stores per-conversation memory, so persisting it to disk at the end of a session is most of it.
- **Opportunity:** the lore files are plain Markdown, so a small tool to check a lore file for
  contradictions before loading it would be cheap to add.

Which of these should I fix?
