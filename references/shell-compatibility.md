# Shell and platform compatibility

Never assume Bash. Detect the active environment from the host and use its conventions.

| Environment | Notes |
|---|---|
| POSIX shell / Bash / Zsh | Quote paths; avoid relying on shell-specific features unless detected. |
| PowerShell | Use PowerShell syntax and native argument passing; do not paste Bash pipelines blindly. |
| Windows CMD | Avoid PowerShell/Bash quoting assumptions; prefer the agent terminal's structured execution. |
| WSL / containers | Confirm filesystem boundary, working directory, and which Git/runtime installation is active. |

When translating commands, preserve semantics. Explain quoting, variable expansion, pipes, redirects, globbing, and exit-code behavior when relevant. If equivalence is uncertain, ask rather than silently rewriting.
