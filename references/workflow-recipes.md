# Workflow recipes

Recipes describe a repeatable shape of work. They are not universal command sequences. Inspect project instructions and configuration, then adapt each recipe.

## `project.inspect`

Goal: understand a repository before making changes.

1. Locate the project root and read relevant agent/project guidance.
2. Inspect the top-level structure and identify the language, framework, package manager, and build/test scripts.
3. Check the current Git branch and working-tree changes.
4. Summarize the architecture and likely entry points relevant to the user's request.

## `git.review`

Goal: understand the current diff without changing it.

1. Inspect branch and working-tree status.
2. Review changed-file names and diff statistics.
3. Check whitespace/conflict markers.
4. Read relevant diffs in context; distinguish staged, unstaged, and untracked files.
5. Report potential bugs, missing tests, accidental files, and unresolved questions.

## `tests.run`

Goal: run the smallest useful test set for a change.

1. Detect project language, package manager, and test framework from manifests and docs.
2. Inspect available scripts and test layout.
3. Select targeted tests first; run broader tests when useful and feasible.
4. Report exact commands and pass/fail/skip status.
5. Do not claim the entire suite passed when only targeted tests ran.

## `quality.check`

Goal: run the project's relevant static checks.

1. Discover lint, type-check, formatting, and build scripts from project configuration.
2. Run checks relevant to the changed files.
3. Do not install a new tool solely to satisfy a generic checklist without discussing the trade-off.
4. Report skipped checks and why they were skipped.

## `commit.prepare`

Goal: prepare a focused, reviewable commit.

1. Review the full working tree, including untracked files.
2. Group changes by purpose and identify unrelated or sensitive files.
3. Propose the exact files to stage and a concise commit message.
4. Stage only the approved files; do not stage everything by default.
5. Review the staged diff before committing.
6. Commit only when the user's request authorizes the commit; do not push unless separately requested.

## `release.prepare`

Goal: prepare a release without publishing it.

1. Inspect branch, working tree, versioning strategy, changelog, tags, and CI status.
2. Discover the repository's documented build and release steps.
3. Run relevant local verification.
4. Produce a release checklist and identify blockers.
5. Do not tag, publish, push, deploy, or modify remote release state unless the user explicitly authorizes that exact action.

## `dependency.audit`

Goal: understand dependency health before changing dependencies.

1. Identify the package manager and lockfile.
2. Inspect direct dependencies and project policy.
3. Use available audit/report commands only when their behavior and network access are understood.
4. Distinguish advisory findings from confirmed exploitable issues.
5. Do not update or remove packages unless the user requests remediation or approves the proposed changes.
