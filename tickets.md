# 01 — Mark todo items complete (toggle, persist, visual state, error handling)

**Before implementing: read the parent ticket's tagged Design Decisions,
Testing Decisions, and Out of Scope items referenced below.**

**What to build:** A checkbox on each todo item that toggles its completed
state, persists across reload, shows a strikethrough when complete, and
reverts with an inline error if the toggle fails to save.

- **Blocked by:** None — can start immediately.
- **Status:** ready-for-agent
- **Story Points:** 8 — cross-layer (backend + UI), 5 ACs, introduces both
  seams for the first time rather than reusing existing ones, no
  regression required (would push toward 13 if it did).
- **Parent:** #3 — relevant Design
  Decisions: `#patch-endpoint-contract`, `#in-memory-store`,
  `#fetch-partial-update`, `#revert-on-failure`. Relevant Out of Scope:
  `#no-crud`, `#no-auth`, `#no-real-db`.

## Acceptance Criteria
- [ ] AC1 (Stories 1, 2): `PATCH /todos/<id>` with `{"completed":
  true|false}` updates the todo's completed field and returns the updated
  todo as JSON, both directions — **Seam:** Backend (`#backend-test-client`)
  — toggling true→false and false→true.
- [ ] AC2 (no direct story — edge case from Testing Decisions): `PATCH
  /todos/<id>` for a nonexistent id returns 404 — **Seam:** Backend
  (`#backend-test-client`) — nonexistent id returns 404.
- [ ] AC3 (Stories 1, 4): Checking the checkbox for a todo marks it
  complete and the row shows a strikethrough — **Seam:** UI
  (`#ui-playwright`) — check the box, confirm strikethrough appears.
- [ ] AC4 (Story 3): The completed state (checkbox + strikethrough)
  persists after a page reload — **Seam:** UI (`#ui-playwright`) — check
  the box, reload, assert state and strikethrough survive.
- [ ] AC5 (Story 5): A failed PATCH (simulated network/server error) leaves
  the checkbox showing its prior state and displays an inline error
  message next to the row — **Seam:** UI (`#ui-playwright`) — intercept the
  network call to force a failure, assert checkbox reverts and error shows.

## Regression
None — this is the first ticket in this repo; there's no pre-existing
behavior to regress against.

## Notes
This is a deliberately small dummy feature, used to dry-run the
`to-spec-with-review` → `to-tickets-with-seams` → `implement-with-seams`
pipeline end to end.
