# Cross-platform command workflow

**Goal:** perform one task on the current OS/shell without assuming command syntax.

1. Discover OS, shell, working directory, and tool versions (`python scripts/shell_detect.py --json`).
2. Inspect project instructions and existing scripts before choosing a command.
3. Prefer agent-native tools, then project scripts, then a native CLI, then a small reusable helper.
4. Keep command arguments structured. If displaying shell syntax, render for the detected shell and review quoting.
5. Assess risk with `python scripts/command_validate.py --argv-json '[...]'`; treat the result as a heuristic only.
6. Explain side effects and obtain required approval.
7. Execute through the host agent's approved tool, then verify exit status and result.
