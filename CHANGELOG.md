# Changelog

## 0.3.1
- Added behavioral evidence: pressure-scenario baselines + paired control/treatment wording tests (S4 baseline không thu được sạch do giới hạn môi trường sandbox kế thừa cwd chứa skill — see `tests/pressures/baseline.md`).
- Added "Exact scope of authorization" rule, rationalization table, and red flags to SKILL.md from observed violations.
- Moved universal shell / hybrid execution details to `references/universal-shell.md`; slimmed SKILL.md and compressed duplicated sections.
- Docs aligned with actual layout (bin/, agents/, examples/ added to README); frontmatter description starts with "Use when..."; removed duplicate LICENSE.txt.
- All 25 unit tests, workflow lint, and catalogue validation pass.

## 0.3.0
- Added universal OS/shell detection for Windows, macOS, and Linux.
- Added display-only argv renderers for Bash, Zsh, POSIX sh, Fish, PowerShell, and conservative CMD output.
- Added heuristic command risk assessment with explicit limitations.
- Added hybrid tool-selection guidance (agent-native tools, project automation, API/MCP/SDK, CLI, helper scripts).
- Added cross-platform command, long-command refactor, and tool-selection playbooks.
- Added adapter guidance for Codex, Claude Code, GitHub Copilot, OpenCode, Cursor, and Gemini CLI.
- Added shell-specific references and error-recovery guidance.
- Expanded tests; all 25 tests pass.

## 0.2.0
- Added project inspection, workflow linting, recipes, and safety references.

## 0.1.0
- Initial workflow planner and command explainer.
