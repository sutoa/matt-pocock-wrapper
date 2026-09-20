# Todo: Mark Complete

## Problem Statement

A user viewing their todo list has no way to mark an item as done — every item just sits there, complete or not, with no way to tell.

## Solution

Add a "mark complete" toggle to each todo item: a checkbox in the UI that flips the item's completed state, persisted via a backend endpoint, so the state survives a page reload.

## User Stories

1. As a todo-list user, I want to check a box next to an item, so that it's marked complete.
2. As a todo-list user, I want to uncheck a completed item, so that I can undo a mistaken completion.
3. As a todo-list user, I want the completed state to persist across a page reload, so that my progress isn't lost.
4. As a todo-list user, I want a completed item to be visually distinct (e.g. strikethrough), so that I can scan the list and see what's left at a glance.
5. As a todo-list user, I want an error toggling completion (e.g. network failure) to leave the checkbox showing the last known persisted state, so that the UI never silently lies about whether an item is actually done.

## Implementation Decisions

- `#patch-endpoint-contract` New endpoint: `PATCH /todos/<id>`, body `{"completed": true|false}`, returns the updated todo as JSON.
- `#in-memory-store` The Flask app holds todos in an in-memory list for this dummy feature (no real database) — each todo is `{id, title, completed}`.
- `#fetch-partial-update` The static HTML page renders todos server-side (Jinja) on load, then updates a single item's row via a `fetch()` call to the PATCH endpoint on checkbox toggle — no full-page reload on toggle.
- `#revert-on-failure` On a failed PATCH (non-2xx or network error), the checkbox reverts to its pre-click state and a small inline error message shows next to that row.

## Testing Decisions

- `#backend-test-client` Backend: test `PATCH /todos/<id>` directly against the Flask app (Flask's test client), not over real HTTP — toggling true→false, false→true, and a nonexistent id (404).
- `#ui-playwright` UI: Playwright test against the rendered page — check a box, reload, confirm it's still checked and shows strikethrough; verify a simulated failed PATCH leaves the checkbox showing the prior state and shows the inline error.
- Prior art: none yet — this is the first feature in this repo, so these tests establish the pattern for what follows.

## Out of Scope

- `#no-crud` Creating or deleting todos (this feature only toggles existing ones).
- `#no-auth` Multi-user support or authentication.
- `#no-real-db` A real database — the in-memory list is explicitly temporary and not part of this feature's scope to replace.

## Further Notes

This is a deliberately small dummy feature, used to dry-run the `to-spec-with-review` → `to-tickets-with-seams` → `implement-with-seams` pipeline end to end before relying on it for real work.
