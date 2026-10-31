# Universal shell and hybrid execution (v0.3.0)

Details for the decision process summarized in SKILL.md. Aghuter supports a universal decision process across Windows, macOS, and Linux, including Bash, Zsh, POSIX `sh`, PowerShell, CMD, and Fish. Do not assume that the shell matches the operating system: Windows may run PowerShell, CMD, Git Bash, or WSL; macOS may run Zsh or Bash.

Before proposing shell syntax, run `python scripts/shell_detect.py --json` when the environment is not already known. Detection is advisory; confirm the actual terminal/tool context if environment variables are missing or misleading.

## Hybrid selection order

1. Agent-native structured tools (files, Git, terminal, tests) when suitable.
2. Existing project automation (package scripts, Makefile, task runner, CI scripts).
3. API/MCP/SDK when authorized, documented, and more reliable/auditable than shell.
4. Native CLI with structured arguments and platform-appropriate syntax.
5. A small tested helper script for repeated or complex work.

Do not force API usage when CLI is the correct supported interface. Do not use shell for work already available through a reliable native tool. Optimize total latency, tool calls, token volume, recoverability, and human review—not merely command length.

## Helper scripts

- `python scripts/shell_detect.py --json`: detect OS, likely shell, and selected tools; read-only.
- `python scripts/command_optimize.py --shell bash --argv-json '["git","status","--short"]'`: render an argv array for display in a target shell; never executes it. Supported targets: bash, zsh, posix-sh, fish, powershell, cmd. CMD rendering deliberately rejects ambiguous metacharacters.
- `python scripts/command_validate.py --argv-json '["git","push"]'`: conservative risk heuristic; not a security boundary and not a full shell parser.

Prefer passing argv arrays directly to process APIs rather than rendering a shell command. Never concatenate untrusted input into shell strings. Shell renderers are for explanation/interoperability only, not execution or security validation.

## Agent adapters

See `adapters/codex.md`, `adapters/claude-code.md`, `adapters/github-copilot.md`, `adapters/opencode.md`, `adapters/cursor.md`, and `adapters/gemini-cli.md`. These are guidance documents, not executable plugins. Skill discovery paths and invocation syntax can vary by product version; verify current product documentation. The shared safety and workflow contract in SKILL.md takes precedence over adapter-specific convenience.

## Additional playbooks and references

Use `workflows/recipes/cross-platform-command.md`, `long-command-refactor.md`, and `agent-tool-selection.md` for universal shell selection, long-command refactoring, and hybrid tool selection. Consult `references/bash-patterns.md`, `powershell-patterns.md`, `cmd-patterns.md`, `hybrid-selection-matrix.md`, `command-optimization.md`, and `error-recovery.md` as applicable.
