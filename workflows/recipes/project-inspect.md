# Inspect a repository before acting

**Workflow ID:** `project.inspect`

1. Read root and nested agent instructions that apply to target files.
2. Identify language, package manager, manifests, lockfiles, and documented scripts.
3. Check Git branch and worktree state; preserve existing edits.
4. Return a concise project map and unknowns. Do not run project scripts during discovery.

## Completion report

- Outcome and scope
- Commands/tools used and why
- Checks: passed / failed / skipped / inconclusive
- Files changed (if any)
- Approval or follow-up required
