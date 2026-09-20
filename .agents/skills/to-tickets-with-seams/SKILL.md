---
name: to-tickets-with-seams
description: "Break a spec into vertical-slice tickets the same way /to-tickets does, but with what's genuinely per-ticket carried inline (seam classification per acceptance criterion, the AC-specific scenario, regression scope, story points, User Story traceability by number) and a precise tag-based citation — never a restated copy — into whatever lives on the parent past publish (Design Decisions, Testing Decisions tooling, Out of Scope), so /implement-with-seams knows exactly what to read without re-reading all of spec.md. Draft mode writes tickets.md to disk; publish mode creates the parent issue from spec.md and links every child ticket to it."
disable-model-invocation: true
---

# To Tickets, With Seams

Runs `/to-tickets`'s vertical-slicing process, extended so each ticket carries everything an implementer needs from the spec without having to go back and read it. Has two modes.

## Why this exists

`/to-tickets` deliberately keeps "What to build" scoped to user-facing behavior, not implementation detail — which is right, but it means a ticket on its own doesn't say what seam to test at, whether regression coverage matters, or which of the spec's Implementation Decisions, Testing Decisions, and Out of Scope items actually apply to it. The only link back is a loose parent reference, easy to skip in a fresh context. This skill carries what's genuinely per-ticket inline (seam classification, acceptance criteria, regression, the AC-specific scenario) — zero-hop, because getting testing right is the highest-leverage thing to get right — while citing what's shared and lives on the parent past publish (Design Decisions, testing tooling/methodology, Out of Scope) by tag rather than restating it, since restating risks drift the moment the parent's version changes independently of any child ticket.

## Which mode

- No `tickets.md` yet, or the user is asking to break down a spec → **draft mode**.
- The user passes both a `spec.md` and a `tickets.md` (or says "publish the tickets") → **publish mode**.

If it's ambiguous, ask.

## Draft mode

Follow `/to-tickets`'s process for steps 1–2 unchanged (gather context from the spec, explore the codebase, look for prefactoring opportunities). For step 3, draft the vertical slices as usual, but for each ticket also work out:

**Seam per acceptance criterion, not per ticket.** A vertical slice can span both UI and backend, so one ticket-level seam can't represent it. For every acceptance criterion, decide: `UI`, `Backend`, or `Full-stack` (only when an AC genuinely can't be verified without crossing both). This classification is genuinely per-AC and stays inline — no tag needed, nothing shared to duplicate. Do this for every AC before presenting the ticket — a ticket isn't done drafting until every AC has a seam.

**Testing tooling, cited by tag; scenario detail, written out.** The *methodology* behind a seam — "via the Flask test client, not real HTTP," "via Playwright against the rendered page" — is a shared fact from `spec.md`'s Testing Decisions section, tagged there for exactly this reason (see below). Cite its tag rather than restating the methodology in every AC that uses it — the AC-specific *scenario* ("toggling true→false and false→true," "check a box, reload, confirm still checked") is unique to that AC and stays written out in full, since there's nothing shared to duplicate there. So an AC line reads: classification, tagged tooling, spelled-out scenario — e.g. `**Seam:** Backend (`#backend-test-client`) — toggling true→false and false→true`.

**Traceability to the originating User Story, by plain number.** Where an AC derives directly from one of `spec.md`'s numbered User Stories, cite it by that number — `(Story 3)` — not a tag. User Stories are consumed in the same pass that drafts both `spec.md` and `tickets.md`, before either is published, so if a story changes, this ticket gets regenerated in the same sitting — there's no independent-editing window for the reference to go stale in. Some ACs won't map to a single story (an edge case surfaced by Testing Decisions, say, like a 404 check) — say so plainly rather than forcing a mapping that isn't there.

**Regression, when the ticket is cross-layer.** Classify each ticket while drafting: does it touch schema/API only, UI only, or both? A "both" ticket is significant enough that `/implement`'s default "run the full suite at the end" isn't enough — list the specific existing flows that need re-verification before this ticket's dependents can start, as a `## Regression` section. Single-layer tickets get none.

**Design Decisions, cited by tag, not restated.** `to-spec-with-review` tags each Implementation Decision and Out of Scope item with a stable, content-anchored slug (e.g. `` `#patch-endpoint-contract` ``). For each ticket, cite the tags of the items it depends on — `` `#patch-endpoint-contract`, `#fetch-partial-update` `` — and nothing more. Don't restate what those items say: a restated copy drifts the moment the parent's version changes and nobody remembers to update the copy, whereas a bare citation always resolves to whatever the parent currently says. If `spec.md` wasn't produced by `to-spec-with-review` and its Implementation Decisions / Out of Scope items aren't already tagged, tag them now, in `spec.md` itself, before citing them — the citation only works if the source has stable anchors to point at.

**Out of Scope, same treatment.** Cite the tags of whichever Out of Scope items are directly adjacent to this ticket's behavior, so the implementer knows what *not* to build — without restating them either.

**Story points**, Fibonacci scale (1, 2, 3, 5, 8, 13), using this as a starting rubric — refine it with the user once you've calibrated against a few real tickets:

| Points | When |
|---|---|
| 1 | Single layer, 1 AC, existing seam, no regression |
| 2 | Single layer, 2–3 ACs, existing seam, no regression |
| 3 | Single layer with real complexity, or cross-layer with one simple AC, existing seams |
| 5 | Cross-layer, 2–4 ACs, existing seams, no regression required |
| 8 | Cross-layer with several ACs, or regression required, or a new seam being introduced |
| 13 | Cross-layer + regression + several ACs — treat this as a signal to split the ticket further, per `/to-tickets`'s own vertical-slice-sizing rule |

Present the breakdown the same way `/to-tickets` does (step 4: title, blocked-by, what it delivers) — plus seam coverage and story points — and iterate with the user until they approve it.

Write the approved set to `tickets.md` in the current directory, one ticket per entry, using this template:

```
# NN — <Ticket title>

**Before implementing: read the parent ticket's tagged Design Decisions,
Testing Decisions, and Out of Scope items referenced below.**

**What to build:** <end-to-end behavior, user-facing>

- **Blocked by:** <ticket numbers, or "None">
- **Status:** ready-for-agent
- **Story Points:** <Fibonacci: 1, 2, 3, 5, 8, 13> — <which rubric criteria
  drove this number, e.g. "cross-layer, 3 ACs, existing seams, no
  regression">
- **Parent:** <pending — filled in at publish time> — relevant Design
  Decisions: `#tag-one`, `#tag-two`. Relevant Out of Scope: `#tag-three`.

## Acceptance Criteria
- [ ] AC1 (Story 1): <behavior> — **Seam:** Backend (`#tag`) — <scenario detail>
- [ ] AC2 (no direct story — edge case from Testing Decisions): <behavior> — **Seam:** Backend (`#tag`) — <scenario detail>

## Regression  (only when this ticket is cross-layer / significant)
- [ ] <existing flow that must be re-verified before dependents start>

## Notes
<anything from the spec's Further Notes relevant to this ticket, if any>
```

**Do not publish anything.** Tell the user `tickets.md` is ready for review alongside `spec.md`, and that running this skill again in publish mode (passing both files) is the next step once they're happy with the breakdown.

## Publish mode

Takes `spec.md` and `tickets.md` as input. Before doing anything, read `docs/agents/issue-tracker.md` — it defines this repo's actual tracker mechanics (issue type for the parent, how children link to it, any markdown-to-description conversion needed). Don't assume a specific tracker; follow what that file says. If it has no section describing a parent/child feature hierarchy, stop and ask the user to add one (or run `/setup-matt-pocock-skills` first) rather than guessing at tracker-specific API calls.

1. **Create the parent issue** from `spec.md`'s full content as its description/body, per `docs/agents/issue-tracker.md`'s convention for this. Capture its real identifier.
2. **Create each child ticket** from `tickets.md`, in dependency order (blockers first), linking each to the parent using whatever mechanism `docs/agents/issue-tracker.md` specifies. Fill in the ticket's `Parent:` field with the real identifier, replacing the draft-mode placeholder.
3. **Set blocking edges** between children per each ticket's `Blocked by:` field, using the tracker's native dependency mechanism if `docs/agents/issue-tracker.md` describes one, or the documented fallback (a `Blocked by:` line in the body) if not.
4. Confirm back to the user: the parent's link, and each child's link with its blocking edges and story points.

Do not close or modify any pre-existing parent issue that wasn't created by this run.
