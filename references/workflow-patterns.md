# Workflow patterns

## Naming pattern

Prefer a verb or outcome that a developer can say aloud:

| Name | Intended outcome | Common constituent steps |
|---|---|---|
| `check` | Fast project health check | status, lint, type check, quick tests |
| `test` | Run the relevant test suite | unit or project test command |
| `verify` | Validate before handoff | lint, tests, build, diff review |
| `build` | Produce a local build artifact | project build script |
| `format` | Apply configured formatting | formatter in write mode |
| `review` | Inspect a change set | diff, tests, targeted static checks |
| `release-check` | Prepare a release assessment | version, changelog, tests, build; no publish |

Do not use a generic name such as `go`, `all`, or `do-it` when its effects are unclear. Use a project-specific name when two tasks have materially different outcomes.

## Compose by outcome, not by shell syntax

Bad: one opaque shell expression that nests substitutions, pipes, and conditionals.

Better: a named workflow with explicit steps and observable boundaries:

1. Inspect the working tree.
2. Run lint.
3. Run the focused tests.
4. Run the build if earlier checks pass.
5. Summarize results and changed files.

A workflow is not required to be one OS-specific shell alias. Prefer the project's existing package scripts or task runner.

## Command explanation format

For a command that is unfamiliar or non-trivial, explain:

- **Purpose:** the outcome it produces.
- **Inputs:** files, flags, environment, or service it uses.
- **Effects:** what it can modify or contact.
- **Failure signals:** what a non-zero exit or warning means.
- **Undo/recovery:** only when a practical recovery path is known.

Avoid describing every trivial flag unless asked.

## Examples of human-facing requests

- "Tóm tắt trạng thái repo và những file đã thay đổi."
- "Chạy test cho phần vừa sửa, không chạy toàn bộ nếu không cần."
- "Tạo workflow verify để nhóm dùng trước khi tạo PR."
- "Giải thích tác động của lệnh này trước khi chạy."
- "Tôi chỉ muốn chuẩn bị release, chưa publish hay deploy."

## Keep workflows maintainable

- Reuse official project scripts where possible.
- Keep a task focused on one outcome.
- Avoid duplicating a command in both `package.json` and a second task runner without a reason.
- Document prerequisites and platform limitations.
- Prefer short output and actionable failure messages.
- Version-control project workflows when they are shared team conventions.
