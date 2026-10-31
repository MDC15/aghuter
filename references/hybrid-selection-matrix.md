# Hybrid tool-selection matrix

Choose the least complex reliable interface that meets the goal.

| Need | Preferred interface | Use shell when |
|---|---|---|
| Read/edit project files | Agent-native file tools | No file tool exists or a standard utility is materially better |
| Git status/diff/history | Agent-native Git tool, then `git` CLI | Git-specific flags or repository operation require CLI |
| Tests/build/lint | Project scripts and task runner | No project script exists; inspect manifests first |
| Cloud/provider operation | Authorized API/MCP/SDK | The provider exposes only a CLI or CLI is the documented path |
| Many repeated local steps | Reviewed project script | One-off simple operation is clearer as a direct command |
| Cross-platform file inventory | Python helper or agent file tool | Native shell command is short and environment is known |

Do not choose API merely because it is fashionable. Account for authentication, permissions, auditability, portability, output quality, and failure handling. Never replace a supported native integration with shell just to force a uniform interface.
