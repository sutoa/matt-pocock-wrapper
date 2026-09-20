# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` then keep only `authorAssociation` of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` (drop `OWNER`/`MEMBER`/`COLLABORATOR`).
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `gh issue create --label wayfinder:map`.
- **Child ticket**: an issue linked to the map as a GitHub sub-issue (`gh api` on the sub-issues endpoint). Where sub-issues aren't enabled, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies** — the canonical, UI-visible representation. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _not_ the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate). Where dependencies aren't available, fall back to a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children (`gh issue list --state open`, scoped to the map's sub-issues / task list), drop any with an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in the `Blocked by` line) or an assignee; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me` — the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.

## Feature parent/child hierarchy (for `to-spec-with-review` + `to-tickets-with-seams`)

The **parent** is a single issue holding the full `spec.md` content as its body. **Children**
are the vertical-slice tickets from `tickets.md`, linked to the parent as GitHub native
sub-issues — the same mechanism `/wayfinder` uses above, reused here for feature work.

- **Create the parent**: `gh issue create --title "<feature title>" --body-file spec.md`.
  Capture the returned issue number (parse it from the URL `gh issue create` prints — it does
  **not** support `--json` on create, only on `view`/`list`).
- **Link a child as a sub-issue** (verified working against the sub-issues REST endpoint):
  1. Get the parent's numeric **database id**: `gh api repos/<owner>/<repo>/issues/<parent-number> --jq .id`
  2. Get the child's numeric **database id** the same way, once the child issue is created.
  3. `gh api --method POST repos/<owner>/<repo>/issues/<parent-number>/sub_issues -F sub_issue_id=<child-db-id>`
     — **must use `-F` (typed field), not `-f`**: the endpoint requires `sub_issue_id` as an
     integer, and `-f` sends it as a string, which the API rejects with a 422.
  4. Confirm by re-fetching the parent — `sub_issues_summary.total` increments per linked child.
- **Fallback** if sub-issues are ever unavailable on a repo: a task list in the parent body
  (one checkbox per child) plus `Part of #<parent>` at the top of each child's body.
- **Blocking edges between children** (declared by `/to-tickets`): use the same native issue
  dependencies mechanism described under Wayfinding operations above — `blocked_by` edges via
  `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`.
- **Relevant Design Decisions / Out of Scope pointer**: each child issue's body should
  reference *specific* items from the parent's Design Decisions/Out of Scope sections by name
  or number — not just a bare link to the parent — per the ticket template these skills use.
