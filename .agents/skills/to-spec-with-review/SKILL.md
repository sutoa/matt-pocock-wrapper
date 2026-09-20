---
name: to-spec-with-review
description: "Draft a spec the same way /to-spec does, but stop before publishing anything to the issue tracker — writes spec.md to disk only, so it can be reviewed together with the ticket breakdown before either goes live."
disable-model-invocation: true
---

# To Spec, With Review

Runs `/to-spec`'s own process, with two differences: it never publishes, and it tags the Implementation Decisions, Testing Decisions, and Out of Scope items so they can be cited precisely later, without duplicating their content.

## Why this exists

Stock `/to-spec` drafts the spec and publishes it to the issue tracker in the same step. That's fine when the spec is the only thing being reviewed — but when tickets are drafted from it afterward (`/to-tickets-with-seams`), a problem discovered while reviewing the *tickets* often means the spec itself needs a tweak. If the spec is already a live tracker issue by then, that tweak means editing something already public instead of a local file. Holding the spec back until both `spec.md` and the resulting `tickets.md` have been reviewed together avoids that entirely — nothing touches the tracker until both are right.

The tagging exists for a related reason: `to-tickets-with-seams` needs to point each ticket at the *specific* Implementation Decisions, Testing Decisions, and Out of Scope items it depends on, not restate them (restating risks drift the moment the source changes) and not just link to the whole section (that dumps a wall of text on the implementer and defeats the point of pointing at anything specific). A stable, content-anchored tag is what makes a precise, drift-proof pointer possible — a positional reference like "item 3" breaks silently the moment an item is inserted or reordered, since everything after it shifts without anyone noticing.

This only matters for content that outlives publishing. These three sections end up living on the **parent tracker issue**, editable independently of any child ticket, weeks after the ticket that cited them was created — that's the actual risk surface a tag protects against. User Stories don't need the same treatment: they're consumed by `to-tickets-with-seams` in the same pass that drafts `spec.md` and `tickets.md` together, before either is published, so if a story changes, the ticket referencing it gets regenerated in the same sitting. A plain number is fine for a reference that's always recomputed alongside its source; a tag is for one that has to survive independent edits after the fact.

## Process

1. Follow `/to-spec`'s process for exploring the codebase and sketching/confirming seams exactly as written — nothing changes there. Use the project's domain vocabulary, respect ADRs in the area being touched, and confirm the proposed seams with the user before writing anything.

2. Write the spec using `/to-spec`'s own template (Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes) to `spec.md` in the current directory. Leave **User Stories** numbered exactly as `/to-spec` already numbers them — no tagging needed there. For the **Implementation Decisions**, **Testing Decisions**, and **Out of Scope** sections, prefix each concrete decision with a short, stable, kebab-case tag that names it — e.g. `` `#patch-endpoint-contract` `` — chosen from its content, not its position, so the tag stays valid no matter how the list around it is edited later:

   ```
   ## Implementation Decisions
   - `#patch-endpoint-contract` New endpoint: `PATCH /todos/<id>`...
   - `#in-memory-store` The Flask app holds todos in an in-memory list...

   ## Testing Decisions
   - `#backend-test-client` Test PATCH /todos/<id> directly against the Flask app (Flask's test client), not over real HTTP.
   - `#ui-playwright` Playwright test against the rendered page.
   ```

   Keep tags short and distinct; if two items would earn the same tag, that's a sign they should probably be merged. A freeform note that isn't itself a concrete decision — "Prior art: none yet, this is the first feature in this repo" — doesn't need a tag; nothing would ever cite it.

3. **Stop here.** Do not create or publish anything to the issue tracker — that's `to-tickets-with-seams`'s job, later, once both documents have been reviewed together.

Tell the user the spec is written and ready to review, and that the next step is `/to-tickets-with-seams` (draft mode) once they're happy with it, or a direct edit to `spec.md` (or another run of this skill) if they want changes first.
