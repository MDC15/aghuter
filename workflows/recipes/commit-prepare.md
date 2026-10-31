# Prepare a focused commit

**Workflow ID:** `commit.prepare`

1. Inspect all tracked and untracked changes.
2. Review diffs and identify only files belonging to the requested change.
3. Show the exact proposed file list and commit message.
4. Stage reviewed paths only, inspect the staged diff, then commit only if authorized. Never infer permission to push.

## Completion report

- Outcome and scope
- Commands/tools used and why
- Checks: passed / failed / skipped / inconclusive
- Files changed (if any)
- Approval or follow-up required
