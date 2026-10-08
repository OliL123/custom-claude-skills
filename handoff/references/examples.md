# Examples

## Leaving: the one list

After `handoff_scan.py --fetch` on the laptop:

> Before you switch, here's what would be stranded on LAPTOP and what I'd do:
>
> 1. **claude-skills**: 3 changes from this session (devlog fix, DEVLOG.md, new handoff skill).
>    → Commit "Add handoff skill; fix devlog first-commit range" and push.
> 2. **Cadence**: 11 files changed in the last 30 minutes, probably the sync-fix session.
>    → Leave it; note "sync fix in progress on LAPTOP, not pushed" in HANDOFF.md.
> 3. **NPCRAGSystem**: BRIEF.md is new, plus two `.zip` files.
>    → Commit and push BRIEF.md only; leave the zips (build archives don't belong in git).
> 4. Then update HANDOFF.md and push it.
>
> Also not pushed, not on your list: happybdaydad (owned by eunicela). No action.
>
> OK to do all of these? Or tell me which to change.

One question, one answer. If Oliver says "yes but push Cadence to a wip branch", change just that
line and go.

## Arriving: the summary

After pulling the skills repo and reading HANDOFF.md on the PC:

> You left off on LAPTOP an hour ago. Focus: testing the new skills, then code-tutor.
> Cadence has a sync fix in progress on the laptop that isn't pushed, so don't start on sync here.
> Re-upload `devlog` to your account (it changed since you last saved it).
>
> Pulled: claude-skills (2 commits), NPCRAGSystem (1). Not on this PC: Chronicle; want me to clone it?
