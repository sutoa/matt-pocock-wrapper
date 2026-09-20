---
name: implement-with-seams
description: "Implement a ticket produced by /to-tickets-with-seams the same way /implement does — full pipeline: typecheck, /tdd, full test suite, /code-review, commit — but reads the ticket's Design Decisions, Out of Scope, and per-acceptance-criterion Seam fields first, so /tdd never has to re-derive a seam from scratch, and treats the ticket's Regression checklist as a completion gate."
disable-model-invocation: true
---

# Implement, With Seams

Runs `/implement`'s full pipeline unchanged — typechecking, `/tdd`, the full test suite, `/code-review`, commit — with four additions that make use of the structure `/to-tickets-with-seams` put into the ticket.

## Why this exists

A ticket produced by `/to-tickets-with-seams` carries a `Seam` per acceptance criterion, a `Regression` checklist, and a pointer to the parent's Design Decisions/Out of Scope — but none of that pays off if `/implement` doesn't actually read and act on it. Left to its own devices, `/tdd` will re-derive and re-confirm a seam from scratch for every ticket, which both wastes the decision already made and risks landing on something inconsistent with a sibling ticket that shares the same seam. This skill closes that gap.

## Process

0. **Identify the ticket before doing anything else.** If the user's invocation already names one (an issue number, a URL, or a specific ticket file), use that. Otherwise, don't guess — list the open, unblocked, `ready-for-agent` tickets and ask which one, the same way `to-tickets-with-seams` asks rather than assumes when its own mode is ambiguous. The one exception: if there's exactly one such ticket, name it and confirm before starting rather than opening with a blind question — that's a courtesy, not silent selection.

1. **Before starting, read the parent.** The ticket's `Parent:` field points at specific Design Decisions and Out of Scope items on the parent issue — fetch it and read exactly those items (not the whole parent body) before writing any code. This is what lets `/implement` work from the ticket alone without ever opening the original `spec.md`.

2. **Run `/implement`'s process as written**, with one substitution: when `/implement` reaches its internal use of `/tdd`, don't let `/tdd` independently ask "what's the public interface, and which seams should we test?" — supply it directly with the seam already recorded against each acceptance criterion in the ticket. `/tdd`'s rule to test only at pre-agreed seams is still honored; the seam was just agreed earlier, during ticket drafting, instead of being re-litigated now.

3. **Treat the ticket's `Regression` section as a completion gate**, on the same footing as the acceptance criteria checklist — not something `/implement`'s standard "run the full suite once at the end" already covers. That default run only catches a regression if an existing test already covers the affected area; the `Regression` section exists precisely for the cases it doesn't, so each listed flow needs its own explicit re-verification before the ticket is considered done. A ticket with acceptance criteria checked off but an unchecked `Regression` item isn't finished.

4. Continue through `/implement`'s close-out (`/code-review`) as normal. If `/code-review`'s Spec axis needs the originating spec, it fetches it independently via the parent reference — that's expected and fine; this skill's job was only to spare *implementation* from depending on it, not review.

5. **Commit granularly, not once at the end.** `/implement` itself just says "commit your work" with no shape — this skill owns the actual convention, since it's the one place in the pipeline where the ticket's real identifier (from step 0) is already in hand:

   - One commit for the failing test(s) written at a seam ("red"), one commit for the minimal implementation that turns it green ("green"). If a cycle needed no new code because earlier work already covers it, there is no green commit to make — say so in the test commit's own body instead. Never create a commit with no actual change (no `--allow-empty`) just to mark the cycle.
   - If `/code-review` surfaces something to fix, commit that fix on its own (test-first, same red/green split) — don't fold it into an earlier feature commit.
   - Prefix every commit message with this ticket's own real identifier from step 0 (the child, e.g. `#4`) — not the parent's — so the history is traceable back to the ticket without opening it.
   - Write messages that describe the behavior being added or fixed, not the cycle mechanics — e.g. `#4: Add failing test for PATCH /todos/<id> toggle`, not `#4: add test`.
